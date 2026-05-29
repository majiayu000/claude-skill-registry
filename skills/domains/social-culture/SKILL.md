---
name: social-culture
description: Extract social and cultural entities from narrative text. Use when analyzing social classes, honor, karma, reputation, festivals, ceremonies, tournaments, competitions, and social mobility.
---
# social-culture

Domain skill for social systems and cultural event extraction.

## Entity Types

| Type | Description |
|------|-------------|
| `social_class` | Social class or caste |
| `social_mobility` | Social advancement or demotion mechanism |
| `affinity` | Affinity or positive disposition |
| `disposition` | General attitude or stance |
| `honor` | Honor system or code |
| `karma` | Karma or moral balance system |
| `reputation` | Reputation level or standing |
| `festival` | Festival or recurring cultural event |
| `celebration` | One-time celebration or joyous event |
| `ceremony` | Formal ceremony or ritual observance |
| `concert` | Musical performance event |
| `competition` | Contest or competitive event |
| `tournament` | Organized tournament or championship |

## Extraction Rules

1. **Social structure**: Class hierarchy, barriers, privileges
2. **Moral systems**: Honor codes, karma rules, reputation effects
3. **Cultural events**: Festivals, ceremonies — meaning, frequency, significance
4. **Social mobility**: Can people change class? How?
5. **Reputation**: How it's gained/lost, what it affects

## Output Format

Write to `entities/society.json` (society-team file):

```json
{
  "social_classes": [
    {
      "id": "2d9a3c9e-78a9-4b5d-9c5e-0f6d5b3b9f2a",
      "tenant_id": "t-1",
      "character_id": "c-1",
      "class_name": "noble",
      "tier": 7,
      "title": "Lord",
      "benefits": ["land ownership", "council vote"],
      "restrictions": ["must serve in court"],
      "hereditary": true,
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00"
    }
  ],
  "festivals": [
    {
      "id": "7c9a3b21-3b54-4c9a-9c2a-6f18d0f1b6c2",
      "tenant_id": "t-1",
      "name": "Festival of Lights",
      "festival_type": "memorial",
      "location_id": "l-1",
      "start_date": "2026-12-20T00:00:00+00:00",
      "end_date": "2026-12-27T00:00:00+00:00",
      "organizer_id": "c-1",
      "participants": ["c-2", "c-3"],
      "rewards": { "honor": 10 },
      "traditions": ["lantern release", "oath of remembrance"],
      "is_annual": true,
      "is_active": true,
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00"
    }
  ]
}
```

## Key Considerations

- **Social stratification**: Clear hierarchies with barriers between classes
- **Reputation effects**: Honor/karma/reputation affect NPC interactions
- **Cultural values**: Festivals reflect what society values most
- **Cross-references**: If needed, track relationships separately in drafts, but final JSON must match `LoreData.from_dict`.
