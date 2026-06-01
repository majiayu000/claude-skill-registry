---
name: ffi-code-review
description: "Reviews Rust FFI code for type safety, memory layout compatibility, string handling, callback patterns, and unsafe boundary correctness. Use when reviewing extern blocks, #[repr(C)] types, bindgen output, or code calling C/C++ libraries."
---

# FFI Code Review

## Review Workflow

1. **Check Cargo.toml** -- Note Rust edition (2024 has breaking changes to extern blocks and unsafe attributes), `build-dependencies` (bindgen, cc, pkg-config), `crate-type` (`cdylib`, `staticlib`), and `links` key
2. **Check build.rs** -- Verify link directives (`cargo:rustc-link-lib`, `cargo:rustc-link-search`), bindgen configuration, and C source compilation
3. **Check extern blocks** -- Verify calling conventions, symbol declarations, and safety annotations
4. **Check type layout** -- Every type crossing FFI must be `#[repr(C)]` or a primitive FFI type
5. **Check string and pointer handling** -- CStr/CString usage, null checks, ownership transfers
6. **Check callbacks** -- `extern "C" fn` pointers, panic safety across FFI boundary
7. **Gates** -- Complete **Gates** below before reporting; do not skip ahead on “internal verification”

## Gates

Complete in order. **Do not emit findings** until **Gate 4** passes for each issue.

**Gate 1 — Crate context (on disk)**  
**PASS when:** You opened the reviewed crate’s `Cargo.toml` (workspace member path if applicable) and recorded `edition =`, plus any of `links`, `crate-type`, or `build-dependencies` that matter for this FFI.  
**Blocks rationalization:** Edition-specific findings (`unsafe extern "C" {}`, `#[unsafe(no_mangle)]`, etc.) require this — if `edition` is not 2024, do not flag 2024-only requirements.

**Gate 2 — Linkage and binding sources**  
**PASS when:** If the crate links native code or uses bindgen/pkg-config, you opened `build.rs` (or the checked-in bindings entry point). If there is no `build.rs`, you stated that bindings are hand-written and reviewed those `extern` / `include!` sites.  
**Artifact:** At least one path you opened (e.g. `build.rs`, `src/ffi.rs`, or `OUT_DIR` bindings via `include!`).

**Gate 3 — Code evidence**  
**PASS when:** Every planned finding has a target `[FILE:LINE]` from a full function/block you read, not only diff hunks or partial snippets.

**Gate 4 — Pre-report protocol**  
**PASS when:** You loaded and applied the [review-verification-protocol](../review-verification-protocol/SKILL.md) skill, including **FFI-Specific Verification** for `repr(C)`, safety comments, ownership/callbacks, or bindgen-heavy code.

## Output Format

Report findings as:

```text
[FILE:LINE] ISSUE_TITLE
Severity: Critical | Major | Minor | Informational
Description of the issue and why it matters.
```

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| C-to-Rust type mapping, repr(C) layout, enums, opaque types | [references/type-mapping.md](references/type-mapping.md) |
| Safe wrappers, ownership transfer, callbacks, build.rs, testing | [references/safety-patterns.md](references/safety-patterns.md) |

## Review Checklist

### extern Blocks and Calling Conventions
- [ ] Foreign function declarations use `extern "C"` (explicit, not bare `extern`)
- [ ] **Edition 2024**: `extern "C" {}` blocks written as `unsafe extern "C" {}`
- [ ] Functions exposed to C use `extern "C" fn` (not default Rust calling convention)
- [ ] Calling convention matches the foreign library (`"C"`, `"system"` for Win32 API)
- [ ] `#[link(name = "...")]` specifies the correct library name
- [ ] `#[link(name = "...", kind = "static")]` used when statically linking

### Symbol Management
- [ ] Exported functions use `#[no_mangle]` to preserve symbol names
- [ ] **Edition 2024**: `#[no_mangle]` written as `#[unsafe(no_mangle)]`
- [ ] **Edition 2024**: `#[export_name = "..."]` written as `#[unsafe(export_name = "...")]`
- [ ] `#[link_name = "..."]` used when Rust name differs from C symbol
- [ ] Exported items are `pub` (only public `#[no_mangle]` symbols appear in library output)

### Type Layout
- [ ] Every struct/union crossing FFI has `#[repr(C)]` -- Rust's default layout is undefined
- [ ] Primitive types use `std::ffi` / `std::os::raw` equivalents (`c_int`, `c_char`, `c_void`)
- [ ] No bare `i32` where C uses `int` -- use `c_int` (width varies by platform)
- [ ] Quirky C types like `__be32` use byte arrays (`[u8; 4]`), not Rust integers
- [ ] Enums crossing FFI use `#[repr(C)]` or `#[repr(u8)]`/`#[repr(u32)]` with explicit discriminants
- [ ] C-style bitflag enums use a newtype around an integer (or `bitflags` crate), not a Rust enum
- [ ] `#[non_exhaustive]` on enums representing C enumerations that may gain new values

### String Handling
- [ ] C strings use `CStr` (borrowed) or `CString` (owned), never `&str` or `String`
- [ ] `CString::new()` result is checked for interior null bytes (returns `Err` on `\0`)
- [ ] `CString` outlives any `*const c_char` pointer derived from it via `.as_ptr()`
- [ ] Incoming `*const c_char` validated with `CStr::from_ptr()` inside `unsafe`
- [ ] No assumption that C strings are valid UTF-8 -- use `to_str()` which returns `Result`
- [ ] OS paths use `OsStr`/`OsString` and `CStr`, not `&str`

### Ownership and Allocation
- [ ] Clear ownership contract: who allocates, who frees
- [ ] Rust-allocated memory freed by Rust (`Box::from_raw`), C-allocated freed by C
- [ ] `Box::into_raw` / `Box::from_raw` paired correctly for heap transfers
- [ ] `Vec::into_raw_parts` used when passing arrays to C (pointer + length + capacity)
- [ ] Destructor functions exposed for every opaque Rust type given to C
- [ ] No `Drop` running on C-allocated memory (and vice versa)

### Callbacks
- [ ] Callback types are `extern "C" fn(...)`, not closures or `fn(...)`
- [ ] Callbacks use `std::panic::catch_unwind` to prevent panics from unwinding across FFI
- [ ] Callback context passed as `*mut c_void` with safe reconstruction at call site
- [ ] `Option<extern "C" fn(...)>` used for nullable function pointers (niche optimization)

### Bindgen and Build Scripts
- [ ] Bindgen output reviewed for correctness (auto-generated types may need adjustment)
- [ ] `-sys` crate pattern used for raw bindings, separate crate for safe wrappers
- [ ] `build.rs` uses `cargo:rustc-link-lib` and `cargo:rustc-link-search` correctly
- [ ] `links` key in `Cargo.toml` prevents duplicate linking of the same native library
- [ ] Platform-specific bindings generated per-build (not checked in for a single platform)

### Safety Documentation
- [ ] Every `unsafe` block has a `// SAFETY:` comment explaining invariants
- [ ] Every public FFI wrapper function documents safety requirements
- [ ] **Edition 2024**: `unsafe fn` bodies use explicit `unsafe {}` blocks around unsafe ops

## Severity Calibration

### Critical (Block Merge)
- Missing `#[repr(C)]` on types crossing FFI boundary (undefined memory layout)
- Wrong string handling: `&str`/`String` where `CStr`/`CString` required
- Ownership confusion: freeing C-allocated memory with Rust's allocator (or vice versa)
- Panic unwinding across FFI boundary without `catch_unwind`
- Using Rust enum for C bitflags (invalid discriminant = undefined behavior)
- Passing closure where `extern "C" fn` pointer required

### Major (Should Fix)
- Missing safety documentation on `unsafe` blocks or public FFI functions
- No null pointer check on incoming `*const T` / `*mut T` before dereferencing
- `CString` dropped before its pointer is used by C (dangling pointer)
- Missing `#[link(name = "...")]` causing link failures on some platforms
- **Edition 2024**: `extern` block not marked `unsafe extern`
- **Edition 2024**: `#[no_mangle]` not wrapped in `#[unsafe(...)]`

### Minor (Consider Fixing)
- Using `i32` instead of `c_int` for C `int` (correct on most platforms but not portable)
- Missing `#[non_exhaustive]` on enums mapping to extensible C enumerations
- Verbose manual bindings where bindgen would be more maintainable
- Checked-in bindings without platform guards

### Informational
- Suggestions to split raw bindings into a `-sys` crate
- Suggestions to add opaque wrapper types for distinct `*mut c_void` pointers
- Suggestions to use `Option<NonNull<T>>` for nullable pointers

## Valid Patterns (Do NOT Flag)

- **`unsafe extern "C" {}` in edition 2024** -- correct form for foreign declarations
- **`#[unsafe(no_mangle)]` in edition 2024** -- correct form for symbol export
- **`Option<extern "C" fn(...)>` for nullable callbacks** -- niche optimization guaranteed
- **`Option<NonNull<T>>` for nullable pointers** -- zero-cost nullable pointer pattern
- **`*mut c_void` for opaque C types** -- standard when internal layout is irrelevant
- **Distinct empty structs wrapping `c_void` for type-safe opaque pointers** -- prevents pointer confusion
- **`CStr::from_bytes_with_nul_unchecked` with compile-time literal** -- safe when literal is known null-terminated
- **`extern "C-unwind"` for controlled unwinding** -- valid per RFC 2945
- **`include!(concat!(env!("OUT_DIR"), "/bindings.rs"))` in bindgen crates** -- standard pattern
- **`Box::into_raw` / `Box::from_raw` pairs for ownership transfer** -- correct pattern when paired

## Before Submitting Findings

Complete **Gates 1-4 in order** before reporting any issue; Gate 4 incorporates the [review-verification-protocol](../review-verification-protocol/SKILL.md) skill.
