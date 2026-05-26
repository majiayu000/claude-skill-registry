---
name: instagram-profile-meta
description: "Fetches Instagram user profile metadata including bio, follower count, following count, post count, verification status and other profile details. Use when user mentions Instagram profile info, user stats, account details, follower count, bio scraping, Instagram user data, IG profile, check Instagram account, Instagram user info, how many followers does someone have on Instagram, get Instagram profile, Instagram account metadata."
---

# Instagram — Profile Metadata

> username → profile details (bio, counts, verification status)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Fetch complete metadata for an Instagram user profile via the internal REST API.

## Prerequisites

- Browser is open on any Instagram page: `https://www.instagram.com/`
- No login required for this capability

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### API: get profile metadata

`eval "$(python scripts/get-profile-meta.py '{username}')"`

Parameters:
- username: Instagram username without @ (e.g., `natgeo`)

Output example:
```json
{
  "id": "787132",
  "username": "natgeo",
  "full_name": "National Geographic",
  "biography": "The official Instagram page of National Geographic magazine.",
  "follower_count": 283000000,
  "following_count": 163,
  "media_count": 29500,
  "is_verified": true,
  "is_business_account": true,
  "profile_pic_url": "https://scontent.cdninstagram.com/...",
  "external_url": "https://www.nationalgeographic.com",
  "is_private": false
}
```

## Pagination

Not applicable — single user metadata.

## Success Criteria

`result count >= 1 AND id field non-null AND username field matches input`

## Known Limitations

- Private accounts: metadata (follower_count, biography) is returned, but posts are not accessible without following
- Rate limiting may occur with high-frequency requests

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/instagram-scraper-instagram-profile-meta.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
