---
name: google-trends
version: 1.0.0
description: Monitor Google Trends - get trending searches, compare keywords, and track interest over time. Use for market research, content planning, and trend analysis.
author: Buba Draugelis
license: MIT
tags:
  - trends
  - marketing
  - research
  - seo
  - content
metadata:
  openclaw:
    emoji: "📈"
---

# Google Trends Monitoring

Monitor and analyze Google Trends data for market research, content planning, and trend tracking.

## Capabilities

1. **Daily Trending Searches** - What's trending today in any country
2. **Keyword Interest Over Time** - Historical trend data for keywords
3. **Keyword Comparison** - Compare multiple keywords
4. **Related Topics & Queries** - Discover related searches
5. **Regional Interest** - See where keywords are most popular

## Usage

### Get Trending Searches (Today)

Use web_fetch to get Google Trends RSS:

```bash
# US Daily Trends
curl -s "https://trends.google.com/trending/rss?geo=US" | head -100

# Lithuania
curl -s "https://trends.google.com/trending/rss?geo=LT" | head -100

# Worldwide
curl -s "https://trends.google.com/trending/rss?geo=" | head -100
```

### Check Keyword Interest

For detailed keyword analysis, use the Google Trends website:

```bash
# Open in browser
open "https://trends.google.com/trends/explore?q=bitcoin&geo=US"

# Or fetch via web_fetch for basic data
web_fetch "https://trends.google.com/trends/explore?q=bitcoin"
```

### Compare Keywords

```bash
# Compare multiple terms (comma-separated)
open "https://trends.google.com/trends/explore?q=bitcoin,ethereum,solana&geo=US"
```

## Scripts

### trends-daily.sh

Get today's trending searches:

```bash
#!/bin/bash
# Usage: ./trends-daily.sh [country_code]
# Example: ./trends-daily.sh LT

GEO="${1:-US}"
curl -s "https://trends.google.com/trending/rss?geo=$GEO" | \
  grep -o '<title>[^<]*</title>' | \
  sed 's/<[^>]*>//g' | \
  tail -n +2 | \
  head -20
```

### trends-compare.sh

Generate comparison URL:

```bash
#!/bin/bash
# Usage: ./trends-compare.sh keyword1 keyword2 keyword3
# Example: ./trends-compare.sh bitcoin ethereum solana

KEYWORDS=$(echo "$@" | tr ' ' ',')
echo "https://trends.google.com/trends/explore?q=$KEYWORDS"
```

## Example Workflows

### Morning Market Research

```
1. Get US trending searches
2. Get LT trending searches  
3. Check if any trends relate to our business
4. Report interesting findings
```

### Content Planning

```
1. Compare potential blog topics
2. Find which has more search interest
3. Check seasonal patterns
4. Decide on content focus
```

### Competitor Monitoring

```
1. Compare brand names
2. Track interest over time
3. Identify when competitors spike
4. Investigate causes
```

## Cron Job Integration

Set up automated trend monitoring:

```javascript
// Example cron job for daily trends report
{
  "name": "Daily Trends Report",
  "schedule": { "kind": "cron", "expr": "0 9 * * *" },
  "payload": {
    "kind": "agentTurn",
    "message": "Get today's Google Trends for US and LT. Summarize top 10 trends for each. Highlight any tech/business related trends."
  }
}
```

## Countries

Common country codes:
- US - United States
- LT - Lithuania
- DE - Germany
- GB - United Kingdom
- FR - France
- JP - Japan
- (empty) - Worldwide

## Limitations

- Google Trends doesn't provide official API
- Rate limiting may apply for heavy usage
- Data is relative (not absolute numbers)
- Historical data limited to ~5 years for detailed view

## Tips

1. **Use specific terms** - "iPhone 15 Pro" vs just "iPhone"
2. **Check seasonality** - Some trends are cyclical
3. **Compare with baseline** - Use a stable term for reference
4. **Look at related queries** - Discover new opportunities
5. **Monitor competitors** - Track brand interest over time
