---
name: kit
description: (ePost) Use when user says "create an agent", "add a skill", "write a hook", "optimize a skill", or "kit authoring" — entry point for epost-kit content creation and optimization workflows
user-invocable: true
context: fork
agent: epost-fullstack-developer
metadata:
  argument-hint: "[--add-agent | --add-skill | --add-hook | --optimize] [name]"
  connections:
    enhances: []
    requires: [kit-agents, kit-skill-development]
---

# Kit — Unified Kit Authoring Command

Create or optimize agents, skills, hooks, and commands for epost_agent_kit.

## Step 0 — Flag Override

If `$ARGUMENTS` starts with `--add-agent`: load `references/add-agent.md` and execute. Pass remaining args as agent name.
If `$ARGUMENTS` starts with `--add-skill`: load `references/add-skill.md` and execute. Pass remaining args as skill name.
If `$ARGUMENTS` starts with `--add-hook`: load `references/add-hook.md` and execute. Pass remaining args as hook name.
If `$ARGUMENTS` starts with `--optimize`: load `references/optimize.md` and execute. Pass remaining args as skill name.
Otherwise: continue to Auto-Detection.

## Aspect Files

| File | Purpose |
|------|---------|
| `references/add-agent.md` | Create a new agent definition |
| `references/add-skill.md` | Create a new skill definition |
| `references/add-hook.md` | Create a new hook for Claude Code automation |
| `references/optimize.md` | Optimize an existing agent skill |

## Auto-Detection

Analyze `$ARGUMENTS` for type keywords:

| Keyword | Load Reference |
|---------|---------------|
| "agent" | `references/add-agent.md` |
| "skill" | `references/add-skill.md` |
| "hook" | `references/add-hook.md` |
| "optim" | `references/optimize.md` |
| Empty or ambiguous | Ask user: what type to create? (agent, skill, hook, or optimize existing) |

## Execution

Load the matching reference file and execute its workflow.
