---
name: sanctum-creator
description: "Create Sanctums (personal magical workspaces) for Mage: The Ascension 20th Anniversary Edition. Sanctums exist in the material world with magical protections and optional Reality Zones that modify Practice difficulties. Requires mage-rules-reference for Practice and Reality Zone lookups. Triggers: create a sanctum, design a workspace, mage's laboratory, magical workshop."
---

# Sanctum Creator

Design personal magical workspaces for M20. Sanctums exist in the material world but may have magical protections and reality-shaping effects.

## Sanctum vs Other Locations

| Location | Exists In | Key Feature |
|----------|-----------|-------------|
| **Sanctum** | Material world | Personal workspace, Reality Zone |
| **Chantry** | Material world | Group headquarters, shared resources |
| **Node** | Material world | Quintessence source |
| **Demesne** | Pocket realm | Separate reality entirely |

## Sanctum Statistics

### Rank (0-5)

| Rank | Description | Features |
|------|-------------|----------|
| 0 | Minimal | Basic workspace, no special features |
| 1 | Minor | Small protected space, basic wards |
| 2 | Modest | Well-equipped, simple ritual space |
| 3 | Significant | Reality Zone, specialized equipment |
| 4 | Major | Strong protections, Umbral anchoring |
| 5 | Grand | Powerful reality effects, Node connection |

### Reality Zone (Rank 3+)

Higher-ranked Sanctums can have a Reality Zone that modifies Practice difficulties. Query rules:
```bash
python lookup.py references/reality-zones.json --all
```

**Rules:**
- Each +1 rating → -1 difficulty for that Practice
- Each -1 rating → +1 difficulty for that Practice
- Positive total = Sanctum Rank
- Max ±3 per Practice typical

**Example (Rank 3 Hermetic Sanctum):**

| Practice | Rating | Effect |
|----------|--------|--------|
| High Ritual Magick | +2 | -2 difficulty |
| Alchemy | +1 | -1 difficulty |
| Gutter Magick | -2 | +2 difficulty |
| Chaos Magick | -1 | +1 difficulty |

Positive total: 3 = Rank ✓

## Features by Rank

### Rank 1-2
- Basic wards against intrusion
- Personal library/workspace
- Simple ritual space
- Mundane security

### Rank 3-4
- Reality Zone effects
- Sophisticated magical security
- Specialized equipment for paradigm
- Umbral anchoring possible
- Guardian spirits/constructs

### Rank 5
- Powerful reality manipulation
- Multiple specialized chambers
- Near-impenetrable defenses
- Connection to Nodes or Demesnes
- Legendary reputation

## Creation Workflow

1. **Concept**: Whose workspace? What paradigm?
2. **Rank**: Based on investment/power
3. **Location**: Where in the material world?
4. **Reality Zone** (rank 3+): Which Practices favored/hindered?
5. **Features**: Equipment, protections, special properties
6. **Mundane Cover**: How does it appear to Sleepers?

## Output Format

---

# [Sanctum Name]

**Rank:** [0-5] | **Owner:** [Name] | **Tradition:** [Faction]

## Concept
*[1-2 paragraphs: What it is, who created it, atmosphere]*

## Statistics

| Stat | Value |
|------|-------|
| Rank | [0-5] |
| Owner | [Name] |
| Tradition | [Faction] |
| Location | [Physical location] |

### Reality Zone (if Rank 3+)

| Practice | Rating | Effect |
|----------|--------|--------|
| [Practice] | +X | -X diff |
| [Practice] | -X | +X diff |
| **Positive Total** | [= Rank] | |

## Physical Layout
*[Rooms, arrangement, size]*

## Features

| Feature | Description |
|---------|-------------|
| Wards | [Protections] |
| Equipment | [Specialized tools] |
| Ritual Space | [Working area] |
| Special | [Unique properties] |

## Security
*[Mundane and magical protections]*

## Mundane Cover
*[Sleeper appearance, cover story]*

## Story Hooks
- [Hook 1]
- [Hook 2]

---

## Validation

- [ ] Rank 0-5
- [ ] Reality Zone positive total = Rank (if present)
- [ ] Features appropriate to rank
- [ ] Reflects owner's paradigm
- [ ] Mundane cover is plausible
