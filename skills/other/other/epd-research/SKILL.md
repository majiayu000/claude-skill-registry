---
name: epd-research
description: Search for EPDs by product category, CSI division, or material type. Finds EPDs from EC3, program operator registries, and manufacturer sites.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - AskUserQuestion
  - mcp__google__sheets_values_get
  - mcp__google__sheets_values_update
  - mcp__google__sheets_spreadsheet_get
---

# /epd-research — EPD Research

Receives a brief describing a material or product category, searches the web for matching EPDs (Environmental Product Declarations), and returns a curated shortlist sorted by environmental impact. Selected EPDs are saved to the EPD Google Sheet — the same one used by `/epd-parser` and the other EPD skills.

## How It Works

```
User describes what they need EPDs for
        |
Claude searches registries + manufacturer sites
        |
Presents candidates sorted by GWP (lowest first)
        |
User picks winners
        |
Saved to EPD Google Sheet (42-column schema)
```

## Step 1: Take the Brief

The user describes what they need EPDs for. A brief can be loose or specific:

**Loose:**
> "I need concrete EPDs"

**Specific:**
> "Looking for ready-mix concrete EPDs, 4000-5000 PSI, plants within 500 miles of NYC, GWP under 350 kg CO2e/m3"

### What to capture from the brief

Extract as many of these as the user provides. **Don't ask for fields they didn't mention** — work with what you have.

| Field | Examples |
|-------|---------|
| **Material/product** | Ready-mix concrete, structural steel, mineral wool insulation, carpet tile |
| **CSI division** | Division 03, Division 09, "all structural materials" |
| **Performance specs** | 4000 PSI, R-21, Class A fire rating |
| **Geographic preference** | Plants near NYC, manufactured in North America, European suppliers ok |
| **GWP target** | Under 350 kg CO2e/m3, below industry average, lowest available |
| **Manufacturers** | "Include Holcim and CEMEX", "no imported steel" |
| **EPD type** | Product-specific only, industry-average ok |
| **Standard** | EN 15804+A2, ISO 21930 |
| **Certification** | LEED v4.1 eligible, third-party verified |

**Don't interview the user.** If the brief is "concrete EPDs," that's enough to start searching. Clarify *after* showing initial results if needed.

## Step 2: Research

Search the web for EPDs matching the brief. Use multiple targeted queries to cover different sources.

### Key registries and sources

| Source | URL pattern | Notes |
|--------|------------|-------|
| **Building Transparency / EC3** | buildingtransparency.org | Largest EPD database. Requires authenticated API access (free professional account + API key). See notes below. |
| **UL EPD Program** | ul.com | Major US program operator. Product-specific EPDs. |
| **NSF International** | nsf.org | US program operator, strong in concrete/masonry. |
| **SCS Global Services** | scsglobalservices.com | US program operator. |
| **Environdec (International EPD System)** | environdec.com | Largest international registry. European + global. |
| **IBU (Institut Bauen und Umwelt)** | ibu-epd.com | German program operator. Strong in European products. |
| **ASTM International** | astm.org | US program operator (newer). |
| **Manufacturer sites** | varies | Major manufacturers publish EPDs on their sustainability pages. |

### Search strategy

For a brief like "ready-mix concrete EPDs, 4000 PSI, near NYC":

1. **Program operator search**: `site:ul.com ready-mix concrete environmental product declaration`
2. **International registry search**: `site:environdec.com ready-mix concrete EPD`
3. **Manufacturer + region search**: `ready-mix concrete EPD northeast US 4000 PSI`
4. **Specific manufacturer searches** if mentioned: `Holcim ready-mix EPD`, `CEMEX concrete EPD`
5. **Industry body search**: `NRMCA concrete EPD` (National Ready Mixed Concrete Association)

Run **3-5 searches** depending on brief complexity. Aim for breadth — different manufacturers, regions, GWP ranges.

### For each EPD found

Attempt to fetch the registry page or EPD listing with WebFetch. Extract:

- Product name and manufacturer
- GWP (A1-A3) per declared unit — the primary comparison metric
- Declared unit
- Program operator and registration number
- System boundary
- Validity dates
- Link to EPD PDF
- Plant/facility and location (if listed)

If the page is JS-rendered and returns limited data, use whatever info is available from the search result snippet plus general knowledge. Note as "unverified" if sourced from snippets.

**Target: 6-12 EPD candidates** that genuinely match the brief. Don't pad with weak matches.

## Step 3: Present Candidates

Show results as a numbered shortlist sorted by GWP (lowest first):

```
## EPD Research: Ready-Mix Concrete (4000 PSI, Northeast US)

### 1. ECOPact — Holcim
Plant: South Plainfield, NJ · GWP: 242 kg CO2e/m3
Declared Unit: 1 m3 · System Boundary: Cradle-to-gate
Program Operator: NSF · Reg: EPD-00123 · Valid: 2024-06-01 to 2029-06-01
LEED: Yes (product-specific, third-party verified)
PDF: [link]
Why: Lowest GWP in the region. ECOPact line is Holcim's low-carbon
concrete — uses SCM substitution. Plant is ~50 miles from NYC.

### 2. ProPaving 4000 — CEMEX
Plant: Yonkers, NY · GWP: 298 kg CO2e/m3
Declared Unit: 1 m3 · System Boundary: Cradle-to-gate
Program Operator: ASTM · Reg: EPD-00456 · Valid: 2023-11-01 to 2028-11-01
LEED: Yes
PDF: [link]
Why: Close to site. Higher GWP than ECOPact but still below NRMCA
industry average (~400 kg CO2e/m3 for 4000 PSI).

### 3. ...

---

## Summary

| # | Product | Manufacturer | Plant | GWP (A1-A3) | Unit | Valid To | LEED |
|---|---------|-------------|-------|-------------|------|----------|------|
| 1 | ECOPact | Holcim | South Plainfield, NJ | 242 | kg CO2e/m3 | 2029-06 | Yes |
| 2 | ProPaving 4000 | CEMEX | Yonkers, NY | 298 | kg CO2e/m3 | 2028-11 | Yes |
| 3 | ... | ... | ... | ... | ... | ... | ... |

Industry average (NRMCA, 4000 PSI): ~400 kg CO2e/m3

Which ones should I save to your EPD library?
```

### Presentation rules

- **Sort by GWP (lowest first)** — environmental performance is the primary ranking criterion
- **Include industry average** for the material category if known (NRMCA for concrete, AISC for steel, etc.)
- **Include "Why"** for each — explain why this EPD is relevant to the brief, flag any trade-offs
- **Flag expired EPDs** — include them if relevant but clearly mark as expired
- **Note system boundary differences** — if some are cradle-to-gate and others cradle-to-grave, call it out
- **Distinguish EPD types** — product-specific vs. industry-average matters for LEED

## Step 4: Save to Sheet

When the user picks EPDs ("save 1, 3, and 5"), write them to the EPD Google Sheet using the 42-column schema.

### Connecting to the sheet

If not already connected, ask for the Google Sheet ID or URL. This is a **separate spreadsheet** from the FF&E product library — EPD data has a different schema.

### Row format

Write to the 42-column EPD schema. Set:
- `Parsed At` — current ISO timestamp
- `Source` — `epd-research`
- `Notes` — the "Why" reasoning from the presentation + any caveats
- `Tags` — from brief context (e.g., "4000-psi, northeast, project-name")
- `LEED Eligible` — based on EPD type and verification status

### After saving

```
Saved 3 EPDs to your library (rows 12-14).
Tagged: 4000-psi, northeast

Want me to compare these? Or search for more options?
```

## Step 5 (Optional): Iterate

The user may want to refine:

- **"Any with lower GWP?"** — search for supplementary cementitious material (SCM) blends, newer EPDs
- **"What about precast?"** — expand to related product categories
- **"Compare #1 and #2"** — hand off to `/epd-compare`
- **"Write spec language for #1's GWP as the max threshold"** — hand off to `/epd-to-spec`
- **"Find the PDF for #3 so I can parse the full data"** — search for downloadable EPD document

## Conversation Style

- **Don't over-ask before searching.** A material name is enough to start.
- **Show results, then refine.** It's faster to react to real options than to specify everything upfront.
- **Be opinionated.** Flag the lowest-GWP options, note which are below industry average, recommend what to specify.
- **Know the industry.** Understand that GWP varies by region (local plants use local materials), that SCM content drives concrete GWP, that steel GWP depends on EAF vs. BOF, that insulation GWP depends on blowing agent.

## Notes

- **EC3 (Building Transparency) requires an API key.** EC3 is the largest EPD database, but all data is behind authenticated API access — `site:buildingtransparency.org` web searches will not return results. If the user hasn't configured EC3 API credentials, tell them: *"EC3 has the largest EPD database but requires a free API key from buildingtransparency.org (professional account with a business email). I'll search program operator registries and manufacturer sites directly instead."* Then proceed with the other sources listed above — UL, NSF, Environdec, IBU, SCS, ASTM, and manufacturer sustainability pages all publish EPDs publicly.
- **EPD validity matters.** A 2019 EPD based on EN 15804+A1 is less useful than a 2024 EPD based on +A2. Prefer newer EPDs when available.
- **Regional EPDs are more useful than national averages.** A plant-specific EPD from a nearby facility is more valuable for a project than a company-wide average.
- **This skill finds EPDs. `/epd-parser` extracts full data from the PDFs.** If the user wants deep data from a found EPD, download the PDF and run `/epd-parser`.
