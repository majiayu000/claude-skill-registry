---
name: google-search-serp
description: "Extracts Google Search results page (SERP) data including organic results, paid ads, related searches, People Also Ask questions, AI Overview text, and total result count from google.com. Use when user mentions Google search results, SERP scraping, google search data, search engine results page, organic rankings, keyword SERP, Google SERP extraction, scrape Google search, Google search API alternative, SEO ranking data, paid search ads, PPC ads on Google, Google search monitoring, keyword research, search results export, check Google rankings, what shows up on Google, search engine scraper, google results checker."
---

# Google — Search SERP Extraction

> Search keyword + parameters → structured SERP data (organic results, ads, related queries, PAA, AI Overview)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract all visible content from a Google Search results page: organic listings, paid ads, related searches, People Also Ask, AI Overview, and total result count.

## Prerequisites

- Target page is already open in the browser: `https://www.google.com/search?q={query}`

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### DOM: Google Search SERP (data extraction)

Parameters are injected via URL navigation; data is extracted from the server-rendered HTML page:

1. `navigate https://www.google.com/search?q={query}&num={num}&hl={lang}&gl={country}&start={start}`
2. `wait stable`
3. `eval "$(python scripts/serp-extract.py)"`

URL parameters:
- `q`: Search query (required)
- `num`: Results per page — `10` (default), `20`, `50`, `100`
- `hl`: Interface language code — e.g., `en`, `zh-CN`, `fr`, `de` (omit for browser default)
- `gl`: Country targeting code — e.g., `us`, `gb`, `de`, `cn` (omit for browser default)
- `start`: Pagination offset — `0` for page 1, `10` for page 2 (when `num=10`); formula: `(page - 1) * num`

Error handling: If extraction returns `{"error": true, "message": "captcha required"}`, the session is blocked by Google — switch to a browser with a US rotating proxy and retry. If `"No search results found"` is returned, run `screenshot` to verify the page loaded correctly before retrying.

Output example:
```json
{
  "searchQuery": {
    "term": "machine learning",
    "url": "https://www.google.com/search?q=machine+learning",
    "device": "DESKTOP",
    "page": 1,
    "type": "SEARCH",
    "domain": "www.google.com",
    "countryCode": "US",
    "languageCode": "en"
  },
  "resultsTotal": "14900000000",
  "organicResults": [
    {
      "position": 1,
      "type": "organic",
      "title": "Machine learning - Wikipedia",
      "url": "https://en.wikipedia.org/wiki/Machine_learning",
      "displayedUrl": "en.wikipedia.org › wiki › Machine_learning",
      "description": "Machine learning (ML) is a field of study in artificial intelligence...",
      "emphasizedKeywords": ["machine learning", "ML"],
      "siteLinks": [
        {"title": "Supervised learning", "url": "https://en.wikipedia.org/wiki/Supervised_learning"}
      ]
    }
  ],
  "paidResults": [
    {
      "adPosition": 1,
      "type": "paid",
      "title": "Learn Machine Learning Online",
      "url": "https://example.com/ml-course",
      "displayedUrl": "example.com",
      "description": null,
      "siteLinks": []
    }
  ],
  "relatedQueries": [
    {"title": "machine learning examples", "url": "https://www.google.com/search?q=machine+learning+examples"}
  ],
  "peopleAlsoAsk": [
    {"question": "What is machine learning used for?"}
  ],
  "aiOverview": null
}
```

Field notes:
- `resultsTotal`: total result count string (commas removed), `null` when stat bar is absent
- `organicResults[*].emphasizedKeywords`: bold/italic terms in the description, empty array when none
- `organicResults[*].siteLinks`: sub-links shown under some results, empty array when none
- `paidResults[*].description`: ad description text, `null` when the advertiser omits it
- `aiOverview`: AI Overview paragraph text joined with spaces, `null` when absent or unavailable

## Pagination

**URL Pagination**: URL pattern `https://www.google.com/search?q={query}&num={num}&start={(page-1)*num}`. Increment `start` by `num` for each subsequent page. Termination: `organicResults` array is empty, or `start` exceeds the desired page count.

## Success Criteria

`organicResults.length >= 1` and `searchQuery.term` matches the requested keyword.

## Known Limitations

- **AI Overview unreliable in stealth sessions**: Google rarely serves AI Overview to automated browsers. `aiOverview` will be `null` in most sessions; it only populates when Google serves it without login or cookie context.
- **Paid ad descriptions often null**: Many ads omit a description block — `paidResults[*].description` returns `null` for those. This reflects the advertiser's choice, not an extraction failure.
- **Google anti-bot detection**: Stealth browsers may be redirected to a CAPTCHA (`/sorry/` page). Use a browser session with a US rotating proxy to reduce blocks. Solve any CAPTCHA manually via `remote-assist` if needed.
- **Related queries load asynchronously**: `relatedQueries` requires `wait stable` after navigation; results may be empty if the page has not fully settled.

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through keywords serially within one browser session; add a 2–5 second delay between requests to avoid triggering rate limits.
- **Test before batch execution**: After writing a batch script, test with 1–2 keywords first to verify it runs correctly; only then run the full batch.
- **Reduce redundant pre-operations**: Reuse the same browser session across multiple keywords — navigate directly to each search URL without returning to the homepage.
- **Error resumption**: Save results keyword by keyword; on CAPTCHA or failure, resume from the breakpoint rather than starting over.
- **Multi-session parallelism**: To increase throughput, open multiple stealth browser sessions (each with its own proxy fingerprint) and distribute keywords across them.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/google-search-scraper-google-search-serp.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
