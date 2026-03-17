---
name: abaqus-static-analysis
description: Complete workflow for static structural analysis. Use when analyzing stress, displacement, or reaction forces under constant loads. For strength and stiffness evaluation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
  - Skill
---

# Abaqus Static Analysis Workflow

Complete workflow for static structural analysis - stress, displacement, and reaction forces under constant loads.

## When to Use This Skill

**Route here when user mentions:**
- "stress analysis", "structural analysis"
- "how much will it deflect", "displacement"
- "is this strong enough", "strength check"
- "factor of safety", "safety factor"
- "reaction forces", "support loads"
- "simulate a load on this part"

**Route elsewhere:**
- Time-varying loads, impact, vibration → `/abaqus-dynamic-analysis`
- Natural frequencies, resonance → `/abaqus-modal-analysis`
- Temperature effects, thermal stress → `/abaqus-coupled-analysis`
- Heat transfer only → `/abaqus-thermal-analysis`
- Parts touching, friction → `/abaqus-contact-analysis`

## Workflow Steps

Execute these skills in order:

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | `/abaqus-geometry` | Create part and assembly |
| 2 | `/abaqus-material` | Define material properties |
| 3 | `/abaqus-mesh` | Generate finite element mesh |
| 4 | `/abaqus-bc` | Apply supports and constraints |
| 5 | `/abaqus-load` | Apply forces and pressures |
| 6 | `/abaqus-step` | Configure analysis step (optional - default is fine) |
| 7 | `/abaqus-job` | Run the analysis |
| 8 | `/abaqus-odb` | Extract results |

## What to Ask User

### Required Information

| Input | What to Ask |
|-------|-------------|
| Geometry | "What are the dimensions? (e.g., 100x50x20 mm)" |
| Material | "What material? (Steel, Aluminum, or custom E/v)" |
| Supports | "How is it supported? (fixed face, pinned points, rollers)" |
| Loads | "What loads? (force magnitude, location, direction)" |

### Optional (Has Defaults)

| Input | Default | Ask If |
|-------|---------|--------|
| Mesh size | Auto-calculated | Stress concentrations present |
| Element type | C3D8R | Complex curved geometry |
| Nonlinear | OFF | Large deformation expected |

## Key Decisions

### Linear vs Nonlinear Analysis

| Condition | Setting | When |
|-----------|---------|------|
| Small deformation, linear material | nlgeom=OFF | Displacements < 1% of part size |
| Large deformation or rotation | nlgeom=ON | Thin structures, rubber, cables |
| Yielding expected | nlgeom=ON + Plasticity | Stress > yield strength |

**Default:** Start with linear. Switch to nonlinear if convergence issues or large deformation.

### What Results to Extract

| User Goal | Output Variables | Acceptance Criteria |
|-----------|-----------------|---------------------|
| Strength assessment | S (stress), MISES | MISES < yield stress |
| Stiffness check | U (displacement) | Max deflection acceptable |
| Support sizing | RF (reaction force) | Reactions match applied loads |

## Validation Checkpoints

### After Each Step

| Step | What to Verify |
|------|----------------|
| Geometry | Part has cells, no error messages |
| Material | Section assigned to all cells |
| Mesh | Node count OK (Learning Edition: <=1000) |
| BCs | At least one fixed constraint exists |
| Loads | Applied to correct surface/point |
| Job | Completes without errors in .sta file |

### Results Sanity Checks

| Check | Expected |
|-------|----------|
| Reaction force sum | Approximately equals applied loads |
| Displacement magnitude | Physically reasonable |
| Stress pattern | Follows logical load path |
| Max stress location | At expected concentration points |

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Zero pivot" | Rigid body motion | Add more BCs to constrain all 6 DOFs |
| "Negative eigenvalue" | Buckling or instability | Check BCs, may need stabilization |
| "Too many increments" | Load too large | Reduce load or use more increments |
| "Equilibrium not achieved" | Convergence failure | Try smaller initial increment |
| "Memory exceeded" | Mesh too fine | Increase element size |

## Feedback Loops

- **Mesh fails:** Return to geometry, add partitions or simplify
- **Zero pivot error:** Return to BCs, ensure all rigid body modes constrained
- **Unreasonable results:** Verify material properties, check load direction/sign
- **Stress too high:** Either design issue (expected) or incorrect BC/load setup

## Code Patterns

For API syntax and code examples, see:
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
