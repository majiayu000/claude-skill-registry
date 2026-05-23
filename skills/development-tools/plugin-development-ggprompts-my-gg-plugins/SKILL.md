---
name: plugin-development
description: Create and manage Claude Code plugins including commands, agents, skills, hooks, and MCP servers. This skill should be used when building new plugins, debugging plugin issues, understanding plugin structure, or working with plugin marketplaces.
---

# Plugin Development

This skill provides guidance for creating, structuring, and debugging Claude Code plugins.

## When to Use

This skill should be used when:
- Creating a new Claude Code plugin from scratch
- Adding components (commands, agents, skills, hooks, MCP servers) to an existing plugin
- Debugging plugin loading or configuration issues
- Understanding plugin directory structure and manifest format
- Preparing plugins for distribution via marketplaces

## Plugin Overview

A Claude Code plugin is a directory containing:
1. **`.claude-plugin/plugin.json`** (required) - Plugin manifest with metadata
2. **Component directories** (optional) - `commands/`, `agents/`, `skills/`, `hooks/`, `.mcp.json`
3. **Scripts and assets** - Supporting files for hooks and utilities

## Creating a Plugin

### Step 1: Create Directory Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json       # REQUIRED - manifest
├── commands/             # Slash commands (.md files)
├── agents/               # Subagents (.md files)
├── skills/               # Agent skills (dirs with SKILL.md)
├── hooks/
│   └── hooks.json        # Hook configurations
├── .mcp.json             # MCP server definitions
└── scripts/              # Utility scripts for hooks
```

### Step 2: Create plugin.json

Minimal manifest:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does"
}
```

Full manifest - see `references/manifest-schema.md`.

### Step 3: Add Components

**Commands** - Create `commands/name.md`:
```markdown
---
description: Brief description for autocomplete
---

# Command Name

Instructions for the command...
```

**Agents** - Create `agents/name.md`:
```markdown
---
description: What this agent specializes in
capabilities: ["task1", "task2"]
---

# Agent Name

Agent instructions...
```

**Skills** - Create `skills/name/SKILL.md`:
```markdown
---
name: skill-name
description: What the skill does
---

# Skill Name

Skill instructions...
```

**Hooks** - Create `hooks/hooks.json` or inline in plugin.json:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint.sh"
      }]
    }]
  }
}
```

**MCP Servers** - Create `.mcp.json` or inline in plugin.json:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["@company/mcp-server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

## Publishing as a Marketplace

To make your plugin installable via `github:` or `local:` sources, add `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-marketplace",
  "plugins": [
    {
      "name": "my-skill",
      "description": "What it does",
      "source": "./skills/my-skill"
    },
    {
      "name": "full-plugin",
      "description": "Everything in this plugin",
      "source": "./"
    }
  ]
}
```

**Critical:** All `source` paths must start with `./` (e.g., `"./"` not `"."`).

See `references/marketplace-schema.md` for complete schema.

## Critical Rules

1. **`.claude-plugin/` contains ONLY `plugin.json` and `marketplace.json`** - All component directories go at plugin root
2. **All paths are relative** - Must start with `./`
3. **Use `${CLAUDE_PLUGIN_ROOT}`** - For absolute paths in hooks/MCP configs
4. **Scripts must be executable** - Run `chmod +x script.sh`

## Debugging

Run `claude --debug` to see:
- Which plugins are loading
- Errors in plugin manifests
- Command, agent, and hook registration
- MCP server initialization

### Common Issues

| Issue                  | Cause                      | Solution                              |
|------------------------|----------------------------|---------------------------------------|
| Plugin not loading     | Invalid plugin.json        | Validate JSON syntax                  |
| Commands not appearing | Wrong directory structure  | Ensure `commands/` at root, not in `.claude-plugin/` |
| Hooks not firing       | Script not executable      | Run `chmod +x script.sh`              |
| MCP server fails       | Missing CLAUDE_PLUGIN_ROOT | Use variable for all plugin paths     |
| Path errors            | Absolute paths used        | All paths must be relative with `./`  |
| "marketplace not found" | Missing marketplace.json   | Add `.claude-plugin/marketplace.json` |
| "source must start with ./" | Source path is `"."` not `"./"` | Change to `"./"` for root plugin |

## Resources

- `references/plugin-structure.md` - Complete directory layout and file locations
- `references/manifest-schema.md` - Full plugin.json schema with all fields
- `references/marketplace-schema.md` - Marketplace.json schema for github/local sources
- `references/components.md` - Detailed specs for commands, agents, skills, hooks, MCP
- `assets/templates/` - Template files for creating new plugins
