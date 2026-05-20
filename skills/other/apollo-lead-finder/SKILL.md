---
name: apollo-lead-finder
description: >
  Two-phase Apollo.io prospecting: free People Search to discover ICP-matching
  leads, then selective enrichment to reveal emails/phones (credits per contact).
  Creates Apollo lists. Deduplicates against Supabase.
tags: [lead-generation]
---

# Apollo Lead Finder

Two-phase Apollo.io prospecting: **free** People Search for lead discovery, then selective **paid** enrichment to reveal emails and phone numbers. Creates Apollo lists and contacts. Deduplicates against Supabase.

**Key advantage over CrustData:** Apollo People Search is free (no credits consumed). Credits are only spent when enriching contacts to reveal email/phone. This lets you search tens of thousands of leads at zero cost, review results, then selectively enrich only the best matches.

## Prerequisites (One-Time Setup)

### 1. Apollo API Key

Get your API key from Apollo.io Settings > Integrations > API. Add to `.env`:
```
APOLLO_API_KEY=your-api-key-here
```

### 2. Supabase Project

Same Supabase project used by `crustdata-supabase`. The full schema lives in `tools/supabase/schema.sql`. This skill writes to the `people` table (dedup by `linkedin_url` UNIQUE constraint). Run `python3 tools/supabase/setup_database.py` if setting up fresh.

### 3. Verify Environment

Ensure `.env` has all three keys:
```
APOLLO_API_KEY=...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

## Phase 0: Intake

Ask the user these questions to build the Apollo filter config:

### ICP Criteria

1. What **job titles** are you targeting? (e.g., "VP of Sales", "Head of Growth")
2. What **seniority levels**? Options: owner, founder, c_suite, partner, vp, director, manager, senior, entry
3. **Company size** (employee range)? Format: "51,200" "201,500" "501,1000" "1001,5000"
4. **Geographic regions**? (e.g., "United States", "San Francisco, California")
5. **Industry/keyword tags**? (e.g., "SaaS", "Software", "FinTech")
6. Any titles to **exclude**? (e.g., "intern", "assistant")
7. Should we **create an Apollo list** with these contacts? (default: yes)
8. How many results do you want? (test: 100, standard: 5,000, full: 50,000)

### Map Answers to Config

Build the config JSON with Apollo's filter format:

```json
{
  "client_name": "example-client",
  "search_config_name": "vp-sales-us-midmarket",
  "icp_segment": "sales-leaders",
  "apollo_filters": {
    "person_titles": ["VP of Sales", "Head of Sales", "Director of Sales"],
    "person_seniority": ["vp", "director"],
    "person_locations": ["United States"],
    "organization_num_employees_ranges": ["51,200", "201,500", "501,1000"],
    "q_organization_keyword_tags": ["SaaS", "Software"]
  },
  "enrichment_filters": {
    "exclude_titles_containing": ["intern", "assistant"]
  },
  "apollo_list_name_prefix": "example-sales-leaders",
  "create_apollo_list": true,
  "mode": "standard",
  "max_pages": 50
}
```

Available Apollo search filters:
- `person_titles` — job title keywords (array of strings)
- `person_seniority` — seniority levels: owner, founder, c_suite, partner, vp, director, manager, senior, entry
- `person_locations` — geographic locations (array of strings)
- `organization_num_employees_ranges` — employee count ranges, format "min,max" (e.g., "51,200")
- `q_organization_keyword_tags` — company keyword tags (e.g., "SaaS", "Software")
- `person_not_titles` — titles to exclude (array of strings)
- `q_organization_name` — organization name search
- `organization_locations` — company HQ locations

Save config:
```bash
skills/apollo-lead-finder/configs/{client-name}.json
```

## Phase 1: Search (FREE)

```bash
python3 skills/apollo-lead-finder/scripts/apollo_lead_finder.py \
  --config skills/apollo-lead-finder/configs/{client}.json \
  --phase search \
  [--test] [--yes] [--dry-run]
```

### What the free search returns

Apollo's `api_search` endpoint returns **limited preview data**: Apollo person ID, first name, obfuscated last name, title, company name, and boolean flags (has_email, has_phone). **No LinkedIn URLs, emails, or full names** — those require enrichment.

### Pipeline Steps

**Step 1: Build Apollo search payload** — Map config filters to Apollo People Search format.

**Step 2: Search page 1** — Get first 100 results + `total_entries` for total count.

**Step 3: Paginate** — Fetch remaining pages (100 per page, up to mode cap). Apply title filters.

**Step 4: Save manifest** — Write Apollo person IDs + preview data to a JSON manifest file for the enrich phase.

**Step 5: Export preview CSV** — Write search results to `output/{client-name}-search-{timestamp}.csv` (limited data — full data after enrichment).

### Mode Caps

| Parameter | Test | Standard | Full |
|-----------|------|----------|------|
| Max pages | 1 | 50 | 500 |
| Max results | 100 | 5,000 | 50,000 |
| Search credits | 0 | 0 | 0 |

**Cost: FREE.** People Search does not consume Apollo credits.

## Database Write Policy

**CRITICAL: Never upsert leads to Supabase without explicit user approval.**

This skill writes to the `people` table during the enrich phase. The search phase is free and produces no database writes — but enrichment both costs credits AND writes to the database.

**Required flow:**
1. Run `--phase search` first (free) — review the search results and preview CSV
2. Present search results to the user: total matches, sample leads, title distribution
3. **Get explicit user approval** before running enrich phase
4. After enrichment, present the enriched results to the user **before upserting to Supabase**
5. Only upsert after the user confirms the results look good

**The agent must NEVER pass `--yes` on a first run.** The `--yes` flag is only for pre-approved automated runs.

**If the user hasn't approved the upsert:** Export the CSV and show sample results. Let the user review. Only proceed to upsert after they confirm.

## Phase 2: Enrich (COSTS CREDITS)

```bash
python3 skills/apollo-lead-finder/scripts/apollo_lead_finder.py \
  --config skills/apollo-lead-finder/configs/{client}.json \
  --phase enrich \
  [--test] [--yes] [--limit N]
```

### Pipeline Steps

**Step 1: Load search manifest** — Read the manifest JSON saved by the search phase. Contains Apollo person IDs.

**Step 2: Connect to Supabase** — Fetch existing LinkedIn URLs for dedup.

**Step 3: Confirm credits** — Display lead count and credit cost estimate. Wait for confirmation.

**Step 4: Bulk enrich** — Call `/people/bulk_match` with Apollo person IDs in batches of 10. Each match costs 1 credit. Returns full data: email, phone, LinkedIn URL, full name, location, company details.

**Step 5: Dedup against Supabase** — Filter out leads whose LinkedIn URLs already exist in Supabase.

**Step 6: Present results to user** — Show enriched sample leads (names, titles, companies, email coverage) and ask for explicit approval before writing to the database.

**Step 7: Upsert to Supabase** — **Only after user approval.** Insert net-new people with `source='apollo'`, `enrichment_status='complete'`.

**Step 8: Export CSV** — Write enriched leads to `output/{client-name}-enriched-{timestamp}.csv`. Update manifest to remove enriched people.

### Mode Caps

| Parameter | Test | Standard | Full |
|-----------|------|----------|------|
| Max enrichments | 10 | 500 | 2,500 |
| Credits used | 10 | 500 | 2,500 |

**Cost: 1 credit per contact enriched.** Always run search first, review results, then selectively enrich.

## Phase 3: Review & Refine

Present results:
- **Total matching** — how many profiles match the filters in Apollo
- **New leads found** — net-new profiles (after Supabase dedup)
- **Apollo list** — name and link to the list in Apollo
- **Enriched** — how many have emails revealed
- **Email coverage** — percentage of enriched leads with valid emails
- **Top 10 leads** — name, title, company preview

Common adjustments:
- **Too broad** — add more filters (seniority, employee range, keyword tags)
- **Too narrow** — broaden title list, remove location filters
- **Low email coverage** — some contacts genuinely have no known email; try enriching more leads
- **Wrong ICP** — adjust title include/exclude lists

## Example Usage

**Trigger phrases:**
- "Search Apollo for [titles] at [industries]"
- "Find leads in Apollo matching my ICP"
- "Run Apollo search for [client]"
- "Enrich the Apollo leads from last search"

**Test search (free, no DB writes):**
```bash
python3 skills/apollo-lead-finder/scripts/apollo_lead_finder.py \
  --config skills/apollo-lead-finder/configs/example.json --phase search --test
```

**Dry run (no API calls):**
```bash
python3 skills/apollo-lead-finder/scripts/apollo_lead_finder.py \
  --config skills/apollo-lead-finder/configs/example.json --phase search --dry-run
```

**Enrich only (after reviewing search results and getting user approval):**
```bash
python3 skills/apollo-lead-finder/scripts/apollo_lead_finder.py \
  --config skills/apollo-lead-finder/configs/example.json --phase enrich --limit 100
```

**Full search + enrich (only for pre-approved repeat runs):**
```bash
python3 skills/apollo-lead-finder/scripts/apollo_lead_finder.py \
  --config skills/apollo-lead-finder/configs/example.json --phase both
```

## Apollo API Reference

- **People Search:** `POST https://api.apollo.io/api/v1/mixed_people/api_search` — FREE, returns Apollo IDs + preview data (first name, title, org name, boolean flags). No LinkedIn URLs or emails.
- **People Match (enrich):** `POST https://api.apollo.io/api/v1/people/match` — 1 credit, reveals email/phone
- **Bulk People Match:** `POST https://api.apollo.io/api/v1/people/bulk_match` — up to 10 per request, 1 credit each
- **Create List:** `POST https://api.apollo.io/api/v1/labels` — create a named list
- **Create Contact:** `POST https://api.apollo.io/api/v1/contacts` — add person to Apollo CRM + optional list
- **Auth:** `x-api-key: {APOLLO_API_KEY}` header on all requests
- **Rate limit:** Varies by plan. Handle 429 with Retry-After header.
- **Search Pagination:** `page` param (1-indexed), `per_page` max 100
