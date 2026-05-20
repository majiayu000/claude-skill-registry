---
name: qlaw-jl
description: Develop and maintain QLaw.jl, a Julia library for Q-Law Lyapunov-based low-thrust guidance. Use when working on QLaw.jl, designing low-thrust orbit transfers, tuning Q-Law weights, or implementing feedback control for orbital maneuvering.
---

# QLaw.jl

Julia implementation of the Q-Law Lyapunov-based feedback control law for low-thrust orbit transfers. Repo: [HAMMERHEAD-Space/QLaw.jl](https://github.com/HAMMERHEAD-Space/QLaw.jl)

## Architecture

### Spacecraft Types
```
QLawSpacecraft            # Constant thrust (dry, wet, thrust, isp)
SEPQLawSpacecraft         # Solar electric (+ r_ref for 1/r^2 scaling)
```

### Control Types
```
# Effectivity (coasting logic)
AbsoluteEffectivity       # Coast when absolute effectivity < threshold
RelativeEffectivity       # Coast when relative effectivity < threshold

# Convergence criteria
SummedErrorConvergence    # Sum of weighted element errors
MaxElementConvergence     # Maximum individual element error
VargaConvergence          # Varga's convergence metric
```

### Problem/Solution Types
```
QLawParameters            # Algorithm configuration (smoothing, tolerances)
QLawWeights               # Element weights for proximity quotient Q
QLawProblem               # Problem definition (SciML pattern)
QLawSolution              # Transfer result (converged, time, mass, trajectory)
```

### Source Layout
```
src/
  QLaw.jl                # Module entry
  types.jl               # All type definitions
  api.jl                 # qlaw_problem(), solve(), remake()
  qlaw_core.jl           # Q function, optimal thrust angles (α*, β*), effectivity
  dynamics.jl            # ODE RHS: Gauss VE in modified equinoctial elements
```

## Key Patterns

### SciML Interface
```julia
# Define transfer
prob = qlaw_problem(oe0, oeT, tspan, μ, spacecraft;
    weights=QLawWeights(...),
    qlaw_params=QLawParameters(...))

# Solve
sol = solve(prob)

# Remake
prob2 = remake(prob; spacecraft=new_spacecraft)
```

### Modified Equinoctial Elements
Q-Law operates in modified equinoctial elements `[p, f, g, h, k, L]`:
```julia
oe0 = ModEq(kep_initial, μ)   # Convert from Keplerian via AstroCoords
oeT = ModEq(kep_target, μ)
```

### Q-Law Core Math
- **Proximity quotient Q**: Weighted sum of squared element errors, penalized near singularities
- **Optimal thrust angles**: `α*` (in-plane) and `β*` (out-of-plane) computed via ForwardDiff of dQ/doe
- **Effectivity**: Measures how efficiently current thrust reduces Q; used for coasting decisions
- **Smooth activations**: `tanh` for AD-compatible coasting thresholds

### Weight Optimization
```julia
# Global optimization via BlackBoxOptim
# Local optimization via SAMIN (Optim.jl)
# Both through Optimization.jl unified interface
```

### Perturbation Support
Integrates with AstroForceModels.jl for:
- J2+ gravity harmonics
- Third-body perturbations (Moon, Sun)
- Eclipse/shadow modeling

### Integration with Ecosystem
- **AstroCoords**: Coordinate conversions (Keplerian <-> ModEq)
- **AstroPropagators**: ODE integration infrastructure
- **AstroForceModels**: Perturbation force models
- **ComponentArrays**: Named state vectors

## Adding New Features

### New Convergence Criterion
1. Define `struct NewConvergence` type
2. Implement convergence check dispatch
3. Test on known reference transfers

### New Effectivity Model
1. Define effectivity type struct
2. Implement smooth (AD-compatible) effectivity computation
3. Verify ForwardDiff compatibility

## Dependencies
- `AstroCoords` 0.3, `AstroForceModels` 0.3, `AstroPropagators` 0.2
- `ComponentArrays` 0.15, `ForwardDiff` 1, `StaticArrays` 1
- `Optim` 2 (local optimization for weight tuning)
- `OrdinaryDiffEqAdamsBashforthMoulton` 1.5, `OrdinaryDiffEqCore` 1
- `SciMLBase` 2
