---
name: cook
description: "Implement, build, create, or add any feature, endpoint, page, component, or functionality. Use this skill whenever the user asks you to write new code or make code changes — whether it's adding an API endpoint, building a UI page, creating an export feature, wiring up a webhook, implementing a search/filter, or any other hands-on coding task. This is the default skill for all 'build this', 'add this', 'create this', 'wire up', 'implement' requests. Covers the full cycle: clarify requirements, plan if needed, write code, verify, and review. Do NOT use for pure research, debugging, documentation, or explanation — only when the user wants working code delivered."
argument-hint: what-to-implement
---

ultrathink.

## How cook works

Cook is an incremental loop: break work into tasks, implement one, verify it works, move to the next. The key discipline is that nothing is "done" until there's evidence it works — but *how* you verify adapts to the situation.

## Before you start

If the request is clear, start. If it's ambiguous or multi-faceted, ask clarifying questions. If the work is large or multi-path, plan first (`/give-plan`). Otherwise, just start.

## The loop

### 1. Break into tasks only when it helps

For a small single-concern request, just implement, verify, and continue.

For multi-step work or collaboration, use `.claude/scripts/tasks.py` to track concrete outcomes. Task files persist in `.tasks/`, so a fresh context can pick up where the last one left off.

Every task requires three fields: `title`, `desc`, `expected`. Read the authoring rubric before writing tasks — bad tasks are worse than no tasks:

- `.claude/scripts/tasks.py --help` for the short-form rubric and examples
- `.claude/scripts/tasks-authoring.md` for the full guide

```
.claude/scripts/tasks.py --task-file <slug> add "<title>" "<desc>" "<expected>"
.claude/scripts/tasks.py --task-file <slug> list
.claude/scripts/tasks.py --task-file <slug> verify <id> "<evidence>"
.claude/scripts/tasks.py --task-file <slug> done <id>
```

### 2. Implement → Verify → Review → Next

Pick the next unblocked task, make the change, then hand off to a **tester** and (for risky work) a **reviewer** — isolated teammates that judge the change independently. See `.claude/skills/test/teammate.md` and `.claude/skills/review-code/teammate.md` for how to spawn them.

`/cook` owns implementation. The tester owns verification. Give the tester:
- the user-visible claim or acceptance criteria
- the files or behavior you changed
- the most likely regression surface
- any constraints that matter

You can still add durable tests, fixtures, or stable selectors when they belong to the product change itself. Do not stuff temporary verification tactics into `/cook` just to get through one run.

Before invoking verification, confirm the edits actually landed on disk. If the change you expect is missing from the diff, fix that first; a passing check against unchanged code is worthless evidence.

Do not mark a task done on confidence alone. The tester proves the behavior. The reviewer checks that the implementation is correct, scoped, and aligned with the repo. For risky or non-trivial work, spawn a reviewer before marking the task complete.

Update task status as you go so the execution trail stays trustworthy.

### 3. Review the whole change set

After the task list is complete, review the combined diff before declaring success. Cross-task issues often appear only in the final aggregate: mismatched assumptions, naming drift, incomplete ripple updates, or verification that was too narrow. Spawn a reviewer for this final pass.

### 4. Report

When done, summarize:
- what changed
- how each claim was verified
- decisions that materially shaped the implementation
- any follow-up the user should know about

## Request

<request>$ARGUMENTS</request>
