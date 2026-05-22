---
name: claude-code-mcp
description: Configure and build Model Context Protocol (MCP) servers for Claude Code integration. Set up database, filesystem, git, and API connections. Build custom MCP servers with TypeScript/Python SDK, implement tools and resources, configure transports (stdio, HTTP), and deploy for production.
---

# Claude Code MCP

Specification: https://modelcontextprotocol.io/specification/2025-11-25 (November 2025)

Use this skill when you need to:

- Configure `.claude/.mcp.json` for official/community MCP servers
- Build custom MCP servers (TypeScript or Python)
- Deploy and harden remote MCP servers (HTTP transport)

## Quick Start (Local stdio via npx)

1) Create or edit `.claude/.mcp.json`:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "POSTGRES_URL": "${DATABASE_URL}" }
    }
  }
}
```

2) Provide env vars and validate the connection:

```bash
export DATABASE_URL="postgresql://user:pass@localhost:5432/db"
claude mcp list
claude mcp get postgres
```

Notes:
- Default config path is typically `.claude/.mcp.json`. If needed, override via `claude --mcp-config <path>`.
- Prefer `python3` as the Python interpreter in server configs unless your environment guarantees `python`.

## Permission Management (Recommended)

```bash
# Allow all tools from a server (wildcard)
claude mcp add --allow "mcp__postgres__*" postgres -- npx -y @modelcontextprotocol/server-postgres

# Allow specific tools only
claude mcp add --allow "mcp__postgres__query,mcp__postgres__list_tables" postgres -- npx -y @modelcontextprotocol/server-postgres

# Deny a specific tool
claude mcp add --deny "mcp__filesystem__write_file" filesystem -- npx -y @modelcontextprotocol/server-filesystem ./data
```

## Production Guardrails (Required)

- Assume tool outputs are untrusted (prompt injection). Sanitize/structure before reuse.
- Default to least privilege: read-only DB, scoped filesystem allowlists, minimal tool allowlists.
- Keep secrets out of `.mcp.json`; inject via env vars or a secret manager at runtime.
- Add timeouts, retries, and rate limits; log all tool invocations for audit.

## What To Read Next

- Choose an existing server: `references/mcp-servers.md`
- Build a custom server: `references/mcp-custom.md`
- Implementation patterns (DB/API/filesystem): `references/mcp-patterns.md`
- Security hardening (OAuth, scopes, injection defense): `references/mcp-security.md`
- Templates: `assets/database/template-mcp-database.md`, `assets/filesystem/template-mcp-filesystem.md`, `assets/api/template-mcp-api.md`, `assets/deployment/template-mcp-docker.md`
- Curated links: `data/sources.json`
