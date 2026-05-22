---
name: review-rust-code
description: Review and enforce Rust best practices, clean code principles, and idiomatic patterns. Use when reviewing code, writing new Rust code, or refactoring existing implementations. Covers type-driven design, error handling, async patterns, testing, and project-specific standards.
---

# Review Rust Code - Best Practices & Standards

**Context**: Feather-Flow is a schema validation framework with static analysis as a first-class citizen. See **[HOW_FEATHERFLOW_WORKS.md](../../../HOW_FEATHERFLOW_WORKS.md)** for the full architecture. Code review should ensure changes align with the core goal: mandatory schemas, compile-time validation before execution, AST-based analysis, and the one-node-one-transformation principle.

Apply these standards when working with Rust code in this project. These patterns leverage Rust's type system, ownership model, and trait system to make illegal states unrepresentable and enforce clean code at compile time.

## Core Principles

1. **Never nest**: Max 3 levels of indentation — if you hit 4, refactor
2. **Type-driven design**: Use the type system to make invalid states unrepresentable
3. **Parse, don't validate**: Enforce invariants at construction time
4. **No `unwrap()` outside tests**: Every `unwrap()` is an implicit assertion that something can never fail — use `?` or `.expect("reason")`
5. **No `clone()` to appease the borrow checker**: Restructure ownership, use `Cow<T>`, `Arc`, or references instead
6. **Minimal visibility**: `pub` is a code smell unless you're building a library API — default to private, then `pub(crate)`, then `pub(super)`, then `pub`
7. **AST over regex**: Use proper parsers and abstract syntax trees instead of string manipulation
8. **No inline comments**: Code should be self-explanatory — if it needs a comment, the code needs rewriting
9. **Prefer iterators over manual loops**: `.iter().filter().map().collect()` over `for` loops with mutable accumulators
10. **Clippy is not optional**: `cargo clippy` is mandatory in CI and local development
11. **Separate test files**: Tests go in `_test.rs` files, not inline `#[cfg(test)] mod tests`

---

## The Never Nester's Rules

**The hard constraint: max 3 levels of indentation.** If you hit 4, refactor. Two fundamental techniques plus Rust-specific superpowers.

### Technique 1: Inversion (Early Returns / Guard Clauses)

Check the unhappy case first, bail out, let the happy path flow downward. Rust gives you three distinct tools for this.

#### The `?` Operator — Inversion for free

The single most powerful de-nesting tool in Rust. It replaces entire `match` trees with a single character:

```rust
// BAD: 3 levels of nesting
fn process_order(id: u32) -> Result<Receipt, AppError> {
    match find_order(id) {
        Ok(order) => {
            match validate(&order) {
                Ok(valid) => {
                    match charge(valid) {
                        Ok(receipt) => Ok(receipt),
                        Err(e) => Err(e.into()),
                    }
                }
                Err(e) => Err(e.into()),
            }
        }
        Err(e) => Err(e.into()),
    }
}

// GOOD: Zero nesting — each ? is an implicit early return on the error path
fn process_order(id: u32) -> Result<Receipt, AppError> {
    let order = find_order(id)?;
    let valid = validate(&order)?;
    let receipt = charge(valid)?;
    Ok(receipt)
}
```

Set up proper `From` impls on your error types so `?` chains cleanly. This alone eliminates most nesting in Rust.

#### `let-else` — Guard clauses for pattern matching

When you need to unwrap an `Option` or destructure an enum but bail on the unhappy case:

```rust
// BAD: Nested if-let pyramid
fn get_display_name(user_id: u32) -> Result<String, AppError> {
    if let Some(user) = find_user(user_id) {
        if let Some(profile) = user.profile {
            if let Some(name) = profile.display_name {
                Ok(name)
            } else {
                Err(AppError::MissingName)
            }
        } else {
            Err(AppError::NoProfile)
        }
    } else {
        Err(AppError::NotFound)
    }
}

// GOOD: Flat guard clauses — declare requirements up front, then do the real work
fn get_display_name(user_id: u32) -> Result<String, AppError> {
    let Some(user) = find_user(user_id) else {
        return Err(AppError::NotFound);
    };
    let Some(profile) = user.profile else {
        return Err(AppError::NoProfile);
    };
    let Some(name) = profile.display_name else {
        return Err(AppError::MissingName);
    };
    Ok(name)
}
```

#### Classic early returns with boolean guards

```rust
fn process(items: &[Item]) -> Result<Summary, AppError> {
    if items.is_empty() {
        return Err(AppError::EmptyInput);
    }
    if !items.iter().all(|i| i.is_valid()) {
        return Err(AppError::InvalidItems);
    }
    compute_summary(items)
}
```

### Technique 2: Extraction (Pull blocks into named functions)

When your loop body or match arm gets complex, extract it:

```rust
// BAD: Deeply nested match-in-a-loop
fn run(&mut self) {
    for download in &mut self.downloads {
        match download.state {
            State::Pending => {
                match self.client.start(&download.url) {
                    Ok(handle) => { /* ... */ }
                    Err(e) => { /* ... */ }
                }
            }
            State::InProgress => {
                match download.handle.process() {
                    Status::Done => { /* ... */ }
                    Status::Error(e) => {
                        match e.kind() {
                            // 4+ deep — unacceptable
                        }
                    }
                    _ => {}
                }
            }
        }
    }
}

// GOOD: run() is a table of contents
fn run(&mut self) {
    self.process_queue();
    self.process_downloads();
    self.cleanup_completed();
    self.wait_for_signal();
}

fn process_downloads(&mut self) {
    for download in &mut self.downloads {
        match download.state {
            State::Pending => self.start_download(download),
            State::InProgress => self.check_progress(download),
            _ => {}
        }
    }
}
```

### Rust-Specific De-Nesting Techniques

#### Combinator chains on `Option`/`Result`

Instead of nested `if let`, chain transformations:

```rust
// BAD: Nested
fn get_config_port(config: &Config) -> u16 {
    if let Some(server) = &config.server {
        if let Some(port) = server.port {
            port
        } else {
            8080
        }
    } else {
        8080
    }
}

// GOOD: Flat with combinators
fn get_config_port(config: &Config) -> u16 {
    config.server
        .as_ref()
        .and_then(|s| s.port)
        .unwrap_or(8080)
}
```

#### `match` as an expression (not a statement)

Assign directly from `match` to avoid nesting:

```rust
let action = match download.status {
    Status::Complete => Action::Remove,
    Status::Failed(e) if e.retryable() => Action::Retry,
    Status::Failed(_) => Action::Fail,
    Status::InProgress => Action::Continue,
};
```

#### State machine enums to eliminate conditional nesting

If you find yourself with nested conditions checking combinations of booleans, encode valid states in an enum:

```rust
// GOOD: Eliminates a whole class of nested if/else
enum Connection {
    Disconnected,
    Connecting { attempt: u32 },
    Connected { session: Session },
    Failed { reason: String, retries: u32 },
}

// BAD: Bag of booleans where half the combinations are nonsensical
struct Connection {
    is_connected: bool,
    is_connecting: bool,
    is_failed: bool,
    session: Option<Session>,
    attempt: Option<u32>,
    failure_reason: Option<String>,
}
```

### Never Nester Summary

1. **Max 3 levels of indentation.** Period.
2. **Use `?` aggressively.** Set up `From` impls so `?` chains cleanly.
3. **Use `let-else` for guard clauses** on `Option`/`Result`/pattern matches.
4. **Early return for boolean guards** — check the bad case, bail, keep the happy path flowing down.
5. **Extract match arms and loop bodies** into named methods when they grow beyond a few lines.
6. **Use combinators** (`.map`, `.and_then`, `.unwrap_or_else`) to flatten `Option`/`Result` transformations.
7. **Encode state in enums**, not in nested conditionals over booleans.

---

## Rust Discipline

These are community conventions enforced as hard rules in this project. The compiler doesn't require any of them — the discipline does.

### No `unwrap()` outside tests

Every `unwrap()` is an implicit assertion that something can never fail. If you're wrong, you get a panic with a useless message instead of a recoverable error.

```rust
// BAD: unwrap in production code
let user = find_user(id).unwrap();

// ACCEPTABLE: expect() with a reason (grudging compromise)
let user = find_user(id).expect("user must exist after auth check");

// GOOD: The true path
let user = find_user(id)?;

// OK: unwrap in tests
#[test]
fn test_something() {
    let result = do_thing().unwrap();
    assert_eq!(result, expected);
}
```

### No `clone()` to appease the borrow checker

When fighting lifetimes, don't sprinkle `.clone()` everywhere to make it compile. Restructure so data flows naturally.

```rust
// BAD: Cloning to satisfy the borrow checker
fn process(data: &Data) {
    let owned = data.name.clone();
    let result = transform(&owned);
    use_result(result, &data.name.clone());
}

// GOOD: Restructure ownership or use references
fn process(data: &Data) {
    let result = transform(&data.name);
    use_result(result, &data.name);
}

// ACCEPTABLE: When clone is the genuinely pragmatic choice (and you know it)
// e.g., small Copy types, Arc::clone for shared ownership, one-time setup
let config = Arc::clone(&shared_config);
```

### Prefer iterators over manual loops

Iterator chains are more idiomatic, composable, and less error-prone. The compiler generates identical code.

```rust
// BAD: Manual loop with mutable accumulator
fn get_active_names(users: &[User]) -> Vec<String> {
    let mut names = Vec::new();
    for user in users {
        if user.is_active {
            names.push(user.name.clone());
        }
    }
    names
}

// GOOD: Iterator chain
fn get_active_names(users: &[User]) -> Vec<String> {
    users.iter()
        .filter(|u| u.is_active)
        .map(|u| u.name.clone())
        .collect()
}
```

### No `Rc<RefCell<T>>` without genuine reason

`Rc<RefCell<T>>` opts out of Rust's compile-time borrow checking. It has legitimate uses (tree structures, graphs) but reaching for it in application code means your architecture needs rethinking.

### No async in library code unless you actually need it

Libraries should be runtime-agnostic and synchronous where possible. Making a library function `async` forces users into a specific executor model. Only add `async` when the function genuinely performs I/O.

### Implement `Display` for error types, not just `Debug`

Errors should produce human-readable messages. Use `thiserror` for automatic `Display` impls:

```rust
// GOOD: thiserror gives you Display for free
#[derive(Error, Debug)]
pub enum AppError {
    #[error("user {user_id} not found")]
    NotFound { user_id: u32 },

    #[error("database connection failed")]
    Database(#[from] sqlx::Error),
}

// BAD: Only deriving Debug — errors print as AppError { kind: NotFound, ... }
#[derive(Debug)]
pub struct AppError {
    kind: ErrorKind,
    context: Option<String>,
}
```

### Clippy is mandatory

`cargo clippy` is not optional. Run it locally, enforce it in CI. Treat clippy warnings as errors:

```bash
cargo clippy -- -D warnings
```

---

## Comments and Inline Code

**Project standard: No inline comments.** Write self-explanatory code. If the code needs a comment to be understood, the code needs to be rewritten with better names, smaller functions, or clearer structure.

### What is never acceptable

```rust
// BAD: Inline comments that narrate the code
fn process_payment(amount: Decimal) -> Result<Payment> {
    // Convert amount to cents
    let amount_cents = (amount * 100).round() as i64;

    // Call stripe charge function
    let payment = stripe::charge(amount_cents)?;

    // Return the payment
    Ok(payment)
}

// BAD: Comments compensating for unclear code
fn calc(u: &User, t: &Task) -> f64 {
    // Calculate the priority score based on task urgency and importance
    let x = if t.d < Utc::now() + Duration::days(1) { 2.0 } else { 1.0 };
    let y = if t.i == Impact::High { 2.0 } else { 1.0 };
    x * y
}
// Fix: Make the code clear, delete the comment
fn calculate_priority_score(user: &User, task: &Task) -> f64 {
    let urgency_multiplier = if task.due_date < Utc::now() + Duration::days(1) { 2.0 } else { 1.0 };
    let importance_multiplier = if task.impact == Impact::High { 2.0 } else { 1.0 };
    urgency_multiplier * importance_multiplier
}

// BAD: Commented-out code (use version control)
pub fn calculate_total(items: &[Item]) -> Decimal {
    // let total = items.iter().map(|i| i.price).sum();
    // total * Decimal::new(109, 2) // Old tax rate
    items.iter()
        .map(|i| i.price * Decimal::new(108, 2))
        .sum()
}
```

### What is acceptable (sparingly)

```rust
// OK: Explains WHY — non-obvious business logic or external constraints
fn process_payment(amount: Decimal) -> Result<Payment> {
    // Stripe requires amounts in cents, not dollars
    let amount_cents = (amount * 100).round() as i64;

    // Stripe returns transient 500s during high load (see incident #1234)
    let payment = retry_with_backoff(|| stripe::charge(amount_cents), 3)?;
    Ok(payment)
}

// OK: Non-obvious business rule
pub fn can_refund(order: &Order) -> bool {
    // Per company policy, refunds allowed within 30 days unless QA-flagged as defective
    order.created_at > Utc::now() - Duration::days(30) || order.is_defective
}

// OK: TODO with ticket reference
pub fn legacy_import(data: &OldFormat) -> Result<NewFormat> {
    // TODO(#1842): Remove after migration completes (Q2 2026)
    convert_legacy_format(data)
}
```

### The rule of thumb

If you're tempted to write a comment, first try:
1. Rename the variable/function to be self-describing
2. Extract a helper function whose name explains the operation
3. Use a newtype or enum to encode the meaning in the type system

If none of those work and the "why" still isn't obvious, then a comment is acceptable.

### Doc comments for public APIs

Public items get `///` doc comments. These are documentation, not inline comments — they describe the contract, not the implementation:

```rust
/// Processes a user payment through the payment provider.
///
/// # Errors
///
/// Returns `PaymentError::InsufficientFunds` if the account balance is too low.
/// Returns `PaymentError::NetworkError` if unable to reach the payment provider.
pub fn process_payment(amount: Decimal, method: PaymentMethod) -> Result<Payment, PaymentError> {
    // ...
}
```

---

## Test File Organization

**Project standard: Tests go in separate `_test.rs` files**, following the Go convention of keeping test code out of production files.

### Unit tests

```
src/
  model.rs          # Production code only
  model_test.rs     # Unit tests for model.rs
  project.rs
  project_test.rs
```

```rust
// model_test.rs
#[cfg(test)]
use super::*;

#[test]
fn test_model_creation() {
    let model = Model::new("test");
    assert_eq!(model.name.as_str(), "test");
}
```

### Integration tests

Integration tests live in `tests/` at the crate root (standard Rust convention):

```
crate/
  src/
    lib.rs
    model.rs
    model_test.rs
  tests/
    integration_test.rs
```

### Why separate files

- Production files stay focused on production code
- Tests are easy to find — look for `_test.rs`
- Diffs are cleaner — test changes don't pollute production file history
- Files stay shorter and more navigable

---

## Early Returns and Guard Clauses

(See **The Never Nester's Rules** above for the full treatment with examples.)

### Prefer `ok_or_else` over `ok_or`

Use lazy evaluation to avoid unnecessary error construction:

```rust
// GOOD: Lazy evaluation
get_user().ok_or_else(|| AppError::NotFound("User not found".to_string()))?

// BAD: Eager evaluation (constructs error even on success path)
get_user().ok_or(AppError::NotFound("User not found".to_string()))?
```

---

## Type-Driven Design

### Newtype pattern for domain types

Wrap primitive types to prevent entire categories of bugs. Zero runtime cost.

```rust
// GOOD: Distinct types prevent mixing
struct UserId(Uuid);
struct ProductId(Uuid);

fn get_user(id: UserId) -> Option<User> { /* ... */ }

let product_id = ProductId(Uuid::new_v4());
// get_user(product_id);  // COMPILE ERROR: types don't match

// GOOD: If you have fn transfer(from: u64, to: u64, amount: u64),
// nothing stops swapping args. Use newtypes:
struct AccountId(u64);
struct Amount(u64);

fn transfer(from: AccountId, to: AccountId, amount: Amount) -> Result<()> { /* ... */ }
```

### Parse, don't validate

Instead of accepting a `String` and checking if it's valid at every call site, create a validated type whose constructor validates once:

```rust
pub struct Email(String);

impl Email {
    pub fn parse(s: String) -> Result<Self, ValidationError> {
        if is_valid_email(&s) {
            Ok(Email(s))
        } else {
            Err(ValidationError::InvalidEmail)
        }
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

// If an Email exists, it's guaranteed to be valid — no re-validation needed
```

### Make invalid states unrepresentable

Instead of a struct with `is_active: bool, is_verified: bool, is_banned: bool` where half the combinations are nonsensical, use an enum:

```rust
// GOOD: Each state carries exactly the data it needs
enum Order {
    Draft { items: Vec<Item> },
    Submitted { items: Vec<Item>, at: DateTime<Utc> },
    Paid { items: Vec<Item>, at: DateTime<Utc>, payment: Payment },
    Shipped { items: Vec<Item>, at: DateTime<Utc>, payment: Payment, tracking: TrackingInfo },
}

impl Order {
    fn submit(self) -> Result<Order, OrderError> {
        match self {
            Order::Draft { items } => Ok(Order::Submitted {
                items,
                at: Utc::now(),
            }),
            _ => Err(OrderError::InvalidTransition),
        }
    }
}

// BAD: Boolean flags and nullable fields
struct Order {
    items: Vec<Item>,
    submitted: bool,
    paid: bool,
    shipped: bool,
    payment: Option<Payment>,
    tracking: Option<TrackingInfo>,
}
```

### Typestate pattern for builders

Use the type system to enforce required fields at compile time:

```rust
struct RequestBuilder<State> {
    url: Option<String>,
    method: Option<String>,
    _state: PhantomData<State>,
}

struct NoUrl;
struct HasUrl;

impl RequestBuilder<NoUrl> {
    fn url(self, url: String) -> RequestBuilder<HasUrl> {
        RequestBuilder {
            url: Some(url),
            method: self.method,
            _state: PhantomData,
        }
    }
}

impl RequestBuilder<HasUrl> {
    fn build(self) -> Request {
        Request {
            url: self.url.unwrap(),
            method: self.method.unwrap_or_else(|| "GET".to_string()),
        }
    }
}
```

---

## Error Handling

### Use `thiserror` for libraries, `anyhow` for applications

```rust
// Library code with thiserror (gives you Display for free)
#[derive(Error, Debug)]
pub enum DataStoreError {
    #[error("data store disconnected")]
    Disconnect(#[from] io::Error),

    #[error("the data for key `{0}` is not available")]
    Redaction(String),

    #[error("invalid header (expected {expected:?}, found {found:?})")]
    InvalidHeader { expected: String, found: String },

    #[error(transparent)]
    Other(#[from] anyhow::Error),
}

// Application code with anyhow
fn run_app() -> Result<()> {
    let config = load_config()
        .context("Failed to load config")?;

    let db = connect_db(&config.db_url)
        .context("Failed to connect to database")?;

    Ok(())
}
```

### Always include error context

```rust
#[derive(Error, Debug)]
pub enum AppError {
    #[error("failed to process user {user_id}")]
    UserProcessing {
        user_id: u32,
        #[source]
        source: Box<dyn std::error::Error + Send + Sync>,
    },

    #[error("database error")]
    Database(#[from] sqlx::Error),
}
```

---

## SOLID Principles Through Traits

### Single Responsibility

Small, focused modules with visibility controls:

```rust
pub(crate) mod user_service {
    use super::User;

    pub(crate) fn create_user(email: &str) -> Result<User, Error> {
        // Single responsibility: user creation
    }
}
```

### Open/Closed — Extend via trait implementations

```rust
trait Shape {
    fn area(&self) -> f64;
}

fn calculate_total_area(shapes: &[impl Shape]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}
```

### Interface Segregation — Small, focused traits

```rust
// GOOD: Types implement only what they need
trait Printer {
    fn print(&self, doc: &Document);
}

trait Scanner {
    fn scan(&self) -> Document;
}

// BAD: Monolithic trait
trait Machine {
    fn print(&self, doc: &Document);
    fn scan(&self) -> Document;
    fn fax(&self, doc: &Document, number: &str);
}
```

### Dependency Inversion — Trait-based DI

```rust
trait Messenger {
    fn send(&self, user: &str, message: &str);
}

struct NotificationService<M: Messenger> {
    messenger: M,
}

impl<M: Messenger> NotificationService<M> {
    fn notify(&self, user: &str, message: &str) {
        self.messenger.send(user, message);
    }
}
```

Decision matrix:
- **Generics** (`impl Trait`, `<T: Trait>`): compile-time DI, zero cost
- **Trait objects** (`Box<dyn Trait + Send + Sync>`): runtime polymorphism, heterogeneous collections

---

## Trait Design

### Static vs. dynamic dispatch

```rust
// Static dispatch: zero cost, but increases binary size
fn process_shapes_static(shapes: &[impl Shape]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}

// Dynamic dispatch: runtime polymorphism, vtable overhead
fn process_shapes_dynamic(shapes: &[Box<dyn Shape + Send + Sync>]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}
```

### Associated types vs. generic parameters

```rust
// Associated types: one logical implementation per type
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}

// Generic parameters: multiple implementations make sense
trait From<T> {
    fn from(value: T) -> Self;
}
```

### Sealed traits

```rust
mod sealed {
    pub trait Sealed {}
}

pub trait MyTrait: sealed::Sealed {
    fn method(&self);
}

impl sealed::Sealed for MyType {}
impl MyTrait for MyType {
    fn method(&self) { /* ... */ }
}
```

---

## Ownership Patterns

### Use `Cow` for flexible borrowing

```rust
use std::borrow::Cow;

fn process_text(input: &str) -> Cow<str> {
    if input.contains("old") {
        Cow::Owned(input.replace("old", "new"))
    } else {
        Cow::Borrowed(input)
    }
}
```

### Multi-threaded patterns

```rust
// Arc<T> for immutable shared data
let shared_config = Arc::new(Config::load());

// Arc<RwLock<T>> for read-heavy mutable data
let cache = Arc::new(RwLock::new(HashMap::new()));

// Keep critical sections minimal
{
    let mut data = cache.write().unwrap();
    data.insert(key, value);
}
```

---

## Module Organization

### Visibility hierarchy

Default to private, expose deliberately:

```rust
mod internal {
    pub(crate) struct Helper;

    impl Helper {
        pub(super) fn assist(&self) { /* ... */ }
        fn private_method(&self) { /* ... */ }
    }
}

// lib.rs: Curated public API
pub use crate::internal::Helper;
```

### Prelude pattern

```rust
pub mod prelude {
    pub use crate::{Error, Result};
    pub use crate::traits::{Process, Validate};
    pub use crate::types::{UserId, Email};
}
```

---

## AST Parsing Over String Manipulation

**Project-specific standard**: When working with SQL queries, templates, or code generation, always use the parser's AST.

```rust
// GOOD: Using the SQL parser's AST
fn extract_table_references(sql: &str) -> Result<Vec<String>> {
    let ast = Parser::parse_sql(sql)?;
    let extractor = DependencyExtractor::new();
    Ok(extractor.extract_tables(&ast))
}

// BAD: Using regex for SQL manipulation
fn extract_table_references_bad(sql: &str) -> Vec<String> {
    let re = Regex::new(r"FROM\s+(\w+)").unwrap();
    re.captures_iter(sql)
        .map(|cap| cap[1].to_string())
        .collect()
    // Misses JOINs, subqueries, CTEs. Breaks on qualified names.
    // Can't handle comments or strings containing FROM. Fragile.
}
```

Regex is acceptable only for simple pattern matching that doesn't require understanding structure (e.g., extracting template placeholders, normalizing whitespace).

---

## Async Patterns

### Never block the async runtime

```rust
// GOOD: Use spawn_blocking for blocking or CPU-intensive operations
async fn process_data(data: Vec<u8>) -> Result<String> {
    let result = task::spawn_blocking(move || {
        expensive_computation(data)
    }).await??;
    Ok(result)
}
```

### Don't hold `std::sync::Mutex` across `.await`

Use `tokio::sync::Mutex` for async code.

### Cancellation safety

```rust
// GOOD: Keep mutable state outside futures
loop {
    select! {
        result = operation1() => { state.update(result); }
        result = operation2() => { state.update(result); }
    }
}
```

### Async traits

```rust
// Native async fn in traits (Rust 1.75+, not dyn-compatible)
trait Repository {
    async fn get(&self, id: u64) -> Result<Item>;
}

// Use async-trait for trait objects
#[async_trait]
trait DynRepository: Send + Sync {
    async fn get(&self, id: u64) -> Result<Item>;
}
```

---

## Testing

### Test file organization

Tests go in separate `_test.rs` files:

```
src/
  model.rs           # Production code
  model_test.rs      # Tests for model.rs
```

```rust
// model_test.rs
#[cfg(test)]
use super::*;

#[test]
fn model_from_file_requires_yaml() {
    let dir = tempfile::TempDir::new().unwrap();
    // ...
}
```

### Table-based testing

Use table-based testing to avoid duplicating test logic:

```rust
#[rstest]
#[case("valid@email.com", true)]
#[case("invalid.email", false)]
#[case("@invalid.com", false)]
#[case("", false)]
fn test_email_validation(#[case] email: &str, #[case] expected_valid: bool) {
    let result = Email::parse(email.to_string());
    assert_eq!(result.is_ok(), expected_valid);
}
```

### Property-based testing

```rust
proptest! {
    #[test]
    fn test_reversible_encoding(data: Vec<u8>) {
        let encoded = encode(&data);
        let decoded = decode(&encoded);
        prop_assert_eq!(data, decoded);
    }
}
```

### Mocking with mockall

```rust
#[automock]
trait Database {
    fn get_user(&self, id: u32) -> Result<User>;
}

#[test]
fn test_with_mock() {
    let mut mock = MockDatabase::new();
    mock.expect_get_user()
        .with(eq(123))
        .times(1)
        .returning(|_| Ok(User::default()));

    let service = UserService::new(mock);
    assert!(service.get_user(123).is_ok());
}
```

---

## Structured Logging

### Use tracing with structured fields

```rust
#[instrument(skip(password))]
async fn login(username: &str, password: &str) -> Result<Session> {
    info!(username = %username, "Login attempt");
    let user = authenticate(username, password).await?;
    info!(user_id = %user.id, "Login successful");
    Ok(create_session(user))
}

// GOOD: Structured fields for filtering
info!(user_id = %id, action = "created", ip_address = %addr, "User created");

// BAD: String interpolation loses structure
info!("User {} created from {}", id, addr);
```

---

## Code Review Checklist

When reviewing Rust code, check:

- **Nesting**: No more than 3 levels of indentation anywhere
- **No `unwrap()`**: Only in tests — production code uses `?` or `.expect("reason")`
- **No gratuitous `clone()`**: Ownership restructured, not cloned away
- **Type safety**: Domain types using newtypes? Invalid states unrepresentable?
- **Error handling**: `thiserror` for libs, `anyhow` for apps? `Display` implemented? Context provided?
- **Early returns**: Functions use `?`, `let-else`, and guard clauses instead of nesting
- **Iterator chains**: Prefer `.iter().filter().map().collect()` over manual loops
- **Visibility**: Everything private by default, `pub(crate)` where needed, `pub` only for true API
- **AST parsing**: SQL/template manipulation uses AST parsers, not regex
- **No inline comments**: Code is self-explanatory; only "why" comments survive review
- **Test separation**: Tests in `_test.rs` files, not inline modules
- **Clippy clean**: `cargo clippy -- -D warnings` passes
- **No `Rc<RefCell<T>>`** in application code without justification
- **Async discipline**: No unnecessary `async` in library code; no blocking in async runtime
- **Trait design**: Static vs dynamic dispatch chosen deliberately; traits are small and focused

---

## Summary

These patterns make clean code the path of least resistance in Rust:

1. **Never nest beyond 3 levels** — use `?`, `let-else`, extraction, and combinators
2. **No `unwrap()` in production** — `?` is the true path
3. **No `clone()` to fight the borrow checker** — restructure ownership
4. **Make invalid states unrepresentable** with newtypes and state-machine enums
5. **No inline comments** — write self-explanatory code or refactor until it is
6. **Tests in separate `_test.rs` files** — keep production code clean
7. **Iterators over manual loops** — more idiomatic, composable, same performance
8. **Clippy is law** — no exceptions
9. **Visibility is minimal** — private by default, `pub` only when genuinely public API
10. **AST parsing over regex** for structural transformations

For detailed examples and supporting documentation, see [examples.md](examples.md).

---

## Verification

**After every unit of work, run `make ci` before moving on.** This ensures format, clippy, tests, and docs all pass. Do not proceed to the next task until CI is green.
