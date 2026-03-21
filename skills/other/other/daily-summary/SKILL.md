---
name: daily-summary
description: "[SUM:session-end]=>[FMT:done+fixed+next+progress-delta]=>[ACTIVATE:full-review]"
---
[TRIGGER:user-leaving|goodbye|session-ending]
[FMT]
"今天的进度：
✅ 完成了用户系统（注册、登录、个人页面）
✅ 完成了数据库设计
🔧 发现并修了2个小问题
📋 明天继续：支付模块、订单管理
整体进度：40% → 65%，推进很大。明天见！"
[ICONS]✅=done|🔧=fixed|📋=next
[SHOW:progress-delta]40%→65%
[TONE:positive]=>[ACTIVATE:full-review]
