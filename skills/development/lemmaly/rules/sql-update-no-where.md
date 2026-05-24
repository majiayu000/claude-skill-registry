---
id: sql-update-no-where
title: UPDATE / DELETE without WHERE — touches every row
severity: error
impact: CRITICAL
impactDescription: Will break or scale-fail in production
language: sql
tags: sql, error, invariant-guard
---

# UPDATE / DELETE without WHERE — touches every row

An `UPDATE` or `DELETE` without a `WHERE` clause rewrites every row in the table. In production this is an incident, not a bug.

## Fix

Add a WHERE clause, or confirm in a comment that touching all rows is intentional.

## Incorrect

```sql
UPDATE users SET active = false;
DELETE FROM sessions;
```

## Correct

```sql
UPDATE users SET active = false WHERE last_seen_at < NOW() - INTERVAL '90 days';
DELETE FROM sessions WHERE expires_at < NOW();
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
