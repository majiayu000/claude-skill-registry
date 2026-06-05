---
name: xiaohongshu-user-profile
description: "Fetch Xiaohongshu (RedNote / xhs) user profile information and their published notes list by user ID, returning nickname, bio, follower/following counts, engagement totals, tags, and paginated notes with engagement stats. Use when user mentions user profile xiaohongshu, rednote creator profile, xhs influencer data, scrape xiaohongshu user, get blogger notes, xiaohongshu author info, KOL discovery xiaohongshu, rednote user stats, creator profile rednote, xiaohongshu blogger analysis, get xhs user followers, rednote influencer profile, xiaohongshu account info, xhs creator data, user notes list xiaohongshu, rednote account scrape, xiaohongshu KOL research."
---

# Xiaohongshu — User Profile & Notes

> user_id → profile info (nickname, followers, bio, tags) + published notes list

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Navigate to a Xiaohongshu user profile page and extract the user's basic information, social stats, and their published notes list.

## Prerequisites

- Browser opened to `https://www.xiaohongshu.com/user/profile/{user_id}`
- User is logged in (avatar or username visible in the left sidebar)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Xiaohongshu has been confirmed in the current session → skip this step.

Otherwise: open `https://www.xiaohongshu.com` and observe the left sidebar:
- User avatar or "Me" entry visible → logged in, continue execution
- "Login" button visible → not logged in, inform the user that login is required, use `remote-assist` to let the user scan the QR code

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### DOM: extract user profile

Navigate to the user profile page, wait for Vue SSR state to populate, then extract from `window.__INITIAL_STATE__.user.userPageData`:

1. `navigate https://www.xiaohongshu.com/user/profile/{user_id}`
2. `wait stable`
3. `eval "$(python scripts/extract-user-profile.py {user_id})"`

Parameters:
- `{user_id}`: user ID (from note detail `userId` field or from the profile URL)

Output example:
```json
{
  "userId": "5bac4e3f7a4c7300016a6b88",
  "nickname": "LaLaIrene",
  "desc": "Personal bio text...",
  "gender": 1,                   // 0=unknown, 1=male, 2=female
  "ipLocation": "Shanghai",
  "avatar": "https://sns-avatar-...",
  "follows": "361",
  "fans": "23904",
  "interaction": "1086463",      // total likes + collects received
  "tags": ["travel", "food"]
}
```

Error handling: if `error: true` is returned, verify the page URL is a user profile page and `wait stable` has completed.

### DOM: extract user notes list

After navigating to the profile page (same page as user profile), extract notes already loaded into Vue state:

`eval "$(python scripts/extract-user-notes.py --limit {limit})"`

Parameters:
- `--limit`: max notes to return from current state, default `30`

Output example:
```json
{
  "total": 24,
  "hasMore": false,
  "notes": [
    {
      "id": null,
      "type": "normal",
      "title": "Not Switzerland! This is a natural grassland in Fujian!!",
      "likedCount": "5149",
      "collectedCount": "4170",
      "commentCount": "390",
      "coverUrl": "https://sns-..."
    }
  ]
}
```

Error handling: if `error: true` is returned, ensure the user profile page is loaded first (steps 1–2 above).

### Composite: get full user data (profile + notes)

Run both extractions on the same page load — no additional navigation needed:

1. `navigate https://www.xiaohongshu.com/user/profile/{user_id}`
2. `wait stable`
3. `eval "$(python scripts/extract-user-profile.py {user_id})"`
4. `eval "$(python scripts/extract-user-notes.py --limit {limit})"`

Merge results by `userId` field.

## Pagination

**DOM Pagination** (notes list): Initial page load pre-populates visible notes. To load more:

1. `scroll down --amount 3000`
2. `wait stable`
3. `eval "$(python scripts/extract-user-notes.py --limit {limit})"`

Each scroll triggers the page to load additional notes into `user.notes[0]`. Re-running the extraction script after each scroll retrieves the full accumulated list. Termination: `hasMore: false` in extraction output.

## Success Criteria

`profile.userId is non-null AND profile.nickname is non-null AND notes.total >= 0`

## Known Limitations

- Accessing user profiles requires login; without login the page shows a QR code overlay and `userPageData` is empty
- Notes list only includes notes from the default "Notes" tab; collected notes and liked notes are on separate tabs not covered by this capability
- Note `id` is always `null` in user profile notes state — the Vue state for user profile notes does not populate individual note IDs; use `xiaohongshu-search` to obtain note IDs and xsecTokens for downstream detail lookup
- `interaction` count combines total likes and collects received by all the user's notes — it is not a standalone likes-only or collects-only metric

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/xiaohongshu-data-xiaohongshu-user-profile.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what user IDs were fetched or how many notes were returned — those are task outputs, not experience.
