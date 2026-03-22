---
name: llmlb-cli-usage
description: Use llmlb assistant CLI commands (curl/openapi/guide) instead of the deprecated MCP server flow.
allowed-tools: Read, Grep, Bash
---

# llmlb Assistant CLI Usage (Codex)

Use `llmlb assistant` for llmlb API inspection and safe curl execution.

## Workflow

1. Inspect schema with `llmlb assistant openapi`.
2. Read focused guidance with `llmlb assistant guide --category <...>`.
3. Execute API calls with `llmlb assistant curl --command "curl ..."`.

## Examples

```bash
llmlb assistant openapi
llmlb assistant guide --category endpoint-management
llmlb assistant curl --command "curl http://localhost:32768/api/endpoints" --json
```

## Environment variables

- `LLMLB_URL`
- `LLMLB_API_KEY`
- `LLMLB_ADMIN_API_KEY`
- `LLMLB_JWT_TOKEN`

## Notes

- The CLI blocks unapproved hosts and common injection patterns.
- `assistant curl` auto-injects auth headers unless `--no-auto-auth` is set.
