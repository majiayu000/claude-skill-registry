---
name: crustdata-supabase
description: >
  Search CrustData People Search API for ICP-matching leads with automatic
  Supabase deduplication. Queries existing leads in the database, passes them
  as exclude_profiles to CrustData, fetches only net-new leads, and upserts
  results. Supports pagination, rate limiting, test mode, and reusable configs.
tags: [lead-generation]
---

# CrustData + Supabase Prospect Search

Search for ICP-matching leads using CrustData's People Search API with automatic deduplication against a Supabase database. Each run fetches only net-new leads — existing database entries are excluded at the API level via CrustData's `exclude_profiles` feature.

## Prerequisites (One-Time Setup)

### 1. Supabase Project

You need a Supabase project with URL and service role key. Add to `.env`:
```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

### 2. Database Tables

The full database schema lives in `tools/supabase/schema.sql`. Run it via the Supabase SQL Editor or using the setup script:

```bash
python3 tools/supabase/setup_database.py
```

This creates 6 tables: `runs`, `companies`, `people`, `signals`, `enrichment_log`, `outreach_log`. This skill writes to the `people` table (dedup by `linkedin_url` UNIQUE constraint).

### 3. Verify CrustData Token

Ensure `CRUSTDATA_API_TOKEN` is set in `.env`.

## Phase 0: Intake

Ask the user these questions to build the CrustData filter config:

### ICP Criteria

1. What **job titles** are you targeting? (e.g., "VP Sales", "Head of Growth")
2. Any titles to **exclude**? (e.g., "Software Engineer", "Intern")
3. **Company size** (headcount range)? Options: Self-employed, 1-10, 11-50, 51-200, 201-500, 501-1,000, 1,001-5,000, 5,001-10,000, 10,001+
4. **Industry** focus? (e.g., Software Development, Financial Services)
5. **Geographic region**? (e.g., "San Francisco Bay Area", "United States")
6. **Seniority level**? Options: CXO, Vice President, Director, Experienced Manager, Entry Level Manager, Strategic, Senior
7. Any specific **companies** to target or exclude?
8. Any other filters? (function, years of experience, recently changed jobs, posted on LinkedIn)
9. How many results do you need? (test: 25, standard: up to 500, full: up to 2,500)

### Map Answers to Config

Build the `filters` array using CrustData's exact filter format. Each filter is:
```json
{
  "filter_type": "FILTER_NAME",
  "type": "in" or "not in",
  "value": ["value1", "value2"]
}
```

Available filter types: `CURRENT_TITLE`, `PAST_TITLE`, `CURRENT_COMPANY`, `PAST_COMPANY`, `COMPANY_HEADQUARTERS`, `COMPANY_HEADCOUNT`, `REGION`, `INDUSTRY`, `SENIORITY_LEVEL`, `FUNCTION`, `YEARS_AT_CURRENT_COMPANY`, `YEARS_IN_CURRENT_POSITION`, `YEARS_OF_EXPERIENCE`, `COMPANY_TYPE`, `PROFILE_LANGUAGE`, `SCHOOL`, `KEYWORD`, `FIRST_NAME`, `LAST_NAME`.

Boolean filters (no type/value): `RECENTLY_CHANGED_JOBS`, `POSTED_ON_LINKEDIN`, `IN_THE_NEWS`.

For titles, `fuzzy_match: true` can be added for broader matching.

Save config:
```bash
skills/crustdata-supabase/configs/{client-name}.json
```

Config JSON structure:
```json
{
  "client_name": "happy-robot",
  "search_config_name": "growth-leaders-sf",
  "icp_segment": "growth-leaders",
  "filters": [
    {
      "filter_type": "CURRENT_TITLE",
      "type": "in",
      "value": ["Head of Growth", "VP Growth", "Director of Growth"],
      "fuzzy_match": true
    },
    {
      "filter_type": "REGION",
      "type": "in",
      "value": ["San Francisco Bay Area"]
    },
    {
      "filter_type": "COMPANY_HEADCOUNT",
      "type": "in",
      "value": ["51-200", "201-500", "501-1,000"]
    },
    {
      "filter_type": "INDUSTRY",
      "type": "in",
      "value": ["Software Development", "Technology, Information and Internet"]
    }
  ],
  "post_processing": {
    "strict_title_and_company_match": false,
    "exclude_names": []
  },
  "max_pages": 20,
  "mode": "standard"
}
```

## Database Write Policy

**CRITICAL: Never upsert leads to Supabase without explicit user approval.**

This skill writes to the `people` table. Unwanted writes pollute the database, and cleaning up bad entries across multiple test runs is painful.

**Required flow:**
1. Run `--preview` first to show total matching count and cost estimate
2. Run `--test` to fetch a small sample (~25 leads) — present results to the user **before any database write**
3. **Get explicit user approval** before upserting to Supabase
4. Only then run the full pipeline

**The agent must NEVER pass `--yes` on a first run.** The `--yes` flag is only for pre-approved automated runs where the user has already reviewed and confirmed the filters work correctly.

**If the user hasn't approved the upsert:** Export the CSV and show sample results. Let the user review. Only proceed to upsert after they confirm.

## Phase 1: Run the Pipeline

```bash
python3 skills/crustdata-supabase/scripts/prospect_search.py \
  --config skills/crustdata-supabase/configs/{client-name}.json \
  [--test] [--yes] [--preview] [--dry-run]
```

**Flags:**
- `--config` (required) — path to client config JSON
- `--test` — limit to 1 page / 25 results max
- `--yes` — skip cost confirmation prompt. **Only use for pre-approved automated runs, never on first runs.**
- `--preview` — show total matching count only (5 credits)
- `--dry-run` — show what would happen, no API calls

### Pipeline Steps

**Step 1: Connect to Supabase** — Verify connection, count existing leads.

**Step 2: Fetch existing URLs** — SELECT all `linkedin_url` from people table for dedup.

**Step 3: Build CrustData payload** — Combine user filters with `exclude_profiles` from Supabase.

**Step 4: Search page 1** — Get first 25 results + `total_display_count`. Show cost estimate.

**Step 5: Paginate** — Fetch remaining pages with 4s delay between requests (rate limit: 15 req/min).

**Step 6: Present results to user** — Show sample leads (names, titles, companies) and ask for explicit approval before writing to the database.

**Step 7: Upsert to Supabase** — **Only after user approval.** Insert new leads, update existing on conflict (linkedin_url UNIQUE).

**Step 8: Export CSV** — Write results to `output/{client-name}-{timestamp}.csv`.

### Mode Caps

| Parameter | Test | Standard | Full |
|-----------|------|----------|------|
| Max pages | 1 | 20 | 100 |
| Max results | 25 | 500 | 2,500 |
| Est. credits | 5-25 | 25-500 | 100-2,500 |

### Cost

CrustData charges **1 credit per profile** returned (minimum 5 per request). Preview mode costs **5 credits**. Always run `--preview` or `--test` first to verify filters before a full run.

## Phase 2: Review & Refine

Present results:
- **Total matching** — how many profiles match the filters in CrustData
- **Existing excluded** — how many were already in Supabase
- **New leads found** — net-new profiles fetched
- **Email coverage** — how many have verified emails
- **Top 10 leads** — name, title, company preview

Common adjustments:
- **Too broad** — add more filters (region, seniority, headcount)
- **Too narrow** — relax title matching (`fuzzy_match: true`), broaden regions
- **Wrong ICP** — adjust title include/exclude lists
- **Too expensive** — lower `max_pages` or switch to test mode

## Phase 3: Output

### Supabase (Primary)

New leads are stored in the `people` table with full CrustData data including email, title, company, location, industry, and headcount. Each person is tagged with `client_name`, `search_config_name`, and `icp_segment` for traceability.

### CSV (Secondary)

Exported to `skills/crustdata-supabase/output/{client-name}-{timestamp}.csv`:

| Column | Description |
|--------|-------------|
| Name | Full name |
| Title | Current job title |
| Company | Current company name |
| Company LinkedIn URL | Company page URL |
| Company Website | Company domain |
| Company Industry | Industry |
| Company Headcount | Employee count |
| Company Type | Public, Private, etc. |
| Person LinkedIn URL | Profile URL |
| Region | Geographic location |
| Headline | LinkedIn headline |
| Years of Experience | Total YoE |
| Connections | LinkedIn connection count |
| Skills | Semicolon-separated skills |
| Email | Business email (if available) |

## Example Usage

**Trigger phrases:**
- "Find leads matching [ICP description]"
- "Search CrustData for [titles] at [companies/industries]"
- "Run prospect-search for [client]"
- "Source new leads for [client] — skip duplicates"

**Preview (count only):**
```bash
python3 skills/crustdata-supabase/scripts/prospect_search.py \
  --config skills/crustdata-supabase/configs/happy-robot.json --preview
```

**Test run (review results before approving DB write):**
```bash
python3 skills/crustdata-supabase/scripts/prospect_search.py \
  --config skills/crustdata-supabase/configs/happy-robot.json --test
```

**Full run (only after user approves test results):**
```bash
python3 skills/crustdata-supabase/scripts/prospect_search.py \
  --config skills/crustdata-supabase/configs/happy-robot.json
```

## CrustData API Reference

- **Endpoint:** `POST https://api.crustdata.com/screener/person/search/`
- **Auth:** `Authorization: Token {CRUSTDATA_API_TOKEN}`
- **Rate limit:** 15 requests/minute
- **Max per page:** 25 profiles (synchronous)
- **Max page number:** 100
- **Dedup:** `post_processing.exclude_profiles` — array of LinkedIn URLs to skip
- **Full docs:** `Crustdata/Crustdata_documentation/people-docs/realtime-searchapi.md`
- **Filter reference:** `Crustdata/Crustdata_documentation/how_to_build_people_filters.md`
