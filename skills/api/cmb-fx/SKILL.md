---
name: cmb-fx
description: "查询招商银行外汇牌价（中间价）"
emoji: "💱"
metadata:
  clawdhub:
    requires:
      bins: ["curl"]
---

# CMB FX Skill

查询招商银行外汇牌价（中间价）。

## API

**必须使用官方 API：**
```
https://fx.cmbchina.com/api/v1/fx/rate
```

## 查询示例

```bash
curl -s "https://fx.cmbchina.com/api/v1/fx/rate" | jq '.body[] | select(.ccyNbrEng | contains("HKD"))'
```

## 响应字段说明

| 字段 | 含义 |
|------|------|
| rthBid | 现汇买入价 (每 100 外币) |
| rthOfr | 现汇卖出价 (每 100 外币) |
| rtcBid | 现钞买入价 (每 100 外币) |
| rtcOfr | 现钞卖出价 (每 100 外币) |
| ratTim | 更新时间 |

## 中间价计算

现汇中间价 = (rthBid + rthOfr) / 2 / 100

注意：API 返回的是 **每 100 外币** 的价格
