---
name: gay-julia
description: Wide-gamut color sampling with splittable determinism using Pigeons.jl
  SPI pattern and LispSyntax integration.
metadata:
  trit: 0
---

# Gay.jl - Wide-Gamut Deterministic Color Sampling

Wide-gamut color sampling with splittable determinism using Pigeons.jl SPI pattern and LispSyntax integration.

## Repository
- **Source**: https://github.com/bmorphism/Gay.jl
- **Language**: Julia
- **Pattern**: SplitMix64 → GF(3) trits → LCH colors

## Core Concepts

### SplitMix64 Determinism
```julia
# Deterministic color from seed
using Gay

seed = 0x598F318E2B9E884
color = gay_color(seed)  # Returns LCH color
trit = gf3_trit(seed)    # Returns :MINUS, :ERGODIC, or :PLUS
```

### GF(3) Conservation
Every color operation preserves the tripartite balance:
- **MINUS** (-1): Contractive operations
- **ERGODIC** (0): Neutral/balanced operations  
- **PLUS** (+1): Expansive operations

Sum of trits across parallel streams must equal 0 (mod 3).

### LispSyntax Integration
```julia
using LispSyntax

# S-expression colorization
sexp = @lisp (defun factorial (n) (if (<= n 1) 1 (* n (factorial (- n 1)))))
colored = colorize(sexp, seed=seed)
```

## Integration with plurigrid/asi

### With gay-mcp skill
```julia
# MCP tool registration with deterministic colors
using Gay, MCP

tool = MCPTool("color-palette", seed=0x1069)
palette = generate_palette(tool, n=5)
```

### With spi-parallel-verify
```julia
# Verify GF(3) conservation across parallel execution
using Gay, SPI

streams = trifurcate(seed, [:task1, :task2, :task3])
verify_conservation(streams)  # Asserts sum(trits) ≡ 0 (mod 3)
```

### With triad-interleave
```julia
# Interleave three color streams
using Gay, TriadInterleave

schedule = interleave(
    minus_stream(seed),
    ergodic_stream(seed),
    plus_stream(seed)
)
```

## Key Functions

| Function | Description |
|----------|-------------|
| `gay_color(seed)` | Generate LCH color from seed |
| `gf3_trit(seed)` | Extract GF(3) trit assignment |
| `splitmix64(state)` | Advance RNG state |
| `colorize(sexp, seed)` | Color S-expression nodes |
| `palette(seed, n)` | Generate n-color palette |

## Use Cases

1. **Deterministic UI theming** - Same seed → same colors everywhere
2. **Parallel task coloring** - GF(3) ensures balanced distribution
3. **CRDT conflict resolution** - Trit-based merge ordering
4. **Terminal session coloring** - vterm integration via crdt-vterm-bridge

## Related Skills
- `gay-mcp` - MCP server with Gay.jl colors
- `spi-parallel-verify` - Strong Parallelism Invariance verification
- `triad-interleave` - Three-stream scheduling
- `bisimulation-game` - GF(3) conservation in game semantics
