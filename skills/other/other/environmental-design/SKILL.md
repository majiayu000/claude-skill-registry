---
name: environmental-design
description: Extract environmental entities from narrative text. Use when analyzing weather, atmosphere, lighting, time periods, natural disasters, cataclysms, plagues, and world events.
---
# environmental-design

Domain skill for environmental conditions and events extraction.

## Entity Types

| Type | Description |
|------|-------------|
| `environment` | General environmental setting or biome |
| `weather_pattern` | Weather system or meteorological condition |
| `atmosphere` | Atmospheric condition (fog, pressure, air quality) |
| `lighting` | Lighting condition (natural or magical) |
| `time_period` | Time of day or seasonal context |
| `disaster` | Natural disaster (storm, flood, earthquake) |
| `cataclysm` | Major catastrophic event |
| `world_event` | Significant world-scale event |
| `seasonal_event` | Recurring seasonal occurrence |
| `plague` | Disease outbreak or epidemic |

## Domain Constraints

- `time_of_day`: day, night, dawn, dusk
- `weather`: clear, rainy, stormy, foggy
- `lighting`: bright, dim, dark, magical

## Extraction Rules

1. **Weather**: Rain, snow, storms, clear sky — note intensity and duration
2. **Time**: Dawn, noon, dusk, midnight — track progression through text
3. **Atmosphere**: Fog, oppressive heat, crisp air — sensory details
4. **Disasters**: Storms, floods, earthquakes — scale, impact, duration
5. **World events**: Wars, plagues, seasonal celebrations — scope and significance

## Output Format

Write to `entities/world.json` (world-team file):

```json
{
  "environments": [
    {
      "id": 1,
      "world_id": 1,
      "location_id": 10,
      "name": "Stormy Night",
      "description": "Dark clouds gathering from the north, storm imminent",
      "time_of_day": "night",
      "weather": "stormy",
      "lighting": "dim",
      "temperature": "chilly",
      "sounds": "distant thunder",
      "smells": "wet earth",
      "is_active": true,
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "weather_patterns": [
    {
      "id": 2,
      "tenant_id": 1,
      "name": "Approaching Storm",
      "pattern_type": "storm",
      "severity": 0.9,
      "duration_minutes": 180,
      "affected_regions": [10],
      "conditions": { "wind": "strong", "precipitation": "heavy" },
      "is_active": true,
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00"
    }
  ],
  "next_id": 3
}
```

## Key Considerations

- **Mood impact**: Environment affects narrative tone (storms = tension, dawn = hope)
- **Narrative function**: Weather often mirrors story events (pathetic fallacy)
- **Temporal flow**: Track time progression and environmental changes through text
- **Cross-references**: If needed, track relationships separately in drafts, but final JSON must match `LoreData.from_dict`.
