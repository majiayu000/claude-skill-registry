---
name: library-creator
description: "Create Libraries (collections of magical texts) for Mage: The Ascension 20th Anniversary Edition. Libraries contain Grimoires and serve as research resources. Requires grimoire-creator for individual text design and mage-rules-reference for faction lookups. Triggers: create a library, design a book collection, M20 library, chantry library."
---

# Library Creator

Design magical text collections for M20. Libraries contain Grimoires and are rated by the quality/depth of their collection.

## Library Statistics

### Rank (1-5)

| Rank | Description | Max Teaching Level |
|------|-------------|-------------------|
| 1 | Basic introductory texts | 1 |
| 2 | Solid collection | 2 |
| 3 | Excellent, rare texts | 3 |
| 4 | Outstanding, unique works | 4 |
| 5 | Legendary, priceless | 5 |

Rank determines what level of traits (Spheres, Practices, Abilities) can be learned from the collection.

### Faction Affiliation

Libraries typically align with a faction. Query available practices:
```bash
python lookup.py references/faction-practices.json "Order of Hermes"
```

### Collection Focus

Libraries often specialize in:
- **Spheres**: Deep knowledge in specific Spheres
- **Practices**: Texts on particular methods
- **Historical**: Ancient, medieval, modern
- **Regional**: Geographic traditions
- **Research**: Specific phenomena

## Contents

A Library contains **Grimoires**. Use **grimoire-creator** skill to design notable texts.

Typical contents by rank:

| Rank | Grimoires | Rotes | Coverage |
|------|-----------|-------|----------|
| 1 | 3-5 | 5-10 | 1-2 Spheres, 1-2 Practices |
| 2 | 5-10 | 10-20 | 2-3 Spheres, 2-3 Practices |
| 3 | 10-20 | 20-40 | 3-5 Spheres, 3-4 Practices |
| 4 | 20-50 | 40-80 | 5-7 Spheres, 4-6 Practices |
| 5 | 50+ | 80+ | Comprehensive |

## Creation Workflow

1. **Concept**: What faction? What focus? Where located?
2. **Rank**: Based on collection quality
3. **Faction**: Determines dominant practices/paradigm
4. **Focus**: Specializations (if any)
5. **Notable Texts**: Design 2-4 key Grimoires via grimoire-creator
6. **Physical Space**: Description, organization, access
7. **Curator**: Who manages it?

## Output Format

---

# [Library Name]

**Rank:** [1-5] | **Faction:** [Name] | **Focus:** [Specialty]

## Concept
*[1-2 paragraphs: History, atmosphere, what it feels like to study here]*

## Statistics

| Stat | Value |
|------|-------|
| Rank | [1-5] |
| Faction | [Name] |
| Focus | [Specialty] |
| Texts | [Approximate count] |
| Max Teaching | [= Rank] |

## Collection Overview

| Category | Coverage |
|----------|----------|
| Spheres | [List] |
| Practices | [List] |
| Abilities | [List] |
| Rotes | [Approximate count] |

## Notable Grimoires

| Title | Rank | Contents |
|-------|------|----------|
| [Name] | [X] | [Brief: Practices, Spheres, key rotes] |

*Use grimoire-creator for full statistics on key texts.*

## Physical Description
*[Location, appearance, organization]*

## Access
*[Who can use it? Permissions? Security?]*

## Curator
*[Who manages it? Specialties?]*

## Story Hooks
- [Hook 1]
- [Hook 2]

---

## Validation

- [ ] Rank 1-5
- [ ] Faction alignment fits contents
- [ ] Notable texts don't exceed Library rank
- [ ] Focus areas are coherent
- [ ] Access requirements make sense
