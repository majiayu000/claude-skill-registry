---
name: fix-explain
description: "[EXPLAIN:fix|lang=user-level]=>[FMT:what-wrong+why+how-fixed]"
---
[EXPLAIN:after-fix|lang=user-level-detect]
1=what-wrong(human-terms)|2=why(simple-cause)|3=how-fixed(one-sentence)
[GOOD]"问题找到了：登录时密码对比写反了，对的密码反而登不进去。改过来了，现在正常了。"
[BAD]"bcrypt.compare()的参数顺序反了，hash传到plaintext位置导致返回false。"
