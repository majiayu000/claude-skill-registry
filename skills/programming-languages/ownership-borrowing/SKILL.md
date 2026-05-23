---
name: ownership-borrowing
description: Master Rust's ownership, borrowing, and lifetime system
sasmp_version: "1.3.0"
bonded_agent: rust-fundamentals-agent
bond_type: PRIMARY_BOND
version: "1.0.0"
---

# Ownership & Borrowing Skill

Master Rust's revolutionary memory safety system without garbage collection.

## Quick Start

### The Three Rules of Ownership

```rust
// Rule 1: Each value has exactly ONE owner
let s1 = String::from("hello");  // s1 owns this String

// Rule 2: Only ONE owner at a time
let s2 = s1;  // Ownership MOVES to s2
// println!("{}", s1);  // ERROR: s1 no longer valid

// Rule 3: Value is dropped when owner goes out of scope
{
    let s3 = String::from("temporary");
}  // s3 dropped here, memory freed
```

### Borrowing Basics

```rust
fn main() {
    let s = String::from("hello");

    // Immutable borrow
    let len = calculate_length(&s);
    println!("{} has length {}", s, len);

    // Mutable borrow
    let mut s = String::from("hello");
    change(&mut s);
    println!("{}", s);  // "hello, world"
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn change(s: &mut String) {
    s.push_str(", world");
}
```

### Lifetime Annotations

```rust
// Explicit lifetime annotation
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct with lifetime
struct Excerpt<'a> {
    part: &'a str,
}
```

## Common Patterns

### Pattern 1: Clone When Needed

```rust
let s1 = String::from("hello");
let s2 = s1.clone();  // Deep copy
println!("{} {}", s1, s2);  // Both valid
```

### Pattern 2: Return Ownership

```rust
fn process(s: String) -> String {
    // Do something with s
    s  // Return ownership
}
```

### Pattern 3: Borrow for Read-Only

```rust
fn analyze(data: &Vec<i32>) -> Summary {
    // Only read, don't own
    Summary::from(data)
}
```

## Error Solutions

### "value borrowed after move"

```rust
// Problem
let s = String::from("hello");
let s2 = s;
println!("{}", s);  // ERROR

// Solution 1: Clone
let s2 = s.clone();

// Solution 2: Borrow
let s2 = &s;
```

### "cannot borrow as mutable"

```rust
// Problem
let s = String::from("hello");
change(&mut s);  // ERROR: s is not mut

// Solution: Declare as mutable
let mut s = String::from("hello");
change(&mut s);  // OK
```

## Resources

- [Rust Book Ch.4](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)
- [Rust by Example: Ownership](https://doc.rust-lang.org/rust-by-example/scope/move.html)
