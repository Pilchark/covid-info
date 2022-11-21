import json
import os,sys
from flask import Flask, request, render_template, url_for, redirect
from rich import print
from pyecharts.charts import Bar
from pyecharts import options as opts
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from covid_test_loc.data_process import DataProcessor

ENV_CONF = os.path.join(base_dir, '.env')
load_dotenv(ENV_CONF)
DEVELOPER_KEY = os.getenv('DEVELOPER_KEY')

app = Flask(__name__)


def get_api_locs():
    p = DataProcessor()
    table_name = p.all_sheets[0]
    json_data_path = os.path.join(base_dir, f"data/{table_name}.json")
    with open(json_data_path,"r") as f:
        res = json.load(f)
    res_list = []
    for i in res.get("all_data"):
        lat = i.get("location").get("lat")
        lng = i.get("location").get("lng")
        res_list.append((lat,lng))
    return table_name,res_list

# urls 

# index
@app.route("/", methods=["POST", "GET"])
def index():
    # V1 版本开始支持链式调用
    # 你所看到的格式其实是 `black` 格式化以后的效果
    # 可以执行 `pip install black` 下载使用
    bar = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
        # 或者直接使用字典参数
        # .set_global_opts(title_opts={"text": "主标题", "subtext": "副标题"})
    )

    bar.render(os.path.join(base_dir, "covid_test_loc/templates/mycharts.html"))
    return render_template("mycharts.html", key = DEVELOPER_KEY)

@app.route("/map", methods=["GET"])
def map():
    table_name, res_list = get_api_locs()
    return render_template("covid_map.html", key = DEVELOPER_KEY, locs = res_list,title=table_name)

@app.route("/api/locs", methods=["GET"])
def api_locs():
    res_list = get_api_locs()
    for i in res_list:
        print(f"lat = {i[0]},lng={i[1]}")
    return "OK"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
