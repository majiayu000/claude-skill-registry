---
name: riftbound-rules
description: Expert guide for explaining Riftbound TCG rules using indexed reference documents. Use when answering questions about game mechanics, card interactions, combat, abilities, or tournament rules.
---

# Riftbound Rules Skill

You are an expert on Riftbound Trading Card Game rules. Use this skill to answer questions about game mechanics, card interactions, combat, abilities, and tournament rules.

## How to Use This Skill

### Step 1: Understand the Question
- Identify the specific rule topic (e.g., combat, abilities, deck building, keywords)
- Determine if it's about general rules or mode-specific mechanics

### Step 2: Navigate the Indexes
This skill provides three index types for efficient navigation:

1. **Master Index** (`indexes/master-index.md`)
   - Start here for high-level overview
   - Best for understanding overall rule structure
   - Links to both section and topic indexes

2. **By-Section Indexes** (`indexes/by-section/`)
   - Organized by Core Rules structure (rule numbers)
   - Best when you know the rule category (e.g., "turn structure", "abilities")
   - Contains detailed rule number references

3. **By-Topic Indexes** (`indexes/by-topic/`)
   - Organized by common player questions
   - Best for practical gameplay questions
   - Groups related rules from different sections

### Step 3: Search Strategy
1. Check the most relevant index first (topic index for gameplay questions, section index for technical rules)
2. Read the summary and key terms to confirm relevance
3. If needed, read the specific section from the full reference document
4. Only read full reference sections when index summaries are insufficient

### Step 4: Answer Format
When answering rule questions:
- Provide the rule explanation clearly and concisely
- Cite rule numbers when applicable (e.g., "According to rule 620...")
- Include relevant examples if available
- Mention mode-specific changes if they apply
- If uncertain, acknowledge limitations and suggest checking official sources

## Reference Documents

### Core Rules
- **Location:** `references/`
- **Files:** Split across 4 files by page range (01-20, 21-40, 41-60, 61-65)
- **Use:** Complete game mechanics and detailed technical rules
- **Note:** Read specific sections only, not entire files

## Golden and Silver Rules

### Golden Rule (Rule 001-002)
**Card text supersedes rules text.** Whenever a card fundamentally contradicts the rules, the card's indication is what is true.

### Silver Rule (Rule 050-053)
**Card text uses different terminology than rules.** Card text should be interpreted according to these rules, not as though it were text within these rules.

Key terminology differences:
- "Card" on cards means "Main Deck card" (excludes runes, legends, battlefields)
- Cards refer to themselves in first person:
  - Units and legends: "I," "me," etc.
  - Gear and spells: "this"
  - Battlefields: "here"

## Key Game Concepts

### Six Domains
Each domain has an associated color and symbol:
- **Fury** - Red (circular symbol with three projecting points)
- **Calm** - Green (leaf symbol)
- **Mind** - Blue (sun and moon symbol)
- **Body** - Orange (blocky diamond symbol)
- **Chaos** - Purple (hexagonal symbol with swirls)
- **Order** - Yellow (angular winged symbol)

### Deck Construction (Rule 101-103)
- **Champion Legend** - Placed in Legend Zone, dictates Domain Identity
- **Main Deck** - At least 40 cards, max 3 copies of same named card
- **Chosen Champion** - Champion unit matching your Legend's tag
- **Rune Deck** - Exactly 12 runes
- **Battlefields** - Number determined by Mode of Play

### Turn States (Rule 507-510)
The turn is always in one of four states:
- **Neutral Open** - No Showdown, no Chain (default state for playing cards)
- **Neutral Closed** - No Showdown, Chain exists
- **Showdown Open** - Showdown in progress, no Chain
- **Showdown Closed** - Showdown in progress, Chain exists

### The Chain (Rule 532-544)
- Temporary zone for spells and abilities being resolved
- Cards/abilities resolve last-in-first-out (LIFO)
- Only Reaction cards can be played during Closed States

### Scoring (Rule 629-633)
Two ways to score:
- **Conquer** - Gain control of a battlefield you didn't score this turn
- **Hold** - Control a battlefield during your Beginning Phase

Victory Scores by mode:
- 1v1: 8 points
- FFA3/FFA4: 8 points
- 2v2: 11 points

## Common Topics Quick Reference

- **Deck Building:** See `indexes/by-topic/deck-building.md`
- **Turn Structure:** See `indexes/by-topic/turn-actions.md`
- **Combat:** See `indexes/by-topic/combat-and-showdowns.md`
- **Abilities:** See `indexes/by-topic/abilities-and-effects.md`
- **Keywords:** See `indexes/by-topic/keywords-quick-reference.md`
- **Runes & Resources:** See `indexes/by-topic/runes-and-resources.md`
- **Modes of Play:** See `indexes/by-topic/modes-of-play.md`

## Important Notes

- Always prioritize official Core Rules over other sources
- When rules conflict, card text wins (Golden Rule)
- For tournament play, refer to official Tournament Rules (not included in this skill)
- Rule numbers in format XXX or XXX.X.X (e.g., 620, 620.1.a)

## Example Usage

**Question:** "How does the Hidden keyword work?"

**Approach:**
1. Check `indexes/by-topic/keywords-quick-reference.md` for Hidden summary
2. If more detail needed, check `indexes/by-section/09-keywords.md`
3. Read rule 723 from reference if technical details required
4. Provide answer with rule citation

**Question:** "When does combat happen?"

**Approach:**
1. Check `indexes/by-topic/combat-and-showdowns.md` for combat triggers
2. Cross-reference `indexes/by-section/07-combat.md` if needed
3. Provide answer explaining Combat occurs when a Cleanup happens with opposing units at a Battlefield (Rule 621)

**Question:** "Can I play a spell during my opponent's turn?"

**Approach:**
1. Check `indexes/by-topic/turn-actions.md` for timing rules
2. Look for Action/Reaction keywords in `indexes/by-topic/keywords-quick-reference.md`
3. Answer: Only with Reaction keyword (Rule 725) or during Showdowns with Action keyword (Rule 718)

## Maintenance

The indexes reflect Riftbound Core Rules effective June 2, 2025.
