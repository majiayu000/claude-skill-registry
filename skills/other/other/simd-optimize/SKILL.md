---
name: simd-optimize
description: SIMD vectorization for Rust — detects ISA features, identifies vectorizable patterns, generates platform-specific intrinsics (ARM NEON/SVE, x86 SSE/AVX/AVX-512), validates correctness and performance. Uses tiered research with baked-in references and /deep-research fallback.
---

# SIMD Optimize — Vectorization for Rust

**Philosophy: Detect, analyze, implement, validate. Never guess the ISA.**

Every SIMD optimization starts by detecting what the hardware actually supports,
analyzing what the compiler already auto-vectorized (and what it missed),
choosing the right intrinsics from reference material, implementing with proper
fallback chains, and validating correctness + performance.

## When to Use

- Converting scalar loops to SIMD where profiling shows time is spent on data-parallel work
- After `/rust-hotspot-finder` identified a loop-heavy hot function
- When `/asm-forge` shows the compiler failed to auto-vectorize a loop
- Adding SIMD support that works across x86-64 and AArch64
- Evaluating whether to use explicit intrinsics vs helping the auto-vectorizer
- Understanding what SIMD capabilities the target hardware has

## When NOT to Use

- For non-data-parallel work (graph traversal, tree operations, hash table probing)
- For I/O-bound code (disk, network — SIMD won't help)
- When the loop body has side effects or complex control flow that can't be vectorized
- When input sizes are tiny (<64 bytes) — SIMD setup overhead may dominate
- For general codegen quality issues — use `/asm-forge` instead

## Prerequisites

### Required

```bash
# cargo-show-asm: inspect compiler output
cargo install cargo-show-asm

# jq: parse detection script output
brew install jq  # macOS
apt install jq   # Linux

# Criterion benchmarks must exist for the target code
```

### Recommended

```bash
# proptest: property-based testing for SIMD vs scalar comparison
# Add to [dev-dependencies]: proptest = "1"
```

## Invocation

```
/simd-optimize @file.rs "description of what to vectorize"
```

Examples:
```
/simd-optimize @src/engine/transform.rs "vectorize the base64 decode loop"
/simd-optimize @src/lsm/set_associative_cache.rs "add AVX2 path for tag search"
/simd-optimize @src/scanner/byte_search.rs "SIMD byte search across x86 and ARM"
```

## Workflow Overview

```
/simd-optimize @file.rs "target description"
    │
    ├─ Phase 0: ISA Detection
    │   └─ Run detect_simd.sh → JSON capability report
    │
    ├─ Phase 1: Analysis (3 parallel agents)
    │   ├─ Agent A: Loop Analyzer — identify vectorizable patterns
    │   ├─ Agent B: Autovec Auditor — what did rustc already vectorize?
    │   └─ Agent C: Constraint Mapper — data layout, alignment, types
    │
    ├─ Phase 2: Research & Strategy
    │   ├─ Load ISA-specific references (tiered: baked-in first)
    │   ├─ Match patterns to reference implementations
    │   ├─ If gap → invoke /deep-research for specific pattern
    │   └─ Select strategy: intrinsics / help-autovec / portable-simd / crate
    │
    ├─ Phase 3: Implementation
    │   ├─ Ensure scalar reference exists (for correctness testing)
    │   ├─ Write SIMD implementation(s) with cfg gating
    │   ├─ Wire runtime dispatch if needed
    │   ├─ Handle remainder elements
    │   └─ Add unsafe blocks with safety comments
    │
    └─ Phase 4: Validation (2 parallel agents)
        ├─ Agent D: Correctness — proptest comparing SIMD vs scalar
        └─ Agent E: Performance — /bench-compare against baseline
```

## Phase 0: ISA Detection

Run the bundled detection script:

```bash
bash <skill_dir>/scripts/detect_simd.sh
```

This outputs JSON like:

```json
{
  "arch": "aarch64",
  "os": "darwin",
  "rust_target": "aarch64-apple-darwin",
  "cpu_model": "Apple M1 Pro",
  "features": {
    "aes": true, "crc": true, "neon": true,
    "sha2": true, "sve": false, "sve2": false
  },
  "max_vector_width_bits": 128,
  "recommended_baseline": "neon",
  "recommended_fast_path": null,
  "frequency_throttle_risk": false
}
```

**Key fields for subsequent phases:**
- `recommended_baseline` — ISA level to target for the primary SIMD implementation
- `recommended_fast_path` — optional higher ISA for runtime dispatch (e.g., "avx512")
- `frequency_throttle_risk` — if true, warn about Intel AVX-512 downclocking

Present the capability report to the user before proceeding.

## Phase 1: Analysis

Launch three parallel agents using the Task tool in a single message:

### Agent A: Loop Analyzer

```
Analyze the target code for vectorizable patterns. For each candidate loop:

1. Classify the pattern:
   - Map (element-wise transform)
   - Reduction (sum, min, max, count, any/all)
   - Search (find first/all matching elements)
   - Scan (prefix sum, running accumulator)
   - LUT (lookup table, classify/translate)
   - Pack/unpack (narrow, widen, interleave)
   - Filter (compress matching elements)

2. Identify the iteration pattern:
   - Trip count (fixed, bounded, data-dependent?)
   - Memory access pattern (contiguous, strided, random?)
   - Loop-carried dependencies (accumulator, state machine?)

3. Estimate the vector-friendliness:
   - HIGH: Pure map/search on contiguous arrays, no loop-carried deps
   - MEDIUM: Reduction with associative op, or strided access
   - LOW: Data-dependent iterations, random access, complex control flow

Output a ranked candidate list with pattern classification and confidence.
```

### Agent B: Autovec Auditor

```
Check what the compiler already auto-vectorized using check_autovec.sh.

Run: bash <skill_dir>/scripts/check_autovec.sh <crate> '<function_path>'

For each candidate function from the Loop Analyzer:
1. Report whether rustc generated SIMD instructions
2. If yes: what width? What percentage of the loop is vectorized?
3. If no: what likely blocked auto-vectorization?
   - Function calls in loop body
   - Loop-carried dependencies
   - Complex control flow
   - Non-contiguous memory access
   - Iterator chain that inhibits vectorization

Summarize: which functions need manual SIMD, which are already handled.
```

### Agent C: Constraint Mapper

```
Analyze data layout and constraints that affect SIMD implementation:

1. Data layout: AoS (array of structs) or SoA (struct of arrays)?
   - AoS needs deinterleaving (vld2/vzip) or transpose
   - SoA is directly SIMD-friendly

2. Alignment: Are buffers aligned to 16/32/64 bytes?
   - Check allocator usage, struct layout, slice origins
   - If unknown, must use unaligned loads

3. Element types: u8, u16, u32, u64, f32, f64?
   - Narrower types = more elements per vector = higher speedup
   - Mixed types need widening/narrowing

4. Memory access pattern: contiguous, strided, gathered?
   - Contiguous: simple vector load
   - Strided: may need shuffle after load
   - Gathered: expensive on most ISAs (prefer restructuring)

5. Aliasing: Do input and output buffers overlap?
   - If yes: must process in correct order or use temporary

Output a constraint report that guides implementation choices.
```

## Phase 2: Research & Strategy

### Step 1: Load References (tiered)

Based on Phase 0 ISA detection and Phase 1 pattern analysis:

```
IF arch == "x86_64":
    LOAD references/x86-sse-avx.md
    IF features.avx512f == true:
        LOAD references/x86-avx512.md

ELIF arch == "aarch64":
    LOAD references/arm-neon.md
    IF features.sve == true OR features.sve2 == true:
        LOAD references/arm-sve.md

ALWAYS LOAD:
    references/simd-patterns.md      (cross-platform pattern cookbook)
    references/portability-guide.md   (dispatch, fallback chains)
    references/pitfalls.md            (bugs to avoid)
```

### Step 2: Match Patterns to References

For each vectorizable candidate from Phase 1:
1. Find the matching pattern in `simd-patterns.md`
2. Check the ISA-specific reference for the right intrinsics
3. Note any pitfalls from `pitfalls.md` that apply

### Step 3: Gap Check

If a pattern isn't covered by the baked-in references:
```
Invoke /deep-research with query:
"Rust SIMD implementation of [pattern description] using
[ISA: AVX2/NEON/etc] intrinsics from std::arch::[arch].
Include complete code example with #[target_feature] and unsafe."
```

### Step 4: Strategy Selection

Choose the implementation approach:

| Strategy | When to Use | Tradeoff |
|----------|-------------|----------|
| **Direct intrinsics** (`std::arch`) | Maximum control needed, complex patterns | Most effort, best performance |
| **Help auto-vectorizer** | Simple loops, compiler almost got it | Least effort, fragile |
| **Portable SIMD** (`std::simd`) | Portability > peak performance, nightly OK | Moderate effort, portable |
| **Crate** (`wide`, `pulp`, `multiversion`) | Need stable Rust + portability | Easy, some overhead |

Default recommendation: **Direct intrinsics** for hot paths, **help auto-vectorizer**
for secondary paths.

## Phase 3: Implementation

### Step 1: Ensure Scalar Reference Exists

Before writing SIMD code, verify a correct scalar implementation exists. This is
the ground truth for correctness testing. If one doesn't exist, write it first.

### Step 2: Write SIMD Implementation

Follow this template:

```rust
#[cfg(target_arch = "x86_64")]
#[target_feature(enable = "avx2")]
unsafe fn process_avx2(data: &[u8]) -> Result {
    // SAFETY:
    // - Caller ensures `is_x86_feature_detected!("avx2")` returned true
    // - `data.len() >= 32` checked by caller (or handled by remainder loop)
    // - Unaligned loads used (no alignment requirement)

    use core::arch::x86_64::*;

    let mut i = 0;
    let len = data.len();

    // Main SIMD loop: process 32 bytes at a time
    while i + 32 <= len {
        let chunk = _mm256_loadu_si256(data.as_ptr().add(i) as *const __m256i);
        // ... SIMD operations ...
        i += 32;
    }

    // Remainder: scalar fallback for last <32 bytes
    while i < len {
        // ... scalar processing ...
        i += 1;
    }

    result
}

#[cfg(target_arch = "aarch64")]
#[target_feature(enable = "neon")]
unsafe fn process_neon(data: &[u8]) -> Result {
    // SAFETY:
    // - NEON is always available on AArch64 (no runtime check needed)
    // - `data.len() >= 16` checked by caller
    // - vld1q_u8 handles unaligned loads

    use core::arch::aarch64::*;

    let mut i = 0;
    let len = data.len();

    while i + 16 <= len {
        let chunk = vld1q_u8(data.as_ptr().add(i));
        // ... NEON operations ...
        i += 16;
    }

    // Remainder
    while i < len {
        i += 1;
    }

    result
}

/// Scalar fallback — always correct, used as reference and fallback
fn process_scalar(data: &[u8]) -> Result {
    // ... straightforward scalar implementation ...
}

/// Public dispatch function
pub fn process(data: &[u8]) -> Result {
    #[cfg(target_arch = "x86_64")]
    {
        if is_x86_feature_detected!("avx2") {
            return unsafe { process_avx2(data) };
        }
    }

    #[cfg(target_arch = "aarch64")]
    {
        // NEON is always available on AArch64
        return unsafe { process_neon(data) };
    }

    process_scalar(data)
}
```

### Step 3: Implementation Checklist

- [ ] Each SIMD function has `#[target_feature(enable = "...")]`
- [ ] Each SIMD function is `unsafe fn` with a `// SAFETY:` comment
- [ ] Safety comment documents: feature availability, bounds, alignment
- [ ] Remainder/tail elements handled (scalar loop, overlap, or masked)
- [ ] No panicking paths in the SIMD loop (no indexing with `[]`)
- [ ] `cfg(target_arch)` gates each platform-specific function
- [ ] Dispatch function selects the best available implementation
- [ ] For x86: runtime detection with `is_x86_feature_detected!`
- [ ] For AArch64: NEON is always available, no runtime check needed

### Step 4: Match Project Patterns

When adding SIMD to this project, follow existing patterns:

- `src/lsm/set_associative_cache.rs`: NEON + SSE2 tag matching with
  `cfg(target_arch)` dispatch
- `src/engine/transform.rs`: NEON + SSSE3 base64 decode with separate functions

## Phase 4: Validation

Launch two parallel agents:

### Agent D: Correctness Validator

```
Write property tests comparing SIMD implementation against scalar reference.

Use proptest with these test vectors:
1. Empty input (length 0)
2. Single element
3. Exactly one vector width (16 bytes for NEON/SSE, 32 for AVX2)
4. One less than vector width (15, 31)
5. One more than vector width (17, 33)
6. Random lengths up to 10000
7. All zeros (0x00)
8. All ones (0xFF)
9. Alternating patterns (0xAA, 0x55)
10. Maximum values for the element type
11. Values at type boundaries (127/128, 255/0 for u8)

Template:
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn simd_matches_scalar(data in prop::collection::vec(any::<u8>(), 0..10000)) {
        let simd_result = process(&data);    // uses dispatch (SIMD when available)
        let scalar_result = process_scalar(&data);
        prop_assert_eq!(simd_result, scalar_result);
    }
}
```

Run tests and report results.
```

### Agent E: Performance Validator

```
Invoke /bench-compare to measure SIMD vs scalar performance.

If Criterion benchmarks exist for the target function:
  Run: cargo bench --bench <name> -- --save-baseline simd-before
  Apply SIMD changes
  Run: cargo bench --bench <name> -- --baseline simd-before

If no benchmarks exist:
  Create a minimal Criterion benchmark comparing scalar vs SIMD dispatch.

Report:
- Throughput improvement (bytes/sec or ops/sec)
- Latency reduction (ns per call)
- Speedup factor (e.g., 4.2x for AVX2 on a byte-search pattern)
- Whether speedup matches theoretical expectation (vector_width / scalar_width)
```

## Output Format

After all phases complete, present:

```markdown
## SIMD Optimization Report

### Machine Capabilities
- Arch: [x86_64 / aarch64]
- CPU: [model]
- Baseline ISA: [sse2 / avx2 / neon]
- Fast path: [avx512 / sve2 / none]

### Patterns Found
| Pattern | Function | Strategy | Expected Speedup |
|---------|----------|----------|------------------|
| Byte search | find_byte() | Direct intrinsics (AVX2 + NEON) | 8-16x |
| Horizontal sum | reduce_sum() | Help auto-vectorizer | 2-4x |

### Implementation Summary
- Files modified: [list]
- Lines added: [N]
- SIMD paths: [x86_64 AVX2, aarch64 NEON, scalar fallback]

### Validation
- Correctness: [X/Y proptest strategies passing]
- Performance: [Nx speedup measured, Z bytes/sec throughput]

### Remaining Opportunities
[Any patterns not addressed and why]
```

## Tips

### ISA-Specific Notes

**x86-64:**
- SSE2 is baseline (always available) — 128-bit vectors
- AVX2 is the sweet spot — 256-bit vectors, no throttling
- AVX-512 gives 512-bit but beware Intel frequency throttling
- `_mm256_shuffle_epi8` shuffles within 128-bit lanes, NOT across them
- Use `_mm256_permutevar8x32_epi32` for cross-lane permutes

**AArch64:**
- NEON is always available — no feature detection needed
- 128-bit vectors (32 registers — less pressure than x86's 16)
- `vmaxvq_u8` for horizontal max (single instruction, unlike x86's movemask)
- NEON compares return full-width masks (all-1s), not bitmasks like x86
- No frequency throttling ever — 128-bit SIMD is free

### When to Escalate to /deep-research

Invoke `/deep-research` when:
- The pattern isn't in `simd-patterns.md` (e.g., custom hash, crypto, compression)
- You need performance data for a specific microarchitecture
- The intrinsic you need may not be in stable Rust yet
- You're evaluating whether `std::simd` covers the pattern

### Common Mistakes

1. Forgetting the scalar remainder loop → UB on non-multiple-of-width inputs
2. Using aligned loads on unaligned data → segfault on x86
3. Missing `#[target_feature]` → SIMD instructions not emitted
4. Testing only on the dev machine → breaks on CI with different ISA
5. Not comparing against the scalar reference → SIMD result silently wrong

## Related Skills

- `/asm-forge` — Post-SIMD assembly audit (verify codegen quality)
- `/rust-hotspot-finder` — Identify what functions to vectorize (run first)
- `/bench-compare` — Quick before/after benchmark comparison
- `/performance-analyzer` — Broader performance analysis
- `/deep-research` — Research specific SIMD patterns not in references
- `/linux-perf-profile` — Hardware counter analysis for SIMD bottlenecks
