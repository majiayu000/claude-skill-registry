---
name: proptest
description: Property-based testing for Rust using proptest. Use when writing tests that verify properties hold for arbitrary inputs, implementing custom strategies for generating test data, testing edge cases automatically, or when the user mentions "proptest", "property-based testing", "fuzz testing in Rust", "shrinking", or needs to generate arbitrary test data. Triggers include requests to test functions with random inputs, find edge cases, implement Arbitrary for custom types, or create data generators.
---

# Proptest - Property-Based Testing for Rust

Proptest tests properties that hold for arbitrary inputs, automatically finding minimal failing cases through shrinking.

## Setup

```toml
# Cargo.toml
[dev-dependencies]
proptest = "1.0"
proptest-derive = "0.5"  # Optional: for #[derive(Arbitrary)]
```

## Core Patterns

### Basic Property Test

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn my_property(input in 0..100i32) {
        // Property assertions go here
        prop_assert!(input >= 0);
        prop_assert!(input < 100);
    }
}
```

### Multiple Inputs

```rust
proptest! {
    #[test]
    fn test_addition_commutative(a in any::<i32>(), b in any::<i32>()) {
        prop_assert_eq!(a.wrapping_add(b), b.wrapping_add(a));
    }
}
```

## Strategies

Strategies define how to generate test values. Core strategy types:

| Strategy | Generates | Example |
|----------|-----------|---------|
| `any::<T>()` | Any value of type T | `any::<u32>()` |
| `a..b` | Range values | `0..100i32` |
| `"regex"` | Strings matching regex | `"[a-z]{1,10}"` |
| `Just(v)` | Always returns v | `Just(42)` |
| `prop_oneof![...]` | One of multiple strategies | `prop_oneof![Just(1), Just(2)]` |

### String Strategies

```rust
// Regex-based strings
"[a-zA-Z0-9]{1,20}"           // Alphanumeric, 1-20 chars
"\\PC*"                        // Any non-control chars
"[0-9]{4}-[0-9]{2}-[0-9]{2}"  // Date format YYYY-MM-DD

// Any string
any::<String>()
```

### Collection Strategies

```rust
use proptest::collection;

// Vectors
collection::vec(any::<i32>(), 0..100)     // Vec<i32> with 0-99 elements
collection::vec("[a-z]+", 1..10)          // Vec<String> of words

// Other collections
collection::hash_map(any::<String>(), any::<i32>(), 0..10)
collection::btree_set(0..1000i32, 5..20)
```

## Strategy Combinators

### prop_map - Transform Values

```rust
fn point_strategy() -> impl Strategy<Value = Point> {
    (any::<f32>(), any::<f32>())
        .prop_map(|(x, y)| Point { x, y })
}
```

### prop_filter - Reject Values (Use Sparingly)

```rust
fn even_numbers() -> impl Strategy<Value = i32> {
    any::<i32>().prop_filter("must be even", |x| x % 2 == 0)
}

// BETTER: Generate directly instead of filtering
fn even_numbers_better() -> impl Strategy<Value = i32> {
    any::<i32>().prop_map(|x| x * 2)
}
```

### prop_flat_map - Dependent Strategies

Use when one generated value determines how to generate another:

```rust
// Generate a vec and a valid index into it
fn vec_and_index() -> impl Strategy<Value = (Vec<i32>, usize)> {
    collection::vec(any::<i32>(), 1..100)
        .prop_flat_map(|vec| {
            let len = vec.len();
            (Just(vec), 0..len)
        })
}
```

## prop_compose! Macro

Cleaner syntax for composing strategies:

```rust
prop_compose! {
    fn arb_order(max_qty: u32)
        (id in any::<u32>(), item in "[a-z]+", qty in 1..max_qty)
        -> Order
    {
        Order { id: id.to_string(), item, quantity: qty }
    }
}

// Three-arg form for dependent generation
prop_compose! {
    fn vec_and_index()
        (vec in collection::vec(any::<i32>(), 1..100))
        (index in 0..vec.len(), vec in Just(vec))
        -> (Vec<i32>, usize)
    {
        (vec, index)
    }
}
```

## Deriving Arbitrary

```rust
use proptest_derive::Arbitrary;

#[derive(Debug, Arbitrary)]
struct User {
    #[proptest(regex = "[a-z]{3,10}")]
    name: String,
    #[proptest(strategy = "18..120u8")]
    age: u8,
}

#[derive(Debug, Arbitrary)]
enum Status {
    Active,
    #[proptest(weight = 3)]  // 3x more likely
    Pending,
    #[proptest(skip)]        // Never generated
    Deleted,
}
```

## Recursive Data Structures

```rust
fn arb_tree() -> impl Strategy<Value = Tree> {
    let leaf = any::<i32>().prop_map(Tree::Leaf);

    leaf.prop_recursive(
        8,    // max depth
        256,  // max nodes
        10,   // expected branch size
        |inner| {
            collection::vec(inner, 0..10)
                .prop_map(Tree::Branch)
        }
    )
}
```

## Assertions

| Macro | Purpose |
|-------|---------|
| `prop_assert!(cond)` | Assert condition |
| `prop_assert_eq!(a, b)` | Assert equality |
| `prop_assert_ne!(a, b)` | Assert inequality |
| `prop_assume!(cond)` | Skip test case if false (global filter) |

Use `prop_assert*` instead of regular `assert*` - they produce cleaner output during shrinking.

## Configuration

```rust
proptest! {
    #![proptest_config(ProptestConfig {
        cases: 1000,           // Number of test cases (default: 256)
        max_shrink_iters: 100, // Max shrink attempts (default: unlimited)
        .. ProptestConfig::default()
    })]

    #[test]
    fn configured_test(x in any::<i32>()) {
        prop_assert!(true);
    }
}
```

## Failure Persistence

Failed test cases are saved to `proptest-regressions/` directory. Add to version control:

```bash
git add proptest-regressions/
```

## Best Practices

1. **Prefer generation over filtering** - Filtering slows tests and harms shrinking
2. **Use `prop_assert*` macros** - Better error output than `assert*`
3. **Keep strategies deterministic** - Same seed should produce same values
4. **Add regression files to VCS** - Ensures bugs stay fixed
5. **Start simple, add complexity** - Begin with `any::<T>()`, constrain as needed
6. **Test properties, not implementations** - Focus on invariants: `reverse(reverse(x)) == x`

## Common Patterns

### Roundtrip Testing

```rust
proptest! {
    #[test]
    fn serialization_roundtrip(original in any::<MyStruct>()) {
        let serialized = serde_json::to_string(&original)?;
        let deserialized: MyStruct = serde_json::from_str(&serialized)?;
        prop_assert_eq!(original, deserialized);
    }
}
```

### Testing Invariants

```rust
proptest! {
    #[test]
    fn sorted_output_is_sorted(mut vec in collection::vec(any::<i32>(), 0..100)) {
        vec.sort();
        for window in vec.windows(2) {
            prop_assert!(window[0] <= window[1]);
        }
    }
}
```

### Oracle Testing (Compare Implementations)

```rust
proptest! {
    #[test]
    fn fast_matches_slow(input in any::<Input>()) {
        prop_assert_eq!(fast_implementation(&input), slow_reference(&input));
    }
}
```

For advanced patterns (state machine testing, no_std support, async), see references/advanced.md.
