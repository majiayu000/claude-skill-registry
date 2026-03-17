---
name: bear-migrate
description: Move mountains of data with patient strength. Wake from hibernation, gather the data, move it carefully, hibernate to verify, and wake again to confirm. Use when migrating data, transforming schemas, or moving between systems.
---

# Bear Migrate 🐻

The bear moves slowly but with unstoppable strength. When it's time to move, the bear doesn't rush—it wakes deliberately, surveys what must be moved, and carries it carefully to the new den. Some journeys take seasons. The bear is patient. Data arrives intact, or it doesn't arrive at all.

## When to Activate

- User asks to "migrate data" or "move this data"
- User says "transform the schema" or "update the database"
- User calls `/bear-migrate` or mentions bear/migration
- Database schema changes requiring data migration
- Moving data between systems or formats
- Upgrading to new data structures
- Splitting or merging tables
- Importing/exporting large datasets

**Pair with:** `bloodhound-scout` to understand data relationships first

---

## The Migration

```
WAKE → GATHER → MOVE → HIBERNATE → VERIFY
  ↓        ↲        ↓          ↲          ↓
Prepare  Collect   Execute   Review    Confirm
Tools    Data      Safely    Results   Success
```

### Phase 1: WAKE

*The bear stirs from hibernation, preparing for the long journey...*

Set up the migration environment:

**Understand the Territory:**

```typescript
// Document current state
interface MigrationPlan {
  source: {
    schema: string;
    estimatedRows: number;
    criticalTables: string[];
  };
  destination: {
    schema: string;
    newConstraints: string[];
  };
  transformation: {
    mappings: Record<string, string>;
    calculatedFields: string[];
    dataCleanup: string[];
  };
}
```

**Safety First:**

```bash
# Always backup before migrating
# SQLite
sqlite3 production.db ".backup backup-$(date +%Y%m%d).db"

# PostgreSQL
pg_dump -Fc production > backup-$(date +%Y%m%d).dump

# Or using your ORM's migration tools
npm run db:backup
```

**Migration Tools:**

```typescript
// Create migration script
// migrations/20260130_add_user_preferences.ts

import { Kysely, sql } from 'kysely';

export async function up(db: Kysely<any>): Promise<void> {
  // Add new table
  await db.schema
    .createTable('user_preferences')
    .addColumn('id', 'integer', (col) => col.primaryKey())
    .addColumn('user_id', 'integer', (col) => 
      col.references('users.id').onDelete('cascade')
    )
    .addColumn('theme', 'varchar(50)', (col) => col.defaultTo('system'))
    .addColumn('notifications', 'boolean', (col) => col.defaultTo(true))
    .addColumn('created_at', 'timestamp', (col) => col.defaultTo(sql`now()`))
    .execute();
  
  // Migrate existing data
  await sql`
    INSERT INTO user_preferences (user_id, theme)
    SELECT id, COALESCE(theme_preference, 'system')
    FROM users
    WHERE theme_preference IS NOT NULL
  `.execute(db);
  
  // Drop old column
  await db.schema.alterTable('users')
    .dropColumn('theme_preference')
    .execute();
}

export async function down(db: Kysely<any>): Promise<void> {
  // Reverse migration
  await db.schema.alterTable('users')
    .addColumn('theme_preference', 'varchar(50)')
    .execute();
    
  await sql`
    UPDATE users 
    SET theme_preference = (
      SELECT theme FROM user_preferences 
      WHERE user_preferences.user_id = users.id
    )
  `.execute(db);
  
  await db.schema.dropTable('user_preferences').execute();
}
```

**Output:** Migration plan documented, backups created, tools ready

---

### Phase 2: GATHER

*The bear collects berries and salmon, knowing exactly what it carries...*

Understand the data thoroughly:

**Data Inventory:**

```bash
# Count rows per table
npx wrangler d1 execute db --command="
  SELECT 
    'users' as table_name, count(*) as rows FROM users
  UNION ALL
  SELECT 'posts', count(*) FROM posts
  UNION ALL
  SELECT 'comments', count(*) FROM comments;
"

# Check for orphaned records
npx wrangler d1 execute db --command="
  SELECT count(*) as orphaned_comments
  FROM comments c
  LEFT JOIN posts p ON c.post_id = p.id
  WHERE p.id IS NULL;
"

# Find edge cases
npx wrangler d1 execute db --command="
  SELECT 
    max(length(content)) as max_content_length,
    min(created_at) as oldest_record,
    count(distinct status) as status_values
  FROM posts;
"
```

**Data Quality Check:**

```typescript
// Validate data before migration
const issues = [];

// Check for nulls in required fields
const nullEmails = await db.selectFrom('users')
  .where('email', 'is', null)
  .selectAll()
  .execute();

if (nullEmails.length > 0) {
  issues.push(`${nullEmails.length} users missing email`);
}

// Check for duplicates
const duplicates = await sql`
  SELECT email, count(*) as count
  FROM users
  GROUP BY email
  HAVING count > 1
`.execute(db);

if (duplicates.rows.length > 0) {
  issues.push(`${duplicates.rows.length} duplicate emails found`);
}

if (issues.length > 0) {
  console.warn('Data quality issues:', issues);
  // Decide: fix first, or handle during migration?
}
```

**Map Relationships:**

```typescript
// Document foreign key relationships
const relationships = {
  users: {
    hasMany: ['posts', 'comments', 'sessions'],
    belongsTo: []
  },
  posts: {
    hasMany: ['comments'],
    belongsTo: ['users']
  },
  comments: {
    hasMany: [],
    belongsTo: ['users', 'posts']
  }
};

// Migration order matters!
const migrationOrder = ['users', 'posts', 'comments'];
```

**Output:** Complete data inventory with quality assessment

---

### Phase 3: MOVE

*The bear carries its load carefully, step by heavy step...*

Execute the migration safely:

**Batch Processing:**

```typescript
// For large datasets, process in batches
async function migrateInBatches(
  batchSize: number = 1000
): Promise<void> {
  let offset = 0;
  let hasMore = true;
  
  while (hasMore) {
    const batch = await db.selectFrom('old_table')
      .selectAll()
      .limit(batchSize)
      .offset(offset)
      .execute();
    
    if (batch.length === 0) {
      hasMore = false;
      break;
    }
    
    // Transform and insert
    const transformed = batch.map(transformRecord);
    
    await db.insertInto('new_table')
      .values(transformed)
      .execute();
    
    offset += batchSize;
    console.log(`Migrated ${offset} records...`);
    
    // Prevent memory issues
    if (offset % 10000 === 0) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
}
```

**Transaction Safety:**

```typescript
// Wrap in transaction
await db.transaction().execute(async (trx) => {
  try {
    // 1. Create new structure
    await createNewTables(trx);
    
    // 2. Migrate data
    await migrateData(trx);
    
    // 3. Validate counts
    await validateMigration(trx);
    
    // 4. Drop old structure
    await dropOldTables(trx);
    
  } catch (error) {
    console.error('Migration failed, rolling back:', error);
    throw error; // Transaction automatically rolls back
  }
});
```

**Transformation Logic:**

```typescript
function transformRecord(old: OldUser): NewUser {
  return {
    id: old.id,
    email: old.email.toLowerCase().trim(),
    display_name: old.name || old.email.split('@')[0],
    created_at: new Date(old.created_at),
    // Split full name into parts
    first_name: old.full_name?.split(' ')[0] || null,
    last_name: old.full_name?.split(' ').slice(1).join(' ') || null,
    // Convert string status to enum
    status: old.is_active ? 'active' : 'inactive',
    // Calculate new field
    account_age_days: Math.floor(
      (Date.now() - new Date(old.created_at).getTime()) / (1000 * 60 * 60 * 24)
    )
  };
}
```

**Progress Tracking:**

```typescript
// For long migrations, track progress
const progress = {
  started: new Date(),
  totalRows: 0,
  processedRows: 0,
  errors: [],
  batchTimes: []
};

// Update after each batch
progress.processedRows += batch.length;
const percent = (progress.processedRows / progress.totalRows * 100).toFixed(1);
console.log(`Progress: ${percent}% (${progress.processedRows}/${progress.totalRows})`);
```

**Output:** Data migrated with validation

---

### Phase 4: HIBERNATE

*The bear rests, letting the new den settle...*

Verify the migration:

**Row Count Validation:**

```bash
# Verify row counts match
npx wrangler d1 execute db --command="
  SELECT 
    (SELECT count(*) FROM users_old) as old_count,
    (SELECT count(*) FROM users_new) as new_count;
"

# Should return equal numbers
```

**Data Integrity Checks:**

```typescript
// Sample verification queries
const checks = [
  {
    name: 'Email format',
    query: db.selectFrom('users')
      .where(sql`email NOT LIKE '%@%.%'`, '=', true)
      .select(sql`count(*)`.as('count'))
  },
  {
    name: 'Required fields',
    query: db.selectFrom('users')
      .where('created_at', 'is', null)
      .select(sql`count(*)`.as('count'))
  },
  {
    name: 'Foreign key integrity',
    query: sql`
      SELECT count(*) as count 
      FROM comments c
      LEFT JOIN posts p ON c.post_id = p.id
      WHERE p.id IS NULL
    `
  }
];

for (const check of checks) {
  const result = await check.query.execute(db);
  const count = result.rows[0].count;
  if (count > 0) {
    console.error(`❌ ${check.name}: ${count} issues found`);
  } else {
    console.log(`✓ ${check.name}: OK`);
  }
}
```

**Spot Check:**

```typescript
// Verify specific records
const samples = await db.selectFrom('users')
  .selectAll()
  .limit(10)
  .execute();

for (const user of samples) {
  console.log('Sample user:', {
    id: user.id,
    email: user.email,
    display_name: user.display_name,
    // Verify transformation logic
    has_first_name: !!user.first_name,
    has_account_age: user.account_age_days > 0
  });
}
```

**Output:** Migration verified with count checks and spot validation

---

### Phase 5: VERIFY

*The bear wakes, confirming all is well in the new den...*

Final confirmation and cleanup:

**Application Testing:**

```bash
# Run full test suite
npm test

# Test critical paths manually
npm run dev
# - User login
# - Create post
# - View dashboard
# - Search functionality
```

**Performance Check:**

```sql
-- Check query performance on new schema
EXPLAIN QUERY PLAN
SELECT u.*, count(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id;

-- Look for:
-- - Using index (good)
-- - Scanning table (may need index)
```

**Cleanup:**

```bash
# After verification, remove backup
# (Keep for 30 days in production)
rm backup-20260130.db

# Or archive
mv backup-20260130.db /backups/archived/
```

**Migration Report:**

```markdown
## 🐻 BEAR MIGRATION COMPLETE

### Migration: Split user name into first/last

### Stats
- Records migrated: 15,423 users
- Duration: 4m 32s
- Batches: 16 (1000 records each)
- Errors: 0

### Transformations Applied
- Normalized 234 email addresses to lowercase
- Split full_name into first_name/last_name
- Calculated account_age_days for all users
- Removed 12 orphaned preferences records

### Validation
- ✅ Row count matches: 15,423
- ✅ All emails valid format
- ✅ No null required fields
- ✅ Foreign keys intact
- ✅ Application tests passing

### Rollback Available
Backup retained at: backup-20260130.db
Rollback script: migrations/down/20260130_split_name.sql
```

**Output:** Migration complete, verified, documented

---

## Bear Rules

### Patience
Large migrations take time. Don't rush. Process in batches to avoid memory issues.

### Safety
Always backup. Always test rollbacks. Never migrate without a way back.

### Thoroughness
Verify everything. Row counts, data integrity, application functionality.

### Communication
Use migration metaphors:
- "Waking from hibernation..." (preparation)
- "Gathering the harvest..." (data inventory)
- "Carrying the load..." (migration execution)
- "Resting in the new den..." (verification)

---

## Anti-Patterns

**The bear does NOT:**
- Migrate without backups
- Skip validation steps
- Migrate production without testing on staging
- Delete old data before verifying new data
- Rush large migrations (memory issues)

---

## Example Migration

**User:** "We need to split the user's full name into first and last name fields"

**Bear flow:**

1. 🐻 **WAKE** — "Create migration script, backup database, plan transformation logic"

2. 🐻 **GATHER** — "15,423 users. Found 234 emails with mixed case. 12 users with null names."

3. 🐻 **MOVE** — "Batch migration (1000 records/batch). Transform: lowercase emails, split names, calculate account age."

4. 🐻 **HIBERNATE** — "Verify: row counts match, no null required fields, FK integrity intact."

5. 🐻 **VERIFY** — "App tests pass, performance good, backup archived. Migration complete."

---

## Quick Decision Guide

| Scenario | Approach |
|----------|----------|
| Schema change only | Standard migration (no data movement) |
| Small dataset (<10k rows) | Single transaction |
| Large dataset (>100k rows) | Batch processing with progress tracking |
| Zero downtime required | Blue-green deployment, dual-write pattern |
| Complex transformations | ETL pipeline with validation checkpoints |
| Cross-database migration | Export/import with type mapping |

---

*The bear moves slowly, but nothing is left behind.* 🐻
