---
name: skills
description: List all available skills (core + custom)
user-invocable: true
---

# Available Skills

List all skills available in Director Mode Lite.

---

## Core Skills

| Skill | Purpose |
|-------|---------|
| `code-reviewer` | Code quality, security review |
| `test-runner` | Test automation, TDD support |
| `debugger` | 5-step debugging methodology |
| `doc-writer` | README, API docs, comments |

---

## Workflow Skills

| Skill | Function |
|-------|----------|
| `/workflow` | Complete 5-step development |
| `/focus-problem` | Problem analysis |
| `/test-first` | TDD Red-Green-Refactor |
| `/smart-commit` | Conventional Commits |
| `/plan` | Task breakdown |
| `/auto-loop` | Autonomous TDD loop |
| `/evolving-loop` | Self-evolving development |

---

## Utility Skills

| Skill | Function |
|-------|----------|
| `/project-init` | Project setup |
| `/project-health-check` | 7-point audit |
| `/check-environment` | Verify dev environment |
| `/claude-md-check` | Validate CLAUDE.md |
| `/agent-check` | Validate agents |
| `/skill-check` | Validate skills |
| `/hooks-check` | Validate hooks |
| `/mcp-check` | Validate MCP |

---

## Template Skills

| Skill | Function |
|-------|----------|
| `/claude-md-template` | Generate CLAUDE.md |
| `/agent-template` | Generate agent |
| `/skill-template` | Generate skill |
| `/hook-template` | Generate hook |

---

## Creating Custom Skills

```markdown
---
name: my-skill
description: What this skill does
user-invocable: true
---

# Skill Name

## Purpose
## Workflow
## Output
```

Save to `.claude/skills/my-skill/SKILL.md`
