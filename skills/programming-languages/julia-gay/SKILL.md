---
name: julia-gay
description: Gay.jl integration for deterministic color generation. SplitMix64 RNG, GF(3) trits, and SPI-compliant fingerprints in Julia.
version: 1.0.0
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

## Julia Scientific Package Integration

From `julia-scientific` skill - related Julia packages for color/visualization:

| Package | Use | julia-scientific Category |
|---------|-----|---------------------------|
| **Colors.jl** | Color types, conversions | Visualization |
| **ColorSchemes.jl** | Predefined palettes | Visualization |
| **Makie.jl** | GPU-accelerated vis with color | Visualization |
| **CairoMakie.jl** | Publication-quality with color | Visualization |
| **AlgebraOfGraphics.jl** | Grammar-of-graphics + color | Visualization |
| **Catlab.jl** | ACSets + color labeling | Data Science |
| **Gay.jl** | Core deterministic colors | Core |

### Bridge to Scientific Domains

```julia
# Molecular visualization with deterministic colors
using Gay, MolecularGraph, CairoMakie

mol = smilestomol("CCO")
atom_colors = [Gay.color_at(seed, i) for i in 1:natoms(mol)]
visualize_molecule(mol, colors=atom_colors)

# Single-cell UMAP with Gay.jl cluster colors
using Gay, SingleCellProjections, CairoMakie

clusters = cluster(adata)
cluster_colors = Gay.palette(seed, n_clusters)
scatter(umap_coords, color=cluster_colors[cluster_labels])
```

## See Also

- `gay-mcp` - MCP server for color generation
- `triad-interleave` - 3-stream scheduling
- `world-hopping` - Badiou possible world navigation
- `julia-scientific` - Full Julia package mapping (137 skills)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Visualization
- **matplotlib** [○] via bicomodule
  - Hub for all visualization

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.