---
name: chitti-mcp
description: Use this skill when you need to start or call Chitti's MCP server (chitti.decide/recall/policy/audit) from Codex, keeping tool details out of context until invoked.
---

# Chitti MCP Skill

Use this when you need to record, recall, or audit decisions via Chitti's MCP tools.

## Quick start

- Start the MCP server:
  - `scripts/start_server.sh`
- Call a tool in one shot (starts server, calls tool, exits):
  - `scripts/mcp_call.sh chitti.decide '{"action":"pay","amount":5,"currency":"USDC","reason":"example"}'`

## When to use which tool

- `chitti.decide`: record a decision (requires `action`, `amount`, `reason`).
- `chitti.recall`: query history (filters like `action`, `to`, `outcome`, `query`, `limit`).
- `chitti.policy.*`: manage/evaluate rules.
- `chitti.audit`: fetch decision by id.

## Notes

- This skill wraps the existing MCP server; do not remove MCP if you need ChatGPT connectors or other MCP clients.
- If a tool call fails, retry with valid JSON arguments and required fields.
