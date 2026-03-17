---
name: tune-mjcf
description: This skill provides guidance for optimizing MuJoCo MJCF simulation files to improve performance while maintaining physics accuracy. Use this skill when tuning simulation parameters, reducing computation time, or balancing speed vs. accuracy trade-offs in MuJoCo models.
---

# MuJoCo MJCF Tuning

## Overview

This skill provides strategies for optimizing MuJoCo MJCF simulation configurations to achieve better performance while maintaining physics accuracy. MuJoCo optimization requires understanding the distinction between different error sources and systematically exploring available parameters.

## Critical Concepts

### Error Source Distinction

Understanding the difference between these error sources is essential:

1. **Integration Discretization Error**: Caused by timestep size. Larger timesteps mean fewer integration steps, leading to trajectory divergence from the reference. This error CANNOT be compensated by solver iterations.

2. **Constraint Solver Error**: Caused by insufficient solver iterations. This affects how well contacts and constraints are resolved within each timestep. Increasing solver iterations improves constraint satisfaction but NOT integration accuracy.

**Key insight**: Solver iterations and integration accuracy are fundamentally different concepts. Increasing solver iterations will never compensate for timestep-induced discretization error.

### Integrator Behavior

Different integrators follow different mathematical trajectories:
- `Euler` (explicit): Simple but less stable at large timesteps
- `implicit` and `implicitfast`: More stable but follow different trajectories than Euler
- Switching integrators changes the physics trajectory regardless of solver precision

Matching reference results typically requires using the same integrator as the reference configuration.

## Systematic Approach

### Step 1: Establish True Baseline

Before any optimization, test the exact reference configuration:
1. Run the evaluation with the unmodified reference model
2. Record baseline timing and accuracy metrics
3. Verify the evaluation passes with reference settings
4. Document what "correct" physics behavior looks like

### Step 2: Identify Optimization Categories

MuJoCo offers multiple independent optimization categories:

**Timestep-Related** (affects integration accuracy):
- `timestep`: Simulation step size
- `integrator`: Integration method

**Solver-Related** (affects constraint resolution):
- `iterations`: Solver iteration count
- `tolerance`: Solver convergence threshold
- `solver`: Solver type (PGS, CG, Newton)
- `noslip_iterations`, `mpr_iterations`: Specialized iterations

**Computation-Related** (may not affect physics):
- `<flag>` settings (e.g., `energy`, `fwdinv`, `sensornoise`)
- Compiler options (`autolimits`, `boundmass`, etc.)
- Memory settings (`memory`, `njmax`, `nconmax`)

**Model-Specific** (affects physics fidelity):
- Contact parameters (`condim`, `margin`, `gap`)
- Body/joint parameters
- Composite element counts

### Step 3: Use Systematic Parameter Sweeps

Rather than ad-hoc trial and error, implement methodical searches:

```
For each optimization category:
  1. Identify parameter range
  2. Test boundary values first
  3. Use binary search to find acceptable threshold
  4. Document: parameter value → accuracy → timing
```

### Step 4: Early Termination Criteria

Establish clear thresholds to avoid wasted effort:
- If accuracy error exceeds X at parameter value Y, larger/more aggressive values will not work
- If a strategy fails after N systematic attempts, pivot to a different category
- Document which strategies are fundamentally limited vs. need fine-tuning

## Verification Strategies

### Structured Testing Protocol

1. **Single Parameter Changes**: Change only one parameter at a time to isolate effects
2. **Record All Results**: Maintain a log of: configuration → accuracy → timing
3. **Save Working Configurations**: Never overwrite a working configuration without backup
4. **Incremental Changes**: Make small adjustments to find optimal thresholds

### Validation Checklist

Before finalizing any configuration:
- [ ] XML syntax is valid (no truncated files)
- [ ] Accuracy requirement is met
- [ ] Performance requirement is met
- [ ] Configuration is reproducible
- [ ] No unintended side effects on physics

## Common Pitfalls

### Pitfall 1: Over-Reliance on Single Strategy

**Mistake**: Spending excessive time on timestep + solver iteration combinations after early evidence shows fundamental limitations.

**Solution**: After 5-10 systematic attempts show a strategy cannot work, pivot entirely to different optimization categories.

### Pitfall 2: Confusing Solver Iterations with Integration Accuracy

**Mistake**: Increasing solver iterations hoping to compensate for timestep-induced error.

**Solution**: Recognize that solver iterations affect constraint satisfaction, not time integration. For accuracy, keep timestep close to reference; for constraint quality, adjust solver iterations.

### Pitfall 3: Incomplete Exploration of Available Options

**Mistake**: Focusing narrowly on obvious parameters while ignoring:
- `<flag>` element options
- Compiler settings
- Memory configuration
- Contact/collision parameters

**Solution**: Read all available MuJoCo documentation sections before committing to a narrow strategy. Create a checklist of all option categories to explore.

### Pitfall 4: Not Preserving Valid Intermediate Results

**Mistake**: Continuously overwriting model.xml without saving working configurations.

**Solution**: Save each valid configuration with descriptive names (e.g., `model_70pct_speed_passing.xml`) before testing more aggressive optimizations.

### Pitfall 5: Incomplete or Invalid XML

**Mistake**: Truncated Write operations leaving invalid XML files.

**Solution**: After any file write, verify XML validity by reading the file back or attempting to parse it.

## Decision Framework

When optimizing a MuJoCo model:

```
1. Can computation flags be disabled without affecting physics?
   → Test <flag> options first (lowest risk)

2. Can memory/compiler settings improve performance?
   → Test memory and compiler options (low risk)

3. Is the model over-specified for the use case?
   → Consider contact parameters, composite counts (medium risk)

4. Can solver settings be relaxed while maintaining constraint quality?
   → Adjust iterations, tolerance (medium risk)

5. Can timestep be increased while staying accurate?
   → Only after exhausting other options (high risk for accuracy)
```

## MuJoCo Option Reference

Key `<option>` attributes to explore:
- `timestep`: Simulation timestep (default: 0.002)
- `integrator`: "Euler", "implicit", "implicitfast", "RK4"
- `iterations`: Maximum solver iterations (default: 100)
- `tolerance`: Solver tolerance (default: 1e-8)
- `solver`: "PGS", "CG", "Newton"
- `cone`: "pyramidal", "elliptic"
- `jacobian`: "dense", "sparse", "auto"

Key `<flag>` attributes:
- `energy`: Enable/disable energy computation
- `fwdinv`: Enable/disable forward/inverse dynamics
- `sensornoise`: Enable/disable sensor noise
- `constraint`: Enable/disable constraints
- `contact`: Enable/disable contacts

Key `<compiler>` attributes:
- `autolimits`: Auto-compute joint limits
- `boundmass`: Minimum mass for bodies
- `boundinertia`: Minimum inertia for bodies
