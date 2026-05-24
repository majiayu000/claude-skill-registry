---
name: plugin-master
description: |
  Complete guide to Claude Code plugin development, architecture, directory layout, components, and marketplace publishing.
  PROACTIVELY activate for: (1) creating a plugin from scratch, (2) building or scaffolding a plugin, (3) writing plugin.json, (4) adding commands/agents/skills/hooks/MCP servers, (5) packaging code as a plugin, (6) publishing to a marketplace, (7) validating plugin structure, (8) marketplace.json registration, (9) cross-platform compatibility, (10) version and metadata sync.
  Provides: plugin schema, layouts, workflows, and publishing steps.
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

```text
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

### Step 4 (conditional): Attribution manifest

If the plugin ships any vendored, derived, or licensed third-party content, create `NOTICES.md` at the plugin root **before** registering in the marketplace. Treat it as a first-class shipping artifact alongside `plugin.json` and `README.md`, not as doc polish. See `references/publishing-guide.md` ("Licensed / Vendored / Derived Content" checklist) for the structural integrity, license-text-preservation, and cross-reference requirements.

If the plugin contains no third-party content, skip this step.

### Step 5: Register in Marketplace

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
  Brief role summary. PROACTIVELY activate for: (1) trigger, (2) trigger, ..., (N) trigger. Provides: capability list.

  # Optional. Include 3-5 <example> blocks ONLY when the agent body
  # exceeds 2,500 words. Lean orchestrators omit them by design.
  # See agent-development "Example-block requirement by agent body size".
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
| Agent not triggering | Check description has `PROACTIVELY activate for:` enumeration. Add 3-5 `<example>` blocks only if agent body > 2,500 words — see `agent-development` SKILL.md "Example-block requirement by agent body size". Lean orchestrators are exempt. |
| Marketplace not found | Ensure repo is public, check path in marketplace.json |

## Additional Resources

For detailed information, see:

- **`references/manifest-reference.md`** - Complete plugin.json fields
- **`references/component-patterns.md`** - Advanced component patterns
- **`references/publishing-guide.md`** - Marketplace publishing details
- **`examples/minimal-plugin.md`** - Simplest working plugin
- **`examples/full-plugin.md`** - Complete plugin with all features
