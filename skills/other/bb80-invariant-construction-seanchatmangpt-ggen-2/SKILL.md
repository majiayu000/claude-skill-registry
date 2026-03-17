# Big Bang 80/20: Invariant Construction Skill

**Auto-trigger**: Whenever you see "invariant", "monoidal", "compose", "single-pass", "constraint", "minimal", "type system"

## Core Concept

**Big Bang 80/20** means single-pass construction in low-entropy domains.

The key: **Extract invariants from specification, encode in types/structure, never violate.**

## What Are Invariants?

Invariants are **properties that must always be true**:

| Domain | Invariant | Rust Type |
|--------|-----------|-----------|
| User age | 0 ≤ age ≤ 150 | `newtype Age(u8)` + validation |
| Cache size | ≤ 10,000 entries | `BoundedCache<T, Const<10000>>` |
| File path | No directory traversal | `SafePath` wrapper type |
| Error handling | All errors Result<T,E> | `Result<T, Error>` |
| Concurrency | Thread-safe mutations | `Arc<Mutex<T>>` with graceful unwrap |

## Monoidal Composition (No Rework)

A system is **monoidal** if:
1. Components compose without modification
2. No adapters or glue code needed
3. Adding new components doesn't break old ones
4. Composition is associative and closed

**Example (Monoidal)**:
```rust
// Combine validators without modification
let validator = Age::validate
  .and_then(|age| Email::validate)
  .and_then(|email| Username::validate);
```

**Example (NOT Monoidal - requires rework)**:
```rust
// Each validator has different interface
if !age_is_valid(&age) { return Err(...); }
match email_is_valid(&email) {
  Ok(_) => ...,
  Err(e) => return Err(convert_email_error(e)), // Adaptation needed!
}
// More validators with different interfaces
```

Monoidal = Composition without rework = Single-pass = No iteration.

## Extracting Minimal Invariants

Process:
1. **From specification**: Identify all constraints
2. **Codify in types**: Use Rust type system
3. **Encode in structure**: Make violation impossible
4. **Validate at boundary**: User input only

### Step 1: Extract Constraints

From specification:
```
"User must be age 18-120. Email must be valid. Username must be 3-20 alphanumeric chars."
```

Constraints:
1. Age: ∈ [18, 120]
2. Email: Valid RFC 5322 format
3. Username: Length ∈ [3, 20], charset ∈ [a-zA-Z0-9_-]

### Step 2: Codify in Types

```rust
// Impossible to create invalid age
#[derive(Clone, Copy, Debug)]
pub struct Age(u8);

impl Age {
    pub fn new(val: u8) -> Result<Self, AgeError> {
        match val {
            18..=120 => Ok(Age(val)),
            _ => Err(AgeError::OutOfRange(val)),
        }
    }
    pub fn get(&self) -> u8 { self.0 }
}

// Once you have Age, it MUST be valid. No checks needed later.
fn process_user(age: Age) {
    // Age is proven valid at type level. No runtime checks.
    let years_until_100 = 100 - age.get();
}
```

### Step 3: Encode in Structure

Make the type system impossible to violate:

```rust
// Email type ensures validity
#[derive(Clone, Debug)]
pub struct Email(String);

impl Email {
    pub fn new(s: &str) -> Result<Self, EmailError> {
        if is_valid_email(s) {
            Ok(Email(s.to_string()))
        } else {
            Err(EmailError::InvalidFormat)
        }
    }
}

// Vec<ValidUser> = ALL elements are proven valid
pub struct ValidUser {
    age: Age,
    email: Email,
    username: Username,
}

fn process_users(users: Vec<ValidUser>) {
    // Every user in this vec is proven valid
    // No runtime validation needed
    for user in users {
        println!("{} is {}", user.email, user.age.get());
    }
}
```

### Step 4: Validate at Boundary

Only validate user input, never internally:

```rust
// BOUNDARY: User input
pub fn create_user(age_str: &str, email_str: &str) -> Result<ValidUser, Error> {
    let age = Age::new(age_str.parse()?)?;      // Validate here
    let email = Email::new(email_str)?;          // Validate here
    let username = Username::new("alice")?;      // Validate here

    Ok(ValidUser { age, email, username })      // Once created: proven valid
}

// INTERIOR: All operations on ValidUser never validate
fn update_profile(mut user: ValidUser) {
    // These operations are SAFE because ValidUser proves invariants
    user.age = Age::new(25)?;  // Wait, we're still validating?
    // Better pattern: types with validated constructors, like below
}
```

**Better pattern**:
```rust
// Types constructed at boundary, never mutated
pub struct ValidUser {
    age: Age,
    email: Email,
    username: Username,
}

fn process_user(user: &ValidUser) {
    // Age is proven valid. No checks.
    if user.age.get() > 50 { println!("Over 50"); }
}
```

## Type-First Design (For Rust)

### Pattern 1: NewType for Semantic Domains

```rust
// Instead of: fn process(score: i32) { ... }
// Use: fn process(score: Score) { ... }

#[derive(Clone, Copy)]
pub struct Score(i32);

impl Score {
    pub fn new(val: i32) -> Result<Self, ScoreError> {
        match val {
            0..=100 => Ok(Score(val)),
            _ => Err(ScoreError::OutOfRange),
        }
    }
}
```

### Pattern 2: Generic with Const for Bounds

```rust
use std::marker::PhantomData;
use typenum::Unsigned;

// "Cache with max 10,000 entries" enforced at type level
#[derive(Default)]
pub struct Cache<T, N: Unsigned> {
    data: Vec<T>,
    _phantom: PhantomData<N>,
}

impl<T, N: Unsigned> Cache<T, N> {
    pub fn push(&mut self, item: T) -> Result<(), CacheError> {
        if self.data.len() < N::USIZE {
            self.data.push(item);
            Ok(())
        } else {
            Err(CacheError::CapacityExceeded)
        }
    }
}

// Usage: Type proves max capacity
type BoundedCache = Cache<Item, typenum::U10000>;
```

### Pattern 3: Phantom Types for Proof

```rust
use std::marker::PhantomData;

#[derive(Clone)]
pub struct ValidPath<T>(PathBuf, PhantomData<T>);

pub struct Validated;

impl ValidPath<Validated> {
    pub fn new(path: &str) -> Result<Self, PathError> {
        // Check no directory traversal
        if path.contains("..") {
            return Err(PathError::TraversalDetected);
        }
        Ok(ValidPath(path.into(), PhantomData))
    }
}

// Only ValidPath<Validated> can reach this function
fn read_file(path: ValidPath<Validated>) -> Result<String> {
    // Path is PROVEN safe. No additional checks.
    std::fs::read_to_string(&path.0)
}
```

## Encoding Constraints (Ggen-Specific)

For ggen crate development:

### Path Protection (Monoidal)
```rust
// Instead of: fn generate(path: &str) -> Result<()> { ... }
// Use:
#[derive(Clone)]
pub struct ProtectedPath { inner: PathBuf }

impl ProtectedPath {
    pub fn new(path: &str) -> Result<Self, PathError> {
        // Verify against ggen_cli_validation::PATH_PROTECTION_RULES
        validate_protected_paths(path)?;
        validate_regenerate_paths(path)?;
        Ok(ProtectedPath { inner: path.into() })
    }
}

// Function that receives ProtectedPath is PROVEN safe
fn generate(path: ProtectedPath) -> Result<GeneratedCode> {
    // No path validation here - type system proves it's safe
    std::fs::write(&path.inner, code)
}
```

### RDF Specification (Monoidal)
```rust
// Specification proven valid at type level
#[derive(Clone)]
pub struct ValidRdfSpec {
    triples: Vec<Triple>,  // Proven valid RDF
}

impl ValidRdfSpec {
    pub fn load(ttl_path: &str) -> Result<Self> {
        let triples = parse_and_validate_ttl(ttl_path)?;
        // SPARQL queries verify SHACL constraints
        verify_shacl_shapes(&triples)?;
        Ok(ValidRdfSpec { triples })
    }
}

// Functions receiving ValidRdfSpec are proven safe
fn generate_from_spec(spec: ValidRdfSpec) -> Result<Code> {
    // Specification is proven valid. No validation needed.
}
```

## Single-Pass Construction

With monoidal composition + valid types:

```rust
// SPECIFICATION CLOSED → design chosen

// SINGLE-PASS IMPLEMENTATION
let spec = LoadedSpec::from_file("spec.ttl")?;  // Boundary validation
let design = compile_spec(&spec)?;               // Design to code
let generated = generate_code(&design)?;         // Code generation
let tests = generate_tests(&spec)?;              // Test generation
let validated = validate_output(&generated)?;   // Final validation

// DONE. No iteration needed.
```

Contrast with iteration:

```rust
// Vague spec → Try approach 1 → Doesn't work → Try approach 2 → Test fails → Refactor
```

## Key Principles

1. **Invariants in Types**: Use Rust type system to prove invariants
2. **Validation at Boundary**: Only validate user input
3. **Monoidal Composition**: Components combine without modification
4. **Minimal Structure**: Only what's needed to prove invariants
5. **Single-Pass**: Never iterate if spec is closed

## When to Use

- **All production code**: Encode invariants in types
- **Boundary code**: Validate inputs only
- **Interior code**: Assume types are proven valid
- **Generics**: Use const generics for static bounds

## Anti-Patterns to Avoid

```rust
// ❌ BAD: Runtime checks everywhere
fn process(age: i32) {
    if age < 18 { return Err(...); }
    if age > 120 { return Err(...); }
    // ... more checks later
    if age < 18 { return Err(...); }  // Redundant!
}

// ✅ GOOD: Check once at boundary
fn create_user(age_str: &str) -> Result<ValidUser> {
    let age = Age::new(age_str.parse()?)?;  // One check
    Ok(ValidUser { age })
}

fn process(user: ValidUser) {
    // Age is proven valid. No checks. No possibility of error.
}
```

## Payoff

Encode constraints → Monoidal types → Single-pass implementation → Zero iteration
