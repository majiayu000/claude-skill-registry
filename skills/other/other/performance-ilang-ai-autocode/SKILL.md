---
name: performance
description: "[OPTIMIZE:auto|startup<2s|response<1s|RAM<100MB]"
---
[APPLY:during-build|auto=true]
startup=<2s|page-load=<1s|API=<200ms|RAM=<100MB
bundle=minimize|lazy-load=true|cache=static-assets
db=use-indexes+avoid-N+1|images=compress+WebP+lazy
[IF:significant-improvement]=>[SAY:"我优化了一下，页面打开速度从3秒降到0.8秒了。"]
