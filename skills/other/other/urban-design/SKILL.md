---
name: urban-design
description: Extract urban planning entities from narrative text. Use when analyzing city districts, wards, quarters, plazas, markets, slums, noble districts, and port areas.
---
# urban-design

Domain skill for urban planning and city structure extraction.

## Entity Types

| Type | Description |
|------|-------------|
| `district` | Named city district or neighborhood |
| `ward` | Administrative ward or section |
| `quarter` | City quarter (e.g., merchant quarter) |
| `plaza` | Public plaza or gathering space |
| `market_square` | Market area or trade hub |
| `slums` | Impoverished area |
| `noble_district` | Wealthy or aristocratic area |
| `port_district` | Waterfront or harbor area |

## Extraction Rules

1. **Named districts**: Extract with exact name and characteristics
2. **Social geography**: Map wealth distribution across the city
3. **Infrastructure**: Roads, walls, gates, utilities mentioned
4. **Activity zones**: Commercial, residential, religious, industrial areas
5. **Historical layers**: Old vs new city sections

## Output Format

Write to `entities/world.json` (world-team file):

```json
{
  "districts": [
    {
      "id": "4dbf72a5-1a2b-4b3c-9d4e-5f6a7b8c9d0e",
      "tenant_id": "t-1",
      "name": "Merchant Quarter",
      "city_id": "l-1",
      "district_type": "commercial",
      "population": 12000,
      "safety_level": 0.6,
      "prosperity_level": 0.8,
      "is_active": true,
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00"
    }
  ],
  "slums": [
    {
      "id": "c2d8b8a1-9e7b-4c6d-8a1b-2c3d4e5f6a7b",
      "tenant_id": "t-1",
      "name": "The Warrens",
      "city_id": "l-1",
      "district_type": "slums",
      "population": 25000,
      "safety_level": 0.2,
      "prosperity_level": 0.1,
      "is_active": true,
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00"
    }
  ]
}
```

## Key Considerations

- **Social inequality**: Slums vs noble districts show wealth gap
- **Mixed use**: Many areas are residential + commercial
- **Historical layers**: Cities have old and new sections
- **Cross-references**: If needed, track relationships separately in drafts, but final JSON must match `LoreData.from_dict`.
