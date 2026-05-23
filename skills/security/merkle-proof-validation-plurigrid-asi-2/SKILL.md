---
name: merkle-proof-validation
description: Merkle Proof Validation Skill
trit: 0
color: "#26D826"
catsharp:
  home: Prof
  poly_op: ⊗ (parallel)
  kan_role: Adj
  bicomodule: true
---

# merkle-proof-validation Skill


> *"Trust but verify. Every leaf proves its tree."*

## Overview

**Merkle Proof Validation** implements cryptographic verification of inclusion proofs. Given a leaf and a path, validate membership in a Merkle tree without the full tree.

## GF(3) Role

| Aspect | Value |
|--------|-------|
| Trit | -1 (MINUS) |
| Role | VALIDATOR |
| Function | Validates Merkle inclusion proofs |

## Core Algorithm

```python
import hashlib

def hash_pair(left: bytes, right: bytes) -> bytes:
    """Hash two nodes together."""
    return hashlib.sha256(left + right).digest()

def verify_merkle_proof(
    leaf: bytes,
    proof: list[tuple[bytes, str]],  # (sibling_hash, position)
    root: bytes
) -> bool:
    """
    Verify a Merkle inclusion proof.

    Args:
        leaf: The leaf value to verify
        proof: List of (sibling_hash, 'left'|'right') pairs
        root: Expected Merkle root

    Returns:
        True if leaf is in tree with given root
    """
    current = hashlib.sha256(leaf).digest()

    for sibling, position in proof:
        if position == 'left':
            current = hash_pair(sibling, current)
        else:
            current = hash_pair(current, sibling)

    return current == root
```

## Move Implementation

```move
module merkle::validation {
    use std::vector;
    use aptos_std::aptos_hash;

    const E_INVALID_PROOF: u64 = 1;

    struct MerkleProof has store, drop {
        leaf: vector<u8>,
        siblings: vector<vector<u8>>,
        positions: vector<bool>,  // true = sibling on left
        root: vector<u8>,
    }

    public fun verify(proof: &MerkleProof): bool {
        let current = aptos_hash::sha3_256(proof.leaf);
        let len = vector::length(&proof.siblings);
        let i = 0;

        while (i < len) {
            let sibling = vector::borrow(&proof.siblings, i);
            let is_left = *vector::borrow(&proof.positions, i);

            current = if (is_left) {
                hash_pair(*sibling, current)
            } else {
                hash_pair(current, *sibling)
            };
            i = i + 1;
        };

        current == proof.root
    }

    fun hash_pair(left: vector<u8>, right: vector<u8>): vector<u8> {
        let combined = vector::empty<u8>();
        vector::append(&mut combined, left);
        vector::append(&mut combined, right);
        aptos_hash::sha3_256(combined)
    }
}
```

## Proof Structure

```
                    Root
                   /    \
                  /      \
                H01      H23
               /   \    /   \
              H0   H1  H2   H3
              |    |   |    |
             L0   L1  L2   L3  ← Leaves

Proof for L1: [(H0, left), (H23, right)]
Verify: hash(H0 || hash(L1)) → H01
        hash(H01 || H23) → Root ✓
```

## GF(3) Integration

```python
class GF3MerkleValidator:
    """Merkle validation with GF(3) conservation."""

    TRIT = -1  # VALIDATOR role

    def validate_batch(self, proofs: list) -> dict:
        """
        Validate batch of proofs.
        Each validation is a MINUS operation.
        """
        results = []
        for proof in proofs:
            valid = self.verify(proof)
            results.append({
                'leaf': proof.leaf,
                'valid': valid,
                'trit': self.TRIT  # -1 for validation
            })

        # GF(3) check: need balancing generators
        trit_sum = len(proofs) * self.TRIT
        return {
            'results': results,
            'trit_sum': trit_sum,
            'needs_generators': -trit_sum  # To balance
        }
```

## IECsat Integration

For hierarchical tile validation:

```python
def validate_tile_inclusion(
    tile_code: str,      # e.g., "9C3XGV2F+QQ"
    tile_hash: bytes,
    root_tile: str,      # e.g., "9C3XGV2F+"  (10-char)
    proof: list
) -> bool:
    """
    Validate that a fine tile belongs to a root tile's Merkle tree.

    On-chain: 10-char root tiles with Merkle roots
    Off-chain: 11-17 char tiles with proofs
    """
    # Verify the Plus Code hierarchy
    assert tile_code.startswith(root_tile.rstrip('+'))

    # Verify Merkle inclusion
    return verify_merkle_proof(tile_hash, proof, get_root(root_tile))
```

## GF(3) Triads

```
merkle-proof-validation (-1) ⊗ iecsat-storage (0) ⊗ aptos-gf3-society (+1) = 0 ✓
merkle-proof-validation (-1) ⊗ datalog-fixpoint (0) ⊗ anoma-intents (+1) = 0 ✓
merkle-proof-validation (-1) ⊗ spi-parallel-verify (0) ⊗ polyglot-spi (+1) = 0 ✓
```

## Commands

```bash
# Generate Merkle proof (Python)
python3 -c "
from merkle import MerkleTree
tree = MerkleTree(leaves)
proof = tree.get_proof(leaf_index)
print(proof.to_json())
"

# Verify on-chain (Move)
aptos move run --function merkle::validation::verify --args ...
```

---

**Skill Name**: merkle-proof-validation
**Type**: Cryptographic Verification
**Trit**: -1 (MINUS - VALIDATOR)
**GF(3)**: Validates inclusion proofs

## Cat# Integration

This skill maps to Cat# = Comod(P) as a bicomodule in the Prof home:

```
Trit: 0 (ERGODIC)
Home: Prof (profunctors/bimodules)
Poly Op: ⊗ (parallel composition)
Kan Role: Adj (adjunction bridge)
```

### GF(3) Naturality

The skill participates in triads where:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.
