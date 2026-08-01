---
name: threads-profile-search
description: "Discovers Threads user accounts by keyword, extracting profile data including username, display name, verification status, biography, and follower count. Use when user asks to find Threads accounts, search Threads profiles, discover Threads users by keyword, look up Threads creators, find influencers on Threads, search for people on Threads, get Threads user details, collect Threads profile information, find accounts related to a topic on Threads, search Threads for accounts by name or keyword, or enumerate Threads users matching a search term."
---

# Threads — Profile Search

> keyword → list of matching user profiles with optional enrichment (bio, follower count)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Search Threads for user accounts matching a keyword and extract profile information, with optional per-user enrichment to retrieve biography and follower count via the profile API.

## Prerequisites

- A browser is open and connected via browser-act
- No login required for profile search (unauthenticated: up to 16 profiles per query, no pagination)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### SSR: Extract profile search results (basic info)

Navigate to the profile search page, then extract user accounts from the SSR-embedded JSON:

1. `navigate https://www.threads.com/search/?q={keyword}&type=profiles`
2. `wait stable`
3. `eval "$(python scripts/extract-profile-search.py '{keyword}')"`

Output example:
```json
{
  "keyword": "zuck",
  "profiles": [
    {
      "pk": "14803522782",                 // Instagram-based user ID
      "username": "ceozuck162",            // Threads username (without @)
      "full_name": "ceo,zuck",             // display name
      "is_verified": false,                // blue checkmark verification status
      "is_private": false,                 // true if account is private
      "profile_pic_url": "https://...",    // profile picture URL
      "profile_url": "https://www.threads.com/@ceozuck162"
    }
  ],
  "count": 16,
  "page_info": {
    "end_cursor": null,
    "has_next_page": false,
    "has_previous_page": false,
    "start_cursor": null
  }
}
```

Error handling: If `error: true` is returned, verify the page URL ends with `&type=profiles`. If `searchResults not found`, retry `navigate` and `wait stable` once. If `count: 0`, no accounts matched the keyword.

### API: Get full profile details (biography + follower count)

Enrich a single username with full profile data including biography and follower count. The browser must be on any Threads page (authentication state is shared across the session):

`eval "$(python scripts/get-profile-details.py '{username}')"`

Parameters:
- `username`: Threads username without `@` (e.g., `zuck`)

Output example:
```json
{
  "pk": "314216",                          // Instagram user ID
  "username": "zuck",
  "full_name": "Mark Zuckerberg",
  "biography": "I build stuff",            // profile bio text, null if empty
  "follower_count": 16944740,             // number of followers, null if unavailable
  "following_count": 464,                  // number of accounts followed
  "is_verified": true,
  "is_private": false,
  "profile_pic_url": "https://...",
  "profile_url": "https://www.threads.com/@zuck",
  "external_url": null                     // website URL from profile, null if not set
}
```

Error handling: If `error: true` with a 429 status, the profile API is rate-limited — wait 10-30 seconds before retrying. If `User not found`, the username may be invalid or the account may be deleted.

### Composite: Search profiles + enrich each with full details

To collect profiles with biography and follower count for all results:

1. `navigate https://www.threads.com/search/?q={keyword}&type=profiles` → `wait stable`
2. `eval "$(python scripts/extract-profile-search.py '{keyword}')"` → collect profiles list
3. For each `username` in profiles:
   a. `eval "$(python scripts/get-profile-details.py '{username}')"` → merge biography, follower_count, following_count, external_url into profile record
4. Output merged list with all fields

Note: Profile API calls are made in the browser context and share the same session cookies. Add 1-2 second intervals between per-user calls to avoid rate limiting.

## Pagination

Pagination is not available for unauthenticated access on profile search (`has_next_page: false`). Results are limited to approximately 16 profiles per keyword without login.

## Success Criteria

`result.count >= 1` and `result.profiles[0].username != null`

For enriched flow: `profiles[0].follower_count != null` and `profiles[0].biography != null`

## Known Limitations

- Unauthenticated access: no pagination; approximately 16 profiles per query
- Basic profile search does not include biography or follower count — enrichment step required
- Profile API (`get-profile-details.py`) may be rate-limited; add intervals in batch loops
- Private accounts appear in search results but their post data is inaccessible
- `pk` from SSR profile search is the Instagram-based ID, which differs from the Threads-specific ID in post data

## Execution Efficiency

- **Batch orchestration**: Run `extract-profile-search.py` once per keyword, then loop through the returned usernames for enrichment. Do not call `get-profile-details.py` in parallel within the same session — rate limit applies.
- **Test before batch execution**: Test with 1-2 keywords first before running full enrichment batch.
- **Reduce redundant pre-operations**: After the search page load, all subsequent `get-profile-details.py` calls use `fetch()` in the current browser context — no additional navigation needed.
- **Error resumption**: Save results per username; on failure, resume enrichment from the breakpoint.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/threads-scraper-threads-profile-search.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions; adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
