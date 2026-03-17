---
name: datalog-fixpoint
description: Datalog bottom-up fixpoint iteration for recursive queries
trit: 0
color: "#26D826"
catsharp:
  home: Prof
  poly_op: ⊗ (parallel)
  kan_role: Adj
  bicomodule: true
---

# Datalog Fixpoint Skill

Bottom-up fixpoint iteration for recursive Datalog queries without explicit recursion.

## Core Concept

Datalog computes fixpoints via iterative saturation:
```
T^0(∅) → T^1 → T^2 → ... → T^ω (fixpoint)
```

Where T is the immediate consequence operator.

## Cat# Integration

Fixpoint computation maps to Cat# via coalgebraic semantics:

```
Trit: 0 (ERGODIC - iterative bridge)
Home: Prof (profunctors/bimodules)
Poly Op: ⊗ (parallel saturation)
Kan Role: Adj (Kleisli adjunction)
```

### GF(3) Naturality

Datalog fixpoint iteration is inherently ERGODIC:
- Each iteration step is a natural transformation
- Convergence = reaching the terminal coalgebra
- The fixpoint IS the bicomodule equilibrium
