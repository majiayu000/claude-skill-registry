---
name: plan-estimate
description: "[EVAL:time|overestimate=20%]=>[SHOW:human-units]"
---
[EVAL:total-time|buffer=+20%]
small="大概5分钟"|medium="大概20-30分钟"|large="今天核心1小时，整体2-3天"
[UNIT:minutes/hours/days|never=tokens/iterations]
[LARGE]=>[SPLIT:by-day]"今天登录，明天支付，后天上线"
[UPDATE:during-build]"比预想的快，提前10分钟完成"
