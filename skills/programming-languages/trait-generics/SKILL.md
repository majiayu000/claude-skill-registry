---
name: trait-generics
description: Master Rust traits, generics, and type system
sasmp_version: "1.3.0"
bonded_agent: rust-type-system-agent
bond_type: PRIMARY_BOND
version: "1.0.0"
---

# Traits & Generics Skill

Master Rust's powerful type system with traits and generics.

## Quick Start

### Defining Traits

```rust
pub trait Summary {
    // Required method
    fn summarize(&self) -> String;

    // Default implementation
    fn preview(&self) -> String {
        format!("Read more: {}", self.summarize())
    }
}
```

### Implementing Traits

```rust
struct Article {
    title: String,
    author: String,
    content: String,
}

impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{} by {}", self.title, self.author)
    }
}
```

### Generic Functions

```rust
// impl Trait syntax
fn print_summary(item: &impl Summary) {
    println!("{}", item.summarize());
}

// Trait bound syntax
fn print_summary<T: Summary>(item: &T) {
    println!("{}", item.summarize());
}

// Multiple bounds
fn process<T: Summary + Clone>(item: &T) {
    let copy = item.clone();
    println!("{}", copy.summarize());
}

// Where clause
fn complex<T, U>(t: T, u: U)
where
    T: Summary + Clone,
    U: std::fmt::Debug,
{
    // ...
}
```

### Generic Structs

```rust
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn new(x: T, y: T) -> Self {
        Point { x, y }
    }
}

// Specific implementations
impl Point<f64> {
    fn distance(&self) -> f64 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}
```

## Common Patterns

### Static vs Dynamic Dispatch

```rust
// Static dispatch (monomorphization, zero-cost)
fn process_static(item: &impl Summary) {
    println!("{}", item.summarize());
}

// Dynamic dispatch (trait object, runtime cost)
fn process_dynamic(item: &dyn Summary) {
    println!("{}", item.summarize());
}

// Collection of different types
let items: Vec<Box<dyn Summary>> = vec![
    Box::new(article),
    Box::new(tweet),
];
```

### Associated Types

```rust
trait Container {
    type Item;

    fn get(&self, index: usize) -> Option<&Self::Item>;
}

impl<T> Container for Vec<T> {
    type Item = T;

    fn get(&self, index: usize) -> Option<&Self::Item> {
        <[T]>::get(self, index)
    }
}
```

### Operator Overloading

```rust
use std::ops::Add;

#[derive(Debug, Copy, Clone)]
struct Point {
    x: i32,
    y: i32,
}

impl Add for Point {
    type Output = Point;

    fn add(self, other: Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

let p3 = p1 + p2;  // Uses Add trait
```

## Derivable Traits

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
struct Config {
    timeout: u64,
    retries: u32,
}
```

| Trait | Purpose |
|-------|---------|
| Debug | {:?} formatting |
| Clone | Explicit deep copy |
| Copy | Implicit bitwise copy |
| PartialEq | == comparison |
| Eq | Total equality |
| Hash | Use in HashMap |
| Default | Default::default() |

## Resources

- [Rust Book Ch.10](https://doc.rust-lang.org/book/ch10-00-generics.html)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
