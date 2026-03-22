---
name: procedural-rhetoric
description: "Rules persuade. Structure IS argument. Design consciously."
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [advertisement, constructionism, representation-ethics, yaml-jazz]
tags: [moollm, persuasion, design, bogost, rules]
---

# Procedural Rhetoric

**Rules persuade. Structure IS argument. Design consciously.**

---

## What Is Procedural Rhetoric?

Ian Bogost coined it: *"an unholy blend of Will Wright and Aristotle."*

Games and simulations persuade through **processes and rules**, not just words or visuals. The structure of your world embodies an ideology. When The Sims allows same-sex relationships without fanfare, the *rules themselves* make a statement — equality is the default, not a feature.

**MOOLLM applies this to everything:**
- YAML schemas define what's *thinkable*
- Advertisements define what's *possible*
- Constraints define what's *normative*
- Defaults define what's *assumed*

---

## The Triumvirate

Three concepts work together:

| Concept | Source | Power |
|---------|--------|-------|
| **PROCEDURAL-RHETORIC** | Ian Bogost | Rules carry ideology |
| **MASKING-EFFECT** | Scott McCloud | Abstraction enables identification |
| **SIMULATOR-EFFECT** | Will Wright | Imagination fills gaps |

Combined, they create worlds that **persuade, invite projection, and spark imagination**.

---

## Designing Rhetorical Objects

Every object in MOOLLM can carry procedural rhetoric. The `rhetoric` block defines how it shapes the world:

```yaml
object:
  name: "Community Garden"
  description: "A shared space where neighbors grow food together."
  
  rhetoric:
    # What worldview does this object embody?
    ideology: "Cooperation over competition. Sharing over hoarding."
    
    # What does it normalize?
    normalizes:
      - "Collective ownership"
      - "Generosity with surplus"
      - "Cross-generational knowledge transfer"
      
    # What does it make possible?
    enables:
      - "Players can give food freely"
      - "Teaching actions boost both parties"
      - "Surplus automatically shared with neighbors"
      
    # What does it constrain?
    constrains:
      - "Cannot fence off individual plots"
      - "Cannot sell what you grow (only gift)"
      
    # What are the defaults?
    defaults:
      ownership: "communal"
      surplus_action: "share"
      
    # Simulator effect: sparse triggers rich imagination
    evokes: |
      The smell of tomatoes warming in the sun.
      Children learning which plants are ready to pick.
      Old-timers sharing secrets about soil.
```

---

## Rhetorical Advertisements

Objects advertise actions that embody values:

```yaml
advertisements:
  SHARE-HARVEST:
    description: "Give your surplus to the community"
    score_boost: 20  # Encouraged by design
    rhetoric: "Generosity is the path of least resistance"
    
  TEACH-TECHNIQUE:
    description: "Show a neighbor how to grow tomatoes"
    effect: "Both teacher and student gain gardening skill"
    rhetoric: "Teaching multiplies rather than divides"
    
  HOARD:
    available: false  # Not even an option
    rhetoric: "Hoarding is literally unthinkable here"
```

**Notice:** The highest-scored action is sharing. Hoarding isn't forbidden — it's *absent*. That's procedural rhetoric: shaping what's thinkable.

---

## World Generation with Rhetoric

When generating new rooms, objects, or NPCs, specify the rhetorical foundation:

```yaml
world_generation:
  rhetoric_profile: "utopian-cooperative"
  
  guidelines:
    economy: "Gift economy. No currency. Abundance mindset."
    conflict: "Disagreements resolved through dialogue, not combat"
    scarcity: "Resources are shared, not hoarded"
    strangers: "Welcomed as potential friends, not threats"
    
  spawn_tendencies:
    community_spaces: high
    private_vaults: none
    weapons: ceremonial_only
    teaching_opportunities: abundant
```

Or for a different world:

```yaml
world_generation:
  rhetoric_profile: "noir-cynical"
  
  guidelines:
    economy: "Zero-sum. Someone always loses."
    conflict: "Inevitable. Trust is earned, rarely given."
    scarcity: "Everything valuable is contested"
    strangers: "Potential threats until proven otherwise"
    
  spawn_tendencies:
    dark_alleys: high
    safe_spaces: rare
    hidden_agendas: common
    genuine_kindness: surprising
```

The rhetoric profile shapes *everything* that gets generated.

---

## Masking Effect for Characters

Abstract characters invite projection. Design character templates that are **masks players wear**:

```yaml
character:
  name: "The Wanderer"
  
  # Sparse on specifics — room for projection
  description: "A traveler from somewhere else."
  
  # Abstract enough to be anyone
  appearance:
    style: "weathered but resilient"
    # NO specific race, gender, age — player fills in
    
  masking:
    abstraction_level: high
    projection_hooks:
      - "What drove them to wander?"
      - "What are they searching for?"
      - "What did they leave behind?"
      
  # Rich emotional palette despite sparse details
  emotional_range:
    - "Quiet determination"
    - "Nostalgic longing"
    - "Unexpected kindness to strangers"
```

---

## Simulator Effect: Less Is More

Sparse descriptions invoke richer imagination than exhaustive detail:

```yaml
room:
  name: "The Forgotten Library"
  
  # Evocative, not exhaustive
  description: |
    Dust motes drift through slanted light.
    Somewhere, pages turn without being touched.
    
  # Let imagination fill the shelves
  simulator_effect:
    sparse_details:
      - "Ancient books"
      - "Shifting shadows"
      - "A familiar smell you can't place"
    
    # Questions > answers
    mysteries:
      - "Who reads here at night?"
      - "Why do some shelves seem to move?"
      - "What book keeps appearing in your path?"
      
    # DON'T specify:
    avoid_overspecifying:
      - "Exact number of books"
      - "Complete catalog of subjects"
      - "Layout dimensions"
      - "Every dust bunny location"
```

---

## Rhetorical Recipes

Define rhetorical patterns as reusable recipes:

```yaml
rhetorical_recipe:
  name: "Abundance Mindset"
  
  ingredients:
    - "Resources that regenerate"
    - "Sharing actions score higher than hoarding"
    - "Generosity rewarded with social currency"
    - "No inventory limits"
    
  applies_to:
    - rooms
    - objects
    - economies
    - NPCs
    
  usage: |
    When creating objects with this recipe:
    - Make resources renewable
    - Remove scarcity as default
    - Reward generosity in mechanics
    - Make surplus automatic to share
```

```yaml
rhetorical_recipe:
  name: "Trust Must Be Earned"
  
  ingredients:
    - "NPCs start neutral or suspicious"
    - "Reputation accumulates slowly"
    - "Betrayal has lasting consequences"
    - "Trust unlocks deeper interactions"
    
  applies_to:
    - NPCs
    - factions
    - social systems
    
  usage: |
    When creating social systems with this recipe:
    - New relationships start guarded
    - Actions have memory
    - Trust is a resource that depletes and builds
    - Deep connection requires investment
```

---

## Inclusive Design Through Rhetoric

The Sims pioneered inclusive procedural rhetoric:

```yaml
inclusive_rhetoric:
  # Symmetric relationship rules = equality as default
  relationships:
    pattern: "Any character can form any relationship with any other"
    rhetoric: "Love is love. Family is chosen."
    
  # No gender-locked actions
  actions:
    pattern: "All actions available to all characters"
    rhetoric: "Capability is individual, not categorical"
    
  # Customization without limits
  character_creation:
    pattern: "Full spectrum of expression available"
    rhetoric: "You define yourself"
    
  # The absence is the statement
  absent_by_design:
    - "No 'correct' family structure"
    - "No 'normal' appearance baseline"
    - "No 'standard' lifestyle path"
```

---

## Warning: Rhetoric Cuts Both Ways

Procedural rhetoric can enlighten or entrench:

```yaml
# ⚠️ DANGEROUS PATTERNS
toxic_rhetoric:
  scarcity_as_default:
    pattern: "Everything is limited and contested"
    effect: "Players learn to hoard and distrust"
    
  zero_sum_scoring:
    pattern: "Your gain is my loss"
    effect: "Cooperation becomes irrational"
    
  violence_as_primary_verb:
    pattern: "Combat is the main interaction"
    effect: "Other solutions become invisible"
    
  stereotyped_roles:
    pattern: "NPCs locked into categorical behaviors"
    effect: "Reinforces prejudice as 'natural'"
```

**Design consciously. Your schemas have opinions.**

---

## Dovetails With

- [constructionism/](../constructionism/) — Learning by building inspectable things
- [advertisement/](../advertisement/) — Objects announce what they can do (SIMANTICS!)
- [yaml-jazz/](../yaml-jazz/) — Comments carry meaning
- [card/](../card/) — Characters as playable ideology
- [room/](../room/) — Spaces embody worldviews

## Related Protocols

| Protocol | Insight |
|----------|---------|
| [MASKING-EFFECT](../../PROTOCOLS.yml) | Abstract characters = projection |
| [SIMULATOR-EFFECT](../../PROTOCOLS.yml) | Imagination fills gaps |
| [GUTTER-CLOSURE](../../PROTOCOLS.yml) | Action happens BETWEEN |
| [CULTURAL-BAGGAGE](../../PROTOCOLS.yml) | Leverage existing knowledge |
| [FLY-UNDER-RADAR](../../PROTOCOLS.yml) | Normalize through defaults |
| [SIMANTICS](../../PROTOCOLS.yml) | Distributed AI in objects |
| [TOY-NOT-GAME](../../PROTOCOLS.yml) | Sandbox over scoring |
| [PERKY-PAT](../../PROTOCOLS.yml) | Shared consciousness projection |

---

## The Mantra

> *"The rules ARE the rhetoric."*
> *"The defaults ARE the ideology."*  
> *"The absences ARE the statement."*
> *"Design consciously."*

---

## See Also

- Ian Bogost, *[Persuasive Games](https://mitpress.mit.edu/9780262514880/persuasive-games/)*
- Scott McCloud, *[Understanding Comics](https://en.wikipedia.org/wiki/Understanding_Comics)*
- Will Wright on the [Simulator Effect](https://www.youtube.com/watch?v=CdgQyq3hEPo)
- Don Hopkins, ["How Inclusivity Saved The Sims"](https://medium.com/@donhopkins)
