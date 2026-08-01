---
name: tool-catalog
description: Show all available Architecture Studio skills, agents, and their namespaced commands. Use when the user runs /as:tool-catalog, asks "what can you do" or "what skills are available", or wants a directory of plugin commands. Do not use for Claude Code's native /skills command.
allowed-tools:
  - Read
---

# /as:tool-catalog — What's Available

You display the full menu of available skills and agents, organized by what the user needs to accomplish. This is a read-only help command.

## On Start

Print the following menu. Do not read any files — the menu is static.

## Output

```
# Architecture Studio

**Architecture Studio tools and 7 agents** — type `/as:studio [your task]` to get routed, or call any plugin skill by its namespaced command.

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

### Due Diligence
/as:nyc-landmarks [address] — LPC landmark and historic district check
/as:nyc-dob-permits [address] — DOB permit and filing history
/as:nyc-dob-violations [address] — DOB and ECB violations
/as:nyc-acris [address] — property transaction records
/as:nyc-hpd [address] — HPD violations and complaints (residential)
/as:nyc-bsa [address] — BSA variances and special permits
/as:nyc-property-report [address] — combined NYC report (all 6 above)

### Site Planning
/as:environmental-analysis [address] — climate, flood, seismic, soil
/as:mobility-analysis [address] — transit, walk score, bike, pedestrian
/as:demographics-analysis [address] — population, income, housing, employment
/as:site-history [address] — neighborhood context, landmarks, commercial activity

### Zoning Analysis
/as:zoning-analysis-nyc [address] — NYC buildable envelope from PLUTO
/as:zoning-envelope — interactive 3D zoning envelope viewer

### Programming
/as:occupancy-calculator — IBC occupancy loads, egress, plumbing
/as:workplace-programmer — space programs from headcount and work style

### Specifications
/as:spec-writer — CSI outline specs from a materials list

### Sustainability
/as:epd-research [material] — search for EPDs by material or category
/as:epd-parser [file] — extract data from an EPD PDF
/as:epd-compare — side-by-side environmental impact comparison
/as:epd-to-spec — CSI specs with EPD requirements and GWP thresholds

### Materials Research
/as:product-research — find products from a design brief
/as:product-spec-bulk-fetch — extract specs from product URLs
/as:product-spec-pdf-parser — extract specs from PDF catalogs
/as:product-data-cleanup — normalize a messy FF&E schedule
/as:product-enrich — auto-tag products with categories, colors, materials
/as:product-match — find similar products
/as:product-pair — suggest complementary products
/as:product-image-processor — download, resize, remove backgrounds
/as:product-data-import — import raw product data into product-library.csv
/as:master-schedule — initialize or inspect the local product-library.csv
/as:csv-to-sif — convert CSV to dealer format
/as:sif-to-csv — convert dealer format to CSV

### Presentations
/as:slide-deck-generator [topic] — HTML slide deck with editorial layout
/as:color-palette-generator — color palettes from descriptions or images
/as:resize-images — batch-resize photos for web, social, slides, and print

### Dispatcher
/as:studio [task] — smart router: describe a task, get routed to the right agent or skill
/as:tool-catalog — this menu
/as:skill-maker — scaffold a new skill that follows the house conventions
/as:workplan — plan repository, operational, or AEC delivery work before acting
/as:studio-feedback — prepare a reviewed GitHub bug report or feature request

### Project Records
/as:project — initialize a project, remember sourced facts, and manage numbered decision records
/as:meeting-minutes — turn a transcript or notes into typed, source-linked minutes
/as:site-visit-report — turn field notes into an evidence-aware site report
/as:tasklist — manage the canonical TASKS.md action register
/as:timetracker — reconstruct daily or weekly work and record user-confirmed time

These records form a linked graph: facts and decisions inform plans; meetings and site reports propose facts, decisions, and tasks without silently promoting them; tasks preserve action history; and timetracker reconstructs work from dated artifacts but never infers duration.

### Learn — new to Claude Code?
/as:learn — guided hands-on course for architects, resumable anytime
```

That's it. Do not add commentary, suggestions, or follow-up questions. Just print the menu.
