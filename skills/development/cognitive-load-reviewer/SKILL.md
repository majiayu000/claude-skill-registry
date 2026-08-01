---
name: cognitive-load-reviewer
description: Analyze and reduce cognitive load in code by identifying complex conditionals,
  deep nesting, shallow modules, excessive abstractions, and architectural over-engineering.
  Use when reviewing code qualit
---

---
name: cognitive-load-reviewer
description: Analyze and reduce cognitive load in code by identifying complex conditionals, deep nesting, shallow modules, excessive abstractions, and architectural over-engineering. Use when reviewing code quality, refactoring for maintainability, or simplifying systems. Keywords: cognitive load, complexity, refactor, simplify, maintainability, readability, mental overhead, abstraction, architecture review
---

# Cognitive Load Reviewer

Identifies and reduces extraneous cognitive load in software systems following evidence-based principles.

## Core Principle

**Working Memory Limit**: Humans can hold ~4 chunks of information simultaneously. Code exceeding this threshold creates mental fatigue and slows development.

**Goal**: Reduce *extraneous* cognitive load (caused by poor design) while accepting *intrinsic* load (inherent domain complexity).

## Analysis Framework

### 1. Complex Conditionals

**Look for:**
- Nested boolean expressions: `if val > X && (a || b) && (c && !d)`
- Multiple conditions without intermediate variables
- Logic requiring mental simulation to understand

**Fix:**
```rust
// ❌ High cognitive load
if val > constant && (cond2 || cond3) && (cond4 && !cond5) {
    // ...
}

// ✅ Externalized mental bookkeeping
let exceeds_threshold = val > constant;
let has_valid_mode = cond2 || cond3;
let is_enabled = cond4 && !cond5;

if exceeds_threshold && has_valid_mode && is_enabled {
    // ...
}
```

### 2. Deep Nesting

**Look for:**
- Multiple levels of indentation (>3 levels)
- Nested if/match statements
- Accumulated context requirements

**Fix:**
```rust
// ❌ Nested context tracking
fn process(data: Option<Data>) -> Result<Output> {
    if let Some(data) = data {
        if data.is_valid() {
            if let Some(result) = data.compute() {
                return Ok(result);
            }
        }
    }
    Err(Error::Invalid)
}

// ✅ Early returns focus on happy path
fn process(data: Option<Data>) -> Result<Output> {
    let data = data.ok_or(Error::Missing)?;
    if !data.is_valid() {
        return Err(Error::Invalid);
    }
    data.compute().ok_or(Error::ComputeFailed)
}
```

### 3. Shallow vs. Deep Modules

**Identify shallow modules:**
- Complex interface with minimal functionality
- Many small functions/methods requiring multiple mental models
- High coupling between components

**Prefer deep modules:**
- Simple interface hiding complex implementation
- Unix I/O principle: 5 basic calls, 100K+ lines internal complexity
- Single entry point with clear contract

**Example:**
```rust
// ❌ Shallow - many small pieces
struct UserValidator;
struct PasswordHasher;
struct SessionCreator;
struct TokenGenerator;
// ... requires understanding 4+ components

// ✅ Deep - simple interface, complex internals
struct AuthService {
    pub fn authenticate(&self, credentials: Credentials) -> Result<Session>
    // Hides validation, hashing, session creation internally
}
```

### 4. Abstraction Layers

**Red flags:**
- Hexagonal/Onion architecture with 5+ layers
- Repository patterns abstracting simple queries
- Domain/Application/Infrastructure separation without clear benefit
- "MetricsProviderFactoryFactory" naming patterns

**Reality check:**
- Can newcomers contribute within hours or days?
- Does debugging require tracing through multiple layers?
- Are abstraction layers solving real extension points or architectural purity?

**Principle:** Add abstraction only for justified extension points, not preemptive flexibility.

### 5. DRY Abuse

**Look for:**
- Shared code between unrelated domains
- Premature abstractions creating tight coupling
- "Generic" utilities requiring mental mapping

**Guideline:**
```rust
// ✅ "A little copying is better than a little dependency"
// Duplicate 5-10 lines if it maintains clarity and independence
// Abstract only when 3+ use cases demonstrate clear pattern
```

### 6. Microservices Over-Granularity

**Warning signs:**
- Changes require modifying 4+ services
- Distributed monolith patterns
- More services than team members

**Case study:** 5 developers, 17 microservices → 10 months behind schedule

**Principle:** Defer network boundaries until logical system boundaries are clear.

### 7. Framework Magic

**Look for:**
- Business logic embedded in framework code
- Annotations/macros hiding control flow
- "Magic" requiring framework internals knowledge before contributing

**Fix:**
```rust
// ❌ Framework-coupled business logic
#[framework::magic_handler]
async fn process_order(ctx: FrameworkContext) -> FrameworkResponse {
    // Business logic intertwined with framework
}

// ✅ Framework as library, business logic separate
async fn process_order(order: Order) -> Result<Receipt> {
    // Pure business logic, framework-agnostic
}

// Adapter layer handles framework integration
```

### 8. Self-Describing Values

**Look for:**
- Numeric error codes requiring mental mappings
- Boolean flags without semantic names
- Magic numbers without constants

**Fix:**
```rust
// ❌ Requires memorization
return Err(401);

// ✅ Self-describing
return Err(AuthError::JwtExpired);

// ❌ Magic number
if status == 418 { ... }

// ✅ Named constant
const TEAPOT_STATUS: u16 = 418;
if status == TEAPOT_STATUS { ... }
```

### 9. Inheritance Hierarchies

**Look for:**
- Multiple inheritance levels (>2)
- Vertical cognitive chains requiring class-hopping
- Overridden behavior modifications

**Prefer:**
- Composition over inheritance
- Trait/interface implementations without deep hierarchies
- Flat structures with explicit dependencies

## Analysis Process

### Step 1: Identify Cognitive Hotspots

Scan code for:
- Functions >50 lines
- Nesting depth >3 levels
- Complex boolean logic
- Multiple abstraction layers
- Module coupling patterns

### Step 2: Measure Mental Overhead

Ask:
- How many facts must I hold in memory?
- Can I understand this without context-switching?
- Would a newcomer understand this in <5 minutes?
- Does this require memorizing mappings/conventions?

### Step 3: Categorize Load Type

- **Intrinsic**: Domain complexity (accept it)
- **Extraneous**: Design choices (fix it)

### Step 4: Recommend Improvements

Prioritize:
1. **High impact, low effort**: Extract intermediate variables, early returns
2. **Medium impact**: Simplify module boundaries, reduce abstractions
3. **Strategic**: Architecture simplification, framework decoupling

## Output Format

Present findings as:

### 🧠 Cognitive Load Analysis

**High Load Areas** (>4 mental chunks required)
- `crates/parser/src/query.rs:145` - Complex conditional with 6 boolean clauses
- `crates/storage/src/engine.rs:89` - 5 levels of nesting, difficult to track state

**Shallow Module Patterns** (complex interface, minimal functionality)
- `StorageAdapter` + `QueryExecutor` + `ResultMapper` could merge into single `QueryEngine`

**Excessive Abstraction**
- Repository pattern adds indirection without extension points
- Consider direct SQL calls via jOOQ-style query builder

**Improvement Priorities**

1. **Extract intermediate variables** in `query.rs:145`
   ```rust
   let has_valid_columns = !columns.is_empty() && columns.iter().all(|c| c.is_valid());
   let within_bounds = offset >= 0 && limit <= MAX_LIMIT;
   if has_valid_columns && within_bounds { ... }
   ```

2. **Flatten nesting** in `engine.rs:89` using early returns

3. **Merge shallow modules** to create deeper interface with simpler mental model

## Onboarding Metric

**Critical test:** Can a new developer contribute within 1-2 days?

If newcomers struggle >40 consecutive minutes, cognitive load needs reduction.

## Project Integration

Reference `CLAUDE.md` principles:
- Incremental development reduces cognitive overhead
- TDD externalizes requirements into tests
- Small commits maintain reviewability
- Parallel sub-agents distribute analysis cognitive load

## Success Examples

- Instagram: 14M users with 3 engineers (simple architecture)
- Unix I/O: Deep module pattern (5 calls, 100K+ lines hidden)
- Raft consensus: Designed explicitly for understandability

## Anti-Pattern Summary

❌ Overly granular module decomposition
❌ Excessive architectural layers without benefit
❌ Numeric codes requiring memorization
❌ Framework-embedded business logic
❌ Premature DRY abstractions
❌ Deep inheritance chains
❌ Nested conditionals without intermediate variables
❌ Shallow modules forcing multi-component mental models

## Remember

**"The best components provide powerful functionality yet have a simple interface."**

Optimize for reducing the mental effort required to understand and modify code.