---
name: gesture-hypergestures
description: Gesture Hypergestures Skill
version: 1.0.0
---

# Gesture Hypergestures Skill

> *"A gesture is a continuous curve in a topological category."*
> — Guerino Mazzola, Topos of Music III: Gestures

**Trit**: +1 (PLUS - generative)
**Color**: #C42990 (from seed 137508, index 23)
**Foundation**: Mazzola's Diamond Conjecture

## Overview

**Gestures** are the missing link between structure (forms/denotators) and performance (physical action). This skill implements Mazzola's gesture theory from *Topos of Music III*.

```
Form (static) → Gesture (dynamic) → Performance (physical)
    ↓              ↓                    ↓
 Denotator    Hypergesture           Sound wave
```

## Core Concepts

### Gesture Definition

A gesture is a continuous curve `γ: [0,1] → X` in a topological category:

```julia
struct Gesture{T}
    domain::Interval      # [0, 1] or [a, b]
    target::T             # Topological space
    curve::Function       # t → target
end

# Example: pitch gesture (glissando)
glissando = Gesture(
    (0.0, 1.0),
    PitchSpace,
    t -> 60 + 12 * t  # C4 to C5
)
```

### Hypergestures

A **hypergesture** is a gesture of gestures - a higher-order curve:

```julia
struct Hypergesture{T}
    base_gestures::Vector{Gesture{T}}
    interpolation::Function  # Gesture × Gesture → Gesture
end

# Hypergesture: morphing between two melodic contours
melody_morph = Hypergesture(
    [melody_a, melody_b],
    (g1, g2, t) -> interpolate_gesture(g1, g2, t)
)
```

### Diamond Conjecture

The fundamental theorem relating local to global:

```
H^n(Gesture) ≅ H^n(Skeleton) ⊗ H^n(Body)

Local gesture fragments glue iff cohomology obstructions vanish.
```

## Integration with Loaded Skills

### Gestures ↔ topos-of-music

Gestures extend the Form/Denotator framework:

```julia
# Form → Gesture
NoteGestureForm = GestureForm(NoteForm)

# Denotator → Gestured Denotator
performed_note = GesturedDenotator(
    note,
    timing_gesture,   # Micro-timing
    dynamics_gesture  # Expression curve
)
```

### Gestures ↔ catsharp-sonification

Sonify gesture trajectories:

```julia
function sonify_gesture(g::Gesture, seed::Int)
    Gay.gay_seed!(seed)
    for t in 0:0.1:1
        point = g.curve(t)
        color = Gay.next_color()
        freq = pitch_to_freq(point)
        trit = hue_to_trit(Gay.hue(color))
        play_tone(freq, waveform_for_trit(trit))
    end
end
```

### Gestures ↔ persistent-homology

Track gesture stability across filtrations:

```julia
# Gesture persistence: which contours survive simplification?
filtration = [ε for ε in 0.1:0.1:1.0]
persistence = compute_gesture_persistence(gesture_space, filtration)

# Stable gestures = robust performance features
stable_gestures = filter(g -> g.persistence > 0.5, all_gestures)
```

### Gestures ↔ sheaf-cohomology

Verify gesture gluing conditions:

```julia
# Local gesture patches
left_hand = Gesture(...)
right_hand = Gesture(...)

# Check if they glue into coherent performance
H1 = compute_gesture_cohomology([left_hand, right_hand])
if H1 == 0
    println("Gestures glue correctly!")
else
    println("Obstruction detected: hands don't coordinate")
end
```

### Gestures ↔ interaction-nets

Gesture composition as net reduction:

```
    ┌──────┐     ┌──────┐
    │ G1   ├─────┤ G2   │
    └──┬───┘     └───┬──┘
       │             │
       └──────┬──────┘
              │
         ┌────┴────┐
         │ G1;G2   │  (composed gesture)
         └─────────┘
```

### Gestures ↔ stellogen

Gestures as continuous star trajectories:

```stellogen
' Gesture as constellation with time parameter
(def gesture_star
  [(+time T) (+pitch (interp P0 P1 T)) (-note N)])

' Hypergesture: nest gestures
(def hyper
  [(+meta_time S) 
   (+gesture (gesture_star S))
   (-performance P)])
```

## Mathematical Structure

### Gesture Category

```
Objects: Topological spaces (pitch, dynamics, timing, ...)
Morphisms: Continuous curves γ: I → X
Composition: Path concatenation (up to homotopy)
```

### Hypergesture Homology

```
H_0(G) = Connected components of gesture space
H_1(G) = Loops in gesture space (repeating patterns)
H_n(G) = Higher-dimensional voids (complex structures)
```

### Diamond Diagram

```
           Skeleton
              ↑
    Body ←─── G ───→ Gesture
              ↓
           Performance

G = Gesture object relating all three domains
```

## Commands

```bash
# Create gesture from MIDI
just gesture-from-midi performance.mid

# Interpolate between gestures
just gesture-interpolate g1.json g2.json --steps 10

# Verify hypergesture cohomology
just gesture-h1 hypergesture.json

# Sonify gesture trajectory
just gesture-sonify contour.json --seed 137508

# Visualize gesture space
just gesture-viz --output gesture.svg
```

## GF(3) Triads

```
gesture-hypergestures (+1) ⊗ topos-of-music (0) ⊗ rubato-composer (-1) = 0 ✓
gesture-hypergestures (+1) ⊗ catsharp-sonification (0) ⊗ persistent-homology (-1) = 0 ✓
gesture-hypergestures (+1) ⊗ interaction-nets (0) ⊗ sheaf-cohomology (-1) = 0 ✓
```

## Example: Rubato Performance

```julia
# Rubato = tempo gesture
rubato = Gesture(
    (0.0, 1.0),
    TempoSpace,
    t -> 120 * (1 + 0.1 * sin(2π * t * 4))  # Oscillating around 120 BPM
)

# Apply to note sequence
for note in score
    performed_onset = apply_gesture(rubato, note.onset)
    play(note.pitch, performed_onset, note.duration)
end
```

## Files

- **Core implementation**: `lib/gesture.jl`
- **Hypergesture homology**: `lib/hypergesture_homology.jl`
- **Sonification bridge**: `lib/gesture_sonify.jl`

## Related Skills

| Skill | Trit | Relationship |
|-------|------|--------------|
| topos-of-music | 0 | Forms → Gestures |
| catsharp-sonification | 0 | Sonify trajectories |
| rubato-composer | -1 | Execute performances |
| persistent-homology | -1 | Gesture stability |
| sheaf-cohomology | -1 | Gluing verification |

## References

- Mazzola, G. *The Topos of Music III: Gestures* (2017)
- Mazzola, G. *Musical Performance* (2011)
- Mazzola et al. "The Diamond Conjecture for Hypergestures"

---

**Skill Name**: gesture-hypergestures
**Type**: Musical Performance Theory
**Trit**: +1 (PLUS - GENERATOR)
**GF(3)**: Generates continuous performance curves
**Sonification**: C#4 sine (hue 55°, warm)