---
name: midnight-core-concepts:architecture
description: Use when asking about Midnight transaction structure, system architecture, building blocks, how Zswap/Kachina/Impact components fit together, bindings, commitments, or Schnorr proofs.
---

# Midnight Architecture

Midnight combines ZK proofs, shielded tokens, and smart contracts into a unified privacy-preserving system. Understanding how pieces connect is essential for building applications.

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Midnight Network                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Zswap     │  │   Kachina   │  │   Impact    │     │
│  │  (Tokens)   │←→│ (Contracts) │←→│    (VM)     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         ↑                ↑                ↑             │
│         └────────────────┼────────────────┘             │
│                          │                              │
│              ┌───────────────────────┐                  │
│              │   ZK Proof System     │                  │
│              │   (ZK SNARKs)         │                  │
│              └───────────────────────┘                  │
└─────────────────────────────────────────────────────────┘
```

## Transaction Anatomy

Every Midnight transaction contains:

```
Transaction {
  guaranteed_zswap_offer,    // Required: token operations
  fallible_zswap_offer?,     // Optional: may-fail token ops
  contract_calls?,           // Optional: contract interactions
  binding_randomness         // Cryptographic binding
}
```

### Guaranteed vs Fallible

| Section | Behavior |
|---------|----------|
| Guaranteed | Must succeed, or entire tx rejected |
| Fallible | May fail without affecting guaranteed section |

**Use case**: Guaranteed section collects fees. Fallible section attempts swap. If swap fails, fees still collected.

## Building Blocks

### 1. Zswap Offers

Token movement layer:

```
Offer {
  inputs: Coin[],      // Spent coins (nullifiers)
  outputs: Coin[],     // Created coins (commitments)
  transient: Coin[],   // Created and spent same tx
  balance: Map<Type, Value>  // Net value per token
}
```

### 2. Contract Calls

Computation layer:

```
ContractCall {
  guaranteed_transcript,     // Visible effects
  fallible_transcript,       // May-fail effects
  communication_commitment,  // Cross-contract (future)
  zk_proofs                  // Validity proofs
}
```

### 3. Cryptographic Binding

All components bound together via:
- **Pedersen commitments** - Homomorphic value binding
- **Schnorr proofs** - Contract contribution carries no hidden value
- **ZK proofs** - Transcript validity

## Transaction Integrity

### Homomorphic Commitments

Midnight extends Zswap's Pedersen commitment scheme:

```
Commitment(v1) + Commitment(v2) = Commitment(v1 + v2)
```

This allows verifying total value without revealing individual values.

### Binding Mechanism

```
Transaction binding ensures:
1. Zswap values balance (inputs = outputs + fees)
2. Contract effects match proofs
3. All components cryptographically linked
4. No value created from nothing
```

## State Architecture

### Ledger Structure

```
Ledger {
  zswap_state: {
    coin_commitments: MerkleTree,
    free_slot_index: Index,
    nullifier_set: Set<Nullifier>,
    valid_roots: Set<MerkleRoot>
  },
  contract_map: Map<Address, ContractState>
}
```

### Contract State

```
ContractState {
  public_fields: Map<Name, Value>,
  merkle_trees: Map<Name, MerkleTree>,
  sets: Map<Name, Set>
}
```

## Execution Flow

### Transaction Processing

```
1. Well-formedness Check (stateless)
   ├─ Format validation
   ├─ ZK proof verification
   ├─ Schnorr proof verification
   ├─ Balance verification
   └─ Claim matching

2. Guaranteed Execution (stateful)
   ├─ Contract lookups
   ├─ Zswap offer application
   ├─ Contract call execution
   └─ State persistence

3. Fallible Execution (stateful, may fail)
   ├─ Similar to guaranteed
   └─ Failure doesn't revert guaranteed
```

### Contract Call Execution

```
For each contract call:
1. Lookup contract state
2. Verify ZK proof against circuit
3. Execute Impact program
4. Verify effects match declared effects
5. Update state
```

## Merging Transactions

Zswap enables atomic composition:

```
Tx1 (Party A)     Tx2 (Party B)
     ↓                 ↓
     └─────┬───────────┘
           ↓
    Merged Transaction
    (atomic, all-or-nothing)
```

### Merging Rules

- At least one tx must have empty contract calls
- Values must balance when combined
- Proofs remain independently valid

## Address Derivation

```
Contract Address = Hash(deployment_data)
Token Type = Hash(contract_address, domain_separator)
Coin Commitment = Pedersen(type, value, owner, randomness)
Nullifier = Hash(commitment, owner_secret)
```

## Component Integration

### How Tokens Flow

```
User Wallet                    Contract
    │                              │
    │ ──── Zswap Input ────────→  │  (spend coin)
    │                              │
    │ ←─── Zswap Output ───────── │  (receive coin)
    │                              │
    │ ──── Contract Call ──────→  │  (invoke logic)
```

### How Privacy Works

```
Private Domain          Public Domain
──────────────          ─────────────
User secrets     ──ZK Proof──→  Transcript
Local state                     State changes
Merkle paths                    Nullifiers
Witness data                    Commitments
```

## Practical Patterns

### Simple Value Transfer

```
1. Construct Zswap offer
   - Input: Your coin (create nullifier)
   - Output: Recipient coin (create commitment)
2. Balance must be zero (minus fees)
3. Generate ZK proof
4. Submit transaction
```

### Contract Interaction

```
1. Prepare witness data (private inputs)
2. Construct contract call
3. Generate ZK proof (proves valid execution)
4. Optionally combine with Zswap offers
5. Submit transaction
```

### Atomic Swap

```
1. Party A: Create partial offer (gives TokenX)
2. Party B: Create partial offer (gives TokenY, wants TokenX)
3. Merge offers off-chain
4. Submit merged transaction
5. Both transfers atomic
```

## References

For detailed technical information:
- **`references/transaction-deep-dive.md`** - Complete transaction structure
- **`references/state-management.md`** - Ledger operations, state transitions
- **`references/cryptographic-binding.md`** - Pedersen, Schnorr, proof composition

## Examples

Working patterns:
- **`examples/transaction-construction.md`** - Building transactions step by step
