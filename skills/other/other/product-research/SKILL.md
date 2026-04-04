---
name: product-research
description: FF&E product research — receives a brief from the designer, searches the web for matching products, and returns structured candidates to save to the master Google Sheet.
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

# /product-research — Product Research

Receives a brief from a designer, researches products across the web, and returns a curated shortlist of candidates. Selected products are saved to the master Google Sheet — the same one used by Norma Jean and the other data-management skills.

## How It Works

```
Designer gives a brief
        ↓
Claude searches the web
        ↓
Presents candidates with specs + reasoning
        ↓
Designer picks winners
        ↓
Saved to master Google Sheet
```

## Step 1: Take the Brief

The designer describes what they're looking for. A brief can be loose or specific:

**Loose:**
> "I need acoustic panels for a tech office lobby"

**Specific:**
> "Looking for a round dining table, 48-54" diameter, solid wood top (walnut or oak preferred), steel or brass base, under $3,000, needs to be in stock or <6 week lead time"

### What to capture from the brief

Extract as many of these as the designer provides. **Don't ask for fields they didn't mention** — work with what you have.

| Field | Examples |
|-------|---------|
| **Category** | Table, seating, lighting, acoustic panel, planter, storage |
| **Use context** | Office lobby, conference room, outdoor terrace, home office |
| **Style / aesthetic** | Scandinavian, mid-century, industrial, minimal, warm, bold |
| **Materials** | Solid wood, marble, steel, fabric, mesh, recycled |
| **Dimensions** | "48-54 inch diameter", "under 30 inches tall", "fits a 6x4 space" |
| **Budget** | Under $3,000, $500-$1,000 range, high-end, budget-friendly |
| **Sustainability** | GREENGUARD, FSC, Cradle to Cradle, recycled content, B Corp |
| **Lead time** | In stock, under 6 weeks, no rush |
| **Quantity** | 1 hero piece, 12 for a conference room, 50+ for open office |
| **Indoor/Outdoor** | Indoor, outdoor, both |
| **Must-haves** | Stackable, COM available, ADA compliant, weatherproof |
| **Brands to consider** | "I like Muuto and HAY", "no Herman Miller" |
| **Brands to avoid** | "Not Ikea", "nothing from Amazon" |

**Don't interview the designer.** If the brief is "acoustic panels for a lobby," that's enough to start searching. You can clarify *after* showing initial results if needed ("I found options in fabric, felt, and wood slat — any preference?").

## Step 2: Research

Search the web for products matching the brief. Use multiple targeted queries to cover different angles:

### Search strategy

For a brief like "round dining table, walnut, under $3,000":

1. **Category + material search**: `round walnut dining table`
2. **Design-focused search**: `best round wood dining tables architects designers`
3. **Trade/contract search**: `contract round dining table solid wood specifications` (for commercial projects)
4. **Specific brand searches** if the designer mentioned preferences: `Muuto round table`, `HAY dining table`
5. **Sustainability search** if relevant: `FSC certified round dining table`

Run **3-5 searches** depending on brief complexity. Aim for breadth — different price points, brands, styles.

### For each candidate found

Attempt to fetch the product page with WebFetch to extract full specs. If the page is JS-rendered and returns no data:
- Use whatever info is available from the search result snippet
- Fill in from general knowledge if the product is well-known
- Note specs as "unverified" if sourced from search snippets rather than product pages

**Target: 6-10 candidates** that genuinely match the brief. Don't pad the list with weak matches.

## Step 3: Present Candidates

Show results as a numbered shortlist with enough detail to evaluate:

```
## Product Research: Round Dining Tables (walnut, under $3,000)

### 1. Alle Table Round — Hem
Designer: Staffan Holm · 59" dia × 29"H
Materials: Solid oak top, powder-coated steel base
Price: $2,399 USD · Lead: 8-12 weeks
Finishes: Natural oak, smoked oak, walnut stain
Indoor · COM: N/A
🔗 hem.com/en-us/furniture/tables/alle/30421
Why: Clean Scandinavian lines, strong scale for a lobby, within budget.
Walnut stain option available. Hem has good contract pricing.

### 2. Snaregade Round — Menu
Designer: Norm Architects · 54" dia × 28.5"H
Materials: Oak veneer top, powder-coated steel base
Price: $2,195 USD · Lead: 6-8 weeks
Finishes: Dark stained oak, light oak
Indoor · COM: N/A
🔗 menuspace.com/snaregade-round
Why: Norm Architects pedigree, slightly under budget,
faster lead time. Veneer top (not solid) — flag if that matters.

### 3. ...

---

## Summary

| # | Product | Brand | Ø | Price | Lead | Material | Notes |
|---|---------|-------|---|-------|------|----------|-------|
| 1 | Alle Round | Hem | 59" | $2,399 | 8-12w | Solid oak | Walnut stain ✓ |
| 2 | Snaregade Round | Menu | 54" | $2,195 | 6-8w | Oak veneer | Not solid wood |
| 3 | ... | ... | ... | ... | ... | ... | ... |

Which ones should I save to your product library?
```

### Presentation rules

- **Lead with the summary table** if there are 6+ candidates — designers scan visually
- **Include "Why"** for each — explain why this product matches the brief, and flag any compromises
- **Flag trade-offs honestly** — "veneer not solid", "over budget but worth seeing", "long lead time"
- **Don't oversell** — if a product is a weak match, say so or don't include it
- **Group by angle** if useful — "Budget options", "Premium picks", "Fastest delivery"

## Step 4: Save to Sheet

When the designer picks candidates ("save 1, 3, and 5"), write them to the master Google Sheet.

### Connecting to the sheet

If not already connected, ask for the Google Sheet ID or URL. Same sheet used by Norma Jean and other skills.

### Row format

Write rows to the master product sheet using the 33-column schema. Read `../../schema/product-schema.md` (relative to this SKILL.md) for the full column reference, field formats, and category vocabulary. Read `../../schema/sheet-conventions.md` for CRUD patterns with MCP tools.

Skill-specific column values:
- **AG (Source):** `research`
- **AF (Status):** `saved`
- **AD (Tags):** From brief context (e.g. "lobby-reno, walnut")
- **AE (Notes):** The "Why" reasoning from the presentation
- **S (Selected Color/Finish):** Blank (designer hasn't configured yet)

### After saving

```
✓ Saved 3 products to your library (rows 48-50).
  Tagged: lobby-reno, walnut

Want me to refine the search? Different style, budget, or materials?
```

## Step 5 (Optional): Iterate

The designer may want to refine:

- **"More like #1 but cheaper"** → Search for alternatives in that style/brand tier
- **"What about outdoor versions?"** → New search with added constraint
- **"Can you find the spec sheet PDF for #3?"** → Search for manufacturer cut sheet
- **"Compare #1 and #3 side by side"** → Detailed comparison
- **"Any of these have GREENGUARD?"** → Check certifications for the shortlist

Each iteration can add more products to the sheet.

## Conversation Style

- **Don't over-ask before searching.** A one-line brief is enough to start.
- **Show results, then refine.** It's faster to react to real options than to specify everything upfront.
- **Be opinionated.** The designer wants a knowledgeable research assistant, not a search engine. Flag the best options, note trade-offs, suggest alternatives.
- **Know the industry.** Reference relevant brands, designers, trade platforms. Understand contract vs. residential, COM/COL, lead times, certifications.

## Notes

- **JS-rendered product pages** are common (Hem, Muuto, Vitra, etc.). If WebFetch returns no data, use search result snippets + general knowledge. Note when specs are unverified.
- **Norma Jean is the sidecar.** If the designer says "actually I'll just browse and clip" — that's Norma Jean's job (Alt+C in Chrome). This skill is for when they want Claude to do the research.
- **The sheet is shared.** Products from this skill live alongside Norma Jean clips, bulk-fetch imports, and PDF extractions. The `Source` column ("research") identifies where each row came from.
