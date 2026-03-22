---
name: rust
description: Rust coding conventions. Apply when writing, reviewing, or modifying Rust code. Covers error handling, types, ownership, testing, and anti-patterns.
---

# Rust Coding Conventions

## Error Handling

- Return `Result<T, E>` for fallible operations
- Use `thiserror` with `#[derive(Error)]` for library error enums. Structure: variant name describes the failure, `#[error("...")]` format string includes diagnostic context (sizes, IDs), use `#[from]` for transparent wrapping of upstream errors
- Propagate with `?` operator — avoid match chains for error forwarding
- Never use `.unwrap()` or `.expect()` outside of tests
- `anyhow` for binary/CLI code where specific error types don't matter; never in library crates

## Borrowing & Ownership

- Prefer `&T` over `.clone()` unless ownership transfer is required
- Use `&str` over `String`, `&[T]` over `Vec<T>` in function parameters
- Small `Copy` types (<=24 bytes) can be passed by value
- Use `Cow<'_, T>` when ownership is ambiguous at compile time
- If you're adding `.clone()` to satisfy the borrow checker, step back and reconsider the data flow

## Type Design

- Use newtypes for semantic distinction: `pub struct UserId(pub Uuid)`, `pub struct Port(pub u16)`
- Derive ordering: `Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize` — include only what's semantically correct
- `Copy` for small value types (IDs, enums). `Clone` but not `Copy` for larger types
- Implement `Display` manually when the type appears in logs or user-facing output

## Documentation Style

- `///` doc comments on all public types, functions, and enum variants — explain **what** and **how**
- `//` inline comments only to explain **why** (safety invariants, workarounds, design rationale)
- Function docs should include format specs when relevant (e.g., wire format, encoding details)
- Group related constants with `// --- Section Name ---` separators
- Every `TODO` needs a linked issue: `// TODO(#42): description`
- No module-level `//!` doc comments unless the module is a public API entry point

## Testing Conventions

- Tests live inline: `#[cfg(test)] mod tests { }` at the bottom of each module
- Test naming: `snake_case_description` — be descriptive (e.g., `buffer_duplicate_insert_ignored`)
- For serialization testing, use round-trip helpers that encode then decode and assert equality
- `#[tokio::test]` for async tests — always with timeouts
- One assertion per test when possible; multiple related assertions are fine if testing one logical behavior
- Test error conditions explicitly — assert the specific error variant, not just "is error"
- Use polling with backoff for async assertions, never fixed `sleep`

## Iterators & Collections

- Prefer iterators (`.iter()`, `.map()`, `.filter()`) over index-based loops
- Avoid intermediate `.collect()` — chain iterators directly
- Use `.iter()` for `Copy` types, `.into_iter()` when consuming ownership

## Clippy & Linting

- Run `cargo clippy` after every change
- Use `#[expect(clippy::lint_name)]` over `#[allow(...)]` — `expect` warns if the lint no longer triggers
- Key lints to watch: `redundant_clone`, `large_enum_variant` (consider `Box`), `needless_collect`

## Anti-Patterns

| Anti-Pattern | Why Bad | Better |
|---|---|---|
| `.clone()` everywhere | Hides ownership issues | Proper references or restructure data flow |
| `.unwrap()` in library code | Runtime panics | `?`, or handle the error |
| `String` in function params | Unnecessary allocation | `&str`, `Cow<str>` |
| Index-based loops | Error-prone, unidiomatic | Iterators |
| `Rc`/`Arc` when single owner | Unnecessary overhead | Simple ownership |
| Giant match arms | Unmaintainable | Extract to methods |
| Ignoring `#[must_use]` | Silently dropped errors | Handle or `let _ =` |
| `unsafe` without SAFETY comment | UB risk, no audit trail | Document invariants or find safe pattern |
