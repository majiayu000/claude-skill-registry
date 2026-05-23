---
name: Player Psychology
description: This skill should be used when the user asks about "player motivation", "player types", "engagement", "onboarding", "flow state", "frustration", "rewards", "player retention", "why players play", "player behavior", "fun", or needs to understand what makes games engaging.
version: 1.0.0
---

# Player Psychology

Understanding what motivates players and how to design for engagement without manipulation.

## Core Principle: Respect the Player

Understanding psychology helps design better games—not exploit players. Use these insights to:
- Remove unnecessary frustration
- Amplify genuine satisfaction
- Match content to player desires
- Create meaningful experiences

---

## Player Motivation Types

### Intrinsic vs Extrinsic

| Type | Source | Examples | Durability |
|------|--------|----------|------------|
| **Intrinsic** | Internal satisfaction | Mastery, curiosity, expression | Long-lasting |
| **Extrinsic** | External rewards | Points, achievements, unlocks | Fades over time |

**Design priority:** Build on intrinsic motivation. Use extrinsic as enhancement, not foundation.

### Player Type Framework

| Type | Driven By | Design For |
|------|-----------|------------|
| **Achiever** | Completion, mastery | Clear goals, 100% targets, rankings |
| **Explorer** | Discovery, understanding | Secrets, lore, hidden content |
| **Socializer** | Connection, community | Multiplayer, sharing, co-op |
| **Competitor** | Winning, comparison | Leaderboards, PvP, challenges |

Most players are combinations. Design for multiple types.

---

## Flow State

### The Flow Channel

```
Anxiety (too hard)
        │      ╱
Challenge│    ╱ ← FLOW
        │  ╱
        │╱
Boredom (too easy)
        └────────→ Skill
```

**Flow occurs when:** Challenge ≈ Skill level

### Creating Flow

| Element | How to Provide |
|---------|---------------|
| Clear goals | Obvious objectives, visible progress |
| Immediate feedback | Responsive controls, clear results |
| Challenge-skill balance | Dynamic difficulty, multiple paths |
| Concentration | Minimize interruptions, reduce UI clutter |
| Control | Player agency, predictable systems |

---

## Onboarding

### The First 5 Minutes

| Minute | Goal | Method |
|--------|------|--------|
| 0-1 | Hook interest | Dramatic opening, immediate action |
| 1-2 | Teach core | One mechanic, guided success |
| 2-3 | Provide agency | Let player experiment |
| 3-4 | Create goal | Show objective, create motivation |
| 4-5 | First reward | Early win, positive reinforcement |

### Teaching Principles

1. **Show, don't tell:** Actions over text
2. **One thing at a time:** Sequential mechanics
3. **Safe failure:** Low-stakes learning
4. **Immediate application:** Use new skill right away
5. **Player discovery:** Let them figure some things out

---

## Reward Psychology

### Reward Schedules

| Schedule | Pattern | Effect |
|----------|---------|--------|
| **Fixed ratio** | Every N actions | Predictable, can feel grindy |
| **Variable ratio** | Random chance | Engaging, risk of addiction |
| **Fixed interval** | Every N minutes | Creates return behavior |
| **Variable interval** | Random timing | Maintains attention |

**Ethical note:** Variable schedules are powerful. Use responsibly.

### Reward Hierarchy

```
Small, frequent    →    Large, rare
    │                       │
  Keeps momentum      Creates goals
```

Mix both: small rewards maintain engagement, large rewards create milestones.

---

## Frustration Management

### Frustration Sources

| Source | Solution |
|--------|----------|
| Unclear goal | Better communication, visible objectives |
| Unfair death | Clearer enemy tells, adjusted timing |
| Lost progress | Better checkpoints, auto-save |
| Stuck/blocked | Hints, alternative paths, difficulty options |
| Repetition | Reduce backtracking, skip options |

### The 3-Strike Rule

After 3 failures at the same point:
- Offer hint (subtle)
- After 5: Offer help (clear)
- After 7+: Consider dynamic difficulty

---

## Engagement Patterns

### Session Hooks

| Hook Type | Function | Example |
|-----------|----------|---------|
| **Cliffhanger** | Incomplete goal | "Almost reached the boss" |
| **Investment** | Progress at risk | "Carrying valuable loot" |
| **Discovery** | Unanswered question | "What's behind that door?" |
| **Social** | Multiplayer commitment | "Friends are online" |

### Return Motivation

What brings players back:
- [ ] Unfinished objectives
- [ ] Desire for mastery
- [ ] New content promised
- [ ] Social connections
- [ ] Completion drive

---

## Quick Engagement Checklist

- [ ] First 5 minutes are compelling
- [ ] Goals are always clear
- [ ] Progress is visible
- [ ] Rewards match effort
- [ ] Failure teaches, doesn't punish
- [ ] Multiple motivation types supported
- [ ] Sessions have satisfying end points

---

## Additional Resources

### Reference Files

- **`references/motivation-types.md`** — Detailed player type analysis
- **`references/onboarding-checklist.md`** — Tutorial design checklist
- **`references/engagement-patterns.md`** — Session and retention design

### Related Skills

- **`core-loop-design`** — Loop engagement
- **`game-balance`** — Challenge tuning
- **`replayability-engineering`** — Long-term engagement
