---
name: naming
description: Big-endian file naming as semantic binding
license: MIT
tier: 1
allowed-tools: []
related: [room, character, yaml-jazz, k-lines]
tags: [moollm, naming, filesystem, semantic, convention]
---

# Naming Skill

> *"The filesystem is a semantic network."*

This skill wraps [kernel/NAMING.yml](../../kernel/NAMING.yml).

## Core Pattern

```
TYPE-VARIANT.ext
```

| Part | Meaning | Examples |
|------|---------|----------|
| TYPE | Category/role | `cat`, `staff`, `ROOM` |
| VARIANT | Specific instance | `terpie`, `marieke` |
| ext | File type | `.yml`, `.md` |

## Examples

```
pub/
├── ROOM.yml            # Type only — the pub itself
├── cat-terpie.yml      # Type-variant
├── cat-stroopwafel.yml
├── staff-marieke.yml
└── menu-strains.yml    # Menu type, strains variant
```

## Sorting Advantage

```bash
ls *.yml | sort
# cat-stroopwafel.yml
# cat-terpie.yml
# menu-strains.yml
# ROOM.yml
# staff-marieke.yml
```

Categories cluster. Finding "all cats" → `cat-*.yml`

## Special Filenames

| Name | Purpose |
|------|---------|
| `ROOM.yml` | Room definition |
| `CHARACTER.yml` | Character definition |
| `SKILL.md` | Skill specification |
| `README.md` | Human landing page |
| `INDEX.yml` | Registry |

## Canonical Forms

See [kernel/NAMING.yml](../../kernel/NAMING.yml) for:
- Full naming rules
- Big-endian rationale
- Minsky K-line connection

## Dovetails With

### Kernel
- [kernel/NAMING.yml](../../kernel/NAMING.yml) — definitive reference
