---
name: gsc
description: Query Google Search Console for SEO data - search queries, top pages, CTR opportunities, URL inspection, and sitemaps. Use when analyzing search performance, finding optimization opportunities, or checking indexing status.
---

# Google Search Console Skill

Query GSC for search analytics, indexing status, and SEO insights.

## Setup

### Required Environment Variables

Add to `.env`:
```
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REFRESH_TOKEN=your-refresh-token
```

### Setup Steps

1. **Enable API**: Go to [Google Cloud Console](https://console.cloud.google.com/apis/library/searchconsole.googleapis.com) and enable Search Console API
2. **Create OAuth Credentials**: In Google Cloud Console → APIs & Services → Credentials → Create OAuth client ID
3. **Add Scopes**: Configure `webmasters.readonly` scope on your OAuth consent screen
4. **Get Refresh Token**: Run initial auth flow to get refresh token
5. **Property Access**: Your Google account must have access to the Search Console properties

### First-time Auth

```bash
# Run the auth script to get your refresh token
python3 scripts/gsc_query.py auth
```

## Commands

### List Available Sites
```bash
python3 .claude/skills/gsc/scripts/gsc_query.py sites
```

### Top Search Queries
```bash
python3 .claude/skills/gsc/scripts/gsc_query.py top-queries \
  --site "https://opened.co" \
  --days 28 \
  --limit 20
```

### Top Pages by Traffic
```bash
python3 .claude/skills/gsc/scripts/gsc_query.py top-pages \
  --site "https://opened.co" \
  --days 28 \
  --limit 20
```

### Find Low-CTR Opportunities
High impressions but low click-through rate = optimization opportunities:
```bash
python3 .claude/skills/gsc/scripts/gsc_query.py opportunities \
  --site "https://opened.co" \
  --days 28 \
  --min-impressions 100
```

### Inspect URL Indexing Status
```bash
python3 .claude/skills/gsc/scripts/gsc_query.py inspect-url \
  --site "https://opened.co" \
  --url "/blog/waldorf-vs-montessori"
```

### List Sitemaps
```bash
python3 .claude/skills/gsc/scripts/gsc_query.py sitemaps \
  --site "https://opened.co"
```

### Raw Search Analytics (JSON)
```bash
python3 .claude/skills/gsc/scripts/gsc_query.py search-analytics \
  --site "https://opened.co" \
  --days 28 \
  --dimensions query page \
  --limit 100
```

## Available Dimensions
- `query` - Search query
- `page` - Landing page URL
- `country` - Country code
- `device` - DESKTOP, MOBILE, TABLET
- `date` - Date

## Metrics Returned
- **clicks** - Number of clicks from search
- **impressions** - Number of times shown in search
- **ctr** - Click-through rate (clicks/impressions)
- **position** - Average ranking position

## SEO Use Cases

### 1. Content Optimization
Find high-impression/low-CTR pages → improve titles & descriptions

### 2. Keyword Research
See what queries bring traffic → create more content around them

### 3. Technical SEO
Check indexing status, find crawl issues

### 4. Ranking Tracking
Monitor position changes over time

### 5. Sitemap Health
Verify sitemaps are submitted and error-free

## Integration with SEO Content Production

After publishing a new article:
```bash
# Check if indexed (wait 1-2 weeks)
python3 .claude/skills/gsc/scripts/gsc_query.py inspect-url \
  --site "https://opened.co" \
  --url "/blog/waldorf-vs-montessori"

# Monitor ranking position
python3 .claude/skills/gsc/scripts/gsc_query.py search-analytics \
  --site "https://opened.co" \
  --days 28 \
  --dimensions query \
  --filter "page=/blog/waldorf-vs-montessori"
```

## Notes

- Data has ~3 day delay (GSC limitation)
- Credentials shared with GA4 skill
- URL inspection requires the page to be in the property

## Troubleshooting

**"Access denied"**: Make sure your Google account has access to the GSC property

**"Invalid credentials"**: Run auth flow again to refresh tokens

**"No data"**: New pages take 1-2 weeks to appear in GSC
