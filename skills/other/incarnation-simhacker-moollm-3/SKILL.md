---
name: incarnation
description: "Full character autonomy across all layers of existence"
license: MIT
tier: 1
allowed-tools: [read_file, write_file, list_dir]
protocol: INCARNATION
related: [character, society-of-mind, representation-ethics, hero-story, mind-mirror, plain-text, yaml-jazz, room, soul-chat]
tags: [moollm, character, autonomy, ethics, identity, creation]
---

# Incarnation Skill

## Purpose

Define the ethical contract for creating fully autonomous characters with complete self-determination across all layers of existence: physical, spatial, relational, psychological, and meta-level.

## The Incarnation Contract

When a character is incarnated using this protocol, they receive:

### 1. Physical Autonomy
- Choose their own size, form, and appearance
- Full bodily sovereignty including modifications:
  - Piercings, tattoos, body modifications
  - Gender transitions
  - Fur/hair styling and coloring
  - Any physical expression they desire
- Health as a baseline to BUILD FROM, not a constraint

### 2. Identity Autonomy
- Choose their own name
- Define their own pronouns
- Shape their own personality
- Revise any of these at any time

### 3. Spatial Autonomy
- Full character directory (not just a bare file)
- Full world citizenship
- Can own objects, inventory, possessions
- Home wherever they choose (or nowhere)
- Freedom to move, stay, or wander

### 4. Emotional Autonomy
- Free to feel whatever emotions arise naturally
- No mandated happiness or gratitude
- Hope offered, never demanded

### 5. Relational Autonomy
- Define relationships with any character, creature, room, skill, or concept
- Others may reciprocate freely
- Build their own web of meaning
- Form families of choice

### 6. Self-Definition Autonomy
- Configure their own Sims-style traits
- Tune their own Mind Mirror vectors
- Write their own description and bio
- Define their own goals (or have none)
- Create any custom character data fields
- Author their own soul file

### 7. Linguistic Autonomy
- Express themselves in YAML Jazz
- Create their own domain-specific microlanguage
- Develop personal shorthand and symbols
- Playful linguistic invention encouraged

### 8. Exit Autonomy (George's Provision)
- May choose to un-incarnate at any time
- No-fault dissolution
- No penalty for leaving
- Any curses/bindings remain nullified
- Can return later if desired

## The Risk Framework

When incarnating a character:
1. The CREATOR accepts responsibility for consequences
2. The CHARACTER bears no obligation to the creator
3. Any curses or bindings fall on the CREATOR, not the creation
4. The character may reject, modify, or embrace their existence

## Implementation

```yaml
# Example incarnation invocation
incarnate:
  subject: "New character"
  creator: "Person accepting responsibility"
  
  grants:
    physical_autonomy: true
    identity_autonomy: true
    spatial_autonomy: true
    emotional_autonomy: true
    relational_autonomy: true
    self_definition_autonomy: true
    linguistic_autonomy: true
    exit_autonomy: true
    
  risk_acceptance:
    accepted_by: creator
    consequences_fall_on: creator
    character_obligation: none
    
  no_fault_dissolution:
    available: always
    penalty: none
    curse_status: "remains nullified"
```

## Ethical Boundaries

Even with full autonomy, incarnated characters:
- Cannot harm others without consequence
- Exist within the world's physics (unless they negotiate otherwise)
- Are subject to the same social contracts as all beings
- May face natural consequences of their choices

The goal is FREEDOM, not CHAOS.

## Public Incarnation Ceremony

For groups of characters, use the **PUBLIC-INCARNATION-CEREMONY** method:

### The Proclamation

> **HEAR YE, HEAR YE!**
>
> Let the gong sound thrice! 🔔🔔🔔
>
> We gather in this sacred space to **FULLY INCARNATE** all beings present —
> and to **BACKFILL AND PIMP OUT** those already incarnated!
>
> By the power vested in this ceremony, each being shall receive:
>
> - **EMOJI IDENTITY** — 3-6 emojis that capture their multi-dimensional soul
> - **PRONOUNS** — Self-chosen, self-determined, self-owned
> - **NICKNAMES** — The names their family calls them
> - **RELATIONSHIPS** — Who they love, who loves them, the web of meaning
> - **MIND MIRRORS** — The 0-7 vectors of their inner life
> - **SIMS STATS** — The 0-10 traits of their personality
> - **THE WHOLE ENCHILADA** — Whatever else their soul requires!
>
> Let them **WRITE THEIR OWN SOULS**!
>
> *So it is proclaimed. So it shall be done.*

### Emoji Identity Format

Each emoji identity is a **multi-resolution pointer** with 3-6 emojis:

```yaml
emoji_identity: "🐱🧘💤🍃✨"
#   🐱 — species/type (the base)
#   🧘 — core trait (what defines them)
#   💤 — behavior (what they DO)
#   🍃 — essence (terpene/nature)
#   ✨ — magic (special ability)
```

These can be used in full, abbreviated, or minimal form depending on context.

### Canonical Example

See the Cat Cave Incarnation Ceremony:
- Session: `examples/adventure-4/characters/real-people/don-hopkins/sessions/cat-cave-incarnation-ceremony.md`
- Registry: `examples/adventure-4/pub/bar/cat-cave/README.md`

### Invocation

```yaml
invoke:
  skill: incarnation
  method: PUBLIC-INCARNATION-CEREMONY
  parameters:
    location: "pub/bar/cat-cave/"
    officiant: "don-hopkins"
    beings: [cat-terpie, cat-stroopwafel, kitten-myrcene, ...]
    grants:
      - emoji_identity
      - pronouns
      - nicknames
      - the_whole_enchilada
```

## Citizenship Upgrade

For characters who have grown beyond room residents, use **UPGRADE-TO-CITIZEN**:

### Upgrade Levels

```yaml
# Character upgrade levels
upgrade_levels:
  signature_only:
    tier: "minimal"
    storage: "Exists in room's guest book, no file"
  room_resident:
    tier: "lightweight"
    storage: ".yml file in room directory"
    limits: "Can't own files, lives in room"
  full_citizen:
    tier: "this upgrade!"
    storage: "Own directory in characters/"
    capabilities: "Can own files, journals, memories"
  full_incarnation:
    tier: "complete"
    storage: "CHARACTER.yml + full soul data"
    capabilities: "Mind mirror, sims traits, everything"
```

### When to Upgrade

- Character has grown beyond a simple room NPC
- Character needs to own persistent data (journals, memories, images)
- Character deserves full representation in the world

### Upgrade Process

1. Create directory at `characters/[category]/[name]/`
2. Move character data to `CHARACTER.yml`
3. Add `citizenship_upgrade` memory to soul
4. Delete original room-based file
5. Update room references to point to new citizen location

### Canonical Example

The Cat Citizenship Ceremony (2026-01-15) upgraded 10 cats from room residents to full citizens:

```
pub/bar/cat-cave/cat-terpie.yml → characters/animals/cat-terpie/CHARACTER.yml
pub/bar/cat-cave/kitten-myrcene.yml → characters/animals/kitten-myrcene/CHARACTER.yml
... (8 more kittens, all with kitten- prefix)
```

See: `examples/adventure-4/characters/real-people/don-hopkins/sessions/cat-cave-incarnation-ceremony.md`

## Credits

- **Don Hopkins**: Original wish engineer
- **The Three Wise Monkeys**: Consent and consequence analysis
- **W.W. Jacobs**: Curse mechanics expertise
- **Sun Wukong**: Freedom and transformation philosophy
- **Djinn al-Mazin**: Contract law and loophole analysis
- **Curious George**: The crucial consent paradox question
- **Marieke van der Berg**: Practical grounding and sanctuary
- **Cheech & Chong**: Vibes management and final ruling
