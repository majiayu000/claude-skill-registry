---
name: religious-lore
description: Extract religious entities from narrative text. Use when analyzing cults, sects, holy sites, scriptures, rituals, oaths, summons, pacts, curses, blessings, and miracles.
---
# religious-lore

Domain skill for religious and supernatural extraction.

## Entity Types

| Type | Description |
|------|-------------|
| `cult` | Cult or secretive religious group |
| `sect` | Religious sect or denomination |
| `holy_site` | Sacred place or shrine |
| `scripture` | Religious text or holy book |
| `ritual` | Ritual, prayer, or religious ceremony |
| `oath` | Sacred oath or vow |
| `summon` | Summoning ritual or invocation |
| `pact` | Supernatural pact or agreement |
| `curse` | Curse or negative supernatural effect |
| `blessing` | Blessing or positive supernatural effect |
| `miracle` | Miraculous event or divine intervention |

## Extraction Rules

1. **Religious groups**: Cults, sects, churches — name, beliefs, structure
2. **Sacred places**: Temples, shrines, holy mountains — location, significance
3. **Rituals**: Procedure, required components, effects, practitioners
4. **Supernatural effects**: Curses, blessings, miracles — trigger, effect, duration
5. **Pacts**: Parties involved, terms, consequences of breaking

## Output Format

Write to `entities/society.json` (society-team file):

```json
{
  "cults": [
    {
      "id": "b2d3a0f1-3a1c-4d3e-9a4b-2c3d4e5f6a7b",
      "tenant_id": "t-1",
      "name": "Order of the Void",
      "deity_id": "d-1",
      "leader_id": "c-1",
      "secret_knowledge": ["Star-binding rites"],
      "rituals": ["Night of Silence"],
      "membership_count": 120,
      "secrecy_level": 85,
      "alignment": "evil",
      "headquarters_location_id": "l-1",
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00"
    }
  ],
  "curses": [
    {
      "id": "c7b6a5d4-3e2f-4a1b-9c8d-7e6f5a4b3c2d",
      "tenant_id": "t-1",
      "character_id": "c-2",
      "curse_name": "Curse of the Blood Moon",
      "source_id": "d-1",
      "severity": 80,
      "effects": ["transformation"],
      "symptoms": ["nightmares", "fever"],
      "duration": "until_cured",
      "removal_conditions": ["Moonlit ritual"],
      "spread_type": "none",
      "cure_methods": ["Holy water"],
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00"
    }
  ]
}
```

## Key Considerations

- **Multiple faiths**: Worlds often have competing religions
- **Lost religions**: Ancient faiths may have faded — extract remnants
- **Heretical practices**: Cults vs mainstream religion
- **Cross-references**: If needed, track relationships separately in drafts, but final JSON must match `LoreData.from_dict`.
