---
name: abaqus-modal-analysis
description: Complete workflow for modal/frequency analysis - extract natural frequencies and mode shapes. Use for vibration analysis and resonance avoidance.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
  - Skill
---

# Abaqus Modal Analysis Skill

Extract natural frequencies and mode shapes from a structure. Use for vibration analysis, resonance avoidance, and dynamic characterization.

## When to Use This Skill

**Route here when user mentions:**
- "Natural frequency", "modal analysis", "vibration"
- "Resonance", "mode shapes", "eigenvalue"
- "How will it vibrate?", "avoid resonance at X Hz"
- "First mode frequency", "natural frequency of beam/plate"

**Route elsewhere:**
- Forced vibration response → use transient dynamic
- Frequency response function → use steady-state dynamics
- Static stress/deflection → `/abaqus-static-analysis`
- Impact/crash → `/abaqus-dynamic-analysis`

## Prerequisites

Before modal analysis:
1. Geometry and mesh ready
2. Material MUST have density defined (required for mass matrix)
3. Boundary conditions define the modal boundary
4. NO loads needed for eigenvalue extraction

## Workflow: Modal Analysis

### Step 1: Understand User's Goal

Ask if unclear:
- **How many modes?** First few (5-10) or all in frequency range?
- **Boundary conditions?** Fixed, pinned, free-free?
- **Frequency range of interest?** Motor at 60 Hz, etc.?
- **What geometry?** Beam, plate, bracket, assembly?

### Step 2: Create Geometry

Route to `/abaqus-geometry` for part creation.

### Step 3: Define Material WITH DENSITY

Route to `/abaqus-material` - density is **essential**.

Without density, Abaqus cannot compute the mass matrix and modal analysis will fail.

| Material | Density (tonne/mm^3) |
|----------|---------------------|
| Steel | 7.85e-9 |
| Aluminum | 2.7e-9 |
| Titanium | 4.5e-9 |

### Step 4: Create Mesh

Route to `/abaqus-mesh` for meshing.

Mesh quality affects mode shapes - finer mesh gives more accurate high-frequency modes.

### Step 5: Apply Boundary Conditions

Route to `/abaqus-bc` to define support type.

| Configuration | Expected Modes | Use Case |
|---------------|----------------|----------|
| Free-free (no BCs) | 6 rigid body modes at ~0 Hz, then elastic | Test correlation |
| Cantilever (one end fixed) | First mode is bending | Mounted component |
| Simply supported | Bending, plate modes | Bridge-like structures |
| Fixed-fixed | Higher frequencies than cantilever | Both ends constrained |

**Note:** Free-free analysis gives 6 modes at ~0 Hz (rigid body translation/rotation). Real elastic modes start at mode 7.

### Step 6: Create Frequency Step

Route to `/abaqus-step` for FrequencyStep configuration.

Key decisions:
- **Fixed count:** Extract exactly N modes (numEigen=10)
- **Frequency range:** All modes between min and max Hz
- **Shift-invert:** Modes near target frequency (for high-frequency focus)

### Step 7: Run and Extract

Route to `/abaqus-job` to submit, then `/abaqus-odb` to read frequencies from result frames.

## Key Parameters

| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| Eigensolver | LANCZOS | Best for most problems |
| numEigen | 10 | Start with first 10 modes |
| Normalization | DISPLACEMENT | Mode shapes max = 1 |
| Mesh size | Adequate for highest mode | Finer mesh for high frequencies |

## Validation Checklist

After analysis, verify:
- [ ] Density defined in material
- [ ] BCs match intended support condition
- [ ] No loads applied (eigenvalue extraction ignores loads)
- [ ] Mesh adequate for highest mode of interest
- [ ] Frequencies reasonable for geometry/material
- [ ] Free-free: confirm 6 modes near 0 Hz

## Analytical Comparison (Simple Geometries)

For cantilever beams, first mode can be verified analytically:
- f1 ~ (1.875^2 / 2*pi*L^2) * sqrt(E*I / rho*A)

Compare FEA result to analytical for validation.

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| "Material has no density" | Density not defined | Add density to material |
| Negative eigenvalue | Unconstrained/unstable | Check BCs or add soft springs |
| 6 zero-frequency modes | Free-free (expected) | Real modes start at mode 7 |
| Frequencies too high/low | Unit error | Verify mm-tonne-s-N-MPa units |
| Memory error | Too many modes/elements | Reduce numEigen or coarsen mesh |

## Related Skills

- `/abaqus-material` - Must include density
- `/abaqus-bc` - Define modal boundary conditions
- `/abaqus-step` - FrequencyStep configuration
- `/abaqus-odb` - Extract frequencies and mode shapes
- `/abaqus-geometry` - Create geometry
- `/abaqus-mesh` - Mesh affects mode accuracy

## Code Patterns

For API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
