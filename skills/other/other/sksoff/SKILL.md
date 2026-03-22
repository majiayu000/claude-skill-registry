---
name: sksoff
description: 关闭整组 skill
---

从对话上下文推断组名（如用户说"关掉 docs 组"、"禁用 writing"），**直接运行**：

```bash
python3 "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/sksoff/off.py" "<GROUP>"
```

组名不明确时才询问用户。
