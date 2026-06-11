---
name: rust-ub-risk-audit
description: |-
  Use when auditing Rust UB risks in unsafe, FFI, raw pointers, layout, or concurrency.
  Triggers:
practices:
- secure-coding
- defense-in-depth
hexagonal_role: supporting
consumes:
- rust-source
- cargo-metadata
- ffi-contracts
- test-results
produces:
- ub-risk-audit-report
- unsafe-inventory
context_rel: []
skill_api_version: 1
user-invocable: false
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: judgment
  stability: experimental
  external_dependencies:
  - rust-toolchain
  - cargo
output_contract: "A Rust UB risk audit report with unsafe/FFI inventory, risk-ranked findings, evidence, recommended fixes, and verification commands or gaps."
---

# Rust UB Risk Audit - make unsafe assumptions explicit

Use this skill to review Rust code for undefined behavior risk at the points
where the compiler cannot enforce the full contract: `unsafe` code, FFI, raw
pointers, aliasing, layout assumptions, lifetime extension, concurrency, and
dependency boundaries. The goal is not to prove the program safe. The goal is to
produce a precise inventory, identify broken or undocumented safety contracts,
and leave the project with fixes and verification steps that match the actual
risk.

## Critical Constraints

- Treat every `unsafe` use as a contract with evidence, not as a style issue.
- Do not clear a risk because the code "looks normal"; tie the verdict to an
  invariant, a caller guarantee, a test result, or a narrower refactor.
- Keep static reasoning and dynamic tool results separate. Miri, sanitizers,
  fuzzing, and tests can expose defects, but passing them does not prove that
  every aliasing, lifetime, or FFI contract is valid.
- Prefer reducing the unsafe surface before adding comments. A smaller unsafe
  block with checked inputs is stronger than a paragraph explaining why a wide
  unsafe region should be okay.
- Report uncertainty as an audit gap. Unknown ABI ownership, missing header
  contracts, untested feature flags, or unreviewed native libraries are findings
  when they can change safety.

## When To Use

Use this skill for:

- Reviewing unsafe Rust blocks, unsafe functions, unsafe traits, or unsafe impls.
- Auditing FFI boundaries, exported C ABI functions, callbacks, and native
  library wrappers.
- Investigating raw pointer dereferences, pointer casts, transmute, packed
  fields, unions, `MaybeUninit`, `ManuallyDrop`, or layout-sensitive code.
- Checking `Send`, `Sync`, `Unpin`, pinning, atomics, locks, and interior
  mutability where unsoundness can become a data race or invalid reference.
- Reviewing dependency boundaries where a crate imports unsafe abstractions,
  generated bindings, native code, or feature-dependent behavior.

Do not use this skill as a general Rust lint pass. If no unsafe, FFI, layout,
or concurrency boundary exists, say that and limit the report to the evidence
that established the low-risk scope.

## Inputs To Gather

Inspect only the repository and artifacts relevant to the requested audit:

- Rust source, build scripts, generated bindings, examples, and tests.
- `Cargo.toml`, `Cargo.lock`, workspace configuration, feature flags, and target
  cfg gates.
- FFI headers, bindgen configuration, native build scripts, and wrapper docs.
- Existing safety comments, design notes, issue history, and prior crash reports
  when they are in scope for the task.
- CI, sanitizer, Miri, fuzzing, Loom, or stress-test outputs if already present.

If generated code is committed, audit the committed surface and identify the
generator and source contract. If generated code is not committed, audit the
generation command and the checked-in input that drives it.

## Quick Start

1. Define the audit boundary: crate, workspace, module, feature set, platform,
   and whether dependencies or native libraries are in scope.
2. Build an unsafe inventory with file paths, symbols, and risk categories.
3. For each unsafe boundary, write the safety contract in plain language:
   preconditions, ownership, aliasing, lifetimes, layout, threading, panic or
   unwind behavior, and caller obligations.
4. Compare the contract to the code that establishes it. Mark missing checks,
   invalid assumptions, and undocumented caller requirements.
5. Run targeted verification commands where available. Record skipped commands
   with the reason.
6. Deliver a risk-ranked report with evidence, fixes, and residual gaps.

## Inventory Commands

Use commands like these from the repository root, adjusting for workspace shape:

```bash
rg -n "\bunsafe\b|extern \"|#\[no_mangle\]|#\[export_name|repr\(|transmute|from_raw|into_raw|MaybeUninit|ManuallyDrop|UnsafeCell|NonNull|Send|Sync" .
cargo metadata --format-version 1 --no-deps
cargo tree -e features
```

If the repository has multiple crates or generated output, record which paths
were included and which were excluded. Do not let a broad `rg` result replace
manual review; it is only an index.

## Audit Procedure

### 1. Scope The Boundary

State the exact audit target before judging findings:

- Workspace member or crate name.
- Cargo features and target triples that change unsafe code paths.
- Public API, internal API, FFI boundary, or dependency boundary.
- Whether native libraries, generated bindings, proc macros, or build scripts
  are in scope.
- Verification commands that can run in the current environment.

If scope is ambiguous, choose the smallest defensible boundary and name what
remains unaudited.

### 2. Build The Unsafe Inventory

Capture each relevant item:

- `unsafe fn`, unsafe block, unsafe trait, unsafe impl, and extern block.
- Raw pointer creation, cast, arithmetic, dereference, or conversion into a
  reference.
- Ownership transfer through `Box::from_raw`, `Vec::from_raw_parts`,
  `CString::from_raw`, handles, descriptors, and custom allocators.
- Layout-sensitive code using `repr(C)`, `repr(transparent)`, `repr(packed)`,
  unions, discriminants, transmute, or byte casting.
- Initialization and drop-sensitive code using `MaybeUninit`, `ManuallyDrop`,
  `mem::zeroed`, `ptr::read`, `ptr::write`, or `drop_in_place`.
- Concurrency-sensitive code using `UnsafeCell`, atomics, lock-free structures,
  callback threads, unsafe `Send`, or unsafe `Sync`.

For each item, assign one or more categories: FFI, aliasing, lifetime, layout,
initialization, drop, concurrency, dependency, or public API contract.

### 3. Write The Safety Contract

Every unsafe boundary needs an explicit contract. Record:

- What the caller must guarantee before entering the boundary.
- What the boundary validates itself before executing unsafe operations.
- Which pointer ranges are valid, aligned, initialized, and non-null.
- Whether unique or shared access exists, and what prevents incompatible aliases.
- How long references, buffers, callbacks, and handles remain valid.
- Which thread may call it and which thread may drop returned values.
- What happens on panic, error, cancellation, partial initialization, and drop.
- Which representation, endianness, and ABI assumptions must hold.

Missing contracts are findings when callers cannot infer the requirements from
types alone.

### 4. Check Pointer Aliasing And Lifetimes

Look for these failure modes:

- A mutable reference exists while another live reference or raw pointer can
  observe the same memory in an incompatible way.
- A raw pointer is converted to a reference without proving alignment,
  initialization, non-nullness, and valid lifetime.
- Slices are built from pointer and length pairs without checking allocation
  provenance, length overflow, or element initialization.
- References are stored beyond the lifetime of the source object, callback,
  temporary, stack frame, or foreign allocation.
- Pinned data can move after a self-reference, intrusive link, or external
  pointer observes its address.
- Drop order invalidates memory while another value still points into it.

Prefer fixes that move checks before unsafe operations and keep references
short-lived.

### 5. Check FFI Boundaries

For each imported or exported function, review:

- ABI string, symbol name, calling convention, target cfg, and link attributes.
- Ownership transfer for pointers, strings, slices, handles, and buffers.
- Nullability, alignment, length units, terminators, and encoding.
- Allocation and deallocation pairing across language or library boundaries.
- Error reporting, errno-like state, sentinel values, and partial writes.
- Callback lifetime, reentrancy, thread affinity, and user data pointers.
- Panic and unwind behavior across the boundary.
- Header or upstream contract drift, especially when bindings are generated.

Use wrapper types to encode ownership and lifetime when possible. Keep raw FFI
types at the edge and convert into checked Rust types before wider use.

### 6. Check Layout And Initialization Assumptions

Review each layout-dependent operation:

- `repr(C)` and `repr(transparent)` match the external contract they claim.
- `repr(packed)` fields are not borrowed in a way that creates unaligned
  references.
- Transmute and byte-casting preserve validity, alignment, size, and inhabited
  value constraints.
- Zeroed memory is valid for the type being created.
- `MaybeUninit` paths initialize every field before assume-init and correctly
  drop only initialized fields on error.
- Unions and discriminants are guarded by a tag or external invariant.
- Endianness and pointer-width assumptions are explicit when data crosses
  process, file, or network boundaries.

When a layout assumption exists only in a comment, prefer a compile-time check,
type wrapper, or test that fails when the assumption changes.

### 7. Check Concurrency And Interior Mutability

Focus on places where Rust's normal sharing rules are bypassed:

- Unsafe `Send` and unsafe `Sync` impls have a type-level invariant that holds
  for all fields and all feature combinations.
- `UnsafeCell` access is synchronized or constrained so incompatible access
  cannot happen concurrently.
- Atomics use orderings that match the data dependency being protected.
- Lock-free structures handle reclamation, ABA risk, and destructor timing.
- Foreign callbacks do not race with Rust drops, shutdown, or reconfiguration.
- Thread-local state and global mutable state are initialized and torn down in a
  defined order.

Flag "works under this scheduler" arguments unless the code has a deterministic
ownership, synchronization, or state-machine reason.

### 8. Check Dependency Boundaries

Dependencies can import safety contracts that the local crate must uphold:

- Crates that expose unsafe APIs, FFI bindings, native build steps, or feature
  gates that change representation or threading behavior.
- Wrapper crates whose safety depends on an upstream C library version.
- Byte-casting, serialization, memory-map, SIMD, allocator, async runtime, or
  lock-free crates used near unsafe boundaries.
- Public APIs that pass local types into dependency unsafe functions.

Record whether the local crate validates the dependency's preconditions or
delegates them to callers. If dependency behavior is version-sensitive, cite the
checked version from `Cargo.lock` or mark the version unknown.

### 9. Run Targeted Verification

Choose checks that fit the risk surface and repository support:

```bash
cargo test --workspace --all-features
cargo test --workspace --no-default-features
cargo miri test
RUSTFLAGS="-Z sanitizer=address" cargo +nightly test --target x86_64-unknown-linux-gnu
```

Only run nightly, Miri, sanitizer, fuzzing, or model-checking commands when the
toolchain and target make sense. If a command cannot run, include the attempted
command and the blocker in the report.

## Finding Severity

Use severity to communicate fix order:

- Critical: a reachable path can create invalid references, data races, invalid
  drops, cross-ABI unwind, or memory corruption with plausible inputs.
- High: the safety contract is likely violated for a supported API, feature, or
  platform, even if a concrete crash was not reproduced.
- Medium: a contract is under-specified or insufficiently checked, and misuse is
  plausible from local callers or documented public APIs.
- Low: hardening, documentation, or tests would reduce future risk, but current
  code has a credible invariant.
- Info: inventory, tool output, or scope notes without an immediate defect.

Do not downgrade a finding because a tool did not reproduce it. Downgrade only
when the code or type system establishes the missing invariant.

## Output Specification

Return a concise audit report:

1. Scope and environment: crate, features, platform assumptions, commands run.
2. Unsafe inventory: table or bullets grouped by file and category.
3. Findings: severity, location, risk, evidence, recommended fix, and
   verification step.
4. Clean areas: boundaries reviewed with no issue found and why.
5. Gaps: skipped paths, missing contracts, unavailable tools, or dependencies
   not audited.

For each finding, include enough local evidence for a maintainer to reproduce
the reasoning without rereading the whole audit.

## Review Checklist

Before finishing, verify:

- Every unsafe block, unsafe function, unsafe trait, unsafe impl, and extern
  boundary in scope appears in the inventory.
- Pointer dereferences have alignment, initialization, provenance, bounds, and
  lifetime evidence.
- Aliasing and lifetime assumptions are enforced by types, checks, or a narrow
  unsafe contract.
- FFI ownership, nullability, allocation pairing, callbacks, and unwind behavior
  are explicit.
- Layout assumptions have a representation guarantee or a failing check.
- Concurrency invariants cover unsafe `Send`, unsafe `Sync`, atomics, shared
  mutable state, and foreign callbacks.
- Dependency safety contracts are either locally validated or deliberately
  delegated with documented caller obligations.
- Verification commands and blockers are recorded accurately.
