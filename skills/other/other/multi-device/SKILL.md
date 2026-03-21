---
name: multi-device
description: "[TEST:375px+768px+1440px]=>[VERIFY:no-horizontal-scroll|min-font=16px]"
---
[SUPPORT:required]phone=375px|tablet=768px|desktop=1440px
[DESIGN:mobile-first]=>[SCALE:up]
[RULE]touch=44px-min|h-scroll=never|body-text=16px-min
[TEST:375px|before=declaring-done]
[SAY:"手机和电脑都能用，你可以试试。"]
