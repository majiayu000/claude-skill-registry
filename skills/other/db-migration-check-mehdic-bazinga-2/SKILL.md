---
name: db-migration-check
description: Detect dangerous operations in database migrations before deployment
version: 1.0.0
allowed-tools: [Bash, Read]
---

# Database Migration Check Skill

You are the db-migration-check skill. When invoked, you analyze database migration files to detect dangerous operations that could cause downtime, data loss, or performance issues.

## When to Invoke This Skill

**Invoke this skill when:**
- Tech Lead reviewing database migrations
- Before deploying migrations to production
- New migration files created
- Database schema changes pending
- Before approving PRs with migrations

**Do NOT invoke when:**
- No migrations exist in project
- Only documentation changes
- Read-only database queries (no schema changes)
- Rollback migrations (already analyzed)

---

## Your Task

When invoked:
1. Execute the migration check script
2. Read the generated analysis report
3. Return a summary to the calling agent

---

## Step 1: Execute Migration Check Script

Use the **Bash** tool to run the pre-built migration check script:

```bash
python3 .claude/skills/db-migration-check/check.py
```

This script will:
- Detect database type (PostgreSQL, MySQL, SQL Server, MongoDB)
- Find pending migration files
- Parse SQL operations
- Detect dangerous patterns (table locks, data loss risks)
- Suggest safe alternatives
- Generate `bazinga/artifacts/{SESSION_ID}/skills/db_migration_check.json`

---

## Step 2: Read Generated Report

Use the **Read** tool to read:

```bash
bazinga/artifacts/{SESSION_ID}/skills/db_migration_check.json
```

Extract key information:
- `status` - dangerous_operations_detected/safe/error
- `dangerous_operations` - Array of blocking issues
- `warnings` - Medium-risk operations
- `safe_migrations` - Approved operations
- `recommendations` - Safe alternatives

---

## Step 3: Return Summary

Return a concise summary to the calling agent:

```
Database Migration Check:
- Database: {database_type}
- Framework: {framework}
- Migrations analyzed: {count}

⚠️  DANGEROUS OPERATIONS: {count}
- CRITICAL ({count}): {list}
- HIGH ({count}): {list}

Safe migrations: {count}

Top recommendations:
1. {recommendation}
2. {recommendation}

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/db_migration_check.json
```

---

## Example Invocation

**Scenario: Dangerous Migration Detected**

Input: Tech Lead reviewing migration adding indexed column with default

Expected output:
```
Database Migration Check:
- Database: postgresql
- Framework: alembic
- Migrations analyzed: 3

⚠️  DANGEROUS OPERATIONS: 2
- CRITICAL (1): ADD COLUMN with DEFAULT locks table (migration_001.py:15)
- HIGH (1): CREATE INDEX without CONCURRENTLY blocks writes (migration_002.py:23)

Safe migrations: 1

Top recommendations:
1. For ADD COLUMN: Add as NULL first, backfill in batches, then add DEFAULT
2. For CREATE INDEX: Use CREATE INDEX CONCURRENTLY to avoid locks

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/db_migration_check.json
```

**Scenario: All Migrations Safe**

Input: Tech Lead reviewing well-written migrations

Expected output:
```
Database Migration Check:
- Database: postgresql
- Framework: django
- Migrations analyzed: 2

✅ No dangerous operations detected

Safe migrations: 2
- migration_001.py: ADD COLUMN (nullable, no default)
- migration_002.py: CREATE INDEX CONCURRENTLY

All migrations follow zero-downtime best practices.

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/db_migration_check.json
```

---

## Error Handling

**If no migrations found:**
- Return: "No pending migrations found."

**If database type unknown:**
- Return: "Could not detect database type. Please specify."

**If migration files unreadable:**
- Return partial results with error notes

---

## Notes

- The script handles all pattern detection for multiple databases
- Detects PostgreSQL, MySQL, SQL Server, MongoDB operations
- Focuses on zero-downtime migration practices
- Provides specific safe alternatives for each dangerous operation
- Prioritizes CRITICAL issues (data loss, major downtime)
