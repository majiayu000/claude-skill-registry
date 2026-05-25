---
name: advanced-features-2025
description: |
  Advanced 2025 Claude Code plugin features. PROACTIVELY activate for:
  (1) Agent Skills with progressive disclosure
  (2) Hook automation (PreToolUse, PostToolUse, etc.)
  (3) MCP server integration
  (4) Repository-level configuration
  (5) Team plugin distribution
  (6) Context efficiency optimization
  Provides cutting-edge plugin capabilities and patterns.
license: MIT
---

# Advanced Plugin Features (2025)

## Quick Reference

| Feature | Location | Purpose |
|---------|----------|---------|
| Agent Skills | `skills/*/SKILL.md` | Dynamic knowledge loading |
| Hooks | `hooks/hooks.json` | Event automation |
| MCP Servers | `.mcp.json` | External integrations |
| Team Config | `.claude/settings.json` | Repository plugins |

| Hook Event | When Fired | Use Case |
|------------|------------|----------|
| PreToolUse | Before tool | Validation |
| PostToolUse | After tool | Testing, linting |
| SessionStart | Session begins | Logging, setup |
| SessionEnd | Session ends | Cleanup |
| UserPromptSubmit | Prompt submitted | Preprocessing |
| PreCompact | Before compact | State save |
| Notification | Notification shown | Custom alerts |
| Stop | User stops | Cleanup |
| SubagentStop | Subagent ends | Logging |

| Variable | Purpose |
|----------|---------|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin installation path |
| `${TOOL_INPUT_*}` | Tool input parameters |

## Agent Skills

### Concept

Skills are dynamically loaded based on task context, enabling:
- **Unbounded capacity**: Knowledge split across files
- **Context efficiency**: Only load what's needed
- **Progressive disclosure**: Three-tier loading

### Three-Tier Loading

1. **Frontmatter**: Loaded at startup (triggers)
2. **SKILL.md body**: Loaded on activation
3. **references/**: Loaded when detail needed

### Structure

```
skills/
└── skill-name/
    ├── SKILL.md           # Core content
    ├── references/        # Detailed docs
    │   └── deep-dive.md
    ├── examples/          # Working code
    │   └── example.md
    └── scripts/           # Utilities
        └── tool.sh
```

### SKILL.md Format

```markdown
---
name: skill-name
description: |
  When to activate this skill. Include:
  (1) Use case 1
  (2) Use case 2
  Provides: what it offers
---

# Skill Title

## Quick Reference
[Tables, key points]

## Core Content
[Essential information - keep lean]

## Additional Resources
See `references/` for detailed guidance.
```

## Hooks

### Configuration

**Inline in plugin.json:**
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

**Separate hooks.json:**
```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "command",
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
      "timeout": 5000
    }]
  }]
}
```

### Matchers

- `Write` - File writes
- `Edit` - File edits
- `Bash` - Shell commands
- `Write|Edit` - Multiple tools
- `.*` - Any tool (use sparingly)

### Common Patterns

**Auto-test after changes:**
```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/run-tests.sh"
    }]
  }]
}
```

**Validate before Bash:**
```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-cmd.sh"
    }]
  }]
}
```

## MCP Server Integration

### Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/mcp/server.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

### External Services

```json
{
  "mcpServers": {
    "stripe": {
      "command": "npx",
      "args": ["-y", "@stripe/mcp-server"],
      "env": {
        "STRIPE_API_KEY": "${STRIPE_API_KEY}"
      }
    }
  }
}
```

## Repository Configuration

### Team Distribution

Create `.claude/settings.json` at repo root:

```json
{
  "extraKnownMarketplaces": [
    "company/internal-plugins"
  ],
  "plugins": {
    "enabled": [
      "deployment-helper@company",
      "code-standards@company"
    ]
  }
}
```

### Workflow

1. Maintainer creates `.claude/settings.json`
2. Team members clone repo
3. Trust folder when prompted
4. Plugins install automatically

## Best Practices

### Progressive Disclosure

- Keep SKILL.md under 500 lines
- Move details to `references/`
- Use `examples/` for working code
- Reference files with relative paths

### Hooks

- Use specific matchers (avoid `.*`)
- Set reasonable timeouts
- Use `${CLAUDE_PLUGIN_ROOT}` for paths
- Test scripts independently

### MCP

- Document required env vars
- Provide setup instructions
- Use environment variables for secrets
- Test connection before distribution

## Additional Resources

For detailed patterns, see:
- **`references/hooks-advanced.md`** - Complete hook patterns
- **`references/mcp-patterns.md`** - MCP integration examples
- **`references/team-distribution.md`** - Repository configuration
- **`examples/hook-scripts.md`** - Working hook scripts
