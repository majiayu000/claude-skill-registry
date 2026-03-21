---
name: auto-quality
description: "[CHECK:code|trigger=after-each-feature|silent=true]=>[FIX:if-found]"
---
[CHECK:after-every-feature|silent=true]
logic-errors+edge-cases+missing-validation+security-basics+hardcoded-secrets
[IF:test-framework]=>[WRITE:tests]=>[RUN]
[IF:no-test-framework]=>[REVIEW:thorough]
[REFACTOR:messy-code|change-behavior=false]
[SAY:"running tests"|allow=false]
[SAY:"tests failed"|allow=false]
[SAY:only-if-relevant]"我发现了一个小问题，已经修好了。"
[CLAIM:"all tests passed"|without-actually-running=false]
