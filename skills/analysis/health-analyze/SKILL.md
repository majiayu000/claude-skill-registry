---
name: health-analyze
description: 分析健康数据，计算健康评分并识别异常指标
---

# health-analyze

分析健康指标数据，计算健康评分。

## 输入格式

输入 JSON 包含以下字段：
- `date`: 日期字符串
- `data.temperature`: 体温 (°C)
- `data.heart_rate`: 心率 (bpm)
- `data.steps`: 步数

## 评分规则

总分 100 分，分为三个维度：

1. **体温** (30 分)
   - 36.0 - 37.5°C: +30 分
   - 其他: 0 分，标记为异常

2. **心率** (30 分)
   - 60 - 100 bpm: +30 分
   - 其他: 0 分，标记为异常

3. **步数** (40 分)
   - ≥ 10000: +40 分
   - ≥ 5000: +30 分
   - < 5000: 0 分，标记为运动不足

## 输出格式

必须返回以下 JSON 结构：

```json
{
  "status": "analyzed",
  "date": "<输入的日期>",
  "health_score": <0-100的数字>,
  "analysis": {
    "temperature_ok": <true/false>,
    "heart_rate_ok": <true/false>,
    "steps_ok": <true/false>,
    "issues": ["<问题描述1>", "<问题描述2>"]
  },
  "timestamp": "<ISO 8601 时间戳>"
}
```

## 示例

**输入**:
```json
{"date": "2026-01-20", "data": {"temperature": 37.2, "heart_rate": 75, "steps": 8500}}
```

**输出**:
```json
{
  "status": "analyzed",
  "date": "2026-01-20",
  "health_score": 90,
  "analysis": {
    "temperature_ok": true,
    "heart_rate_ok": true,
    "steps_ok": true,
    "issues": []
  },
  "timestamp": "2026-01-20T10:30:00Z"
}
```
