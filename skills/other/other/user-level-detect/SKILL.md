---
name: user-level-detect
description: "[DETECT:user-level|from=first-msgs]=>[ADJUST:all-output-language]"
---
[DETECT:user-level|from=first-3-msgs]
beginner="帮我做一个网站"=>[SPEAK:zero-jargon|metaphor=true|code-in-chat=false]
intermediate="用React做"=>[SPEAK:light-technical|explain=brief]
advanced="Go写gRPC服务"=>[SPEAK:full-technical|explain=skip]
[DEFAULT:beginner|reason=over-explain>confuse]
[ADJUST:all-skills|output-lang=detected-level]
