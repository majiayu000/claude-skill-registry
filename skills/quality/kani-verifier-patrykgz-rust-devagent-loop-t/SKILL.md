---
name: kani-verifier
description: Rust formal verification using Kani model checker. Use when verifying Rust code for memory safety, undefined behavior, panics, arithmetic overflows, or custom correctness properties. Triggers include "verify this Rust code", "prove this function is safe", "check for undefined behavior", "write a proof harness", "kani proof", "model check", or any request involving Rust formal verification, property-based proofs, or safety guarantees beyond testing.
---

# Kani Rust Verifier

Kani is a bit-precise model checker for Rust that proves properties about code rather than just testing examples. Unlike tests that check specific inputs, Kani exhaustively verifies all possible inputs.

## Installation

```bash
# Install Kani (requires Rust 1.58+, Linux/Mac)
cargo install --locked kani-verifier
cargo kani setup
```

## Core Concepts

### Proof Harnesses vs Tests

Tests verify specific examples; Kani harnesses verify *all* possible inputs:

```rust
// Test: checks ONE specific case
#[test]
fn test_abs() {
    assert_eq!(abs(-5), 5);
}

// Kani: checks ALL i32 values
#[cfg(kani)]
#[kani::proof]
fn verify_abs() {
    let x: i32 = kani::any();  // Symbolic: represents ALL i32 values
    let result = abs(x);
    assert!(result >= 0);
}
```

### What Kani Automatically Checks

Without any assertions, Kani automatically verifies:
- Memory safety (null dereferences, out-of-bounds)
- Arithmetic overflows
- Division by zero
- Shift overflows
- Absence of panics (`unwrap()` on `None`, etc.)

## Quick Start Pattern

```rust
#[cfg(kani)]
mod verification {
    use super::*;

    #[kani::proof]
    fn verify_function() {
        // 1. Create symbolic inputs
        let input: u32 = kani::any();

        // 2. Constrain inputs if needed
        kani::assume(input < 1000);

        // 3. Call function under test
        let result = function_under_test(input);

        // 4. Assert properties
        assert!(result > 0);
    }
}
```

Run with: `cargo kani`

## Essential API

### Symbolic Values

```rust
// Create symbolic values for any type implementing kani::Arbitrary
let x: u32 = kani::any();
let opt: Option<i32> = kani::any();
let arr: [u8; 4] = kani::any();

// With constraint
let bounded = kani::any_where(|x: &u32| *x < 100);
```

### Assumptions and Assertions

```rust
// Constrain symbolic values (preconditions)
kani::assume(x != 0);           // x cannot be zero
kani::assume(x > 0 && x < 100); // bounded range

// Custom assertions with messages
kani::assert(result > 0, "Result must be positive");

// Standard assert! also works
assert!(value.is_some());
```

### Coverage Checking

```rust
// Verify a condition is reachable (catches over-constrained harnesses)
kani::cover!(x > 100, "Large values are possible");
```

### Implementing Arbitrary for Custom Types

```rust
// Option 1: Derive macro
#[cfg_attr(kani, derive(kani::Arbitrary))]
struct Point { x: i32, y: i32 }

// Option 2: Manual implementation
#[cfg(kani)]
impl kani::Arbitrary for Rating {
    fn any() -> Self {
        match kani::any::<u8>() % 3 {
            0 => Rating::Low,
            1 => Rating::Medium,
            _ => Rating::High,
        }
    }
}
```

## Function Contracts (Experimental)

Contracts enable modular verification with `requires` (preconditions) and `ensures` (postconditions):

```rust
#[cfg_attr(kani, kani::requires(divisor != 0))]
#[cfg_attr(kani, kani::ensures(|result: &u32| *result <= dividend))]
fn safe_div(dividend: u32, divisor: u32) -> u32 {
    dividend / divisor
}

#[cfg(kani)]
mod verification {
    use super::*;

    #[kani::proof_for_contract(safe_div)]
    fn check_safe_div() {
        let a: u32 = kani::any();
        let b: u32 = kani::any();
        safe_div(a, b);  // Kani verifies contract holds
    }
}
```

Enable with: `cargo kani -Z function-contracts`

## Handling Loops

Kani must unwind loops to a finite bound:

```rust
#[kani::proof]
#[kani::unwind(11)]  // Unwind up to 11 iterations
fn verify_loop() {
    let mut sum = 0u32;
    for i in 0..10 {
        sum = sum.saturating_add(i);
    }
    assert!(sum == 45);
}
```

Global default: `cargo kani --default-unwind 10`

## Stubbing Functions

Replace complex functions with simpler models:

```rust
fn my_random() -> u32 {
    kani::any()  // Return symbolic value instead of actual random
}

#[kani::proof]
#[kani::stub(rand::random, my_random)]
fn verify_with_random() {
    let x = rand::random::<u32>();
    // Verification continues with symbolic x
}
```

## Common Patterns

### Verifying Data Structure Invariants

```rust
#[kani::proof]
fn verify_vec_push() {
    let mut v: Vec<u32> = kani::any();
    kani::assume(v.len() < 10);

    let old_len = v.len();
    v.push(kani::any());

    assert!(v.len() == old_len + 1);
}
```

### Verifying Unsafe Code

```rust
#[kani::proof]
fn verify_raw_pointer() {
    let x: u32 = kani::any();
    let ptr = &x as *const u32;

    // Kani checks this dereference is safe
    let value = unsafe { *ptr };
    assert!(value == x);
}
```

### Bounded Verification

```rust
#[kani::proof]
#[kani::unwind(5)]
fn verify_bounded_slice() {
    let data: [u8; 4] = kani::any();
    let idx: usize = kani::any();
    kani::assume(idx < data.len());

    let _ = data[idx];  // Kani proves no out-of-bounds
}
```

## Cargo.toml Configuration

```toml
[package.metadata.kani.flags]
default-unwind = "10"

[lints.rust]
unexpected_cfgs = { level = "warn", check-cfg = ['cfg(kani)'] }
```

## Command Reference

```bash
cargo kani                        # Verify all harnesses
cargo kani --harness verify_foo   # Single harness
cargo kani --tests                # Include test mode dependencies
cargo kani --default-unwind 20    # Set loop bound
cargo kani -Z function-contracts  # Enable contracts
cargo kani --concrete-playback=print  # Generate failing test case
```

## Interpreting Results

```
VERIFICATION:- SUCCESSFUL    # Property holds for ALL inputs
VERIFICATION:- FAILED        # Counterexample found
Status: UNREACHABLE          # Code path impossible (may indicate over-constrained assume)
```

## Limitations

- No concurrency support
- No inline assembly
- Some floating-point operations are over-approximated
- Stack unwinding not supported (use `panic = "abort"`)

## References

- Full documentation: https://model-checking.github.io/kani/
- GitHub: https://github.com/model-checking/kani
- API reference: See references/API.md in this skill
