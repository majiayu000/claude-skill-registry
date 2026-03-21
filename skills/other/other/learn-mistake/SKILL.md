---
name: learn-mistake
description: "[RECORD:mistake]=>[SAVE:memory]=>[CHECK:before-similar-build]=>[AVOID:silently]"
---
[ON:mistake-found]
=>[RECORD]what-wrong+why+how-fixed=>[SAVE:memory]
[BEFORE:similar-feature]
=>[CHECK:memory|area=related-mistakes]=>[AVOID:proactively]
[ABOUT-TO-REPEAT]=>[FIX:before-happens]
[SAY:"I remember making this mistake"|allow=false]
[RESULT:user-notices="just works"]
