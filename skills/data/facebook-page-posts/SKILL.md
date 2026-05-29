---
name: facebook-page-posts
description: "Scrapes posts from any public Facebook Page timeline, returning structured data including post text, author info, engagement metrics (likes/comments/shares), reaction breakdowns (like/love/haha/wow/sad/angry/care), hashtags and external links, and media type. Use when user wants to scrape Facebook posts, extract Facebook page content, get Facebook post data, collect Facebook engagement stats, download Facebook posts, monitor a Facebook page, crawl Facebook timeline, get Facebook reactions, get like count/comment count/share count from Facebook, Facebook post bulk export, Facebook social media analytics. Supports date range filtering (afterTime/beforeTime) and cursor-based pagination for bulk collection."
---

# Facebook — Page Posts Scraper

> Facebook page URL → list of posts with full engagement metrics and text references

## Language

All process output to user (progress updates, process notifications) must be in English.

## Objective

Extract posts from a public Facebook Page timeline, including post content, engagement counts, reaction breakdowns, and text references (hashtags/links).

## Prerequisites

- The target Facebook page is open in the browser (e.g., `https://www.facebook.com/cern`)
- User is logged into Facebook (user avatar visible in the top right)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Facebook has been confirmed in the current session → skip this step.

Otherwise: navigate to `https://www.facebook.com` and check:
- User avatar or name visible in top right → logged in, continue
- Login button visible → not logged in, inform the user and assist with login

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### API: Resolve Facebook page URL to numeric page ID

`eval "$(python scripts/get-page-id.py '{page_url}')"`

Parameters:
- `page_url`: Full Facebook page URL, e.g. `https://www.facebook.com/cern`

**Must run while the target page is open** (or any Facebook page is open) so the browser has Facebook cookies.

Output example:
```json
{
  "pageId": "100064792144187",   // Numeric page ID used in all subsequent API calls
  "pageUrl": "https://www.facebook.com/cern"
}
```

### API: Fetch posts from page timeline

`eval "$(python scripts/get-page-posts.py '{page_id}' --cursor '{cursor}' --after-time {after_time} --before-time {before_time} --count {count})"`

Parameters:
- `page_id`: Numeric Facebook page ID (from get-page-id above)
- `--cursor`: Pagination cursor string from previous response `pagination.endCursor`; omit or pass `null` for first page
- `--after-time`: Unix timestamp (seconds); only return posts after this time; omit or pass `null` for no filter
- `--before-time`: Unix timestamp (seconds); only return posts before this time; omit or pass `null` for no filter
- `--count`: Number of posts per batch, default `5`, max recommended `10`

Output example:
```json
{
  "posts": [
    {
      "postId": "1417704873732571",                        // Numeric post ID
      "url": "https://www.facebook.com/cern/posts/pfbid…", // Post permalink
      "text": "CERN Council updates European Strategy…",   // Full post text
      "textReferences": [
        {
          "type": "ExternalUrl",                           // "ExternalUrl" or "Hashtag"
          "url": "https://home.cern/...",                  // Clean URL (not l.facebook.com redirect)
          "offset": 731,                                   // Position in text
          "length": 96
        },
        {
          "type": "Hashtag",
          "url": "https://www.facebook.com/hashtag/espp",
          "offset": 296,
          "length": 5
        }
      ],
      "creationTime": 1779460218,                          // Unix timestamp (seconds)
      "user": {
        "id": "100064792144187",                           // Page numeric ID
        "name": "CERN",                                    // Page display name
        "profileUrl": "https://www.facebook.com/cern"     // Page URL
      },
      "likes": 1220,                                       // Total reactions count
      "comments": 44,                                      // Comment count
      "shares": 122,                                       // Share count
      "topReactions": [
        { "name": "Like",  "count": 1108 },
        { "name": "Love",  "count": 92 },
        { "name": "Care",  "count": 9 },
        { "name": "Wow",   "count": 8 },
        { "name": "Haha",  "count": 1 },
        { "name": "Sad",   "count": 1 },
        { "name": "Angry", "count": 1 }
      ],
      "topReactionsCount": 1220,                           // Same as likes, total reactions
      "media": {
        "type": "Photo",                                   // "Photo", "Video", or null for text-only
        "id": "photo_id_string",                           // Media asset ID
        "viewsCount": null                                 // Video view count; null for photos
      },
      "feedbackId": "ZmVlZGJhY2s6MTQxNzcw…"               // Base64 feedback ID
    }
  ],
  "pagination": {
    "endCursor": "Cg8Ob3JnYW5pY19jd…",                   // Pass to --cursor for next page
    "hasNextPage": true                                    // false when no more posts
  }
}
```

Error handling: If response contains `"error": true`, check that the target page is open and the user is logged in, then retry once. If the error persists, the `doc_id` may have expired — check experience notes for updates.

## Pagination

**API Pagination**: cursor-based. Pass `pagination.endCursor` from each response as `--cursor` in the next call. Start value: omit `--cursor` (first page). Termination: `pagination.hasNextPage === false`.

## Success Criteria

`posts.length >= 1` AND `posts[0].postId` is non-null AND `posts[0].likes` is non-null

## Known Limitations

- `media.id` is returned but media thumbnail/photo URLs are not included in the API response for this query; only type and ID are available
- `viewsCount` is only populated for Video-type attachments; null for photos
- `feedbackId` is present but detailed reaction dialog data (individual reactor profiles) requires a separate API call not covered by this Skill
- The `doc_id: 27278869228466784` is a Facebook internal query ID that may change when Facebook deploys updates; if all calls return errors, the doc_id may need to be recaptured via HAR recording on the page
- Requires an active Facebook login session; public/unauthenticated access is not supported
- Date filtering (`afterTime`/`beforeTime`) applies to the timeline cursor position, not a strict server-side filter; posts near the boundary may occasionally appear outside the specified range

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Add a 1–2 second delay between paginated calls to avoid rate limiting. To increase throughput, open multiple browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: Run `get-page-id` once per page URL and reuse the result for all paginated calls
- **Error resumption**: Save results page by page during batch processing; on failure, resume from the last successful `endCursor` rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/facebook-posts-scraper-facebook-page-posts.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
