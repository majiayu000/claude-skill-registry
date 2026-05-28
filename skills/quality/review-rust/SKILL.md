---
description: Comprehensive Rust code review with optional parallel agents
name: review-rust
disable-model-invocation: true
---

# Rust Code Review

## Arguments

- `--parallel`: Spawn specialized subagents per technology area
- Path: Target directory (default: current working directory)

## Hard gates

Complete in order before writing **Issues** in the output (empty scope is allowed; fabricated findings are not).

1. **Scope gate:** You have an explicit list of `.rs` paths under review (from Step 1 or the user-provided path). **Pass:** List printed or "No Rust files in scope" — then stop with no Issues.
2. **Compiler/linter gate:** Step 3 commands were run from the crate or workspace root (`Cargo.toml` present); if they cannot run, one line states why (e.g. missing toolchain, no `Cargo.toml`, sandbox). **Pass:** You do not report a problem already shown as an error/warning in Step 3 output, and you do not duplicate compiler or clippy diagnostics the author must fix first.
3. **Protocol gate:** `beagle-rust:review-verification-protocol` is loaded before Step 7. **Pass:** Every Critical/Major finding satisfies Step 8 (and the protocol); if there are zero findings, say "Protocol applied; no issues" in the Review Summary.
4. **Evidence gate (Critical/Major):** For each Critical or Major item, you re-read the file at `FILE:LINE` with full surrounding context (not only the diff hunk). **Pass:** The Issue description matches observable code at that location.

## Step 1: Identify Changed Files

```bash
git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E '\.rs$'
```

## Step 2: Check Rust Edition and MSRV

```bash
# Check Cargo.toml for edition and rust-version
grep -E 'edition|rust-version' Cargo.toml

# Check workspace members if workspace
grep -A 20 '\[workspace\]' Cargo.toml
```

**Edition 2024 awareness** (requires MSRV 1.85+):

If `edition = "2024"` is detected, the following behavioral changes apply throughout the review:
- `unsafe_op_in_unsafe_fn` is deny by default — unsafe operations inside `unsafe fn` MUST use explicit `unsafe {}` blocks
- `extern "C" {}` blocks must be `unsafe extern "C" {}`
- `#[no_mangle]` and `#[export_name]` must be `#[unsafe(no_mangle)]` and `#[unsafe(export_name)]`
- `-> impl Trait` captures ALL in-scope lifetimes by default (RPIT lifetime capture change); use `+ use<'a>` for precise capture
- `gen` is a reserved keyword — code using it as an identifier must use `r#gen`
- `!` (never type) falls back to `!` instead of `()` — may change behavior of inferred types
- Temporaries in `if let` conditions and tail expressions are dropped earlier than in edition 2021
- `Box<[T]>` now implements `IntoIterator`

Record the detected edition — it affects severity calibration in Steps 3, 8, and the verification protocol.

## Step 3: Verify Linter Status

CRITICAL: Run clippy and check BEFORE flagging style or correctness issues. Do NOT flag issues that clippy or the compiler already catches.

```bash
cargo clippy --all-targets --all-features -- -D warnings 2>&1 | head -50
cargo clippy -- -D clippy::perf 2>&1 | head -20
cargo check --all-targets 2>&1 | head -50
```

**Edition 2024 note:** Edition 2024 promotes several previously-warn lints to deny (notably `unsafe_op_in_unsafe_fn`). If clippy or `cargo check` already reports edition-related errors, do not duplicate those as review findings — instead note that the author must fix compiler errors first.

## Step 4: Detect Technologies

```bash
# Detect tokio async runtime
grep -r "tokio" --include="Cargo.toml" -l | head -3

# Detect axum web framework
grep -r "axum" --include="Cargo.toml" -l | head -3

# Detect sqlx database
grep -r "sqlx" --include="Cargo.toml" -l | head -3

# Detect serde serialization
grep -r "serde" --include="Cargo.toml" -l | head -3

# Detect thiserror / anyhow
grep -r "thiserror\|anyhow" --include="Cargo.toml" -l | head -3

# Detect tracing
grep -r "tracing" --include="Cargo.toml" -l | head -3

# Check for test files in diff
git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E '((^|/)(test|tests)/.*\.rs$)|(_test\.rs$)'

# Check for unsafe code in diff
git diff $(git merge-base HEAD main)..HEAD -- '*.rs' | grep -c 'unsafe'

# Detect async fn in traits (no async-trait crate needed since Rust 1.75)
grep -r "async-trait" --include="Cargo.toml" -l | head -3

# Detect LazyLock/LazyCell usage (replaces once_cell/lazy_static since 1.80)
grep -r "once_cell\|lazy_static" --include="Cargo.toml" -l | head -3

# Detect #[expect] lint attribute usage (stable since 1.81)
git diff $(git merge-base HEAD main)..HEAD -- '*.rs' | grep -c '#\[expect('

# Detect macro definitions in diff
git diff $(git merge-base HEAD main)..HEAD -- '*.rs' | grep -cE 'macro_rules!|#\[proc_macro|#\[derive\('

# Detect FFI code in diff
git diff $(git merge-base HEAD main)..HEAD -- '*.rs' | grep -cE 'extern "C"|#\[no_mangle\]|#\[repr\(C\)\]|bindgen|#\[unsafe\(no_mangle\)\]'

# Detect concurrency primitives (atomics, lock-free, hand-rolled sync)
git diff $(git merge-base HEAD main)..HEAD -- '*.rs' | grep -cE 'std::sync::atomic|Atomic(Bool|U?size|U?(8|16|32|64)|Ptr)|compare_exchange|fetch_(add|sub|or|and|xor|update)|UnsafeCell|unsafe impl (Send|Sync)|Ordering::(Relaxed|Acquire|Release|AcqRel|SeqCst)|atomic::fence'

# Detect concurrency test tooling
grep -rE 'loom|^miri$' --include='Cargo.toml' -l | head -3
git diff $(git merge-base HEAD main)..HEAD -- '*.rs' | grep -cE 'loom::|#\[cfg\(loom\)\]|cfg_attr\(miri'

# Detect concurrency crates
grep -rE '^crossbeam|^arc-swap|^parking_lot|^dashmap|^flurry|^haphazard|^seize|^atomic_wait' --include='Cargo.toml' -l | head -3

# Detect criterion benchmarks
grep -rE '^criterion' --include='Cargo.toml' -l | head -3
ls -d benches 2>/dev/null

# Detect proc-macro crate or trybuild
grep -rE 'proc-macro\s*=\s*true|^trybuild' --include='Cargo.toml' -l | head -3

# Detect public-surface changes (interface-design.md routing)
git diff $(git merge-base HEAD main)..HEAD -- '*.rs' | grep -cE '^\+\s*pub (trait|fn|struct|enum|mod|use)|^\+\s*impl[<\s].*Drop for'

# Detect ecosystem patterns (patterns-in-the-wild.md routing)
grep -rE '^slotmap|^petgraph|^scopeguard|^indexmap' --include='Cargo.toml' -l | head -3
git diff $(git merge-base HEAD main)..HEAD -- '*.rs' | grep -cE 'mem::replace|swap_remove|prelude'
```

**Modern Rust detection notes:**
- If `async-trait` is a dependency but the project uses edition 2024 or MSRV >= 1.75, flag as Informational — native `async fn` in traits is available and `async-trait` can likely be removed.
- If `once_cell` or `lazy_static` is a dependency but MSRV >= 1.80, flag as Informational — `std::sync::LazyLock` and `std::cell::LazyCell` are stable replacements.
- If `#[allow(...)]` is used where `#[expect(...)]` would be better (MSRV >= 1.81), note as Minor — `#[expect]` warns when the suppressed lint no longer fires, keeping suppressions clean.

**Concurrency detection notes:**
- If atomics (`std::sync::atomic`, `compare_exchange`, `fetch_*`), `UnsafeCell`, `unsafe impl Send/Sync`, or `crossbeam` / `arc-swap` / `parking_lot` are present in the diff, load `beagle-rust:rust-code-review` and consult `references/concurrency-primitives.md`, `references/memory-ordering.md`, and `references/lock-free-patterns.md`.
- If the diff introduces or restructures concurrency (worker pools, actor-style channels, `tokio::spawn` patterns, threads-vs-async choices), also consult `references/concurrency-models.md` for design-level review questions.
- If hand-rolled atomics / lock-free types appear with no `loom` dependency or no `cargo +nightly miri test` in CI, load `beagle-rust:rust-testing-code-review` and consult `references/concurrency-testing.md`.

**Interface design / API surface detection:**
- If the diff introduces or changes `pub trait`, `pub fn`, `pub struct`, derive impls on public types, `impl Drop` on owning types, or re-exports of foreign types, load `beagle-rust:rust-code-review` and consult `references/interface-design.md` for object-safety, ergonomic-impl, fallible-destructor, and hidden-contract review checks.
- If the diff uses index-pointer graphs (`Vec<Node> + usize`, `slotmap`, `petgraph`), `mem::replace`-style drop guards, extension traits, or modifies a `prelude` module, also consult `references/patterns-in-the-wild.md`.

**Testing detection (criterion / trybuild / clippy strategy):**
- If `benches/` directory or `criterion` dependency is present, load `beagle-rust:rust-testing-code-review` and consult `references/advanced-testing.md` for criterion baseline, `black_box`, and `iter_batched` review checks.
- If proc-macro crate (`proc-macro = true`) or `trybuild` in `[dev-dependencies]`, consult `references/advanced-testing.md` for trybuild `.stderr` stability checks plus `beagle-rust:macros-code-review` `references/procedural-macros.md` for span hygiene and `syn` feature audits.

## Step 5: Load Verification Protocol

Load `beagle-rust:review-verification-protocol` skill and keep its checklist in mind throughout the review.

## Step 6: Load Skills

Use the `Skill` tool to load each applicable skill (e.g., `Skill(skill: "beagle-rust:rust-code-review")`).

**Always load:**
- `beagle-rust:rust-code-review`

**Conditionally load based on detection:**

| Condition | Skill |
|-----------|-------|
| Tokio detected | `beagle-rust:tokio-async-code-review` |
| Axum detected | `beagle-rust:axum-code-review` |
| sqlx detected | `beagle-rust:sqlx-code-review` |
| Serde detected | `beagle-rust:serde-code-review` |
| Test files changed | `beagle-rust:rust-testing-code-review` |
| Macro definitions in diff | `beagle-rust:macros-code-review` |
| FFI code detected (extern, repr(C), bindgen) | `beagle-rust:ffi-code-review` |
| Atomics, `UnsafeCell`, `unsafe impl Send/Sync`, `compare_exchange`, `crossbeam`, `arc-swap`, `parking_lot` | `beagle-rust:rust-code-review` (load `references/concurrency-primitives.md`, `references/memory-ordering.md`, `references/lock-free-patterns.md`) |
| Concurrency design changes (worker pools, channels, threads-vs-async restructuring) | `beagle-rust:rust-code-review` (load `references/concurrency-models.md`) |
| Public trait / `pub fn` / `pub struct` / `impl Drop` / re-export changes | `beagle-rust:rust-code-review` (load `references/interface-design.md`) |
| Graph/tree code, `slotmap`, `petgraph`, `mem::replace` drop guards, extension traits, `prelude` module changes | `beagle-rust:rust-code-review` (load `references/patterns-in-the-wild.md`) |
| `criterion` benchmarks, `benches/` directory | `beagle-rust:rust-testing-code-review` (load `references/advanced-testing.md` — criterion baseline + `black_box` + `iter_batched` checks) |
| Proc-macro crate (`proc-macro = true`) or `trybuild` in dev-deps | `beagle-rust:rust-testing-code-review` + `beagle-rust:macros-code-review` (load `references/advanced-testing.md` trybuild + `references/procedural-macros.md` span hygiene) |
| `loom`, `miri`, hand-rolled lock-free code under test | `beagle-rust:rust-testing-code-review` (load `references/concurrency-testing.md`) |

## Step 7: Review

**Sequential (default):**
1. Load applicable skills
2. Review core Rust quality (ownership, error handling, unsafe, traits)
3. Review detected technology areas
4. Consolidate findings

**Parallel (--parallel flag):**
1. Detect all technologies upfront
2. Spawn one subagent per technology area with `Task` tool
3. Each agent loads its skill and reviews its domain
4. Wait for all agents
5. Consolidate findings

## Step 8: Verify Findings

Before reporting any issue:
1. Re-read the actual code (not just diff context)
2. For "unused" claims - did you search all references across the workspace?
3. For "missing" claims - did you check trait definitions, derive macros, and `#[cfg]` gated code?
4. For "unnecessary clone" - did you verify the borrow checker allows a reference?
5. For "unsafe" issues - did you check the safety comments and surrounding invariants?
6. Remove any findings that are style preferences, not actual issues

**Edition 2024 verification rules:**
7. Do NOT flag `unsafe {}` blocks inside `unsafe fn` as unnecessary — they are REQUIRED in edition 2024
8. Do NOT flag `unsafe extern "C"` as unusual syntax — it is REQUIRED in edition 2024
9. Do NOT flag `#[unsafe(no_mangle)]` or `#[unsafe(export_name)]` as unusual — they are REQUIRED in edition 2024
10. For `-> impl Trait` returns, verify whether implicit lifetime capture is intentional — in edition 2024 all in-scope lifetimes are captured by default; suggest `+ use<'a>` only when narrower capture is needed
11. For code using `Box<[T]>` in iterator contexts, remember `IntoIterator` is now available in edition 2024 — do not flag `.iter()` on boxed slices as the only approach
12. If temporaries in `if let` or tail expressions cause borrow issues, consider whether edition 2024's earlier drop semantics are the root cause

## Step 9: Review Convergence

### Single-Pass Completeness

You MUST report ALL issues across ALL categories (ownership, error handling, async, types, tests, security, performance) in a single review pass. Do not hold back issues for later rounds.

Before submitting findings, ask yourself:
- "If all my recommended fixes are applied, will I find NEW issues in the fixed code?"
- "Am I requesting new code (tests, types, modules) that will itself need review?"

If yes to either: include those anticipated downstream issues NOW, in this review, so the author can address everything at once.

### Scope Rules

- Review ONLY the code in the diff and directly related existing code
- Do NOT request new features, test infrastructure, or architectural changes that didn't exist before the diff
- If test coverage is missing, flag it as ONE Minor issue ("Missing test coverage for X, Y, Z") — do NOT specify implementation details
- Doc comments, naming issues are Minor unless they affect public API contracts
- Do NOT request adding new dependencies (e.g., proptest, mockall, criterion)

### Fix Complexity Budget

Fixes to existing code should be flagged at their real severity regardless of size.

However, requests for **net-new code that didn't exist before the diff** must be classified as Informational:
- Adding a new dependency
- Creating entirely new modules, files, or test suites
- Extracting new traits or abstractions
- Adding benchmark suites

These are improvement suggestions for the author to consider in future work, not review blockers.

### Iteration Policy

If this is a re-review after fixes were applied:
- ONLY verify that previously flagged issues were addressed correctly
- Do NOT introduce new findings unrelated to the previous review's issues
- Accept Minor/Nice-to-Have issues that weren't fixed — do not re-flag them
- The goal of re-review is VERIFICATION, not discovery

## Output Format

```markdown
## Review Summary

[1-2 sentence overview of findings]

## Issues

### Critical (Blocking)

1. [FILE:LINE] ISSUE_TITLE
   - Issue: Description of what's wrong
   - Why: Why this matters (unsound unsafe, data race, panic, security)
   - Fix: Specific recommended fix

### Major (Should Fix)

2. [FILE:LINE] ISSUE_TITLE
   - Issue: ...
   - Why: ...
   - Fix: ...

### Minor (Nice to Have)

N. [FILE:LINE] ISSUE_TITLE
   - Issue: ...
   - Why: ...
   - Fix: ...

### Informational (For Awareness)

N. [FILE:LINE] SUGGESTION_TITLE
   - Suggestion: ...
   - Rationale: ...

## Good Patterns

- [FILE:LINE] Pattern description (preserve this)

## Verdict

Ready: Yes | No | With fixes 1-N (Critical/Major only; Minor items are acceptable)
Rationale: [1-2 sentences]
```

## Rules

- Complete **Hard gates** before writing Issues
- Load skills BEFORE reviewing (not after)
- Number every issue sequentially (1, 2, 3...)
- Include FILE:LINE for each issue
- Separate Issue/Why/Fix clearly
- Categorize by actual severity
- Run clippy before flagging style issues
- Run verification after fixes
- Report ALL issues in a single pass — do not hold back findings for later iterations
- Re-reviews verify previous fixes ONLY — no new discovery
- Requests for net-new code (new modules, dependencies, test suites) are Informational, not blocking
- The Verdict ignores Minor and Informational items — only Critical and Major block approval

## Post-Fix Verification

After fixes are applied, run:

```bash
cargo check --all-targets
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-targets
```

All checks must pass before approval.
