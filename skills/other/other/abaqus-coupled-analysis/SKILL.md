---
name: abaqus-coupled-analysis
description: Complete workflow for coupled thermomechanical analysis. Use when user mentions thermal stress, thermal expansion, or temperature causing deformation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
  - Skill
---

# Abaqus Coupled Thermomechanical Analysis Workflow

Analyze problems where temperature and mechanical response interact. Use for thermal stress, expansion-induced deformation, and high-temperature structural components.

## When to Use This Skill

**Natural language triggers:**
- "Thermal stress analysis"
- "Thermomechanical coupling"
- "Temperature causes stress/deformation"
- "Thermal expansion effects"
- "Heat causes deformation"
- "Thermal shock"
- "High temperature component"
- "Thermal gradient stress"

**Route elsewhere:**
- Heat transfer only (no stress) -> `/abaqus-thermal-analysis`
- Structural only (no thermal) -> `/abaqus-static-analysis`

## Prerequisites

Before starting coupled analysis:
1. Working thermal OR structural analysis that converges
2. Material must have BOTH thermal and mechanical properties
3. Understand whether coupling is one-way or two-way

## Workflow: Coupled Thermomechanical Analysis

### Step 1: Determine Coupling Type

Ask if unclear: "Does mechanical deformation affect the temperature field?"

| Scenario | Coupling Type | Approach |
|----------|---------------|----------|
| Heat causes stress, no feedback | One-way | Sequential coupling |
| Friction or plastic work generates heat | Two-way | Fully coupled |
| Large deformation changes heat path | Two-way | Fully coupled |
| Simple thermal expansion | One-way | Sequential is simpler |

**Decision rule:** If only temperature affects stress -> Sequential. If deformation affects temperature -> Fully coupled.

### Step 2: Define Complete Material Properties

Material must include BOTH sets:

**Mechanical:** E (Young's modulus), nu (Poisson's ratio)

**Thermal:** k (conductivity), alpha (expansion coefficient), T_ref (reference temperature)

**For transient:** Also need cp (specific heat) and rho (density)

Typical steel values (SI-mm units):
- E = 210000 MPa, nu = 0.3
- k = 50 mW/(mm*K), alpha = 12e-6 /K
- cp = 5.0e11 mJ/(tonne*K), rho = 7.85e-9 tonne/mm^3

### Step 3: Choose Analysis Type

**Fully Coupled (simultaneous):**
- Use `CoupledTempDisplacementStep`
- Response: STEADY_STATE or TRANSIENT
- Elements: C3D8T, C3D8RT, or C3D10MT (coupled elements)

**Sequential (thermal first, then structural):**
1. Run thermal analysis with `HeatTransferStep`
2. Import temperature results into structural model
3. Run structural analysis with `StaticStep`

### Step 4: Set Initial Conditions

- Define initial temperature (should match T_ref for zero initial stress)
- Thermal strain = alpha * (T - T_ref)

### Step 5: Apply Boundary Conditions

**Thermal BCs:** Temperature, heat flux, convection, or radiation

**Mechanical BCs:** Fixed supports (prevent rigid body motion)

### Step 6: Mesh with Appropriate Elements

| Element | Description | Use |
|---------|-------------|-----|
| C3D8T | 8-node coupled brick | General coupled |
| C3D8RT | Reduced integration | Faster, watch hourglassing |
| C3D10MT | 10-node tet | Complex geometry |

For sequential: Use standard thermal elements (DC3D8) then structural elements (C3D8R).

### Step 7: Request Coupled Output Variables

Key variables to request:
- S: Mechanical stress
- U: Displacement
- NT: Temperature (nodal)
- THE: Thermal strain
- E: Total strain
- EE: Elastic strain (mechanical only)

## What to Ask User

If requirements unclear, ask:
1. Is the coupling one-way (heat->stress) or two-way (mutual interaction)?
2. Steady-state or transient thermal conditions?
3. What is the reference temperature (zero thermal strain)?
4. What temperatures will be applied?
5. Are there any mechanical loads in addition to thermal effects?

## Validation Checklist

After setup, verify:
- [ ] Expansion coefficient (alpha) defined with correct T_ref
- [ ] Initial temperature matches T_ref (for zero initial stress)
- [ ] Both mechanical and thermal BCs applied
- [ ] Using coupled elements (C3D*T) for fully coupled
- [ ] Thermal strain (THE) appears in output requests

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Large/unrealistic thermal strain | Wrong alpha units | alpha should be ~1e-5/K for metals |
| Zero thermal stress | Missing Expansion property | Add material.Expansion() |
| Non-convergence | Large temperature change | Reduce time increments or deltmx |
| No thermal expansion effect | Wrong element type | Use coupled elements (C3D8T not C3D8) |
| Cannot import ODB | Path or step name wrong | Verify ODB exists and step name matches |

## Related Skills

- `/abaqus-thermal-analysis` - Thermal-only (heat transfer without stress)
- `/abaqus-static-analysis` - Structural-only (no thermal effects)
- `/abaqus-field` - Import temperature fields from external sources
- `/abaqus-material` - Material property definitions
- `/abaqus-step` - Analysis step configuration

## Code Patterns

For API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
