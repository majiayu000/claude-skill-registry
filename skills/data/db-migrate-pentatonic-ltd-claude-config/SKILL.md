---
name: db-migrate
description: Run D1 database migrations for Cloudflare. Use when applying schema changes, creating new tables, or modifying database structure.
allowed-tools: Bash(wrangler:*), Bash(npx:*), Read, Glob, Grep
---

# D1 Database Migrations

## Project Database
- Database name: `agentic-commerce-p2p-db`
- Location: `migrations/` directory

## List Existing Migrations
```bash
ls -la migrations/
```

## Apply Migrations (Remote)
```bash
npx wrangler d1 execute agentic-commerce-p2p-db --remote --file=migrations/YOUR_MIGRATION.sql
```

## Apply All Pending Migrations
```bash
npx wrangler d1 migrations apply agentic-commerce-p2p-db --remote
```

## Check Current Schema
```bash
npx wrangler d1 execute agentic-commerce-p2p-db --remote --command="SELECT name FROM sqlite_master WHERE type='table';"
```

## Creating New Migrations
1. Create file: `migrations/NNN_description.sql`
2. Use sequential numbering (e.g., 019, 020)
3. Include both up and down if possible
4. Test locally first with `--local` flag

## Local Testing
```bash
npx wrangler d1 execute agentic-commerce-p2p-db --local --file=migrations/YOUR_MIGRATION.sql
```

## Rollback
D1 doesn't have built-in rollback. Create a reverse migration manually.

## Best Practices
- Always backup before major schema changes
- Test migrations locally first
- Use transactions where possible
- Document breaking changes
