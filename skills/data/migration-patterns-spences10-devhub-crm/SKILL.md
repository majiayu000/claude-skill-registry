---
name: migration-patterns
# prettier-ignore
description: Database migration patterns for SQLite. Use when creating migrations, modifying schema, or running database changes.
---

# Migration Patterns

## Quick Start

```sql
-- migrations/001_add_tags.sql
-- Migration: Add Tags Feature
-- Created: 2025-01-15
-- Description: Adds tags table for organizing contacts

CREATE TABLE IF NOT EXISTS tags (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  name TEXT NOT NULL,
  color TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_tags_user_id ON tags(user_id);
```

## Core Principles

- **Dual approach**: Create migration in `migrations/` + update
  `schema.sql`
- **Naming**: `{number}_{description}.sql` (e.g., `001_add_tags.sql`)
- **Zero-padded numbers**: 001, 002, 003 (run alphabetically)
- **IF NOT EXISTS**: Always use for idempotency
- **One feature per migration**: Keep focused
- **Include indexes**: Add in same migration as tables
- **Never modify**: Once committed, create new migration instead

## Reference Files

- [migration-guide.md](references/migration-guide.md) - Complete
  workflow and examples
- [troubleshooting.md](references/troubleshooting.md) - Common issues

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual

LLM WORKFLOW (when editing this file):
1. Write/edit SKILL.md
2. Format (if formatter available)
3. Run: claude-skills-cli validate <path>
4. If multi-line description warning: run claude-skills-cli doctor <path>
5. Validate again to confirm
-->
