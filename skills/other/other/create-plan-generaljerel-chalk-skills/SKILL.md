---
name: create-plan
description: Create a .plan.md file when the user asks to make a plan, create a plan, write a plan, or similar
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Write
argument-hint: "[plan description]"
read-only: false
destructive: false
idempotent: true
open-world: false
user-invocable: true
tags: planning, tasks, execution
capabilities: planning.create, chalk.plans
activation-intents: create plan, make a plan, plan this
activation-events: user-prompt
activation-artifacts: .chalk/.cursor/plans/**, AGENTS.md
risk-level: low
---

Follow the plan creation conventions defined in `.chalk/.cursor/plans/` and any project `AGENTS.md` if present.

## Quick Reference

### Where Plans Live

New plans go into the **unsorted backlog** (root of `.chalk/.cursor/plans/`) by default unless the user specifies a column (`todo/`, `inprogress/`, `testing/`, `done/`).

### Workflow

1. **Check the backlog** — Read filenames in the root of `.chalk/.cursor/plans/` (not subfolders) to find the highest numbered plan. The next plan number is that number + 1.
2. **Draft the plan** — Use the format specified in the conventions file. Break the work into concrete, actionable todos.
3. **Write the file** — Save to `.chalk/.cursor/plans/<number>_<slug>.plan.md`.
4. **Confirm** — Tell the user the plan was created with its filename and a brief summary.

### Filename Convention

```
<number>_<snake_case_slug>.plan.md
```

### Plan File Format

Every plan has YAML frontmatter (`name`, `overview`, `todos` with `id`/`content`/`status`) and a markdown body with `# Title`, `## Objective`, `## Architecture`, `## File Changes`, and `## Key Design Decisions` sections.

Refer to `AGENTS.md` for the full spec and format details.
