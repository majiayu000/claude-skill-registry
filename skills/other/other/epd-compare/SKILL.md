---
name: epd-compare
description: Compare 2+ products side-by-side on environmental impact metrics. Normalizes declared units, checks system boundary alignment, and flags LEED MRc2 compliance.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__google-sheets__get_sheet_data
  - mcp__google-sheets__list_sheets
---

# /epd-compare — EPD Comparator

Compare 2 or more products side-by-side on environmental impact metrics. Validates comparability (declared units, system boundaries, PCR alignment), generates comparison tables with percentage deltas, and checks LEED v4.1 MRc2 eligibility.

This skill **reads** from the EPD Google Sheet but does **not write** to it. Output is a markdown comparison report.

## Input

The user provides EPD data in one of these ways:

1. **Sheet row references** — "compare rows 5, 8, and 12" from the EPD Google Sheet
2. **Inline data** — pasted product names with GWP values
3. **File path** — a CSV or markdown file with EPD data
4. **From prior skills** — "compare the EPDs I just parsed/found" (uses data from the current conversation)
5. **Mixed** — "compare this PDF I just parsed against what's in the sheet"

If the user doesn't specify a source, ask: **"Where is the EPD data? Sheet rows, pasted values, or from earlier in this conversation?"**

## Workflow

### Step 1: Collect data

Gather EPD data from the specified source. For each product, you need at minimum:

- Product name and manufacturer
- GWP (A1-A3) value
- Declared unit

Additional fields improve the comparison: ODP, AP, EP, POCP, energy use, water use, system boundary, PCR, validity dates, LEED eligibility.

### Step 2: Validate comparability

Before comparing, run these checks and report findings:

**Declared unit alignment:**
- Are all products using the same declared unit (e.g., all per m3, all per kg)?
- If units differ, attempt normalization where possible:
  - kg ↔ ton (multiply/divide by 1000)
  - m2 at different thicknesses (if thickness is known, normalize to same thickness)
- If normalization is impossible, warn: "Product A reports per m2, Product B reports per kg. Direct comparison requires density or thickness data. Provide conversion factors, or I'll compare only within matching units."
- **Never silently compare products with different declared units.**

**System boundary alignment:**
- Flag if some are cradle-to-gate (A1-A3) and others cradle-to-grave (A1-A3 + C1-C4 + D).
- Note: "A1-A3 comparison is still valid across both types. Full life cycle comparison is only valid for cradle-to-grave EPDs."

**PCR alignment:**
- Flag if products use different PCRs. Products under the same PCR are most directly comparable.
- Note the PCR names if they differ.

**EN 15804 version:**
- Flag if some use +A1 and others +A2. Impact indicator units may differ (AP in kg SO2e vs. mol H+ eq).
- GWP in kg CO2e is comparable across versions.

**Validity:**
- Flag any expired EPDs with their expiration date.

**EPD type:**
- Flag mix of product-specific and industry-average EPDs. Note that industry-average EPDs are less precise.

Report all findings before proceeding:

```
## Comparability Check

✓ Declared unit: All products use 1 m3
✓ System boundary: All cradle-to-gate (A1-A3)
⚠ PCR: Products 1-2 use NRMCA PCR, Product 3 uses NSF PCR — results are comparable but not identical methodology
⚠ Validity: Product 2 expired 2025-12-01
✓ EPD type: All product-specific
```

### Step 3: Generate comparison

Produce three outputs:

#### a. Side-by-side impact table

```
## Environmental Impact Comparison

| Metric | ECOPact (Holcim) | ProPaving (CEMEX) | ReadyMix (Buzzi) | Unit |
|--------|-----------------|-------------------|------------------|------|
| **GWP-total (A1-A3)** | **242** | 298 | 385 | kg CO2e/m3 |
| GWP-fossil (A1-A3) | 238 | 291 | — | kg CO2e/m3 |
| GWP-biogenic (A1-A3) | 4 | 7 | — | kg CO2e/m3 |
| ODP (A1-A3) | 1.2e-6 | 1.5e-6 | 1.8e-6 | kg CFC-11e/m3 |
| AP (A1-A3) | 0.45 | 0.52 | 0.61 | kg SO2e/m3 |
| EP (A1-A3) | 0.08 | 0.11 | 0.14 | kg PO4e/m3 |
| PERE (A1-A3) | 180 | 95 | 72 | MJ/m3 |
| PENRE (A1-A3) | 1,450 | 1,890 | 2,340 | MJ/m3 |
| FW (A1-A3) | 0.32 | 0.41 | 0.55 | m3/m3 |
| Recycled Content | 35% | 22% | 12% | % |
```

Bold the **best value** in each row (lowest for impacts, highest for recycled content/renewable energy).

Use `—` for missing data. Never fill in missing values.

#### b. Percentage comparison (relative to lowest)

```
## GWP Comparison (relative to lowest)

| Product | GWP (A1-A3) | vs. Lowest | vs. Industry Avg |
|---------|-------------|------------|-------------------|
| ECOPact (Holcim) | 242 kg CO2e/m3 | — baseline — | -40% |
| ProPaving (CEMEX) | 298 kg CO2e/m3 | +23% | -26% |
| ReadyMix (Buzzi) | 385 kg CO2e/m3 | +59% | -4% |
| *Industry average* | *~400 kg CO2e/m3* | — | — |
```

Include an industry average baseline **only if the user provides one** (e.g., from an industry-average EPD or a published baseline document). Do not use approximate or hardcoded baselines.

If the user hasn't provided a baseline, ask: **"Do you have an industry-average EPD or published baseline for this material category? If so, share it and I'll include it in the comparison. We're working on EC3 API integration that will automate baseline lookups — for now, provide an EPD or use `/epd-research` to find one."**

If no baseline is available, omit the "vs. Industry Avg" column entirely rather than guessing.

#### c. LEED v4.1 MRc2 assessment

Include this section if the user mentions LEED, or if LEED eligibility data is available:

```
## LEED v4.1 MRc2 Assessment

### Option 1 — EPD Disclosure (1 point for 20+ products with EPDs)
| Product | Qualifying EPD? | Type | Notes |
|---------|----------------|------|-------|
| ECOPact | ✓ | Product-specific | Third-party verified, ISO 14025 conforming |
| ProPaving | ✓ | Product-specific | Third-party verified |
| ReadyMix | ✗ | Industry-average | Does not qualify — industry-average EPDs earn half credit |

### Option 2 — Embodied Carbon Optimization (up to 2 points)
Products must demonstrate GWP below category baseline:
| Product | GWP | Baseline | Delta | Qualifies? |
|---------|-----|----------|-------|------------|
| ECOPact | 242 | 400 | -40% | ✓ Yes — significant reduction |
| ProPaving | 298 | 400 | -26% | ✓ Yes |
| ReadyMix | 385 | 400 | -4% | Marginal — minimal reduction |
```

### Step 4: Recommendation summary

End with a brief recommendation:

```
## Recommendation

**ECOPact by Holcim** is the clear winner on environmental performance — 40% below
industry average GWP and lowest across all impact categories. The South Plainfield
plant is closest to the project site.

**ProPaving by CEMEX** is a strong second option if Holcim can't meet schedule or
volume requirements — still 26% below average.

Both qualify for LEED MRc2 Option 1 and Option 2 credits.
```

Be direct and opinionated. The user wants a recommendation, not just data.

### Step 5: Save output

Save the comparison report as markdown:

- **Default path**: `./epd-comparison-YYYY-MM-DD.md`
- If the user says it's final: `./deliverables/`
- If no client context: `./deliverables/`
- Ask the user if they want a different path

After saving:

```
Comparison saved to [path].

Next steps:
- /epd-to-spec — generate spec language using ECOPact's GWP (242) as the threshold
- /epd-research — find more options to compare
```

## Edge Cases

- **Single product**: Can't compare, but can still show the data card with industry average context. Suggest finding more EPDs to compare against.
- **Mixed material categories**: Warn that cross-material comparison (e.g., concrete vs. steel) is generally not meaningful because declared units and functional roles differ. Offer to group by category.
- **Incomplete data**: Compare on whatever fields are available. Use `—` for missing values. Note which products have more complete data.
- **All expired EPDs**: Proceed with comparison but add a prominent warning that results are based on expired declarations and should be verified with current EPDs.
- **Very large comparisons (10+ products)**: Show summary table first, then offer to drill into top 3-5 candidates.

## Notes

- **This skill reads, not writes.** It does not add rows to the EPD Google Sheet. It produces a comparison report as a markdown file.
- **No hardcoded baselines.** Never use approximate GWP baselines from training data. If the user needs a baseline comparison, ask them to provide an industry-average EPD or use `/epd-research` to find one. EC3 API integration is in progress and will automate this.
- **GWP (A1-A3) is the primary metric** for most comparisons and LEED. Other indicators (ODP, AP, EP) provide a fuller picture but GWP drives most specification decisions.
- **Suggest next skills.** After comparison, the natural next steps are `/epd-to-spec` (to write spec language) or `/epd-research` (to find alternatives).
