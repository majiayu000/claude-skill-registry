---
name: tiktok-hashtag-videos
description: "TikTok hashtag video scraper: input a hashtag name → output paginated video list with full metadata (author profile, engagement stats, music, video meta, hashtag list). Use when user mentions TikTok hashtag scraping, TikTok tag videos, scrape TikTok by hashtag, extract TikTok hashtag data, TikTok challenge videos, get videos from a TikTok tag, bulk collect TikTok hashtag posts, TikTok video collection by tag, TikTok topic videos, collect TikTok tag data, batch fetch TikTok videos by hashtag, tiktok tag scraper, tiktok challenge scraper. Also applies to competitive research on TikTok trending topics, influencer discovery by hashtag, content monitoring for specific TikTok tags, or any task requiring video lists from a specific TikTok hashtag or challenge."
---

# TikTok — Hashtag Videos

> hashtag name → challenge info + paginated video list with author, engagement, music, and video metadata

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract the video list for a given TikTok hashtag using the `/api/challenge/item_list/` endpoint triggered by page navigation.

## Prerequisites

- Browser is open and can access `https://www.tiktok.com`
- No login required for public hashtag data
- Browser must use a non-HK proxy (TikTok has shut down in Hong Kong)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify.

### API: Get challenge ID from hashtag name

`eval "$(python scripts/get-challenge-id.py '{hashtag}')"`

Parameters:
- `{hashtag}`: hashtag name without `#`, e.g., `fitness`

Output example:
```json
{
  "id": "9261",             // challengeID — required for item_list requests
  "title": "fitness",       // canonical hashtag title
  "videoCount": "63107035", // total videos under this hashtag
  "viewCount": "760591731095" // total views
}
```

### Network Capture: Hashtag video list (parameters injected via URL navigation)

`/api/challenge/item_list/` requires TikTok's dynamic signing (X-Bogus/X-Gnarly); direct fetch returns empty. Navigate to the hashtag page — TikTok's JS triggers the signed request automatically:

1. `navigate https://www.tiktok.com/tag/{hashtag}`
2. `wait stable`
3. `network requests --type xhr,fetch --filter "challenge/item_list"`
4. `network request <id>`

Endpoint characteristic: URL contains `/api/challenge/item_list/` with `cursor=0`

Error handling: If no matching request is found after navigation, take a `screenshot` to confirm the page loaded correctly, then retry navigation once. If the page shows a region-restriction notice, switch to a browser with a non-HK proxy.

Output example:
```json
{
  "cursor": "30",   // use as cursor value to identify next page's request
  "hasMore": true,  // false when all pages exhausted
  "itemList": [
    {
      "id": "7212410220977392938",
      "desc": "Daily Push Up Workout🚀#fitness #athlete",
      "createTime": 1679270124,
      "isAd": false,
      "isPinned": false,
      "locationCreated": "US",
      "author": {
        "uniqueId": "marcusriosofficial",  // username for webVideoUrl
        "nickname": "Marcus Rios",
        "verified": false,
        "signature": "Former NFL Athlete 🏈",
        "bioLink": null,
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
      "effectStickers": [],
      "imagePost": null  // non-null for slideshow posts
    }
  ]
}
```

### Network Capture: Hashtag video list pagination (page 2+)

After reading page 1, scroll down to trigger the next page request:

1. `scroll down`
2. `wait stable`
3. `network requests --type xhr,fetch --filter "challenge/item_list"`
4. Find the request whose URL contains a `cursor` value higher than the previous page (e.g., `cursor=30`, `cursor=60`)
5. `network request <id>`

Termination: `hasMore` is `false` in response, or `itemList` is empty.

### Composite: Full hashtag extraction (challenge ID + paginated video list)

1. `eval "$(python scripts/get-challenge-id.py '{hashtag}')"` → record `id` as challengeId (confirms hashtag exists)
2. `navigate https://www.tiktok.com/tag/{hashtag}` → `wait stable`
3. `network requests --filter "challenge/item_list"` → `network request <id>` → collect `itemList`, note `cursor` and `hasMore`
4. While `hasMore` is `true`:
   a. `scroll down` → `wait stable`
   b. `network requests --filter "challenge/item_list"` → find new request (cursor changed) → `network request <id>`
   c. Collect `itemList`, update `hasMore`
5. Merge all collected `itemList` arrays

## Pagination

**DOM Pagination**: Scroll triggers new `challenge/item_list` requests. Each page returns 30 items. Cursor advances numerically (0 → 30 → 60...). Termination: `hasMore === false` or empty `itemList`.

## Success Criteria

`itemList.length >= 1` and first item has non-null `id`, `stats.playCount`, `author.uniqueId`

## Known Limitations

- Requires non-HK proxy (TikTok shut down in Hong Kong)
- `challenge/item_list` requires dynamic signing — always use navigate + network capture
- `get-challenge-id.py` (challenge/detail) works via direct fetch without signing
- Private or age-restricted hashtags may return empty `itemList`
- Page returns ~30 videos per scroll; high-volume extraction requires many scroll iterations

## Execution Efficiency

- **Batch orchestration**: Loop through multiple hashtags serially in one session; do not parallelize within one browser. Add 2–3s intervals between navigations.
- **Test before batch execution**: Test with 1 hashtag first, then run the full batch.
- **Error resumption**: Save results page-by-page; resume from the last successful page on failure.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/tiktok-scraper-tiktok-hashtag-videos.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations from past executions; adjust strategy accordingly.

**After execution**: If an unexpected situation occurs (strategy failed, page redesigned, anti-scraping upgraded, better path found), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file.
