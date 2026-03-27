---
name: windows-hook-debugging
description: "Windows环境下Claude Code插件Hook执行错误的诊断与修复。当遇到hook error、cannot execute binary file、.sh regex误匹配、WSL/Git Bash冲突时使用。"
---

# Windows Hook Debugging Skill

诊断和修复 Windows 环境下 Claude Code 插件 Hook 执行失败的问题。

## When to Use This Skill

触发条件（满足任一即可）：
- Claude Code 启动时出现 `SessionStart hook error` 或 `Stop hook error`
- 错误信息包含 `cannot execute binary file`
- 错误信息包含 `/d/` 或 `/c/` 风格的路径（MSYS2/Git Bash 路径格式）
- 错误信息包含 `bash: node: No such file or directory`
- 错误信息包含 WSL 相关乱码或 `wsl:` 前缀
- Hook 命令中包含 `.sh` 参数导致 Windows 下被错误处理

## Not For / Boundaries

- 不适用于 macOS/Linux 上的 hook 问题（那些平台没有 WSL/Git Bash 冲突）
- 不适用于 hook 逻辑错误（如 JSON 解析失败、权限拒绝等业务逻辑问题）
- 不适用于 MCP Server 连接问题
- 需要的输入：完整的错误信息、当前 settings.json 内容、相关 hooks.json 内容
