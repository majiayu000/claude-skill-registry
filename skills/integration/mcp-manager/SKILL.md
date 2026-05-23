---
name: mcp-manager
description: Conversational interface for managing MCP (Model Context Protocol) server configurations in Claude Code
type: skill
activationStrategy: lazy-aggressive
activationKeywords:
  - MCP
  - Model Context Protocol
  - MCP server
  - MCP configuration
  - configure MCP
  - manage MCP
  - enable MCP
  - disable MCP
  - add MCP
  - remove MCP
  - list MCPs
  - show MCP
  - validate MCP
  - export MCP
  - import MCP
activationContextWindow: 3
persistenceThreshold: 20
---

# MCP Manager Skill

## Overview

Natural language interface to MCP Manager CLI tool for managing Model Context Protocol server configurations. Users interact conversationally: "enable the filesystem MCP", "add a database server", "show me all my MCPs".

## Activation

Activates on MCP keywords within 3-message window or explicit invocation: `/mcp-manager`

## Commands

### 1. List MCPs

Display all configured MCP servers with status.

- "List all my MCPs" / "Show me my MCP servers"
- CLI: `python3 -m mcp-manager.cli list`

### 2. Enable MCP

Activate a disabled MCP server.

- "Enable the filesystem MCP" / "Turn on puppeteer"
- CLI: `python3 -m mcp-manager.cli enable <server-name>`

### 3. Disable MCP

Deactivate an MCP server without removing it. Requires confirmation.

- "Disable the puppeteer MCP" / "Turn off github"
- CLI: `python3 -m mcp-manager.cli disable <server-name>`

### 4. Add MCP

Add new MCP server interactively (collects name, command, args, env vars).

- "Add a new MCP server" / "Configure a database MCP"
- CLI: `python3 -m mcp-manager.cli add <name> <command> [args...] --env KEY=VALUE`

### 5. Remove MCP

Delete MCP server configuration completely. Requires confirmation with warning.

- "Remove the puppeteer MCP" / "Delete the old-server"
- CLI: `python3 -m mcp-manager.cli remove <server-name>`

### 6. Show MCP

Display detailed information for specific MCP server.

- "Show me the filesystem MCP" / "Details for github server"
- CLI: `python3 -m mcp-manager.cli show <server-name>`

### 7. Validate MCPs

Check all MCP configurations for errors.

- "Validate my MCP configuration" / "Check for MCP errors"
- CLI: `python3 -m mcp-manager.cli validate`

### 8. Export MCPs

Export configurations to JSON file for backup.

- "Export my MCP configuration" / "Back up my MCPs"
- CLI: `python3 -m mcp-manager.cli export [output-file]`

### 9. Import MCPs

Import configurations from JSON file.

- "Import MCPs from backup.json" / "Restore my MCPs"
- CLI: `python3 -m mcp-manager.cli import <input-file> [--merge]`

## Usage Examples

### Example 1: List and Enable

**User:** "List all my MCPs"

[Executes: `cd .claude/scenarios && python3 -m mcp-manager.cli list`]

**Response:**
"You have 3 MCP servers configured:
✓ filesystem (enabled) - Local filesystem access
✓ github (enabled) - GitHub API integration
✗ puppeteer (disabled) - Browser automation"

**Follow-up:** "Turn on puppeteer"

[Executes: `python3 -m mcp-manager.cli enable puppeteer`]

"✓ Successfully enabled 'puppeteer' MCP server."

### Example 2: Add New Server

**User:** "Add a new MCP for database access"

**Interactive Collection:**

1. Name: "postgres-local"
2. Command: "node /opt/mcp-servers/postgres/index.js"
3. Args: "--port 5432 --host localhost"
4. Env: "DATABASE_URL=postgresql://localhost:5432/mydb"

[Executes: `python3 -m mcp-manager.cli add postgres-local "node /opt/mcp-servers/postgres/index.js" --port 5432 --host localhost --env "DATABASE_URL=postgresql://localhost:5432/mydb"`]

"✓ Successfully added 'postgres-local' MCP server.
Server is currently disabled. Enable with: 'enable postgres-local'"

### Example 3: Remove Server

**User:** "Remove the puppeteer MCP"

**Confirmation:**
"⚠️ WARNING: You're about to remove 'puppeteer' MCP server. This will delete the configuration completely. This action cannot be undone. Are you sure? (yes/no)"

[User confirms: "yes"]

[Executes: `python3 -m mcp-manager.cli remove puppeteer`]

"✓ Successfully removed 'puppeteer' MCP server."

## Tool Invocation

All commands execute from `.claude/scenarios/` directory:

```bash
cd .claude/scenarios && python3 -m mcp-manager.cli <command> [args]
```

**Key Commands:**

- `list` - List all MCPs
- `enable <name>` - Enable server
- `disable <name>` - Disable server
- `add <name> <cmd> [args...] --env KEY=VAL` - Add server
- `remove <name>` - Remove server
- `show <name>` - Show details
- `validate` - Validate all configurations
- `export [file]` - Export to JSON
- `import <file> [--merge]` - Import from JSON

**Output Handling:**

- Success: Exit code 0, stdout with ✓ prefix
- Error: Non-zero exit code, stderr with ❌ prefix
- Redact sensitive info (tokens, passwords) in responses

## Error Handling

**Common Errors:**

1. **CLI Not Found**: Offer installation instructions (see README)
2. **Server Not Found**: List available servers, suggest alternatives
3. **Server Already Exists**: Suggest show/remove/rename
4. **Permission Denied**: Check file/directory permissions
5. **Malformed settings.json**: Validate JSON, offer backup restore
6. **Invalid Command**: Show common command patterns

For detailed error scenarios and troubleshooting, see `.claude/scenarios/mcp-manager/README.md`

## Best Practices

- Always confirm destructive operations (disable, remove)
- Validate server names before executing
- Redact sensitive information in responses
- Provide clear error messages with actionable next steps
- Show current state before and after changes

## See Also

- Full documentation: `.claude/scenarios/mcp-manager/README.md`
- Tool creation guide: `.claude/scenarios/mcp-manager/HOW_TO_CREATE_YOUR_OWN.md`
- MCP Protocol: https://modelcontextprotocol.io/
- Claude Code Settings: `.claude/settings.json`

---

**Version:** 1.0.0 | **Updated:** 2025-11-24 | **Maintainer:** amplihack team
