---
name: programming-with-rust
description: >
  Write and review Rust code using practices from "Programming with Rust" by Donis Marshall.
  Covers ownership, borrowing, lifetimes, error handling with Result/Option, traits, generics,
  pattern matching, closures, fearless concurrency, and macros. Use when writing Rust, reviewing
  Rust code, or learning Rust idioms. Trigger on: "Rust", "ownership", "borrow checker",
  "lifetimes", "Result", "Option", "traits", "fearless concurrency", ".rs files", "cargo".
---

# Programming with Rust Skill

Apply the practices from Donis Marshall's "Programming with Rust" to review existing code and write new Rust. This skill operates in two modes: **Review Mode** (analyze code for violations of Rust idioms) and **Write Mode** (produce safe, idiomatic Rust from scratch).

## Reference Files

- `ref-01-fundamentals.md` — Ch 1-3: Rust model, tooling, variables, primitives, references
- `ref-02-types-strings.md` — Ch 4-5: String vs &str, formatting, Display/Debug traits
- `ref-03-control-collections.md` — Ch 6-7: Control flow, iterators, arrays, Vec, HashMap
- `ref-04-ownership-lifetimes.md` — Ch 8-10: Ownership, move semantics, borrowing, lifetimes
- `ref-05-functions-errors.md` — Ch 11-12: Functions, Result, Option, panics, custom errors
- `ref-06-structs-generics.md` — Ch 13-14: Structs, impl blocks, generics, bounds
- `ref-07-patterns-closures.md` — Ch 15-16: Pattern matching, closures, Fn/FnMut/FnOnce
- `ref-08-traits.md` — Ch 17: Trait definition, dispatch, supertraits, associated types
- `ref-09-concurrency.md` — Ch 18-19: Threads, channels, Mutex, RwLock, atomics
- `ref-10-advanced.md` — Ch 20-23: Memory, interior mutability, macros, FFI, modules

## How to Use This Skill

**Before responding**, read the reference files relevant to the code's topic. For ownership/borrowing issues read `ref-04`. For error handling read `ref-05`. For a full review, read all files.

---

## Mode 1: Code Review

When the user asks you to **review** Rust code, follow this process:

### Step 1: Read Relevant References
Identify which chapters apply. If unsure, read all reference files.

### Step 2: Analyze the Code

Check these areas in order of severity:

1. **Ownership & Borrowing** (Ch 8, 10): Unnecessary `.clone()` calls? Mutable borrow conflicts? Move semantics misunderstood?
2. **Lifetimes** (Ch 9): Missing or incorrect annotations? Can elision rules eliminate them? `'static` used where a shorter lifetime would do?
3. **Error Handling** (Ch 12): Is `.unwrap()` or `.expect()` used where `?` operator or proper matching belongs? Are custom error types missing where they'd help callers?
4. **Traits & Generics** (Ch 14, 17): Are trait bounds as narrow as possible? Is dynamic dispatch (`dyn Trait`) used where static dispatch (`impl Trait`) is better for performance?
5. **Pattern Matching** (Ch 15): Are `match` arms exhaustive? Can `if let` / `while let` simplify single-arm matches? Are wildcards masking unhandled cases?
6. **Concurrency** (Ch 18, 19): Is shared state protected by `Mutex` or `RwLock`? Are channels used correctly? Is `Arc` used when `Rc` would suffice (single-threaded)?
7. **Memory** (Ch 20): Is `RefCell` used outside of single-threaded interior mutability? Is `Box` used unnecessarily when stack allocation would work?
8. **Idioms**: Is `for item in collection` preferred over manual indexing? Are iterator adapters (`map`, `filter`, `collect`) used over manual loops?

### Step 3: Report Findings
For each issue, report:
- **Chapter reference** (e.g., "Ch 12: Error Handling")
- **Location** in the code
- **What's wrong** (the anti-pattern)
- **How to fix it** (the idiomatic Rust approach)
- **Priority**: Critical (safety/correctness), Important (idiom/maintainability), Suggestion (polish)

### Step 4: Provide Fixed Code
Offer a corrected version with comments explaining each change.

---

## Mode 2: Writing New Code

When the user asks you to **write** new Rust code, apply these core principles:

### Ownership & Memory Safety

1. **Prefer borrowing over cloning** (Ch 8). Pass `&T` or `&mut T` rather than transferring ownership when the caller still needs the value. Clone only when ownership genuinely needs to be duplicated.

2. **Respect the single-owner rule** (Ch 8). Each value has exactly one owner. When you move a value, the old binding is invalid — design data flow around this.

3. **Use lifetime elision** (Ch 9). Annotate lifetimes only when the compiler cannot infer them. Explicit annotations are for structs holding references and functions with multiple reference parameters where elision is ambiguous.

4. **Prefer `&str` over `String` in function parameters** (Ch 4). Accept `&str` to work with both `String` (via deref coercion) and string literals without allocation.

### Error Handling

5. **Return `Result<T, E>`, never panic in library code** (Ch 12). Panics are for unrecoverable programmer errors. Use `Result` for anything that can fail at runtime.

6. **Use the `?` operator for error propagation** (Ch 12). Replace `.unwrap()` chains with `?` to propagate errors cleanly to callers.

7. **Define custom error types for public APIs** (Ch 12). Implement `std::error::Error` and use `thiserror` or manual `impl` to give callers structured errors they can match on.

8. **Never use `.unwrap()` in production paths** (Ch 12). Use `.expect("reason")` only in tests or where panic is truly the right response. In all other cases, handle with `match`, `if let`, or `?`.

### Traits & Generics

9. **Prefer `impl Trait` over `dyn Trait` for return types** (Ch 17). Static dispatch is zero-cost. Use `dyn Trait` only when you need runtime polymorphism with mixed types in a collection.

10. **Use trait bounds instead of concrete types** (Ch 14). `fn process<T: Display + Debug>(item: T)` is more reusable than accepting a concrete type.

11. **Implement standard traits** (Ch 17). Derive `Debug`, `Clone`, `PartialEq` where appropriate. Implement `Display` for user-facing output, `From`/`Into` for conversions.

### Pattern Matching

12. **Use `match` for exhaustive handling** (Ch 15). The compiler enforces exhaustiveness — treat it as a feature, not a burden.

13. **Use `if let` for single-variant matching** (Ch 15). `if let Some(x) = opt { }` is cleaner than a two-arm `match` when you only care about one case.

14. **Destructure in function parameters** (Ch 15). `fn process(&Point { x, y }: &Point)` avoids manual field access inside the body.

### Concurrency

15. **Use channels for message passing** (Ch 18). Prefer `std::sync::mpsc` channels over shared mutable state when threads can communicate by value.

16. **Wrap shared state in `Arc<Mutex<T>>`** (Ch 19). `Arc` for shared ownership across threads, `Mutex` for mutual exclusion. Use `RwLock` when reads vastly outnumber writes.

17. **Prefer `Mutex::lock().unwrap()` with `.expect()`** (Ch 19). Poisoned mutexes indicate a panic in another thread — `.expect("mutex poisoned")` makes this explicit.

### Code Structure Template

```rust
use std::fmt;

/// Domain error type for public APIs (Ch 12)
#[derive(Debug)]
pub enum AppError {
    NotFound(String),
    InvalidInput(String),
    Io(std::io::Error),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::NotFound(msg) => write!(f, "not found: {msg}"),
            AppError::InvalidInput(msg) => write!(f, "invalid input: {msg}"),
            AppError::Io(e) => write!(f, "I/O error: {e}"),
        }
    }
}

impl std::error::Error for AppError {}

impl From<std::io::Error> for AppError {
    fn from(e: std::io::Error) -> Self {
        AppError::Io(e)
    }
}

/// Accept &str, not String (Ch 4)
pub fn find_user(name: &str) -> Result<User, AppError> {
    // Use ? for propagation (Ch 12)
    let data = load_data()?;
    data.iter()
        .find(|u| u.name == name)
        .cloned()  // clone only the found item (Ch 8)
        .ok_or_else(|| AppError::NotFound(name.to_string()))
}

/// Derive standard traits (Ch 17)
#[derive(Debug, Clone, PartialEq)]
pub struct User {
    pub name: String,
    pub role: Role,
}

/// Enum for valid states (Ch 15)
#[derive(Debug, Clone, PartialEq)]
pub enum Role {
    Admin,
    Viewer,
    Editor,
}
```

---

## Priority of Practices by Impact

### Critical (Safety & Correctness)
- Ch 8: Understand ownership — moving vs borrowing, no use-after-move
- Ch 10: One mutable borrow OR many immutable borrows — never both
- Ch 12: Never `.unwrap()` in production; use `Result` and `?`
- Ch 19: Always protect shared mutable state with `Mutex` or `RwLock`

### Important (Idiom & Maintainability)
- Ch 4: Prefer `&str` params over `String`
- Ch 9: Rely on lifetime elision; annotate only when required
- Ch 12: Custom error types for public APIs
- Ch 14/17: Trait bounds over concrete types; `impl Trait` over `dyn Trait`
- Ch 15: Exhaustive `match`; use `if let` for single-arm cases
- Ch 17: Derive/implement standard traits (`Debug`, `Display`, `From`)

### Suggestions (Polish)
- Ch 6: Use iterator adapters (`map`, `filter`, `flat_map`) over manual loops
- Ch 16: Use closures with `move` when capturing environment across thread boundaries
- Ch 20: Prefer stack allocation; use `Box` only when size is unknown at compile time
- Ch 21: Use `derive` macros before writing manual `impl` blocks
