---
name: asm-forge
description: ASM-guided deep performance optimization. Collects assembly, audits codegen quality, applies targeted transforms, validates with benchmarks. Uses cargo-show-asm + Criterion as ground truth.
user-invocable: true
---

# ASM Forge — Assembly-Guided Performance Optimization

**Philosophy: ASM and benchmarks are truth. Everything else is hypothesis.**

Every optimization starts by reading what the compiler actually emitted, identifying
where it fell short, making a targeted change, and measuring the result. No guessing,
no cargo-culting `#[inline]` annotations.

## When to Use

- Squeezing the last 5-30% out of hot functions where profiling shows the time is spent
- After `/rust-hotspot-finder` or `/rust-perf-triage` identified a hot function
- When you suspect the compiler is generating suboptimal code (bounds checks, spills, missed SIMD)
- When `/bench-compare` shows a regression and you need to understand *why* at the instruction level
- Validating that a "clever" optimization actually improved codegen

## Prerequisites

### Required

```bash
# cargo-show-asm: primary ASM inspection tool
cargo install cargo-show-asm

# Criterion benchmarks must exist for the target code
# (this project has 24+ benchmarks in benches/)
```

### Recommended

```bash
# For LLVM-IR analysis when ASM isn't enough
rustup component add llvm-tools-preview

# For instruction-level profiling on Linux
# (optional, use /linux-perf-profile skill instead)
```

### Build Configuration

Always build with debug info for source mapping, but full optimization:

```bash
RUSTFLAGS="-C target-cpu=native -C debuginfo=2" cargo build --release
```

The project's `Cargo.toml` already has `opt-level=3`, `lto="thin"`, `codegen-units=1`.

## Workflow Overview

```
/asm-forge @file.rs "focus description"
    │
    ├─ Phase 0: Recon (3 parallel subagents)
    │   ├─ Agent A: Collect ASM for target functions
    │   ├─ Agent B: Run baseline benchmarks
    │   └─ Agent C: Static hotspot analysis of target code
    │
    ├─ Phase 1: ASM Audit
    │   └─ Read assembly, classify codegen issues using references
    │
    ├─ Phase 2: Optimization Plan
    │   └─ Ranked list of source transforms with predicted ASM impact
    │
    ├─ Phase 3: Forge Loop (iterative, ONE change at a time)
    │   ├─ Apply source change
    │   ├─ Re-collect ASM → diff before/after
    │   ├─ Run benchmarks → compare against baseline
    │   └─ Accept (ASM + benchmark both improved) or revert
    │
    └─ Phase 4: Summary Report
        └─ Total improvement, ASM diffs, remaining opportunities
```

## Phase 0: Recon

Launch three parallel subagents using the Task tool:

### Agent A: ASM Collection

Use the Task tool with `subagent_type=Bash` to collect assembly:

```bash
# List available functions in a module (find exact symbol names)
cargo asm --lib -p scanner-rs 2>&1 | grep '<module_path>'

# Collect ASM for a specific function (Intel syntax, interleaved with Rust source)
cargo asm --lib -p scanner-rs --rust '<full::path::to::function>' > /tmp/asm-before.s

# For multiple functions, collect each:
cargo asm --lib -p scanner-rs '<function_1>' > /tmp/asm-before-fn1.s
cargo asm --lib -p scanner-rs '<function_2>' > /tmp/asm-before-fn2.s

# If cargo-show-asm can't find the function, list candidates:
cargo asm --lib -p scanner-rs 2>&1 | grep -i '<partial_name>'

# For LLVM-IR view (useful for understanding optimization decisions):
cargo asm --lib -p scanner-rs --llvm '<function>' > /tmp/llvm-before.ll

# For MIR view (useful for understanding Rust-level optimizations):
cargo asm --lib -p scanner-rs --mir '<function>' > /tmp/mir-before.mir
```

**ISA auto-detection**: `cargo-show-asm` emits native ISA by default:
- Apple Silicon → AArch64 instructions
- Intel Mac → x86-64 instructions
- Linux CI → depends on target (use `--target` flag for cross-compilation)

### Agent B: Benchmark Baseline

Use the Task tool with `subagent_type=Bash`:

```bash
# Save baseline for the relevant benchmarks
# Identify which bench file covers the target functions
cargo bench --bench <relevant_bench> -- --save-baseline forge-before

# For benchmarks requiring the bench feature:
cargo bench --features bench --bench <relevant_bench> -- --save-baseline forge-before
```

**Benchmark selection guide for this project:**
- `src/engine/` functions → `hotspots`, `scan`, `scanner_throughput`
- `src/engine/rule_repr.rs` → `hotspots`, `rule_isolation`, `rule_scaling`
- `src/stdx/` data structures → the corresponding bench (e.g., `ring_buffer`, `fixed_set`)
- Validation code → `validator`, `offline_validation`

### Agent C: Static Hotspot Analysis

Use the Task tool with `subagent_type=general-purpose`:

Prompt: Read the target file(s) and identify performance-relevant patterns:
- Loops with potential bounds checks
- Data dependencies that limit ILP
- Branch-heavy control flow
- Allocation/clone patterns in hot paths
- Struct layout and field access patterns
- Functions that could benefit from `#[cold]` or `#[inline(always)]`

Cross-reference with `references/forge-techniques.md` for known source→ASM mappings.

## Phase 1: ASM Audit

Once recon completes, read the collected ASM files and audit codegen quality.

**Load these references based on the target ISA:**
- Apple Silicon / AArch64 Linux → `references/aarch64-codegen.md`
- Intel Mac / x86-64 Linux → `references/x86-64-codegen.md`
- Always load → `references/asm-red-flags.md` and `references/ilp-and-microarch.md`

### What to Look For

Scan the ASM for these categories (detailed patterns in references):

**1. Panic paths in hot code** (highest priority)
```
; x86-64: look for
call  core::panicking::panic_bounds_check
call  core::panicking::panic

; AArch64: look for
bl    core::panicking::panic_bounds_check
bl    core::panicking::panic
```
These are bounds checks the compiler couldn't elide. Each one adds a branch and
cold-path code to the hot loop. Fix with `get_unchecked()` (with safety proof) or
restructure to help the compiler prove bounds.

**2. Register spills**
```
; x86-64: look for stack spills
mov   [rsp+offset], reg    ; spill to stack
mov   reg, [rsp+offset]    ; reload from stack

; AArch64: look for
str   xN, [sp, #offset]    ; spill
ldr   xN, [sp, #offset]    ; reload
```
Spills mean the compiler ran out of registers. The function is too complex for the
register allocator. Fix by splitting the function, reducing live variables, or
restructuring to reduce register pressure.

**3. Long dependency chains (ILP killers)**
Each instruction that depends on the previous one's result creates a serial chain.
The CPU can't execute them in parallel even with out-of-order execution.

Look for sequences where each instruction uses the result of the previous one:
```asm
; Bad: serial chain, ~4 cycles each = 12 cycles total
load  rax, [mem]     ; cycle 0: load
add   rax, rbx      ; cycle 4: depends on load
imul  rax, rcx      ; cycle 5: depends on add
```

Fix by restructuring to create independent operations the CPU can overlap.

**4. Missed vectorization**
If you see scalar operations on arrays where SIMD instructions exist:
```asm
; Bad: scalar loop processing one element at a time
.loop:
  movzx  eax, byte [rdi]
  ; ... process one byte ...
  inc    rdi
  cmp    rdi, rsi
  jne    .loop

; Good: SIMD processing 16/32 bytes at a time
.loop:
  vmovdqu ymm0, [rdi]      ; load 32 bytes
  ; ... process 32 bytes ...
  add     rdi, 32
  cmp     rdi, rsi
  jne     .loop
```

**5. Unnecessary memory traffic**
Values loaded from memory, used once, then reloaded instead of staying in registers.
Often caused by aliasing concerns or complex control flow.

**6. Suboptimal instruction selection**
- Division where shift works (`>> 3` instead of `/ 8`)
- Multiply where lea works (on x86-64)
- Branch where conditional move works (`cmov` on x86-64, `csel` on AArch64)

### Audit Output Format

For each issue found, record:

```markdown
### Issue N: [Category]
**Location**: instruction offset or source line (from interleaved view)
**ASM evidence**:
```asm
; the problematic instruction sequence
```
**Root cause**: Why the compiler generated this
**Proposed fix**: Source-level change to improve codegen
**Expected ASM impact**: What the improved code should look like
**Confidence**: High/Medium/Low (based on how predictable the compiler response is)
```

## Phase 2: Optimization Plan

Rank all identified issues by:

1. **Impact**: How many cycles does this cost per invocation?
   - Panic paths: 0 cycles normally (predicted correctly) but pollute icache
   - Spills: 4-7 cycles per spill+reload pair
   - Dependency chains: pipeline depth × chain length
   - Missed SIMD: Nx speedup where N = vector width / scalar width

2. **Confidence**: How predictable is the compiler's response to our change?
   - High: Removing bounds checks, adding `#[cold]`, `get_unchecked` → always works
   - Medium: Restructuring for ILP, data packing → usually works
   - Low: Hoping for auto-vectorization → compiler may not cooperate

3. **Risk**: Could this change introduce bugs?
   - `unsafe` changes need safety proofs
   - Layout changes need all access sites audited
   - Algorithmic changes need correctness tests

Present as:

```markdown
## Forge Plan

### 1. [Issue] — Expected: X% improvement, Confidence: High
Source change: [specific diff]
ASM prediction: [what should change]
Benchmark: `cargo bench --bench <name> -- '<filter>'`

### 2. [Issue] — Expected: X% improvement, Confidence: Medium
...
```

## Phase 3: Forge Loop

**Critical discipline: ONE change at a time.**

For each planned optimization:

### Step 1: Apply the Change

Make the source modification. Keep it minimal and isolated.

### Step 2: Collect New ASM

```bash
cargo asm --lib -p scanner-rs --rust '<function>' > /tmp/asm-after.s
```

### Step 3: Diff ASM

```bash
# Use the bundled diff script
bash <skill_dir>/scripts/diff_asm.sh /tmp/asm-before.s /tmp/asm-after.s
```

Or manually:
```bash
diff --color=always /tmp/asm-before.s /tmp/asm-after.s | head -100
```

Verify the ASM actually changed as predicted:
- Did the panic path disappear?
- Did register spills decrease?
- Did the dependency chain get shorter?
- Did SIMD instructions appear?

**If the ASM didn't improve as expected**: The compiler may need a different hint,
or the issue is elsewhere. Investigate before proceeding.

### Step 4: Benchmark

```bash
cargo bench --bench <relevant_bench> -- --baseline forge-before '<filter>'

# For bench-feature benchmarks:
cargo bench --features bench --bench <relevant_bench> -- --baseline forge-before '<filter>'
```

### Step 5: Accept or Revert

| ASM improved? | Benchmark improved? | Action |
|:---:|:---:|---|
| Yes | Yes | **Accept**. Update baseline: `cargo bench --bench <name> -- --save-baseline forge-before` |
| Yes | No | Investigate. ASM looks better but real workload didn't benefit. Bottleneck is elsewhere. Consider reverting. |
| No | Yes | Suspicious. Measurement noise? Re-run with more iterations. |
| No | No | **Revert immediately**. `git checkout -- <file>` |

### Iteration

After accepting a change:
1. Update the ASM baseline files (`/tmp/asm-before-*.s`)
2. Update the benchmark baseline
3. Move to the next optimization in the plan
4. Repeat until all planned optimizations are evaluated

## Phase 4: Summary Report

After completing the forge loop, produce:

```markdown
## ASM Forge Report: [target]

### Environment
- ISA: [AArch64 / x86-64]
- CPU: [Apple M3 / Intel i9 / Graviton3 / etc.]
- Build: `opt-level=3, lto=thin, codegen-units=1, target-cpu=native`
- Rust: [rustc version]

### Changes Applied

| # | Optimization | ASM Impact | Benchmark Impact | Status |
|---|---|---|---|---|
| 1 | Elided bounds check in inner loop | -2 branches, -1 panic path | -8.3% latency | Accepted |
| 2 | Restructured for ILP (2 independent chains) | +4 parallel ops | -12.1% latency | Accepted |
| 3 | Packed struct from 48→32 bytes | -2 cache lines per iter | -3.2% latency | Accepted |
| 4 | Attempted SIMD for byte scan | No vectorization emitted | No change | Reverted |

### Aggregate Improvement

| Benchmark | Before | After | Delta |
|---|---|---|---|
| hot_function | 145 ns | 112 ns | -22.8% |
| end_to_end_scan | 3.2 ms | 2.8 ms | -12.5% |

### Remaining Opportunities

[List any issues identified in Phase 1 that weren't addressed, with rationale]

### Key ASM Diffs

[Include the most instructive before/after ASM snippets for documentation]
```

## Tips

### Effective cargo-show-asm Usage

```bash
# List all functions in a module (grep for your target)
cargo asm --lib -p scanner-rs 2>&1 | grep 'rule_repr'

# Show ASM with interleaved Rust source (best for audit)
cargo asm --lib -p scanner-rs --rust 'scanner_rs::engine::rule_repr::RuleCompiled::matches'

# Show only ASM (cleaner for diffing)
cargo asm --lib -p scanner-rs 'scanner_rs::engine::rule_repr::RuleCompiled::matches'

# Show LLVM-IR (understand optimizer decisions)
cargo asm --lib -p scanner-rs --llvm 'function_name'

# Show MIR (understand Rust-level optimizations, monomorphization)
cargo asm --lib -p scanner-rs --mir 'function_name'

# When function name is ambiguous, cargo-show-asm shows candidates
# Pick the right monomorphization by examining the type parameters
```

### Rust Source Patterns That Produce Bad ASM

Load `references/forge-techniques.md` for the complete catalog. Key ones:

- **Indexing with `[]`** → bounds check + panic path. Use iterators or `get_unchecked()`.
- **Match on enum in tight loop** → branch per variant. Consider lookup table or branchless.
- **Multiple return paths** → register spills at merge points. Simplify control flow.
- **Large structs by value** → memcpy. Pass by reference or shrink the struct.
- **`Option<u32>`** → 8 bytes (niche optimization sometimes fails). Use sentinel values.

### Cross-ISA Considerations

When optimizing for both Apple Silicon and x86-64 Linux:

- **AArch64 has more registers** (31 GP + 32 SIMD vs 16 GP + 16 SIMD on x86-64).
  Spills on x86-64 may not appear on AArch64. Optimize for x86-64 first.
- **AArch64 has fixed-width instructions** (4 bytes each). Instruction count ≈ code size.
  On x86-64, instruction count != code size (variable-length encoding).
- **AArch64 conditional select (`csel`)** is free and common. x86-64 `cmov` has limitations.
  Branchless patterns may look different across ISAs.
- **SIMD differs**: AArch64 NEON is 128-bit, SVE is scalable. x86-64 SSE is 128-bit,
  AVX2 is 256-bit. Auto-vectorization width varies.
- **Always benchmark on both ISAs** when possible. An optimization that helps x86-64
  may hurt AArch64 or vice versa.

### When to Stop

Stop forging when:
- Remaining ASM issues have low expected impact (<2% per change)
- The function is dominated by unavoidable work (memory latency, I/O)
- Further optimization requires algorithmic changes (different skill: refactoring)
- You've exhausted the codegen-quality improvements and need hardware profiling
  (escalate to `/linux-perf-profile` on Linux)

## Related Skills

- `/rust-hotspot-finder` — Identifies which functions to forge (run first)
- `/rust-perf-triage` — Interprets profiling data when ASM alone isn't enough
- `/bench-compare` — Quick before/after benchmark comparison
- `/linux-perf-profile` — Hardware counter analysis on Linux (PMU, cache, TLB)
- `/perf-regression` — Full regression testing workflow before merging
- `/performance-analyzer` — Static analysis checklist for this project's patterns
