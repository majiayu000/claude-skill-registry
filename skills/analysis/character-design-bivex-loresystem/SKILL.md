---
name: character-design
description: Extract character entities from narrative text. Use when analyzing characters, relationships, psychology, development arcs, voice/mocap data, and character variants.
---
# character-design

Domain skill for character extraction.

## Entity Types

| Type | Description |
|------|-------------|
| `character` | Main character entity with name, role, personality, motivation |
| `character_evolution` | Character development arc or growth moment |
| `character_profile_entry` | Backstory detail or profile information |
| `character_relationship` | Relationship between two characters |
| `character_variant` | Alternate version, iteration, or form |
| `voice_actor` | Voice acting information |
| `motion_capture` | Motion capture performance data |

## Extraction Rules

1. **Identify characters**: Named characters with dialogue/actions, referred-to characters, groups
2. **Extract details**: Name, role, status, personality traits, motivations, goals
3. **Track development**: Growth moments, realizations, motivation changes
4. **Map relationships**: Type (friend, rival, family, romantic), strength, dynamics
5. **Note variants**: Alternate forms, timelines, disguises

## Domain Constraints

- `backstory`: minimum 100 characters
- `ability.power_level`: integer 1–10
- `combat_stats`: attack, defense, health, speed ≥ 0
- `status`: "active" or "inactive"

## Output Format

Write to `entities/narrative.json` (narrative-team file):

```json
{
  "characters": [
    {
      "id": 1,
      "world_id": 1,
      "name": "Kira",
      "backstory": "... minimum 100 characters ...",
      "status": "active",
      "abilities": [
        { "name": "Flame Mastery", "description": "...", "power_level": 8 }
      ],
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "character_relationships": [
    {
      "id": 2,
      "character_from_id": 1,
      "character_to_id": 3,
      "relationship_type": "friend",
      "description": "Strong friendship forged through shared battles",
      "relationship_level": 60,
      "is_mutual": true,
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "next_id": 3
}
```

## Key Considerations

- **Uniqueness**: Each character has a unique ID; name variations reference the same ID
- **Implicit relationships**: Track both explicit and implied connections
- **Cross-references**: If needed, track relationships separately in drafts, but final JSON must be compatible with `LoreData.from_dict`.
