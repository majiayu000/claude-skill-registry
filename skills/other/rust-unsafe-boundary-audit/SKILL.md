---
name: rust-unsafe-boundary-audit
description: |-
  Use when auditing Rust unsafe blocks and FFI boundaries, invariants, tests, and tooling.
  Triggers:
practices:
- secure-by-design
- defense-in-depth
- docs-as-code
hexagonal_role: supporting
consumes:
- rust-source
- ffi-bindings
- test-results
produces:
- unsafe-boundary-audit
- safety-invariant-inventory
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
  tier: library
  stability: experimental
  dependencies: []
output_contract: "A Rust unsafe and FFI boundary audit that inventories unsafe surfaces, names invariants, identifies surface-reduction fixes, and records test/tool evidence plus residual risk."
---

# Rust Unsafe Boundary Audit - make every unsafe edge small, named, and tested

Use this skill when a Rust change, crate, or repository needs a focused audit of
`unsafe` blocks, raw pointer handling, layout assumptions, or foreign-function
boundaries. The goal is not to forbid unsafe code; it is to make each unsafe
operation local, justified, mechanically guarded where possible, and covered by
tests or tooling that exercise the contract.

## Critical Constraints

- Treat every `unsafe` block as a proof obligation. The audit must state the
  invariant that makes the operation sound, who must uphold it, and how the code
  prevents invalid callers from reaching the operation.
- FFI boundaries must document ownership, lifetime, nullability, threading,
  allocator, layout, and panic/unwind behavior. Missing contract text is a
  finding even when the implementation looks correct.
- Prefer shrinking the unsafe surface before adding comments. Safe wrappers,
  typed handles, length-checked slices, and sealed modules are stronger than
  broad caller obligations.
- Do not approve unsafe code from tool output alone. Tooling is evidence, not a
  substitute for checking aliasing, initialization, provenance, and lifetime
  assumptions in the source.
- Keep findings behavior-specific. A useful finding names the exact operation,
  the invariant that can fail, a realistic failure mode, and the smallest
  corrective action.

## Read Before Auditing

Inspect only the project under review and its in-repo contracts:

- `Cargo.toml`, workspace layout, feature flags, build scripts, and target
  configuration that can change unsafe behavior.
- Modules containing `unsafe`, `extern`, `repr(C)`, raw pointers, manual
  allocation, inline assembly, generated bindings, or platform-specific code.
- Public APIs that wrap unsafe internals, especially APIs accepting pointers,
  file descriptors, handles, lengths, callbacks, or ownership transfer.
- Tests, fuzz targets, Miri configuration, sanitizer jobs, Clippy settings, and
  CI workflows that claim to validate unsafe contracts.
- Existing safety comments, architecture notes, FFI headers, C ABI docs, and
  generated binding metadata.

If generated bindings are present, audit the handwritten boundary that calls
them. Do not spend the main review on generated code unless the generation
options or wrapper policy are part of the risk.

## Boundary Inventory

Build a concise inventory before judging individual sites. Search broadly, then
deduplicate by boundary:

```sh
rg -n '\bunsafe\b|extern[[:space:]]+"C"|no_mangle|export_name|repr\(C\)|repr\(transparent\)|from_raw|into_raw|as_ptr|as_mut_ptr|NonNull|MaybeUninit|ManuallyDrop|transmute|slice::from_raw_parts|CStr::from_ptr|CString::from_raw|libc::|windows_sys::|asm!' .
```

For each boundary, record:

| Field | What to capture |
| --- | --- |
| Site | File, function, and public entry path. |
| Operation | The unsafe action: dereference, slice construction, FFI call, layout cast, allocation transfer, callback, concurrency primitive, or assembly. |
| Required invariant | The condition that must be true for soundness. |
| Enforcer | Type system, checked wrapper, runtime guard, caller contract, external library, or none. |
| Evidence | Unit test, property test, fuzz target, Miri run, sanitizer run, platform CI, or manual reasoning. |
| Verdict | Pass, fix required, needs owner decision, or out of scope. |

Group repeated unsafe blocks behind the same abstraction. The audit should make
the module's boundary shape clear, not bury the reader in duplicate line items.

## Safety Invariant Checks

For each inventory item, test the contract against these questions.

Pointer and slice validity:

- Can null pointers, dangling pointers, unaligned pointers, or incorrect lengths
  reach the unsafe operation?
- Is provenance preserved when converting through integers, byte buffers, or
  foreign handles?
- Are zero-length slices handled without requiring a non-null data pointer where
  Rust requires one?

Aliasing and mutability:

- Can `&mut T` or mutable slices alias any other live reference?
- Does interior mutability use the right primitive and document synchronization
  or single-thread assumptions?
- Are `Send` and `Sync` implementations justified by the data they protect, not
  by the absence of compiler errors?

Initialization, layout, and drop:

- Is every byte read from initialized memory?
- Are `repr(C)` and `repr(transparent)` assumptions matched to the actual ABI
  requirement?
- Are `MaybeUninit`, `ManuallyDrop`, `ptr::read`, and `ptr::write` paired with a
  clear drop story for success and failure paths?

Lifetime and ownership:

- Does any pointer, callback, or handle outlive the Rust value it depends on?
- Is ownership transfer across FFI one-way and paired with the correct release
  function?
- Are borrowed buffers protected from mutation or deallocation by the foreign
  side while Rust references exist?

FFI and ABI behavior:

- Are nullability, length units, string encoding, struct packing, and enum values
  stated at the boundary?
- Can a Rust panic or foreign exception cross an ABI that does not permit
  unwinding?
- Does the code use the same allocator family for allocation and release?
- Are callbacks reentrant, thread-safe, and cancellation-safe according to the
  contract?

Integer and platform assumptions:

- Are pointer-sized values, signedness, truncation, endian behavior, and
  alignment different on supported targets?
- Do feature flags or target-specific modules bypass guards used on the primary
  platform?

## Surface Reduction Procedure

When a boundary fails, prefer fixes in this order:

1. Encode the invariant in a safe type: non-zero length, owned handle, checked
   pointer wrapper, lifetime-bearing reference, or enum with valid variants.
2. Move the unsafe operation into the smallest private function that can check
   its inputs immediately before the operation.
3. Replace caller promises with runtime validation where validation is cheap and
   complete.
4. Split construction from use so invalid states cannot be represented after
   initialization.
5. Add a `SAFETY:` comment beside the unsafe block that names the invariant and
   points to the guard that enforces it.
6. If the invariant cannot be encoded or checked, document the public `unsafe`
   API contract and require call-site evidence for every caller.

Reject broad module-level safety comments that do not tie a specific unsafe
operation to specific guards. A reader should be able to stand on the unsafe
line and see why it is sound.

## Validation Evidence

Match checks to the risk instead of running a generic omnibus gate:

- `cargo test` for normal behavior and regression coverage.
- `cargo test --all-features` when feature flags alter unsafe paths.
- `cargo miri test` for undefined-behavior-sensitive code when the crate and
  dependencies support Miri.
- Address, leak, or thread sanitizers for pointer lifetime, allocation, and data
  race risks on targets where those checks are available.
- Fuzz or property tests for parsers, length arithmetic, byte decoding, and FFI
  input adapters.
- ABI/layout assertions for `repr(C)` structs, exported symbols, and handles
  consumed outside Rust.
- Negative tests for rejected null pointers, invalid lengths, double-free
  attempts, callback misuse, panic containment, and mismatched ownership.

Record commands exactly as run, the platform, important feature flags, and any
tests that were skipped. If a tool cannot run, say why and compensate with a
targeted source review or narrower test.

## Report Shape

Produce a short audit report in this order:

1. Scope: crate, modules, commit range, target platforms, and excluded areas.
2. Unsafe inventory: grouped boundary table with invariant and enforcer columns.
3. Findings: severity, file/function, failed invariant, failure mode, fix.
4. Surface-reduction plan: concrete wrappers, type changes, module moves, or
   call-site contract changes.
5. Validation evidence: commands run, results, platform, skipped checks, and why.
6. Residual risk: assumptions that still depend on callers, foreign code,
   platform ABIs, generated bindings, or unavailable tooling.
7. Verdict: pass, pass with follow-up, block until fixed, or needs owner
   decision.

## Finding Standards

A finding is actionable when it includes:

- The exact unsafe operation or FFI edge.
- The invariant that is missing, unenforced, or contradicted by the code.
- A plausible path from safe or external input to undefined behavior, memory
  corruption, data race, leak, panic across FFI, or ABI mismatch.
- The narrowest fix that removes or encodes the unsafe obligation.
- The test or tooling evidence that should prove the fix.

Avoid findings that only say "unsafe code exists" or "add more tests." The
audit exists to prove or improve the boundary, not to count unsafe keywords.

## Quality Rubric

The audit passes when all hold:

- Every unsafe boundary has a named invariant and an identified enforcer.
- Public safe APIs cannot trigger undefined behavior by passing ordinary invalid
  input.
- Public unsafe APIs state caller obligations in Rust terms and, for FFI, ABI
  terms.
- The unsafe surface is private and minimal unless public unsafe is essential to
  the crate's purpose.
- Validation evidence targets the specific invariants under review.
- Residual risk is explicit enough for maintainers to accept, schedule, or block.
