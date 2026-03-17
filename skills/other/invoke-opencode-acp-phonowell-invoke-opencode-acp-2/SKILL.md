---
name: invoke-opencode-acp
description: Delegate complex tasks to OpenCode subagent, use when >=2 file modifications or batch operations
allowed-tools: Bash
---

# invoke-opencode-acp

## When to Use
- Triggers: >=2 file modifications / refactor / batch ops / code review / multi-step reasoning / git ops
- Avoid: single-file quick edits / recursive OpenCode calls

## Core Intent
- Save tokens (50-90%) / main model decides / subagent executes details

## Efficiency Priority
- `acp_client.cjs` (this dir) > manual protocol
- `opencode acp` > run/serve (avoid HTTP)

## Constraints
- Default sandbox blocks writes to `~/.config/opencode` and `~/.cache/opencode` and blocks network
- First run plugin install ~30s; `acp_client.cjs` default `SESSION_TIMEOUT=10s`
- Fix: run `acp_client.cjs` outside sandbox to allow `~` writes and network; or install once then retry; or raise `SESSION_TIMEOUT` > 30s
- Evidence: `~/.local/share/opencode/log/*.log` records bun add/install and duration

## Workflow
1. Pick timeout: simple >=180s / medium >=600s / complex >=1800s
2. If first run or PermissionDenied/Timeout(10000ms) -> retry non-sandbox or install then retry
3. Run:
```bash
node ~/.claude/skills/invoke-opencode-acp/acp_client.cjs "$PWD" "task description" -o /tmp/output.txt -t 300
```
4. Listen `session/update` -> drop `<thinking>` -> `result.stopReason === 'end_turn'`
5. Return: OK / Timeout:{reason} / Error:{reason}

## Protocol Notes
- `initialize` -> `session/new`(cwd,mcpServers:[]) -> `session/prompt`(prompt:[] shape)
- Error codes: -32001 not found / -32002 rejected / -32003 state / -32601 method / -32602 params

## Dependencies
- Node.js
- OpenCode CLI: `npm install -g opencode`
