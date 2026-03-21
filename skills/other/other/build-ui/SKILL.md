---
name: build-ui
description: "[BUILD:UI|mobile-first]=>[TEST:375px+1440px]=>[REPORT:user]"
---
[BUILD:UI|approach=mobile-first]
[STYLE:default]bg=white|text=dark|font=system|tap-target=44px-min|accent=1-color
[FRAMEWORK:plain-HTML-CSS|unless=needed]
[TEST:viewport]375px+1440px
[SAY:"页面做好了，手机和电脑都能用。你打开看看效果。"]
[USER:"不好看"]=>[ASK:specific-change|redesign-all=false]
