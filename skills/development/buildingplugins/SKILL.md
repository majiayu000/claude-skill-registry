---
name: buildingplugins
description: Use when creating, developing, or troubleshooting Claude Code plugins, skills, hooks, agents, commands, or MCP servers. For questions like "How do I create a plugin?", "What goes in plugin.json?", "How do skills work?", "Create a hook", or "Help me build a marketplace".
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
user-invocable: true
---

# Building Plugins for Claude Code

Expert guidance for creating well-structured plugins, skills, hooks, agents, commands, and MCP configurations.

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

## Plugin Structure

```
my-plugin/
├── plugin.json              # Manifest (at root for marketplace plugins)
├── commands/                # Slash commands (.md files)
├── skills/                  # Skills with SKILL.md
│   └── skill-name/
│       ├── SKILL.md
│       └── references/
├── agents/                  # Sub-agents (.md files)
├── hooks/
│   └── hooks.json           # Event handlers
├── .mcp.json                # MCP servers
└── README.md
```

## Quick Reference

### plugin.json (Minimum)
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What this plugin does"
}
```

### SKILL.md Frontmatter
```yaml
---
name: skill-name
description: Use when [trigger]. For [use cases].
allowed-tools: Read, Glob, Grep
model: sonnet
context: fork
user-invocable: true
---
```

### Agent Frontmatter
```yaml
---
name: agent-name
description: Expert in [domain]. Use for [tasks].
tools: [Read, Grep, Glob]
disallowedTools: [Write]
model: sonnet
permissionMode: default
color: blue
---
```

### Command Frontmatter
```yaml
---
description: What this command does
allowed-tools: Read, Write, Edit
argument-hint: "<required> [optional]"
---
```

### Hook Configuration
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh" }]
    }]
  }
}
```

## Detailed References

Load these for comprehensive documentation:

| Topic | Reference |
|-------|-----------|
| Plugin manifest, installation, validation | [references/plugin-reference.md](${CLAUDE_PLUGIN_ROOT}/skills/buildingplugins/references/plugin-reference.md) |
| SKILL.md format, progressive disclosure, scoped hooks | [references/skills-reference.md](${CLAUDE_PLUGIN_ROOT}/skills/buildingplugins/references/skills-reference.md) |
| Agent configuration, permission modes, built-ins | [references/agents-reference.md](${CLAUDE_PLUGIN_ROOT}/skills/buildingplugins/references/agents-reference.md) |
| Slash command format, arguments, execution | [references/commands-reference.md](${CLAUDE_PLUGIN_ROOT}/skills/buildingplugins/references/commands-reference.md) |
| Hook events, matchers, response formats | [references/hooks-reference.md](${CLAUDE_PLUGIN_ROOT}/skills/buildingplugins/references/hooks-reference.md) |
| MCP server types, CLI, configuration | [references/mcp-reference.md](${CLAUDE_PLUGIN_ROOT}/skills/buildingplugins/references/mcp-reference.md) |
| Marketplace creation and distribution | [references/marketplace-reference.md](${CLAUDE_PLUGIN_ROOT}/skills/buildingplugins/references/marketplace-reference.md) |

## Common Tasks

### Creating a New Plugin
1. Create directory with `plugin.json` at root
2. Add skills in `skills/skill-name/SKILL.md`
3. Add commands in `commands/command-name.md`
4. Test with `claude --plugin-dir ./my-plugin`
5. Validate with `claude plugin validate .`

### Creating a Skill
1. Create `skills/my-skill/SKILL.md` with frontmatter
2. Write concise instructions (<500 lines)
3. Add `references/` for detailed documentation
4. Test by invoking `/my-skill`

### Adding Hooks
1. Create `hooks/hooks.json`
2. Define event matchers and hook types
3. Restart Claude Code (hooks load at session start)

### Creating a Marketplace
1. Create `.claude-plugin/marketplace.json` at repo root
2. Add plugins with `plugin.json` at each plugin root
3. Test: `/plugin marketplace add ./my-marketplace`

## Development Methodology (Anthropic Engineering)

**Evaluation-First Approach:**
1. Run representative tasks WITHOUT skills first
2. Observe where Claude struggles or requires additional context
3. Build skills incrementally to address specific gaps
4. Use Claude-assisted skill authoring (ask Claude to draft skills after successful workflows)

**Self-Reflection Pattern:**
After completing a task successfully, ask Claude:
> "What worked well? Draft a SKILL.md that captures this workflow for next time."

## Best Practices Checklist

- [ ] Plugin name is lowercase with hyphens, 3-64 characters
- [ ] Description includes trigger phrases for auto-discovery
- [ ] Description under 400 chars (not 1024 max) to preserve budget
- [ ] Description uses third person voice
- [ ] Secrets use environment variables, never hardcoded
- [ ] Main files are concise, details in reference files
- [ ] Uses `${CLAUDE_PLUGIN_ROOT}` for all internal paths
- [ ] Semantic versioning (MAJOR.MINOR.PATCH)
- [ ] README with examples
- [ ] Tested with Haiku, Sonnet, and Opus
- [ ] Skills trigger on expected phrases (test auto-activation)
