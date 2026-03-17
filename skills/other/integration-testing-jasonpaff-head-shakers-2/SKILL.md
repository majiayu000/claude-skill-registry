---
name: integration-testing
description: Enforces project integration testing conventions for facades, server actions, and database operations using Testcontainers with real PostgreSQL.
---

# Integration Testing Skill

## Purpose

This skill provides integration testing conventions for facades, server actions, and database operations. Integration tests use real database interactions via Testcontainers.

## Activation

This skill activates when:

- Creating or modifying files in `tests/integration/`
- Testing facades or business logic
- Testing server actions
- Testing database queries with real data
- Working with Testcontainers

## File Patterns

- `tests/integration/**/*.test.ts`
- `tests/integration/**/*.integration.test.ts`

## Workflow

1. Detect integration test work (file path contains `tests/integration/`)
2. Load `references/Integration-Testing-Conventions.md`
3. Also load `testing-base` skill for shared conventions
4. Apply integration test patterns with database helpers
5. Ensure proper database cleanup between tests

## Key Patterns (REQUIRED)

### Database Management

- Database auto-starts via global setup (Testcontainers)
- Use `getTestDb()` from `tests/setup/test-db.ts`
- Use `resetTestDatabase()` or `cleanupTable()` in `beforeEach`
- Mock `@/lib/db` to use test database

### Factory Usage

- Use factories from `tests/fixtures/` for test data
- Create realistic test scenarios with proper relationships
- Clean up created data between tests

### External Service Mocking

- Mock Sentry for breadcrumb verification
- Mock CacheService for cache behavior control
- Mock Redis client to avoid connection issues

## References

- `references/Integration-Testing-Conventions.md` - Complete integration testing conventions
