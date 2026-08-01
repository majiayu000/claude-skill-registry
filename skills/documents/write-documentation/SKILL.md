---
name: write-documentation
description: 'Write and format Rust documentation correctly. Apply proactively when
  writing code with rustdoc comments (//! or ///). Covers structure (inverted pyramid),
  intra-doc links (crate:: paths, reference-st'
---

---
name: write-documentation
description: Write and format Rust documentation correctly. Apply proactively when writing code with rustdoc comments (//! or ///). Covers structure (inverted pyramid), intra-doc links (crate:: paths, reference-style), constant conventions (binary/byte literal/decimal), and formatting (cargo rustdoc-fmt). Also use retroactively via /fix-intradoc-links, /fix-comments, or /fix-md-tables commands.
---

# Writing Good Rust Documentation

This consolidated skill covers all aspects of writing high-quality rustdoc:

1. **Structure** - Inverted pyramid principle
2. **Links** - Intra-doc link patterns
3. **Constants** - Human-readable numeric literals
4. **Formatting** - Markdown tables and cargo rustdoc-fmt

## When to Use

### Proactively (While Writing Code)

- Writing new code that includes `///` or `//!` doc comments
- Creating new modules, traits, structs, or functions
- Adding links to other types or modules in documentation
- Defining byte/u8 constants

### Retroactively (Fixing Issues)

- `/fix-intradoc-links` - Fix broken links, convert inline to reference-style
- `/fix-comments` - Fix constant conventions in doc comments
- `/fix-md-tables` - Fix markdown table formatting
- `/docs` - Full documentation check and fix

---

## Part 1: Structure (Inverted Pyramid)

Structure documentation with high-level concepts at the top, details below:

```text
╲────────────╱
 ╲          ╱  High-level concepts - Module/trait/struct documentation
  ╲────────╱
   ╲      ╱  Mid-level details - Method group documentation
    ╲────╱
     ╲  ╱  Low-level specifics - Individual method documentation
      ╲╱
```

**Avoid making readers hunt through method docs for the big picture.**

### Placement Guidelines

| Level | What to Document | Example Style |
|-------|------------------|---------------|
| **Module/Trait** | Why, when, conceptual examples, workflows, ASCII diagrams | Comprehensive |
| **Method** | How to call, exact types, parameters | Brief (IDE tooltips) |

### Reference Up, Not Down

```rust
/// See the [module-level documentation] for complete usage examples.
///
/// [module-level documentation]: mod@crate::example
pub fn some_method(&self) -> Result<()> { /* ... */ }
```

---

## Part 2: Intra-doc Links

### Golden Rules

1. **Use `crate::` paths** (not `super::`) - absolute paths are stable
2. **Use reference-style links** - keep prose clean
3. **Place all link definitions at bottom** of comment block
4. **Include `()` for functions/methods** - distinguishes from types

### Link All Symbols for Refactoring Safety

**Every codebase symbol in backticks must be a link.** This isn't just style—it's safety.

When you rename, move, or delete a symbol:
- **With links**: `cargo doc` fails with a clear error pointing to the stale reference
- **Without links**: The docs silently rot, referencing symbols that no longer exist

| Docs say | Symbol renamed to | With link | Without link |
|----------|-------------------|-----------|--------------|
| `` [`Parser`] `` | `Tokenizer` | ❌ Build error | ✅ Silently stale |
| `` [`process()`] `` | `handle()` | ❌ Build error | ✅ Silently stale |

**Rule:** If it's a symbol from your codebase and it's in backticks, make it a link.

```rust
// ❌ Bad: Will silently rot when Parser is renamed
/// Uses `Parser` for tokenization.

// ✅ Good: cargo doc will catch if Parser is renamed
/// Uses [`Parser`] for tokenization.
///
/// [`Parser`]: crate::Parser
```

### Quick Reference

| Link To | Pattern |
|---------|---------|
| Struct | `[`Foo`]: crate::Foo` |
| Function | `[`process()`]: crate::process` |
| Method | `[`run()`]: Self::run` |
| Module | `[`parser`]: mod@crate::parser` |
| Section heading | `[`docs`]: mod@crate::module#section-name` |
| Dependency crate | `[`tokio::spawn()`]: tokio::spawn` |

### ✅ Good: Reference-Style Links

```rust
/// This struct uses [`Position`] to track cursor location.
///
/// The [`render()`] method updates the display.
///
/// [`Position`]: crate::Position
/// [`render()`]: Self::render
```

### ❌ Bad: Inline Links

```rust
/// This struct uses [`Position`](crate::Position) to track cursor location.
```

### ❌ Bad: No Links

```rust
/// This struct uses `Position` to track cursor location.
```

### Linking to Dependency Crates

For crates listed in your `Cargo.toml` dependencies, **use direct intra-doc links** instead of
external hyperlinks to docs.rs. Rustdoc automatically resolves these when the dependency is built.

| Link To | Pattern |
|---------|---------|
| Crate root | `[`crossterm`]: ::crossterm` |
| Type in crate | `[`mio::Poll`]: mio::Poll` |
| Function in crate | `[`tokio::io::stdin()`]: tokio::io::stdin` |
| Macro in crate | `[`tokio::select!`]: tokio::select` |

#### ✅ Good: Direct Dependency Links

```rust
//! **UI freezes** on terminal resize when using [`tokio::io::stdin()`].
//! Internally, cancelling a [`tokio::select!`] branch doesn't stop the read.
//! However, the use of [Tokio's stdin] caused the first two issues.
//!
//! [`tokio::select!`]: tokio::select
//! [`tokio::io::stdin()`]: tokio::io::stdin
//! [Tokio's stdin]: tokio::io::stdin
```

```rust
/// Uses [`mio::Poll`] to efficiently wait on file descriptor events.
///
/// [`mio::Poll`]: mio::Poll
```

```rust
//! Use [`crossterm`]'s `enable_raw_mode` for terminal input.
//!
//! [`crossterm`]: ::crossterm
```

#### ❌ Bad: External docs.rs Links for Dependencies

```rust
/// Uses [mio::Poll](https://docs.rs/mio/latest/mio/struct.Poll.html) to wait.
```

Don't use docs.rs URLs for crates that are **already in your `Cargo.toml`**.

**Why direct links are better for dependencies:**
- Clickable in local `cargo doc` output (works offline)
- Version-matched to your actual dependency version
- Validated by rustdoc (broken links caught at build time)
- Consistent style with internal crate links

#### ✅ OK: External docs.rs Links for Non-Dependencies

For crates that are **not** in your `Cargo.toml`, external links are fine:

```rust
/// This is similar to how [rayon](https://docs.rs/rayon) handles parallel iteration.
```

Since `rayon` isn't a dependency, there's no local documentation to link to.

**For detailed patterns, see `link-patterns.md` in this skill.**

---

## Part 3: Constant Conventions

Use human-readable numeric literals for byte constants:

| Type | Format | Example |
|------|--------|---------|
| **Bitmasks** (used in `&`, `\|`, `^`) | Binary | `0b0110_0000` |
| **Printable ASCII** | Byte literal | `b'['` |
| **Non-printable bytes** | Decimal | `27` |
| **Comments** | Show hex | `// (0x1B in hex)` |

### ✅ Good: Human-Readable

```rust
/// ESC byte (0x1B in hex).
pub const ANSI_ESC: u8 = 27;

/// CSI bracket byte: `[` (91 decimal, 0x5B hex).
pub const ANSI_CSI_BRACKET: u8 = b'[';

/// Mask to convert control character to lowercase (0x60 in hex).
pub const CTRL_TO_LOWERCASE_MASK: u8 = 0b0110_0000;
```

### ❌ Bad: Hex Everywhere

```rust
pub const ANSI_ESC: u8 = 0x1B;
pub const ANSI_CSI_BRACKET: u8 = 0x5B;
pub const CTRL_TO_LOWERCASE_MASK: u8 = 0x60;
```

**For detailed conventions, see `constant-conventions.md` in this skill.**

---

## Part 4: Formatting

### Run cargo rustdoc-fmt

```bash
# Format specific file
cargo rustdoc-fmt path/to/file.rs

# Format all git-changed files
cargo rustdoc-fmt

# Format entire workspace
cargo rustdoc-fmt --workspace
```

**What it does:**
- Formats markdown tables with proper column alignment
- Converts inline links to reference-style
- Preserves code examples

**If not installed:**
```bash
cd build-infra && cargo install --path . --force
```

### Verify Documentation Builds

```bash
cargo doc --no-deps
cargo test --doc
```

---

## Code Examples in Docs

**Golden Rule:** Don't use `ignore` unless absolutely necessary.

| Scenario | Use |
|----------|-----|
| Example compiles and runs | ` ``` ` (default) |
| Compiles but shouldn't run | ` ```no_run ` |
| Can't make it compile | Link to real code instead |
| Macro syntax | ` ```ignore ` with HTML comment explaining why |

### Linking to Test Modules and Functions

```rust
/// See [`test_example`] for actual usage.
///
/// [`test_example`]: crate::tests::test_example
```

Make test module visible to docs:
```rust
#[cfg(any(test, doc))]
pub mod tests;
```

#### Platform-Specific Test Modules

**When you see this warning:**
> "unresolved link to `crate::path::test_module`"
>
> And the module is `#[cfg(test)]` only

**Don't give up on links** — Add conditional visibility instead of using plain text:

```rust
// Before (links won't resolve):
#[cfg(test)]
mod backend_tests;

// After (links resolve in docs):
#[cfg(any(test, doc))]
pub mod backend_tests;

// For platform-specific test modules:
#[cfg(all(any(test, doc), target_os = "linux"))]
pub mod linux_only_tests;
```

**Apply at all levels** — If linking to a nested test module, both parent and child modules need
the visibility change. See `organize-modules` skill for complete patterns.

---

## Checklist

Before committing documentation:

- [ ] High-level concepts at module/trait level (inverted pyramid)
- [ ] All links use reference-style with `crate::` paths
- [ ] All link definitions at bottom of comment blocks
- [ ] Constants use binary/byte literal/decimal (not hex)
- [ ] Hex shown in comments for cross-reference
- [ ] Markdown tables formatted (`cargo rustdoc-fmt`)
- [ ] No broken links (`cargo doc --no-deps`)
- [ ] All code examples compile (`cargo test --doc`)

---

## Supporting Files

| File | Content | When to Read |
|------|---------|--------------|
| `link-patterns.md` | 15 detailed intra-doc link patterns | Writing links to modules, private types, test functions, section headings |
| `constant-conventions.md` | Full human-readable constants guide | Writing byte constants, decision guide |
| `examples.md` | 5 production-quality doc examples | Need to see inverted pyramid in action |
| `rustdoc-formatting.md` | cargo rustdoc-fmt deep dive | Installing, troubleshooting formatter |

---

## Related Commands

| Command | Purpose |
|---------|---------|
| `/docs` | Full documentation check (invokes this skill) |
| `/fix-intradoc-links` | Fix only link issues |
| `/fix-comments` | Fix only constant conventions |
| `/fix-md-tables` | Fix only markdown tables |

---

## Related Skills

- `check-code-quality` - Includes doc verification step
- `organize-modules` - Re-export chains, conditional visibility for doc links
- `run-clippy` - May suggest doc improvements
