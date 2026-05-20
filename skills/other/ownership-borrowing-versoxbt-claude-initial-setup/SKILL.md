---
name: ownership-borrowing
description: >
  Master Rust's ownership, borrowing, and lifetime system for memory-safe code.
  Use when the user encounters borrow checker errors, lifetime annotations,
  needs smart pointers (Box/Rc/Arc), works with move semantics, or asks about
  Clone vs Copy, ownership transfer, and reference management in Rust.
---

# Rust Ownership and Borrowing

Understand and apply Rust's ownership system to write memory-safe code without
a garbage collector. Master borrowing rules, lifetimes, and smart pointers.

## When to Use
- Encountering borrow checker errors ("cannot borrow as mutable")
- Deciding between references, cloning, and moving
- Adding lifetime annotations to structs or functions
- Choosing between Box, Rc, Arc for heap allocation and sharing
- Understanding when to derive Clone vs Copy

## Core Patterns

### Pattern 1: Ownership Rules

Three rules govern all Rust memory:
1. Each value has exactly one owner.
2. When the owner goes out of scope, the value is dropped.
3. Ownership can be transferred (moved) but not duplicated (unless Copy).

```rust
fn main() {
    let name = String::from("Alice"); // name owns the String
    let greeting = greet(name);       // ownership moves to greet
    // println!("{name}");            // ERROR: name was moved
    println!("{greeting}");
}

fn greet(name: String) -> String {    // takes ownership
    format!("Hello, {name}!")         // returns a new owned String
}
```

### Pattern 2: Borrowing -- Shared and Mutable References

Borrow data without taking ownership. Two rules:
- Any number of shared references (`&T`) OR exactly one mutable reference (`&mut T`).
- References must always be valid (no dangling pointers).

```rust
fn analyze(data: &[i32]) -> (i32, i32) {
    // Shared borrow: can read, cannot modify
    let sum: i32 = data.iter().sum();
    let count = data.len() as i32;
    (sum, count)
}

fn normalize(data: &mut Vec<f64>) {
    // Mutable borrow: can read and modify
    let max = data.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    if max != 0.0 {
        for val in data.iter_mut() {
            *val /= max;
        }
    }
}

fn main() {
    let mut values = vec![1.0, 2.0, 3.0];
    normalize(&mut values);     // mutable borrow
    let (sum, _) = analyze(&[1, 2, 3]); // shared borrow
    println!("{sum}");
}
```

### Pattern 3: Lifetimes

Lifetimes tell the compiler how long references are valid. Most are inferred;
annotate when the compiler cannot determine the relationship.

```rust
// The returned reference lives as long as the shortest input lifetime
fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {
    if a.len() >= b.len() { a } else { b }
}

// Lifetime in structs: the struct cannot outlive the referenced data
struct Excerpt<'a> {
    text: &'a str,
}

impl<'a> Excerpt<'a> {
    fn first_word(&self) -> &'a str {
        self.text.split_whitespace().next().unwrap_or("")
    }
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago...");
    let excerpt = Excerpt {
        text: novel.split('.').next().unwrap(),
    };
    println!("{}", excerpt.first_word());
}
```

### Pattern 4: Smart Pointers

Use smart pointers when ownership rules need more flexibility.

```rust
// Box<T>: heap allocation, single owner
fn build_tree() -> Box<Node> {
    Box::new(Node {
        value: 1,
        left: Some(Box::new(Node { value: 2, left: None, right: None })),
        right: Some(Box::new(Node { value: 3, left: None, right: None })),
    })
}

// Rc<T>: shared ownership, single-threaded (reference counted)
use std::rc::Rc;

fn shared_config() {
    let config = Rc::new(AppConfig::default());
    let service_a = Service::new(Rc::clone(&config));
    let service_b = Service::new(Rc::clone(&config));
    // Both services share the same config; dropped when last Rc is dropped
}

// Arc<T>: shared ownership, thread-safe (atomic reference counted)
use std::sync::Arc;

fn concurrent_cache() {
    let cache = Arc::new(Mutex::new(HashMap::new()));

    let handles: Vec<_> = (0..4)
        .map(|i| {
            let cache = Arc::clone(&cache);
            std::thread::spawn(move || {
                cache.lock().unwrap().insert(i, i * 10);
            })
        })
        .collect();

    for h in handles {
        h.join().unwrap();
    }
}
```

### Pattern 5: Clone vs Copy

`Copy`: bitwise copy, implicit, for small stack types (integers, bools, tuples of Copy types).
`Clone`: explicit `.clone()`, for types that need deep duplication.

```rust
// Copy: automatically duplicated on assignment
let x: i32 = 42;
let y = x;      // x is copied, both x and y are valid
println!("{x} {y}");

// Clone: explicit duplication
let a = String::from("hello");
let b = a.clone(); // deep copy -- both a and b are valid
println!("{a} {b}");

// Without clone, a would be moved:
let c = String::from("world");
let d = c;        // c is MOVED to d
// println!("{c}"); // ERROR: c was moved

// Derive both when your struct contains only Copy types
#[derive(Debug, Clone, Copy)]
struct Point {
    x: f64,
    y: f64,
}
```

### Pattern 6: Common Borrow Checker Patterns

Solutions to frequent borrow checker issues.

```rust
// Problem: cannot borrow as mutable because also borrowed as immutable
// Solution: limit the scope of the immutable borrow
fn update_map(map: &mut HashMap<String, Vec<i32>>, key: &str) {
    // Use entry API to avoid double-borrow
    map.entry(key.to_string())
        .or_insert_with(Vec::new)
        .push(42);
}

// Problem: returning a reference to a local variable
// Solution: return owned data
fn create_greeting(name: &str) -> String {
    // Return owned String, not &str
    format!("Hello, {name}!")
}

// Problem: self-referential struct
// Solution: use indices instead of references, or use Pin
struct Document {
    content: String,
    // Instead of &str references into content, store byte offsets
    highlights: Vec<(usize, usize)>,
}

impl Document {
    fn highlighted_text(&self, idx: usize) -> &str {
        let (start, end) = self.highlights[idx];
        &self.content[start..end]
    }
}
```

## Anti-Patterns

- **Cloning to silence the borrow checker** -- `.clone()` everywhere is a sign of
  misunderstood ownership. Restructure code to use borrows instead.

- **Unnecessary `Arc<Mutex<T>>`** -- Only use Arc when data is shared across threads.
  Single-threaded code should use Rc or plain ownership.

- **Lifetime annotations on everything** -- Let the compiler infer lifetimes. Only
  annotate when the compiler asks or when the relationship is ambiguous.

- **Returning references from functions that create data** -- Functions that allocate
  must return owned types. References can only point to data that outlives them.

## Quick Reference

| Type | Ownership | Thread-safe | Heap | Use Case |
|------|-----------|-------------|------|----------|
| `T` | Sole owner | N/A | Stack* | Default |
| `&T` | Shared borrow | Yes (if T: Sync) | No | Read access |
| `&mut T` | Exclusive borrow | No | No | Write access |
| `Box<T>` | Sole owner | N/A | Yes | Large/recursive types |
| `Rc<T>` | Shared | No | Yes | Single-thread sharing |
| `Arc<T>` | Shared | Yes | Yes | Multi-thread sharing |

Move vs Copy: types implementing `Copy` are duplicated on assignment; all others are moved.
