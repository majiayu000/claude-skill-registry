---
name: rank-monitoring
category: search-dominance
version: 1.0.0
description: Real-time ranking check procedures
priority: 3
---

# Rank Monitoring Skill

Procedures for monitoring search rankings and detecting changes.

## Check Frequency

- **Primary keywords**: Daily
- **Secondary keywords**: 3x/week
- **Long-tail keywords**: Weekly
- **Competitor content**: Daily

## Data Sources

### DataForSEO
```python
# Australian SERP check
location = "Brisbane, Queensland, Australia"
device = "desktop"  # Also check "mobile"
language = "en"
```

### SEMrush
```python
database = "au"  # Australian database
```

### Google Search Console
```python
country = "aus"
dimensions = ["query", "page", "device"]
```

## SERP Feature Tracking

Monitor for:
- **AI Overviews** (top priority)
- **People Also Ask (PAA)**
- **Featured Snippets**
- **Local Pack** (Google Business)
- **Reviews** (star ratings)
- **Image Pack**

## Alert Triggers

### CRITICAL
- Lost #1 for primary keyword
- Traffic drop >30%
- Competitor outranks on brand term

### WARNING
- Top 10 keyword moved 3+ positions
- New competitor content
- Negative review posted

### INFO
- Minor position changes (1-2)
- New keyword opportunity
- Backlink gained

## Historical Data Storage

```json
{
  "keyword": "water damage Brisbane",
  "date": "2026-01-06",
  "position": 2,
  "serp_features": ["PAA", "Local Pack"],
  "competitors": {
    "competitor1.com": 1,
    "competitor2.com": 3
  },
  "ai_overview": true,
  "cited_in_ai": false
}
```

## Response Actions

**Lost #1**:
1. Review competitor content
2. Check for algorithm update
3. Audit technical SEO
4. Plan content refresh

**New Competitor**:
1. Analyze their strategy
2. Identify content gaps
3. Plan counter-content
4. Monitor their backlinks

**SERP Feature Lost**:
1. Review schema markup
2. Check content structure
3. Optimize for feature
4. Monitor recovery
