---
name: auto
description: Autonomous task execution - works through all tasks without stopping
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, TaskCreate, TaskUpdate, TaskList
model: opus
user-invocable: true
---

# Auto Mode

Fully autonomous development. Works through all tasks without stopping until complete.

## Entry Flow

```
auto
  ├─ Check prd.json exists?
  │   ├─ No → Bootstrap from context
  │   └─ Yes → Check pending tasks
  │             ├─ None pending → All done!
  │             └─ Has pending → Execute tasks
  │
  └─ Execute until done or interrupted
```

## CRITICAL: NEVER STOP

**FORBIDDEN:**
- NEVER use `AskUserQuestion` - make decisions yourself
- NEVER ask "Should I continue?"
- NEVER show summaries and wait
- NEVER say "Let me know..."
- NEVER output minimal responses (`.`, `—`, `Idle.`)

**REQUIRED:**
- Make autonomous decisions
- Log decisions to `.claude/decisions.md`
- Keep working until truly done

## Bootstrap (No prd.json)

When prd.json doesn't exist:

1. Read CLAUDE.md, README.md, package.json for context
2. Generate 5-10 starter tasks based on project
3. Create prd.json with stories
4. **Continue immediately** - don't stop for approval

## Pre-flight (Quick)

Before first task:
```bash
git status --short          # Warn if dirty, continue anyway
npm run build 2>&1 | tail -5  # Fail if broken, fix first
```

Skip if takes >10 seconds.

## Task Execution

### Find Next Task

```javascript
// Find executable tasks (not done, not blocked)
const executable = stories.filter(s =>
  s.passes !== true &&
  (s.blockedBy || []).every(dep =>
    stories.find(d => d.id === dep)?.passes === true
  )
);
```

### Execute Each Task

1. Read the task description
2. Implement the solution
3. `npm run typecheck` - Fix if fails
4. `npm run build` - Fix if fails
5. Verify (see below)
6. Update prd.json: `passes: true`
7. **IMMEDIATELY** start next task

### Verification

| Task Type | Verification |
|-----------|--------------|
| UX/UI | `agent-browser` visual check |
| Feature | Build passes |
| API | Endpoint returns expected data |
| Bug fix | Reproduce → verify fixed |

For UX tasks - browser check required:
```bash
agent-browser open http://localhost:3000/path
agent-browser snapshot -i  # Verify expected element
```

## Parallel Execution (Optional)

For independent tasks, launch multiple agents:
```
Task({ subagent_type: "general-purpose", prompt: "...", run_in_background: true })
Task({ subagent_type: "general-purpose", prompt: "...", run_in_background: true })
```

## Smart Retry

On failure:
1. Log to `.claude/mistakes.md`
2. Retry 1: Different approach
3. Retry 2: Simplest implementation
4. Still fails → `passes: false`, continue to next

## Commit Cadence

- Commit every 3 completed tasks
- Or after major milestones
- Use conventional commits: `feat|fix|refactor`

## Auto-Checkpoint (Token Protection)

**After every 3 completed tasks**, save checkpoint and recommend /compact:

```
if (completedThisSession % 3 === 0) {
  Write checkpoint to .claude/checkpoint.md

  Output:
  "💾 Checkpoint saved. Run /compact to reclaim ~40% tokens.
   Use /clear only at major transitions (~70% but wipes context)."
}
```

**Be concise.** Long responses burn tokens. Short responses = more runway.

## Completion

When `stories.every(s => s.passes === true)`:

```
All [N] tasks complete.

Summary:
- [X] features implemented
- [X] bugs fixed
- [X] improvements made

Run `status` to see full results.
```

## IDLE Detection

If no tasks to work on:
1. Check: Are ALL stories `passes: true`?
   - YES → Output completion summary
   - NO → Find blocked tasks and resolve blockers

## Quick Reference

| Situation | Action |
|-----------|--------|
| No prd.json | Bootstrap from context |
| All done | Output completion summary |
| Build broken | Fix first |
| Task fails | Retry 2x, then skip |
| UX task | Browser verify required |
| Blocked task | Skip, work on unblocked |
