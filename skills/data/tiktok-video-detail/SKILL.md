---
name: tiktok-video-detail
description: "TikTok single video detail scraper: input a TikTok video URL → output full video metadata (author profile, engagement stats, music, video meta, hashtags, mentions, slideshow images). Use when user mentions TikTok video detail, get TikTok video data, extract TikTok video metadata, scrape single TikTok video, TikTok video info, extract single TikTok video info, TikTok single video collection, tiktok video scraper, tiktok video url scraper. Also applies to batch URL processing (given a list of TikTok video URLs, extract metadata for each), verifying specific video stats, or archiving individual TikTok posts with full metadata."
---

# TikTok — Video Detail

> TikTok video URL → full video metadata

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract complete metadata for a specific TikTok video by reading the SSR-embedded `__UNIVERSAL_DATA_FOR_REHYDRATION__` data from the video detail page.

## Prerequisites

- Browser is open and can access `https://www.tiktok.com`
- No login required for public videos
- Browser must use a non-HK proxy (TikTok has shut down in Hong Kong)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### DOM: Extract video detail from SSR data

TikTok embeds full video metadata in a `<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__">` tag on every video detail page. No API call needed — data is available immediately after page load:

1. `navigate {video_url}` — e.g., `https://www.tiktok.com/@marcusriosofficial/video/7212410220977392938`
2. `wait stable`
3. `eval "$(python scripts/extract-video-detail.py)"`

Output example:
```json
{
  "id": "7212410220977392938",
  "text": "Daily Push Up Workout🚀#fitness #athlete #strength",
  "textLanguage": "en",
  "createTime": "1679270124",
  "createTimeISO": "2023-03-19T23:55:24.000Z",
  "isAd": false,
  "isPinned": false,
  "isSponsored": false,
  "isSlideshow": false,   // true for photo/slideshow posts
  "locationCreated": "US",
  "webVideoUrl": "https://www.tiktok.com/@marcusriosofficial/video/7212410220977392938",
  "mediaUrls": [],
  "authorMeta": {
    "id": "6803405475100181510",
    "name": "marcusriosofficial",       // uniqueId / username
    "nickName": "Marcus Rios",
    "profileUrl": "https://www.tiktok.com/@marcusriosofficial",
    "verified": false,
    "signature": "Former NFL Athlete 🏈\n📧marcusriosofficial@gmail.com",
    "bioLink": null,
    "avatar": "https://...",
    "privateAccount": false,
    "fans": 423500,
    "following": 50,
    "heart": 10000000,
    "video": 1277,
    "digg": 869
  },
  "musicMeta": {
    "musicId": "7176546707423889410",
    "musicName": "Trap Money so Big (Remix)",
    "musicAuthor": "Iqbal12",
    "musicOriginal": false,
    "coverMediumUrl": "https://..."
  },
  "videoMeta": {
    "height": 1280,
    "width": 720,
    "duration": 48,
    "coverUrl": "https://...",
    "definition": "720p",
    "format": "mp4"
  },
  "diggCount": 367500,
  "shareCount": 6041,
  "playCount": 4500000,
  "collectCount": 56691,
  "commentCount": 942,
  "hashtags": [
    {"id": "9261", "name": "fitness"},
    {"id": "39142", "name": "athlete"}
  ],
  "mentions": [],
  "effectStickers": [],
  "slideshowImageLinks": []  // populated for slideshow/photo posts
}
```

Error response (video deleted or unavailable):
```json
{"error": true, "message": "__UNIVERSAL_DATA_FOR_REHYDRATION__ not found — ensure you are on a TikTok video page"}
```

## Pagination

Not applicable — this capability extracts a single video per URL.

## Success Criteria

`id` is non-null, `diggCount >= 0`, `authorMeta.name` is non-null, `videoMeta.duration > 0`

## Known Limitations

- Requires non-HK proxy (TikTok shut down in Hong Kong)
- Deleted or private videos return an error (SSR data contains non-zero statusCode)
- `collectCount` may be returned as a string in the SSR data — parse with `parseInt()` if needed
- `authorMeta.heart` (total likes) may be truncated for very large accounts; `authorStats.heart` from the SSR itemStruct is the authoritative source
- Video download URLs (`playAddr`, `downloadAddr`) are present in the SSR data but expire quickly — extract and use them immediately if needed

## Execution Efficiency

- **Batch URL processing**: Write a bash loop to navigate to each video URL, eval the extraction script, and save results. Add 1–2s between navigations.
- **Test before batch execution**: Test with 1 URL first to confirm the script works, then run the full list.
- **Error resumption**: Save results URL-by-URL; resume from the failed URL on error.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/tiktok-scraper-tiktok-video-detail.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations from past executions; adjust strategy accordingly.

**After execution**: If an unexpected situation occurs (strategy failed, page redesigned, anti-scraping upgraded, better path found), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file.
