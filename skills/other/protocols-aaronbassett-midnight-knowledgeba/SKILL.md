---
name: midnight-core-concepts:protocols
description: Use when asking about Kachina smart contract protocol, Zswap token transfers, atomic swaps, shielded transfers, offers, coins, or private transaction mechanisms in Midnight.
---

# Midnight Protocols

Midnight uses two foundational protocols: **Kachina** for privacy-preserving smart contracts and **Zswap** for shielded token transfers.

## Protocol Selection

| Need | Protocol |
|------|----------|
| Smart contract logic | Kachina |
| Token transfers | Zswap |
| Atomic multi-party swaps | Zswap |
| Private computation | Kachina |
| Shielded coins | Zswap |

## Kachina Protocol

Kachina enables confidential, general-purpose smart contracts while maintaining decentralization.

### Core Architecture

```
┌─────────────────────────────────────────┐
│           On-Chain (Public)             │
│  • Contract code                        │
│  • Public state                         │
│  • Merkle roots                         │
└─────────────────────────────────────────┘
              ↑ ZK Proofs ↑
┌─────────────────────────────────────────┐
│           Off-Chain (Private)           │
│  • User's private inputs                │
│  • Local state                          │
│  • Witness data                         │
└─────────────────────────────────────────┘
```

### Two-State Model

| State Type | Location | Visibility |
|------------|----------|------------|
| Public state | Blockchain | Everyone |
| Private state | User's machine | Owner only |

ZK proofs bridge these states: prove something about private state without revealing it.

### How Kachina Works

1. User submits command to contract
2. User maintains transcript of interactions (queries + expected responses)
3. ZK proof validates transcript correctness
4. Public effects applied to blockchain

### Key Properties

| Property | Benefit |
|----------|---------|
| Concurrency | Multiple users act simultaneously without blocking |
| Privacy | Private state never leaves user's machine |
| Composability | Contracts interact via public state |
| Reordering | Conflicting transactions optimally reordered |

### Use Cases

- DeFi protocols with private balances
- Supply chain with confidential data
- Healthcare with patient privacy
- Any computation mixing public and private data

## Zswap Protocol

Zswap is a shielded token mechanism for confidential atomic swaps, based on Zerocash.

### Core Concept

```
Zswap Offer = Inputs + Outputs + Transient + Balance
```

- **Inputs**: Coins being spent (nullifiers)
- **Outputs**: New coins being created (commitments)
- **Transient**: Coins created and spent in same transaction
- **Balance**: Net value change per token type

### Transaction Privacy

| Hidden | Visible |
|--------|---------|
| Sender | Transaction occurred |
| Receiver | Proof validity |
| Amount | Fee payment |
| Token type (can be) | Nullifiers (unlinkable) |

### Offer Structure

```
Offer {
  inputs: [
    { nullifier, type_value_commit, merkle_proof, zk_proof }
  ],
  outputs: [
    { commitment, type_value_commit, optional_contract, optional_ciphertext, zk_proof }
  ],
  transient: [...],
  balance: { token_type → value }
}
```

### Atomic Swaps

Zswap enables multi-party atomic exchanges:

```
Party A: Offers 10 TokenX
Party B: Offers 5 TokenY
            ↓
    Merged off-chain
            ↓
   Single atomic transaction
   (Either both happen or neither)
```

### Merging Rules

Two transactions can merge if at least one has an empty contract call section. Merged transaction combines:
- All inputs (coins spent)
- All outputs (coins created)
- Balanced value vectors

### Integration with Contracts

Contracts issue custom tokens via Zswap:

```compact
// Token type = Hash(contractAddress, domainSeparator)
// Contract can mint/burn tokens through Zswap operations
```

### Zswap Outputs

Creating new coins:

```
Output = {
  commitment: Pedersen(type, value, owner, randomness),
  type_value_commit: Pedersen(type, value),
  contract_address: optional,  // For contract-targeted coins
  ciphertext: optional,        // Encrypted for recipient
  zk_proof: validity_proof
}
```

### Zswap Inputs

Spending existing coins:

```
Input = {
  nullifier: Hash(commitment, owner_secret),
  type_value_commit: Pedersen(type, value),
  contract_address: optional,
  merkle_proof: path_to_commitment,
  zk_proof: validity_proof
}
```

**Critical**: Nullifier is unlinkable to original commitment.

## Protocol Interaction

```
┌──────────────────────────────────────────┐
│              Transaction                  │
├──────────────────────────────────────────┤
│  Zswap Section        │  Contract Section │
│  • Guaranteed offer   │  • Contract calls │
│  • Fallible offer     │  • ZK proofs      │
│  (Token transfers)    │  (State changes)  │
└──────────────────────────────────────────┘
```

Transactions combine Zswap (value movement) with Kachina (computation).

## Practical Application

### Simple Transfer

```
1. Create Zswap offer with:
   - Input: Your coin (nullifier + proof)
   - Output: Recipient's new coin (commitment)
   - Balance: Must net to zero (minus fees)
2. Submit transaction
```

### Atomic Swap

```
1. Party A creates partial offer: -10 TokenX
2. Party B creates partial offer: -5 TokenY, +10 TokenX
3. Merge offers (balanced)
4. Submit single transaction
5. Both transfers atomic
```

### Contract + Transfer

```
1. Zswap offer moves tokens
2. Contract call updates state
3. Both bound cryptographically
4. Atomic execution
```

## References

For detailed technical information:
- **`references/kachina-deep-dive.md`** - UC security model, transcript validation
- **`references/zswap-internals.md`** - Pedersen commitments, offer construction

## Examples

Working patterns:
- **`examples/basic-transfer.md`** - Simple shielded transfer
- **`examples/atomic-swap.md`** - Multi-party atomic exchange
