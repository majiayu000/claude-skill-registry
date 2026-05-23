---
name: numerical-validation
description: Verify mathematical correctness and numerical accuracy after code changes
tags: [testing, numerical, validation, mathematical, scientific]
version: 1.0
---

# Numerical Validation for Scientific Code

## Overview

Verify that changes to mathematical/algorithmic code maintain numerical accuracy and mathematical properties.

**Core principle:** Capture baseline, make change, compare numerically, verify invariants, provide full analysis.

**Announce at start:** "I'm using the numerical-validation skill to verify mathematical correctness."

## When to Use This Skill

**MUST use when modifying:**

- `src/non_local_detector/core.py` (HMM algorithms)
- `src/non_local_detector/likelihoods/` (likelihood models)
- `src/non_local_detector/continuous_state_transitions.py`
- `src/non_local_detector/discrete_state_transitions.py`
- `src/non_local_detector/initial_conditions.py`
- Any code involving JAX transformations or numerical computations

**Also use when:**

- Refactoring mathematical code (tolerance: 1e-14)
- Optimizing algorithms (tolerance: 1e-10)
- Changing convergence criteria or tolerances
- Updating numerical dependencies

## Process Checklist

Copy to TodoWrite:

```
Numerical Validation Progress:
- [ ] Capture baseline outputs before change
- [ ] Make the code change
- [ ] Capture new outputs after change
- [ ] Compare numerical differences
- [ ] Verify mathematical invariants
- [ ] Run property-based tests
- [ ] Run golden regression tests
- [ ] Generate full analysis report
- [ ] Present analysis and request approval (if differences found)
```

## Detailed Steps

### Step 1: Capture Baseline Outputs

Before making any changes:

```bash
# Run tests and capture output
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest \
  src/non_local_detector/tests/test_golden_regression.py \
  -v > /tmp/baseline_output.txt 2>&1

# Run property tests
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest \
  -m property -v > /tmp/baseline_property.txt 2>&1

# Run snapshot tests
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest \
  -m snapshot -v > /tmp/baseline_snapshot.txt 2>&1
```

**Save output:** Keep baseline files for comparison

### Step 2: Make Code Change

Implement your modification to the mathematical/algorithmic code.

### Step 3: Capture New Outputs

After making changes:

```bash
# Run same tests
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest \
  src/non_local_detector/tests/test_golden_regression.py \
  -v > /tmp/new_output.txt 2>&1

/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest \
  -m property -v > /tmp/new_property.txt 2>&1

/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest \
  -m snapshot -v > /tmp/new_snapshot.txt 2>&1
```

### Step 4: Compare Numerical Differences

**Difference tolerances:**

- **Refactoring (no behavior change):** Max 1e-14 (floating-point noise only)
- **Intentional algorithm changes:** Max 1e-10 (must be justified)
- **Any larger difference:** Requires investigation and explanation

**Compare outputs:**

```bash
# Check if outputs differ
diff /tmp/baseline_output.txt /tmp/new_output.txt
```

**For each difference:**

- Is it expected based on the change?
- What is the magnitude? (< 1e-14 is floating-point noise, < 1e-10 is acceptable for algorithm changes)
- Does it affect scientific conclusions?

### Step 5: Verify Mathematical Invariants

**Critical invariants that must ALWAYS hold:**

1. **Probability distributions sum to 1.0:**

   ```python
   assert np.allclose(probabilities.sum(axis=-1), 1.0, atol=1e-10)
   ```

2. **Transition matrices are stochastic:**

   ```python
   assert np.allclose(transition_matrix.sum(axis=-1), 1.0, atol=1e-10)
   assert np.all(transition_matrix >= 0)
   assert np.all(transition_matrix <= 1)
   ```

3. **Log-probabilities are finite:**

   ```python
   assert np.all(np.isfinite(log_probs))
   ```

4. **Covariance matrices are positive semi-definite:**

   ```python
   eigenvalues = np.linalg.eigvalsh(covariance)
   assert np.all(eigenvalues >= -1e-10)
   ```

5. **Likelihoods are non-negative:**

   ```python
   assert np.all(likelihood >= 0)
   ```

**Verify these with tests or spot checks after changes.**

### Step 6: Run Property-Based Tests

```bash
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest -m property -v
```

**Expected:** All property tests pass

**Property tests verify:**

- Invariants hold across many random inputs (hypothesis library)
- Edge cases are handled correctly
- Mathematical properties are maintained

**If failures:** Investigate why property violated - likely a bug in your change.

### Step 7: Run Golden Regression Tests

```bash
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest \
  src/non_local_detector/tests/test_golden_regression.py -v
```

**Golden regression tests:**

- Use real scientific data
- Compare against validated reference outputs
- Catch subtle numerical changes that affect scientific results

**Expected for refactoring:** Exact match (or < 1e-14 difference)
**Expected for algorithm changes:** Document and justify any differences

### Step 8: Generate Full Analysis Report

Create a comprehensive report with:

**1. Diff - What Changed:**

```
Snapshot changes:
- test_model_output: posterior probabilities differ by max 2.3e-11
- test_transition_matrix: no changes

Test output changes:
- Golden regression: 3 values differ by < 1e-10
```

**2. Explanation - Why It Changed:**

```
Changed optimizer tolerance from 1e-6 to 1e-8, resulting in:
- More precise convergence
- Slight differences in final parameter estimates
- Differences are within acceptable scientific tolerance
```

**3. Validation - Invariants Still Hold:**

```
Verified:
✓ All probabilities sum to 1.0 (max deviation: 3.4e-15)
✓ Transition matrices stochastic (max row sum deviation: 1.2e-14)
✓ No NaN or Inf values in any outputs
✓ All property tests pass (42/42)
✓ Covariance matrices positive semi-definite
```

**4. Test Case - Demonstrate Correctness:**

```python
# Before change:
old_result = [0.342156, 0.657844]  # Posterior at time 10

# After change:
new_result = [0.342156023, 0.657843977]  # Posterior at time 10

# Difference: 2.3e-8 (acceptable)
# Scientific interpretation: No change to conclusions
# Both results indicate strong preference for state 2
```

### Step 9: Present Analysis and Request Approval

**If differences are within tolerance (< 1e-14 for refactoring):**

- Present analysis for information
- Proceed with change
- No approval needed

**If differences are 1e-14 to 1e-10:**

- Present full analysis
- Explain why differences are acceptable
- Request approval: "These differences are expected and scientifically acceptable. Approve?"
- Wait for user response

**If differences are > 1e-10:**

- Present full analysis
- Explain significance of differences
- Provide scientific justification
- Request explicit approval
- If rejected: Investigate further or revert change

## Approval Process

**For snapshot updates with numerical changes:**

1. Generate full analysis (all 4 sections above)
2. Present to user
3. Ask: "These changes are [expected/acceptable/significant]. Approve snapshot update?"
4. If approved: User will set approval flag, then run:

   ```bash
   /Users/edeno/miniconda3/envs/non_local_detector/bin/pytest --snapshot-update
   ```

## Integration with Other Skills

- **Use with scientific-tdd:** After implementing new feature, validate numerics
- **Use with safe-refactoring:** Verify no numerical changes during refactoring
- **Use with jax:** After JAX optimizations, verify numerical equivalence

## Tolerance Guidelines

| Change Type | Max Acceptable Difference | Approval Required |
|-------------|---------------------------|-------------------|
| Pure refactoring | 1e-14 | No |
| Code optimization | 1e-10 | Yes (informational) |
| Algorithm modification | 1e-10 | Yes (justification) |
| > 1e-10 | Any | Yes (strong justification) |

## Example Workflow

**Task:** Refactor HMM filtering to use scan instead of for loop

```
1. Capture baseline:
   - Run golden regression: All pass
   - Run property tests: 42 pass
   - Save outputs to /tmp/baseline_*

2. Make change:
   - Replace for loop with jax.lax.scan
   - Maintain identical logic

3. Capture new outputs:
   - Run same tests: All pass
   - Save outputs to /tmp/new_*

4. Compare:
   - Max difference: 4.2e-15 (floating-point noise)
   - Within refactoring tolerance

5. Verify invariants:
   ✓ Probabilities sum to 1.0
   ✓ No NaN/Inf
   ✓ Property tests pass

6. Report:
   "Refactoring complete. Max numerical difference: 4.2e-15 (floating-point noise).
   All invariants verified. No approval needed."
```

## Red Flags

**Don't:**

- Skip baseline capture
- Ignore numerical differences > 1e-14
- Assume "small" differences don't matter
- Update snapshots without analysis
- Skip property or golden regression tests
- Proceed with NaN/Inf in outputs

**Do:**

- Always capture baseline before changes
- Investigate all unexpected differences
- Verify mathematical invariants explicitly
- Provide full analysis for any differences
- Get approval before snapshot updates
- Document tolerance justifications
