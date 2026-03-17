---
name: ga4
description: Query Google Analytics 4 (GA4) data via the Analytics Data API. Use when you need to pull website analytics like top pages, traffic sources, user counts, sessions, conversions, or any GA4 metrics/dimensions.
---

# GA4 - Google Analytics 4 Data API

Query GA4 properties for analytics data: page views, sessions, users, traffic sources, conversions, and more.

## Setup

### Required Environment Variables

Add to `.env`:
```
GA4_PROPERTY_ID=your-property-id
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REFRESH_TOKEN=your-refresh-token
```

### Setup Steps

1. **Enable API**: [Google Analytics Data API](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com)
2. **Find Property ID**: GA4 Admin → Property Settings → Property ID (numeric)
3. **Create OAuth**: Google Cloud Console → APIs & Services → Credentials
4. **Get Refresh Token**: Run initial auth flow

## Commands

### Top Pages (by pageviews)
```bash
python3 .claude/skills/ga4/scripts/ga4_query.py \
  --metric screenPageViews \
  --dimension pagePath \
  --limit 30
```

### Top Pages with Sessions & Users
```bash
python3 .claude/skills/ga4/scripts/ga4_query.py \
  --metrics screenPageViews,sessions,totalUsers \
  --dimension pagePath \
  --limit 20
```

### Traffic Sources
```bash
python3 .claude/skills/ga4/scripts/ga4_query.py \
  --metric sessions \
  --dimension sessionSource \
  --limit 20
```

### Landing Pages
```bash
python3 .claude/skills/ga4/scripts/ga4_query.py \
  --metric sessions \
  --dimension landingPage \
  --limit 30
```

### Custom Date Range
```bash
python3 .claude/skills/ga4/scripts/ga4_query.py \
  --metric sessions \
  --dimension pagePath \
  --start 2026-01-01 \
  --end 2026-01-28
```

### Filter by Page Path (Blog Posts)
```bash
python3 .claude/skills/ga4/scripts/ga4_query.py \
  --metric screenPageViews \
  --dimension pagePath \
  --filter "pagePath=~/blog/"
```

### Track Specific Article Performance
```bash
python3 .claude/skills/ga4/scripts/ga4_query.py \
  --metrics screenPageViews,sessions,totalUsers,bounceRate \
  --dimension date \
  --filter "pagePath=/blog/waldorf-vs-montessori" \
  --start 2026-01-28 \
  --end 2026-02-28
```

## Available Metrics

| Metric | Description |
|--------|-------------|
| `screenPageViews` | Total page views |
| `sessions` | Number of sessions |
| `totalUsers` | Total unique users |
| `newUsers` | First-time visitors |
| `activeUsers` | Users with engagement |
| `bounceRate` | Single-page session rate |
| `averageSessionDuration` | Avg time on site |
| `conversions` | Goal completions |
| `eventCount` | Total events |

## Available Dimensions

| Dimension | Description |
|-----------|-------------|
| `pagePath` | URL path |
| `pageTitle` | Page title |
| `landingPage` | Entry page |
| `sessionSource` | Traffic source |
| `sessionMedium` | Traffic medium |
| `sessionCampaignName` | Campaign name |
| `country` | Visitor country |
| `city` | Visitor city |
| `deviceCategory` | Desktop/Mobile/Tablet |
| `browser` | Browser name |
| `date` | Date |

## Output Formats

```bash
# Default: Table format
python3 scripts/ga4_query.py --metric sessions --dimension pagePath

# JSON output
python3 scripts/ga4_query.py --metric sessions --dimension pagePath --json

# CSV output
python3 scripts/ga4_query.py --metric sessions --dimension pagePath --csv
```

## SEO Content Tracking

### After Publishing New Content

Track article performance over time:

```bash
# Week 1: Check initial traffic
python3 .claude/skills/ga4/scripts/ga4_query.py \
  --metrics screenPageViews,sessions,bounceRate \
  --dimension date \
  --filter "pagePath=/blog/waldorf-vs-montessori" \
  --start 2026-01-28 \
  --end 2026-02-04

# Compare to similar content
python3 .claude/skills/ga4/scripts/ga4_query.py \
  --metric screenPageViews \
  --dimension pagePath \
  --filter "pagePath=~/blog/" \
  --limit 20
```

### Monthly SEO Report

```bash
# Top organic landing pages
python3 .claude/skills/ga4/scripts/ga4_query.py \
  --metrics sessions,totalUsers,bounceRate \
  --dimension landingPage \
  --filter "sessionSource=google" \
  --limit 30

# Traffic by source
python3 .claude/skills/ga4/scripts/ga4_query.py \
  --metric sessions \
  --dimensions sessionSource,sessionMedium \
  --limit 20
```

## Integration Notes

- Credentials shared with GSC skill
- Data is near real-time (unlike GSC's 3-day delay)
- Use with `seo-content-production` skill for performance tracking
