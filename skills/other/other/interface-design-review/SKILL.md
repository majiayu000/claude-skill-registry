---
name: interface-design-review
description: Review Rust interfaces for ease of correct use and resistance to misuse, applying "make interfaces easy to use correctly and hard to use incorrectly"
---

# Interface Design Review

Review public APIs, traits, structs, and module boundaries against the guiding
principle: **"Make interfaces easy to use correctly and hard to use incorrectly."**

The correct path should be the path of least resistance. Incorrect usage should
be caught at compile time when possible, at construction time when not, and at
runtime only as a last resort.

## When to Use

- After designing or modifying a public API (`pub fn`, `pub struct`, `pub trait`)
- When adding a new module or crate boundary
- Before stabilizing an interface that other code will depend on
- When reviewing builder patterns, configuration types, or plugin interfaces
- After discovering a bug caused by caller misuse of an existing API
- When an API requires documentation to explain "don't do X" — that's a signal
  the interface should prevent X structurally

## The Hierarchy of Enforcement

Prefer enforcement higher in this list. Each level down is weaker:

| Level | Mechanism | Example | Strength |
|-------|-----------|---------|----------|
| **1. Unrepresentable** | Type system makes the wrong state impossible | Newtype, typestate, `NonZeroU32` | Strongest |
| **2. Unconstructable** | Invalid values can't be built | Private fields + validated `new()` | Strong |
| **3. Compile error** | Misuse fails to compile | Ownership, lifetimes, trait bounds | Strong |
| **4. Visible at call site** | Misuse is obvious when reading code | Enums over bools, named types over primitives | Moderate |
| **5. Runtime rejection** | Validated at runtime with clear error | `TryFrom`, `Result`-returning methods | Weak |
| **6. Documentation** | "Don't do this" in a doc comment | /// # Panics | Weakest |

## Review Checklist

### A. Make Invalid States Unrepresentable

- [ ] **Newtype wrappers for domain IDs** — Are `u32`/`u64`/`usize` values
  that carry distinct meaning (file IDs, rule IDs, buffer indices) wrapped in
  newtypes to prevent silent mixing?
- [ ] **Enums over booleans** — Does any function take `bool` parameters? Replace
  with a two-variant enum that documents intent at the call site.
  ```rust
  // BAD: what does `true` mean here?
  scan(data, true, false)

  // GOOD: intent is self-documenting
  scan(data, Encoding::Utf8, CaseSensitivity::Insensitive)
  ```
- [ ] **Typestate for protocols** — If an object has a lifecycle (connect →
  authenticate → use → close), do the types enforce the ordering at compile time?
- [ ] **`NonZero*` for values that must not be zero** — Capacity, counts, sizes.
- [ ] **Exhaustive enums** — Can the caller forget to handle a variant? Use
  `#[non_exhaustive]` on enums that may grow to force `_ =>` arms.

### B. Validate at the Boundary, Trust Internally

- [ ] **Parse, don't validate** — Does the constructor parse raw input into a
  validated type, or does the code validate and then carry around the raw value?
  ```rust
  // BAD: validated but raw — nothing stops later code from skipping validation
  fn process(rule_yaml: &str) { validate(rule_yaml)?; /* use rule_yaml */ }

  // GOOD: parsing produces a type that is valid by construction
  fn process(rule_yaml: &str) -> Result<Rule> { Rule::parse(rule_yaml) }
  ```
- [ ] **Private fields + public constructors** — Can callers bypass invariants
  by directly constructing a struct? Fields that participate in invariants must
  be private.
- [ ] **`TryFrom` / `TryInto`** — For conversions that can fail, is the
  fallible path the only path?
- [ ] **No `pub` on fields with invariants** — If `start <= end` must hold,
  neither field should be `pub`.

### C. Guide the Caller Toward Correct Usage

- [ ] **Builder pattern for complex construction** — If a constructor takes more
  than 3-4 parameters, does a builder exist? Consider typestate builders for
  required fields.
  ```rust
  // Compile error if you forget `source`:
  ScanConfig::builder()
      .source(path)       // required — returns SourceSet state
      .max_depth(10)      // optional
      .build()            // only available after required fields set
  ```
- [ ] **Accept the widest useful input type** — `&str` not `&String`,
  `impl AsRef<Path>` not `&PathBuf`, `impl Into<X>` for ergonomic construction.
- [ ] **Return the most specific type** — Don't return `Box<dyn Error>` when a
  concrete error enum would let callers handle cases. Don't return `Vec<u8>`
  when a `Digest` newtype carries meaning.
- [ ] **Default values via `Default` trait** — If most callers want the same
  config, implement `Default` so the common case is one line.
- [ ] **Method chaining for configuration** — `self` methods that return `Self`
  guide callers through a fluent API.

### D. Make Misuse Visible

- [ ] **No stringly-typed APIs** — Are identifiers, paths, or modes passed as
  raw `String`/`&str` when an enum or newtype would be type-safe?
- [ ] **Parameter order reflects natural reading** — Does `copy(src, dst)` or
  `range(start, end)` match what a caller would guess?
- [ ] **Consistent naming conventions** — Do similar operations across the
  codebase use the same verb (`get_` vs `fetch_` vs `load_`)?
- [ ] **`#[must_use]` on results** — Can the caller silently ignore a return
  value that indicates failure or carries important data?
  ```rust
  #[must_use = "dropping the guard releases the lock immediately"]
  pub fn acquire(&self) -> LockGuard<'_> { ... }
  ```
- [ ] **Unit types for flags** — Instead of `fn set_flag(&mut self, flag: u32)`,
  use `fn enable_unicode(&mut self)`.

### E. Leverage Ownership and Lifetimes

- [ ] **Ownership transfer for single-use resources** — If a value should only
  be used once (tokens, one-shot channels), does the API consume it by value?
- [ ] **Borrow for observation, own for mutation** — Does the API give `&T` for
  reads and require owned `T` or `&mut T` for writes?
- [ ] **Lifetime-bounded references** — If a reference must not outlive its
  source, does the lifetime annotation enforce this?
- [ ] **No hidden shared mutability** — If interior mutability (`Cell`, `RefCell`,
  `Mutex`) is necessary, is it encapsulated rather than leaked through the API?

### F. Error Design

- [ ] **Actionable error types** — Can the caller match on error variants and
  take different recovery actions, or is it an opaque string?
- [ ] **No panicking APIs** — Public functions should return `Result` rather than
  `unwrap`/`expect`. Reserve panics for genuine invariant violations in internal
  code.
- [ ] **Error context** — Does the error carry enough context (file path, line
  number, input snippet) for the caller to diagnose the problem without reading
  source code?

## Anti-Patterns to Flag

| Anti-Pattern | Why It's Bad | Fix |
|---|---|---|
| `fn foo(verbose: bool, recursive: bool)` | Callers write `foo(true, false)` — meaning is invisible | Use enums: `Verbosity::Quiet`, `Traversal::Flat` |
| `pub struct Range { pub start: u32, pub end: u32 }` | Nothing enforces `start <= end` | Private fields + `Range::new(start, end) -> Result<Range>` |
| `fn process(id: u64, parent_id: u64)` | Easy to swap arguments silently | `fn process(id: RuleId, parent: ParentId)` |
| `fn configure(opts: HashMap<String, String>)` | Unbounded input, typos compile fine | Typed config struct or builder |
| `fn init() -> *mut State` | Caller must remember to free, can use-after-free | Return `Box<State>` or `Arc<State>` |
| Returning `i32` error codes | Caller can ignore, misinterpret, or mix with valid values | Return `Result<T, E>` with typed error |
| `fn send(data: &[u8], compress: bool, encrypt: bool, sign: bool)` | 3 bools = 8 combinations, many invalid | Options struct or builder with valid combinations |
| Silent default on invalid input | Caller doesn't know their input was wrong | Return `Err` or use a type that can't be invalid |

## Project-Specific Patterns

This codebase already uses several "easy to use correctly" patterns. New code
should follow them:

- **Sentinel values as constants**: `NONE_U32 = u32::MAX` — centralizes the
  sentinel so callers don't invent their own.
- **Const generics for granularity**: Compile-time selection via `<const G: usize>`
  prevents runtime branching on a configuration value.
- **Feature-gated test tooling**: `#[cfg(feature = "sim-harness")]` ensures test
  infrastructure can't accidentally leak into production builds.
- **`debug_assert!` for internal invariants**: Zero-cost in release, catches
  contract violations during development.

When reviewing, check that new APIs are consistent with these existing patterns.

## Output Format

```markdown
## Interface Design Review: [module/type/function]

### Enforcement Level Assessment

| Aspect | Current Level | Target Level | Gap |
|--------|--------------|--------------|-----|
| ID parameters | 6 (docs say "pass rule ID") | 1 (newtype `RuleId`) | 5 levels |
| Construction validity | 5 (runtime check in `new()`) | 2 (`new()` → private fields) | 3 levels |
| Flag parameters | 6 (doc: "`true` = verbose") | 4 (enum `Verbosity`) | 2 levels |

### Findings

| Priority | Issue | Location | Enforcement Gap |
|----------|-------|----------|-----------------|
| HIGH | Raw `u64` used for rule ID and parent ID — easy to swap | `fn register(id: u64, parent: u64)` | Unrepresentable → Newtype |
| MEDIUM | `bool` parameter for mode selection | `fn scan(data: &[u8], lenient: bool)` | Visible → Enum |
| LOW | Missing `#[must_use]` on `Result`-returning fn | `fn validate()` | Already level 5, add attribute |

### Recommendations

1. **[Issue]**: [Fix with code showing before/after]
   ```rust
   // Before: callers can silently swap IDs
   pub fn register(id: u64, parent: u64) { ... }

   // After: compiler rejects swapped arguments
   pub fn register(id: RuleId, parent: ParentId) { ... }
   ```

### Positive Patterns Observed

- [Note any good patterns already present — reinforces correct design]
```

## Related Skills

- `/security-reviewer` - Complements this: security reviews focus on memory
  safety; interface reviews focus on API misuse prevention
- `/test-strategy` - Property-based tests are powerful for validating that an
  interface's invariants hold across all inputs
- `/doc-rigor` - If an interface passes this review, its docs should describe
  *why* the design prevents misuse, not just *how* to use it
