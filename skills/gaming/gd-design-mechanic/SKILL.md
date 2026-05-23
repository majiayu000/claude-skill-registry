---
name: gd-design-mechanic
description: Game mechanics documentation and design. Use when designing core gameplay systems, documenting player actions and responses, balancing game systems, or explaining mechanics to developers.
---

# Game Mechanics Design

## Mechanics Documentation Template

For each mechanic, document:

```markdown
## [Mechanic Name]

### Description
[What the mechanic does in plain language]

### Purpose
[Why this mechanic exists - what player fantasy it fulfills]

### Trigger
[What causes this mechanic to activate]

### Input
[Player controls required]
- Primary: [input]
- Alternative: [input]

### Process
[Step-by-step of what happens]

### Output
[Result of the mechanic]

### Feedback
[Visual/audio cues to player]
- Visual: [what player sees]
- Audio: [what player hears]
- Haptic: [touch feedback]

### Edge Cases
[What happens in unusual situations]
- Edge case 1: [handling]
- Edge case 2: [handling]

### Balance Considerations
[How to keep this fair and fun]
- Tuning lever 1: [description]
- Tuning lever 2: [description]

### Dependencies
- Requires: [other mechanics/systems]
- Blocks: [what this prevents]
```

## Core Mechanics Categories

### Movement

Player locomotion through the game world.

**Consider:**
- Ground movement (walk, run, crouch, crawl)
- Aerial movement (jump, double jump, glide, fly)
- Swimming/water movement
- Climbing/vaulting
- Teleportation
- Speed curves and acceleration

### Combat

Player vs player or player vs environment conflict.

**Consider:**
- Attack types (melee, ranged, magic)
- Damage calculation
- Hit detection
- Defense/blocking
- Hit points and damage
- Death/respawn

### Interaction

How players manipulate objects and the world.

**Consider:**
- Pick up/drop items
- Use consumables
- Open doors/containers
- Activate switches/levers
- Talk to NPCs
- Craft items

### Progression

How players advance and grow.

**Consider:**
- Experience points
- Leveling up
- Skill unlocks
- Stat increases
- Equipment acquisition
- Currency earning

### Economy

How resources flow through the game.

**Consider:**
- Currency types
- Earning methods (faucets)
- Spending methods (sinks)
- Trading between players
- Vendor transactions

## Mechanics Design Principles

### Clarity

Mechanics should be:
- **Discoverable** - Players can learn through play
- **Consistent** - Same inputs produce same outputs
- **Predictable** - Experienced players can plan ahead

### Depth

Mechanics should have:
- **Skill ceiling** - Room for mastery
- **Counterplay** - No unbeatable strategies
- **Variety** - Multiple valid approaches

### Fairness

Mechanics should be:
- **Balanced** - No overpowered options
- **Transparent** - Rules are visible
- **Forgiving** - Mistakes aren't catastrophic

## Common Mechanics Patterns

### Rock-Paper-Scissors

Each option has a counter:

```
A beats B
B beats C
C beats A
```

### Risk/Reward

Higher risk = higher potential reward:

```
Safe action → Low reward
Risky action → High reward
```

### Resource Management

Limited resources force choices:

```
Resource pool → Action → Depletion
Regeneration method → Renewal
```

### Progression Gates

Content unlocks over time:

```
Requirement → Unlock → New content
```

## Balance Documentation

For each mechanic, document balance considerations:

### Tuning Levers

Variables that can be adjusted:

| Lever | Current | Range | Effect |
|-------|---------|-------|--------|
| [Name] | [Value] | [Min-Max] | [Impact] |

### Counterplay

What beats this mechanic:

| Situation | Counter | Why It Works |
|-----------|---------|--------------|
| [Scenario] | [Counter-strategy] | [Reasoning] |

## Mechanics Review Checklist

Before finalizing a mechanic:

- [ ] Purpose is clear
- [ ] Inputs are discoverable
- [ ] Feedback is immediate
- [ ] Edge cases handled
- [ ] Balance levers identified
- [ ] Counterplay exists
- [ ] Fun to use
- [ ] Feels fair
- [ ] Technical feasibility confirmed
