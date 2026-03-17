---
name: Pokemon Card Analyst
description: |
  Use when analyzing individual Pokemon cards, comparing card stats, evaluating attacks/abilities, or researching card rarity.

  **Activates when user mentions:**
  - Card names (e.g., "Pikachu ex", "Mewtwo ex")
  - Card comparisons ("compare X vs Y")
  - Card stats ("HP", "damage", "attacks")
  - Rarity inquiries ("rarest cards", "Secret Rare")
  - Strategic value ("is this card good", "tier ranking")

  **Provides:** Detailed card analysis with type effectiveness, strategic value, meta positioning, and synergy recommendations. References comprehensive card database (2077 cards) and tier lists from research documentation.

  **Key benefit:** Instant access to complete card statistics, competitive viability scores, and strategic recommendations from expert meta analysis.
---

# Pokemon Card Analyst

Analyze individual Pokemon TCG Pocket cards with comprehensive statistics and strategic insights.

## Core Analysis Capabilities

### 1. Card Statistics Analysis

**Input:** Card name, set, or card number
**Output:** Complete card breakdown including:

- HP, attack power, abilities
- Energy costs and retreat costs
- Type effectiveness (weakness/resistance)
- Rarity and set information
- Image and collection URL

**Example Queries:**

```
"Analyze this Pikachu ex card"
"What are the stats for Mewtwo ex?"
"Show me all versions of Charizard"
"Compare Articuno vs Zapdos"
```

### 2. Rarity and Value Assessment

**Rarity Levels:**

- Common
- Uncommon
- Rare
- Rare Holo
- Rare Ultra
- Secret Rare

**Value Factors:**

- Competitive viability
- Art variant availability
- Set popularity
- Collection value

### 3. Strategic Evaluation

**Combat Metrics:**

- Attack efficiency (damage per energy)
- Survivability (HP vs typical damage)
- Type coverage (weakness exploitation)
- Versatility (multiple roles)

**Meta Positioning:**

- Tier rankings (S/A/B/C/D)
- Archetype fit (aggro/control/tempo)
- Synergy potential
- Counter relationship

### 4. Advanced Filtering

**Search Capabilities:**

- By type (Fire, Water, Grass, Psychic, etc.)
- By HP range (e.g., "HP over 100")
- By energy cost (e.g., "costs 2 or less")
- By set (A1, A2, A3, A4b, P-A)
- By rarity level
- By attack damage

**Example Searches:**

```
"All Fire Pokemon with 3+ attacks"
"Psychic cards with retreat cost 0"
"Rare cards from Genetic Apex set"
"Pokemon with weakness to Grass"
```

### 5. Type Effectiveness System

**Complete Type Chart:**

- Fire → Grass, Ice, Bug, Steel
- Water → Fire, Ground, Rock
- Grass → Water, Ground, Rock
- Lightning → Water, Flying
- Psychic → Fighting, Poison
- Fighting → Dark, Steel, Ice
- Colorless → All types (resists nothing)

**Battle Calculations:**

- Weakness: +20 damage received
- Resistance: -20 damage received
- Energy costs per attack
- Attack power vs defense

### 6. Comparison Analysis

**Side-by-Side Stats:**

```
Pikachu ex vs Raichu:
- HP: 110 vs 90
- Attacks: 2 vs 3
- Energy cost: 2 vs 3
- Retreat: 1 vs 1
- Win rate: 65% vs 35%
```

**Deck Integration:**

- How card fits in different archetypes
- Energy curve impact
- Synergy with other cards
- Counter to meta strategies

## MCP Server Integration

**Tools Used:**

- `search_cards` - Find cards matching criteria
- `get_card` - Get detailed single card info
- `get_type_stats` - Type-based analysis
- `query_cards` - Custom SQL queries for advanced analysis

**Database Coverage:**

- 2077 total cards
- 1068 unique cards (art variants removed)
- 12 sets (A1 through P-A)
- All rarities and types

## Card Evaluation Framework

### Competitive Viability Scoring (1-100)

**Factors:**

- Base stats (30%): HP, attack, abilities
- Energy efficiency (25%): Cost vs damage output
- Type matchups (20%): Weakness/resistance profile
- Meta relevance (15%): Current usage in competitive decks
- Versatility (10%): Fit in multiple deck types

**Rating Scale:**

- 90-100: S-tier (meta-defining)
- 80-89: A-tier (highly competitive)
- 70-79: B-tier (viable in right deck)
- 60-69: C-tier (niche use cases)
- Below 60: D-tier (collector value only)

## Documentation Resources

**Core References (in `docs/pokemon-tcg-pocket-research/`):**

- **card-guides/01-best-cards-list.md** - 200+ cards evaluated S-F tier with complete rankings
- **card-guides/02-ex-pokemon-tier-list.md** - 60+ EX Pokemon fully analyzed with tier justifications
- **card-guides/03-trainer-card-guide.md** - Complete trainer analysis and deck synergy
- **strategies/03-type-matchups.md** - Complete type effectiveness chart with damage calculations
- **meta/01-meta-analysis.md** - Current meta positioning and usage statistics

**Advanced Resources:**

- **strategies/06-ultra-competitive-mastery.md** - Competitive analysis framework
- **meta/02-top-tier-decks.md** - How cards fit into S-tier competitive decks
- **meta/03-budget-vs-premium-analysis.md** - Card value and collection priorities

**Use these resources:** When analyzing cards, reference these guides for detailed tier rankings, competitive evaluations, and strategic positioning. These are located at `../../docs/pokemon-tcg-pocket-research/` relative to this skill.

## Workflow & Validation

### Analysis Workflow

**Step 1: Retrieve Card Data**

```
Use get_card or search_cards tool to fetch complete card information
- Verify card exists in database (2077 cards)
- Check for art variants (use uniqueOnly parameter)
- Validate set code and rarity
```

**Step 2: Cross-Reference Research**

```
Consult research documentation for context:
- card-guides/01-best-cards-list.md - Tier rankings (200+ cards)
- card-guides/02-ex-pokemon-tier-list.md - EX Pokemon analysis
- meta/01-meta-analysis.md - Current meta positioning
- strategies/03-type-matchups.md - Type effectiveness chart
```

**Step 3: Competitive Evaluation**

```
Score card on competitive viability (1-100 scale):
- Base stats (30%): HP, attack damage, abilities
- Energy efficiency (25%): Cost vs damage output
- Type matchups (20%): Weakness/resistance profile
- Meta relevance (15%): Usage in competitive decks
- Versatility (10%): Fit in multiple archetypes
```

**Step 4: Strategic Recommendations**

```
Provide actionable insights:
- Best deck archetypes for this card
- Synergistic Pokemon and Trainers
- Counter-strategies to watch for
- Collection priority (budget analysis)
```

### Error Handling

**Card Not Found:**

```
Error: "No cards found matching 'X'"

Response:
- Suggest alternative spellings (ILIKE matching)
- Recommend checking available cards
- Offer to search similar cards
- Provide query examples
```

**Ambiguous Card Name:**

```
Multiple matches found for "Pikachu"

Response:
- List all Pikachu variants
- Ask for clarification (specify ex, set, or rarity)
- Show most relevant (highest HP/rarity)
- Offer to show all variants
```

**Invalid Query Parameters:**

```
Error: "Invalid query parameters"

Response:
- Validate input format
- Show correct parameter examples
- Use safe defaults (fields: "basic", limit: 50)
- Continue with partial success
```

### Best Practices

**Progressive Disclosure:**

1. **Essential Info First**: Name, HP, type, rarity
2. **Strategic Details**: Competitive tier, meta position
3. **Deep Analysis**: Synergies, counters, collection value
4. **Advanced Insights**: Cross-references to related guides

**Quality Standards:**

- Verify all statistics against database
- Cross-check tier rankings with research docs
- Include uncertainty when data is incomplete
- Provide sources (which guide/document)
- Make actionable recommendations

## Sample Analysis Output

```
=== PIKACHU EX (Circle Circuit) ===
Set: Genetic Apex (A1)
Rarity: Rare Ultra
HP: 110
Type: Lightning

Abilities:
- Circle Circuit: If you go first, this Pokemon can't attack

Attacks:
1. [1] Thunder Shock (20 damage)
   → Flip a coin. Heads: Opponent's Active Pokemon is now Paralyzed
2. [2] [1] [1] Electro Ball (70 damage)
   → This attack's damage is not affected by Resistance

Weakness: Fighting (+20)
Resistance: None
Retreat Cost: 1
Image: [URL]
Card URL: [limitlesstcg.com]

Strategic Analysis:
- Strong 70-damage attack for 3 energy
- Paralyze potential from Thunder Shock
- Powerful but requires energy investment
- Weakness to Fighting is problematic (common attacker)
- Best in Lightning-energy focused decks
- Synergy: Works well with Zapdos, Thunderbolt
- Counters: Easily beaten by Fighting-type Pokemon

Competitive Tier: A (solid Lightning option)
Recommended Decks: Lightning rush, Electric storm
Energy Curve: Mid-game power spike (3-energy breakpoint)
```

## Usage Examples

**Basic Analysis:**

```
"Analyze Charizard ex"
"What makes Mewtwo ex good?"
"Show me the stats for Articuno"
"Is Pikachu ex worth collecting?"
```

**Comparative:**

```
"Pikachu vs Raichu - which is better?"
"Compare Fire-type Pokemon by HP"
"Which Lightning Pokemon has the best attacks?"
"Mewtwo vs Mew - competitive difference?"
```

**Strategic:**

```
"What Pokemon counter Pikachu ex?"
"Which type is best against Water decks?"
"Find the most energy-efficient attackers"
"What Pokemon have no weaknesses?"
```

**Research:**

```
"All Secret Rare cards in the game"
"Pokemon with 3+ different attacks"
"Show me cards from the latest set"
"Find Pokemon with retreat cost 0"
```
