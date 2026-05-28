---
name: task-orchestration
description: Execute repo work one task at a time using a strict plan → execute → iterate loop tracked in .copilot-todo.yaml.
compatibility: Designed for GitHub Copilot CLI; requires Python 3 and local filesystem access.
metadata:
  author: github-copilot-cli
  version: "1.0"
---

# Task Orchestration

Use this skill to drive work through a **single authoritative YAML todo file**: `.copilot-todo.yaml`.

## Source of truth
- `.copilot-todo.yaml` — **only** status tracker.
- `.copilot-todo.md` — legacy/migration only (do not update by hand).

## Getting Started with Templates

### Creating a new plan from template
```bash
# Copy the template to your repo root or session folder
cp .github/skills/task-orchestration/template/plan.md.template plan.md

# Edit plan.md with your tasks (use Markdown checkboxes: - [ ] Task name)

# Generate .copilot-todo.yaml from your plan
python3 .github/skills/task-orchestration/scripts/task_orchestrator.py \
  --plan-md plan.md \
  --plan-mode regen \
  init
```

### Creating a .copilot-todo.yaml from scratch
```bash
# Copy the template
cp .github/skills/task-orchestration/template/copilot-todo.yaml.template .copilot-todo.yaml

# Edit the tasks section, then initialize
python3 .github/skills/task-orchestration/scripts/task_orchestrator.py init
```

**Template locations:**
- `template/plan.md.template` — Markdown plan with task checkboxes
- `template/copilot-todo.yaml.template` — YAML structure with example task

## Loop (plan → execute → iterate)
Repeat until no runnable tasks remain:

1) Sync / migrate state

- Reuse existing `.copilot-todo.yaml` (default):
```bash
python3 .github/skills/task-orchestration/scripts/task_orchestrator.py init
```

- (Optional) Seed/regenerate tasks from `plan.md` using **Markdown task list items** (`- [ ] ...` / `- [x] ...`).
  - If an item starts with an explicit ID prefix like `A1. ...` or `T-001: ...`, that ID is used.
  - Otherwise a stable-ish `P-XXXXXXXX` ID is generated from the text.
```bash
python3 .github/skills/task-orchestration/scripts/task_orchestrator.py \
  --plan-md plan.md \
  --plan-mode regen \
  init
```

2) Start next task
```bash
python3 .github/skills/task-orchestration/scripts/task_orchestrator.py next
```

3) Plan (short bullets, only for the chosen task)

4) Execute (minimal diff; run smallest relevant existing build/test)

5) Update status
```bash
python3 .github/skills/task-orchestration/scripts/task_orchestrator.py update <ID> completed --note "..."
# or
python3 .github/skills/task-orchestration/scripts/task_orchestrator.py update <ID> blocked --note "..."
```

5b) Commit (required when using `ralph_loop.py --require-commit`)
```bash
git add -A
git commit -m "<ID>: <short summary>"
```

6) Iterate / expand
If you discover missing work, **add follow-up tasks** (don’t silently expand scope):
```bash
python3 .github/skills/task-orchestration/scripts/task_orchestrator.py add "Title" --deps <ID1,ID2> --priority Medium --goal "..."
```

## Ralph-style multi-session loop (Copilot CLI)
To run **one fresh Copilot run per task** (uses `copilot -p`, consuming Copilot requests accordingly):
```bash
python3 .github/skills/task-orchestration/scripts/ralph_loop.py \
  --non-interactive \
  --max-steps 10

# or: derive tasks from plan.md
python3 .github/skills/task-orchestration/scripts/ralph_loop.py \
  --non-interactive \
  --plan-md plan.md \
  --plan-mode regen \
  --max-steps 10
```

Notes:
- This does **not** bypass quotas; it just splits work into multiple sessions.
- By default `ralph_loop.py` enforces **one commit per finished task** (use `--no-require-commit` to disable).
- Keep `--max-steps` small to avoid burning requests if a task gets stuck.
