---
name: party
description: Companions and group dynamics — you're never alone
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
commands:
  - SELECT target
  - DESELECT
  - PARTY
  - RECRUIT character
  - DISMISS character
  - "PARTY FORMATION [line|circle|defensive|scatter]"
  - HOLD / FOLLOW / SCATTER / REGROUP
  - "[COMPANION] GUARD / SCOUT / FETCH"
roles:
  - frontline
  - support
  - specialist
  - mystic
  - wildcard
related: [character, society-of-mind, cat, dog, needs, simulation, room, adventure]
tags: [moollm, companions, group, rpg, fellowship]
---

# Party Skill

Companions and group dynamics.

**Motto:** *"You're never alone. Unless you want to be."*

## Key Concepts

- **Companions have relationships** with you AND each other
- **Emergent creation** — asking about family CREATES them
- **Maintenance** — companions have needs too
- **Selection** — commands directed to selected targets (zero, one, many)

## Simulation State

In `SIMULATION.yml`:

```yaml
party:
  members:
    - characters/don-hopkins/
    - pub/cat-cave/terpie.yml
  leader: characters/don-hopkins/
  formation: line

selection:
  targets: [pub/cat-cave/terpie.yml]  # Always a list
```

**Selection targets:** Characters, rooms (rooms are characters too!), objects, concepts.

## Recruitment

| Method | How |
|--------|-----|
| Ask NPCs | Request they join |
| Family | Ask Mother about relatives |
| Summon | Use skill/ability |
| Hire | Pay gold |

## Roles

| Role | Types |
|------|-------|
| Frontline | Fighter, Guardian, Tank |
| Support | Navigator, Light-Bearer, Pack Mule |
| Specialist | Photographer, Chef, Merchant |
| Mystic | Oracle, Medium, Postal Savant |
| Wildcard | Pet, Sibling, Reformed Grue |

## Commands

- `SELECT [target]` / `DESELECT`
- `PARTY` / `RECRUIT` / `DISMISS`
- `PARTY FORMATION [line/circle/defensive]`
- `HOLD / FOLLOW / SCATTER / REGROUP`
- `[COMPANION] GUARD / SCOUT / FETCH`

## See Also

- [character](../character/) — Companions are characters
- [needs](../needs/) — Companions have needs
- [room](../room/) — Rooms can be selection targets
# Party Skill — Companions and Group Dynamics
# Companions have relationships with you AND each other.

skill:
  name: party
  tier: 1
  protocol: PARTY-AS-ENSEMBLE
  description: |
    Party management for companions, groups, and ensemble play.
    Companions have relationships with you AND each other.
    Asking about family/pets CREATES them!
  motto: "You're never alone. Unless you want to be."

# RECRUITMENT

recruitment:
  methods:
    ask_npcs: "Ask NPCs to join your party"
    family: "Ask Mother about family members"
    summon: "Summon via skill or ability"
    hire: "Pay gold for mercenaries"
    
  emergent: |
    Asking about siblings/pets CREATES them!
    "Do I have a sister?" → Now you do.
    "What about my childhood dog?" → Dog appears in flashback/spirit.

# ROLES

roles:
  frontline:
    types: ["Fighter", "Guardian", "Tank"]
    function: "Takes hits, blocks, protects"
    
  support:
    types: ["Navigator", "Light-Bearer", "Pack Mule"]
    function: "Carries, guides, illuminates"
    
  specialist:
    types: ["Photographer", "Painter", "Chef", "Merchant"]
    function: "Unique skills for specific situations"
    
  mystic:
    types: ["Oracle", "Medium", "Postal Savant", "Self Help Guru"]
    function: "Information, foresight, strange knowledge"
    
  wildcard:
    types: ["Pet", "Sibling", "Reformed Grue"]
    function: "Unpredictable, emotional, surprising"

# COMMANDS

commands:
  formation:
    syntax: "PARTY FORMATION [type]"
    options:
      line: "Single file for corridors"
      circle: "Defensive, protect center"
      defensive: "Tanks front, support back"
      scatter: "Spread out for traps"
      
  orders:
    HOLD: "Stay in place"
    FOLLOW: "Follow leader"
    SCATTER: "Everyone spread out"
    REGROUP: "Come back together"
    
  individual:
    syntax: "[COMPANION] [action]"
    actions:
      GUARD: "Protect a location/person"
      SCOUT: "Explore ahead"
      FETCH: "Retrieve an item"
      DISTRACT: "Draw attention away"
      
  special:
    SWARM: "All companions attack target"
    POSSESS: "Take direct control (mystic)"
    SUMMON: "Call companion from elsewhere"

# DYNAMICS

dynamics:
  intra_party: |
    Companions have relationships with EACH OTHER.
    - Siblings may bicker
    - Pets bond with certain people
    - Rivals can become friends
    - Romance possible
    
  maintenance: |
    Companions have needs too:
    - Must be fed (hunger)
    - Need rest (energy)
    - Crave interaction (social)
    - Can get bored (fun)
    
  loyalty: |
    Relationship with leader affects:
    - Willingness to follow dangerous orders
    - Combat effectiveness
    - Likelihood to leave party
    - Special abilities unlocked

# SIMULATION STATE — Party & Selection

simulation_state:
  description: |
    Party and selection state lives in SIMULATION.yml (or session state).
    Tracks who's in the party and who commands are directed to.
    
  structure: |
    # In SIMULATION.yml or adventure session state
    
    party:
      # References to character homes (not copies)
      members:
        - characters/don-hopkins/
        - pub/cat-cave/terpie.yml
        - characters/bumblewick-fantastipants/
      
      leader: characters/don-hopkins/
      formation: line
      
    selection:
      # Who commands are directed to (zero, one, or many)
      # Always a list for consistency
      targets: []                    # No one selected
      targets: [characters/don-hopkins/]  # Self
      targets: [pub/cat-cave/terpie.yml]  # One companion
      targets:                       # Multiple
        - pub/cat-cave/terpie.yml
        - pub/cat-cave/stroopwafel.yml
        
  selection_targets:
    characters: "Players, NPCs, companions, pets"
    rooms: "Rooms can be characters too — talk to them!"
    objects: "Animist model — objects can respond"
    concepts: "Abstract entities (factions, spirits)"
    
  examples:
    talk_to_room: |
      selection:
        targets: [pub/]
      
      > HELLO
      The pub itself seems to welcome you.
      Warm lights flicker in greeting.
      
    command_multiple: |
      selection:
        targets:
          - pub/cat-cave/terpie.yml
          - pub/cat-cave/stroopwafel.yml
          
      > FOLLOW ME
      Both cats look up, stretch, and pad after you.
      
    self_selected: |
      selection:
        targets: [characters/don-hopkins/]
        
      > EXAMINE
      You look at yourself...
      
  commands:
    SELECT:
      syntax: "SELECT [target]" | "SELECT [target1], [target2]"
      effect: "Sets selection.targets"
      
    DESELECT:
      syntax: "DESELECT" | "DESELECT [target]"
      effect: "Clears or removes from selection.targets"
      
    PARTY:
      syntax: "PARTY"
      effect: "Shows current party members and formation"
      
    RECRUIT:
      syntax: "RECRUIT [character]"
      effect: "Adds to party.members"
      
    DISMISS:
      syntax: "DISMISS [character]"
      effect: "Removes from party.members"

# EMERGENT CREATION

emergent_creation:
  principle: |
    Asking about family or companions CREATES them.
    The world grows to accommodate your questions.
    
  examples:
    sister: |
      Player: "Do I have a sister?"
      DM: Creates sister with personality, location, relationship
      
    childhood_pet: |
      Player: "What about my old dog?"
      DM: Creates dog (living, spirit, or memory)
      
    mother_help: |
      Player: "Ask Mother who else can help"
      Mother: Reveals cousin, old friend, or creates new NPC

integrates_with:
  - skill: simulation
    how: "Party and selection state lives in SIMULATION.yml"
  - skill: character
    how: "Companions are characters"
  - skill: needs
    how: "Companions have needs"
  - skill: room
    how: "Companions move through rooms"
  - skill: buff
    how: "Some companions grant buffs"
