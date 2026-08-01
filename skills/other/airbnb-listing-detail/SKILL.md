---
name: airbnb-listing-detail
description: "Fetches complete Airbnb listing details for a given numeric listing ID via the internal GraphQL API, returning title, room type, description, amenities, photos, coordinates, city, house rules, highlights, ratings, review count, bedroom configuration, and property overview. Use when user mentions Airbnb listing details, Airbnb property info, Airbnb room details, get Airbnb listing data, Airbnb amenities list, Airbnb house rules, Airbnb property description, Airbnb detail page scraper, Airbnb rooms detail, Airbnb property page data, Airbnb listing info, fetch Airbnb room details, pull Airbnb listing."
---

# Airbnb — Listing Detail

> Listing ID → full property detail via internal GraphQL API (no login required)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Fetch comprehensive listing data for an Airbnb property using the internal StaysPdpSections GraphQL API.

## Prerequisites

- Browser is open (any page). The API call is made via `fetch()` in the browser context — no specific page navigation required.
- No login required — the API endpoint is publicly accessible

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### API: fetch listing detail

`eval "$(python scripts/listing-detail.py '{listing_id}')"`

Parameters:
- `listing_id`: numeric Airbnb listing ID (e.g., `5476930`). Extract from listing URL: `airbnb.com/rooms/{listing_id}`
- `--checkin`: check-in date in YYYY-MM-DD format, default: none (price info unavailable without dates)
- `--checkout`: check-out date in YYYY-MM-DD format, default: none
- `--adults`: number of adult guests, default: `1`
- `--locale`: response locale, default: `en`
- `--currency`: price currency code, default: `USD`

Output example:
```json
{
  "id": "5476930",
  "url": "https://www.airbnb.com/rooms/5476930",
  "title": "Bright Studio in Notting Hill",
  "room_type": "ENTIRE_HOME",
  "description": "<p>Welcome to this charming studio...</p>",
  "photos": ["https://a0.muscache.com/im/pictures/...jpeg"],
  "lat": 51.5101,
  "lng": -0.1949,
  "city": "London, England, United Kingdom",
  "amenities": [
    {"name": "Kitchen", "available": true},
    {"name": "Wifi", "available": true}
  ],
  "house_rules": ["Check-in after 3:00 PM", "Checkout before 11:00 AM", "1 guest maximum"],
  "highlights": [
    {"title": "Self check-in", "subtitle": "Check yourself in with the keypad."}
  ],
  "rating_overall": 4.85,
  "review_count": 142,
  "ratings": [
    {"category": "CLEANLINESS", "value": "4.9"},
    {"category": "LOCATION", "value": "4.8"}
  ],
  "bedrooms": [
    {"title": "Bedroom 1", "subtitle": "1 king bed"}
  ]
}
```

Error handling: If `error: true` is returned with HTTP 4xx, verify the listing ID is valid by visiting `https://www.airbnb.com/rooms/{listing_id}` in the browser. If `No data in response` is returned, the listing may have been removed or the API schema may have changed — check the `raw` field for details.

## Pagination

Not applicable — each call returns complete detail for one listing.

## Success Criteria

`title is not null AND amenities.length >= 1 AND photos.length >= 1`

## Known Limitations

- `rating_overall` and `review_count` are null for new listings with no reviews
- `bedrooms` array may be empty for studio or hotel-style rooms
- Host personal details (bio, profile photo, response rate) are not available from this endpoint — they return as deferred sentinel sections
- Price per night is not included in the response without `--checkin` and `--checkout` dates
- Calling this endpoint too rapidly may trigger rate limiting; add 1-2 second delays between batch requests

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through listing IDs serially with a 1-second delay between calls
- **Test before batch execution**: After writing a batch script, test with 1-2 listing IDs to verify output before running full batch
- **Error resumption**: Save results per listing ID; resume from the breakpoint on failure

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/airbnb-scraper-airbnb-listing-detail.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what listing IDs were fetched or how many results were returned — those are task outputs, not experience.
