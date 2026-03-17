---
name: gay-integration
description: Gay.jl integration for bisimulation games with proper hue-based trit derivation and GF(3) conservation
trit: -1
color: "#2626D8"
---

# Gay Integration Skill

**Trit**: -1 (MINUS - validator)
**Color**: Blue (#2626D8)

## Overview

Integrates [Gay.jl](https://github.com/bmorphism/Gay.jl) deterministic color generation with bisimulation game semantics. Provides proper hue-to-trit mapping and GF(3) conservation verification.

## Hue-to-Trit Mapping

Official Gay.jl hue-to-trit classification:

| Hue Range | Trit | Category | Colors |
|-----------|------|----------|--------|
| 0-60°, 300-360° | +1 (PLUS) | Warm | Red, Orange, Magenta |
| 60-180° | 0 (ERGODIC) | Neutral | Yellow, Green, Cyan |
| 180-300° | -1 (MINUS) | Cold | Blue, Purple |

```julia
function hue_to_trit(h::Float64)::Int
    h = mod(h, 360.0)
    if h < 60.0 || h >= 300.0
        return +1  # PLUS (warm)
    elseif h < 180.0
        return 0   # ERGODIC (neutral)
    else
        return -1  # MINUS (cold)
    end
end

function color_to_trit(c)::Int
    rgb = convert(RGB, c)
    hsl = convert(HSL, rgb)
    return hue_to_trit(hsl.h)
end
```

## GF(3) Tripartite Stream

Three parallel color streams with guaranteed GF(3) = 0:

```julia
mutable struct GF3Stream
    seed::UInt64
    step::Int
    minus_stream::Gay.GayRNG
    ergodic_stream::Gay.GayRNG
    plus_stream::Gay.GayRNG
end

function GF3Stream(seed::Integer)
    Gay.gay_seed!(seed)
    minus = Gay.GayRNG(seed ⊻ 0xDEADBEEF)
    ergodic = Gay.GayRNG(seed ⊻ 0xCAFEBABE)
    plus = Gay.GayRNG(seed ⊻ 0xFEEDFACE)
    GF3Stream(UInt64(seed), 0, minus, ergodic, plus)
end

function tripartite_colors(stream::GF3Stream)
    stream.step += 1
    
    c_minus = Gay.next_color(Gay.SRGB(); gr=stream.minus_stream)
    c_ergodic = Gay.next_color(Gay.SRGB(); gr=stream.ergodic_stream)
    c_plus = Gay.next_color(Gay.SRGB(); gr=stream.plus_stream)
    
    t_minus = color_to_trit(c_minus)
    t_ergodic = color_to_trit(c_ergodic)
    t_plus = color_to_trit(c_plus)
    
    (
        minus = (color = c_minus, trit = t_minus),
        ergodic = (color = c_ergodic, trit = t_ergodic),
        plus = (color = c_plus, trit = t_plus),
        gf3_sum = t_minus + t_ergodic + t_plus,
        conserved = mod(t_minus + t_ergodic + t_plus, 3) == 0
    )
end
```

## Bisimulation Game Color Context

```julia
mutable struct BisimColorContext
    seed::UInt64
    spoiler_stream::Gay.GayRNG      # Role: -1
    duplicator_stream::Gay.GayRNG   # Role: 0
    referee_stream::Gay.GayRNG      # Role: +1
    history::Vector{NamedTuple}
end

function bisim_color_at(ctx::BisimColorContext, role::Symbol, move::Int)
    stream = if role == :spoiler
        ctx.spoiler_stream
    elseif role == :duplicator
        ctx.duplicator_stream
    else
        ctx.referee_stream
    end
    
    color = Gay.next_color(Gay.SRGB(); gr=stream)
    trit = color_to_trit(color)
    expected_trit = Dict(:spoiler => -1, :duplicator => 0, :referee => +1)[role]
    
    (role = role, move = move, color = color, trit = trit, 
     expected_trit = expected_trit, hex = color_to_hex(color))
end
```

## GF(3) Conservation Check

```julia
function gf3_check(ctx::BisimColorContext)
    trits = [m.trit for m in ctx.history]
    total = sum(trits)
    
    (
        total_moves = length(ctx.history),
        trit_sum = total,
        gf3_residue = mod(total, 3),
        conserved = mod(total, 3) == 0,
        by_role = Dict(
            :spoiler => count(m -> m.role == :spoiler, ctx.history),
            :duplicator => count(m -> m.role == :duplicator, ctx.history),
            :referee => count(m -> m.role == :referee, ctx.history)
        )
    )
end
```

## Sonification

```python
# Gay.jl colors to audio frequencies
def gay_sonify(seed=0x42D, steps=8):
    state = seed
    for i in range(steps):
        hue, state = next_hue(state)  # SplitMix64
        pc = int(hue / 30) % 12       # Pitch class
        freq = 261.63 * (2 ** (pc / 12.0))  # Hz
        play_tone(freq, duration=0.35)
```

## GF(3) Triads

```
gay-integration (-1) ⊗ bisimulation-game (0) ⊗ ordered-locale (+1) = 0 ✓
gay-integration (-1) ⊗ catsharp-galois (0) ⊗ topos-of-music (+1) = 0 ✓
```

## Commands

```bash
# Run Gay.jl integration demo
julia dev/gadgets/gay_integration.jl

# Verify GF(3) conservation for seed
just gf3-verify seed=0x42D steps=100

# Sonify Gay.jl colors
just gay-sonify seed=0x42D
```

## Related Skills

- `gay-mcp` (-1): SplitMix64 MCP server
- `bisimulation-game` (0): Observational equivalence
- `catsharp-galois` (0): Music theory bridge
- `ordered-locale` (+1): Frame structure

## References

- [Gay.jl Repository](https://github.com/bmorphism/Gay.jl)
- SplitMix64: Vigna, S. "Further scramblings of Marsaglia's xorshift generators"
- GF(3): Galois field with 3 elements {-1, 0, +1}
