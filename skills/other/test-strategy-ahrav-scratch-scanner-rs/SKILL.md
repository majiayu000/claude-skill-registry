---
name: test-strategy
description: Assess and recommend the appropriate testing strategy for Rust code - unit tests, property-based tests, fuzz tests, Kani model checking, or simulation testing
---

# Test Strategy Assessment

Analyze code and recommend the optimal testing approach from this project's testing toolkit.

## Testing Toolkit Available

| Type | Tool | Feature Flag | Best For |
|------|------|--------------|----------|
| **Unit Tests** | `#[test]` | None | Specific behavior, edge cases, regression tests |
| **Property Tests** | proptest | `stdx-proptest` | Invariants over input domains, mathematical properties |
| **Fuzz Tests** | cargo-fuzz | External | Security-critical parsing, untrusted input handling |
| **Model Checking** | Kani | `kani` | Memory safety proofs, absence of panics, formal verification |
| **Simulation Tests** | Project harnesses | See below | System-level invariants, scheduling, chunking, archive expansion |

### Simulation Harnesses

This project has five purpose-built deterministic simulation harnesses. **Always consider whether new or changed code should be covered by one of these.**

| Harness | Location | Feature | Scope | When to Add Cases |
|---------|----------|---------|-------|-------------------|
| **Scanner Sim** | `src/sim_scanner/` | `sim-harness` | End-to-end chunked scanning, overlap dedup, fault injection, ground-truth oracle | Any change to scanning pipeline, chunking logic, finding dedup, or file discovery |
| **Scheduler Sim** | `src/scheduler/sim.rs` | `scheduler-sim` | Work-stealing scheduler invariants, buffer pool, I/O depth, budget enforcement | Any change to scheduling, buffer management, permit accounting, or budget caps |
| **Archive Sim** | `src/sim_archive/` | `sim-harness` | Deterministic archive building (zip/tar/gzip), entry locators, path canonicalization | Any change to archive format support, entry path handling, or extraction logic |
| **Git Scan Sim** | `src/sim_git_scan/` | `sim-harness` | Commit graph traversal, pack I/O, watermark handling | Any change to git scanning, blob iteration, or commit history logic |
| **Tiger Harness** | `src/tiger_harness.rs` | `tiger-harness` | Chunking correctness via oracle comparison (root-span containment) | Any change to chunk splitting, overlap computation, or scan-scratch merging |

## Decision Framework

### Use Unit Tests When:
- Testing specific, known edge cases
- Verifying exact output for exact input
- Regression tests for fixed bugs
- Simple function behavior verification
- Fast feedback during development

```rust
#[cfg(test)]
mod tests {
    #[test]
    fn specific_edge_case() {
        assert_eq!(function(edge_input), expected_output);
    }
}
```

### Use Property-Based Tests (proptest) When:
- Function should satisfy invariants for ALL valid inputs
- Testing mathematical properties (commutativity, associativity, idempotence)
- Round-trip properties (encode/decode, serialize/deserialize)
- Relationship between functions (e.g., `parse` and `format` are inverses)
- Exploring large input spaces systematically

```rust
#[cfg(all(test, feature = "stdx-proptest"))]
mod prop_tests {
    use proptest::prelude::*;

    proptest! {
        #[test]
        fn roundtrip_property(input in any::<ValidInput>()) {
            let encoded = encode(&input);
            let decoded = decode(&encoded).unwrap();
            prop_assert_eq!(input, decoded);
        }
    }
}
```

**Run with**: `cargo test --features stdx-proptest`

### Use Fuzz Tests When:
- Parsing untrusted or external input (files, network data)
- Security-critical code paths
- Looking for crashes, panics, or undefined behavior
- Complex state machines with many paths
- Finding inputs that cause pathological performance

```rust
// In fuzz/fuzz_targets/
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    let _ = parse_untrusted(data);
});
```

**Run with**: `cargo +nightly fuzz run <target>`

### Use Kani Model Checking When:
- Proving absence of panics/undefined behavior
- Verifying memory safety in unsafe code
- Proving loop bounds and termination
- Exhaustive verification of small input spaces
- Critical algorithms where bugs are unacceptable

```rust
#[cfg(kani)]
mod verification {
    use super::*;

    #[kani::proof]
    fn verify_no_panic() {
        let x: u32 = kani::any();
        kani::assume(x < 1000);
        let result = critical_function(x);
        // Kani proves this never panics
    }

    #[kani::proof]
    #[kani::unwind(10)]
    fn verify_loop_bounds() {
        let arr: [u8; 8] = kani::any();
        process_array(&arr); // Prove no out-of-bounds
    }
}
```

**Run with**: `cargo kani --features kani`

### Use Simulation Tests When:
- Testing system-level behavior that emerges from component interactions
- Verifying invariants under many possible interleavings or schedules
- Changes touch the scanning pipeline, scheduler, archive handling, or git scanning
- You need deterministic replay of failure cases
- Verifying that chunked scanning matches a single-pass oracle
- Testing fault tolerance (I/O errors, corruption, cancellation)
- Ensuring budget/cap enforcement across the full pipeline

**Choosing the right harness:**

```
Is it about how work gets scheduled, buffer pools, or permits?
  → Scheduler Sim (src/scheduler/sim.rs, feature: scheduler-sim)

Is it about scanning files, finding secrets, or chunking?
  → Scanner Sim (src/sim_scanner/, feature: sim-harness)
  → Also Tiger Harness if specifically about chunk boundary correctness

Is it about archive formats (zip/tar/gzip) or entry extraction?
  → Archive Sim (src/sim_archive/, feature: sim-harness)
  → Scanner Sim for end-to-end archive-then-scan flows

Is it about git blob scanning, commit traversal, or pack I/O?
  → Git Scan Sim (src/sim_git_scan/, feature: sim-harness)
```

**Adding a corpus case** (scanner sim example):
```rust
// tests/simulation/scanner_corpus.rs — add a new #[test] fn
#[test]
fn regression_my_new_edge_case() {
    let scenario = Scenario { /* ... */ };
    let config = RunConfig { /* ... */ };
    let outcome = sim_scanner::runner::run(&scenario, &config);
    assert!(outcome.is_success(), "{outcome:#?}");
}
```

**Adding a corpus case** (scheduler sim example):
```rust
// tests/simulation/scheduler_sim.rs
#[test]
fn my_new_scheduler_invariant() {
    let config = SimConfig { /* ... */ };
    let report = scheduler::sim::run(config, seed);
    report.assert_invariants();
}
```

**Run with**:
```bash
cargo test --features scheduler-sim --test simulation   # Scheduler only
cargo test --features sim-harness --test simulation      # Scanner + archive + git
cargo test --features sim-harness,scheduler-sim --test simulation  # All
```

## Assessment Checklist

When analyzing code for test strategy, consider:

1. **Input Domain**
   - [ ] Fixed, known inputs → Unit tests
   - [ ] Large/infinite input space → Property tests
   - [ ] Untrusted/adversarial input → Fuzz tests
   - [ ] Small but critical input space → Kani
   - [ ] Interleaving-sensitive behavior → Simulation tests

2. **Properties to Verify**
   - [ ] Specific behavior → Unit tests
   - [ ] Invariants over all inputs → Property tests
   - [ ] "Never crashes" → Fuzz tests + Kani
   - [ ] Memory safety → Kani (especially for unsafe)
   - [ ] System-level invariants (no leaks, monotonic progress, ground truth) → Simulation tests

3. **Code Characteristics**
   - [ ] Pure functions → Property tests
   - [ ] Parsers/decoders → Fuzz tests
   - [ ] Unsafe blocks → Kani proofs
   - [ ] State machines → Property tests + Fuzz
   - [ ] Scanning pipeline components → Scanner Sim + Tiger Harness
   - [ ] Scheduler / buffer pool / permits → Scheduler Sim
   - [ ] Archive format handling → Archive Sim
   - [ ] Git blob / commit traversal → Git Scan Sim

4. **Simulation Harness Checklist** (always evaluate)
   - [ ] Does this change affect how files are discovered or scanned? → Scanner Sim
   - [ ] Does this change affect chunking, overlap, or finding dedup? → Scanner Sim + Tiger Harness
   - [ ] Does this change affect task scheduling, buffer management, or budget caps? → Scheduler Sim
   - [ ] Does this change affect archive reading, entry extraction, or path handling? → Archive Sim
   - [ ] Does this change affect git scanning, pack I/O, or commit walking? → Git Scan Sim
   - [ ] Can a new corpus case reproduce the scenario deterministically? → Add to `tests/simulation/` or `tests/corpus/`

5. **Existing Patterns in This Codebase**
   - Unit tests: Same file under `#[cfg(test)] mod tests`
   - Property tests: Sibling `*_tests.rs` files with `stdx-proptest` feature
   - Kani proofs: `#[cfg(kani)]` blocks, see `docs/kani-verification.md`
   - Simulation tests: `tests/simulation/` directory, corpus in `tests/corpus/` and `tests/simulation/corpus/`

## Example Assessment Output

```markdown
## Test Strategy for `WindowValidator`

### Recommended Approach: Property Tests + Kani + Scanner Sim

**Rationale:**
- Operates on sliding windows over byte streams (large input space)
- Has invariant: validated windows never exceed buffer bounds
- Contains unsafe pointer arithmetic
- Part of the scanning pipeline → needs sim coverage

**Specific Tests:**

1. **Property Test**: Window position invariants
   - Property: `window.end <= buffer.len()` for all inputs
   - Property: Windows never overlap incorrectly

2. **Kani Proof**: Memory safety of unsafe block
   - Prove: No out-of-bounds access in `unsafe` pointer ops
   - Bound: Unwind factor based on max window size

3. **Unit Tests**: Known edge cases
   - Empty buffer
   - Single-byte buffer
   - Window at buffer boundary

4. **Simulation**: Scanner Sim corpus case
   - Add scenario exercising the new window behavior under chunking
   - Tiger Harness: verify chunk boundaries don't lose findings
   - Verify oracle match (chunked result == single-pass result)
```

```markdown
## Test Strategy for `ZipEntryIterator`

### Recommended Approach: Fuzz + Archive Sim + Scanner Sim

**Rationale:**
- Parses untrusted archive data (fuzz target)
- Changes archive extraction path → needs Archive Sim coverage
- End-to-end scanning of archive entries → needs Scanner Sim coverage

**Specific Tests:**

1. **Fuzz Test**: Parse arbitrary zip bytes without panic
2. **Archive Sim**: Corpus case with edge-case zip entries
   (long names, deflate truncation, encrypted entries)
3. **Scanner Sim**: End-to-end scenario: zip file → extract → scan → ground truth
4. **Unit Tests**: Known zip quirks (zip64, empty entries, duplicate names)
```

## Quick Reference

| Scenario | Primary | Secondary |
|----------|---------|-----------|
| New data structure | Property tests | Unit tests for edges |
| Parser/decoder | Fuzz tests | Property tests for roundtrip |
| Unsafe code | Kani proofs | Property tests for API |
| Algorithm correctness | Property tests | Unit tests for examples |
| Bug fix | Unit test (regression) | Sim corpus case if pipeline-related |
| Performance-critical loop | Kani (bounds) | Property tests |
| Scanning pipeline change | Scanner Sim | Tiger Harness for chunk correctness |
| Scheduler / buffer mgmt | Scheduler Sim | Unit tests for edge cases |
| Archive format handling | Archive Sim | Fuzz tests for untrusted input |
| Git scanning change | Git Scan Sim | Unit tests for specific commit patterns |
| Chunking / overlap logic | Tiger Harness | Scanner Sim for end-to-end |
| New file type support | Scanner Sim | Archive Sim if archive-based |
