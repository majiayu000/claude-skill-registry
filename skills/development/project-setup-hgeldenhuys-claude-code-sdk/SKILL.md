---
name: project-setup
description: Guide for setting up projects to work optimally with Claude Code. Use when configuring new projects, migrating existing projects, setting up team permissions, or troubleshooting project configuration. Covers directory structure, settings files, permissions, and best practices.
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob"]
---

# Project Setup

Set up projects to work optimally with Claude Code with proper configuration, permissions, and team sharing.

## Quick Reference

| Directory/File | Purpose | Committed |
|----------------|---------|-----------|
| `.claude/` | Project configuration root | Yes (mostly) |
| `.claude/settings.json` | Project settings and hooks | Yes |
| `.claude/settings.local.json` | Personal project overrides | No |
| `.claude/commands/` | Project slash commands | Yes |
| `.claude/skills/` | Project-specific skills | Yes |
| `CLAUDE.md` | Project knowledge for Claude | Yes |
| `.mcp.json` | Shared MCP servers | Yes |
| `~/.claude/` | Personal global configuration | No |

## Quick Setup Checklist

For new projects:

- [ ] Create `.claude/` directory structure
- [ ] Add `CLAUDE.md` with project knowledge
- [ ] Configure `.claude/settings.json` with permissions
- [ ] Add `.claude/settings.local.json` to `.gitignore`
- [ ] Set up MCP servers in `.mcp.json` if needed
- [ ] Create project-specific slash commands
- [ ] Run `/init` to verify setup

## Directory Structure

### Minimal Setup

```
project/
├── .claude/
│   └── settings.json          # Basic permissions
└── CLAUDE.md                  # Project knowledge
```

### Standard Setup

```
project/
├── .claude/
│   ├── settings.json          # Shared project settings
│   ├── settings.local.json    # Personal overrides (gitignored)
│   ├── commands/              # Project slash commands
│   │   └── deploy.md
│   └── skills/                # Project-specific skills
│       └── domain-model/
│           └── SKILL.md
├── .mcp.json                  # Shared MCP servers
├── CLAUDE.md                  # Project knowledge (root)
└── src/
    └── CLAUDE.md              # Subdirectory knowledge (optional)
```

### Full Setup (with hooks)

```
project/
├── .claude/
│   ├── settings.json          # Settings with hooks
│   ├── settings.local.json    # Personal overrides
│   ├── commands/              # Slash commands
│   │   ├── deploy.md
│   │   └── test.md
│   ├── skills/                # Project skills
│   │   └── domain-model/
│   │       └── SKILL.md
│   └── hooks/                 # Hook scripts
│       ├── format.sh
│       └── validate.py
├── .mcp.json                  # Shared MCP servers
└── CLAUDE.md                  # Project knowledge
```

## CLAUDE.md

The most important file for Claude Code. Place in project root.

### Template

```markdown
# CLAUDE.md

## Project Overview
[Brief description of what this project does]

## Tech Stack
- [Framework/language]
- [Database]
- [Key dependencies]

## Commands
- `bun install` - Install dependencies
- `bun dev` - Start development server
- `bun test` - Run tests
- `bun build` - Build for production

## Architecture
[Key directories and their purposes]

## Code Style
- [Linting rules]
- [Naming conventions]
- [Patterns to follow]

## Important Notes
- [Gotchas and things Claude should know]
```

### Location Precedence

Claude reads CLAUDE.md files in this order (all are included):

1. `~/.claude/CLAUDE.md` - Personal global instructions
2. `~/CLAUDE.md` - Home directory instructions
3. `./CLAUDE.md` - Project root
4. `./src/CLAUDE.md` - Subdirectory (and any other CLAUDE.md files)

**Tip:** Use subdirectory CLAUDE.md files for module-specific guidance.

## Settings Files

### .claude/settings.json

Project settings committed to version control.

```json
{
  "permissions": {
    "allow": [
      "Bash(bun:*)",
      "Bash(git:*)",
      "Read",
      "Write",
      "Edit"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(sudo:*)"
    ]
  },
  "env": {
    "NODE_ENV": "development"
  },
  "hooks": {}
}
```

### .claude/settings.local.json

Personal overrides (add to .gitignore).

```json
{
  "permissions": {
    "allow": [
      "Bash(docker:*)"
    ]
  },
  "env": {
    "DEBUG": "true"
  }
}
```

### ~/.claude/settings.json

User-level settings (applies to all projects).

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep"
    ],
    "deny": []
  },
  "env": {}
}
```

## Permission Setup

### Permission Patterns

| Pattern | Matches |
|---------|---------|
| `Read` | All Read operations |
| `Bash(git:*)` | All git commands |
| `Bash(npm install:*)` | npm install with any args |
| `Bash(bun test src/**:*)` | bun test on src directory |
| `Write(*.md)` | Write to markdown files |
| `Edit(src/**)` | Edit files in src/ |

### Recommended Permissions by Project Type

**Node.js/Bun:**
```json
{
  "permissions": {
    "allow": [
      "Bash(bun:*)", "Bash(npm:*)", "Bash(npx:*)",
      "Bash(git:*)",
      "Read", "Write", "Edit", "Glob", "Grep"
    ],
    "deny": [
      "Bash(rm -rf /*))",
      "Bash(sudo:*)"
    ]
  }
}
```

**Python:**
```json
{
  "permissions": {
    "allow": [
      "Bash(python:*)", "Bash(pip:*)", "Bash(uv:*)",
      "Bash(pytest:*)",
      "Bash(git:*)",
      "Read", "Write", "Edit", "Glob", "Grep"
    ],
    "deny": [
      "Bash(rm -rf /*))",
      "Bash(sudo:*)"
    ]
  }
}
```

**Rust:**
```json
{
  "permissions": {
    "allow": [
      "Bash(cargo:*)", "Bash(rustc:*)",
      "Bash(git:*)",
      "Read", "Write", "Edit", "Glob", "Grep"
    ],
    "deny": [
      "Bash(rm -rf /*))",
      "Bash(sudo:*)"
    ]
  }
}
```

## MCP Server Configuration

### .mcp.json (Shared)

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Adding Servers

```bash
# Add to project (creates .mcp.json)
claude mcp add --scope project memory -- npx -y @modelcontextprotocol/server-memory

# Add to user (all projects)
claude mcp add --scope user github -- npx -y @modelcontextprotocol/server-github

# Add remote server
claude mcp add --transport http context7 https://mcp.context7.com/v1/mcp
```

## Hooks Setup

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.sh"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"Project: $(basename $CLAUDE_PROJECT_DIR)\""
          }
        ]
      }
    ]
  }
}
```

## Team Considerations

### What to Commit

| File | Commit? | Reason |
|------|---------|--------|
| `.claude/settings.json` | Yes | Shared project config |
| `.claude/settings.local.json` | No | Personal overrides |
| `.claude/commands/` | Yes | Team slash commands |
| `.claude/skills/` | Yes | Team knowledge |
| `.claude/hooks/` | Yes | Shared automation |
| `.mcp.json` | Yes | Shared MCP servers |
| `CLAUDE.md` | Yes | Project knowledge |

### .gitignore Additions

```gitignore
# Claude Code personal settings
.claude/settings.local.json
.claude/*.local.json

# MCP server data (if any)
.mcp-data/
```

### Team Onboarding

1. Clone repository
2. Run `/init` to verify Claude Code setup
3. Create personal `.claude/settings.local.json` for overrides
4. Set required environment variables
5. Run `/project-status` (if command exists) to verify

## Validation Commands

```bash
# Check Claude Code settings
claude config list

# Verify MCP servers
claude mcp list

# Check permissions
/permissions

# View hooks
/hooks
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Settings not loading | Check JSON syntax with `jq . .claude/settings.json` |
| MCP server not starting | Run `claude mcp logs <name>` |
| Permissions not applying | Check precedence: local > project > user |
| CLAUDE.md not read | Ensure it's in project root or cwd |
| Hooks not running | Verify script is executable |

## Reference Files

| File | Contents |
|------|----------|
| [CONFIGURATION.md](./CONFIGURATION.md) | Deep dive into all configuration options |
| [PERMISSIONS.md](./PERMISSIONS.md) | Permission patterns and security |
| [CHECKLIST.md](./CHECKLIST.md) | Complete setup and migration checklists |
