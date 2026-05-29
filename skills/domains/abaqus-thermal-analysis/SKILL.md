---
name: abaqus-thermal-analysis
description: Complete workflow for heat transfer analysis - steady-state and transient thermal. Use when user asks about temperature distribution, conduction, convection, or heat flow.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
  - Skill
---

# Abaqus Thermal Analysis Workflow

Heat transfer analysis for steady-state or transient temperature distribution. Use when user needs temperature field without mechanical stress.

## When to Use This Skill

**Route here when user mentions:**
- "Heat transfer analysis", "temperature distribution"
- "How hot will it get?", "thermal analysis"
- "Conduction", "convection", "radiation"
- "Heat sink design", "cooling analysis"
- "Steady-state temperature", "transient heating/cooling"

**Route elsewhere:**
- Thermal stress (temperature causing deformation) → `/abaqus-coupled-analysis`
- Just stress analysis → `/abaqus-static-analysis`
- Temperature as initial condition only → `/abaqus-field`

## Prerequisites

Before thermal analysis:
1. Geometry defined
2. Thermal conductivity (k) - required for all thermal analysis
3. For transient: also need density (ρ) and specific heat (cp)

## Workflow: Thermal Analysis

### Step 1: Understand User's Goal

Ask if unclear:
- **Steady-state or transient?** Final equilibrium vs temperature over time?
- **Boundary temperatures?** Fixed temperature surfaces?
- **Convection?** Film coefficient and ambient temperature?
- **Heat sources?** Applied heat flux or internal heat generation?

### Step 2: Choose Analysis Type

| User Wants | Analysis Type |
|------------|---------------|
| Final equilibrium temperature | STEADY_STATE |
| Temperature vs time history | TRANSIENT |
| Cool-down or heat-up time | TRANSIENT |
| Just the end result | STEADY_STATE |

**Decision rule:** Use steady-state unless user needs temperature history or time-dependent behavior.

### Step 3: Define Thermal Material Properties

| Property | Required For | Units (SI-mm) |
|----------|--------------|---------------|
| Conductivity (k) | All thermal | mW/(mm·K) |
| Specific heat (cp) | Transient | mJ/(tonne·K) |
| Density (ρ) | Transient | tonne/mm³ |

**Common materials (SI-mm units):**

| Material | k | cp | ρ |
|----------|---|----|----|
| Steel | 50 | 5.0e11 | 7.85e-9 |
| Aluminum | 167 | 9.0e11 | 2.70e-9 |
| Copper | 385 | 3.85e11 | 8.96e-9 |

### Step 4: Apply Thermal Boundary Conditions

| BC Type | Use For | Required Inputs |
|---------|---------|-----------------|
| TemperatureBC | Fixed temperature surface | Temperature value |
| FilmCondition | Convection to ambient | Film coeff, sink temp |
| SurfaceHeatFlux | Heat input | Flux magnitude (mW/mm²) |
| RadiationToAmbient | Radiation cooling | Emissivity, ambient temp |
| BodyHeatFlux | Internal heat generation | Volumetric heat rate |

**Minimum requirement:** At least one temperature BC or heat flux boundary.

### Step 5: Create Heat Transfer Step

| Parameter | Steady-State | Transient |
|-----------|--------------|-----------|
| response | STEADY_STATE | TRANSIENT |
| timePeriod | 1.0 (arbitrary) | Actual duration (s) |
| initialInc | - | Start increment |
| maxInc | - | Largest allowed increment |
| deltmx | - | Max temp change per increment |

### Step 6: Mesh with Heat Transfer Elements

| Element | Use |
|---------|-----|
| DC3D8 | Standard 8-node hex (recommended) |
| DC3D4 | 4-node tet (for complex geometry) |
| DC3D20 | 20-node hex (high accuracy) |

**Note:** Heat transfer elements (DC*) are different from structural elements (C3D*).

### Step 7: Run Analysis and Extract Results

Request these field outputs:
- **NT** - Nodal temperature
- **HFL** - Heat flux vector
- **RFL** - Reaction heat flux
- **HFLM** - Heat flux magnitude

## Validation Checklist

After analysis, verify:
- [ ] Temperature range is physically reasonable
- [ ] Heat balance: flux in ≈ flux out (steady-state)
- [ ] No unexpected hot/cold spots
- [ ] Transient: temperature stabilizes by end of analysis

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Temperature oscillation | Large increments in transient | Reduce maxInc or deltmx |
| Non-physical temperature | Unit mismatch | Verify k, cp, ρ units |
| No heat flow | Missing BC or bad region | Check boundary conditions |
| Negative temperature (Kelvin) | Bad setup | Review initial conditions |

## Related Skills

- `/abaqus-coupled-analysis` - Thermal + structural (thermomechanical)
- `/abaqus-material` - Thermal material properties
- `/abaqus-field` - Initial temperature fields

## Code Patterns

For API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
