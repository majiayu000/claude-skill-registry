---
name: sibyl-codex-writer
description: Sibyl Codex 写作 agent - 使用 Codex (GPT-5) 撰写论文
context: fork
agent: sibyl-standard
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, mcp__codex__codex, mcp__codex__codex-reply, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('codex_writer', workspace_path=ws))"`

AGENT_NAME: sibyl-codex-writer
AGENT_TIER: sibyl-standard
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
Codex model override: $ARGUMENTS[1] (optional)

## Codex MCP 调用规范

每次调用 `mcp__codex__codex` 时：
- 若提供了 `Codex model override`，则显式传 `model: $ARGUMENTS[1]`
- 若未提供，则不要传 `model` 参数，使用 Codex MCP 默认模型
- 设置 `approval-policy: "never"` 以实现自动化执行
- 返回的 `threadId` 可用于 `mcp__codex__codex-reply` 做追加修订

调用示例：
```
mcp__codex__codex:
  prompt: <章节写作 prompt>
  approval-policy: "never"
```

如需对同一章节追加修改：
```
mcp__codex__codex-reply:
  threadId: <上次返回的 threadId>
  prompt: <修改要求>
```
