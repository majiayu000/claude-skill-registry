---
description: Close current increment if ready and suggest next work. Use when saying "what's next", "next increment", or "move on".
---

# Next Increment (Smart Workflow Transition)

**CRITICAL**: This command requires **EXPLICIT USER CONFIRMATION** before closing any increment!

## Workflow

### Step 1: Find Active Increment

```bash
find .specweave/increments -type f -name "spec.md" -exec grep -l "status: in-progress" {} \;
```

- One in-progress → Validate for closure
- Multiple in-progress → Warn about WIP limit, ask which to close
- None in-progress → Skip to Step 4 (suggest next work)

### Step 2: PM Validation (3 Gates)

#### Gate 1: Tasks Completed
- All P1 (critical) tasks completed
- All P2 (important) tasks completed OR deferred with reason
- P3 tasks completed, deferred, or moved to backlog
- No tasks in "blocked" state

#### Gate 2: Tests Passing
- All test suites passing (no failures)
- Coverage meets target (default 80%+ critical paths)
- No skipped tests without documentation

#### Gate 3: Documentation Updated
- CLAUDE.md updated with new features
- README.md updated with usage examples
- CHANGELOG.md updated (if public API changed)

### Step 3: Closure Decision

**If ALL gates pass** — use AskUserQuestion for explicit confirmation:
```
AskUserQuestion({
  questions: [{
    header: "Close increment?",
    question: "All PM gates passed. Ready to permanently close this increment?",
    options: [
      { label: "Yes, close it", description: "Mark as completed (irreversible)" },
      { label: "No, keep open", description: "Stay at ready_for_review status" }
    ],
    multiSelect: false
  }]
})
```

Only on user confirmation: update status → completed, set completion date, generate report, free WIP slot.

**If ANY gate fails** — present options:
- A. Complete remaining work (recommended)
- B. Force close and defer incomplete tasks
- C. Stay on current increment

**NEVER auto-close!** Always give user control.

### Step 3.5: Post-Closure Quality Assessment

After successful closure, automatically run `/sw:qa ${incrementId}`. Quality gate: PASS (≥80), CONCERNS (60-79), FAIL (<60). If FAIL, suggest creating follow-up increment.

### Step 4: Suggest Next Work

1. Check for planned increments in backlog
2. Present options: start backlog item, continue in-progress work, or create new increment

## Key Differences

| Command | Purpose |
|---------|---------|
| `/sw:do` | Execute tasks in increment |
| `/sw:progress` | Check status (no action) |
| `/sw:done` | Explicit close with validation |
| `/sw:next` | **Smart transition** (close + QA + suggest next) |
