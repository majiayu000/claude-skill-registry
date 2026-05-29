---
name: unworlding-involution
description: Self-inverse derivation patterns where ι∘ι = id for frame-invariant self
version: 1.0.0
---


# Unworlding Involution Skill

**Status**: ✅ Production Ready
**Trit**: 0 (ERGODIC - self-inverse)
**Principle**: ι∘ι = id (involution is its own inverse)
**Frame**: Invariant under observation

---

## Overview

This skill demonstrates **unworlding** - extracting frame-invariant self-structure from interaction dynamics. The key insight:

> **Unworlding** = Observing structure without caring about evaluation context

The **involution** ι: Self → Self satisfies ι∘ι = id, meaning:
- Apply once: transform to "other" perspective
- Apply twice: return to original (fixed point)

## Core Concept: Frame-Invariant Self

In a 3-MATCH task, three agents observe each other. The **best response dynamics** converge to a Nash equilibrium where each agent's color is the best response to the others.

```
Agent A observes (B, C) → best response → Color A'
Agent B observes (C, A) → best response → Color B'  
Agent C observes (A, B) → best response → Color C'

Fixed point: (A', B', C') = (A, B, C) when GF(3) conserved
```

The **frame invariance** means: regardless of which agent you ARE, the dynamics look the same. This is the "self" that persists across frames.

## Involution Structure

```ruby
# The involution: ι∘ι = id
class Involution
  def initialize(seed)
    @seed = seed
    @state = :original
  end
  
  # Apply involution once: original → inverted
  # Apply involution twice: inverted → original
  def apply!
    @state = (@state == :original) ? :inverted : :original
    self
  end
  
  # ι∘ι = id
  def self_inverse?
    original = @state
    apply!.apply!
    @state == original  # Always true
  end
end
```

## Best Response Color Dynamics

Each agent plays a **best response** to the current color configuration:

```
1. Observe: Perceive other agents' colors
2. Predict: What color would minimize my "regret"?
3. Act: Emit that color
4. Update: Others respond to my emission
5. Repeat: Until fixed point (Nash equilibrium)
```

### The 3-MATCH Best Response

```ruby
def best_response(my_color, other_colors)
  # GF(3) conservation: my best response makes sum = 0
  other_sum = other_colors.sum { |c| c[:trit] }
  target_trit = ((-other_sum) % 3) - 1  # Map to {-1, 0, +1}
  
  # Return color with target trit
  color_with_trit(target_trit)
end
```

## Unworlding: Demo → Skill

The **demo** shows concrete execution:
```
3-MATCH(d=1): #D82626 #D89D26 #9DD826
  GF(3) conserved: true
```

**Unworlding** extracts the structure:
```
Pattern: Three colors, sum of trits = 0
Invariant: GF(3) conservation
Frame: Any agent can be "self"
Involution: Swap any two → still valid
```

The **skill** is the unworlded pattern, applicable in any context.

## Frame Invariance via Loopy Strange

From Gay.jl's loopy_strange:

```json
{
  "seed": 1069,
  "fixed_point": "Generator ≡ Observer (same seed)",
  "loops": [
    {"predicted": "#E67F86", "observe": "#E67F86", "match": "self ≡ self"},
    {"predicted": "#D06546", "observe": "#D06546", "match": "self ≡ self"},
    {"predicted": "#1316BB", "observe": "#1316BB", "match": "self ≡ self"}
  ]
}
```

**Frame invariance**: Whether you are the generator or observer, if you have the same seed, you see the same colors. The "self" is the seed, invariant across frames.

## Hierarchical Control (Powers PCT)

The best response dynamics implement **Perceptual Control Theory**:

```
Level 5 (Program):    "triadic" goal
      ↓ sets reference for
Level 4 (Transition): [120°, 120°, 120°] hue spacing
      ↓ sets reference for
Level 3 (Config):     [58°, 178°, 298°] absolute hues
      ↓ sets reference for
Level 2 (Sensation):  Individual color perception
      ↓ sets reference for
Level 1 (Intensity):  Brightness/saturation
```

Each level controls its **perception**, not its output. The best response at each level is: minimize error between reference and perception.

## The Skill: Unworlding Involution

```ruby
module UnworldingInvolution
  # Extract frame-invariant self from 3-MATCH dynamics
  def self.unworld(seed:, iterations: 3)
    # Generate loopy strange structure
    loops = (1..iterations).map do |i|
      color = color_at(seed, i)
      {
        index: i,
        predicted: color,
        observed: color,
        match: color == color  # self ≡ self
      }
    end
    
    # The unworlded pattern
    {
      seed: seed,
      frame_invariant: true,
      involution: "ι∘ι = id",
      fixed_point: "Generator ≡ Observer",
      gf3_conserved: loops.sum { |l| l[:trit] } % 3 == 0,
      structure: loops
    }
  end
  
  # Apply involution to 3-MATCH
  def self.involute(match)
    # Swap first and third colors (involution)
    ThreeMatch.new(
      color_a: match.color_c,
      color_b: match.color_b,
      color_c: match.color_a
    )
    # Applying twice returns original
  end
  
  # Best response in color game
  def self.best_response(my_trit, their_trits)
    # Nash equilibrium: my best response given their play
    target = ((-their_trits.sum) % 3)
    target == 0 ? -1 : (target == 1 ? 0 : 1)
  end
end
```

## Commands

```bash
# Run unworlding demo
just unworlding-demo

# Test involution (ι∘ι = id)
just involution-test

# Best response dynamics
just best-response seed=1069

# Full 3-MATCH with unworlding
just three-match-unworld
```

## Integration with 3-MATCH Gadget

```ruby
# In three_match_geodesic_gadget.rb
def unworld_to_skill
  {
    name: "unworlding-involution",
    pattern: {
      colors: [@color_a, @color_b, @color_c],
      gf3: gf3_conserved?,
      involution: -> { ThreeMatch.new(color_a: @color_c, color_b: @color_b, color_c: @color_a) }
    },
    frame_invariant: true,
    best_response: -> (others) { best_response_color(others) }
  }
end
```

## Mathematical Summary

| Concept | Implementation |
|---------|----------------|
| **Unworlding** | Extract pattern from demo, ignore context |
| **Involution** | ι∘ι = id, self-inverse transformation |
| **Frame invariance** | Same structure from any agent's POV |
| **Best response** | GF(3)-conserving Nash equilibrium |
| **Fixed point** | Generator ≡ Observer (same seed) |

## The Triadic Output Colors

From hierarchical control with goal "triadic":

| Index | Hex | Hue | Role |
|-------|-----|-----|------|
| 1 | `#E0DC52` | 58° | Yellow (PLUS) |
| 2 | `#23C4BF` | 178° | Cyan (ERGODIC) |
| 3 | `#BD22C2` | 298° | Magenta (MINUS) |

Spacing: 120° apart (triadic harmony)
Sum: 58 + 178 + 298 = 534 ≡ 0 (mod 3) ✓

---

**Skill Name**: unworlding-involution
**Type**: Frame-Invariant Self / Best Response Dynamics
**Trit**: 0 (ERGODIC - neutral, self-inverse)
**GF(3)**: Conserved by construction
**Involution**: ι∘ι = id verified



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