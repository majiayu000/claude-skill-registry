---
name: item-provenance
description: Adds origin/provenance + rumor hooks to Emberwild item entries and updates
  indexes.
---

name: item-provenance
description: Adds origin/provenance + rumor hooks to Emberwild item entries and updates indexes.
metadata:
  short-description: Add item backstories + links
---

## Goal
Take a batch of items and add micro-lore depth WITHOUT changing tone or breaking formatting.

## Inputs I will be given
- A source file (usually 08_Items/Items_Master_List - GLOBAL A-Z.md or a region pack)
- A batch size + range (e.g., items 001–050)

## Steps
1) Preserve existing numbering + fields.
2) Add these fields per item:
   - Origin:
   - First Known Maker:
   - Rumor:
   - See also: (3 markdown links to existing relevant files/sections)
3) If needed, create 1–3 tiny supporting lore stubs (short files) ONLY when no good link targets exist.
4) Update 00_MASTER_INDEX/Items_Index.md if new files were created or new packs added.

## Output
- A concise summary + list of touched files.
- A “review checklist” (formatting, links, tone).
