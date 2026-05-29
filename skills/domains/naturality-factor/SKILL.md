---
name: naturality-factor
description: Naturality Factor Skill
version: 1.0.0
---

# Naturality Factor Skill

> *"The naturality condition ensures transformations commute with structure."*

Measures how well transformations preserve conservation laws across musical and categorical structures.

## Overview

**Trit**: 0 (ERGODIC - Coordinator)  
**Location**: `lib/conserved_quantity.rb`, `lib/rubato_bridge.rb`  
**Dependencies**: GF(3), Z/12Z chromatic, Rubato morphisms

## Core Concept

In category theory, a **natural transformation** η: F → G satisfies:

```
    η_A
F(A) ───→ G(A)
  │         │
F(f)       G(f)
  ↓         ↓
F(B) ───→ G(B)
    η_B
```

The **naturality factor** ν ∈ [0,1] measures how well this square commutes:
- ν = 1.0 → perfectly natural (conservation preserved)
- ν = 0.0 → maximally unnatural (conservation violated)

## Mazzola's Insight

From *Topos of Music*: "Conservation" in music IS naturality of functors. Transposition preserves intervals because the naturality square closes.

## Classes

### NaturalityFactor

```ruby
nf = ConservedQuantity::NaturalityFactor.new(
  conservation: ConservedQuantity::Laws::CHROMATIC,
  source_functor: ->(x) { x },
  target_functor: ->(x) { x }
)

result = nf.compute(
  eta: ->(x) { x + 7 },      # Transposition
  morphism: ->(x) { x },      # Identity morphism
  object_a: 60,               # C4
  object_b: 64                # E4
)
# => { factor: 1.0, defect: 0, natural?: true }
```

### Chromatic Naturality

```ruby
# Does transposition preserve intervals?
result = ConservedQuantity::NaturalityFactor.chromatic_naturality(
  interval: 7,           # Perfect fifth
  notes: [0, 4, 7]       # C major triad
)
# => { factor: 1.0, natural?: true, original_intervals: [4, 3] }
```

### Triadic Naturality (GF(3))

```ruby
# Does doubling preserve trit balance?
result = ConservedQuantity::NaturalityFactor.triadic_naturality(
  transform: ->(x) { x * 2 },
  objects: [0, 1, 2, 3, 4, 5],
  charge_fn: ->(x) { x % 3 }
)
# => { factor: 1.0, defect: 0, natural?: true }
```

### Yoneda Conservation

Objects determined by ALL their relationships (Yoneda lemma):

```ruby
yoneda = ConservedQuantity::YonedaConservation.new(
  conservation: ConservedQuantity::Laws::TRIADIC,
  objects: [0, 1, 2, 3, 4, 5, 6, 7, 8]
)

yoneda.yoneda_charge(3)  # Sum of all relationships
yoneda.yoneda_balanced?(0, 3, 6)  # Check if balanced
```

## Rubato Integration

### NaturalMorphism

Rubato morphisms with naturality tracking:

```ruby
t7 = RubatoBridge::Morphisms.transposition(7)
transposed_score = t7.apply(score)

# Check naturality
result = t7.compute_naturality(notes)
puts t7.naturality_factor  # => 1.0
```

### Standard Morphisms

| Morphism | Naturality | Preserves |
|----------|------------|-----------|
| `transposition(n)` | 1.0 | Intervals |
| `inversion(axis:)` | 1.0 | Interval magnitudes |
| `retrograde` | 1.0 | Pitch content |
| `augmentation(f)` | varies | Depends on f |

## GF(3) Triads

Naturality factor connects to skill triads:

```
three-match (-1) ⊗ naturality-factor (0) ⊗ gay-mcp (+1) = 0 ✓
sheaf-cohomology (-1) ⊗ naturality-factor (0) ⊗ rubato-composer (+1) = 0 ✓
persistent-homology (-1) ⊗ naturality-factor (0) ⊗ topos-generate (+1) = 0 ✓
```

## Commands

```bash
# Run conservation demo with naturality
ruby lib/conserved_quantity.rb

# Run Rubato bridge with naturality demo
ruby lib/rubato_bridge.rb

# Check naturality of a transposition
just naturality-check T7 "0,4,7"
```

## Mathematical Foundation

### Defect Calculation

For transformation η with conservation law C:

```
defect = C.combine(charge(left_path), -charge(right_path))
factor = defect == identity ? 1.0 : 1.0 / (1.0 + |defect|)
```

### Conservation Laws Supported

| Law | Modulus | Use Case |
|-----|---------|----------|
| GF(3) | 3 | Trit balance |
| Chromatic | 12 | Pitch classes |
| Diatonic | 7 | Scale degrees |
| Parity | 2 | XOR operations |
| Integer | ∞ | Unbounded |

## See Also

- [conserved_quantity.rb](file:///Users/bob/ies/music-topos/lib/conserved_quantity.rb)
- [rubato_bridge.rb](file:///Users/bob/ies/music-topos/lib/rubato_bridge.rb)
- [ctp-yoneda skill](.agents/skills/ctp-yoneda/SKILL.md)
- [rubato-composer skill](.agents/skills/rubato-composer/SKILL.md)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

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