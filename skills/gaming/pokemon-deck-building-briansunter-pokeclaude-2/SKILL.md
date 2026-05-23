---
name: Pokemon Deck Builder
description: |
  Use when building, analyzing, or optimizing Pokemon TCG Pocket decks.

  **Activates when user mentions:**
  - Deck building ("build a deck", "create deck")
  - Deck analysis ("analyze my deck", "check deck")
  - Synergy finding ("what works with X", "synergies")
  - Optimization ("improve my deck", "fix my deck")
  - Energy calculations ("energy curve", "energy needs")

  **Provides:** Complete deck construction with validation, energy curve analysis, synergy recommendations, and optimization suggestions. References proven deck archetypes and meta strategies from comprehensive research.

  **Key benefit:** Legal, optimized, competitive-ready 20-card decks with detailed strategy explanations and improvement recommendations.
---

# Pokemon TCG Pocket Deck Builder

Build competitive Pokemon TCG Pocket decks with AI-powered analysis and strategy recommendations.

## Core Capabilities

### 1. Deck Construction Workflow

- **Initial Deck Build**: Start with a Pokemon ex or core strategy card
- **Synergy Analysis**: Find cards that work well together (same type + trainers)
- **Energy Optimization**: Calculate energy requirements (1-2 types recommended)
- **Coverage Analysis**: Ensure diverse Pokemon types for matchup flexibility

### 2. Pokemon TCG Pocket Rules Integration

- **Deck Size**: 20 cards (standard format)
- **Energy Zone**: Auto-generates 1 Energy/turn (NOT from deck)
- **Win Conditions**: 3 points (ex Pokemon = 2 pts, regular = 1 pt)
- **Bench Limit**: Max 3 Pokemon on bench (not 5 like standard TCG)
- **Turn 1**: No draw, no energy, no attack
- **Card Copies**: Max 2 copies per card

### 3. MCP Server Integration

Access 2000+ Pokemon cards via integrated MCP server:

**Tools Available:**

- `search_cards`: Search with filters (name, type, HP, set, rarity)
- `find_synergies`: Find cards that work well together
- `find_counters`: Identify cards that counter specific strategies
- `get_type_stats`: Analyze type distributions and averages
- `analyze_deck`: Get detailed deck composition analysis

**Example Queries:**

```
"Find synergies for Pikachu ex deck"
"Calculate energy needs for Grass/Poison deck"
"What counters a Water-type deck?"
"Show me all Fire Pokemon with high HP"
```

### 4. Strategic Analysis

**Deck Archetypes:**

- **Aggro**: Fast ex Pokemon, low energy costs
- **Control**: High HP Pokemon, defensive strategies
- **Tempo**: Early game pressure, mid-game finish

**Key Metrics:**

- Average HP and attack power
- Energy curve (cost distribution)
- Type diversity and coverage
- Trainer card efficiency

### 5. Sample Deck Building Session

```
Step 1: "Build a deck around Charizard ex"
→ Search for Charizard ex cards
→ Find Fire-type synergies
→ Identify energy requirements

Step 2: "Add support cards"
→ Search for Fire trainers
→ Find energy acceleration
→ Check for complementary Pokemon

Step 3: "Analyze the deck"
→ Calculate average HP/attack
→ Verify energy curve
→ Check for weaknesses

Step 4: "Find counters"
→ Identify deck's weaknesses
→ Suggest counter-strategies
→ Recommend improvements
```

## Best Practices

### Deck Composition

- **Core Pokemon**: 8-10 Pokemon (mix of ex and regular)
- **Trainers**: 4-6 cards (support, items, stadium)
- **Energy**: 0 (handled by energy zone)
- **Curve Balance**: Mix of 1-3 energy costs

### Type Synergies

- **Mono-type**: Consistent strategy, easier energy
- **Dual-type**: More flexibility, higher synergy potential
- **Avoid**: 3+ types (too inconsistent in 20-card format)

### Common Mistakes to Avoid

- Too many high-energy Pokemon (4+ cost)
- Inconsistent type spread
- Missing basic Pokemon for early game
- Overloading on trainer cards
- Not accounting for bench limits

## Documentation Resources

**Core References (in `docs/pokemon-tcg-pocket-research/`):**

- **rules/01-core-rules-guide.md** - Complete rules, turn structure, energy zone system
- **deckbuilding/01-deckbuilding-guide.md** - Deck building fundamentals and evolution timing
- **deckbuilding/02-deck-archetypes.md** - All 5 major archetypes (Aggro, Midrange, Control, Combo)
- **deckbuilding/03-budget-decks.md** - Budget competitive builds (under $50) + F2P options
- **strategies/04-energy-zone-mastery.md** - Energy zone mastery (THE most important mechanic)
- **meta/02-top-tier-decks.md** - 5 complete S-tier deck breakdowns with 20-card lists

**Advanced Resources (for competitive play):**

- **strategies/06-ultra-competitive-mastery.md** - Situational decision trees and exact responses
- **strategies/03-type-matchups.md** - Complete type effectiveness chart with 81 matchup scenarios
- **card-guides/01-best-cards-list.md** - 200+ cards evaluated S-F tier with budget alternatives

**Use these resources:** When building decks, reference these comprehensive guides for detailed strategies, complete tier lists, and proven deck compositions. These are located at `../../docs/pokemon-tcg-pocket-research/` relative to this skill.

## Workflow & Validation

### Deck Building Workflow

**Phase 1: Define Strategy**

```
1. Identify core Pokemon (typically 1-2 ex Pokemon)
2. Choose archetype (Aggro, Midrange, Control, Tempo)
3. Determine type strategy (mono-type vs dual-type)
4. Set budget constraints (budget vs premium)
```

**Phase 2: Build Core**

```
1. Search for core Pokemon: search_cards({name: "Pikachu ex"})
2. Find synergies: find_synergies({cardName: "Pikachu ex"})
3. Identify supporting Pokemon (8-10 total)
4. Select Trainer cards (4-6 cards)
```

**Phase 3: Validation**

```
Use analyze_deck tool to validate:
✅ Exactly 20 cards
✅ Max 2 copies per card
✅ At least 5-6 basic Pokemon
✅ 0 energy cards (auto-generated)
✅ Reasonable type distribution
```

**Phase 4: Optimization**

```
1. Analyze energy curve (1-3 energy costs)
2. Check for anti-synergies
3. Validate against meta
4. Test matchup spread
```

### Deck Validation Checklist

**Legal Compliance:**

- [ ] Exactly 20 cards
- [ ] Max 2 copies per card
- [ ] No energy cards (energy zone auto-generates)
- [ ] All card names match database
- [ ] Valid set codes (A1, A2, A3, A4b, P-A)

**Strategic Balance:**

- [ ] 5-6 basic Pokemon (early game)
- [ ] 2-3 ex Pokemon (win condition)
- [ ] 1-2 stage 2 evolution Pokemon (mid game)
- [ ] 4-6 Trainer cards (support)
- [ ] Type diversity: 1-2 types (consistency)

**Energy Curve:**

- [ ] 30% low-cost attackers (1 energy)
- [ ] 40% mid-cost attackers (2 energy)
- [ ] 20% high-cost attackers (3 energy)
- [ ] 10% utility/support

### Error Handling

**Invalid Card Names:**

```
Error: "Card 'X' not found in database"

Response:
- Suggest spellings (ILIKE matching)
- Show available cards with similar names
- Ask for clarification (ex vs regular)
- Provide query examples
```

**Illegal Deck Composition:**

```
Error: "Deck has 25 cards (max 20)"

Response:
- List which cards exceed limit
- Suggest cards to remove
- Recommend prioritization
- Show complete analysis
```

**Too Many Copies:**

```
Error: "3 copies of Pikachu ex (max 2)"

Response:
- Identify duplicate cards
- Suggest alternatives
- Maintain energy curve
- Validate remaining 18 cards
```

**Missing Basics:**

```
Warning: "Only 3 basic Pokemon (recommend 5-6)"

Response:
- List current basics
- Suggest additional basics
- Explain importance (early game)
- Show revised composition
```

**Energy Zone Confusion:**

```
Error: "10 energy cards in deck"

Response:
- Clarify: No energy cards in TCG Pocket
- Explain energy zone system
- Reference: strategies/04-energy-zone-mastery.md
- Provide corrected deck list
```

### Common Deck Problems & Solutions

**Problem: Inconsistent Energy**

```
Symptoms: Multiple types (3+), high energy costs

Solution:
- Reduce to 1-2 types maximum
- Lower average energy cost
- Reference: strategies/04-energy-zone-mastery.md
```

**Problem: No Win Condition**

```
Symptoms: No ex Pokemon, only basics

Solution:
- Add 2-3 ex Pokemon
- Build around ex as focal point
- Reference: meta/02-top-tier-decks.md
```

**Problem: Bench Overflow**

```
Symptoms: More than 3 benched Pokemon

Solution:
- Reduce bench Pokemon
- Focus on active Pokemon
- Reference: rules/01-core-rules-guide.md
```

**Problem: No Synergy**

```
Symptoms: Random card collection, no theme

Solution:
- Find card synergies: find_synergies
- Choose type-based strategy
- Reference: deckbuilding/02-deck-archetypes.md
```

### Progressive Disclosure

**Level 1: Basic Deck**

```
Provide: 20-card list, simple validation
Good for: Beginners, casual play
```

**Level 2: Optimized Deck**

```
Add: Energy curve analysis, synergy explanations
Good for: Intermediate players
```

**Level 3: Competitive Deck**

```
Add: Meta positioning, matchup analysis, tech cards
Good for: Tournament play
```

**Level 4: Expert Build**

```
Add: Advanced tech, sideboard options, meta adaptation
Good for: High-level competition
```

### Quality Standards

**Deck Lists Must Include:**

1. Card names (exact database match)
2. Card counts (e.g., "2x Pikachu ex")
3. Validation summary (legal/compliant)
4. Strategy explanation
5. Matchup notes
6. Improvement suggestions

**Validation Report Format:**

```
=== DECK VALIDATION REPORT ===

Legal Status: ✅ VALID
- Card Count: 20/20
- Max Copies: ✅ All cards ≤2 copies
- Basic Pokemon: 6 (recommended: 5-6)
- EX Pokemon: 2 (recommended: 2-3)

Composition:
- Pokemon: 14 (70%)
- Trainers: 6 (30%)
- Types: Lightning (14), Colorless (6)

Energy Curve:
- 1-energy: 8 cards
- 2-energy: 6 cards
- 3-energy: 0 cards

Warnings: None

Suggestions:
- Consider adding tech card for Fighting matchup
- See meta/02-top-tier-decks.md for optimization
```

## MCP Server Configuration

The Pokemon MCP server is automatically integrated:

- Database: 2077 cards across 12 sets
- Unique Cards: 1068 (auto-deduplicated art variants)
- Search: Advanced filters and SQL queries
- Analysis: Deck stats, type breakdowns, synergy matching

## Usage Examples

**Deck Building:**

```
"Build an ultra-competitive Mewtwo ex deck"
"Optimize my current Grass deck"
"Find the best cards for a Water-type strategy"
```

**Analysis:**

```
"Analyze my deck's energy curve"
"What Pokemon should I add to counter Fire decks?"
"Show me all Psychic Pokemon with good attacks"
"Calculate average HP of my current deck"
```

**Strategy:**
"What's the current meta for competitive play?"
"How do I beat ex Pokemon heavy decks?"
"What trainers work best with Pikachu ex?"

```

```
