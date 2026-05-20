---
name: add-mcp
description: Add an MCP server to the project and sync to all AI tools
allowed-tools: Bash(python3 *), Read, Edit
argument-hint: <name> <url-or-command>
---

# Add MCP Server

Add a new MCP server to `.mcp.json` (the single source of truth) and sync to all AI tool configs.

## Steps

1. Parse the arguments: `$ARGUMENTS`
   - Format: `<name> <url>` for HTTP servers (e.g. `loki http://loki-mcp.ablz.au:8081/stream`)
   - Format: `<name> <command> [args...]` for stdio servers (e.g. `mcp-nixos uvx mcp-nixos`)
   - If arguments are missing or ambiguous, ask the user.

2. Read the current `.mcp.json` from the repo root.

3. Add the new server entry:
   - For URLs (starts with `http://` or `https://`): `{"type": "http", "url": "<url>"}`
   - For commands (anything else): `{"command": "<command>", "args": ["<remaining args>"]}`

4. Write the updated `.mcp.json`.

5. Run the sync script to push to Codex:
   ```
   python3 .claude/skills/sync-mcp/sync.py
   ```

6. Report what was added and remind the user to restart Claude Code for the new MCP server to take effect.
