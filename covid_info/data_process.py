import os, sys
from datetime import datetime
import json, time
import pandas as pd
from rich import print
from rich.progress import track
import requests
from dotenv import load_dotenv

# add current project to sys path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from covid_info.logger import logger

# load env from .env
ENV_CONF = os.path.join(base_dir, ".env")
load_dotenv(ENV_CONF)
DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")
ADDR_TO_LOC_URL = os.getenv("ADDR_TO_LOC_URL")


class DataProcessor:
    def __init__(self, filename: str) -> None:
        self.origin_data = os.path.join(base_dir, f"data/{filename}.xlsx")
        self.all_sheets = self.get_all_sheets_from_xls()

    def get_all_sheets_from_xls(self) -> list:
        """
        args: xls file location.
        return: all sheet names in xls file.
        """
        xls = pd.ExcelFile(self.origin_data)
        return xls.sheet_names

    def trans_xls_to_csv(self, num: int = None):
        """
        use pandas read xls, transfer to csv file.
        """
        if num is not None:
            sheets = self.all_sheets[num : num + 1]
        else:
            sheets = self.all_sheets
        for i_name in sheets:
            print(f"transitioning {i_name}..")
            df = pd.read_excel(self.origin_data, sheet_name=i_name)
            last_col = list(df.columns)[-1]

            df[last_col] = df[last_col].astype("string")
            df = df.replace("\n", " ", regex=True)
            df = df.replace(r"\s+", " ", regex=True)
            df = df.fillna(method="pad")

            output_path = os.path.join(base_dir, f"data/{i_name}.csv")
            df.to_csv(output_path, index=None, header=None)

    def trans_csv_to_json(self, num: int = None):
        """
        use pandas read csv file, output to json.
        """
        if num is not None:
            sheets = self.all_sheets[num : num + 1]
        else:
            sheets = self.all_sheets
        for i_name in sheets:
            logger.info(f"transitioning {i_name} csv to json ...")
            df = pd.read_csv(os.path.join(base_dir, f"data/{i_name}.csv"))
            result = df.to_json(force_ascii=False, orient="records")
            parsed_list = json.loads(result)
            output_path = os.path.join(base_dir, f"data/{i_name}.json")
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dict = {"title": i_name, "updated_date": today, "all_data": parsed_list}
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(dict, f, ensure_ascii=False, indent=4)
            logger.info(f"{i_name} json file export success !")

    def update_loc_info_from_json(self, num=None):
        """
        use pandas read csv file, add new loc col by tencent geocoder tool.
        """
        if num is not None:
            sheets = self.all_sheets[num : num + 1]
        else:
            sheets = self.all_sheets
        for i_name in sheets:
            json_data_path = os.path.join(base_dir, f"data/{i_name}.json")
            with open(json_data_path, "r") as f:
                json_data = json.load(f)
            count = 0
            for i in track(json_data["all_data"]):
                i_addr_name = i.get("采样点地址")
                res_location = i.get("location", None)
                if res_location is not None:
                    continue
                res_location = self.bd_addr_to_loc(addr=i_addr_name)
                i["location"] = res_location
                time.sleep(0.5)
                count += 1
                # backup when transition every 100 data
                if count % 100 == 0:
                    output_json_data_path = os.path.join(
                        base_dir, f"data/{i_name}_update.json"
                    )
                    with open(output_json_data_path, "w") as f:
                        json.dump(json_data, f, ensure_ascii=False, indent=4)
                    time.sleep(5)
            output_json_data_path = os.path.join(base_dir, f"data/{i_name}_update.json")
            with open(output_json_data_path, "w") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)

    @classmethod
    def bd_addr_to_loc(cls, addr):
        """通过地址获取经纬度"""
        url = ADDR_TO_LOC_URL + f"address={addr}&output=json&ak={DEVELOPER_KEY}"
        res = requests.get(url)
        answer = res.json()
        try:
            location = answer.get("result").get("location")
            return location
        except Exception as e:
            logger.info("get location failed")
            print(f"request addr : {addr}")
            print(f"return : {answer}")
            raise e


if __name__ == "__main__":
    p = DataProcessor(filename="Inoculation_point")
    print(p.all_sheets[0])
    p.trans_xls_to_csv(num=0)
    # p.trans_csv_to_json()
    # p.update_loc_info_from_json(2)
    # p.bd_addr_to_loc(addr="大连市庄河市伟业城市绿洲小区5#-7#楼西社区会议室门前")
