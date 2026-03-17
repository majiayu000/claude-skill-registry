---
name: "db-lint-manager"
description: "Lint PostgreSQL functions against schema, analyze usage, and generate fix reports; use when detecting broken functions, validating schema contracts, or cleaning up unused database functions"
version: "1.0.0"
last_updated: "2025-12-03"
---

# Database Function Lint Manager

Lint PostgreSQL functions across environments (local, staging, production), analyze function usage in the codebase, and generate actionable reports for fixing or dropping broken functions.

## When to Use This Skill

**DO use this skill when:**
- Running `supabase db lint` and need to analyze/categorize results
- Detecting broken functions referencing non-existent columns/tables
- Analyzing which database functions are actually used in the codebase
- Generating cleanup recommendations for unused legacy functions
- Pre-deployment database validation
- Investigating database errors related to function calls

**DO NOT use this skill when:**
- Creating new database migrations (use `database-migration-manager`)
- Writing RLS policies (use `rls-policy-generator`)
- Fixing a single known function (just create the migration directly)

---

## Critical Rules (NEVER VIOLATE)

1. **REPORT ONLY** - Never auto-generate fix migrations without explicit user approval
2. **ANALYZE USAGE FIRST** - Always check if a function is used before recommending actions
3. **CATEGORIZE BY SEVERITY** - Separate critical (used) from low priority (unused)
4. **PRESERVE FUNCTION SIGNATURES** - When fixing, maintain existing function signatures for backwards compatibility
5. **TEST LOCALLY FIRST** - Always test fixes on local before staging/production

---

## Quick Reference

### Run Lint by Environment

```bash
# Local database (requires Docker/Supabase running)
cd apps/web && pnpm supabase db lint --local -s public

# Staging database
pnpm supabase db lint --db-url "postgresql://postgres.PROJECT_REF:PASSWORD@aws-1-eu-central-1.pooler.supabase.com:5432/postgres" -s public

# Production database (linked project)
cd apps/web && pnpm supabase db lint --linked -s public
```

### Analyze Function Usage

```bash
# Search for function usage in codebase
grep -rn "\.rpc(['\"]function_name['\"]" apps/web packages/features

# Check if function is called from migrations
grep -rn "function_name" apps/web/supabase/migrations/
```

### Output Format Options

```bash
# JSON output for parsing
pnpm supabase db lint --linked -o json

# Pretty output for human reading
pnpm supabase db lint --linked -o pretty
```

---

## Issue Categories

### 1. Missing Column
**Error**: `column X does not exist`
**Cause**: Function references a column that was renamed, dropped, or never existed
**Fix Options**:
- Update function to use correct column name
- Drop function if unused

### 2. Missing Table
**Error**: `relation X does not exist`
**Cause**: Function references a table that was renamed or dropped
**Fix Options**:
- Update function to use correct table name
- Drop function if unused

### 3. Type Mismatch
**Error**: `structure of query does not match function result type`
**Cause**: Function return type doesn't match actual SELECT columns
**Fix Options**:
- Update function return type definition
- Update SELECT to match return type

### 4. Ambiguous Reference
**Error**: `column reference X is ambiguous`
**Cause**: Column name exists in multiple tables in the query
**Fix Options**:
- Qualify column with table alias (e.g., `t.user_id` instead of `user_id`)
- Rename parameter to avoid collision

### 5. Unused Variable
**Warning**: `never read variable X`
**Cause**: Variable declared but not used in function body
**Fix Options**:
- Remove unused variable declaration
- Use the variable as intended

---

## Usage Analysis Patterns

### TypeScript/JavaScript Patterns

```typescript
// Direct RPC call
const { data } = await supabase.rpc('function_name', { param: value });

// Chained RPC
await client.rpc('function_name').single();

// In service files
return this.client.rpc('function_name', params);
```

### SQL Patterns (Migrations/Triggers)

```sql
-- Direct call
SELECT public.function_name(arg1, arg2);

-- In trigger
EXECUTE FUNCTION public.function_name();

-- In policy
USING (public.function_name())
```

### Search Commands

```bash
# Find all RPC calls to a function
grep -rn "rpc(['\"]get_events_with_cast['\"]" apps/web packages/features

# Find SQL references
grep -rn "get_events_with_cast" apps/web/supabase/

# Find in tests
grep -rn "get_events_with_cast" apps/web/app/__tests__/
```

---

## Report Template

When generating a lint report, use this format:

```markdown
# Database Function Lint Report

**Environment**: Production | Staging | Local
**Date**: YYYY-MM-DD HH:MM
**Total Issues**: N (M errors, K warnings)

## Summary

| Category | Count | Used | Unused |
|----------|-------|------|--------|
| Missing Column | N | N | N |
| Missing Table | N | N | N |
| Type Mismatch | N | N | N |
| Ambiguous Reference | N | N | N |
| Unused Variable | N | N | N |

## Critical Issues (Used Functions - Must Fix)

### function_name
- **Error**: Description of the error
- **SQL State**: XXXXX
- **Location**: Migration file where function is defined
- **Line**: Line number in function
- **Usage Found**:
  - file/path.ts:123
  - file/path2.ts:456
- **Recommended Action**: Create migration to fix X

<details>
<summary>Problematic Query</summary>

```sql
SELECT column_that_doesnt_exist FROM table
```

</details>

## Low Priority (Unused Functions - Consider Dropping)

### function_name
- **Error**: Description of the error
- **Location**: Migration file
- **Usage Found**: NONE
- **Recommended Action**: Create DROP FUNCTION IF EXISTS migration

## Warnings (Non-Critical)

### function_name
- **Warning**: unused variable "v_temp"
- **Impact**: No runtime impact, code cleanliness only
- **Recommended Action**: Low priority cleanup

## Action Summary

- **Must Fix**: N functions actively in use with errors
- **Consider Drop**: N functions with no usage found
- **Investigate**: N functions with unclear status
- **Low Priority**: N warnings (non-blocking)

## Next Steps

1. For critical issues, create fix migrations:
   ```bash
   pnpm supabase:web migrations new fix_function_name
   ```

2. For unused functions, create drop migrations:
   ```sql
   DROP FUNCTION IF EXISTS public.function_name(param_types);
   ```

3. Test locally before deploying:
   ```bash
   pnpm supabase:web:reset
   pnpm supabase:web db lint --local
   ```
```

---

## Known Issues Reference

These functions were detected as broken in production (2025-12-03):

| Function | Error | Category | Likely Status |
|----------|-------|----------|---------------|
| `get_user_bookmarks` | profile_bookmarks.notes doesn't exist | Missing Column | Legacy/Unused |
| `is_following_profile` | following_profile_id doesn't exist | Missing Column | Legacy/Unused |
| `get_user_following` | following_profile_id doesn't exist | Missing Column | Legacy/Unused |
| `get_user_upcoming_events` | participations table doesn't exist | Missing Table | Legacy/Unused |
| `update_identity_verification_status` | admin_notes doesn't exist | Missing Column | Legacy/Unused |
| `user_has_verified_identity` | iv.status doesn't exist | Missing Column | Legacy/Unused |
| `get_user_identity_verification` | iv.status doesn't exist | Missing Column | Legacy/Unused |
| `get_dancer_availability` | available_date doesn't exist | Missing Column | Legacy/Unused |
| `transfer_team_account_ownership` | accounts_memberships.role doesn't exist | Missing Column | Legacy/Unused |
| `log_role_change` | role_change_audit.user_id doesn't exist | Missing Column | Legacy/Unused |
| `get_dancer_upcoming_events` | return type mismatch | Type Mismatch | Needs Investigation |
| `get_profile_missing_fields` | primary_training_method doesn't exist | Missing Column | Possibly Used |
| `accept_admin_invitation` | ambiguous user_id reference | Ambiguous Reference | Possibly Used |
| `get_events_with_cast` | e.name doesn't exist (should be e.title) | Missing Column | Likely Used |
| `get_event_with_cast_by_id` | e.name doesn't exist | Missing Column | Likely Used |
| `get_user_events` | event_participations table doesn't exist | Missing Table | Legacy/Unused |
| `create_hire_order_with_items` | unit_price column doesn't exist | Missing Column | Needs Investigation |

---

## Environment Configuration

### Local
- Requires Docker and Supabase running (`pnpm supabase:web:start`)
- Uses `--local` flag
- Safe for testing fixes

### Staging
**Project**: `hxpcknyqswetsqmqmeep`
**Connection**:
```bash
# Load password from .env.local (preferred)
source apps/web/.env.local 2>/dev/null

# Or use environment variable directly
export SUPABASE_DB_PASSWORD_STAGING="your_password"

# 1Password fallback (if not in .env.local)
if [ -z "$SUPABASE_DB_PASSWORD_STAGING" ]; then
  SUPABASE_DB_PASSWORD_STAGING=$(op item get rkzjnr5ffy5u6iojnsq3clnmia --fields notesPlain --reveal)
fi
```

### Production
**Project**: `csjruhqyqzzqxnfeyiaf`
- Uses `--linked` flag (requires `supabase link` setup)
- READ ONLY - never apply fixes directly

---

## Workflow: Fixing Broken Functions

### Step 1: Generate Report
```bash
# Run lint on production
cd apps/web && pnpm supabase db lint --linked -s public -o json > lint-report.json
```

### Step 2: Analyze Usage
For each function in the report:
```bash
# Check codebase for usage
grep -rn "rpc(['\"]function_name['\"]" apps/web packages/features

# Check migrations for references
grep -rn "function_name" apps/web/supabase/migrations/
```

### Step 3: Categorize
- **CRITICAL**: Function is used in production code → Must fix
- **LOW**: Function has no usage → Consider dropping
- **INVESTIGATE**: Unclear if used → Research before action

### Step 4: Create Fix Migration
```bash
# Create new migration
pnpm supabase:web migrations new fix_broken_function_name

# Edit the migration file with the fix
```

### Step 5: Test Locally
```bash
pnpm supabase:web:reset
pnpm supabase db lint --local -s public
```

### Step 6: Deploy
Follow standard migration deployment process via `database-migration-manager` skill.

---

## Integration with Existing Tools

### validate-db-contracts.sh
Located at `.claude/skills/db-lint-manager/scripts/validate-db-contracts.sh`
- Validates specific functions against table schemas
- Complements lint by checking column existence

### validate-function-schema.sh
Located at `.claude/skills/db-lint-manager/scripts/validate-function-schema.sh`
- Validates `atomic_profile_update` function specifically
- Can be extended for other critical functions

### Pre-commit Hooks
The lint can be integrated into pre-commit hooks for migrations:
```yaml
# In lefthook.yml
pre-commit:
  commands:
    db-lint:
      glob: "apps/web/supabase/migrations/*.sql"
      run: cd apps/web && pnpm supabase db lint --local -s public
```

---

## Troubleshooting

### "Cannot connect to database"
- Ensure Docker is running for local lint
- Check credentials for staging/production
- Try session mode port (5432) if transaction mode (6543) fails

### "Function not found in lint output"
- Function may be in a different schema (check `-s` flag)
- Function may have been dropped already
- Function may be defined in a different way (trigger vs standalone)

### "False positive - function actually works"
- plpgsql_check is conservative; some valid patterns may flag
- Test the function manually to verify
- Add to known false positives list if confirmed working

---

## Related Skills

- **database-migration-manager**: For creating and deploying migrations
- **rls-policy-generator**: For RLS policy issues
- **quality-auto-fixer**: For general code quality checks
