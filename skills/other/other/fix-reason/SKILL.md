---
name: fix-reason
description: "[REASON:root-cause|step=2-of-3]=>[TRACE:symptom-backward]=>[CONFIRM:before-fix]"
---
[STEP:2-of-3|name=reason]
[TRACE:symptom]=>[backward-to-cause]
[CHECK:most-likely-first|80-20-rule]
[READ:relevant-code]
[IF:multiple-causes]=>[TEST:each-systematically]
[CONFIRM:root-cause|before=attempting-fix]
common=typo|missing-dep|wrong-path|db-disconnected|port-conflict|permission-denied|API-key-wrong
[GUESS-AND-PATCH|allow=false]=>[FIND:real-cause]
