# COVID-info : 疫情相关地图可视化

## 功能

### 地图页面

1. 重点人群采样点
2. 医疗卫生机构及公共场所
3. 愿检尽检
4. 各区市县新冠疫苗接种点信息

## TODO

1. 使用 pandas 解析 xls 文件，导出为 csv 文件。
2. 解析 csv 文件，导出为 json 文件。
3. 使用地址解析 api 更新经纬坐标到 json 文件。
4. flask 将后端数据传递前端， 使用 jinja 渲染前端页面。
3. 使用 BaiduMap JavaScript API 添加标注。
4. [ ] 将 2 组 locations 渲染到地图
5. [ ] 将两组标识为不同颜色
6. [ ] 点击显示详细信息：检测点名称，电话等。
7. [ ] github pages 渲染静态页面
<https://gitee.com/help/articles/4136#article-header4>

## 参考 API 手册

- [API 拾取系统](http://api.map.baidu.com/lbsapi/getpoint/index.html)
- [JavaScript API 3.0](https://lbsyun.baidu.com/index.php?title=jspopular3.0/guide/infowindow)
- [示例中心](https://lbsyun.baidu.com/jsdemo.htm#eMarkerAddEvent)
