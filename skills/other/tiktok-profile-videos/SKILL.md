---
name: tiktok-profile-videos
description: "TikTok user profile video scraper: input a TikTok username → output the user's profile info plus paginated video list with full metadata (engagement stats, music, video meta). Use when user mentions TikTok profile scraping, scrape TikTok user videos, get TikTok creator videos, extract TikTok profile data, TikTok user posts, TikTok account video collection, collect TikTok profile page videos, TikTok creator video list, TikTok creator data, TikTok profile scraper, tiktok user scraper, tiktok creator scraper. Also applies to influencer research, competitor analysis, content archiving for a specific TikTok creator, or extracting all posts from a TikTok account."
---

# TikTok — Profile Videos

> TikTok username → user profile info + paginated video list with full metadata

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract the video list and profile metadata for a given TikTok user using the `/api/post/item_list/` endpoint triggered by navigating to their profile page.

## Prerequisites

- Browser is open and can access `https://www.tiktok.com`
- No login required for public profiles
- Browser must use a non-HK proxy (TikTok has shut down in Hong Kong)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### Network Capture: Profile video list (parameters injected via URL navigation)

`/api/post/item_list/` requires TikTok's dynamic signing and the user's `secUid` (internal ID). Navigate to the profile page — TikTok's JS resolves the secUid and triggers the signed request automatically:

1. `navigate https://www.tiktok.com/@{username}`
2. `wait stable`
3. `network requests --type xhr,fetch --filter "post/item_list"`
4. `network request <id>`

Endpoint characteristic: URL contains `/api/post/item_list/` with `secUid={secUid}&cursor=0`

Note: The `secUid` is a long internal identifier (e.g., `MS4wLjABAAAA-VASjiXTh7wDDyXvjk10VFhMWUAoxr8bgfO1kAL1-9s`) visible in the captured request URL — record it for pagination requests.

Error handling: If no matching request appears, verify the profile page loaded (`screenshot`). Private accounts return an empty `itemList`. If the page shows a region block, switch to a non-HK proxy browser.

Output example:
```json
{
  "cursor": "1778468677570", // timestamp-based cursor for next page
  "hasMore": true,           // false when all videos loaded
  "itemList": [
    {
      "id": "7212410220977392938",
      "desc": "Daily Push Up Workout🚀#fitness",
      "createTime": 1679270124,
      "isAd": false,
      "isPinned": false,
      "isSponsored": false,
      "locationCreated": "US",
      "author": {
        "id": "6803405475100181510",
        "uniqueId": "marcusriosofficial",
        "nickname": "Marcus Rios",
        "verified": false,
        "signature": "Former NFL Athlete 🏈\n📧marcusriosofficial@gmail.com",
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
      "authorStatsV2": {
        "followerCount": "423500",
        "followingCount": "50",
        "heart": "10000000",
        "videoCount": "1277"
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
      "imagePost": null
    }
  ]
}
```

To build the `webVideoUrl` for each item: `https://www.tiktok.com/@{item.author.uniqueId}/video/{item.id}`

Profile info is available from the first item's `author` and `authorStats` fields: followerCount, following, heart total, video count, bio, verified status.

### Network Capture: Profile video list pagination (page 2+)

After reading page 1, scroll down to load more videos:

1. `scroll down`
2. `wait stable`
3. `network requests --type xhr,fetch --filter "post/item_list"`
4. Find the new request (cursor value changed from the previous page's cursor)
5. `network request <id>`

Termination: `hasMore` is `false` in response, or `itemList` is empty.

## Pagination

**DOM Pagination**: Scroll triggers new `post/item_list` requests with timestamp-based cursor. Each page returns 16 items. Termination: `hasMore === false` or empty `itemList`.

## Success Criteria

`itemList.length >= 1` and first item has non-null `id`, `stats.playCount`, `author.uniqueId`, `authorStats.followerCount`

## Known Limitations

- Requires non-HK proxy (TikTok shut down in Hong Kong)
- `post/item_list` requires dynamic signing + secUid resolved by TikTok's JS — always use navigate + network capture
- Private accounts return empty `itemList`
- `authorStats.heartCount` may overflow to negative for accounts with very high like counts — use `authorStats.heart` instead
- `followers/following` lists are not available via this capability (separate scraper needed, requires login)

## Execution Efficiency

- **Batch orchestration**: Loop through multiple usernames serially in one session; add 2–3s between profile navigations.
- **Test before batch execution**: Test with 1 username first before running the full list.
- **Error resumption**: Save results profile-by-profile; resume from the failed username on error.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/tiktok-scraper-tiktok-profile-videos.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations from past executions; adjust strategy accordingly.

**After execution**: If an unexpected situation occurs (strategy failed, page redesigned, anti-scraping upgraded), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file.
