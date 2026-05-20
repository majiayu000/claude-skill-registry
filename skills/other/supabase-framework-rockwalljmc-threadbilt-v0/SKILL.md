---
name: supabase-framework
description: Use for any Supabase database work in PierceDesk, including schema, migrations, RLS, and query patterns. Requires MCP-only database access and references docs/system execution/design guidance.
---

# Supabase Framework Skill

## Core rules

- **Cloud database only**: use Supabase MCP tools for all DB operations.
- **No local DB connections** (no psql, no DATABASE_URL).
- **RLS required**: all tables must enforce `auth.uid()` or org-scoped policies.
- **Align schema with existing CRM patterns** in docs/system.

## Required references (read before DB work)

- `references/system-docs-map.md`
- `references/rls-auth-patterns.md`

## Operational guidance

- Validate auth context in API routes; DB layer assumes `auth.uid()`.
- Use migrations and seeds in `database/` when applicable.
- Prefer indexed columns for frequently filtered fields.
- For large datasets, design queries with pagination + selective columns.

## Process checklist

1. Identify existing schema and tables in docs/system.
2. Use MCP tools to verify current schema.
3. Implement migrations or SQL updates via MCP.
4. Add/verify RLS policies per table.
5. Seed minimal data if required and document changes.
