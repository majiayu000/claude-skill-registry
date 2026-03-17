---
name: rust-quality
description: Rust code quality for crates/engine. Use when reviewing Rust code, auditing the engine, or running quality checks.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Rust Code Quality

Comprehensive quality standards for Rust crates in `crates/`.

## Quick Commands

```bash
cd crates/engine

# Quality checks
cargo clippy --all-targets -- -D warnings
cargo test
cargo fmt --check
cargo doc --no-deps

# Full workspace check
cd crates && cargo clippy --workspace --all-targets -- -D warnings
```

---

## Clippy Configuration

Add to each crate's `lib.rs` or `main.rs`:

```rust
// Required lints (deny these)
#![deny(clippy::correctness)]
#![deny(unsafe_code)]  // Unless crate needs unsafe

// Warn on these
#![warn(clippy::all)]
#![warn(clippy::pedantic)]
#![warn(missing_docs)]

// Specific valuable lints
#![warn(clippy::unwrap_used)]
#![warn(clippy::expect_used)]
#![warn(clippy::panic)]
#![warn(clippy::dbg_macro)]
#![warn(clippy::todo)]
#![warn(clippy::print_stdout)]
#![warn(clippy::print_stderr)]

// Pedantic exceptions (allow these)
#![allow(clippy::module_name_repetitions)]
#![allow(clippy::must_use_candidate)]
#![allow(clippy::missing_errors_doc)]
#![allow(clippy::missing_panics_doc)]
```

### CI Configuration

Create `clippy.toml` in crate root:

```toml
cognitive-complexity-threshold = 25
too-many-arguments-threshold = 10
type-complexity-threshold = 300
```

---

## Error Handling

### Required Pattern

Every crate MUST have a `Result` type alias:

```rust
// src/lib.rs or src/errors.rs
pub type Result<T> = std::result::Result<T, Error>;
```

### Error Enum Pattern

Use `thiserror` for all error types:

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum Error {
    // Wrap external errors with context
    #[error("Failed to read config '{path}': {source}")]
    ConfigRead {
        path: String,
        #[source]
        source: std::io::Error,
    },

    // Domain errors with payloads
    #[error("Spell {spell_id} not found")]
    SpellNotFound { spell_id: u32 },

    // Conversion from other errors
    #[error("Parse error: {0}")]
    Parse(#[from] ParseError),
}
```

### Forbidden Patterns

```rust
// WRONG: unwrap in non-test code
let value = result.unwrap();

// WRONG: expect without context
let value = result.expect("failed");

// WRONG: panic! for recoverable errors
panic!("invalid state");

// RIGHT: propagate with ?
let value = result?;

// RIGHT: provide context
let value = result.context("loading spell definitions")?;

// RIGHT: match and handle
let value = result.unwrap_or_else(|e| {
    tracing::warn!("Using default: {e}");
    Default::default()
});
```

### When unwrap/expect IS Allowed

1. **Test code** - `#[cfg(test)]` modules
2. **Initialization** - `OnceLock::get().expect()` after verified set
3. **Static guarantees** - Regex::new for compile-time patterns
4. **Infallible conversions** - When types guarantee success

Always document WHY it's safe:

```rust
// SAFETY: Regex is compile-time constant, always valid
static PATTERN: OnceLock<Regex> = OnceLock::new();
fn get_pattern() -> &'static Regex {
    PATTERN.get_or_init(|| Regex::new(r"^\d+$").expect("valid regex"))
}
```

---

## Anti-Patterns

### Deref Polymorphism

```rust
// WRONG - using Deref to emulate inheritance
impl Deref for Player {
    type Target = Actor;
    fn deref(&self) -> &Self::Target { &self.actor }
}

// RIGHT - explicit delegation or traits
impl Player {
    pub fn name(&self) -> &str { self.actor.name() }
}

// RIGHT - use traits for shared behavior
trait Named {
    fn name(&self) -> &str;
}
```

### Clone to Fight Borrow Checker

```rust
// WRONG - cloning to satisfy borrow checker
for item in items.iter().cloned() { ... }
let copy = data.clone(); // just to avoid borrow

// RIGHT - restructure to avoid
for item in &items { ... }
for item in items { ... }  // consume if you can

// RIGHT - if clone needed, document why
let copy = data.clone(); // Clone needed: data used after async boundary
```

### Excessive Borrow Lifetimes

```rust
// WRONG - storing borrows in structs
struct Processor<'a> {
    data: &'a Data,  // Forces caller to manage lifetime
}

// RIGHT - owned data or pass at call site
struct Processor {
    data: Data,  // Owned
}

impl Processor {
    fn process(&self, data: &Data) { ... }  // Borrow at use
}
```

---

## Performance Patterns

### Use Appropriate Collections

```rust
// Fast hashing for IDs (u32, u64)
use ahash::AHashMap;
let map: AHashMap<SpellIdx, SpellDef> = AHashMap::new();

// Stack allocation for small vecs
use smallvec::SmallVec;
let effects: SmallVec<[Effect; 4]> = SmallVec::new();

// Faster mutex for low-contention
use parking_lot::RwLock;
let data: RwLock<Data> = RwLock::new(data);
```

### Avoid Hidden Allocations

```rust
// WRONG: Creates owned String
fn get_name(&self) -> String {
    self.name.clone()
}

// RIGHT: Return reference
fn name(&self) -> &str {
    &self.name
}

// WRONG: Clone in loop
for item in items.iter().cloned() { ... }

// RIGHT: Borrow or consume
for item in &items { ... }
for item in items { ... }
```

### Profile with Criterion

```rust
use criterion::{criterion_group, criterion_main, Criterion};

fn bench_simulation(c: &mut Criterion) {
    c.bench_function("sim_10s", |b| {
        b.iter(|| run_simulation(Duration::from_secs(10)))
    });
}

criterion_group!(benches, bench_simulation);
criterion_main!(benches);
```

---

## Type Safety Patterns

### Newtype IDs

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct SpellIdx(pub u32);

impl SpellIdx {
    pub const fn new(id: u32) -> Self {
        Self(id)
    }
}

impl std::fmt::Display for SpellIdx {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Spell({})", self.0)
    }
}
```

### Builder Pattern

```rust
pub struct SpellBuilder {
    id: SpellIdx,
    name: String,
    damage: Option<DamageEffect>,
}

impl SpellBuilder {
    pub fn new(id: SpellIdx, name: impl Into<String>) -> Self {
        Self {
            id,
            name: name.into(),
            damage: None,
        }
    }

    pub fn damage(mut self, effect: DamageEffect) -> Self {
        self.damage = Some(effect);
        self
    }

    pub fn build(self) -> SpellDef {
        SpellDef { id: self.id, name: self.name, damage: self.damage }
    }
}
```

### Prefer Slices Over Vecs

```rust
// WRONG: Takes ownership unnecessarily
fn process(items: Vec<Item>) { ... }

// RIGHT: Accepts any contiguous sequence
fn process(items: &[Item]) { ... }
```

---

## Testing Standards

### Test Organization

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_functionality() {
        // Arrange
        let input = create_input();

        // Act
        let result = process(input);

        // Assert
        assert_eq!(result, expected);
    }
}
```

### Snapshot Testing

Use `insta` for parser/serializer tests:

```rust
use insta::assert_snapshot;

#[test]
fn test_parse_profile() {
    let input = include_str!("fixtures/profile.simc");
    let result = parse(input).unwrap();
    assert_snapshot!(format!("{result:#?}"));
}
```

### Test Naming

```rust
#[test]
fn test_spell_damage_with_crit_modifier() { }

#[test]
fn test_aura_refresh_extends_duration() { }

#[test]
fn test_parse_error_on_invalid_input() { }
```

---

## Documentation Standards

### Module Docs

````rust
//! Spell effect handling and damage calculation.
//!
//! This module provides the core damage pipeline including:
//! - Base damage calculation
//! - Stat scaling
//! - Critical strike handling
//! - Armor mitigation
//!
//! # Example
//!
//! ```
//! use engine::combat::DamagePipeline;
//!
//! let damage = DamagePipeline::calculate(base, coefficients, stats);
//! ```
````

### Function Docs

```rust
/// Calculate final damage after all modifiers.
///
/// # Arguments
///
/// * `base` - Base damage before coefficients
/// * `stats` - Current player stats
/// * `target` - Target for armor calculations
///
/// # Returns
///
/// Final damage value after all modifiers applied.
pub fn calculate_damage(base: f32, stats: &Stats, target: &Target) -> f32 {
    // ...
}
```

---

## Unsafe Code Guidelines

### When Unsafe is Justified

1. FFI calls (Cranelift, system APIs)
2. Performance-critical CPU detection
3. Memory-mapped I/O

### Required Documentation

```rust
/// # Safety
///
/// This function uses platform-specific system calls that are well-defined
/// for all supported platforms (Linux, macOS, Windows). The returned value
/// is validated to be non-zero before use.
#[cfg(feature = "parallel")]
pub unsafe fn detect_cores() -> usize {
    // ...
}
```

### Unsafe Audit Checklist

- [ ] Document safety invariants
- [ ] Validate all inputs
- [ ] No undefined behavior paths
- [ ] Tested on all target platforms
- [ ] Reviewed by second person

---

## Quality Checklist

### Error Handling

- [ ] No `.unwrap()` outside tests
- [ ] No `.expect()` without safety comment
- [ ] Errors have context (file paths, IDs)
- [ ] Result type alias exists

### Performance

- [ ] No `.clone()` in hot paths without justification
- [ ] Collections sized appropriately (SmallVec, ahash)
- [ ] No allocations in tight loops

### API Design

- [ ] Public types have `#[derive(Debug)]`
- [ ] Constructors are `new()` or `builder()`
- [ ] Getters don't take `&mut self`
- [ ] No `&String` or `&Vec` parameters

### Code Style

- [ ] `cargo fmt` passes
- [ ] No `TODO` without issue reference
- [ ] No commented-out code
- [ ] Module docs present

### Testing

- [ ] New code has tests
- [ ] Edge cases covered
- [ ] Error paths tested

---

## Pre-Review Commands

Run before any PR:

```bash
# Format
cargo fmt --all

# Lint (strict)
cargo clippy --workspace --all-targets -- \
    -D warnings \
    -D clippy::unwrap_used \
    -D clippy::expect_used \
    -A clippy::module_name_repetitions

# Test
cargo test --workspace

# Doc check
cargo doc --workspace --no-deps

# Security audit (if cargo-audit installed)
cargo audit
```

---

## Audit Commands

```bash
# Find unwrap/expect outside tests
grep -rn "\.unwrap()\|\.expect(" crates/engine/src/ --include="*.rs" | grep -v "_test\|tests\|#\[test\]"

# Find TODO comments
grep -rn "TODO\|FIXME" crates/engine/src/ --include="*.rs"

# Find panic! calls
grep -rn "panic!" crates/engine/src/ --include="*.rs" | grep -v "_test\|tests"

# Find missing docs on pub items
cargo doc --workspace --no-deps 2>&1 | grep "warning: missing documentation"

# Find clone in loops
grep -rn "\.iter()\.cloned()\|\.clone()" crates/engine/src/ --include="*.rs"

# Find magic numbers
grep -rn "[^0-9][0-9]\+\.[0-9]\+" crates/engine/src/ --include="*.rs" | grep -v "const\|static\|test"
```

---

## References

- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Clippy Lint List](https://rust-lang.github.io/rust-clippy/master/index.html)
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)
- [Idiomatic Rust](https://github.com/mre/idiomatic-rust)
- Existing patterns: `crates/engine/src/`, `crates/common/src/`
