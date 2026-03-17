---
name: df:new-project
description: |
  Initialize a new project with deep context gathering and PROJECT.md.
  Use when the user wants to start a new project or initialize DevFlow for the first time.
  Triggers on: "start a new project", "initialize project", "let's build something new", "set up a new project", "new project"
argument-hint: "[--auto]"
allowed-tools:
  - Read
  - Bash
  - Write
  - Task
  - AskUserQuestion
---
<context>
**Flags:**
- `--auto` — Automatic mode. After config questions, runs research → requirements → roadmap without further interaction. Expects idea document via @ reference.
</context>

<objective>
Initialize a new project through unified flow: questioning → research (optional) → requirements → roadmap.

**Creates:**
- `.planning/PROJECT.md` — project context
- `.planning/config.json` — workflow preferences
- `.planning/research/` — domain research (optional)
- `.planning/REQUIREMENTS.md` — scoped requirements
- `.planning/ROADMAP.md` — objective structure
- `.planning/STATE.md` — project memory

**After this command:** Run `/df:plan-objective 1` to start execution.
</objective>

<execution_context>
@~/.claude/devflow/workflows/new-project.md
@~/.claude/devflow/references/questioning.md
@~/.claude/devflow/references/ui-brand.md
@~/.claude/devflow/templates/project.md
@~/.claude/devflow/templates/requirements.md
</execution_context>

<process>
Execute the new-project workflow from @~/.claude/devflow/workflows/new-project.md end-to-end.
Preserve all workflow gates (validation, approvals, commits, routing).
</process>
