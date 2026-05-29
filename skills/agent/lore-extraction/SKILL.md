---
name: lore-extraction
description: Base extraction rules for all lore subagents. Governs entity identification, contextual analysis, relationship mapping, and JSON output formatting.
user-invocable: false
---
# lore-extraction

Base skill for all loreSystem extraction subagents. Common rules for extracting entities from narrative text.

## Extraction Pipeline

1. **Read** the source text completely before extracting
2. **Identify** entities — look for named things, described systems, relationships
3. **Classify** each entity to its correct type from the entity ownership map
4. **Format** according to the export schema
5. **Output** as JSON compatible with `LoreData.to_dict` (see `src/presentation/gui/lore_data.py`)
6. **Validate** against domain model constraints
7. **Review** for completeness and accuracy

## Entity Identification Rules

- Named entities (proper nouns, titles) → extract with exact name
- Described systems (magic system, economy) → extract with descriptive name
- Implied entities (unnamed but significant) → extract with contextual name
- Groups/collections → extract as single entity with members in description

## Cross-Domain References

When text mentions an entity owned by another skill:
- Do NOT create the entity — it belongs to the other skill
- Record the reference in a separate draft note for the lead to merge
- Include enough context (name, location, relation) for reconciliation

## Quality Rules

- Extract only what the text explicitly states or strongly implies
- Do not invent details not supported by the text
- If unsure, add a short comment in your draft note (not in the JSON export)
- Prefer fewer high-quality entities over many low-quality ones
