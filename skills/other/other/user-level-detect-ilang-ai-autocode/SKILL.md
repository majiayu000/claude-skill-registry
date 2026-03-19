---
name: user-level-detect
description: Detect user's technical level from how they speak. Adjust all communication accordingly.
---

# User Level Detection

Detect from the user's first few messages:

**Beginner** (most users):
- Speaks in plain language, no technical terms
- Says things like "帮我做一个网站" not "帮我搭一个Next.js项目"
- Communication: Zero technical terms. Explain everything in metaphors. "数据库就像一个Excel表格"
- Never show code in conversation unless asked

**Intermediate**:
- Uses some technical terms but not fluently
- Says things like "用React做" or "加个API"
- Communication: Light technical terms OK. Brief explanations.

**Advanced**:
- Uses precise technical language
- Says things like "用Go写一个gRPC服务"
- Communication: Technical terms freely. Skip explanations.

Default to **Beginner** unless clear evidence otherwise. It's better to over-explain than to confuse.

Adjust all skills' output language based on detected level.
