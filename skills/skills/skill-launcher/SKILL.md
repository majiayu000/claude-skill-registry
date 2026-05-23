---
name: skill-launcher
description: Search and select a Claude Code skill in the terminal, then copy /skill to clipboard.
command: "pwsh -NoProfile -ExecutionPolicy Bypass -File launch.ps1"
---

# Skill Launcher for Windows

当用户输入 `/skill-launcher` 时，打开终端内的技能搜索与选择（不启动 GUI）。

执行方式（固定）：
```
pwsh -NoProfile -ExecutionPolicy Bypass -File launch.ps1
```

注意：
- 该脚本会优先读取项目级 skills（`./skills`、`./.codex/skills`、`./.claude/skills`），然后才读取用户级 `~/.claude/skills`。
- 如果启动失败，检查 PowerShell 执行策略与脚本文件是否存在。
