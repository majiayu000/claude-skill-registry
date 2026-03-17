# Gay Monte Carlo Measurements

---
name: gay-monte-carlo
description: Monte Carlo uncertainty propagation with Gay.jl deterministic coloring and Enzyme.jl autodiff for gamut-aware probability distributions.
trit: 1
color: "#77DEB1"
---

## Overview

**GayMonteCarloMeasurements.jl** extends MonteCarloMeasurements.jl with Gay.jl chromatic identity for deterministic color-coded uncertainty propagation.

## Core Concepts

### Particles as Colored Distributions

```julia
using MonteCarloMeasurements
using Gay

# Construct uncertain parameters with color tracking
gay_seed!(0xcd0a0fde6e0a8820)
a = π ± 0.1  # Particles{Float64,2000}

# Propagate through nonlinear functions
sin(a)  # → Particles with full distribution
```

### Enzyme Gamut Learning

```julia
using Enzyme

# Learnable colorspace parameters
params = OkhslParameters()

function loss(params, seed, target_gamut=:srgb_boundary)
    color = forward_color(params, projection, seed)
    gamut_penalty = out_of_gamut_distance(color, target_gamut)
    bandwidth_reward = color_distinctiveness(color)
    return gamut_penalty - 0.1 * bandwidth_reward
end

∂params = Enzyme.gradient(Reverse, loss, params, seed)
```

## Features

- **Nonlinear uncertainty propagation** - Handles x², sign(x), integration
- **Correlated quantities** - Multivariate particles
- **Distribution fitting** - `fit(Gamma, p)` for any Particles
- **Visualization** - `plot(p)` shows histogram, `density(p)` shows KDE
- **SPI verification** - Fingerprint matching across network

## GF(3) Integration

| Trit | Role | Operation |
|------|------|-----------|
| +1 | PLUS | Generative sampling |
| 0 | ERGODIC | Distribution transport |
| -1 | MINUS | Constraint verification |

## Self-Avoiding Walk

```
next_color() → visited check
     │
     ├─ fresh → XOR into fingerprint
     │
     └─ collision → triadic fork
```

## Repository

- **Source**: bmorphism/GayMonteCarloMeasurements.jl
- **Seed**: `0xcd0a0fde6e0a8820`
- **Index**: 103/1055

## Related Skills

- `gay-julia` - Core Gay.jl integration
- `spi-parallel-verify` - Fingerprint verification
- `fokker-planck-analyzer` - Equilibrium analysis
