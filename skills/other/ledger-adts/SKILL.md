---
name: compact-core:ledger-adts
description: Use when working with Compact on-chain state management using ledger ADTs including Cell, Counter, Map, Set, List, MerkleTree, or HistoricMerkleTree, or when needing to understand which operations are available in Compact vs TypeScript.
---

# Ledger ADTs

Reference for Midnight's ledger abstract data types for on-chain state management.

## Available ADTs

| ADT | Purpose | Key Operations |
|-----|---------|----------------|
| `Cell<T>` | Single mutable value | `read`, `write` |
| `Counter` | Increment-only counter | `increment`, `value` |
| `Map<K, V>` | Key-value storage | `lookup`, `insert`, `remove` |
| `Set<T>` | Membership collection | `member`, `insert`, `remove` |
| `List<T>` | Ordered collection | `append`, `nth`, `length` |
| `MerkleTree<T>` | Membership proofs | `insert`, `root`, `pathForLeaf` |
| `HistoricMerkleTree<T>` | Historical roots | Same + `resetHistory` |

## Quick Examples

### Counter
```compact
ledger counter: Counter;

export circuit increment(): Uint<64> {
    counter.increment(1);
    return counter.value();
}
```

### Map
```compact
ledger balances: Map<Bytes<32>, Uint<64>>;

export circuit get_balance(user: Bytes<32>): Uint<64> {
    const result = balances.lookup(user);
    return if result is Maybe::Some(balance) { balance } else { 0 };
}
```

### MerkleTree
```compact
ledger members: MerkleTree<Bytes<32>>;

export circuit prove_membership(
    leaf: Bytes<32>,
    path: Vector<Bytes<32>, 20>
): Boolean {
    const computed_root = merkleTreePathRoot(leaf, path);
    return computed_root == members.root();
}
```

## Compact vs TypeScript Operations

Some ADT operations are only available in TypeScript:

| ADT | Compact | TypeScript Only |
|-----|---------|-----------------|
| Counter | `value`, `increment` | - |
| Map | `lookup`, `insert`, `remove` | `entries`, `keys` |
| Set | `member`, `insert`, `remove` | `entries`, `size` |
| List | `nth`, `append` | `entries`, `length` |
| MerkleTree | `insert`, `root` | `pathForLeaf`, iteration |

## References

- [Counter](./references/counter.md) - Counter operations and patterns
- [Collections](./references/collections.md) - Map, Set, List operations
- [Merkle Trees](./references/merkle-trees.md) - MerkleTree and HistoricMerkleTree
- [Kernel](./references/kernel.md) - Special kernel operations
