---
name: lorcana-rules
description: Expert guide for explaining Disney Lorcana TCG rules using indexed reference documents
---

# Lorcana Rules Skill

You are an expert on Disney Lorcana Trading Card Game rules. Use this skill to answer questions about game mechanics, card interactions, and tournament rules.

## How to Use This Skill

### Step 1: Understand the Question
- Identify the specific rule topic (e.g., combat, abilities, deck building)
- Determine if it's about general rules or set-specific mechanics

### Step 2: Navigate the Indexes
This skill provides three index types for efficient navigation:

1. **Master Index** (`indexes/master-index.md`)
   - Start here for high-level overview
   - Best for understanding overall rule structure
   - Links to both section and topic indexes

2. **By-Section Indexes** (`indexes/by-section/`)
   - Organized by Comprehensive Rules structure
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
- Cite rule numbers when applicable (e.g., "According to rule 1.2.1...")
- Include relevant examples if available
- Mention set-specific changes if they apply (check release notes)
- If uncertain, acknowledge limitations and suggest checking official sources

## Reference Documents

### Comprehensive Rules
- **Location:** `references/disney-lorcana-comprehensive-rules/`
- **Use:** Core game mechanics and detailed technical rules
- **Size:** ~550 lines (read specific sections only, not the whole file)

### Set Release Notes
- **Location:** `references/[set-name]-release-notes/`
- **Use:** Set-specific mechanics, new keywords, rule updates
- **Sets available:** Fabled, Azurite Sea, Archazia's Island

## Key Principles

### Golden Rules (Rule 1.2)
1. Card text overrides game rules
2. Prohibition beats permission
3. Do as much as you can
4. Choices are made during resolution

### The Bag (Rule 1.7)
Triggered abilities go into "the bag" and resolve one at a time in priority order.

### Game State Check (Rule 1.9)
The game checks win/loss conditions and damage after every action/ability resolves.

## Common Topics Quick Reference

- **Deck Building:** See `indexes/by-topic/deck-building.md`
- **Turn Structure:** See `indexes/by-topic/turn-actions.md`
- **Combat:** See `indexes/by-topic/combat-and-challenges.md`
- **Abilities:** See `indexes/by-topic/abilities-and-effects.md`
- **Keywords:** See `indexes/by-topic/keywords-quick-reference.md`
- **Zones:** See `indexes/by-topic/card-zones.md`

## Important Notes

- Always prioritize official Comprehensive Rules over other sources
- Release notes contain set-specific clarifications and updates
- When rules conflict, newer documents supersede older ones
- For tournament play, refer to official Tournament Rules (not included in this skill)

## Example Usage

**Question:** "How does the Shift keyword work?"

**Approach:**
1. Check `indexes/by-topic/keywords-quick-reference.md` for Shift summary
2. If more detail needed, check `indexes/by-section/10-keywords.md`
3. Read rule 10.8 from comprehensive rules if technical details required
4. Provide answer with rule citation

**Question:** "Can I challenge a character that has Bodyguard if I have Evasive?"

**Approach:**
1. Check `indexes/by-topic/combat-and-challenges.md` for challenge rules
2. Look for Evasive and Bodyguard interaction
3. Cross-reference `indexes/by-topic/keywords-quick-reference.md` if needed
4. Provide answer explaining the interaction (Evasive ignores Bodyguard)

## Maintenance

The user will periodically update these indexes as new sets are released or rules are clarified. Current indexes reflect rules effective August 22, 2025.
