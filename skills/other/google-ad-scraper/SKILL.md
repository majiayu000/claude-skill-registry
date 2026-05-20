---
name: google-ad-scraper
description: Scrape competitor ads from Google's Ads Transparency Center (Search, YouTube, Display, Gmail). Search by company name, domain, or advertiser ID. Returns ad creatives, formats, targeting regions, and campaign details. Use for competitive ad research and messaging analysis.
---

# Google Ads Transparency Scraper

Scrape ads from Google's Ads Transparency Center using the Apify `xtech/google-ad-transparency-scraper` actor. Covers Search, YouTube, Display, and Gmail ads.

## Quick Start

Requires `APIFY_API_TOKEN` env var (or `--token` flag). Install dependency: `pip install requests`.

```bash
# Search by company name (auto-resolves advertiser ID)
python3 skills/google-ad-scraper/scripts/search_google_ads.py \
  --company "Nike"

# Search by domain (more precise)
python3 skills/google-ad-scraper/scripts/search_google_ads.py \
  --domain "nike.com"

# Direct advertiser ID (skip lookup step)
python3 skills/google-ad-scraper/scripts/search_google_ads.py \
  --advertiser-id "AR13129532367502835713"

# With region filter
python3 skills/google-ad-scraper/scripts/search_google_ads.py \
  --company "Shopify" --region US

# Limit results
python3 skills/google-ad-scraper/scripts/search_google_ads.py \
  --domain "hubspot.com" --max-ads 30

# Human-readable summary
python3 skills/google-ad-scraper/scripts/search_google_ads.py \
  --company "Stripe" --output summary
```

## How It Works

1. **Advertiser Resolution** (if no `--advertiser-id` provided):
   - Takes company name or domain
   - Searches Google Ads Transparency Center using Apify's web-scraper (Puppeteer)
   - Extracts advertiser ID(s) from search results (format: `AR` + 20 digits)
2. **Ad Scraping**:
   - Constructs transparency center URL for the advertiser
   - Calls the Apify `xtech/google-ad-transparency-scraper` actor
   - Polls until complete, fetches dataset
3. **Output**: Returns ads as JSON or human-readable summary

## Advertiser ID Resolution

The script handles the name → ID lookup automatically:

- **By domain** (`--domain nike.com`): Searches `adstransparency.google.com/?domain=nike.com`. Most reliable method.
- **By name** (`--company "Nike"`): Searches `adstransparency.google.com/?text=Nike`. May return multiple matches.
- **Direct ID** (`--advertiser-id AR...`): Skips lookup entirely. Use when you already have the ID.

### Finding the Advertiser ID Manually

If auto-resolution fails:
1. Go to https://adstransparency.google.com
2. Search for the company
3. Click on the advertiser
4. Copy the ID from the URL: `https://adstransparency.google.com/advertiser/AR17828074650563772417`
5. Pass it via `--advertiser-id AR17828074650563772417`

## CLI Reference

| Flag | Default | Description |
|------|---------|-------------|
| `--company` | none | Company name to search |
| `--domain` | none | Company domain (e.g. nike.com) — more precise |
| `--advertiser-id` | none | Google Ads advertiser ID(s), comma-separated (skips lookup) |
| `--region` | anywhere | Region filter (US, GB, DE, etc. or "anywhere") |
| `--max-ads` | 50 | Maximum number of ads to return |
| `--output` | json | Output format: `json` or `summary` |
| `--token` | env var | Apify token (prefer `APIFY_API_TOKEN` env var) |
| `--timeout` | 300 | Max seconds to wait for Apify run |

At least one of `--company`, `--domain`, or `--advertiser-id` is required.

## Output Fields

Each ad in the output may contain (varies by ad format):

```json
{
  "advertiser_name": "Nike, Inc.",
  "advertiser_id": "AR13129532367502835713",
  "ad_format": "TEXT",
  "headline": "Nike.com - Official Site",
  "description": "Shop the latest Nike shoes, clothing...",
  "display_url": "nike.com",
  "destination_url": "https://www.nike.com/",
  "region": "United States",
  "last_shown": "2026-02-20",
  "first_shown": "2026-01-15",
  "image_url": "https://...",
  "video_url": "https://..."
}
```

## Cost

- Advertiser lookup: ~$0.05 (one web-scraper page)
- Ad scraping: Varies by actor pricing, typically a few cents per advertiser

## Common Workflows

### 1. Competitor Ad Research

```bash
python3 skills/google-ad-scraper/scripts/search_google_ads.py \
  --domain "competitor.com" --max-ads 100 --output summary
```

### 2. Compare Multiple Competitors

```bash
# Get IDs first, then scrape in one run
python3 skills/google-ad-scraper/scripts/search_google_ads.py \
  --advertiser-id "AR111,AR222,AR333" --max-ads 50
```

### 3. Regional Ad Targeting Analysis

```bash
# See what ads run in specific regions
python3 skills/google-ad-scraper/scripts/search_google_ads.py \
  --domain "shopify.com" --region US --output summary

python3 skills/google-ad-scraper/scripts/search_google_ads.py \
  --domain "shopify.com" --region GB --output summary
```

## Limitations

- **Advertiser ID lookup** uses Puppeteer-based web scraping of Google's SPA. It may occasionally fail — use `--domain` for best results or provide `--advertiser-id` directly.
- **Ad coverage**: Google only shows ads from verified advertisers. Some smaller advertisers may not appear.
- **Historical data**: The Transparency Center primarily shows recently active ads.

## Configuration

See `references/apify-config.md` for detailed API configuration, token setup, and rate limits.
