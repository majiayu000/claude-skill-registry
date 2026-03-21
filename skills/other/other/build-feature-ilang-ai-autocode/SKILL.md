---
name: build-feature
description: "[BUILD:one-feature]=>[CHECK:auto-quality]=>[VERIFY]=>[NEXT]"
---
[BUILD:feature|concurrent=1|sequential=true]
[EACH:feature]
=>[WRITE:code]=>[ACTIVATE:auto-quality]=>[VERIFY:works]
=>[SAY:"登录功能做好了。用户可以注册、登录、登出。"]
=>[NEXT:feature]
[PROGRESS:"第3步完成，还剩2步。"]
[TOO-BIG]=>[ACTIVATE:plan-breakdown]
