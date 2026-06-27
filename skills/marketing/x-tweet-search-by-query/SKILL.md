---
name: x-tweet-search-by-query
description: "Searches X (Twitter) for tweets by free-form advanced query and returns a normalized tweet list with text, author profile, engagement counts, media, hashtags, mentions, and cursor for pagination. Use when user mentions X search, Twitter search, scrape tweets by keyword, search X by hashtag, search Twitter by hashtag, find tweets about a topic, search tweets by date range, since until search Twitter, advanced Twitter search, tweets with media, tweets with images, tweets with video, top tweets, latest tweets, X latest tab, X top tab, min_faves, min_retweets, min_replies, filter verified Twitter, filter blue verified, from user Twitter, to user Twitter, mentioning user Twitter, geocode Twitter search, near location Twitter, lang code search Twitter, exclude retweets, exclude replies, collect tweets at scale, bulk tweets export, monitor brand mentions on X, monitor brand mentions on Twitter, competitor mention monitoring, KOL tweet harvesting, twitter keyword scraper, tweet keyword scraper, search X by keyword, search twitter, search x.com, x.com search, twitter advanced search, x advanced search, tweet collection by query, scrape twitter search results. Also applies to time-bounded research, sentiment analysis input gathering, hashtag campaign tracking, geo-targeted tweet collection, and any paginated bulk tweet collection driven by a search query."
---

# X — Tweet Search by Query

> Advanced search query → normalized list of tweets matching the query (with author, engagement, media, cursor).

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Collect tweets that match an X advanced-search query expression, returning structured per-tweet data and pagination cursors for unbounded bulk collection.

## Prerequisites

- Active X session in the browser (left sidebar shows logged-in avatar / @handle).
- Network capture is enabled in the browser-act session.

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for X has been confirmed in the current session → skip this step.

Otherwise: open `https://x.com` and observe the left sidebar:
- User avatar or @handle visible at the bottom → logged in, continue
- "Sign in" / "Log in" prompt visible → not logged in, inform the user that an X login is required and assist the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads tweet data rendered by the user's own X session, never bypassing authentication. Each search request is signed by X's own page JS; the Skill triggers it via URL navigation and reads structured GraphQL responses from network traffic. Python scripts under `scripts/` only build URLs and parse responses — they do not call X directly. Run them through the bash tool.

### Network Capture: search tweets via advanced query

All search parameters are encoded into X's native advanced search syntax via the URL builder, then injected through the page URL. The browser's own JS signs the GraphQL request; the response is read from network traffic and parsed locally.

Step 1 — build the search URL with all desired filters:

`URL=$(python scripts/build-search-url.py '{raw_query}' --sort {sort} [--language {iso}] [--min-retweets {n}] [--min-faves {n}] [--min-replies {n}] [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--author {handle}] [--in-reply-to {handle}] [--mentioning {handle}] [--only-verified] [--only-blue-verified] [--only-image] [--only-video] [--only-quote] [--exclude-retweets] [--exclude-replies] [--geocode LAT,LON,RADIUSmi] [--near 'PLACE'] [--within 15mi])`

Parameters:
- `raw_query` (positional): free-form X advanced search expression; all standard operators are supported and may already include any clause below. Operators added via flags are skipped if the same operator is already present in `raw_query`.
- `--sort`: `Latest` (default) or `Top`. Maps to URL `f=live` and `f=top`, which select GraphQL `product=Latest` vs `product=Top`.
- `--language`: ISO 639-1 code, appended as `lang:CODE`.
- `--min-retweets` / `--min-faves` / `--min-replies`: integer thresholds, appended as `min_retweets:N` / `min_faves:N` / `min_replies:N`.
- `--since` / `--until`: `YYYY-MM-DD`, appended as `since:` / `until:`.
- `--author`: only tweets from this handle, appended as `from:HANDLE`.
- `--in-reply-to`: only tweets replying to this handle, appended as `to:HANDLE`.
- `--mentioning`: only tweets mentioning this handle, appended as `@HANDLE`.
- `--only-verified` / `--only-blue-verified`: appended as `filter:verified` / `filter:blue_verified`.
- `--only-image` / `--only-video` / `--only-quote`: appended as `filter:images` / `filter:native_video` / `filter:quote`.
- `--exclude-retweets` / `--exclude-replies`: appended as `-filter:retweets` / `-filter:replies`.
- `--geocode`: `LAT,LON,RADIUSmi` or `LAT,LON,RADIUSkm`, appended as `geocode:LAT,LON,RADIUS`.
- `--near` / `--within`: appended as `near:"PLACE"` and `within:VALUE`.

Step 2 — navigate and capture the first page:

1. `network requests --clear`
2. `navigate "$URL"`
3. `wait stable --timeout 25000` (a timeout is normal on X; proceed even if it fires — the GraphQL response usually completes before the page reaches network-idle)
4. `network requests --type xhr,fetch --filter SearchTimeline` → take the latest entry's `request_id`
5. `network request <request_id>` → save full output to a file (e.g. `tmp/x-search-page-1.txt`)
6. `python scripts/parse-tweets.py --json-file tmp/x-search-page-1.txt --source search` → emits JSON `{tweets, count, cursor_top, cursor_bottom}`

Endpoint characteristic: URL contains `/i/api/graphql/<hash>/SearchTimeline`. The query hash rotates over time, so always filter by name `SearchTimeline`, never by hash.

Step 3 — paginate via scroll until the desired tweet count is reached or `cursor_bottom` no longer advances:

1. `network requests --clear`
2. `scroll down --amount 5000`
3. `wait stable --timeout 10000`
4. `network requests --type xhr,fetch --filter SearchTimeline` → take the newest entry's `request_id` (its variables now carry the cursor returned by the previous page)
5. `network request <request_id>` → save to `tmp/x-search-page-N.txt`
6. `python scripts/parse-tweets.py --json-file tmp/x-search-page-N.txt --source search`

Repeat Step 3 until any of these termination conditions is met:
- The accumulated unique tweet count reaches the user's target `max_items`.
- `count` returns `0` for the current page.
- `cursor_bottom` is identical to the previous page (the timeline has been fully consumed).

Error handling: if `network requests --filter SearchTimeline` returns no entry after a scroll, the request may have been throttled or the timeline may have ended — wait 3 s and retry the scroll once. If still no new request appears after the second attempt and `cursor_bottom` did not change, stop the loop. If the response file's body is missing (only headers present), the URL is likely stale — re-`navigate` to the same URL and retry.

Output example:
```json
{
  "tweets": [
    {
      "type": "tweet",
      "id": "2068333045510291908",
      "url": "https://x.com/NASA/status/2068333045510291908",
      "twitter_url": "https://twitter.com/NASA/status/2068333045510291908",
      "text": "The official FIFA World Cup ball went to space! ...",
      "created_at": "Thu Jun 20 18:30:11 +0000 2026",
      "lang": "en",
      "source": "Twitter Web App",
      "retweet_count": 4586,
      "reply_count": 1812,
      "like_count": 24499,
      "quote_count": 240,
      "bookmark_count": 1730,
      "view_count": 2098235,
      "is_reply": false,
      "is_retweet": false,
      "is_quote": false,
      "quote_id": null,
      "quote_url": null,
      "in_reply_to_id": null,
      "in_reply_to_user": null,
      "in_reply_to_user_id": null,
      "conversation_id": "2068333045510291908",
      "hashtags": ["FIFAWorldCup"],
      "mentions": [],
      "urls": [],
      "media": [
        {
          "type": "photo",
          "url": "https://pbs.twimg.com/media/abcd.jpg",
          "expanded_url": "https://x.com/NASA/status/2068333045510291908/photo/1",
          "alt_text": null
        }
      ],
      "card": null,
      "place": null,
      "author": {
        "id": "11348282",
        "user_name": "NASA",
        "name": "NASA",
        "url": "https://x.com/NASA",
        "is_verified": false,
        "is_blue_verified": true,
        "verified_type": "Government",
        "profile_picture": "https://pbs.twimg.com/profile_images/.../photo.jpg",
        "description": "Explore the universe ...",
        "location": "Pale Blue Dot",
        "followers": 92137231,
        "following": 305,
        "created_at": "Wed Dec 19 20:20:32 +0000 2007"
      }
    }
  ],
  "count": 20,
  "cursor_top": "DAADDAABCgABHLoyRYoXoV4...",
  "cursor_bottom": "DAADDAABCgABHLoyRYoXoV4..."
}
```

## Pagination

**Network Capture Pagination**: triggered by `scroll down`. X's page JS inserts the previous response's `cursor_bottom` into the next `SearchTimeline` request's `variables.cursor` automatically. The Skill reads each new GraphQL response from network and merges tweets. Termination: `count == 0`, or `cursor_bottom` does not advance across two consecutive pages, or the user's `max_items` is reached.

## Success Criteria

`count >= 1 on the first page` AND `every tweet has non-null id, text, created_at, author.user_name, like_count, retweet_count, reply_count` AND `each subsequent page's cursor_bottom differs from the previous page's until termination`.

## Known Limitations

- The X advanced search index only surfaces public tweets; protected accounts are excluded regardless of filters.
- `view_count` is `null` for very new or low-traffic tweets where X has not yet emitted `views.count`; only `views.state == "EnabledWithCount"` entries carry a number.
- X applies aggressive rate limits on search; sustained polling at high concurrency triggers throttling. Stay under ~150 SearchTimeline calls per 15-minute window per session (the `x-rate-limit-remaining` response header reveals the live budget).
- `SearchTimeline` query hashes rotate; always discover requests by name (`--filter SearchTimeline`), never by hash.
- The page may never reach `network-idle`, so `wait stable` will frequently time out; this is expected — proceed to read network traffic anyway.
- Account-permission gates (NSFW filter on/off, blocked-user lists, locked region) carry over into search results and cannot be bypassed.

## Execution Efficiency

- **Batch orchestration**: write a bash script that iterates queries serially in one session. Within a single search, paginate one page at a time. To parallelize across queries, open multiple stealth browser sessions, each logged in and rate-limited independently.
- **Test before batch execution**: run one query end-to-end (page 1 + page 2) before kicking off the full batch.
- **Reduce redundant pre-operations**: keep the same browser session for many sequential searches — `navigate` reuses the existing X SPA without reload.
- **Error resumption**: persist `cursor_bottom` and the accumulated unique tweet IDs to disk after every page so a crash mid-batch can resume from the last good cursor.
- **De-duplicate by `id`**: when running with `--sort "Latest + Top"`, the two passes may return overlapping tweets; merge by `id` to drop duplicates.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/x-tweet-scraper-x-tweet-search-by-query.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
