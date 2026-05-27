---
name: co2lpm
description: Validates code and provides physics reasoning for the 0-D CO2 lumped-parameter model for geothermal reservoirs. Use when modifying ODE solvers, parameter classes, emissions calculations, or concentration dynamics. Also use when debugging simulation behavior, explaining physics concepts, or planning changes to physics-related code.
allowed-tools: Read, Grep, Glob, Bash
---

# CO2 Lumped Parameter Model Physics Knowledge

This skill provides physics knowledge for the 0-D CO2 lumped-parameter model implemented in the `co2lpm` package.

## When This Skill Applies

- Modifying code that implements concentration evolution equations
- Changing ODE solver logic or state variable handling
- Implementing or modifying emissions partitioning (field, plant, degassing)
- Debugging unexpected simulation behavior
- Planning changes to physics-related code
- Explaining why the model behaves a certain way
- Working with pressure reversal scenarios

## Core Physics Reference

The model tracks reservoir CO2 concentration over time during geothermal extraction. Key state variables:

| Variable | Symbol | Meaning | Units |
|----------|--------|---------|-------|
| Pressure | P(t) | Reservoir pressure (relative to hydrostatic) | Pa |
| Concentration | C(t) | CO2 mass fraction in reservoir fluid | kg/kg |
| Upflow rate | q_up | Mass rate into reservoir from depth | kg/s |
| Outflow rate | q_out | Mass rate leaving reservoir to surface | kg/s |

For detailed equations, see [EQUATIONS.md](EQUATIONS.md).
For symbol definitions and units, see [SYMBOLS.md](SYMBOLS.md).
For derivation logic, see [DERIVATIONS.md](DERIVATIONS.md).
For edge cases and sanity checks, see [SANITY_CHECKS.md](SANITY_CHECKS.md).

---

## Workflow A: Physics Validation

Use this workflow when reviewing or planning code changes.

### Step 1: Identify affected equations

Determine which equations from [EQUATIONS.md](EQUATIONS.md) are affected by the change:
- Pressure evolution: E1 (exponential pressure decline)
- Concentration ODE: E2-E4 (with and without delay)
- Emissions: E5-E8 (degassing, field, plant, total)
- Solubility: E9-E10

### Step 2: Check dimensional consistency

Using [SYMBOLS.md](SYMBOLS.md), verify that:
- All terms in an equation have matching units
- ODE coefficients (alpha, beta, gamma, delta) have correct units
- Source terms have correct rate units (kg/s for mass)

### Step 3: Verify mass balance

Changes must preserve:
- CO2 mass conservation in the reservoir
- Correct partitioning between dissolved, degassed, and emitted CO2

### Step 4: Check sanity conditions

Verify the change doesn't violate sanity checks S1-S5 in [SANITY_CHECKS.md](SANITY_CHECKS.md).

### Step 5: Report findings

Summarize:
- Which equations are affected
- Any dimensional inconsistencies found
- Any mass balance violations
- Any sanity check concerns
- Recommendations for correction

---

## Workflow B: Physics Reasoning

Use this workflow when explaining behavior, debugging, or proposing solutions.

### For explaining physics concepts:

1. Identify the relevant equations and parameters
2. State the physical interpretation
3. Explain cause-and-effect relationships between variables
4. Use the derivation steps from [DERIVATIONS.md](DERIVATIONS.md) to show how equations connect

### For debugging simulation issues:

1. Identify which state variables are behaving unexpectedly
2. Check if the issue relates to:
   - Pressure reversal (q_eff > q_0c)
   - Delay effects (tau > 0)
   - Solubility limiting (degas=True)
   - ODE coefficient calculation
3. Trace through the analytical solution (gamma_exact or Cf_dde)
4. Check edge cases against [SANITY_CHECKS.md](SANITY_CHECKS.md)

### For proposing physics-consistent changes:

1. Identify which equations are affected
2. Show how new terms integrate into the ODE system
3. Demonstrate that mass balance remains satisfied
4. Identify any new sanity checks needed

---

## Quick Reference: Module Structure

| Module | Purpose | Key Functions/Classes |
|--------|---------|----------------------|
| `model.py` | Core LPM class | `LumpedParameterModel`, `StateArrays` |
| `parameters.py` | Dataclasses for inputs | `ReservoirParams`, `OperationParams`, `ChemistryParams` |
| `solvers.py` | ODE/DDE solvers | `pressure_exp`, `integrate_ode`, `dde_solve` |
| `postproc.py` | Emissions calculation | `emissions()` |
| `utils.py` | CO2 solubility | `solubility_linear`, `solubility_slope_vs_T` |
| `scenarios.py` | Preset configurations | `high_gas()`, `low_gas()`, `delay_demo()` |

---

## Key Physical Constraints

These must always hold:

1. **Concentration non-negative**: C(t) >= 0
2. **Solubility limit**: C(t) <= C_s(P) when degas=True
3. **Pressure reversal**: Occurs when q_eff > q_0c (extraction exceeds critical rate)
4. **Steady state exists**: C_inf = alpha/beta (no delay) or alpha/(beta-gamma) (with delay)
5. **Delay stability**: For tau > 0, the characteristic root lambda_1 must have negative real part

---

## Scenario Classification

| Scenario | Key Parameters | Behavior |
|----------|---------------|----------|
| High-gas (Ohaaki-like) | degas=True, high C0 | Solubility-limited, significant degassing |
| Low-gas (Wairakei-like) | degas=False, low C0 | No degassing, concentration dilutes |
| Concentrating | fC < critical | CO2 accumulates in reservoir |
| Diluting | fC > critical | CO2 decreases in reservoir |
| Reversal | fq*q0 > q0c | Outflow reverses direction |
| Delay | tau > 0 | Breakthrough lag, DDE dynamics |
