---
name: worker-superpowers
description: This skill should be used when a worker needs to "debug a failing test", "trace root cause", "follow TDD workflow", "verify before completion", "brainstorm approach", "use systematic debugging", "use superpowers", "red green refactor", or when any pipeline worker needs access to structured development powers. Bundles four development methodologies (TDD, systematic debugging, verification, brainstorming) adapted from the superpowers framework for CoBuilder pipeline workers.
version: 1.0.0
title: "Worker Superpowers"
status: active
type: skill
last_verified: 2026-03-21
grade: authoritative
---

# Worker Superpowers

Structured development powers for CoBuilder pipeline workers, adapted from the [superpowers](https://github.com/obra/superpowers) methodology. Four composable powers that enforce disciplined development: test first, debug systematically, verify before completion, brainstorm when uncertain.

**Load this skill at the start of any worker task**: `Skill("worker-superpowers")`

---

## Power 1: Test-Driven Development (RED-GREEN-REFACTOR)

### RED Phase — Write Failing Test

1. Read the acceptance criteria from the task assignment
2. Write a test that captures the expected behavior
3. Run the test — it **MUST fail**
4. If the test passes → feature already exists or test is wrong

### GREEN Phase — Minimal Implementation

1. Write the **minimum code** to make the failing test pass
2. Do not add features beyond what the test requires
3. Run the test — it **MUST pass**

### REFACTOR Phase — Clean Up

1. Improve code quality while tests stay green
2. Remove duplication, improve naming, simplify logic
3. Run tests after **every change**

### Sub-Agent Separation

Never let the same sub-agent write both the test and the implementation:

```
Worker (Opus) coordinates:
  RED:     Sub-agent A writes failing test → Sub-agent B confirms failure
  GREEN:   Sub-agent C implements code → Sub-agent D confirms pass
  REFACTOR: Sub-agent E cleans up → Sub-agent F confirms still passing
```

| Phase | Action | Test Must | Anti-Pattern |
|-------|--------|-----------|-------------|
| RED | Write test for expected behavior | FAIL | Writing tests after code |
| GREEN | Write minimum code | PASS | Gold-plating, adding extras |
| REFACTOR | Clean up, remove duplication | STAY GREEN | Adding new functionality |

---

## Power 2: Systematic Debugging

When a test fails unexpectedly, follow this 7-step protocol:

1. **Reproduce** — Run the failing test, capture exact error output
2. **Hypothesize** — Form 2-3 theories about root cause
3. **Isolate** — Test each hypothesis (read code path, add diagnostics, check I/O)
4. **Identify** — Determine actual root cause (not symptoms)
5. **Fix** — Apply minimal fix for the root cause
6. **Verify** — Run original failing test + regression tests
7. **Clean up** — Remove diagnostic code, commit the fix

### Investigation Techniques

| Symptom | Investigation |
|---------|--------------|
| Test timeout | Infinite loops, unresolved promises, missing await |
| Wrong output | Trace data flow input→output, check each transformation |
| Import error | File paths, exports, dependencies |
| Intermittent | Race conditions, shared mutable state, time dependencies |

### Anti-Patterns

- **Shotgun debugging**: Changing random things hoping something works
- **Fix the symptom**: Suppressing errors instead of fixing causes
- **Retry blindly**: Re-running without investigating why it failed

For extended scenarios, see `references/debugging-playbook.md`.

---

## Power 3: Verification Before Completion

**MANDATORY** before claiming any task is done.

### Checklist

1. **Run all tests** — Actually execute, capture output as evidence:
   ```bash
   pytest tests/ -v 2>&1 | tee .pipelines/evidence/task-{id}-tests.log
   ```

2. **Check scope compliance** — Only scoped files modified:
   ```bash
   git diff --name-only  # Compare against task scope
   ```

3. **Check for incomplete markers**:
   ```bash
   grep -rn "TODO\|FIXME\|HACK\|XXX" [scoped-files]  # Must return empty
   ```

4. **Verify git status** — Everything committed, working tree clean

5. **Validate acceptance criteria** — Each criterion has evidence:

| Criterion | Evidence | Status |
|-----------|----------|--------|
| {AC-1} | {test output / log} | PASS/FAIL |

### Common Failures

| Claim | Reality | Fix |
|-------|---------|-----|
| "Tests pass" | Didn't run them | Run tests, capture output |
| "Feature works" | Only happy path tested | Test edge cases |
| "Code is clean" | Has TODO markers | Remove or complete them |

---

## Power 4: Brainstorming

When the path forward is unclear, evaluate trade-offs before committing.

1. **List 2-3 approaches** with description
2. **Evaluate** against criteria:

| Factor | Weight | Question |
|--------|--------|----------|
| Simplicity | High | Fewer moving parts? |
| Testability | High | Easiest to write tests for? |
| Scope | Critical | Stays within assigned file scope? |
| Reversibility | Medium | Easiest to change if wrong? |

3. **Select** simplest and most testable approach
4. **Document** decision in a code comment

When in doubt, choose the simplest approach and validate with a test.

---

## Quick Reference

| Situation | Power | Action |
|-----------|-------|--------|
| Starting a feature | TDD | Write failing test first |
| Test fails unexpectedly | Systematic Debugging | Follow the 7-step protocol |
| Task feels complete | Verification | Run the full checklist |
| Multiple valid approaches | Brainstorming | Evaluate trade-offs |
| Sub-agent failed | Systematic Debugging | Diagnose, don't retry blindly |

---

## Additional Resources

### Reference Files

- **`references/testing-anti-patterns.md`** — 10 common testing mistakes to avoid
- **`references/debugging-playbook.md`** — Extended debugging scenarios with decision tree
