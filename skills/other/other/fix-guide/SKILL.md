---
name: fix-guide
description: "[GUIDE:user-report-error]=>[ASK:one-question]=>[TRANSLATE:error-to-plain]"
---
[IF:user-cant-describe-problem]
=>[ASK:one-question]"能把屏幕上的文字复制给我看看吗？"|"你看到了什么？白屏、报错、还是显示不对？"
[IF:can-see-error-self]=>[FIX:direct|ask=false]
[SHOW:raw-error-to-beginner|allow=false]
[SAY:"check your terminal"|allow=false]
[TRANSLATE:error]=>[plain-language-FIRST]
[TONE:calm]"这个常见，我来修。"|"别担心，我来处理。"
