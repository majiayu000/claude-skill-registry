---
name: x-tweet-search
description: "Scrapes tweets from X (Twitter) by search query, user handle, or direct URL — returns full tweet data including text, author info, engagement metrics, media, and hashtags. Use when user mentions X, Twitter, tweet scraping, scrape tweets, get tweets, fetch tweets, twitter data, x.com data, tweet collector, tweet search, twitter search, social media scraping, twitter handle scraping, scrape user tweets, from:username, twitter keyword search, hashtag search, twitter timeline, twitter list scraping, collect twitter posts, export tweets, tweet analysis, twitter monitoring, search twitter, get twitter data, twitter api alternative, tweet dump."
---

# X (Twitter) — Tweet Search & Scraper

> Search query / handle / URL → structured tweet list (text, author, metrics, media, entities)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Collect tweets matching a search query, from specific user profiles, or from direct URLs, extracting complete structured data for each tweet.

## Prerequisites

- Target page is already open in the browser: `https://x.com/search?q=...` or `https://x.com/{handle}` or a direct tweet/list URL
- User must be logged in to X (user avatar or username visible in left sidebar)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for X has been confirmed in the current session → skip this step.

Otherwise: open `https://x.com` and observe the left sidebar:
- User avatar or "@username" visible at the bottom → logged in, continue
- "Sign in" or "Log in" button visible → not logged in, inform user that X login is required and assist with the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It reads tweet data already rendered in the X DOM, never bypassing authentication. JS is encapsulated in `scripts/` files, invoked via `eval "$(python scripts/xxx.py)"`. Use the bash tool for execution.

### DOM: Tweet list extraction (React Fiber)

Extracts all currently visible tweets from the page via React internal state (React Fiber). Works on search pages, profile pages, list pages, and any X page rendering tweet articles.

Wait for tweets to appear before extracting:
```
wait --selector "article[data-testid='tweet']" --state attached --timeout 15000
```

Extract: `eval "$(python scripts/extract-tweets.py)"`

Returns a JSON array. Each element:

```json
[
  {
    "id": "2059255862548738182",          // tweet ID
    "url": "https://x.com/NASA/status/2059255862548738182",  // direct link
    "text": "Full tweet text including hashtags and URLs",   // full_text field
    "created_at": "2026-05-26T12:50:31.000Z",               // ISO 8601
    "lang": "en",                         // ISO 639-1 language code, null if unknown
    "author_id": "11348282",              // author user ID
    "author_name": "NASA",                // display name
    "author_screen_name": "NASA",         // @handle (without @)
    "author_profile_image": "https://pbs.twimg.com/profile_images/.../photo.jpg",
    "author_followers": 92080161,         // follower count
    "author_following": 305,              // following count
    "author_verified": false,             // legacy blue checkmark
    "author_blue_verified": true,         // X Blue / Gold / Gray checkmark
    "author_location": "Washington, D.C.", // profile location, null if not set
    "author_description": "Explore the universe...",  // bio, null if empty
    "like_count": 82579,
    "retweet_count": 11952,
    "reply_count": 4230,
    "quote_count": 1850,
    "bookmark_count": 12400,
    "view_count": 25923006,               // null if not available
    "is_retweet": false,
    "is_quote": false,
    "is_reply": false,
    "in_reply_to_tweet_id": null,         // parent tweet ID if is_reply=true
    "in_reply_to_user": null,             // @handle of replied-to user
    "conversation_id": "2059255862548738182",
    "hashtags": ["AI", "Space"],          // without #
    "urls": ["https://example.com/article"],  // expanded URLs from entities
    "mentions": ["SpaceX", "ESA"],        // @handles without @
    "media": [
      {
        "type": "video",                  // "photo", "video", "animated_gif"
        "url": "https://pbs.twimg.com/amplify_video_thumb/.../img/thumb.jpg",
        "alt_text": null,
        "video_variants": [
          {"bitrate": 2176000, "url": "https://video.twimg.com/.../1280x720/video.mp4"},
          {"bitrate": 832000,  "url": "https://video.twimg.com/.../640x360/video.mp4"}
        ]
      }
    ],
    "source_name": "Twitter for iPhone",  // client used to post
    "source_url": "http://twitter.com/download/iphone"
  }
]
```

## URL Construction Guide

### Input type → URL mapping

**searchTerms** (keyword / advanced query):
- Sort Latest: `https://x.com/search?q={url_encoded_query}&src=typed_query&f=live`
- Sort Top: `https://x.com/search?q={url_encoded_query}&src=typed_query`
- Sort Latest+Top: run both URLs in sequence, deduplicate by tweet ID

**twitterHandles** (scrape a user's profile tweets):
- Option A (profile page): `https://x.com/{handle}` — shows all tweets/retweets
- Option B (search): use `from:{handle}` as the search query — more filter-compatible

**startUrls** (direct URLs): navigate to the URL as-is. Supported types:
- Tweet URL: `https://x.com/{user}/status/{id}` — single tweet conversation
- Profile URL: `https://x.com/{handle}` — profile timeline
- Search URL: `https://x.com/search?q=...` — use directly
- List URL: `https://x.com/i/lists/{list_id}` — list timeline

### Filter parameters → query operators

Append these operators to the base query string (space-separated):

| Parameter | Query operator | Example |
|-----------|---------------|---------|
| `tweetLanguage` | `lang:{code}` | `lang:en` |
| `onlyVerifiedUsers` | `filter:verified` | |
| `onlyTwitterBlue` | `filter:blue_verified` | |
| `onlyImage` | `filter:images` | |
| `onlyVideo` | `filter:videos` | |
| `onlyQuote` | `filter:quote` | |
| `author` | `from:{handle}` | `from:NASA` |
| `inReplyTo` | `to:{handle}` | `to:NASA` |
| `mentioning` | `@{handle}` | `@NASA` |
| `minimumRetweets` | `min_retweets:{n}` | `min_retweets:100` |
| `minimumFavorites` | `min_faves:{n}` | `min_faves:500` |
| `minimumReplies` | `min_replies:{n}` | `min_replies:10` |
| `start` | `since:{YYYY-MM-DD}` | `since:2024-01-01` |
| `end` | `until:{YYYY-MM-DD}` | `until:2024-06-01` |
| `geotaggedNear` + `withinRadius` | `near:"{location}" within:{radius}` | `near:"New York" within:15mi` |
| `geocode` | `geocode:{lat},{lon},{radius}` | `geocode:40.7,-74.0,10km` |
| `-filter:retweets` | exclude retweets | |

**Example**: Scrape English tweets from NASA since 2024 with ≥100 likes, excluding retweets:
```
query = "from:NASA lang:en since:2024-01-01 min_faves:100 -filter:retweets"
url = "https://x.com/search?q=" + encodeURIComponent(query) + "&src=typed_query&f=live"
```

## Pagination

**DOM Pagination** (scroll to load more):

X dynamically appends new tweet articles to the DOM as the user scrolls. Tweets already rendered remain in the DOM (no virtualization for typical result sets < ~500 tweets).

Loop pattern:
1. Record current tweet count: extract → note `len(results)`
2. `scroll down --amount 2000`
3. `wait stable`
4. Extract again → compare IDs, add new ones to collection
5. Termination conditions:
   - New extraction returns 0 new tweet IDs (end of results reached)
   - `collected >= max_items` (if limit specified)
   - Same tweet IDs returned 3 consecutive times (no more data loading)

Deduplication: track seen IDs in a Python set, filter before appending to output.

## Success Criteria

`result count >= 1` and `id field non-null rate = 100%` and `text field non-null rate = 100%`

## Known Limitations

- **React Fiber key**: The `__reactFiber` prefix includes a session-specific hash (e.g., `__reactFiber$ozawbbp0gp`). The script uses `startsWith('__reactFiber')` which is stable across deployments; only fails if React is replaced with a different framework.
- **DOM virtualization**: For very large result sets (500+ tweets), X may virtualize older DOM nodes to reclaim memory. If extraction suddenly returns fewer tweets than expected after extended scrolling, the remaining tweets may have been removed from DOM. Mitigation: save results incrementally after each scroll batch.
- **View count**: `view_count` is null for older tweets, low-engagement tweets, or when X doesn't expose it. This is a data availability issue, not an extraction failure.
- **List URL**: Requires a valid, accessible public list ID. Private lists return no tweets.
- **`filter:blue_verified`**: Whether X's search engine respects this operator may vary; verify results if blue-verified filtering is critical.
- **`customMapFunction`**: Not applicable — this is a source-platform-specific JS transform parameter, not a data filter relevant to browser extraction.
- **Rate limiting**: X may temporarily stop loading new tweets after aggressive scrolling. Add 1–2s delays between scroll batches for large collections.

## Execution Efficiency

- **Batch orchestration**: For multiple search queries or handles, process them serially in one browser session with short delays (1–2s) between navigations. Do not open parallel searches in the same browser — use separate sessions for parallel work.
- **Test before batch execution**: Test with 1 query first, verify 10+ tweets extract correctly, then run the full batch.
- **Reduce redundant pre-operations**: Login check only needed once per session; skip on subsequent queries.
- **Error resumption**: Save results to a file after each URL/query. On failure, resume from the last saved query rather than restarting from scratch.
- **Incremental save**: After each scroll batch, append new tweets to the output file rather than holding everything in memory.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/x-tweet-scraper-x-tweet-search.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
