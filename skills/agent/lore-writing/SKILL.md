---
name: lore-writing
description: Extract lore and narrative device entities from text. Use when analyzing codex entries, bestiary entries, journals, dreams, nightmares, memories, secrets, foreshadowing, and plot devices.
---
# lore-writing

Domain skill for lore knowledge and narrative device extraction.

## Entity Types

| Type | Description |
|------|-------------|
| `lore_fragment` | Piece of world lore or historical knowledge |
| `codex_entry` | Codex or encyclopedia entry |
| `journal_page` | Journal, diary, or log entry |
| `bestiary_entry` | Creature or monster description |
| `memory` | Character memory or recollection |
| `dream` | Dream or prophetic vision |
| `nightmare` | Nightmare or dark vision |
| `foreshadowing` | Narrative foreshadowing element |
| `chekhovs_gun` | Setup element that must pay off later |
| `red_herring` | Misleading narrative element |
| `deus_ex_machina` | Unexpected resolution device |
| `flash_forward` | Future glimpse or time skip |
| `plot_device` | General narrative mechanism |
| `lore_axioms` | Fundamental world rules or laws |

## Extraction Rules

1. **Lore fragments**: Historical references, myths, legends, folklore mentioned in passing
2. **Bestiary**: Creature abilities, behaviors, habitats, weaknesses
3. **Dreams/visions**: Symbolism, prophetic content, emotional context
4. **Narrative devices**: Foreshadowing setups, Chekhov's guns, red herrings
5. **World rules**: Fundamental axioms that govern the world's logic

## Output Format

Write to `entities/narrative.json` (narrative-team file):

```json
{
  "lore_fragments": [
    {
      "id": 1,
      "world_id": 1,
      "title": "The Old War Legend",
      "content": "A legend about the ancient war between mages and warriors",
      "rarity": "common",
      "is_discoverable": true,
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "foreshadowings": [
    {
      "id": 2,
      "story_id": 10,
      "scene_id": 11,
      "foreshadowing_type": "symbolic",
      "subtlety": "moderate",
      "name": "The Cracked Amulet",
      "description": "The amulet shows a crack — hints at its eventual breaking",
      "hinted_event_id": null,
      "is_paid_off": false,
      "player_discovery_rate": 40.0,
      "character_ids": [3],
      "location_id": 5,
      "requires_knowledge": [1],
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "next_id": 3
}
```

## Key Considerations

- **Fragmentary nature**: Lore often comes in small, incomplete pieces
- **Unreliable narrators**: Stories within stories may be biased or inaccurate
- **Symbolic dreams**: Not all dream content is literal
- **Cross-references**: If needed, track relationships separately in drafts, but final JSON must match `LoreData.from_dict`.
