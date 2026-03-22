---
name: skson
description: 激活整组 skill
---

从对话上下文推断组名（如用户说"开启 docs 组"、"激活 writing"），**直接运行**：

```bash
python3 "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/skson/on.py" "<GROUP>"
```

组名不明确时才询问用户。
