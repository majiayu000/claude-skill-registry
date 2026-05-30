---
name: facebook-ads-library-search
description: "Searches Meta Ad Library (Facebook/Instagram/WhatsApp ads) by keyword or Facebook page ID and extracts ad details including creatives, copy, CTA, publisher platforms, spend, impressions, reach estimates, and page transparency info. Use when user mentions Meta Ad Library, Facebook ads scraper, Instagram ads data, FB ad library, search Facebook ads, get ads from a Facebook page, scrape Meta ads, Facebook advertising data, ad creative extraction, competitor ads analysis, brand ads monitoring, Meta advertising transparency, political ads Facebook, housing ads Facebook, view all ads from a page, facebook ads search, fb ads library api, facebook ad archive, instagram ad data, get ad creatives."
---

# Meta Ad Library — Search Ads

> keyword or page ID → ad list with creatives, metrics, and pagination cursor

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Fetch ads from Meta Ad Library for a keyword search or a specific Facebook page, returning structured ad data with all available fields.

## Prerequisites

- Browser is open on any Facebook page: `https://www.facebook.com/`
- No login required for this capability

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### API: search ads by keyword

`eval "$(python scripts/search-ads.py --query '{keyword}' --country {country} --first {count})"`

Parameters:
- `--query`: keyword to search (mutually exclusive with `--page-id`)
- `--country`: 2-letter ISO country code or `ALL`, default `ALL`
- `--active-status`: `active` | `inactive` | `all`, default `active`
- `--ad-type`: `ALL` | `POLITICAL_AND_ISSUE_ADS` | `HOUSING_ADS`, default `ALL`
- `--media-type`: `all` | `image` | `video` | `meme`, default `all`
- `--platforms`: space-separated list, e.g. `facebook instagram`, default all platforms
- `--cursor`: pagination cursor from previous response's `end_cursor`, default first page
- `--first`: number of ads to return per page, default `10`

Output example:
```json
{
  "error": false,
  "count": 10,
  "has_next_page": true,
  "end_cursor": "AQHSmvKYSBolzAS9Wq8VSnt4...",
  "ads": [
    {
      "ad_archive_id": "1869276447125570",  // unique ad archive ID
      "ad_id": null,                         // ad ID (null for some ads)
      "page_id": "15087023444",              // advertiser's Facebook page ID
      "page_name": "Nike",                   // advertiser's page name
      "page_profile_uri": "https://facebook.com/nike",
      "page_profile_picture_url": "https://scontent.xx.fbcdn.net/...",
      "is_active": true,                     // whether ad is currently running
      "start_date": 1773730800,              // ad start date (unix timestamp)
      "end_date": 1779692400,                // ad end date (unix timestamp), null if still active
      "publisher_platform": ["facebook", "instagram"],  // platforms the ad runs on
      "currency": "USD",                     // spend currency, null if not disclosed
      "spend": null,                         // estimated spend range, null if not disclosed
      "impressions_with_index": null,        // impression estimate, null if not disclosed
      "reach_estimate": null,                // reach estimate, null if not disclosed
      "categories": [],                      // ad categories
      "contains_sensitive_content": false,
      "body": "Get the gear that never misses.",  // main ad body text
      "caption": "nike.com",                // ad caption
      "title": "Nike Air Monarch IV",        // ad title
      "cta_text": "Shop Now",               // CTA button text
      "cta_type": "SHOP_NOW",               // CTA button type
      "link_url": "https://www.nike.com/...",// destination URL
      "display_format": "carousel",          // ad format
      "cards": [...],                        // carousel cards (each has body, title, cta_type, link_url, original_image_url, video_hd_url)
      "images": [...],                       // image creatives
      "videos": [...]                        // video creatives
    }
  ]
}
```

### API: search ads by page ID

`eval "$(python scripts/search-ads.py --page-id '{page_id}' --country {country} --first {count})"`

Parameters:
- `--page-id`: Facebook page ID (mutually exclusive with `--query`). To find a page ID: navigate to the Facebook page, the ID appears in the URL or in the page's "About" section
- All other parameters same as keyword search above

Output example: same structure as keyword search above.

## Enum Parameters

`--active-status`: `active` | `inactive` | `all`

`--ad-type`: `ALL` | `POLITICAL_AND_ISSUE_ADS` | `HOUSING_ADS`

`--media-type`: `all` | `image` | `video` | `meme`

`--platforms`: `facebook` | `instagram` | `whatsapp` | `messenger` | `audience_network` | `threads` (pass multiple values space-separated)

`--country`: ISO 2-letter country code (e.g. `US`, `GB`, `DE`, `ALL`) [collection partially done — full list of supported country codes follows ISO 3166-1 alpha-2 standard]

## Pagination

**API Pagination**: `--cursor`, type: cursor, start value: omit for first page. Next page value source: `end_cursor` field in response. Termination: `has_next_page: false`.

## Success Criteria

`error = false AND count >= 0 AND has_next_page field present`

(count may be 0 for valid queries that return no results; this is not an error)

## Known Limitations

- `spend`, `impressions_with_index`, `reach_estimate` fields are frequently `null` — Meta only discloses these for political/social issue ads or at their discretion
- `ad_id` is often `null` — `ad_archive_id` is the reliable unique identifier
- Rate limiting may occur with very high-frequency requests; add 1-2 second delays between requests in batch scripts
- Private or restricted ads may not appear in results
- The `doc_id` (`27201872659451053`) is a compiled query ID that may change when Meta updates their frontend; if errors occur, re-explore to find the updated ID

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/facebook-ads-scraper-facebook-ads-library-search.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} -> {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
