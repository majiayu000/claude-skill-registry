---
name: rg-flow-acset
description: 'RG Flow ACSet Skill'
version: 1.0.0
---

# RG Flow ACSet Skill

Renormalization Group flow with ACSet categorical semantics, XY model topological defects, and Powers PCT hierarchical control.

## Seed
```
741086072858456200
```

## Triadic Palette (Powers PCT Cascade)
| Color | Hue | Hex | Role |
|-------|-----|-----|------|
| Cyan | 172° | `#23C8B3` | Ordered phase |
| Purple | 292° | `#AA22BE` | Critical/BKT |
| Gold | 52° | `#E0CE51` | Converged fixed point |

## ACSet Schema: RGFlow

```julia
@present SchRGFlow(FreeSchema) begin
  # Objects
  Trace::Ob
  EquivalenceClass::Ob
  RGStep::Ob
  FixedPoint::Ob
  
  # Morphisms
  condenses_to::Hom(Trace, EquivalenceClass)
  transforms_via::Hom(EquivalenceClass, RGStep)
  flows_to::Hom(RGStep, FixedPoint)
  
  # Attributes
  tau::Attr(RGStep, Float64)
  net_charge::Attr(RGStep, Int)
  hue::Attr(EquivalenceClass, Float64)
end

# Predicates (as computed attributes)
NetChargeZero(step) = net_charge(step) == 0
Ordered(step) = tau(step) < 0.893  # Below BKT
Converged(step) = abs(tau(step) - 0.5) < 0.01
```

## XY Model Configuration (τ=0.5)
```
Phase: Ordered (below BKT critical τ_c ≈ 0.893)
Defects: 2 vortex/antivortex pairs
Net topological charge: 0 (conserved)
Phenomenal bisect: τ* ≈ 0.5 (converged)
```

## Hierarchical Control (Powers PCT)

```
Level 5 (Program): "triadic" goal
    ↓ sets reference for
Level 4 (Transition): hue velocities [172°, 292°, 52°]
    ↓ sets reference for
Level 3 (Configuration): complementary angles
    ↓ sets reference for
Level 2 (Sensation): target hues
    ↓ sets reference for
Level 1 (Intensity): lightness 0.55
```

## RG Flow Semantics

The morphism chain `Trace → EquivalenceClass → RGStep → FixedPoint` implements:

1. **condenses_to**: Traces coarse-grain to equivalence classes (irrelevant operators drop)
2. **transforms_via**: Equivalence classes evolve under RG transformation
3. **flows_to**: RG steps converge to fixed points (universality)

## GF(3) Conservation

Triadic colors sum to 0 (mod 3):
- `#23C8B3` → trit 0 (identity)
- `#AA22BE` → trit +1 (creation)
- `#E0CE51` → trit -1 (annihilation)

Net charge: 0 + 1 + (-1) = 0 ✓

## Usage

```julia
using ACSets

@acset_type RGFlowACSet(SchRGFlow)

# Create instance at BKT transition
rg = @acset RGFlowACSet begin
  Trace = 4
  EquivalenceClass = 2
  RGStep = 1
  FixedPoint = 1
  condenses_to = [1, 1, 2, 2]
  transforms_via = [1, 1]
  flows_to = [1]
  tau = [0.5]
  net_charge = [0]
  hue = [172.0, 292.0]
end
```

## Related Skills
- `xy-model`: XY spin dynamics and BKT transition
- `phenomenal-bisect`: Temperature search for critical τ*
- `hierarchical-control`: Powers PCT cascade
- `gay-mcp`: Deterministic color generation
