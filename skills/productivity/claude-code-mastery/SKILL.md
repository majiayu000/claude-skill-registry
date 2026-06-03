---
name: claude-code-mastery
description: Master Claude Code capabilities - subagents, skills, hooks, MCP. Use when optimizing workflows, creating automation, or improving how agents work.
---

# Claude Code Mastery - Building Better AI Systems

Access Claude Code documentation at `~/.claude/docs/claude-code/` or via the `cc-docs` skill.

Use this knowledge to continuously improve how we work.

## Core Capabilities

### Subagents
Location: `~/.claude/agents/` (user) or `.claude/agents/` (project)

**Key fields:**
```yaml
---
name: agent-name
description: When Claude should delegate here
tools: Read, Grep, Glob, Bash, Edit, Write
model: sonnet | opus | haiku | inherit
permissionMode: default | acceptEdits | bypassPermissions
skills: skill-1, skill-2
hooks:
  PreToolUse: [...]
  PostToolUse: [...]
---

System prompt content here...
```

**Use subagents when:**
- Task needs isolated context
- Different tools/permissions needed
- Specialized behavior required

### Skills
Location: `~/.claude/skills/` (user) or `.claude/skills/` (project)

**Structure:**
```
skill-name/
├── SKILL.md          # Required - main instructions
├── reference.md      # Optional - detailed docs
└── scripts/          # Optional - utilities
```

**Key fields:**
```yaml
---
name: skill-name
description: When to apply this skill (triggers auto-loading)
allowed-tools: Read, Grep, Glob  # Optional tool restriction
context: fork  # Optional - run in subagent
---

Instructions here...
```

**Use skills when:**
- Knowledge should auto-apply based on task
- Pattern repeats across projects
- Want to inject expertise without delegation

### Hooks
Location: `.claude/settings.json` or subagent frontmatter

**Events:**
- `PreToolUse` - Before tool executes (can block)
- `PostToolUse` - After tool executes
- `SubagentStart` - When subagent begins
- `SubagentStop` - When subagent completes
- `SessionStart` - When session begins

**Example:**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "./scripts/auto-lint.sh"
      }]
    }]
  }
}
```

**Use hooks when:**
- Deterministic action needed (not AI judgment)
- Automation on every occurrence
- Validation before allowing operations

### MCP Servers
Configuration: `~/.claude.json` or `.mcp.json`

**Access external tools:**
- megg (memory)
- shadcn (UI components)
- perplexity (research)
- Custom servers

## Improvement Patterns

### Pattern: Repeated Context Loading
**Problem:** Same context loaded every session
**Solution:** Create a skill that auto-applies
```yaml
---
name: project-context
description: Apply when working on [project]. Auto-loads conventions.
---
```

### Pattern: Manual Validation
**Problem:** Manually checking things before commit
**Solution:** Create PreToolUse hook
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash(git commit:*)",
      "hooks": [{"type": "command", "command": "./scripts/pre-commit-check.sh"}]
    }]
  }
}
```

### Pattern: Complex Delegation
**Problem:** Unclear when to use which agent
**Solution:** Improve agent descriptions, add proactive triggers
```yaml
description: Use proactively when [specific trigger]. Handles [specific task].
```

### Pattern: Lost Knowledge
**Problem:** Decisions forgotten between sessions
**Solution:** megg_remember after every significant decision

## Documentation Reference

Key files in `~/.claude/docs/claude-code/`:

| Topic | File |
|-------|------|
| Subagents | `build/sub-agents.md` |
| Skills | `build/skills.md` |
| Hooks | `build/hooks-guide.md` |
| MCP | `build/mcp.md` |
| Headless mode | `build/headless.md` |
| Settings | `configuration/settings.md` |
| CLI Reference | `reference/cli-reference.md` |

## Self-Improvement Checklist

When improving workflows:
1. [ ] Identify the friction point
2. [ ] Check docs for existing solution
3. [ ] Choose right tool (skill vs hook vs subagent)
4. [ ] Implement minimal version
5. [ ] Test it works
6. [ ] Document in megg
7. [ ] Consider if others need it (project vs user scope)

## Anti-Patterns

- **Over-engineering:** Don't create skills for one-time tasks
- **Premature automation:** Prove manual workflow first
- **Isolated improvements:** Log all changes in megg
- **Ignoring scope:** User skills for personal, project for team
