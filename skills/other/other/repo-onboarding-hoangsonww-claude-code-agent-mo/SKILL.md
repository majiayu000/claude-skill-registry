---
name: repo-onboarding
description: Onboard quickly to this repository. Use when asked to understand architecture, locate ownership, choose the right module, or identify the correct commands and verification strategy before coding.
---

# Repo Onboarding

Use this workflow when a task begins with discovery.

## Steps
- Read `README.md` and `ARCHITECTURE.md` for system-level context.
- Identify target layer:
  - `server/` for API, hooks, DB, websocket
  - `client/` for UI and routing
  - `mcp/` for local MCP tools and policy gates
- Select the smallest set of files required to answer the task.
- Confirm verification commands before implementation.

## Verification defaults
- Backend: `npm run test:server`
- Frontend: `npm run test:client`
- MCP: `npm run mcp:typecheck` and `npm run mcp:build`

## References
- Module map: `references/module-map.md`
- Command map: `references/command-map.md`
