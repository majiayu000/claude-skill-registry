---
name: alma-scraper
description: Intelligent scraper for Australian youth justice sources. Discovers, extracts, and learns from government, Indigenous, research, and media sources.
---

# ALMA Intelligent Scraper

## When to Use
- Finding new youth justice information
- Updating ALMA intelligence
- Discovering new sources
- Analyzing coverage gaps
- Checking what's new in youth justice

## Commands

| Command | Purpose | Duration |
|---------|---------|----------|
| `quick` | Top 10 high-value sources | 5 min |
| `deep` | All 50+ sources with discovery | 30-60 min |
| `discover` | Follow discovered links | Variable |
| `source "QLD"` | Deep dive specific jurisdiction | 15 min |
| `gaps` | Show coverage gaps | 2 min |
| `status` | Current knowledge state | Instant |

## Learning Cycle

```
SCRAPE → EXTRACT → EVALUATE → LEARN → STORE
         (Claude)   (Quality)  (Patterns)
```

## Quality Signals

| Signal | Weight |
|--------|--------|
| Relevance (AU youth justice?) | 30% |
| Novelty (new info?) | 25% |
| Specificity (concrete details?) | 20% |
| Evidence (research backed?) | 15% |
| Actionability (useful?) | 10% |

## Priority Formula
```
priority = (quality × 0.4) + (freshness_need × 0.3) + (coverage_gap × 0.3)
```

## Sacred Boundaries

**Never scrape:** Private info, court records, social media, paywalled
**Always mark:** Community Controlled, Indigenous orgs, cultural knowledge
**Always check:** Consent level, cultural authority, data sovereignty

## File References

| Need | Reference |
|------|-----------|
| Database schema | `references/database-schema.md` |
| Extraction patterns | `references/extraction-patterns.md` |
| Coverage tracking | `references/coverage-tracking.md` |
| Implementation code | `references/implementation.md` |
