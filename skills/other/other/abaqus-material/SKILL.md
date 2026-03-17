---
name: abaqus-material
description: Define material properties for FEA models. Use when user mentions steel, aluminum, Young's modulus, elastic, plastic, density, or asks about material properties.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Material Skill

Define material properties and assign sections to parts. This skill handles elastic, plastic, thermal, and composite material definitions.

## When to Use This Skill

**Route here when user mentions:**
- "steel", "aluminum", "titanium", or other material names
- "Young's modulus", "elastic", "Poisson's ratio"
- "plastic", "yielding", "hardening"
- "density" for gravity/dynamics
- "thermal conductivity", "expansion"
- "assign material to part"

**Route elsewhere:**
- Contact properties (friction, damping) → `/abaqus-interaction`
- Optimization material interpolation → `/abaqus-optimization`
- Temperature boundary conditions → `/abaqus-field`

## Key Decisions

### 1. What Properties Are Needed?

| Analysis Type | Required | Optional |
|--------------|----------|----------|
| Static stress | E, ν | - |
| Static with gravity | E, ν, ρ | - |
| Yielding/plastic | E, ν, σy | ρ |
| Modal/frequency | E, ν, ρ | - |
| Dynamic explicit | E, ν, ρ | Plasticity |
| Thermal stress | E, ν, α | k, cp |
| Heat transfer only | k | cp, ρ |

**Key insight:** Density (ρ) is required whenever inertia matters - modal analysis, dynamics, gravity loads.

### 2. Common Material Values

| Material | E (MPa) | ν | ρ (t/mm³) | σy (MPa) |
|----------|---------|---|-----------|----------|
| Steel (mild) | 210000 | 0.30 | 7.85e-9 | 250 |
| Steel (high-strength) | 210000 | 0.30 | 7.85e-9 | 550 |
| Stainless 304 | 193000 | 0.29 | 8.00e-9 | 215 |
| Aluminum 6061-T6 | 68900 | 0.33 | 2.70e-9 | 276 |
| Aluminum 7075-T6 | 71700 | 0.33 | 2.81e-9 | 503 |
| Titanium Ti-6Al-4V | 113800 | 0.34 | 4.43e-9 | 880 |

**Unit system:** mm-tonne-s-N-MPa (consistent SI)

### 3. Section Type Selection

| Geometry Type | Section Type | When to Use |
|--------------|--------------|-------------|
| 3D solid (hex/tet) | HomogeneousSolidSection | Most FEA models |
| Thin walls (t/L < 0.1) | HomogeneousShellSection | Plates, sheet metal |
| Slender members (L/d > 10) | BeamSection | Frames, trusses |
| Layered composites | CompositeShellSection | Carbon fiber, laminates |

## What to Ask User

If unclear, ask:
- **What material?** Steel, aluminum, custom values?
- **Need plasticity?** Will stresses exceed yield?
- **Need density?** Is this for dynamics, modal, or gravity?
- **Temperature effects?** Thermal expansion, temperature-dependent properties?

## Workflow

### Step 1: Create Material
Create a material object with a descriptive name.

### Step 2: Add Required Properties
At minimum, add elastic properties (E, ν). Add density if analysis requires it.

### Step 3: Add Optional Properties
Add plasticity, thermal, or other properties as needed.

### Step 4: Create Section
Create appropriate section type (solid, shell, beam) referencing the material.

### Step 5: Assign Section to Part
Assign section to all cells/faces that need this material.

## Validation Checklist

Before running analysis, verify:
- [ ] E > 0 (positive stiffness)
- [ ] -1 < ν < 0.5 (ν = 0.5 causes numerical issues)
- [ ] ρ > 0 if required for analysis type
- [ ] Plastic table starts at zero plastic strain
- [ ] Section assigned to ALL cells that need it

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| "Material has no density" | Analysis requires density | Add density property |
| "Negative eigenvalue in stiffness" | Invalid Poisson's ratio | Ensure -1 < ν < 0.5 |
| "Section not assigned" | Missing assignment call | Assign section to region |
| "Material X not found" | Typo in material name | Check spelling matches |
| "Region has no mesh" | Mesh order issue | Mesh after section assignment |

## Code Patterns

For actual API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Materials Database](references/materials-database.md)
- [Troubleshooting Guide](references/troubleshooting.md)
