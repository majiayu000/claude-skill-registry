---
name: oapply-colimit
description: "oapply: Operad algebra evaluation via colimits. Composes machines/resource sharers."
source: AlgebraicJulia/AlgebraicDynamics.jl
license: MIT
trit: +1
---

# oapply-colimit Skill

## Core Pattern

`oapply` computes **colimit** of component diagram over wiring pattern:

```julia
using AlgebraicDynamics

# Pattern + components → composite
composite = oapply(wiring_diagram, [machine1, machine2, ...])
```

## Two Composition Modes

| Mode | Type | Gluing | Example |
|------|------|--------|---------|
| **Undirected** | ResourceSharer | Pushout (shared state) | Lotka-Volterra |
| **Directed** | Machine | Wiring (signal flow) | Control systems |

## Implementation

```julia
function oapply(d::UndirectedWiringDiagram, xs::Vector{ResourceSharer})
    # 1. Coproduct of state spaces
    S = coproduct((FinSet ∘ nstates).(xs))
    
    # 2. Pushout identifies shared variables
    S′ = pushout(portmap, junctions)
    
    # 3. Induced dynamics sum at junctions
    return ResourceSharer(induced_interface, induced_dynamics)
end
```

## GF(3) Triads

```
schema-validation (-1) ⊗ acsets (0) ⊗ oapply-colimit (+1) = 0 ✓
interval-presheaf (-1) ⊗ algebraic-dynamics (0) ⊗ oapply-colimit (+1) = 0 ✓
```

## References

- Libkind "An Algebra of Resource Sharers" arXiv:2007.14442
- AlgebraicJulia/AlgebraicDynamics.jl
