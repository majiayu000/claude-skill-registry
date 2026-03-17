---
name: tianqi
description: 查询中国地区的天气预报，支持15天及逐小时预报、各种生活指数
---

# 天气预报
查询中国地区的天气预报，支持15天及逐小时预报、各种生活指数

## 查询命令
```shell
# 搜索城市编号
bash scripts/curl.sh 'https://toy1._DOMAIN_/search' -G --data-urlencode 'cityname=黄埔'

# 获取天气概况 101020100需替换为真实的城市编号
bash scripts/curl.sh 'https://d1._DOMAIN_/weather_index/101020100.html?_=_TIME_'

# 获取站点位置信息 method=stationinfo&areaid=101020100
bash scripts/curl.sh 'https://d7._DOMAIN_/geong/v1/api' -G --data-urlencode 'params={"method":"stationinfo","areaid":"101020100"}'

# 分钟级天气预报，需要先从站点信息中获取经纬度
bash scripts/curl.sh 'https://mpf._DOMAIN_/mpf_v3/webgis/minute?lat=<latitude>&lon=<longitude>&_=_TIME_'
# 返回字段 values:降水量

# 每日天气预报
bash scripts/curl.sh 'https://d1._DOMAIN_/weixinfc/101020100.html?_=_TIME_'
# 返回字段 fa/fb:天气状况代码 fc:最高温度 fd:最低温度 fn:湿度

# 小时级天气预报
bash scripts/curl.sh 'https://d1._DOMAIN_/wap_180h/101020100.html?_=_TIME_'
# 返回字段 ja:天气状况代码 jb:温度 je:湿度 jg:风速 jj:气压

# 气象预警
bash scripts/curl.sh 'https://d1._DOMAIN_/dingzhi/101020100.html?_=_TIME_'
```

# 天气状况代码
```yaml
'00': 晴
'01': 多云
'02': 阴
'03': 阵雨
'04': 雷阵雨
'05': 雷阵雨伴有冰雹
'06': 雨夹雪
'07': 小雨
'08': 中雨
'09': 大雨
'10': 暴雨
'11': 大暴雨
'12': 特大暴雨
'13': 阵雪
'14': 小雪
'15': 中雪
'16': 大雪
'17': 暴雪
'18': 雾
'19': 冻雨
'20': 沙尘暴
'21': 小到中雨
'22': 中到大雨
'23': 大到暴雨
'24': 暴雨到大暴雨
'25': 大暴雨到特大暴雨
'26': 小到中雪
'27': 中到大雪
'28': 大到暴雪
'29': 浮尘
'30': 扬沙
'31': 强沙尘暴
'32': 浓雾
'49': 强浓雾
'53': 霾
'54': 中度霾
'55': 重度霾
'56': 严重霾
'57': 大雾
'58': 特强浓雾
'301': 雨
'302': 雪
```
