---
name: skills-menu
description: Show all available skills, agents, and how to use them — organized by task.
allowed-tools:
  - Read
user-invocable: true
---

# /skills — What's Available

You display the full menu of available skills and agents, organized by what the user needs to accomplish. This is a read-only help command.

## On Start

Print the following menu. Do not read any files — the menu is static.

## Output

```
# Architecture Studio

**36 skills, 7 agents** (includes master-schedule) — type /studio [your task] to get routed, or call any skill directly.

## Agents — describe your task, they figure out the rest

| Agent | What it does |
|-------|-------------|
| Site Planner | Full site brief — climate, transit, demographics, neighborhood context |
| NYC Zoning Expert | NYC property + zoning — due diligence, FAR, buildable envelope, 3D viewer |
| Workplace Strategist | Space programs — headcount to occupancy compliance to room schedules |
| Product & Materials Researcher | Find products from a brief, extract specs from URLs/PDFs, find alternatives |
| FF&E Designer | Build schedules from messy inputs, compose room packages, QA, export |
| Sustainability Specialist | EPD research, GWP comparison, LEED eligibility, spec thresholds |
| Brand Manager | Presentations, color palettes, visual consistency, deliverable QA |

## Skills — call directly for a specific task

### Site & Due Diligence
/environmental-analysis [address] — climate, flood, seismic, soil
/mobility-analysis [address] — transit, walk score, bike, pedestrian
/demographics-analysis [address] — population, income, housing, employment
/history [address] — neighborhood context, landmarks, commercial activity
/nyc-landmarks [address] — LPC landmark and historic district check
/nyc-dob-permits [address] — DOB permit and filing history
/nyc-dob-violations [address] — DOB and ECB violations
/nyc-acris [address] — property transaction records
/nyc-hpd [address] — HPD violations and complaints (residential)
/nyc-bsa [address] — BSA variances and special permits
/nyc-property-report [address] — combined NYC report (all 6 above)

### Zoning
/zoning-analysis-nyc [address] — NYC buildable envelope from PLUTO
/zoning-analysis-uruguay — Maldonado, Uruguay lot analysis
/zoning-envelope — interactive 3D zoning envelope viewer

### Programming
/occupancy-calculator — IBC occupancy loads, egress, plumbing
/workplace-programmer — space programs from headcount and work style

### Specifications
/spec-writer — CSI outline specs from a materials list

### Sustainability
/epd-research [material] — search for EPDs by material or category
/epd-parser [file] — extract data from an EPD PDF
/epd-compare — side-by-side environmental impact comparison
/epd-to-spec — CSI specs with EPD requirements and GWP thresholds

### Product & Materials Research
/product-research — find products from a design brief
/product-spec-bulk-fetch — extract specs from product URLs
/product-spec-pdf-parser — extract specs from PDF catalogs
/product-data-cleanup — normalize a messy FF&E schedule
/product-enrich — auto-tag products with categories, colors, materials
/product-match — find similar products
/product-pair — suggest complementary products
/product-image-processor — download, resize, remove backgrounds
/product-data-import — import raw product data into the master schedule
/master-schedule — connect a product library sheet to the project
/csv-to-sif — convert CSV to dealer format
/sif-to-csv — convert dealer format to CSV

### Presentations
/slide-deck-generator [topic] — HTML slide deck with editorial layout
/color-palette-generator — color palettes from descriptions or images
/resize-images — batch-resize photos for web, social, slides, and print
```

That's it. Do not add commentary, suggestions, or follow-up questions. Just print the menu.
