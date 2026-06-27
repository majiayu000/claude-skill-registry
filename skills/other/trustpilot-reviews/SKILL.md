---
name: trustpilot-reviews
description: "Trustpilot customer reviews scraper for any company listed on trustpilot.com — given a company domain (e.g. shopify.com, apple.com, shopwagandtail.com) plus optional filters (page number, single star rating 1-5, single language ISO code, verified-only flag, has-company-reply flag, date period last30days/last3months/last6months/last12months, free-text keyword search, and reviewer countryCode client-side filter), extracts paginated reviews with 20+ fields per review: reviewId, reviewUrl, reviewTitle, reviewDescription, reviewRatingScore (1-5), reviewDate (ISO publishedDate), reviewDateOfExperience, reviewLabel, isReviewVerified, reviewer (display name), reviewerId, reviewersCountry (ISO Alpha-2), reviewLanguage, reviewCompanyResponse (the company reply text), plus pagination metadata (currentPage, totalPages, totalCount). Optional flags add reviewer profile metadata (reviewerNumberOfReviews, reviewerProfileIsVerified), reply analysis dates (companyReplyPublishedDate, companyReplyUpdatedDate), extended metadata (reviewSource, reviewVerificationSource, reviewLikes), and review photos. Use when user mentions Trustpilot reviews, scrape Trustpilot, get reviews from Trustpilot, Trustpilot review scraper, Trustpilot customer reviews, extract Trustpilot reviews, Trustpilot review data, download Trustpilot reviews, paginate Trustpilot, paginated Trustpilot reviews, filter Trustpilot reviews by star, filter Trustpilot by language, verified reviews Trustpilot, has reply Trustpilot, company response Trustpilot, Trustpilot reply analysis, brand monitoring Trustpilot, sentiment analysis Trustpilot, competitor reviews Trustpilot, bulk reviews from a Trustpilot page, batch download reviews, trustpilot.com reviews scraping, fake review research Trustpilot, Trustpilot dataset, persona research from Trustpilot reviews, Trustpilot keyword search reviews, Trustpilot date range reviews, review export Trustpilot. Also applies to comparing review trends across competitors, training data for LLM sentiment classifiers, monitoring competitor response time, exporting reviews for BI dashboards, lead generation from active reviewers, ML / fake-review detection, and aggregator sites that display third-party reviews."
---

# Trustpilot — Reviews

> Input a company domain plus optional filters → output paginated review records with reviewer info, ratings, dates, company replies, and 20+ structured fields per review.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract one page of customer reviews from `trustpilot.com/review/{domain}` with the chosen filters applied. Designed to be called in a loop across pages to collect the full filtered review set.

## Prerequisites

- Target page is reachable on the public web: `https://www.trustpilot.com/review/{domain}`
- No login required — Trustpilot review pages are publicly accessible

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### URL Pattern (server-side filters)

Trustpilot accepts filter values as URL query parameters. Build the URL before navigating:

```
https://www.trustpilot.com/review/{domain}?page={page}&languages={lang}&sort=recency&stars={stars}&verified={true|false}&replies={true|false}&date={period}&search={keyword}
```

All parameters except `domain` are optional. Recommended construction rules:
- `page`: integer ≥ 1 (omit for page 1; pagination defaults to 20 per page)
- `languages`: single ISO code (e.g. `en`, `da`, `de`, `es`, `fr`); omit or use `all` for no language filter
- `sort`: only `recency` is currently honoured by the public review page (older `relevancy` values are stripped on redirect)
- `stars`: single value `1`, `2`, `3`, `4`, or `5` — only one star tier can be selected
- `verified`: `true` to keep only verified reviews
- `replies`: `true` to keep only reviews that received a company response
- `date`: one of `last30days`, `last3months`, `last6months`, `last12months`
- `search`: URL-encoded keyword to search inside review text

Country-of-reviewer filtering is **not supported by Trustpilot's URL** — it is applied client-side after extraction using `--filter-country` (see below).

### DOM: extract reviews from current page (SSR JSON)

The Trustpilot review page is server-rendered with Next.js; the full reviews array is embedded in `<script id="__NEXT_DATA__">`. Extraction reads it directly — no separate API call needed.

Steps:
1. Build the URL as described above.
2. `navigate {built-url}`
3. `wait stable --timeout 30000`
4. `eval "$(python scripts/extract-reviews.py [options])"`

Parameters (all optional flags / values):
- `--include-reviewer-metadata`: adds `reviewerNumberOfReviews`, `reviewerProfileIsVerified`.
- `--include-reply-analysis`: adds `companyReplyPublishedDate`, `companyReplyUpdatedDate` (null when no reply).
- `--include-extended-metadata`: adds `reviewSource` (e.g. `Organic`, `Shopify`, `InvitationApi`), `reviewVerificationSource` (e.g. `invitation`, `complianceDocumentation`), `reviewLikes`.
- `--include-review-photos`: adds `reviewPhotoUrls` array via best-effort DOM scan of the review card; returns `[]` when no photos.
- `--no-experience-date`: omit the default `reviewDateOfExperience` field.
- `--filter-country {ISO2}`: client-side filter — keep only reviews whose reviewer `countryCode` matches the given ISO Alpha-2 code (e.g. `US`, `GB`, `DK`). Case-insensitive. Applied after the page-level filters from the URL.

Output example (one page, with all optional flags):
```json
{
  "reviews": [                                              // array of review objects (≤ perPage items)
    {
      "companyName": "Wag + Tail",
      "companyPageUrl": "https://www.trustpilot.com/review/shopwagandtail.com?page=1&languages=en",
      "businessUnitId": "624c24851220e2743a4d7916",         // Trustpilot internal company ID
      "reviewId": "65fd6a055de8c560404349e1",
      "reviewUrl": "https://www.trustpilot.com/reviews/65fd6a055de8c560404349e1",
      "reviewTitle": "Great product looks so cute on my girl",
      "reviewDescription": "Great product looks so cute on my girl and fits so well",
      "reviewRatingScore": 5,                                // 1-5
      "reviewDate": "2024-03-22T13:22:45.000Z",              // when review was posted
      "reviewLabel": "verified",                             // "verified" or "not-verified"
      "isReviewVerified": true,
      "reviewer": "Angela Rosalie",
      "reviewerId": "656cc367ad3fb4001307cba8",
      "reviewersCountry": "US",                              // ISO Alpha-2
      "reviewLanguage": "en",
      "reviewCompanyResponse": "",                           // empty string when no reply
      "scrapedDateTime": "2026-06-26T04:13:03.026Z",
      "scrapedAtReviewPageNumber": 1,
      "reviewDateOfExperience": "2024-01-27T00:00:00.000Z",  // default; remove with --no-experience-date
      "reviewerNumberOfReviews": 2,                          // --include-reviewer-metadata
      "reviewerProfileIsVerified": false,                    // --include-reviewer-metadata
      "companyReplyPublishedDate": null,                     // --include-reply-analysis (null when no reply)
      "companyReplyUpdatedDate": null,                       // --include-reply-analysis
      "reviewSource": "Shopify",                             // --include-extended-metadata
      "reviewVerificationSource": "invitation",              // --include-extended-metadata
      "reviewLikes": 0,                                      // --include-extended-metadata
      "reviewPhotoUrls": []                                  // --include-review-photos
    }
  ],
  "pagination": {
    "currentPage": 1,
    "perPage": 20,
    "totalPages": 12,
    "totalCount": 231                                        // total reviews matching the active filters
  },
  "activeFilters": {                                         // what Trustpilot actually applied (after URL normalization)
    "languages": "en",
    "sort": "recency",
    "stars": null,
    "verified": false,
    "replies": false,
    "date": null,
    "search": null,
    "countryFilter": null                                    // mirrors --filter-country when set
  },
  "companyContext": {                                        // company snapshot for joining with company-info output
    "businessUnitId": "624c24851220e2743a4d7916",
    "companyName": "Wag + Tail",
    "identifyingName": "shopwagandtail.com",
    "trustScore": 4.7,
    "stars": 4.5,
    "totalReviews": 258
  },
  "totalFiltered": 231,                                      // duplicate of pagination.totalCount, kept for clarity
  "scrapedDateTime": "2026-06-26T04:13:03.026Z",
  "isCompanyFound": true
}
```

Output example (company not found):
```json
{
  "isCompanyFound": false,
  "companyPageUrl": "https://www.trustpilot.com/review/nonexistent-xyz-9999.com",
  "searchedDomain": "nonexistent-xyz-9999.com",
  "scrapedDateTime": "2026-06-26T04:13:45.151Z",
  "reviews": [],
  "pagination": null
}
```

Error handling: when the script fails to find `__NEXT_DATA__` or `businessUnit` (and the page is not the 404 page) it returns `{"error": true, "message": "..."}`. Resolution sequence: (1) confirm `wait stable` finished; (2) re-run the extraction; (3) if Trustpilot served an anti-bot challenge, switch to a stealth browser with proxy and retry once.

## Enum Parameters

[DOM] `languages` — read from the `__NEXT_DATA__` SSR data on any Trustpilot review page:
```
eval "(() => { const s=document.querySelector('script#__NEXT_DATA__'); const d=JSON.parse(s.textContent); const langs=d.props.pageProps.filters.reviewStatistics.reviewLanguages; return JSON.stringify(langs.map(l => ({ code: l.isoCode, name: l.displayName, count: l.reviewCount }))); })()"
```
Each entry: `{ code, name, count }`. The literal `all` is also accepted as the URL value to disable the language filter.

[Static] `sort`: `recency` (currently the only honoured value on the public review page; older `relevancy` is stripped on redirect).

[Static] `stars`: `1`, `2`, `3`, `4`, `5` — only one value at a time.

[Static] `date`: `last30days`, `last3months`, `last6months`, `last12months`.

[Static] `verified`, `replies`: `true` or `false`.

[Static] `filterByCountryOfReviewers`: any ISO Alpha-2 country code (e.g. `US`, `GB`, `DE`, `DK`). Applied client-side via `--filter-country`.

## Pagination

**URL Pagination**: URL pattern `https://www.trustpilot.com/review/{domain}?page={N}&{otherFilters}`. Next page = increment `page` by 1. Termination conditions: (a) `pagination.currentPage >= pagination.totalPages`, OR (b) `reviews.length === 0` on the current page, OR (c) caller-supplied `endAtPageNumber` reached.

Recommended loop pattern (bash):
```
PAGE=1
END=0   # 0 means "until totalPages"
while : ; do
  URL="https://www.trustpilot.com/review/${DOMAIN}?page=${PAGE}&languages=en&sort=recency"
  browser-act --session {S} navigate "$URL"
  browser-act --session {S} wait stable --timeout 30000
  RESP=$(browser-act --session {S} eval "$(python scripts/extract-reviews.py --include-extended-metadata)")
  # append RESP.reviews to a JSONL file
  TOTAL=$(echo "$RESP" | python -c "import sys,json; print(json.loads(sys.stdin.read())['pagination']['totalPages'])")
  PAGE=$((PAGE+1))
  if [ "$PAGE" -gt "$TOTAL" ]; then break; fi
  if [ "$END" -gt 0 ] && [ "$PAGE" -gt "$END" ]; then break; fi
  sleep 2
done
```

## Success Criteria

`isCompanyFound === true && Array.isArray(reviews) && pagination.currentPage === expected_page && (reviews.length > 0 || pagination.totalCount === 0)` — for an existing company; `isCompanyFound === false && searchedDomain !== null && reviews.length === 0` — for a not-found domain.

## Known Limitations

- Trustpilot caps URL filters to **one star tier** and **one language code** per request — combining multiple values is not supported by the public URL and silently stripped on redirect.
- `sort=relevancy` is no longer honoured on the public review page; only `recency` is applied. Build URLs accordingly.
- `filterByCountryOfReviewers` is **client-side only**: a page may return up to `perPage` reviews of which fewer match the country filter, so the returned list per page can be sparse. To collect a fixed-size sample by country, page deeper or remove other restrictive filters.
- `pagination.totalCount` represents reviews after server-side filters and may differ from `companyContext.totalReviews` (Trustpilot's official count may include hidden / machine-filtered reviews).
- `reviewPhotoUrls` is best-effort: Trustpilot does not consistently expose review photos in the SSR JSON, so the script falls back to scanning known photo-host URL patterns inside the review card DOM. Reviews without photos return `[]`; some valid photos may be missed on layout changes.
- Trustpilot redirects `page=1` to the bare URL — `pagination.currentPage` still reports `1`, so callers should trust that field rather than the URL.
- Very large companies (thousands of reviews) may take many pages; budget at least one hour of wall-clock time for full-set extraction and consider rotating sessions if rate-limited.

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through pages serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/trustpilot-reviews-scraper-trustpilot-reviews.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
