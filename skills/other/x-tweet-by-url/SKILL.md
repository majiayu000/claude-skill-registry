---
name: x-tweet-by-url
description: "Scrapes tweets from any X (Twitter) URL — search results, user profile, single tweet detail, or list timeline — and returns normalized per-tweet data with text, author, engagement counts, media, hashtags, mentions, and cursor for pagination. Use when user mentions X URL scraper, Twitter URL scraper, scrape from URL, given an X link, given a Twitter link, accept mixed X URLs, accept mixed Twitter URLs, search URL, profile URL, list URL, status URL, tweet detail URL, scrape startUrls Twitter, X startUrls, mixed batch of Twitter links, paste links and scrape, mass URL extraction X, mass URL extraction Twitter, scrape from a list of links, x.com URLs, twitter.com URLs, classify Twitter URLs, auto-detect Twitter URL type, scrape lists on X, scrape Twitter lists, list timeline scraper, list tweet scraper, scrape conversation by URL. Also applies to processing seed URL files, dispatching mixed X URLs through a single workflow, list-based KOL monitoring, batch-collecting tweets from a curated list of profiles, lists, and individual posts."
---

# X — Tweets by URL

> Any X URL (search, profile, single tweet, list) → normalized list of tweets matching that URL's timeline.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Accept any X URL as input, automatically detect which timeline endpoint it triggers, navigate to it, and return structured per-tweet data with pagination cursors. This unifies search, profile, single-tweet conversation, and list extraction under one entry point.

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
- User avatar or @handle visible → logged in, continue
- "Sign in" / "Log in" prompt visible → not logged in, inform the user and assist the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads tweet data already shown to the user, never bypassing authentication. The browser's own JS signs the GraphQL request; the Skill triggers it via URL navigation and reads the response from network traffic. Python scripts under `scripts/` only classify URLs and parse responses — they do not call X directly. Run them through the bash tool.

### Network Capture: tweets via input URL

Step 1 — classify the URL to determine which GraphQL endpoint will be triggered and which `--source` to pass to the parser:

`META=$(python scripts/classify-url.py '{url}')`

`classify-url.py` outputs a JSON object with fields:
- `normalized_url`: the URL with `twitter.com` rewritten to `x.com`.
- `kind`: one of `search`, `user_tweets`, `user_replies`, `user_media`, `tweet_detail`, `list`, `unknown`.
- `endpoint`: the GraphQL endpoint name to filter by (`SearchTimeline` / `UserTweets` / `UserTweetsAndReplies` / `UserMedia` / `TweetDetail` / `ListLatestTweetsTimeline`).
- `extract_source`: the `--source` value to pass to `parse-tweets.py` (`search` / `user_tweets` / `user_replies` / `user_media` / `tweet_detail` / `list`).
- `params`: detected path parameters (`handle`, `tweet_id`, `list_id`) when applicable.

If `kind == "unknown"`, report to the user that the URL is not a supported X timeline type and stop.

Step 2 — navigate and capture the first page:

1. `network requests --clear`
2. `navigate "$(echo "$META" | python -c "import sys,json;print(json.load(sys.stdin)['normalized_url'])")"`
3. `wait stable --timeout 25000` (timeout is normal on X; proceed)
4. Let `EP` = `endpoint` from `$META`. `network requests --type xhr,fetch --filter "$EP"` → take the latest entry's `request_id`.
5. `network request <request_id>` → save to `tmp/x-url-page-1.txt`.
6. Let `SRC` = `extract_source` from `$META`. `python scripts/parse-tweets.py --json-file tmp/x-url-page-1.txt --source "$SRC"`.

Endpoint characteristic: URL contains `/i/api/graphql/<hash>/<endpoint-name>`. The query hash rotates; always filter by name.

Step 3 — paginate via scroll (skip when `kind == "tweet_detail"` and only the focal tweet is required; keep paginating when collecting the full reply thread):

1. `network requests --clear`
2. `scroll down --amount 5000`
3. `wait stable --timeout 10000`
4. `network requests --type xhr,fetch --filter "$EP"` → newest entry's `request_id`
5. `network request <request_id>` → save to `tmp/x-url-page-N.txt`
6. `python scripts/parse-tweets.py --json-file tmp/x-url-page-N.txt --source "$SRC"`

Repeat Step 3 until any termination condition is met:
- Accumulated unique tweet count reaches the user's target.
- `count == 0` on the current page.
- `cursor_bottom` is unchanged across two consecutive pages.

Error handling: if no matching request appears after a scroll, wait 3 s and retry once. If `kind == "search"` and the page shows a captcha challenge (detect via `state` showing an "Authorize access to your account" or "Help us keep X safe" panel), pause and ask the user. If `kind == "list"` and the response's `data.list.tweets_timeline.timeline.instructions` is empty, the list is empty or access-restricted to the owner — terminate and report.

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
        {"type": "photo", "url": "https://pbs.twimg.com/media/abcd.jpg", "expanded_url": "https://x.com/NASA/status/2068333045510291908/photo/1", "alt_text": null}
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

**Network Capture Pagination**: triggered by `scroll down`. X's page JS automatically inserts the previous response's `cursor_bottom` into the next request's `variables.cursor`. Termination: `count == 0`, `cursor_bottom` does not advance across two consecutive pages, or user target reached. For `tweet_detail`, pagination loads more replies; when only the focal tweet is required, stop after the first page.

## Success Criteria

`kind != "unknown"` AND `count >= 1 on the first page` (unless the source is genuinely empty) AND `every tweet has non-null id, text, created_at, author.user_name, like_count, retweet_count, reply_count` AND `each subsequent page's cursor_bottom differs from the previous page's until termination`.

## Known Limitations

- Only X resources whose URLs match `https://x.com/search`, `https://x.com/{handle}`, `https://x.com/{handle}/with_replies`, `https://x.com/{handle}/media`, `https://x.com/{handle}/status/{id}`, or `https://x.com/i/lists/{id}` are supported. Internal pages like Communities, Bookmarks, Likes, and Notifications fall back to `kind: unknown`.
- `twitter.com` URLs are rewritten to `x.com` automatically; mobile (`mobile.twitter.com`) URLs are NOT rewritten and may fail — pass the canonical `x.com` form.
- Protected, suspended, or deleted resources return empty responses; the Skill terminates the loop and reports the cause.
- `view_count` is `null` for very new or low-traffic tweets where X has not emitted `views.count`.
- Sustained polling triggers per-session throttling; stay under ~150 timeline calls per 15-minute window per session.

## Execution Efficiency

- **Batch orchestration**: write a bash script that iterates URLs serially in one session; URLs of mixed kinds are fine because the classifier picks the right endpoint per URL. To parallelize, fan out across multiple stealth browsers, each with its own login and rate budget.
- **Test before batch execution**: run one URL of each `kind` in your input set end-to-end before the full batch — different timelines have slightly different cursor advance patterns.
- **Reduce redundant pre-operations**: keep the same session for many sequential URLs.
- **Error resumption**: persist `cursor_bottom` and accumulated tweet IDs per URL after every page.
- **De-duplicate by `id`**: when the same tweet is reachable via multiple input URLs (search + profile, profile + status), merge by `id`.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/x-tweet-scraper-x-tweet-by-url.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what URLs were processed or how many tweets were returned — those are task outputs, not experience.
