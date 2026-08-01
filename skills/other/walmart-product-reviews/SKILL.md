---
name: walmart-product-reviews
description: "Walmart product reviews scraper: given a walmart.com product item ID, navigate to the reviews page and extract paginated customer reviews including reviewId, rating, title, review text, author nickname, submission date, verified purchase status, helpful votes, variant selected (color/size), badges, fulfilled by, seller name, and photo count. Use when user mentions walmart reviews, walmart product reviews, walmart customer reviews, scrape walmart reviews, extract walmart reviews, walmart review scraper, walmart ratings and reviews, walmart review data, walmart review text, walmart review pagination, get reviews from walmart, walmart review collector, walmart verified purchase reviews, walmart review analysis, walmart sentiment analysis, walmart review export, walmart buyer feedback. Also applies to bulk collection of walmart product reviews across multiple items, sentiment analysis on walmart reviews for market research, competitor product review benchmarking on walmart, and monitoring new walmart reviews over time."
---

# Walmart — Product Reviews

> product item ID + page → paginated customer reviews from walmart.com

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract paginated customer reviews from a Walmart product reviews page, returning structured review data with ratings, text, author info, and metadata.

## Prerequisites

- Target reviews page is open in the browser: `https://www.walmart.com/reviews/product/{item-id}?page={page}`

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### DOM: extract reviews from current reviews page

Navigate to the target reviews URL first, then extract:

1. `navigate "https://www.walmart.com/reviews/product/{item-id}?page={page}"`
2. `wait stable`
3. `eval "$(python scripts/extract-reviews.py)"`

Parameters in URL:
- `{item-id}`: Walmart item ID (numeric, e.g., `18656507313`)
- `{page}`: page number starting from `1`; 10 reviews per page

Note: The `walmart-product-detail` Skill also returns the first 10 reviews in its `reviewSummary.reviewsLookupId` field along with `numberOfReviews`. Use these to determine total pages before starting pagination.

Output example:
```json
{
  "totalReviews": 279,
  "averageRating": 4.2,
  "reviewsOnPage": 10,
  "ratingBreakdown": {
    "5": 191,
    "4": 29,
    "3": 15,
    "2": 10,
    "1": 34
  },
  "lookupId": "19X7KSSCUQU5",
  "reviews": [
    {
      "reviewId": "431060075",
      "rating": 5,
      "title": null,
      "text": "Purchased for adult daughter's bday! She loves it...",
      "author": "kimberly",
      "submittedDate": "7/4/2026",
      "verifiedPurchase": true,
      "helpfulVotes": 0,
      "notHelpfulVotes": 0,
      "variantSelected": {"Color": "Tranquil pink"},
      "badges": ["Verified Purchase"],
      "fulfilledBy": "Walmart",
      "sellerName": "Walmart.com",
      "media": null
    }
  ]
}
```

Error response (when extraction fails or wrong page):
```json
{"error": true, "message": "No reviews in __NEXT_DATA__. Ensure the page is a Walmart reviews page (walmart.com/reviews/product/...) or product detail page with reviews."}
```

## Pagination

**URL Pagination**: URL pattern `https://www.walmart.com/reviews/product/{item-id}?page={N}`. Start at page 1. Increment page by 1 each iteration. Termination: `reviewsOnPage === 0` OR `page > ceil(totalReviews / 10)`. Each page returns 10 reviews.

## Success Criteria

`reviewsOnPage >= 1` AND `reviews[0].reviewId` is non-null AND `reviews[0].rating` is a number between 1 and 5

## Known Limitations

- 10 reviews per page; Walmart does not expose an API to change page size
- `title` is null for most reviews that do not have a title
- `media` (photo URLs) is null for most text-only reviews; photo URLs are not included in `__NEXT_DATA__` for reviews with photos — only a count is available
- `variantSelected` is null when the reviewer did not select a specific variant
- Review ordering defaults to most recent; sort order cannot be changed via URL parameter

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through pages serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Add 1–2 second intervals between page navigations. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 pages to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results page by page during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/walmart-scraper-walmart-product-reviews.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what products were reviewed or what ratings were found — those are task outputs, not experience.
