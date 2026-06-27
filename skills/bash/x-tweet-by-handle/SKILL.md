---
name: x-tweet-by-handle
description: "Scrapes tweets from an X (Twitter) user profile timeline given a handle, with selectable mode: tweets, tweets+replies, or media-only. Returns normalized per-tweet data including text, author profile, engagement counts, media, hashtags, mentions, and cursor for pagination. Use when user mentions X user tweets, Twitter user tweets, profile timeline, user feed, @handle tweets, scrape Twitter user, scrape X account, get all tweets from a user, scrape user timeline, download user posts, export tweets from user, with_replies tab, replies tab Twitter, media tab Twitter, photos of user Twitter, videos of user Twitter, latest tweets from user, recent tweets from account, KOL tweets, influencer tweet history, account post extraction, twitter handle scraper, x handle scraper, get tweets by username, monitor a Twitter account, monitor an X account, daily tweet export from handle, scrape from:username, twitter profile posts, x profile posts, by handle, by username. Also applies to building a creator backlog, tracking competitor accounts, populating quote-tweet research datasets, or any paginated bulk collection driven by a single user handle."
---

# X — Tweets by Handle

> X handle + timeline mode → normalized list of that user's tweets (or replies / media-only) with author, engagement, media, cursor.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Collect tweets from one or more X user profile timelines, selectable between the default tweets tab, the tweets-and-replies tab, and the media-only tab, returning structured per-tweet data and pagination cursors.

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

> This Skill's operational boundary = what the user can manually do in their browser. It only reads tweet data already shown to the user, never bypassing authentication. The browser's own JS signs the GraphQL request; the Skill triggers it via URL navigation and reads the response from network traffic. Python scripts under `scripts/` only build URLs and parse responses — they do not call X directly. Run them through the bash tool.

### Network Capture: profile timeline (tweets / replies / media)

Step 1 — build the profile URL for the desired mode:

`URL=$(python scripts/build-profile-url.py '{handle}' --mode {mode})`

Parameters:
- `handle` (positional): X handle without `@`, case-insensitive.
- `--mode`: one of `tweets` (default — triggers `UserTweets`), `replies` (triggers `UserTweetsAndReplies`), `media` (triggers `UserMedia`).

Step 2 — navigate and capture the first page:

1. `network requests --clear`
2. `navigate "$URL"`
3. `wait stable --timeout 25000` (timeout is normal on X; proceed even if it fires)
4. Determine the endpoint name to filter by — `UserTweets`, `UserTweetsAndReplies`, or `UserMedia` matching the chosen mode:
   - `network requests --type xhr,fetch --filter UserTweets` (when `--mode tweets`)
   - `network requests --type xhr,fetch --filter UserTweetsAndReplies` (when `--mode replies`)
   - `network requests --type xhr,fetch --filter UserMedia` (when `--mode media`)
5. Take the latest matching entry's `request_id`.
6. `network request <request_id>` → save full output to a file (e.g. `tmp/x-profile-page-1.txt`).
7. Parse with the matching `--source` flag:
   - `python scripts/parse-tweets.py --json-file tmp/x-profile-page-1.txt --source user_tweets` (for `tweets`)
   - `python scripts/parse-tweets.py --json-file tmp/x-profile-page-1.txt --source user_replies` (for `replies`)
   - `python scripts/parse-tweets.py --json-file tmp/x-profile-page-1.txt --source user_media` (for `media`)

Endpoint characteristic: URL contains `/i/api/graphql/<hash>/UserTweets` (or `UserTweetsAndReplies` / `UserMedia`). The query hash rotates; always filter by name.

Step 3 — paginate via scroll:

1. `network requests --clear`
2. `scroll down --amount 5000`
3. `wait stable --timeout 10000`
4. `network requests --type xhr,fetch --filter <EndpointName>` → take the newest entry's `request_id`
5. `network request <request_id>` → save to `tmp/x-profile-page-N.txt`
6. `python scripts/parse-tweets.py --json-file tmp/x-profile-page-N.txt --source <source>`

Repeat Step 3 until any termination condition is met:
- Accumulated unique tweet count reaches the user's target.
- `count == 0` on the current page.
- `cursor_bottom` is unchanged across two consecutive pages.

Error handling: if no matching request appears after a scroll, wait 3 s and retry once. If the page redirects to a "This account doesn't exist" or "Account suspended" view (visible in `state` output), terminate with an explanatory result. Pinned tweets appear at the top of the first page — they are normal tweets and are included in the output; de-duplicate by `id` when merging if a pinned tweet would also appear later in chronological order.

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
  "cursor_top": "DAAHCgABHLo27Q8__-s...",
  "cursor_bottom": "DAAHCgABHLo27Q8__-s..."
}
```

## Pagination

**Network Capture Pagination**: triggered by `scroll down`. X's page JS inserts the previous response's `cursor_bottom` into the next request's `variables.cursor`. Termination: `count == 0`, `cursor_bottom` does not advance across two consecutive pages, or user target reached.

## Success Criteria

`count >= 1 on the first page` (unless the account has zero tweets in the chosen mode) AND `every tweet has non-null id, text, created_at, author.user_name, like_count, retweet_count, reply_count` AND `each subsequent page's cursor_bottom differs from the previous page's until termination`.

## Known Limitations

- Protected (locked) accounts return zero tweets unless the logged-in session follows that account.
- Suspended or deleted accounts return an error page; the Skill will detect via empty `count` and a redirect to `/account_suspended` or `/account/access` and terminate the loop.
- `view_count` is `null` for very new or low-traffic tweets where X has not yet emitted `views.count`.
- `--mode media` returns tweets that contain native media only; pure-text or quote-only tweets are skipped by X server-side.
- Sustained polling triggers per-session throttling; stay under ~150 timeline calls per 15-minute window per session (`x-rate-limit-remaining` shows the live budget).
- The page may never reach `network-idle`; `wait stable` will frequently time out — proceed to read network anyway.

## Execution Efficiency

- **Batch orchestration**: write a bash script that iterates handles serially in one session; for parallelism, fan out across multiple stealth browsers each with its own login.
- **Test before batch execution**: run one handle end-to-end (page 1 + page 2) first.
- **Reduce redundant pre-operations**: keep the same session for many sequential handles — `navigate` reuses the SPA.
- **Error resumption**: persist `cursor_bottom` + accumulated tweet IDs to disk after every page; a crash mid-batch resumes from the last good cursor.
- **De-duplicate by `id`**: pinned tweets reappear when chronological order catches up; merge by `id`.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/x-tweet-scraper-x-tweet-by-handle.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what handle was scraped or how many tweets were returned — those are task outputs, not experience.
