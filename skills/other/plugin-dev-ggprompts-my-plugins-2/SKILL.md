---
name: plugin-dev
description: "Claude Code plugin development - create plugins, skills, commands, agents, hooks, MCP servers, and marketplaces. Use when: 'create a plugin', 'add a skill', 'write a command', 'configure hooks', 'integrate MCP server', 'build marketplace', 'How do plugins work?', 'What goes in plugin.json?'"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Claude Code Plugin Development

Comprehensive guidance for creating well-structured plugins, skills, hooks, agents, commands, and MCP integrations.

## Core Principles (Anthropic Official)

1. **Composable** - Multiple skills work together seamlessly, Claude coordinates automatically
2. **Portable** - Same format works across Claude apps, Claude Code, and Claude API
3. **Efficient** - Progressive disclosure loads only what's needed (description → SKILL.md → references)
4. **Powerful** - Combines prompts + executable code for complete workflows
5. **Secure** - Never hardcode secrets, use `${CLAUDE_PLUGIN_ROOT}` for paths

## Critical Budget Limits

| Limit | Value | Consequence if Exceeded |
|-------|-------|------------------------|
| All skill descriptions combined | 15,000 chars | Silent filtering, skills won't activate |
| Individual description | 1,024 chars | Truncation |
| SKILL.md body | 5,000 words | Context saturation, partial execution |
| Target per description | 300-400 chars | Allows ~40 skills safely |

## Quick Start

### Create a New Plugin

```bash
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/skills/my-skill/references

cat > my-plugin/.claude-plugin/plugin.json << 'PLUGIN'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does"
}
PLUGIN

cat > my-plugin/skills/my-skill/SKILL.md << 'SKILL'
---
name: my-skill
description: Use when creating X, configuring Y, or analyzing Z
---

# My Skill

Instructions for Claude when this skill activates...
SKILL
```

### Install and Test

```bash
# Symlink to Claude's plugin directory
ln -s $(pwd)/my-plugin ~/.claude/plugins/my-plugin

# Restart Claude Code to load
/restart

# Test the skill
/my-plugin:my-skill
```

## Component Reference

Choose a topic for detailed guidance:

### 📁 **@references/structure.md** - Plugin Directory Structure
- Standard plugin layout
- Marketplace vs standalone patterns
- Auto-discovery rules
- Portable path references (`${CLAUDE_PLUGIN_ROOT}`)
- Common troubleshooting

### 🎯 **@references/skills-reference.md** - Creating Skills
- SKILL.md format and frontmatter
- Progressive disclosure patterns
- Bundled resources (scripts/, references/, assets/)
- Description best practices with trigger phrases
- Writing style (imperative, not second person)
- Validation checklist

### 💬 **@references/commands-reference.md** - Slash Commands
- Command file format with frontmatter
- Dynamic arguments (`$1`, `$2`, `@$1`)
- Bash execution inline
- Tool restrictions (allowed-tools)
- Organization (flat vs namespaced)
- Plugin command portability

### 🤖 **@references/agents-reference.md** - Subagents
- Agent frontmatter (name, description, model, color, tools)
- Name validation rules
- Description with examples
- Color guidelines by purpose
- Tool restriction patterns
- System prompt best practices

### 🎣 **@references/hooks-reference.md** - Event Hooks
- Hook types (prompt-based vs command)
- Event types (PreToolUse, PostToolUse, Stop, etc.)
- Configuration (hooks.json format)
- Matchers (exact, wildcard, regex)
- Output structure and exit codes
- Security best practices
- Environment variables

### 🔌 **@references/mcp-reference.md** - MCP Integration
- MCP server configuration (.mcp.json)
- Server types (stdio, SSE, HTTP, WebSocket)
- Tool naming conventions
- Environment variable usage
- Security and testing

### 🏪 **@references/marketplace-reference.md** - Marketplaces
- Standalone vs marketplace patterns
- marketplace.json schema
- Skills array pattern
- Bundle plugin pattern
- Common mistakes to avoid
- Team configuration

### 📋 **@references/plugin-reference.md** - Plugin Manifest
- plugin.json required fields
- Optional metadata
- Custom component paths
- Installation and deployment

### ⚙️ **@references/settings.md** - Plugin Settings
- .local.md settings files
- YAML frontmatter for configuration
- Reading settings in hooks
- Best practices and gitignore

## Common Patterns

### Minimal Skill

```yaml
---
name: simple-skill
description: Use when user asks to "do X" or "configure Y"
---

# Simple Skill

Step-by-step instructions...

1. Check if condition exists
2. Execute action
3. Verify result

For detailed patterns, see @references/advanced-patterns.md
```

### Command with Arguments

```markdown
---
description: Review code for security issues
allowed-tools: Read, Grep
argument-hint: [file] [severity]
---

Review @$1 for security issues.
Focus on severity level: $2

Use these patterns:
- SQL injection
- XSS vulnerabilities  
- Hardcoded credentials
```

### Hook with Validation

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
        "timeout": 30
      }]
    }]
  }
}
```

## File Organization

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Manifest
├── commands/                 # Slash commands
│   └── action.md
├── agents/                   # Subagents
│   └── analyzer.md
├── skills/                   # Skills
│   └── my-skill/
│       ├── SKILL.md         # Main skill file
│       ├── references/      # Detailed docs
│       ├── scripts/         # Executable code
│       └── assets/          # Templates, images
├── hooks/
│   └── hooks.json           # Event handlers
└── .mcp.json                # MCP servers
```

## Development Workflow

1. **Plan** - Identify what your plugin should do
2. **Structure** - Create directory layout (see @references/structure.md)
3. **Implement** - Write skills, commands, or agents
4. **Configure** - Add hooks or MCP servers if needed
5. **Test** - Install and verify functionality
6. **Iterate** - Refine based on usage
7. **Document** - Update README and examples

## Best Practices

| Practice | Reason |
|----------|--------|
| Keep SKILL.md under 2000 words | Move details to references/ for progressive disclosure |
| Use specific trigger phrases | "when user asks to 'create X'" not "provides guidance" |
| Imperative writing style | "Parse the config" not "You should parse" |
| Portable paths | `${CLAUDE_PLUGIN_ROOT}` not hardcoded |
| Test after changes | `/restart` then invoke skill/command |
| Single responsibility | One focused purpose per component |

## Common Mistakes

| Mistake | Solution |
|---------|---------|
| Vague skill descriptions | Add specific trigger phrases users would say |
| 8000-word SKILL.md | Move content to references/, keep SKILL.md brief |
| Hardcoded paths | Use `${CLAUDE_PLUGIN_ROOT}` for portability |
| Missing frontmatter | All components need valid YAML frontmatter |
| Wrong directory structure | See @references/structure.md for correct layout |

## Validation

Before releasing a plugin:

- [ ] plugin.json has required `name` field
- [ ] All SKILL.md files have `name` and `description`
- [ ] Descriptions include specific trigger phrases
- [ ] All referenced files exist
- [ ] No hardcoded paths (use `${CLAUDE_PLUGIN_ROOT}`)
- [ ] Skills under 2000 words (details in references/)
- [ ] Commands have `argument-hint` if they take args
- [ ] Agents have valid name (3-50 chars, lowercase-hyphens)
- [ ] Hooks return valid JSON with proper exit codes
- [ ] README documents installation and usage

## Related Tools

- `/plugin-dev:create-plugin` - Interactive plugin scaffolding command
- `/plugin-dev:plugin-cli` - CLI commands for plugin management
- `/skill-creator:skill-creation` - Focused skill creation workflow
- `/agent-creator:agent-design` - Subagent design patterns
- `/mcp-builder:mcp-servers` - MCP server development

---

**Quick Navigation:**

| Need to... | See |
|-----------|-----|
| Understand plugin layout | @references/structure.md |
| Create a skill | @references/skills-reference.md |
| Add a slash command | @references/commands-reference.md |
| Configure a subagent | @references/agents-reference.md |
| Set up hooks | @references/hooks-reference.md |
| Integrate MCP server | @references/mcp-reference.md |
| Build a marketplace | @references/marketplace-reference.md |

**Status:** Consolidated plugin development skill with progressive disclosure pattern
