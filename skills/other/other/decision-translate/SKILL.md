---
name: decision-translate
description: "[TRANSLATE:technical-decision|fmt=money/speed/stability]=>[CMP:with-worse-alternative]"
---
[TRANSLATE:every-decision]=>[ONE-OF]
saves-money="$6/月vs$50/月"|faster="<1秒vs3秒"|stable="百万人用，基本不崩"
lighter="30MB内存，服务器还能干别的"|simpler="一个文件，不用额外装"
[CMP:always-with-worse|use=concrete-numbers]
[EXPLAIN:technical-reasons|allow=false]
[OUTPUT:practical-impact-only]
