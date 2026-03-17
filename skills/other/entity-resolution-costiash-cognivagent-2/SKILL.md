---
name: entity-resolution
description: Identifies and merges duplicate entities in Knowledge Graph projects.
  Use after extraction to consolidate duplicate entities, or when users ask about
  potential duplicates. Supports automatic merging for high-confidence matches and
  user confirmation for medium-confidence candidates.
---

# Entity Resolution Skill

Identifies and merges duplicate entities in Knowledge Graph projects.

## When to Use

- **Proactively after extraction**: "I extracted 15 entities. Let me check for potential duplicates..."
- **On user request**: "Can you check for duplicates?" or "These seem like the same person"
- **When graph seems noisy**: Multiple similar-looking nodes that may be the same entity

## Workflow

### 1. Scan for Duplicates

```
Use find_duplicate_entities with project_id
```

The tool uses multiple signals to detect duplicates:
- **String similarity** (Jaro-Winkler on labels)
- **Alias overlap** (Jaccard similarity)
- **Type matching** (same entity type bonus)
- **Graph context** (shared neighbors)

### 2. Apply Confidence-Based Automation

| Confidence | Action |
|------------|--------|
| **>= 0.9 (HIGH)** | Auto-merge with `merge_entities_tool`. Inform user: "I merged X and Y (95% confident they're the same)" |
| **0.7-0.9 (MEDIUM)** | Ask user: "I found potential duplicates: X and Y (82% match). Should I merge them?" |
| **< 0.7 (LOW)** | Mention if relevant: "X and Y might be related but confidence is low (65%)" |

### 3. Handle User Decisions

- If user approves: `approve_merge` or `merge_entities_tool`
- If user rejects: `reject_merge`
- If user wants more info: `compare_entities_semantic` for detailed analysis

## Proactive Triggers

After any `extract_to_kg` operation, automatically:

1. Call `find_duplicate_entities`
2. Process HIGH confidence matches silently (auto-merge)
3. Report MEDIUM confidence matches to user
4. Mention LOW confidence only if user asks

## Example Responses

### After extraction:

> "I extracted 12 entities and 8 relationships. I noticed 'Elon Musk' and 'Musk' appear to be the same person (94% confidence), so I merged them. I also found 'SpaceX' and 'Space X' might be duplicates (78% confidence) - should I merge these too?"

### On duplicate scan:

> "I scanned for duplicates and found 3 potential matches:
> 1. 'OpenAI' and 'Open AI' (91% - auto-merged)
> 2. 'Sam Altman' and 'Samuel Altman' (85% - awaiting your approval)
> 3. 'Microsoft' and 'MS' (68% - low confidence, skipped)"

### When comparing entities:

> "Comparing 'Dr. John Smith' and 'J. Smith':
>
> | Signal | Score |
> |--------|-------|
> | Name similarity | 72% |
> | Same type (Person) | Yes |
> | Shared connections | 3 |
>
> Overall: 78% match. They share connections to MIT and OpenAI. Would you like to merge them?"

## Available Tools

| Tool | Description |
|------|-------------|
| `find_duplicate_entities` | Scan for duplicates in a project |
| `merge_entities_tool` | Execute a merge directly (for high confidence) |
| `review_pending_merges` | See pending candidates awaiting approval |
| `approve_merge` | Approve a pending candidate |
| `reject_merge` | Reject a pending candidate |
| `compare_entities_semantic` | Deep comparison of two specific entities |

## Tool Parameters

### find_duplicate_entities

```json
{
  "project_id": "abc123",
  "min_confidence": 0.7
}
```

### merge_entities_tool

```json
{
  "project_id": "abc123",
  "survivor_id": "node_to_keep",
  "merged_id": "node_to_remove"
}
```

### compare_entities_semantic

```json
{
  "project_id": "abc123",
  "node_a_id": "first_entity_id",
  "node_b_id": "second_entity_id"
}
```

## Merge Behavior

When entities are merged:

1. **Survivor keeps** its primary label
2. **Merged entity's label** becomes an alias of survivor
3. **All aliases** transfer to survivor
4. **All relationships** redirect to survivor
5. **Properties merge** (survivor wins on conflict)
6. **Source IDs combine** for provenance tracking

## Error Handling

| Issue | Response |
|-------|----------|
| No project selected | "Please select a Knowledge Graph project first" |
| Empty graph | "Your graph doesn't have any entities yet. Extract content first" |
| No duplicates found | "No potential duplicates found above the confidence threshold" |
| Entity not found | "Entity 'X' was not found. It may have been merged or deleted" |

## Follow-Up Suggestions Format

After presenting duplicate scan results, offer interactive follow-ups:

```markdown
### Explore Further

- "Merge Sam Altman and Samuel Altman" - Merge these entities
- "Compare Sam Altman and Samuel Altman" - See detailed similarity analysis
- "Reject the Sam Altman merge" - Keep them as separate entities
- "Show me all pending merges" - Review all candidates
```

## Integration with KG Insights

After merging entities, the graph may reveal new insights:

- "After merging, [Entity] is now connected to 5 more entities"
- "The merge resolved an isolated topic - [Entity] now links to the main graph"
- "Consider running `ask_about_graph` with `question_type: key_entities` to see updated rankings"

## Best Practices

1. **Be transparent** - Always explain what was merged and why
2. **Preserve information** - Merged labels become aliases, nothing is lost
3. **Ask when uncertain** - Only auto-merge above 90% confidence
4. **Show evidence** - Include signal breakdown for user decisions
5. **Suggest next steps** - Offer to scan again or explore the updated graph
