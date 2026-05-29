---
name: gay-mcp
description: Deterministic color generation with SplitMix64, GF(3) trits, and MCP tools for palettes and threads.
source: local
license: UNLICENSED
---

<!-- Propagated to codex | Trit: 0 | Source: .ruler/skills/gay-mcp -->

# Gay-MCP Skill: Deterministic Color Generation

**Status**: ✅ Production Ready
**Trit**: +1 (PLUS - optimistic/generative)
**Principle**: Same seed → Same colors (SPI guarantee)
**Implementation**: Gay.jl (Julia) + SplitMixTernary (Ruby)

---

## Overview

**Gay-MCP** provides deterministic color generation via SplitMix64 + golden angle. Every invocation with the same seed produces identical colors, enabling:

1. **Parallel computation**: Fork generators, get same results
2. **Reproducibility**: Colors are functions of (seed, index)
3. **GF(3) trits**: Each color maps to {-1, 0, +1}

## Core Algorithm

```
SplitMix64:
  state = (state + γ) mod 2⁶⁴
  z = state
  z = (z ⊕ (z >> 30)) × 0xBF58476D1CE4E5B9
  z = (z ⊕ (z >> 27)) × 0x94D049BB133111EB
  return z ⊕ (z >> 31)

Color Generation:
  L = 10 + random() × 85    # Lightness: 10-95
  C = random() × 100        # Chroma: 0-100
  H = random() × 360        # Hue: 0-360
  trit = hue_to_trit(H)     # GF(3) mapping
```

## Constants

```ruby
GOLDEN = 0x9E3779B97F4A7C15  # φ⁻¹ × 2⁶⁴
MIX1   = 0xBF58476D1CE4E5B9
MIX2   = 0x94D049BB133111EB
MASK64 = 0xFFFFFFFFFFFFFFFF
```

## MCP Server

The Gay MCP server provides these tools:

| Tool | Description |
|------|-------------|
| `color_at` | Get color at specific index |
| `palette` | Generate N-color palette |
| `golden_thread` | Golden angle spiral |
| `reafference` | Self-recognition loop |
| `loopy_strange` | Generator ≡ Observer |

## Commands

```bash
# Start MCP server
julia --project=@gay -e "using Gay; Gay.serve_mcp()"

# Generate palette
just gay-palette seed=1069 n=12

# Test determinism
just gay-test
```

## API (Ruby)

```ruby
require 'splitmix_ternary'

# Create generator
gen = SplitMixTernary.new(1069)

# Get color at index
color = gen.color_at(42)
# => { L: 45.2, C: 67.8, H: 234.5, trit: -1, index: 42 }

# Generate trits
gen.next_trit  # => -1, 0, or +1

# Split for parallelism
child = gen.split(7)  # Independent child generator
```

## API (Julia)

```julia
using Gay

# Set seed
Gay.gay_seed(1069)

# Get color
color = Gay.color_at(42)

# Generate palette
palette = Gay.palette(12)

# Golden thread
colors = Gay.golden_thread(steps=10)
```

## Tripartite Streams

Three independent streams with GF(3) = 0:

```ruby
streams = SplitMixTernary::TripartiteStreams.new(seed)

triplet = streams.next_triplet
# => { minus: -1, ergodic: 0, plus: 1, gf3_sum: 0, conserved: true }
```

## Trit Mapping

```
Hue 0-60°, 300-360° → +1 (PLUS, warm)
Hue 60-180°         →  0 (ERGODIC, neutral)
Hue 180-300°        → -1 (MINUS, cold)
```

## Out-of-Order Proof

```ruby
proof = SplitMixTernary.prove_out_of_order(seed)
# => { 
#      ordered_equals_reversed: true,
#      ordered_equals_shuffled: true,
#      proof: "QED: Math is doable out of order"
#    }
```

## Integration with Unworld

Colors are derived, not temporal:

```ruby
# Seed chaining
next_seed = Unworld.chain_seed(current_seed, color[:trit])

# Derive color
color = Unworld.derive_color(seed, index)
```

## Example Output

```
╔═══════════════════════════════════════════════════════════════════╗
║  GAY.JL: Deterministic Color Generation                          ║
╚═══════════════════════════════════════════════════════════════════╝

Seed: 0x42D

─── Palette (12 colors) ───
  1: #D8267F (trit=+1)
  2: #2CD826 (trit=0)
  3: #4FD826 (trit=0)
  ...

─── Out-of-Order Proof ───
  Indices: [1, 5, 10, 20, 50]
  Ordered = Reversed: true
  Ordered = Shuffled: true
  QED: Math is doable out of order
```

---

**Skill Name**: gay-mcp
**Type**: Deterministic Color Generation
**Trit**: +1 (PLUS)
**GF(3)**: Conserved via tripartite streams
**SPI**: Guaranteed (same seed → same output)
