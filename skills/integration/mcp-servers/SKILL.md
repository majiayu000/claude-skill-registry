---
name: mcp-servers
description: "Model Context Protocol integration for external tools (GitHub, filesystem, SPARQL)."
allowed_tools: "Read"
---

# MCP Server Integration

## Overview

Model Context Protocol connects LLMs to external tools:
- **GitHub**: Issues, PRs, repositories
- **Filesystem**: Enhanced file operations
- **Custom**: SPARQL, validation, domain-specific

## Configuration

In `.claude/settings.json`:

```json
{
  "mcp_servers": {
    "github": {
      "command": "mcp-server-github",
      "env": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"}
    },
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["/home/user/ggen"]
    }
  }
}
```

## Status

Currently disabled in ggen (can be enabled per project needs).

## Reference
See `.claude/settings.json` mcp_servers section for configuration.
