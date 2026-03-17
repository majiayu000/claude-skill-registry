---
name: entity-validator
description: Validation rules for extracted entities. Checks required fields, data types, cross-references, duplicates, enum values, and domain constraints.
user-invocable: false
---
# entity-validator

Base skill for validating extracted lore entities against the domain model.

## Validation Checks

1. **Export format**: Verify that the top level contains only collections from the schema `lore_data.py` and `next_id`
2. **Data types**: Verify string, number, boolean, array, object types match schema
3. **Required fields**: Every entity must have all required fields corresponding to the domain model
4. **Cross-references**: All referenced entity IDs must exist and refer to numeric `id`
5. **No duplicates**: Same entity type + name combination must not appear twice

## Domain Constraints

From `src/domain/`:

| Constraint | Rule |
|------------|------|
| Character backstory | min 100 characters |
| Ability power_level | integer 1–10 |
| Item level | integer 1–100 |
| Reputation value | integer -1000 to 1000 |
| Combat stats | ≥ 0 (attack, defense, health, speed) |
| Timestamps | updated_at ≥ created_at |
| Version | ≥ 1 |

## Error Handling

- **WARN** on missing optional fields
- **ERROR** on missing required fields or invalid types
- **ERROR** on duplicate entity (same type + name)
- **WARN** on unresolved cross-references (may be resolved during merge)
