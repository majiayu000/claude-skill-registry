---
name: ui-ux-pro-max
description: Generate a UI/UX design system using local datasets and scripts. Use
  when you need structured visual guidance, color palettes, typography pairings, and
  UX rules for a product or page.
license: MIT
---

# UI/UX Pro Max

Use this skill to generate a design system and UI/UX recommendations with the local dataset.

## Quick Start

```bash
python3 scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"
```

## Optional Commands

```bash

# Persist design system
python3 scripts/search.py "<query>" --design-system --persist -p "Project Name"

# Domain search
python3 scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]

# Stack guidance
python3 scripts/search.py "<keyword>" --stack html-tailwind
```

## Notes
- Data lives in `data/`
- Scripts live in `scripts/`
