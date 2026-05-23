---
name: "flutter-query-lint"
description: "Lint Flutter Supabase queries against database schema; use when validating mobile app queries, debugging query failures, or before pushing mobile changes"
version: "1.0.0"
last_updated: "2026-01-05"
---

# Flutter Query Linter

Validates Supabase queries in Flutter API files against the database schema (`database.types.ts`). Reports mismatches in table names, column names, relationships, and RPC function calls.

## When to Use This Skill

**DO use this skill when:**
- Debugging Flutter API query failures
- Before pushing mobile app changes that modify queries
- After database schema changes to check for breaking changes
- Investigating "column does not exist" or similar errors
- Reviewing PRs that touch Flutter API files

**DO NOT use this skill when:**
- Writing new queries (just write them, then validate)
- The issue is clearly RLS/permissions related (not schema)
- Debugging non-query Flutter issues

---

## Quick Reference

### Run the Linter

```bash
# From project root
npx ts-node .claude/skills/flutter-query-lint/scripts/lint-queries.ts
```

### Output Format

The linter produces a markdown report with:
- **Errors**: Invalid table/column names, missing relationships
- **Warnings**: RPC functions that may have issues
- **Summary**: Statistics on validated queries

---

## Query Patterns Detected

### Table Queries
```dart
.from('table_name')
```

### Column Selections
```dart
// Simple
.select('col1, col2, col3')

// With relationships
.select('*, relation_name(col1, col2)')

// Aliased relationships
.select('alias:table_name!foreign_key(col1, col2)')

// Multiline
.select('''
  col1,
  col2,
  relation(nested_col)
''')
```

### Filters
```dart
.eq('column', value)
.inFilter('column', ['values'])
.gte('column', value)
.lte('column', value)
.neq('column', value)
```

### RPC Calls
```dart
.rpc('function_name')
.rpc('function_name', params: {...})
```

### Ordering
```dart
.order('column', ascending: true)
```

---

## Validation Rules

### 1. Table Existence
Checks that the table name in `.from('table')` exists in `database.types.ts`.

### 2. Column Existence
For each column in `.select()`, `.eq()`, `.order()`, etc., validates it exists on the target table.

**Note**: The linter handles:
- `*` wildcard (skipped)
- Nested relationships like `relation(col1, col2)`
- Aliased relationships like `alias:table!fk(col1)`

### 3. Relationship Resolution
For relationship queries like:
```dart
.select('productions(id, name)')
```
Validates that `productions` is either:
- A valid table name (implicit FK)
- An alias with explicit FK reference

### 4. RPC Function Existence
Checks `.rpc('function_name')` against `Functions` in `database.types.ts`.

---

## Common Issues

### Missing Column
```
Error: Column 'name' does not exist on table 'events'
Suggestion: Did you mean 'title'?
```
**Fix**: Update the query to use the correct column name.

### Invalid Table
```
Error: Table 'event_participations' does not exist
Suggestion: Did you mean 'event_participants'?
```
**Fix**: Use the correct table name.

### Unknown Relationship
```
Warning: Relationship 'venue' on 'events' cannot be validated
```
**Note**: May be valid if using implicit FK. Check manually.

### Missing RPC Function
```
Error: RPC function 'get_user_events' does not exist
```
**Fix**: Either create the function or remove the call.

---

## Integration with Development Workflow

### Before Committing Mobile Changes
```bash
# Run lint before committing API changes
npx ts-node .claude/skills/flutter-query-lint/scripts/lint-queries.ts
```

### After Schema Changes
When you modify the database schema:
1. Regenerate types: `pnpm supabase:web:typegen`
2. Run Flutter query lint to find broken queries
3. Fix any reported issues

---

## Files Scanned

The linter scans:
```
apps/mobile/lib/modules/*/api/*.dart
apps/mobile/lib/core/data/api/*.dart
```

## Schema Source

Validation uses:
```
apps/web/supabase/database.types.ts
```

---

## Limitations

1. **Dynamic queries**: Cannot validate queries built dynamically at runtime
2. **Computed columns**: Views may have columns not in base tables
3. **Complex select strings**: Very complex nested selections may not parse correctly
4. **RPC return types**: Doesn't validate RPC parameter types or return values

---

## Related Skills

- **db-lint-manager**: For PostgreSQL function validation
- **database-migration-manager**: For creating schema migrations
- **flutter-development**: For Flutter patterns and best practices
