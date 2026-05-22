---
name: safe-refactoring
description: Change code structure without changing behavior, with zero tolerance for behavioral changes
tags: [refactoring, testing, scientific, quality]
version: 1.0
---

# Safe Refactoring for Scientific Code

## Overview

Change code structure without changing behavior. Zero tolerance for behavioral changes during refactoring.

**Core principle:** Establish baseline, refactor, verify exact match (within floating-point noise).

**Announce at start:** "I'm using the safe-refactoring skill to restructure this code."

## When to Use This Skill

**Use for:**
- Improving code readability without changing logic
- Extracting reusable functions
- Renaming variables/functions for clarity
- Reorganizing code structure
- Performance optimization (without changing numerical behavior)

**Don't use for:**
- Changing behavior or algorithms (use scientific-tdd instead)
- Adding new features (use scientific-tdd instead)
- Fixing bugs (use scientific-tdd or fix directly with tests)

## Process Checklist

Copy to TodoWrite:

```
Safe Refactoring Progress:
- [ ] Run full test suite (establish baseline)
- [ ] Run snapshot tests (establish baseline)
- [ ] Capture coverage report
- [ ] Perform refactoring
- [ ] Run full test suite (must match baseline exactly)
- [ ] Run snapshot tests (must match baseline exactly)
- [ ] Compare coverage (should stay same or improve)
- [ ] Run quality checks (ruff + black)
- [ ] Verify no numerical differences
- [ ] Commit refactoring
```

## Strict Rules

**ZERO tolerance for:**
- Any test that passed before and fails after
- Any test that failed before and passes after (suggests test was broken)
- Any snapshot differences (not even floating-point noise)
- Decreased test coverage
- Any behavioral changes

**If any of these occur:** Revert and investigate why.

## Detailed Steps

### Step 1: Run Full Test Suite (Baseline)

```bash
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest -v 2>&1 | tee /tmp/baseline_tests.txt
```

**Record:**
- Total tests: `grep "passed" /tmp/baseline_tests.txt`
- Any failures (if refactoring existing code with known issues)
- Test execution time

**Expected:** All tests pass (or document any known failures)

### Step 2: Run Snapshot Tests (Baseline)

```bash
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest -m snapshot -v 2>&1 | tee /tmp/baseline_snapshots.txt
```

**CRITICAL:** Snapshots must match exactly after refactoring.

**Expected:** All snapshot tests pass

### Step 3: Capture Coverage Report

```bash
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest --cov=non_local_detector --cov-report=term --cov-report=json:coverage_baseline.json
```

**Record:** Coverage percentage for files being refactored

**Why:** Coverage should not decrease during refactoring (ideally improves)

### Step 4: Perform Refactoring

**Refactoring techniques:**

1. **Extract function:**
   ```python
   # Before
   def complex_function():
       # ... 50 lines of code
       result = x * 2 + y
       # ... more code
       return final_result

   # After
   def complex_function():
       # ... code
       result = _calculate_intermediate(x, y)
       # ... code
       return final_result

   def _calculate_intermediate(x, y):
       return x * 2 + y
   ```

2. **Rename for clarity:**
   ```python
   # Before
   def f(x):
       return x * 2

   # After
   def calculate_doubled_value(value):
       return value * 2
   ```

3. **Reorganize structure:**
   ```python
   # Before: All in one file

   # After: Separated into modules
   # - core_logic.py
   # - utilities.py
   # - validation.py
   ```

4. **Optimize performance (numerically equivalent):**
   ```python
   # Before
   for i in range(n):
       result[i] = f(x[i])

   # After (JAX)
   result = jax.vmap(f)(x)
   ```

**During refactoring:**
- Make small, incremental changes
- Test after each change if possible
- Keep numerical operations identical
- Maintain exact same algorithms

### Step 5: Run Full Test Suite (Verify Match)

```bash
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest -v 2>&1 | tee /tmp/refactored_tests.txt
```

**Compare to baseline:**
```bash
diff /tmp/baseline_tests.txt /tmp/refactored_tests.txt
```

**MUST verify:**
- Same number of tests run
- Same tests pass
- Same tests fail (if any)
- Similar execution time (within 20%)

**If differences:**
- Any new test failures: REVERT IMMEDIATELY
- Any new test passes: Investigate (test was broken?)
- Different test count: Investigate (tests missing or duplicated?)

### Step 6: Run Snapshot Tests (Verify Match)

```bash
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest -m snapshot -v 2>&1 | tee /tmp/refactored_snapshots.txt
```

**CRITICAL:** Must match baseline EXACTLY.

**Expected:** All snapshot tests pass, no differences

**If snapshot differences:**
1. **DO NOT UPDATE SNAPSHOTS**
2. Investigate why behavior changed
3. This is NOT a refactoring if behavior changed
4. Revert and reconsider approach

### Step 7: Compare Coverage

```bash
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest --cov=non_local_detector --cov-report=term --cov-report=json:coverage_refactored.json
```

**Compare:**
```bash
# If you have jq installed
jq '.totals.percent_covered' coverage_baseline.json
jq '.totals.percent_covered' coverage_refactored.json
```

**Expected:**
- Coverage stays same or improves
- Never decreases

**If coverage decreased:**
- Some code paths no longer tested
- Investigate and fix or revert

### Step 8: Run Quality Checks

```bash
/Users/edeno/miniconda3/envs/spectral_connectivity/bin/ruff check src/
/Users/edeno/miniconda3/envs/spectral_connectivity/bin/ruff format src/
/Users/edeno/miniconda3/envs/non_local_detector/bin/black src/
```

**Expected:** All checks pass

**Fix any issues:** Refactoring is good opportunity to improve code quality

### Step 9: Verify No Numerical Differences

For mathematical code, verify numerical equivalence:

```bash
# Run golden regression
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest \
  src/non_local_detector/tests/test_golden_regression.py -v
```

**Expected:** Exact match (or differences < 1e-14)

**If differences > 1e-14:**
- This is NOT a pure refactoring
- Behavior has changed
- Use numerical-validation skill instead

### Step 10: Commit Refactoring

**Only commit if ALL checks pass:**

```bash
git add <refactored_files> <test_files>
git commit -m "refactor: improve <component> code structure

- Extract <function> for reusability
- Rename <variable> for clarity
- Reorganize <module> structure

No behavioral changes:
- All tests pass (N tests)
- Snapshots unchanged
- Coverage: X% → Y%

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Performance Optimization Refactoring

When optimizing for performance:

1. **Capture performance baseline:**
   ```bash
   pytest --durations=10 > /tmp/baseline_durations.txt
   ```

2. **Make optimization**

3. **Verify numerical equivalence** (use numerical-validation skill)

4. **Measure performance improvement:**
   ```bash
   pytest --durations=10 > /tmp/optimized_durations.txt
   ```

5. **Document improvement:**
   ```
   Optimization: Use JAX vmap instead of for loop
   Speedup: 3.2x (450ms → 140ms)
   Numerical difference: < 1e-14 (verified)
   ```

## Integration with Other Skills

- **Before refactoring:** Consider if change actually needs new behavior (use scientific-tdd instead)
- **With numerical-validation:** If refactoring mathematical code, use numerical-validation to verify equivalence
- **With jax skill:** When optimizing JAX code, use jax skill for best practices

## Example Workflow

**Task:** Extract position decoding logic into reusable function

```
1. Baseline:
   - Run pytest: 427 passed, 0 failed
   - Run snapshots: 15 passed, 0 failed
   - Coverage: 69%

2. Refactor:
   - Extract _decode_position_from_posterior() function
   - Update 3 call sites to use new function
   - No logic changes, just extraction

3. Verify:
   - Run pytest: 427 passed, 0 failed ✓
   - Run snapshots: 15 passed, 0 failed ✓
   - Coverage: 69% (unchanged) ✓

4. Quality:
   - Ruff: All checks pass ✓
   - Black: Formatted ✓

5. Commit:
   "refactor: extract position decoding into reusable function"
```

## Red Flags

**STOP and revert if:**
- Any test changes status (pass → fail or fail → pass)
- Any snapshot differences appear
- Coverage decreases
- Numerical differences > 1e-14
- You're tempted to update snapshots
- You're adding new logic (use scientific-tdd instead)

**Safe to proceed if:**
- All tests match baseline exactly
- No snapshot changes
- Coverage same or better
- Code quality improves
- No new functionality added

## Common Mistakes

**"It's just a small behavioral change"**
- No such thing in refactoring
- Any behavioral change = not refactoring
- Use scientific-tdd for behavioral changes

**"I'll update the snapshots since the new output is better"**
- That's not refactoring, it's changing behavior
- Refactoring = zero snapshot changes
- Use scientific-tdd if output should change

**"Tests are slow, I'll skip them"**
- Never skip tests during refactoring
- Tests are your safety net
- Without tests, you can't verify it's a refactoring

**"Coverage went down but the code is better"**
- Better code shouldn't lose coverage
- Investigate why coverage decreased
- Fix or revert
