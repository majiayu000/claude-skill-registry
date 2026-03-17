---
name: interaction-nets
description: Interaction Nets Skill
trit: 0
color: "#26D826"
catsharp:
  home: Prof
  poly_op: ⊗ (parallel)
  kan_role: Adj
  bicomodule: true
---

# interaction-nets Skill


> *"Computation as graph rewriting. No duplication. No erasure. Pure interaction."*

## Overview

**Interaction Nets** implements Lafont's interaction nets for optimal lambda calculus evaluation. Nodes interact pairwise; no garbage collection needed.

## GF(3) Role

| Aspect | Value |
|--------|-------|
| Trit | 0 (ERGODIC) |
| Role | COORDINATOR |
| Function | Coordinates node interactions in computation graphs |

## Core Concepts

### Interaction Rules

```
      ┌───┐        ┌───┐           ┌───────────┐
   ───┤ A ├────────┤ B ├───   →   ─┤  Result   ├─
      └───┘        └───┘           └───────────┘

Two agents meet at their principal ports.
They interact according to their types.
Result replaces both agents.
```

### Agent Types

```haskell
data Agent
  = Lambda Nat        -- λ-abstraction
  | App               -- Application
  | Dup               -- Duplicator (for sharing)
  | Era               -- Eraser
  | Sup Nat Nat       -- Superposition
```

## Interaction Rules

```
-- β-reduction
(λ x) @ arg  →  x[arg]

-- Duplication
Dup (λ x)  →  (λ x₁), (λ x₂)

-- Annihilation
Era (λ x)  →  Era x

-- Superposition
Sup a b  →  parallel(a, b)
```

## HVM-style Implementation

```rust
// Interaction net node
struct Node {
    tag: u8,           // Agent type
    ports: [Port; 3],  // Principal + 2 auxiliary
}

// Interaction rule
fn interact(a: Node, b: Node) -> Vec<Node> {
    match (a.tag, b.tag) {
        (LAMBDA, APP) => beta_reduce(a, b),
        (DUP, LAMBDA) => duplicate_lambda(a, b),
        (ERA, _) => erase(b),
        (SUP, SUP) if a.label == b.label => annihilate(a, b),
        (SUP, SUP) => commute(a, b),
        _ => vec![a, b]  // No interaction
    }
}
```

## Optimal Reduction

```
λf. λx. f (f x)     -- Church numeral 2

Compile to interaction net:
┌──────────────────────────────────────┐
│                                      │
│    ┌───┐     ┌───┐     ┌───┐        │
│ ───┤ λ ├─────┤ λ ├─────┤ @ ├───     │
│    └─┬─┘     └─┬─┘     └─┬─┘        │
│      │         │         │           │
│      └────┬────┘         │           │
│           │              │           │
│        ┌──┴──┐           │           │
│        │ Dup │───────────┘           │
│        └─────┘                       │
│                                      │
└──────────────────────────────────────┘

No duplication of work!
Sharing is explicit via Dup nodes.
```

## GF(3) Node Types

```python
class InteractionNet:
    """Interaction net with GF(3) node classification."""

    # Node roles
    GENERATOR = +1   # Lambda, constructors
    COORDINATOR = 0  # Application, routing
    VALIDATOR = -1   # Erasers, checkers

    def classify_node(self, node):
        if node.tag in [LAMBDA, CON]:
            return self.GENERATOR
        elif node.tag in [APP, DUP]:
            return self.COORDINATOR
        elif node.tag in [ERA, CHK]:
            return self.VALIDATOR

    def verify_conservation(self):
        """Check GF(3) balance after interaction."""
        trit_sum = sum(self.classify_node(n) for n in self.nodes)
        return trit_sum % 3 == 0
```

## Parallel Evaluation

```rust
// Interactions are confluent - order doesn't matter
fn parallel_reduce(net: &mut Net) {
    loop {
        // Find all active pairs (nodes connected at principal ports)
        let pairs = find_active_pairs(net);

        if pairs.is_empty() {
            break;  // Normal form reached
        }

        // Reduce all pairs in parallel
        pairs.par_iter().for_each(|(a, b)| {
            interact(a, b);
        });
    }
}
```

## GF(3) Triads

```
interaction-nets (0) ⊗ lambda-calculus (+1) ⊗ linear-logic (-1) = 0 ✓
interaction-nets (0) ⊗ hvm-runtime (+1) ⊗ type-checker (-1) = 0 ✓
```

---

**Skill Name**: interaction-nets
**Type**: Computation Model / Graph Rewriting
**Trit**: 0 (ERGODIC - COORDINATOR)
**GF(3)**: Coordinates node interactions

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
