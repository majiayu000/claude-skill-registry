---
name: julia-gay
description: "Gay.jl integration for deterministic color generation. SplitMix64 RNG, GF(3) trits, and SPI-compliant fingerprints in Julia."
metadata:
  trit: +1
  version: "1.0.0"
  bundle: core
---

# Julia Gay Skill

**Trit**: +1 (PLUS - generative color computation)  
**Foundation**: Gay.jl + SplitMix64 + SPI  

## Core Concept

Gay.jl provides:
- Deterministic color from seed + index
- GF(3) trit classification
- SPI-compliant parallel fingerprints
- Wide-gamut color space support

## API

```julia
using Gay

# Color at index
color = color_at(seed, index)
# => (r=0.65, g=0.32, b=0.88)

# Palette generation
palette = Gay.palette(seed, 5)

# Trit classification
trit = Gay.trit(color)  # => -1, 0, or +1

# XOR fingerprint
fp = Gay.fingerprint(colors)
```

## SPI Guarantees

```julia
# Strong Parallelism Invariance
@assert fingerprint(colors_thread1) ⊻ fingerprint(colors_thread2) == 
        fingerprint(vcat(colors_thread1, colors_thread2))
```

## Ergodic Bridge

```julia
using Gay: ErgodicBridge

# Create time-color bridge
bridge = create_bridge(seed, n_colors)

# Verify bidirectionally
verify_bridge(bridge)

# Detect obstructions
obstructions = detect_obstructions(seed, n_samples)
```

## Canonical Triads

```
bisimulation-game (-1) ⊗ acsets (0) ⊗ julia-gay (+1) = 0 ✓
sheaf-cohomology (-1) ⊗ bumpus-narratives (0) ⊗ julia-gay (+1) = 0 ✓
spi-parallel-verify (-1) ⊗ triad-interleave (0) ⊗ julia-gay (+1) = 0 ✓
```

## See Also

- `gay-mcp` - MCP server for color generation
- `triad-interleave` - 3-stream scheduling
- `world-hopping` - Badiou possible world navigation
