---
name: Genre Design Patterns
description: This skill should be used when the user asks about "RPG design", "platformer design", "roguelike", "roguelite", "metroidvania", "action game", "puzzle game", "adventure game", "genre conventions", "genre patterns", "what makes a good [genre]", or needs genre-specific design guidance.
version: 1.0.0
---

# Genre Design Patterns

Quick-reference patterns for common game genres. Use as starting points—the best games often blend genres.

## How to Use This Skill

1. Identify your primary genre
2. Review its core pillars
3. Check essential elements
4. Consider which secondary genres to blend
5. Use templates as starting framework

---

## Platformer

### Core Pillars
- Precise movement and jumping
- Obstacle navigation
- Timing challenges

### Essential Elements

| Element | Purpose |
|---------|---------|
| Responsive controls | Feel good, predictable |
| Clear platforms | Readable jump targets |
| Fair hazards | Visible before dangerous |
| Checkpoints | Reduce frustration |
| Collectibles | Exploration reward |

### Design Template
```
PLATFORMER DESIGN

Movement feel: [ ] Floaty [ ] Tight [ ] Momentum-based
Jump type: [ ] Fixed [ ] Variable height [ ] Double/multi
Core gimmick: _______________
Level structure: [ ] Linear [ ] Hub [ ] World map
Death penalty: _______________
```

---

## Action RPG

### Core Pillars
- Real-time combat
- Character progression
- Loot/equipment

### Essential Elements

| Element | Purpose |
|---------|---------|
| Satisfying combat | Core loop engagement |
| Meaningful stats | Progression feeling |
| Build variety | Player expression |
| Loot drops | Reward and excitement |
| Enemies that teach | Skill development |

### Design Template
```
ACTION RPG DESIGN

Combat style: [ ] Hack-slash [ ] Souls-like [ ] Character action
Stat impact: [ ] Heavy (numbers matter) [ ] Light (skill matters more)
Build system: [ ] Class-based [ ] Skill tree [ ] Equipment-based
Loot rarity tiers: _______________
Core loop: Kill → Loot → Upgrade → Kill stronger
```

---

## Roguelike / Roguelite

### Core Pillars
- Procedural generation
- Permadeath or run-based play
- Progressive mastery

### Essential Elements

| Element | Purpose |
|---------|---------|
| Run variety | Each attempt feels fresh |
| Fair randomness | Bad luck doesn't doom run |
| Quick restart | Minimize frustration |
| Meta-progression | Long-term goals (roguelite) |
| Build diversity | Many viable paths |

### Design Template
```
ROGUELIKE DESIGN

Permadeath: [ ] Full [ ] Roguelite (meta-progression)
Run length: _____ minutes target
Seed-based: [ ] Yes [ ] No (important for replays/multiplayer)
Unlock system: _______________
Core randomization: [ ] Levels [ ] Items [ ] Enemies [ ] All
```

See **`replayability-engineering`** for deeper roguelike patterns.

---

## Metroidvania

### Core Pillars
- Interconnected world
- Ability-gated exploration
- Backtracking with new powers

### Essential Elements

| Element | Purpose |
|---------|---------|
| Satisfying movement | Traversal is constant |
| Clear ability gates | Know what you need |
| Rewarding backtracking | Old areas have new value |
| Map system | Navigation in complex space |
| Sequence-breaking (optional) | Reward mastery |

### Design Template
```
METROIDVANIA DESIGN

World size: _____ screens/rooms
Key abilities: _______________
Gate types: [ ] Ability [ ] Item [ ] Skill
Map reveal: [ ] Auto [ ] Manual [ ] Exploration-based
Shortcut system: _______________
```

---

## Puzzle

### Core Pillars
- Problem-solving
- "Aha" moments
- Clear rules, emergent complexity

### Essential Elements

| Element | Purpose |
|---------|---------|
| Teachable rules | Player understands system |
| Fair solutions | No guessing required |
| Escalating complexity | Difficulty progression |
| Hints (optional) | Accessibility |
| Undo/reset | Experimentation |

### Design Template
```
PUZZLE DESIGN

Core mechanic: _______________
Complexity source: [ ] More elements [ ] Tighter constraints [ ] Combinations
Puzzle count: _____
Hint system: [ ] None [ ] Optional [ ] Progressive
Success feedback: _______________
```

---

## Adventure / Narrative

### Core Pillars
- Story-driven
- Exploration and discovery
- Character interaction

### Essential Elements

| Element | Purpose |
|---------|---------|
| Compelling narrative | Drives player forward |
| Interesting characters | Emotional investment |
| Meaningful choices | Player agency |
| Environmental storytelling | World feels alive |
| Clear objectives | Direction when needed |

### Design Template
```
ADVENTURE DESIGN

Story structure: [ ] Linear [ ] Branching [ ] Open
Player character: [ ] Defined [ ] Blank slate [ ] Customizable
Dialogue system: [ ] Simple [ ] Branching [ ] Full RPG
Choice impact: [ ] Flavor [ ] Story [ ] Endings
Core mystery/goal: _______________
```

---

## Genre Blending

### Popular Combinations

| Blend | Examples | Key Tension |
|-------|----------|-------------|
| Roguelike + Platformer | Dead Cells style | Tight controls + Randomness |
| RPG + Puzzle | Puzzle RPGs | Stats + Pure logic |
| Action + Narrative | Action-adventure | Pacing gameplay vs story |
| Platformer + Metroidvania | Most metroidvanias | Linear flow vs backtracking |

### Blending Checklist

- [ ] Primary genre is clear
- [ ] Secondary adds value, not confusion
- [ ] Core loops don't conflict
- [ ] Player expectations are set early

---

## Additional Resources

### Reference Files

- **`references/rpg-patterns.md`** — Detailed RPG design
- **`references/platformer-patterns.md`** — Platformer design deep dive
- **`references/roguelike-patterns.md`** — Roguelike essentials
- **`references/metroidvania-patterns.md`** — Metroidvania design

### Related Skills

- **`replayability-engineering`** — For roguelike/lite design
- **`core-loop-design`** — Genre-specific loops
- **`narrative-design`** — Story-focused genres
