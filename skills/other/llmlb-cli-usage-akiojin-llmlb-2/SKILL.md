---
name: llmlb-cli-usage
description: Practical guide for llmlb assistant CLI commands replacing the legacy MCP server flow.
allowed-tools: Read, Grep, Bash
---

# llmlb Assistant CLI Usage (Claude Code)

Use `llmlb assistant` as the default interface for API inspection and curl execution.

## Preferred command order

1. `llmlb assistant openapi` to inspect endpoint schema.
2. `llmlb assistant guide --category <...>` to load task-specific API notes.
3. `llmlb assistant curl --command "curl ..."` to execute requests safely.

## Examples

```bash
llmlb assistant openapi
llmlb assistant guide --category overview
llmlb assistant curl --command "curl http://localhost:32768/v1/models" --json
```

## Auth and environment

- `LLMLB_URL` (default: `http://localhost:32768`)
- `LLMLB_API_KEY` for `/v1/*`
- `LLMLB_ADMIN_API_KEY` for `/api/*`
- `LLMLB_JWT_TOKEN` fallback for `/api/auth/*`

## Safety notes

- Requests to non-allowed hosts are blocked.
- Shell-injection patterns and dangerous curl options are rejected.
- Use `--no-auto-auth` only when you must send custom auth headers.
