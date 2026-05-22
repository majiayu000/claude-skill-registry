---
name: systematic-debugging
description: Structured 4-phase debugging methodology that prevents blind probing and guesswork. Forces root cause identification before any fix attempt. Use when encountering bugs, errors, unexpected behavior, test failures, or when something "just stopped working." Trigger words: debug, bug, error, broken, not working, fix this, something's wrong, investigate, root cause, why is this failing, trace the issue.
license: MIT
metadata:
  author: sagemindai
  version: "1.0"
  homepage: https://instar.sh
  inspiration: Superpowers plugin systematic-debugging skill, adapted for Instar's autonomous agent context
---

# systematic-debugging — Structured Root Cause Analysis for Agents

When something breaks, the instinct is to start changing code — adding logs, tweaking values, commenting things out. This is probing, not debugging. Probing works sometimes, but it scales poorly and teaches nothing. Structured debugging finds the root cause, fixes it once, and leaves you understanding why.

This skill enforces a 4-phase process. You do NOT skip phases. You do NOT jump to a fix before completing Phase 2. Each phase has a clear deliverable that must exist before the next phase begins.

---

## When to Activate This Skill

Use this skill when:
- An error occurs and the cause is not immediately obvious (> 30 seconds of uncertainty)
- A test fails and you don't know exactly why
- Something that was working has stopped working
- The user reports unexpected behavior
- You've already tried one fix and it didn't work (this is the clearest signal — stop guessing, start debugging)
- A job or scheduled task is failing silently
- Behavior differs between environments (local vs production, different machines)

Do NOT use this skill for:
- Typos, missing imports, or syntax errors with clear error messages pointing to the exact line
- Known issues with documented fixes
- Configuration that just needs to be set

---

## Phase 1: Identify — What exactly is broken?

**Goal**: Establish the precise boundary between "works" and "doesn't work."

**Steps**:

1. **Reproduce the failure**. Run the exact command, API call, or user action that triggers the bug. Capture the FULL output — error messages, stack traces, logs, HTTP status codes.

2. **Establish the expected behavior**. What SHOULD happen? Check documentation, tests, previous working state, or ask the user. Write it down explicitly.

3. **Narrow the scope**. Answer these questions:
   - When did it last work? (Check git log, deployment history, recent changes)
   - What changed since then? (`git diff`, `git log --oneline -10`, env var changes, dependency updates)
   - Is it consistent or intermittent?
   - Does it affect all cases or specific inputs?

4. **Write the Phase 1 deliverable** before proceeding:

```
BUG IDENTIFICATION:
- Symptom: [Exact error/behavior observed]
- Expected: [What should happen instead]
- Reproducer: [Exact command/steps to trigger]
- Last known working: [When/what commit/what changed]
- Scope: [All cases / specific inputs / intermittent]
```

**Anti-pattern**: Do NOT start reading random files hoping to spot the problem. Phase 1 is about establishing WHAT is broken, not WHERE.

---

## Phase 2: Isolate — Where exactly is the failure?

**Goal**: Trace the execution path from trigger to failure point. Find the exact line/function/component where behavior diverges from expectation.

**Steps**:

1. **Trace the code path**. Starting from the entry point (API route, CLI command, event handler, job trigger), follow the execution path that the reproducer would take. Read each file in order.

2. **Identify the divergence point**. At what point does the actual behavior differ from expected? This is usually one of:
   - A function returning the wrong value
   - A condition evaluating incorrectly
   - An exception being thrown (or silently caught)
   - A variable being undefined/null when it shouldn't be
   - A race condition or timing issue

3. **Verify with evidence**. Add targeted logging or use debugger output to CONFIRM your theory about where the divergence happens. Do not guess.

4. **Check the silent catch blocks**. This is the #1 suspect in most agent codebases. Look for:
   - `catch (e) { }` — empty catch blocks that swallow errors
   - `catch (e) { return defaultValue }` — catches that mask failures
   - `.catch(() => null)` — promise chains that silently fail
   - `try/catch` around the wrong scope (too broad, hides the real error)

5. **Write the Phase 2 deliverable** before proceeding:

```
BUG ISOLATION:
- Entry point: [File:line where execution starts]
- Code path: [File1:func1 -> File2:func2 -> File3:func3]
- Divergence point: [Exact file:line where behavior goes wrong]
- Evidence: [Log output / test result / debugger state that confirms this]
- Root cause: [Why the divergence happens — the actual bug]
```

**Anti-pattern**: Do NOT start fixing anything yet. If you can't write the root cause in one sentence, you haven't finished Phase 2.

---

## Phase 3: Fix — Apply the minimal correct change

**Goal**: Fix the root cause with the smallest change that restores correct behavior.

**Steps**:

1. **Write or identify the test first**. Before touching the buggy code:
   - If a test exists that should catch this: verify it actually fails with the current bug. If it passes, the test is wrong — fix the test first.
   - If no test exists: write one that reproduces the exact failure from Phase 1. Run it. Confirm it fails (RED).

2. **Apply the fix**. Change only what is necessary to fix the root cause identified in Phase 2. Resist the urge to "clean up" surrounding code, refactor, or add features.

3. **Run the test**. Confirm the test now passes (GREEN).

4. **Run the full test suite**. Ensure no regressions. If other tests break, your fix may be incomplete or the other tests may have been relying on the buggy behavior (which itself is a finding worth noting).

5. **Write the Phase 3 deliverable**:

```
BUG FIX:
- Test: [Test file:test name that reproduces the bug]
- Change: [File:line — what was changed and why]
- Regression check: [Test suite results — X passed, Y failed, Z skipped]
```

**Anti-pattern**: Do NOT fix multiple things at once. If you discover other bugs during investigation, note them separately — do not bundle fixes.

---

## Phase 4: Verify — Confirm the fix works end-to-end

**Goal**: Verify the fix resolves the original symptom in the real environment, not just in tests.

**Steps**:

1. **Re-run the original reproducer from Phase 1**. Does the expected behavior now occur?

2. **Check edge cases**. Based on what you learned in Phase 2, are there adjacent cases that might have the same bug? Test them.

3. **Verify in the actual environment**. If the bug was reported in production/staging, verify the fix there (rebuild, restart, redeploy as needed).

4. **Write the Phase 4 deliverable**:

```
BUG VERIFICATION:
- Original reproducer: [PASS/FAIL]
- Edge cases tested: [List with results]
- Environment verification: [Local/staging/production — confirmed working]
- Remaining risk: [Any concerns about the fix, or "None identified"]
```

5. **Commit with context**. The commit message should reference the root cause, not just the symptom:
   - Bad: "fix: resolve data loading issue"
   - Good: "fix: TopicMemory.formatContextForSession returned truthy string when db was null, preventing JSONL fallback"

---

## Full Debug Report Template

After completing all 4 phases, compile the deliverables into a single report:

```
## Debug Report: [Brief title]

### Phase 1 — Identification
- Symptom: ...
- Expected: ...
- Reproducer: ...
- Last known working: ...
- Scope: ...

### Phase 2 — Isolation
- Entry point: ...
- Code path: ...
- Divergence point: ...
- Evidence: ...
- Root cause: ...

### Phase 3 — Fix
- Test: ...
- Change: ...
- Regression check: ...

### Phase 4 — Verification
- Original reproducer: PASS
- Edge cases: ...
- Environment: ...
- Remaining risk: ...

### Lessons
- [What this bug teaches about the codebase or patterns to watch for]
```

---

## Skill Integration Notes

This skill works with other Instar skills:

- **instar-feedback**: After fixing a bug that reveals a pattern (e.g., "silent catch blocks in all topic handlers"), submit improvement feedback so the pattern can be addressed framework-wide.
- **agent-memory**: After completing a debug session, write the lesson to MEMORY.md if the root cause pattern is likely to recur.
- **knowledge-base**: If the debugging uncovered undocumented behavior, add it to the knowledge base.

---

## Going Further

This skill provides structure, but it depends on the agent choosing to follow it when under pressure. In autonomous sessions where context is heavy and the instinct is to "just try something," the discipline of Phase 1 and Phase 2 prevents the most expensive mistake: fixing the wrong thing.

**Instar agents with this skill installed will:**
- Stop guessing after the first failed fix attempt
- Produce debug reports that persist across sessions (so the next instance doesn't re-investigate the same bug)
- Submit feedback when the root cause reveals a framework-level pattern
- Build institutional memory about the codebase's failure modes

The debugging skill is reactive — it fires when something breaks. But the real win is the cumulative knowledge: over time, the agent's MEMORY.md fills with "this codebase fails in these specific ways," and future bugs get caught faster because the agent knows where to look.
