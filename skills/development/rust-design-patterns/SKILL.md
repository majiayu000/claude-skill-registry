---
name: rust-design-patterns
description: "Rust idioms and design patterns for writing idiomatic code. Use when: (1) Writing new Rust code, (2) Reviewing Rust code, (3) Solving borrow checker issues, (4) Designing Rust APIs. Triggers on: Rust ownership problems, lifetime errors, API design questions, 'how to do X idiomatically in Rust'."
user-invocable: false
---

# Rust Design Patterns

Idioms and patterns for writing idiomatic Rust code. Focus on Rust-specific patterns that leverage ownership, borrowing, and the type system.

## Decision Tree

```
Problem?
├── Borrow checker error?
│   ├── Need to move value from &mut enum → mem::take/replace
│   ├── Need independent field borrows → struct decomposition
│   ├── Tempted to clone? → Check: Rc/Arc? Or refactor ownership?
│   └── Lifetime too short → consider owned types or 'static
│
├── API design?
│   ├── Many constructor params → Builder pattern
│   ├── Accept flexible input → Borrowed types (&str, &[T])
│   ├── Type safety at compile time → Newtype pattern
│   ├── Default values needed → Default trait + struct update syntax
│   └── Resource cleanup needed → RAII guards (Drop trait)
│
├── FFI boundary?
│   ├── Error handling → Integer codes + error description fn
│   ├── String passing → CString/CStr patterns
│   └── Object lifetime → Opaque pointers with explicit free
│
├── Unsafe code?
│   ├── Need unsafe operations → Contain in small modules with safe wrappers
│   └── FFI types → Type consolidation into opaque wrappers
│
└── Performance concern?
    ├── Avoid monomorphization bloat → On-stack dynamic dispatch
    └── Reduce allocations → mem::take instead of clone
```

## Quick Patterns

### Borrowed Types (CRITICAL)

Prefer `&str` over `&String`, `&[T]` over `&Vec<T>`:

```rust
// Bad: only accepts &String
fn process(s: &String) { }

// Good: accepts &String, &str, string literals
fn process(s: &str) { }

// Usage: all work with &str
process(&my_string);      // String
process("literal");       // &'static str
process(&my_string[1..5]); // slice
```

**Why**: Deref coercion allows `&String` → `&str`, but not reverse. Using borrowed types accepts more input types.

### mem::take Pattern (CRITICAL)

Move owned values out of `&mut` without clone:

```rust
use std::mem;

enum State {
    Active { data: String },
    Inactive,
}

fn deactivate(state: &mut State) {
    if let State::Active { data } = state {
        // Take ownership without clone
        let owned_data = mem::take(data);
        *state = State::Inactive;
        // use owned_data...
    }
}
```

**When**: Changing enum variants while keeping owned inner data. Avoids clone anti-pattern.

### Newtype Pattern

Type safety with zero runtime cost:

```rust
// Distinct types prevent mixing
struct UserId(u64);
struct OrderId(u64);

fn get_order(user: UserId, order: OrderId) { }

// Compile error: can't mix up IDs
// get_order(order_id, user_id);
```

**When**: Need compile-time distinction between same underlying types, or custom trait implementations.

### Builder Pattern

For complex construction:

```rust
#[derive(Default)]
struct RequestBuilder {
    url: String,
    timeout: Option<u32>,
    headers: Vec<(String, String)>,
}

impl RequestBuilder {
    fn url(mut self, url: impl Into<String>) -> Self {
        self.url = url.into();
        self
    }

    fn timeout(mut self, ms: u32) -> Self {
        self.timeout = Some(ms);
        self
    }

    fn build(self) -> Request {
        Request { /* ... */ }
    }
}

// Usage
let req = RequestBuilder::default()
    .url("https://example.com")
    .timeout(5000)
    .build();
```

**When**: Many optional parameters, or construction has validation/side effects.

### RAII Guards

Resource management through ownership:

```rust
struct FileGuard {
    file: File,
}

impl Drop for FileGuard {
    fn drop(&mut self) {
        // Cleanup runs automatically when guard goes out of scope
        self.file.sync_all().ok();
    }
}

fn process() -> Result<()> {
    let guard = FileGuard { file: File::open("data.txt")? };
    // Even with early return or panic, Drop runs
    do_work()?;
    Ok(())
} // guard.drop() called here
```

**When**: Need guaranteed cleanup (locks, files, connections, transactions).

### Default + Struct Update

Partial initialization with defaults:

```rust
#[derive(Default)]
struct Config {
    host: String,
    port: u16,
    timeout: u32,
    retries: u8,
}

let config = Config {
    host: "localhost".into(),
    port: 8080,
    ..Default::default()  // timeout=0, retries=0
};
```

### On-Stack Dynamic Dispatch

Avoid heap allocation for trait objects:

```rust
use std::io::{self, Read};

fn process(use_stdin: bool) -> io::Result<String> {
    let readable: &mut dyn Read = if use_stdin {
        &mut io::stdin()
    } else {
        &mut std::fs::File::open("input.txt")?
    };

    let mut buf = String::new();
    readable.read_to_string(&mut buf)?;
    Ok(buf)
}
```

**When**: Need dynamic dispatch without Box allocation. Since Rust 1.79, lifetime extension makes this ergonomic.

### Option as Iterator

`Option` implements `IntoIterator` (0 or 1 element):

```rust
let maybe_name = Some("Turing");
let mut names = vec!["Curry", "Kleene"];

// Extend with Option
names.extend(maybe_name);

// Chain with Option
for name in names.iter().chain(maybe_name.iter()) {
    println!("{name}");
}
```

**Tip**: For always-`Some`, prefer `std::iter::once(value)`.

### Closure Capture Control

Control what closures capture via rebinding:

```rust
use std::rc::Rc;

let num1 = Rc::new(1);
let num2 = Rc::new(2);

let closure = {
    let num2 = num2.clone();  // clone before move
    let num1 = num1.as_ref(); // borrow
    move || { *num1 + *num2 }
};
// num1 still usable, num2 was cloned
```

### Temporary Mutability

Make variable immutable after setup:

```rust
// Method 1: Nested block
let data = {
    let mut data = get_vec();
    data.sort();
    data
};
// data is immutable here

// Method 2: Rebinding
let mut data = get_vec();
data.sort();
let data = data;  // now immutable
```

### Return Consumed Argument on Error

If function consumes argument, return it in error for retry:

```rust
pub struct SendError(pub String);  // contains the original value

pub fn send(value: String) -> Result<(), SendError> {
    if can_send() {
        do_send(&value);
        Ok(())
    } else {
        Err(SendError(value))  // caller can retry
    }
}

// Usage: retry loop without clone
let mut msg = "hello".to_string();
loop {
    match send(msg) {
        Ok(()) => break,
        Err(SendError(m)) => { msg = m; }  // recover and retry
    }
}
```

**Example**: `String::from_utf8` returns `FromUtf8Error` containing original `Vec<u8>`.

## Anti-Patterns Checklist

Review code for these common mistakes:

- [ ] **Clone to satisfy borrow checker** - Usually indicates ownership design issue. Consider `mem::take`, `Rc`/`Arc`, or refactoring.

- [ ] **`#![deny(warnings)]` in library** - Breaks downstream on new Rust versions. Use `RUSTFLAGS="-D warnings"` in CI instead.

- [ ] **Deref for inheritance** - Surprising behavior, doesn't provide true subtyping. Use composition + delegation or traits.

- [ ] **`&String` or `&Vec<T>` in function params** - Use `&str` or `&[T]` for flexibility.

- [ ] **Manual `drop()` calls** - Usually unnecessary. If needed for ordering, prefer scoped blocks.

- [ ] **Ignoring clippy suggestions for `.clone()`** - Run `cargo clippy` to find unnecessary clones.

## References

For detailed patterns with full examples:

- **[ownership-patterns.md](references/ownership-patterns.md)** - Borrow checker patterns: mem::take/replace, struct decomposition, RAII guards, Rc/Arc decisions
- **[api-design.md](references/api-design.md)** - API patterns: borrowed types, builders, newtype, Default trait, FFI
- **[common-pitfalls.md](references/common-pitfalls.md)** - Anti-patterns in detail: clone abuse, deny(warnings), Deref polymorphism
