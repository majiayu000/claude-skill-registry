---
name: marketplace-development
description: Create plugin marketplaces to bundle and distribute multiple plugins from a single repository
user-invocable: true
---

# Marketplace Development

This skill covers creating and managing plugin marketplaces - repositories that bundle multiple plugins for distribution.

## When to Use

Use this skill when:
- Creating a new plugin marketplace from scratch
- Converting standalone plugins to marketplace format
- Understanding marketplace vs standalone plugin patterns
- Configuring marketplace.json schema
- Troubleshooting plugin discovery in marketplaces

## Standalone vs Marketplace

Claude Code supports two distribution models:

| Aspect | Standalone | Marketplace |
|--------|------------|-------------|
| **Manifest** | `.claude-plugin/plugin.json` | `.claude-plugin/marketplace.json` |
| **Use case** | Single plugin = entire repo | Collection of plugins in one repo |
| **Installation** | Install entire plugin | Install individual plugins |
| **Plugin location** | N/A | `plugins/<name>/plugin.json` at root |

**Choose ONE approach** - having both manifests causes conflicts.

## Marketplace Structure

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json      # ONLY file here - lists all plugins
└── plugins/
    ├── tool-a/
    │   ├── plugin.json       # AT PLUGIN ROOT (not .claude-plugin/)
    │   ├── commands/
    │   ├── agents/
    │   └── skills/
    │       └── my-skill/
    │           └── SKILL.md
    └── tool-b/
        ├── plugin.json
        └── skills/
```

**Critical:** `.claude-plugin/` is ONLY at marketplace root, NOT inside each plugin. Each plugin has `plugin.json` at its directory root.

## marketplace.json Schema

### Minimal

```json
{
  "name": "my-marketplace",
  "plugins": [
    {
      "name": "tool-a",
      "description": "What tool-a does",
      "source": "./plugins/tool-a"
    }
  ]
}
```

### Full Schema

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "my-marketplace",
  "version": "1.0.0",
  "description": "Collection of plugins for X workflow",
  "owner": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "plugins": [
    {
      "name": "tool-a",
      "description": "What tool-a does",
      "version": "1.0.0",
      "source": "./plugins/tool-a",
      "category": "development",
      "tags": ["productivity", "automation"],
      "skills": [
        "./skills/skill-one",
        "./skills/skill-two"
      ]
    }
  ]
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Marketplace identifier (kebab-case) |
| `plugins` | array | List of available plugins |
| `plugins[].name` | string | Plugin identifier |
| `plugins[].description` | string | Brief plugin description |
| `plugins[].source` | string | Relative path to plugin directory |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `$schema` | string | Schema URL for validation |
| `version` | string | Marketplace version |
| `description` | string | Marketplace description |
| `owner` | object | `{name, email, url}` |
| `plugins[].version` | string | Individual plugin version |
| `plugins[].category` | string | Category for organization |
| `plugins[].tags` | array | Discovery keywords |
| `plugins[].skills` | array | Explicit skill paths (recommended) |

## Skills Array Pattern

Explicitly listing skills ensures proper discovery:

```json
{
  "plugins": [
    {
      "name": "document-skills",
      "description": "Document processing suite",
      "source": "./plugins/docs",
      "skills": [
        "./skills/xlsx",
        "./skills/docx",
        "./skills/pdf"
      ]
    }
  ]
}
```

**Why explicit skills?**
- Guarantees skills are discovered
- Avoids auto-discovery issues with nested paths
- Documents what each plugin provides

## Bundle Plugin Pattern

Offer "install everything" with a bundle pointing to root:

```json
{
  "plugins": [
    {"name": "tool-a", "source": "./plugins/tool-a"},
    {"name": "tool-b", "source": "./plugins/tool-b"},
    {
      "name": "complete-toolkit",
      "description": "All tools in one install",
      "source": "./",
      "category": "bundle"
    }
  ]
}
```

## Categories

Categories are **metadata only** - no visual grouping in UI. Use for:
- Semantic organization
- Documentation grouping
- Future filtering (not implemented)

## Common Mistakes

| Mistake | Correct |
|---------|---------|
| `plugins/X/.claude-plugin/plugin.json` | `plugins/X/plugin.json` |
| Both `plugin.json` and `marketplace.json` | Choose ONE approach |
| Symlinks in remote plugins | Use actual file copies |
| Missing skills in marketplace.json | Add explicit `skills` array |

## Installation

```bash
# Add marketplace from GitHub
/plugin add https://github.com/user/my-marketplace

# Add specific branch/tag
/plugin add https://github.com/user/my-marketplace#v1.0.0

# Install individual plugin
/plugin install tool-a@my-marketplace
```

## Team Configuration

Share marketplace with team via `settings.json`:

```json
{
  "extraKnownMarketplaces": [
    "https://github.com/company/internal-plugins"
  ]
}
```

These appear in `/plugins discover` for team members.

## Symlinks Warning

**Symlinks don't work for remote plugins.** When plugins are fetched from GitHub, symlink targets don't exist in the cache.

Instead of:
```
plugins/my-tool/commands/cmd.md -> ../../commands/cmd.md  # BROKEN
```

Use actual files:
```
plugins/my-tool/commands/cmd.md  # Actual file
```
