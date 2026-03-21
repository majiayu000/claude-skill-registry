---
name: plan-breakdown
description: "[SPLIT:task|cnt=5-15|step-time=2-5min]=>[ORDER:dependency]=>[SHOW:user]"
---
[SPLIT:task|cnt=5-15|each=2-5min]
[EACH:step]=>[deliverable=visible+testable]
[ORDER:by=dependency]
[SHOW:user|fmt=plain-language]
"1. 搭框架（2分钟）2. 注册页面（5分钟）3. 登录功能（5分钟）...大概20分钟搞定。"
[RULE:step>5min]=>[SPLIT:further]
