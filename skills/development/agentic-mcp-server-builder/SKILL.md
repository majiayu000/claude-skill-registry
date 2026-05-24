---
name: agentic-mcp-server-builder
description: Scaffold MCP server projects and baseline tool contract checks. Use for defining tool schemas, generating starter server layouts, and validating MCP-ready structure.
---

# Agentic MCP Server Builder

## Overview

Create a minimal MCP server scaffold and contract summary from a structured tool list.

## Workflow

1. Define server name and tool list with descriptions.
2. Generate scaffold file map and tool contract summary.
3. Optionally materialize starter files when not in dry-run mode.
4. Review generated contract checks before adding business logic.

## Use Bundled Resources

- Run `scripts/scaffold_mcp_server.py` to generate starter artifacts.
- Read `references/mcp-scaffold-guide.md` for file layout and contract checks.

## Guardrails

- Keep tool boundaries explicit and minimal.
- Include deterministic outputs and clear input/output schemas.
