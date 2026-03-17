---
name: plugin-master
description: |
  Complete Claude Code plugin development system. PROACTIVELY activate when users want to:
  (1) Create/build/make plugins with 2025 features
  (2) Add skills/commands/agents to plugins
  (3) Package existing code as plugins
  (4) Publish plugins to marketplace
  (5) Validate plugin structure
  (6) Get plugin development guidance
  Autonomously creates production-ready plugins with proper structure and best practices.
license: MIT
---

# Plugin Development Guide

## Quick Reference

| Component | Location | Required |
|-----------|----------|----------|
| Plugin manifest | `.claude-plugin/plugin.json` | Yes |
| Commands | `commands/*.md` | No (auto-discovered) |
| Agents | `agents/*.md` | No (auto-discovered) |
| Skills | `skills/*/SKILL.md` | No (auto-discovered) |
| Hooks | `hooks/hooks.json` | No |
| MCP Servers | `.mcp.json` | No |

| Task | Action |
|------|--------|
| Create plugin | Ask: "Create a plugin for X" |
| Validate plugin | Run: `/validate-plugin` |
| Install from marketplace | `/plugin marketplace add user/repo` then `/plugin install name@user` |

## Critical Rules

### Directory Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # MUST be inside .claude-plugin/
├── agents/
│   └── domain-expert.md
├── commands/
├── skills/
│   └── skill-name/
│       ├── SKILL.md
│       ├── references/
│       └── examples/
└── README.md
```

### Plugin.json Schema

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Complete [domain] expertise. PROACTIVELY activate for: (1) ...",
  "author": {
    "name": "Author Name",
    "email": "email@example.com"
  },
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

**Validation Rules:**
- `author` MUST be an object `{ "name": "..." }` - NOT a string
- `version` MUST be a string `"1.0.0"` - NOT a number
- `keywords` MUST be an array `["word1", "word2"]` - NOT a string
- Do NOT include `agents`, `skills`, `slashCommands` - these are auto-discovered

### YAML Frontmatter (REQUIRED)

ALL markdown files in agents/, commands/, skills/ MUST begin with frontmatter:

```markdown
---
description: Brief description of what this component does
---

# Content...
```

**Without frontmatter, components will NOT load.**

## Plugin Design Philosophy (2025)

### Agent-First Design

- **Primary interface**: ONE expert agent named `{domain}-expert`
- **Minimal commands**: Only 0-2 for automation workflows
- **Why**: Users want conversational interaction, not command menus

**Naming Standard:**
- `docker-master` → agent named `docker-expert`
- `terraform-master` → agent named `terraform-expert`

### Progressive Disclosure for Skills

Skills use three-tier loading:
1. **Frontmatter** - Loaded at startup for triggering
2. **SKILL.md body** - Loaded when skill activates
3. **references/** - Loaded only when specific detail needed

This enables unbounded capacity without context bloat.

## Creating a Plugin

### Step 1: Detect Repository Context

Before creating files, check:
```bash
# Check if in marketplace repo
if [[ -f .claude-plugin/marketplace.json ]]; then
    PLUGIN_DIR="plugins/PLUGIN_NAME"
else
    PLUGIN_DIR="PLUGIN_NAME"
fi

# Get author from git config
AUTHOR_NAME=$(git config user.name)
AUTHOR_EMAIL=$(git config user.email)
```

### Step 2: Create Structure

```bash
mkdir -p $PLUGIN_DIR/.claude-plugin
mkdir -p $PLUGIN_DIR/agents
mkdir -p $PLUGIN_DIR/skills/domain-knowledge
```

### Step 3: Create Files

1. **plugin.json** - Manifest with metadata
2. **agents/domain-expert.md** - Primary expert agent
3. **skills/domain-knowledge/SKILL.md** - Core knowledge
4. **README.md** - Documentation

### Step 4: Register in Marketplace

**CRITICAL**: If `.claude-plugin/marketplace.json` exists at repo root, you MUST add the plugin:

```json
{
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "Same as plugin.json description",
      "version": "1.0.0",
      "author": { "name": "Author" },
      "keywords": ["same", "as", "plugin.json"]
    }
  ]
}
```

## Component Types

### Commands

User-initiated slash commands in `commands/*.md`:

```markdown
---
description: What this command does
---

# Command Name

Instructions for Claude to execute...
```

### Agents

Autonomous subagents in `agents/*.md`:

```markdown
---
name: agent-name
description: |
  Use this agent when... Examples:
  <example>
  Context: ...
  user: "..."
  assistant: "..."
  <commentary>Why trigger</commentary>
  </example>
model: inherit
color: blue
---

System prompt for agent...
```

### Skills

Dynamic knowledge in `skills/skill-name/SKILL.md`:

```markdown
---
name: skill-name
description: When to use this skill...
---

# Skill content with progressive disclosure...
```

### Hooks

Event automation in `hooks/hooks.json`:

```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint.sh"
    }]
  }]
}
```

**Events**: PreToolUse, PostToolUse, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, Notification, Stop, SubagentStop

## Best Practices

### Naming Conventions

- **Plugins**: `kebab-case` (e.g., `code-review-helper`)
- **Commands**: verb-based (e.g., `review-pr`, `run-tests`)
- **Agents**: role-based (e.g., `code-reviewer`, `test-generator`)
- **Skills**: topic-based (e.g., `api-design`, `error-handling`)

### Portability

Use `${CLAUDE_PLUGIN_ROOT}` for all internal paths:

```json
"command": "${CLAUDE_PLUGIN_ROOT}/scripts/run.sh"
```

Never use hardcoded absolute paths.

### Platform Notes

- **Windows**: Use GitHub marketplace installation (local paths may fail)
- **Git Bash/MinGW**: Detect with `$MSYSTEM`, use GitHub method
- **Mac/Linux**: All installation methods work

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Plugin not loading | Check plugin.json is in `.claude-plugin/` |
| Commands missing | Verify frontmatter has `description` field |
| Agent not triggering | Add `<example>` blocks to description |
| Marketplace not found | Ensure repo is public, check path in marketplace.json |

## Additional Resources

For detailed information, see:

- **`references/manifest-reference.md`** - Complete plugin.json fields
- **`references/component-patterns.md`** - Advanced component patterns
- **`references/publishing-guide.md`** - Marketplace publishing details
- **`examples/minimal-plugin.md`** - Simplest working plugin
- **`examples/full-plugin.md`** - Complete plugin with all features
