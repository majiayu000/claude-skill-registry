---
name: abaqus-fatigue-analysis
description: Workflow for fatigue and durability analysis - cycle counting, damage accumulation, and fatigue life prediction.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
  - Skill
---

# Abaqus Fatigue Analysis Skill

Predict fatigue life from FEA stress results using S-N curves and damage accumulation.

## When to Use This Skill

**Route here when user mentions:**
- "fatigue", "how many cycles", "fatigue life"
- "durability", "S-N curve", "cycles to failure"
- "rainflow counting", "Miner's rule"
- "high-cycle fatigue", "low-cycle fatigue"

**Route elsewhere:**
- Just stress analysis → `/abaqus-static-analysis`
- Crack propagation → specialized fracture tools
- Static strength check → `/abaqus-static-analysis`

## Important: Abaqus Fatigue Limitations

Abaqus has **limited native fatigue** capabilities. The typical workflow is:

1. Run structural analysis in Abaqus (stress/strain results)
2. Extract stress history from ODB
3. Apply fatigue criteria externally (Basquin, Miner's rule)

For full fatigue analysis, consider external tools: **fe-safe**, **nCode**, **FEMFAT**.

## Prerequisites

Before fatigue analysis:
1. ✅ Completed static or dynamic analysis with converged results
2. ✅ Material fatigue data (S-N curve or Coffin-Manson parameters)
3. ✅ Stress output at critical locations

## Workflow Steps

### Step 1: Run Stress Analysis

Use `/abaqus-static-analysis` for constant loads or `/abaqus-dynamic-analysis` for time-varying.

Ensure output requests include:
- `S` - Stress components (principal, Mises)
- `E` - Strain components
- `PEEQ` - Equivalent plastic strain (for low-cycle)

### Step 2: Identify Critical Location

Find the maximum stress location:
- Use `/abaqus-odb` to extract peak stress
- Check stress concentrations (fillets, holes, notches)
- Consider fatigue notch factor (Kf) vs stress concentration (Kt)

### Step 3: Extract Stress History

For constant amplitude: single max/min stress values.
For variable amplitude: full stress-time history for rainflow counting.

### Step 4: Apply Fatigue Criteria

Use appropriate method based on loading and life regime.

### Step 5: Calculate Life and Damage

Apply Basquin equation for life, Miner's rule for cumulative damage.

## Key Decisions

### Fatigue Approach

| Approach | When to Use | Data Needed |
|----------|-------------|-------------|
| Stress-life (S-N) | High-cycle (N > 10^4) | S-N curve |
| Strain-life (e-N) | Low-cycle (N < 10^4) | Coffin-Manson params |
| Fracture mechanics | Crack growth | da/dN curve |

### Loading Type

| Loading | Analysis Method |
|---------|-----------------|
| Constant amplitude | Single static analysis |
| Variable amplitude | Multiple loads + rainflow |
| Proportional | Single load case |
| Non-proportional | Critical plane method |

### Mean Stress Correction

| Method | Use Case |
|--------|----------|
| Goodman | Conservative, tensile mean |
| Gerber | Less conservative |
| Soderberg | Very conservative |
| SWT | Strain-life with mean stress |

## What to Ask the User

If unclear, ask:
- **Material fatigue properties?** S-N curve coefficients or test data?
- **Loading type?** Constant amplitude or variable (spectrum)?
- **Mean stress?** Fully reversed (R=-1) or with mean stress (R=0)?
- **Critical location known?** Or need to find max stress?
- **Life target?** What's the required number of cycles?

## Key Parameters

| Parameter | Typical Values | Notes |
|-----------|----------------|-------|
| S-N slope (b) | 0.08-0.15 | Lower = longer life |
| Endurance limit | 40-50% UTS (steel) | Stress below which infinite life |
| Fatigue notch factor (Kf) | 1.0-3.0 | Kf = 1 + q(Kt-1) |
| Notch sensitivity (q) | 0.7-0.95 | Higher for stronger steels |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Unrealistically short life | Stress singularity | Use Kf correction, refine mesh away from singularity |
| Wrong units | MPa vs Pa mismatch | Verify stress units match S-N data |
| Unconservative prediction | Missing mean stress | Apply Goodman/Gerber correction |
| Very long calculated life | Stress below endurance limit | Check if stress > endurance limit |

## Related Skills

- `/abaqus-static-analysis` - Base stress analysis
- `/abaqus-dynamic-analysis` - Time-varying loading
- `/abaqus-amplitude` - Cyclic loading definition
- `/abaqus-odb` - Extract stress history from results

## Code Patterns

For API syntax, equations, and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
