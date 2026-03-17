---
name: rust-developer
description: Comprehensive Rust development guidelines based on 6 months of code reviews. Use when writing Rust code, debugging Rust issues, or reviewing Rust PRs. Covers error handling, file I/O safety, type safety patterns, performance optimization, common footguns, and fundamental best practices. Perfect for both new and experienced Rust developers working on CLI tools, hooks, or production code.
---

# Rust Developer Guide

## Purpose

Provides comprehensive Rust development best practices learned from 6 months of code reviews across the Catalyst project. Helps avoid common mistakes, write idiomatic Rust, and build safe, performant production code.

## When to Use This Skill

Automatically activates when you:
- Write or modify Rust code (`.rs` files)
- Debug Rust compiler errors or warnings
- Review Rust pull requests
- Ask about Rust best practices
- Implement CLI tools or hooks
- Work with error handling, file I/O, or type safety
- Optimize Rust code for performance
- Question Rust patterns or idioms

---

## Quick Start

**New to Rust or this codebase?**
Start with [Quick Reference Checklist](../../../docs/rust-lessons/quick-reference.md) - Scannable checklist of all 20+ rules

**Working on specific topic?**
Jump to the relevant resource file below

**Made a specific mistake?**
Check [Common Footguns](../../../docs/rust-lessons/common-footguns.md)

**Writing production code?**
Review [Error Handling Deep Dive](../../../docs/rust-lessons/error-handling-deep-dive.md) first

---

## Resource Files

### Quick Reference (Start Here)

**[quick-reference.md](../../../docs/rust-lessons/quick-reference.md)** - 400-line scannable checklist

- All 20+ lessons in one place
- Rule + Quick check + Example + Link to deep dive
- Perfect for code review or quick lookup
- Can be scanned in under 2 minutes

### Additional Patterns

**[rust-patterns.md](rust-patterns.md)** - ~555 lines

**When to use:**
- Choosing between thiserror and anyhow
- Input validation at boundaries
- Concurrent database access
- Preventing SQL injection
- Ownership patterns (borrow vs owned)
- Testing error paths

**Topics covered:**
- thiserror vs anyhow (when to use each)
- Input validation with validator crate
- Arc<Mutex<T>> for thread-safe shared state
- Parameterized queries for SQL injection prevention
- Ownership patterns (borrow params, return owned)
- Testing error paths explicitly
- Match-based error classification

**Skill level:** Intermediate

**Complements:** Error Handling, Type Safety, Common Footguns

---

### Deep-Dive Guides (Comprehensive Learning)

#### 1. Fundamentals
**[fundamentals-deep-dive.md](../../../docs/rust-lessons/fundamentals-deep-dive.md)** - ~450 lines

**When to use:**
- Setting up a new Rust project
- Organizing imports and dependencies
- Setting up tracing/logging
- First-time Rust contributor

**Topics covered:**
- Imports and code organization
- Tracing subscribers (avoid duplicated setup)
- CLI user feedback patterns
- TTY detection for colored output
- Avoiding duplicated logic

**Skill level:** Beginner

---

#### 2. Error Handling
**[error-handling-deep-dive.md](../../../docs/rust-lessons/error-handling-deep-dive.md)** - ~600 lines

**When to use:**
- Using `Option<T>` or `Result<T, E>`
- Deciding between `unwrap()`, `expect()`, and `?`
- Path operations that can fail
- Converting between error types

**Topics covered:**
- Option handling patterns (unwrap_or, unwrap_or_else, map_or)
- Result handling and error propagation
- When to use expect() vs unwrap() vs ?
- Path operation footguns (display().to_string())
- Context with anyhow or thiserror

**Skill level:** Beginner/Intermediate

---

#### 3. File I/O Safety
**[file-io-deep-dive.md](../../../docs/rust-lessons/file-io-deep-dive.md)** - ~500 lines

**When to use:**
- Writing files (especially config/state files)
- Creating directories
- Working with temporary files
- Testing file operations

**Topics covered:**
- Atomic file writes with tempfile crate
- Parent directory creation patterns
- NamedTempFile usage
- Testing file I/O (in-memory, temp dirs)
- Avoiding TOCTOU races

**Skill level:** Intermediate

---

#### 4. Type Safety
**[type-safety-deep-dive.md](../../../docs/rust-lessons/type-safety-deep-dive.md)** - ~650 lines

**When to use:**
- Validating string inputs
- Designing APIs with constrained values
- Providing user-friendly error messages
- Converting magic strings to types

**Topics covered:**
- Constants → Enums progression
- Newtype pattern for preventing type confusion
- Validation at boundaries
- User-friendly error messages
- "Did you mean?" suggestions with edit distance
- Pattern matching for exhaustiveness

**Skill level:** Intermediate

---

#### 5. Performance Optimization
**[performance-deep-dive.md](../../../docs/rust-lessons/performance-deep-dive.md)** - ~450 lines

**When to use:**
- Optimizing hot paths
- Processing large datasets
- Reducing allocations
- Profiling performance bottlenecks

**Topics covered:**
- Loop optimizations (pre-allocation, iteration patterns)
- Zero-copy abstractions (AsRef, Borrow, Cow)
- Pre-compilation patterns (static regexes, lazy_static)
- Performance profiling tools
- Benchmarking with criterion

**Skill level:** Intermediate/Advanced

---

#### 6. Common Footguns
**[common-footguns.md](../../../docs/rust-lessons/common-footguns.md)** - ~400 lines

**When to use:**
- Debugging borrow checker errors
- Path operation failures
- Race conditions in file operations
- Unexpected behavior in production

**Topics covered:**
- Path operations (display().to_string() vs to_path_buf())
- TOCTOU (Time-of-Check-Time-of-Use) races
- Borrow checker with HashSet and collections
- Common pitfalls and how to avoid them

**Skill level:** Mixed (Beginner through Advanced)

---

## Learning Paths

### Path 1: Beginner (First PRs)

Recommended reading order for new Rust developers:

1. **[Fundamentals](../../../docs/rust-lessons/fundamentals-deep-dive.md)**
   - Imports and code organization
   - Tracing subscribers
   - Avoiding duplicated logic

2. **[Error Handling](../../../docs/rust-lessons/error-handling-deep-dive.md)** (Sections 1-2)
   - Option handling basics
   - When to use expect vs unwrap

3. **[Quick Reference](../../../docs/rust-lessons/quick-reference.md)**
   - Scan all rules to build awareness

**Goal:** Avoid the most common beginner mistakes

---

### Path 2: Intermediate (Production Code)

For developers writing production-quality Rust:

1. **[Error Handling](../../../docs/rust-lessons/error-handling-deep-dive.md)** (Complete)
   - All Option/Result patterns
   - Path operation footguns

2. **[Rust Patterns](rust-patterns.md)** (NEW!)
   - thiserror vs anyhow
   - Input validation
   - Ownership patterns
   - Arc<Mutex<T>> for concurrency
   - SQL injection prevention
   - Testing error paths

3. **[File I/O Safety](../../../docs/rust-lessons/file-io-deep-dive.md)**
   - Atomic writes
   - Safe file operations
   - Testing file I/O

4. **[Type Safety](../../../docs/rust-lessons/type-safety-deep-dive.md)**
   - Constants → Enums progression
   - Validation patterns
   - User-friendly errors

5. **[Common Footguns](../../../docs/rust-lessons/common-footguns.md)**
   - TOCTOU races
   - Borrow checker patterns

**Goal:** Write robust, safe production code

---

### Path 3: Advanced (Performance & Safety)

For optimizing critical code paths:

1. **[Performance](../../../docs/rust-lessons/performance-deep-dive.md)**
   - Loop optimizations
   - Zero-copy abstractions
   - Profiling techniques

2. **[Common Footguns](../../../docs/rust-lessons/common-footguns.md)**
   - Borrow checker with collections
   - Advanced safety patterns

3. Review all deep-dives for edge cases

**Goal:** Maximize performance while maintaining safety

---

## Code Review Checklist

When reviewing Rust PRs, check against:

1. **[Quick Reference](../../../docs/rust-lessons/quick-reference.md)** - All 20+ rules
2. **Error Handling** - Are Options/Results handled safely?
3. **File I/O** - Are writes atomic? Are parent dirs created?
4. **Type Safety** - Are magic strings replaced with enums?
5. **Performance** - Are hot paths optimized? Pre-allocated?
6. **Common Footguns** - Any TOCTOU races? Path operations safe?

---

## Quick Topic Lookup

| Topic | Resource |
|-------|----------|
| **anyhow vs thiserror** | [Rust Patterns](rust-patterns.md) |
| **Arc<Mutex<T>> Pattern** | [Rust Patterns](rust-patterns.md) |
| **Atomic File Writes** | [File I/O Deep Dive](../../../docs/rust-lessons/file-io-deep-dive.md) |
| **Borrow Checker Issues** | [Common Footguns](../../../docs/rust-lessons/common-footguns.md) |
| **CLI User Feedback** | [Fundamentals](../../../docs/rust-lessons/fundamentals-deep-dive.md) |
| **Concurrent Database Access** | [Rust Patterns](rust-patterns.md) |
| **Error Classification** | [Rust Patterns](rust-patterns.md) |
| **Error Handling Patterns** | [Error Handling Deep Dive](../../../docs/rust-lessons/error-handling-deep-dive.md) |
| **Enums vs Strings** | [Type Safety Deep Dive](../../../docs/rust-lessons/type-safety-deep-dive.md) |
| **expect() vs unwrap()** | [Error Handling Deep Dive](../../../docs/rust-lessons/error-handling-deep-dive.md) |
| **Newtype Pattern** | [Type Safety Deep Dive](../../../docs/rust-lessons/type-safety-deep-dive.md) |
| **Input Validation** | [Rust Patterns](rust-patterns.md) |
| **Loop Optimizations** | [Performance Deep Dive](../../../docs/rust-lessons/performance-deep-dive.md) |
| **Option Handling** | [Error Handling Deep Dive](../../../docs/rust-lessons/error-handling-deep-dive.md) |
| **Ownership Patterns** | [Rust Patterns](rust-patterns.md) |
| **Path Operations** | [Common Footguns](../../../docs/rust-lessons/common-footguns.md) |
| **Performance Profiling** | [Performance Deep Dive](../../../docs/rust-lessons/performance-deep-dive.md) |
| **SQL Injection Prevention** | [Rust Patterns](rust-patterns.md) |
| **Testing Error Paths** | [Rust Patterns](rust-patterns.md) |
| **TOCTOU Races** | [Common Footguns](../../../docs/rust-lessons/common-footguns.md) |
| **Tracing Setup** | [Fundamentals](../../../docs/rust-lessons/fundamentals-deep-dive.md) |
| **Validation Patterns** | [Type Safety Deep Dive](../../../docs/rust-lessons/type-safety-deep-dive.md) |

---

## Example Project Patterns

> **Note:** The following patterns are examples from a real project. Adapt them to your own project structure.

### Project Structure Example

```
my-project/
├── my-project-core/       # Core library (shared logic)
│   ├── src/
│   │   └── lib.rs
│   └── Cargo.toml
└── my-project-cli/        # CLI binaries (hooks, tools)
    ├── src/bin/
    │   ├── file_analyzer.rs
    │   ├── skill_activation_prompt.rs
    │   └── settings_manager.rs
    └── Cargo.toml
```

### Common Patterns

**Binary Structure:**
```rust
use thiserror::Error;
use tracing::{debug, error};

#[derive(Error, Debug)]
enum MyError {
    #[error("[CODE] {message}\n{context}")]
    SomeError { message: String, context: String },
}

fn run() -> Result<(), MyError> {
    // Initialize tracing (do once in main, not in libraries)
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .init();

    // Business logic here
    Ok(())
}

fn main() {
    if let Err(e) = run() {
        eprintln!("Error: {}", e);
        std::process::exit(1);
    }
}
```

**Custom Error Types with thiserror:**
```rust
#[derive(Error, Debug)]
enum ToolError {
    #[error("[ERR001] File not found: {}\nTry: touch {}", path.display(), path.display())]
    FileNotFound { path: PathBuf },

    #[error("[ERR002] {0}")]
    Io(#[from] std::io::Error),
}
```

**Structured Logging:**
```rust
error!(
    error_code = "ERR001",
    error_kind = "FileNotFound",
    path = %path.display(),
    "File operation failed"
);
```

---

## When to Use This Skill

This skill is useful when:

1. **File Triggers:**
   - Editing any `.rs` file in the project
   - Creating new Rust binaries or libraries
   - Modifying `Cargo.toml` files

2. **Prompt Triggers:**
   - Mentioning "Rust", "cargo", "rustc"
   - Asking about error handling, Option, Result
   - Discussing performance optimizations
   - Requesting code reviews for Rust

3. **Content Triggers:**
   - Code contains Rust-specific patterns (Result, Option, impl, trait)
   - Working with thiserror, anyhow, serde
   - Using Rust ecosystem crates

---

## Contributing New Lessons

Found a new Rust footgun or best practice? See:

**[CONTRIBUTING.md](../../../docs/rust-lessons/CONTRIBUTING.md)** - Complete guide for adding lessons

Quick steps:
1. Add to appropriate deep-dive guide
2. Update [quick-reference.md](../../../docs/rust-lessons/quick-reference.md)
3. Maintain cross-references
4. Include before/after examples

---

## Version History

**Current Version:** 1.0
**Based on:** Rust Lessons Learned v2.0 (6 months of code reviews, Phases 0-2.6)
**Last Updated:** 2025-11-02
**Maintainer:** Catalyst Project Team

---

## Quick Links

- 🚀 **[Quick Reference Checklist](../../../docs/rust-lessons/quick-reference.md)** - Start here
- 📚 **[All Deep-Dive Guides](../../../docs/rust-lessons/)** - Comprehensive learning
- 🔍 **[Common Footguns](../../../docs/rust-lessons/common-footguns.md)** - Avoid mistakes
- 📖 **[Navigation Guide](../../../docs/rust-lessons/index.md)** - Full documentation index

---

**Ready to write better Rust?** Start with the [Quick Reference →](../../../docs/rust-lessons/quick-reference.md)
