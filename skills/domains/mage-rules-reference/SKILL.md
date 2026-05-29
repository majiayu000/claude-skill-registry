---
name: mage-rules-reference
description: "Shared M20 rules data for Mage: The Ascension 20th Anniversary Edition. Contains Practice-Ability associations, Faction-Practice associations, and Faction-Language associations. Use this skill when building other M20 content (grimoires, rotes, characters, chantries) that requires faction/practice/ability lookups. Query via scripts/lookup.py rather than loading full reference files."
---

# M20 Rules Reference

Shared reference data for Mage: The Ascension 20th Anniversary Edition.

## Available Data

| File | Contents |
|------|----------|
| `references/practice-abilities.json` | Practice → Associated Abilities |
| `references/practices.json` | Practice → Description |
| `references/faction-practices.json` | Faction → Available Practices |
| `references/faction-languages.json` | Faction → Common Languages |
| `references/faction-chantry-names.json` | Faction → Chantry name (Covenant, Chapel, etc.) |
| `references/faction-titles.json` | Faction → Title systems by Arete/role |
| `references/sphere-levels.json` | Sphere → Level descriptions (1-5) |
| `references/common-effects.json` | Effect name → Required Spheres |
| `references/resonance-traits.json` | Sphere → Common Resonance traits |
| `references/reality-zones.json` | Reality Zone rules and examples |

## Lookup Script

Use `scripts/lookup.py` to query data without loading full files into context.

### Usage

```bash
# Get abilities for a practice
python scripts/lookup.py references/practice-abilities.json "High Ritual Magick"

# Get practices for multiple factions
python scripts/lookup.py references/faction-practices.json "Order of Hermes" "Verbena"

# List all keys in a file
python scripts/lookup.py references/faction-practices.json --keys

# Find all entries containing a term (searches keys and values)
python scripts/lookup.py references/practice-abilities.json --find Herbalism

# What Spheres do I need for telepathy?
python scripts/lookup.py references/common-effects.json "Telepathy"

# What can Mind 3 do?
python scripts/lookup.py references/sphere-levels.json "Mind"

# What effects involve Spirit?
python scripts/lookup.py references/common-effects.json --find Spirit

# Dump entire file
python scripts/lookup.py references/faction-languages.json --all
```

### From Other Skills

Reference this skill's data:
```bash
python /path/to/mage-rules-reference/scripts/lookup.py \
  /path/to/mage-rules-reference/references/practice-abilities.json \
  "Witchcraft"
```

## Data Structure

### practice-abilities.json / practices.json
```json
{ "Practice Name": ["Ability1", ...] }
{ "Practice Name": "Description" }
```

### faction-practices.json
```json
{
  "_meta": { "traditions": [...], "conventions": [...], "crafts": [...] },
  "Faction Name": ["Practice1", ...]
}
```
Note: Orphans have `["_any"]` indicating any Practice is valid.

### sphere-levels.json
```json
{
  "_meta": { "pattern_spheres": [...], "connecting_spheres": [...], ... },
  "Sphere Name": { "1": "desc", "2": "desc", ... }
}
```

### common-effects.json
```json
{
  "Effect Name": { "spheres": "Mind 3", "category": "Perception & Psychic", "notes": "optional" }
}
```
Categories: Body Magick, Crafting Wonders, Fate & Fortune, Spirit Powers, Objects & Elements, Perception & Psychic, Time & Distance, Quintessence

### resonance-traits.json
```json
{
  "_meta": { "description": "..." },
  "Sphere Name": ["Trait1", "Trait2", ...]
}
```
Query: `lookup.py references/resonance-traits.json "Forces"` → Fiery, Bright, Energetic, etc.

### reality-zones.json
```json
{
  "_meta": { "description": "...", "balance_rule": "...", "valid_practices": "..." },
  "effects": { "positive": "...", "negative": "...", "max_rating": "...", "stacking": "..." },
  "excluded_practices": {
    "specialized": ["Practice1", ...],
    "corrupted": ["Practice1", ...]
  },
  "examples": { "Zone Name": { "Practice": "+/-N", "notes": "..." } }
}
```
**Key rule**: Only base Practices (in `practices.json`) may be used in Reality Zones. Query excluded:
```bash
python scripts/lookup.py references/reality-zones.json "excluded_practices"
```

### faction-chantry-names.json
```json
{
  "_meta": { "description": "..." },
  "Faction Name": "Chantry Term"
}
```
Query: `lookup.py references/faction-chantry-names.json "Order of Hermes"` → "Covenant"

### faction-titles.json
```json
{
  "_meta": { "description": "..." },
  "Faction Name": {
    "by_arete": { "1": "Title", "2": "Title", ... },
    "by_role": { "leader": [...], "senior": [...], "member": [...], "apprentice": [...] },
    "houses": [...],
    "sub_factions": [...]
  }
}
```
Query: `lookup.py references/faction-titles.json "Order of Hermes"` → Full title structure
