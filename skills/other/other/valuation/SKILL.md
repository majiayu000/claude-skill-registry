---
name: valuation
description: Reference for auction item valuation logic, market data analysis, pricing strategies, and confidence scoring. Use when working on valuation features, market analysis dashboard, sales analysis, or search query logic.
argument-hint: [topic or item type]
---

# Auction Valuation & Market Analysis Reference

Use this skill when working on valuation logic, market data features, or pricing. Focus on: `$ARGUMENTS`

## Valuation Architecture in the Extension

### Data Flow
```
Item fields → SearchQuerySSoT → Auctionet API (3.65M+ results) → Market metrics → Dashboard display
                                      ↓
                              AI relevance filtering (Haiku)
                                      ↓
                              Filtered market data → Median, range, trends
```

### Key Components
- **SearchQuerySSoT** (`modules/search-query-ssot.js`) — single source of truth for all search queries
- **SalesAnalysisManager** (`modules/sales-analysis-manager.js`) — fetches and processes market data
- **DashboardManagerV2** (`modules/dashboard-manager-v2.js`) — renders market analysis UI
- **AuctionetAPI** (`modules/auctionet-api.js`) — Auctionet public API wrapper
- **ValuationRequestAssistant** (`modules/valuation-request-assistant.js`) — valuation page logic

## Pricing Rules

### Reserve vs Estimate
- **Estimate** (uppskattat värde): expected market value based on comparables
- **Reserve** (utropspris): minimum starting bid, typically 60–80% of estimate
- **Minimum reserve**: 400 SEK (auction house rule)
- Reserve should be low enough to attract bidding but protect seller interest

### Valuation Approach (4-step)
1. **Object analysis** — identify type, material, artist, period, condition
2. **Market research** — search Auctionet historical data for comparables
3. **Valuation logic** — median of filtered comparables, adjusted for condition/quality
4. **Conclusion** — estimate with confidence level and reasoning

### Confidence Scoring
| Level | Meaning | Typical scenario |
|-------|---------|-----------------|
| High (>80%) | Strong comparable data | Known artist/maker, many recent sales |
| Medium (50–80%) | Some comparables, wider range | Similar items exist but not exact matches |
| Low (<50%) | Limited data, high uncertainty | Rare items, no recent comparables |

### AI Relevance Filtering
When Auctionet API returns results with high price spread (>5x between min and max):
- Claude Haiku validates each result for relevance
- Filters out false positives (same name but different item)
- Re-calculates metrics on filtered set
- Reports data quality to user via dashboard

## Market Data Metrics

### Key Metrics Displayed
- **Median price** — middle value of comparable sales (more robust than mean)
- **Price range** — min to max of filtered comparables
- **Mean price** — average (shown alongside median)
- **Result count** — number of comparable sales found
- **Market status** — rising/stable/falling trend indicator
- **Historical change %** — YoY or period-over-period price movement

### Search Query Strategy
Terms are generated from multiple sources:
1. **AI-extracted** — Claude Sonnet extracts optimal search terms from title + description
2. **User-refined** — cataloger can toggle/add terms via interactive pills
3. **Artist name** — always quoted for exact matching in API
4. **Object type** — extracted from title (first word typically)

### Term Quoting Rules
- Artist names: always quoted for exact match → `"Bruno Mathsson"`
- Multi-word terms: quoted to prevent partial matching
- Single common terms: unquoted for broader matching

## Valuation Request Pages

### Multi-Group Valuation Flow
1. Customer submits images + description via Auctionet website
2. Extension scrapes page for: customer name, email, images, description
3. AI clusters images into logical groups (e.g., 3 images = 1 item)
4. Cataloger can drag/drop images between groups, rename groups
5. Each group gets independent valuation with:
   - AI estimate from images + description
   - Market data override from Auctionet API comparables
   - Confidence score
6. Email template generated in Swedish or English

### Valuation Email Conventions
- Professional but warm tone
- Per-item breakdown with estimate range
- Disclaimer: estimates are not guarantees
- Next steps: how to consign items
- Language matches customer preference (Swedish default)

### AI Model Selection for Valuations
- **Opus** for valuation requests (highest accuracy for customer-facing content)
- **Sonnet** for quick cataloging valuations (balanced speed/quality)
- **Haiku** for relevance filtering of market data (speed critical)

## Common Valuation Pitfalls

### Over-valuation Risks
- AI tends to overvalue when it recognizes a famous maker/artist
- Always cross-reference with actual Auctionet hammer prices
- Condition significantly impacts value — a damaged piece by a famous maker can be worth less than a pristine unknown

### Under-valuation Risks
- Low/medium confidence should NOT automatically lead to low valuations
- Rare items may have few comparables but high value
- Consider: is it rare because it's undesirable, or because it's genuinely scarce?

### Market Data Interpretation
- Small sample size (<5 results): treat as indicative only
- Old data (>2 years): market may have shifted, weight recent results higher
- Outliers: single very high/low result can skew mean — median is more reliable
- Category matters: "stol" (chair) matches thousands — refine with style/period/maker
