---
name: quest-design
description: Extract quest entities from narrative text. Use when analyzing quest chains, objectives, moral choices, prerequisites, rewards, quest givers, and branching quest structures.
---
# quest-design

Domain skill for quest structure extraction.

## Entity Types

| Type | Description |
|------|-------------|
| `quest` | Main quest container |
| `quest_chain` | Sequence of linked quests |
| `quest_node` | Individual step within a quest chain |
| `quest_giver` | NPC who assigns the quest |
| `quest_objective` | Specific goal within a quest |
| `quest_prerequisite` | Requirement to start a quest |
| `quest_reward_tier` | Reward tier or level for completion |
| `quest_tracker` | Progress tracking state |
| `moral_choice` | Player moral decision point |

## Domain Constraints

- `quest.status`: active, completed, failed, cancelled
- `objective.type`: kill, collect, interact, deliver, escort, defend, explore, talk, craft, use
- `objective.status`: not_started, in_progress, completed, failed
- `prerequisite.type`: level, quest, item, skill, location, reputation, custom

## Output Format

Write to `entities/narrative.json` (narrative-team file):

```json
{
  "quests": [
    {
      "id": 1,
      "world_id": 1,
      "name": "Find Lost Brother",
      "description": "Kira must find her missing brother near the Ancient Ruins",
      "objectives": ["Speak to village elder"],
      "status": "active",
      "participant_ids": [3],
      "reward_ids": [],
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "quest_objectives": [
    {
      "id": 2,
      "world_id": 1,
      "quest_node_id": 1,
      "objective_type": "talk",
      "description": "Ask Elder Theron about the brother's last known location",
      "target_type": null,
      "target_id": null,
      "target_quantity": 1,
      "current_progress": 0,
      "status": "not_started",
      "is_optional": false,
      "is_hidden": false,
      "order_index": 0,
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "next_id": 3
}
```

## Key Considerations

- **Implicit quests**: Some objectives are implied, not explicitly stated
- **Moral ambiguity**: Not all choices are clearly good/bad
- **Cross-references**: If needed, track relationships separately in drafts, but final JSON must match `LoreData.from_dict`.
