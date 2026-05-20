---
name: historical-research
description: Extract historical entities from narrative text. Use when analyzing eras, timelines, calendars, holidays, seasons, alliances, empires, kingdoms, and era transitions.
---
# historical-research

Domain skill for historical and chronological extraction.

## Entity Types

| Type | Description |
|------|-------------|
| `era` | Historical era, age, or epoch |
| `era_transition` | Transition between eras |
| `timeline` | Chronological sequence of events |
| `calendar` | Calendar or timekeeping system |
| `holiday` | Holiday or special date |
| `season` | Named season or time of year |
| `alliance` | Historical or political alliance |
| `empire` | Empire or major state entity |
| `kingdom` | Kingdom or sovereign territory |
| `nation` | Nation or country |

## Extraction Rules

1. **Eras**: Named periods (Age of Magic, Dark Times) — extract with timeframe
2. **Transitions**: What caused era changes (wars, discoveries, cataclysms)
3. **Timelines**: Chronological sequence of mentioned events
4. **Calendars**: Timekeeping systems, named months, cycles
5. **States**: Empires, kingdoms, nations — with their boundaries and rulers

## Output Format

Write to `entities/society.json` (society-team file):

```json
{
  "eras": [
    {
      "id": 1,
      "world_id": 1,
      "name": "Age of Magic",
      "description": "Ancient era when sorcerers ruled the skies",
      "start_date": "1026-01-01T00:00:00+00:00",
      "end_date": "1526-01-01T00:00:00+00:00",
      "parent_era_id": null,
      "child_era_ids": [],
      "major_events": ["Great War"],
      "cultural_notes": "Magic was central to society",
      "technological_level": "Arcane",
      "is_ongoing": false,
      "color_code": "#5b3bff",
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "era_transitions": [
    {
      "id": 2,
      "world_id": 1,
      "name": "The Great War Transition",
      "description": "Magic waned after the Great War, ending the Age of Magic",
      "from_era_id": 1,
      "to_era_id": 3,
      "transition_date": "1526-01-01T00:00:00+00:00",
      "transition_type": "catastrophic",
      "trigger_events": ["Great War"],
      "key_figures": [5],
      "social_impact": "Collapse of mage houses",
      "economic_impact": null,
      "political_impact": null,
      "magical_impact": "Mana scarcity",
      "stories_and_legends": ["The Last Spell"],
      "artifacts": [],
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "next_id": 3
}
```

## Key Considerations

- **Relative time**: Not all systems use absolute dates (cycles, ages)
- **Multiple perspectives**: History may differ by culture (victors write history)
- **Cross-references**: If needed, track relationships separately in drafts, but final JSON must match `LoreData.from_dict`.
