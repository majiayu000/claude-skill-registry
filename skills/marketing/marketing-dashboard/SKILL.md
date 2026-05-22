---
name: marketing-dashboard
description: Unified marketing metrics dashboard and CLI. Use when building or running a marketing status dashboard that pulls from PostHog, Google Search Console, Stripe, and ad platforms. Covers traffic, SEO, ads, revenue, and funnel conversion reporting in terminal output.
---

# Marketing Dashboard

Unified CLI for marketing metrics. Built for quick status checks and deeper dives.

## Quick Start

```bash
./dashboard.py status
./dashboard.py seo --period 30d
./dashboard.py ads --period 7d
./dashboard.py revenue --period 90d
./dashboard.py funnel
```

## Commands

- `mktg status` - Traffic (7d), revenue (30d), top errors
- `mktg seo --period [7d|30d|90d]` - GSC clicks, impressions, avg position, top queries
- `mktg ads --period [7d|30d]` - Spend, impressions, clicks, CPA by platform
- `mktg revenue --period [30d|90d]` - MRR, churn, new subs, revenue by product
- `mktg funnel` - Funnel: visit → signup → trial → paid

## Environment

| Variable | Purpose |
| --- | --- |
| `POSTHOG_API_KEY` | PostHog API key |
| `POSTHOG_PROJECT_ID` | PostHog project id |
| `GSC_SITE_URL` | Search Console property URL |
| `GOOGLE_APPLICATION_CREDENTIALS` | Service account JSON path |
| `STRIPE_SECRET_KEY` | Stripe API key |
| `ADS_METRICS_PATH` | JSON file for ad platform metrics |
| `ADS_METRICS_JSON` | Inline JSON for ad metrics |
| `FUNNEL_STEPS` | Comma list of PostHog events (default: `$pageview,signup,trial,paid`) |

### Ads JSON Shape

```json
{
  "google": {"spend": 123.45, "impressions": 10000, "clicks": 321, "cpa": 12.34},
  "meta": {"spend": 98.76, "impressions": 9000, "clicks": 210, "cpa": 15.67}
}
```

## Files

- `dashboard.py` - Click CLI entrypoint (`mktg`)
- `src/posthog_client.py` - PostHog API wrapper via `httpx`
- `src/gsc_client.py` - Search Console wrapper via `google-auth` + `googleapiclient`
- `src/stripe_client.py` - Stripe metrics wrapper
- `src/display.py` - Rich tables and formatting

## Notes

- Prefer PostHog for traffic and funnel. Uses `insights/trend` and `insights/funnel`.
- GSC reads only. Requires Search Console access for the service account.
- Stripe metrics are computed from subscriptions and invoices; keep product naming consistent.
