---
name: midnight-core-concepts:smart-contracts
description: Use when asking about Midnight smart contracts, Compact language basics, Impact VM, contract state separation, circuit entry points, deployment, or transaction execution model.
---

# Midnight Smart Contracts

Midnight smart contracts are **replicated state machines** that process transactions to modify ledger state. Unlike traditional blockchains, they incorporate zero-knowledge proofs to enable data privacy.

## Core Architecture

### Contract = State Machine + ZK Proofs

```
Transaction = Public Transcript + Zero-Knowledge Proof
```

- **Public transcript**: Visible state changes
- **ZK proof**: Cryptographic validation that rules were followed

The proof demonstrates correct execution without revealing private inputs.

## Compact Language

Compact is Midnight's domain-specific language for writing privacy-preserving contracts.

### Contract Structure

```compact
// Ledger state (on-chain, public unless MerkleTree)
ledger {
  counter: Field;
  commitments: MerkleTree<32, Bytes<32>>;
}

// Circuit = entry point with ZK proof
export circuit increment(amount: Field): Void {
  ledger.counter = ledger.counter + amount;
}

// Witness = circuit with private inputs
export witness privateIncrement(
  secret: Field  // Private, not revealed
): Void {
  assert secret > 0;
  ledger.counter = ledger.counter + 1;
}
```

### Key Constructs

| Construct | Purpose |
|-----------|---------|
| `ledger { }` | On-chain public state |
| `export circuit` | Public entry point, generates ZK proof |
| `export witness` | Entry point with private inputs |
| `assert` | Constraint that must hold (proven via ZK) |

## Public vs Private State

### Public State (Ledger)

Everything in `ledger { }` is publicly visible **except** MerkleTree contents:

```compact
ledger {
  public_counter: Field;           // Visible to all
  public_address: Address;         // Visible to all
  hidden_set: MerkleTree<32, T>;   // Contents hidden
}
```

### Private State

Private data exists only in the user's local environment:
- Witness inputs (never go on-chain)
- Local variables in circuit execution
- Merkle tree paths

```compact
export witness transfer(
  secret_key: Bytes<32>,    // Private - user's machine only
  amount: Field             // Private - user's machine only
): Void {
  // Prove authorization without revealing key
  const pub_key = persistentHash(secret_key);
  assert pub_key == ledger.authorized;
  // ... rest of logic
}
```

## Execution Model

### Transaction Phases

1. **Well-formedness check** (no ledger state needed)
   - Format validation
   - ZK proof verification
   - Schnorr proof verification
   - Balance checks

2. **Guaranteed phase** (must succeed)
   - Contract lookups
   - Zswap offer application
   - Sequential contract call execution
   - State persistence

3. **Fallible phase** (may fail without reverting guaranteed)
   - Similar mechanics but failure doesn't prevent ledger inclusion
   - Guaranteed effects persist regardless

### State Transitions

```
Old State + Transaction → New State
                ↓
        Impact Program Execution
                ↓
        Effects must match declared effects
                ↓
        New state stored
```

## Impact VM

Impact is the on-chain virtual machine that executes contract logic.

### Characteristics

| Property | Description |
|----------|-------------|
| Stack-based | Operations push/pop from stack |
| Non-Turing-complete | Bounded execution, no infinite loops |
| Deterministic | Same input → same output always |
| Gas-bounded | Programs have cost limits |

### Stack Structure

```
[Context, Effects, State]
   ↓        ↓        ↓
 Tx data  Actions  Contract data
```

### Developer Note

Developers write Compact, not Impact. Impact is an implementation detail visible when inspecting transactions.

## Value Handling

Contracts interact with tokens through Zswap:

```compact
// Receive coins into contract
receive coins: Coin[];

// Send coins from contract
send value: QualifiedValue, to: Address;
```

**Important**: Coin operations are recorded in the public transcript but don't directly modify contract state. They're Zswap-level operations.

## Contract Deployment

Contracts are deployed via deployment transactions:

```
Deployment Transaction = Contract State + Nonce
Contract Address = Hash(deployment data)
```

## Practical Patterns

### Simple Counter

```compact
ledger {
  count: Field;
}

export circuit increment(): Void {
  ledger.count = ledger.count + 1;
}
```

### Private Authorization

```compact
ledger {
  owner_hash: Bytes<32>;
  value: Field;
}

export witness authorizedUpdate(
  owner_secret: Bytes<32>,
  new_value: Field
): Void {
  assert persistentHash(owner_secret) == ledger.owner_hash;
  ledger.value = new_value;
}
```

### Commitment-Based State

```compact
ledger {
  commitments: MerkleTree<32, Bytes<32>>;
  nullifiers: Set<Bytes<32>>;
}

export witness spend(
  amount: Field,
  secret: Bytes<32>,
  path: MerkleTreePath<32, Bytes<32>>
): Void {
  const commitment = persistentCommit(amount, secret);
  assert ledger.commitments.member(commitment, path);

  const nullifier = persistentHash(commitment, secret);
  assert !ledger.nullifiers.member(nullifier);
  ledger.nullifiers.insert(nullifier);
}
```

## References

For detailed technical information:
- **`references/compact-syntax.md`** - Complete language reference
- **`references/impact-vm.md`** - VM internals, opcodes, gas costs
- **`references/execution-semantics.md`** - Detailed transaction execution flow

## Examples

Working contracts:
- **`examples/counter.compact`** - Minimal contract example
- **`examples/private-vault.compact`** - Private state management
