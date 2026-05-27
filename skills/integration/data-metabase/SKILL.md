---
name: data-metabase
description: "Metabase REST API automation and troubleshooting: authenticate (API key preferred, session fallback), export/upsert questions (cards) and dashboards, standardize visualization_settings, and run/export results."
---

# Metabase

Automate Metabase via API: reports (cards), dashboards, and chart settings.

## Quick Start

### Inputs (env vars)

- `METABASE_URL` (e.g., `https://metabase.example.com`)
- Preferred: `METABASE_API_KEY`
- Fallback: `METABASE_USERNAME` + `METABASE_PASSWORD`

### Sanity checks

```bash
python3 frameworks/shared-skills/skills/data-metabase/scripts/metabase_api.py health
python3 frameworks/shared-skills/skills/data-metabase/scripts/metabase_api.py whoami
```

### Live API documentation

Your Metabase instance serves OpenAPI docs at `/api/docs` (e.g., `https://metabase.example.com/api/docs`). Use this to discover version-specific endpoints and request shapes.

## Workflow

1. Confirm API availability (`GET /api/util/health`).
2. Authenticate with an API key (preferred) or a short-lived session (fallback).
3. Discover IDs (prefer discovery over hardcoding across environments):
   - `collection_id` for where to save
   - `database` id for `dataset_query`
   - `source-table` / field ids if using MBQL
4. Create/update a card:
   - Prefer native SQL for stable automation.
   - Set `display` + `visualization_settings` explicitly.
5. Create/update a dashboard and add cards with consistent layout.
6. Validate by running/exporting results.

## Key Concepts

- UI "Question" == API `card`
- Chart configuration lives on the card as `display` + `visualization_settings`
- Most viz keys are easiest to manage by copying from an existing card JSON, then editing

## Guardrails

- Prefer Metabase "serialization" (Pro/Enterprise) for bulk, cross-environment migrations; use direct API for incremental upserts.
- Do not hardcode numeric IDs across environments when you can discover them or use serialization/entity IDs.
- Never commit `METABASE_API_KEY`, passwords, or session tokens.
- Prefer a dedicated, least-privileged automation account and collection.

## References (read only as needed)

| Topic                                 | File                                                           |
|---------------------------------------|----------------------------------------------------------------|
| Authentication (API key + fallback)   | [references/api-auth.md](references/api-auth.md)               |
| Reports (cards): create/edit patterns | [references/reports-cards.md](references/reports-cards.md)     |
| Dashboards and card placement         | [references/dashboards.md](references/dashboards.md)           |
| Charts and `visualization_settings`   | [references/charts-settings.md](references/charts-settings.md) |

## Scripts

`scripts/metabase_api.py` is a small, dependency-free helper to test auth and upsert cards.

Examples:

```bash
# Print authenticated user (tries API key, then session)
python3 frameworks/shared-skills/skills/data-metabase/scripts/metabase_api.py whoami

# Export an existing card JSON (use as a template for visualization_settings)
python3 frameworks/shared-skills/skills/data-metabase/scripts/metabase_api.py export-card --id 123 --out card.json

# Export an existing dashboard JSON (use as a template for layout)
python3 frameworks/shared-skills/skills/data-metabase/scripts/metabase_api.py export-dashboard --id 5 --out dashboard.json

# Create/update a card from a JSON spec (see references/reports-cards.md)
python3 frameworks/shared-skills/skills/data-metabase/scripts/metabase_api.py upsert-card --spec card-spec.json

# Create/update a dashboard from a JSON spec (base fields only)
python3 frameworks/shared-skills/skills/data-metabase/scripts/metabase_api.py upsert-dashboard --spec dashboard-spec.json
```
