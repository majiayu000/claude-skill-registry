---
name: compact-core:standard-library
description: Use when importing from CompactStandardLibrary, working with crypto functions (persistentHash, persistentCommit, ecAdd, ecMul), utility types (Maybe, Either), token operations (mintToken, send, receive, mergeCoin), or time functions (blockTime, blockTimeBefore, blockTimeAfter).
---

# Compact Standard Library

Complete reference for `CompactStandardLibrary` - the built-in module providing cryptographic functions, utility types, token operations, and time functions.

## Import

```compact
import { persistentHash, Maybe, mintToken, blockTime } from "CompactStandardLibrary";
```

## Quick Reference

### Cryptographic Functions

| Function | Safe? | Purpose |
|----------|-------|---------|
| `persistentCommit(value)` | Yes | Create hiding commitment with nonce (cross-transaction stable) |
| `transientCommit(value)` | Yes | Create hiding commitment with nonce (transaction-local) |
| `persistentHash(domain, value)` | No | Domain-separated hash (cross-transaction stable) |
| `transientHash(domain, value)` | No | Domain-separated hash (transaction-local) |
| `ecAdd(p1, p2)` | - | Elliptic curve point addition |
| `ecMul(scalar, point)` | - | Elliptic curve scalar multiplication |

**Safe vs Unsafe**: Commit functions include a random nonce, making them hiding. Hash functions do not include a nonce - if the input has low entropy, the hash can be brute-forced.

### Utility Types

| Type | Purpose | Variants |
|------|---------|----------|
| `Maybe<T>` | Optional value | `Some(T)`, `None` |
| `Either<L, R>` | Result/choice | `Left(L)`, `Right(R)` |

### Token Operations

| Function | Purpose |
|----------|---------|
| `mintToken(info)` | Create new tokens |
| `send(coin, recipient)` | Send tokens to address |
| `receive()` | Receive tokens in circuit |
| `mergeCoin(coins)` | Combine multiple coins |

### Time Functions

| Function | Purpose |
|----------|---------|
| `blockTime()` | Current block timestamp |
| `blockTimeBefore(time)` | Assert current time < time |
| `blockTimeAfter(time)` | Assert current time > time |

## Common Patterns

### Safe Commitment

```compact
import { persistentCommit } from "CompactStandardLibrary";

witness get_secret(): Field;

export circuit commit_secret(): Bytes<32> {
    const secret = get_secret();
    // Safe: commitment hides the secret
    return persistentCommit(secret);
}
```

### Nullifier Generation

```compact
import { persistentHash } from "CompactStandardLibrary";

witness get_secret(): Field;

export circuit generate_nullifier(): Bytes<32> {
    const secret = get_secret();
    // Unsafe but intentional: nullifier should be deterministic
    return persistentHash("nullifier", secret);
}
```

### Optional Value Handling

```compact
import { Maybe } from "CompactStandardLibrary";

ledger values: Map<Bytes<32>, Field>;

export circuit get_or_default(key: Bytes<32>): Field {
    const result = values.lookup(key);
    return if result is Maybe::Some(v) { v } else { 0 };
}
```

### Time-Locked Action

```compact
import { blockTime, blockTimeAfter } from "CompactStandardLibrary";

ledger unlock_time: Cell<Uint<64>>;

export circuit withdraw(): [] {
    // Fails if current block time <= unlock_time
    blockTimeAfter(unlock_time.read());
    // Perform withdrawal...
}
```

## References

- [Crypto Functions](./references/crypto-functions.md) - Hash, commit, EC operations
- [Utility Types](./references/utility-types.md) - Maybe, Either patterns
- [Token Operations](./references/token-operations.md) - mintToken, send, receive, mergeCoin
- [Time Functions](./references/time-functions.md) - blockTime and time constraints

## Examples

- [Crypto Patterns](./examples/crypto-patterns.compact) - Cryptographic function usage
- [Token Contract](./examples/token-contract.compact) - Token operations example
- [Time-Locked](./examples/time-locked.compact) - Time-based logic example
