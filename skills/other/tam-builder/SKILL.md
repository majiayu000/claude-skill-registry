---
name: tam-builder
description: >
  Build and maintain a scored Total Addressable Market (TAM) using Apollo Company Search.
  Upserts companies to Supabase, scores ICP fit, assigns tiers, and auto-builds a persona
  watchlist for Tier 1-2 companies using Apollo People Search (free). Supports build, refresh,
  and status modes. Designed for CLI now, automation-ready for trigger.dev later.
tags: [lead-generation]
---

# TAM Builder

Build and maintain a scored Total Addressable Market. Uses Apollo Company Search to discover companies, upserts them to Supabase, scores ICP fit (0-100), assigns tiers (1/2/3), and auto-builds a persona watchlist for Tier 1-2 companies using Apollo People Search (free).

**Three modes:**
- **build** — First-time TAM construction from Apollo search
- **refresh** — Update existing TAM: re-score, detect tier changes, deprecate stale companies
- **status** — Read-only report of current TAM state

## Prerequisites

### 1. Apollo API Key
Add to `.env`:
```
APOLLO_API_KEY=your-api-key-here
```

### 2. Supabase Project
Same project used by other skills. Schema in `tools/supabase/schema.sql`. This skill writes to `companies` and `people` tables.

### 3. Verify Environment
Ensure `.env` has:
```
APOLLO_API_KEY=...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

## Config Format

Create a JSON config per client/segment:

```json
{
  "client_name": "happy-robot",
  "tam_config_name": "voice-ai-midmarket",

  "company_filters": {
    "organization_num_employees_ranges": ["51,200", "201,500", "501,1000"],
    "q_organization_keyword_tags": ["call center", "contact center"],
    "organization_locations": ["United States"]
  },

  "scoring": {
    "weights": {
      "employee_count_fit": 30,
      "industry_fit": 25,
      "funding_stage_fit": 20,
      "geo_fit": 15,
      "keyword_match": 10
    },
    "tier_thresholds": { "tier_1_min_score": 75, "tier_2_min_score": 50 },
    "target_industries": ["Telecommunications", "Customer Service"],
    "target_employee_ranges": [[51, 200], [201, 500], [501, 1000]],
    "target_funding_stages": ["Series A", "Series B", "Series C"],
    "target_geos": ["United States"]
  },

  "watchlist": {
    "enabled": true,
    "personas_per_company": 3,
    "person_filters": {
      "person_titles": ["VP of Operations", "Head of Customer Service"],
      "person_seniority": ["vp", "director", "c_suite"]
    },
    "tiers_to_watch": [1, 2]
  },

  "mode": "standard",
  "max_pages": 50
}
```

Save to: `skills/capabilities/tam-builder/configs/{client-name}.json`

## Database Write Policy

**CRITICAL: Never write to Supabase without explicit user approval.**

The TAM builder touches the `companies` and `people` tables. Unwanted writes are hard to clean up — they pollute the database, create duplicates on re-runs, and contaminate existing good data.

**Required flow before any database write:**
1. Run `--preview` to show the total TAM universe count and cost implications
2. Run `--sample` (with `--test` for 1 page) to show scored results in-memory — NO database writes
3. Present sample results to user: tier distribution, example Tier 1/2 companies, scoring sanity check
4. **Get explicit user approval** before proceeding to a build that writes to Supabase
5. Only then run without `--sample` to execute the actual build

**Why this matters:**
- If sample results look wrong, the user adjusts filters and re-runs — no cleanup needed
- Multiple test iterations don't create orphaned rows in the database
- Existing good data from prior builds is never accidentally overwritten
- The user stays in control of what enters the database

**The agent must NEVER pass `--yes` on a first run.** The `--yes` flag is only for automated/scheduled refreshes where the user has pre-approved the operation.

## Usage

### Sample (review before committing — ALWAYS DO THIS FIRST)
```bash
python3 skills/capabilities/tam-builder/scripts/tam_builder.py \
  --config skills/capabilities/tam-builder/configs/{client}.json \
  --mode build --sample --test
```
This searches Apollo (1 page, ~100 companies), scores them in-memory, and prints tier distribution + top companies. **No database writes.** Review output with user before proceeding.

### Build (first-time — only after user approves sample)
```bash
python3 skills/capabilities/tam-builder/scripts/tam_builder.py \
  --config skills/capabilities/tam-builder/configs/{client}.json \
  --mode build [--test] [--yes] [--dry-run] [--skip-watchlist]
```

### Refresh (update existing)
```bash
python3 skills/capabilities/tam-builder/scripts/tam_builder.py \
  --config skills/capabilities/tam-builder/configs/{client}.json \
  --mode refresh [--test] [--yes]
```

### Status (read-only report)
```bash
python3 skills/capabilities/tam-builder/scripts/tam_builder.py \
  --config skills/capabilities/tam-builder/configs/{client}.json \
  --mode status
```

## Pipeline: Build Mode

```
Step 0: --preview → total count + cost estimate (no DB writes)
Step 1: --sample --test → search 1 page, score in-memory, show results (no DB writes)
Step 2: User reviews sample → approves, adjusts filters, or caps scope
Step 3: Full build → Apollo Company Search → Upsert to Supabase → Score → Tier → Watchlist
```

Phase details (Step 3 only — after user approval):
```
Phase 1: Apollo Company Search → Upsert raw companies → Score ICP fit → Assign tiers
Phase 2: (skipped in build mode — no prior data to deprecate)
Phase 3: Persona Watchlist — pull 2-3 personas per Tier 1-2 company (free)
```

## Pipeline: Refresh Mode

```
Phase 1: Apollo Company Search → Upsert/update companies → Re-score → Detect tier changes
Phase 2: Deprecation — companies missing 2+ consecutive refreshes get deprecated
Phase 3: Persona Watchlist — pull personas for new/promoted Tier 1-2 companies,
         disqualify personas at deprecated companies
```

## ICP Scoring (0-100)

Pure function, no API calls. Weighted scoring across 5 dimensions from config:
- `employee_count_fit` — headcount in target ranges?
- `industry_fit` — industry matches targets?
- `funding_stage_fit` — funding stage in targets?
- `geo_fit` — HQ location in target geos?
- `keyword_match` — org keywords overlap config keywords?

Score thresholds (configurable): >=75 = Tier 1, >=50 = Tier 2, else Tier 3.

## Deprecation Rules (refresh only)

- First miss (not returned by search): `metadata.refresh_miss_count = 1`, keep active
- Second consecutive miss: `tam_status = 'deprecated'`
- Employee count drops to 0: immediate deprecation
- Companies with `tam_status = 'converted'` are always exempt

## Watchlist — Persona Sync

| Scenario | Behavior |
|----------|----------|
| New Tier 1-2 company | Pull 2-3 personas immediately |
| Company promoted Tier 3→2 | Pull personas during refresh |
| Company deprecated | Disqualify monitoring personas |
| Company demoted Tier 1→3 | Keep existing personas, stop refreshing |

## Mode Caps

| Parameter | Test | Standard | Full |
|-----------|------|----------|------|
| Max pages | 1 | 50 | 200 |
| Max companies | 100 | 5,000 | 20,000 |

## Flags

| Flag | Effect |
|------|--------|
| `--test` | Limit to 1 page / 100 companies |
| `--sample` | Search + score in-memory, NO database writes. Shows tier distribution and top companies for user review. Combine with `--test` for a quick 1-page sample. |
| `--yes` | Skip confirmation prompts. **Only use for pre-approved automated refreshes, never on first runs.** |
| `--dry-run` | No API calls, show what would happen |
| `--preview` | Show total count only (build mode) |
| `--skip-watchlist` | Skip persona watchlist phase |
