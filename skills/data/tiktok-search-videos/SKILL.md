---
name: tiktok-search-videos
description: "TikTok keyword search video scraper: input search keyword → output paginated video list with full metadata (author, engagement stats, music, video meta). Use when user mentions TikTok search scraping, search TikTok by keyword, TikTok search results, extract TikTok search data, scrape TikTok videos by keyword, TikTok keyword videos, TikTok keyword search, TikTok search results collection, find TikTok videos by topic, tiktok search scraper, tiktok keyword scraper. Also applies to market research on TikTok content for specific topics, competitor content monitoring, or discovering videos and creators around a keyword."
---

# TikTok — Search Videos

> search keyword → paginated video list with author, engagement, music, and video metadata

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract TikTok video search results for a given keyword using the `/api/search/item/full/` endpoint triggered by navigating to the search results page.

## Prerequisites

- Browser is open and can access `https://www.tiktok.com`
- **Login required**: TikTok blocks video search API for non-logged-in users; ensure the browser has an active TikTok session

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### Network Capture: Search video results (parameters injected via URL navigation)

`/api/search/item/full/` requires TikTok's dynamic signing; navigate to the search page to trigger it automatically:

1. `navigate https://www.tiktok.com/search/video?q={keyword}`
2. `wait stable`
3. `network requests --type xhr,fetch --filter "search/item/full"`
4. `network request <id>`

Endpoint characteristic: URL contains `/api/search/item/full/` with `keyword={keyword}&cursor=0`

Error handling: If no matching request appears after navigation, take a `screenshot` to verify the page loaded correctly (check for anti-bot challenge), then retry once.

Output example:
```json
{
  "status_code": 0,
  "cursor": "12",    // use to identify next-page requests
  "has_more": 1,     // 0 when all results exhausted
  "item_list": [
    {
      "id": "7212410220977392938",
      "desc": "Daily Push Up Workout🚀#fitness #athlete",
      "createTime": 1679270124,
      "isAd": false,
      "locationCreated": "US",
      "author": {
        "uniqueId": "marcusriosofficial",
        "nickname": "Marcus Rios",
        "verified": false,
        "signature": "Former NFL Athlete 🏈",
        "avatarThumb": "https://...",
        "privateAccount": false
      },
      "authorStats": {
        "followerCount": 423500,
        "followingCount": 50,
        "heart": 10000000,
        "videoCount": 1277,
        "diggCount": 869
      },
      "stats": {
        "diggCount": 367500,
        "shareCount": 6041,
        "playCount": 4500000,
        "commentCount": 942,
        "collectCount": 56691
      },
      "video": {
        "duration": 48,
        "height": 1280,
        "width": 720,
        "cover": "https://...",
        "definition": "720p",
        "format": "mp4"
      },
      "music": {
        "id": "7176546707423889410",
        "title": "Trap Money so Big (Remix)",
        "authorName": "Iqbal12",
        "original": false,
        "coverMedium": "https://..."
      },
      "textExtra": [{"hashtagId": "9261", "hashtagName": "fitness"}],
      "effectStickers": []
    }
  ]
}
```

To build the `webVideoUrl` for each item: `https://www.tiktok.com/@{item.author.uniqueId}/video/{item.id}`

### Network Capture: Search results pagination (page 2+)

After reading page 1, scroll down to load the next page:

1. `scroll down`
2. `wait stable`
3. `network requests --type xhr,fetch --filter "search/item/full"`
4. Find the request where the URL `cursor` value is higher than the previous page (e.g., `cursor=12`, `cursor=24`)
5. `network request <id>`

Termination: `has_more` is `0` in response, or `item_list` is empty.

## Pagination

**DOM Pagination**: Scroll triggers new `search/item/full` requests. Each page returns 12 items. Cursor increments by 12 per page. Termination: `has_more === 0` or empty `item_list`.

## Success Criteria

`item_list.length >= 1` and first item has non-null `id`, `stats.playCount`, `author.uniqueId`

## Known Limitations

- `search/item/full` requires dynamic signing — always use navigate + network capture
- **Login required**: TikTok blocks the video search API for non-logged-in users — `search/item/full` will not be triggered without an active TikTok session; exploration was done on a logged-in browser and this dependency was not caught at the time
- Search returns ~12 videos per page (fewer than hashtag's 30 per page)
- Logged-in users may see personalized results; use a fresh browser session for unbiased results
- `searchQuery` field is not returned in the raw API response body

## Execution Efficiency

- **Batch orchestration**: Loop multiple keywords serially in one session; add 2–3s between navigations.
- **Test before batch execution**: Test with 1 keyword first before running the full list.
- **Error resumption**: Save results keyword-by-keyword; resume from the failed keyword on error.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/tiktok-scraper-tiktok-search-videos.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations from past executions; adjust strategy accordingly.

**After execution**: If an unexpected situation occurs (strategy failed, page redesigned, anti-scraping upgraded), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file.
