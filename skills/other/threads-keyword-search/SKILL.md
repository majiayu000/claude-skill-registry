---
name: threads-keyword-search
description: "Searches Threads posts by keyword or hashtag and returns matching posts with engagement metrics, extracted from SSR-embedded JSON. Use when user asks to search Threads posts, find Threads content by topic, scrape Threads search results, collect Threads posts about a keyword, monitor Threads hashtag activity, pull Threads posts mentioning a term, gather Threads content by hashtag, search for posts on Threads, extract Threads search feed, get trending posts on Threads, find Threads discussions about a subject, or fetch recent or top Threads posts by keyword."
---

# Threads — Keyword & Hashtag Search

> keyword + sort filter → list of matching posts with engagement metrics

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Search Threads for posts matching a keyword or hashtag and extract the results from SSR-embedded JSON, with support for top/recent sort ordering.

## Prerequisites

- A browser is open and connected via browser-act
- No login required for public search results (unauthenticated: typically 17-18 results per query, no pagination)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### SSR: Extract keyword search results

Navigate to the search page with the keyword and sort filter, then extract all results embedded in the initial HTML:

1. `navigate https://www.threads.com/search/?q={keyword}&serp_type={filter}`
   - `{keyword}`: URL-encoded search term or hashtag (e.g., `AI` or `%23AI` for `#AI`)
   - `{filter}`: `top` (default, most relevant) or `recent` (chronologically newest)
2. `wait stable`
3. `eval "$(python scripts/extract-search-results.py '{keyword}' --filter {filter})"`

Output example:
```json
{
  "keyword": "AI",
  "filter": "top",
  "posts": [
    {
      "id": "3936653356768062022",          // post internal ID (pk)
      "code": "DZyvcdEl-W1",               // post short code for URL
      "url": "https://www.threads.com/@flower_popy/post/DZyvcdEl-W1",
      "text": "AI is changing everything...", // post text content, null if no caption
      "taken_at": 1781926571,              // Unix timestamp of post creation
      "like_count": 34,                    // number of likes
      "reply_count": 6,                    // number of direct replies
      "repost_count": 0,                   // number of reposts
      "quote_count": 0,                    // number of quote posts
      "is_reply": false,                   // true if this post is a reply
      "media_type": 19,                    // 1=photo, 2=video, 8=carousel, 19=text-only
      "has_media": false,                  // true if post contains image/video/carousel
      "user": {
        "pk": "14803522782",
        "username": "flower_popy",
        "full_name": "Flower",
        "is_verified": false
      }
    }
  ],
  "count": 17,
  "page_info": {
    "end_cursor": null,
    "has_next_page": false,
    "has_previous_page": false,
    "start_cursor": null
  }
}
```

Error handling: If `error: true` is returned, check that the search page loaded correctly by verifying the URL contains the query parameter. If `searchResults not found`, the page may have failed to render SSR data — retry `navigate` and `wait stable` once. If `count: 0`, no posts matched the keyword.

### SSR: Hashtag search

Hashtag search uses the same URL pattern. Prefix keyword with `#`:

1. `navigate https://www.threads.com/search/?q=%23{hashtag}&serp_type={filter}`
   - Example: `%23AI` for `#AI`
2. `wait stable`
3. `eval "$(python scripts/extract-search-results.py '#AI' --filter top)"`

The `#` prefix in the keyword argument is for labeling only; the URL encoding `%23` is what Threads uses to identify hashtag searches.

## Enum Parameters

[DOM] filter — values: `top` (most relevant/popular posts), `recent` (newest posts first). Set via `--filter` argument and `serp_type` URL parameter.

## Pagination

Pagination is not available for unauthenticated access on the search endpoint (`has_next_page: false` is returned regardless of result volume). Results are limited to approximately 17-18 posts per query without login. For broader coverage, run multiple searches with related keywords.

## Success Criteria

`result.count >= 1` and `result.posts[0].id != null` and `result.posts[0].user.username != null`

## Known Limitations

- Unauthenticated access: no pagination; approximately 17-18 results per keyword
- Date filtering is not supported as a URL parameter; filter by `taken_at` (Unix timestamp) client-side after extraction
- Private account posts may appear in search results but their full content may be restricted
- Search index may not include very new posts (lag of minutes to hours)

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop keywords serially within a single session. Add 1-2 second intervals between searches. For higher throughput, distribute keywords across multiple parallel browser sessions.
- **Test before batch execution**: Test with 1-2 keywords first before running full batch.
- **Reduce redundant pre-operations**: Each keyword requires a fresh `navigate` to the search URL — the search parameters are baked into the URL.
- **Error resumption**: Save results per keyword; on failure, resume from the breakpoint.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/threads-scraper-threads-keyword-search.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions; adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
