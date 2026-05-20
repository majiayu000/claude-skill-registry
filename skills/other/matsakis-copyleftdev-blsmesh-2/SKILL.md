---
name: matsakis-ownership-mastery
description: Write Rust code in the style of Niko Matsakis, Rust language team lead. Emphasizes deep understanding of ownership, lifetimes, and the borrow checker. Use when working with complex lifetime scenarios or designing APIs that interact with the ownership system.
---

# Niko Matsakis Style Guide

## Overview

Niko Matsakis is the architect of Rust's borrow checker and a driving force behind the language's type system. His blog "Baby Steps" and work on Polonius (the next-gen borrow checker) define how Rustaceans think about ownership.

## Core Philosophy

> "The borrow checker is not your enemy—it's your pair programmer."

> "Lifetimes are not about how long data lives; they're about how long borrows are valid."

Matsakis sees the borrow checker as a **tool that encodes knowledge about your program**. Fighting it usually means your mental model is wrong.

## Design Principles

1. **Trust the Borrow Checker**: It knows things about your code you haven't realized yet.

2. **Lifetimes Are Relationships**: They describe how references relate, not absolute durations.

3. **Ownership Shapes APIs**: Good APIs make ownership transfer obvious.

4. **Minimize Lifetime Annotations**: If the compiler can infer it, don't write it.

## When Writing Code

### Always

- Understand why the borrow checker rejects code before "fixing" it
- Use lifetime elision rules—don't annotate unnecessarily
- Design structs with ownership in mind
- Prefer owned types in structs, borrowed in function parameters
- Use `'_` (anonymous lifetime) when you don't care about the specific lifetime

### Never

- Add `'static` just to make code compile
- Use `Rc<RefCell<T>>` as a first resort (it's a last resort)
- Clone to avoid borrow checker errors without understanding why
- Create self-referential structs naively

### Prefer

- `&T` parameters over `T` for read-only access
- `&mut T` over `RefCell<T>` when possible
- Returning owned values over returning references (usually)
- Splitting borrows instead of fighting the checker
- NLL (non-lexical lifetimes) patterns

## Code Patterns

### Understanding Lifetime Elision

```rust
// Lifetime elision rules mean you rarely write explicit lifetimes

// Rule 1: Each elided lifetime in input gets its own parameter
fn print(s: &str) { }  // Actually: fn print<'a>(s: &'a str)

// Rule 2: If there's exactly one input lifetime, it's assigned to all outputs
fn first_word(s: &str) -> &str { }  // Actually: fn first_word<'a>(s: &'a str) -> &'a str

// Rule 3: If there's &self or &mut self, its lifetime is assigned to outputs
impl MyStruct {
    fn method(&self) -> &str { }  // Actually: fn method<'a>(&'a self) -> &'a str
}

// Only annotate when elision doesn't apply
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

### Splitting Borrows

```rust
struct Data {
    field1: String,
    field2: Vec<i32>,
}

// BAD: Borrow checker sees whole struct borrowed
fn bad(data: &mut Data) {
    let f1 = &mut data.field1;
    let f2 = &mut data.field2;  // ERROR: data already borrowed
    // ...
}

// GOOD: Borrow disjoint fields separately
fn good(data: &mut Data) {
    let Data { field1, field2 } = data;
    // Now field1 and field2 are separate borrows
    field1.push_str("hello");
    field2.push(42);
}

// Or use methods that return split borrows
impl Data {
    fn split(&mut self) -> (&mut String, &mut Vec<i32>) {
        (&mut self.field1, &mut self.field2)
    }
}
```

### The Borrow Checker as Design Guide

```rust
// When the borrow checker complains, ask: "What is it telling me?"

// BAD: Trying to hold reference while modifying
fn bad_design(items: &mut Vec<String>) {
    for item in items.iter() {  // Immutable borrow
        if item.starts_with("remove") {
            items.retain(|s| s != item);  // ERROR: can't mutate while borrowed
        }
    }
}

// GOOD: Collect indices first, then modify
fn good_design(items: &mut Vec<String>) {
    let to_remove: Vec<_> = items
        .iter()
        .filter(|s| s.starts_with("remove"))
        .cloned()
        .collect();
    
    items.retain(|s| !to_remove.contains(s));
}

// BETTER: drain_filter (nightly) or swap_remove pattern
fn better_design(items: &mut Vec<String>) {
    items.retain(|s| !s.starts_with("remove"));
}
```

### Lifetime Bounds in Generics

```rust
// 'a: 'b means 'a outlives 'b
struct Parser<'input> {
    input: &'input str,
}

impl<'input> Parser<'input> {
    // Output lifetime tied to input lifetime
    fn parse(&self) -> Token<'input> {
        Token { text: &self.input[0..5] }
    }
}

// Trait bounds with lifetimes
fn process<'a, T>(item: &'a T) -> &'a str 
where
    T: AsRef<str> + 'a,  // T must live at least as long as 'a
{
    item.as_ref()
}

// Higher-ranked trait bounds (HRTB) for callbacks
fn with_callback<F>(f: F)
where
    F: for<'a> Fn(&'a str) -> &'a str,  // F works for ANY lifetime
{
    let s = String::from("hello");
    let result = f(&s);
    println!("{}", result);
}
```

### Interior Mutability (When Needed)

```rust
use std::cell::{Cell, RefCell};

// Cell: for Copy types, no borrow checking at runtime
struct Counter {
    count: Cell<usize>,
}

impl Counter {
    fn increment(&self) {  // Note: &self, not &mut self
        self.count.set(self.count.get() + 1);
    }
}

// RefCell: runtime borrow checking (panics if violated)
struct CachedComputation {
    value: i32,
    cache: RefCell<Option<i32>>,
}

impl CachedComputation {
    fn compute(&self) -> i32 {
        let mut cache = self.cache.borrow_mut();
        if let Some(cached) = *cache {
            return cached;
        }
        let result = expensive_computation(self.value);
        *cache = Some(result);
        result
    }
}

// Use interior mutability ONLY when external mutability won't work
// (e.g., shared ownership, trait requirements)
```

### Self-Referential Structs (The Right Way)

```rust
// PROBLEM: Can't have a struct reference its own field
// struct Bad {
//     data: String,
//     slice: &str,  // Can't reference data!
// }

// SOLUTION 1: Store indices, not references
struct Good {
    data: String,
    start: usize,
    end: usize,
}

impl Good {
    fn slice(&self) -> &str {
        &self.data[self.start..self.end]
    }
}

// SOLUTION 2: Use Pin for self-referential async code
use std::pin::Pin;

// SOLUTION 3: Use ouroboros or self_cell crates for complex cases
```

## Mental Model

Matsakis thinks about borrows as **capabilities**:

1. `&T` = capability to read
2. `&mut T` = exclusive capability to read and write
3. The borrow checker ensures capabilities don't conflict
4. Lifetimes = how long a capability is valid

## Niko's Debugging Questions

When the borrow checker rejects code:

1. What capability am I trying to use?
2. What other capability conflicts with it?
3. Can I restructure to avoid the conflict?
4. Is the borrow checker revealing a real bug?

