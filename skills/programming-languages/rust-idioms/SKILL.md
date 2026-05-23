---
name: rust-idioms
description: Rust refactoring and idiomatic patterns guidelines from the Rust Community (formerly rust-refactor). This skill should be used when writing, reviewing, or refactoring Rust code to ensure idiomatic patterns and clean architecture. Triggers on tasks involving Rust types, ownership, error handling, traits, modules, conversions, or iterator patterns.
---

# Rust Community Rust Refactoring Best Practices

Comprehensive refactoring and idiomatic patterns guide for Rust applications, maintained by the Rust Community. Contains 44 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Rust code with strong type guarantees
- Refactoring ownership and borrowing patterns
- Designing error handling strategies
- Creating public APIs with traits and generics
- Organizing modules and controlling visibility

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Type Safety & Newtype Patterns | CRITICAL | `type-` |
| 2 | Ownership & Borrowing | CRITICAL | `own-` |
| 3 | Error Handling Patterns | HIGH | `err-` |
| 4 | API Design & Traits | HIGH | `api-` |
| 5 | Module & Visibility | MEDIUM-HIGH | `mod-` |
| 6 | Conversion Traits | MEDIUM | `conv-` |
| 7 | Idiomatic Patterns | MEDIUM | `idiom-` |
| 8 | Iterator & Collections | LOW-MEDIUM | `iter-` |

## Quick Reference

### 1. Type Safety & Newtype Patterns (CRITICAL)

- [`type-newtype-units`](references/type-newtype-units.md) - Use newtype pattern for unit safety
- [`type-newtype-invariants`](references/type-newtype-invariants.md) - Encode invariants in newtype constructors
- [`type-non-exhaustive-enums`](references/type-non-exhaustive-enums.md) - Use non-exhaustive for extensible enums
- [`type-phantom-data`](references/type-phantom-data.md) - Use PhantomData for type-level state
- [`type-strong-typing-strings`](references/type-strong-typing-strings.md) - Replace stringly-typed APIs with strong types
- [`type-builder-required-fields`](references/type-builder-required-fields.md) - Use typestate builders for required fields

### 2. Ownership & Borrowing (CRITICAL)

- [`own-prefer-borrowing`](references/own-prefer-borrowing.md) - Prefer borrowing over ownership in parameters
- [`own-cow-conditional-clone`](references/own-cow-conditional-clone.md) - Use Cow for conditional ownership
- [`own-accept-borrowed-types`](references/own-accept-borrowed-types.md) - Accept borrowed types over owned references
- [`own-return-owned-for-flexibility`](references/own-return-owned-for-flexibility.md) - Return owned types for caller flexibility
- [`own-avoid-unnecessary-clone`](references/own-avoid-unnecessary-clone.md) - Avoid unnecessary clone calls
- [`own-lifetime-elision`](references/own-lifetime-elision.md) - Leverage lifetime elision rules

### 3. Error Handling Patterns (HIGH)

- [`err-use-result-not-panic`](references/err-use-result-not-panic.md) - Use Result instead of panic! for recoverable errors
- [`err-thiserror-for-libraries`](references/err-thiserror-for-libraries.md) - Use thiserror for library error types
- [`err-anyhow-for-applications`](references/err-anyhow-for-applications.md) - Use anyhow for application error handling
- [`err-question-mark-propagation`](references/err-question-mark-propagation.md) - Use the question mark operator for error propagation
- [`err-option-for-absence`](references/err-option-for-absence.md) - Use Option for absence, not sentinel values

### 4. API Design & Traits (HIGH)

- [`api-derive-common-traits`](references/api-derive-common-traits.md) - Derive common traits for public types
- [`api-impl-standard-traits`](references/api-impl-standard-traits.md) - Implement standard traits for ergonomic APIs
- [`api-generic-bounds`](references/api-generic-bounds.md) - Use trait bounds for generic flexibility
- [`api-sealed-traits`](references/api-sealed-traits.md) - Use sealed traits to prevent external implementation
- [`api-builder-pattern`](references/api-builder-pattern.md) - Use builder pattern for complex construction
- [`api-extension-traits`](references/api-extension-traits.md) - Use extension traits to add methods to foreign types

### 5. Module & Visibility (MEDIUM-HIGH)

- [`mod-minimize-pub-api`](references/mod-minimize-pub-api.md) - Minimize public API surface
- [`mod-pub-use-reexports`](references/mod-pub-use-reexports.md) - Use pub use for clean module re-exports
- [`mod-split-large-modules`](references/mod-split-large-modules.md) - Split large modules into submodules
- [`mod-crate-prefix-imports`](references/mod-crate-prefix-imports.md) - Use crate:: prefix for internal imports
- [`mod-tests-submodule`](references/mod-tests-submodule.md) - Use tests submodule for unit tests

### 6. Conversion Traits (MEDIUM)

- [`conv-impl-from-not-into`](references/conv-impl-from-not-into.md) - Implement From instead of Into
- [`conv-asref-for-flexibility`](references/conv-asref-for-flexibility.md) - Accept AsRef for flexible string parameters
- [`conv-impl-deref-for-newtypes`](references/conv-impl-deref-for-newtypes.md) - Implement Deref for transparent newtype access
- [`conv-tryfrom-for-fallible`](references/conv-tryfrom-for-fallible.md) - Use TryFrom for fallible conversions
- [`conv-inner-function-pattern`](references/conv-inner-function-pattern.md) - Use inner function pattern to reduce monomorphization

### 7. Idiomatic Patterns (MEDIUM)

- [`idiom-default-trait`](references/idiom-default-trait.md) - Implement Default instead of new() without arguments
- [`idiom-constructor-naming`](references/idiom-constructor-naming.md) - Follow constructor naming conventions
- [`idiom-let-else`](references/idiom-let-else.md) - Use let-else for early returns on pattern match failure
- [`idiom-struct-update-syntax`](references/idiom-struct-update-syntax.md) - Use struct update syntax for partial overrides
- [`idiom-destructuring-assignment`](references/idiom-destructuring-assignment.md) - Use destructuring for multiple returns and field access
- [`idiom-match-guards`](references/idiom-match-guards.md) - Use match guards for complex conditions

### 8. Iterator & Collections (LOW-MEDIUM)

- [`iter-prefer-iterators-over-loops`](references/iter-prefer-iterators-over-loops.md) - Prefer iterator methods over manual loops
- [`iter-use-collect-turbofish`](references/iter-use-collect-turbofish.md) - Use turbofish for explicit collect type
- [`iter-filter-map-combined`](references/iter-filter-map-combined.md) - Use filter_map for combined filter and transform
- [`iter-avoid-collect-then-iterate`](references/iter-avoid-collect-then-iterate.md) - Avoid collecting then iterating
- [`iter-enumerate-for-indices`](references/iter-enumerate-for-indices.md) - Use enumerate instead of manual index tracking

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Full Compiled Document

For a single-file comprehensive guide, see [AGENTS.md](AGENTS.md).
