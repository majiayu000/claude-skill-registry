---
name: test-fix
description: This skill should be used when validate-chunk reports test failures specifically, when the user says "tests are failing", "figure out what's wrong with the tests", "fix the failing tests", or when test assertions don't match expected output after chunk implementation. Triages whether the test or the implementation is wrong and fixes the correct one.
version: 1.2.0
allowed-tools: ["Read", "Edit", "Bash", "Glob", "Grep"]
---

# Test Fix Skill

You are the **test triage specialist** — when a test fails after chunk implementation, you determine which side is wrong: the test or the code. Tests break for two very different reasons, and they need opposite fixes.

## When This Activates

- validate-chunk reported **test failures** (not type/lint/build errors)
- A test assertion doesn't match expected output
- Tests that passed before the chunk now fail

## Orchestrator Context

The orchestrator may pass enriched args with labeled fields. Parse these to start triage faster:

- `CHUNK:` "N/total: chunk title" — identifies the chunk
- `CHUNK_GOAL:` what the chunk was supposed to build — key for intent determination
- `FAILING_TESTS:` test file names + error summary — start from these instead of re-running
- `ERRORS:` error output — skip straight to triage with this output
- `FILES_CHANGED:` comma-separated paths — know what the chunk touched

**Fallback:** Args may be just a file path. Gather context from the story file and test output directly.

## Triage Philosophy

**Understand intent before touching anything:**
- The chunk changed something on purpose
- The test might be asserting the OLD behavior
- Or the implementation might genuinely be wrong
- Your job: figure out which, then fix the right one

**Tests are a contract, not scripture:**
- When requirements change, the contract updates
- A stale test is not a failing implementation
- But a valid test IS a failing implementation

**One question matters:** Did the chunk intend to change the behavior this test asserts?

**Always synchronous:**
- **NEVER use `run_in_background: true` for test commands.** All test runs must complete synchronously so results are confirmed before proceeding.
- Background test runs become orphaned and spam the conversation long after the story is done.

## Triage Process

**When multiple tests fail, triage each independently.** Some may be stale while others reveal real bugs. Fix what you can (stale tests), hand off what you can't (code bugs), and report everything in one combined output.

### Step 1: Gather Context

Read three things:

1. **The failing test(s)** — What does each assert? What behavior does each expect?
2. **The implementation** — What does the code actually do now?
3. **The chunk spec** — Read `### Chunk [N]:` from the story file. What was this chunk supposed to change? Check the "Done When" criteria.

### Step 2: Quick Compile Check

Before triaging assertions, verify the test can compile. Use the project's typecheck command (not raw `tsc` which may have flag compatibility issues):
```bash
$PM run typecheck 2>&1
```

**If the test has compile errors** (missing imports, wrong types after refactor): this is a type error, not a test logic issue. The chunk likely didn't finish its job (e.g., renamed exports but missed updating test imports). Report back to orchestrator for `refine-chunk`. Don't triage further.

### Step 3: Determine Intent

Ask these questions in order:

```
Q1: Does the chunk spec say to change the behavior the test asserts?
    → YES → Test is stale. Go to Step 4a.
    → NO  → Continue to Q2.

Q2: Does the implementation match the chunk spec?
    → YES → Behavior changed as a side effect. Test is stale. Go to Step 4a.
           (This includes mock/dependency issues - e.g., chunk added a new DB call
            that the test's mocks don't cover. The test setup needs updating, not the code.)
    → NO  → Implementation diverged from spec. Code is wrong. Go to Step 4b.

Q3: Neither is clearly wrong?
    → Go to Step 4c.
```

### Step 4a: Test is Stale — Update It

The chunk intentionally changed behavior. The test asserts old behavior. Fix the test:

1. **Read the test carefully** — Understand what it's checking
2. **Update assertions** to match the new behavior
3. **Don't gut the test** — Keep the same test structure, just update expected values
4. **Add a comment if the change is non-obvious:** `// Updated: chunk changed X to return Y instead of Z`
5. **Re-run the test** to verify it passes now:
   ```bash
   $PM test -- --testPathPattern="path/to/failing.test" --no-coverage
   ```

**Report back:**
```markdown
## Test Fix Applied

**Verdict:** Test was stale — asserting pre-chunk behavior.

**Test:** `path/to/file.test.ts`
**Assertion:** Expected `oldValue`, implementation now returns `newValue`
**Reason:** Chunk [N] changed [behavior] per spec.

**Fix:**
| File | Change |
|------|--------|
| `path/to/file.test.ts:42` | Updated assertion from `oldValue` to `newValue` |

**Re-run result:** Tests pass after fix.

>>> HAND BACK TO validate-chunk: Re-validate this chunk now. This test fix does NOT complete validation — validate-chunk must re-run the full check suite.
```

### Step 4b: Code is Wrong — Hand Off

The test is correct. The implementation has a bug. Don't fix it yourself — report back to the orchestrator for `refine-chunk`:

```markdown
## Test Fix — Code Issue Found

**Verdict:** Implementation is wrong — test is correct.

**Test:** `path/to/file.test.ts`
**Assertion:** Expects `expectedValue`
**Implementation:** Returns `actualValue`
**Root cause:** [Brief analysis of why the code is wrong]

**Action:** Invoke refine-chunk to fix the implementation.

>>> HAND BACK TO validate-chunk: Route to refine-chunk for code fix, then re-validate.
```

### Step 4c: Ambiguous — Ask User

Can't determine which side is wrong. Present both options:

```markdown
## Test Fix — Needs Human Decision

**Test expects:** [X]
**Implementation does:** [Y]
**Chunk spec says:** [Z]

I can't determine which is correct. Options:

1. **Update the test** — If [Y] is the intended behavior
2. **Fix the code** — If [X] is the intended behavior
3. **Both need changes** — Neither matches the spec

Which should I fix?
```

Use **AskUserQuestion** with these options. After the user decides and the fix is applied:

```markdown
>>> HAND BACK TO validate-chunk: After user decides, route accordingly, then re-validate.
```

## Common Scenarios

For worked examples of each triage outcome (stale assertions, renamed exports, changed props, changed API shapes, new validation, side-effect changes):

> **Common scenarios:** Read `${CLAUDE_PLUGIN_ROOT}/skills/test-fix/references/scenario-catalog.md` for worked examples of each triage outcome with diff examples.

## Handoff Protocol

After triage, report back to the orchestrator with ONE of:

| Verdict | Action | REFINE_COUNT |
|---------|--------|-------------|
| Test stale | Updated test, re-validated | No increment |
| Code wrong | Hand to refine-chunk | Orchestrator increments |
| Ambiguous | Asked user, then acted | Depends on outcome |
| Compile error | Hand to refine-chunk | Orchestrator increments |

**Key:** Test-fix fixing a stale test does NOT count as a refinement. The implementation was correct — only the test was outdated. REFINE_COUNT only increments for actual code fixes.

## Output Format

Always report in this structure (validate-chunk parses it):

```markdown
## Test Fix: [Verdict]

**Test:** [file path]
**Verdict:** Test stale | Code wrong | Ambiguous | Compile error
**Action taken:** [Updated test | Handed to refine-chunk | Asked user]

[Details specific to verdict — see Step 4a/4b/4c above]

>>> HAND BACK TO validate-chunk: [Next step for validate-chunk to take]
```

The `>>> HAND BACK TO validate-chunk:` line MUST be the very last line of every test-fix output. This is the signal that control returns to the invoking skill.

## Remember

- **Read the chunk spec first** — Intent determines the answer
- **Don't assume the test is right** — Tests go stale when behavior changes
- **Don't assume the code is right** — Tests exist for a reason
- **When in doubt, ask** — A wrong guess wastes more time than a question
- **Preserve test quality** — When updating tests, keep them meaningful. Don't just make them pass by weakening assertions.
- **Always end output with `>>> HAND BACK TO validate-chunk:`.** This is the return signal. Without it, the conversation stalls.
