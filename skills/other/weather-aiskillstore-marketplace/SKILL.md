---
name: weather
description: 查询指定城市的天气信息
version: 1.0.0
author: AI Creator
tags:
  - weather
  - 天气
  - forecast
  - 预报
triggers:
  - 天气
  - 温度
  - 预报
  - weather
  - temperature
  - forecast
---

# Weather Skill

## 功能描述

Weather Skill 提供天气查询功能，可以查询指定城市的当前天气信息。

## 使用方法

### 查询当前天气

提供城市名称即可查询当前天气：

```
查询北京的天气
查询上海的天气
```

### 查询指定日期天气

可以指定日期查询历史或未来天气：

```
查询北京 2024-01-01 的天气
查询上海明天的天气
```

## 返回信息

天气查询返回以下信息：
- 温度（摄氏度）
- 天气状况（晴、多云、雨等）
- 湿度百分比

## 支持的城市

目前支持以下主要城市：
- 北京
- 上海
- 广州
- 深圳
- 杭州

其他城市会返回模拟数据。

## 相关资源

- `cities.md`: 支持的城市列表
- `weather_api.md`: 天气 API 使用说明
