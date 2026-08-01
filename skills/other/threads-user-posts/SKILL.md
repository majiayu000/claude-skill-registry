---
name: threads-user-posts
description: "Fetches public posts from a Threads user's profile page, extracting post text, engagement metrics, and media info from SSR-embedded JSON. Use when user asks to scrape Threads posts, get someone's Threads feed, pull posts from a Threads account, collect Threads content by username, download Threads user posts, extract Threads profile posts, monitor a Threads user's activity, retrieve recent posts from a Threads handle, gather Threads post data for a creator, or fetch all posts from a specific Threads profile."
---

# Threads — User Posts

> username → list of public posts with engagement metrics (SSR + scroll pagination)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract public posts from a given Threads user's profile page using SSR-embedded JSON data, with optional scroll-triggered pagination to load more posts.

## Prerequisites

- A browser is open and connected via browser-act
- **Login recommended**: Threads enforces a login wall on profile pages in most regions as of mid-2026. A logged-in browser session is required for reliable access. Unauthenticated access via US-based proxies may work in some configurations but is not guaranteed.

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Threads has been confirmed in the current session → skip this step.

Otherwise: `navigate https://www.threads.com` and check page state:
- User avatar or username visible at top → logged in, continue
- "Log in" / "Sign up" buttons visible → not logged in, inform the user that login is needed, assist completing the login flow via the Threads login page

If not logged in and user cannot log in → the capability may still work on some proxy/IP configurations; attempt `navigate https://www.threads.com/@{username}` and check if profile content loads. If the page redirects to `/login/`, terminate and inform the user that a logged-in session is required.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### SSR: Extract posts from profile page (initial load)

Navigate to the user's profile page first, then extract all posts embedded in the initial page HTML:

1. `navigate https://www.threads.com/@{username}`
2. `wait stable`
3. `eval "$(python scripts/extract-posts.py)"`

Output example:
```json
{
  "posts": [
    {
      "id": "3936653356768062022",          // post internal ID (pk)
      "code": "DKmzN8wJzFG",               // post short code for URL
      "url": "https://www.threads.com/@zuck/post/DKmzN8wJzFG",  // direct post link
      "text": "Excited to share...",        // post text content, null if no caption
      "taken_at": 1780953646,              // Unix timestamp of post creation
      "like_count": 3583,                  // number of likes
      "reply_count": 3039,                 // number of direct replies
      "repost_count": 232,                 // number of reposts
      "quote_count": 114,                  // number of quote posts
      "reshare_count": 460,                // number of reshares
      "is_reply": false,                   // true if this post is a reply to another
      "media_type": 19,                    // 1=photo, 2=video, 8=carousel, 19=text-only
      "has_media": false,                  // true if post contains image/video/carousel
      "user": {
        "pk": "63055343223",              // Threads-specific user ID
        "username": "zuck",
        "full_name": "Mark Zuckerberg",
        "is_verified": true
      }
    }
  ],
  "count": 4,                             // number of posts in this batch
  "page_info": {
    "end_cursor": "QVFES...",             // cursor for next page (null when no more)
    "has_next_page": true,                // whether more posts are available
    "has_previous_page": false,
    "start_cursor": null
  }
}
```

Error handling: If `error: true` is returned, check that the profile page was fully loaded (`navigate` and `wait stable` completed without timeout). If `mediaData not found`, the page may have redirected to a login wall or the username is invalid.

### DOM: Scroll to trigger more posts

When `page_info.has_next_page` is true, scroll the page to trigger GraphQL auto-load:

`eval "$(python scripts/scroll-load-more.py)"`

Then `wait stable` and read the new batch from network traffic:

`network requests --type xhr,fetch --filter threads.com`

Find the `POST https://www.threads.com/graphql/query` request(s) that appeared after the scroll. Read the response:

`network request <id>`

The response body contains `data.mediaData.edges[]` with the same post structure as the SSR extraction output. Each edge has `node.thread_items[0].post` with the same field layout (id/pk, code, caption.text, taken_at, like_count, text_post_app_info.direct_reply_count, etc.).

Error handling: If no new `graphql/query` requests appear after scrolling, the user may have reached the login wall (~15 posts without authentication) or all posts have loaded. Check for a "Log in to see more" message on screen via `screenshot`.

### Composite: Full profile post collection (SSR + scroll pagination)

To collect all available posts for a user:

1. `navigate https://www.threads.com/@{username}` → `wait stable`
2. `eval "$(python scripts/extract-posts.py)"` → collect initial posts, note `page_info`
3. While `page_info.has_next_page == true`:
   a. `eval "$(python scripts/scroll-load-more.py)"`
   b. `wait stable`
   c. `network requests --type xhr,fetch --filter threads.com` → locate new `graphql/query` POST
   d. `network request <id>` → extract `data.mediaData.edges[]` posts
   e. Check `data.mediaData.page_info.has_next_page` in response to decide whether to continue
4. Stop when `has_next_page == false` or login wall encountered (~15 posts without login)

## Pagination

**DOM Pagination**: Scroll `#scrollview` via `eval "$(python scripts/scroll-load-more.py)"`, then `wait stable` and read new `POST /graphql/query` response from network traffic. Termination: `page_info.has_next_page == false` in the GraphQL response, or login wall visible on screen (approximately 15 posts without authentication).

## Success Criteria

`result.count >= 1` and `result.posts[0].id != null` and `result.posts[0].user.username != null`

## Known Limitations

- **Login wall**: As of mid-2026, Threads redirects unauthenticated profile page requests to the login page in most regions. A logged-in browser session is required for reliable use; unauthenticated access works only on specific proxy/IP configurations.
- Authenticated access: up to approximately 15 posts per profile before hitting a soft pagination limit; further posts require additional scroll cycles.
- Private accounts: profile page shows no posts even for logged-in users who don't follow the account.
- Deleted or suspended accounts return `mediaData not found` error.
- `taken_at` is a Unix timestamp; convert to readable date with `new Date(taken_at * 1000).toISOString()`.

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser. Add 2-3 second intervals between profile navigations to avoid rate limiting. For higher throughput, distribute usernames across multiple parallel browser sessions.
- **Test before batch execution**: After writing a batch script, test with 1-2 usernames first to verify the script runs correctly; only then run the full batch.
- **Reduce redundant pre-operations**: When collecting multiple profiles in the same session, the session state is preserved across navigations — no need to reinitialize.
- **Error resumption**: Save results per username during batch processing; on failure, resume from the breakpoint rather than starting over.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/threads-scraper-threads-user-posts.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
