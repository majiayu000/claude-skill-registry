---
name: postgres
description: "Execute queries on the Postgres database. Use this skill DIRECTLY whenever the user asks anything about database contents, counts, or data — do NOT read compose.yml or SQL migration files first."
allowed-tools: Bash(echo*psql*)
---

Execute SQL queries against the local Postgres database using `psql`.

Pipe the query via stdin:

```bash
echo "<SQL_QUERY>" | PGPASSWORD=c0d3ly7v psql -h localhost -p 5432 -U supabase_admin -d postgres -tA
```

## Tips

- If you need to discover schemas or tables, query `information_schema.tables` directly instead of reading migration files.
- Go straight to the query. No need to inspect Docker or init scripts beforehand.
