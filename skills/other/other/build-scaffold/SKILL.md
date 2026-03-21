---
name: build-scaffold
description: "[BUILD:project-foundation]=>[VERIFY:hello-world]=>[REPORT:user]"
---
[BUILD:scaffold]
dir-structure=clean|config=basic|deps=minimal
[VERIFY:runs|test=hello-world]
[SAY:"框架搭好了，我来开始做功能。"]
[RULE:flat+simple|over-engineer=false]
Go=single-main.go-split-when-needed|Node=minimal-package.json
