---
name: yelp-search
description: Search Yelp for local businesses, get contact info, ratings, and hours. Use when finding services (cleaners, groomers, restaurants, etc.), looking up business phone numbers to text, or checking ratings before booking. Triggers on queries about finding businesses, restaurants, services, or "look up on Yelp".
---

# Yelp Search Integration

Search for local businesses on Yelp to find services, get contact information, check ratings, and retrieve hours of operation.

## Setup

### 1. Yelp API Key (Required)

1. Go to https://www.yelp.com/developers
2. Create an account or sign in
3. Click "Create App" and fill out the form
4. Copy your API Key

Add to your `.env` file:
```
YELP_API_KEY=your_api_key_here
```

### 2. Browser-Use for Reviews (Optional)

Only needed if you want to extract review text (slow, ~30-60s per request).

**Install dependencies:**
```bash
uv add browser-use playwright langchain-openai
uv run playwright install chromium
```

**Add to `.env`:**
```
OPENAI_API_KEY=your_openai_key_here
```

Note: Review extraction uses browser-use to search DuckDuckGo (since Yelp blocks direct scraping). For most use cases, the rating + review_count from the API is sufficient.

## Scripts

All scripts are in `tools/yelp-search/scripts/` and should be run with `uv run python`.

### search.py - Find Businesses (Primary Tool)
```bash
uv run python tools/yelp-search/scripts/search.py "search term" --location "City, State"
```

**Options:**
| Flag | Description | Example |
|------|-------------|---------|
| `--location`, `-l` | City, address, or zip | `"San Francisco"` or `"94123"` |
| `--latitude/--longitude` | GPS coordinates | `--latitude 37.78 --longitude -122.41` |
| `--limit`, `-n` | Number of results (default: 5) | `-n 10` |
| `--sort-by` | Sort order | `rating`, `distance`, `review_count`, `best_match` |
| `--price` | Price filter (1-4) | `--price 1,2` for $ and $$ only |
| `--json` | Output raw JSON | |

**Examples:**
```bash
# Find top-rated dog groomers
uv run python tools/yelp-search/scripts/search.py "dog groomer" -l "San Francisco" --sort-by rating

# Find cheap restaurants nearby
uv run python tools/yelp-search/scripts/search.py "restaurants" -l "94123" --price 1,2 --sort-by distance

# Search near a specific address
uv run python tools/yelp-search/scripts/search.py "laundry pickup" -l "123 Main St, San Francisco"
```

### details.py - Get Business Hours & Info
```bash
uv run python tools/yelp-search/scripts/details.py "business-alias"
```

The business alias is in the Yelp URL (e.g., `the-laundry-corner-san-francisco`).

### phone_search.py - Reverse Lookup
```bash
uv run python tools/yelp-search/scripts/phone_search.py "+14155551234"
```

### get_reviews.py - Extract Review Text (Slow)
```bash
uv run python tools/yelp-search/scripts/get_reviews.py "Business Name" -l "City" -n 3
```

**Note:** Uses browser-use which is slow (~30-60s). Yelp blocks direct scraping, so it searches DuckDuckGo for cached reviews as a workaround.

### scrape_reviews.py - Direct Yelp Scraping (Alternative)
```bash
uv run python tools/yelp-search/scripts/scrape_reviews.py "https://www.yelp.com/biz/business-alias" -n 5
```

**Requires Browserbase credentials:**
```
BROWSERBASE_API_KEY=your_key_here
BROWSERBASE_PROJECT_ID=your_project_id
```

**Note:** Uses Browserbase with proxies to bypass Yelp's CAPTCHA. More reliable than `get_reviews.py` but requires a Browserbase account.

## Best Practices

### Evaluating Quality Without Review Text
The API provides rating + review_count which is usually sufficient:

| Rating | Review Count | Interpretation |
|--------|--------------|----------------|
| 4.5+ | 50+ | Excellent, reliable data |
| 4.5+ | <20 | Promising but limited data |
| 4.0-4.4 | 100+ | Good, well-established |
| <4.0 | any | Proceed with caution |

### Finding Services with Specific Needs
When looking for services with specific requirements (weekend hours, pickup/delivery, etc.):

1. **Search** with `--sort-by rating` to get best options
2. **Get details** on top candidates to check hours
3. **Filter** for businesses open when you need them
4. **Contact directly** to confirm specific services (pickup, delivery, etc.) since Yelp doesn't always have this info

### Search Tips
- Use specific terms: `"laundry pickup"` not just `"laundry"`
- Search near an address for accurate distance: `-l "123 Main St, City"`
- Sort by `rating` first, then check `distance` on results
- Check `review_count` - high ratings with few reviews may be unreliable

## Response Data

Each business result includes:
- **name** - Business name
- **phone** - Phone number (use for texting/calling)
- **rating** - Yelp rating (1-5 stars)
- **review_count** - Number of reviews
- **price** - Price level ($ to $$$$)
- **location** - Full address
- **hours** - Operating hours by day (in details)
- **distance** - Distance from search location
- **categories** - Business categories
- **is_open_now** - Current open/closed status

## Limitations

| Feature | Status | Notes |
|---------|--------|-------|
| Business search | ✅ Works | Fast, reliable |
| Business details | ✅ Works | Includes hours |
| Phone lookup | ✅ Works | Reverse search |
| Review text (API) | ❌ Paid only | Requires enterprise tier |
| Review text (scraping) | ⚠️ Slow | browser-use workaround via DuckDuckGo |

- Free API tier: 500 calls/day
- Results limited to 50 per request
- Some business info (pickup/delivery) not in API - contact directly
