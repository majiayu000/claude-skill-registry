---
name: web-database-validator
description: Validate database schema, migrations, indexes, and query behavior with structured pass/fail reporting.
compatibility: codex, claude-code, claude-ai, agent-skills
license: Apache-2.0
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
  - web_search
metadata:
  category: web-builder
  stage: 6-database-validation
  pipeline: web-builder
---

# Web Database Validator

## Objective

Validate schema and query quality after backend scaffolding, including
migration sanity checks and performance guardrails.

## Required Workflow

1. Read `project-config.json` and ORM schema files.
2. Run migrations in a local test database (Docker or in-memory SQLite for dry runs).
3. Validate:
   - foreign key constraints
   - indexes on foreign keys and hot query columns
   - N+1 query risk with query logs or explain plans
   - soft-delete fields where required
   - auto timestamps (`created_at`, `updated_at`)
4. Seed realistic test data using Faker.js or Python Faker.
5. Run query checks for row counts, relationships, and cascades.
6. Output `db-validation-report.json` with pass/fail per check.

## Execution

```bash
python skills/web-database-validator/scripts/database_validator.py --input <workspace> --output <out.json> --format json
```

## References

- `references/tools.md`
