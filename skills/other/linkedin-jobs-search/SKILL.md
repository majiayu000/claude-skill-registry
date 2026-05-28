---
name: linkedin-jobs-search
description: "Search LinkedIn job listings and extract full job details. Supports filtering by work type (remote/on-site/hybrid), contract type (full-time/part-time/contract/internship), experience level, date posted, and company. Returns job title, company, location, work type, contract type, experience level, posted date, applicant count, job description, salary, and direct job URLs. Use when user mentions linkedin jobs, linkedin job search, scrape linkedin jobs, extract linkedin job listings, find jobs on linkedin, job openings, job postings linkedin, linkedin career search, job hunting linkedin, linkedin vacancy, jobs remote linkedin, work from home jobs linkedin, linkedin scraper jobs, linkedin job data, linkedin hiring, collect job leads linkedin."
---

# LinkedIn — Job Search

> keywords + location + filters → paginated job list with full details

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Search LinkedIn job listings with full filter support, extract complete job data with full field coverage.

## Prerequisites

- The browser is open and the LinkedIn session is active (logged in). A LinkedIn jobs search page such as `https://www.linkedin.com/jobs/search/` must have been visited at least once so the CSRF token cookie is set.

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for LinkedIn has been confirmed in the current session → skip this step.

Otherwise: open `https://www.linkedin.com` and observe the page:
- User avatar or "Me" menu visible → logged in, continue
- Sign in / Join button visible → not logged in, inform user that LinkedIn login is required first

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It accesses LinkedIn through the user's logged-in browser, only reading data already available to the user. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### API: Search LinkedIn jobs (list page)

`eval "$(python scripts/search-jobs.py '{keywords}' '{location}' --count {count} --start {start} --work-type {work_type} --job-type {job_type} --experience {experience} --time-posted {time_posted} --company-ids {company_ids})"`

Parameters:
- `keywords`: job title or search keywords (e.g., `software engineer`, `data analyst`)
- `location`: location name (e.g., `United States`, `New York`, `San Francisco Bay Area`)
- `--count`: results per API call, default `25`, max `100`
- `--start`: pagination offset, default `0`. Increment by `count` for each page
- `--work-type`: work arrangement filter — `1`=On-site, `2`=Remote, `3`=Hybrid (optional)
- `--job-type`: contract type filter — `F`=Full-time, `P`=Part-time, `C`=Contract, `T`=Temporary, `I`=Internship, `V`=Volunteer (optional)
- `--experience`: experience level filter — `1`=Internship, `2`=Entry, `3`=Associate, `4`=Mid-Senior, `5`=Director (optional)
- `--time-posted`: recency filter — `r86400`=24h, `r604800`=7 days, `r2592000`=30 days (optional)
- `--company-ids`: comma-separated LinkedIn company numeric IDs (optional, e.g., `76987811,1441`)

Output example:
```json
{
  "total": 36015,
  "start": 0,
  "count": 5,
  "jobs": [
    {
      "id": "4416832078",
      "title": "Lead Frontend Software Engineer",
      "company": "RowsOne",
      "location": "Boca Raton, FL",
      "workType": "Remote",
      "jobUrl": "https://www.linkedin.com/jobs/view/4416832078",
      "companyUrl": "https://www.linkedin.com/company/rowsone"
    }
  ]
}
```

Error handling: If `{"error": true}` is returned, check that the browser is still logged in to LinkedIn and navigate to `https://www.linkedin.com/jobs/search/` to refresh the session, then retry once.

### API: Get full job details

`eval "$(python scripts/job-detail.py '{job_id}')"`

Parameters:
- `job_id`: numeric LinkedIn job posting ID (from `id` field in search results)

Output example:
```json
{
  "id": "4416832078",
  "title": "Lead Frontend Software Engineer",
  "company": "RowsOne",
  "companyUrl": "https://www.linkedin.com/company/rowsone",
  "location": "Boca Raton, FL",
  "workType": "Remote",
  "contractType": "Full-time",
  "experienceLevel": "Mid-Senior level",
  "listedAt": "2026-05-26T16:14:30.000Z",
  "applicantCount": 37,
  "description": "Lead Frontend Engineer (React / Next.js)...",
  "salary": null,
  "jobUrl": "https://www.linkedin.com/jobs/view/4416832078"
}
```

Error handling: HTTP 404 means job has been removed or ID is invalid. If `{"error": true, "message": "HTTP 403"}`, the LinkedIn session may have expired — navigate back to LinkedIn and verify login, then retry.

### Composite: Full job extraction (search list + detail for each job)

For complete output with all fields (description, contract type, experience level, posted date):

1. Run search component to collect job IDs and basic info
2. For each job ID, run the detail component
3. Merge results by job ID

Batch script template (bash):
```bash
#!/bin/bash
SESSION="fb_explore"
KEYWORDS="software engineer"
LOCATION="United States"
TOTAL_ROWS=50
COUNT=25
OUTPUT_FILE="output/jobs.jsonl"

offset=0
collected=0
while [ $collected -lt $TOTAL_ROWS ]; do
  batch_count=$((TOTAL_ROWS - collected))
  [ $batch_count -gt $COUNT ] && batch_count=$COUNT

  result=$(browser-act --session $SESSION eval "$(python scripts/search-jobs.py "$KEYWORDS" "$LOCATION" --count $batch_count --start $offset)")
  echo "$result" | python -c "
import json, sys
data = json.loads(sys.stdin.read())
for job in data.get('jobs', []):
    print(json.dumps(job))
" >> output/jobs_basic.jsonl

  job_ids=$(echo "$result" | python -c "import json,sys; [print(j['id']) for j in json.loads(sys.stdin.read()).get('jobs',[])]")
  for job_id in $job_ids; do
    detail=$(browser-act --session $SESSION eval "$(python scripts/job-detail.py $job_id)")
    echo "$detail" >> $OUTPUT_FILE
    sleep 1
  done

  page_count=$(echo "$result" | python -c "import json,sys; print(json.loads(sys.stdin.read()).get('count',0))")
  [ "$page_count" -eq 0 ] && break
  collected=$((collected + page_count))
  offset=$((offset + page_count))
  sleep 2
done
echo "Done. Collected $collected jobs."
```

Note: Add `sleep 1` between detail calls to avoid rate limiting. For large batches (>200 jobs), use multiple browser sessions in parallel — each session counts independently toward rate limits.

## Enum Parameters

Filter values are hardcoded in scripts; no dynamic enumeration needed.

Work type (`--work-type`): `1`=On-site, `2`=Remote, `3`=Hybrid

Contract type (`--job-type`): `F`=Full-time, `P`=Part-time, `C`=Contract, `T`=Temporary, `I`=Internship, `V`=Volunteer

Experience level (`--experience`): `1`=Internship, `2`=Entry level, `3`=Associate, `4`=Mid-Senior level, `5`=Director

Time posted (`--time-posted`): `r86400`=Past 24 hours, `r604800`=Past week, `r2592000`=Past month

## Pagination

**API Pagination**: parameter `--start`, type: page-offset, start value: `0`. Next page: increment by `--count` value. Termination: when `count` in response is `0`, or `start >= total`, or `start >= rows` target.

LinkedIn typically returns results up to `start=1000` maximum regardless of `total`.

## Success Criteria

`result count >= 1` and `jobs[0].id` is non-null

## Known Limitations

- LinkedIn limits accessible search results to approximately the first 1000 jobs per query even when `total` shows a higher number
- `experienceLevel` may be null for many postings — companies do not always fill in this field
- `salary` is null for most postings; LinkedIn only shows salary when the employer explicitly provides it
- Rate limiting: sustained rapid requests (e.g., >100 detail calls without sleep) may trigger temporary blocks. Add `sleep 1` between detail calls
- Login required: unlike public job boards, LinkedIn's Voyager API requires an authenticated session. The CSRF token is derived from the `JSESSIONID` cookie set at login

## Execution Efficiency

- **Batch orchestration**: write a bash loop iterating over job IDs serially; do not parallelize within one browser. For higher throughput, use multiple stealth browsers with separate sessions
- **Test before batch**: run with `--count 3` first to confirm the script runs correctly before scaling up
- **Error resumption**: append results to `.jsonl` file line-by-line so the job can resume from a specific offset on failure
- **Search only for large volumes**: for >500 jobs where full description is not needed, use the search component alone — it returns title, company, location, work type, and URLs without per-job detail calls

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/linkedin-job-search-linkedin-jobs-search.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
