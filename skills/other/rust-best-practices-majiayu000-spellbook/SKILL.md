---
name: rust-best-practices
description: Rust coding best practices based on Microsoft Pragmatic Rust Guidelines. ALWAYS invoke before writing or modifying Rust code. Covers error handling, API design, performance, and idiomatic patterns.
---
# Rust Best Practices

Based on Microsoft Pragmatic Rust Guidelines and Rust community standards.

## Core Principles

1. **Leverage the type system** — Use types to make invalid states unrepresentable
2. **Embrace ownership** — Work with the borrow checker, not against it
3. **Explicit over implicit** — Be clear about fallibility, mutability, and lifetimes
4. **Zero-cost abstractions** — Use iterators, generics, and traits without runtime cost
5. **Fail fast, recover gracefully** — Validate early, handle errors explicitly

---

## Error Handling

### Use `thiserror` for Libraries
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum MyError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    #[error("Parse error at line {line}: {message}")]
    Parse { line: usize, message: String },
    #[error("Not found: {0}")]
    NotFound(String),
}
```

### Use `anyhow` for Applications
```rust
use anyhow::{Context, Result};

fn main() -> Result<()> {
    let config = load_config()
        .context("Failed to load configuration")?;
    run_app(config)?;
    Ok(())
}
```

### Never Panic in Libraries
```rust
// ❌ BAD
pub fn get_item(index: usize) -> &Item {
    &self.items[index]  // Panics on out-of-bounds
}

// ✅ GOOD
pub fn get_item(&self, index: usize) -> Option<&Item> {
    self.items.get(index)
}

// ✅ GOOD - when you need Result
pub fn get_item(&self, index: usize) -> Result<&Item, Error> {
    self.items.get(index).ok_or(Error::NotFound(index))
}
```

---

## API Design

### Use Builder Pattern for Complex Configs
```rust
pub struct Client {
    url: String,
    timeout: Duration,
    retries: u32,
}

impl Client {
    pub fn builder(url: impl Into<String>) -> ClientBuilder {
        ClientBuilder {
            url: url.into(),
            timeout: Duration::from_secs(30),
            retries: 3,
        }
    }
}

pub struct ClientBuilder {
    url: String,
    timeout: Duration,
    retries: u32,
}

impl ClientBuilder {
    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = timeout;
        self
    }

    pub fn retries(mut self, retries: u32) -> Self {
        self.retries = retries;
        self
    }

    pub fn build(self) -> Client {
        Client {
            url: self.url,
            timeout: self.timeout,
            retries: self.retries,
        }
    }
}
```

### Use Newtype Pattern
```rust
// ❌ BAD - primitive obsession
fn create_user(name: String, email: String, age: u32) -> User { ... }

// ✅ GOOD - newtype wrappers
pub struct Username(String);
pub struct Email(String);
pub struct Age(u32);

impl Email {
    pub fn new(email: impl Into<String>) -> Result<Self, ValidationError> {
        let email = email.into();
        if email.contains('@') {
            Ok(Self(email))
        } else {
            Err(ValidationError::InvalidEmail)
        }
    }
}

fn create_user(name: Username, email: Email, age: Age) -> User { ... }
```

### Accept `impl Trait` for Flexibility
```rust
// ❌ BAD - overly specific
pub fn process(items: Vec<String>) { ... }

// ✅ GOOD - accept any iterable
pub fn process(items: impl IntoIterator<Item = impl AsRef<str>>) {
    for item in items {
        println!("{}", item.as_ref());
    }
}
```

---

## Performance

### Avoid Unnecessary Clones
```rust
// ❌ BAD
fn process(data: &String) {
    let owned = data.clone();  // Unnecessary allocation
    do_something(owned);
}

// ✅ GOOD
fn process(data: &str) {
    do_something(data);
}
```

### Use `Cow` for Conditional Ownership
```rust
use std::borrow::Cow;

fn normalize(input: &str) -> Cow<'_, str> {
    if input.contains(' ') {
        Cow::Owned(input.replace(' ', "_"))
    } else {
        Cow::Borrowed(input)
    }
}
```

### Prefer Iterators Over Loops
```rust
// ❌ BAD
let mut result = Vec::new();
for item in items {
    if item.is_valid() {
        result.push(item.transform());
    }
}

// ✅ GOOD
let result: Vec<_> = items
    .into_iter()
    .filter(|item| item.is_valid())
    .map(|item| item.transform())
    .collect();
```

---

## Async Patterns

### Use `tokio` Runtime
```rust
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::init();
    run().await
}
```

### Structured Concurrency with `JoinSet`
```rust
use tokio::task::JoinSet;

async fn process_all(urls: Vec<String>) -> Vec<Result<Response, Error>> {
    let mut set = JoinSet::new();

    for url in urls {
        set.spawn(async move {
            fetch(&url).await
        });
    }

    let mut results = Vec::new();
    while let Some(res) = set.join_next().await {
        results.push(res.unwrap());
    }
    results
}
```

### Use `#[instrument]` for Tracing
```rust
use tracing::instrument;

#[instrument(skip(password))]
async fn login(username: &str, password: &str) -> Result<Token> {
    tracing::info!("Attempting login");
    // ...
}
```

---

## Testing

### Use `#[test]` and `proptest`
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use proptest::prelude::*;

    #[test]
    fn test_basic() {
        assert_eq!(add(2, 2), 4);
    }

    proptest! {
        #[test]
        fn test_add_commutative(a: i32, b: i32) {
            prop_assert_eq!(add(a, b), add(b, a));
        }
    }
}
```

### Use `mockall` for Mocking
```rust
#[cfg_attr(test, mockall::automock)]
trait Database {
    async fn get(&self, id: u64) -> Result<Record>;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_with_mock() {
        let mut mock = MockDatabase::new();
        mock.expect_get()
            .returning(|_| Ok(Record::default()));

        let service = Service::new(mock);
        assert!(service.process(1).await.is_ok());
    }
}
```

---

## Common Anti-Patterns to Avoid

| Anti-Pattern | Better Alternative |
|-------------|-------------------|
| `unwrap()` everywhere | `?` operator with proper error types |
| `clone()` to satisfy borrow checker | Restructure code, use references |
| `Box<dyn Error>` | Concrete error types with `thiserror` |
| `String` for all text | `&str`, `Cow<str>`, or domain types |
| Manual `Drop` for cleanup | RAII with struct destructors |
| `unsafe` without justification | Safe abstractions first |
| `Arc<Mutex<_>>` overuse | Message passing, channels |
| Blocking in async context | `spawn_blocking` for CPU work |

---

## References

- [Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [The Rust Book](https://doc.rust-lang.org/book/)
