---
name: planning
description: Persistent markdown planning for complex tasks. Auto-activates when a task requires 5+ steps. Creates and updates task_plan.md to track progress across sessions.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

When working on a complex task, create and maintain a persistent plan in `task_plan.md` at the project root.

## When to Activate

- Task requires 5+ tool calls or file changes
- Multiple files need to be created or modified
- Task has dependencies between steps
- User explicitly asks to plan

## Plan Format

Create `task_plan.md` with this structure:

```markdown
# Task: [description]

## Status: In Progress | Completed | Blocked

## Steps

- [x] Step 1: [completed step]
- [ ] Step 2: [current step] ← CURRENT
- [ ] Step 3: [next step]
- [ ] Step 4: [future step]

## Key Files
- [file] → [what needs to change]

## Decisions Made
- [decision and why]

## Blockers
- [any blockers]
```

## Rules

1. **Create plan BEFORE starting work** — write task_plan.md first
2. **Update after each step** — mark completed, move CURRENT marker
3. **Track decisions** — record why you chose an approach
4. **Note blockers** — if stuck, write it down
5. **Read plan on resume** — if task_plan.md exists, read it first to continue where you left off
6. **Delete on completion** — remove task_plan.md when all steps are done

## On Session Resume

If `task_plan.md` exists:
1. Read it
2. Find the CURRENT step
3. Continue from there
4. Update progress as you go

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
