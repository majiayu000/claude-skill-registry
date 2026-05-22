---
description: "Comprehensive Flutter Supabase query testing: static validation, live testing, RLS verification, and CI integration. Use when validating queries before deployment, debugging query failures, or setting up query testing pipelines."
version: "1.0.0"
updated: "2026-01-07"
---

# Flutter Query Testing

Comprehensive guide for validating Flutter Supabase queries against database schema, testing them locally, and integrating into CI/CD pipelines. Catch query errors before they reach production.

## Table of Contents

1. [When to Use](#when-to-use)
2. [Quick Reference](#quick-reference)
3. [Query Patterns in Ballee](#query-patterns-in-ballee)
4. [Static Analysis](#static-analysis)
5. [Live Testing](#live-testing)
6. [RLS Testing](#rls-testing)
7. [Integration Testing](#integration-testing)
8. [CI/CD Integration](#cicd-integration)
9. [Common Issues](#common-issues)
10. [Related Skills](#related-skills)

---

## When to Use

**DO use this skill when:**
- Validating queries before merging PRs
- Debugging "column does not exist" errors
- After database schema changes
- Setting up query testing pipelines
- Writing integration tests for API layer
- Testing RLS policy behavior

**DO NOT use this skill when:**
- Issue is clearly UI-related (not API)
- Debugging non-Supabase Flutter code
- Working on web app queries (use `db-lint-manager`)

---

## Quick Reference

### Run Validation Scripts

```bash
# Static analysis (no DB needed)
cd apps/mobile
dart run scripts/validate_queries.dart

# Live testing (requires local Supabase)
dart run scripts/test_queries_local.dart

# Generate full report
dart run scripts/generate_query_report.dart
```

### Pre-commit Hook (automatic)

```yaml
# Already configured in lefthook.yml
pre-commit:
  flutter-query-static:
    glob: "apps/mobile/lib/**/api/**/*.dart"
    run: cd apps/mobile && dart run scripts/validate_queries.dart --changed-only
```

---

## Query Patterns in Ballee

### Generated Type Constants

Ballee uses generated Supabase types in `lib/core/generated/supabase/`:

```dart
// Table names
CastAssignment.table_name  // 'cast_assignments'
EventParticipant.table_name  // 'event_participants'

// Column names (prefixed with c_)
CastAssignment.c_userId  // 'user_id'
CastAssignment.c_assignmentStatus  // 'assignment_status'
Profile.c_firstName  // 'first_name'
```

### Query Patterns

```dart
// Simple query with generated constants
await _client
    .from(CastAssignment.table_name)
    .select()
    .eq(CastAssignment.c_userId, userId);

// Nested relationships
await _client
    .from(Conversations.table_name)
    .select('''
      *,
      participants:${ConversationParticipants.table_name}!inner(
        *,
        profile:${Profile.table_name}!conversation_participants_user_id_profiles_fkey(
          ${Profile.c_id},
          ${Profile.c_firstName}
        )
      )
    ''');

// RPC calls
await _client.rpc(
  'get_or_create_direct_conversation',
  params: {'p_other_user_id': otherUserId},
);
```

---

## Static Analysis

Static analysis validates queries without running them.

### What It Checks

| Check | Description | Example Error |
|-------|-------------|---------------|
| Table existence | Table name exists in schema | `Table 'event_participations' not found` |
| Column existence | Column exists on target table | `Column 'name' not found on 'events'` |
| Relationship validity | FK relationship exists | `Unknown relationship 'venue' on 'events'` |
| RPC function existence | Function exists in DB | `RPC 'get_user_data' not found` |
| Type constant usage | Generated constants are used | Warning: Use `Profile.c_id` instead of `'id'` |

### Algorithm

```
1. Parse all *_api.dart files
2. Extract Supabase calls:
   - .from('table') → table name
   - .select('columns') → column names
   - .eq('column', value) → filter column
   - .rpc('function') → RPC function
3. Load schema from lib/core/generated/supabase/
4. Validate each extracted element
5. Report errors with file:line references
```

### Output Format

```
Flutter Query Static Analysis
=============================

apps/mobile/lib/modules/schedule/api/schedule_api.dart
  Line 28: ✓ .from(CastAssignment.table_name) → cast_assignments
  Line 30: ✓ .select('id, assignment_status, ...')
  Line 43: ✓ .eq(CastAssignment.c_userId, _userId)

apps/mobile/lib/modules/inbox/api/inbox_api.dart
  Line 34: ✓ .from(Conversations.table_name) → conversations
  Line 47: ✗ .eq('conversation_participants.user_id', ...)
           Warning: Consider using generated constant

Summary: 45 queries validated, 0 errors, 2 warnings
```

---

## Live Testing

Live testing executes queries against local Supabase to catch runtime errors.

### Prerequisites

```bash
# Start local Supabase
cd apps/web
pnpm supabase:web:start

# Verify it's running
curl http://localhost:54321/rest/v1/
```

### What It Tests

| Test | Description |
|------|-------------|
| Query execution | Query runs without PostgreSQL errors |
| Response structure | Response matches expected shape |
| Performance | Query completes within threshold (default: 1000ms) |
| RLS behavior | Query respects RLS policies |

### Test Categories

```dart
// 1. Basic CRUD tests
// Verify queries execute successfully

// 2. Relationship tests
// Verify nested selects return correct structure

// 3. RLS tests
// Verify authenticated vs anonymous access

// 4. Edge case tests
// Empty results, null handling, special characters
```

### Output Format

```
Flutter Query Live Testing
==========================

Testing schedule_api.dart...
  ✓ getScheduleItems() - 3 rows in 45ms
  ✓ getUpcomingItems() - 1 row in 32ms

Testing inbox_api.dart...
  ✓ getConversations() - 2 rows in 78ms
  ✓ getConversation(id) - 1 row in 25ms
  ✗ getOrCreateDirectConversation() - RLS denied
    Error: new row violates row-level security policy

Summary: 12 tests, 11 passed, 1 failed
```

---

## RLS Testing

Testing Row Level Security is critical for mobile apps.

### Test Patterns

```dart
// Test 1: Authenticated user access
test('authenticated user can read own data', () async {
  await signInAsTestUser();

  final result = await _client
      .from('profiles')
      .select()
      .eq('id', testUserId);

  expect(result, isNotEmpty);
});

// Test 2: Cross-user isolation
test('user cannot read other user data', () async {
  await signInAsTestUser();

  final result = await _client
      .from('profiles')
      .select()
      .eq('id', otherUserId);

  expect(result, isEmpty); // RLS blocks access
});

// Test 3: Anonymous access
test('anonymous cannot access protected tables', () async {
  await signOut();

  expect(
    () => _client.from('profiles').select(),
    throwsA(isA<PostgrestException>()),
  );
});

// Test 4: Write permissions
test('user can only update own profile', () async {
  await signInAsTestUser();

  // Should succeed
  await _client
      .from('profiles')
      .update({'bio': 'updated'})
      .eq('id', testUserId);

  // Should fail (RLS)
  expect(
    () => _client
        .from('profiles')
        .update({'bio': 'hacked'})
        .eq('id', otherUserId),
    throwsA(isA<PostgrestException>()),
  );
});
```

### RLS Test Matrix

| Table | Anonymous | Authenticated (own) | Authenticated (other) | Super Admin |
|-------|-----------|---------------------|----------------------|-------------|
| profiles | - | CRUD | R (limited) | CRUD |
| events | R (public) | CRUD | R (public) | CRUD |
| messages | - | CRUD (participant) | - | CRUD |

---

## Integration Testing

Full integration tests for API classes.

### Test Setup

```dart
// test/modules/schedule/schedule_api_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

void main() {
  late SupabaseClient client;
  late ScheduleApi api;

  setUpAll(() async {
    // Initialize Supabase with local instance
    await Supabase.initialize(
      url: 'http://localhost:54321',
      anonKey: 'eyJ...', // Local anon key
    );
    client = Supabase.instance.client;
    api = ScheduleApi(client);
  });

  setUp(() async {
    // Sign in as test user before each test
    await client.auth.signInWithPassword(
      email: 'test@example.com',
      password: 'test123',
    );
  });

  tearDown(() async {
    await client.auth.signOut();
  });

  group('ScheduleApi', () {
    test('getScheduleItems returns items within date range', () async {
      final items = await api.getScheduleItems(
        startDate: DateTime(2026, 1, 1),
        endDate: DateTime(2026, 1, 31),
      );

      expect(items, isA<List<ScheduleItemEntity>>());
      for (final item in items) {
        expect(item.startDateTime.isAfter(DateTime(2026, 1, 1)), isTrue);
        expect(item.startDateTime.isBefore(DateTime(2026, 1, 31)), isTrue);
      }
    });

    test('getUpcomingItems returns next 30 days', () async {
      final items = await api.getUpcomingItems();

      final now = DateTime.now();
      final thirtyDaysLater = now.add(Duration(days: 30));

      for (final item in items) {
        expect(item.startDateTime.isAfter(now), isTrue);
        expect(item.startDateTime.isBefore(thirtyDaysLater), isTrue);
      }
    });
  });
}
```

### Mock Setup for Unit Tests

```dart
// For unit tests without DB, mock the Supabase client
import 'package:mocktail/mocktail.dart';

class MockSupabaseClient extends Mock implements SupabaseClient {}
class MockSupabaseQueryBuilder extends Mock implements SupabaseQueryBuilder {}

void main() {
  late MockSupabaseClient mockClient;
  late ScheduleApi api;

  setUp(() {
    mockClient = MockSupabaseClient();
    api = ScheduleApi(mockClient);

    // Setup mock responses
    final mockQueryBuilder = MockSupabaseQueryBuilder();
    when(() => mockClient.from(any())).thenReturn(mockQueryBuilder);
    when(() => mockQueryBuilder.select(any())).thenReturn(mockQueryBuilder);
    when(() => mockQueryBuilder.eq(any(), any())).thenReturn(mockQueryBuilder);
    when(() => mockQueryBuilder.execute()).thenAnswer(
      (_) async => PostgrestResponse(data: [], count: 0),
    );
  });

  test('calls correct table', () async {
    await api.getUpcomingItems();
    verify(() => mockClient.from('cast_assignments')).called(1);
  });
}
```

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/flutter-quality.yml
name: Flutter Quality

on:
  push:
    paths:
      - 'apps/mobile/**'
  pull_request:
    paths:
      - 'apps/mobile/**'

jobs:
  query-validation:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: supabase/postgres:15.1.0.147
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 54322:5432

    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.24.0'
          channel: 'stable'

      - name: Install dependencies
        run: cd apps/mobile && flutter pub get

      - name: Static Query Validation
        run: cd apps/mobile && dart run scripts/validate_queries.dart

      - name: Setup Supabase
        run: |
          cd apps/web
          npx supabase start

      - name: Live Query Testing
        run: cd apps/mobile && dart run scripts/test_queries_local.dart

      - name: Generate Report
        run: cd apps/mobile && dart run scripts/generate_query_report.dart

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: query-report
          path: apps/mobile/query-report.md
```

### Pre-commit Hook

```yaml
# lefthook.yml (additions)
pre-commit:
  commands:
    flutter-query-static:
      glob: "apps/mobile/lib/**/api/**/*.dart"
      run: |
        cd apps/mobile && dart run scripts/validate_queries.dart --changed-only
      fail_text: "Flutter query static validation failed"

pre-push:
  commands:
    flutter-query-live:
      glob: "apps/mobile/**/*.dart"
      run: |
        if pgrep -f "supabase" > /dev/null; then
          cd apps/mobile && dart run scripts/test_queries_local.dart
        else
          echo "Skipping live query tests (Supabase not running)"
        fi
      fail_text: "Flutter query live testing failed"
```

### Schema Sync Hook

```bash
#!/bin/bash
# apps/mobile/scripts/sync_schema.sh

set -e

echo "Regenerating Supabase types..."
cd ../web
npx supabase gen types dart --local > ../mobile/lib/core/generated/supabase/schema.dart

echo "Validating queries against new schema..."
cd ../mobile
dart run scripts/validate_queries.dart

echo "Schema sync complete!"
```

---

## Common Issues

### Issue: Column Not Found

```
Error: Column 'name' not found on table 'events'
Suggestion: Did you mean 'title'?
```

**Fix**: Use the correct column name. Check generated types in `lib/core/generated/supabase/`.

### Issue: Invalid FK Reference

```
Error: Unknown relationship 'venue' on 'events'
```

**Fix**: Use explicit FK syntax:
```dart
// Before
'venue(name, city)'

// After
'venue:venues!events_venue_id_fkey(name, city)'
```

### Issue: RPC Function Not Found

```
Error: RPC function 'get_user_data' not found
```

**Fix**: Verify function exists in migrations or create it:
```sql
CREATE OR REPLACE FUNCTION get_user_data(p_user_id uuid)
RETURNS json AS $$
  -- function body
$$ LANGUAGE sql SECURITY DEFINER;
```

### Issue: Generated Types Out of Date

```
Warning: Using hardcoded 'user_id' instead of Profile.c_userId
```

**Fix**: Regenerate types:
```bash
cd apps/web && pnpm supabase:web:typegen
```

### Issue: RLS Blocks Query

```
Error: new row violates row-level security policy
```

**Fix**: Check RLS policies in `apps/web/supabase/migrations/`. Common causes:
- Missing `is_super_admin()` bypass
- Incorrect `USING` clause
- Missing `WITH CHECK` for INSERT/UPDATE

---

## Related Skills

- **flutter-query-lint**: Basic static linting (superseded by this skill)
- **flutter-development**: General Flutter patterns
- **flutter-testing**: Test patterns for all Flutter code
- **database-migration-manager**: Creating schema changes
- **rls-policy-generator**: Writing RLS policies
- **test-patterns**: Web E2E test patterns (similar RLS testing)

---

## Files Reference

### API Files
```
apps/mobile/lib/modules/*/api/*_api.dart
apps/mobile/lib/core/data/api/*_api.dart
```

### Generated Types
```
apps/mobile/lib/core/generated/supabase/*.dart
```

### Scripts
```
apps/mobile/scripts/validate_queries.dart
apps/mobile/scripts/test_queries_local.dart
apps/mobile/scripts/generate_query_report.dart
apps/mobile/scripts/sync_schema.sh
```

### Test Files
```
apps/mobile/test/modules/*/api/*_api_test.dart
```
