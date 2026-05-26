---
name: instagram-profile-posts
description: "Scrapes posts from an Instagram user's profile feed including captions, media URLs, like/comment counts, timestamps and location tags. Use when user mentions scraping Instagram posts, download Instagram feed, get posts from Instagram account, IG profile posts, Instagram user posts, pull posts from Instagram, Instagram post list, get someone's Instagram content, batch download Instagram, Instagram media scraper."
---

# Instagram — Profile Posts

> username → paginated list of posts (media, caption, counts, timestamps)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Fetch all posts from an Instagram user's profile using the internal feed API with cursor-based pagination.

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

### API: get user ID from username

`eval "$(python scripts/get-user-id.py '{username}')"`

Parameters:
- username: Instagram username without @ (e.g., `natgeo`)

Output example:
```json
{
  "id": "787132",
  "username": "natgeo",
  "is_private": false
}
```

### API: get profile posts page

`eval "$(python scripts/get-profile-posts.py '{user_id}' --count 12 --max-id '{cursor}')"`

Parameters:
- user_id: Numeric user ID (from get-user-id output)
- --count: Posts per page, default `12` (max 12)
- --max-id: Pagination cursor; leave empty for first page, use `next_max_id` from previous response for subsequent pages

Output example:
```json
{
  "items": [
    {
      "pk": "3900557621921709539",
      "code": "DYwOA07iPmB",
      "taken_at": 1779686199,
      "media_type": 1,
      "like_count": 45230,
      "comment_count": 312,
      "caption": "Caption text here...",
      "thumbnail_url": "https://scontent.cdninstagram.com/...",
      "video_url": null,
      "location": {"id": "212988663", "name": "New York, New York"},
      "username": "natgeo",
      "user_id": "787132"
    }
  ],
  "more_available": true,
  "next_max_id": "3890000000000000000_787132"
}
```

### Composite: fetch all profile posts

Navigate to instagram.com first, then loop through pages:

1. `navigate https://www.instagram.com/` → `wait stable`
2. `eval "$(python scripts/get-user-id.py '{username}')"` → extract `id` as `user_id`
3. `eval "$(python scripts/get-profile-posts.py '{user_id}' --count 12)"` → collect `items`, note `more_available` and `next_max_id`
4. While `more_available` is `true`:
   a. `eval "$(python scripts/get-profile-posts.py '{user_id}' --count 12 --max-id '{next_max_id}')"` → accumulate `items`
5. Merge all collected items

## Pagination

**API Pagination**: `max_id`, type: cursor, start value: empty string. Next page value source: `next_max_id` field in response. Termination: `more_available` is `false` or `next_max_id` is null.

## Success Criteria

`result count >= 1 AND items[0].pk non-null AND items[0].code non-null`

## Known Limitations

- Private accounts: posts are not accessible unless the logged-in user follows the account
- Login required: without authentication, feed API returns `require_login: true`
- Account with 0 posts: API returns empty items array with `more_available: false`
- Maximum ~12 posts per API call

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/instagram-scraper-instagram-profile-posts.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
