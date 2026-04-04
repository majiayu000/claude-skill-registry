---
name: agent-tuning
description: Configure and optimize AI coding agents (OpenCode/Claude). Use when setting up or improving agent behavior.
---

## Configuration Locations

### OpenCode
```
~/.config/opencode/
├── opencode.json          # Main config
├── agent/                 # Custom agent prompts
│   ├── oscar.md
│   ├── scout.md
│   ├── ivan.md
│   └── jester.md
├── skills/                # Reusable skills
│   └── <name>/SKILL.md
└── rules/                 # Always-active rules
    └── RULES.md
```

### Claude Code
```
~/.claude/
├── settings.json          # Main config
├── agents/                # Custom agents
│   └── <name>.md
├── skills/                # Reusable skills
│   └── <name>/SKILL.md
└── CLAUDE.md              # Global instructions
```

## Agent File Structure

### Frontmatter (YAML)
```yaml
---
tools:
  read: true
  write: false
  edit: false
  glob: true
  grep: true
  bash: true
  task: false
  webfetch: true
  todoread: true
  todowrite: true
  question: true    # Ask user questions
  skill: true       # Load skills

permission:
  bash:
    "git *": allow
    "gh *": allow
    "*": deny
---
```

### Tool Reference

| Tool | Purpose | Risk Level |
|------|---------|------------|
| `read` | Read files | Low |
| `write` | Create/overwrite files | High |
| `edit` | Modify files | High |
| `glob` | Find files by pattern | Low |
| `grep` | Search file contents | Low |
| `list` | List directories | Low |
| `bash` | Execute commands | Variable |
| `task` | Delegate to subagents | Low |
| `webfetch` | Fetch web content | Medium |
| `todoread` | Read task list | Low |
| `todowrite` | Update task list | Low |
| `question` | Ask user questions | Low |
| `skill` | Load skill files | Low |

## Permission Patterns

### Restrictive (Read-Only Agent)
```yaml
tools:
  read: true
  write: false
  edit: false
  bash: true

permission:
  bash:
    "ls *": allow
    "cat *": allow
    "git status": allow
    "*": deny
```

### Permissive (Full Access)
```yaml
tools:
  read: true
  write: true
  edit: true
  bash: true

permission:
  bash:
    "*": allow
```

### Balanced (Common Pattern)
```yaml
tools:
  read: true
  write: true
  edit: true
  bash: true

permission:
  bash:
    # Safe commands
    "ls *": allow
    "cat *": allow
    "head *": allow
    "tail *": allow
    
    # Git operations
    "git *": allow
    
    # Python in venv only
    ".venv/bin/*": allow
    
    # Deny everything else
    "*": deny
```

## Agent Roles

### Orchestrator (Oscar-style)
- Has `task: true` to delegate
- Has `question: true` to interact with user
- Limited direct tool access
- Coordinates other agents

### Researcher (Scout-style)
- Read-only access
- Has `webfetch: true`
- Full search tools (glob, grep)
- No `task` (can't delegate)

### Implementor (Ivan-style)
- Full write access
- Full bash access
- No `task` (can't delegate)
- Does the actual work

### Reviewer (Jester-style)
- Read-only access
- Different model for diversity
- Challenges assumptions
- No write access

## Tuning Tips

### 1. Start Restrictive
Begin with minimal permissions, expand as needed.

### 2. Use Specific Bash Patterns
```yaml
# Good - specific
".venv/bin/pytest *": allow

# Bad - too broad
"*pytest*": allow
```

### 3. Separate Concerns
- Orchestrator: coordinates
- Researcher: investigates
- Implementor: changes code
- Reviewer: validates

### 4. Test Permission Changes
After modifying permissions, test that:
- Allowed commands work
- Denied commands are blocked
- Edge cases are handled

## Debugging

### Check Active Config
```bash
# OpenCode
cat ~/.config/opencode/opencode.json

# View agent prompt
cat ~/.config/opencode/agent/<name>.md
```

### Common Issues
- **Tool not working**: Check `tools:` section
- **Command denied**: Check `permission.bash` patterns
- **Skill not loading**: Check skill name matches directory
- **Agent not found**: Check `opencode.json` agent definitions
