---
name: airbnb-search-listing
description: "Extracts Airbnb accommodation search results from a destination query via SSR-embedded data, returning listing ID, URL, name, coordinates, rating, price, photos, and badge info for each result, plus pagination cursors for multi-page retrieval. Use when user mentions Airbnb search results, Airbnb listings, vacation rental search, short-term rental listings, scrape Airbnb, get Airbnb data, find rentals on Airbnb, Airbnb destination search, Airbnb property list, Airbnb stays search, Airbnb accommodation results, pull Airbnb listings, collect Airbnb search data, Airbnb scraper, Airbnb search page extraction, Airbnb search by destination."
---

# Airbnb — Search Listing Extraction

> Navigate to Airbnb search URL → extract listing results from SSR-embedded data

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract accommodation listing results from an Airbnb search page using SSR-embedded niobeClientData JSON.

## Prerequisites

- Target search page is already open in the browser: `https://www.airbnb.com/s/{destination}/homes`
- No login required — search results are publicly accessible

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### DOM: extract search results (SSR niobeClientData)

Navigate to the search URL first, wait for the page to load, then run:

`eval "$(python scripts/search-listing.py)"`

URL construction pattern:
```
https://www.airbnb.com/s/{destination}/homes?checkin={YYYY-MM-DD}&checkout={YYYY-MM-DD}&adults={N}&children={N}&infants={N}&pets={N}&price_min={N}&price_max={N}&min_beds={N}&min_bedrooms={N}&min_bathrooms={N}&cursor={base64_cursor}
```

All URL parameters are optional except destination. Omit any parameter to use the Airbnb default.

Full invocation sequence:
1. `navigate https://www.airbnb.com/s/{destination}/homes?{params}`
2. `wait stable`
3. `eval "$(python scripts/search-listing.py)"`

Output example:
```json
{
  "items": [
    {
      "id": "5476930",
      "url": "https://www.airbnb.com/rooms/5476930",
      "name": "Bright Studio in Notting Hill",
      "lat": 51.5101,
      "lng": -0.1949,
      "rating": "4.85",
      "title": "Entire studio in London",
      "price_total": "$120 total",
      "price_qualifier": "before taxes",
      "photos": ["https://a0.muscache.com/im/pictures/...jpeg"],
      "badges": ["Guest favorite"]
    }
  ],
  "count": 18,
  "total_pages": 13,
  "cursors": ["eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoxOCwidmVyc2lvbiI6MX0="]
}
```

Error handling: If `error: true` is returned, verify the current page is an Airbnb search results page (URL contains `/s/` and `/homes`), then retry once after `wait stable`. If niobeClientData is not found, the page may still be loading — wait and retry.

## Pagination

**URL Pagination**: URL pattern `https://www.airbnb.com/s/{destination}/homes?{filters}&cursor={cursor}`. Each page returns a `cursors` array where `cursors[0]` is the current page, `cursors[1]` is page 2, `cursors[2]` is page 3, etc. `total_pages` equals the length of `cursors`. Termination: index >= `total_pages` OR `count` is 0.

Paginate by taking the cursor from the previous result and navigating:
1. First page: navigate without cursor; extract `cursors` array from result
2. Page 2: `navigate https://www.airbnb.com/s/{destination}/homes?{filters}&cursor={cursors[1]}`
3. `wait stable`
4. `eval "$(python scripts/search-listing.py)"`
5. Page N: use `cursors[N-1]` from the original page-1 `cursors` array
6. Stop when page index >= total_pages or count is 0

## Success Criteria

`count >= 1 AND items[0].id is not null AND items[0].url is not null`

## Known Limitations

- Returns up to 18 listings per page (Airbnb's default page size)
- Maximum ~240 results total across all pages (Airbnb's search cap)
- `rating` may be null for new listings with no reviews
- `price_total` is null when no dates are specified in search

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through cursors serially; do not parallelize within one browser session
- **Test before batch execution**: After writing a batch script, test with 1-2 pages before running full pagination
- **Error resumption**: Save results page by page; resume from the last successful page on failure

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/airbnb-scraper-airbnb-search-listing.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
