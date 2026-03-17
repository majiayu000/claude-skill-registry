---
name: simsflanagan-jl
description: Develop and maintain SimsFlanagan.jl, a Julia library for low-thrust trajectory optimization using the Sims-Flanagan transcription method. Use when working on SimsFlanagan.jl, designing low-thrust transfers, or optimizing trajectory segments with impulsive delta-V.
---

# SimsFlanagan.jl

Julia implementation of the Sims-Flanagan transcription method for low-thrust trajectory optimization. Repo: [HAMMERHEAD-Space/SimsFlanagan.jl](https://github.com/HAMMERHEAD-Space/SimsFlanagan.jl)

## Architecture

### Spacecraft Types
```
AbstractSpacecraft
├── Spacecraft            # Constant thrust
├── SEPSpacecraft         # Solar electric propulsion (1/r^2 thrust scaling)
└── SolarSail             # Solar sail (radiation pressure)
```

### Problem/Solution Types
```
SimsFlanaganProblem       # Problem definition (SciML pattern)
SimsFlanaganSolution      # Optimized trajectory result
```

### Initial Guess Strategies
```
AbstractInitialGuess
├── RandomGuess           # Random throttle vectors
├── ZeroGuess             # Zero thrust (ballistic)
├── ConstantGuess         # Constant throttle direction
├── RadialGuess           # Radial thrust direction
└── LambertGuess          # Lambert arc-based initialization
```

### Source Layout
```
src/
  SimsFlanagan.jl         # Module entry
  types.jl                # All type definitions
  problem.jl              # simsflanagan_problem() construction
  propagation.jl          # Kepler propagation, segment/leg propagation, mismatch
  solve.jl                # solve() via MadNLP optimizer
  utils.jl                # safe_norm (AD-safe), utilities
```

## Key Patterns

### SciML Interface
```julia
# Create problem
prob = simsflanagan_problem(r0, v0, rf, vf, tof, μ, spacecraft; kwargs...)

# Solve
sol = solve(prob; kwargs...)

# Remake for different parameters
prob2 = remake(prob; tof=new_tof)
```

### Solution Accessors
```julia
position_mismatch(sol)     # Match-point position error
velocity_mismatch(sol)     # Match-point velocity error
mass_mismatch(sol)         # Mass continuity error
```

### Optimization Stack
- **MadNLP** interior-point NLP solver with MUMPS linear solver
- **ForwardDiff** for gradient computation
- **Optimization.jl** unified interface via OptimizationMOI bridge

### Trajectory Discretization
- Splits trajectory into forward/backward legs from match point
- Each segment has impulsive delta-V at midpoint (`SVector{3}` throttle)
- Sundman transformation for adaptive segment sizing based on orbital distance

### AD-Safe Utilities
```julia
safe_norm(v)  # Handles zero vector without NaN gradients
```

### Lambert-Based Initialization
Uses `Lambert.jl` to compute initial guess from Lambert arcs, providing better convergence than random initialization.

## Adding a New Spacecraft Model

1. Define `struct NewCraft <: AbstractSpacecraft` with propulsion parameters
2. Implement thrust computation method (how thrust scales with position/state)
3. Add dispatch in propagation for the new thrust model
4. Add initial guess compatibility
5. Test: convergence on known transfer, AD gradient correctness

## Dependencies
- `AstroCoords` 0.3, `Lambert` 0.1, `SciMLBase` 2, `StaticArrays` 1.9
- `ForwardDiff` 1.3 (AD for optimization gradients)
- `MadNLP` 0.8, `MadNLPMumps` 0.5 (interior-point NLP solver)
- `Optimization` 5, `OptimizationMOI` 1, `OptimizationMadNLP` 1
