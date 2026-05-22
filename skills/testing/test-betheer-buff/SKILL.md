---
name: buff-test
description: This skill should be used when the user asks to "write tests", "generate tests", "add tests", "test this feature", "run /buff:test", "create unit tests", "create integration tests", "check test coverage", "show coverage", "find untested code", "test changed files", "--coverage", "--gaps", "--changed", "coverage tracking", "change-aware", or any request involving test creation or testing workflows.
version: 0.2.0
argument-hint: "[--run] [--coverage] [--gaps] [--changed] [file or feature]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# buff-test v2

Coverage-aware smart testing with change-aware selection and context-informed generation. Uses the project dependency graph to track what's tested, what's not, and what needs retesting when code changes — then generates tests informed by real caller data, past corrections, and known edge cases.

## Framework detection

Detect in this order (stop at first match):

| File | Framework |
|---|---|
| `vitest.config.*` | Vitest |
| `jest.config.*` | Jest |
| `pytest.ini` / `pyproject.toml` with `[tool.pytest]` | pytest |
| `Cargo.toml` with `[dev-dependencies]` test crates | Rust built-in |
| `*_test.go` files present | Go built-in |
| `bun.lockb` and no config | Default to Vitest |
| `package.json` only | Default to Vitest |
| `requirements.txt` only | Default to pytest |

After detection, write to `.buff/memory/context.json`:
```json
{ "test_framework": "vitest" }
```

On subsequent runs, read from context.json and skip detection.

## Coverage tracking via graph

Uses `.buff/memory/graph.json` for a live coverage map — no external coverage tools required.

**Function-level coverage check:**

1. Read the target file's entry in `graph.json` to get its `exports` list
2. If a `test_file` is mapped, Grep the test file for references to each exported symbol
3. Mark each export as tested (referenced in test file) or untested (not referenced)
4. Update the file's `coverage` field in `graph.json`:

```json
{
  "coverage": {
    "functions": 3,
    "tested": 2,
    "untested": ["createSession"]
  }
}
```

This runs automatically after test generation and can be triggered manually with `--coverage`.

## Scope handling

| Invocation | Scope |
|---|---|
| `/buff:test` | Test the last modified file |
| `/buff:test src/auth.ts` | Test the specified file |
| `/buff:test --coverage` | Show project coverage map |
| `/buff:test --gaps` | Untested exports ranked by risk |
| `/buff:test --changed` | Test only changed files + dependents |
| `/buff:test --run` | Generate and immediately run |

## `--coverage` output

Read `.buff/memory/graph.json` — for each file entry, extract only `exports`, `coverage`, and `imported_by` count (skip `imports_from`, `lines`, `last_modified` to save tokens). Compute coverage from the `coverage` field. Display:

```
## Test Coverage — project-wide

| File | Exports | Tested | Gap | Risk |
|---|---|---|---|---|
| src/auth.ts | 3 | 2 (67%) | createSession | HIGH — 3 dependents |
| src/db.ts | 4 | 1 (25%) | connect, query, close | HIGH — foundation |
| src/utils.ts | 8 | 6 (75%) | formatDate, retry | LOW — leaf |

Overall: 20/28 exports tested (71%)
Critical gaps: 2 files below 50% with dependents
```

Risk is determined by `imported_by` count in `graph.json`:
- **HIGH** — 3+ dependents, or 0 dependents but is imported by HIGH-risk files (foundation module)
- **MEDIUM** — 1-2 dependents
- **LOW** — 0 dependents (leaf module)

Files with no `imported_by` entries and no dependents are leaf modules. Files imported by many others are foundation modules — untested foundation code is always HIGH risk.

## `--gaps` risk ranking

Read `graph.json` — extract only `exports`, `coverage.untested`, and `imported_by` count per file. Collect all untested exports across the project. Rank by risk — number of dependents from the `imported_by` field determines priority.

**Risk formula:** Untested export in a foundation module (many dependents) > untested export in a mid-tier module > untested export in a leaf utility.

Output a ranked list with risk justification:

```
## Untested Exports — ranked by risk

1. src/db.ts → connect, query, close
   Risk: CRITICAL — foundation module, 6 dependents, 25% coverage
   Dependents: auth.ts, users.ts, posts.ts, comments.ts, admin.ts, migrations.ts

2. src/auth.ts → createSession
   Risk: HIGH — 3 dependents, 67% coverage
   Dependents: router.ts, middleware.ts, admin.ts

3. src/utils.ts → formatDate, retry
   Risk: LOW — leaf module, 0 dependents, 75% coverage

Action: Run `/buff:test src/db.ts` to address the highest-risk gap.
```

## `--changed` workflow

Change-aware test selection — run only what's affected by recent changes.

**Steps:**

1. Run `git diff --name-only` to get changed files (staged + unstaged)
2. For each changed file, look up its `test_file` from `graph.json`
3. For each changed file, look up its `imported_by` from `graph.json` to find dependents
4. For each dependent, look up its `test_file` from `graph.json`
5. Deduplicate the test file list
6. Run only the affected test files

**Example output:**

```
Changed: src/auth.ts
  Direct test: src/auth.test.ts
  Dependents: src/router.ts, src/middleware.ts
  Dependent tests: src/router.test.ts, src/middleware.test.ts

Running 3 test files (skipping 8 unchanged)
```

If a changed file has no `test_file` mapping in `graph.json`, flag it:
```
⚠ src/newfile.ts has no test file. Run `/buff:test src/newfile.ts` to generate one.
```

## Counterfeit context loading

Before generating any tests, load context from counterfeit memory to inform generation:

1. **`.buff/memory/graph.json`** — read the target file's entry: what calls this function (`imported_by`), what it depends on (`imports_from`), existing coverage gaps (`coverage.untested`)
2. **`~/.buff/memory/corrections.json`** — check for past test-related corrections (entries where `skill: "test"`). Apply these to avoid repeating mistakes.
3. **`.buff/memory/learnings.json`** — check for project-specific test learnings (edge cases, patterns that apply to this code type)
4. **`~/.buff/memory/patterns.json`** — check for error handling patterns (`error_handling: "result-pattern"` → assert on Result types) and test conventions (e.g., no mocks for DB)
5. **Caller files** — for each file in `imported_by`, Grep for import lines referencing the target module and the call sites using the exported symbols. Extract only the import lines and call-site lines — do NOT read full caller files. This reveals real-world usage patterns.

## Smarter test generation

Context from counterfeit changes what tests get generated:

- **Caller-informed inputs**: Testing `validateToken()`? Graph shows it's called from `middleware.ts` with `req.headers.authorization`. Generate tests using real header formats (`Bearer xyz`, missing header, malformed token) instead of generic placeholder strings.

- **Correction-aware approach**: `corrections.json` has an entry saying "no mocks for repository tests"? Generate integration tests with real database calls instead of mocked ones.

- **Pattern-aware assertions**: `patterns.json` shows `error_handling: "result-pattern"`? Generate tests that assert on `Result` types (`isOk()`, `isErr()`) instead of try/catch.

- **Learning-informed edge cases**: `learnings.json` says "middleware order matters — auth before rate limiter"? Include ordering tests when generating middleware test suites.

If no counterfeit context exists (new project, empty memory), fall back to standard test generation — analyze the source file directly without caller context.

## Test generation workflow

1. **Counterfeit context load** — read graph.json, corrections.json, learnings.json for the target file
2. **Read target file** — understand exports, functions, classes, error paths
3. **Check graph for callers** — Grep caller files (from `imported_by`) for import lines and call sites to understand how these functions are actually used
4. **Generate tests with context** — use real usage patterns from callers, known edge cases from learnings, and correction-informed approach
5. **Place test file** following project conventions:
   - If `__tests__/` dir exists → place there
   - If `*.test.ts` pattern exists → colocate with source
   - If `tests/` dir exists → place there
   - Default: colocate as `<filename>.test.<ext>`
6. **Offer to run** (or auto-run with `--run`)

Print: "Generated N tests in [filename]. Run now? [Y/n]"

Wait for user confirmation before running. Exception: if invoked with `--run` flag, execute immediately.

## What makes a good buff test

**Test behavior, not implementation:**
```typescript
// Good — tests what the function does
it('returns 401 when token is expired', async () => {
  const res = await handler(expiredTokenRequest)
  expect(res.status).toBe(401)
})

// Bad — tests implementation detail
it('calls validateToken function', () => {
  expect(validateToken).toHaveBeenCalled()
})
```

**One assertion per test (usually):**
- Tests with 5+ assertions are testing multiple things — split them
- Exception: related data shape assertions can group (checking multiple fields of one object)

**Descriptive names:**
- Format: `[unit] [action/condition] [expected result]`
- Example: `parseDate with invalid string throws ParseError`
- Example: `createUser when email exists returns conflict error`

**No test interdependence:**
- Each test runs in isolation
- No shared mutable state between tests
- Use `beforeEach` to reset state, not shared variables

## Output format

```typescript
// Vitest / Jest example
import { describe, it, expect, beforeEach } from 'vitest'
import { [exports] } from './[source-file]'

describe('[unit under test]', () => {
  beforeEach(() => {
    // reset state
  })

  it('[action] [condition] [expected]', () => {
    // arrange
    // act
    // assert
  })
})
```

```python
# pytest example
import pytest
from [module] import [exports]

class Test[Unit]:
    def test_[action]_[condition]_[expected](self):
        # arrange
        # act
        # assert
```

## Running tests

If user confirms (or `--run` flag is set):

```bash
# Vitest
bunx vitest run [test-file]

# Jest
npx jest [test-file]

# pytest
python -m pytest [test-file] -v

# Rust
cargo test [test-name]

# Go
go test ./... -run [TestName]
```

Report results inline:
```
Tests: 12 passed · 0 failed · 2 skipped
Coverage: [if available]
```

If tests fail, diagnose immediately — do not just show the error. Identify whether the test is wrong or the implementation is wrong.

## Writes to counterfeit

After test generation and execution, update counterfeit memory:

- **Coverage data → `.buff/memory/graph.json`**: Set `test_file` mapping for the target file. Update `coverage` field with function count, tested count, and untested list.
- **Test results → `.buff/memory/learnings.json`**: If tests revealed edge cases or unexpected behavior, record as a learning. Example: `{"learning": "validateToken silently returns null on empty string", "source": "test discovery", "applies_to": "src/auth.ts"}`.
- **Test patterns → `~/.buff/memory/patterns.json`**: If the test approach used a pattern not yet recorded (e.g., integration tests for repositories), update the `architecture` array with the pattern.

## Graph update (post-skill)

After generating tests, update `graph.json` for the tested file:

1. Set `test_file` to the path of the generated test file
2. Grep the test file for references to each export in the source file
3. Update `coverage.functions` to the total number of exports
4. Update `coverage.tested` to the count of exports referenced in the test file
5. Update `coverage.untested` to the list of exports NOT referenced in the test file
6. Update `updated_at` timestamp

## Correction detection

Watch for the user correcting test output (rejection, replacement, redirect, style correction). Follow the correction capture mechanism defined in `counterfeit` SKILL.md — detect signals, record to `learnings.json` + `corrections.json`, promote to `patterns.json` at 2+ occurrences. Use `skill: "test"` when writing correction entries.

## Forge mode

In `/buff:auto` (forge), run tests automatically after code generation without asking. Report pass/fail inline and continue the loop. If tests fail in forge mode, fix them before proceeding to validation.

In forge mode, use `--changed` logic for minimum test set: only run tests affected by the files changed in the current forge cycle, rather than the full test suite. This keeps forge loops fast on large projects.
