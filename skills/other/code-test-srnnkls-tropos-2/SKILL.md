---
name: code-test
description: Enforce test-driven development (RED-GREEN-REFACTOR). Use when implementing features, fixing bugs, or changing behavior - write failing test first, then minimal code to pass.
---

# Test-Driven Development

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

---

## When to Use

**Always use for:**
- New features
- Bug fixes
- Behavior changes
- Refactoring

**Exceptions (confirm with user):**
- Throwaway prototypes
- Generated code
- Configuration files

**Workflow Integration:**
- **Multiple independent tasks from a plan?** → Use `task-dispatch` skill (it enforces TDD per task with quality gates)
- **Single implementation task?** → Use this skill directly for TDD workflow

---

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? Delete it. Start over. No exceptions.

---

## Red-Green-Refactor Cycle

### 1. RED - Write Failing Test

Write one minimal test showing what should happen.

**Requirements:**
- One behavior per test
- Clear name describing behavior
- Real code (avoid mocks unless unavoidable)

### 2. Verify RED - Watch It Fail

**MANDATORY. Never skip.**

Run the test. Confirm:
- Test fails (not errors from typos)
- Failure message matches expectation
- Fails because feature is missing

**Test passes immediately?** You're testing existing behavior. Fix the test.

### 3. GREEN - Minimal Code

Write the simplest code to pass the test.

**DO:** Just enough to pass, simple implementation
**DON'T:** Add features, refactor other code, add configurability

### 4. Verify GREEN - Watch It Pass

**MANDATORY.**

Run the test. Confirm:
- Test passes
- Other tests still pass
- No errors or warnings

### 5. REFACTOR - Clean Up

Only after green:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

### 6. Repeat

Next failing test for next behavior.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Already manually tested" | Ad-hoc is not systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Unverified code is debt. |
| "Need to explore first" | Fine. Throw away exploration, then TDD. |
| "Test hard to write" | Hard to test = hard to use. Simplify design. |

---

## Red Flags - Stop and Start Over

- Code written before test
- Test passes immediately
- Can't explain why test failed
- "Just this once" rationalization
- Keeping code "as reference"

**All of these mean:** Delete code. Start with TDD.

---

## Verification Checklist

Before marking work complete:

- [ ] Every new function has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] No errors or warnings in output

---

## TDD Evidence Format (For Subagent Verification)

When implementing as a subagent, you MUST output this evidence block:

```yaml
tdd_evidence:
  tests_written:
    - name: "test_feature_x"
      file: "tests/test_x.py"
      red_output: "FAILED - [actual failure message]"
      green_output: "PASSED - 1 passed in 0.05s"
  implementation_files:
    - path: "src/feature.py"
  all_tests_pass: true
  test_command: "pytest tests/test_x.py -v"
  final_output: "[full test output]"
```

**This is REQUIRED for SubagentStop hook verification.**

---

## Integration

**Use with:**
- `code-debug` - Write failing test to reproduce bug before fixing
- `task-dispatch` - Subagents follow TDD for each task
- `completion-verify` - Run tests before claiming completion
