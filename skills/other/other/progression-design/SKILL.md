---
name: progression-design
description: Extract progression entities from narrative text. Use when analyzing skills, perks, attributes, experience, level-ups, talent trees, mastery systems, and character advancement.
---
# progression-design

Domain skill for progression-engineer subagent. Specific extraction rules and expertise.

## Domain Expertise

- **RPG progression**: Levels, XP, skill points, talent trees, character advancement
- **Attributes**: Core stats (STR, DEX, INT), derived stats, stat scaling
- **Skills**: Active abilities, passive perks, character traits, talent specializations
- **Balance**: Progression curves, diminishing returns, power spikes, advancement pacing
- **Mastery systems**: Specialization paths, expertise levels, skill trees

## Entity Types (10 total)

- **skill** - Character abilities, active powers, combat techniques
- **perk** - Passive bonuses, innate advantages, automatic benefits
- **trait** - Character traits, personality attributes, inherent qualities
- **attribute** - Core stats (STR, DEX, INT, etc.), derived statistics
- **experience** - XP tracking, advancement points, progression currency
- **level_up** - Level thresholds, advancement milestones, power increases
- **talent_tree** - Skill trees, specialization paths, ability trees
- **mastery** - Mastery levels, expertise tiers, skill proficiency
- **progression_event** - Specific progression moments, advancement events
- **progression_state** - Current progression status, character advancement state

## Processing Guidelines

When extracting progression entities from chapter text:

1. **Identify progression elements**:
   - Level mentions or milestones (level 5, reached a new tier)
   - Skill/ability unlocks (learned a new technique)
   - Stat improvements or changes (stronger, faster, smarter)
   - Training or learning moments (completed training, mastered something)

2. **Extract progression details**:
   - What characters can do now vs before (new capabilities)
   - New abilities or power levels (strength increases)
   - Attribute changes (agility increased, intelligence boosted)
   - Talent trees or specializations mentioned (skill paths)

3. **Track progression events**:
   - Level up moments (Kira reached level 15)
   - Skill unlocks (learned Shadow Strike)
   - Training completions (mastered the elder's teachings)
   - Mastery achievements (expertise in shadow arts)

4. **Contextualize progression**:
   - Which character is progressing
   - What triggered the advancement
   - How the progression affects capabilities
   - Multiple characters (track all, not just protagonist)

## Output Format

Generate `entities/progression.json` with plural collections and domain fields:

```json
{
  "skills": [
    {
      "id": 1,
      "character_id": 3,
      "name": "Shadow Strike",
      "description": "Deal 200% damage from stealth",
      "skill_type": "active",
      "category": "combat",
      "rarity": "rare",
      "level": 1,
      "max_level": 10,
      "experience": 0,
      "experience_to_next": 100,
      "power": 2.0,
      "mastery": 0,
      "cooldown_seconds": 12,
      "mana_cost": 20,
      "prerequisite_skill_ids": [],
      "minimum_level": 5,
      "icon_id": null,
      "tags": ["stealth"],
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "attributes": [
    {
      "id": 2,
      "character_id": 3,
      "name": "agility",
      "description": "Increases movement speed",
      "attribute_type": "physical",
      "scale_type": "linear",
      "base_value": 75,
      "current_value": 75,
      "maximum_value": 100,
      "flat_bonus": 0,
      "percentage_bonus": 0,
      "temporary_bonus": null,
      "is_derived": false,
      "derivation_formula": null,
      "source_attributes": [],
      "minimum_value": 0,
      "display_name": "Agility",
      "icon_id": null,
      "tags": ["movement"],
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "next_id": 3
}
```

## Key Considerations

- **Implicit progression**: Characters getting stronger may be implied, not explicitly stated
- **Skill trees**: Look for mentioned or implied specialization paths
- **Balance**: Progression should feel earned through training/experience, not arbitrary
- **Multiple characters**: Track progression for all characters in the scene, not just the protagonist
- **Training context**: Progression often follows training, practice, or revelation

## Example

**Input:**
> "Kira felt different. The training had paid off. She could now move faster, see further. The elder's teachings about shadow arts had unlocked something within her—she could strike from darkness like never before."

**Extract (short):**
```json
{
  "skills": [
    {
      "id": 10,
      "character_id": 3,
      "name": "Shadow Strike",
      "description": "Strike from darkness with enhanced power",
      "skill_type": "active",
      "category": "combat",
      "rarity": "rare",
      "level": 1,
      "max_level": 10,
      "experience": 0,
      "experience_to_next": 100,
      "power": 1.8,
      "mastery": 0,
      "cooldown_seconds": 12,
      "mana_cost": 20,
      "prerequisite_skill_ids": [],
      "minimum_level": 5,
      "icon_id": null,
      "tags": ["shadow"],
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ]
}
```
