---
name: content-ideas
description: Suggest content topics ranked by opportunity score. Analyzes GSC keyword data and cross-references with personas to find high-potential topics.
---

# /content-ideas — The Research Lead

"What should I write next?" This skill analyzes your GSC keyword data to find high-potential topics — keywords you already rank for that could perform better with targeted content.

## Arguments

Optional:
- **site**: Site key to analyze (required if multiple sites configured)
- **--count**: Number of ideas to suggest (default: 10)

Example: `/content-ideas kaicalls`
Example: `/content-ideas kaicalls --count 5`

## The Skill

### Step 1: Pull GSC Keyword Data

Run:
```bash
kai-report --site {site} --format json
```

Also pull keyword opportunities by looking for:
- Keywords at position 5-20 (striking distance — could reach page 1 with targeted content)
- Keywords with high impressions but low CTR (opportunity for better content)
- Keywords with high CTR but low impressions (opportunity for broader targeting)

### Step 2: Cross-Reference with Personas

For each keyword opportunity, match it against the 8 personas in `knowledge/personas/`. Score each keyword-persona match by relevance.

### Step 3: Score and Rank

Calculate an **Opportunity Score** (0-100) for each keyword based on:
- **Position gap**: How close to page 1? (position 5-10 = high, 10-20 = medium, 20+ = low)
- **Impression volume**: Higher impressions = bigger opportunity
- **CTR gap**: Current CTR vs expected CTR for that position = room for improvement
- **Persona match**: Strong persona match = higher score
- **Existing content**: Already have content targeting this? Lower score (avoid cannibalization)

### Step 4: Display Ideas

```
CONTENT IDEAS — {site}
══════════════════════════════════════════

Top {N} topics ranked by opportunity score:

  #1  [92] "AI receptionist for law firms"
      Position: 8  |  Impressions: 1,240/mo  |  CTR: 1.8%
      Persona: Shock Absorber
      Why: Position 8 with high impressions — one quality blog post could reach page 1
      Format: blog (recommended)

  #2  [85] "virtual receptionist vs answering service"
      Position: 12  |  Impressions: 890/mo  |  CTR: 0.9%
      Persona: System Manager
      Why: Comparison keyword — no existing content targeting this directly
      Format: blog (recommended)

  #3  [78] "law firm after hours answering"
      Position: 15  |  Impressions: 2,100/mo  |  CTR: 0.4%
      Persona: Shock Absorber
      Why: High impression volume at position 15 — significant traffic upside
      Format: seo (recommended)

  ...
```

### Step 5: Offer Next Step

"Want to create a brief for any of these? Type `/content-brief {format} {site} \"{keyword}\"` to start."

If user picks one, suggest the exact command.

## Error Handling

- **No GSC data**: "GSC data unavailable. Configure your site's GSC property in `kai-config set sites.{site}.gsc_property {value}`"
- **No existing content**: "No published content for {site}. Ideas are based on GSC data only — publish your first piece with `/marketing-sprint` to start the feedback loop."

## Chain State

**Standalone:** First skill in a new content cycle
**Feeds into:** `/content-brief` (user picks a topic)
