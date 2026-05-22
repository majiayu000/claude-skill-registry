---
name: supabase
description: Query a Supabase/PostgreSQL database with safety guardrails.
user-invocable: true
argument-hint: "<query|tables|users|analytics> [args]"
context: fork
agent: ops
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Supabase Database — Safe Query Interface

## SAFETY RULES (MANDATORY)

**FORBIDDEN — Never execute these, regardless of user request:**
- `DROP`, `DELETE`, `TRUNCATE`, `ALTER`, `GRANT`, `REVOKE`, or any DDL statement
- Any write operation on `auth.*` tables
- `UPDATE` without a `WHERE` clause

**ALLOWED:**
- `SELECT` on any table (always safe, read-only)
- `INSERT` on non-critical tables only (user must specify which are safe)
- `UPDATE` on non-critical tables only, **with a WHERE clause**

**REQUIRED — Before any write operation:**
1. Show the exact SQL statement to the user
2. Wait for explicit user confirmation ("yes", "go ahead", etc.)
3. Only then execute

If the user asks you to run a forbidden operation, **refuse** and explain why.

Current Supabase status:
!command supabase projects list 2>/dev/null | head -5 || echo "Supabase CLI not available; using MCP postgres tools"

## Commands

### `tables` — List all tables
Use the Supabase MCP postgres tools to query:
```sql
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;
```

### `query <SQL>` — Run a SELECT query
Validate the query is a SELECT statement before executing. Use MCP postgres tools.

### `users` — User statistics
```sql
SELECT count(*) as total_users,
       count(*) FILTER (WHERE created_at > now() - interval '7 days') as new_this_week,
       count(*) FILTER (WHERE created_at > now() - interval '30 days') as new_this_month
FROM users;
```

### `analytics` — Usage analytics
```sql
SELECT date_trunc('day', created_at) as day, count(*) as events
FROM activity_log
WHERE created_at > now() - interval '7 days'
GROUP BY 1 ORDER BY 1;
```

## Notes

- This is a **production database** — treat with extreme caution
- The MCP supabase server connects via `$SUPABASE_DB_URL` (wrapper script, no plaintext passwords in config)
- Future: a read-only Postgres role provides defense-in-depth
- `context: fork` ensures queries run in an isolated subagent
