---
name: loop-review-skill-until-fixed-point
description: Iterate /review-skill on a target until fixed point. Runs review passes until all reviewers return NO ISSUES.
---

# Loop Review Skill Until Fixed Point

Run `/review-skill` on a target document repeatedly until fixed point—when all reviewers return NO ISSUES.

## Core Concept

```
/review-skill <target> --auto
         │
         ▼
    ┌─────────┐
    │ Issues? │
    └────┬────┘
         │
    yes ─┴─ no
     │      │
     ▼      ▼
  repeat   done (fixed point)
```

Fixed point = the document is both correct AND unambiguous. No reviewer can find anything to flag.

---

## Arguments

| Arg        | Required | Description                |
| ---------- | -------- | -------------------------- |
| `<target>` | yes      | Path to SKILL.md to review |

---

## State

```yaml
max_iterations: 10 # Safety limit
iteration_count: 0 # Current iteration
target: "<from args>" # Target SKILL.md path
history: [] # Minimal: just iteration outcomes
```

### History Entry Schema

Each iteration appends a minimal entry:

```yaml
- iteration: 1
  fixed_point: false
- iteration: 2
  fixed_point: false
- iteration: 3
  fixed_point: true # All reviewers returned NO ISSUES
```

The orchestrator does NOT track per-reviewer metrics. That detail stays inside `/review-skill` where it belongs. This prevents context leak between iterations.

---

## Phase: Initialize

1. Parse target path from arguments
2. Set `iteration_count = 0`
3. Set `max_iterations = 10`
4. Confirm target exists

---

## Phase: Loop

**Isolation requirement**: Each iteration must be context-isolated. The orchestrator must NOT carry synthesis, triage details, or "recurring theme" narratives between iterations. This prevents context leak that would bias subsequent reviews.

```
while iteration_count < max_iterations:
    iteration_count += 1

    1. Run: /review-skill <target> --auto
       (This is a FRESH invocation—no prior iteration context)
    2. Capture only the exit status: "fixed point" or "issues remain"
    3. Append to history file: { iteration, fixed_point: bool }
    4. Output: "Iteration {N}: {'fixed point' | 'issues remain'}"
    5. If fixed point → exit loop
    6. Else → continue loop (do NOT summarize or analyze findings here)
```

The orchestrator is intentionally stateless. All synthesis, triage, and issue-addressing happens INSIDE `/review-skill --auto`. The orchestrator only observes the outcome.

### Exit Conditions

| Condition                           | Action                                    |
| ----------------------------------- | ----------------------------------------- |
| `/review-skill` reports fixed point | Exit with success                         |
| `iteration_count >= max_iterations` | Safety limit hit, ask user how to proceed |

---

## Phase: Report

Present final state:

```markdown
## Loop Complete

| Metric              | Value             |
| ------------------- | ----------------- |
| Target              | {target}          |
| Iterations          | {iteration_count} |
| Fixed point reached | yes/no            |
```

If fixed point reached:

> {target} reached fixed point after {N} iterations.

If max iterations hit:

> Safety limit reached after {max_iterations} iterations without convergence.

---

Begin now.
