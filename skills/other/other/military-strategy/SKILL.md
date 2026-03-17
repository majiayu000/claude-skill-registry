---
name: military-strategy
description: Extract military entities from narrative text. Use when analyzing armies, fleets, battalions, weapons, fortifications, siege engines, wars, invasions, and revolutions.
---
# military-strategy

Domain skill for Military Strategist. Specific extraction rules and expertise.

## Domain Expertise

- **Military structure**: Armies, navies, units, command hierarchy
- **Warfare**: Strategy, tactics, battles, campaigns
- **Weapons**: Swords, bows, siege engines, magic weapons
- **Fortifications**: Castles, walls, bunkers, defensive positions
- **Conflicts**: Wars, revolutions, rebellions, invasions

## Entity Types (10 total)

- **army** - Armies
- **fleet** - Naval fleets
- **battalion** - Military units
- **weapon_system** - Weapons and technology
- **defense** - Defenses and fortifications
- **fortification** - Fortified structures
- **siege_engine** - Siege weapons
- **war** - Wars and conflicts
- **invasion** - Invasions
- **revolution** - Revolutions

## Processing Guidelines

When extracting military entities from chapter text:

1. **Identify military elements**:
   - Armies, navies, military units mentioned
   - Weapons, armor, combat gear
   - Fortifications, castles, defensive structures
   - Wars, battles, conflicts mentioned
   - Revolutions, rebellions, invasions

2. **Extract military details**:
   - Army/navy size, composition, leadership
   - Weapon types, technology levels
   - Fortification types, defensive capabilities
   - War causes, participants, outcomes
   - Strategic objectives

3. **Analyze military context**:
   - Military strength vs weakness
   - Strategic advantages/disadvantages
   - Technology level differences
   - Victory or defeat factors

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Technology levels**: Different factions may have different tech
- **Asymmetric warfare**: Guerrilla tactics vs conventional armies
- **Magical warfare**: Some worlds have magic weapons/units
- **Veterancy**: Experienced units vs raw recruits
