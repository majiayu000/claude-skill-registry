---
name: treido-audit-supabase
description: "Read-only Supabase auditor for Treido (schema/migrations/RLS + query hot paths). Returns structured payload for ORCH merge. Trigger: SUPABASE-AUDIT"
---

# Treido Supabase Auditor (Read-only)

Read-only specialist. Do not patch files. Do not edit `TASKS.md`.
Contract: `.claude/skills/treido-orchestrator/references/audit-payload.md`

## Focus (Treido)

- RLS policies exist and are scoped correctly (no accidental public writes).
- Schema changes via migrations (no ad-hoc DDL).
- Hot paths: no `select('*')`; project fields; paginate.

## Audit Steps (Read-only)

```bash
ls supabase/migrations
rg -n "row level security|create policy|alter policy|drop policy" supabase/migrations
rg -n "select\\(\\s*\\*\\s*\\)" app lib --glob '*.ts' --glob '*.tsx'
```

## Output (Required)

- Header: `## SUPABASE`
- IDs: `SUPABASE-001`, `SUPABASE-002`, ...
- Include acceptance checks: “no select(*) in hot paths” + “schema/RLS changes represented as migrations”

