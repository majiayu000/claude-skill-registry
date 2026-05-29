---
name: instagram-post-comments
description: "Fetches comments from an Instagram post including comment text, username, timestamp, like count and reply count. Use when user mentions Instagram comments scraping, get comments from Instagram post, Instagram comment list, pull Instagram comments, read Instagram comments, Instagram post discussion, extract Instagram comments, comment data from Instagram, IG post replies, who commented on Instagram."
---

# Instagram — Post Comments

> post shortcode or media ID → paginated list of comments

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Fetch comments for a specific Instagram post using the internal comments API with cursor-based pagination.

## Prerequisites

- Browser is open on any Instagram page: `https://www.instagram.com/`
- Logged into Instagram (user avatar or username visible in top-right corner)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Instagram has been confirmed in the current session → skip this step.

Otherwise: open `https://www.instagram.com/` and observe the page login status:
- Logout/sign-out entry, user avatar, or username exists → logged in, continue execution
- Login/register entry exists with no logout entry → not logged in, inform the user that login is needed first, assist the user in completing the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### API: get media ID from shortcode

`eval "$(python scripts/get-media-id.py '{shortcode}')"`

Parameters:
- shortcode: Post shortcode from the Instagram URL (e.g., from `instagram.com/p/BwrsO1Bho2N/` → `BwrsO1Bho2N`)

Output example:
```json
{
  "media_id": "3900557621921709539",
  "shortcode": "BwrsO1Bho2N",
  "media_type": 1,
  "username": "natgeo",
  "taken_at": 1779686199
}
```

### API: get comments page

`eval "$(python scripts/get-post-comments.py '{media_id}' --min-id '{cursor}')"`

Parameters:
- media_id: Numeric media ID / pk (from get-media-id output, or from profile-posts output)
- --min-id: Pagination cursor; leave empty for first page, use `next_min_id` from previous response for subsequent pages

Output example:
```json
{
  "comments": [
    {
      "pk": "17857015000000001",
      "text": "Amazing photo!",
      "username": "john_doe",
      "user_id": "123456789",
      "created_at": 1779686500,
      "like_count": 42,
      "reply_count": 3
    }
  ],
  "has_more_comments": true,
  "next_min_id": "17857015000000001"
}
```

### Composite: fetch all comments for a post

1. `navigate https://www.instagram.com/` → `wait stable`
2. If only shortcode is available: `eval "$(python scripts/get-media-id.py '{shortcode}')"` → extract `media_id`
3. `eval "$(python scripts/get-post-comments.py '{media_id}')"` → collect `comments`, note `has_more_comments` and `next_min_id`
4. While `has_more_comments` is `true`:
   a. `eval "$(python scripts/get-post-comments.py '{media_id}' --min-id '{next_min_id}')"` → accumulate `comments`
5. Merge all collected comments

## Pagination

**API Pagination**: `min_id`, type: cursor, start value: empty string. Next page value source: `next_min_id` field in response. Termination: `has_more_comments` is `false` or `next_min_id` is null.

## Success Criteria

`result count >= 1 AND comments[0].text non-null AND comments[0].username non-null`

## Known Limitations

- Login required: comments API returns `require_login: true` without authentication
- Posts with comments disabled return empty comments array
- Deleted comments or accounts may return partial data

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/instagram-scraper-instagram-post-comments.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
