---
name: mcp-operations
description: Operate and maintain the local MCP server for this project. Use when creating MCP host config, troubleshooting tool connectivity, modifying tool domains, or adjusting safety policy flags.
---

# MCP Operations

Use this skill whenever work touches `mcp/` behavior or MCP host integration.

## Core workflow
- Confirm dashboard API is running (`/api/health`).
- Confirm MCP server build status.
- Validate env flags for mutation/destructive modes.
- Verify host configuration path and command.

## Safe operations policy
- Default to read-only mode (`MCP_DASHBOARD_ALLOW_MUTATIONS=false`).
- Enable mutations only for explicit admin tasks.
- Enable destructive mode only transiently and require explicit confirmation token.

## Required verification for code changes
- `npm run mcp:typecheck`
- `npm run mcp:build`

## References
- Host config examples: `references/host-config.md`
- Operations runbook: `references/runbook.md`
