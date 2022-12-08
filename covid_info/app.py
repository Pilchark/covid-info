import json
import os, sys
from flask import Flask, render_template

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

DEBUG_MODE = os.getenv("FLASK_DEBUG")
if DEBUG_MODE is None:
    # load env file
    from dotenv import load_dotenv

    ENV_CONF = os.path.join(base_dir, ".env")
    load_dotenv(ENV_CONF)
    DEBUG_MODE = True
elif int(DEBUG_MODE) == 1:
    # development mode
    DEBUG_MODE = True
else:
    # deploy
    DEBUG_MODE = False

WEB_KEY = os.getenv("WEB_KEY")
app = Flask(__name__)


def get_api_locs(table_name: str):
    """
    args: default=0, elect different maps.
    """
    json_data_path = os.path.join(base_dir, f"data/{table_name}.json")
    with open(json_data_path, "r") as f:
        res = json.load(f)
    res_list = []
    for i in res.get("all_data"):
        index = i.get("序号")
        lng = i.get("location").get("lng")
        lat = i.get("location").get("lat")
        name = i.get("采样点名称")
        addr = i.get("采样点地址")
        open_time = i.get("开放时间")
        tel = i.get("联系电话")
        res_list.append((index, lng, lat, name, addr, open_time, tel))
    return table_name, res_list


# urls


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html", title="首页")


@app.route("/map/<name>", methods=["GET"])
def map(name):
    table_name, res_list = get_api_locs(name)
    return render_template("map.html", key=WEB_KEY, locs=res_list, title=table_name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=DEBUG_MODE)
