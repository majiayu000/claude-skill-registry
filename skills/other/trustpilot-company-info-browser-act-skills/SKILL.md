---
name: trustpilot-company-info
description: "Trustpilot company profile lookup on trustpilot.com — input a company domain (e.g. apple.com, shopify.com, shopwagandtail.com) and extract company metadata: official display name, businessUnitId, TrustScore (1-5), star rating, total review count, last-12-months review count, primary category and all categories, verification flags (verifiedByGoogle, verifiedPaymentMethod, verifiedUserIdentity), claimed/closed status, website URL, contact info (email, phone, country, city, address, zip), profile image, and optional reply behavior metrics (averageDaysToReply, replyPercentage, negativeReviewsWithRepliesCount, companyUsesAIResponses). Detects company-not-found and returns isCompanyFound=false with the searched domain. Use when user mentions Trustpilot company info, Trustpilot TrustScore, look up Trustpilot rating, check Trustpilot stars, Trustpilot business profile, Trustpilot review count, Trustpilot company lookup, Trustpilot verification status, Trustpilot reply percentage, Trustpilot AI responses, business unit ID Trustpilot, get company rating from Trustpilot, scrape Trustpilot company, batch enrich domains with Trustpilot, bulk company info Trustpilot, fast domain enrichment with TrustScore, Trustpilot company metadata, Trustpilot brand monitoring, competitor TrustScore comparison, trustpilot.com domain enrichment, trustpilot company profile, trustpilot domain check, trustpilot business listing, check if company is on Trustpilot, Trustpilot category lookup, company contact info from Trustpilot. Also applies to lead-list enrichment with reputation scores, supplier vetting, agency or KOL vetting via review reputation, aggregator sites that need TrustScores for many domains, due-diligence workflows, and pre-outreach reputation checks."
---

# Trustpilot — Company Info

> Input a company domain (or list of domains) → output the company's Trustpilot profile: name, TrustScore, stars, review count, verification flags, category, contact info, and optional reply behavior metrics.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract a single company's public Trustpilot profile data from `trustpilot.com/review/{domain}`. Designed to be called once per domain; chain calls or write a batch loop when enriching many domains.

## Prerequisites

- Target page is reachable on the public web: `https://www.trustpilot.com/review/{domain}`
- No login required — Trustpilot review pages are publicly accessible

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### DOM: extract company profile (from SSR JSON embedded in the review page)

The Trustpilot review page is server-rendered with Next.js; the complete businessUnit record is embedded in `<script id="__NEXT_DATA__">`. Extraction reads this script directly — no separate API call required.

Steps:
1. `navigate https://www.trustpilot.com/review/{domain}` (replace `{domain}` with the company domain, e.g. `apple.com`, `shopwagandtail.com`)
2. `wait stable --timeout 30000`
3. `eval "$(python scripts/extract-company-info.py)"` — basic profile
4. `eval "$(python scripts/extract-company-info.py --include-response-metrics)"` — also include reply behavior + AI response flag

Parameters:
- `--include-response-metrics` (optional flag): adds `replyAverageDaysToReply`, `replyPercentage`, `totalNegativeReviewsCount`, `negativeReviewsWithRepliesCount`, `lastReplyToNegativeReview`, `companyUsesAIResponses`, `claimedDate`, `isAskingForReviews` to the output.

Output example (company found, with `--include-response-metrics`):
```json
{
  "isCompanyFound": true,                                    // false when domain has no Trustpilot page
  "company": "Wag + Tail",                                   // display name
  "businessUnitId": "624c24851220e2743a4d7916",              // Trustpilot internal ID
  "identifyingName": "shopwagandtail.com",                   // canonical domain on Trustpilot
  "rating": "4.7",                                           // TrustScore as string
  "trustScoreNumeric": 4.7,                                  // TrustScore as number
  "stars": 4.5,                                              // visual star rating
  "OfficialTotalReviewCount": 258,                           // total reviews (may include hidden)
  "numberOfReviewsLast12Months": 1,                          // rolling 12-month review count
  "isCompanyVerified": "yes",                                // "yes" if any verification flag is true, else "no"
  "verificationFlags": {                                     // breakdown of verification sources
    "verifiedByGoogle": false,
    "verifiedPaymentMethod": false,
    "verifiedUserIdentity": true
  },
  "isClaimed": true,                                         // claimed by the business owner
  "isClosed": false,
  "isTemporarilyClosed": false,
  "isCollectingReviews": false,
  "category": "Pet Store",                                   // primary category name
  "categoryId": "pet_store",
  "allCategories": [{ "id": "pet_store", "name": "Pet Store", "isPrimary": true }],
  "websiteUrl": "https://shopwagandtail.com",
  "websiteTitle": "shopwagandtail.com",
  "profileImageUrl": "//s3-eu-west-1.amazonaws.com/tpd/logos/624c24851220e2743a4d7916/0x0.png",
  "contactEmail": "sales@shopwagandtail.com",                // may be null
  "contactPhone": null,
  "contactCountry": "US",
  "contactCity": null,
  "contactAddress": null,
  "contactZipCode": null,
  "locationsCount": 0,
  "companyPageUrl": "https://www.trustpilot.com/review/shopwagandtail.com",
  "scrapedDateTime": "2026-06-26T04:12:17.272Z",
  "replyAverageDaysToReply": 0,                              // only when --include-response-metrics
  "replyPercentage": 0,
  "totalNegativeReviewsCount": 0,
  "negativeReviewsWithRepliesCount": 0,
  "lastReplyToNegativeReview": null,
  "companyUsesAIResponses": false,
  "claimedDate": "2022-04-05T13:54:41.000Z",
  "isAskingForReviews": false
}
```

Output example (company not found on Trustpilot):
```json
{
  "isCompanyFound": false,
  "companyPageUrl": "https://www.trustpilot.com/review/nonexistent-xyz-9999.com",
  "searchedDomain": "nonexistent-xyz-9999.com",
  "scrapedDateTime": "2026-06-26T04:13:45.151Z"
}
```

Error handling: when the `__NEXT_DATA__` script tag is missing or `businessUnit` is absent for a non-404 page, the script returns `{"error": true, "message": "..."}`. If this happens, confirm the page loaded fully (`wait stable`), then re-run. If the page is rate-limited or shows an anti-bot challenge, switch to a stealth browser with proxy and retry.

## Success Criteria

`isCompanyFound === true && company !== null && OfficialTotalReviewCount !== null && trustScoreNumeric !== null` — for an existing company; `isCompanyFound === false && searchedDomain !== null` — for a not-found domain.

## Known Limitations

- `OfficialTotalReviewCount` is Trustpilot's official count and may include reviews currently hidden by Trustpilot's filtering (deleted, flagged, machine-filtered). This is a platform-level characteristic, not a script bug.
- Reply behavior metrics (`replyAverageDaysToReply`, `replyPercentage`, etc.) reflect only negative-review replies on Trustpilot's `activity.replyBehavior` block; positive-review replies are not tracked separately.
- Some companies have empty `contactInfo` fields (phone/address/city/zipCode null) — Trustpilot only surfaces what the business has filled in.
- `numberOfReviewsLast12Months` represents the rolling 12-month window the page advertises; rerunning months later returns a different number naturally.

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through domains serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/trustpilot-reviews-scraper-trustpilot-company-info.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
