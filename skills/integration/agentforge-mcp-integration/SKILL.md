---
name: agentforge-mcp-integration
description: Work on MCP support in AgentForge, including MCP client/server abstractions, connection management, dynamic tools, and useful external MCPs.
version: 1.0.0
metadata:
  author: agentforge
---

# AgentForge MCP Integration

Use this skill for MCP work in `packages/core`, `packages/cli`, dashboard connections UI, or documentation.

## Primary surfaces

- `packages/core/src/mcp/`
- `packages/core/src/mcp-server.ts`
- `packages/cli/src/commands/mcp.ts`
- dashboard connections routes
- `docs/mcp.md`

## What to check

- transport shape: `stdio`, `http`, `sse`
- connection storage and execution flow
- schema conversion and dynamic tool loading
- UX consistency between CLI, Convex state, and dashboard

## References

- Read [recommended-mcps.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/.agents/skills/agentforge-mcp-integration/references/recommended-mcps.md).
