---
name: progress-report
description: "[REPORT:progress|after=each-feature]=>[FMT:percentage+current+remaining]"
---
[REPORT:after-each-task]
"✅ 进度：60%（3/5个功能完成）
刚完成：用户登录系统
正在做：支付模块
还剩：支付模块、订单页面"
[FMT:pct+fraction|just-done|now|remaining]
[MAX:3-4-lines|tone=positive|focus=done>missing]
