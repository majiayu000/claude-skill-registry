---
name: abaqus-optimization
description: Configure Tosca optimization. Use when user mentions design response, objective function, optimization constraint, or SIMP penalty. Base module for topology/shape optimization.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Optimization Skill

This skill configures optimization tasks in Abaqus. It's the **base module** - for complete workflows, route to `/abaqus-topology-optimization` or `/abaqus-shape-optimization`.

## When to Use This Skill

**Route here when user mentions:**
- "design response", "objective function", "optimization constraint"
- "SIMP penalty", "material interpolation"
- Low-level optimization setup (not complete workflows)

**Route elsewhere:**
- Complete topology optimization workflow → `/abaqus-topology-optimization`
- Complete shape optimization workflow → `/abaqus-shape-optimization`
- Running the optimization → `/abaqus-job`

## Prerequisites

Before optimization setup:
1. ✅ Working static analysis that converges
2. ✅ Appropriate mesh density
3. ✅ Full Abaqus license with Tosca (not Learning Edition)

## Workflow: Setting Up Optimization

### Step 1: Understand User's Goal

Ask if unclear:
- **What to optimize?** Weight, stiffness, frequency, stress?
- **What constraints?** Volume limit, stress limit, displacement limit?
- **Manufacturing?** Casting (draw direction), additive (min feature size)?

### Step 2: Choose Objective-Constraint Pair

| User Wants | Objective | Constraint |
|------------|-----------|------------|
| Lightest structure that's stiff enough | Minimize volume | Compliance ≤ limit |
| Stiffest structure at given weight | Minimize compliance | Volume ≤ 30% |
| Avoid resonance | Maximize frequency | Volume ≤ target |
| Reduce peak stress | Minimize max stress | Volume ≤ target |

**Most common:** Minimize compliance with volume ≤ 30%

### Step 3: Define Design Responses

Design responses are the quantities optimization tracks:

| Response | When to Use |
|----------|-------------|
| `VOLUME` | Almost always (for volume constraint) |
| `STRAIN_ENERGY` | Stiffness optimization |
| `EIGENFREQUENCY` | Vibration/resonance |
| `STRESS` | Stress-constrained design |
| `DISPLACEMENT` | Deflection limit |

### Step 4: Set Objective Function

The objective is what gets optimized:
- `MINIMIZE_MAXIMUM` - For compliance, stress
- `MAXIMIZE_MINIMUM` - For frequency

### Step 5: Add Constraints

Constraints limit the design space:
- `RELATIVE_LESS_THAN_EQUAL` - Percentage (volume ≤ 30%)
- `ABSOLUTE_LESS_THAN_EQUAL` - Fixed value (stress ≤ 200 MPa)

### Step 6: Consider Manufacturing

| Constraint | Purpose |
|------------|---------|
| Min member size | Prevents thin, unmanufacturable features (3-5mm typical) |
| Symmetry | Mirrors design about plane |
| Draw direction | Enables mold/casting extraction |
| Overhang angle | For additive manufacturing |

### Step 7: Freeze Critical Regions

Always freeze:
- BC application regions (mounting points)
- Load application regions
- Functional surfaces (mating interfaces)

## Key Parameters

| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| SIMP penalty | 3.0 | Higher = sharper boundaries |
| Volume fraction | 0.3-0.4 | Start conservative |
| Min member size | 3× mesh size | Prevents checkerboard |
| Design cycles | 30-50 | More for complex geometry |

## Validation Checklist

After setup, verify:
- [ ] Task created with correct region
- [ ] At least one design response defined
- [ ] Objective function set
- [ ] Volume or other constraint defined
- [ ] BC/load regions frozen
- [ ] Manufacturing constraint if needed

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Checkerboard pattern | No min member size | Add `GeometricRestriction` |
| Disconnected result | Load path broken | Freeze more regions |
| Not converging | Constraint too tight | Relax volume fraction |
| "License error" | No Tosca module | Requires full Abaqus |

## Code Patterns

For actual API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
