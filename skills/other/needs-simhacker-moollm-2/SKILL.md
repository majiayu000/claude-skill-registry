---
name: needs
description: Dynamic motivations (Sims-style) — needs fluctuate and drive behavior
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
scale:
  range: "0-10"
  meaning:
    10: "Fully satisfied"
    7-9: "Comfortable"
    4-6: "Manageable"
    2-3: "Urgent"
    0-1: "Critical"
standard_needs:
  - hunger
  - energy
  - fun
  - social
  - comfort
  - bladder
related: [simulation, society-of-mind, time, buff, character, cat, dog, yaml-jazz, advertisement]
tags: [moollm, sims, motives, behavior, autonomy, game]
---

# Needs Skill

Dynamic motivations (Sims-style).

**Motto:** *"Needs drive the story. Low needs create urgency."*

## Key Concepts

- **Scale** — 0-10 (10 = fully satisfied)
- **Decay** — Needs decrease over time
- **Urgency** — Low needs interrupt other activities
- **Inner voice** — YAML Jazz comments reflect mental state

## Standard Needs

| Need | Decay | Satisfy | Critical |
|------|-------|---------|----------|
| Hunger | 2 hours | EAT, DRINK | 2 |
| Energy | 3 hours | SLEEP, REST | 2 |
| Fun | 4 hours | PLAY, GAMES | 3 |
| Social | 6 hours | TALK, hang out | 3 |
| Comfort | Situational | Safe place | 4 |
| Bladder | 4 hours | Use bathroom | 1 |

## Inner Voice (YAML Jazz)

```yaml
hunger: 7   # Satisfied. No food thoughts.
hunger: 3   # Getting peckish. Is that pie?
hunger: 1   # FOOD. FOOD. FOOD. FOOD.
```

## See Also

- [time](../time/) — Needs decay over simulation turns
- [buff](../buff/) — Some buffs affect need decay
- [character](../character/) — Needs stored in character

## Full Protocol

```yaml
# Needs Skill — Dynamic Motivations (Sims-Style)
# Needs fluctuate over time and drive behavior.

skill:
  name: needs
  tier: 1
  protocol: NEEDS-AS-MOTIVATION
  description: |
    Needs fluctuate over time and drive behavior.
    Low needs create urgency. Satisfied needs enable other activities.
    Comments update to reflect inner voice.
  motto: "Needs drive the story. Low needs create urgency."

# SCALE

scale:
  range: "0-10"
  meaning:
    10: "Fully satisfied"
    7-9: "Comfortable"
    4-6: "Manageable"
    2-3: "Urgent"
    0-1: "Critical"

# STANDARD NEEDS

standard_needs:
  hunger:
    decay_rate: "-1 per 2 hours"
    satisfy: ["EAT", "DRINK"]
    low_effects: ["distraction", "irritability", "food fixation"]
    critical_at: 2
    
  energy:
    decay_rate: "-1 per 3 hours (faster if Active high)"
    satisfy: ["SLEEP", "REST", "coffee (temporary)"]
    low_effects: ["reduced effectiveness", "yawning", "sluggishness"]
    critical_at: 2
    
  fun:
    decay_rate: "-1 per 4 hours"
    satisfy: ["PLAY", "GAMES", "social", "exploration"]
    low_effects: ["boredom", "restlessness", "seeking novelty"]
    critical_at: 3
    
  social:
    decay_rate: "-1 per 6 hours (varies by Outgoing)"
    satisfy: ["TALK", "hang out", "party"]
    low_effects: ["loneliness", "craving conversation"]
    critical_at: 3
    
  comfort:
    decay_rate: "Situational (environment-dependent)"
    satisfy: ["Safe location", "familiar place", "cozy setting"]
    low_effects: ["anxiety", "restlessness", "seeking home"]
    critical_at: 4
    
  bladder:
    decay_rate: "-1 per 4 hours"
    satisfy: ["Use bathroom"]
    low_effects: ["urgency", "distraction", "accident risk"]
    critical_at: 1

# INNER VOICE (YAML Jazz)

yaml_jazz_comments:
  description: |
    Need values have DYNAMIC COMMENTS that serve as inner voice.
    Comments update when values change!
    
  examples:
    hunger:
      high: "hunger: 7  # Satisfied. No food thoughts."
      medium: "hunger: 5  # Could eat. Not urgent."
      low: "hunger: 3  # Getting peckish. Is that pie?"
      critical: "hunger: 1  # FOOD. FOOD. FOOD. FOOD."
      
    energy:
      high: "energy: 8  # Wide awake. Let's DO things."
      medium: "energy: 5  # Fine. Maybe coffee later."
      low: "energy: 2  # So tired. Everything is hard."
      critical: "energy: 1  # Can't... keep... eyes..."
      
    social:
      high: "social: 9  # People are great. I love everyone."
      medium: "social: 5  # Could use a chat."
      low: "social: 2  # Is anyone there? Hello?"

# DECAY

decay:
  timing: "Needs decay over simulation turns"
  factors:
    - "Base decay rate"
    - "Personality traits (Active, Outgoing)"
    - "Current location effects"
    - "Active buffs"
    - "Dribble food to bladder"

# SATISFACTION

satisfaction:
  actions: "Most needs satisfied by specific actions"
  locations: "Some locations satisfy needs passively (home, pub)"
  items: "Some items satisfy needs (food, bed)"
  social: "Interactions can satisfy social need"

# CRITICAL NEEDS

critical_needs:
  description: |
    When a need hits critical level, behavior changes:
    - Inner voice becomes URGENT
    - Other activities interrupted
    - May trigger autonomous actions
    
  example: |
    hunger: 1
    # I CAN'T THINK ABOUT ANYTHING ELSE
    # IS THERE FOOD? WHERE IS FOOD?
    # [Character may abandon current task to find food]

integrates_with:
  - skill: character
    how: "Needs stored in character state"
  - skill: time
    how: "Needs decay over simulation turns"
  - skill: buff
    how: "Some buffs affect need decay rates"
  - skill: room
    how: "Locations can satisfy needs"
```