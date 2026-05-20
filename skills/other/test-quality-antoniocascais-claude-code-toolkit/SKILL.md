---
name: test-quality
description: >-
  Guides strong, effective unit test generation using proven testing techniques.
  Use when writing unit tests, reviewing test quality, improving existing tests,
  generating test cases, checking test coverage strength, or when tests exist
  but may be weak. Triggers on: unit test, test quality, test coverage, write tests,
  improve tests, review tests, test strength, mutation testing, boundary testing.
---

# Test Quality Guide

Apply these principles when writing or reviewing tests. High line coverage does NOT mean strong tests — tests must verify correctness, not just exercise code paths.

## Principles Checklist

When generating tests, systematically apply each technique:

### 1. Boundary Value Analysis (BVA)
Test at the edges of valid ranges, not the middle.
- Lower bound, upper bound, just past each bound
- For `i < 10`: test 0, 9, 10 (and optionally -1)
- For strings: empty string, single char, max length, max+1

### 2. Equivalence Partitioning
Group inputs into classes that should behave identically. Test one representative per class.
- Valid vs invalid partitions
- Reduces redundant tests while maintaining coverage

### 3. Decision Table Testing
For combinatorial logic (multiple conditions → different outcomes):
- Enumerate all condition combinations
- Especially important for business rules with compound conditions
- AI frequently misses edge combos — be exhaustive

### 4. State Transition Testing
For stateful code (workflows, FSMs, connection pools):
- Test all valid state transitions
- Test INVALID transitions — verify they're rejected
- Test sequences: what happens after multiple transitions?

### 5. Error Path Testing — AI's Biggest Blind Spot
Explicitly test every failure mode:
- Null/undefined/empty inputs
- Malformed data (wrong types, invalid formats)
- Timeouts and network failures
- Permission denied / authorization failures
- Resource exhaustion (full disk, OOM)
- Concurrent access / race conditions
- Empty collections, single-element collections

### 6. Property-Based Testing
Define invariants that must ALWAYS hold, let the framework generate inputs:
- `sort(x)` output is always ordered and same length
- `encode(decode(x)) == x` (roundtrip)
- `f(x) >= 0` for all valid x (domain constraints)

Tools by language:
- Python: `hypothesis`
- JS/TS: `fast-check`
- Java: `jqwik`
- Rust: `proptest`

### 7. Assertion Quality
Every test MUST verify something meaningful:
- BAD: call function, assert no exception → proves nothing
- BAD: assert result is not null → barely proves anything
- GOOD: assert specific return value matches expected
- GOOD: assert side effects occurred (DB write, API call, event emitted)
- GOOD: assert error type AND message for failure cases

### 8. AAA Pattern
Structure every test as: Arrange → Act → Assert
- One logical assertion per test (multiple `assert` calls are fine if testing one behavior)
- Test name describes the behavior being verified

### 9. Test Behavior, Not Implementation
- Test the public contract / API surface
- If mocking 3+ internal methods, the test is too coupled
- Refactors should not break tests unless behavior changes

## Mutation Testing

After writing tests, recommend running mutation testing to validate test strength:
- **JS/TS**: Stryker (`npx stryker run`)
- **Python**: mutmut (`mutmut run`)
- **Java**: PIT (`mvn org.pitest:pitest-maven:mutationCoverage`)
- **Rust**: cargo-mutants (`cargo mutants`)

A mutation score below 60% with high line coverage = weak tests.

## When Writing New Tests

1. Identify the function/module under test
2. List input partitions (valid classes, invalid classes)
3. For each partition, identify boundaries
4. Write happy path tests with specific assertions
5. Write error path tests for every failure mode
6. Consider: are there invariants suitable for property-based tests?
7. Check: would a mutation (flipping `<` to `<=`, removing a line) be caught?

## When Reviewing Existing Tests

Flag these weaknesses:
- Tests that call code without meaningful assertions
- Missing boundary values
- No error/failure path tests
- Over-mocking (testing mocks, not behavior)
- Redundant tests in the same equivalence class

## Test Strength Summary

After generating or reviewing tests, output a brief summary:

```
Test Strength:
- Boundaries: [covered/partial/missing] — list any gaps
- Error paths: [covered/partial/missing] — list untested failures
- Assertion quality: [strong/moderate/weak]
- Property-based candidates: [yes/no] — suggest if applicable
- Mutation resilience: [likely high/moderate/likely low]
```
