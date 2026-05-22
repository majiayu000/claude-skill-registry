---
name: verify
description: Pre-commit verification - checks changes won't break the deployed app or corrupt the database
---

# Pre-Commit Verification

Before committing and pushing, verify that changes across all layers of the app are consistent and safe.

## CRITICAL CONTEXT

This is a **deployed production app** with a **live PostgreSQL database containing real data**. The user NEVER runs commands directly on the live database. Schema changes happen automatically when the app restarts through the build/deploy process.

**Deployment flow:**
1. Code is pushed to git
2. Coolify rebuilds Docker container
3. On startup, `main.py` runs: `migrate_db()` → `init_db()` → `seed_db()`
4. Migrations execute automatically against the live database

**If a migration is wrong, data could be lost or corrupted with no easy recovery.**

## APP ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React/TS)                      │
│  /frontend/src/types/*.ts  ←→  /frontend/src/api/*.ts       │
└─────────────────────────────────────────────────────────────┘
                              ↓ REST API
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Python/FastAPI)                  │
│  /routes/*.py (REST)  ←→  /tools/*.py (MCP for Claude)      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     DATABASE LAYER                           │
│  /db/*.py  ←→  /db/validation.py  ←→  /db/connection.py     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      POSTGRESQL                              │
│  Schema defined in: /db/connection.py (init_db, migrate_db) │
│  Migrations in: /migrations/*.sql                           │
└─────────────────────────────────────────────────────────────┘
```

## VERIFICATION CHECKLIST

Run through these checks based on what was changed:

### 1. DATABASE SCHEMA CHANGES

If any changes to `/db/connection.py` (init_db or migrate_db) or `/migrations/*.sql`:

**Migration Safety Checks:**
- [ ] Migration is idempotent (uses `IF EXISTS`, `IF NOT EXISTS`, checks column existence)
- [ ] Migration preserves existing data (no `DROP TABLE` without migration, no `TRUNCATE`)
- [ ] Migration handles NULL values when adding NOT NULL columns
- [ ] Foreign key order is correct (referenced tables must exist)
- [ ] Index names are unique and follow naming convention `idx_{table}_{column}`

**Data Migration Checks:**
- [ ] If removing a column, data is migrated to new location FIRST
- [ ] If changing column type, existing data is safely converted
- [ ] If adding constraints, existing data satisfies them

**Read these files to verify:**
- `/db/connection.py` - Check `migrate_db()` function around line 89
- `/db/connection.py` - Check `init_db()` function around line 610
- `/migrations/*.sql` - Any new or modified migration files
- `/schema.sql` - Reference for full schema (not used in prod, but documents intent)

### 2. TYPE CONSISTENCY

If any changes to types, ensure they match across all layers:

**Frontend Types → Backend:**
```
/frontend/src/types/*.ts  ←→  /db/validation.py (constants)
                          ←→  /db/*.py (function signatures)
                          ←→  /routes/*.py (response structures)
                          ←→  /tools/*.py (MCP tool returns)
```

**Check these specific mappings:**
- `CaseStatus` values in `/frontend/src/types/common.ts` match `CASE_STATUSES` in `/db/validation.py`
- `TaskStatus` values match `TASK_STATUSES`
- `PersonType` values match `DEFAULT_PERSON_TYPES`
- `PersonSide` values match `PERSON_SIDES`

**Property name consistency:**
- Frontend uses camelCase OR snake_case? (This app uses snake_case throughout)
- JSONB fields (phones, emails, attributes) have matching structures
- Date fields use ISO string format (YYYY-MM-DD or full ISO timestamp)

### 3. API CONTRACT CONSISTENCY

If any changes to API endpoints or their responses:

**REST Routes (`/routes/*.py`):**
- Response structure matches frontend type definition
- Error responses use format: `{"success": false, "error": {"message": "...", "code": "..."}}`
- All routes have `auth.require_auth(request)` check
- Query params and body parsing matches frontend API calls

**MCP Tools (`/tools/*.py`):**
- Return same data structure as equivalent REST endpoint
- Tool parameters have correct types and descriptions
- Error handling uses `error_response()`, `validation_error()`, `not_found_error()` helpers

**Frontend API (`/frontend/src/api/*.ts`):**
- Function signatures match route parameters
- Return types match actual response structure
- New functions are exported from `/frontend/src/api/index.ts`

### 4. BUILD VERIFICATION

**Run these commands:**
```bash
# Frontend TypeScript check
cd frontend && npm run build

# If build fails, fix TypeScript errors before proceeding
```

**Common build issues:**
- Unused imports (remove them)
- Type mismatches (check property names, optional vs required)
- Missing exports from barrel files (index.ts)

### 5. EXPORTS AND IMPORTS

If adding new functions or types:

**Database layer:**
- [ ] New db functions exported from `/db/__init__.py`
- [ ] New db functions added to `__all__` list

**Frontend types:**
- [ ] New types exported from `/frontend/src/types/{domain}.ts`
- [ ] New types re-exported from `/frontend/src/types/index.ts`

**Frontend API:**
- [ ] New API functions exported from `/frontend/src/api/{domain}.ts`
- [ ] New API functions re-exported from `/frontend/src/api/index.ts`

**Backend routes:**
- [ ] New route module registered in `/routes/__init__.py`

**Backend tools:**
- [ ] New tool module registered in `/tools/__init__.py`

### 6. BACKWARDS COMPATIBILITY

If changing existing APIs or data structures:

- [ ] Existing frontend code still works with new backend
- [ ] Existing data in database is still valid
- [ ] No breaking changes to MCP tools (Claude integrations depend on them)
- [ ] Consider adding new fields as optional first, then migrating

## MIGRATION SAFETY PATTERNS

**Safe: Adding a new nullable column**
```sql
ALTER TABLE foo ADD COLUMN IF NOT EXISTS bar TEXT;
```

**Safe: Adding a new table**
```sql
CREATE TABLE IF NOT EXISTS foo (...);
```

**Safe: Adding an index**
```sql
CREATE INDEX IF NOT EXISTS idx_foo_bar ON foo(bar);
```

**DANGEROUS: Removing a column**
```sql
-- MUST migrate data first, then drop
INSERT INTO new_location SELECT ... FROM old_table WHERE old_column IS NOT NULL;
ALTER TABLE foo DROP COLUMN IF EXISTS bar;
```

**DANGEROUS: Adding NOT NULL without default**
```sql
-- This will fail if table has rows
ALTER TABLE foo ADD COLUMN bar TEXT NOT NULL;

-- Safe version:
ALTER TABLE foo ADD COLUMN bar TEXT;
UPDATE foo SET bar = 'default' WHERE bar IS NULL;
ALTER TABLE foo ALTER COLUMN bar SET NOT NULL;
```

**DANGEROUS: Changing column type**
```sql
-- Check that all existing values can convert
ALTER TABLE foo ALTER COLUMN bar TYPE INTEGER USING bar::INTEGER;
```

## FINAL VERIFICATION

Before committing, confirm:

1. **Build passes:** `cd frontend && npm run build` succeeds
2. **No console errors:** Check browser console in dev mode
3. **Migration is safe:** Will not corrupt or lose production data
4. **Types are consistent:** Frontend types match backend responses
5. **Exports are complete:** New code is properly exported

## QUICK REFERENCE: Key Files by Domain

| Domain | DB | Routes | Tools | API | Types |
|--------|-----|--------|-------|-----|-------|
| Cases | `/db/cases.py` | `/routes/cases.py` | `/tools/cases.py` | `/frontend/src/api/cases.ts` | `/frontend/src/types/case.ts` |
| Persons | `/db/persons.py` | `/routes/persons.py` | `/tools/persons.py` | `/frontend/src/api/persons.ts` | `/frontend/src/types/person.ts` |
| Tasks | `/db/tasks.py` | `/routes/tasks.py` | `/tools/tasks.py` | `/frontend/src/api/tasks.ts` | `/frontend/src/types/task.ts` |
| Events | `/db/events.py` | `/routes/events.py` | `/tools/events.py` | `/frontend/src/api/events.ts` | `/frontend/src/types/event.ts` |
| Proceedings | `/db/proceedings.py` | `/routes/proceedings.py` | `/tools/proceedings.py` | `/frontend/src/api/proceedings.ts` | `/frontend/src/types/proceeding.ts` |
| Activities | `/db/activities.py` | `/routes/activities.py` | `/tools/activities.py` | `/frontend/src/api/activities.ts` | `/frontend/src/types/activity.ts` |
| Notes | `/db/notes.py` | `/routes/notes.py` | `/tools/notes.py` | `/frontend/src/api/notes.ts` | `/frontend/src/types/note.ts` |
| Jurisdictions | `/db/jurisdictions.py` | `/routes/stats.py` | `/tools/jurisdictions.py` | `/frontend/src/api/stats.ts` | `/frontend/src/types/common.ts` |

**Validation constants:** `/db/validation.py`
**DB exports:** `/db/__init__.py`
**Migration logic:** `/db/connection.py` (migrate_db ~line 89, init_db ~line 610)
**SQL migrations:** `/migrations/*.sql`

---

Now review the git diff and verify each changed file against these checks. Report any concerns before proceeding with the commit.
