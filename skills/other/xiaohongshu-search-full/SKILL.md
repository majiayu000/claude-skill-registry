---
name: xiaohongshu-search-full
description: "Search Xiaohongshu (XHS / RedNote) notes by keyword with full field extraction including body text, topics/tags, image list URLs, video stream URL, publish timestamp, and all engagement stats (likes, collects, comments, shares). Supports all page filter options: sort order (general, latest, most liked, most commented, most collected), note type (image-text, video), publish time range (within 1 day, 1 week, 6 months), search scope (seen, unseen, followed), and location distance (same city, nearby). Use when user mentions search xiaohongshu notes, xhs keyword search, rednote note search, search xiaohongshu posts, scrape xhs search results, xiaohongshu note discovery, rednote content search, collect xhs notes by keyword, xiaohongshu topic search, xhs note body text, xiaohongshu video notes, xiaohongshu image notes, rednote post filter, xhs search with filters, xiaohongshu full note data, xhs note details from search, extract rednote posts, xiaohongshu content monitoring, xhs search scrape."
---

# Xiaohongshu — Search Notes (Full Fields)

> keyword + filters → note list with full metadata (title, body, images, video URL, tags, stats) + detail enrichment

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Search Xiaohongshu notes by keyword, apply page filter options, and extract the maximum available fields from both the search results list and individual note detail pages.

## Prerequisites

- Browser opened to `https://www.xiaohongshu.com/search_result/?keyword={keyword}`
- User is logged in (avatar or username visible in the left sidebar)

## Phase 0: Collect User Inputs

**First action**: check whether the search keyword is already present in the user's message.

**Keyword is present** (e.g., "搜索 BrowserAct", "search for AI tools", "/xiaohongshu-search-full blockchain") → use it directly, skip to Pre-execution Checks.

**Keyword is NOT present** → STOP. Do NOT output "ready" or proceed with any execution. Ask the user for the keyword:
- If the **AskUserQuestion** tool is available → call it immediately with:
  - Question 1 (required): "请问您想在小红书上搜索什么关键词？" 
  - Question 2 (optional): pages needed (default: first page only)
  - Question 3 (optional): filters — sort order, note type, publish time range
- If AskUserQuestion is NOT available → output the following text and wait for the user's reply before doing anything else:
  > "请问您想搜索什么关键词？（如需指定页数或筛选条件，也可一并告知）"

Do NOT guess, infer, or assume any keyword. Wait for the user's explicit reply.

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

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `python scripts/xxx.py {params} | browser-act --session <name> eval --stdin`.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### DOM: extract search feeds list (preferred method)

Navigate to the search page, then read the rendered note list directly from Vue state. This is the **preferred method** because it reflects exactly what the page renders — including exact-match notes that the search API omits due to semantic expansion.

1. `navigate https://www.xiaohongshu.com/search_result/?keyword={keyword}`
2. `wait stable`
3. (optional) Apply filters — see **AI Workflow: apply filters** below
4. `python scripts/extract-search-feeds.py | browser-act --session <name> eval --stdin` — retrieves all page results. **Do NOT pass `--keyword` for a full keyword search** (title + body); see **AI Workflow: keyword search (title + body match)** below. Pass `--keyword {keyword}` only when title-only pre-filtering is explicitly required.

Parameters:
- `--keyword {keyword}` (optional): plain text keyword — when passed, `items` contains only title-matched notes and `keyword_count` is populated. Omit to get all rendered notes (required for body-text matching).

Output example:
```json
{
  "total_count": 40,
  "keyword_count": 3,
  "has_more": true,
  "items": [
    {
      "id": "6a422f88000000001603cdd3",
      "xsec_token": "ABbCLyAhrP9qgixS_rCW...",
      "note_url": "https://www.xiaohongshu.com/explore/6a422f88000000001603cdd3?xsec_token=ABbCLy...%3D&xsec_source=pc_search",
      "type": "video",                           // "normal" = image-text, "video" = video note
      "title": "note title text here",
      "publish_date": "06-29",                   // human-readable date string (not exact timestamp)
      "cover_url": "http://sns-webpic-qc.xhscdn.com/...",
      "liked_count": "3",
      "collected_count": "7",
      "comment_count": "0",
      "shared_count": "0",
      "author_nickname": "author nickname here",
      "author_id": "670caaaa000000001d0239d1",
      "author_avatar": "https://sns-avatar-qc.xhscdn.com/..."
    }
  ]
}
```

- `total_count`: all notes rendered by the page (includes semantically expanded results)
- `keyword_count`: notes whose **title** fuzzy-matches the keyword (Levenshtein edit distance ≤ 20% of keyword length, min 1 edit)
- `items`: the fuzzy-filtered list (only notes whose title fuzzy-matches the keyword)
- `keyword_count: null` means no `--keyword` was passed and `items` = all notes

Fuzzy matching details: `--keyword` uses Levenshtein edit distance with threshold `max(1, floor(kw.length * 0.2))` per sliding window over each word in the title. This catches typos, capitalization variants (e.g., `linfox` → `LinkFox`, `linxfox`), and minor spelling differences within the threshold.

Note: `has_more` indicates whether more pages exist. `body text (desc)`, `topics (tagList)`, `video stream URL`, and `exact publish timestamp (ms)` are NOT in this response — use the detail component below to obtain them. When `--keyword` is passed, matching is title-only (fuzzy); for title + body matching, omit `--keyword` and follow **AI Workflow: keyword search (title + body match)** below.

Error handling: if `error: true`, verify `wait stable` completed and the page is not a login gate. Reload and retry once.

### AI Workflow: keyword search (title + body match)

Run this workflow whenever a keyword is provided. It finds all notes where the keyword appears in either the **title** OR the **body text (desc)**.

**Step 1 — Extract all page results** (no `--keyword` flag):
```bash
python scripts/extract-search-feeds.py | browser-act --session <name> eval --stdin
```
→ `all_items` list (`total_count` items, no pre-filtering)

**Step 2 — Title filter** (in-memory, no extra requests):
- `title_matches` = items where `keyword` fuzzy-matches `title` (use same Levenshtein threshold as `--keyword`: `max(1, floor(len(keyword) * 0.2))` edits per word, case-insensitive, exact substring first)
- `candidates` = remaining items (ALL items not matched by title fuzzy match)
- Inform user: "Found {len(title_matches)} title match(es). Checking body text of {len(candidates)} candidates..."
- **CRITICAL: When `title_matches == 0`, do NOT stop. Zero title matches means body-text checking is MORE important, not less — the keyword may appear only in the body. Proceed to Step 3 unconditionally unless `total_count == 0`.**

**Step 3 — Body-text check** (detail page per candidate, skip only if `candidates` is empty):
For each item in `candidates`:
1. `browser-act --session <name> navigate https://www.xiaohongshu.com/explore/{id}?xsec_token={xsec_token}&xsec_source=pc_search`
2. `browser-act --session <name> wait stable`
3. `python scripts/extract-note-detail.py {id} | browser-act --session <name> eval --stdin`
4. If `keyword` fuzzy-matches (case-insensitive, same Levenshtein threshold) in `desc` → add to `body_matches`
5. Wait 2–3 seconds before next request.

**Step 4 — Report**:
- `final_results` = `title_matches` + `body_matches` (in original page order, deduplicated by `id`)
- Inform user: "{len(title_matches)} title match(es) + {len(body_matches)} body-only match(es) = {total} notes containing '{keyword}' (from {total_count} page results)"
- Clearly label each result: `match_type: "title"` or `match_type: "body"`

**Edge cases**:
- `title_matches == 0 AND body_matches == 0` → inform user: no notes found containing `{keyword}` in title or body text; suggest checking login status or trying a different keyword
- `total_count == 0` → inform user: no results at all; suggest checking login or trying a different keyword

### Network Capture: search notes list (fallback method)

Use as fallback only when the DOM feeds extraction above fails. Navigate to the search page and read results from the `so.xiaohongshu.com` API response captured in browser traffic.

**Important limitation**: the search API applies semantic expansion — for niche or brand-specific keywords, exact-match notes may be absent or pushed to later pages in the API response even when they appear prominently in the rendered page. Always prefer the DOM feeds method above.

1. `navigate https://www.xiaohongshu.com/search_result/?keyword={keyword}`
2. `wait stable`
3. (optional) Apply filters — see **AI Workflow: apply filters** below
4. `network requests --type xhr,fetch --filter so.xiaohongshu`
5. Identify the request with URL containing `/api/sns/web/v2/search/notes`
6. `network request <id>`
7. Parse `response_body` JSON — field paths: `data.items[n].id`, `data.items[n].xsec_token`, `data.items[n].note_card.display_title`, `data.items[n].note_card.interact_info.*`

Note: `data.has_more` indicates whether more pages exist.

Error handling: If no request matching `/api/sns/web/v2/search/notes` is found, check that `wait stable` completed and the page is a search result page (not a login gate). Reload the page and retry once.

### DOM: extract note detail (body, topics, video URL, exact timestamp)

Navigate to the note detail page and extract enriched fields from the Vue SSR state:

1. `navigate https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}&xsec_source=pc_search`
2. `wait stable`
3. `python scripts/extract-note-detail.py {note_id} | browser-act --session <name> eval --stdin`

Parameters:
- `{note_id}`: note ID from the search list result (`id` field)
- `{xsec_token}`: security token from the search list result (`xsec_token` field)

Output example:
```json
{
  "noteId": "694692cc000000001d039ea3",
  "title": "note title here",
  "desc": "note body text here",                // full body text
  "type": "video",                               // "normal" or "video"
  "time": 1766232780000,                         // exact publish timestamp (milliseconds)
  "ipLocation": "Fujian",                        // IP location, null if unavailable
  "userId": "59e9658411be10340721cd79",
  "nickname": "author nickname here",
  "avatar": "https://sns-avatar-qc.xhscdn.com/avatar/...",
  "likedCount": "0",
  "collectedCount": "0",
  "commentCount": "0",
  "shareCount": "0",
  "tagList": [
    {"name": "topic name", "type": "topic", "id": "123"}   // topics/hashtags
  ],
  "imageList": [
    {"url": "http://sns-webpic-qc.xhscdn.com/...", "width": 720, "height": 960}
  ],
  "videoUrl": "http://sns-video-v6.xhscdn.com/stream/1/110/259/..."   // null for image-text notes
}
```

Error handling: if `error: true` is returned, verify the page URL is a note detail page, `wait stable` has completed, and `note_id` matches the URL. If `noteDetailMap` is empty after wait, try `wait --selector ".note-content" --state attached --timeout 15000` then re-run the extraction.

### AI Workflow: apply filters (before search capture)

Run this workflow **before** step 4 of the search capture component when filters are needed. Open the filter panel and select desired options, then wait for the filtered search request to fire.

1. `state` — locate the "Filter" button (labeled with filter icon) in the top-right area of the search content area → `click <index>`
2. Wait for filter panel to appear (visible on the right side of the page)
3. For **sort order** — `state` locate the desired sort tag in the "Sort By" row → `click <index>`
4. For **note type** — `state` locate the desired type tag in the "Note Type" row → `click <index>`
5. For **publish time** — `state` locate the desired range tag in the "Publish Time" row → `click <index>`
6. For **search scope** — `state` locate the desired scope tag in the "Search Scope" row → `click <index>`
7. For **location distance** — `state` locate the desired distance tag in the "Location Distance" row → `click <index>`
8. `wait stable`
9. Proceed with `network requests --type xhr,fetch --filter so.xiaohongshu` to capture the filtered results

Filters are sent in the POST body `filters` array. Each filter entry has shape `{"type": "{filter_id}", "tags": ["{selected_value}"]}`. See Enum Parameters for all verified values.

### Composite: search + enrich (search list → detail page loop)

Use when full fields including body text, topics, video URL, and exact timestamp are needed for **all** notes regardless of keyword filtering. Also used as a sub-step in **AI Workflow: keyword search (title + body match)** for the body-text candidate checking phase.

1. Navigate to search page and extract feeds via DOM (preferred): `python scripts/extract-search-feeds.py | browser-act --session <name> eval --stdin`
2. Parse `items` array from result to get note list with `id` and `xsec_token`
3. For each note:
   a. `navigate https://www.xiaohongshu.com/explore/{id}?xsec_token={xsec_token}&xsec_source=pc_search`
   b. `wait stable`
   c. `python scripts/extract-note-detail.py {id} | browser-act --session <name> eval --stdin`
   d. Merge detail fields with feeds list fields (cover from feeds is higher resolution than detail page cover)
4. Save merged result per note

Recommended batch delay: 2–3 seconds between detail page requests to avoid anti-scraping triggers.

## Enum Parameters

Note: Some API parameter values below are platform-internal Chinese strings — they must be sent to the server exactly as shown (the server rejects English substitutes). All surrounding documentation text is English per Skill standards.

[AI] sort_type — `filters` array entry `{"type": "sort_type", "tags": ["{value}"]}`. Verified values from filter API response:

| UI Label | API Value (send as-is in `tags`) |
|---|---|
| General (default) | `general` |
| Latest | `time_descending` |
| Most Liked | `popularity_descending` |
| Most Commented | `comment_descending` |
| Most Collected | `collect_descending` |

[AI] filter_note_type — `filters` array entry `{"type": "filter_note_type", "tags": ["{value}"]}`. API values are platform-internal Chinese strings (non-substitutable):

| UI Label | API Value |
|---|---|
| All (default) | `不限` |
| Video | `视频笔记` |
| Image-text | `普通笔记` |

[AI] filter_note_time — `filters` array entry `{"type": "filter_note_time", "tags": ["{value}"]}`. API values are platform-internal Chinese strings:

| UI Label | API Value |
|---|---|
| All (default) | `不限` |
| Within 1 day | `一天内` |
| Within 1 week | `一周内` |
| Within 6 months | `半年内` |

[AI] filter_note_range — `filters` array entry `{"type": "filter_note_range", "tags": ["{value}"]}`. API values are platform-internal Chinese strings:

| UI Label | API Value |
|---|---|
| All (default) | `不限` |
| Seen | `已看过` |
| Unseen | `未看过` |
| Followed | `已关注` |

[AI] filter_pos_distance — `filters` array entry `{"type": "filter_pos_distance", "tags": ["{value}"]}`. API values are platform-internal Chinese strings:

| UI Label | API Value |
|---|---|
| All (default) | `不限` |
| Same city | `同城` |
| Nearby | `附近` |

Acquisition method for all enums: open filter panel via `state` + `click` on the Filter button, read filter option rows; or read directly from the `edith.xiaohongshu.com/api/sns/web/v1/search/filter?keyword={keyword}` GET response captured on initial page load.

## Pagination

**DOM Pagination** (search feeds): `scroll down --amount 3000` → `wait stable` → re-run `python scripts/extract-search-feeds.py | browser-act --session <name> eval --stdin` (result count accumulates as page loads more). Each scroll loads ~20 more results. Termination: `has_more` is `false` in extraction output.

**Network Capture Pagination** (fallback only): `scroll down --amount 3000` → `wait stable` → re-read `network requests --filter so.xiaohongshu` → `network request <id>` (new request will appear with `page` incremented). Termination: `data.has_more` is `false` in the latest response.

## Success Criteria

DOM feeds extraction: `result.count >= 1 AND result.items[0].id is non-null AND result.items[0].title is non-null`

For detail extraction: `result.noteId is non-null AND result.title is non-null`

## Known Limitations

- Search and detail extraction require login; without login the page shows a QR code overlay and returns no data
- `xsec_token` must correspond to the `note_id`; tokens from other sources result in redirect or empty state
- **Search API semantic expansion**: the `/v2/search/notes` API applies semantic query expansion — for niche or brand-specific keywords, exact-match notes may be absent from or pushed to later pages in the API response even when they appear prominently in the rendered page. The DOM feeds extraction (`extract-search-feeds.py`) reads `window.__INITIAL_STATE__.search.feeds` which mirrors exactly what the page renders, and is not affected by this limitation
- `publish_date` in feeds list gives a human-readable date string (e.g., `"2025-10-29"` or `"06-27"`) but not a precise timestamp — go to the detail page for the exact millisecond timestamp
- `filter_pos_distance` values for same-city and nearby require the browser's location permission to be enabled; without permission these filters may return empty results
- Body text (`desc`) and topics (`tagList`) are only available from the detail page SSR state, not from the search feeds list
- Video stream URLs contain time-limited signed tokens (`sign=...&t=...`) — links expire; re-navigate to generate fresh URLs

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/xiaohongshu-search-full-xiaohongshu-search-full.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
