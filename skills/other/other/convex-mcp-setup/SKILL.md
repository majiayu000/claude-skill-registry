---
name: convex-mcp-setup
description: Set up and troubleshoot Convex MCP access, environment variables, and local development workflow without importing Cursor-only plugin behavior.
version: 1.0.0
metadata:
  author: agentforge
  source: get-convex/convex-agent-plugins@f104efb49a787a1ef4a6c84df496d58800ce334a
---

# Convex MCP Setup

Use this when the task involves Convex MCP configuration, troubleshooting, or explaining how MCP fits local Convex workflows.

## Upstream MCP baseline

The upstream plugin uses this launch command:

```bash
npx -y convex@latest mcp start
```

## Environment

Provide these when deployment access is required:

```bash
CONVEX_DEPLOYMENT=your-deployment-name
CONVEX_DEPLOY_KEY=your-deploy-key
```

## Local guidance

- Treat upstream `mcp.json` as source material, not as a file to install directly into this repo.
- Do not port Cursor plugin manifests or hooks as active repo behavior.
- Use `npx convex dev` for normal development and reserve `npx convex deploy` for production.
- Agent mode is mainly for cloud-hosted coding agents. Local agents usually do not need it.

## References

- Read [mcp-troubleshooting.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/.agents/skills/convex-mcp-setup/references/mcp-troubleshooting.md) for setup checks and common failures.
