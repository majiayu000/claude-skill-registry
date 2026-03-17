---
name: kit-builder
description: Build ClaudeKit Marketing components - skills, agents, commands, workflows. Use when creating new automation, extending marketing capabilities, or understanding kit structure. Includes templates, examples, and init scripts.
license: MIT
---

# Kit Builder

Build skills, agents, commands, and workflows for ClaudeKit Marketing.

## When to Use

- Creating new skill for specialized task
- Adding new agent for marketing automation
- Building command for user workflow
- Designing workflow for process orchestration
- Understanding kit component structure

## Component Types

| Type | Location | Purpose |
|------|----------|---------|
| Skill | `.claude/skills/{name}/SKILL.md` | Domain knowledge + tools |
| Agent | `.claude/agents/{name}.md` | Specialized subagent |
| Command | `.claude/commands/{path}.md` | User-invocable action |
| Workflow | `.claude/workflows/{name}.md` | Process orchestration |

## Quick Start

**Create skill:** Load `references/skill-guide.md`
**Create agent:** Load `references/agent-guide.md`
**Create command:** Load `references/command-guide.md`
**Create workflow:** Load `references/workflow-guide.md`

## Init Script

```bash
python .claude/skills/kit-builder/scripts/init_component.py <type> <name>
```

Types: `skill`, `agent`, `command`, `workflow`

## Decision Tree

```
What to build?
├── Reusable domain knowledge → Skill
│   └── API, tool, workflow patterns
├── Autonomous task handler → Agent
│   └── Orchestrates skills + tools
├── User-triggered action → Command
│   └── Slash command (/name)
└── Process definition → Workflow
    └── Multi-step orchestration
```

## References

| Guide | File |
|-------|------|
| Skill Creation | `references/skill-guide.md` |
| Agent Creation | `references/agent-guide.md` |
| Command Creation | `references/command-guide.md` |
| Workflow Creation | `references/workflow-guide.md` |
| Best Practices | `references/best-practices.md` |
| Marketing Checklist | `references/marketing-checklist.md` |

## Templates

| Template | Path |
|----------|------|
| Skill | `templates/skill-template.md` |
| Agent | `templates/agent-template.md` |
| Command | `templates/command-template.md` |
| Workflow | `templates/workflow-template.md` |

## Integration

**Related:** skill-creator, claude-code

**Agents:** planner, researcher, docs-manager
