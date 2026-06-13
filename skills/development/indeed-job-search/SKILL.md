---
name: indeed-job-search
description: "Scrape job listings from Indeed.com by keyword, location, and country. Returns job title, company, salary, rating, description, benefits, and apply links. Use when user mentions Indeed, Indeed scraper, Indeed jobs, scrape Indeed, job search Indeed, Indeed job listings, extract Indeed data, Indeed job data, get jobs from Indeed, Indeed employment data, job market research Indeed, Indeed salary data, bulk job extraction Indeed, Indeed job scraper, monitor Indeed listings, Indeed hiring data, job postings Indeed, Indeed career search. Also applies to: job market analysis, salary benchmarking from Indeed, competitor hiring monitoring, recruitment data collection, building job databases from Indeed search results."
---

# Indeed — Job Search

> keyword + location + country → structured job listing data (title, company, salary, description, benefits, apply link)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract structured job listing data from Indeed search results including full job descriptions, salary information, company details, and application links.

## Prerequisites

- Target page is already open in the browser: `https://www.indeed.com/jobs?q={keyword}&l={location}`
- For pagination beyond page 1: user must be logged into Indeed (login/sign-in button is NOT visible, user avatar or account menu IS visible)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification (for pagination beyond page 1)

If login status for Indeed has been confirmed in the current session → skip this step.

Otherwise: open Indeed and observe the page login status:
- Sign out entry, user avatar, or account menu exists → logged in, continue execution
- Sign in/Register entry exists with no sign out entry → not logged in, inform the user that login is needed for pagination beyond page 1, assist the user in completing the login flow

User refuses or cannot log in → can still extract page 1 results (up to 24 jobs per search), but cannot paginate.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### API: Extract job list from search results page

`eval "$(python scripts/search-jobs.py --max-items {max_items})"`

Parameters:
- --max-items: Maximum number of items to return from current page, 0 for all (default: 0)

Prerequisites: Browser must be on an Indeed search results page (`indeed.com/jobs?q=...`). Navigate first:
1. `navigate https://www.indeed.com/jobs?q={keyword}&l={location}` (add `&start={offset}` for pagination)
2. `wait stable`
3. If page title contains "Security Check" → `solve-captcha` → `wait stable`

Output example:
```json
{
  "pageNumber": 1,
  "totalResults": 24,
  "results": [
    {
      "id": "8c06afbaf73fc880",
      "positionName": "Software Engineer",
      "company": "Google",
      "location": "San Francisco, CA",
      "postedAt": "3 days ago",
      "salary": "$120,000 - $180,000 a year",
      "salaryMin": 120000,
      "salaryMax": 180000,
      "salaryCurrency": "USD",
      "salaryType": "YEARLY",
      "jobType": ["Full-time"],
      "rating": 4.3,
      "reviewsCount": 15000,
      "companyLogo": "https://d2q79iu7y748jz.cloudfront.net/s/_squarelogo/256x256/...",
      "snippet": "<ul>...<b>software</b>...</ul>",
      "sponsored": false,
      "expired": false,
      "newJob": true,
      "url": "https://www.indeed.com/viewjob?jk=8c06afbaf73fc880",
      "externalApplyLink": null
    }
  ]
}
```

### API: Fetch full job detail by job key

`eval "$(python scripts/fetch-job-detail.py '{jobkey}')"`

Parameters:
- jobkey: Indeed job key (the `id` field from search results)

Prerequisites: Browser must be on the same Indeed search results page where the job was found (the fetch uses same-origin cookies). Do NOT navigate away between search and detail fetch.

Output example:
```json
{
  "id": "a39828c8395d5dfe",
  "positionName": "Sr. Application Developer",
  "company": "University of California San Francisco",
  "location": "San Francisco, CA 94158",
  "rating": 4,
  "reviewsCount": 709,
  "companyLogo": "https://d2q79iu7y748jz.cloudfront.net/s/_squarelogo/256x256/...",
  "salary": "$101,300 - $190,000 a year",
  "salaryMin": 101300,
  "salaryMax": 190000,
  "salaryCurrency": "USD",
  "salaryType": "YEARLY",
  "jobType": "Full-time",
  "description": "<p><b>Job Description:</b></p><p>...(full HTML)...</p>",
  "benefits": ["Health insurance", "401(k)", "Dental insurance"],
  "postedAt": "13 days ago",
  "isExpired": false, "url": "https://www.indeed.com/viewjob?jk=a39828c8395d5dfe"
}
```

### Composite: Full job search with descriptions

Complete workflow to extract job listings with full descriptions:

1. `navigate https://www.indeed.com/jobs?q={keyword}&l={location}` → `wait stable`
2. If title contains "Security Check" → `solve-captcha` → `wait stable`
3. `eval "$(python scripts/search-jobs.py)"` → get job list with IDs
4. For each job `id` from step 3:
   - `eval "$(python scripts/fetch-job-detail.py '{id}')"` → get full description
5. Merge: search results provide base data, detail fetch adds `description`, `benefits`, enriched `salary`/`rating`

For pagination (requires login):
- Repeat steps 1-4 with `&start=10`, `&start=20`, `&start=30`, etc.
- Termination: when search-jobs.py returns fewer results than expected or `error: true`

Output: Combined array where each item has all fields from both search-jobs and fetch-job-detail.

## Enum Parameters

[API] country — supported country codes for Indeed search (append to URL as domain variant `https://{country-domain}/jobs?q=...`):

| Code | Domain | Country |
|------|--------|---------|
| US | www.indeed.com | United States |
| GB | uk.indeed.com | United Kingdom |
| CA | ca.indeed.com | Canada |
| AU | au.indeed.com | Australia |
| IN | in.indeed.com | India |
| DE | de.indeed.com | Germany |
| FR | fr.indeed.com | France |
| JP | jp.indeed.com | Japan |
| BR | br.indeed.com | Brazil |
| MX | mx.indeed.com | Mexico |
| SG | sg.indeed.com | Singapore |
| NL | nl.indeed.com | Netherlands |
| IT | it.indeed.com | Italy |
| ES | es.indeed.com | Spain |
| SE | se.indeed.com | Sweden |
| CH | ch.indeed.com | Switzerland |
| HK | hk.indeed.com | Hong Kong |
| KR | kr.indeed.com | South Korea |
| PL | pl.indeed.com | Poland |
| AT | at.indeed.com | Austria |
| BE | be.indeed.com | Belgium |
| NZ | nz.indeed.com | New Zealand |

For other countries, use format: `{country-code-lowercase}.indeed.com`

## Pagination

**URL Pagination**: Parameter `start`, type: page-number (offset-based). Start value: `0` (page 1, implicit). Next page: increment by 10 (`start=10`, `start=20`, `start=30`...). Termination: search-jobs.py returns `error: true` with message about no results, or returns fewer than expected items. Note: each page actually returns ~15-24 items despite the offset increment of 10.

**Login requirement**: Page 2+ (`start=10` and above) redirects to `secure.indeed.com/auth` if not logged in.

## Success Criteria

- `result count >= 1` from search-jobs.py
- Core fields non-null: `id`, `positionName`, `company`, `location` present for all results
- `description` field from fetch-job-detail.py is non-null HTML string with length > 100
- Data matches page content (job titles correspond to visible listings)

## Known Limitations

- Pagination beyond page 1 requires Indeed login (unauthenticated access limited to first page, ~24 results)
- Indeed may trigger captcha/security check on first visit; `solve-captcha` resolves this
- Job detail fetch (`fetch-job-detail.py`) must execute from within the search results page context (same-origin requirement)
- Indeed's anti-bot detection may block access after excessive requests; use appropriate intervals (2-5 seconds between detail fetches)
- Some fields (salary, jobType, benefits) may be null when not provided by the employer

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Add 2-3 second intervals between detail fetches. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: Extract all job IDs from the search page first (one eval), then batch-fetch details — avoid re-navigating to the search page between fetches
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `browser-act-skill-forge-memories/indeed-jobs-scraper-indeed-job-search.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
