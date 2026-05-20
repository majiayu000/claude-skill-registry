---
name: faction-design
description: Extract faction entities from narrative text. Use when analyzing organizations, hierarchies, ideologies, territories, resources, leaders, banners, and inter-faction relationships.
---
# faction-design

Domain skill for faction and organization extraction.

## Entity Types

| Type | Description |
|------|-------------|
| `faction` | Organization, guild, cult, or group |
| `faction_hierarchy` | Internal power structure |
| `faction_ideology` | Beliefs, goals, worldview |
| `faction_leader` | Leadership position or person |
| `faction_membership` | Member roster or membership info |
| `faction_resource` | Controlled resources and assets |
| `faction_territory` | Controlled or influenced territory |
| `banner` | Faction banner, emblem, or symbol |

## Domain Constraints

- `faction.type`: political, religious, military, criminal, magical, merchant, secret, monster
- `faction.alignment`: good, neutral, evil, chaotic
- `faction_membership.reputation`: integer -1000 to 1000

## Extraction Rules

1. **Named groups**: Guilds, armies, cults, orders — extract with exact name
2. **Implied groups**: Bandits, rebels, authorities — create descriptive name
3. **Hierarchy**: Who leads, how power is organized, ranks
4. **Relationships**: Allies, enemies, neutral parties between factions
5. **Resources**: Wealth, military power, information, magic, territory

## Output Format

Write to `entities/society.json`:

```json
{
  "factions": [
    {
      "id": 1,
      "world_id": 1,
      "name": "Shadow Brotherhood",
      "description": "Secret criminal organization operating in the underworld",
      "type": "criminal",
      "alignment": "evil",
      "leader_character_id": null,
      "member_character_ids": [],
      "allied_faction_ids": [],
      "enemy_faction_ids": [],
      "headquarters_location_id": null,
      "controlled_location_ids": [],
      "reputation_hostile_threshold": -500,
      "reputation_neutral_threshold": 0,
      "reputation_friendly_threshold": 500,
      "reputation_exalted_threshold": 1000,
      "vendor_discount_at_friendly": 10.0,
      "vendor_discount_at_exalted": 25.0,
      "exclusive_items_unlocked_at": 750,
      "faction_icon_path": null,
      "faction_color": null,
      "is_hidden": false,
      "is_joinable": true,
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "next_id": 2
}
```

## Key Considerations

- **Overlapping membership**: Characters may belong to multiple factions
- **Hidden factions**: Some operate in secret — extract even unnamed ones
- **Dynamic relationships**: Alliances shift; note current state from text
- **Cross-references**: If needed, track relationships separately in drafts, but final JSON must match `LoreData.from_dict`.
