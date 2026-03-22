---
name: local-prospect-audit
description: >
  Quick pre-sales assessment of a local business prospect. Determines GO / SOFT GO / NO-GO
  before investing time in a client. Use when user says "oceń tego klienta", "czy warto go brać",
  "zrób pre-sales audit", "sprawdz konkurencje dla X", "czy łatwo go wypromować", or shares
  a business name/URL asking if it's worth pursuing. Costs max $0.10 in DataForSEO credits.
allowed-tools: Bash
---

### Goal
Produce a GO / SOFT GO / NO-GO decision in under 5 minutes using cheap data sources.
Max DataForSEO spend: $0.10 per prospect.

### Required inputs (ask if missing)
- Business name
- City / primary market
- Primary service category
- Website URL (if they have one)

### Data sources
- DataForSEO `business_data/google/my_business_info/live` -- GBP data for client and top 3 competitors (~$0.01)
- DataForSEO `serp/google/organic/live/regular` depth=1 -- check organic ranking (~$0.003)
- Direct website fetch -- check title tag, location pages (free)
- Auth: load DATAFORSEO_BASE64 from .env

### Checklist (run in this order)

**Step 1: GBP presence**
Call DataForSEO business_data for the client's business name + city.
- Does GBP exist? Is it verified?
- What is the primary category?
- How many reviews? What is approximate velocity (check date of most recent reviews)?

**Step 2: Competitor benchmark**
Call DataForSEO business_data for "[primary service] [city]" to get top 3 map pack results.
For each competitor record:
- Review count + velocity (look at most recent review date)
- Primary category
- Website domain

Velocity Override Rule:
- Competitor with 200+ reviews but last review 2+ months ago = WEAK (subtract 1 point from competition score)
- Competitor with 60+ reviews at 1-2/month = beatable despite total count
- Apply same logic to client: high count + low velocity = stagnating

**Step 3: Title tag check**
Fetch client's homepage. Check:
- Does title tag start with [Service] + [City]?
- If not = easy win available

**Step 4: Location pages**
Check if client has dedicated pages per city/neighborhood or just one page for all.
No location pages = easy wins available.

**Step 5: Organic position check**
DataForSEO SERP check for 2-3 main keywords. Is client visible at all?

**Step 6: Competitor SEO activity**
Signs of active SEO agency: many optimized city pages, schema markup, keyword-rich title tags.
Low competitor SEO activity = easier market.

### Scoring

**Opportunity Score (1-10)** -- higher = better opportunity
- No GBP or unverified: +3
- Wrong/suboptimal category: +2
- Title tag not optimized: +2
- No location pages: +2
- Low review count vs competitors: +1

**Competition Score (1-10)** -- lower = easier market
- Top competitor 100+ reviews at 5+/month: +3
- Top competitor 50-99 reviews: +2
- Top competitor has active SEO (city pages, schema): +2
- Top competitor 10-30 reviews or low velocity: +1
- Apply velocity override: high count + low velocity = reduce score by 1

### Decision logic

| Opportunity | Competition | Decision |
|---|---|---|
| 6+ | 1-4 | GO |
| 4-5 | 1-4 | SOFT GO |
| 6+ | 5-7 | SOFT GO |
| Any | 8-10 | NO-GO |
| 1-3 | Any | NO-GO (client already good, little to improve) |

### Output format

```
PROSPECT ASSESSMENT: [Business Name]
Decision: GO / SOFT GO / NO-GO

Opportunity Score: X/10
Competition Score: X/10

Key Findings:
- GBP: [present/missing] | Category: [correct/wrong -- should be: X] | Reviews: X (~Y/month)
- Title tag: "[current title]" -- [optimized/needs fix]
- Location pages: [yes/no]
- Top competitor: [name] | Reviews: X (~Y/month) | SEO activity: [low/medium/high]
- Review gap to beat top competitor: X reviews

Quick wins (week 1): [list]
Hard work needed: [list]

Recommendation:
[2-3 sentences: why GO/NO-GO, what the pitch is, what to watch out for]

Estimated effort: [Easy: 2-3h setup / Medium: 10-15h / Hard: ongoing competitive]
DataForSEO cost: ~$X
```

### Edge cases
- No website at all: major opportunity (easy win), note in recommendation
- Client already ranking top 3: NO-GO or SOFT GO for maintenance only
- National franchise competitor dominating: flag as hard to beat
- 0 reviews: huge opportunity if category/market has demand
