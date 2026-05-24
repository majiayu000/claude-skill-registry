---
name: rust-core-patterns
description: Production-ready Rust patterns for type-safe domain modeling including newtypes, type states, builders, smart constructors, and const generics. Use when creating domain primitives (IDs, emails), state machines, builders, or enforcing compile-time invariants in Rust code.
---

# Rust Core Patterns

*Minimal, production-ready Rust patterns for memory safety and type-driven design*

## Version Context
- **Rust**: 1.91.1 (stable)
- **Edition**: 2021
- **MSRV**: 1.78+

## When to Use This Skill

- Creating domain primitives (UserId, Email, OrderId)
- Implementing state machines with compile-time guarantees
- Building complex objects with mandatory fields
- Enforcing invariants at construction time
- Fixed-size constraints known at compile time
- Testable dependency injection patterns

## Core Pattern Library

### 1. Newtype Pattern for Domain Modeling

```rust
use std::fmt;

/// UserId newtype with validation
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct UserId(uuid::Uuid);

impl UserId {
    pub fn new() -> Self {
        Self(uuid::Uuid::new_v4())
    }

    pub fn from_str(s: &str) -> Result<Self, ParseError> {
        uuid::Uuid::parse_str(s)
            .map(Self)
            .map_err(|_| ParseError::InvalidUserId)
    }

    pub fn as_uuid(&self) -> &uuid::Uuid {
        &self.0
    }
}

impl fmt::Display for UserId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

/// Email newtype with compile-time validation
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Email(String);

impl Email {
    pub fn new(s: String) -> Result<Self, ValidationError> {
        if s.contains('@') && s.len() >= 3 {
            Ok(Self(s))
        } else {
            Err(ValidationError::InvalidEmail)
        }
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}
```

### 2. Type State Pattern

```rust
use std::marker::PhantomData;

/// Connection lifecycle using type states
pub struct Connection<State> {
    inner: ConnectionInner,
    _state: PhantomData<State>,
}

pub struct Disconnected;
pub struct Connected;
pub struct Authenticated;

impl Connection<Disconnected> {
    pub fn new() -> Self {
        Self {
            inner: ConnectionInner::new(),
            _state: PhantomData,
        }
    }

    pub async fn connect(self) -> Result<Connection<Connected>, ConnectionError> {
        self.inner.connect().await?;
        Ok(Connection {
            inner: self.inner,
            _state: PhantomData,
        })
    }
}

impl Connection<Connected> {
    pub async fn authenticate(
        self,
        credentials: Credentials,
    ) -> Result<Connection<Authenticated>, AuthError> {
        self.inner.auth(credentials).await?;
        Ok(Connection {
            inner: self.inner,
            _state: PhantomData,
        })
    }
}

impl Connection<Authenticated> {
    pub async fn query(&self, sql: &str) -> Result<QueryResult, QueryError> {
        self.inner.execute(sql).await
    }
}
```

### 3. Builder Pattern with Typestate

```rust
/// Builder with mandatory fields enforced at compile time
#[derive(Default)]
pub struct RequestBuilder<Email, Name> {
    email: Email,
    name: Name,
    age: Option<u8>,
}

pub struct Set<T>(T);
pub struct Unset;

impl RequestBuilder<Unset, Unset> {
    pub fn new() -> Self {
        Self::default()
    }
}

impl<N> RequestBuilder<Unset, N> {
    pub fn email(self, email: String) -> RequestBuilder<Set<String>, N> {
        RequestBuilder {
            email: Set(email),
            name: self.name,
            age: self.age,
        }
    }
}

impl<E> RequestBuilder<E, Unset> {
    pub fn name(self, name: String) -> RequestBuilder<E, Set<String>> {
        RequestBuilder {
            email: self.email,
            name: Set(name),
            age: self.age,
        }
    }
}

impl RequestBuilder<Set<String>, Set<String>> {
    pub fn age(mut self, age: u8) -> Self {
        self.age = Some(age);
        self
    }

    pub fn build(self) -> CreateUserRequest {
        CreateUserRequest {
            email: self.email.0,
            name: self.name.0,
            age: self.age,
        }
    }
}
```

### 4. Smart Constructors

```rust
/// NonEmptyVec ensures the vector is never empty
#[derive(Debug, Clone)]
pub struct NonEmptyVec<T> {
    head: T,
    tail: Vec<T>,
}

impl<T> NonEmptyVec<T> {
    /// Smart constructor enforces non-empty invariant
    pub fn new(head: T, tail: Vec<T>) -> Self {
        Self { head, tail }
    }

    pub fn from_vec(mut vec: Vec<T>) -> Option<Self> {
        if vec.is_empty() {
            None
        } else {
            let head = vec.remove(0);
            Some(Self { head, tail: vec })
        }
    }

    pub fn head(&self) -> &T {
        &self.head
    }

    pub fn len(&self) -> usize {
        1 + self.tail.len()
    }
}
```

### 5. Const Generics for Compile-Time Bounds

```rust
/// String with compile-time length bounds
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundedString<const MIN: usize, const MAX: usize> {
    value: String,
}

impl<const MIN: usize, const MAX: usize> BoundedString<MIN, MAX> {
    pub fn new(value: String) -> Result<Self, BoundsError> {
        let len = value.len();
        if len < MIN {
            Err(BoundsError::TooShort { min: MIN, actual: len })
        } else if len > MAX {
            Err(BoundsError::TooLong { max: MAX, actual: len })
        } else {
            Ok(Self { value })
        }
    }

    pub fn as_str(&self) -> &str {
        &self.value
    }
}

/// Type aliases for domain constraints
pub type Username = BoundedString<3, 20>;
pub type Bio = BoundedString<0, 500>;
```

### 6. Safe Concurrency Primitives

```rust
use std::sync::Arc;
use std::sync::atomic::{AtomicU64, Ordering};
use tokio::sync::{RwLock, Semaphore};

/// Thread-safe counter using atomics
pub struct Counter {
    value: AtomicU64,
}

impl Counter {
    pub fn new() -> Self {
        Self {
            value: AtomicU64::new(0),
        }
    }

    pub fn increment(&self) -> u64 {
        self.value.fetch_add(1, Ordering::SeqCst)
    }

    pub fn get(&self) -> u64 {
        self.value.load(Ordering::SeqCst)
    }
}

/// Bounded concurrency with semaphore
pub struct ConcurrencyLimiter {
    semaphore: Arc<Semaphore>,
}

impl ConcurrencyLimiter {
    pub fn new(max_concurrent: usize) -> Self {
        Self {
            semaphore: Arc::new(Semaphore::new(max_concurrent)),
        }
    }

    pub async fn run<F, T>(&self, f: F) -> T
    where
        F: std::future::Future<Output = T>,
    {
        let _permit = self.semaphore.acquire().await.unwrap();
        f.await
    }
}
```

### 7. Trait-Based Dependency Injection

```rust
use async_trait::async_trait;

/// Repository trait for abstraction
#[async_trait]
pub trait UserRepository: Send + Sync {
    async fn find_by_id(&self, id: UserId) -> Result<User, RepoError>;
    async fn save(&self, user: &User) -> Result<(), RepoError>;
}

/// Service depends on trait, not concrete type
pub struct UserService<R: UserRepository> {
    repo: Arc<R>,
}

impl<R: UserRepository> UserService<R> {
    pub fn new(repo: Arc<R>) -> Self {
        Self { repo }
    }

    pub async fn get_user(&self, id: UserId) -> Result<User, ServiceError> {
        self.repo.find_by_id(id)
            .await
            .map_err(ServiceError::from)
    }
}
```

## Key Principles

1. **Make invalid states unrepresentable** - Use types to enforce invariants
2. **Fail fast at construction** - Validate in constructors, not at use sites
3. **Prefer compile-time over runtime** - Use const generics and type states
4. **Explicit over implicit** - No hidden state or magic
5. **Zero-cost abstractions** - Patterns compile to optimal code

## Performance Notes

- Newtypes: Zero runtime cost (optimized away)
- Type states: Zero runtime cost (PhantomData is zero-sized)
- Const generics: Compile-time validation, no runtime checks
- Arc for shared ownership: Minimal overhead, lock-free reference counting

## Pattern Selection Guide

- **Newtypes**: Always for domain primitives (IDs, emails, etc.)
- **Type states**: Complex state machines, connection lifecycles
- **Builders**: Objects with many optional fields or configuration
- **Smart constructors**: When invariants must be maintained
- **Const generics**: Fixed-size constraints known at compile time
- **Trait injection**: Testing, swappable implementations
