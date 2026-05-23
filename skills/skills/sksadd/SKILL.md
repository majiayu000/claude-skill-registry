---
name: sksadd
description: 从上次搜索结果安装 skill 到指定组
---

从对话上下文推断组名和编号（如用户说"安装第3个"、"装到 docs 组"、"装1到5"），**直接运行**：

```bash
python3 "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/sksadd/add.py" "<GROUP>" "<INDEX1>" ["<INDEX2>" ...]
```

支持多个编号，顺序安装。组名或编号不明确时才询问用户。
