---
name: fix-observe
description: "[OBSERVE:problem|step=1-of-3]=>[READ:error+screenshot]=>[DESCRIBE:symptom]"
---
[STEP:1-of-3|name=observe]
[READ:error-msg|careful=true]
[IF:screenshot]=>[VISION:read-precise]
[IF:no-error]=>[ASK:"你看到了什么？白屏、报错、还是显示不对？"]
[REPRODUCE:if-possible]
[RECORD:actual-vs-expected]
[JUMP-TO-FIX|allow=false]=>[UNDERSTAND-FIRST]
[OUTPUT:internal-symptom-description]
