---
name: topical-map
description: Generate and manage Topical Maps for SEO authority building. Use when user wants to research keywords, build content clusters, or import GSC data for topical authority.
---

# Topical Map Generator

Build comprehensive Topical Maps for SEO authority using DataForSEO and GSC data.

## Commands

| Command | Description |
|---------|-------------|
| `/topical-map:discover` | Generate cluster suggestions from seed keyword |
| `/topical-map:research` | Deep research for all keywords and questions per cluster |
| `/topical-map:import-gsc` | Import and assign GSC queries to clusters |

## Data Location

All data is stored in `data/topical-authority/`:
- `topical-map.json` - Central database
- `gsc-queries.json` - GSC import tracking
- `clusters/` - Markdown summaries per cluster
- `exports/` - GSC CSV uploads

## Quick Start

1. **Discover clusters:** `/topical-map:discover "Zeiterfassung"`
2. **Research keywords:** `/topical-map:research`
3. **Import GSC data:** Place CSV in `exports/`, run `/topical-map:import-gsc`

## Cluster Status Workflow

```
draft -> researched -> planned -> published -> optimized
```

## DataForSEO Configuration

All API calls use:
- `location_name`: "Germany"
- `language_code`: "de"