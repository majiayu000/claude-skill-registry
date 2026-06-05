---
name: xiaohongshu-search
description: "Search Xiaohongshu (RedNote / xhs) notes by keyword and return a paginated list with title, author, engagement stats (likes, collects, comments), cover image URL, and xsecToken for detail lookup. Use when user mentions find notes on xiaohongshu, search rednote, search xhs, scrape xiaohongshu search, xiaohongshu keyword search, rednote post search, xhs search results, monitor xiaohongshu topics, KOL content discovery via xiaohongshu, xiaohongshu note list, rednote scrape, xhs data collection, collect xiaohongshu posts, xiaohongshu topic search, xiaohongshu content monitoring, rednote post list, xhs keyword scrape."
---

# Xiaohongshu — Search Notes

> keyword → list of notes with title, author, engagement stats, xsecToken

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Search Xiaohongshu notes by keyword and extract the result list including engagement metrics and tokens for downstream detail lookup.

## Prerequisites

- Browser opened to `https://www.xiaohongshu.com/search_result/?keyword={keyword}`
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

### DOM: extract search results

Navigate to the search page (business parameters injected via URL), wait for the Vue SSR state to populate, then extract from `window.__INITIAL_STATE__.search.feeds`:

1. `navigate https://www.xiaohongshu.com/search_result/?keyword={keyword}`
2. `wait stable`
3. (optional) apply filters — see AI Workflow below
4. `eval "$(python scripts/extract-search.py --limit {limit})"`

Parameters:
- `{keyword}`: URL-encoded search keyword (e.g., `travel`, `coffee`)
- `--limit`: max items to return from current feeds buffer, default `20`

Output example:
```json
{
  "total": 44,
  "hasMore": true,
  "page": 2,
  "items": [
    {
      "id": "69d8cd8c0000000022002295",
      "xsecToken": "ABpK6gG0Dmt6MoVt60wJf-J0VMaCw5Y1Hi766ap7uWrxE=",
      "type": "normal",
      "title": "Not Switzerland! This is a natural grassland in Fujian!!",
      "userId": "5bac4e3f7a4c7300016a6b88",
      "nickname": "half-goose",
      "likedCount": "5149",       // likes
      "collectedCount": "4170",   // collects/saves
      "commentCount": "390",      // comments
      "coverUrl": "https://sns-..."
    }
  ]
}
```

Error handling: if `error: true` is returned, verify the page URL is a search result page and `wait stable` has completed before retrying.

### AI Workflow: apply sort and note-type filters (before extraction)

Run this workflow before the extraction step when the user specifies a sort order or note type. Uses the filter panel on the search result page:

1. `state` — locate the "Filter" button in the top-right area of the search content area → `click <index>`
2. Wait for filter panel to appear (visible on the right side of the page)
3. For **sort order** — `state` locate the desired sort tag in the "Sort By" row → `click <index>`

   | UI Label | filterParams value |
   |---|---|
   | General (default) | `general` |
   | Latest | `time_descending` |
   | Most Liked | `popularity_descending` |
   | Most Commented | `comment_descending` |
   | Most Collected | `collect_descending` |

4. For **note type** — `state` locate the desired type tag in the "Note Type" row → `click <index>`

   | UI Label | filterParams value |
   |---|---|
   | All (default) | — |
   | Video | `video-note` (site internal) |
   | Image-text | `image-text-note` (site internal) |

5. `state` locate the "Collapse" button at the bottom of the filter panel → `click <index>`
6. `wait stable`
7. Then run: `eval "$(python scripts/extract-search.py --limit {limit})"`

## Enum Parameters

[AI] sort — filterParams.tags[0] value for the sort_type filter. Acquisition: open filter panel via `state` + `click`, read "Sort By" row options. Verified values: `general`, `time_descending`, `popularity_descending`, `comment_descending`, `collect_descending`.

[AI] note_type — filterParams.tags[0] value for the filter_note_type filter. Acquisition: open filter panel via `state` + `click`, read "Note Type" row options. Verified values: video-note type (obtained by clicking "Video" option), image-text-note type (obtained by clicking "Image-text" option).

time_filter [collection failed]: time filter API parameter value not captured — UI interaction applies filter but POST body parameter mapping was not observed.

## Pagination

**DOM Pagination**: `scroll down --amount 3000` → `wait stable` → re-run `eval "$(python scripts/extract-search.py --limit {limit})"`. Each scroll loads ~20 more results into `feeds`. Termination: `hasMore: false` in extraction output.

## Success Criteria

`result.items.length >= 1 AND result.items[0].id is non-null`

## Known Limitations

- Search requires login; without login the page shows a QR code overlay and `feeds` is empty
- Filter interaction applies changes to the current page's Vue state; after page navigation or reload, filters reset to defaults

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/xiaohongshu-data-xiaohongshu-search.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
