---
name: scientific-tdd
description: Pragmatic test-driven development for scientific code with numerical validation
tags: [testing, tdd, scientific, numerical]
version: 1.0
---

# Scientific Test-Driven Development

## Overview

Pragmatic test-driven development for scientific code: write tests first for new features and complex changes, verify with tests for simple bug fixes.

**Core principle:** Tests before implementation for new behavior, tests verify implementation for known bugs.

**Announce at start:** "I'm using the scientific-tdd skill to implement this feature."

## When to Use This Skill

**MUST use for:**

- New features or algorithms
- Complex modifications to existing code
- Adding new mathematical models
- Implementing new likelihood functions or state transitions

**Can skip test-first for:**

- Simple bug fixes where existing tests already cover the behavior
- Documentation changes
- Refactoring with existing comprehensive tests (use safe-refactoring instead)

## Process Checklist

Copy to TodoWrite:

```
Scientific TDD Progress:
- [ ] Understand existing behavior (read code and tests)
- [ ] Write test capturing desired new behavior
- [ ] Run test to confirm RED (fails as expected)
- [ ] Implement minimal code to pass test
- [ ] Run test to confirm GREEN (passes)
- [ ] Run full test suite (check for regressions)
- [ ] Run numerical validation if mathematical code changed
- [ ] Run code-reviewer agent (and/or ux-reviewer when appropriate)
- [ ] Refactor if needed (keep tests green)
- [ ] Commit with descriptive message
```

## Detailed Steps

### Step 1: Understand Existing Behavior

Before writing new tests, understand current state:

- Read relevant source files
- Read existing tests for similar functionality
- Run existing tests to see current behavior
- Identify what needs to change

**Commands:**

```bash
# Find relevant tests
pytest --collect-only -q | grep <relevant_term>

# Run specific test file
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest src/non_local_detector/tests/<test_file>.py -v
```

### Step 2: Write Failing Test (RED)

Write test that captures desired behavior:

**Test Structure:**

```python
def test_descriptive_name_of_behavior():
    """Test that [specific behavior] works correctly.

    This test verifies that [explain what you're testing] when [condition].
    """
    # Arrange: Set up test data
    input_data = create_test_input()

    # Act: Call the function/method
    result = function_under_test(input_data)

    # Assert: Verify behavior
    assert result.shape == expected_shape
    assert np.allclose(result.sum(), 1.0, atol=1e-10)  # Probabilities sum to 1
```

**For mathematical code, verify:**

- Correct output shapes
- Mathematical invariants (probabilities sum to 1, matrices are stochastic)
- Expected numerical values (with appropriate tolerances)
- Edge cases (empty inputs, single element, boundary conditions)

### Step 3: Run Test - Confirm RED

**CRITICAL:** Test MUST fail before implementing:

```bash
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest src/non_local_detector/tests/<test_file>.py::test_name -v
```

**Expected output:** Test fails with clear error (function not defined, wrong output, etc.)

**If test passes:** The test isn't testing new behavior - reconsider what you're testing.

### Step 4: Implement Minimal Code

Write simplest code that makes test pass:

- Don't over-engineer
- Don't add features not tested
- Follow YAGNI (You Aren't Gonna Need It)
- Use existing patterns from codebase

**For scientific code:**

- Maintain numerical stability
- Use JAX operations where appropriate
- Follow existing conventions for shapes and broadcasting

### Step 5: Run Test - Confirm GREEN

```bash
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest src/non_local_detector/tests/<test_file>.py::test_name -v
```

**Expected output:** Test passes

**If test fails:** Debug until it passes, then verify you're testing the right thing.

### Step 6: Run Full Test Suite

Check for regressions:

```bash
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest -v
```

**Expected:** All tests pass (same count as before)

**If new failures:** Your change broke something - fix before proceeding.

### Step 7: Numerical Validation (if applicable)

If you modified mathematical/algorithmic code:

**Use numerical-validation skill:**

```
@numerical-validation
```

This verifies:

- Mathematical invariants still hold
- Property-based tests pass
- Golden regression tests pass
- No unexpected numerical differences

### Step 8: Refactor (optional)

If code can be improved while keeping tests green:

- Improve readability
- Extract reusable functions
- Optimize performance (but verify numerics don't change)

**After each refactor:**

```bash
/Users/edeno/miniconda3/envs/non_local_detector/bin/pytest -v
```

### Step 9: Commit

```bash
git add <test_file> <implementation_file>
git commit -m "feat: add <feature description>

- Add test for <specific behavior>
- Implement <what you implemented>
- All tests passing (<N> tests)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Example Workflow

**Task:** Add new random walk transition with custom variance

```
1. Read: src/non_local_detector/continuous_state_transitions.py
2. Read: src/non_local_detector/tests/transitions/test_continuous_transitions.py
3. Write test: test_random_walk_custom_variance()
4. Run test: FAIL - "NotImplementedError: custom variance not supported"
5. Implement: Add variance parameter to RandomWalk class
6. Run test: PASS
7. Run full suite: 427 tests passed
8. Run numerical validation: All invariants hold
9. Commit: "feat: add custom variance support to RandomWalk"
```

## Integration with Other Skills

- **Before using this skill:** Often preceded by brainstorming or design discussion
- **Use with numerical-validation:** For mathematical code changes
- **After this skill:** May use safe-refactoring for cleanup
- **Alternative to this skill:** Use safe-refactoring if changing structure, not behavior

## Red Flags

**Don't:**

- Write implementation before test (except for documented bug fixes)
- Skip running test to see it fail
- Add untested code "for future use"
- Skip full test suite after implementation
- Commit failing tests
- Skip numerical validation for mathematical code

**Do:**

- Write descriptive test names
- Test one behavior per test
- Use appropriate numerical tolerances (1e-10 for probabilities)
- Run tests frequently
- Commit small, working increments
- Ask if unsure whether to use TDD for a specific change
