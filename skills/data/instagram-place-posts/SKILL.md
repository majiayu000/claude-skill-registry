---
name: instagram-place-posts
description: "Scrapes Instagram posts tagged at a specific location or place, returning media items with captions, like/comment counts, media URLs and user info. Use when user mentions Instagram location posts, posts from a place on Instagram, Instagram geotag scraping, posts tagged at location, Instagram place feed, get posts from a venue on Instagram, Instagram location data, posts near me Instagram, place-based Instagram content, tagged location posts."
---

# Instagram — Place Posts

> location name/ID → paginated list of posts tagged at that location

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Search for a location by name, then fetch posts tagged at that location using the internal locations sections API with cursor-based pagination.

## Prerequisites

- Browser is open on any Instagram page: `https://www.instagram.com/`
- Logged into Instagram (user avatar or username visible in top-right corner)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Instagram has been confirmed in the current session → skip this step.

Otherwise: open `https://www.instagram.com/` and observe the page login status:
- Logout/sign-out entry, user avatar, or username exists → logged in, continue execution
- Login/register entry exists with no logout entry → not logged in, inform the user that login is needed first, assist the user in completing the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### API: search for location ID

`eval "$(python scripts/search-location.py '{keyword}')"`

Parameters:
- keyword: Location name to search for (e.g., `New York`, `Eiffel Tower`, `Times Square`)

Output example:
```json
{
  "venues": [
    {
      "id": "212988663",
      "name": "New York, New York",
      "address": "New York, NY",
      "lat": 40.7128,
      "lng": -74.0059
    }
  ]
}
```

### API: get posts for a location

`eval "$(python scripts/get-place-posts.py '{location_id}' --tab ranked --max-id '{cursor}' --session-id '{session_id}')"`

Parameters:
- location_id: Numeric location ID (from search-location output)
- --tab: Feed type, `ranked` (top posts, default) or `recent` (chronological)
- --max-id: Pagination cursor; leave empty for first page, use `next_max_id` from previous response for subsequent pages
- --session-id: Session identifier for deduplication across pages; use a consistent value per scraping session (e.g., `session-001`)

Output example:
```json
{
  "items": [
    {
      "pk": "3904677093853259503",
      "code": "DYwMyEFumbv",
      "media_type": 2,
      "taken_at": 1779686199,
      "like_count": 1203,
      "comment_count": 48,
      "caption": "NYC skyline at sunset 🌆",
      "thumbnail_url": "https://scontent.cdninstagram.com/...",
      "video_url": "https://scontent.cdninstagram.com/...",
      "username": "nyc_photos",
      "user_id": "330873185",
      "location_name": "New York, New York"
    }
  ],
  "more_available": true,
  "next_max_id": "32120594f3584430b0d3a4e72372c376"
}
```

### Composite: fetch all posts for a location by name

1. `navigate https://www.instagram.com/` → `wait stable`
2. `eval "$(python scripts/search-location.py '{location_name}')"` → select the best-matching venue, extract its `id` as `location_id`
3. `eval "$(python scripts/get-place-posts.py '{location_id}' --session-id 'session-001')"` → collect `items`, note `more_available` and `next_max_id`
4. While `more_available` is `true`:
   a. `eval "$(python scripts/get-place-posts.py '{location_id}' --max-id '{next_max_id}' --session-id 'session-001')"` → accumulate `items`
5. Merge all collected items

## Pagination

**API Pagination**: `max_id`, type: cursor, start value: empty string. Next page value source: `next_max_id` field in response. Termination: `more_available` is `false` or `next_max_id` is null. Keep `session_id` consistent across all pages for the same scraping session.

## Success Criteria

`result count >= 1 AND items[0].pk non-null AND items[0].location_name non-null`

## Known Limitations

- Login required: location sections API requires authentication (CSRF token from logged-in session)
- Location search may return multiple venues with similar names; select the best match by name and address
- Posts count per page varies (approximately 30 posts) depending on media type distribution in sections

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/instagram-scraper-instagram-place-posts.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
