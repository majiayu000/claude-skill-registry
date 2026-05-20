---
name: reward
description: "Motto: Rewards should feel earned and fitting."
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [scoring, buff, hero-story, adventure]
tags: [moollm, achievement, prizes, narrative, game]
---

# Reward Protocol

> Dynamic achievement rewards — the treasure matches the quest.
> *"Rewards should feel earned and fitting."*

## Core Principle

**Thematic Appropriateness**

Rewards match achievements:
- Slay a dragon → dragon-themed rewards (scales, hoard, reputation)
- Save a village → village's gratitude (shelter, allies, title)
- Solve a puzzle → knowledge rewards (secrets, techniques, lore)

## Reward Types

| Type | Examples | When Granted |
|------|----------|--------------|
| **Items** | Weapons, tools, treasures | Combat, exploration |
| **Gold** | Currency, valuables | Commerce, quests |
| **Buffs** | Temporary powers | Heroic moments |
| **Titles** | LIGHT-BEARER, DRAGON-SLAYER | Major achievements |
| **Abilities** | New skills, techniques | Learning, training |
| **Access** | Keys, permissions, trust | Social achievements |
| **Knowledge** | Secrets, lore, maps | Investigation |
| **Heirlooms** | Items with history | Generational play |

## Methods

### GRANT - Give a Reward

```yaml
invoke: GRANT
params:
  recipient: "Who gets it"
  achievement: "What they did"
  reward: "What they get (or auto-generate)"
effect:
  - Add to recipient's inventory or state
  - Record in achievement log
  - Narrate the granting
```

### GENERATE - Create Thematic Reward

```yaml
invoke: GENERATE
params:
  achievement: "What was accomplished"
  context: "Where and how"
effect:
  - Analyze achievement theme
  - Generate appropriate reward
  - Propose with justification
```

## Reward Generation Logic

```
Achievement: "Rescued the blacksmith from the fire"
Context: Village fire, heroic action

Thematic analysis:
  - Fire → fire-related items?
  - Blacksmith → smithing reward?
  - Heroic → reputation boost?

Generated rewards:
  1. Fireproof cloak (practical, thematic)
  2. Free repairs for life (relationship)
  3. Title: FLAME-WALKER (reputation)
  4. Secret: location of rare ore (knowledge)
```

## Scaling Rewards

| Achievement Level | Reward Scale |
|-------------------|--------------|
| Minor task | Small token, few coins |
| Significant quest | Useful item, title |
| Major accomplishment | Powerful item, ability |
| Legendary feat | Unique artifact, lasting fame |

## Curse Lifting Rewards

When curses are lifted, special rewards apply:

```yaml
curse:
  name: "Curse of Darkness"
  lift_condition: "Light 3 dark places"
  
reward_on_lift:
  - title: "LIGHT-BEARER"
  - ability: "Glow in darkness"
  - knowledge: "Location of the Shadow Temple"
```

## Delayed Rewards

Some rewards mature over time:

```yaml
delayed_reward:
  type: "Planted seed"
  matures: "After 3 game days"
  becomes: "Magical fruit tree"
  
relationship_reward:
  type: "Merchant's favor"
  grows_with: "Repeated business"
  becomes: "Exclusive supplier"
```

## State

```yaml
reward_state:
  earned_rewards: []
  pending_rewards: []
  titles: []
  achievements_log:
    - date: "2026-01-15"
      achievement: "Rescued the blacksmith"
      reward: "Fireproof cloak"
```

## Integration

| Skill | Integration |
|-------|-------------|
| **scoring** | Score determines reward quality |
| **buff** | Some rewards are buffs |
| **economy** | Gold rewards |
| **character** | Rewards update character state |
| **adventure** | Quest completion triggers rewards |

## Safety Guidelines

- **Proportional** — reward matches difficulty
- **Consistent** — similar achievements, similar rewards
- **Meaningful** — rewards should matter to the story
- **No inflation** — keep rewards valuable

## Example Session

```
> [Player completes fire rescue quest]

GENERATE: achievement="rescued blacksmith from fire"

Analysis:
- Heroic action in dangerous situation
- Relationship established with craftsman
- Fire element prominent

Proposed rewards:
1. 🛡️ Fireproof Cloak - practical protection
2. 🔨 Free Smithing - relationship benefit
3. 🏆 Title: FLAME-WALKER - reputation

Which feels right for this character?
```
