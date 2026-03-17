---
name: test-consolidate
description: Consolidate verbose test suites by replacing repetitive unit tests with property-based tests, parameterized tests (rstest), or fuzz tests. Less code to maintain, same or better coverage.
---

# Test Consolidator

Analyze test modules for opportunities to replace many similar unit tests with
a single, more powerful testing construct — property-based tests, parameterized
tests, or fuzz tests. The goal is comprehensive coverage with minimal code to
maintain, review, and keep updated.

## When to Use

- A test module has 5+ unit tests for the same function with different inputs
- Tests follow a pattern: call function with input X, assert output Y
- You notice copy-paste test bodies differing only in values
- Before a PR when test files are growing faster than source files
- After refactoring: old tests may cluster around the same behavior
- During periodic test hygiene alongside `test-dedup`

## Philosophy

**Tests should scale with behaviors, not with inputs.**

If a function has 20 valid inputs worth testing, the answer is NOT 20 test
functions. The answer is one construct that covers all 20 — and ideally the
infinite space between them.

The hierarchy of consolidation (prefer higher):

1. **Property-based test (proptest)** — When you can state an invariant that
   holds for ALL valid inputs. One `proptest!` replaces unbounded unit tests.
   Maximum coverage, minimum code.

2. **Parameterized test (rstest)** — When you have a finite, important set of
   (input, expected) pairs and no general invariant. One `#[rstest]` with a
   `#[case]` list replaces N identical test bodies.

3. **Table-driven test** — When the inputs and outputs fit a simple table.
   A `for` loop over a `Vec<(Input, Expected)>` inside a single `#[test]`.
   Simpler than rstest if there's no need for individual test names.

4. **Fuzz test** — When exploring adversarial or untrusted input spaces. One
   fuzz target can subsume hundreds of hand-crafted "weird input" tests.

5. **Individual unit tests** — The last resort. Only when each test truly
   exercises unique setup, distinct error paths, or documents a specific bug.

**Never consolidate for the sake of shorter code.** The goal is less code to
*maintain* — meaning fewer places to update when the function signature changes,
fewer tests to rename when behavior evolves, and fewer copy-paste errors.

## Analysis Process

### Step 1: Identify Test Clusters

A **test cluster** is a group of tests that:
- Test the same function or method
- Have the same structure (setup → call → assert)
- Differ primarily in input values and expected outputs
- May also differ in minor setup variations

Scan the module and group tests into clusters. A single test can belong to
multiple clusters if it tests more than one function.

```
Cluster: parse_duration()
  - test_parse_seconds          → parse_duration("5s")  == Duration::from_secs(5)
  - test_parse_minutes          → parse_duration("3m")  == Duration::from_secs(180)
  - test_parse_hours            → parse_duration("2h")  == Duration::from_secs(7200)
  - test_parse_zero             → parse_duration("0s")  == Duration::ZERO
  - test_parse_large            → parse_duration("999h") == Duration::from_secs(3596400)
  - test_parse_invalid_unit     → parse_duration("5x")  == Err(...)
  - test_parse_empty            → parse_duration("")     == Err(...)
  - test_parse_negative         → parse_duration("-1s")  == Err(...)
```

### Step 2: Classify Each Cluster

For each cluster, determine the best consolidation strategy:

**Can you state a universal property?**
→ Property-based test. Examples:
  - "parse then format roundtrips for all valid inputs"
  - "output length is always ≤ input length"
  - "sorted output is a permutation of input"
  - "encoding never produces invalid UTF-8"

**Is it a finite set of (input, expected) with no general property?**
→ Parameterized test (rstest) or table-driven test. Examples:
  - Known error codes mapping to messages
  - Specific file extensions mapping to MIME types
  - Configuration keys mapping to defaults

**Are the tests exploring adversarial/edge inputs?**
→ Fuzz test. Examples:
  - "doesn't panic on any byte sequence"
  - "doesn't allocate more than 10x input size"

**Does each test have genuinely unique setup or assertions?**
→ Keep as individual tests. Don't force consolidation.

### Step 3: Evaluate Consolidation Candidates

For each cluster, answer:

| Question | If Yes | If No |
|----------|--------|-------|
| Can I state one invariant covering all cases? | proptest | Next question |
| Are all test bodies structurally identical? | rstest or table-driven | Partial consolidation |
| Do >3 tests share the same assertion pattern? | At minimum table-driven | Probably keep individual |
| Would adding a new case require a new function? | Consolidate (adding cases should be trivial) | Fine as-is |
| Do tests differ only in values, not in logic? | Strong consolidation candidate | Keep separate |

### Step 4: Choose the Right Tool

#### Property-Based (proptest) — Best for invariants

Use when: The assertion is about a *property* that holds regardless of input.

```rust
// BEFORE: 6 unit tests
#[test] fn encode_ascii()    { assert_eq!(encode("hello"), "aGVsbG8="); }
#[test] fn encode_empty()    { assert_eq!(encode(""), ""); }
#[test] fn encode_unicode()  { assert_eq!(encode("café"), "Y2Fmw6k="); }
#[test] fn decode_ascii()    { assert_eq!(decode("aGVsbG8="), "hello"); }
#[test] fn decode_empty()    { assert_eq!(decode(""), ""); }
#[test] fn decode_unicode()  { assert_eq!(decode("Y2Fmw6k="), "café"); }

// AFTER: 1 property test (covers infinite inputs)
proptest! {
    #[test]
    fn roundtrip(input in "\\PC*") {
        let encoded = encode(&input);
        let decoded = decode(&encoded).unwrap();
        prop_assert_eq!(input, decoded);
    }
}
// KEEP: encode_empty as anchor (documents empty-input behavior)
```

#### Parameterized (rstest) — Best for case tables

Use when: You have specific (input, expected) pairs with no general property.

```rust
// BEFORE: 7 unit tests
#[test] fn status_200() { assert_eq!(status_text(200), "OK"); }
#[test] fn status_201() { assert_eq!(status_text(201), "Created"); }
#[test] fn status_400() { assert_eq!(status_text(400), "Bad Request"); }
#[test] fn status_404() { assert_eq!(status_text(404), "Not Found"); }
#[test] fn status_500() { assert_eq!(status_text(500), "Internal Server Error"); }
#[test] fn status_unknown() { assert_eq!(status_text(999), "Unknown"); }
#[test] fn status_zero() { assert_eq!(status_text(0), "Unknown"); }

// AFTER: 1 parameterized test
#[rstest]
#[case(200, "OK")]
#[case(201, "Created")]
#[case(400, "Bad Request")]
#[case(404, "Not Found")]
#[case(500, "Internal Server Error")]
#[case(999, "Unknown")]
#[case(0, "Unknown")]
fn status_text_mapping(#[case] code: u16, #[case] expected: &str) {
    assert_eq!(status_text(code), expected);
}
```

#### Table-Driven — Best for simple mappings without rstest

Use when: Cases are simple, no need for individual test names in output.

```rust
// AFTER: 1 table-driven test
#[test]
fn status_text_cases() {
    let cases = [
        (200, "OK"),
        (201, "Created"),
        (400, "Bad Request"),
        (404, "Not Found"),
        (500, "Internal Server Error"),
        (999, "Unknown"),
        (0, "Unknown"),
    ];
    for (code, expected) in cases {
        assert_eq!(status_text(code), expected, "code={code}");
    }
}
```

#### Fuzz Test — Best for adversarial input exploration

Use when: Tests are exploring "weird inputs" to find crashes.

```rust
// BEFORE: 12 unit tests trying to crash the parser
#[test] fn parse_null_bytes()   { let _ = parse(b"\x00\x00"); }
#[test] fn parse_huge_input()   { let _ = parse(&vec![0xFF; 10_000]); }
#[test] fn parse_truncated()    { let _ = parse(b"\x01\x02"); }
// ... 9 more ...

// AFTER: 1 fuzz target (explores billions of inputs)
fuzz_target!(|data: &[u8]| {
    let _ = parse(data);
});
// KEEP: 1-2 specific regression tests if they document known bugs
```

### Step 5: Check for Blockers

Before recommending consolidation, verify:

- [ ] **Feature gates**: proptest requires `stdx-proptest`. If all tests move
  behind a feature gate, keep at least one ungated unit test as baseline.
- [ ] **Regression tests**: Tests with bug references (`// Regression: GH-123`)
  should stay as individual tests even if technically consolidatable.
- [ ] **Error path tests**: Tests verifying specific error messages or error
  variants may need individual tests if the exact error matters.
- [ ] **Readability anchors**: Keep one simple example test per public function
  as documentation, even if a property test covers it.
- [ ] **rstest availability**: This project does not currently use rstest.
  If recommending it, note that `rstest = "0.23"` needs to be added to
  `[dev-dependencies]` in Cargo.toml.

### Step 6: Produce Consolidation Plan

For each cluster, specify:

1. **Current state**: Number of tests, lines of test code
2. **Recommended strategy**: Which tool and why
3. **What gets removed**: Which specific tests are replaced
4. **What gets kept**: Which tests survive and why
5. **New test code**: The actual replacement test(s)
6. **Net effect**: Lines removed vs added, maintenance burden change

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

### Dependencies to add if recommending new tools
- **rstest**: Add `rstest = "0.23"` to `[dev-dependencies]` in Cargo.toml
- **proptest**: Already available behind `stdx-proptest` feature
- **cargo-fuzz**: External tool, no Cargo.toml change needed

## Output Format

```markdown
## Test Consolidation Report: [module/file]

### Cluster Analysis

#### Cluster 1: `function_name()` — N tests, M lines

**Tests in cluster:**
| # | Test | Input | Assertion |
|---|------|-------|-----------|
| 1 | `test_foo_basic` | "hello" | returns "HELLO" |
| 2 | `test_foo_empty` | "" | returns "" |
| 3 | `test_foo_unicode` | "café" | returns "CAFÉ" |
| ... | ... | ... | ... |

**Pattern detected:** All tests call `foo(input)` and assert exact output.
Inputs vary, assertion structure is identical.

**Recommended strategy:** Property-based test
**Rationale:** The invariant `foo(x).to_lowercase() == x.to_lowercase()` holds
for all inputs. A single proptest replaces all 8 unit tests.

**Consolidation:**
- REPLACE tests #1-#6 with proptest `prop_foo_case_invariant`
- KEEP `test_foo_empty` as anchor (documents empty-input behavior)
- KEEP `test_foo_regression_gh_42` (regression test, bug reference)

**Proposed code:**
```rust
proptest! {
    #[test]
    fn prop_foo_case_invariant(input in "\\PC{0,100}") {
        prop_assert_eq!(foo(&input).to_lowercase(), input.to_lowercase());
    }
}
```

#### Cluster 2: `bar()` — N tests, M lines

...

### Summary

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total tests | 34 | 12 | -22 (65%) |
| Test lines | 280 | 95 | -185 (66%) |
| Behaviors covered | 8 | 8 | No change |
| Input space covered | ~34 points | Continuous | Vastly improved |

### Dependency Changes

- [ ] Add `rstest = "0.23"` to `[dev-dependencies]` (if rstest recommended)
- [ ] No new dependencies needed (if only proptest/fuzz)

### Migration Order

1. Add proptest for Cluster 1 (highest value: 8 tests → 1)
2. Add rstest for Cluster 3 (6 tests → 1 parameterized)
3. Rewrite Cluster 5 as table-driven (4 tests → 1)
4. Run full test suite to verify no coverage loss
5. Delete subsumed unit tests
```

## Decision Heuristics

### When to prefer proptest over rstest
- You can state a property about the output without knowing the exact value
- The input space is continuous or very large
- Roundtrip properties exist (encode/decode, serialize/deserialize)
- Order/sorting/containment invariants exist

### When to prefer rstest over proptest
- Each case has a specific expected output that must be exact
- The set of important cases is finite and known
- The mapping is arbitrary (no mathematical relationship)
- You want each case to appear as a named sub-test in output

### When to prefer table-driven over rstest
- Cases are simple value pairs
- You don't need individual test names in CI output
- You want to avoid adding a dependency
- The table fits in <20 lines

### When to prefer fuzz over all else
- The function processes untrusted/external input
- The goal is "never panic" rather than "correct output"
- You've been writing tests that try to "trick" the parser

### When NOT to consolidate
- Each test has genuinely different setup logic (not just different values)
- Tests verify different error paths with different error types
- Tests are regression tests for specific bugs (keep the history)
- The "consolidated" version would be harder to understand than the originals
- There are only 2-3 tests — consolidation overhead isn't worth it

## Judgment Calls

- **Threshold**: Don't consolidate clusters of fewer than 4 tests unless the
  consolidation is obviously cleaner (e.g., perfect roundtrip property).
- **Mixed clusters**: If 6 of 8 tests consolidate but 2 are genuinely unique,
  consolidate the 6 and keep the 2. Don't force everything into one construct.
- **Error tests**: Tests for error cases often belong in a separate rstest or
  table, not mixed into the happy-path property test. Group by success/failure.
- **Naming**: Consolidated tests should have clear names describing the
  invariant or case set, not generic names like `test_all_cases`.

## Related Skills

- `test-dedup` — Remove tests subsumed by higher-level tests (complementary)
- `test-strategy` — Decide what kind of test to write for new code
