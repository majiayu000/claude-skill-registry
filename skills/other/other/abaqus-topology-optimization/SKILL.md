---
name: abaqus-topology-optimization
description: Complete workflow for topology optimization using Tosca. Use to minimize weight while maintaining stiffness. Requires full Abaqus license (not Learning Edition).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
  - Skill
---

# Abaqus Topology Optimization Workflow

Complete workflow for topology optimization - determining optimal material distribution to minimize weight while maintaining structural performance.

## When to Use This Skill

**Triggers:** topology optimization, minimize weight, lightweight design, organic structure, generative design, where to remove material, material efficiency, design for additive

**USE for:** Minimize weight while maintaining stiffness, maximize stiffness for given weight, generate organic load-carrying structures

**Do NOT use for:** Shape optimization (surface only) -> `/abaqus-shape-optimization`, Learning Edition users -> Tosca requires full license

## Important: License Required

Topology optimization requires a **full Abaqus license with Tosca module**. NOT available in Learning Edition.

## Prerequisites

1. Working static analysis that converges
2. Design space defined (bounding volume for material)
3. Clear objective (usually max stiffness at target weight)
4. Known load cases and boundary conditions

## Workflow Steps

### Phase 1: Setup Base Model

1. `/abaqus-geometry` - Design space with partitions for frozen regions
2. `/abaqus-material` - Elastic properties + **density (required for TO)**
3. `/abaqus-mesh` - Fine mesh (2-5mm typical for TO)
4. `/abaqus-bc` - Fixed supports (these regions become frozen)
5. `/abaqus-load` - Applied forces (these regions become frozen)
6. `/abaqus-step` - Static step for stiffness optimization

### Phase 2: Configure Optimization

Use `/abaqus-optimization` for detailed API patterns.

1. Create TopologyTask with SIMP interpolation
2. Define design responses (volume, strain energy)
3. Set objective function (minimize compliance)
4. Add constraints (volume <= target fraction)
5. Define frozen regions (BC and load attachment areas)
6. Add manufacturing constraints (min member size)

### Phase 3: Run and Post-Process

1. `/abaqus-job` - Submit OptimizationProcess
2. `/abaqus-odb` - View density distribution
3. `/abaqus-export` - STL export at density threshold (0.3-0.5 typical)

## Key Decisions

| Goal | Objective | Constraint |
|------|-----------|------------|
| Stiffest at weight | Minimize compliance | Volume <= X% |
| Lightest that works | Minimize volume | Compliance <= Y |
| Avoid resonance | Maximize frequency | Volume <= X% |

**Most common:** Minimize compliance with volume constraint at 30%.

### Volume Fraction

| Fraction | Use Case |
|----------|----------|
| 20-30% | Aggressive (aerospace) |
| 30-40% | Balanced (general) |
| 40-50% | Conservative (safety-critical) |

### Manufacturing Constraints

| Constraint | When to Use |
|------------|-------------|
| Minimum member size | Always (3-5mm typical) |
| Draw direction | Casting, molding |
| Symmetry plane | Balanced loads, aesthetics |
| Overhang angle | Additive manufacturing |

## What to Ask User

**Critical:**
- Design space: "What is the bounding volume where material can exist?"
- Frozen regions: "Which areas must remain solid? (BC/load attachment)"
- Volume fraction: "What percentage of material should remain? (20-50%)"
- Loads and BCs: "What loads and supports act on the structure?"

**With Defaults:**
- Objective: Min compliance (change if stress/frequency is primary)
- Min member size: 3mm (adjust for manufacturing)
- Material: Steel (if not specified)
- Max iterations: 50 (increase if not converging)
- SIMP penalty: 3.0 (higher for sharper boundaries)

## Validation

| Stage | Check |
|-------|-------|
| Base model | Static analysis runs, results sensible |
| After iteration 5 | Objective decreasing, no disconnection |
| Convergence | Objective stable (< 0.1% change) |
| Final design | Load path intact, no floating regions |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Checkerboard pattern | Add min member size constraint |
| Not converging | Relax volume fraction, check frozen regions |
| Disconnected regions | Add more frozen regions along load path |
| Takes forever | Coarsen mesh, reduce iterations |
| License error | Requires full Abaqus with Tosca |

## Code Patterns

For API syntax and code examples, see:
- `/abaqus-optimization` - Task, response, objective, constraint API
- `references/common-patterns.md` - Complete TO code patterns

## Related Skills

- `/abaqus-optimization` - Base optimization API details
- `/abaqus-static-analysis` - Required before optimization
- `/abaqus-shape-optimization` - Alternative for surface-only changes
- `/abaqus-export` - Export optimized geometry
