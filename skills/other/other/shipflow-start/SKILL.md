---
name: shipflow-start
description: Start a task — load context, mark task in-progress in TASKS.md, plan the work. Use at the beginning of any work session.
argument-hint: <task description or TASKS.md item>
---

## Context

- Current directory: !`pwd`
- Current date: !`date '+%Y-%m-%d'`
- Project name: !`basename $(pwd)`
- Git branch: !`git branch --show-current 2>/dev/null || echo "unknown"`
- Git status: !`git status --short 2>/dev/null || echo "Not a git repo"`
- Master TASKS.md: !`cat /home/claude/shipflow_data/TASKS.md 2>/dev/null || echo "No master TASKS.md"`
- Local TASKS.md (if exists): !`cat TASKS.md 2>/dev/null || echo "No local TASKS.md"`

## Your task

Start a work session on a task. Load context, mark the task as in-progress, and plan the approach.

### Step 1 — Identify the task

If `$ARGUMENTS` is provided, use it as the task description.

If `$ARGUMENTS` is empty, look at TASKS.md from context and use **AskUserQuestion**:
- Question: "Quelle tâche veux-tu commencer ?"
- `multiSelect: false`
- Options: top 5-7 uncompleted tasks from TASKS.md (highest priority first), each with its priority emoji as prefix
- Add a final option: "Autre — je décris ma tâche"

### Step 2 — Load context (silent)

Use the Agent tool with subagent_type=Explore to quickly find the 3-5 most relevant files for this task. Focus on:
- Files mentioned in the task description
- Files likely to be modified
- Config/entry points for the area of code involved

Read only what's needed. Do NOT read more than 5 files.

### Step 3 — Mark task in-progress

Update TASKS.md:
- Find the matching task and change its status: `📋 todo` → `🔄 in progress` (or `- [ ]` stays but add `🔄` prefix)
- If the task doesn't exist in TASKS.md yet, add it under the right section with `🔄 in progress`
- Update master `/home/claude/shipflow_data/TASKS.md` — always
- If a local `TASKS.md` also exists, update both
- No output at this step.

### Step 4 — Plan and report

Output a concise plan:

```
## Starting: [task name]

**Files in context:**
- [file] — [why it's relevant]

**Key constraints:**
- [any relevant decisions from memory or CLAUDE.md]

**Plan:**
1. [step]
2. [step]
3. [step]

**Estimated scope:** [small / medium / large]
```

Then ask: "On y va ?"

### Rules

- Do NOT start coding — this skill only primes and plans
- Do NOT commit or push anything
- Do NOT update CHANGELOG.md (that's for shipflow-end)
- Keep the plan under 10 steps
- If the task is vague, ask ONE clarifying question before planning
