---
name: xiaohongshu-note-detail
description: "Fetch Xiaohongshu (RedNote / xhs) note detail and comments by note ID, returning title, description, author info, engagement stats, tags, and paginated comment list. Use when user mentions note detail xiaohongshu, get rednote post, xhs note content, xiaohongshu comment scrape, fetch post comments, scrape xhs comments, rednote note details, xiaohongshu post engagement, xiaohongshu note content, rednote post data, xhs post detail, get xiaohongshu comments, rednote comment list, xiaohongshu note metadata, xhs note scrape, fetch rednote note."
---

# Xiaohongshu — Note Detail & Comments

> note_id + xsecToken → note metadata, author info, engagement stats, comment list

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Navigate to a Xiaohongshu note detail page and extract the full note metadata plus its paginated comment list.

## Prerequisites

- Browser opened to `https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsecToken}&xsec_source=pc_search`
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

### DOM: extract note detail

Navigate to the note page, wait for Vue SSR state to populate, then extract from `window.__INITIAL_STATE__.note.noteDetailMap`:

1. `navigate https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsecToken}&xsec_source=pc_search`
2. `wait stable`
3. `eval "$(python scripts/extract-note-detail.py {note_id})"`

Parameters:
- `{note_id}`: note ID (from search result `id` field or from the note URL)
- `{xsecToken}`: security token (from search result `xsecToken` field)

Output example:
```json
{
  "noteId": "69d8cd8c0000000022002295",
  "title": "Not Switzerland! This is a natural grassland in Fujian!!",
  "desc": "Full post body text...",
  "type": "normal",
  "time": 1748390400000,        // publish timestamp (ms)
  "ipLocation": "Fujian",
  "userId": "5bac4e3f7a4c7300016a6b88",
  "nickname": "half-goose",
  "avatar": "https://sns-avatar-...",
  "likedCount": "5149",
  "collectedCount": "4170",
  "commentCount": "390",
  "shareCount": "112",
  "tagList": [{"name": "travel", "type": "topic"}],
  "imageCount": 9
}
```

Error handling: if `error: true` is returned, verify the page URL is a note detail page, `wait stable` has completed, and the `note_id` matches the URL.

### DOM: extract note comments

After navigating to the note page (same page as note detail), extract initial comments already loaded into Vue state:

`eval "$(python scripts/extract-note-comments.py {note_id})"`

Parameters:
- `{note_id}`: same note ID used when navigating

Output example:
```json
{
  "count": 10,
  "cursor": "aabbcc112233",     // pass to next page load; empty string when on first page
  "hasMore": true,
  "comments": [
    {
      "id": "6835ae0e000000001203a14c",
      "content": "So beautiful!",
      "likeCount": "23",
      "createTime": 1748390500000,
      "ipLocation": "Guangdong",
      "userId": "5c3a6f020000000007010b9f",
      "nickname": "travel-enthusiast-xw",
      "avatar": "https://sns-avatar-..."
    }
  ]
}
```

Error handling: if `error: true` is returned, ensure the note detail page is loaded first (step 3 of note detail component above).

### Composite: get full note (detail + initial comments)

Run both extractions on the same page load — no additional navigation needed:

1. `navigate https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsecToken}&xsec_source=pc_search`
2. `wait stable`
3. `eval "$(python scripts/extract-note-detail.py {note_id})"`
4. `eval "$(python scripts/extract-note-comments.py {note_id})"`

Merge results by `noteId` field.

## Pagination

**DOM Pagination** (comments): Initial page load pre-populates up to 10 comments. To load more:

1. `scroll down --amount 3000`
2. `wait stable`
3. `eval "$(python scripts/extract-note-comments.py {note_id})"`

Each scroll triggers the page to load additional comments into `noteDetailMap[noteId].comments`. Re-running the extraction script after each scroll retrieves the full accumulated list. Termination: `hasMore: false` in extraction output.

## Success Criteria

`detail.noteId is non-null AND detail.title is non-null`

## Known Limitations

- Accessing note detail requires login; without login the page shows a QR code overlay and `noteDetailMap` is empty
- `xsec_token` must correspond to the `note_id`; mismatched tokens result in a redirect or empty state
- Comment count in note detail (`commentCount`) may exceed comments available via DOM scroll — some comments may be filtered or not loaded without deeper scrolling
- Image content (actual image URLs from `imageList`) is not extracted by `extract-note-detail.py` — only `imageCount` is returned

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/xiaohongshu-data-xiaohongshu-note-detail.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what note IDs were fetched or how many comments were returned — those are task outputs, not experience.
