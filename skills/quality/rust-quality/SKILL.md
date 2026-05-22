---
name: rust-quality
description: Review Rust code for idiomatic patterns, best practices, and production quality. Use when reviewing Rust crates, checking code quality, or before committing Rust changes.
allowed-tools: Read, Grep, Glob, Bash
---

# Rust Code Quality

Review skill for checking Rust code against idiomatic patterns and best practices.

## Checklist

### Error Handling

- [ ] Uses `thiserror` for library errors, `anyhow` for applications
- [ ] No `.unwrap()` or `.expect()` in production paths (use `?` operator)
- [ ] Error types have meaningful context/payloads
- [ ] `Result` is returned, not panics
- [ ] Uses `?` operator, not `.unwrap()` chains

### Ownership & Borrowing

- [ ] Prefers borrowing (`&T`, `&mut T`) over cloning
- [ ] Uses `Clone` only when necessary
- [ ] Avoids unnecessary `Arc`/`Rc` when ownership transfer works
- [ ] Lifetime annotations are minimal and correct
- [ ] No needless `to_string()` / `clone()` in hot paths

### Idiomatic Patterns

- [ ] Uses iterators over manual loops (`for i in 0..len` → `.iter()`)
- [ ] Uses `if let` / `match` for Option/Result handling
- [ ] Uses `?` for early returns, not nested `if let`
- [ ] Prefers `impl Trait` for return types when appropriate
- [ ] Uses builder pattern for complex construction
- [ ] Derives common traits: `Debug`, `Clone`, `Default` where applicable

### Naming Conventions (RFC 430)

- [ ] Types: `PascalCase`
- [ ] Functions/methods: `snake_case`
- [ ] Constants: `SCREAMING_SNAKE_CASE`
- [ ] Conversion methods: `as_*` (cheap ref), `to_*` (expensive), `into_*` (ownership)
- [ ] Getters: no `get_` prefix (just `fn name(&self)`)
- [ ] Predicates: `is_*`, `has_*`, `can_*`

### API Design

- [ ] Public items have doc comments (`///`)
- [ ] Examples in doc comments use `?` not `unwrap`
- [ ] Implements standard traits: `From`, `TryFrom`, `Default`, `Display`
- [ ] Uses newtypes for type safety (not raw primitives)
- [ ] Validates inputs at boundaries
- [ ] Functions take `impl Into<T>` for flexible APIs

### Async/Concurrency

- [ ] Uses `tokio::spawn` for fire-and-forget tasks
- [ ] Channels sized appropriately (not unbounded without reason)
- [ ] No blocking in async contexts (use `spawn_blocking`)
- [ ] Mutex guards dropped before await points
- [ ] Uses `Arc` for shared ownership across threads

### Performance

- [ ] Avoids allocations in hot paths
- [ ] Uses `&str` over `String` for borrowed data
- [ ] Uses `Cow<str>` when ownership is conditional
- [ ] Prefers `Vec::with_capacity` when size is known
- [ ] Uses `#[inline]` sparingly and intentionally

### Project Structure

- [ ] `mod.rs` or `module/mod.rs` pattern is consistent
- [ ] Public API is re-exported cleanly from `lib.rs`
- [ ] Internal modules use `pub(crate)` not `pub`
- [ ] Tests in `tests/` or `#[cfg(test)]` modules
- [ ] Feature flags for optional dependencies

### Clippy Lints

Run these checks:
```bash
cargo clippy -- -W clippy::pedantic -W clippy::nursery
cargo clippy -- -D clippy::unwrap_used -D clippy::expect_used
```

Key lint groups:
- `clippy::correctness` - Must fix (deny by default)
- `clippy::suspicious` - Should fix
- `clippy::style` - Idiomatic code
- `clippy::complexity` - Simplification opportunities
- `clippy::perf` - Performance improvements
- `clippy::pedantic` - Extra strictness (recommended)

## Common Anti-Patterns

### Wrong

```rust
// Unnecessary clone
let name = self.name.clone();
do_something(&name);

// Unwrap in production
let value = map.get("key").unwrap();

// Manual loop
for i in 0..vec.len() {
    process(vec[i]);
}

// Nested if-let
if let Some(x) = opt {
    if let Ok(y) = x.parse() {
        // ...
    }
}

// Getter with get_ prefix
fn get_name(&self) -> &str { &self.name }
```

### Right

```rust
// Borrow directly
do_something(&self.name);

// Handle error properly
let value = map.get("key").ok_or(MyError::KeyNotFound)?;

// Iterator
for item in &vec {
    process(item);
}

// let-else or ? operator
let Some(x) = opt else { return None };
let y = x.parse()?;

// Clean getter
fn name(&self) -> &str { &self.name }
```

## How to Use

1. Run `cargo clippy -- -W clippy::pedantic` first
2. Read the files to review
3. Check against patterns above
4. Report issues with `file:line` references
5. Suggest idiomatic fixes

## References

- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Clippy Lints](https://rust-lang.github.io/rust-clippy/master/index.html)
- [The Rust Book](https://doc.rust-lang.org/book/)
