---
name: fix
description: "Use when review findings need fixing via subagents - invoked by review-loop after each iteration"
---

# Fix Skill

**You DISPATCH subagents to fix issues. You do NOT fix them yourself.**

**Violating the letter of these rules is violating the spirit.**

## When to Use

- Invoked by review-loop after each review iteration
- When review output file exists with findings

**Not for:** Manual fixes, direct code editing.

## Input

Args format: `<review-file> NEXT_ITER_TASK_ID=<task_id>`

Example: `/tmp/review/iter1.md NEXT_ITER_TASK_ID=11`

## The Iron Rules

1. **NEVER use Edit tool** - subagents fix code, not you
2. **NEVER read code files** - only read the review findings file
3. **DISPATCH sequentially** - one subagent at a time, wait for completion
4. **FIX critical/major** - skip only false positives or trivial minors
5. **Block next iteration** - add ALL fix tasks to next iteration's blockedBy

## Process (EXACT sequence)

**Step 1:** Parse args - extract review file path and NEXT_ITER_TASK_ID

**Step 2:** Read ONLY the review findings file
```
Read <review-file>
```

**Step 3:** Display findings table to user
```
| # | Severity | File:Line | Issue | Action |
|---|----------|-----------|-------|--------|
| 1 | critical | foo.rs:42 | SQL injection | FIX |
| 2 | major    | bar.rs:15 | Race condition | FIX |
| 3 | minor    | baz.rs:99 | Unused import | SKIP |
```

**Step 4:** Create fix Tasks and block next iteration

For EACH issue to fix:
```
TaskCreate(subject: "Fix: [summary]",
           description: "Fix [ISSUE] in [FILE]:[LINE]. Minimal change.",
           activeForm: "Fixing [summary]")
→ Returns task ID (e.g., #20)
```

Collect all fix task IDs: `FIX_TASKS=[20, 21, 22]`

Add ALL fix tasks to next iteration's blockedBy:
```
TaskUpdate(taskId: "${NEXT_ITER_TASK_ID}", addBlockedBy: ["20", "21", "22"])
```

Now TaskList will show: `Iteration 2 [blocked by #10, #20, #21, #22]`

**Step 5:** Execute fixes sequentially

For EACH fix task:
```
TaskUpdate(taskId: "${fix_id}", status: "in_progress")
Task(subagent_type: "general-purpose", description: "Fix: [summary]",
     prompt: "Fix [ISSUE] in [FILE]:[LINE]. Minimal change. Run tests. Verify compiles.")
TaskUpdate(taskId: "${fix_id}", status: "completed")
```

**Step 6:** Report summary
```
## Fix Summary
- Found: N, Fixed: M, Skipped: K
- Next iteration unblocked: [yes/no]
```

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I'll just fix this quickly" | NO. Dispatch subagent. |
| "This is a one-line fix" | NO. Dispatch subagent. |
| "Let me check the code first" | NO. Only read findings file. Subagent checks code. |
| "I can be more efficient" | NO. Follow the process exactly. |
| "Running fixes in parallel" | NO. Sequential only. |
| "This isn't a real issue" | Mark SKIP in table. Don't decide silently. |
| "I'll skip updating blockedBy" | NO. Next iteration MUST be blocked by all fix tasks. |
| "No NEXT_ITER_TASK_ID provided" | ERROR. Review-loop must provide it. Report failure. |

## Red Flags - STOP IMMEDIATELY

If you catch yourself doing ANY of these, STOP:

- Using Edit tool
- Using Read on code files (not findings file)
- Fixing issues directly
- Running subagents in parallel
- Skipping issues without marking SKIP in table
- Not adding fix tasks to next iteration's blockedBy
- Completing without all fix tasks being completed
- "Adapting" the process

**All of these mean: You are violating the skill. Stop and follow it.**
