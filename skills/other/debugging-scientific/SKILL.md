---
name: debugging-scientific
description: Systematic debugging for numerical and scientific Julia code. Use when encountering wrong results, NaN/Inf values, numerical instability, AD failures, allocation regressions, type instabilities, or unexpected solver behavior.
---

# Debugging Scientific Julia Code

## Purpose

Systematic approach to diagnosing issues in numerical/scientific code where bugs often manifest as subtly wrong answers rather than crashes.

## Common Failure Modes

| Symptom | Likely Causes |
|---------|---------------|
| NaN/Inf in output | Division by zero, sqrt of negative, log of zero, norm of zero vector |
| Slowly diverging results | Numerical instability, wrong frame, accumulated truncation error |
| Sudden jump in state | Units mismatch (m vs km, deg vs rad), sign error, wrong epoch |
| AD returns NaN gradient | Mutation in tracked path, branch on float, norm(zero_vec) |
| Solver fails to converge | Stiff problem with non-stiff solver, tolerances too loose, bad initial state |
| Allocations in hot path | Captured variable in closure, non-concrete type, dynamic dispatch |
| Wrong but plausible answer | Off-by-one in index, transposed matrix, wrong convention (TA vs MA) |

## Diagnostic Process

### 1. Reproduce and Isolate

- Create a minimal reproducing example
- Fix random seeds if stochastic components exist
- Record exact inputs: state vector, epoch, parameters, solver settings
- Compare against a known-good reference (analytical solution, textbook, GMAT/STK)

### 2. Check the Basics First

Before deep debugging, verify:
- **Units**: Are inputs in expected units? (km not m, radians not degrees)
- **Frames**: Is everything in the same reference frame? (J2000 ECI vs ECEF vs body-fixed)
- **Epoch**: Is the Julian Date correct? Is time elapsed in seconds?
- **Signs**: Velocity direction, angular conventions, coordinate handedness
- **Indices**: Is the state vector `[r; v]` or `[v; r]`? 1-indexed correctly?

### 3. Numerical Diagnostics

```julia
# Check for NaN/Inf propagation
any(isnan, result) || any(isinf, result)

# Check type stability
@code_warntype my_function(args...)

# Check allocations
@allocated my_function(args...)

# Check energy conservation (Keplerian)
E_initial = orbitalNRG(state_initial, μ)
E_final = orbitalNRG(state_final, μ)
@test E_initial ≈ E_final rtol=1e-10

# Step through integration to find divergence point
sol = solve(prob, solver; saveat=small_dt)
plot(sol.t, [norm(sol.u[i][1:3]) for i in eachindex(sol.u)])
```

### 4. AD-Specific Debugging

If AD is failing:
- Test the function with `ForwardDiff.jacobian` on a simple input first
- Check for array mutation: `x[i] = ...` breaks reverse-mode AD
- Check for branching: `if x > threshold` creates non-smooth gradients
- Check norm-near-zero: `normalize(v)` when `v ≈ [0,0,0]` gives NaN
- Compare AD result against `FiniteDiff.finite_difference_jacobian`
- Try different backends to isolate backend-specific vs code issues

### 5. Bisect the Problem

- For propagation: compare at intermediate times, not just final state
- For force models: test each perturbation in isolation, then combined
- For coordinate transforms: verify round-trip `A -> B -> A ≈ identity`
- For optimizers: check objective value and constraints at each iteration

## Resolution Checklist

After finding and fixing the bug:
- [ ] Root cause is understood (not just symptom suppressed)
- [ ] Fix is verified against the original failing case
- [ ] Regression test added to prevent recurrence
- [ ] No new allocations or type instabilities introduced
- [ ] AD still works after the fix
