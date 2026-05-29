---
name: pun-decomposition
description: Pun Decomposition Skill (MINUS -1)
version: 1.0.0
---


# Pun Decomposition Skill (MINUS -1)

> *"A pun exploits multiple valid decompositions of the same phonetic surface."*

## Core Insight

A **pun** is an information reflow that maps a single surface form to multiple semantic contexts. The humor arises from the unexpected context switch—the inductive bias favors one parse, but the pun activates another.

```
pun : Surface → {Context₁, Context₂, ...}
where each Contextᵢ has a valid decomposition
```

## Neighbor Awareness (Braided Monoidal)

This skill knows its neighbors in the triad:

| Position | Skill | Trit | Role |
|----------|-------|------|------|
| **Left** | gestalt-hacking | 0 | Perceptual grouping exploitation |
| **Self** | pun-decomposition | -1 | Multiple parse validation |
| **Right** | acsets | 0 | Schema-aware decomposition |

**Yang-Baxter coherence**: `(σ₁⊗id)(id⊗σ₁)(σ₁⊗id) = (id⊗σ₁)(σ₁⊗id)(id⊗σ₁)`

## GF(3) Triads

```
pun-decomposition (-1) ⊗ gestalt-hacking (0) ⊗ gay-mcp (+1) = 0 ✓  [Core Pun]
pun-decomposition (-1) ⊗ acsets (0) ⊗ topos-generate (+1) = 0 ✓  [Schema Pun]
pun-decomposition (-1) ⊗ reflow (0) ⊗ gay-mcp (+1) = 0 ✓  [Reflow Pun]
three-match (-1) ⊗ gestalt-hacking (0) ⊗ gay-mcp (+1) = 0 ✓  [Pattern Match]
```

## Pun as Gestalt Attack

From the gestalt hacking thread:

```rust
enum GestaltPrinciple {
    Proximity,    // Close morphemes group
    Similarity,   // Similar sounds group  
    Closure,      // Incomplete parse completed
    Continuity,   // Smooth phonetic path preferred
    FigureGround, // Dominant meaning masks secondary
}
```

A pun exploits **Closure** and **FigureGround**:
- **Closure**: The listener completes the parse with the expected meaning
- **FigureGround**: The secondary meaning lurks in background until activated

## Decomposition Types

### Morphemic Decomposition

```ruby
# "I'm reading a book about anti-gravity. It's impossible to put down."
{
  surface: "put down",
  decompositions: [
    { parse: ["put", "down"], meaning: "place on surface", trit: 1 },
    { parse: ["put-down"], meaning: "stop reading", trit: -1 },
  ],
  inductive_bias: 0.7,  # Favors first parse
  pun_strength: 0.3     # Second parse activation
}
```

### Phonetic Decomposition

```ruby
# "Time flies like an arrow. Fruit flies like a banana."
{
  surface: "flies like",
  decompositions: [
    { parse: ["flies", "like"], pos: ["verb", "prep"], trit: 1 },
    { parse: ["flies", "like"], pos: ["noun", "verb"], trit: -1 },
  ],
  gestalt_principle: :figure_ground,
  context_switch: "arrow → banana"
}
```

### Etymological Decomposition

```ruby
# From the reflow skill:
{
  word: "trimester",
  decomposition: ["tri-", "mester"],
  trits: [0, 0],
  gf3_sum: 0,  # Balanced!
  resonance: :strong
}

{
  word: "semester", 
  decomposition: ["se-", "mester"],  # se- = six (2×3)
  trits: [0, 0],
  gf3_sum: 0,  # Also balanced via factorization
  resonance: :moderate
}
```

## ACSet Schema for Puns

```julia
@present SchPun(FreeSchema) begin
  Surface::Ob
  Parse::Ob
  Morpheme::Ob
  Meaning::Ob
  
  surface::Hom(Parse, Surface)
  morphemes::Hom(Morpheme, Parse)
  meaning::Hom(Parse, Meaning)
  
  # Attributes
  Text::AttrType
  Trit::AttrType
  Bias::AttrType
  
  text::Attr(Surface, Text)
  trit::Attr(Parse, Trit)
  bias::Attr(Parse, Bias)
end

@acset_type Pun(SchPun, index=[:surface, :meaning])
```

## Inductive Bias as Prior

The inductive bias determines which decomposition is "default":

```
P(parse₁ | surface) = softmax(bias₁ / τ)
P(parse₂ | surface) = softmax(bias₂ / τ)

where τ = temperature (context sensitivity)
```

At low temperature (focused context), one parse dominates.
At high temperature (open context), multiple parses activate → PUN.

## OpenGame Structure

From gestalt hacking thread:

```
┌─────────────────────────────────────────────────────────┐
│  PunGame ∆                                              │
│  ─────────────────────────────────────────────────────  │
│  play     :: Surface → ∆ [Parse]     ← enumerate parses │
│  evaluate :: [Parse] → Meaning       ← select by context│
│                                                         │
│  Pun = play produces multiple; evaluate oscillates      │
└─────────────────────────────────────────────────────────┘
```

## Defense: 2-Poisson Disambiguation

When puns attack comprehension, use stochastic sampling:

```rust
impl PunDefender {
    fn disambiguate(&mut self, surface: &str) -> Parse {
        let parses = self.decompose(surface);
        
        if parses.len() > 1 {
            // Multiple valid parses detected
            let (_, selected) = self.poisson.next_arrival(0.0);
            // Use Poisson timing to break tie
            parses[selected.to_usize() % parses.len()].clone()
        } else {
            parses[0].clone()
        }
    }
}
```

## LMBIH Seed Integration

Using the LMBIH seed (327833753928) for pun coloring:

```ruby
# XIP-7074D4: LMBIH Etymological Resonance
seed = 327833753928  # "LMBIH".bytes → hex
index = 43

color_at(seed, index)  # => #7074D4 (purple-blue)

# The pun lives in the purple-blue spectrum:
# - Blue = validation (checking parses)
# - Purple = blend of generation + validation
```

## Commands

```bash
just pun-decompose "time flies"     # Enumerate parses
just pun-triad gestalt acsets       # Show GF(3) triad
just pun-bias 0.7                   # Set inductive bias
just pun-attack closure             # Test gestalt attack
```

## Related Skills

- **gestalt-hacking** (left neighbor): Perceptual grouping exploitation
- **acsets** (right neighbor): Schema-aware decomposition storage
- **reflow**: Cross-context meaning preservation
- **three-match**: Colored subgraph isomorphism for parse matching
- **etymological-resonance**: Morpheme-level decomposition

## Files

- [etymological_resonance.rb](file:///Users/bob/ies/music-topos/lib/etymological_resonance.rb)
- [gestalt hacking thread](https://ampcode.com/threads/T-019b3e8d-1ab1-7548-ab74-fdd531cda57f)
- [chromatic verifier thread](https://ampcode.com/threads/T-019b0ce1-815d-773b-b2ce-f5ef9b26e48d)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `algorithms`: 19 citations in bib.duckdb

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