---
name: sksrm
description: 删除单个 skill
---

从对话上下文推断目标（格式 `<组名>/<skill名>`，如用户说"删掉 docs 组里的 readme-writer"），**直接运行**：

```bash
python3 "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/sksrm/rm.py" "<GROUP/SKILL>"
```

组名或 skill 名不明确时才询问用户。
