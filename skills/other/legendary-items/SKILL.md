---
name: legendary-items
description: Extract legendary item entities from narrative text. Use when analyzing mythical weapons, armor, divine items, cursed items, artifact sets, runes, glyphs, and enchantments.
---
# legendary-items

Domain skill for Legendary Items Specialist. Specific extraction rules and expertise.

## Domain Expertise

- **Legendary items**: Extremely rare, powerful, unique items
- **Artifacts**: Ancient, historical, lore-rich items
- **Cursed items**: Powerful but come with penalties
- **Item sets**: Multiple items that combine for bonus effects
- **Enchantments**: Magical enhancements, glyphs, runes, sockets
- **Lore significance**: Items with history, myths, legends

## Entity Types (10 total)

- **legendary_weapon** - Legendary weapons
- **mythical_armor** - Mythical armor
- **divine_item** - Divine items
- **cursed_item** - Cursed items
- **artifact_set** - Artifact sets
- **relic_collection** - Relic collections
- **glyph** - Glyphs
- **rune** - Runes
- **socket** - Sockets
- **enchantment** - Enchantments

## Processing Guidelines

When extracting legendary item entities from chapter text:

1. **Identify legendary item elements**:
   - Legendary or mythical items mentioned
   - Artifacts or relics with history
   - Cursed items or cursed equipment
   - Item sets or collections
   - Enchantments, runes, glyphs, sockets

2. **Extract legendary item details**:
   - Item names, types, rarities
   - Stats and abilities
   - Lore and history
   - Curse effects (for cursed items)
   - Set bonuses (for item sets)
   - Enchantment types and powers

3. **Analyze legendary item context**:
   - Power level vs balance
   - Lore significance and rarity
   - Acquisition difficulty
   - Trade-offs (curses, limitations)

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Power vs balance**: Legendary items should be powerful but not game-breaking
- **Lore significance**: Items should have history and meaning
- **Acquisition difficulty**: Legendary = rare, challenging to get
- **Trade-offs**: Cursed items have benefits but also penalties
- **Set bonuses**: Full sets should feel rewarding
