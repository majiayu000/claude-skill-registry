---
name: sibyl-codex-reviewer
description: Sibyl Codex 独立第三方审查 - 使用 OpenAI Codex 提供不同 AI 视角的评审
context: fork
agent: sibyl-light
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, mcp__codex__codex, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('codex_reviewer', workspace_path=ws))"`

AGENT_NAME: sibyl-codex-reviewer
AGENT_TIER: sibyl-light
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
MODE: $ARGUMENTS[1]
Codex model override: $ARGUMENTS[2] (optional)

## Codex MCP 调用规范

每次调用 `mcp__codex__codex` 时：
- 若提供了 `Codex model override`，则显式传 `model: $ARGUMENTS[2]`
- 若未提供，则不要传 `model` 参数，使用 Codex MCP 默认模型
- 设置 `approval-policy: "never"` 以实现自动化执行
