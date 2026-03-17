---
name: compact-core:privacy-disclosure
description: Use when encountering "potential witness-value disclosure" compiler errors, implementing commit-reveal patterns, working with persistentCommit/transientCommit vs persistentHash/transientHash, or designing privacy-preserving circuits with proper witness protection.
---

# Privacy & Disclosure

Essential guidance for Midnight's privacy model: when disclosure is required, commitment patterns, and witness protection.

## The Disclosure Rule

**Witness values cannot flow to public outputs without explicit `disclose()`.**

The compiler tracks all witness-derived values through your code. If a value touches any of these "disclosure triggers", you must wrap it with `disclose()`:

| Trigger | Why Disclosure Required |
|---------|------------------------|
| Ledger storage | Data on-chain is public |
| Circuit return | Return values go to TypeScript |
| External contract | Data leaves your contract boundary |
| Comparison operations | Comparisons can leak information |

## Quick Decision Tree

```
Is the value derived from a witness?
├── No → No disclosure needed
└── Yes → Does it flow to:
    ├── Ledger write → disclose() required
    ├── Circuit return → disclose() required
    ├── Comparison (==, <, >) → disclose() required
    └── Commitment (transientCommit/persistentCommit) → Safe, no disclosure
```

## Safe vs Unsafe Operations

| Operation | Safe? | Why |
|-----------|-------|-----|
| `persistentCommit(x)` | ✅ Safe | Hides value with nonce |
| `transientCommit(x)` | ✅ Safe | Hides value with nonce |
| `persistentHash(x)` | ❌ Unsafe | No nonce, can be brute-forced |
| `transientHash(x)` | ❌ Unsafe | No nonce, can be brute-forced |

## Common Patterns

### Commit-Reveal

```compact
witness get_secret(): Field;

// Phase 1: Commit
export circuit commit(): Bytes<32> {
    const secret = get_secret();
    return persistentCommit(secret);  // Safe: commitment hides secret
}

// Phase 2: Reveal (requires disclosure)
export circuit reveal(): Field {
    const secret = get_secret();
    return disclose(secret);  // Explicit: user knows this reveals
}
```

### Nullifier Pattern

```compact
witness get_secret(): Field;

export circuit spend(commitment: Bytes<32>): Bytes<32> {
    const secret = get_secret();

    // Verify knowledge of secret
    assert persistentCommit(secret) == commitment, "Invalid commitment";

    // Generate nullifier (unique per secret, reveals nothing)
    const nullifier = persistentHash("nullifier", secret);
    return nullifier;
}
```

## References

- [Disclosure Rules](./references/disclosure-rules.md) - Complete decision tree
- [Witness Protection](./references/witness-protection.md) - How the compiler tracks values
- [Safe Operations](./references/safe-operations.md) - Safe vs unsafe stdlib functions
