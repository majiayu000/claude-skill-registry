---
name: build-tam
description: |
  Build a Total Addressable Market (TAM) list using ICP filters. Find all companies
  and contacts that match your ideal customer profile across multiple data providers.

  Triggers:
  - "build my TAM"
  - "total addressable market"
  - "find all companies that match my ICP"
  - "how many companies fit my criteria"
  - "build a prospect list from scratch"

  Requires: Deepline CLI — https://code.deepline.com
---

# Build TAM

Use this skill to size and build your total addressable market from ICP filters. Start with a count (virtually free), then pull the actual list.

## Step 1: Size your TAM first (virtually free)

Set `per_page: 1` — most providers return the total count but only charge for 1 result. This lets you validate your filters before spending credits on a full pull.

```bash
deepline tools execute apollo_people_search \
  --payload '{
    "person_titles": ["VP Sales", "Head of Revenue"],
    "include_similar_titles": true,
    "organization_num_employees_ranges": ["51,200", "201,500"],
    "organization_industry_tag_ids": ["technology"],
    "per_page": 1,
    "page": 1
  }' --json
```

Look for `total_people` in the response to see your TAM size before pulling.

## Step 2: Company-first TAM

```bash
# Size first
deepline tools execute apollo_company_search \
  --payload '{
    "q_organization_industry_tag_ids": ["technology"],
    "organization_num_employees_ranges": ["51,200"],
    "per_page": 1,
    "page": 1
  }' --json

# Pull list (100 per page)
deepline tools execute apollo_company_search \
  --payload '{
    "q_organization_industry_tag_ids": ["technology"],
    "organization_num_employees_ranges": ["51,200"],
    "per_page": 100,
    "page": 1
  }' --json
```

## Step 3: Contact-first TAM

```bash
deepline tools execute apollo_people_search \
  --payload '{
    "person_titles": ["VP Sales", "CRO", "Head of Revenue Operations"],
    "include_similar_titles": true,
    "organization_num_employees_ranges": ["51,200", "201,1000"],
    "organization_industry_tag_ids": ["technology"],
    "person_locations": ["United States"],
    "per_page": 100,
    "page": 1
  }' --json
```

## Step 4: Enrich your TAM with signals

Once you've pulled your TAM, enrich with buying signals before outreach:

```bash
deepline enrich --input tam.csv --in-place --rows 0:1 \
  --with 'signals=call_ai_claude_code:{"model":"haiku","json_mode":{"type":"object","properties":{"top_signal":{"type":"string"},"priority":{"type":"string","enum":["high","medium","low"]}},"required":["top_signal","priority"]},"prompt":"Company: {{Company}}\nDomain: {{Domain}}\n\nIs this account showing any buying signals? Return strict JSON."}'
```

## Common ICP filter parameters (Apollo)

| Filter | Parameter | Example values |
|---|---|---|
| Job title | `person_titles` | `["VP Sales", "Head of GTM"]` |
| Similar titles | `include_similar_titles` | `true` |
| Headcount | `organization_num_employees_ranges` | `["51,200", "201,500"]` |
| Industry | `organization_industry_tag_ids` | `["technology", "software"]` |
| Geography | `person_locations` | `["United States", "Canada"]` |
| Revenue | `revenue_range` | `{"min": 1000000, "max": 50000000}` |

## Pagination

Apollo returns up to 100 results per page. For large TAMs:

```bash
# Page 1
deepline tools execute apollo_people_search --payload '{"per_page": 100, "page": 1, ...}' --json

# Page 2
deepline tools execute apollo_people_search --payload '{"per_page": 100, "page": 2, ...}' --json
```

## Tips

- Always check `total_people` or `total_entries` with `per_page: 1` before pulling
- Start narrow (tight ICP), validate quality, then widen filters
- Use `person_locations` to segment by geo for personalized campaigns
- After pulling, prioritize with signal discovery before email enrichment

## Get started

Sign up and get your API key at [code.deepline.com](https://code.deepline.com).

```bash
npm install -g @deepline/cli
deepline auth login
```
