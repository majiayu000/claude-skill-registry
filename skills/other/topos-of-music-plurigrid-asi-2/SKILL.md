---
name: topos-of-music
description: Guerino Mazzola's mathematical music theory - Forms, Denotators, Morphisms, and Neo-Riemannian PLR operations with Gay.jl color integration
trit: +1
color: "#D82626"
---

# Topos of Music Skill

**Trit**: +1 (PLUS - generator)
**Color**: Red (#D82626)

## Overview

Implements Guerino Mazzola's *Topos of Music* categorical framework:

- **Forms**: Types in the musical topos (Simple, Limit, Colimit, List)
- **Denotators**: Instances of forms (notes, chords, scores)
- **Morphisms**: Structure-preserving transformations
- **Neo-Riemannian**: PLR group operations on triads

## Forms (Types)

```julia
abstract type Form end

struct SimpleForm <: Form
    name::Symbol
    module_type::Symbol  # :Z, :R, :Q
end

struct LimitForm <: Form      # Product type
    name::Symbol
    factors::Vector{Form}
end

struct ColimitForm <: Form    # Sum type
    name::Symbol
    summands::Vector{Form}
end

struct ListForm <: Form       # Powerset type
    name::Symbol
    element_form::Form
end

# Standard musical forms
const PitchForm = SimpleForm(:Pitch, :Z)
const OnsetForm = SimpleForm(:Onset, :R)
const DurationForm = SimpleForm(:Duration, :R)
const LoudnessForm = SimpleForm(:Loudness, :R)

const NoteForm = LimitForm(:Note, [PitchForm, OnsetForm, DurationForm, LoudnessForm])
const ChordForm = ListForm(:Chord, NoteForm)
const ScoreForm = ListForm(:Score, ChordForm)
```

## Denotators (Instances)

```julia
function Note(pitch::Int, onset::Float64, duration::Float64, loudness::Float64=0.8)
    LimitDenotator(NoteForm, [
        SimpleDenotator(PitchForm, pitch),
        SimpleDenotator(OnsetForm, onset),
        SimpleDenotator(DurationForm, duration),
        SimpleDenotator(LoudnessForm, loudness)
    ])
end

function Chord(notes::Vector)
    ListDenotator(ChordForm, notes)
end
```

## Morphisms (Transformations)

```julia
struct TranspositionMorphism <: Morphism
    semitones::Int
end

struct InversionMorphism <: Morphism
    axis::Int
end

struct RetrogradeMotion <: Morphism end

struct AugmentationMorphism <: Morphism
    factor::Float64
end

# Apply transposition
function apply(m::TranspositionMorphism, d::SimpleDenotator)
    if d.form == PitchForm
        SimpleDenotator(PitchForm, mod(d.value + m.semitones, 12))
    else
        d
    end
end
```

## Neo-Riemannian PLR Group

```julia
const P = PLROperation(:P)  # Parallel: change third quality
const L = PLROperation(:L)  # Leading-tone exchange
const R = PLROperation(:R)  # Relative

function apply_plr(op::Symbol, triad::Vector{Int})
    root, third, fifth = triad
    
    if op == :P
        # Major ↔ minor
        if mod(third - root, 12) == 4
            [root, mod(third - 1, 12), fifth]
        else
            [root, mod(third + 1, 12), fifth]
        end
    elseif op == :L
        # Leading-tone exchange
        if mod(third - root, 12) == 4
            [mod(root - 1, 12), third, fifth]
        else
            [root, third, mod(fifth + 1, 12)]
        end
    elseif op == :R
        # Relative major/minor
        if mod(third - root, 12) == 4
            [root, third, mod(fifth + 2, 12)]
        else
            [mod(root - 2, 12), third, fifth]
        end
    end
end
```

### PLR Example

```
C Major [0, 4, 7]
  P → c minor [0, 3, 7]
  L → e minor [11, 4, 7] → [7, 11, 4] normalized
  R → a minor [0, 4, 9] → [9, 0, 4] normalized
```

## Gay.jl Color Integration

```julia
const NOTE_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]

function hue_to_pitch_class(hue::Float64)::Int
    mod(round(Int, hue / 30.0), 12)
end

function pitch_class_to_hue(pc::Int)::Float64
    mod(pc, 12) * 30.0 + 15.0
end

function color_to_note(color)::Int
    rgb = convert(RGB, color)
    hsl = convert(HSL, rgb)
    hue_to_pitch_class(hsl.h)
end

# CatSharp trit mapping
function pitch_class_to_trit(pc::Int)::Int
    pc = mod(pc, 12)
    if pc ∈ [0, 4, 8]      # Augmented
        return 1
    elseif pc ∈ [3, 6, 9]  # Diminished
        return 0
    else
        return -1
    end
end
```

## Tonnetz Navigation

```julia
struct Tonnetz
    minor_third::Int   # 3 semitones
    major_third::Int   # 4 semitones
    fifth::Int         # 7 semitones
end

const STANDARD_TONNETZ = Tonnetz(3, 4, 7)

function tonnetz_neighbors(pc::Int, t::Tonnetz=STANDARD_TONNETZ)
    [
        mod(pc + t.minor_third, 12),
        mod(pc - t.minor_third, 12),
        mod(pc + t.major_third, 12),
        mod(pc - t.major_third, 12),
        mod(pc + t.fifth, 12),
        mod(pc - t.fifth, 12)
    ]
end
```

## Klumpenhouwer Networks

```julia
struct KNet
    nodes::Vector{Int}
    arrows::Vector{Tuple{Int,Int,Symbol,Int}}  # (from, to, T/I, n)
end

function verify_knet(knet::KNet)::Bool
    for (from, to, op, n) in knet.arrows
        pc_from = knet.nodes[from]
        pc_to = knet.nodes[to]
        expected = if op == :T
            mod(pc_from + n, 12)
        else  # :I
            mod(n - pc_from, 12)
        end
        if expected != pc_to
            return false
        end
    end
    true
end
```

## GF(3) Triads

```
gay-mcp (-1) ⊗ catsharp-galois (0) ⊗ topos-of-music (+1) = 0 ✓
rubato-composer (-1) ⊗ ordered-locale (0) ⊗ topos-of-music (+1) = 0 ✓
```

## Commands

```bash
# Run Topos of Music demo
julia dev/gadgets/topos_of_music.jl

# Apply PLR transformation
just plr-transform triad="0 4 7" op=P

# Navigate Tonnetz
just tonnetz-walk start=0 steps="m3 M3 P5"

# Verify K-net
just knet-verify nodes="0 4 7" arrows="T4 T3 T7"
```

## Related Skills

- `catsharp-galois` (0): Galois connection to Plurigrid
- `gay-mcp` (-1): Color ↔ pitch mapping
- `rubato-composer` (-1): Rubato Composer integration
- `ordered-locale` (0): Frame structure for scales

## References

- Mazzola, G. *The Topos of Music* (2002)
- Mazzola, G. *Musical Performance* (2011)
- Fiore & Noll. "Commuting Groups and the Topos of Triads"
- Cohn, R. "Neo-Riemannian Operations, Parsimonious Trichords"
