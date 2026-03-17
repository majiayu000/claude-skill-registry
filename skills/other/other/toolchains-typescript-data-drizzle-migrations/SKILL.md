---
name: drizzle-migrations
description: "Migration-first database development workflow using Drizzle ORM for TypeScript/J..."
version: 1.0.0
tags: []
progressive_disclosure:
  entry_point:
    summary: "Migration-first database development workflow using Drizzle ORM for TypeScript/J..."
    when_to_use: "When working with drizzle-migrations or related functionality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Drizzle ORM Database Migrations (TypeScript)

Migration-first database development workflow using Drizzle ORM for TypeScript/JavaScript projects.

## When to Use This Skill

Use this skill when:
- Working with Drizzle ORM in TypeScript/JavaScript projects
- Need to create or modify database schema
- Want migration-first development workflow
- Setting up new database tables or columns
- Need to ensure schema consistency across environments

## Core Principle: Migration-First Development

**Critical Rule**: Schema changes ALWAYS start with migrations, never code-first.

### Why Migration-First?
- ✅ SQL migrations are the single source of truth
- ✅ Prevents schema drift between environments
- ✅ Enables rollback and versioning
- ✅ Forces explicit schema design decisions
- ✅ TypeScript types generated from migrations
- ✅ CI/CD can validate schema changes

### Anti-Pattern (Code-First)
❌ **WRONG**: Writing TypeScript schema first
```typescript
// DON'T DO THIS FIRST
export const users = pgTable('users', {
  id: uuid('id').primaryKey(),
  email: text('email').notNull(),
});
```

### Correct Pattern (Migration-First)
✅ **CORRECT**: Write SQL migration first
```sql
-- drizzle/0001_add_users_table.sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Complete Migration Workflow

### Step 1: Design Schema in SQL Migration

Create descriptive SQL migration file:

```sql
-- drizzle/0001_create_school_calendars.sql
CREATE TABLE school_calendars (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  academic_year TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Add indexes for query performance
CREATE INDEX idx_school_calendars_school_id ON school_calendars(school_id);
CREATE INDEX idx_school_calendars_academic_year ON school_calendars(academic_year);

-- Add constraints
ALTER TABLE school_calendars
  ADD CONSTRAINT check_date_range
  CHECK (end_date > start_date);
```

**Naming Convention**:
- Use sequential numbers: `0001_`, `0002_`, etc.
- Descriptive names: `create_school_calendars`, `add_user_roles`
- Format: `XXXX_descriptive_name.sql`

### Step 2: Generate TypeScript Definitions

Drizzle Kit generates TypeScript types from SQL:

```bash
# Generate TypeScript schema and snapshots
pnpm drizzle-kit generate

# Or using npm
npm run db:generate
```

**What This Creates**:
1. TypeScript schema files (if using `drizzle-kit push`)
2. Snapshot files in `drizzle/meta/XXXX_snapshot.json`
3. Migration metadata

### Step 3: Create Schema Snapshot

Snapshots enable schema drift detection:

```json
// drizzle/meta/0001_snapshot.json (auto-generated)
{
  "version": "5",
  "dialect": "postgresql",
  "tables": {
    "school_calendars": {
      "name": "school_calendars",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "school_id": {
          "name": "school_id",
          "type": "uuid",
          "notNull": true
        }
      }
    }
  }
}
```

**Snapshots in Version Control**:
- ✅ Commit snapshots to git
- ✅ Enables drift detection in CI
- ✅ Documents schema history

### Step 4: Implement TypeScript Schema

Now write TypeScript schema that mirrors SQL migration:

```typescript
// src/lib/db/schema/school/calendar.ts
import { pgTable, uuid, date, text, timestamp } from 'drizzle-orm/pg-core';
import { schools } from './school';

export const schoolCalendars = pgTable('school_calendars', {
  id: uuid('id').primaryKey().defaultRandom(),
  schoolId: uuid('school_id')
    .notNull()
    .references(() => schools.id, { onDelete: 'cascade' }),
  startDate: date('start_date').notNull(),
  endDate: date('end_date').notNull(),
  academicYear: text('academic_year').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
});

// Type inference
export type SchoolCalendar = typeof schoolCalendars.$inferSelect;
export type NewSchoolCalendar = typeof schoolCalendars.$inferInsert;
```

**Key Points**:
- Column names match SQL exactly: `school_id` → `'school_id'`
- TypeScript property names use camelCase: `schoolId`
- Constraints and indexes defined in SQL, not TypeScript
- Foreign keys reference other tables

### Step 5: Organize Schemas by Domain

Structure schemas for maintainability:

```
src/lib/db/schema/
├── index.ts              # Export all schemas
├── school/
│   ├── index.ts
│   ├── district.ts
│   ├── holiday.ts
│   ├── school.ts
│   └── calendar.ts
├── providers.ts
├── cart.ts
└── users.ts
```

**index.ts** (export all):
```typescript
// src/lib/db/schema/index.ts
export * from './school';
export * from './providers';
export * from './cart';
export * from './users';
```

**school/index.ts**:
```typescript
// src/lib/db/schema/school/index.ts
export * from './district';
export * from './holiday';
export * from './school';
export * from './calendar';
```

### Step 6: Add Quality Check to CI

Validate schema consistency in CI/CD:

```yaml
# .github/workflows/quality.yml
name: Quality Checks

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Check database schema drift
        run: pnpm drizzle-kit check

      - name: Verify migrations (dry-run)
        run: pnpm drizzle-kit push --dry-run
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}

      - name: Run type checking
        run: pnpm tsc --noEmit

      - name: Lint code
        run: pnpm lint
```

**CI Checks Explained**:
- `drizzle-kit check`: Validates snapshots match schema
- `drizzle-kit push --dry-run`: Tests migration without applying
- Type checking: Ensures TypeScript compiles
- Linting: Enforces code style

### Step 7: Test on Staging

Before production, test migration on staging:

```bash
# 1. Run migration on staging
STAGING_DATABASE_URL="..." pnpm drizzle-kit push

# 2. Verify schema
pnpm drizzle-kit check

# 3. Test affected API routes
curl https://staging.example.com/api/schools/calendars

# 4. Check for data integrity issues
# Run queries to verify data looks correct

# 5. Monitor logs for errors
# Check application logs for migration-related errors
```

**Staging Checklist**:
- [ ] Migration runs without errors
- [ ] Schema drift check passes
- [ ] API routes using new schema work correctly
- [ ] No data integrity issues
- [ ] Application logs show no errors
- [ ] Query performance acceptable

## Common Migration Patterns

### Adding a Column

```sql
-- drizzle/0005_add_user_phone.sql
ALTER TABLE users
ADD COLUMN phone TEXT;

-- Add index if querying by phone
CREATE INDEX idx_users_phone ON users(phone);
```

TypeScript:
```typescript
export const users = pgTable('users', {
  id: uuid('id').primaryKey(),
  email: text('email').notNull(),
  phone: text('phone'), // New column
});
```

### Creating a Junction Table

```sql
-- drizzle/0006_create_provider_specialties.sql
CREATE TABLE provider_specialties (
  provider_id UUID NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
  specialty_id UUID NOT NULL REFERENCES specialties(id) ON DELETE CASCADE,
  PRIMARY KEY (provider_id, specialty_id)
);

CREATE INDEX idx_provider_specialties_provider ON provider_specialties(provider_id);
CREATE INDEX idx_provider_specialties_specialty ON provider_specialties(specialty_id);
```

TypeScript:
```typescript
export const providerSpecialties = pgTable('provider_specialties', {
  providerId: uuid('provider_id')
    .notNull()
    .references(() => providers.id, { onDelete: 'cascade' }),
  specialtyId: uuid('specialty_id')
    .notNull()
    .references(() => specialties.id, { onDelete: 'cascade' }),
}, (table) => ({
  pk: primaryKey(table.providerId, table.specialtyId),
}));
```

### Modifying Column Type

```sql
-- drizzle/0007_change_price_to_decimal.sql
ALTER TABLE services
ALTER COLUMN price TYPE DECIMAL(10, 2);
```

TypeScript:
```typescript
import { decimal } from 'drizzle-orm/pg-core';

export const services = pgTable('services', {
  id: uuid('id').primaryKey(),
  name: text('name').notNull(),
  price: decimal('price', { precision: 10, scale: 2 }).notNull(),
});
```

### Adding Constraints

```sql
-- drizzle/0008_add_email_constraint.sql
ALTER TABLE users
ADD CONSTRAINT users_email_unique UNIQUE (email);

ALTER TABLE users
ADD CONSTRAINT users_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$');
```

## Configuration

### drizzle.config.ts

```typescript
import type { Config } from 'drizzle-kit';

export default {
  schema: './src/lib/db/schema/index.ts',
  out: './drizzle',
  driver: 'pg',
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
} satisfies Config;
```

### package.json Scripts

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate:pg",
    "db:push": "drizzle-kit push:pg",
    "db:studio": "drizzle-kit studio",
    "db:check": "drizzle-kit check:pg",
    "db:up": "drizzle-kit up:pg"
  }
}
```

## Migration Testing Workflow

### Local Testing

```bash
# 1. Create migration
echo "CREATE TABLE test (...)" > drizzle/0009_test.sql

# 2. Generate TypeScript
pnpm db:generate

# 3. Push to local database
pnpm db:push

# 4. Verify schema
pnpm db:check

# 5. Test in application
pnpm dev
# Manually test affected features

# 6. Run tests
pnpm test
```

### Rollback Strategy

```sql
-- drizzle/0010_add_feature.sql (up migration)
CREATE TABLE new_feature (...);

-- drizzle/0010_add_feature_down.sql (down migration)
DROP TABLE new_feature;
```

Apply rollback:
```bash
# Manually run down migration
psql $DATABASE_URL -f drizzle/0010_add_feature_down.sql
```

## Best Practices

### Do's
- ✅ Write SQL migrations first
- ✅ Use descriptive migration names
- ✅ Add indexes for foreign keys
- ✅ Include constraints in migrations
- ✅ Test migrations on staging before production
- ✅ Commit snapshots to version control
- ✅ Organize schemas by domain
- ✅ Use `drizzle-kit check` in CI

### Don'ts
- ❌ Never write TypeScript schema before SQL migration
- ❌ Don't skip staging testing
- ❌ Don't modify old migrations (create new ones)
- ❌ Don't forget to add indexes
- ❌ Don't use `drizzle-kit push` in production (use proper migrations)
- ❌ Don't commit generated files without snapshots

## Troubleshooting

### Schema Drift Detected
**Error**: `Schema drift detected`

**Solution**:
```bash
# Check what changed
pnpm drizzle-kit check

# Regenerate snapshots
pnpm drizzle-kit generate

# Review changes and commit
git add drizzle/meta/
git commit -m "Update schema snapshots"
```

### Migration Fails on Staging
**Error**: Migration fails with data constraint violation

**Solution**:
1. Rollback migration
2. Create data migration script
3. Run data migration first
4. Then run schema migration

```sql
-- First: Migrate data
UPDATE users SET status = 'active' WHERE status IS NULL;

-- Then: Add constraint
ALTER TABLE users
ALTER COLUMN status SET NOT NULL;
```

### TypeScript Types Out of Sync
**Error**: TypeScript types don't match database

**Solution**:
```bash
# Regenerate everything
pnpm db:generate
pnpm tsc --noEmit

# If still broken, check schema files
# Ensure column names match SQL exactly
```

## Related Skills

- `universal-data-database-migration` - Universal migration patterns
- `toolchains-typescript-data-drizzle` - Drizzle ORM usage patterns
- `toolchains-typescript-core` - TypeScript best practices
- `universal-debugging-verification-before-completion` - Verification workflows
