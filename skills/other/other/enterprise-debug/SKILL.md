---
name: enterprise-debug
description: "4-phase systematic debugging: investigate, blast radius scan, root cause identification, TDD fix. Finds root causes not symptoms. Blast radius scan catches sibling bugs. 3-fail circuit breaker prevents fix-forward loops. Use for any bug, test failure, or unexpected behavior."
---

# Enterprise Debug — 4-Phase Systematic Debugging

## Philosophy

Bugs are never unique. If it is a bug here, it is a bug elsewhere. The blast radius scan is what separates enterprise debugging from guessing.

Three rules:
1. **Find the root cause, not the symptom.** A symptom fix creates two future bugs.
2. **Scan the blast radius.** The same class of bug exists in sibling functions, sibling files, and validation code.
3. **Prove the fix with TDD.** A fix without a failing test is a guess.

```
/enterprise-debug order duplication — processOrder called twice in orderHandler.js
/enterprise-debug test failure: userService.test.js "rejects empty email" now fails
/enterprise-debug users report wrong totals on dashboard page
```

---

## STACK RESOLUTION

Read `.claude/enterprise-state/stack-profile.json` at skill start. Extract:
- `$TEST_CMD` = `commands.test_all`
- `$TEST_SINGLE` = `commands.test_single`
- `$SOURCE_DIR` = `structure.source_dirs.backend`
- `$TENANT_FIELD` = `multi_tenancy.field`
- `$FILE_EXTENSIONS` = `conventions.file_extensions`

If no profile exists: BLOCKED — run /enterprise-discover first.

---

## Phase 1: INVESTIGATE (5-15 minutes)

Goal: reproduce the bug, trace the execution path, form a hypothesis.

### Step 1: Reproduce

Get the exact error. Not a description of the error — the actual error.

```
REPRODUCTION
════════════
Trigger:     [exact steps to reproduce — API call, user action, cron job]
Error:       [exact error message, stack trace, or wrong behavior]
Expected:    [what should happen instead]
Frequency:   [always / intermittent / only under specific conditions]
Environment: [dev / prod / both]
```

If you cannot reproduce, you cannot fix. Spend time here.

**For test failures**: run the failing test and paste the full output.
```bash
$TEST_SINGLE --testPathPattern="<pattern>" --no-coverage 2>&1
```

**For runtime errors**: find the error in logs or reproduce via API call.
```bash
curl -s http://localhost:3000/api/<endpoint> | jq .
```

**For "wrong data" reports**: query the database directly to confirm the data is wrong (not just the display).
```sql
SELECT relevant_columns FROM table WHERE conditions;
```

### Step 2: Trace the Execution Path

Follow the data end-to-end. Every layer. No shortcuts.

```
EXECUTION TRACE
═══════════════
Entry point:  [route/job/webhook that triggers the code]
  → Middleware: [auth, validation — file:line]
  → Route:     [handler function — file:line]
  → Service:   [business logic function — file:line]
  → Query:     [SQL or ORM call — file:line]
  → DB:        [table(s) affected, actual data state]
  → Response:  [what gets returned — file:line]
  → Consumer:  [frontend hook/component — file:line]
  → Render:    [what the user sees — file:line]
```

Read every file in the trace. Do not skip layers. The bug is often NOT where you think it is.

### Step 3: Form a Hypothesis

```
HYPOTHESIS
══════════
I think: [specific root cause]
Because: [evidence from the trace — cite file:line]
This predicts: [if I'm right, then X should also be true]
Verification: [how to test the hypothesis — a query, a log check, a test]
```

Run the verification. If the hypothesis is wrong, form a new one. Do not proceed to Phase 2 until the hypothesis is verified.

### Step 4: Find Working Examples

Search for similar code that works correctly. This reveals what the buggy code is missing.

```bash
# Find functions doing the same operation that work correctly
grep -r "similar_pattern" $SOURCE_DIR/ --include='*.$FILE_EXTENSIONS' -l
```

Compare the working version with the broken version. The difference is often the fix.

---

## Phase 2: BLAST RADIUS SCAN (5-10 minutes)

**This phase is MANDATORY.** Do not skip it. Do not abbreviate it. The blast radius scan is the single highest-value activity in debugging.

### 2a: Same-File Siblings

If the buggy function belongs to a group of similar functions in the same file, check EVERY sibling.

```
SAME-FILE SIBLINGS: [file path]
═══════════════════
Buggy function: [name] — line [N]
Bug class:      [what category of bug — missing filter, wrong column, no null guard, etc.]

Sibling 1: [function name] — line [N]
  Has same guard/filter? [YES / NO — SAME BUG]

Sibling 2: [function name] — line [N]
  Has same guard/filter? [YES / NO — SAME BUG]

... (list ALL siblings, not "a few")
```

**Example**: If `searchSuppliers()` is missing a `WHERE is_active = true` filter, check `searchOrders()`, `searchProducts()`, `searchCustomers()` — every search function in the same file.

### 2b: Cross-File Siblings

Search the ENTIRE module/service directory for functions doing the same logical operation.

```bash
# Find all functions with similar names
grep -rn "function.*Staff\|getStaff\|staff.*query\|staff.*list" $SOURCE_DIR/services/ --include='*.$FILE_EXTENSIONS'

# Find all functions with similar SQL patterns
grep -rn "SELECT.*FROM.*staff\|FROM.*users.*WHERE" $SOURCE_DIR/ --include='*.$FILE_EXTENSIONS'

# Find all files in the same service directory
ls $SOURCE_DIR/services/<module>/
```

```
CROSS-FILE SIBLINGS
════════════════════
Bug class: [what to search for]

Match 1: [function name] in [file:line]
  Does same logical operation? [YES / NO]
  Has same guard/filter?       [YES / NO — SAME BUG]

Match 2: [function name] in [file:line]
  Does same logical operation? [YES / NO]
  Has same guard/filter?       [YES / NO — SAME BUG]

... (list ALL matches from grep scan)
```

### 2c: Validation and Consumer Functions

Find every function that consumes or validates the same data.

```bash
# Find consumers of the affected data
grep -rn "variable_name\|function_name" $SOURCE_DIR/ --include='*.$FILE_EXTENSIONS'
```

```
CONSUMERS & VALIDATORS
══════════════════════
Data source: [function that produces the data]

Consumer 1: [function/component name] in [file:line]
  Purpose:  [what it does with the data]
  Affected by bug? [YES — needs fix / NO — different data path]

Consumer 2: [function/component name] in [file:line]
  Purpose:  [what it does with the data]
  Affected by bug? [YES — needs fix / NO — different data path]

Validator 1: [function name] in [file:line]
  Enforces same constraints? [YES / NO — MISSING GUARD]
```

### 2d: Edge Cases

For each bug, systematically check boundary conditions:

```
EDGE CASES
══════════
Empty/null input:           [OK / BUG — describe]
Zero-length array:          [OK / BUG — describe]
Inactive/deleted records:   [OK / BUG — describe]
System/service accounts:    [OK / BUG — describe]
Permission boundaries:      [OK / BUG — describe]
Different entry points:     [OK / BUG — describe]
  - API route:              [OK / BUG]
  - Internal service call:  [OK / BUG]
  - Cron/background job:    [OK / BUG]
Concurrent execution:       [OK / BUG — describe]
Very large input (10K+):    [OK / BUG — describe]
Unicode/special characters: [OK / BUG — describe]
```

### Blast Radius Summary

```
BLAST RADIUS SUMMARY
════════════════════
Same-file siblings checked:  [N] — [N] with same bug
Cross-file siblings checked: [N] — [N] with same bug
Consumers/validators:        [N] — [N] affected
Edge cases checked:          [N] — [N] bugs found

Total additional bugs found: [N]
All findings become postconditions in Phase 4.
```

---

## Phase 3: ROOT CAUSE (2-5 minutes)

### Identify the Single Root Cause

The root cause is ONE thing. Not "multiple issues" — one thing that, when fixed, resolves all manifestations.

```
ROOT CAUSE
══════════
What:  [the specific defect — e.g., "missing WHERE is_active = true in getStaffUsers query"]
Where: [exact file:line]
Why:   [how it got there — copied from a function that didn't need the filter,
        original author didn't consider inactive users, etc.]
When:  [when it was introduced — git blame if useful]

Verification: fixing this one thing fixes ALL of the following:
  1. [original bug report symptom]
  2. [blast radius finding 1]
  3. [blast radius finding 2]
  ...
```

### Verify the Root Cause

Ask: "If I fix ONLY this one thing, does every manifestation resolve?"

- YES: proceed to Phase 4.
- NO: you found a symptom, not the root cause. Go deeper.

### The Circuit Breaker (NON-NEGOTIABLE)

Track your fix attempts — persisted in JSON so the count survives context compression:

```bash
# Read current fix attempt count
node -e "
  const fs = require('fs');
  const f = '.claude/enterprise-state/<slug>.json';
  try {
    const s = JSON.parse(fs.readFileSync(f));
    s.circuit_breakers.debug_fix_attempts++;
    console.log('Fix attempt:', s.circuit_breakers.debug_fix_attempts, '/', s.circuit_breakers.debug_max);
    if (s.circuit_breakers.debug_fix_attempts >= s.circuit_breakers.debug_max) {
      console.log('>>> CIRCUIT BREAKER TRIGGERED <<<');
    }
    fs.writeFileSync(f, JSON.stringify(s, null, 2));
  } catch(e) {
    console.log('No pipeline state file — tracking manually');
  }
"
```

```
FIX ATTEMPTS (also persisted in .claude/enterprise-state/<slug>.json)
═════════════
Attempt 1: [what you tried] — Result: [still broken because...]
Attempt 2: [what you tried] — Result: [still broken because...]
Attempt 3: [what you tried] — Result: [still broken because...]

>>> CIRCUIT BREAKER TRIGGERED <<<
```

**If 3 fix attempts fail**: STOP. Do not try fix #4. Instead:

1. **Question the architecture.** The bug may be a design problem, not a code problem.
2. **Widen the investigation.** You may be looking at the wrong layer entirely.
3. **Ask for help.** Describe what you've tried and why each attempt failed.
4. **Consider rewriting.** If the code is unmaintainable, a targeted rewrite may be cheaper than a 4th patch.

The circuit breaker exists because fix-forward loops are the most expensive failure mode in debugging. Each failed attempt adds complexity, introduces regression risk, and burns context. Three attempts is the limit.

---

## Phase 4: FIX — TDD (5-20 minutes)

Every bug fix follows the TDD sequence. No exceptions.

### Step 1: Write the Reproduction Test

Write a test that proves the bug exists by asserting the WRONG behavior.

```javascript
// Example: bug is that getStaffUsers returns inactive users
test('BUG REPRODUCTION: getStaffUsers currently returns inactive users', async () => {
  // Setup: create an inactive user
  // Act: call getStaffUsers
  // Assert: inactive user IS in the result (proving the bug exists)
  const result = await getStaffUsers(tenantId);
  const inactiveUser = result.find(u => u.id === inactiveUserId);
  expect(inactiveUser).toBeDefined(); // This PASSES — bug exists
});
```

### Step 2: Run the Test — Watch it PASS

```bash
$TEST_SINGLE --testPathPattern="<pattern>" --no-coverage 2>&1 | tail -20
```

The test MUST pass. This proves the bug is real and the test catches it.

### Step 3: Invert the Assertion

Change the test to assert the CORRECT behavior.

```javascript
test('getStaffUsers excludes inactive users', async () => {
  const result = await getStaffUsers(tenantId);
  const inactiveUser = result.find(u => u.id === inactiveUserId);
  expect(inactiveUser).toBeUndefined(); // This FAILS — fix not applied yet
});
```

### Step 4: Run the Test — Watch it FAIL

```bash
$TEST_SINGLE --testPathPattern="<pattern>" --no-coverage 2>&1 | tail -20
```

The test MUST fail. This proves the test will catch regressions.

### Step 5: Write the Fix

Fix the root cause identified in Phase 3.

### Step 6: Run the Test — Watch it PASS

```bash
$TEST_SINGLE --testPathPattern="<pattern>" --no-coverage 2>&1 | tail -20
```

The test MUST pass. The bug is fixed.

### Step 7: Blast Radius Postconditions

Every finding from Phase 2 becomes a test:

```
POSTCONDITION MAPPING
═════════════════════
Root cause fix:
  PC-1: [original bug] → test: "[test description]"

Same-file siblings:
  PC-2: [sibling 1 fix] → test: "[test description]"
  PC-3: [sibling 2 fix] → test: "[test description]"

Cross-file siblings:
  PC-4: [cross-file fix] → test: "[test description]"

Edge cases:
  PC-5: [null input handling] → test: "[test description]"
  PC-6: [inactive user handling] → test: "[test description]"

Consumer verification:
  PC-7: [consumer 1 gets correct data] → test: "[test description]"
  PC-8: [consumer 2 gets correct data] → test: "[test description]"
```

Write each test following the same RED-GREEN sequence (steps 3-6).

### Step 8: Run Full Suite

```bash
$TEST_CMD --no-coverage 2>&1 | tail -30
```

All tests must pass. Zero regressions.

### Step 9: Commit

```bash
git add -A && git commit -m "fix: [root cause description]

Blast radius: [N] sibling bugs fixed, [N] edge cases covered
Tests: [N] new tests, [N] total passing"
```

---

## Output — Debug Report

Print this as your final output after the fix is verified:

```
═══════════════════════════════════════════════════════════
                    ENTERPRISE DEBUG REPORT
═══════════════════════════════════════════════════════════

## Bug
[1-2 sentence description of the bug as reported]

## Root Cause
[1-2 sentences — the actual defect, not the symptom]
File: [file:line]

## Investigation Trace
Entry → [layer] → [layer] → [layer] → ROOT CAUSE at [file:line]

## Blast Radius
Same-file siblings:   [N] checked, [N] had same bug
Cross-file siblings:  [N] checked, [N] had same bug
Consumers/validators: [N] checked, [N] affected
Edge cases:           [N] checked, [N] bugs found
Total additional bugs found: [N]

## Fix
Files changed: [list]
  [file 1]: [what changed and why]
  [file 2]: [what changed and why]

## TDD Evidence
  PC-1: [description] — RED at [time] → GREEN at [time]
  PC-2: [description] — RED at [time] → GREEN at [time]
  ...
  Tests: [N] new, [N] total passing, 0 failing

## Fix Attempts
  Attempts: [N] (limit: 3)
  Circuit breaker: [not triggered / triggered at attempt N]

## Prevention
  [How to prevent this class of bug in future — pattern to follow,
   lint rule to add, guard to standardize]

═══════════════════════════════════════════════════════════
```

---

## Quick Reference — When to Use Each Phase

| Situation | Phases |
|-----------|--------|
| Test failure with clear error | Phase 1 (reproduce) → Phase 3 (root cause) → Phase 4 (TDD fix) |
| "Wrong data" user report | Phase 1 (reproduce + trace ALL fields) → Phase 2 (full blast radius) → Phase 3 → Phase 4 |
| Intermittent error | Phase 1 (reproduce — spend extra time) → Phase 2 (race conditions) → Phase 3 → Phase 4 |
| Regression after deploy | Phase 1 (git bisect to find the commit) → Phase 2 → Phase 3 → Phase 4 |
| Performance issue | Phase 1 (measure baseline) → Phase 2 (find N+1, unbounded queries) → Phase 3 → Phase 4 |

---

## Anti-Patterns — Things That Feel Productive but Waste Time

| Anti-Pattern | Why It Fails | Do This Instead |
|-------------|-------------|-----------------|
| Fix the first thing you see | It is usually a symptom, not the cause | Trace end-to-end first |
| Add a try/catch around the error | Hides the bug, does not fix it | Find and fix the root cause |
| "Works on my machine" | Different data, different state, different timing | Reproduce with the same data/state |
| Fix only the reported instance | Same bug exists in 5 sibling functions | Blast radius scan |
| Skip the test, "I can see it works" | You cannot see race conditions, edge cases, or regressions | TDD — always |
| Fix attempt #4 after 3 failures | Diminishing returns, increasing risk | Circuit breaker — question architecture |
| Fix forward instead of revert | Each patch adds complexity | If the fix is not obvious, revert first |
