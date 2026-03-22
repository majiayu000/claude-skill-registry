---
name: ga4
description: Query Google Analytics 4 (GA4) data via the Analytics Data API. Use when you need to pull website analytics like top pages, traffic sources, user counts, sessions, conversions, or any GA4 metrics/dimensions. Supports custom date ranges and filtering.
homepage: https://developers.google.com/analytics
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires":
          {
            "anyBins": ["python3", "python"],
            "env": ["GA4_PROPERTY_ID", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"],
          },
      },
  }
---

# GA4 - Google Analytics 4 Data API

Query GA4 properties for analytics data: page views, sessions, users, traffic sources, conversions, and more.

## Setup (one-time)

1. Enable Google Analytics Data API: https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com
2. Create OAuth credentials or use existing Google Cloud project
3. Set environment variables:
   - `GA4_PROPERTY_ID` - Your GA4 property ID (numeric, e.g., "123456789")
   - `GOOGLE_CLIENT_ID` - OAuth client ID
   - `GOOGLE_CLIENT_SECRET` - OAuth client secret
   - `GOOGLE_REFRESH_TOKEN` - OAuth refresh token (from initial auth flow)



## Safety Boundaries

- This skill only connects to Google Analytics Data API endpoints.
- It does NOT write to or modify your GA4 property — read-only queries only.
- It does NOT store or transmit credentials beyond the current session.
- It requires OAuth credentials (client ID, secret, refresh token) set as environment variables.
## Common Queries

### Top Pages (by pageviews)
```bash
python3 scripts/ga4_query.py --metric screenPageViews --dimension pagePath --limit 30
```

### Top Pages with Sessions & Users
```bash
python3 scripts/ga4_query.py --metrics screenPageViews,sessions,totalUsers --dimension pagePath --limit 20
```

### Traffic Sources
```bash
python3 scripts/ga4_query.py --metric sessions --dimension sessionSource --limit 20
```

### Landing Pages
```bash
python3 scripts/ga4_query.py --metric sessions --dimension landingPage --limit 30
```

### Custom Date Range
```bash
python3 scripts/ga4_query.py --metric sessions --dimension pagePath --start 2026-01-01 --end 2026-01-15
```

### Filter by Page Path
```bash
python3 scripts/ga4_query.py --metric screenPageViews --dimension pagePath --filter "pagePath=~/blog/"
```

## Available Metrics

Common metrics: `screenPageViews`, `sessions`, `totalUsers`, `newUsers`, `activeUsers`, `bounceRate`, `averageSessionDuration`, `conversions`, `eventCount`

## Available Dimensions

Common dimensions: `pagePath`, `pageTitle`, `landingPage`, `sessionSource`, `sessionMedium`, `sessionCampaignName`, `country`, `city`, `deviceCategory`, `browser`, `date`

## Output Formats

Default: Table format
Add `--json` for JSON output
Add `--csv` for CSV output
