---
name: mcp-configuration
description: MCP (Model Context Protocol) server configurations for various IDEs including setup, troubleshooting, and discovery management
version: 1.0.0
compatibility: All repositories with MCP integrations

metadata:
  category: tooling
  tags:
    - mcp
    - ide-configuration
    - github-mcp
    - vscode
    - cursor
  triggers:
    - on-demand
---

# MCP Configuration

Configuration and setup for MCP (Model Context Protocol) servers across different IDEs and tools.

## Overview

MCP server configurations are distributed to IDEs in different ways depending on the tool.

## Skill Contents

### Sections

- [Overview](#overview) (L23-L26)
- [IDE Configuration Paths](#ide-configuration-paths) (L47-L56)
- [Quick Reference](#quick-reference) (L57-L71)
- [References](#references) (L72-L79)
- [GitHub MCP Server](#github-mcp-server) (L80-L101)
- [Related](#related) (L102-L105)

### Available Resources

**📚 references/** - Detailed documentation
- [github mcp setup](references/github-mcp-setup.md)
- [ide configurations](references/ide-configurations.md)
- [troubleshooting](references/troubleshooting.md)

---

## IDE Configuration Paths

| IDE/Tool | Configuration File | Type |
|----------|-------------------|------|
| **Cursor** | `.cursor/mcp.json` | Repository-based |
| **VS Code** (GitHub Copilot) | `.vscode/mcp.json` | Repository-based |
| **Claude Code** | `.mcp.json` | Repository-based |
| **IntelliJ IDEA** (Copilot) | `~/.config/github-copilot/intellij/mcp.json` | User-based |
| **GitHub Copilot CLI** | `~/.copilot/mcp-config.json` | User-based |

## Quick Reference

### Automatic (Repository-based)

These IDEs automatically detect MCP configurations from the repository:
- Cursor
- VS Code (with GitHub Copilot)
- Claude Code

### Manual (User-based)

These tools require configuration in the user's home directory:
- IntelliJ IDEA (with GitHub Copilot)
- GitHub Copilot CLI

## References

| Reference | Content |
|-----------|---------|
| `references/ide-configurations.md` | Configuration paths for each IDE |
| `references/github-mcp-setup.md` | GitHub MCP server setup with Docker |
| `references/troubleshooting.md` | Common issues and solutions |

## GitHub MCP Server

The GitHub MCP server provides access to:
- Dependabot alerts
- Code security features
- Secret protection
- Security advisories
- Labels management
- Pull requests

### Prerequisites

1. **Docker** - Must be installed and running
2. **GITHUB_TOKEN** - Environment variable with your GitHub PAT
3. **Cloudflare CA Certificate** - Required for Bitso network TLS

### Readiness Check

```bash
./global/scripts/check-github-mcp-readiness.sh
```

## Related

- `java/commands/add-sonarqube-mcp-to-intellij-and-copilot-cli.md` - IntelliJ & CLI setup
- `global/scripts/check-github-mcp-readiness.sh` - GitHub MCP readiness script
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → global/skills/mcp-configuration/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

