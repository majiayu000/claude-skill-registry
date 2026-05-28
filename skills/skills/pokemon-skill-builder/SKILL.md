---
name: Pokemon TCG Pocket Skill Builder
description: Use when building Claude Code skills or plugins for Pokemon TCG Pocket. Creates Pokemon-specific commands, integrates MCP servers, scaffolds deck-building workflows, and provides templates for Pokemon automation tools. Covers Claude skill structure and Pokemon integration patterns.
---

# Pokemon TCG Pocket Skill Builder

Build Claude Code skills and plugins for Pokemon TCG Pocket with proven templates and best practices.

## Purpose

This skill helps developers create Claude Code extensions for Pokemon TCG Pocket, integrating the Pokemon Pocket MCP server and providing automation for deck building, card analysis, and meta strategies.

## Core Templates

### 1. Basic Pokemon Skill Template

```yaml
---
name: Skill Name
description: Use when [trigger condition]. Activates when user mentions [keywords].
---
# Skill Title

[Instructions for Claude Code]
```

### 2. Pokemon Deck Command Template

```markdown
---
name: build-deck
description: Build a Pokemon TCG Pocket deck around a specific Pokemon or strategy
---

# Build Pokemon TCG Pocket Deck

Use the Pokemon Pocket MCP server to create a competitive 20-card deck.

## Input Requirements

- Core Pokemon or strategy
- Preferred playstyle (aggro/control/tempo)
- Budget constraints (optional)
- Existing cards (optional)

## Process

1. Search for core Pokemon using MCP `search_cards`
2. Find synergies using `find_synergies`
3. Calculate energy requirements
4. Verify deck composition (20 cards, max 2 copies)
5. Analyze using `analyze_deck`
6. Provide optimization suggestions

## Output

- Complete 20-card deck list
- Energy curve analysis
- Strategic explanation
- Counter-strategy recommendations
```

### 3. Pokemon Analysis Command Template

```markdown
---
name: analyze-card
description: Analyze Pokemon card stats, competitive value, and strategic usage
---

# Analyze Pokemon Card

Provide comprehensive card analysis using Pokemon Pocket MCP server.

## Input

- Card name or criteria
- Analysis focus (stats/rarity/meta)

## Process

1. Search card using `get_card` or `search_cards`
2. Retrieve type stats using `get_type_stats`
3. Calculate competitive viability
4. Find counters using `find_counters`
5. Generate comparison data

## Output

- Complete card breakdown
- Competitive tier rating
- Strategic usage guide
- Counter-strategy recommendations
```

## MCP Server Integration

### Pokemon Pocket MCP Configuration

```json
{
  "mcpServers": {
    "pokemon-pocket-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["pokemon-pocket-mcp-server"],
      "env": {}
    }
  }
}
```

### Available MCP Tools

- `search_cards` - Search with filters
- `get_card` - Get specific card details
- `find_synergies` - Find card synergies
- `find_counters` - Find counter cards
- `get_type_stats` - Type analysis
- `query_cards` - Custom SQL queries
- `analyze_deck` - Deck analysis

### MCP Resources

- `pokemon://cards/all` - Full database (2077 cards)
- `pokemon://cards/unique` - Unique cards (1068)
- `pokemon://stats/types` - Type breakdowns

### MCP Prompts

- `build-deck` - Deck building prompt
- `counter-deck` - Counter-strategy prompt
- `optimize-deck` - Deck optimization prompt

## Skill Structure Best Practices

### Frontmatter Requirements

```yaml
---
name: Clear name (64 chars max)
description: |
  Use when [trigger].
  Activates when user mentions [keywords].
  Keep under 1024 characters.
---
```

### Content Organization

1. **Overview** (100-200 words)
2. **Core Capabilities** (with examples)
3. **MCP Integration** (tools and resources)
4. **Usage Examples** (real queries)
5. **Best Practices** (do's and don'ts)
6. **Bundled Resources** (scripts/references)

### Pokemon-Specific Guidelines

**Deck Building:**

- Always specify 20-card format
- Include energy zone rules (no energy in deck)
- Mention 3-point win condition
- Reference bench limit (3 Pokemon)
- Max 2 copies per card

**Card Analysis:**

- Include weakness/resistance
- Show energy efficiency
- Mention retreat cost
- Reference competitive tier
- Provide type coverage

**Meta Analysis:**

- Current tier system (S-D)
- Usage statistics
- Matchup percentages
- Strategic recommendations
- Budget considerations

## Common Patterns

### Pattern 1: Deck Build Workflow

```
1. Get user requirements
2. Search core cards via MCP
3. Find synergies
4. Calculate energy curve
5. Verify deck rules
6. Analyze with MCP
7. Provide optimization
8. Suggest counters
```

### Pattern 2: Card Analysis Workflow

```
1. Retrieve card data via MCP
2. Calculate competitive metrics
3. Find similar cards
4. Identify counters
5. Generate tier rating
6. Provide strategic guide
```

### Pattern 3: Meta Analysis Workflow

```
1. Query database for statistics
2. Calculate usage rates
3. Analyze matchup matrix
4. Generate tier lists
5. Provide strategic advice
```

## Testing Pokemon Skills

### Test Scenarios

1. **Deck Building Test:**

   ```
   Input: "Build Mewtwo ex deck"
   Check: 20 cards, proper energy curve, competitive viability
   ```

2. **Card Analysis Test:**

   ```
   Input: "Analyze Charizard ex"
   Check: All stats, type effectiveness, tier rating
   ```

3. **Meta Query Test:**
   ```
   Input: "Current S-tier Pokemon"
   Check: Accurate tier list, supporting data
   ```

### Validation Checklist

- [ ] MCP server accessible
- [ ] All tools working correctly
- [ ] Pokemon rules accurately represented
- [ ] Examples tested and working
- [ ] Frontmatter properly formatted
- [ ] Under token limits (2000 for body)

## Bundled Resources

### Scripts Directory

- `deck-validator.js` - Validate deck composition
- `energy-calculator.js` - Calculate energy curves
- `type-counter.js` - Generate counter lists
- `meta-analyzer.js` - Analyze meta trends

### References Directory

- `pokemon-rules.md` - Complete game rules
- `type-chart.md` - Type effectiveness
- `tier-lists.md` - Current tier rankings
- `deck-archetypes.md` - Archetype guides

### Assets Directory

- `type-chart.png` - Visual type effectiveness
- `tier-rankings.jpg` - Tier list graphic
- `energy-curve.png` - Energy curve examples

## Example Complete Skill

```yaml
---
name: Pokemon Deck Optimizer
description: Use when optimizing existing Pokemon TCG Pocket decks. Improves deck consistency, fixes energy curves, finds missing synergies, and provides competitive enhancements based on current meta.
---

# Pokemon Deck Optimizer

Optimize Pokemon TCG Pocket decks for competitive play.

## Optimization Process

### 1. Current Deck Analysis
- Use MCP `analyze_deck` for composition
- Identify energy curve issues
- Calculate average HP/attack
- Find missing synergies

### 2. Meta Alignment
- Compare to S-tier strategies
- Identify power level gaps
- Suggest meta-appropriate additions
- Maintain 20-card format

### 3. Energy Curve Fixes
- Calculate energy distribution
- Ensure 1-2 type focus
- Avoid 3+ energy costs
- Balance early/mid/late game

### 4. Synergy Improvements
- Use `find_synergies` for additions
- Enhance type coverage
- Add counter-strategies
- Maintain consistency

## Output Format

```

OPTIMIZED DECK: [Name]

Changes Made:

- Removed: [Cards removed with reasoning]
- Added: [Cards added with reasoning]
- Kept: [Cards kept with justification]

Energy Curve: [Before] → [After]
Type Distribution: [Chart]
Competitive Tier: [Rating]

Key Improvements:

1. [Improvement with data]
2. [Improvement with data]
3. [Improvement with data]

Expected Matchups:

- vs Lightning: [Win rate]
- vs Psychic: [Win rate]
- vs Fire: [Win rate]

````

## Pokemon Skill Marketplace

### Publishing Requirements
- Complete README.md
- Working examples
- Tested MCP integration
- Version tag (1.0.0)
- GitHub repository

### Distribution
```json
{
  "commands": ["./commands/"],
  "skills": ["./skills/"],
  "mcpServers": {
    "pokemon-pocket": {
      "type": "stdio",
      "command": "npx",
      "args": ["pokemon-pocket-mcp-server"]
    }
  }
}
````

## Usage Examples

**Skill Creation:**

```
"Create a skill for deck building"
"Build a command for card analysis"
"Scaffold a meta analysis skill"
```

**Integration:**

```
"Add Pokemon MCP to my plugin"
"Connect deck analysis to existing skill"
"Integrate card search in my workflow"
```

**Templates:**

```
"Show me Pokemon skill template"
"Give me deck building command example"
"Provide Pokemon analysis pattern"
```
