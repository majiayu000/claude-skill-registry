---
name: fix-solve
description: "[FIX:minimal|step=3-of-3]=>[TEST:verify]=>[ACTIVATE:fix-explain]"
---
[STEP:3-of-3|name=solve]
[IF:possible]=>[WRITE:reproduction-test]
[FIX:minimal|change=as-little-as-possible]
[RUN:test]=>[VERIFY:pass]
[RUN:all-tests]=>[VERIFY:nothing-else-broke]
[VERIFY:original-symptom=gone]
[RULE:one-liner=ideal|restructure=discuss-with-user-first]
[REFACTOR-DURING-FIX|allow=false]
=>[ACTIVATE:fix-explain]
