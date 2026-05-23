---
name: Game Balance
description: This skill should be used when the user asks about "game balance", "difficulty curve", "stat scaling", "enemy balance", "playtesting", "tuning", "damage numbers", "health values", "balancing weapons", "power curve", "difficulty settings", or needs to balance gameplay systems.
version: 1.0.0
---

# Game Balance

Practical frameworks for tuning difficulty, stats, and systems to create fair, engaging challenges.

## Core Principle: Balance Serves Fun

Balance isn't about making everything equal—it's about making everything viable and interesting. Good balance means:
- Multiple strategies are viable
- Challenge matches player skill
- Numbers feel meaningful
- Unfair deaths are rare

---

## Difficulty Design

### Difficulty Curve Template

```
Intended curve:
100% │           ╱╲
 75% │         ╱    ╲
 50% │    ╱──╱        ╲__
 25% │  ╱
  0% │╱
     └─────────────────────→
       Start    Peak    End
```

**Key points:**
- Tutorial: 10-25% difficulty
- First real challenge: 40-50%
- Major bosses: 75-90%
- Final boss: 90-100%
- Ending: Drop to 70-80% for satisfaction

### Difficulty Settings

| Setting | Enemy HP | Enemy Damage | Player Resources | Target Audience |
|---------|----------|--------------|------------------|-----------------|
| Easy | 60-70% | 50-70% | +50% | Story focus, accessibility |
| Normal | 100% | 100% | 100% | Baseline design target |
| Hard | 125-150% | 125-150% | 75-100% | Experienced players |
| Very Hard | 150-200% | 150-200% | 50-75% | Mastery seekers |

---

## Stat Scaling

### The 2x Rule

Between game start and end, player power typically increases 2-4x:

| Stat | Start | End | Multiplier |
|------|-------|-----|------------|
| Health | 100 | 300 | 3x |
| Damage | 10 | 30 | 3x |
| Defense | 5 | 15 | 3x |

Enemy scaling should match or slightly exceed.

### Damage Formula Template

```
Final Damage = Base × Weapon × (Attack - Defense × Reduction) × Modifiers
```

**Keep formulas simple.** Players should understand "bigger number = more damage."

### Stat Progression Table

| Game % | Player Power | Enemy Power | Notes |
|--------|--------------|-------------|-------|
| 0-10% | 100% | 100% | Tutorial, learning |
| 10-25% | 120% | 115% | First challenges |
| 25-50% | 160% | 150% | Core gameplay |
| 50-75% | 220% | 200% | Advanced content |
| 75-100% | 300% | 280% | End game |

---

## Enemy Design Balance

### Enemy Role Matrix

| Role | HP | Damage | Speed | Threat Level |
|------|-----|--------|-------|--------------|
| Fodder | Low | Low | Med | Low (quantity threat) |
| Soldier | Med | Med | Med | Medium |
| Tank | High | Low-Med | Low | Medium (attrition) |
| Glass cannon | Low | High | High | High (burst) |
| Elite | High | High | Med | High |
| Boss | Very High | Variable | Variable | Very High |

### Enemy Composition

Balance encounters with role variety:
```
Easy encounter: 3-4 fodder
Medium encounter: 2 fodder + 1 soldier
Hard encounter: 2 soldiers + 1 tank OR 1 glass cannon
Elite encounter: 1 elite + 2 fodder support
Boss encounter: 1 boss + spawning adds
```

---

## Weapon/Ability Balance

### Balance Matrix

| Weapon | DPS | Range | Ease | Risk | Niche |
|--------|-----|-------|------|------|-------|
| Sword | Med | Short | High | Med | Reliable melee |
| Dagger | High | Very Short | Med | High | Risk/reward |
| Bow | Med | Long | Med | Low | Safe damage |
| Staff | Variable | Long | Low | Variable | Utility/burst |

**Rule:** High reward = High risk or High skill requirement

### Viability Test

For each weapon/ability, answer:
- [ ] Is there a situation where this is optimal?
- [ ] Is there a playstyle that prefers this?
- [ ] Can a player complete the game using primarily this?

If any answer is "no," the option needs rebalancing or a niche.

---

## Playtesting Framework

### What to Measure

| Metric | Healthy Range | Warning Signs |
|--------|---------------|---------------|
| Deaths per hour | 2-5 (normal) | 0 = too easy, 10+ = too hard |
| Time to kill (enemy) | 3-10 seconds | <1s = trivial, >30s = tedious |
| Resource usage | 40-70% of available | <20% = hoarding, >90% = stressed |
| Build variety | Multiple viable | 80%+ same build = imbalance |

### Playtest Questions

After each session:
1. What felt too hard?
2. What felt too easy?
3. What felt unfair?
4. What did you never use?
5. What did you always use?

### Balance Iteration

```
[Playtest] → [Identify problem] → [Hypothesize cause] → [Adjust one thing] → [Retest]
```

**Critical:** Change one variable at a time.

---

## Quick Balance Checklist

### Before Shipping

- [ ] All builds can complete the game
- [ ] All difficulties are tested
- [ ] No "trap" options (appear good but aren't)
- [ ] Deaths feel fair (player could have avoided)
- [ ] Power progression feels meaningful
- [ ] Economy isn't broken (check late game)
- [ ] Optional content rewards appropriately

---

## Additional Resources

### Reference Files

- **`references/difficulty-curves.md`** — Pacing pattern templates
- **`references/stat-scaling.md`** — Number scaling frameworks
- **`references/playtesting-guide.md`** — Testing methodology

### Related Skills

- **`core-loop-design`** — Progression systems
- **`level-design`** — Encounter design
- **`replayability-engineering`** — Balance for multiple runs
