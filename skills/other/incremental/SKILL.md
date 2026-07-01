---
name: incremental
description: Delivers changes in small, testable slices. Use when a change spans multiple files, a task feels too large for one step, or you're about to write a lot of code at once.
---

# Incremental Implementation

## Overview

Build in thin vertical slices. Implement one piece, test it, verify it, then expand. NEVER implement an entire feature in one pass. Each increment MUST leave the system in a working, testable state. Slicing this way keeps large features tractable.

## When to Use

- Implementing any multi-file change
- Building a new feature from a task breakdown
- Refactoring existing code
- Any time you're tempted to write more than ~100 lines before testing

**When NOT to use:** Single-file, single-function changes where the scope is already minimal.

## The Increment Cycle

```
┌──────────────────────────────────────┐
│                                      │
│   Implement ──→ Test ──→ Verify ──┐  │
│       ▲                           │  │
│       └───── Commit ◄─────────────┘  │
│              │                       │
│              ▼                       │
│          Next slice                  │
│                                      │
└──────────────────────────────────────┘
```

For each slice:

1. **Implement** the smallest complete piece of functionality.
2. **Test** — run the test suite, or write a test if none exists.
3. **Verify** — confirm the slice works: tests pass, build succeeds, manual check holds.
4. **Commit** — save progress with a descriptive message; keep the commit atomic (one logical change).
5. **Move to the next slice** — carry forward, never restart.

## Slicing Strategies

### Vertical Slices (preferred)

Build one complete path through the stack:

```
Slice 1: Create a task (DB + API + basic UI)
    → Tests pass, user can create a task via the UI

Slice 2: List tasks (query + API + UI)
    → Tests pass, user can see their tasks

Slice 3: Edit a task (update + API + UI)
    → Tests pass, user can modify tasks

Slice 4: Delete a task (delete + API + UI + confirmation)
    → Tests pass, full CRUD complete
```

Each slice delivers working end-to-end functionality.

### Contract-First Slicing

When backend and frontend develop in parallel:

```
Slice 0:  Define the API contract (types, interfaces, OpenAPI spec)
Slice 1a: Implement backend against the contract + API tests
Slice 1b: Implement frontend against mock data matching the contract
Slice 2:  Integrate and test end-to-end
```

### Risk-First Slicing

Tackle the riskiest or most uncertain piece first:

```
Slice 1: Prove the WebSocket connection works (highest risk)
Slice 2: Build real-time updates on the proven connection
Slice 3: Add offline support and reconnection
```

If Slice 1 fails, you find out before investing in Slices 2 and 3.

## Implementation Rules

### Rule 0: Simplicity First

Before writing code, ask: what is the simplest thing that could work?

After writing code, check it against:
- Can this be done in fewer lines?
- Are these abstractions earning their complexity?
- Would a staff engineer ask "why didn't you just..."?
- Am I building for hypothetical future requirements, or the current task?

```
SIMPLICITY CHECK:
✗ Generic EventBus with middleware pipeline for one notification
✓ Simple function call

✗ Abstract factory pattern for two similar components
✓ Two straightforward components with shared utilities

✗ Config-driven form builder for three forms
✓ Three form components
```

Three similar lines beat a premature abstraction. Implement the naive, obviously-correct version first. Optimize only after correctness is proven with tests.

### Rule 0.5: Scope Discipline

Touch only what the task requires. Do NOT:

- "Clean up" code adjacent to your change
- Refactor imports in files you're not modifying
- Remove comments you don't fully understand
- Add features absent from the spec because they "seem useful"
- Modernize syntax in files you're only reading

When you notice something worth improving outside scope, record it — do not fix it:

```
NOTICED BUT NOT TOUCHING:
- src/utils/format.ts has an unused import (unrelated to this task)
- The auth middleware could use better error messages (separate task)
→ Want me to create tasks for these?
```

### Rule 1: One Thing at a Time

Each increment changes one logical thing. NEVER mix concerns.

**Bad:** one commit that adds a new component, refactors an existing one, and updates the build config.

**Good:** three separate commits — one per change.

### Rule 2: Keep It Compilable

After each increment the project MUST build and existing tests MUST pass. NEVER leave the codebase broken between slices.

### Rule 3: Feature Flags for Incomplete Features

When a feature isn't ready for users but you need to merge increments, gate it behind a flag so partial work stays dark:

```typescript
// TypeScript
const ENABLE_TASK_SHARING = process.env.FEATURE_TASK_SHARING === 'true';

if (ENABLE_TASK_SHARING) {
  // work-in-progress sharing UI
}
```

```python
# Python
import os

ENABLE_TASK_SHARING = os.environ.get("FEATURE_TASK_SHARING") == "true"

if ENABLE_TASK_SHARING:
    ...  # work-in-progress sharing path
```

This merges small increments to the main branch without exposing incomplete work.

### Rule 4: Safe Defaults

New code MUST default to conservative behavior — opt in to side effects, never opt out:

```typescript
// TypeScript — disabled by default, caller opts in
export function createTask(data: TaskInput, options?: { notify?: boolean }) {
  const shouldNotify = options?.notify ?? false;
  // ...
}
```

```python
# Python — disabled by default, caller opts in
def create_task(data, *, notify: bool = False):
    should_notify = notify
    # ...
```

### Rule 5: Rollback-Friendly

Each increment MUST be independently revertable:

- Additive changes (new files, new functions) revert cleanly.
- Modifications to existing code stay minimal and focused.
- Database migrations carry a corresponding rollback migration.
- NEVER delete something and replace it in the same commit — separate the two.

## Working with Agents

When directing an agent to implement incrementally, scope each increment explicitly:

```
"Implement Task 3 from the plan.

Start with the database schema change and the API endpoint only.
Leave the UI for the next increment.

After implementing, run the stack's test and build gates to confirm
nothing is broken."
```

State what is in scope and what is NOT in scope for each increment.

## Increment Checklist

After each increment, verify. Command examples span ecosystems — run whichever your stack uses:

- [ ] The change does one thing and does it completely.
- [ ] All existing tests still pass (`npm test` / `pytest` / `go test ./...` / `cargo test`).
- [ ] The build succeeds (`npm run build` / `python -m build` / `go build ./...` / `cargo build`).
- [ ] Type checking passes (`tsc --noEmit` / `mypy .` / `cargo check`).
- [ ] Linting passes (`npm run lint` / `ruff check` / `golangci-lint run`).
- [ ] The new functionality works as expected.
- [ ] The change is committed with a descriptive message.

**Note:** Run each verification command after a change that could affect it. After a successful run, do not repeat the same command unless the code has changed since — re-running on unchanged code adds no information.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll test it all at the end" | Bugs compound. A bug in Slice 1 makes Slices 2-5 wrong. Test each slice. |
| "It's faster to do it all at once" | It feels faster until something breaks and you can't find which of 500 changed lines caused it. |
| "These changes are too small to commit separately" | Small commits are free. Large commits hide bugs and make rollbacks painful. |
| "I'll add the feature flag later" | If the feature isn't complete, it MUST NOT be user-visible. Add the flag now. |
| "This refactor is small enough to include" | Refactors mixed with features make both harder to review and debug. Separate them. |
| "Let me run the build command again just to be sure" | After a successful run, repeating the same command adds nothing unless the code changed. Re-run after later edits, not as reassurance. |

## Red Flags

- More than 100 lines written without running tests
- Multiple unrelated changes in a single increment
- "Let me just quickly add this too" scope expansion
- Skipping the test/verify step to move faster
- Build or tests broken between increments
- Large uncommitted changes accumulating
- Building abstractions before the third use case demands it
- Touching files outside the task scope "while I'm here"
- Creating new utility files for one-time operations
- Running the same build/test command twice in a row without an intervening code change

## Verification

After completing all increments for a task:

- [ ] Each increment was individually tested and committed.
- [ ] The full test suite passes.
- [ ] The build is clean.
- [ ] The feature works end-to-end as specified.
- [ ] No uncommitted changes remain.
