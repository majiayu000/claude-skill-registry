---
name: test-review
description: Audit tests for missing edge cases after writing or reviewing test code. Use PROACTIVELY after implementing features or writing tests. Also available as /test-review.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Test Review — Edge Case Audit

Systematic second-pass review of tests after implementation. Catches the gaps that first-pass test writing consistently misses.

## When to use

- **Automatically** after implementing a feature with tests (model-invocable)
- **Manually** via `/test-review` when reviewing test coverage
- **On PRs** as a pre-merge quality gate

## Arguments

- `path` (optional): Specific test file or directory to audit, e.g. `/test-review tests/test_merge.py`
- If no argument, detect changed files via `git diff main...HEAD --name-only`

## Step 1: Identify scope

Determine what was implemented and what tests exist:

1. Find changed source files:
   ```
   Bash: git diff main...HEAD --name-only -- 'src/'
   ```

2. Find changed/new test files:
   ```
   Bash: git diff main...HEAD --name-only -- 'tests/'
   ```

3. Read each changed source file to understand the new/modified code paths
4. Read each test file to understand current coverage

## Step 2: Run the edge case checklist

For every new function, method, class, or code path, systematically check each category. **Do not skip categories** — the value is in the exhaustive scan.

### Category 1: Boundary Values
- [ ] Empty inputs: empty string `""`, empty list `[]`, empty dict `{}`
- [ ] Zero: `0`, `0.0` — especially when used as falsy-but-present
- [ ] Negative numbers: `-1`, `-0.5`
- [ ] `None` / missing / unset where the type allows it
- [ ] Single-element collections: list with 1 item, dict with 1 key
- [ ] Maximum/overflow: very long strings, very large numbers, deeply nested dicts

### Category 2: Type Coercion and Representation
- [ ] Falsy-but-present values: `0`, `""`, `False`, `[]` that exist but evaluate as falsy
- [ ] String-to-type boundaries: `"0"` vs `0`, `"false"` vs `False`, `"null"` vs `None`
- [ ] Case sensitivity: uppercase, lowercase, mixed case where relevant
- [ ] Type mismatches: passing wrong type where the code does duck typing

### Category 3: State and Mutation
- [ ] Input mutation: are inputs unchanged after the operation?
- [ ] Return value identity: is the result a new object, not a reference to input?
- [ ] Idempotency: calling the same operation twice produces same result
- [ ] Order dependence: does the order of inputs matter? Is it tested?

### Category 4: Cross-Feature Interaction
- [ ] Feature A + Feature B in same expression/call
- [ ] New feature combined with all existing selectors/operators/modes
- [ ] New feature through the full stack (unit test passes, but does it work via the public API?)
- [ ] New feature with observe mode, enforce mode, and any other modes

### Category 5: Error Paths and Degradation
- [ ] Invalid input: what should raise, and does it?
- [ ] Missing dependencies: optional feature not available
- [ ] Duplicate entries: same ID, same key, same value appearing twice
- [ ] Conflict resolution: when two things disagree, which wins? Is that tested?

### Category 6: User-Facing Outputs
- [ ] Error messages contain useful information
- [ ] Log messages fire at correct level (warning for duplicates, etc.)
- [ ] Message templates / string formatting with the new feature's data
- [ ] Audit events include the new feature's attributes

### Category 7: Documented Non-Behavior
- [ ] What intentionally does NOT happen? (e.g., hooks not merged, adapters not changed)
- [ ] Backward compatibility: existing tests still pass with new code
- [ ] Features that are explicitly out of scope — test they don't accidentally work

## Step 3: Generate missing test cases

For each gap found, write a specific test case description:

```
MISSING: [Category] — [Description]
  File: tests/test_xxx.py
  Test: test_[descriptive_name]
  Why:  [What could go wrong without this test]
```

Group by priority:
1. **P0 — Correctness**: Could cause wrong behavior in production
2. **P1 — Robustness**: Edge cases that real users will hit
3. **P2 — Completeness**: Nice to have, documents behavior

## Step 4: Write the tests

For each missing test case (P0 and P1 at minimum):
1. Write the test in the appropriate test file
2. Follow existing test patterns and conventions in the file
3. Run the new tests to verify they pass:
   ```
   Bash: pytest {test_file} -v --tb=short -k {test_name}
   ```

## Step 5: Final verification

```
Bash: pytest tests/ -v --tb=short
Bash: ruff check src/ tests/
```

## Step 6: Report

Summarize:
- How many gaps found per category
- How many tests added (P0/P1/P2)
- Any gaps intentionally left (with reason)

## Rules

- **Don't duplicate existing tests.** Read them first.
- **Don't test framework internals.** Only test our code's behavior.
- **Don't add tests for hypothetical features.** Only test what exists.
- **Match the existing test style.** Same fixtures, same helpers, same naming.
- **Every test must assert something specific.** No "smoke tests" that just check no exception.
