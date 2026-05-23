---
name: sksgnew
description: 创建新的 skill 分组
---

从对话上下文推断组名（如用户说"新建一个 docs 组"、"创建 writing 分组"），**直接运行**：

```bash
python3 "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/sksgnew/gnew.py" "<GROUP>"
```

组名不明确时才询问用户。
