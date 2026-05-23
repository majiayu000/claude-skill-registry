---
name: Core Loop Design
description: |
  Use this skill for gameplay loops: "core loop", "gameplay loop", "progression system", "game economy", "feedback loop", "reward system", "engagement loop", "pacing".

  **Load references when:**
  - Detailed loop worksheet → `references/loop-worksheet.md`
  - Progression curves/patterns → `references/progression-templates.md`
  - Economy/resource design → `references/economy-design.md`
version: 1.1.0
---

# Core Loop Design

Frameworks for designing gameplay cycles that keep players engaged. The core loop is your game's heartbeat — players don't remember features, they remember how it felt to play.

## Core Principle

Every game loop has three phases:

```
[ACTION] → [FEEDBACK] → [REWARD] → repeat
```

The loop must be: **Satisfying** (feels good), **Clear** (know what to do), **Variable** (not monotonous), **Progressive** (mastery visible).

---

## Loop Hierarchy

Games have nested loops at different time scales:

| Loop | Duration | Example |
|------|----------|---------|
| **Micro** | Seconds | Attack → Hit feedback → Damage |
| **Core** | Minutes | Clear room → XP → Level progress |
| **Meta** | Hours | Complete dungeon → New gear → Stronger |
| **Session** | Play session | Progress → Reason to return |

Loops connect: Micro rewards → Core loop → Meta loop → Reason to continue.

---

## Loop Patterns

### Action Loop
`[Find challenge] → [Attempt] → [Succeed/Fail] → [Learn]`
- Games: Platformers, action, skill-based
- Key: Failure teaches, success feels earned

### Collection Loop
`[Explore] → [Discover item] → [Add to collection] → [Unlock new areas]`
- Games: Metroidvanias, adventure, collectathons
- Key: Items must be meaningful

### Combat Loop
`[Encounter] → [Fight] → [Victory] → [Loot/XP] → [Get stronger]`
- Games: RPGs, action RPGs, roguelikes
- Key: Power progression feels meaningful

### Build Loop
`[Gather resources] → [Craft/Build] → [Use creation] → [New opportunities]`
- Games: Survival, crafting, city builders
- Key: Building has purpose and visible impact

---

## Progression Types

| Type | Player Gains | Feels Like |
|------|--------------|------------|
| Vertical | More power | Getting stronger |
| Horizontal | More options | Getting versatile |
| Skill | Player improves | Getting better |
| Content | Access to more | Unlocking secrets |

### Progression Curves

- **Linear** `/` — Steady, predictable, can feel grindy
- **Exponential early** `╭─` — Fast start, good for onboarding
- **Stepped** `─┐─┐` — Dramatic power spikes with plateaus

---

## Economy Essentials

### Sources and Sinks
```
[Sources] → Player inventory → [Sinks]
Enemies         ↕              Purchases
Exploration   Save/Load        Consumables
                               Upgrades
```

**Balance rule**: Sinks must match or exceed sources, or economy inflates.

### Scarcity Creates Value

Control through: limited sources, time gating, location gating, skill gating.

*Warning*: Too much scarcity = frustration. Too little = meaninglessness.

---

## Feedback Intensity

Match feedback to action significance:

| Action | Feedback |
|--------|----------|
| Basic attack | Small sound/visual |
| Critical hit | Big sound, camera shake |
| Level up | Fanfare, UI celebration |
| Boss defeat | Extended celebration |

Checklist for each action:
- [ ] Visual feedback exists
- [ ] Audio feedback exists
- [ ] Feedback is immediate
- [ ] Intensity matches significance

---

## Flow State Design

Players enter flow when challenge matches skill:

```
Challenge
   ↑     FLOW ZONE (between too hard/too easy)
   └────────────→ Skill
```

Prevent negative loops:
- **Death spiral**: Fail → Lose resources → Harder → Fail again
  - *Fix*: Failure shouldn't compound difficulty
- **Grinding trap**: Stuck → Grind → Trivialize content → Boredom
  - *Fix*: Skill should matter more than grinding

---

## Session Design

Structure sessions: `[Hook] → [Rising action] → [Peak] → [Cool down] → [Cliffhanger]`

Design natural break points: after objectives, in safe zones, after story beats, before major challenges.

**Target session length**: _____ minutes
- [ ] Loop cycles fit session
- [ ] Progress feels meaningful
- [ ] Natural stopping points exist

---

## Related Skills

- **`game-balance`** — Balancing loop rewards
- **`player-psychology`** — Understanding engagement
- **`replayability-engineering`** — Loops for replayable games
