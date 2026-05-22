---
name: test-dedup
description: Review test suites for duplicate, redundant, or low-value tests — especially unit tests already subsumed by property-based tests. Remove noise, keep signal.
---

# Test Deduplicator

Audit test modules to eliminate duplicate and redundant tests, favoring property-based tests over hand-rolled unit tests when coverage overlaps.

## When to Use

- After adding property-based tests to a module that already has unit tests
- During periodic test hygiene passes
- When a test file feels bloated or tests are hard to distinguish
- Before reviewing a PR that touches test code
- When you suspect unit tests are just "examples of" a property test

## Philosophy

Every test must earn its place. A test exists to:

1. **Document a specific behavior** — a reader should know exactly what contract is being verified
2. **Catch a specific class of regression** — if it can't fail independently, it's dead weight
3. **Cover territory no other test covers** — overlap is waste

**Default to property-based tests.** A single `proptest!` that verifies an invariant over thousands of inputs is strictly more valuable than five hand-picked unit tests checking the same invariant at specific points. The unit tests are subsumed.

**Keep unit tests only when they add unique value:**
- Regression test for a specific, previously-reported bug (with a comment citing the bug)
- Edge case that property generators are unlikely to produce (empty input, MAX values, zero-length)
- Complex setup that would be awkward to express as a property generator
- Readability anchor — one simple example that documents the API's intended usage

## Analysis Process

### Step 1: Inventory the Test Module

For each file or module under review:

1. List every `#[test]` function with a one-line summary of what it checks
2. List every `proptest!` block with the properties it asserts
3. List every `#[kani::proof]` with what it verifies
4. List every simulation harness corpus case that covers this code

### Step 2: Build a Coverage Matrix

Map each test to the **behavior** it exercises:

| Behavior / Invariant | Unit Tests | Property Tests | Kani Proofs | Sim Coverage |
|---|---|---|---|---|
| Roundtrip encode/decode | `test_encode_basic`, `test_encode_empty` | `prop_roundtrip` | — | — |
| Bounds never exceeded | `test_within_bounds` | `prop_bounds_hold` | `verify_bounds` | — |
| Monotonic ordering | `test_sorted_output` | — | — | scanner_sim |

### Step 3: Identify Redundancy

A unit test is **redundant** if ALL of the following are true:

1. A property test exists that covers the same invariant over a broader input domain
2. The unit test's specific input is within the property test's generator range
3. The unit test does not document a specific historical bug
4. The unit test does not serve as a readable usage example that the property test lacks

A unit test is **NOT redundant** if ANY of the following are true:

- It tests a boundary/edge case that the property generator explicitly excludes
- It is a regression test with a bug reference (e.g., `// Regression: GH-123`)
- It is the only test demonstrating basic API usage for a public function
- It tests error paths or panic conditions distinct from the property's happy-path focus
- The property test is gated behind a feature flag (`stdx-proptest`) and the unit test provides baseline ungated coverage

### Step 4: Classify Each Test

For every test, assign one label:

- **KEEP** — Unique value, no overlap, clear purpose
- **KEEP (anchor)** — Redundant coverage but serves as the readable usage example
- **SUBSUME** — Fully covered by a property/Kani/sim test; remove it
- **MERGE** — Multiple unit tests checking variations of the same thing; consolidate into one property test
- **UPGRADE** — Unit test covering an invariant that should be a property test; rewrite it
- **UNCLEAR** — Test name/body doesn't clearly state what behavior it verifies; needs renaming or a doc comment before deciding

### Step 5: Act

For each **SUBSUME** test:
- Verify the subsuming property test truly covers the same input space
- Delete the unit test
- If it was the only readable example, promote one property test case or add a doc-test

For each **MERGE** group:
- Write one `proptest!` that generalizes all merged tests
- Delete the individual unit tests
- If the merged tests had distinct edge cases, ensure the property generator covers them or add `prop_assume!` guards

For each **UPGRADE** test:
- Rewrite as a `proptest!` with appropriate generators
- Gate under `#[cfg(all(test, feature = "stdx-proptest"))]`
- Delete the original unit test

## Project-Specific Conventions

### Test locations in this codebase
- Inline tests: `#[cfg(test)] mod tests { ... }` at bottom of source file
- Separate test files: `src/stdx/*_tests.rs`, `src/engine/tests.rs`
- Property tests: often in the same file, gated with `#[cfg(all(test, feature = "stdx-proptest"))]`
- Kani proofs: `#[cfg(kani)] mod kani_proofs { ... }` or in `*_tests.rs`
- Simulation tests: `tests/simulation/` directory

### Feature gates
- Property tests: `stdx-proptest` feature
- Kani proofs: `kani` feature
- Simulation harnesses: `sim-harness`, `scheduler-sim`

### What counts as "public API" in this project
- Functions/types exported from `src/lib.rs`
- The `Engine` trait and its implementations
- `RuleSpec`, `RuleCompiled`, scanning pipeline entry points
- Anything used cross-module (even if `pub(crate)`)

## Output Format

```markdown
## Test Dedup Report: [module/file]

### Inventory

| # | Test | Type | Behavior Tested |
|---|------|------|-----------------|
| 1 | `test_foo_basic` | unit | Foo returns correct value for simple input |
| 2 | `test_foo_empty` | unit | Foo handles empty input |
| 3 | `prop_foo_roundtrip` | property | Foo roundtrips for all valid inputs |
| 4 | `verify_foo_bounds` | kani | Foo never exceeds buffer bounds |

### Coverage Matrix

| Behavior | Tests Covering It | Redundancy |
|---|---|---|
| Basic correctness | #1, #3 | #1 subsumed by #3 |
| Empty input | #2, #3 | #2 subsumed IF generator includes empty |
| Bounds safety | #4 | unique (Kani proof) |

### Verdicts

| Test | Verdict | Reason |
|------|---------|--------|
| `test_foo_basic` | SUBSUME | `prop_foo_roundtrip` covers all valid inputs including simple ones |
| `test_foo_empty` | KEEP (anchor) | Only readable example of empty-input behavior; property generator may skip empty |
| `prop_foo_roundtrip` | KEEP | Covers the broadest input space |
| `verify_foo_bounds` | KEEP | Unique formal verification value |

### Actions

1. **Delete** `test_foo_basic` — subsumed by `prop_foo_roundtrip`
2. **Keep** `test_foo_empty` — add comment: `// Anchor: documents empty-input edge case`
3. No changes to property/Kani tests

### Net Result

- Tests before: 4
- Tests after: 3
- Removed: 1 (25% reduction)
- Coverage impact: None (all removed tests fully subsumed)
```

## Judgment Calls

Use your best judgment on borderline cases. Some guidelines:

- **When in doubt, keep.** It's better to have a slightly redundant test than to lose coverage.
- **A test that catches a different failure mode is not redundant** even if it tests the same function. A unit test that checks an error message string and a property test that checks the Result variant are testing different things.
- **Don't remove the last ungated test.** If all property tests are behind `stdx-proptest`, keep at least one basic unit test ungated so `cargo test` (no features) still exercises the code.
- **Simulation coverage counts.** If a Scanner Sim corpus case exercises the exact code path, that's real coverage — it can subsume unit tests just like property tests can.
- **Prefer fewer, stronger tests** over many weak ones. Five tests each asserting one field of a struct can become one test asserting the whole struct, or one property test.

## Related Skills

- `/test-strategy` — Decide what kind of test to write for new code
- `/security-reviewer` — Audit unsafe code (may affect test removal decisions)
