---
name: lambert-jl
description: Develop and maintain Lambert.jl, a Julia library implementing multiple algorithms for solving Lambert's problem. Use when working on Lambert.jl, adding new solvers, computing orbital transfers, or generating porkchop plots.
---

# Lambert.jl

Julia library for solving Lambert's problem (two-position, time-of-flight orbital boundary value problem). Repo: [HAMMERHEAD-Space/Lambert.jl](https://github.com/HAMMERHEAD-Space/Lambert.jl)

## Architecture

### Solver Hierarchy
```
AbstractLambertSolver <: SciMLBase.AbstractSciMLAlgorithm
├── GoodingSolver      # Gooding 1990 - robust, accurate
├── IzzoSolver         # Izzo 2015 - very fast
├── ValladoSolver      # Vallado 2013 - guaranteed convergence (bisection)
├── AroraSolver        # Arora 2013 - fast cosine transformation
├── BattinSolver       # Battin 1984 - handles 180° singularity
├── GaussSolver        # Gauss 1809 - historical, limited accuracy
└── AvanziniSolver     # Avanzini 2008 - eccentricity-based, single rev
```

### Problem Types
```
AbstractAstroProblem <: SciMLBase.AbstractSciMLProblem
└── LambertProblem     # (μ, r1, r2, tof)

LambertSolution        # (v1, v2, numiter, retcode)
LambertIterator        # Stateful iterator for solve!
```

### Source Layout
```
src/
  Lambert.jl            # Module, imports SciMLBase.solve/remake/init/solve!
  lambert_problem.jl    # LambertProblem, LambertSolution, LambertIterator
  utils.jl              # Stumpff functions, geometry, normalization, Lagrange coefficients
  porkchop.jl           # PorkchopGrid, porkchop_grid() with EnsembleProblem
  {solver_name}_solver.jl  # One file per solver algorithm
ext/
  LambertPlotsExt.jl    # Weak dep for porkchop plot visualization
```

## Key Patterns

### SciML Interface
```julia
# Object-oriented (recommended)
prob = LambertProblem(μ, r1, r2, tof)
sol = solve(prob, GoodingSolver())
# sol.v1, sol.v2, sol.numiter, sol.retcode

# Remake for parameter sweeps
prob2 = remake(prob; tof=new_tof)
```

### Direct Function Call
```julia
v1, v2, numiter, converged = gooding1990(μ, r1, r2, tof; M=0, prograde=true)
```

### Solver Configuration
Solvers use `@with_kw` for keyword defaults:
```julia
@with_kw struct GoodingSolver <: AbstractLambertSolver
    M::Int = 0             # Number of complete revolutions
    prograde::Bool = true  # Prograde transfer
    low_path::Bool = true  # Low-energy path (multi-rev)
    maxiter::Int = 35
    atol::Float64 = 1e-5
    rtol::Float64 = 1e-7
end
```

### Porkchop Grids
```julia
grid = porkchop_grid(μ, r1_func, r2_func, dep_dates, arr_dates, solver;
    ensemble_method=EnsembleThreads())
```
Uses `SciMLBase.EnsembleProblem` for parallel grid evaluation.

### Return Codes
`:SUCCESS`, `:MAXIMUM_ITERATIONS`, `:COLLINEAR_VECTORS`, `:NEGATIVE_TOF`

### AstroCoords Integration
`LambertProblem` accepts any `AstroCoord` for positions -- auto-converts to Cartesian.

### Heuristic Algorithm Selection
`select_lambert_algorithm()` chooses optimal solver based on transfer angle and revolution count.

## Adding a New Solver

1. Create `src/newsolver_solver.jl`
2. Define `@with_kw struct NewSolver <: AbstractLambertSolver` with config fields
3. Implement `SciMLBase.solve(prob::LambertProblem, alg::NewSolver)`
4. Implement direct function `newsolver(μ, r1, r2, tof; kwargs...)`
5. Add to `ALL_SOLVERS` test constant
6. Test against reference solutions (Vallado, Curtis, Battin textbooks)
7. Add `@check_allocs` test (if allocation-free)

## Dependencies
- `AstroCoords` 0.3, `SciMLBase` 2.67, `Parameters` 0.12
- `Roots` 2.2 (root-finding for some solvers)
- `StaticArraysCore` 1.4
- Weak dep: `Plots` 1.40 (porkchop visualization extension)
