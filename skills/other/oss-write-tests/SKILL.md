---
name: oss-write-tests
description: |
  Write tests for untested OSS code as a standalone contribution. Identifies coverage
  gaps, studies the repo's test conventions, and guides the user through writing tests
  that match existing patterns. Use when contributing tests to an open source repo,
  looking for a low-risk first contribution, or improving test coverage. Not for writing
  tests alongside a bug fix — use oss-contribute for that.
---

# Write Tests

Add tests for untested code — the highest-value, lowest-risk first contribution. You need to understand the code deeply without modifying it, and the result is almost always welcome.

## Purpose

Test contributions teach you a codebase faster than any other contribution type. You read every function signature, trace every code path, and understand every edge case — without the pressure of changing production code. Maintainers love test PRs because they reduce risk for everyone. This skill guides you through finding untested code, learning the repo's test conventions, and writing tests that a maintainer would write themselves.

## When to Use

- Making your first contribution to a repo and want something low-risk
- You've found code with no tests or poor coverage
- You want to learn a codebase deeply before tackling a bug or feature
- **NOT** when writing tests as part of a bug fix — use `oss-contribute` for that
- **NOT** when the repo has no test infrastructure at all — that's a different conversation with maintainers

## Prerequisites

- Repo forked, cloned, and set up (from `oss-prep-to-contribute`)
- Test suite runs successfully (`make test`, `npm test`, `pytest`, etc.)
- User has a target module or area in mind

## Process

### 1. Identify untested code

Find code that lacks test coverage. Use multiple signals — don't rely on just one.

```bash
# Check if the repo has coverage reports
ls coverage/ htmlcov/ .coverage *.lcov 2>/dev/null

# Find source files without corresponding test files
# Adapt the pattern to the repo's naming convention
find src/ -name "*.ts" | while read f; do
  test_file=$(echo "$f" | sed 's|src/|tests/|; s|\.ts$|.test.ts|')
  [ ! -f "$test_file" ] && echo "No tests: $f"
done

# Find public functions without any test assertions
grep -rn "export function\|def \|pub fn\|func " src/ --include="*.ts" --include="*.py" --include="*.rs" --include="*.go" | head -30
```

Then cross-reference against test files:

```bash
# What symbols are already tested?
grep -rn "describe\|it(\|test(\|def test_\|func Test" tests/ test/ __tests__/ spec/ | head -30
```

Look for:
- Source files with zero test counterparts
- Public functions never referenced in test files
- Complex functions with only happy-path tests (no error/edge cases)
- Recently changed code that outpaced its tests (check git log)

### 2. Study the repo's test conventions

Before writing a single test, read 3-5 existing test files in the same area. You must match the repo's patterns exactly.

```bash
# Find test files near the code you're targeting
find tests/ test/ __tests__/ spec/ -name "*relevant_module*" -o -name "*relevant_feature*" 2>/dev/null

# Read the most recent test files (likely to follow current conventions)
git log --diff-filter=A --name-only --pretty=format: -- "tests/" "test/" "__tests__/" "spec/" | head -10
```

Document these conventions:
- **File naming**: `*.test.ts` vs `*_test.go` vs `test_*.py` vs `*_spec.rb`
- **File location**: co-located with source or in separate test directory?
- **Import patterns**: what test framework, what assertion style?
- **Test structure**: BDD (`describe`/`it`) or xUnit (`TestX`) or table-driven?
- **Setup/teardown**: fixtures, factories, `beforeEach`, `setUp`?
- **Mocking strategy**: what gets mocked vs what uses real implementations?
- **Test data**: inline constants, fixture files, factory functions, or builders?
- **Naming conventions**: "should do X" or "test_does_X" or "TestX_WhenY_DoesZ"

### 3. Understand the code under test

Read the target code thoroughly. You're not fixing it — you're documenting its behavior through tests.

```bash
# Read the source file
cat src/path/to/module.ts

# Trace callers — who uses this code?
grep -rn "import.*from.*module\|require.*module" src/ --include="*.ts" --include="*.py"

# Check git history — what was the intent?
git log --oneline -10 -- "src/path/to/module.ts"
git blame src/path/to/module.ts
```

For each function you plan to test, identify:
- **Inputs**: what arguments, what types, what ranges?
- **Outputs**: what does it return? What side effects?
- **Error conditions**: what makes it throw/return an error?
- **Edge cases**: empty input, null, boundary values, concurrent access?
- **Dependencies**: what does it call? What needs mocking?

### 4. Thinking gate — user describes what to test

Present the research (untested code, conventions, function analysis) and ask:

> "Based on the code I've analyzed, list the behaviors this module should exhibit. For each behavior:
> 1. What input produces what output?
> 2. What error conditions exist? (Look at the error handling in the code)
> 3. Which edge cases matter? (Think: empty, null, boundary, large, concurrent)
> 4. Which behaviors are already tested and which aren't?"

Wait for their answer. Do NOT proceed until they've listed specific behaviors, not just "I'll test the main function."

If their list is shallow: "You listed the happy path, but look at `src/module.ts:45` — there's an error branch when the input is empty. What should happen there?"

### 5. User writes the test plan

The user decides:
- Which behaviors to cover (prioritize untested paths)
- What test data is needed for each case
- Which edge cases to include
- What order to write tests in (start with simplest behavior)

Review their plan:
- If they're skipping error paths: "The function at `src/module.ts:30` has a catch block — what triggers it?"
- If test data is unrealistic: "Look at how callers use this function — they pass X, not Y"
- If they're testing internals: "This is a private helper. Test the public function that calls it instead."

### 6. User implements tests

The user describes what each test should verify. The LLM helps with:
- Syntax and framework-specific patterns (matching conventions from step 2)
- Setting up mocks/fixtures following the repo's existing patterns
- Pointing to similar existing tests as reference

```bash
# Point to an existing test as a template
cat tests/path/to/similar.test.ts
```

**What the LLM DOES**:
- Implement test code the user has described ("I want a test that checks X when Y")
- Match the repo's exact test conventions (naming, structure, assertion style)
- Point to existing tests as reference patterns

**What the LLM DOES NOT DO**:
- Write tests the user hasn't described — the user decides what to test
- Pick test data — the user decides what inputs to use
- Skip behaviors the user didn't mention (but DO point out untested paths)

### 7. Verify

```bash
# Run the new tests
# {repo-specific test command for targeted files}

# Run the full suite — make sure nothing broke
# {repo-specific full test command}

# Check coverage improved (if the repo has coverage tooling)
# {repo-specific coverage command}

# Lint/format
# {repo-specific lint command}
```

Check:
- New tests pass
- Existing tests still pass
- No test pollution (tests don't depend on execution order)
- Coverage actually improved for the target code

### 8. Thinking gate — user explains test design

> "Before submitting — walk me through your tests:
> 1. What behaviors does each test verify? (Not 'tests the function' — what specific behavior?)
> 2. Why did you test these cases and not others?
> 3. If the code under test changes, which of your tests would break? (This checks whether you're testing behavior or implementation)"

This catches mechanical testing — writing tests without understanding what they prove.

## Related Skills

- **Previous step**: ← `oss-prep-to-contribute` — set up the repo and build understanding
- **Next step**: → `oss-submit-pr` — submit the test PR following repo guidelines
- **Alternative entry**: ← `oss-find-real-issues` — if you found untested code while exploring
- **If unfamiliar tech**: → `oss-learn-stack` — learn the test framework from the repo's own tests

## Common Rationalizations

| Shortcut | Why It Fails |
|----------|-------------|
| "I'll just add tests for everything in the file" | Untargeted testing produces brittle tests that break on refactors. Test behaviors, not lines of code. Maintainers reject test PRs that add noise. |
| "I don't need to read existing tests, I know how testing works" | Every repo has conventions. If the repo uses table-driven tests and you write individual assertions, your PR looks like it was written by an outsider. It will require a full rewrite. |
| "I'll test the private helpers directly" | Private functions are implementation details. When the maintainer refactors, your tests break even though the behavior hasn't changed. Test public interfaces. |
| "I'll skip the edge cases, the happy path is enough" | Happy-path-only tests are the tests that already exist. The value of your contribution IS the edge cases. |
| "Coverage went up, so the tests are good" | Coverage measures execution, not verification. A test that calls a function without asserting anything gets coverage credit but proves nothing. |

## Red Flags

- User can't explain what behavior each test verifies — they're writing tests mechanically
- Tests duplicate existing coverage instead of filling gaps
- Test data doesn't match how the code is actually called — tests pass but prove nothing about real usage
- Tests mock everything — they're testing the mocks, not the code
- User wants to test and refactor at the same time — that's two PRs, not one

## Verification Checklist

- [ ] Test conventions match the repo's existing patterns (naming, structure, mocking)
- [ ] Each test verifies a specific behavior (not just "calls the function")
- [ ] Edge cases and error paths are covered (not just happy path)
- [ ] All new tests pass
- [ ] Full test suite still passes (no pollution or breakage)
- [ ] User can explain what each test proves and why they chose these cases (step 8)
- [ ] Coverage improved for the target code (if measurable)

## Anti-patterns

- **DO NOT** generate a wall of tests without the user describing what to test — they decide the test plan
- **DO NOT** test private/internal functions directly — test public behavior
- **DO NOT** ignore the repo's test conventions — match them exactly, no matter your personal preference
- **DO NOT** combine test contributions with code changes — tests-only PRs are cleaner and easier to review
- **DO NOT** use test data that doesn't match real usage — read how callers use the function and mirror that
