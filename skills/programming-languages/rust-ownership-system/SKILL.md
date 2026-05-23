---
name: rust-ownership-system
description: Use when Rust's ownership system including ownership rules, borrowing, lifetimes, and memory safety. Use when working with Rust memory management.
allowed-tools:
  - Bash
  - Read
---

# Rust Ownership System

Master Rust's unique ownership system that provides memory safety without
garbage collection through compile-time checks.

## Ownership Rules

**Three fundamental ownership rules:**

1. Each value in Rust has a variable that's its owner
2. There can only be one owner at a time
3. When the owner goes out of scope, the value is dropped

```rust
fn ownership_basics() {
    // s owns the String
    let s = String::from("hello");

    // Ownership moved to s2
    let s2 = s;

    // Error: s no longer owns the value
    // println!("{}", s);

    println!("{}", s2); // OK
} // s2 dropped here, memory freed
```

## Move Semantics

**Ownership transfer (move):**

```rust
fn move_semantics() {
    let s1 = String::from("hello");

    // Ownership moved to function
    takes_ownership(s1);

    // Error: s1 no longer valid
    // println!("{}", s1);
}

fn takes_ownership(s: String) {
    println!("{}", s);
} // s dropped here

// Return ownership from function
fn gives_ownership() -> String {
    String::from("hello")
}

fn main() {
    let s = gives_ownership();
    println!("{}", s);
}
```

**Copy trait for stack types:**

```rust
fn copy_types() {
    // Types implementing Copy are duplicated, not moved
    let x = 5;
    let y = x; // x copied to y

    println!("x: {}, y: {}", x, y); // Both valid

    // Copy types: integers, floats, bool, char, tuples of Copy types
    let tuple = (1, 2.5, true);
    let tuple2 = tuple;
    println!("{:?} {:?}", tuple, tuple2); // Both valid
}
```

## Borrowing

**Immutable borrowing (references):**

```rust
fn immutable_borrow() {
    let s1 = String::from("hello");

    // Borrow s1 (immutable reference)
    let len = calculate_length(&s1);

    println!("Length of '{}' is {}", s1, len); // s1 still valid
}

fn calculate_length(s: &String) -> usize {
    s.len()
} // s goes out of scope, but doesn't drop the value

// Multiple immutable borrows allowed
fn multiple_immutable_borrows() {
    let s = String::from("hello");

    let r1 = &s;
    let r2 = &s;
    let r3 = &s;

    println!("{}, {}, {}", r1, r2, r3); // OK
}
```

**Mutable borrowing:**

```rust
fn mutable_borrow() {
    let mut s = String::from("hello");

    // Mutable borrow
    change(&mut s);

    println!("{}", s); // "hello, world"
}

fn change(s: &mut String) {
    s.push_str(", world");
}

// Only ONE mutable borrow allowed at a time
fn mutable_borrow_rules() {
    let mut s = String::from("hello");

    let r1 = &mut s;
    // let r2 = &mut s; // Error: cannot borrow mutably twice

    println!("{}", r1);
}

// Cannot mix mutable and immutable borrows
fn no_mix_borrows() {
    let mut s = String::from("hello");

    let r1 = &s;     // Immutable borrow
    let r2 = &s;     // Another immutable borrow
    // let r3 = &mut s; // Error: cannot borrow mutably while immutably borrowed

    println!("{} {}", r1, r2);
}
```

**Non-lexical lifetimes (NLL):**

```rust
fn non_lexical_lifetimes() {
    let mut s = String::from("hello");

    let r1 = &s;
    let r2 = &s;
    println!("{} {}", r1, r2);
    // r1 and r2 no longer used after this point

    // OK: immutable borrows ended
    let r3 = &mut s;
    println!("{}", r3);
}
```

## Lifetimes

**Lifetime annotations:**

```rust
// Lifetime 'a ensures returned reference lives as long as both inputs
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

fn main() {
    let string1 = String::from("long string");
    let string2 = String::from("short");

    let result = longest(&string1, &string2);
    println!("Longest: {}", result);
}
```

**Lifetime in structs:**

```rust
// Struct holds a reference, needs lifetime annotation
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 {
        3
    }

    fn announce_and_return_part(&self, announcement: &str) -> &str {
        println!("Attention: {}", announcement);
        self.part
    }
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.').next().unwrap();

    let excerpt = ImportantExcerpt {
        part: first_sentence,
    };

    println!("{}", excerpt.part);
}
```

**Lifetime elision rules:**

```rust
// Compiler infers lifetimes in these cases:

// Rule 1: Each reference parameter gets its own lifetime
fn first_word(s: &str) -> &str {
    // Expanded: fn first_word<'a>(s: &'a str) -> &'a str
    s.split_whitespace().next().unwrap_or("")
}

// Rule 2: If one input lifetime, assign to all outputs
fn foo(s: &str) -> &str {
    s
}

// Rule 3: If &self or &mut self, its lifetime assigned to outputs
impl<'a> ImportantExcerpt<'a> {
    fn get_part(&self) -> &str {
        // Expanded: fn get_part<'a>(&'a self) -> &'a str
        self.part
    }
}
```

**Static lifetime:**

```rust
// 'static means reference lives for entire program duration
fn static_lifetime() -> &'static str {
    "This string is stored in binary"
}

// String literals have 'static lifetime
let s: &'static str = "hello world";
```

## Smart Pointers

**Box for heap allocation:**

```rust
fn box_pointer() {
    // Allocate value on heap
    let b = Box::new(5);
    println!("b = {}", b);
} // b deallocated when out of scope

// Recursive types require Box
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use List::{Cons, Nil};

fn recursive_type() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));
}
```

**Rc for reference counting:**

```rust
use std::rc::Rc;

fn rc_example() {
    let a = Rc::new(5);

    // Clone Rc pointer, increment count
    let b = Rc::clone(&a);
    let c = Rc::clone(&a);

    println!("Reference count: {}", Rc::strong_count(&a)); // 3

    // All owners must go out of scope before value is dropped
}

// Sharing data in graph structures
enum RcList {
    Cons(i32, Rc<RcList>),
    Nil,
}

use RcList::{Cons as RcCons, Nil as RcNil};

fn shared_ownership() {
    let a = Rc::new(RcCons(5, Rc::new(RcCons(10, Rc::new(RcNil)))));

    // b and c both reference a
    let b = RcCons(3, Rc::clone(&a));
    let c = RcCons(4, Rc::clone(&a));
}
```

**RefCell for interior mutability:**

```rust
use std::cell::RefCell;

fn refcell_example() {
    let value = RefCell::new(5);

    // Borrow mutably
    *value.borrow_mut() += 1;

    // Borrow immutably
    println!("Value: {}", value.borrow());
}

// Combine Rc and RefCell for shared mutable data
use std::rc::Rc;
use std::cell::RefCell;

fn rc_refcell() {
    let value = Rc::new(RefCell::new(5));

    let a = Rc::clone(&value);
    let b = Rc::clone(&value);

    *a.borrow_mut() += 10;
    *b.borrow_mut() += 20;

    println!("Value: {}", value.borrow()); // 35
}
```

## Ownership Patterns

**Taking ownership vs borrowing:**

```rust
// Take ownership when you need to consume the value
fn consume(s: String) {
    println!("{}", s);
}

// Borrow when you only need to read
fn read(s: &String) {
    println!("{}", s);
}

// Borrow mutably when you need to modify
fn modify(s: &mut String) {
    s.push_str(" modified");
}

fn main() {
    let mut s = String::from("hello");

    read(&s);        // Still own s
    modify(&mut s);  // Still own s
    consume(s);      // No longer own s
}
```

**Builder pattern with ownership:**

```rust
struct Config {
    name: String,
    value: i32,
}

struct ConfigBuilder {
    name: Option<String>,
    value: Option<i32>,
}

impl ConfigBuilder {
    fn new() -> Self {
        ConfigBuilder {
            name: None,
            value: None,
        }
    }

    // Take ownership and return ownership
    fn name(mut self, name: String) -> Self {
        self.name = Some(name);
        self
    }

    fn value(mut self, value: i32) -> Self {
        self.value = Some(value);
        self
    }

    fn build(self) -> Config {
        Config {
            name: self.name.unwrap_or_default(),
            value: self.value.unwrap_or(0),
        }
    }
}

fn main() {
    let config = ConfigBuilder::new()
        .name(String::from("app"))
        .value(42)
        .build();
}
```

## Slice Types

**String slices:**

```rust
fn string_slices() {
    let s = String::from("hello world");

    // Slice references part of string
    let hello = &s[0..5];
    let world = &s[6..11];

    // Shorthand
    let hello = &s[..5];
    let world = &s[6..];
    let whole = &s[..];

    println!("{} {}", hello, world);
}

fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[..i];
        }
    }

    &s[..]
}
```

**Array slices:**

```rust
fn array_slices() {
    let a = [1, 2, 3, 4, 5];

    let slice = &a[1..3]; // &[i32]

    assert_eq!(slice, &[2, 3]);
}
```

## Clone vs Copy

**Understanding Clone trait:**

```rust
#[derive(Clone)]
struct Point {
    x: f64,
    y: f64,
}

fn clone_example() {
    let p1 = Point { x: 1.0, y: 2.0 };

    // Explicit clone (deep copy)
    let p2 = p1.clone();

    // Both valid
    println!("{} {}", p1.x, p2.x);
}
```

**Copy trait limitations:**

```rust
// Copy requires all fields to implement Copy
#[derive(Copy, Clone)]
struct Coord {
    x: i32,
    y: i32,
}

// Cannot derive Copy with String field
// #[derive(Copy, Clone)]  // Error
struct Person {
    name: String,  // String doesn't implement Copy
}
```

## Drop Trait

**Custom cleanup with Drop:**

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data: {}", self.data);
    }
}

fn main() {
    let c = CustomSmartPointer {
        data: String::from("my stuff"),
    };

    let d = CustomSmartPointer {
        data: String::from("other stuff"),
    };

    println!("CustomSmartPointers created");
} // d dropped, then c dropped
```

**Manual drop:**

```rust
fn manual_drop() {
    let c = CustomSmartPointer {
        data: String::from("some data"),
    };

    println!("Before drop");
    drop(c); // Manually drop early
    println!("After drop");
}
```

## When to Use This Skill

Use rust-ownership-system when you need to:

- Understand Rust's memory management model
- Write memory-safe code without garbage collection
- Handle ownership transfer between functions
- Work with references and borrowing
- Implement structs with lifetime parameters
- Use smart pointers (Box, Rc, RefCell)
- Debug borrow checker errors
- Choose between ownership, borrowing, and cloning
- Implement custom Drop behavior
- Work with slices and references safely

## Best Practices

- Prefer borrowing over ownership transfer when possible
- Use immutable borrows by default, mutable only when needed
- Keep borrow scopes as small as possible
- Use lifetime elision when compiler can infer lifetimes
- Choose appropriate smart pointer for use case
- Avoid RefCell in performance-critical code
- Use slices instead of owned types in function signatures
- Clone only when necessary (it's explicit and visible)
- Implement Drop for custom cleanup logic
- Let compiler guide you with borrow checker errors

## Common Pitfalls

- Moving value and trying to use it afterward
- Creating multiple mutable borrows simultaneously
- Mixing mutable and immutable borrows
- Returning references to local variables
- Fighting the borrow checker instead of understanding it
- Overusing clone() to avoid ownership issues
- Not understanding lifetime relationships
- Circular references with Rc (use Weak)
- Panicking with RefCell borrow violations at runtime
- Using 'static lifetime incorrectly

## Resources

- [Rust Book - Ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)
- [Rust Book - Lifetimes](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html)
- [Rust By Example - Scopes](https://doc.rust-lang.org/rust-by-example/scope.html)
- [The Rustonomicon](https://doc.rust-lang.org/nomicon/)
- [Too Many Linked Lists](https://rust-unofficial.github.io/too-many-lists/)
