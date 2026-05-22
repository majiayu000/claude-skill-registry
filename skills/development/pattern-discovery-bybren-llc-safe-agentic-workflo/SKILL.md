---
name: pattern-discovery
description: Pattern library discovery for pattern-first development. Use BEFORE implementing any new feature, creating components, writing API routes, or adding database operations. Ensures existing patterns are checked first before writing new code.
---

# Pattern Discovery Skill

## Purpose

Enforce pattern-first development by checking the Pattern library before implementing new functionality. This reduces code duplication, ensures consistency, and leverages battle-tested solutions.

## When to Use

Invoke this skill when:

- About to create a new API route
- About to create a new UI component
- About to add database operations
- About to write integration tests
- User asks "how do I implement..." or "how should I build..."
- Starting work on any feature implementation

## Pattern Discovery Protocol

**ALWAYS follow this sequence before writing new code:**

### Step 1: Check Pattern Library

Search `docs/patterns/` for existing patterns:

```bash
# Find patterns by category
ls docs/patterns/api/      # API route patterns
ls docs/patterns/ui/       # UI component patterns
ls docs/patterns/database/ # Database operation patterns
ls docs/patterns/testing/  # Testing patterns
```

### Step 2: Review Pattern Index

Check `docs/patterns/README.md` for the complete pattern index:

| Category | Patterns Available                                                          |
| -------- | --------------------------------------------------------------------------- |
| API      | User Context, Admin Context, Webhook Handler, Zod Validation, Bonus Content |
| UI       | Authenticated Page, Form with Validation, Data Table, Marketing Page        |
| Database | RLS Migration, Prisma Transaction, Server Component Access                  |
| Testing  | API Integration Test, E2E User Flow                                         |

### Step 3: Apply or Escalate

**If pattern exists:**

1. Read the pattern file
2. Copy the code pattern
3. Follow the customization guide
4. Run validation commands

**If pattern is missing:**

1. Search codebase for similar implementations
2. If found, consider extracting as new pattern (BSA/ARCHitect only)
3. If not found, implement from scratch following existing conventions
4. Report pattern gap to BSA for future extraction

## Pattern Library Structure

```
docs/patterns/
├── README.md           # Pattern index and usage guide
├── api/
│   ├── user-context-api.md
│   ├── admin-context-api.md
│   ├── webhook-handler.md
│   ├── zod-validation-api.md
│   └── bonus-content-delivery.md
├── ui/
│   ├── authenticated-page.md
│   ├── form-with-validation.md
│   ├── data-table.md
│   └── marketing-page.md
├── database/
│   ├── rls-migration.md
│   ├── prisma-transaction.md
│   └── server-component-direct-access.md
├── testing/
│   ├── api-integration-test.md
│   └── e2e-user-flow.md
└── ci/
    ├── service-configuration-pattern.md
    └── database-setup-pattern.md
```

## Pattern Matching Guide

| If you need to...                  | Use this pattern                  |
| ---------------------------------- | --------------------------------- |
| Create authenticated API endpoint  | `api/user-context-api.md`         |
| Create admin-only API endpoint     | `api/admin-context-api.md`        |
| Handle external webhooks           | `api/webhook-handler.md`          |
| Validate API input with Zod        | `api/zod-validation-api.md`       |
| Serve private downloadable content | `api/bonus-content-delivery.md`   |
| Create protected page              | `ui/authenticated-page.md`        |
| Build form with validation         | `ui/form-with-validation.md`      |
| Display paginated data             | `ui/data-table.md`                |
| Create marketing/landing page      | `ui/marketing-page.md`            |
| Add new table with RLS             | `database/rls-migration.md`       |
| Run multi-step DB operations       | `database/prisma-transaction.md`  |
| Test API endpoints                 | `testing/api-integration-test.md` |
| Write E2E user flow tests          | `testing/e2e-user-flow.md`        |

## Security Requirements

All patterns enforce:

- **RLS Context** - Database operations use `withUserContext`, `withAdminContext`, or `withSystemContext`
- **Authentication** - Protected routes verify auth before processing
- **Input Validation** - All inputs validated with Zod schemas
- **Error Handling** - Comprehensive error handling with proper status codes

## Validation Commands

After applying a pattern, run:

```bash
yarn lint && yarn type-check  # All patterns
yarn test:integration         # API patterns
yarn test:e2e                 # UI patterns
```

## Authoritative Reference

- **Pattern Index**: `docs/patterns/README.md`
- **RLS Patterns**: See `rls-patterns` skill for database security
- **Frontend Patterns**: See `frontend-patterns` skill for UI conventions
