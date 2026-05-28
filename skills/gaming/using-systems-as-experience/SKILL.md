---
name: using-systems-as-experience
description: Router for systems-as-experience - emergence, sandbox, optimization, discovery, narrative, modding
---

# Using Systems-as-Experience (Meta-Skill Router)

**Your entry point to the systems-as-experience skillpack.** Routes you to the right combination of specialized skills for your game design challenge.

## Purpose

This **meta-skill**:
1. ✅ **Routes** you to the correct skills in this pack
2. ✅ **Combines** multiple skills for complex projects
3. ✅ **Provides** quick-start workflows for common game types
4. ✅ **Explains** the pack's philosophy and when to use it

---

## Core Philosophy: Systems AS Experience

### The Central Idea

**Traditional game design:** Systems support content
- Design story → build mechanics to express it
- Content is king, systems are servants

**Systems-as-experience:** Systems ARE the content
- Design orthogonal mechanics → emergence creates "content"
- Design constraints → player creativity becomes gameplay
- Systems are king, authored content is optional

### When This Philosophy Applies

**✅ Use systems-as-experience when:**
- Core loop is experimentation, creativity, or optimization
- Replayability through emergent outcomes is desired
- Player agency and expression are paramount
- Systems have inherent depth worth discovering

**❌ Don't use systems-as-experience when:**
- Authored narrative is primary experience
- Linear progression with fixed setpieces
- Hand-crafted, bespoke content is the appeal

**Hybrid approach:** Most games blend both (BotW has authored Ganon encounter + emergent physics sandbox)

---

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-systems-as-experience/SKILL.md`

Reference sheets like `emergent-gameplay-design.md` are at:
  `skills/using-systems-as-experience/emergent-gameplay-design.md`

NOT at:
  `skills/emergent-gameplay-design.md` ← WRONG PATH

---

## Pack Overview: 8 Core Skills

### Wave 1: Foundation (Core Concepts)

| Skill | When to Use | Examples | Time |
|-------|-------------|----------|------|
| **emergent-gameplay-design** ⭐ | Every systems-driven game starts here | BotW, Dwarf Fortress, Minecraft | 3-4h |
| **sandbox-design-patterns** | Open-ended creativity games | Minecraft, Factorio, KSP | 2-3h |
| **strategic-depth-from-systems** | Competitive games, build diversity | Path of Exile, StarCraft, Dota | 2-3h |

### Wave 2: Specific Applications

| Skill | When to Use | Examples | Time |
|-------|-------------|----------|------|
| **optimization-as-play** | Factory games, efficiency puzzles | Factorio, Satisfactory, Opus Magnum | 2-4h |
| **discovery-through-experimentation** | Exploration, hidden depth | BotW, Outer Wilds, Noita | 2-4h |
| **player-driven-narratives** | Simulation games, emergent storytelling | Dwarf Fortress, Rimworld, CK3 | 2-4h |

### Wave 3: Ecosystem

| Skill | When to Use | Examples | Time |
|-------|-------------|----------|------|
| **modding-and-extensibility** | Long-term community content | Skyrim, Minecraft, Factorio | 2-3h |
| **community-meta-gaming** | Competitive, theorycrafting communities | Path of Exile, EVE Online, Dark Souls | 2-3h |

---

## Routing Logic: Decision Tree

```
START: What type of game are you building?

├─ SANDBOX / CREATIVITY GAME
│  └─> emergent-gameplay-design + sandbox-design-patterns
│      + optimization-as-play (if optimization core)
│      + discovery-through-experimentation (if discovery-driven)
│      + modding-and-extensibility (if mod support)

├─ COMPETITIVE / STRATEGIC GAME
│  └─> emergent-gameplay-design + strategic-depth-from-systems
│      + community-meta-gaming (if competitive scene planned)

├─ SIMULATION / MANAGEMENT GAME
│  └─> emergent-gameplay-design + player-driven-narratives
│      + optimization-as-play (if optimization gameplay)

├─ EXPLORATION / DISCOVERY GAME
│  └─> emergent-gameplay-design + discovery-through-experimentation
│      + sandbox-design-patterns (if sandbox elements)

└─ MULTIPLAYER SOCIAL GAME
   └─> player-driven-narratives + community-meta-gaming
```

### Quick Reference Table

| Game Type | Primary Skill | Secondary Skills | Examples |
|-----------|---------------|------------------|----------|
| **Sandbox Builder** | sandbox-design-patterns | emergent, optimization, discovery | Minecraft, Terraria |
| **Factory Game** | optimization-as-play | emergent, sandbox | Factorio, Satisfactory |
| **Physics Sandbox** | emergent-gameplay-design | discovery, sandbox | BotW, Noita |
| **Colony Sim** | player-driven-narratives | emergent, optimization | Rimworld, DF |
| **Competitive Strategy** | strategic-depth-from-systems | emergent, meta-gaming | PoE, Dota |
| **Exploration Game** | discovery-through-experimentation | emergent, sandbox | Outer Wilds, Subnautica |
| **MMO Sandbox** | player-driven-narratives | meta-gaming, modding | EVE Online |

---

## Detailed Routing Scenarios

See [routing-scenarios.md](routing-scenarios.md) for 22 detailed examples:
- Minecraft-like voxel sandbox
- Factorio-style factory game
- BotW-style physics playground
- Rimworld-style colony sim
- Path of Exile-style ARPG
- Outer Wilds-style exploration
- EVE Online-style MMO sandbox
- And 15 more...

---

## Multi-Skill Workflows

### Workflow 1: Sandbox Builder (Minecraft, Terraria)
1. **emergent-gameplay-design** (2-3h) - Orthogonal block/item systems
2. **sandbox-design-patterns** (2-3h) - Progressive complexity, constraints
3. **discovery-through-experimentation** (2-3h) - Hidden recipes, secrets
4. **modding-and-extensibility** (2-3h) - Mod API
**Total:** 8-12 hours

### Workflow 2: Factory Game (Factorio, DSP)
1. **emergent-gameplay-design** (2-3h) - Production chains
2. **sandbox-design-patterns** (1-2h) - Spatial constraints
3. **optimization-as-play** (3-4h) - Bottleneck gameplay, metrics
4. **modding-and-extensibility** (2-3h) - Mod API
**Total:** 8-12 hours

### Workflow 3: Physics Playground (BotW, Noita)
1. **emergent-gameplay-design** (3-4h) - Physics interactions
2. **discovery-through-experimentation** (3-4h) - Environmental hints
3. **sandbox-design-patterns** (1-2h) - Open world structure
**Total:** 7-10 hours

### Workflow 4: Colony Simulator (Rimworld, DF)
1. **emergent-gameplay-design** (2-3h) - Simulation systems
2. **player-driven-narratives** (3-4h) - AI storyteller, character arcs
3. **sandbox-design-patterns** (1-2h) - Base building
4. **modding-and-extensibility** (2-3h) - Mod support
**Total:** 8-12 hours

### Workflow 5: Competitive ARPG (Path of Exile)
1. **emergent-gameplay-design** (2-3h) - Skill/item interactions
2. **strategic-depth-from-systems** (3-4h) - Build diversity
3. **community-meta-gaming** (3-4h) - Theorycrafting, economy
**Total:** 8-11 hours

---

## Quick Start Guides

### Quick Start 1: Minimal Viable Emergence (4h)
1. Read emergent-gameplay-design Quick Start (1h)
2. Design 3 orthogonal systems with 9 interactions (1h)
3. Prototype interaction matrix (1h)
4. Playtest for emergent moments (1h)

### Quick Start 2: Optimization Game MVP (4h)
1. Read optimization-as-play Quick Start (1h)
2. Implement production chain with visible metrics (1.5h)
3. Add bottleneck visualization (1h)
4. Playtest optimization loop (0.5h)

### Quick Start 3: Discovery-Driven Exploration (4h)
1. Read discovery-through-experimentation Quick Start (1h)
2. Place environmental hints for 3 mechanics (1h)
3. Create discovery journal system (1h)
4. Playtest hint effectiveness (1h)

---

## Common Pitfalls

### Pitfall 1: Starting with Wrong Skill
**Problem:** Jumping to optimization-as-play without emergent-gameplay-design foundation
**Symptom:** Optimization game with no depth (one optimal solution)
**Fix:** ALWAYS start with emergent-gameplay-design for orthogonal systems, THEN apply optimization

### Pitfall 2: Over-Applying All Skills
**Problem:** Trying to use all 8 skills on every project
**Symptom:** Scope creep, conflicting design goals, nothing gets finished
**Fix:** Use routing logic above. Most projects need 2-4 skills, not all 8.

### Pitfall 3: Skipping Foundation
**Problem:** Going straight to Wave 2/3 skills without Wave 1
**Symptom:** Surface-level implementation without systemic depth
**Fix:** emergent-gameplay-design is FOUNDATIONAL for most projects. Read it first.

### Pitfall 4: Not Recognizing Hybrid Design
**Problem:** Trying to make EVERYTHING systemic (including authored narrative)
**Symptom:** Losing authored emotional moments, pacing issues
**Fix:** Most games blend systems + authored content. Use routing logic for systems portion only.

### Pitfall 5: Underestimating Time
**Problem:** Thinking "I'll just add emergence" will take 30 minutes
**Symptom:** Rushed implementation, no playtesting, shallow system
**Fix:** Each skill requires 2-4 hours minimum. Budget 8-15 hours for multi-skill projects.

---

## Integration with Other Skillpacks

### Cross-Pack Dependencies

| Need | Use |
|------|-----|
| Emergence requires simulation | emergent-gameplay-design + simulation-tactics |
| Systems need math foundation | strategic-depth-from-systems + yzmir/game-theory |
| Systems need feel/polish | optimization-as-play + lyra/game-feel |

---

## Success Criteria

### Your project successfully uses systems-as-experience when:

**Emergence (Core):**
- [ ] Players discover solutions you didn't intend
- [ ] System interactions create "content"
- [ ] Replayability through emergent variety

**Depth:**
- [ ] Hidden depth rewards mastery
- [ ] Community discovers new strategies
- [ ] No single dominant strategy

**Discovery:**
- [ ] Curiosity is rewarded
- [ ] "Aha moments" occur frequently

**Community:**
- [ ] Players create external tools
- [ ] Meta-game emerges beyond playing

---

## Conclusion

**The Golden Rule:**
> "Design systems that interact, then let players surprise you."

### Next Steps
1. **Identify your game type** (use routing logic above)
2. **Read foundational skill** (usually emergent-gameplay-design)
3. **Apply skills in sequence** (use workflows above)
4. **Playtest for emergence** (look for unintended solutions)
5. **Iterate on interactions** (orthogonal systems multiply)

---

## Systems as Experience Specialist Skills Catalog

After routing, load the appropriate specialist skill for detailed guidance:

1. [emergent-gameplay-design.md](emergent-gameplay-design.md) - FOUNDATIONAL ⭐: Orthogonal systems, emergence, simulation over scripting
2. [sandbox-design-patterns.md](sandbox-design-patterns.md) - Open worlds, creative tools, freedom within constraints
3. [strategic-depth-from-systems.md](strategic-depth-from-systems.md) - Build space analysis, strategic decision-making
4. [optimization-as-play.md](optimization-as-play.md) - Factorio-style optimization loops, efficiency challenges
5. [discovery-through-experimentation.md](discovery-through-experimentation.md) - Hidden mechanics, eureka moments
6. [player-driven-narratives.md](player-driven-narratives.md) - Emergent stories, systemic consequences
7. [modding-and-extensibility.md](modding-and-extensibility.md) - Mod support, community content
8. [community-meta-gaming.md](community-meta-gaming.md) - Theorycrafting, shared knowledge ecosystems
9. [routing-scenarios.md](routing-scenarios.md) - 22 game type routing examples

---

**Go build systems that surprise you.**
