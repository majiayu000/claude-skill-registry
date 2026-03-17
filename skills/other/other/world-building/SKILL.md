---
name: world-building
description: Extract location and geography entities from narrative text. Use when analyzing world geography, dungeons, zones, dimensions, arenas, hubs, open world areas, and spatial connections.
---
# world-building

Domain skill for location and geography extraction.

## Entity Types

| Type | Description |
|------|-------------|
| `location` | General location (city, village, landmark) |
| `hub_area` | Central hub, town, or safe zone |
| `instance` | Instanced area (separate from open world) |
| `dungeon` | Dungeon or dangerous enclosed area |
| `raid` | Raid encounter area |
| `arena` | Combat arena or PvP zone |
| `open_world_zone` | Open world explorable area |
| `underground` | Underground or subterranean area |
| `skybox` | Sky or space area |
| `dimension` | Alternate dimension or plane |
| `pocket_dimension` | Small pocket dimension or demiplane |

## Domain Constraints

- `location_type`: building, house, barn, temple, castle, dungeon, cave, forest, mountain, city, village, shop, tavern, ruins, landmark, other
- `name`: max 255 characters

## Extraction Rules

1. **Named places**: Cities, ruins, forests, mountains — extract with exact name
2. **Described areas**: "the dark cave", "the forest to the east" — create descriptive name
3. **Classify type**: Hub (safe), dungeon (dangerous), open world (explorable), exotic (dimensions)
4. **Map connections**: How locations connect — paths, portals, boundaries, adjacency
5. **Note atmosphere**: Dangerous, peaceful, mysterious, abandoned

## Output Format

Write to `entities/world.json`:

```json
{
  "locations": [
    {
      "id": 1,
      "world_id": 1,
      "name": "Eldoria Village",
      "description": "Peaceful village in the Eldorian Valley",
      "location_type": "village",
      "parent_location_id": null,
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "next_id": 2
}
```

## Key Considerations

- **Nested locations**: A town inside a forest inside a kingdom — track hierarchy
- **Connections**: How locations connect (paths, portals, boundaries)
- **Scale**: Relative sizes help establish world geography
- **Cross-references**: If needed, track relationships separately in drafts, but final JSON must match `LoreData.from_dict`.
