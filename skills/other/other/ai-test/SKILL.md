---
name: ai-test
description: "Use when writing tests, enforcing TDD (RED-GREEN-REFACTOR), analyzing coverage gaps, or planning test strategy. Supports Python, TypeScript, .NET, Rust, Go."
effort: high
argument-hint: "plan|run|gap|tdd [target]"
---


# Test

## Purpose

TDD enforcement and testing skill. Tests are executable specifications -- they define what the system does before the system does it. Maximum confidence per minute of developer time.

## When to Use

- `tdd`: driving new features test-first (RED-GREEN-REFACTOR)
- `run`: writing and executing tests for existing code
- `gap`: analyzing coverage gaps and missing edge cases
- `plan`: designing test strategy before writing tests

## Process

### Mode: tdd (RED-GREEN-REFACTOR)

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**Phase RED -- Write Failing Test**

1. Write ONE test showing what SHOULD happen
2. Name: `test_<unit>_<scenario>_<expected_outcome>`
3. AAA pattern: Arrange, Act, Assert (visually separated)
4. Run test -- confirm FAIL for the expected reason (missing feature, not syntax error)
5. Produce Implementation Contract:

```markdown
## Implementation Contract
- Test files: [exact paths]
- Verification: [exact command]
- Failure reason: [why it fails -- tied to missing behavior]
- Constraint: DO NOT modify these test files during GREEN
```

6. STOP. Do not implement.

**Phase GREEN -- Minimal Code**

1. Read the Implementation Contract
2. DO NOT modify test files (they are immutable)
3. Write the simplest code to make the test pass (YAGNI)
4. Run test -- confirm PASS
5. Run ALL tests -- confirm no regressions

If the test still fails: fix your code, not the test.

**Phase REFACTOR -- Clean Up (after GREEN only)**

- Remove duplication, improve names, extract helpers
- Tests MUST stay green throughout
- Do NOT add behavior during refactor

### Mode: run

1. Detect test framework from project files
2. Follow existing conventions (directory structure, naming, fixtures)
3. Write tests using AAA pattern with descriptive names
4. Run with stack-appropriate command
5. Report results: pass/fail count, coverage delta

### Mode: gap

1. Run coverage tool with branch coverage enabled
2. Identify untested critical paths (business logic > glue code)
3. Check for missing edge cases: null, empty, boundary, error paths
4. Produce gap report with prioritized recommendations

### Mode: plan

1. Map the testing surface (modules, public APIs, critical paths)
2. Assign test categories: unit, integration, e2e
3. Define coverage targets per module
4. Identify infrastructure needs (test containers, fixtures, fakes)

## Stack Commands

| Stack | Runner | Coverage | Async |
|-------|--------|----------|-------|
| Python | `uv run pytest` | `pytest-cov` (branch=true) | `asyncio_mode = "auto"` |
| TypeScript | `vitest` or `jest` | `c8` / `istanbul` | `async/await` |
| .NET | `dotnet test` + xUnit | `coverlet` | `async Task` |
| Rust | `cargo test` | `cargo tarpaulin` | `#[tokio::test]` |
| Go | `go test ./...` | `go test -cover` | goroutine tests |

## Testing Rules

**Fakes over mocks**. Mocks test implementation details. Fakes implement the same interface.

Mocks are acceptable ONLY for:
1. Verifying something was NOT called
2. Simulating transient errors for retry logic
3. Third-party libraries (but wrap in your own adapter first)

**AAA pattern** (non-negotiable):

```python
# Arrange -- set up inputs and dependencies
# Act -- call the function under test
# Assert -- verify the outcome
```

**Name pattern**: `test_<unit>_<scenario>_<expected_outcome>`
- Good: `test_parse_email_rejects_missing_at_symbol`
- Bad: `test_parse_email`, `test_1`, `test_it_works`

## Anti-Patterns (Reject These)

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Testing the mock | Proves the mock works, not the code |
| No-op test (assert True) | Tests nothing, inflates coverage |
| Testing implementation | Breaks on refactor, proves nothing about behavior |
| Huge test setup | Design is too coupled -- simplify the interface |
| sleep() for sync | Flaky -- use events, barriers, wait_for |
| Exact float comparison | Flaky -- use approx/closeTo |

## Iron Law

If tests are wrong, escalate to the user. NEVER weaken, skip, or modify tests to make implementation easier. "Tests are wrong" means the requirement changed -- not that passing them is hard.

## Common Mistakes

- Writing tests after implementation (tests-after prove what IS, not what SHOULD be)
- Testing private methods (test the public API)
- 100% coverage with meaningless assertions
- Skipping edge cases (null, empty, boundary, concurrent access)
- Not running ALL tests after changes

## Integration

- **Called by**: `/ai-dispatch` (build tasks), `ai-build agent` (TDD mode), user directly
- **Calls**: stack-specific test runners
- **Transitions to**: `ai-build` (GREEN phase), `/ai-verify` (coverage validation)

$ARGUMENTS
