---
name: creating-plugins
description: Guide for creating full Claude Code plugins that bundle commands, agents, hooks, MCP servers, and LSP servers. Use when building distributable extensions, packaging multiple components together, or preparing plugins for marketplace distribution.
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
---

# Creating Plugins

Create Claude Code plugins that bundle multiple extension types for distribution via marketplaces.

## Quick Reference

| Element | Requirement |
|---------|-------------|
| Manifest location | `.claude-plugin/plugin.json` |
| Required field | `name` (kebab-case) |
| Component dirs | At plugin root, NOT inside `.claude-plugin/` |
| Command naming | `/plugin-name:command` (namespaced) |
| Testing | `claude --plugin-dir ./my-plugin` |

## Plugin vs Standalone

Choose the right approach for your use case:

| Approach | Command Names | Best For |
|----------|---------------|----------|
| **Standalone** (`.claude/`) | `/hello` | Personal workflows, single project |
| **Plugin** (`.claude-plugin/plugin.json`) | `/plugin-name:hello` | Sharing, distribution, reuse |

**Use standalone when:**
- Customizing for a single project
- Personal configuration (not shared)
- Quick experiments before packaging

**Use plugins when:**
- Sharing with team or community
- Same functionality across multiple projects
- Distributing through marketplace
- Bundling multiple component types

## Plugin Structure

```
my-plugin/
├── .claude-plugin/           # Metadata directory
│   └── plugin.json           # Required: plugin manifest
├── commands/                 # Slash commands (Markdown files)
│   ├── deploy.md
│   └── status.md
├── agents/                   # Subagent definitions
│   └── reviewer.md
├── skills/                   # Agent Skills
│   └── code-review/
│       └── SKILL.md
├── hooks/                    # Event handlers
│   └── hooks.json
├── .mcp.json                 # MCP server configurations
├── .lsp.json                 # LSP server configurations
├── scripts/                  # Hook and utility scripts
│   └── format.sh
└── README.md
```

**Critical:** Place `commands/`, `agents/`, `skills/`, `hooks/` at plugin root. Only `plugin.json` goes inside `.claude-plugin/`.

## Minimal Plugin Example

### 1. Create Structure

```bash
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/commands
```

### 2. Create Manifest

```json
// my-plugin/.claude-plugin/plugin.json
{
  "name": "my-plugin",
  "description": "Brief description of plugin purpose",
  "version": "1.0.0"
}
```

### 3. Add a Command

```markdown
<!-- my-plugin/commands/hello.md -->
---
description: Greet the user warmly
---

# Hello Command

Greet the user and ask how you can help today.
```

### 4. Test Locally

```bash
claude --plugin-dir ./my-plugin
```

Then run: `/my-plugin:hello`

## Component Types

Plugins can include any combination of:

| Component | Location | Format |
|-----------|----------|--------|
| Commands | `commands/` | Markdown with frontmatter |
| Agents | `agents/` | Markdown with capabilities |
| Skills | `skills/*/SKILL.md` | Markdown with YAML frontmatter |
| Hooks | `hooks/hooks.json` or inline | JSON configuration |
| MCP Servers | `.mcp.json` or inline | JSON configuration |
| LSP Servers | `.lsp.json` or inline | JSON configuration |

See [COMPONENTS.md](./COMPONENTS.md) for detailed documentation of each type.

## Manifest Schema

Required and optional fields:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What the plugin does",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/user/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

See [MANIFEST.md](./MANIFEST.md) for the complete schema.

## Environment Variables

Use `${CLAUDE_PLUGIN_ROOT}` for portable paths in hooks and servers:

```json
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
      }]
    }]
  }
}
```

## Distribution

### Via Marketplace

1. Create `marketplace.json` in repository
2. Host on GitHub/GitLab
3. Users add via `/plugin marketplace add`
4. Users install via `/plugin install plugin-name@marketplace`

### Team Configuration

Add to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "team-plugins": {
      "source": {
        "source": "github",
        "repo": "org/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "deploy-tools@team-plugins": true
  }
}
```

### Private Repository Support (2.1.5+)

Distribute plugins via private repositories using authentication tokens:

| Provider | Environment Variable | Notes |
|----------|---------------------|-------|
| GitHub | `GITHUB_TOKEN` or `GH_TOKEN` | PAT with `repo` scope |
| GitLab | `GITLAB_TOKEN` or `GL_TOKEN` | Token with `read_repository` scope |
| Bitbucket | `BITBUCKET_TOKEN` | App password or repo access token |

Set in shell config or when running Claude Code:

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

See [DISTRIBUTION.md](./DISTRIBUTION.md) for complete distribution guide.

## Workflow: Create a Plugin

### Prerequisites
- [ ] Claude Code 1.0.33+ installed
- [ ] Clear purpose for plugin
- [ ] Components identified

### Steps

1. **Create Structure**
   - [ ] Create plugin directory
   - [ ] Create `.claude-plugin/` subdirectory
   - [ ] Create component directories as needed

2. **Create Manifest**
   - [ ] Add `plugin.json` with name, description, version
   - [ ] Add author and metadata

3. **Add Components**
   - [ ] Create commands in `commands/`
   - [ ] Create agents in `agents/`
   - [ ] Create skills in `skills/*/SKILL.md`
   - [ ] Configure hooks in `hooks/hooks.json`
   - [ ] Configure MCP in `.mcp.json`
   - [ ] Configure LSP in `.lsp.json`

4. **Test Locally**
   - [ ] Run `claude --plugin-dir ./my-plugin`
   - [ ] Test each command
   - [ ] Verify agents in `/agents`
   - [ ] Confirm hooks fire correctly

5. **Prepare Distribution**
   - [ ] Add README.md
   - [ ] Create marketplace.json
   - [ ] Push to repository

### Validation
- [ ] Commands appear with namespace prefix
- [ ] All components load without errors
- [ ] Scripts are executable (`chmod +x`)
- [ ] Paths use `${CLAUDE_PLUGIN_ROOT}`

## CLI Commands

```bash
# Install plugin
claude plugin install plugin-name@marketplace --scope user

# Uninstall plugin
claude plugin uninstall plugin-name@marketplace

# Enable/disable plugin
claude plugin enable plugin-name@marketplace
claude plugin disable plugin-name@marketplace

# Update plugin
claude plugin update plugin-name@marketplace

# Debug loading
claude --debug
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Components inside `.claude-plugin/` | Move to plugin root |
| Absolute paths in hooks | Use `${CLAUDE_PLUGIN_ROOT}` |
| Scripts not executable | Run `chmod +x script.sh` |
| Missing shebang | Add `#!/bin/bash` first line |
| Referencing parent dirs | Use symlinks or restructure |

## Reference Files

| File | Contents |
|------|----------|
| [MANIFEST.md](./MANIFEST.md) | Complete manifest.json documentation |
| [COMPONENTS.md](./COMPONENTS.md) | All component type specifications |
| [DISTRIBUTION.md](./DISTRIBUTION.md) | Marketplace and team distribution |
