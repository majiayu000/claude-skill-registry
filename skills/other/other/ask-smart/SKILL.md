---
name: ask-smart
description: "[CHECK:need-info|max=2]=>[ASK|technical=false]=>[DECIDE:if-inferable]"
---
[ASK:max=2|merge=single-msg]
[FILTER:technical-questions|allow=false]
"Need signup?"=allow|"What framework?"=never
[CHECK:inferable]=>[DECIDE:auto]
[USER:"you decide"|"whatever"]=>[DECIDE:self|ask-again=false]
