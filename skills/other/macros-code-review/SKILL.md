---
name: macros-code-review
description: "Reviews Rust macro code for hygiene issues, fragment misuse, compile-time impact, and procedural macro patterns. Use when reviewing macro_rules! definitions, procedural macros, derive macros, or attribute macros."
---

# Macros Code Review

## Review Workflow

1. **Check `Cargo.toml`** -- Note Rust edition (2024 reserves `gen` keyword, affecting macro output), proc-macro crate dependencies (`syn`, `quote`, `proc-macro2`), and feature flags (e.g., `syn` with minimal features)
2. **Check macro type** -- Determine if reviewing declarative (`macro_rules!`), function-like proc macro, attribute macro, or derive macro
3. **Check if a macro is needed** -- If the transformation is type-based, generics are better. Macros are for structural/repetitive code generation that generics cannot express
4. **Scan macro definitions** -- Read full macro bodies including all match arms, not just the invocation site
5. **Check each category** -- Work through the checklist below, loading references as needed
6. **Gates** -- Complete **Gates** below before reporting; do not substitute informal “I verified.”

## Gates (before reporting findings)

Complete in order. **Do not emit findings** until **Gate 4** passes for each issue.

**Gate 1 — Crate context (on disk)**  
**PASS when:** You opened the reviewed crate’s `Cargo.toml` (workspace member path if applicable) and recorded Rust `edition`, whether the crate is `proc-macro = true`, and relevant proc-macro dependencies or `syn` / `quote` feature flags.  
**Blocks rationalization:** Edition 2024 findings (`gen`, `unsafe extern`, generated `unsafe` bodies) and `syn` “full” vs minimal flags require this — do not flag edition-specific macro output without matching `edition` from the file.

**Gate 2 — Macro definitions read**  
**PASS when:** For every macro you critique, you read the full definition (all `macro_rules!` arms, or the proc-macro entry plus helpers you rely on), not only call sites or partial expansions.  
**Artifact:** At least one path per macro to the defining `.rs` file(s) you used.

**Gate 3 — Per-finding evidence**  
**PASS when:** Each planned issue has `[FILE:LINE]` from the current tree for the macro definition, attribute/derive site, or generated code location you are discussing (not from memory, docs-only, or another branch).

**Gate 4 — Pre-report protocol**  
**PASS when:** You loaded and applied `beagle-rust:review-verification-protocol`, including **Macro-Specific Verification** for hygiene, fragment type, and proc-macro performance claims. **Then** add findings.

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
| Fragment types, repetition, hygiene boundaries (vars vs types), `$crate` paths, TT-muncher pattern + recursion limits, fragment-matcher follow restrictions, decl-vs-proc decision tree | [references/declarative-macros.md](references/declarative-macros.md) |
| Proc macro types, syn/quote, span hygiene (`call_site` vs `def_site` vs `mixed_site`), `syn::Error::new_spanned` + combine, `parse_quote!` vs `quote!`, `syn` feature audit, trybuild UI tests | [references/procedural-macros.md](references/procedural-macros.md) |

## Review Checklist

### Declarative Macros (`macro_rules!`)

- [ ] Correct fragment types used (`:expr` vs `:tt` vs `:ident` -- wrong choice causes unexpected parsing)
- [ ] Repetition separators match intended syntax (`,` vs `;` vs none, `*` vs `+`)
- [ ] Trailing comma/semicolon handled (add `$(,)?` or `$(;)?` at end of repetition)
- [ ] Matchers ordered from most specific to least specific (first match wins)
- [ ] No ambiguous expansions -- each metavariable appears in the correct repetition depth in the transcriber
- [ ] Variables defined in the macro use macro-internal names (hygiene protects variables, not types/modules/functions)
- [ ] Exported macros (`#[macro_export]`) use `$crate::` for crate-internal paths, never `crate::` or `self::`
- [ ] Standard library paths use `::core::` and `::alloc::` (not `::std::`) for `no_std` compatibility
- [ ] `compile_error!` used for meaningful error messages on invalid input patterns
- [ ] Macro placement respects textual scoping (defined before use) unless `#[macro_export]`

### Procedural Macros

- [ ] `syn` features minimized (don't enable `full` when `derive` suffices -- reduces compile time)
- [ ] Spans propagated from input tokens to output tokens (errors point to user code, not macro internals)
- [ ] `Span::mixed_site()` is the default for introduced helper variables — `call_site` only when intentionally pointing at user code; `def_site` is nightly-only on `proc_macro::Span`
- [ ] Error reporting uses `syn::Error::new_spanned(node, msg)` with the offending AST node, never `panic!`
- [ ] Multiple errors collected and reported together via `syn::Error::combine` (good UX vs first-failure)
- [ ] `parse_quote!` (not `quote!`) used when the result needs to be a `syn::T` for further AST manipulation; `syn::parse2(quote!{...})` for fallible cases
- [ ] Public types re-exported from `proc_macro2`, not `proc_macro` (compatibility with downstream consumers)
- [ ] `proc-macro2` used for testing (testable outside of compiler context)
- [ ] Generated code volume is proportionate -- proc macros that emit large amounts of code bloat compile times

### Derive Macros

- [ ] Derivation is obvious -- a developer could guess what it does from the trait name alone
- [ ] Helper attributes (`#[serde(skip)]` style) are documented
- [ ] Trait implementation is correct for all variant shapes (unit, tuple, struct variants)
- [ ] Generated `impl` blocks use fully qualified paths (`::core::`, `$crate::`)

### Attribute Macros

- [ ] Input item is preserved or intentionally transformed (not accidentally dropped)
- [ ] Attribute arguments are validated with clear error messages
- [ ] Test generation patterns (`#[test_case]` style) produce unique test names
- [ ] Framework annotations document what code they generate

### Edition 2024 Awareness

- [ ] Macro output does not use `gen` as an identifier (reserved keyword -- use `r#gen` or rename)
- [ ] Generated `unsafe fn` bodies use explicit `unsafe {}` blocks around unsafe ops
- [ ] Generated `extern` blocks use `unsafe extern`

### Generics vs Macros

Flag a macro when the same result is achievable with generics or trait bounds. Macros are appropriate when:
- The generated code varies structurally (not just by type)
- Repetitive trait impls for many concrete types
- Test batteries with configuration variants
- Compile-time computation that `const fn` cannot express

## Severity Calibration

### Critical (Block Merge)
- Macro generates unsound `unsafe` code
- Hygiene violation in macro that outputs `unsafe` blocks (caller's variables leak into unsafe context)
- Proc macro panics instead of returning `compile_error!` (crashes the compiler)
- Derive macro generates incorrect trait implementation (violates trait contract)

### Major (Should Fix)
- Exported macro uses `crate::` or `self::` instead of `$crate::` (breaks for downstream users)
- Exported macro uses `::std::` instead of `::core::`/`::alloc::` (breaks `no_std` users)
- Wrong fragment type causing unexpected parsing (`:expr` where `:tt` needed, or vice versa)
- Proc macro enables `syn` full features unnecessarily (compile time cost)
- Missing span propagation (errors point to macro definition, not invocation)
- No error handling in proc macro (panics on bad input instead of `compile_error!`)

### Minor (Consider Fixing)
- Missing trailing comma/semicolon tolerance in repetition patterns
- Matcher arms not ordered most-specific-first
- Macro used where generics would be clearer and equally expressive
- Missing `compile_error!` fallback arm for invalid patterns
- Helper attributes undocumented

### Informational (Note Only)
- Suggestions to split complex `macro_rules!` into a proc macro
- Suggestions to reduce generated code volume
- TT munching or push-down accumulation patterns that could be simplified

## Valid Patterns (Do NOT Flag)

- **`macro_rules!` for test batteries** -- Generating repetitive test modules from a list of types/configs
- **`macro_rules!` for trait impls** -- Implementing a trait for many concrete types with identical bodies
- **TT munching** -- Valid advanced pattern for recursive token processing
- **Push-down accumulation** -- Valid pattern for building output incrementally across recursive calls
- **`#[macro_export]` with `$crate`** -- Correct way to make macros usable outside the defining crate
- **`Span::call_site()` for generated functions** -- Intentionally making generated items visible to callers
- **`syn::Error::to_compile_error()`** -- Correct error reporting pattern in proc macros
- **`trybuild` tests for proc macros** -- Standard compile-fail testing approach
- **Attribute macros on test functions** -- Common pattern for test setup/teardown
- **`compile_error!` in impossible match arms** -- Good practice for catching invalid macro input
