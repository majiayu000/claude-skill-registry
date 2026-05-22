---
name: abstract-strategy
description: "Design abstract strategy games with perfect information, no randomness, and strategic depth. Use when designing a board game, exploring abstract strategy games, brainstorming game mechanics, or evaluating game balance. Keywords: board game, game design, strategy, mechanics, balance."
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Abstract Strategy Game Design

## Purpose

Design abstract strategy games—games with perfect information, no randomness, and strategic depth. Provides frameworks for ideation, design, and evaluation.

## Core Definition

Abstract strategy games require:
- **Perfect Information:** All game state visible to all players
- **No Randomness:** Outcomes determined solely by player decisions
- **Minimal Theme:** Mechanics over narrative
- **Player Agency:** Success depends on strategic thinking

---

## Quick Reference: Game Types

| Type | Core Mechanic | Examples |
|------|---------------|----------|
| Connection | Form paths/networks | Hex, TwixT |
| Territory | Control areas | Go, Othello |
| Capture | Eliminate pieces | Chess, Checkers |
| Pattern | Create arrangements | Gomoku, Pentago |
| Racing | Reach goal first | Chinese Checkers |

---

## Design Principles

### The Holy Grail: Depth-to-Complexity Ratio

**Maximum strategic depth with minimum rules complexity.**

How to achieve:
- Start with single strong core mechanism
- Remove anything that doesn't support the core
- Every rule should create multiple strategic implications
- Prefer emergent complexity over explicit rules

### Meaningful Decision Architecture

Four components of meaningful choice:
1. **Awareness:** Players understand options
2. **Consequence:** Immediate and long-term effects
3. **Permanence:** Decisions have lasting impact
4. **Reminders:** Game state reflects past choices

**Ideal Parameters:**
- Branching factor: 20-40 moves/turn for human play
- Horizon: 3-5 moves ahead with effort
- Multiple paths: 3-4 viable strategies minimum

---

## Core Mechanisms Toolkit

### Board Topology
- **Grids:** Square, hexagonal, triangular, irregular
- **Connectivity:** How spaces relate
- **Edges:** How boundaries affect strategy
- **Size:** Larger = exponentially more complex

### Piece Systems
- **Uniform:** All pieces identical (Go)
- **Differentiated:** Unique abilities (Chess)
- **Transforming:** Change during play (Checkers kings)
- **Ownership:** Fixed vs. capturable

### Movement & Placement
- **Placement only:** Pieces don't move once placed (Go)
- **Movement only:** Pieces start on board (Chess)
- **Hybrid:** Both placement and movement (Hive)

### Victory Conditions
- Elimination, Position, Pattern, Territory, Points, Stalemate

---

## Balance Considerations

### First-Player Advantage Mitigation
- **Pie Rule:** Second player can swap after first move
- **Komi:** Point compensation for second player
- **Variable Setup:** Randomized starting positions
- **Simultaneous:** Both move at once

### Avoiding Degenerate Strategies
- No single dominant path
- Counter-strategies exist for every strong position
- Passive play punishable
- Aggressive play doesn't guarantee victory

---

## Design Process

### Three Starting Points

**1. Mechanism-First**
1. Identify interesting core mechanic
2. Build minimal game around it
3. Add only what enhances core
4. Remove everything else

**2. Experience-First**
1. Define target player experience
2. Identify mechanisms that create it
3. Prototype and test rapidly
4. Iterate on feedback

**3. Constraint-Based**
1. Set specific limitations (components, time, space)
2. Find creative solutions within constraints
3. Often leads to elegant designs

### When to Add/Remove Complexity

**Add when:**
- Core feels solved too quickly
- Players master in <10 plays
- Decisions feel obvious

**Remove when:**
- Rules take >10 minutes
- Players forget rules
- Strategies feel arbitrary

**Scrap when:**
- No tweaking fixes fundamentals
- Core mechanism isn't interesting
- Feels like inferior version of existing game

---

## Brainstorming Techniques

### 1. Mechanism Extraction from Non-Games

Extract from physics, biology, economics, chemistry, social systems:
- Pieces that "decay" unless refreshed (entropy)
- Moves creating "waves" along patterns (physics)
- Pieces forming "bonds" limiting movement (chemistry)
- "Market" squares with fluctuating values (economics)

### 2. Extreme Property Isolation

Take one property to absolute extreme:
- Game where pieces visible only when adjacent to your others
- Every move must maintain rotational symmetry
- Pieces exist only one turn unless refreshed
- Board wraps in non-intuitive ways (Klein bottle)

### 3. Impossible Constraint Challenges

Start with seemingly impossible constraints:
- Game on a 1D line
- Pieces in probability clouds until observed
- Victory condition voted on by piece positions
- Pieces leave "trails" becoming new pieces

### 4. Anti-Pattern Starting Points

Design intentionally bad games, then invert:
- Always-draw game → Add accumulating positional advantages
- Pure calculation → Add pieces that change rules
- Dominant strategy → Make it vulnerable to specific counters

### 5. Mathematical Structure Mining

- Pieces move along Hamiltonian paths only
- Positions valued by prime factorization
- Fractal boards with repeating patterns
- Moves must preserve mathematical invariants

---

## Evaluation Framework

### Strategic Richness Indicators

**Depth:**
- Games last 20+ meaningful turns
- Opening, midgame, endgame feel distinct
- Multiple viable opening strategies
- Comebacks possible but not trivial

**Complexity:**
- New players grasp rules in <5 minutes
- Experts keep discovering patterns
- High-level play looks different from beginner

### Common Failures

| Problem | Symptoms | Solution |
|---------|----------|----------|
| Analysis Paralysis | Excessive turn time | Limit options, clearer objectives |
| Solved Game | Same outcome always | Increase branching, add variety |
| Kingmaker | Loser picks winner | Simultaneous resolution |

---

## Testing Protocol

### Phase 1: Proof of Concept
- Test core mechanic in isolation
- Verify basic fun factor
- Identify broken strategies

### Phase 2: Mechanics
- Test each subsystem
- Look for unintended interactions
- Measure game length

### Phase 3: Integration
- Full game, all systems
- Different skill levels
- Quantitative data

### Phase 4: Blind Testing
- Players learn from rulebook only
- Identify ambiguities
- Test learning curve

---

## Testing Checklist

### Mechanical
- [ ] All rule interactions verified
- [ ] Edge cases resolved
- [ ] Victory achievable but not trivial
- [ ] No unbreakable stalemates

### Balance
- [ ] First player wins 45-55%
- [ ] Multiple strategies win regularly
- [ ] No dominant opening
- [ ] Skill affects outcome

### Experience
- [ ] Games complete in target time
- [ ] Players want rematch
- [ ] Decisions feel meaningful
- [ ] Players improve with practice

### Accessibility
- [ ] Rules learned in <5 minutes
- [ ] Rules fit one page
- [ ] No ambiguous situations
- [ ] Components distinguishable

---

## Quick Evaluation Filters

**30-Second Test:** Can you explain core concept in 30 seconds?

**Originality Test:** Does it feel like variant of existing game?

**Decision Test:** Are there obviously interesting decisions?

**Depth Test:** Could this sustain interest for 50+ plays?

---

## Session Structure (2 Hours)

1. **10 min:** Pick 3-4 brainstorming techniques
2. **60 min:** Generate 15-20 ideas per technique
3. **20 min:** Expand 5-10 promising ideas
4. **20 min:** Combine and explore hybrids
5. **10 min:** Apply filters, select for prototyping

---

## Anti-Patterns

### 1. Complexity as Depth
**Pattern:** Adding rules, exceptions, and special cases to make the game feel "deeper."
**Why it fails:** Complexity and depth are different. Complex rules create burden; depth emerges from simple rules with rich interactions. Chess has simpler rules than many shallow games.
**Fix:** Ruthlessly remove complexity that doesn't add strategic options. If a rule requires explanation but doesn't create interesting decisions, cut it.

### 2. Solved Game Blindness
**Pattern:** Creating a game where optimal play always produces the same outcome—often draws or first-player wins.
**Why it fails:** Once players discover the solution, the game becomes rote execution rather than strategic exploration. No amount of polish fixes a solved game.
**Fix:** Test extensively with strong players. If games start converging on identical patterns, add asymmetry or increase branching factor. The pie rule helps but doesn't solve fundamental issues.

### 3. Decision Paralysis
**Pattern:** Every position has dozens of equally viable options with unclear consequences.
**Why it fails:** Strategic games need meaningful comparison between choices. When all options seem equivalent, decisions become random rather than strategic.
**Fix:** Reduce branching factor or create clearer evaluation heuristics. Players should be able to identify 3-5 promising moves without analyzing every possibility.

### 4. Theme Creep
**Pattern:** Adding narrative or thematic elements that don't connect to mechanical decisions.
**Why it fails:** Abstract strategy games work because mechanics are the content. Theme that doesn't inform decisions is decoration that slows play without adding depth.
**Fix:** Either commit to a themed game (different framework) or keep theme purely cosmetic. Don't let theme suggest mechanics that don't serve strategy.

### 5. Perfect Information Violations
**Pattern:** Adding hidden information, simultaneous resolution, or dice "for variety."
**Why it fails:** Abstract strategy games are defined by perfect information and determinism. Adding randomness or hidden elements creates a different game type with different design principles.
**Fix:** If the game needs variety, add it through board setup, victory condition selection, or piece starting positions—not through mid-game randomness.

## Integration

### Inbound (feeds into this skill)
| Skill | What it provides |
|-------|------------------|
| brainstorming | Ideation techniques for mechanism discovery |
| research | Historical game analysis and mathematical structure research |

### Outbound (this skill enables)
| Skill | What this provides |
|-------|-------------|
| (playtesting) | Designs ready for player validation |
| (rulebook writing) | Tested mechanics ready for documentation |

### Complementary
| Skill | Relationship |
|-------|--------------|
| brainstorming | Use brainstorming for raw idea generation; abstract-strategy provides evaluation and refinement frameworks |
