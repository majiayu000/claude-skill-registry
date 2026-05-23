---
name: Narrative Design
description: |
  Use this skill for game storytelling: "story structure", "narrative", "quest design", "dialogue writing", "branching narrative", "environmental storytelling", "narrative pacing".

  **Load references when:**
  - Story structure templates → `references/story-structures.md`
  - Quest types and chains → `references/quest-patterns.md`
  - Dialogue techniques → `references/dialogue-guide.md`

  For ZX dialogue IMPLEMENTATION (text boxes, typewriter, choices): use zx-game-design:gameplay-mechanics instead.
version: 1.1.0
---

# Narrative Design for Games

Frameworks for integrating story into gameplay. The best game stories feel like the player created them through their choices.

## Core Principle: Player as Protagonist

In games, the player IS the main character. Narrative design must:
- Support player agency (choices matter)
- Make player actions meaningful
- Avoid taking control away unnecessarily
- Integrate story with gameplay mechanics

---

## Story Structure (Games vs Film)

Games adapt traditional structure for interactivity:

| Act | Traditional | Game Adaptation |
|-----|-------------|-----------------|
| **1** | Setup | Tutorial + World intro + Goal |
| **2** | Confrontation | Core loop + Escalating challenges |
| **3** | Resolution | Climax + Denouement + Reflection |

**Act 2 is 60-70% of gameplay** — most content lives here.

### Non-Linear Alternatives

| Pattern | Structure | Best For |
|---------|-----------|----------|
| Hub & Spoke | Central hub, branching content | Open-world, RPGs |
| Episodic | Self-contained segments | Session-based play |
| Emergent | Systems create story | Roguelikes, sims |

See **`references/story-structures.md`** for Hero's Journey adaptation and beat mapping.

---

## Quest Design Essentials

Every quest needs: **Objective**, **Motivation**, **Challenge**, **Reward**, **Closure**.

### Quest Types

| Type | Best For |
|------|----------|
| Kill/Defeat | Combat focus, clear objective |
| Fetch | Exploration, resource gathering |
| Escort | Tension, relationship building |
| Investigate | Narrative focus, mystery |
| Defend | Time pressure, tension |
| Survive | Horror, resource management |

### Quest Chains

```
Linear:     A → B → C
Branching:  A → B1 → C1 (ending 1)
              ↘ B2 → C2 (ending 2)
Convergent: A → B1 ↘ D (same destination)
            A → B2 ↗
```

See **`references/quest-patterns.md`** for templates and examples.

---

## Dialogue Writing

### Every Line Serves a Purpose

| Purpose | Example |
|---------|---------|
| Information | "The key is in the tower" |
| Character | "I never trusted wizards" |
| Emotion | "Please... find my daughter" |
| Choice setup | "Help village or seek treasure?" |
| World building | "Before the war, this was a garden" |

### Guidelines

- **Keep it short** — Long text blocks get skipped
- **Voice each character** — Distinct vocabulary and patterns
- **Show, don't tell** — NPCs react to what player did
- **Avoid false choices** — Each option should lead somewhere different

See **`references/dialogue-guide.md`** for branching dialogue patterns.

---

## Branching Narratives

### Complexity Levels

| Level | Description | Cost |
|-------|-------------|------|
| Flavor | Different dialogue, same outcome | Low |
| Tactical | Different paths to same goal | Medium |
| Strategic | Different goals, different endings | High |
| Systemic | Emergent from interacting systems | Very High |

### The Funnel Approach

Many branches early → Converge at key points → Branch again for endings.

Track player choices for: NPC reactions, content locks, endings, affinity scores.

---

## Exposition Techniques (Best to Worst)

| Method | Immersion |
|--------|-----------|
| Environmental storytelling | High |
| Gameplay integration | High |
| NPC dialogue (on request) | Medium |
| Found documents | Medium |
| Cutscenes | Low-Medium |
| Text dumps | Low |

### Environmental Storytelling

Tell story through the world:
- **Objects**: Sword in ground = grave, empty bottles = desperation
- **Architecture**: Grandeur = former glory, repairs = resilience
- **Sequences**: Blood trail, footprints, damage patterns

---

## Endings Checklist

For satisfying endings:
- [ ] Resolves main conflict
- [ ] Addresses major character arcs
- [ ] Rewards player investment
- [ ] Feels earned by player actions
- [ ] Doesn't invalidate player choices
- [ ] Provides closure (or intentional openness)

---

## Related Skills

- **`character-design`** — Characters in your narrative
- **`world-building`** — Setting for your story
- **`player-psychology`** — Engagement with narrative
