---
name: abaqus-step
description: Define analysis steps and procedures. Use when user mentions static analysis, dynamic step, frequency analysis, heat transfer step, or asks about analysis type, time increments, or nlgeom.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Step Skill

This skill defines analysis steps and procedures in Abaqus. Steps control what physics are solved and how the solution proceeds.

## When to Use This Skill

**Route here when user mentions:**
- "static analysis", "dynamic step", "frequency analysis"
- "heat transfer step", "thermal step", "transient analysis"
- "analysis type", "time increments", "nlgeom"
- "convergence issues", "increment size", "time step"
- "multi-step analysis", "sequential loading"
- "buckling analysis", "modal analysis"
- "impact simulation", "crash analysis"

**Route elsewhere:**
- Applying boundary conditions → `/abaqus-bc`
- Applying loads → `/abaqus-load`
- Setting up optimization → `/abaqus-optimization`
- Configuring output requests → `/abaqus-output`

## Workflow: Creating Analysis Steps

### Step 1: Understand User's Physics

Ask if unclear:
- **What physics?** Stress, vibration, heat transfer, coupled?
- **Static or dynamic?** Constant load vs time-varying?
- **Linear or nonlinear?** Small or large deformations?

### Step 2: Choose Step Type

| Analysis Goal | Step Type | Key Parameter |
|---------------|-----------|---------------|
| Stress under constant load | StaticStep | nlgeom=OFF/ON |
| Natural frequencies | FrequencyStep | numEigen |
| Buckling modes | BuckleStep | numEigen |
| Transient dynamics (smooth) | ImplicitDynamicsStep | timePeriod |
| Impact/crash | ExplicitDynamicsStep | timePeriod |
| Heat conduction | HeatTransferStep | response |
| Thermal + structural | CoupledTempDisplacementStep | timePeriod |
| Harmonic response | SteadyStateDynamicsStep | frequencyRange |

**Most common:** StaticStep with nlgeom=OFF for linear stress analysis.

### Step 3: Determine Linearity

| Condition | nlgeom Setting | When |
|-----------|----------------|------|
| Small deformation, linear material | OFF | Default, fastest |
| Large rotation/displacement | ON | Thin structures, cables |
| Plasticity | ON | Material yields |
| Contact | ON | Parts touching |
| Buckling | ON | Post-buckling behavior |

### Step 4: Configure Increment Control

| Convergence Difficulty | initialInc | minInc | maxInc |
|------------------------|------------|--------|--------|
| Easy (linear) | 1.0 | 1e-6 | 1.0 |
| Moderate | 0.1 | 1e-8 | 0.2 |
| Difficult (contact, plasticity) | 0.01 | 1e-12 | 0.05 |

### Step 5: Chain Multiple Steps (if needed)

For sequential loading:
1. First step uses `previous='Initial'`
2. Subsequent steps chain from previous step name
3. Each step can have different physics or settings

## Key Parameters

| Parameter | Purpose | Typical Value |
|-----------|---------|---------------|
| timePeriod | Duration of step | 1.0 for static |
| initialInc | Starting increment size | 0.1 for nonlinear |
| maxNumInc | Maximum iterations | 100 |
| minInc | Smallest allowed increment | 1e-8 |
| maxInc | Largest allowed increment | 0.1-1.0 |
| numEigen | Modes to extract | 10 |
| deltmx | Max temp change per increment | 5.0-10.0 |

## Special Considerations

### Frequency/Modal Analysis
- Always from Initial step (no preload needed for basic modal)
- Use LANCZOS eigensolver for large models
- Extract 10-20 modes typically

### Buckling Analysis
- Usually follows a load step (to apply reference load)
- Eigenvalues are load multipliers
- First positive eigenvalue is critical

### Explicit Dynamics
- Time period should be very short (milliseconds)
- Increment size determined automatically
- Mass scaling may be needed for quasi-static problems

### Heat Transfer
- STEADY_STATE for equilibrium temperature
- TRANSIENT for time-varying temperature
- deltmx controls accuracy vs speed

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| "Too many increments" | Convergence difficulty | Reduce maxInc, increase maxNumInc |
| "Negative eigenvalues" | Unconstrained or unstable | Check BCs, add stabilization |
| "Time increment too small" | Severe nonlinearity | Add stabilization, check material |
| "Explicit time increment" | Very small elements | Use mass scaling or coarsen mesh |

## Validation Checklist

After step creation, verify:
- [ ] Step type matches analysis physics
- [ ] nlgeom setting appropriate for deformation level
- [ ] Increment control parameters reasonable
- [ ] Step chains correctly from previous
- [ ] Time period appropriate for transient analysis

## Code Patterns

For actual API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
