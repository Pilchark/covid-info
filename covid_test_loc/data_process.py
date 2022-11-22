from datetime import datetime
import json,time
import pandas as pd
from rich import print
import os,sys
import requests
from dotenv import load_dotenv

# add current project to sys path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from covid_test_loc.logger import logger

# load env from .env
ENV_CONF = os.path.join(base_dir, '.env')
load_dotenv(ENV_CONF)
DEVELOPER_KEY = os.getenv('DEVELOPER_KEY')
ADDR_TO_LOC_URL = os.getenv('ADDR_TO_LOC_URL')


class DataProcessor:
    def __init__(self) -> None:
        self.origin_data = os.path.join(base_dir, "data/data.xlsx")
        self.all_sheets = self.get_all_sheets_from_xls()

    def get_all_sheets_from_xls(self) -> list:
        """
        args: xls file location.
        return: all sheet names in xls file.
        """
        xls = pd.ExcelFile(self.origin_data)
        return xls.sheet_names

    def trans_xls_to_csv(self):
        for i_name in self.all_sheets:
            print(f"transitioning {i_name}..")
            df = pd.read_excel(self.origin_data, sheet_name=i_name)
            last_col = list(df.columns)[-1]

            df[last_col] = df[last_col].astype("string")
            df = df.replace("\n"," ",regex=True)

            output_path = os.path.join(base_dir, f"data/{i_name}.csv")
            df.to_csv(output_path, index=None, header=None)

    def trans_csv_to_json(self, num=None):
        """
        use pandas read csv file, output to json 
        """
        if num is not None:
            sheets = self.all_sheets[num:num+1]
        for i_name in sheets:
            logger.info(f"transitioning {i_name} csv to json ...")
            df = pd.read_csv(os.path.join(base_dir, f"data/{i_name}.csv"))
            result = df.to_json(force_ascii=False, orient="records")
            parsed_list = json.loads(result)
            output_path = os.path.join(base_dir, f"data/{i_name}.json")
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dict = {
                "title" : i_name,
                "updated_date" : today,
                "all_data": parsed_list
            }
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(dict, f, ensure_ascii=False, indent=4)
            logger.info(f"{i_name} json file export success !")

    def update_loc_info_from_json(self,num=None):
        """
        use pandas read csv file, add new loc col by tencent geocoder tool.
        """
        if num is not None:
            sheets = self.all_sheets[num:num+1]
        for i_name in sheets:
            json_data_path = os.path.join(base_dir, f"data/{i_name}.json")
            with open(json_data_path, "r") as f:
                json_data = json.load(f)
            for i in json_data["all_data"]:
                i_addr_name = i.get("采样点地址")
                parameters = {'address': i_addr_name, 'key': DEVELOPER_KEY}
                response = requests.get(ADDR_TO_LOC_URL, parameters)
                answer = response.json()
                res_location = answer.get("result").get("location")
                print(res_location)
                i["location"] = res_location
                time.sleep(0.3)

            output_json_data_path = os.path.join(base_dir, f"data/{i_name}_update.json")
            with open(output_json_data_path, "w") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)

    def address_coordinate_post_request(address):
        """通过地址获取经纬度
        """
        parameters = {'address': address, 'key': DEVELOPER_KEY}
        response = requests.get(ADDR_TO_LOC_URL, parameters)
        answer = response.json()
        return answer


if __name__ == "__main__":
    p = DataProcessor()
    # p.trans_xls_to_csv()
    # p.trans_csv_to_json(2)
    p.update_loc_info_from_json(2)

