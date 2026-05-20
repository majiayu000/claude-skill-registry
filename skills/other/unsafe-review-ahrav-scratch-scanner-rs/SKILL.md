---
name: unsafe-review
description: Comprehensive review of unsafe code — audits safety invariants, demands benchmark+ASM proof of performance benefit, and verifies Miri/Kani/fuzz/property test coverage for every unsafe block
user-invocable: true
---

# Unsafe Review — Evidence-Gated Unsafe Audit

**Policy: Unsafe is a performance escape hatch, not a shortcut. Every `unsafe` block must
earn its place with benchmark evidence, ASM proof, and exhaustive verification.**

This skill performs a comprehensive review of unsafe code, enforcing the project rule:

> Unsafe is allowed strictly for performance, only AFTER benchmarks + ASM prove its
> benefit is worth it. All unsafe code must have comprehensive testing including
> Miri, Kani, property-based, and fuzz coverage.

## When to Use

- Before merging any PR that adds or modifies `unsafe`
- Periodic audit of existing unsafe code
- After `/asm-forge` introduces new `unsafe` optimizations
- When reviewing someone else's unsafe code
- When a Miri or Kani CI run fails and you need to understand coverage gaps

## Invocation

```
/unsafe-review                           # Audit all unsafe in the codebase
/unsafe-review @src/engine/hit_pool.rs   # Audit specific file
/unsafe-review @src/runtime.rs:450-530   # Audit specific line range
```

## Workflow Overview

```
/unsafe-review @target
    │
    ├─ Phase 1: Discovery & Inventory
    │   └─ Find every unsafe block/fn/impl in scope, classify each
    │
    ├─ Phase 2: Safety Invariant Audit (parallel per file)
    │   └─ For each unsafe block: check documented invariants, verify they hold
    │
    ├─ Phase 3: Performance Justification Audit
    │   └─ For each unsafe block: demand benchmark + ASM evidence
    │
    ├─ Phase 4: Test Coverage Audit (parallel agents)
    │   ├─ Agent A: Miri coverage check
    │   ├─ Agent B: Kani proof coverage check
    │   ├─ Agent C: Fuzz target coverage check
    │   └─ Agent D: Property test coverage check
    │
    ├─ Phase 5: Verdict & Gap Report
    │   └─ Per-block verdict, missing test list, action items
    │
    └─ Phase 6: Test Generation (if requested)
        └─ Write missing Miri tests, Kani proofs, fuzz targets, property tests
```

## Phase 1: Discovery & Inventory

Search the target scope for all unsafe usage. Classify each occurrence:

### Unsafe Categories

| Category | Description | Example |
|----------|-------------|---------|
| **`unsafe` block** | Inline unsafe operation | `unsafe { ptr.add(n).read() }` |
| **`unsafe fn`** | Entire function is unsafe | `unsafe fn raw_write(...)` |
| **`unsafe impl`** | Unsafe trait implementation | `unsafe impl Send for Pool` |
| **`unsafe` in FFI** | Calling extern C functions | `unsafe { hs_scan(...) }` |
| **`unsafe` for intrinsics** | SIMD or arch intrinsics | `unsafe { _mm_cmpeq_epi8(...) }` |

### Inventory Table Format

For each unsafe occurrence, record:

```markdown
| # | File:Line | Category | Purpose (1-line) | Has Safety Comment | In Hot Path |
|---|-----------|----------|------------------|--------------------|-------------|
| 1 | hit_pool.rs:172 | block | Unchecked index into sorted array | Yes | Yes |
| 2 | hit_pool.rs:184 | block | ptr::copy_nonoverlapping for bulk move | No | Yes |
```

**"In Hot Path"** means the code is in a function that appears in benchmarks or profiling
data. This is the primary justification for unsafe — if it's not in a hot path, it
almost certainly shouldn't be unsafe.

## Phase 2: Safety Invariant Audit

For each unsafe block, verify:

### 2.1 Documentation Check

Every `unsafe` block MUST have a `// SAFETY:` comment immediately above it explaining:
- What invariant makes this safe
- Why the invariant holds at this call site
- What could break the invariant

```rust
// GOOD ✓
// SAFETY: `idx` is bounded by `self.len` which is checked at line 165.
// The backing allocation is guaranteed to be at least `self.cap` elements
// by the constructor invariant (see `new()`).
unsafe { *self.ptr.add(idx) }

// BAD ✗
unsafe { *self.ptr.add(idx) }  // No safety comment

// BAD ✗
// SAFETY: this is safe because we know it works
unsafe { *self.ptr.add(idx) }  // Vacuous justification
```

**Flag as MISSING or INSUFFICIENT** if the safety comment doesn't explain the specific
invariant that makes this particular usage sound.

### 2.2 Invariant Verification

For each claimed invariant, trace it back to its enforcement:

1. **Bounds invariants**: Find the bounds check or proof that index < len
2. **Alignment invariants**: Find the alignment guarantee (allocation, `#[repr(C)]`, etc.)
3. **Lifetime invariants**: Verify the data outlives the reference
4. **Aliasing invariants**: Verify no mutable aliasing (`&mut` uniqueness)
5. **Initialization invariants**: Verify memory is initialized before read
6. **Type invariants**: Verify transmute/cast targets are valid for the bit pattern

### 2.3 Scope Minimality

Verify each unsafe block contains ONLY the operations that require unsafe:

```rust
// GOOD ✓ — minimal unsafe scope
let val = unsafe { *ptr.add(idx) };
process(val);  // safe code outside unsafe block

// BAD ✗ — unnecessary code inside unsafe block
unsafe {
    let val = *ptr.add(idx);
    process(val);        // This doesn't need unsafe
    log::debug!("{val}"); // Neither does this
}
```

### Safety Audit Output

For each unsafe block:

```markdown
### Block #N: file.rs:LINE

**Category**: [block | fn | impl | FFI | intrinsic]
**Purpose**: [one-line description]
**Safety comment**: [Present/Missing/Insufficient]
**Invariant claimed**: [what the safety comment says]
**Invariant verified**: [Yes — traced to LINE | No — EXPLAIN GAP]
**Scope minimal**: [Yes | No — EXPLAIN what can move outside]
**Status**: [SOUND | REVIEW | UNSOUND]
```

## Phase 3: Performance Justification Audit

**This is the gate that matters most.** Every unsafe block must have evidence that:

1. A safe alternative was tried and measured
2. The unsafe version is measurably faster (benchmark proof)
3. The codegen difference is understood (ASM proof)

### 3.1 Evidence Requirements

For each unsafe block, look for:

| Evidence Type | Where to Find | Required? |
|---------------|---------------|-----------|
| **Benchmark comparison** | `benches/` — Criterion results showing safe vs unsafe | YES |
| **ASM diff** | PR description, commit message, or `docs/` | YES |
| **Profiling data** | Flamegraph, perf counters showing this as hot | Recommended |
| **Safe alternative attempted** | Git history, PR discussion, comments in code | YES |

### 3.2 How to Check

For each unsafe block, answer:

1. **Is there a corresponding benchmark?** Search `benches/` for functions that exercise
   this code path. If no benchmark covers this path, the unsafe is **UNJUSTIFIED**.

2. **Was a safe version benchmarked?** Check git history (`git log -p --all -S 'the_function'`)
   for evidence of a safe-vs-unsafe comparison. Check PR descriptions for benchmark data.

3. **Does the ASM actually differ?** Run `/asm-forge` recon on the function. Compare ASM
   for the unsafe version vs the safe alternative. If the compiler generates identical code,
   the unsafe is **UNNECESSARY**.

4. **What is the measured speedup?** The benefit should be significant for the risk:
   - **>10% speedup on a hot path**: Strong justification
   - **2-10% speedup on a hot path**: Acceptable if well-tested
   - **<2% speedup**: Marginal — consider removing the unsafe
   - **Not on a hot path**: Almost never justified — remove the unsafe

### 3.3 Special Cases

**FFI (e.g., vectorscan bindings)**: Unsafe is inherent in FFI. The performance
justification is "we need this library's functionality." Focus the audit on correctness
of the FFI boundary (pointer validity, lifetime, callback safety) rather than demanding
a safe alternative.

**SIMD intrinsics**: If `std::simd` (portable SIMD) can achieve the same result, prefer
it. If arch-specific intrinsics are needed, verify with ASM that portable SIMD doesn't
generate equivalent code. Benchmark both.

**`Send`/`Sync` impls**: No performance justification needed, but correctness justification
is critical. Focus on proving the type is actually thread-safe.

### Performance Justification Output

```markdown
### Block #N: file.rs:LINE

**Benchmark coverage**: [bench_name — COVERED | NONE — needs benchmark]
**Safe alternative tried**: [Yes — git SHA / PR# | No — UNJUSTIFIED]
**Measured speedup**: [X% on bench_name | Unknown — UNJUSTIFIED]
**ASM evidence**: [bounds check eliminated / SIMD enabled / etc. | NONE]
**Hot path**: [Yes — appears in profiling | No — UNJUSTIFIED | FFI — exempt]
**Verdict**: [JUSTIFIED | UNJUSTIFIED | EXEMPT (FFI/Send/Sync)]
```

## Phase 4: Test Coverage Audit

Launch four parallel agents to check test coverage for each unsafe block.

### Agent A: Miri Coverage

Check whether each unsafe block is exercised under Miri:

```bash
# Current Miri command (from CI):
cargo +nightly miri test --lib -- \
  --skip engine:: \
  --skip git_scan:: \
  --skip scheduler::affinity \
  --skip scheduler::device_slots \
  --skip scheduler::rusage \
  --skip scheduler::local_fs_uring \
  --skip scheduler::engine_impl \
  --skip scheduler::parallel_scan \
  --skip rules::yaml \
  --skip archive::
```

**Miri flags used** (from CI):
- `-Zmiri-strict-provenance` — catches pointer provenance violations
- `-Zmiri-symbolic-alignment-check` — catches misaligned access
- `-Zmiri-preemption-rate=0.1` — thread interleaving for concurrent tests
- `-Zmiri-disable-isolation` — allows FFI testing

For each unsafe block:
1. Is the module skipped in Miri? If yes, is there a reason (FFI dependency)?
2. Is there a `#[test]` that exercises this specific unsafe path?
3. Does the test exercise edge cases (empty input, max capacity, boundary values)?

**Miri Gap Classification:**

| Gap Type | Severity | Action |
|----------|----------|--------|
| Module skipped (FFI-dependent) | Medium | Write isolated unit test that exercises the unsafe logic without FFI |
| Module not skipped but no test hits this path | High | Write targeted test |
| Test exists but doesn't cover edge cases | Medium | Add edge case inputs |
| Covered with edge cases | None | Document as verified |

### Agent B: Kani Proof Coverage

Check whether each unsafe block has a corresponding Kani proof:

```bash
# Find existing Kani proofs
grep -rn '#\[kani::proof\]' src/ tests/
```

**Current Kani proof inventory** (49 proofs across 9 components — see `docs/kani-verification.md`):

For each unsafe block, check:
1. Is there a `#[kani::proof]` that exercises this operation?
2. Does the proof cover the full input domain (or appropriate bounds)?
3. Does the proof verify absence of undefined behavior?
4. Is `#[kani::unwind(N)]` set correctly (not too low, not needlessly high)?

**Kani proof requirements for common unsafe patterns:**

| Unsafe Pattern | Required Kani Property |
|----------------|----------------------|
| `ptr.add(n)` / `ptr.offset(n)` | Prove `n <= allocation_size - size_of::<T>()` |
| `slice::from_raw_parts(ptr, len)` | Prove `ptr` is valid for `len` elements, aligned, initialized |
| `get_unchecked(idx)` | Prove `idx < slice.len()` |
| `transmute::<A, B>(val)` | Prove every bit pattern of A is valid B |
| `ptr::copy_nonoverlapping` | Prove regions don't overlap and dest is valid |
| `MaybeUninit::assume_init()` | Prove the value was actually initialized |

### Agent C: Fuzz Target Coverage

Check whether each unsafe block is reachable from a fuzz target:

```bash
# List fuzz targets
ls fuzz/fuzz_targets/
```

**Current fuzz targets** (13):
- `fuzz_b64_gate_determinism.rs`, `fuzz_b64_gate_differential.rs`, `fuzz_b64_gate_build_and_scan.rs`
- `fuzz_anchor_soundness.rs`, `fuzz_tiger_chunking.rs`
- `fuzz_pack_parse_delta.rs`, `fuzz_pack_delta_into.rs`, `fuzz_pack_inflate_stream.rs`, `fuzz_pack_exec.rs`
- `fuzz_atomic_bitset.rs`, `fuzz_vs_cache_load.rs`
- `fuzz_pyc_extract.rs`, `fuzz_java_class_extract.rs`

For each unsafe block:
1. Is it reachable from any existing fuzz target?
2. If not, should a new fuzz target be created?
3. Does the fuzz target exercise the unsafe path with adversarial input shapes?

### Agent D: Property Test Coverage

Check for proptest coverage:

```bash
# Find property tests
grep -rn 'proptest!' src/ tests/
```

For each unsafe block:
1. Is there a property test that exercises the safe public API wrapping this unsafe?
2. Does the property test verify the key invariant (e.g., roundtrip, bounds, monotonicity)?
3. Is the input strategy broad enough to stress edge cases?

### Coverage Matrix Output

```markdown
## Test Coverage Matrix

| # | File:Line | Purpose | Miri | Kani | Fuzz | Proptest | Verdict |
|---|-----------|---------|------|------|------|----------|---------|
| 1 | hit_pool.rs:172 | unchecked index | ✓ | ✗ | ✗ | ✓ | GAPS |
| 2 | hit_pool.rs:184 | copy_nonoverlapping | ✓ | ✗ | ✗ | ✗ | GAPS |
| 3 | spsc.rs:45 | atomic load | ✓ (loom) | ✓ | ✗ | ✗ | OK |
| 4 | vectorscan.rs:317 | FFI call | SKIP(FFI) | N/A | ✓ | N/A | OK |

### Legend
- ✓ = Covered with meaningful test
- ✗ = Missing — needs test
- SKIP(reason) = Intentionally skipped with justification
- N/A = Not applicable for this unsafe category
```

## Phase 5: Verdict & Gap Report

Combine all phases into a final report. For each unsafe block, assign a verdict:

### Verdict Levels

| Verdict | Meaning | Action Required |
|---------|---------|-----------------|
| **APPROVED** | Safety sound, performance justified, tests comprehensive | None |
| **APPROVED-FFI** | FFI boundary — inherently unsafe, correctness verified | None |
| **NEEDS-TESTS** | Safety + perf justified, but test coverage has gaps | Write missing tests |
| **NEEDS-JUSTIFICATION** | Missing benchmark/ASM evidence for performance benefit | Provide evidence or rewrite as safe |
| **NEEDS-SAFETY-COMMENT** | Missing or insufficient `// SAFETY:` documentation | Add documentation |
| **UNJUSTIFIED** | No evidence unsafe is needed — remove it | Rewrite as safe code |
| **UNSOUND** | Safety invariant doesn't hold or can be violated | Fix immediately |

### Final Report Format

```markdown
# Unsafe Review Report: [scope]

**Date**: YYYY-MM-DD
**Reviewer**: Claude (automated)
**Scope**: [files reviewed]

## Summary

| Verdict | Count |
|---------|-------|
| APPROVED | N |
| APPROVED-FFI | N |
| NEEDS-TESTS | N |
| NEEDS-JUSTIFICATION | N |
| NEEDS-SAFETY-COMMENT | N |
| UNJUSTIFIED | N |
| UNSOUND | N |

## Critical Findings (UNSOUND / UNJUSTIFIED)

[List any blocks that need immediate attention]

## Detailed Audit

### File: src/engine/hit_pool.rs

#### Block #1: line 172 — `get_unchecked` in sorted lookup

**Safety**: SOUND — bounds proven by binary search result (line 168)
**Performance**: JUSTIFIED — 8.3% speedup in `hit_pool` bench (commit abc123)
**Tests**:
- Miri: ✓ (test_sorted_lookup exercises this path)
- Kani: ✗ MISSING — need proof that binary search result < len
- Fuzz: ✗ MISSING — no fuzz target reaches hit_pool
- Proptest: ✓ (prop_sorted_invariant in hit_pool_tests.rs)
**Verdict**: NEEDS-TESTS

**Action items**:
1. Add Kani proof: `verify_sorted_lookup_bounds`
2. Add fuzz target or extend existing target to reach this path

[... repeat for each block ...]

## Missing Test Summary

### Kani Proofs to Write
1. `verify_sorted_lookup_bounds` — hit_pool.rs:172
2. `verify_bulk_copy_nonoverlap` — hit_pool.rs:184

### Miri Tests to Write
1. `test_edge_empty_pool` — hit_pool.rs (exercises empty-pool unsafe path)

### Fuzz Targets to Write/Extend
1. `fuzz_hit_pool_accumulate` — new target for hit_pool adversarial input

### Property Tests to Write
1. `prop_copy_preserves_order` — hit_pool.rs:184 bulk move preserves sort
```

## Phase 6: Test Generation (Optional)

If gaps are found in Phase 4-5, generate the missing tests. Use these templates:

### Miri Test Template

```rust
// Tests in this module are designed to be run under Miri for
// undefined behavior detection. Run with:
//   cargo +nightly miri test --lib module::tests::miri_
//
// Miri flags (match CI):
//   MIRIFLAGS="-Zmiri-strict-provenance -Zmiri-symbolic-alignment-check"

#[cfg(test)]
mod tests {
    use super::*;

    /// Exercises [unsafe operation] with [edge case description].
    /// Under Miri, this catches: [what Miri would detect].
    #[test]
    fn miri_edge_case_description() {
        // Setup: construct minimal state that reaches the unsafe path
        // Exercise: call the function with edge-case input
        // Verify: assert the result is correct
        // Miri implicitly checks: no UB, valid provenance, proper alignment
    }

    /// Boundary condition: [description]
    #[test]
    fn miri_boundary_description() {
        // ... tests at capacity limits, zero-size, max-size
    }
}
```

**Key Miri test patterns for this project:**
- **Empty/zero-size inputs**: Catches null pointer dereference, zero-length slices
- **Capacity boundaries**: Catches off-by-one in pointer arithmetic
- **Aliasing patterns**: Catches mutable aliasing through raw pointers
- **Drop order**: Catches use-after-free in pool/arena patterns (see `scratch_memory.rs:514`)
- **Thread interleaving**: Catches data races in atomic/lock-free structures (with loom)

### Kani Proof Template

```rust
#[cfg(kani)]
mod verification {
    use super::*;

    /// Proves [unsafe operation] cannot cause [UB type].
    /// Covers: [input domain description]
    #[kani::proof]
    #[kani::unwind(N)]  // Set to max loop iterations + 1
    fn verify_operation_safety() {
        let size: usize = kani::any();
        kani::assume(size <= MAX_REASONABLE_BOUND);

        // Construct the data structure
        // Perform the operation
        // Kani proves no panics, no UB, no out-of-bounds
    }

    /// Proves [invariant] holds for all valid inputs.
    #[kani::proof]
    fn verify_invariant_name() {
        // Use kani::any() for symbolic inputs
        // Use kani::assume() to constrain to valid domain
        // Assert the invariant
    }
}
```

**Kani proof sizing for this project:**
- `#[kani::unwind(N)]`: Set `N` = max loop iteration count + 1
- Bound symbolic values to keep verification tractable (typical: `size <= 64`)
- For pointer arithmetic proofs: model the allocation symbolically
- See `docs/kani-verification.md` for existing patterns and unwind values

### Fuzz Target Template

```rust
// fuzz/fuzz_targets/fuzz_<component>.rs
#![no_main]
use libfuzzer_sys::fuzz_target;
use arbitrary::Arbitrary;

/// Fuzz target for [component] unsafe operations.
/// Exercises: [list of unsafe paths reached]
///
/// Run: cargo +nightly fuzz run fuzz_<component> -- -max_len=4096
#[derive(Arbitrary, Debug)]
struct FuzzInput {
    // Structured input that exercises the unsafe paths
    // Use Arbitrary derive for automatic generation
}

fuzz_target!(|input: FuzzInput| {
    // Construct component from fuzz input
    // Exercise the operations that contain unsafe
    // No explicit asserts needed — fuzz catches panics and UB (with sanitizers)
});
```

**Don't forget** to register new fuzz targets in `fuzz/Cargo.toml`:
```toml
[[bin]]
name = "fuzz_<component>"
path = "fuzz_targets/fuzz_<component>.rs"
```

### Property Test Template

```rust
#[cfg(all(test, feature = "stdx-proptest"))]
mod prop_tests {
    use super::*;
    use proptest::prelude::*;

    /// Property: [invariant description]
    /// Exercises unsafe path at [file:line] through safe API.
    proptest! {
        #[test]
        fn prop_invariant_name(input in strategy()) {
            // Exercise through safe public API
            // Assert the invariant that the unsafe code relies on
            // e.g., roundtrip, bounds preservation, ordering
        }
    }

    /// Property: [description] — specifically targets edge cases
    /// for the unsafe operation at [file:line].
    proptest! {
        #[test]
        fn prop_edge_case_name(
            size in 0usize..=MAX_CAP,
            idx in 0usize..=MAX_CAP,
        ) {
            prop_assume!(idx < size);
            // Test the operation at various sizes and indices
        }
    }
}
```

## Running Verification Locally

### Quick Miri Check (specific module)

```bash
# Run Miri on a single module's tests
MIRIFLAGS="-Zmiri-strict-provenance -Zmiri-symbolic-alignment-check" \
  cargo +nightly miri test --lib <module>::tests

# Run Miri on a specific test
MIRIFLAGS="-Zmiri-strict-provenance -Zmiri-symbolic-alignment-check" \
  cargo +nightly miri test --lib <module>::tests::miri_test_name
```

### Quick Kani Check (specific proof)

```bash
# Run a single Kani proof
cargo kani --features kani --harness verify_proof_name

# Run all proofs in a module
cargo kani --features kani --module module_name
```

### Quick Fuzz Check (smoke test)

```bash
# Short fuzz run to verify target compiles and finds no immediate crashes
cargo +nightly fuzz run fuzz_target_name -- -max_total_time=30
```

### Full Verification Suite

```bash
# All Miri tests (matching CI)
MIRIFLAGS="-Zmiri-strict-provenance -Zmiri-symbolic-alignment-check -Zmiri-preemption-rate=0.1 -Zmiri-disable-isolation" \
  cargo +nightly miri test --lib -- \
    --skip engine:: --skip git_scan:: --skip scheduler::affinity \
    --skip scheduler::device_slots --skip scheduler::rusage \
    --skip scheduler::local_fs_uring --skip scheduler::engine_impl \
    --skip scheduler::parallel_scan --skip rules::yaml --skip archive::

# All Kani proofs
cargo kani --features kani

# All property tests
cargo test --features stdx-proptest
```

## Checklist (copy into PR)

```markdown
## Unsafe Review Checklist

### Safety
- [ ] Every `unsafe` block has a `// SAFETY:` comment
- [ ] Every claimed invariant is traced to its enforcement point
- [ ] Unsafe scope is minimal (no safe code inside unsafe blocks)
- [ ] No undefined behavior paths identified

### Performance Justification
- [ ] Benchmark exists covering this unsafe code path
- [ ] Safe alternative was benchmarked and is measurably slower
- [ ] ASM diff shows concrete codegen improvement (e.g., bounds check eliminated)
- [ ] Speedup is significant enough to justify the maintenance cost

### Test Coverage
- [ ] Miri: Tests exercise this unsafe path with strict provenance + alignment checks
- [ ] Kani: Formal proof covers the safety-critical invariant
- [ ] Fuzz: Target reaches this code with adversarial inputs (or justification for skip)
- [ ] Proptest: Property test verifies the invariant through the safe public API
- [ ] Edge cases: Empty input, zero-size, max capacity, boundary values tested

### Documentation
- [ ] Safety invariants documented in `// SAFETY:` comments
- [ ] Performance justification documented (benchmark results, ASM evidence)
- [ ] Test coverage documented (which tests verify which unsafe blocks)
```

## Related Skills

- `/asm-forge` — Collect ASM evidence for performance justification
- `/bench-compare` — Run benchmark comparisons (safe vs unsafe)
- `/security-reviewer` — Broader security audit (CWE mapping, input validation)
- `/test-strategy` — Choose testing approach for new code
- `/run-fuzz` — Execute fuzz targets
- `/perf-regression` — Full regression testing before merge
