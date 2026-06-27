---
name: google-maps-contact-extract
description: "Extracts business contact details from Google Maps search results and place detail pages, then visits each business website to collect emails, phone numbers, and social media profiles (Facebook, Instagram, Twitter/X, LinkedIn, YouTube, TikTok, Pinterest, Discord). Use when user mentions Google Maps contact extraction, maps email scraper, business lead generation from Google Maps, find emails from maps, scrape Google Maps businesses, maps business contacts, get phone from Google Maps, social media from maps listing, competitor research from maps, local business contact list, maps data export, google maps scraper, extract contacts from google maps, find business email google, gmaps leads, maps email finder, or wants to replicate Google Maps business data extraction."
---

# Google Maps — Contact Extractor

> keyword + location → business list with name/address/phone/website + email/social media/contacts from each business's website

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Search Google Maps by keyword and location, collect place details from each result, visit each business's website to extract emails and social media profiles, and return a merged dataset replicating Google Maps Email Extractor functionality.

## Prerequisites

- For search: navigate to `https://www.google.com/maps/search/{keyword}/@{lat},{lng},{zoom}z` — the search results sidebar (feed) must be visible
- For place detail: navigate to the individual place URL `https://www.google.com/maps/place/?q=place_id:{place_id}` — the place sidebar with name, address, phone must be visible
- For website contact extraction: navigate to the business's website homepage
- No login required for Google Maps or most business websites

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. It is recommended to use the bash tool for execution. **Working directory**: all `python scripts/` commands must be run from the Skill's root directory (the directory containing `SKILL.md` and `scripts/`). Use `cd {skill-directory}` before running batch scripts, or use absolute paths: `python {absolute-path-to-scripts}/xxx.py`.

### DOM: Search results list — extract business cards from Google Maps search feed

Prerequisite: navigate to and wait for Google Maps search results to load, then extract all visible business cards.

```
navigate https://www.google.com/maps/search/{keyword}/@{lat},{lng},{zoom}z
wait stable
eval "$(python scripts/search-places.py '{keyword}' --max {max_count})"
```

Parameters:
- `{keyword}`: search term, e.g. `coffee shops`
- `--max`: maximum number of places to extract, default `20`
- `{lat},{lng}`: center coordinates, e.g. `40.7580,-73.9855`
- `{zoom}`: zoom level, e.g. `14`

Output example:
```json
{
  "keyword": "coffee shops",
  "count": 20,
  "places": [
    {
      "name": "Blue Dove Coffee",
      "rating": 4.8,
      "review_count": "292",
      "category": "Coffee shop",
      "price_range": null,
      "phone": null,
      "open_status": "Closed · Opens 7 AM",
      "place_id": "0xa5922b78cc420fb1:0x535506dc9cdb2cec",
      "lat": 40.7368708,
      "lng": -73.9909297,
      "maps_url": "https://www.google.com/maps/place/Blue+Dove+Coffee/data=..."
    }
  ]
}
```

Pagination: Google Maps loads ~20 results per view. Scroll down in the results panel to trigger loading of additional results, then re-run the extraction script. Repeat until desired count is reached.

```
scroll down --amount 3000
wait stable
eval "$(python scripts/search-places.py '{keyword}' --max {total_count})"
```

### DOM: Place detail — extract full business info from a Google Maps place page

Prerequisite: navigate to the place page and wait for the sidebar to load with name, address, and phone visible.

```
navigate https://www.google.com/maps/place/?q=place_id:{place_id}
wait stable
wait --selector "h1" --state visible --timeout 15000
eval "$(python scripts/place-detail.py)"
```

Alternatively, navigate directly using the `maps_url` returned from the search results component.

Output example:
```json
{
  "place_id": "0xa5922b78cc420fb1:0x535506dc9cdb2cec",
  "name": "Blue Dove Coffee",
  "rating": 4.8,
  "review_count": 292,
  "category": "Coffee shop",
  "address": "33 Union Square W, New York, NY 10003",
  "located_in": null,
  "phone": "(646) 939-0937",
  "website": "https://www.bluedovecoffee.com/",
  "menu_url": "https://order.dripos.com/Blue-Dove-Coffee",
  "price_range": "$1–10",
  "coordinates": { "lat": 40.7368708, "lng": -73.9909297 },
  "hours": [
    "Monday7 AM–5 PM",
    "Tuesday7 AM–5 PM",
    "Wednesday7 AM–5 PM",
    "Thursday7 AM–5 PM",
    "Friday7 AM–5 PM",
    "Saturday7 AM–5 PM",
    "Sunday7 AM–4 PM"
  ],
  "service_options": ["Serves dine-in", "Offers takeout", "Offers delivery"],
  "amenities": ["Has wheelchair accessible entrance", "Accepts credit cards", "Accepts NFC mobile payments"],
  "maps_url": "https://www.google.com/maps/place/..."
}
```

### DOM: Website contacts — extract emails, phones, social media from a business website

Prerequisite: navigate to the business website homepage.

```
navigate {website_url}
wait stable
eval "$(python scripts/extract-contacts.py --depth shallow)"
```

For deeper extraction (also scans contact/about subpages), use `--depth deep`. After running with `--depth deep`, check `contact_subpages` in the output, then navigate to each and re-run:

```
navigate {subpage_url}
wait stable
eval "$(python scripts/extract-contacts.py --depth shallow)"
```

Parameters:
- `--depth`: `shallow` (homepage only, default) or `deep` (also discovers and lists contact/about subpage URLs)

Output example:
```json
{
  "source_url": "https://www.bluedovecoffee.com/",
  "emails": ["support@bluedovecoffee.com", "careers@bluedovecoffee.com", "orders@bluedovecoffee.com"],
  "phone_numbers": [],
  "social_media": {
    "facebook": ["https://www.facebook.com/people/Blue-Dove-Coffee/100094867009022"],
    "instagram": ["https://www.instagram.com/bluedovecoffee"],
    "tiktok": ["https://www.tiktok.com/@bluedovecoffee"]
  },
  "contact_subpages": []
}
```

### Composite: Full pipeline — search + place details + website contacts

Complete flow replicating Google Maps Email Extractor:

1. Navigate to Google Maps search:
   ```
   navigate https://www.google.com/maps/search/{keyword}/@{lat},{lng},{zoom}z
   wait stable
   eval "$(python scripts/search-places.py '{keyword}' --max {max_count})"
   ```
   Save list of places (especially `name`, `maps_url`, `place_id`).

2. For each place: navigate to place detail page and extract full info:
   ```
   navigate {maps_url}
   wait stable
   wait --selector "h1" --state visible --timeout 15000
   eval "$(python scripts/place-detail.py)"
   ```
   Collect `website`, `phone`, `address`, `hours`, `rating`, etc.

3. For each place with a `website` value: extract contacts from the website:
   ```
   navigate {website}
   wait stable
   eval "$(python scripts/extract-contacts.py --depth deep)"
   ```
   For each URL in `contact_subpages`, navigate and extract again to find additional emails.

4. Merge results: join by `place_id` or `name`. Final record per business:
   ```json
   {
     "name": "Blue Dove Coffee",
     "address": "33 Union Square W, New York, NY 10003",
     "phone": "(646) 939-0937",
     "website": "https://www.bluedovecoffee.com/",
     "rating": 4.8,
     "review_count": 292,
     "category": "Coffee shop",
     "coordinates": { "lat": 40.7368708, "lng": -73.9909297 },
     "hours": ["Monday7 AM–5 PM", "..."],
     "service_options": ["Serves dine-in", "Offers takeout"],
     "emails": ["support@bluedovecoffee.com"],
     "social_media": {
       "instagram": ["https://www.instagram.com/bluedovecoffee"],
       "tiktok": ["https://www.tiktok.com/@bluedovecoffee"]
     }
   }
   ```

## Pagination

**DOM Pagination**: Google Maps search loads ~20 results initially. Scroll down in the sidebar:
```
scroll down --amount 3000
wait stable
eval "$(python scripts/search-places.py '{keyword}' --max {total_count})"
```
Repeat until the desired number of results is reached. Termination: Google Maps typically shows up to ~120 results per search; the sidebar will show "You've reached the end of the results" or stop loading new items.

## Success Criteria

- `places.count >= 1` from search results extraction
- Place detail returns `name != null AND (address != null OR phone != null)`
- Website contact extraction returns `emails.length + phone_numbers.length + Object.keys(social_media).length >= 0` (no contacts = valid result for businesses without public contact info)

## Known Limitations

- Google Maps search results are limited to approximately 120 businesses per search query; to get more, use more specific sub-area searches
- Phone numbers on the Google Maps search list card are not always shown; `place-detail.py` on the individual place page is more reliable
- Website contact extraction depends on the business's website structure; sites using image-based emails or obfuscated text will return no emails
- Some businesses do not have a website listed on Google Maps; those cannot be enriched with contact data
- Google Maps may throttle requests if too many place pages are navigated in rapid succession; add 1–2 second delays between place navigations in batch scripts

## Execution Efficiency

- **Batch orchestration**: Write a bash script that loops through the pipeline steps in a single session. Add a 1–2 second sleep between each place detail navigation to avoid triggering anti-scraping. Example:
  ```bash
  for place_url in "${place_urls[@]}"; do
    browser-act --session gmaps-s1 navigate "$place_url"
    browser-act --session gmaps-s1 wait stable
    browser-act --session gmaps-s1 eval "$(python scripts/place-detail.py)"
    sleep 1.5
  done
  ```
- **Test before batch execution**: Test with 2–3 places before running the full batch
- **Error resumption**: Save each place's result to a JSON file immediately after extraction; on failure, skip already-saved places by checking if the file exists
- **Multiple sessions for throughput**: Open 2–3 parallel stealth browser sessions and distribute places across them; each session has an independent fingerprint

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/google-maps-contact-extract.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file.
