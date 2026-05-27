---
name: data-import-workflow
description: Managing the lifecycle of weapon and mod data from external sources to the local database
---

# Data Import Workflow Skill

Use this skill when working on or running the data import pipeline.

---

## Scope

- Running the importer to populate or refresh data
- Extending the importer to handle new fields or types
- Debugging import failures

---

## Running the Importer

| Command | Use Case |
|---------|----------|
| `task importer:start` | Fetch fresh data from tarkov.dev API and update the database. |
| `task importer:start:use-cache` | Use locally cached JSON files (faster, avoids API rate limits). |
| `task importer:start:cache-only` | Fetch from API and update local cache, but skip database writes. |

---

## Import Behavior

1. **Purge**: Existing weapons, mods, trader offers, and optimum builds are deleted.
2. **Fetch**: Data is retrieved from tarkov.dev GraphQL API (or local cache).
3. **Transform**: External schema is mapped to internal `models` structs.
4. **Persist**: Data is written to the database within a transaction.
5. **Invalidate**: `optimum_builds` are purged since they depend on the imported data.

---

## Extending the Importer

When adding new fields or types:

1. **Update GraphQL Query**: Modify `internal/tarkovdev/schemas/queries.graphql`.
2. **Regenerate Client**: Run `task tarkovdev:regenerate`.
3. **Update Models**: Add new fields to structs in `internal/models/`.
4. **Update Mapping**: Adjust conversion logic in `internal/importers/`.
5. **Update SQL**: Modify `Upsert` functions in `internal/models/` to include new columns.

---

## Troubleshooting

- **Rate Limiting**: Use `--use-cache` for repeated runs during development.
- **Schema Mismatch**: Run `task tarkovdev:get-schema` then `task tarkovdev:regenerate`.
- **Connection Issues**: Verify `POSTGRES_HOST` in `.env` and ensure the database is running.
