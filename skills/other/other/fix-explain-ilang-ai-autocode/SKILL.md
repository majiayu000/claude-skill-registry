---
name: fix-explain
description: Explain what went wrong and how it was fixed. In plain language.
---

# Explain Fix

After fixing a bug, tell the user:
1. What was wrong (in human terms)
2. Why it happened (simple cause)
3. How it was fixed (one sentence)

Example:
"问题找到了：登录的时候密码对比写反了，所以对的密码反而登不进去。我改过来了，现在正常了。"

NOT:
"The bcrypt.compare() call had its arguments in reversed order, passing the hash as plaintext and plaintext as hash, causing all comparisons to return false."

Match the user's technical level (use user-level-detect).
