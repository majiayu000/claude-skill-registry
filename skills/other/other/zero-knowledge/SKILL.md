---
name: midnight-core-concepts:zero-knowledge
description: Use when asking about zero-knowledge proofs, ZK SNARKs, circuit compilation, witness data, prover/verifier roles, constraints, or how Midnight uses ZK for privacy.
---

# Zero-Knowledge Proofs in Midnight

Zero-knowledge proofs let you prove knowledge of a secret without revealing it. In Midnight, ZK proofs validate that transactions follow contract rules without exposing private data.

## Core Concept

A ZK proof proves: "I know values that satisfy these constraints" without revealing the values.

**Midnight application**: Prove a transaction is valid (correct inputs, authorized user, rules followed) without exposing private state or user secrets.

## ZK SNARKs

Midnight uses **ZK SNARKs** (Zero-Knowledge Succinct Non-interactive Arguments of Knowledge):

| Property | Meaning |
|----------|---------|
| **Zero-Knowledge** | Verifier learns nothing beyond validity |
| **Succinct** | Proof size small regardless of computation complexity |
| **Non-interactive** | No back-and-forth between prover and verifier |
| **Argument of Knowledge** | Prover must actually know the secret |

## How Proofs Work in Midnight

### Transaction Structure

Every Midnight transaction contains:
1. **Public transcript** - Visible state changes
2. **Zero-knowledge proof** - Cryptographic validation

The proof demonstrates: "I know private inputs that, when combined with public data, satisfy the contract's constraints."

### Circuit Mental Model

Contract logic compiles to **circuits** - mathematical constraint systems.

```
Compact Code → Circuit Constraints → ZK Proof
```

A circuit defines relationships between variables. The proof shows you know variable assignments satisfying all constraints without revealing the assignments.

### Proof Lifecycle

```
1. Setup      → Generate proving/verification keys (per circuit)
2. Witness    → Prover assembles private inputs
3. Prove      → Generate proof from witness + circuit
4. Verify     → Check proof against public inputs (fast)
```

## Circuits in Practice

### What Gets Proven

When a Compact contract executes:
1. Contract logic compiles to arithmetic circuit
2. Private values become witness inputs
3. Public values become public inputs
4. Proof demonstrates correct execution

### Circuit Constraints

Circuits express computations as polynomial constraints:

```
// Conceptual: proving x * y = z without revealing x, y
constraint: a * b = c
public input: c = 42
witness (private): a = 6, b = 7
```

### Compact to Circuit

```compact
// This Compact code...
export circuit guess(guess: Field): Void {
  const product = guess * other_factor;
  assert product == ledger.target;
}

// ...compiles to constraints that prove:
// 1. guess * other_factor equals target
// 2. Without revealing guess or other_factor values
```

## Practical Applications

### Proving Without Revealing

| Scenario | What's Proven | What's Hidden |
|----------|---------------|---------------|
| Age verification | Age ≥ 18 | Exact birthdate |
| Balance check | Balance ≥ amount | Actual balance |
| Membership | In authorized set | Which member |
| Vote validity | Eligible voter, hasn't voted | Voter identity |

### In Contracts

```compact
// Prove knowledge of factors without revealing them
export circuit proveFactors(
  secret_a: Field,  // Private witness
  secret_b: Field   // Private witness
): Void {
  // Constraint: factors multiply to public target
  assert secret_a * secret_b == ledger.public_target;
}
```

## Key Concepts

### Witness
Private inputs the prover knows. Never revealed, used only to generate proof.

### Public Inputs
Values visible to everyone. Proof verified against these.

### Verification
Checking a proof is fast (milliseconds) regardless of original computation complexity.

### Soundness
Computationally infeasible to create valid proof without knowing witness.

## Performance Characteristics

| Operation | Cost |
|-----------|------|
| Circuit compilation | One-time, expensive |
| Proof generation | Seconds to minutes (depends on circuit size) |
| Proof verification | Milliseconds |
| Proof size | ~200-300 bytes (constant) |

## References

For detailed technical information:
- **`references/snark-internals.md`** - Elliptic curves, pairings, trusted setup
- **`references/circuit-construction.md`** - How Compact compiles to circuits

## Examples

Working patterns:
- **`examples/circuit-patterns.compact`** - Common proof patterns
