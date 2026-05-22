---
name: move-prover
description: Move Prover formal verification expert for Aptos smart contracts. Write specifications (MSL), preconditions (requires), postconditions (ensures), invariants, abort conditions (aborts_if), quantifiers, schemas, and pragmas. Debug verification failures. Triggers on Move Prover, formal verification, spec, invariant, ensures, requires, aborts_if, precondition, postcondition.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
license: MIT
metadata:
  author: raintree
  version: "1.0"
---

# Move Prover Expert

Formal verification for Move smart contracts - mathematically prove your code is correct.

## When to Use

- Writing specifications for Move functions
- Proving correctness properties (invariants, access control)
- Debugging verification failures or timeouts
- Understanding MSL (Move Specification Language)

## Why Move Prover?

**Testing checks specific inputs. Verification proves ALL inputs.**

```move
// Testing: Checks one case
#[test]
fun test_transfer() {
    transfer(alice, bob, 100);
}

// Verification: Proves for ALL possible inputs
spec transfer {
    ensures sender_balance == old(sender_balance) - amount;
    ensures recipient_balance == old(recipient_balance) + amount;
}
```

## Core Constructs

### Preconditions - `requires`

Conditions that must be true BEFORE function runs:

```move
spec withdraw {
    requires exists<Balance>(addr);
    requires global<Balance>(addr).coins >= amount;
}
```

### Postconditions - `ensures`

Conditions that must be true AFTER function runs:

```move
spec transfer {
    ensures global<Balance>(from).coins == old(global<Balance>(from).coins) - amount;
    ensures global<Balance>(to).coins == old(global<Balance>(to).coins) + amount;
}
```

### Abort Conditions - `aborts_if`

When function should abort:

```move
spec withdraw {
    aborts_if !exists<Balance>(addr) with ERROR_NOT_FOUND;
    aborts_if global<Balance>(addr).coins < amount with ERROR_INSUFFICIENT;
}
```

### Modified Resources - `modifies`

Which global resources change:

```move
spec transfer {
    modifies global<Balance>(from);
    modifies global<Balance>(to);
}
```

### The `old()` Operator

Access pre-execution values:

```move
spec increment {
    ensures counter.value == old(counter.value) + 1;
}
```

## Invariants

### Struct Invariants

Properties that always hold for a struct:

```move
struct Balance has key {
    coins: u64,
    locked: u64,
}

spec Balance {
    invariant coins >= locked;
}
```

### Module Invariants

Properties that hold across the module:

```move
spec module {
    invariant [global]
        forall addr: address:
            exists<Balance>(addr) ==> global<Balance>(addr).coins >= 0;
}
```

### Update Invariants

Properties about state transitions:

```move
spec module {
    invariant update [global]
        forall addr: address:
            old(exists<Frozen>(addr)) ==> exists<Frozen>(addr);
    // Once frozen, always frozen
}
```

## Quantifiers

### Universal - `forall`

Property holds for ALL values:

```move
spec transfer {
    // All other balances unchanged
    ensures forall addr: address where addr != from && addr != to:
        global<Balance>(addr).coins == old(global<Balance>(addr).coins);
}
```

### Existential - `exists`

Property holds for AT LEAST ONE value:

```move
spec module {
    invariant exists addr: address: exists<AdminCap>(addr);
    // At least one admin exists
}
```

## Schemas (Reusable Specs)

```move
spec schema BalanceExists {
    addr: address;
    requires exists<Balance>(addr);
}

spec schema SufficientBalance {
    addr: address;
    amount: u64;
    requires global<Balance>(addr).coins >= amount;
}

// Reuse in functions
spec withdraw {
    include BalanceExists;
    include SufficientBalance;
}
```

## Pragmas

```move
spec module {
    pragma verify = true;           // Enable verification
    pragma aborts_if_is_strict;     // Require complete abort specs
    pragma timeout = 120;           // Timeout in seconds
}

spec complex_function {
    pragma verify = false;          // Skip this function
    pragma timeout = 300;           // Custom timeout
}
```

## Common Patterns

### Access Control

```move
spec admin_only_function {
    requires exists<AdminCap>(signer::address_of(admin));
    aborts_if !exists<AdminCap>(signer::address_of(admin));
}

spec module {
    // Only one admin
    invariant [global]
        forall a1: address, a2: address:
            exists<AdminCap>(a1) && exists<AdminCap>(a2) ==> a1 == a2;
}
```

### Supply Conservation

```move
spec module {
    fun total_balance(): u64 {
        sum(all_addresses(), |addr| {
            if (exists<Balance>(addr)) { global<Balance>(addr).coins }
            else { 0 }
        })
    }

    invariant [global] total_balance() == global<TotalSupply>(@admin).value;
}

spec transfer {
    ensures global<TotalSupply>(@admin).value == old(global<TotalSupply>(@admin).value);
}
```

### Overflow Prevention

```move
spec deposit {
    requires global<Balance>(addr).coins + amount <= MAX_U64;
    ensures global<Balance>(addr).coins == old(global<Balance>(addr).coins) + amount;
}
```

## Running the Prover

```bash
# Verify all modules
aptos move prove

# Verify specific module
aptos move prove --filter MyModule

# Verbose output
aptos move prove --verbose
```

### Move.toml Configuration

```toml
[prover]
enabled = true
timeout = 60
solver = "z3"
```

## Debugging Failures

### Reading Errors

```
error: post-condition does not hold
   ┌── example.move:15:9 ───
15 │         ensures balance.coins == old(balance.coins) + amount;
   │         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   = Counterexample:
     amount = MAX_U64
     old(balance.coins) = 1
     Result: overflow
```

**Solution:** Add overflow precondition:
```move
spec deposit {
    requires global<Balance>(addr).coins + amount <= MAX_U64;
}
```

### Common Issues

**Missing precondition:**
```move
// Fails: no existence check
spec withdraw {
    ensures global<Balance>(addr).coins == old(global<Balance>(addr).coins) - amount;
}

// Fixed
spec withdraw {
    requires exists<Balance>(addr);  // Add this
    ensures global<Balance>(addr).coins == old(global<Balance>(addr).coins) - amount;
}
```

**Incomplete abort specs:**
```move
spec module { pragma aborts_if_is_strict; }

// Fails: missing abort condition
spec transfer {
    aborts_if !exists<Balance>(from);
    // Missing: aborts_if !exists<Balance>(to);
    // Missing: aborts_if global<Balance>(from).coins < amount;
}
```

**Timeout:**
```move
spec complex_function {
    pragma timeout = 300;  // Increase timeout
    // Or simplify the specification
}
```

## Complete Example

```move
module 0x1::coin {
    struct Coin has key {
        value: u64
    }

    const ERROR_NOT_FOUND: u64 = 1;
    const ERROR_INSUFFICIENT: u64 = 2;

    public fun transfer(from: &signer, to: address, amount: u64) acquires Coin {
        let from_addr = signer::address_of(from);
        assert!(exists<Coin>(from_addr), ERROR_NOT_FOUND);
        assert!(exists<Coin>(to), ERROR_NOT_FOUND);

        let from_coin = borrow_global_mut<Coin>(from_addr);
        assert!(from_coin.value >= amount, ERROR_INSUFFICIENT);
        from_coin.value = from_coin.value - amount;

        let to_coin = borrow_global_mut<Coin>(to);
        to_coin.value = to_coin.value + amount;
    }

    spec transfer {
        let from_addr = signer::address_of(from);

        // Preconditions
        requires exists<Coin>(from_addr);
        requires exists<Coin>(to);
        requires global<Coin>(from_addr).value >= amount;
        requires global<Coin>(to).value + amount <= MAX_U64;

        // Abort conditions
        aborts_if !exists<Coin>(from_addr) with ERROR_NOT_FOUND;
        aborts_if !exists<Coin>(to) with ERROR_NOT_FOUND;
        aborts_if global<Coin>(from_addr).value < amount with ERROR_INSUFFICIENT;

        // Postconditions
        ensures global<Coin>(from_addr).value == old(global<Coin>(from_addr).value) - amount;
        ensures global<Coin>(to).value == old(global<Coin>(to).value) + amount;

        // Modified resources
        modifies global<Coin>(from_addr);
        modifies global<Coin>(to);
    }

    spec module {
        pragma verify = true;
        pragma aborts_if_is_strict;
    }
}
```

## Specification Checklist

For critical functions, verify:

- [ ] **Preconditions** - What must be true before?
- [ ] **Postconditions** - What must be true after?
- [ ] **Abort conditions** - When should it fail?
- [ ] **Modified resources** - What state changes?
- [ ] **Invariants** - What always holds?
- [ ] **Conservation** - Are resources conserved?
- [ ] **Access control** - Is authorization correct?
- [ ] **Overflow** - Are bounds checked?

## Resources

- **Aptos Move Prover Docs:** https://aptos.dev/move/prover/
- **Move Specification Language:** https://github.com/move-language/move/blob/main/language/move-prover/doc/user/spec-lang.md
