---
name: "Rust Clean Implementation"
description: "Write clean, well-documented Rust code with proper error handling and no_std/std support"
approved: Yes
created: 2026-01-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "3.1-approved"
  last_updated: "2026-01-28"
tags:
  - rust
  - clean-code
  - documentation
  - error-handling
  - no_std
files:
  - examples/documentation-patterns.md: WHY/WHAT/HOW doc patterns with mandatory panic documentation
  - examples/error-handling-guide.md: Error handling with derive_more
  - examples/security-guide.md: Security best practices
  - examples/iterator-patterns.md: Iterator and trait implementation patterns
  - examples/basic-template.md: Basic implementation template
  - templates/basic-example.rs: Starter template for new Rust modules
---

# Rust Clean Implementation

## When to Use This Skill

Read this skill when **implementing new Rust code** (not tests or async). This covers:

- Writing new modules and functions
- Documenting code with WHY/WHAT/HOW pattern
- Error handling with `derive_more`
- Supporting both `no_std` and `std` environments
- Security best practices

**Do NOT read this for:**
- Testing → See [rust-testing-excellence](../rust-testing-excellence/skill.md)
- Async code → See [rust-with-async-code](../rust-with-async-code/skill.md)

---

## Core Principles

### 1. Documentation: WHY/WHAT/HOW Pattern

**MANDATORY:** Every public function must document:
- **WHY** it exists (purpose/business reason)
- **WHAT** it does (summary of behavior)
- **HOW** to use it (arguments, returns, errors, examples)
- **PANICS** when it can panic (conditions that cause panics)

```rust
/// # Purpose (WHY)
///
/// Validates user input before database insertion to prevent invalid state
/// from entering persistent storage.
///
/// # Arguments (WHAT)
///
/// * `username` - Unique username (must be 3+ chars per USERNAME_POLICY)
/// * `email` - User email for notifications (RFC 5322 format)
///
/// # Returns (HOW)
///
/// User ID on success
///
/// # Errors
///
/// * `ValidationError::UsernameTooShort` - Username < 3 characters
/// * `ValidationError::InvalidEmailFormat` - Email doesn't match pattern
///
/// # Panics
///
/// Panics if the internal database connection pool is poisoned.
pub fn register_user(username: &str, email: &str) -> Result<u64, ValidationError> {
    // Implementation...
}
```

**Documentation Checklist for Every Public Function/Method:**

- [ ] `/// Summary` - One-line description
- [ ] `/// # Purpose (WHY)` - Business/design reason (optional but recommended)
- [ ] `/// # Arguments` - Document each parameter (if any)
- [ ] `/// # Returns` - What the function returns
- [ ] `/// # Errors` - What errors can occur (for Result returns)
- [ ] `/// # Panics` - **MANDATORY** - When/why function panics
- [ ] `/// # Safety` - Safety requirements (for unsafe functions only)
- [ ] `/// # Examples` - Code examples showing usage

**Panic Documentation Examples:**

```rust
/// Retrieves a user by ID.
///
/// # Panics
///
/// Panics if `user_id` is 0 or exceeds the maximum valid ID.
pub fn get_user(&self, user_id: u64) -> User {
    assert!(user_id > 0, "user_id must be positive");
    assert!(user_id < MAX_USER_ID, "user_id exceeds maximum");
    // Implementation...
}

/// Processes a slice of data.
///
/// # Panics
///
/// Panics if the slice is empty or if any element is negative.
pub fn process_data(data: &[i32]) -> i32 {
    if data.is_empty() {
        panic!("data cannot be empty");
    }
    // Implementation...
}

/// Divides two numbers.
///
/// # Panics
///
/// Panics if `divisor` is zero.
pub fn divide(dividend: i32, divisor: i32) -> i32 {
    dividend / divisor  // Panics on division by zero
}
```

**When a function cannot panic:**

```rust
/// Adds two numbers.
///
/// This function cannot panic.
pub fn add(a: i32, b: i32) -> i32 {
    a.wrapping_add(b)
}
```

**Or simply omit the Panics section if the function genuinely cannot panic.**

### 2. Error Handling: Use derive_more

**MANDATORY:** Use `derive_more::From` for error types. Never use `thiserror` or `anyhow` in libraries.

```rust
use derive_more::From;

/// Application errors with automatic From conversions
#[derive(Debug, From)]
pub enum AppError {
    /// Configuration file not found at path
    ConfigNotFound(std::path::PathBuf),

    /// I/O error (automatic From<std::io::Error>)
    Io(#[from] std::io::Error),

    /// Invalid configuration format
    InvalidConfig(String),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            Self::ConfigNotFound(path) => write!(f, "config not found: {:?}", path),
            Self::Io(e) => write!(f, "I/O error: {}", e),
            Self::InvalidConfig(msg) => write!(f, "invalid config: {}", msg),
        }
    }
}

impl std::error::Error for AppError {}

// Usage with ? operator
fn load_config(path: &Path) -> Result<Config, AppError> {
    let content = std::fs::read_to_string(path)?; // Automatic conversion
    parse_config(&content)
}
```

### 3. No Unwrap in Production

**FORBIDDEN:** Never use `.unwrap()` or `.expect()` in production code paths.

```rust
// BAD ❌
let value = option.unwrap();
let result = operation().expect("should never fail");

// GOOD ✅
let value = option.ok_or(Error::NotFound)?;
let result = operation()?;
let value = match result {
    Ok(v) => v,
    Err(e) => {
        log::error!("operation failed: {}", e);
        return Err(Error::OperationFailed);
    }
};
```

**Exception:** Tests and truly impossible cases only.

```rust
#[cfg(test)]
fn test_something() {
    let value = result.unwrap(); // OK in tests
}

// Only when mathematically impossible
let idx = value.checked_sub(1)
    .expect("value is always > 0 per invariant");
```

**See also:** [Test Helper Functions](../rust-testing-excellence/skill.md#test-helper-functions) for when `.unwrap()` is acceptable in test utilities.

---

## No_std / Std Support

### Strategy for Hybrid Libraries

Use Cargo features to support both environments:

```toml
# Cargo.toml
[features]
default = []
std = []

[dependencies]
# no_std compatible dependencies
```

### Implementation Decision Tree

1. **For no_std-specific features:**
   - ✅ Always implement from scratch using `core` and atomics
   - Use `#[cfg(not(feature = "std"))]`

2. **For std-available features:**
   - ✅ **If std type sufficient:** Re-export it directly
   - ✅ **If custom methods needed:** Wrap std type
   - ❌ **Don't reimplement** unless explicitly required

### Pattern 1: Re-export std Type

```rust
// GOOD: Use std type when it does everything needed
#[cfg(feature = "std")]
pub use std::sync::Mutex;

#[cfg(not(feature = "std"))]
pub struct Mutex<T> {
    // Custom no_std implementation using atomics
}
```

### Pattern 2: Wrap std Type for Additional Methods

```rust
#[cfg(feature = "std")]
pub struct EnhancedMutex<T> {
    inner: std::sync::Mutex<T>,
}

#[cfg(feature = "std")]
impl<T> EnhancedMutex<T> {
    pub fn try_lock_for(&self, duration: Duration) -> Option<MutexGuard<T>> {
        // Custom method not in std::sync::Mutex
    }

    // Delegate standard methods
    pub fn lock(&self) -> LockResult<MutexGuard<T>> {
        self.inner.lock()
    }
}

#[cfg(not(feature = "std"))]
pub struct EnhancedMutex<T> {
    // Custom no_std implementation
}
```

### Compatibility Layers (Advanced)

For complex type interactions (e.g., Mutex + CondVar), create compatibility modules:

```rust
// In foundation_nostd/src/comp/condvar_comp.rs
#[cfg(feature = "std")]
pub use std::sync::{Mutex, Condvar as CondVar};

#[cfg(not(feature = "std"))]
pub use crate::primitives::condvar::{CondVarMutex as Mutex, CondVar};

// Consuming code - simple, no feature gates
use foundation_nostd::comp::condvar_comp::{Mutex, CondVar};
```

**Key Principle:** Move complexity to dependencies, keep consuming code simple.

---

## Security Best Practices

### Input Validation

Always validate untrusted input:

```rust
const MAX_INPUT_LENGTH: usize = 1024;

pub fn process_user_input(input: &str) -> Result<String, SecurityError> {
    // Length check (DoS prevention)
    if input.len() > MAX_INPUT_LENGTH {
        return Err(SecurityError::InputTooLong);
    }

    // Character whitelist (not blacklist!)
    const VALID_CHARS: &[u8] = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ";
    for &byte in input.as_bytes() {
        if !VALID_CHARS.contains(&byte) {
            return Err(SecurityError::InvalidCharacter(byte));
        }
    }

    Ok(input.trim().to_string())
}
```

### Secrets Management

Use `secrecy` crate to prevent secrets from appearing in logs:

```rust
use secrecy::{Secret, ExposeSecret};

struct Config {
    api_key: Secret<String>,
}

impl Config {
    fn make_request(&self) -> Result<Response> {
        let key = self.api_key.expose_secret(); // Explicit exposure
        // Use key...
        Ok(Response::default())
    }
}
// Secret won't appear in Debug output
```

### SQL Injection Prevention

Always use parameterized queries:

```rust
// GOOD ✅ Parameterized query
async fn get_user_safe(pool: &PgPool, user_id: i64) -> Result<User> {
    sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(user_id)
        .fetch_one(pool)
        .await
}

// BAD ❌ String interpolation
async fn get_user_unsafe(pool: &PgPool, username: &str) -> Result<User> {
    let query = format!("SELECT * FROM users WHERE name = '{}'", username);
    // VULNERABLE TO INJECTION!
}
```

### Command Injection Prevention

Use argument arrays, not shell:

```rust
// GOOD ✅ Safe command execution
fn run_safe(file_path: &Path) -> Result<Vec<u8>> {
    let output = Command::new("process")
        .arg(file_path) // Safe: passed directly, no shell
        .output()?;
    Ok(output.stdout)
}

// BAD ❌ Shell injection
fn run_unsafe(cmd: &str, arg: &str) -> Result<Vec<u8>> {
    Command::new("sh")
        .arg("-c")
        .arg(format!("{} {}", cmd, arg)) // VULNERABLE!
        .output()?;
}
```

---

## Iterator Best Practices

### Avoid Unnecessary Collections

```rust
// BAD ❌ Unnecessary allocation
let has_even = numbers.iter()
    .filter(|&&x| x % 2 == 0)
    .collect::<Vec<_>>() // Allocates!
    .len() > 0;

// GOOD ✅ Short-circuits, no allocation
let has_even = numbers.iter().any(|&x| x % 2 == 0);

// BAD ❌ Collect just to iterate again
let uppercase: Vec<_> = names.iter()
    .map(|s| s.to_uppercase())
    .collect(); // Unnecessary
for name in uppercase {
    println!("{}", name);
}

// GOOD ✅ Iterate directly
for name in names.iter().map(|s| s.to_uppercase()) {
    println!("{}", name);
}
```

### Common Combinators

```rust
let result: Vec<_> = numbers
    .iter()
    .filter(|&&x| x > 0)        // Keep positive only
    .map(|&x| x * 2)             // Double each
    .take(10)                    // First 10 only
    .collect();

// Side effects without collection
numbers.iter()
    .filter(|&&x| x > 100)
    .for_each(|x| println!("{}", x));

// Accumulation
let sum = numbers.iter().fold(0, |acc, &x| acc + x);

// Partition
let (evens, odds): (Vec<_>, Vec<_>) =
    numbers.iter().partition(|&&x| x % 2 == 0);
```

### Custom Iterators

```rust
pub struct Fibonacci {
    curr: u64,
    next: u64,
}

impl Iterator for Fibonacci {
    type Item = u64;

    fn next(&mut self) -> Option<Self::Item> {
        let current = self.curr;
        self.curr = self.next;
        self.next += current;
        Some(current)
    }
}

// Usage
for num in Fibonacci::new().take(10) {
    println!("{}", num);
}
```

---

## Trait Implementation

### Standard Traits

Always implement when applicable:

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct User {
    pub id: UserId,
    pub name: String,
}

// Display for user-facing output
impl fmt::Display for User {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "User(id={}, name={})", self.id, self.name)
    }
}

// From for convenient conversions
impl From<UserDto> for User {
    fn from(dto: UserDto) -> Self {
        Self {
            id: UserId::from(dto.id),
            name: dto.name,
        }
    }
}

// TryFrom for fallible conversions
impl TryFrom<&str> for UserId {
    type Error = ParseError;

    fn try_from(s: &str) -> Result<Self, Self::Error> {
        uuid::Uuid::parse_str(s)
            .map(UserId)
            .map_err(|_| ParseError::InvalidUuid)
    }
}
```

### Trait Bounds

Use `where` clauses for complex bounds:

```rust
fn process<T>(item: T) -> Result<Output>
where
    T: Serialize + DeserializeOwned + Send + Sync + 'static,
{
    // Implementation
}
```

### Avoid Over-Generic Code

```rust
// BAD ❌ Too generic
fn do_thing<T, U, V, F, G>(t: T, f: F, g: G) -> Result<V>
where
    T: Into<U>,
    U: SomeTrait,
    F: Fn(U) -> V,
    G: Fn(Error) -> Error,
{
    // Hard to understand
}

// GOOD ✅ Concrete types
fn transform_user(
    user_dto: UserDto,
    transformer: impl Fn(UserDto) -> User,
) -> Result<User, ValidationError> {
    let user = transformer(user_dto);
    validate_user(&user)?;
    Ok(user)
}
```

---

## Performance Tips

### Allocation Reduction

```rust
// BAD ❌ Many allocations
fn build_message(parts: &[&str]) -> String {
    let mut msg = String::new();
    for part in parts {
        msg = msg + part; // Reallocates each time!
    }
    msg
}

// GOOD ✅ Pre-allocate
fn build_message(parts: &[&str]) -> String {
    let total_len: usize = parts.iter().map(|s| s.len()).sum();
    let mut msg = String::with_capacity(total_len);
    for part in parts {
        msg.push_str(part);
    }
    msg
}

// BEST ✅ Use join
fn build_message(parts: &[&str]) -> String {
    parts.join("")
}
```

### Stack vs Heap

```rust
// Stack for small arrays
let buffer: [u8; 1024] = [0; 1024];

// Heap for dynamic/large data
let large_buffer = vec![0u8; 1024 * 1024];

// Box for large structs
let large_struct = Box::new(VeryLargeStruct::default());
```

---

## Advanced Topics

### Type System Mastery

#### Newtype Pattern for Type Safety

Use newtypes to prevent mixing up similar types:

```rust
// EXCELLENT: Use newtypes to prevent mixing up similar types
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct UserId(uuid::Uuid);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct SessionId(uuid::Uuid);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ProductId(uuid::Uuid);

impl UserId {
    pub fn new() -> Self {
        Self(uuid::Uuid::new_v4())
    }

    pub fn from_str(s: &str) -> Result<Self, uuid::Error> {
        Ok(Self(uuid::Uuid::parse_str(s)?))
    }
}

// Now this won't compile (type safety!):
fn get_user(id: UserId) -> User { /* ... */ }
let product_id = ProductId::new();
// get_user(product_id);  // Compile error! Can't mix types
```

#### Builder Pattern for Complex Construction

```rust
pub struct ServerConfig {
    host: String,
    port: u16,
    max_connections: usize,
    timeout: Duration,
    tls_config: Option<TlsConfig>,
}

impl ServerConfig {
    pub fn builder() -> ServerConfigBuilder {
        ServerConfigBuilder::default()
    }
}

#[derive(Default)]
pub struct ServerConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
    max_connections: Option<usize>,
    timeout: Option<Duration>,
    tls_config: Option<TlsConfig>,
}

impl ServerConfigBuilder {
    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    pub fn build(self) -> Result<ServerConfig, ConfigError> {
        Ok(ServerConfig {
            host: self.host.ok_or(ConfigError::MissingHost)?,
            port: self.port.unwrap_or(8080),
            max_connections: self.max_connections.unwrap_or(100),
            timeout: self.timeout.unwrap_or(Duration::from_secs(30)),
            tls_config: self.tls_config,
        })
    }
}

// Usage
let config = ServerConfig::builder()
    .host("localhost")
    .port(3000)
    .max_connections(500)
    .build()?;
```

#### State Machines with Type States

```rust
// EXCELLENT: Use type states to make invalid states unrepresentable
pub struct Connection<State> {
    socket: TcpStream,
    state: PhantomData<State>,
}

pub struct Disconnected;
pub struct Connected;
pub struct Authenticated;

impl Connection<Disconnected> {
    pub fn new(addr: &str) -> Result<Self, Error> {
        Ok(Self {
            socket: TcpStream::connect(addr)?,
            state: PhantomData,
        })
    }

    pub fn connect(self) -> Result<Connection<Connected>, Error> {
        // Perform connection handshake
        Ok(Connection {
            socket: self.socket,
            state: PhantomData,
        })
    }
}

impl Connection<Connected> {
    pub fn authenticate(
        self,
        credentials: &Credentials,
    ) -> Result<Connection<Authenticated>, Error> {
        // Perform authentication
        Ok(Connection {
            socket: self.socket,
            state: PhantomData,
        })
    }
}

impl Connection<Authenticated> {
    pub fn send_message(&mut self, msg: &Message) -> Result<(), Error> {
        // Only authenticated connections can send messages
        Ok(())
    }
}

// Usage - compile-time state checking!
let conn = Connection::<Disconnected>::new("localhost:8080")?;
// conn.send_message(&msg)?;  // Compile error! Not authenticated
let conn = conn.connect()?;
let mut conn = conn.authenticate(&creds)?;
conn.send_message(&msg)?;  // OK!
```

### Ownership, Borrowing, and Lifetimes

#### Smart Pointer Usage

```rust
use std::rc::Rc;
use std::sync::Arc;
use std::cell::{RefCell, Cell};

// Arc for thread-safe shared ownership
let data = Arc::new(expensive_data);
let data_clone = Arc::clone(&data);
thread::spawn(move || {
    process(data_clone);
});

// Rc for single-threaded shared ownership
let config = Rc::new(Config::load()?);
let service1 = Service::new(Rc::clone(&config));
let service2 = Service::new(Rc::clone(&config));

// RefCell for interior mutability (single-threaded)
let cache = RefCell::new(HashMap::new());
cache.borrow_mut().insert(key, value);
let val = cache.borrow().get(&key).cloned();

// Cell for Copy types
let counter = Cell::new(0);
counter.set(counter.get() + 1);
```

#### Lifetime Elision and Complex Lifetimes

```rust
// No lifetime annotations needed - elision rule 1
fn first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap_or("")
}

// Explicit lifetimes for multiple inputs
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Complex lifetime relationships
fn parse_header<'input, 'headers>(
    input: &'input [u8],
    headers: &'headers mut HeaderMap,
) -> Result<&'input [u8], Error>
where
    'input: 'headers,  // 'input outlives 'headers
{
    Ok(input)
}
```

#### Avoiding Unnecessary Clones

```rust
// BAD: Cloning everything
fn process_data(data: Vec<String>) -> Vec<String> {
    data.iter()
        .map(|s| s.clone().to_uppercase())  // Unnecessary clone!
        .collect()
}

// GOOD: Use references
fn process_data(data: &[String]) -> Vec<String> {
    data.iter()
        .map(|s| s.to_uppercase())  // No clone needed
        .collect()
}

// EXCELLENT: Use Cow for conditional cloning
use std::borrow::Cow;

fn normalize<'a>(input: &'a str) -> Cow<'a, str> {
    if input.chars().all(|c| c.is_lowercase()) {
        Cow::Borrowed(input)  // No allocation!
    } else {
        Cow::Owned(input.to_lowercase())  // Allocate only when needed
    }
}
```

### Common Pitfalls

#### Pitfall 1: String Handling Inefficiency

```rust
// BAD
fn process(s: String) -> String {
    s.to_uppercase()  // Takes ownership, caller must clone
}

// GOOD
fn process(s: &str) -> String {
    s.to_uppercase()  // Borrows, no clone needed
}

// EXCELLENT: Return Cow for zero-copy when possible
fn process(s: &str) -> Cow<'_, str> {
    if s.is_empty() {
        Cow::Borrowed(s)
    } else {
        Cow::Owned(s.to_uppercase())
    }
}
```

#### Pitfall 2: Mutex Deadlocks

**For async code:** See [Pitfall 3: Holding Locks Across Await Points](../rust-with-async-code/skill.md#pitfall-3-holding-locks-across-await-points) for complete guidance on async-safe mutex usage.

**For sync code:**

```rust
// BAD: Acquiring locks in wrong order (potential deadlock)
fn process(mutex_a: &Mutex<Data>, mutex_b: &Mutex<Data>) {
    let guard_a = mutex_a.lock().unwrap();
    // If another thread locks b then a, deadlock!
    let guard_b = mutex_b.lock().unwrap();
}

// GOOD: Always acquire locks in same order
fn process(mutex_a: &Mutex<Data>, mutex_b: &Mutex<Data>) {
    // Establish global lock ordering
    let guard_a = mutex_a.lock().unwrap();
    let guard_b = mutex_b.lock().unwrap();
}
```

#### Pitfall 3: Collecting Unnecessarily

```rust
// BAD
let sum = numbers
    .iter()
    .map(|x| x * 2)
    .collect::<Vec<_>>()  // Unnecessary allocation!
    .iter()
    .sum();

// GOOD
let sum: i32 = numbers
    .iter()
    .map(|x| x * 2)
    .sum();  // Direct sum, no allocation
```

#### Pitfall 4: Large Stack Allocations

```rust
// BAD: Can cause stack overflow
let big_array = [0u8; 1024 * 1024];  // 1MB on stack!

// GOOD: Use Vec for large data
let big_array = vec![0u8; 1024 * 1024];  // Heap allocated

// GOOD: Use Box for large structs
let large_struct = Box::new(VeryLargeStruct::default());
```

### Macros (When Needed)

```rust
// Declarative macros for repetitive code
macro_rules! impl_id_type {
    ($name:ident) => {
        #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
        pub struct $name(uuid::Uuid);

        impl $name {
            pub fn new() -> Self {
                Self(uuid::Uuid::new_v4())
            }
        }

        impl Default for $name {
            fn default() -> Self {
                Self::new()
            }
        }
    };
}

impl_id_type!(UserId);
impl_id_type!(SessionId);
impl_id_type!(ProductId);
```

### Unsafe Code (Use Sparingly)

```rust
// Only use unsafe when absolutely necessary
// MUST document invariants and safety guarantees

/// # Safety
///
/// The caller must ensure that:
/// - `ptr` is valid for reads of `len` bytes
/// - `ptr` is properly aligned
/// - The memory referenced by `ptr` is initialized
/// - No other threads are accessing this memory
pub unsafe fn read_raw_bytes(ptr: *const u8, len: usize) -> Vec<u8> {
    // SAFETY: Caller guarantees pointer validity
    unsafe {
        std::slice::from_raw_parts(ptr, len).to_vec()
    }
}
```

### FFI (Foreign Function Interface)

```rust
// When interfacing with C code
use std::ffi::{CStr, CString};
use std::os::raw::c_char;

#[link(name = "mylib")]
extern "C" {
    fn external_function(input: *const c_char) -> i32;
}

pub fn safe_wrapper(input: &str) -> Result<i32, Error> {
    let c_string = CString::new(input)?;

    // SAFETY: c_string is valid C string, external_function expects C string
    let result = unsafe { external_function(c_string.as_ptr()) };

    Ok(result)
}
```

---

## Learning Log

### 2026-01-28: Skill Restructuring

**Issue:** Original skill.md was 2271 lines with massive duplication and mixed concerns.

**Learning:** Separated concerns into focused sections. Removed 1500+ lines of duplicated verification workflow and learning log content. Created dedicated example markdown files.

**New Standard:** Skills should be concise (< 500 lines), focused, and reference separate example files.

### 2026-01-27: Testing Anti-Patterns

**Issue:** Tests creating variables without validation.

**Learning:** Every test must assert on outputs. Tests without assertions provide false confidence.

**Standard:** All tests must validate actual behavior, not just call functions.

### 2026-01-23: no_std/std Strategy

**Issue:** Needed clear guidelines for hybrid libraries.

**Learning:** Re-export std types when sufficient; only implement from scratch for no_std-specific features.

**Standard:** Move complexity to compatibility layers; keep consuming code simple.

### 2026-01-24: Feature-Gated Type Architecture Pattern

**Issue:** Managing complex feature combinations in no_std/std hybrid libraries.

**Problem:** Mixing std and no_std types directly in consuming modules creates complex feature gates everywhere.

**Solution:** Create compatibility layers in higher-level dependencies.

#### Pattern: Compatibility Module Approach

1. Move types to higher-level dependency
2. Implement std and no_std variants with **same API**
3. Create compatibility module with feature-gated exports
4. Lower modules use simple imports

**Example - CondVar + Mutex Pairing:**

```rust
// BAD ❌ - Feature gates in consuming code
#[cfg(feature = "std")]
use std::sync::{Mutex, Condvar};
#[cfg(not(feature = "std"))]
use foundation_nostd::primitives::condvar::{CondVarMutex as Mutex, CondVar};

// GOOD ✅ - Compatibility layer in foundation_nostd/src/comp/condvar_comp.rs
#[cfg(feature = "std")]
pub use std::sync::{Mutex, Condvar as CondVar};
#[cfg(not(feature = "std"))]
pub use crate::primitives::condvar::{CondVarMutex as Mutex, CondVar};

// Consuming code - SIMPLE
use foundation_nostd::comp::condvar_comp::{Mutex, CondVar};
```

**Benefits:**
- Simple consuming code (no feature gates in business logic)
- Centralized feature complexity
- Type safety (ensures compatible types paired)
- API consistency across std/no_std

**When to Use:**
- ✅ Types that must work together (Mutex + CondVar)
- ✅ Complex feature combinations (ssl backends)
- ✅ Platform-specific implementations
- ❌ Simple single types (regular comp::Mutex fine)

**Key Principle:** Move complexity up to dependency, keep consuming code simple.

**Explicit Imports Requirement:** Always use explicit submodule paths, never wildcard re-exports:

```rust
// GOOD ✅ - Explicit
use foundation_nostd::comp::basic::{Mutex, RwLock};
use foundation_nostd::comp::condvar_comp::{Mutex, CondVar};

// BAD ❌ - Ambiguous (removed)
use foundation_nostd::comp::{Mutex, RwLock};  // Which Mutex?
```

---

## Examples

See `examples/` directory for detailed guides:

- `documentation-patterns.md` - WHY/WHAT/HOW patterns with mandatory panic documentation
- `error-handling-guide.md` - Error types with derive_more
- `security-guide.md` - Input validation, secrets, SQL/command injection
- `iterator-patterns.md` - Iterator combinators and custom iterators
- `basic-template.md` - Starting template for new code

See `templates/` directory for starter code:

- `basic-example.rs` - Starter template for new Rust modules

## Related Skills

- [Rust Testing Excellence](../rust-testing-excellence/skill.md) - For writing tests
- [Rust with Async Code](../rust-with-async-code/skill.md) - For async/await patterns
- [Rust Directory Setup](../rust-directory-and-configuration/skill.md) - For project setup

---

*Last Updated: 2026-01-28*
*Version: 3.1-approved*
