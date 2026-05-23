---
name: grimoire-creator
description: "Create Grimoires (magical instructional texts) for Mage: The Ascension 20th Anniversary Edition (M20). Use when designing magical texts that teach Practices, Spheres, Abilities, and Rotes. Handles mechanical validation (rank, points, content counts) and thematic consistency. Requires mage-rules-reference skill for faction/practice/ability lookups. Triggers: create a grimoire, design a magical text, stat up a grimoire, M20 grimoire."
---

# Grimoire Creator

Create mechanically valid, thematically rich Grimoires for M20. Source: *Prism of Focus: Grimoires* by Charles Siegel.

## What is a Grimoire?

A Grimoire is a magical instructional text (book, scroll, flash drive, etc.) that teaches magical practices. Unlike Talismans that produce effects, Grimoires teach: Practices, Spheres, Abilities, Rotes, and potentially Awakening (as a Primer).

## Core Mechanics

### Rank and Points

| Rank | Description | Points | Max Teaching Level |
|------|-------------|--------|-------------------|
| 1 | Primer/Introduction | 3 | 1 |
| 2 | Journeyman Text | 6 | 2 |
| 3 | Advanced Manual | 9 | 3 |
| 4 | Master's Treatise | 12 | 4 |
| 5 | Legendary Tome | 15 | 5 |

**Points Available = 3 × Rank**

### Free Content (Every Grimoire)

- 1 Practice (up to Rank)
- 1 Ability (associated with that Practice)
- 1 Sphere (up to Rank)

### Point Costs

| Content | Cost |
|---------|------|
| Additional Practice | 2 pts |
| Additional Sphere | 2 pts |
| Additional Ability | 1 pt |
| Rote | Sum of Sphere dots |
| Primer (Arete training) | 3 pts |
| Merits | Variable |
| Flaws | Grant points (max 7) |

## Critical Validation Formula

**Content Count Rule:**
```
Rotes + Practices + Spheres + Abilities + (1 if Primer) = Rank + 3
```

Free content counts toward this total.

**Example (Rank 2):** Required = 2 + 3 = 5 pieces
- 1 Practice + 1 Sphere + 1 Ability + 2 Rotes = 5 ✓
- 2 Practices + 1 Sphere + 2 Abilities + 0 Rotes = 5 ✓

## Creation Process

1. **Concept**: Faction, purpose, narrative role
2. **Set Rank**: 1-2 beginner, 3 established, 4-5 masters
3. **Choose Faction**: Query practices via `mage-rules-reference` skill
4. **Select Free Content**: 1 Practice + 1 associated Ability + 1 Sphere
5. **Purchase Additional Content**: Stay within point budget
6. **Verify Content Count**: Must equal Rank + 3
7. **Add Merits/Flaws**: See [references/grimoire-merits-flaws.md](references/grimoire-merits-flaws.md)
8. **Describe Physical Form**: Medium, language, appearance
9. **Design Rotes**: If included, use rote-creator skill for full mechanical detail
10. **Validate**: Run all checks

## Reference Data

### Shared M20 Data (via mage-rules-reference skill)

Query faction/practice/ability associations:
```bash
# Get practices for a faction
python /path/to/mage-rules-reference/scripts/lookup.py \
  /path/to/mage-rules-reference/references/faction-practices.json "Order of Hermes"

# Get abilities for a practice  
python /path/to/mage-rules-reference/scripts/lookup.py \
  /path/to/mage-rules-reference/references/practice-abilities.json "High Ritual Magick"

# Get languages for a faction
python /path/to/mage-rules-reference/scripts/lookup.py \
  /path/to/mage-rules-reference/references/faction-languages.json "Order of Hermes"
```

### Grimoire-Specific References

- **[grimoire-merits-flaws.md](references/grimoire-merits-flaws.md)**: Merit and Flaw tables
- **[output-template.md](references/output-template.md)**: Standard output format

## Validation Checklist

Before finalizing, verify:

- [ ] Rank 1-5
- [ ] Points spent ≤ (3 × Rank) + Flaw points
- [ ] Content count = Rank + 3
- [ ] No trait taught above Rank (except Advanced Insights: one trait at Rank+1)
- [ ] All Abilities associated with a Practice in the Grimoire
- [ ] All Rotes use only contained Practices, Spheres, Abilities
- [ ] Flaw points ≤ 7
- [ ] Faction-Practice alignment is thematic

## Point Validation Block

Include in output:
```
Base Points:           [3 × Rank] = X
+ Flaw Points:                    + X
= Available:                      = X

Spent:
- Practices (N × 2):              - X
- Spheres (N × 2):                - X  
- Abilities (N × 1):              - X
- Rotes (total dots):             - X
- Primer:                         - X
- Merits:                         - X
= Remaining:                      = X (must be ≥ 0)

Content: Rotes(X) + Practices(X) + Spheres(X) + Abilities(X) + Primer(0/1) = X
Required: Rank + 3 = X
Status: [VALID/INVALID]
```

## Rote Integration

When a Grimoire contains rotes, use the **rote-creator** skill to design each with full mechanical detail. Rotes must use only Practices, Spheres, and Abilities contained in the Grimoire.

For multi-document projects, link rotes:
```markdown
| Rote | Spheres | Link |
|------|---------|------|
| Silver Conduit | Prime 3, Corr 2 | [rote file](../rotes/silver_conduit.md) |
```
