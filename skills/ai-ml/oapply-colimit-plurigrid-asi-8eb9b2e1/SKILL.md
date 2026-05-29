---
name: oapply-colimit
description: oapply operad algebra evaluation via colimits with Specter-style composition patterns
version: 1.0.0
---


# oapply-colimit Skill

> Operad algebra evaluation via colimits with bidirectional navigation

**Version**: 1.1.0
**Trit**: +1 (Generator - composes systems)

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

## Specter-Style Navigation for Wiring Diagrams

Navigate wiring diagrams with bidirectional paths:

```julia
using SpecterACSet

# Navigate to all boxes
select([wd_boxes, ALL], diagram)

# Navigate to all wires from a specific box
select([wd_wires, pred(w -> source_box(w) == 1)], diagram)

# Transform: rename all boxes
transform([wd_boxes, ALL, box_name], uppercase, diagram)
```

### Wiring Diagram Navigators

| Navigator | Select | Transform |
|-----------|--------|-----------|
| `wd_boxes` | All boxes | Update boxes |
| `wd_wires` | All wires | Update wires |
| `wd_ports(box_id)` | Ports of box | Update ports |
| `wd_outer_ports` | Outer interface | Update interface |

## Connection to Specter's comp-navs

Specter's `comp-navs` pattern mirrors oapply:

```julia
# Specter: compose navigators (fast - just allocation)
comp_navs(nav1, nav2, nav3)

# oapply: compose machines (colimit of diagram)
oapply(wiring, [machine1, machine2, machine3])
```

Both use **composition as colimit** - Specter over paths, oapply over state spaces.

## Compositional Dynamics Example

```julia
# Lotka-Volterra as composed resource sharers
rabbit = ResourceSharer{Float64}([:pop], [:pop]) do u, p, t
    [p.α * u[1]]  # growth
end

fox = ResourceSharer{Float64}([:pop], [:pop]) do u, p, t
    [-p.δ * u[1]]  # decay
end

# Compose via shared population interface
predation = oapply(predation_diagram, [rabbit, fox])
```

## Sexp Serialization for Wiring Diagrams

```julia
# Wiring diagram → Sexp
sexp = sexp_of_wiring_diagram(diagram)

# Navigate: find all box names
box_names = select([SEXP_CHILDREN, pred(is_box), SEXP_HEAD, ATOM_VALUE], sexp)

# Roundtrip
diagram2 = wiring_diagram_of_sexp(sexp)
```

## GF(3) Triads

```
schema-validation (-1) ⊗ acsets (0) ⊗ oapply-colimit (+1) = 0 ✓
interval-presheaf (-1) ⊗ algebraic-dynamics (0) ⊗ oapply-colimit (+1) = 0 ✓
bisimulation-game (-1) ⊗ coequalizers (0) ⊗ oapply-colimit (+1) = 0 ✓
```

## Related Skills

- `coequalizers` (0) - Uses pushout = coproduct + coequalizer decomposition
- `bisimulation-game` (-1) - Behavioral equivalence for skill paths
- `topos-adhesive-rewriting` (+1) - Incremental updates via coequalizers

## Koopman Integration

For time-varying systems, oapply composes observable functors:

```julia
# Koopman operator: lift nonlinear → infinite-dim linear
# oapply: compose lifted systems via colimit

composed_koopman = oapply(
    dynamics_diagram,
    [koopman_lift(system1), koopman_lift(system2)]
)
```

## References

- Libkind "An Algebra of Resource Sharers" arXiv:2007.14442
- AlgebraicJulia/AlgebraicDynamics.jl
- Nathan Marz: Specter composition patterns



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 5. Evaluation

**Concepts**: eval, apply, interpreter, environment

### GF(3) Balanced Triad

```
oapply-colimit (−) + SDF.Ch5 (−) + [balancer] (−) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch3: Variations on an Arithmetic Theme
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch10: Adventure Game Example
- Ch7: Propagators

### Connection Pattern

Evaluation interprets expressions. This skill processes or generates evaluable forms.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: -1 (MINUS)
Home: Prof
Poly Op: ⊗
Kan Role: Ran_K
Color: #FF6B6B
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.