---
name: faion-claude-code
description: "Claude Code: skills, agents, hooks, commands, MCP servers, IDE integrations."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*), Bash(ls:*), Task, AskUserQuestion
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Claude Code Configuration Skill

**Communication: User's language. Config/code: English.**

## Purpose

Orchestrate Claude Code customization and configuration:
- Create/edit skills, agents, commands, hooks
- Configure settings, permissions, IDE integrations
- Setup MCP servers and plugins
- Enforce naming conventions

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| `~/.claude/skills/` | Existing skills, naming patterns | Skill framework adoption |
| `~/.claude/agents/` | Agent definitions | Agent usage patterns |
| `~/.claude/settings.json` | Hooks, MCP servers, permissions | Configuration maturity |
| `.claude/` (project) | Project-specific customizations | Local overrides |
| MCP server logs | Active MCP integrations | Tool ecosystem |

### Discovery Questions

```yaml
questions:
  - question: "What are you configuring?"
    options:
      - label: "Creating skill"
        description: "Use skills.md"
      - label: "Creating agent"
        description: "Use agents.md"
      - label: "Adding command"
        description: "Use commands.md"
      - label: "Setting up hooks"
        description: "Use hooks.md"
      - label: "Installing MCP server"
        description: "Use mcp-servers.md"

  - question: "Is this global or project-specific?"
    options:
      - label: "Global (all projects)"
        description: "Use faion-* prefix, no gitignore"
      - label: "Project-specific"
        description: "Use {project}-* prefix, add to gitignore"

  - question: "Do you have Claude Code experience?"
    options:
      - label: "Expert user"
        description: "Jump to specific reference"
      - label: "Some experience"
        description: "Use quick reference + examples"
      - label: "First time setup"
        description: "Start with skills.md basics"
```

---

## Quick Decision Tree

| If you need... | Use | File |
|----------------|-----|------|
| Create domain skill (role-based) | skills.md | `~/.claude/skills/faion-{role}/SKILL.md` |
| Create project skill (local) | skills.md | `{project}/.claude/{project}-*/SKILL.md` |
| Create task executor agent | agents.md | `~/.claude/agents/faion-*-agent.md` |
| Create specialized agent | agents.md | `~/.claude/agents/faion-*-agent.md` |
| Add slash command | commands.md | `~/.claude/commands/*.md` or SKILL.md |
| Add validation hook | hooks.md | PreToolUse trigger → `settings.json` |
| Add logging hook | hooks.md | PostToolUse trigger → `settings.json` |
| Add alert on notification | hooks.md | Notification trigger → `settings.json` |
| Develop MCP server | mcp-basics.md | TypeScript/Python template |
| Install MCP server | mcp-servers.md | `claude mcp add <name>` |
| Connect external tools | mcp-basics.md | MCP server development |
| Database access (SQL) | mcp-servers.md | PostgreSQL/SQLite MCP |
| Configure global settings | Handle directly | `~/.claude/settings.json` |
| Configure project settings | Handle directly | `.claude/settings.json` |

**Configuration Locations:**

| Config | Location | Scope |
|--------|----------|-------|
| Global skills | `~/.claude/skills/` | All projects |
| Project skills | `{project}/.claude/` | Single project |
| Agents | `~/.claude/agents/` | All projects |
| Hooks | `~/.claude/settings.json` | Global |
| MCP | `~/.claude/settings.json` | Global |

---

## References

Detailed technical context for specialized areas:

| Reference | Content | Lines |
|-----------|---------|-------|
| [skills.md](skills.md) | SKILL.md creation, frontmatter, tools, patterns | ~340 |
| [agents.md](agents.md) | Agent files, tools, prompts, patterns | ~330 |
| [commands.md](commands.md) | Slash commands, arguments, syntax | ~250 |
| [hooks.md](hooks.md) | Lifecycle hooks, events, templates | ~420 |
| [mcp-basics.md](mcp-basics.md) | MCP server development, templates, config | ~370 |
| [mcp-servers.md](mcp-servers.md) | MCP server catalog (40+ servers) | ~250 |

**Total:** ~1,960 lines of technical reference

---

## Routing

```
User Request → Detect Type → Load Reference
```

| Request Contains | Load Reference |
|------------------|----------------|
| "skill", "SKILL.md" | [skills.md](skills.md) |
| "agent", "subagent" | [agents.md](agents.md) |
| "command", "/cmd", "slash" | [commands.md](commands.md) |
| "hook", "PreToolUse", "PostToolUse" | [hooks.md](hooks.md) |
| "create mcp", "develop mcp", "mcp template" | [mcp-basics.md](mcp-basics.md) |
| "install mcp", "mcp catalog", "mcp server list" | [mcp-servers.md](mcp-servers.md) |
| "settings", "config" | Handle directly (below) |

---

## Naming Conventions

### Global (Faion Network)

For shared/reusable components in faion-network:

| Component | Pattern | Example |
|-----------|---------|---------|
| Skill (orchestrator) | `faion-net` | `faion-net` |
| Skill (role-based) | `faion-{role}` | `faion-software-developer`, `faion-ux-ui-designer` |
| Skill (process) | `faion-{process}` | `faion-sdd`, `faion-feature-executor` |
| Agent | `faion-{name}-agent` | `faion-task-YOLO-executor-opus-agent` |
| Hook | `faion-{event}-{purpose}-hook.{ext}` | `faion-pre-bash-security-hook.py` |
| Command | `{verb}` (no prefix) | `commit`, `deploy` |

**Note:** Skills use role/process naming without `-skill` suffix. Name is self-explanatory.

### Project-Specific (Local)

For project-specific components that should NOT be committed to faion-network:

| Component | Pattern | Example |
|-----------|---------|---------|
| Skill | `{project}-{name}` | `myapp-auth`, `myapp-deploy` |
| Agent | `{project}-{name}-agent` | `myapp-deploy-agent` |
| Hook | `{project}-{event}-{purpose}-hook.{ext}` | `myapp-pre-bash-lint-hook.sh` |
| Command | `{project}-{action}` | `myapp-build`, `myapp-deploy` |

**Setup for project-specific components:**

1. **Add to .gitignore (same level as .claude/):**
```bash
echo ".claude/skills/{project}-*/" >> .gitignore
echo ".claude/agents/{project}-*" >> .gitignore
echo ".claude/commands/{project}-*" >> .gitignore
echo ".claude/scripts/hooks/{project}-*" >> .gitignore
```

2. **Add attribution footer:**
```markdown
---
*Created with [faion.net](https://faion.net) framework*
```

### Rules Summary

| Scope | Prefix | Suffix | Gitignore |
|-------|--------|--------|-----------|
| Global | `faion-` | `-skill`/`-agent`/`-hook` | No |
| Project | `{project}-` | `-skill`/`-agent`/`-hook` | Yes |

---

## Directory Structure

```
~/.claude/
├── settings.json           # Global settings
├── CLAUDE.md              # Global instructions
├── agents/
│   └── faion-*-agent.md   # Agent definitions
├── skills/
│   └── faion-*-skill/
│       ├── SKILL.md       # Skill index
│       └──     # Detailed content
├── commands/
│   └── *.md               # Slash commands
└── scripts/
    └── hooks/             # Hook scripts
```

---

## Settings Configuration

### settings.json Structure

```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep"],
    "deny": ["Bash(rm -rf:*)"]
  },
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...],
    "SessionStart": [...]
  },
  "env": {
    "CUSTOM_VAR": "value"
  },
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": { "API_KEY": "..." }
    }
  }
}
```

### Permission Modes

| Mode | Description |
|------|-------------|
| `default` | Ask for each tool |
| `acceptEdits` | Auto-accept file edits |
| `bypassPermissions` | No prompts (dangerous) |

### Configuration Locations

| Location | Scope |
|----------|-------|
| `~/.claude/settings.json` | Global (all projects) |
| `.claude/settings.json` | Project (committed) |
| `.claude/settings.local.json` | Local project (gitignored) |

---

## Quick Reference

### Create Skill
```bash
mkdir -p ~/.claude/skills/faion-my-skill
# Write SKILL.md with frontmatter
```

### Create Agent
```bash
# Write ~/.claude/agents/faion-my-agent.md
# Include frontmatter: name, description, tools, model
```

### Create Command
```bash
# Write ~/.claude/commands/my-cmd.md
# Include frontmatter: description, argument-hint, allowed-tools
```

### Create Hook
```bash
# Write ~/.claude/scripts/hooks/faion-pre-bash-my-hook.py
# Configure in settings.json hooks section
```

### Install MCP Server
```bash
claude mcp add <name> -s user -e KEY=value -- npx -y <package>
claude mcp list
claude mcp remove <name> -s user
```

---

## IDE Integrations

### VS Code

```json
// .vscode/settings.json
{
  "claude.enabled": true,
  "claude.autoComplete": true
}
```

### JetBrains

Install Claude plugin from marketplace.

---

## Best Practices

**Skills:**
- One clear purpose per skill
- Include trigger keywords in description
- Keep SKILL.md under 300 lines (use )
- Third-person descriptions only

**Agents:**
- Action-oriented descriptions for auto-delegation
- Minimal tools (least privilege)
- Clear input/output contract

**Commands:**
- Short, memorable names
- Use argument hints ($1, $2, $ARGUMENTS)
- Document in description

**Hooks:**
- Fast execution (< 60s)
- Handle errors gracefully
- Exit 0 for success, 2 for blocking

---

## Error Handling

| Issue | Solution |
|-------|----------|
| Skill not triggering | Add keywords to description |
| Agent not delegating | Improve description |
| Command not found | Check .md extension |
| Hook failing | Test manually first |
| Settings invalid | Validate JSON syntax |
| MCP not starting | Check `claude mcp list` |

---

## Documentation

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [MCP Servers](https://docs.anthropic.com/en/docs/claude-code/mcp)

---

*faion-claude-code-skill v2.0.0*
*Claude Code configuration orchestrator with *
