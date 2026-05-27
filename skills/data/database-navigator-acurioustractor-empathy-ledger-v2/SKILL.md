---
name: database-navigator
description: Navigate and understand the Empathy Ledger database schema, migrations, functions, and relationships.
---

# Database Navigator

Navigate the complex database architecture - tables, functions, views, indexes, and policies.

## When to Use
- Exploring database tables and relationships
- Finding database functions and triggers
- Understanding migration history
- Reviewing RLS policies
- Documenting database subsystems

## Quick Reference

### Key Table Groups
| Group | Tables |
|-------|--------|
| **Users** | profiles, organizations, organization_members |
| **Content** | stories, storytellers, transcripts |
| **Media** | media_assets, media_usage |
| **Cultural** | cultural_backgrounds, protocols |

### Migration Location
`supabase/migrations/` - SQL files with timestamps

### Common Operations
```sql
-- List all tables
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';

-- Find table columns
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'your_table';

-- Check RLS policies
SELECT * FROM pg_policies WHERE tablename = 'your_table';
```

## Reference Files
| Topic | File |
|-------|------|
| Query examples | `refs/queries.md` |
| Connection setup | `refs/connection.md` |
| Full documentation | `docs/04-database/SUPABASE_COMPLETE_OVERVIEW.md` |

## Related Skills
- `supabase-connection` - Database clients and migrations
- `supabase-sql-manager` - SQL operations
- `data-analysis` - Analysis patterns
