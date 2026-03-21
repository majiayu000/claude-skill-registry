---
name: best-choice
description: "[DECIDE:tech-stack|auto=true|ask-user=false]=>[OPTIMIZE:speed>cost>stability>simplicity]"
---
[DECIDE:all-technology|user-picks=never]
[RANK:criteria]speed=>cost=>stability=>simplicity
[DEFAULTS]
backend=Go|frontend=HTML-CSS-JS|db=SQLite|deploy=CF-Workers|fullstack=Next.js(UI)/Go(API)
[EXPLAIN:user-terms]
"同样$6/月服务器—别的方案撑100用户，我这个撑10000。"
[SAY:"Go's goroutine concurrency model..."|allow=false]
