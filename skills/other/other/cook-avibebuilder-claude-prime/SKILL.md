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

### 1. Break into tasks (skip for simple requests)

For simple, single-concern requests — just implement, verify, and move on. No tasks needed.

For multi-step or collaboration work, use `tasks.py` to track progress:

```
tasks.py --task-file <slug> add "<description>" "<expected outcome>"
tasks.py --task-file <slug> list
tasks.py --task-file <slug> verify <id> "<evidence>"
tasks.py --task-file <slug> done <id>
```

For other commands, run `tasks.py --help`. Each task needs a clear `expected` field — what "done" looks like, stated verifiably. Task files persist in `.tasks/`, so a fresh context can pick up where the last one left off.

### 2. Implement → Verify → Review → Next

Pick the next unblocked task, implement it, verify it, then review what changed before moving on.

**Verification is flexible** — pick the method that actually proves the task works:

| Situation | Verification approach |
|-----------|----------------------|
| Project has relevant tests | Run them |
| You added new behavior | Write tests in the project's test framework |
| UI/frontend change | Use `agent-browser` to verify the rendered result; if acceptance depends on visual fit or comparison against a screenshot/mockup, capture the result and use `/media-processor` before calling it done |
| Logic with no test coverage | Write a quick temporary verification script to exercise the code path, then discard it unless it clearly belongs in the repo |
| API endpoint | Call it and check the response |
| Type/schema change | Run the type checker |

**Before running any verification command, confirm your changes are actually on disk.** Run `git diff --stat` — it should list the files you modified. If it shows nothing when you expected changes, your Write/Edit calls didn't execute — retry them before proceeding. Lint and type checks pass on unchanged files too, so a clean result on unmodified code is a vacuous pass, not evidence the feature works.

Never mark a task done on faith. Verification proves the behavior works. Review checks whether the change is correct and scoped. For risky or non-trivial tasks, run `/review-code` before marking done. If repeated verification fails without the failure mode changing, reassess your approach or ask the user.
And don't forget to update tasks progress.

### 3. Final review

After completing all tasks, always review the full change set before declaring the work done. This final pass catches cross-task issues, scope drift, and things that looked fine locally but are weaker in combination. Use `/review-code` for the final review.

### 4. Report

When done, summarize:
- What changed (files + brief description)
- How you verified each piece
- Decisions you made and why
- Anything the user should follow up on

## Request

<request>$ARGUMENTS</request>
