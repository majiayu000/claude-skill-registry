---
name: abaqus-field
description: Define initial conditions and predefined fields. Use when user mentions initial temperature, pre-stress, residual stress, or import from previous analysis.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Field Skill

This skill defines initial conditions and predefined fields in Abaqus. Use it to set starting states or import results from previous analyses.

## When to Use This Skill

**Route here when user mentions:**
- "initial temperature", "starting temperature", "the part starts at..."
- "pre-stress", "residual stress", "initial stress"
- "initial velocity" (for impact/explicit dynamics)
- "import temperature from thermal analysis"
- "transfer results from previous analysis"
- "bolt pre-tension", "bolt preload"

**Route elsewhere:**
- Fixed temperature boundary conditions → `/abaqus-bc`
- Heat flux, convection, radiation loads → `/abaqus-load`
- Time-varying fields via amplitude → `/abaqus-amplitude`

## Key Decisions

### Field Type Selection

| User Need | Field Type | Typical Use |
|-----------|------------|-------------|
| Starting temperature | Temperature | Thermal stress from uniform T |
| Residual stress | Stress | Pre-stressed members |
| Impact velocity | Velocity | Explicit dynamics |
| From other analysis | Predefined Temperature | Sequential thermal-structural |
| Custom variable | Predefined Field | User-defined behaviors |

### Distribution Type

| Type | When to Use |
|------|-------------|
| UNIFORM | Same value everywhere |
| FROM_FILE | Import from ODB or FIL |
| ANALYTICAL_FIELD | Expression-based (X, Y, Z) |
| USER_DEFINED | Via user subroutine |

## What to Ask User

If information is missing, ask:
1. **What initial condition?** Temperature, stress, velocity, or custom field?
2. **Uniform or varying?** Same value everywhere or position-dependent?
3. **Import from ODB?** If transferring, which file/step/frame?
4. **Region?** Entire model or specific region?
5. **Value(s)?** Magnitude, stress components, or velocity vector?

## Workflow: Setting Up Fields

### Step 1: Identify Field Type
Match user request to field type:
- Temperature values → Temperature field
- Stress state → Stress field
- Moving parts → Velocity field
- Previous analysis results → FROM_FILE distribution

### Step 2: Define Region
Determine where the field applies:
- Entire model (assembly set)
- Specific part instance
- Element set or node set

### Step 3: Set Values or Import
For uniform fields: specify single magnitude or component values.
For imported fields: ODB path, step name, increment number.

### Step 4: Verify Step
Initial conditions use `createStepName='Initial'`.
Predefined fields in analysis steps use the step name.

## Sequential Thermal-Structural Workflow

1. Run thermal analysis, save ODB
2. Import temperature as predefined field in structural model
3. Temperature causes thermal strain (requires expansion coefficient)

## Key Parameters

| Parameter | Notes |
|-----------|-------|
| `createStepName` | 'Initial' for initial conditions, step name for predefined |
| `distributionType` | UNIFORM, FROM_FILE, ANALYTICAL_FIELD |
| `fileName` | ODB path for FROM_FILE distribution |
| `beginStep/endStep` | Frame selection for ODB import |

## Validation Checklist

- [ ] Correct field type for the physics
- [ ] Region covers intended elements/nodes
- [ ] Step name is correct (Initial vs analysis step)
- [ ] For FROM_FILE: ODB exists and contains required data
- [ ] For thermal stress: material has expansion coefficient

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Field not applied | Wrong region or step | Verify region covers elements |
| Cannot read from ODB | ODB locked or wrong path | Close other sessions, check path |
| Temperature mismatch | Mesh incompatibility | Use mapping tolerance options |
| Stress equilibrium error | Stress not self-equilibrating | Review stress field consistency |

## Code Patterns

For API syntax and code examples, see `references/` folder.
