---
name: abaqus-load
description: Apply forces and pressures to structures. Use when user asks to apply a force, add pressure, put a load on, or mentions gravity, point loads, or distributed forces.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Load Skill

Apply mechanical and thermal loads to FEA models - forces, pressures, gravity, and heat flux.

## When to Use This Skill

**Route here when user mentions:**
- "Apply a force", "add pressure", "put a load on"
- "Gravity", "self-weight", "body force"
- "Point load", "distributed load", "traction"
- "Heat flux", "thermal load"
- "Force in the X/Y/Z direction"

**Route elsewhere:**
- Fixed supports, displacements, symmetry → `/abaqus-bc`
- Contact forces between parts → `/abaqus-interaction`
- Initial temperature fields, pre-stress → `/abaqus-field`
- Time-varying load profiles → `/abaqus-amplitude`

## Key Decisions

### 1. Which Load Type?

| User Describes | Load Type | Units |
|----------------|-----------|-------|
| Force at a point/vertex | ConcentratedForce | N |
| Force spread over surface | SurfaceTraction | MPa |
| Normal pressure on surface | Pressure | MPa |
| Force along edge | LineLoad | N/mm |
| Self-weight, acceleration | Gravity | mm/s² |
| Heat input to surface | SurfaceHeatFlux | mW/mm² |
| Convective cooling/heating | FilmCondition | mW/(mm²·K) |

### 2. When to Convert Force to Traction

If user gives **total force** but it must be **distributed**:

```
Traction (MPa) = Total Force (N) / Surface Area (mm²)
```

**Example:** 1000 N on a 50×20mm face = 1000 / 1000 = 1.0 MPa

## Sign Conventions

| Load Type | Positive (+) | Negative (-) |
|-----------|--------------|--------------|
| Pressure | Compression (into surface) | Tension (away from surface) |
| Force components (cf1, cf2, cf3) | Positive axis direction | Negative axis direction |
| Gravity | Positive axis acceleration | Negative axis (comp2=-9810 for -Y) |

## What to Ask User

If not specified, clarify:

| Question | Why It Matters |
|----------|----------------|
| Force magnitude? | Required for all loads |
| Direction (X, Y, Z)? | Needed for directional loads |
| Point or distributed? | Determines ConcentratedForce vs SurfaceTraction |
| Which surface/vertex? | Defines load application region |
| Constant or time-varying? | May need amplitude definition |

## Direction Specification

| Load Type | How Direction Works |
|-----------|---------------------|
| ConcentratedForce | cf1, cf2, cf3 = X, Y, Z components |
| SurfaceTraction | directionVector=((origin), (endpoint)) |
| Pressure | Always normal to surface (no direction needed) |
| Gravity | comp1, comp2, comp3 = acceleration components |
| LineLoad | comp1, comp2, comp3 = force/length components |

## Common Scenarios

### Standard Gravity Setup
- Acceleration: comp2 = -9810 mm/s² (for -Y direction)
- **Requires material density defined** - without it, gravity has no effect

### Pressure vs Traction
- **Pressure**: Always normal to surface, simpler to define
- **Traction**: Arbitrary direction, use when force isn't perpendicular

### Thermal Loads
- Heat flux: Direct heat input (mW/mm²)
- Film condition: Convection with ambient temperature

## Time-Varying Loads

For loads that change over time:
1. First define amplitude using `/abaqus-amplitude`
2. Reference amplitude name when creating load

## Modifying Loads Across Steps

| Action | Method |
|--------|--------|
| Change magnitude | setValuesInStep() |
| Turn off load | deactivate() |
| Different load in each step | Create load with step name |

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Zero reaction forces | Wrong direction or tiny magnitude | Check direction vector and units |
| Gravity has no effect | Missing density | Add density to material definition |
| Load region not found | Typo in set/surface name | Verify name matches exactly |
| Equilibrium not achieved | Load too large | Reduce magnitude or improve convergence |
| Negative eigenvalue | Structure unstable | Check BCs provide adequate support |

## Validation Checklist

Before running analysis:
- [ ] Load applied to correct region (surface, vertex, edge)
- [ ] Direction matches physical scenario
- [ ] Magnitude in correct units (N, MPa, mW/mm²)
- [ ] Load assigned to correct step (not Initial)
- [ ] Density defined if using gravity
- [ ] Reactions should balance applied loads

## Code Patterns

For API syntax and implementation examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
