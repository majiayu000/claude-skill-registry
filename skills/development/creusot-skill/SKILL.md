---
name: creusot
description: Formal verification of Rust code using Creusot and the Pearlite specification language. Use when the user wants to (1) add contracts/specifications to Rust functions, (2) prove correctness of Rust code, (3) write loop invariants, (4) use Creusot's Why3-based verification, (5) work with Pearlite syntax (requires, ensures, invariant, logic, predicate), or (6) debug failing Creusot proofs. Triggers include "verify this Rust", "prove", "Creusot", "add contracts", "formal verification", "loop invariant", "precondition", "postcondition", "Pearlite".
---

# Creusot Verification Skill

Creusot is a deductive verification tool for safe Rust. It translates Rust + Pearlite specifications to Why3/Coma and uses SMT solvers to prove correctness.

## Quick Reference

### Imports

```rust
use creusot_contracts::prelude::*;  // Current (creusot_std in newer versions)
```

### Core Attributes

| Attribute | Purpose |
|-----------|---------|
| `#[requires(P)]` | Precondition - must hold when function called |
| `#[ensures(P)]` | Postcondition - guaranteed when function returns |
| `#[invariant(P)]` | Loop invariant - true at every iteration |
| `#[variant(E)]` | Termination measure - must decrease each iteration |
| `#[logic]` | Pure logical function (not callable from Rust) |
| `#[predicate]` | Logical function returning bool |
| `#[trusted]` | Skip verification (assume contract holds) |

### Key Operators

| Operator | Meaning |
|----------|---------|
| `x@` | View/model operator - converts Rust value to logical type (e.g., `i64` → `Int`) |
| `^x` | Final value of mutable borrow (prophecy) |
| `*x` | Current value of borrow |
| `==>` | Logical implication (in `pearlite!{}`) |
| `forall<x: T>` | Universal quantifier (in `pearlite!{}`) |
| `exists<x: T>` | Existential quantifier (in `pearlite!{}`) |

### Logical Types

- `Int` - Unbounded mathematical integers (no overflow)
- `Seq<T>` - Mathematical sequences
- `Set<T>`, `FSet<T>` - Sets (infinite/finite)
- `Map<K, V>` - Mathematical functions
- `Ghost<T>` - Ghost values (exist only in proofs)
- `Snapshot<T>` - Immutable snapshot of a value

## Workflow

### Project Setup

```bash
cargo creusot new project-name
cd project-name
```

### Verification Commands

```bash
cargo creusot              # Compile to Coma only
cargo creusot prove        # Compile and prove
cargo creusot prove -i     # Open Why3 IDE on failure
cargo creusot prove --ide-always  # Always open IDE
```

## Writing Specifications

### Basic Contract

```rust
#[requires(x@ < i64::MAX@)]           // Precondition
#[ensures(result@ == x@ + 1)]         // Postcondition
pub fn add_one(x: i64) -> i64 {
    x + 1
}
```

### Loop Invariants

Loops MUST have invariants to be verified. The invariant must:
1. Hold on loop entry
2. Be preserved by each iteration
3. Combined with negated condition, imply postcondition

```rust
#[requires(n@ * (n@ + 1) / 2 <= u64::MAX@)]
#[ensures(result@ == n@ * (n@ + 1) / 2)]
pub fn sum_up_to(n: u64) -> u64 {
    let mut sum = 0;
    let mut i = 0;
    #[invariant(i@ <= n@)]
    #[invariant(sum@ == i@ * (i@ + 1) / 2)]
    while i < n {
        i += 1;
        sum += i;
    }
    sum
}
```

### For Loop Pattern

For loops use `produced` variable (sequence of yielded elements):

```rust
#[invariant(sum@ * 2 == produced.len() * (produced.len() + 1))]
for i in 1..=n {
    sum += i;
}
```

### Logic Functions and Predicates

```rust
#[predicate]
fn sorted<T: Ord>(s: Seq<T>) -> bool {
    pearlite! {
        forall<i: Int, j: Int> 0 <= i && i < j && j < s.len()
            ==> s[i] <= s[j]
    }
}

#[logic]
fn sum_seq(s: Seq<Int>) -> Int {
    if s.len() == 0 { 0 }
    else { s[0] + sum_seq(s.tail()) }
}
```

### Mutable References with Prophecies

Use `^` (final) to specify the value at end of borrow lifetime:

```rust
#[ensures(^x == *x + 1)]  // Final value equals current + 1
pub fn increment(x: &mut i32) {
    *x += 1;
}
```

### Ghost Code

Ghost code exists only during verification:

```rust
let old_v = ghost!(v);  // Snapshot for invariant
#[invariant(v@.permutation_of(old_v@))]
```

### Type Invariants

```rust
pub struct OPair(pub u64, pub u64);

impl Invariant for OPair {
    #[logic]
    fn invariant(self) -> bool {
        pearlite! { self.0 <= self.1 }
    }
}
```

## Common Patterns

### Overflow Prevention

Always specify bounds to prevent overflow verification failures:

```rust
#[requires(x@ + y@ <= i64::MAX@)]
#[requires(x@ + y@ >= i64::MIN@)]
```

### Vec Operations

```rust
#[requires(i@ < v@.len())]           // Bounds check
#[ensures(result@ == v@[i@])]        // Element access
#[ensures((^v)@.len() == v@.len())]  // Length preserved
```

### Termination Variants

```rust
#[logic]
#[variant(x)]  // x must decrease (implement WellFounded)
#[requires(x >= 0)]
fn factorial(x: Int) -> Int {
    if x == 0 { 1 } else { x * factorial(x - 1) }
}
```

## Debugging Failed Proofs

1. **Run with IDE**: `cargo creusot prove -i verif/[FILE].coma`
2. **Check unproved goals**: Yellow = hypothesis, Green = proved
3. **Common issues**:
   - Missing loop invariant clause
   - Invariant too weak (doesn't imply postcondition)
   - Missing overflow bounds
   - SMT solver timeout (try simplifying formulas)
4. **Avoid division in invariants** - SMT solvers struggle; multiply both sides instead

## File Locations

- Coma output: `verif/[crate]_rlib/[module]/[function].coma`
- Config: `why3find.json`, `Cargo.toml`

## Further Reference

For detailed Pearlite syntax, common specification patterns, and advanced features, see [references/pearlite-syntax.md](references/pearlite-syntax.md).
