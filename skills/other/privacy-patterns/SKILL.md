---
name: midnight-core-concepts:privacy-patterns
description: Use when implementing privacy-preserving logic in Compact, working with hashes, commitments, Merkle trees, nullifier patterns, or keeping data private on-chain.
---

# Privacy Patterns in Midnight

Fundamental rule: **Anything passed to a ledger operation is publicly visible**, except `MerkleTree` types. Use these patterns to keep data private.

## Pattern Selection Guide

| Goal | Pattern | Use When |
|------|---------|----------|
| Hide data, prove later | Hash | Simple verification needed |
| Hide data, prevent correlation | Commitment | Same values must look different |
| Prove membership secretly | Merkle Tree | Set membership without revealing which |
| Single-use tokens | Commitment + Nullifier | Prevent double-spend privately |

## Pattern 1: Hashes

Use `persistentHash` to hide data while allowing later verification.

```compact
import { persistentHash } from "std/compact/hashes";

// Store hash of secret
ledger.stored_hash = persistentHash(secret_data);

// Later, prove knowledge by re-hashing
assert persistentHash(provided_data) == ledger.stored_hash;
```

### Limitations
- Same input → same hash (correlatable)
- Small value sets vulnerable to brute-force

**Use for**: Data that won't repeat and has high entropy.

## Pattern 2: Commitments

Use `persistentCommit` when same values must appear different.

```compact
import { persistentCommit } from "std/compact/commitments";

// Commitment with randomness prevents correlation
const commitment = persistentCommit(value, randomness);
ledger.stored_commitment = commitment;
```

### Why Randomness Matters

Without randomness, commitments to "yes" always look identical. With randomness:
- commit("yes", random1) ≠ commit("yes", random2)
- Prevents correlation between identical values
- Critical for voting, bidding, any repeated values

```compact
// WRONG: Correlatable
const bad = persistentCommit(vote, Bytes<32>::zero());

// CORRECT: Unlinkable
const good = persistentCommit(vote, fresh_randomness);
```

### Randomness Sources

```compact
// Option 1: Fresh randomness (ideal)
const r = generateRandomness();

// Option 2: Derived from secret key + counter (deterministic)
const r = persistentHash(secret_key, counter);
```

**Use for**: Any value that might repeat (votes, bids, choices).

## Pattern 3: Merkle Trees

Use `MerkleTree` to prove set membership without revealing which element.

```compact
ledger authorized_keys: MerkleTree<32, Bytes<32>>;

export circuit authenticate(
  secret_key: Bytes<32>,
  merkle_path: MerkleTreePath<32, Bytes<32>>
): Void {
  // Prove key is in tree without revealing which key
  const public_key = persistentHash(secret_key);
  assert ledger.authorized_keys.member(public_key, merkle_path);
}
```

### Tree Types

| Type | Use Case |
|------|----------|
| `MerkleTree<n, T>` | Static set, proofs against current root |
| `HistoricMerkleTree<n, T>` | Frequent insertions, proofs against past roots |

**Use `HistoricMerkleTree` when**: Elements added frequently and users need to prove membership against roots from when they obtained their path.

## Pattern 4: Commitment + Nullifier

The most powerful pattern: single-use tokens with complete privacy.

### How It Works

1. **Commitment phase**: Store `commit(value, secret)` in Merkle tree
2. **Spend phase**: Reveal `nullifier = hash(commitment, secret)`
3. **Validation**: Prove commitment exists, nullifier not seen before

```compact
ledger commitments: MerkleTree<32, Bytes<32>>;
ledger nullifiers: Set<Bytes<32>>;

export circuit spend(
  value: Field,
  secret: Bytes<32>,
  path: MerkleTreePath<32, Bytes<32>>
): Void {
  // Reconstruct commitment
  const commitment = persistentCommit(value, secret);

  // Prove commitment exists in tree
  assert ledger.commitments.member(commitment, path);

  // Compute and record nullifier
  const nullifier = persistentHash(commitment, secret);
  assert !ledger.nullifiers.member(nullifier);
  ledger.nullifiers.insert(nullifier);
}
```

### Privacy Properties

- **Commitment**: Hides value and owner
- **Nullifier**: Prevents double-spend without linking to commitment
- **Merkle proof**: Proves existence without revealing which commitment

This is the foundation of Zerocash and Zswap's shielded UTXOs.

## Authentication Pattern

Prove identity without revealing credentials:

```compact
export circuit authenticate(secret_key: Bytes<32>): Void {
  const public_key = persistentHash(secret_key);
  assert public_key == ledger.authorized_key;
  // Authorized! secret_key never revealed
}
```

## Common Mistakes

### Mistake 1: Reusing Randomness
```compact
// WRONG: Same randomness = correlatable
const r = fixed_value;
commit(vote1, r); commit(vote2, r);

// CORRECT: Fresh randomness each time
commit(vote1, random1); commit(vote2, random2);
```

### Mistake 2: Small Value Sets Without Randomness
```compact
// WRONG: Only 2 possible values, easily brute-forced
hash(vote); // vote is "yes" or "no"

// CORRECT: Commitment with randomness
persistentCommit(vote, randomness);
```

### Mistake 3: Forgetting What's Public
```compact
// WRONG: This exposes the secret!
ledger.public_field = secret_value;

// CORRECT: Store only commitment
ledger.public_field = persistentCommit(secret_value, randomness);
```

## References

For detailed technical information:
- **`references/commitment-schemes.md`** - Pedersen commitments, binding/hiding properties
- **`references/merkle-tree-usage.md`** - Tree operations, path generation, historic trees

## Examples

Working patterns:
- **`examples/private-voting.compact`** - Complete voting with commitment/nullifier
- **`examples/auth-patterns.compact`** - Authentication without revealing keys
