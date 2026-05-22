---
name: getting-started
description: Guided 5-minute onboarding for Director Mode Lite
user-invocable: true
---

# Getting Started with Director Mode

Welcome! This guide walks you through your first 5 minutes with Director Mode Lite.

---

## Step 1: Verify Installation

Run a quick check:

```bash
ls .claude/skills/ | wc -l    # Should show 31+
ls .claude/agents/ | wc -l    # Should show 14
ls .claude/hooks/ | wc -l     # Should show 5+
```

If any are missing, re-run the install script.

Also check dependencies:
```bash
python3 --version   # Required for hook configuration
jq --version        # Required for hook scripts
```

---

## Step 2: Initialize Your Project

Run `/project-init` to auto-detect your project and generate a CLAUDE.md:

```
/project-init
```

This will:
1. Detect your language and framework
2. Create a CLAUDE.md with your project config
3. Verify hooks are configured
4. List available expert agents

---

## Step 3: Your First Workflow

Try the 5-step development workflow:

```
/workflow
```

Or jump straight to autonomous TDD:

```
/auto-loop "Implement [your feature]

Acceptance Criteria:
- [ ] First requirement
- [ ] Second requirement
- [ ] Tests pass"
```

---

## Quick Reference: Start Here

| Command | When to Use |
|---------|-------------|
| `/project-init` | First time in a new project |
| `/workflow` | Starting a new feature (guided) |
| `/auto-loop "task"` | Autonomous TDD development |
| `/focus-problem "issue"` | Understanding a bug or codebase area |
| `/smart-commit` | Ready to commit changes |

---

## When You're Ready for More

| Level | Commands |
|-------|----------|
| **Beginner** | `/workflow`, `/auto-loop`, `/focus-problem`, `/smart-commit`, `/plan` |
| **Intermediate** | `/test-first`, `/check-environment`, `/project-health-check`, `/changelog` |
| **Advanced** | `/evolving-loop`, `/evolving-status`, `/handoff-codex`, `/handoff-gemini` |
| **Customization** | `/agent-template`, `/skill-template`, `/hook-template` |
| **Validation** | `/claude-md-check`, `/agent-check`, `/skill-check`, `/hooks-check`, `/mcp-check` |

---

## Need Help?

- `/agents` - List all available agents
- `/skills` - List all available skills
- FAQ (`docs/FAQ.md`) - Common questions
- [Discord](https://discord.com/invite/rBtHzSD288) - Community support
- [claude-world.com](https://claude-world.com) - Website
