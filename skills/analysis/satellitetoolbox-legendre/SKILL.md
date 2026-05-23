---
name: satellitetoolbox-legendre
description: SatelliteToolboxLegendre.jl for computing associated Legendre functions and derivatives. Use when working with spherical harmonics, gravity field expansions, or geomagnetic field computations.
---

# SatelliteToolboxLegendre.jl

Associated Legendre functions and derivatives with multiple normalization options. Repo: [JuliaSpace/SatelliteToolboxLegendre.jl](https://github.com/JuliaSpace/SatelliteToolboxLegendre.jl)

## Computing Legendre Functions

```julia
# P[n+1, m+1] = P_{n,m}[cos(ϕ)]
P = legendre(Val(:full), ϕ, n_max)                    # Full normalization
P = legendre(Val(:schmidt), ϕ, n_max, m_max)          # Schmidt semi-normalization
P = legendre(Val(:unnormalized), ϕ, n_max)            # Unnormalized

# In-place (zero-allocation)
legendre!(Val(:full), P, ϕ, n_max, m_max)
```

## Computing Derivatives

```julia
(dP, P) = dlegendre(Val(:full), ϕ, n_max)             # Returns both dP and P
dlegendre!(dP, ϕ, P, n_max, m_max)                     # In-place (P must be pre-computed)
```

## Key Conventions
- First argument `N` selects normalization: `Val(:full)`, `Val(:schmidt)`, `Val(:unnormalized)`
- Angle `ϕ` in **radians**
- Indexing: `P[n+1, m+1]` for degree `n`, order `m`
- Optional `ph_term=true` includes Condon-Shortley phase `(-1)^m`
- In-place variants infer `n_max`/`m_max` from matrix dimensions if omitted
- Zero external dependencies (pure Julia)
