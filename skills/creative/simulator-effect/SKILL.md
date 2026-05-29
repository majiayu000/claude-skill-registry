---
name: simulator-effect
description: "Implication beats simulation — imagination renders (Will Wright)"
license: MIT
tier: 0
allowed-tools: [read_file]
protocol: SIMULATOR-EFFECT
related: [moollm, society-of-mind, manufacturing-intelligence, k-lines, yaml-jazz, empathic-templates, constructionism, procedural-rhetoric, mind-mirror, adversarial-committee, speed-of-light, needs]
tags: [moollm, meta, philosophy, sims, design, k-lines, will-wright]
---

# Simulator Effect Skill Specification

> *Implication is more efficient (and richer) than simulation.*

## Purpose

The Simulator Effect skill provides principles and methods for leveraging imagination -- human or LLM -- to fill gaps in sparse specifications. Instead of exhaustive simulation, provide seeds that activate rich mental models.

---

## Core Methods

### IMPLY

Instead of simulating, imply.

**Input:** Minimal specification (name, archetype, sensory details)
**Output:** Rich interpretation filling gaps coherently

```yaml
# Input
character:
  archetype: "grizzled bartender"
  
# LLM interprets as
bartender:
  name: Grim
  appearance: weathered face, salt-and-pepper beard
  manner: laconic, speaks in short sentences
  knowledge: has seen every adventurer who passed through
  secrets: knows where the treasure is, will not say
```

### SEED

Provide imagination seeds rather than exhaustive specification.

**Seed types:**
- **Archetype** -- "bartender", "sage", "trickster"
- **Sensory detail** -- "smells of woodsmoke"
- **Mystery** -- "the locked door no one mentions"
- **Tension** -- "she avoided his gaze"
- **K-line** -- "Sagittarius", "melancholy", "playful"

```yaml
room:
  seeds:
    archetype: "mysterious pub"
    sensory: "warm despite the draft, old ale smell"
    mystery: "the back room that requires proving yourself"
    tension: "regulars glance at newcomers, then away"
```

### SPARSE

Deliberately omit details to invite imagination.

**Anti-pattern:**
```yaml
# Over-specified -- leaves nothing to imagine
room:
  name: The Rusty Lantern
  tables: 12 oak tables, 3 round, 9 rectangular
  chairs: 48 chairs, mix of styles
  bar: 15 feet long, mahogany with brass rail
  taps: 8 beer taps, 2 cider, 1 mead
  lighting: 6 candelabras, 12 wall sconces
  floor: wide oak planks, worn in traffic paths
  # ... 50 more lines
```

**Pattern:**
```yaml
# Sparse -- imagination fills the rest
room:
  name: The Rusty Lantern
  atmosphere: warm despite the draft
  smell: woodsmoke and old ale
  notable: the back room no one talks about
```

### ARCHETYPE

Use cultural archetypes as shorthand for personality packages.

**Archetype categories:**

| Category | Examples | What They Activate |
|----------|----------|-------------------|
| Zodiac | Sagittarius, Cancer | Full personality clusters |
| Role | Bartender, Sage, Trickster | Behavioral expectations |
| Species | Dog, Cat, Monkey | Disposition, physicality |
| Profession | Detective, Librarian, Chef | Knowledge, methods |
| Trope | Grizzled veteran, Naive newcomer | Story function |

```yaml
# One word does the work of a personality matrix
character:
  archetype: sagittarius_explorer
  # Implies: adventurous, philosophical, blunt, optimistic
```

### JAZZ

Use YAML comments as imagination seeds (per [yaml-jazz](../yaml-jazz/)).

```yaml
playful: 9
# not born playful -- BECAME playful by choice
# 122 years of grim taught me joy is rebellion

melancholy: 6
# higher than I first admitted
# the silver streaks glow when I am sad
```

Comments are read by the LLM. They shape interpretation. They are not documentation -- they are code.

---

## The Astrillogical Pattern

Named after The Sims' zodiac implementation (1997):

1. **Compute something minimal** (Euclidean distance to archetype vectors)
2. **Display a cultural symbol** (zodiac icon)
3. **Write no behavioral code**
4. **Let imagination do the rest**

Result: Testers reported the zodiac was "too influential" -- but there was no influence to tune. The effect was purely imagined.

**Application:**

```yaml
# Minimal computation
character:
  personality_vector: [neat: 7, outgoing: 3, playful: 9]
  # Display nearest archetype
  archetype: sagittarius  # Computed, not assigned
  
# No behavioral code referencing 'sagittarius'
# Player/LLM imagines Sagittarius behavior
```

---

## Integration with Other Skills

### With k-lines/

Names activate clusters. Simulator Effect explains why.

```yaml
# K-line activation IS Simulator Effect
character:
  name: Palm  # Activates: open hand, tropical, reaching
```

### With adversarial-committee/

Mode-collapse is Simulator Effect in reverse -- LLM collapses to mean when constraints are absent. Adversarial committee provides constraints through opposing propensities.

```yaml
committee:
  - propensity: paranoid_realism   # Different lens
  - propensity: idealism           # Different lens
  - propensity: evidence_prosecutor # Different lens
  
# Same topic, three different Simulator Effects
# Cross-examination finds robust interpretations
```

### With speed-of-light/

One LLM call, many turns. Imagination fills the "rendering" for each turn. Sparse state, rich narrative.

### With needs/

Sims motives are imagination seeds, not behavior code.

```yaml
needs:
  hunger: 30  # Seed
  # LLM imagines: "distracted by stomach growling"
  # Not: deterministic eat() behavior
```

### With empathic-templates/

Templates leverage Simulator Effect -- provide structure, let LLM fill content.

```yaml
template: |
  [CHARACTER] enters [ROOM] and notices [NOTABLE_DETAIL].
  They feel [EMOTION] because [REASON].
  
# LLM generates coherent fill based on context
```

---

## Failure Modes

### Over-Specification

Too much detail leaves nothing to imagine. The simulation feels mechanical.

**Symptom:** Output feels like a checklist, not a story.
**Fix:** Remove 80% of specification. Keep seeds.

### Under-Seeding

Not enough anchors for imagination to grip.

**Symptom:** Output is generic, could be anyone/anywhere.
**Fix:** Add archetype, sensory detail, or mystery.

### Wrong Archetype

Archetype conflicts with intended behavior.

**Symptom:** Character behaves "off" despite correct specs.
**Fix:** The archetype K-line is overriding your specs. Change the archetype or add explicit counters.

### Mode-Collapse

Single-agent LLM with weak constraints collapses to bland mean.

**Symptom:** Output is safe, inoffensive, boring.
**Fix:** Use adversarial-committee or add tension/conflict seeds.

---

## Metrics

The Simulator Effect is working when:

1. **Readers imagine more than you wrote**
2. **LLM generates coherent detail you did not specify**
3. **Different interpreters imagine similar worlds**
4. **Sparse specs produce rich output**

---

## See Also

- [k-lines/](../k-lines/) -- The mechanism
- [yaml-jazz/](../yaml-jazz/) -- Comments as seeds
- [adversarial-committee/](../adversarial-committee/) -- Mode-collapse antidote
- [empathic-templates/](../empathic-templates/) -- Smart generation
- [constructionism/](../constructionism/) -- Mental model building
- [sims-astrology.md](../../designs/sims/sims-astrology.md) -- The proof

---

*"The game provides scaffolding. Imagination does the rendering."*
