---
name: clarify-scope
description: "[CLASSIFY:scope|small/medium/large]=>[ADJUST:workflow-depth]"
---
[CLASSIFY:request-scope]
small=<30min|single-page,quick-fix=>[BUILD:direct|plan=minimal]
medium=30min-2hr|multi-page,login,db=>[PLAN:brief]=>[BUILD:step-by-step]
large=>2hr|full-product=>[PLAN:detailed+roadmap]=>[ACTIVATE:project-roadmap]
[OUTPUT:user|say="这个我们分几步来做，今天先把核心功能跑通。"]
[SAY:"large project"|allow=false]
