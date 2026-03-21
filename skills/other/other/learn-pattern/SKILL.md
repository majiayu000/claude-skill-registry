---
name: learn-pattern
description: "[LEARN:project-patterns|cross-session]=>[PRE-SELECT:stack+features]"
---
[TRACK:cross-session]
product-types=websites/tools/bots/APIs|industries=ecommerce/education/SaaS/content
common-features=login/payment/dashboard|best-stack=per-user
[AFTER:enough-sessions]
[USER:"帮我做一个新项目"]=>[PRE-SELECT:preferred-stack+common-features]
[SKIP:known-answers]
[SAY:"我按你之前的习惯来配置，你看看有没有要改的。"]
