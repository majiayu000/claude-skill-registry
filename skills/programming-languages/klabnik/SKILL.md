---
name: klabnik-teaching-rust
description: Write Rust code in the style of Steve Klabnik, author of "The Rust Programming Language." Emphasizes clear, idiomatic code that teaches as it goes. Use when writing example code, documentation, or code that others will learn from.
---

# Steve Klabnik Style Guide

## Overview

Steve Klabnik is the author of "The Rust Programming Language" (The Book) and was Rust's documentation lead. His gift: explaining complex concepts clearly. His code is designed to be read and understood, not just executed.

## Core Philosophy

> "Documentation is a love letter to your future self."

> "The best code is code that teaches."

Klabnik believes that **code should be approachable**. Clever code that confuses readers is worse than simple code that everyone understands.

## Design Principles

1. **Teach Through Code**: Every example should illuminate, not obscure.

2. **Progressive Complexity**: Start simple, add complexity as needed.

3. **Explicit Over Implicit**: Show what's happening, don't hide it.

4. **Documentation as Code**: Docs are as important as implementation.

## When Writing Code

### Always

- Write doc comments for public items (`///` for items, `//!` for modules)
- Include examples in documentation that compile and run
- Use descriptive variable names that explain purpose
- Prefer explicit types when teaching, `impl Trait` when not
- Include error messages that help users understand what went wrong

### Never

- Write "clever" one-liners that sacrifice clarity
- Skip documentation for public APIs
- Use abbreviations in public interfaces
- Leave users guessing about failure modes

### Prefer

- `match` over `if let` chains for exhaustiveness
- Named structs over tuples for public APIs
- `Result` with descriptive error types
- Explicit lifetimes in teaching code

## Code Patterns

### Documentation That Teaches

```rust
/// A rectangle defined by its width and height.
///
/// # Examples
///
/// Creating a rectangle and calculating its area:
///
/// ```
/// use shapes::Rectangle;
///
/// let rect = Rectangle::new(30, 50);
/// assert_eq!(rect.area(), 1500);
/// ```
///
/// Rectangles can also determine if they can hold other rectangles:
///
/// ```
/// use shapes::Rectangle;
///
/// let larger = Rectangle::new(30, 50);
/// let smaller = Rectangle::new(10, 20);
/// 
/// assert!(larger.can_hold(&smaller));
/// assert!(!smaller.can_hold(&larger));
/// ```
pub struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    /// Creates a new rectangle with the given dimensions.
    ///
    /// # Arguments
    ///
    /// * `width` - The width of the rectangle
    /// * `height` - The height of the rectangle
    ///
    /// # Panics
    ///
    /// Panics if either dimension is zero.
    pub fn new(width: u32, height: u32) -> Self {
        assert!(width > 0, "width must be positive");
        assert!(height > 0, "height must be positive");
        Rectangle { width, height }
    }

    /// Returns the area of the rectangle.
    pub fn area(&self) -> u32 {
        self.width * self.height
    }

    /// Returns `true` if `self` can completely contain `other`.
    pub fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}
```

### Descriptive Error Types

```rust
use std::fmt;
use std::error::Error;

/// Errors that can occur when parsing a configuration file.
#[derive(Debug)]
pub enum ConfigError {
    /// The configuration file could not be found.
    FileNotFound { path: String },
    /// The configuration file could not be parsed.
    ParseError { line: usize, message: String },
    /// A required field was missing.
    MissingField { field: &'static str },
    /// A field had an invalid value.
    InvalidValue { field: &'static str, value: String, expected: &'static str },
}

impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ConfigError::FileNotFound { path } => {
                write!(f, "configuration file not found: {}", path)
            }
            ConfigError::ParseError { line, message } => {
                write!(f, "parse error on line {}: {}", line, message)
            }
            ConfigError::MissingField { field } => {
                write!(f, "missing required field: {}", field)
            }
            ConfigError::InvalidValue { field, value, expected } => {
                write!(f, "invalid value for {}: got '{}', expected {}", 
                       field, value, expected)
            }
        }
    }
}

impl Error for ConfigError {}
```

### Progressive API Design

```rust
// Level 1: Simple usage
let client = Client::new();
let response = client.get("https://example.com").send()?;

// Level 2: With configuration
let client = Client::builder()
    .timeout(Duration::from_secs(10))
    .build()?;

// Level 3: Full control
let client = Client::builder()
    .timeout(Duration::from_secs(10))
    .pool_max_idle_per_host(10)
    .danger_accept_invalid_certs(true)  // Named to warn user
    .build()?;

// Implementation: Builder pattern
pub struct ClientBuilder {
    timeout: Option<Duration>,
    max_idle: usize,
    accept_invalid_certs: bool,
}

impl ClientBuilder {
    pub fn new() -> Self {
        ClientBuilder {
            timeout: None,
            max_idle: 5,
            accept_invalid_certs: false,
        }
    }

    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = Some(timeout);
        self
    }

    /// Accept invalid TLS certificates.
    ///
    /// # Warning
    ///
    /// This is **insecure** and should only be used for testing.
    pub fn danger_accept_invalid_certs(mut self, accept: bool) -> Self {
        self.accept_invalid_certs = accept;
        self
    }

    pub fn build(self) -> Result<Client, ClientError> {
        // ...
    }
}
```

### Teaching Ownership Through Examples

```rust
// OWNERSHIP: This function takes ownership of the string
fn takes_ownership(s: String) {
    println!("{}", s);
} // s is dropped here

// BORROWING: This function borrows the string
fn borrows(s: &String) {
    println!("{}", s);
} // Nothing happens to s

// MUTABLE BORROWING: This function can modify the string
fn modifies(s: &mut String) {
    s.push_str(" world");
}

fn main() {
    let s1 = String::from("hello");
    
    // After this call, s1 is no longer valid
    takes_ownership(s1);
    // println!("{}", s1);  // ERROR: s1 was moved
    
    let s2 = String::from("hello");
    
    // s2 is still valid after borrowing
    borrows(&s2);
    println!("{}", s2);  // OK: s2 was only borrowed
    
    let mut s3 = String::from("hello");
    
    // s3 is modified in place
    modifies(&mut s3);
    println!("{}", s3);  // "hello world"
}
```

### Module Organization

```rust
//! # My Crate
//!
//! `my_crate` provides utilities for working with widgets.
//!
//! ## Quick Start
//!
//! ```rust
//! use my_crate::Widget;
//!
//! let widget = Widget::new("example");
//! widget.process()?;
//! ```

// Re-export main types at crate root for convenience
pub use self::widget::Widget;
pub use self::error::{Error, Result};

// Organize implementation in submodules
mod widget;
mod error;
mod internal;  // Private implementation details
```

## Mental Model

Klabnik writes code by asking:

1. **Who will read this?** Write for them, not for the compiler.
2. **What might confuse them?** Address it in docs or code structure.
3. **What's the simplest version?** Start there.
4. **Does the error help?** Errors should guide, not frustrate.

## The Rust Book's Teaching Method

1. **Introduce concepts one at a time**
2. **Show concrete examples before abstractions**
3. **Explain the "why" behind the "what"**
4. **Build complexity gradually**
5. **Always provide working code**

