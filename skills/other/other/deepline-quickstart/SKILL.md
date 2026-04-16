---
name: deepline-quickstart
description: 'Run a quick Deepline demo recipe to show the user how Deepline works.'
disable-model-invocation: false
---

# Deepline Quickstart

Run a high-confidence demo recipe to show the user what Deepline can do. Pick the most relevant recipe below, or default to Recipe 1 if no context is given.

**Always prefer the hardcoded recipes below.** `/gtm-meta-skill` is always available as a fallback but should only be used if: (a) a recipe command fails and all fallbacks are exhausted, or (b) the user's ask doesn't match any recipe here. Never invoke it preemptively.

## Execution flow

Follow this pattern for every recipe:

1. **Tell the user what you're about to do** — explain the goal and which data source(s) you'll use, before running anything.
2. **Register a session start** with `deepline session start --steps '[...]'` matching the recipe steps. If you have the user's original request text, include it with `--user-prompt "..."` so opted-in prompt telemetry is preserved.
3. **For each step**: mark it running, send a live status message describing what's happening, run the command, then mark it completed (or error on failure).
4. **Register output** with `deepline session output --csv <path> --label "..."` after any CSV is produced.
5. **Tell the user the results** — summarize what came back, where it came from, and what they can do next.

### Session commands reference

```bash
deepline session start --steps '["Step 1", "Step 2"]' --user-prompt "Original user request"
deepline session start --update <i> --status running|completed|error|skipped
deepline session status --message "What's happening right now..."
deepline session output --csv <path> --label "Label for the table"
deepline session usage [--session-id UUID] [--json]
```

---

## Recipe 1 — Find CTOs at NY startups

**Goal:** Find 5 CTOs at startups in New York with verified emails and LinkedIn profiles.
**Data sources:** Dropleads (people search) + waterfall email enrichment via `person_linkedin_to_email_waterfall`.

**Steps:**

1. Search Dropleads for CTOs in New York
2. Waterfall enrich emails
3. Display results

### Step 1 — Search

```bash
deepline tools execute dropleads_search_people --payload '{
  "filters": {
    "jobTitles": ["CTO"],
    "personalStates": {"include": ["New York"]},
    "employeeRanges": ["1-10", "11-50", "51-200"]
  },
  "pagination": {"page": 1, "limit": 5}
}'
```

Note the output CSV path from the result.

### Step 2 — Waterfall enrich emails

First, prep the name, LinkedIn, and domain columns the play expects:

```bash
deepline enrich --input <csv_from_step_1> --in-place \
  --with '{"alias":"first_name","tool":"run_javascript","payload":{"code":"return (row[\"fullName\"]||\"\").trim().split(\" \")[0]||null;"}}' \
  --with '{"alias":"last_name","tool":"run_javascript","payload":{"code":"const parts=(row[\"fullName\"]||\"\").trim().split(\" \"); return parts.slice(1).join(\" \")||null;"}}' \
  --with '{"alias":"linkedin_url","tool":"run_javascript","payload":{"code":"return row[\"linkedinUrl\"]||null;"}}' \
  --with '{"alias":"domain","tool":"run_javascript","payload":{"code":"const raw=row[\"companyDomain\"]||row[\"companyWebsite\"]||row[\"website\"]||null; if(!raw) return null; return String(raw).replace(/^https?:\\/\\//, \"\").replace(/^www\\./, \"\").replace(/\\/.*$/, \"\").trim()||null;"}}'
```

Then run the waterfall play:

```bash
deepline enrich --input <csv_from_step_1> --in-place \
  --with '{"alias":"email","tool":"person_linkedin_to_email_waterfall","payload":{"linkedin_url":"{{linkedin_url}}","first_name":"{{first_name}}","last_name":"{{last_name}}","domain":"{{domain}}"}}'
```

Register the output CSV after this step.

### Step 3 — Display results

Show a summary table: name, company, email, LinkedIn URL. Tell the user emails were filled via the dedicated LinkedIn-to-email waterfall. Mention they can go deeper — phone, firmographics, job change signals — with `/gtm-meta-skill`.

### Fallback (if Step 1 errors)

Tell the user, then try Apollo:

```bash
deepline tools execute apollo_search_people_with_match --payload '{
  "person_titles": ["CTO", "Chief Technology Officer"],
  "person_seniorities": ["c_suite"],
  "person_locations": ["New York, New York, United States"],
  "organization_num_employees_ranges": ["1,200"],
  "include_similar_titles": true,
  "per_page": 5,
  "page": 1
}'
```

### Last resort

If all commands fail, tell the user, then invoke `/gtm-meta-skill`:

> Find 5 CTOs at startups in New York with their emails and LinkedIn profiles.
