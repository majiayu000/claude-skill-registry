---
name: Replayability Engineering
description: This skill should be used when the user asks about "replayability", "roguelike design", "roguelite", "meta-progression", "procedural generation", "emergent gameplay", "randomness design", "run-based", "unlocks", "build diversity", "replay value", "procedural variety", "systemic design", "one more run", "permadeath", or needs to design games that players return to repeatedly.
version: 1.0.0
---

# Replayability Engineering

The force multiplier for indie games. Design systems that create hundreds of hours of gameplay from limited content.

## Why This Matters

Small teams can't compete on content volume. But they CAN compete on:
- **Procedural variety:** Infinite from finite
- **Emergent depth:** Simple rules, complex outcomes
- **Mastery curves:** Getting better feels good forever
- **Meta-progression:** Always something to unlock

A solo dev with clever systems can create more replay value than a large team with static content.

---

## Run-Based Design

### The Run Loop

```
[Character select/loadout]
      ↓
[Run start with seed]
      ↓
[Procedural content + player choices]
      ↓
[Success or failure]
      ↓
[Meta-progression update]
      ↓
[One more run?]
```

### Run Parameters

| Parameter | Short Run | Medium Run | Long Run |
|-----------|-----------|------------|----------|
| Duration | 15-30 min | 30-60 min | 60-120 min |
| Stages/floors | 3-5 | 5-10 | 10-20 |
| Item acquisitions | 5-10 | 10-20 | 20-40 |
| Decision points | 10-20 | 20-50 | 50-100 |

### Run Variety Sources

| Source | Variety Type | Example |
|--------|--------------|---------|
| Character choice | Starting conditions | Different abilities |
| Procedural levels | Layout/encounters | Generated maps |
| Item randomness | Build paths | Random drops |
| Enemy composition | Tactical challenge | Different spawns |
| Event choices | Narrative | Random events |

---

## Meta-Progression

### What Persists Between Runs

| Type | Example | Risk Level |
|------|---------|------------|
| **Unlocks** | New items enter pool | Low (expands variety) |
| **Knowledge** | Player learns patterns | None |
| **Currency** | Persistent upgrade points | Medium |
| **Power** | Permanent stat boosts | High (can trivialize) |
| **Story** | Narrative progress | Low |

### Unlock Pacing

```
Early game: Frequent unlocks (every 1-2 runs)
Mid game: Moderate unlocks (every 3-5 runs)
Late game: Rare unlocks (every 10+ runs)
End game: Mastery unlocks (skilled play required)
```

### Meta-Progression Checklist

- [ ] First unlock within first run (or shortly after)
- [ ] Clear unlock requirements visible
- [ ] Unlocks expand options, don't just add power
- [ ] Long-term goals exist (100+ hour targets)
- [ ] No "pay to progress" shortcuts undermine skill

---

## Emergent Systems

### System Interaction Design

Create emergence through interacting simple systems:

```
System A × System B × Context = Emergent outcome

Example:
Fire damage × Oil puddles × Enemy type =
  Burning oil spreading to ignite more enemies
```

### Combinatorial Design

| Elements | Possible Combinations |
|----------|----------------------|
| 10 items | 45 pairs |
| 20 items | 190 pairs |
| 50 items | 1,225 pairs |

**Design for combinations:** Each item should interact with multiple others.

### Synergy Categories

| Synergy Type | Description | Example |
|--------------|-------------|---------|
| Additive | Effects stack | +10% damage + +10% damage = +20% |
| Multiplicative | Effects multiply | 2x damage × 2x speed = OP combo |
| Conditional | Triggers on condition | "On fire, deal 3x damage" |
| Transformative | Changes behavior | "Attacks now heal" |

---

## Procedural Variety

### What to Proceduralize

| Element | Procedural Value | Implementation Cost |
|---------|------------------|---------------------|
| Level layout | High | Medium |
| Enemy placement | High | Low |
| Item drops | High | Low |
| Events/encounters | Medium | Medium |
| Visual variations | Low | Variable |
| Story elements | Medium | High |

### Seed-Based Generation

**Critical for Nethercore:** Rollback netcode requires determinism.

```
All randomness flows from single seed:
Seed → Level generation
Seed → Enemy spawns
Seed → Item drops
Seed → Events
```

**Benefits:**
- Multiplayer sync (same seed = same run)
- Shareable runs
- Debugging reproducibility
- Competitive fairness

### Constrained Randomness

Pure random is rarely fun. Constrain with:
- **Templates:** Random selection from curated sets
- **Rules:** "Always exactly one healing item per floor"
- **Difficulty scaling:** Later = harder random pools
- **Streak protection:** Prevent extreme bad luck

---

## Randomness Design

### Input vs Output Randomness

| Type | When Decided | Player Control | Frustration Risk |
|------|--------------|----------------|------------------|
| **Input** | Before action | Plan around it | Low |
| **Output** | After action | None | High |

**Prefer input randomness:** Random hand dealt, not random damage roll.

### Fairness Patterns

| Pattern | Implementation | Purpose |
|---------|----------------|---------|
| **Pity timer** | Guaranteed after N failures | Prevent bad streaks |
| **Weighted pools** | Skew toward needed items | Balanced builds |
| **Curated random** | Random from designed sets | Quality control |
| **Seed preview** | Show upcoming randomness | Strategic planning |

### Randomness Checklist

- [ ] Bad luck can't end runs alone
- [ ] Good luck doesn't guarantee wins
- [ ] Player can influence odds through skill
- [ ] Outcomes feel fair in retrospect
- [ ] Variance creates stories, not frustration

---

## Build Diversity

### Viable Build Framework

For each "archetype" or build path:
- [ ] Can complete the game
- [ ] Has unique playstyle
- [ ] Has satisfying power fantasy
- [ ] Has counters and challenges
- [ ] Feels different from other builds

### Preventing Dominant Strategies

| Problem | Solution |
|---------|----------|
| One build always best | Buff alternatives |
| Meta is solved | Regular balance updates |
| Same path every run | Randomize availability |
| Optimal boring | Make fun builds viable |

### Build Identity

Each build should have:
- Clear theme (fire, speed, tanks)
- Unique core mechanic
- Specific item synergies
- Distinct playstyle feel
- Recognizable power spike

---

## The "One More Run" Loop

### Why Players Return

| Motivator | Design Support |
|-----------|----------------|
| "So close!" | Progress visible, death feels beatable |
| "New unlock" | Reward waiting to try |
| "Better strategy" | Learning from failure |
| "Different build" | Variety to explore |
| "Quick run" | Respects player time |

### Session Hooks

| Hook | Implementation |
|------|----------------|
| Incomplete goal | "1 more boss to final" |
| New toy | Just unlocked something |
| Streak | On a winning streak |
| Revenge | Died to beatable boss |
| Discovery | "What does this do?" |

---

## Quick Reference Templates

### Run Design Template

```
RUN STRUCTURE

Target length: _____ minutes
Stages: _____
Items per run: _____
Key decisions: _____

Variety sources:
□ Characters  □ Procedural levels  □ Random items
□ Events      □ Enemy composition  □ Other: _____

Meta-progression:
□ Unlocks    □ Currency    □ Story    □ Power
Unlock rate: _____ per run (early) / _____ (late)

Seed-based: □ Yes □ No
```

### Synergy Planning Template

```
ITEM SYNERGIES

Item: _____________
Type: [Damage / Defense / Utility / Build-enabling]

Synergizes with:
• _____________ (effect: _____________)
• _____________ (effect: _____________)
• _____________ (effect: _____________)

Anti-synergy:
• _____________ (why: _____________)

Build archetype fit: _____________
```

---

## Additional Resources

### Reference Files

- **`references/run-based-design.md`** — Run structure patterns
- **`references/meta-progression.md`** — Unlock and persistence design
- **`references/emergent-systems.md`** — System interaction design
- **`references/procedural-variety.md`** — Procedural generation approaches
- **`references/randomness-design.md`** — Fair randomness patterns

### Related Skills

- **`genre-patterns`** → Roguelike patterns
- **`core-loop-design`** — Loop structure
- **`game-balance`** — Build balance
- **`player-psychology`** — Engagement patterns
