---
name: data-store
description: (ePost) Use when an agent needs to persist or retrieve project-level data across sessions via .epost-data/
user-invocable: false
---

# Agent Data Store Convention

Defines how agents store and access persistent project-level data across sessions.

## Directory Layout

```
.epost-data/              ← gitignored, project-level runtime state
  {domain}/
    {domain}.json         ← primary DB (required)
    artifacts/            ← generated patches, diffs, temp files (optional)
```

### a11y Domain Layout

```
.epost-data/a11y/
├── fixes/
│   ├── findings/         ← audit-a11y JSON reports (audit-YYMMDD-HHMM.json)
│   ├── patches/          ← fix-a11y unified diffs (finding-{id}-YYMMDD.diff)
│   └── reviews/          ← review-a11y JSON reports (review-YYMMDD-HHMM.json)
├── README.md             ← structure guide
├── analysis.md           ← trend summary
└── known-findings.json   ← findings DB
```

## Rules

| Rule | Detail |
|------|--------|
| **Always `(if exists)`** | Never hard-fail on missing file — gracefully absent on first run |
| **Gitignored** | Runtime state, not source-tracked; must be in `.gitignore` |
| **One agent = one domain** | Agent owns its domain exclusively; never reads another agent's |
| **Schema in source** | Schema lives at `packages/{pkg}/assets/{domain}-schema.json`, tracked in git |

## Agent Declaration Template

Paste into the agent's system prompt body under a **Data Store** section:

```markdown
## Data Store
- **DB:** `.epost-data/{domain}/{domain}.json` (if exists)
- **Artifacts:** `.epost-data/{domain}/artifacts/` (if exists)
- **Schema:** `.claude/assets/{domain}-schema.json`
```

## Domain Registry

| Domain | Owner Agent           | Primary File          | Package          |
|--------|-----------------------|-----------------------|------------------|
| `a11y` | epost-a11y-specialist | `known-findings.json` | packages/a11y    |

*Add a row here when introducing a new agent data domain.*

## Schema Conventions

Minimum required fields for any `{domain}.json`:

```json
{
  "version": "1.0",
  "created_date": "YYYY-MM-DD",
  "last_reviewed_date": "YYYY-MM-DD",
  "entries": [
    {
      "id": 1,
      "resolved": false,
      "resolved_date": null
    }
  ]
}
```

- Bump `version` string on schema changes (new fields = minor, breaking = major)
- All commands check `resolved` before operating on an entry
- `last_reviewed_date` updated any time the DB is written

## Adopting the Pattern (New Domain)

1. Create schema: `packages/{pkg}/assets/{domain}-schema.json`
2. Add domain row to the registry table above
3. Add "Data Store" section to agent body using the template
4. Reference paths in commands with `(if exists)` guards
5. Add `.epost-data/` to project `.gitignore` (if not already present)
