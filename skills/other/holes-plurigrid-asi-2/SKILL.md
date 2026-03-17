---
name: holes
description: Narya interactive proof development with typed holes
trit: 0
color: "#26D826"
catsharp:
  home: Prof
  poly_op: ⊗ (parallel)
  kan_role: Adj
  bicomodule: true
---

# Holes Skill

Interactive proof development using typed holes in Narya proof assistant.

See [HOLES_GUIDE.md](./HOLES_GUIDE.md) for detailed usage.

## Cat# Integration

This skill maps to Cat# = Comod(P) as a bicomodule:

```
Trit: 0 (ERGODIC - bridge/coordinator)
Home: Prof (profunctors/bimodules)
Poly Op: ⊗ (parallel composition)
Kan Role: Adj (adjunction bridge)
```

### GF(3) Naturality

Typed holes represent "gaps" in the proof space - they are ERGODIC elements
that bridge between what is known (MINUS) and what needs to be constructed (PLUS).
