---
name: "airtable-sync-specialist"
description: "Debug and implement Airtable synchronization logic including duplicate prevention, cache management, change detection, and RLS considerations; use when debugging sync failures, stale cache issues, or implementing new Airtable sync features"
version: "1.0.0"
---

# Airtable Sync Specialist

## When to Use This Skill

Use this skill when:
- Debugging Airtable sync failures or errors
- Investigating duplicate entity creation
- Troubleshooting stale cache issues
- Implementing new Airtable sync features
- Analyzing change detection logic
- Working with `airtable_entity_mapping` table
- Debugging production map inconsistencies
- Implementing client bootstrap logic

**DO NOT use** for:
- General database migrations (use database-migration-manager)
- Non-Airtable related sync issues
- Client-side data fetching

## Architecture Overview

### Core Components

1. **DuplicatePreventionService** (`duplicate-prevention.service.ts`)
   - Prevents duplicate entities using Airtable UniqueID
   - Validates cached entities still exist
   - Auto-cleanup of stale cache entries

2. **ChangeDetectorService** (`change-detector.service.ts`)
   - Detects changes between new Airtable data and cached data
   - Determines if entity needs updating

3. **AirtableSyncService** (`airtable-sync.service.ts`)
   - Main orchestration service
   - Coordinates duplicate prevention, change detection, entity creation

4. **ClientManager** (`client-manager.ts`)
   - Ensures Fever client exists for Airtable sync
   - Bootstrap agent for client setup

5. **RatingSyncService** (`rating-sync.service.ts`)
   - Syncs ratings from Airtable "Ratings" table
   - Handles rating-specific deduplication

### Key Tables

```sql
-- Entity mapping cache (deduplication)
CREATE TABLE airtable_entity_mapping (
  airtable_unique_id text PRIMARY KEY,
  entity_type text NOT NULL, -- 'event' | 'venue' | 'production'
  entity_id uuid NOT NULL,
  airtable_data jsonb,
  first_synced_at timestamptz,
  last_synced_at timestamptz
);

-- Fever client (external organization)
CREATE TABLE clients (
  id uuid PRIMARY KEY,
  name text NOT NULL,
  slug text UNIQUE NOT NULL,
  type text -- 'agency' | 'venue' | 'company'
);

-- Productions owned by clients
CREATE TABLE productions (
  id uuid PRIMARY KEY,
  client_id uuid REFERENCES clients(id),
  name text NOT NULL,
  -- ...
);

-- Events inherit client through productions
CREATE TABLE events (
  id uuid PRIMARY KEY,
  production_id uuid REFERENCES productions(id) NOT NULL,
  -- Note: account_id removed in October 2025 migration
  -- Events inherit client relationship through production
);
```

## Critical Fix: Stale Cache Bug (2025-10-20)

### The Problem

**Symptom**: Airtable sync creates duplicate events even though `airtable_entity_mapping` shows entity already exists.

**Root Cause**: `findExistingEntity()` returned cached entity_id without validating that the entity still exists in the target table. When events/productions/venues were deleted, the cache entry remained, causing sync to skip creation and later fail.

**Impact**: Events failed to sync from Airtable, production map showed "event ID not found" errors.

### The Solution

**File**: `apps/web/app/admin/sync/_lib/server/duplicate-prevention.service.ts:19`

```typescript
async findExistingEntity(
  airtableUniqueId: string,
  entityType: 'event' | 'venue' | 'production',
): Promise<string | null> {
  // Step 1: Check cache
  const { data } = await this.client
    .from('airtable_entity_mapping')
    .select('entity_id')
    .eq('airtable_unique_id', airtableUniqueId)
    .eq('entity_type', entityType)
    .single();

  if (!data?.entity_id) return null;

  const cachedId = data.entity_id;

  // Step 2: CRITICAL - Validate entity still exists in target table
  const tableName = entityType === 'production'
    ? 'productions'
    : entityType === 'venue'
      ? 'venues'
      : 'events';

  const { data: entity } = await this.client
    .from(tableName)
    .select('id')
    .eq('id', cachedId)
    .maybeSingle();

  if (!entity) {
    // Stale cache detected - auto-cleanup
    console.warn(`🧹 Stale cache detected for ${entityType} ${cachedId}`);
    await this.deleteEntityMapping(airtableUniqueId);
    return null; // Force entity recreation
  }

  return cachedId; // Valid cached entity
}
```

**Key Points**:
- ✅ Always validate cached entity exists before returning ID
- ✅ Auto-cleanup stale cache entries
- ✅ Log warnings for debugging
- ✅ Return null to force recreation when stale

## Common Sync Issues & Debugging

### Issue 1: Duplicate Events Created

**Symptoms**:
- Multiple events with same name/date from Airtable
- `airtable_entity_mapping` shows duplicates

**Debugging Steps**:
```sql
-- Check for duplicate mappings
SELECT airtable_unique_id, COUNT(*)
FROM airtable_entity_mapping
WHERE entity_type = 'event'
GROUP BY airtable_unique_id
HAVING COUNT(*) > 1;

-- Find events without cache entries
SELECT e.id, e.name, e.event_date
FROM events e
LEFT JOIN airtable_entity_mapping aem
  ON aem.entity_id = e.id AND aem.entity_type = 'event'
WHERE e.created_at > NOW() - INTERVAL '1 day'
  AND aem.airtable_unique_id IS NULL;
```

**Solution**:
1. Review `DuplicatePreventionService.registerEntity()`
2. Ensure Airtable UniqueID is correctly generated
3. Check for race conditions in parallel sync

### Issue 2: Stale Cache Entries

**Symptoms**:
- Sync skips creating entities but they don't exist
- "Event ID not found" errors in production map
- Cache shows entity_id but table query returns null

**Debugging Steps**:
```bash
# Run diagnostic script
pnpm tsx .claude/skills/airtable-sync-specialist/scripts/diagnose-sync-cache.ts

# Check for stale cache entries manually
pnpm sql:local "
  SELECT aem.*,
         CASE
           WHEN e.id IS NULL THEN 'STALE'
           ELSE 'VALID'
         END as status
  FROM airtable_entity_mapping aem
  LEFT JOIN events e ON e.id = aem.entity_id
  WHERE aem.entity_type = 'event'
    AND e.id IS NULL;
"
```

**Solution**:
1. Upgrade `DuplicatePreventionService` to validate entities (already implemented)
2. Run cleanup script to remove stale entries
3. Re-sync from Airtable

### Issue 3: RLS Policy Blocks Sync

**Symptoms**:
- Sync fails with "permission denied" or "new row violates row-level security"
- Works locally but fails in production

**Debugging Steps**:
```bash
# Check RLS policies
pnpm sql:local --inspect events
pnpm sql:local --inspect airtable_entity_mapping

# Test as super admin
pnpm tsx .claude/skills/rls-policy-generator/scripts/diagnose-fever-client-rls.ts
```

**Common RLS Issues**:
- `airtable_entity_mapping` needs super admin INSERT policy
- Events need super admin bypass for Airtable sync
- Client-based ownership not properly configured

**Solution**:
```sql
-- Add super admin bypass to airtable_entity_mapping
CREATE POLICY airtable_mapping_insert ON airtable_entity_mapping
FOR INSERT TO authenticated
WITH CHECK (
  public.is_super_admin() OR
  auth.uid() = created_by -- if you track creator
);

-- Events should allow super admin to create via sync
CREATE POLICY events_insert ON events
FOR INSERT TO authenticated
WITH CHECK (
  public.is_super_admin() OR
  -- other conditions
);
```

### Issue 4: Client Not Found

**Symptoms**:
- Sync fails with "client 'fever' not found"
- Production creation fails

**Debugging Steps**:
```sql
-- Check if Fever client exists
SELECT * FROM clients WHERE slug = 'fever';

-- Check default client config
SELECT * FROM clients WHERE slug = 'default-airtable-client';
```

**Solution**:
```typescript
// Ensure client via ClientManager
import { ensureClient } from '~/app/admin/sync/_lib/server/client-manager';

const client = await ensureClient(supabaseClient);
// Creates Fever client if not exists
```

**File**: `apps/web/app/admin/sync/_lib/server/client-manager.ts:29`

### Issue 5: Change Detection Not Working

**Symptoms**:
- Sync doesn't update entities when Airtable data changes
- Entities stuck with old data

**Debugging Steps**:
```typescript
// Check change detection logic
import { ChangeDetectorService } from '~/app/admin/sync/_lib/server/change-detector.service';

const detector = new ChangeDetectorService();
const hasChanges = detector.hasChanges(
  newAirtableData,
  cachedAirtableData,
  entityType
);

console.log('Changes detected:', hasChanges);
console.log('New data:', newAirtableData);
console.log('Cached data:', cachedAirtableData);
```

**Solution**:
1. Review which fields are compared
2. Ensure field names match between Airtable and cache
3. Check data type transformations

## Airtable Sync Workflow

### Standard Sync Flow

```
1. Fetch from Airtable
   ↓
2. Ensure Fever client exists (ClientManager)
   ↓
3. For each Airtable record:
   ↓
   a. Generate UniqueID
   ↓
   b. Check cache (DuplicatePreventionService.findExistingEntity)
      ↓
      EXISTS? → c. Check for changes (ChangeDetectorService)
                ↓
                CHANGES? → d. Update entity
                         → e. Update cache
                NO? → Skip (already synced)
      ↓
      NOT EXISTS? → f. Create entity
                   → g. Register in cache
```

### Production Sync Example

```typescript
import { AirtableSyncService } from '~/app/admin/sync/_lib/server/airtable-sync.service';
import { ensureClient } from '~/app/admin/sync/_lib/server/client-manager';

// 1. Ensure Fever client exists
const client = await ensureClient(supabaseClient);

// 2. Initialize sync service
const syncService = new AirtableSyncService(
  supabaseClient,
  client.id // Fever client ID
);

// 3. Sync productions from Airtable
const result = await syncService.syncProductions(airtableRecords);

if (result.success) {
  console.log('Synced:', result.created, 'created,', result.updated, 'updated');
} else {
  console.error('Sync failed:', result.error);
}
```

## Diagnostic Scripts

### diagnose-sync-cache.ts
**Purpose**: Detect stale cache entries
**Usage**: `pnpm tsx .claude/skills/airtable-sync-specialist/scripts/diagnose-sync-cache.ts`
**What it checks**:
- Cache entries pointing to deleted entities
- Orphaned cache entries
- Duplicate mappings

### test-airtable-sync-local.ts
**Purpose**: Test sync logic with local Airtable data
**Usage**: `pnpm tsx .claude/skills/airtable-sync-specialist/scripts/test-airtable-sync-local.ts`
**What it does**:
- Tests sync against local database
- Validates duplicate prevention
- Checks RLS policies

### diagnose-fever-client-rls.ts
**Purpose**: Debug Fever client RLS access
**Usage**: `pnpm tsx .claude/skills/rls-policy-generator/scripts/diagnose-fever-client-rls.ts`
**What it checks**:
- Client exists and accessible
- Productions linked to client
- Events linked to productions

## Best Practices

### Duplicate Prevention

1. ✅ **Always use Airtable UniqueID** - Don't rely on event names or dates
2. ✅ **Validate cached entities** - Check entity exists before trusting cache
3. ✅ **Auto-cleanup stale entries** - Remove cache when entity deleted
4. ✅ **Log all cache operations** - Makes debugging easier

### RLS Considerations

1. ✅ **Use super admin client for sync** - Bypass account-based RLS
2. ✅ **Test RLS policies explicitly** - Write tests for sync scenarios
3. ✅ **Document RLS exceptions** - Why super admin bypass is needed
4. ✅ **Validate permissions in code** - Don't rely solely on RLS

### Change Detection

1. ✅ **Compare meaningful fields only** - Ignore Airtable metadata changes
2. ✅ **Normalize data before comparison** - Handle date formats, timezones
3. ✅ **Log detected changes** - Show what triggered update
4. ✅ **Batch updates** - Don't update one field at a time

### Error Handling

1. ✅ **Log with context** - Include Airtable UniqueID, entity type, IDs
2. ✅ **Fail gracefully** - Continue sync even if one entity fails
3. ✅ **Track sync results** - Return counts of created/updated/failed
4. ✅ **Alert on persistent failures** - Integrate with Sentry

## Common Code Patterns

### Safe Entity Lookup

```typescript
// ✅ CORRECT - Validates entity exists
const existingId = await duplicatePrevention.findExistingEntity(
  airtableUniqueId,
  'event'
);

if (existingId) {
  // Entity exists and is valid
  const hasChanges = changeDetector.hasChanges(newData, cachedData, 'event');

  if (hasChanges) {
    // Update entity
  }
} else {
  // Create new entity
}

// ❌ WRONG - Trusts cache without validation
const { data } = await supabase
  .from('airtable_entity_mapping')
  .select('entity_id')
  .eq('airtable_unique_id', airtableUniqueId)
  .single();

if (data) {
  // Assumes entity exists - may be stale!
}
```

### Idempotent Sync

```typescript
// ✅ CORRECT - Can run multiple times safely
async function syncProduction(airtableRecord: AirtableProduction) {
  const uniqueId = generateUniqueId(airtableRecord);

  // Check if exists (validates entity still exists)
  const existingId = await duplicatePrevention.findExistingEntity(
    uniqueId,
    'production'
  );

  if (existingId) {
    // Update if changed
    if (changeDetector.hasChanges(newData, cachedData, 'production')) {
      await updateProduction(existingId, newData);
      await duplicatePrevention.updateCache(uniqueId, newData);
    }
  } else {
    // Create new
    const newId = await createProduction(newData);
    await duplicatePrevention.registerEntity(uniqueId, 'production', newId);
  }
}
```

### Batch Processing with Error Handling

```typescript
// ✅ CORRECT - Handles failures gracefully
async function syncBatch(records: AirtableRecord[]) {
  const results = {
    created: 0,
    updated: 0,
    failed: 0,
    errors: [] as Array<{ record: string; error: string }>
  };

  for (const record of records) {
    try {
      const result = await syncSingleRecord(record);
      if (result.created) results.created++;
      if (result.updated) results.updated++;
    } catch (error) {
      results.failed++;
      results.errors.push({
        record: record.id,
        error: error.message
      });

      // Log but continue processing
      console.error(`Failed to sync record ${record.id}:`, error);
    }
  }

  return results;
}
```

## Testing Sync Logic

### Unit Tests

```typescript
describe('DuplicatePreventionService', () => {
  test('validates cached entity exists', async () => {
    const service = new DuplicatePreventionService(adminClient);

    // Create cache entry for non-existent entity
    await adminClient.from('airtable_entity_mapping').insert({
      airtable_unique_id: 'test-unique-id',
      entity_type: 'event',
      entity_id: 'non-existent-uuid'
    });

    // Should return null and cleanup cache
    const result = await service.findExistingEntity('test-unique-id', 'event');

    expect(result).toBeNull();

    // Verify cache was cleaned up
    const { data } = await adminClient
      .from('airtable_entity_mapping')
      .select()
      .eq('airtable_unique_id', 'test-unique-id')
      .maybeSingle();

    expect(data).toBeNull();
  });
});
```

### Integration Tests

```typescript
describe('Airtable Sync Integration', () => {
  test('syncs production from Airtable', async () => {
    const syncService = new AirtableSyncService(adminClient, feverClientId);

    const airtableData = {
      id: 'airtable-prod-123',
      fields: {
        Name: 'Swan Lake',
        Type: 'Ballet',
        // ...
      }
    };

    const result = await syncService.syncProductions([airtableData]);

    expect(result.success).toBe(true);
    expect(result.created).toBe(1);

    // Verify production created
    const { data: production } = await adminClient
      .from('productions')
      .select()
      .eq('name', 'Swan Lake')
      .single();

    expect(production).toBeDefined();

    // Verify cache entry
    const { data: mapping } = await adminClient
      .from('airtable_entity_mapping')
      .select()
      .eq('airtable_unique_id', generateUniqueId(airtableData))
      .single();

    expect(mapping.entity_id).toBe(production.id);
  });
});
```

## Airtable Access Configuration (Multi-Table Support)

### Environment Variables Setup

The Ballee system supports accessing **multiple Airtable tables** from the same base using a single API key. All configuration is managed through environment variables.

#### Base Configuration (Required for All Tables)

```bash
# Airtable API Authentication
AIRTABLE_API_KEY=key_xxxxx              # Personal access token from Airtable

# Base ID (workspace + base identifier)
AIRTABLE_BASE_ID=appxxxxx              # Application/Base ID from URL
```

**How to get these**:

1. **AIRTABLE_API_KEY**:
   - Go to https://airtable.com/account/tokens
   - Create new token with `data.records:read` scope
   - Copy the token value

2. **AIRTABLE_BASE_ID**:
   - Open Airtable base in browser
   - URL format: `https://airtable.com/appXXXXXX/...`
   - Extract the `appXXXXXX` portion

#### Table Configuration (Per Table)

**Primary Table (Ballee Dates - "Fever" client events)**:

```bash
# Optional: Explicitly configure primary table
AIRTABLE_TABLE_NAME=Ballee Dates       # Table name in Airtable (default)

# Client configuration for Fever sync
AIRTABLE_CLIENT_SLUG=fever              # Client slug in database
AIRTABLE_CLIENT_NAME=Fever              # Display name
AIRTABLE_CLIENT_EMAIL=contact@fever.co  # Contact email
AIRTABLE_CLIENT_TYPE=agency             # Client type (agency, venue, company)
AIRTABLE_CLIENT_CONTACT_NAME=Fever Team # Contact person name
```

**Secondary Tables (Ratings, Reports, etc.)**:

If you need to access different tables in the same base, modify the sync service to accept table names as parameters:

```typescript
// Current: Hard-coded to use AIRTABLE_TABLE_NAME or default "Ballee Dates"
const tableName = process.env.AIRTABLE_TABLE_NAME || 'Ballee Dates';
const records = await base(tableName).select().all();

// Future: Make table name configurable per sync operation
async function fetchTableData(tableName: string) {
  const airtable = new Airtable({ apiKey: process.env.AIRTABLE_API_KEY });
  const base = airtable.base(process.env.AIRTABLE_BASE_ID);
  return base(tableName).select().all();
}
```

### Multi-Table Sync Architecture

#### Current Setup (Single Client - Fever)

```
Airtable Base (appXXXXXX)
│
├─ Table: "Ballee Dates" (Primary)
│  ├─ Fields: Date, City_linked, Venue, Sub-Programm, Starttime: 1. Show, Starttime: 2. Show, Status
│  ├─ Client: Fever (AIRTABLE_CLIENT_SLUG=fever)
│  └─ Mapped to: events, productions, venues
│
└─ Table: "Ratings" (Secondary)
   ├─ Fields: Name, Date, Show Time, Rating, Comment
   ├─ Client: Fever (same)
   └─ Mapped to: event_ratings
```

#### Adding New Tables

**Use Case**: Sync from additional Airtable tables for same or different clients:

1. **Same Base, Different Tables**:
   ```typescript
   // Extend AirtableSyncService to accept table name
   class AirtableSyncService {
     async syncFromTable(
       tableName: string,
       options: SyncOptions
     ): Promise<SyncResult> {
       // Fetch from specified table
       const records = await this.fetchTableData(tableName);

       // Parse and sync based on table schema
       return this.processRecords(records, options);
     }
   }
   ```

2. **Different Bases**:
   ```typescript
   // Add environment variable for second base
   AIRTABLE_BASE_ID_SECONDARY=appYYYYYY

   // Create separate sync instance
   const secondarySync = new AirtableSyncService(
     supabaseClient,
     clientId,
     process.env.AIRTABLE_BASE_ID_SECONDARY  // Different base
   );
   ```

3. **Different Clients**:
   ```typescript
   // Each client can have separate Airtable configuration
   AIRTABLE_CLIENT_SLUG=fever              # Client 1
   AIRTABLE_CLIENT_SLUG_2=another-org      # Client 2
   AIRTABLE_BASE_ID_2=appZZZZZZ            # Different base
   ```

### Discovering All Tables in Your Airtable Base

The `discover-all-tables.ts` script uses the **Airtable Metadata API** to list all tables in your base, including their fields and types. This is essential for:

- Identifying all available tables for syncing
- Finding table IDs and field names
- Planning multi-table sync strategies
- Validating your Airtable schema

#### How to Use Discovery Script

**Run the discovery**:

```bash
# From project root
cd apps/web
npx tsx scripts/discover-all-tables.ts
```

**Output Example**:

```
🔍 Discovering all tables in Airtable base...

Base ID: appXXXXXXXXXXXXXX

✅ Found 5 table(s) in the base:

1. Ballee Dates
   ID: tblXXXXXXXXXXXXXX
   Description: Performance schedule for all shows
   Fields: 8
   Field names:
     - Date (date)
     - City_linked (singleCollaborator)
     - Venue (singleLineText)
     - Sub-Programm (singleLineText)
     - Starttime: 1. Show (duration)
     - Starttime: 2. Show (duration)
     - Status (singleSelect)
     - UniqueID (singleLineText)

2. Ratings
   ID: tblYYYYYYYYYYYYYY
   Description: Performance ratings and reviews
   Fields: 5
   Field names:
     - Name (singleLineText)
     - Date (date)
     - Show Time (duration)
     - Rating (number)
     - Comment (multilineText)

3. Cities
   ID: tblZZZZZZZZZZZZZZ
   Description: City reference data
   Fields: 3
   Field names:
     - Name (singleLineText)
     - Code (singleLineText)
     - Country (singleLineText)

4. Venues
   ID: tblVVVVVVVVVVVVVV
   Description: Venue reference data
   Fields: 4
   Field names:
     - Name (singleLineText)
     - City (singleLineText)
     - Address (singleLineText)
     - Capacity (number)

5. Productions
   ID: tblPPPPPPPPPPPPPP
   Description: Production/program reference data
   Fields: 3
   Field names:
     - Name (singleLineText)
     - Type (singleSelect)
     - Description (multilineText)

⭐ Found 1 ratings-related table(s):
   - Ratings (tblYYYYYYYYYYYYYY)
```

#### Discovery Output Breakdown

**For Each Table, You Get**:

1. **Name**: Display name in Airtable (e.g., "Ballee Dates")
2. **ID**: Table identifier (e.g., tblXXXXXXXXXXXXXX) - Used in API calls
3. **Description**: Optional description from Airtable
4. **Field Count**: Total number of fields
5. **Field Names & Types**: First 10 fields shown with types:
   - `singleLineText` - Single line text
   - `multilineText` - Long text
   - `date` - Date field
   - `duration` - Time duration
   - `number` - Numeric field
   - `singleSelect` - Dropdown with single selection
   - `singleCollaborator` - Linked person/user
   - And many more...

#### Using Discovery Results for Syncing

Once you discover tables, you can configure sync for any of them:

```typescript
// Example: Sync from Venues table instead of Ballee Dates
const venuesTableId = 'tblVVVVVVVVVVVVVV';
const venuesTableName = 'Venues';

const records = await base(venuesTableName).select().all();

// Process venue records
for (const record of records) {
  const venueName = record.fields['Name'];
  const city = record.fields['City'];
  const capacity = record.fields['Capacity'];

  // Sync to Ballee venues table
  await syncVenue({
    name: venueName,
    city,
    capacity
  });
}
```

#### Common Table Types You'll Find

**Primary Data Tables** (usually sync to Ballee):
- `Ballee Dates` - Performance schedule (primary - maps to events/productions/venues)
- `Ratings` - Reviews and ratings (maps to event_ratings)
- `Invoices` - Financial records (maps to invoices)

**Reference Tables** (lookup/linked data):
- `Cities` - Location reference
- `Venues` - Venue reference
- `Productions` - Program reference
- `Artists` - Performer reference
- `Categories` - Type classification

**Administrative Tables** (internal tracking):
- `Sync Logs` - Airtable-side sync history
- `Error Log` - Failed record tracking
- `Configuration` - Airtable settings

#### Complete Table Reference Map - ACTUAL TABLES (Updated 2025-11-24)

**Permissions Status**: 🔒 READ-ONLY (data.records:read, schema.bases:read)
- ✅ Can READ records from all tables
- ✅ Can READ table schema and metadata
- ❌ Cannot WRITE records (permission denied)
- ❌ Cannot DELETE records (permission denied)

| Table Name | Table ID | Purpose | Fields | Sync Status | Permissions |
|---|---|---|---|---|---|
| **Ballee Dates** | tblIsDWRcG6w9Dre9 | Performance schedule | Date, City_linked, Venue, Sub-Programm, Starttime: 1. Show, Starttime: 2. Show, Status, Aurora/Cinderella (+ 8 more) | ✅ ACTIVE | 🔒 READ-ONLY |
| **Dancer_Data** | tbl8cQHnbsT74Wj0T | Artist/dancer information | Artist's name, Where based, Status, Start Date, End Date, Email, Phone, Address, ID/Passport, Ballee link (+ 22 more) | ⏸️ NOT SYNCED | 🔒 READ-ONLY |
| **Ratings** | tblTQDEu8igwQpV1t | Performance reviews | Name, Date, Show Time, Rating, Comment | ✅ ACTIVE | 🔒 READ-ONLY |

**Note**: Only 3 tables exist in this Airtable base (Fever workspace). The "Cities," "Venues," "Productions," and other example tables mentioned in earlier documentation are NOT present - those were documented as common table types for reference only.

#### How to Find Tables You Need

**Step 1: Run Discovery Script**
```bash
cd apps/web && npx tsx scripts/discover-all-tables.ts
```

**Step 2: Identify Your Target Table**
- Look for table name and description
- Note the table ID (starts with `tbl`)
- Review the fields available

**Step 3: Map Fields to Ballee**
```typescript
// Example: Mapping Invoices table to Ballee invoices
const airtableInvoices = await fetchAirtableTable('Invoices');

const mappedInvoices = airtableInvoices.map(record => ({
  // Airtable field → Ballee field
  externalId: record.fields['Invoice#'],
  date: new Date(record.fields['Date']),
  amount: record.fields['Amount'],
  clientName: record.fields['Client'],
  status: record.fields['Status']
}));
```

**Step 4: Implement Sync**
```typescript
// Generic table sync function
async function syncGenericTable(
  tableName: string,
  mapFunction: (record: any) => object
) {
  const records = await base(tableName).select().all();

  for (const record of records) {
    const mapped = mapFunction(record);
    // Upsert to Ballee database
    await syncToBallee(tableName, mapped);
  }
}
```

#### Field Types Reference

When discovering tables, you'll see these Airtable field types. Here's how to handle each:

| Field Type | Description | Example Value | Sync Handling |
|---|---|---|---|
| `singleLineText` | Single line text | "Swan Lake" | Use directly as string |
| `multilineText` | Long text (paragraph) | "The swan lake tells..." | Use directly as string |
| `email` | Email address | "dancer@example.com" | Validate format, use directly |
| `url` | URL/link | "https://example.com" | Validate URL, use directly |
| `number` | Numeric value | `42`, `3.14` | Parse as number |
| `percent` | Percentage | `75` | Store as decimal (0.75) |
| `date` | Date only | "2025-03-15" | Convert to ISO 8601 |
| `duration` | Time duration | "19:30" | Parse as HH:MM or seconds |
| `singleSelect` | Dropdown (single) | "Live" | Use as enum/string |
| `multipleSelect` | Dropdown (multi) | ["Option1", "Option2"] | Use as array |
| `checkbox` | Boolean toggle | `true`/`false` | Convert to boolean |
| `singleCollaborator` | Person/user | {name: "John", email: "..."} | Extract email or name |
| `multipleCollaborators` | Multiple people | [{...}, {...}] | Extract array of people |
| `singleLineText` | Record link | {id: "rec...", name: "..."} | Store foreign key ID |
| `multipleRecordLinks` | Multiple links | [{id: "..."}, {...}] | Store array of IDs |
| `lookup` | Formula result | (depends on formula) | Handle based on result type |
| `formula` | Calculated field | (depends on formula) | Handle based on result type |
| `createdTime` | Auto timestamp | "2025-01-15T10:30:00Z" | Convert to ISO timestamp |
| `lastModifiedTime` | Last update time | "2025-01-15T10:30:00Z" | Convert to ISO timestamp |
| `createdBy` | Creator info | {id: "...", email: "..."} | Extract email for audit |
| `lastModifiedBy` | Last updater | {id: "...", email: "..."} | Extract email for audit |
| `autoNumber` | Auto-incrementing | `1`, `2`, `3` | Use directly as external ID |
| `barcode` | Barcode scanner | "ABC123456" | Store as string |
| `rating` | Star rating | `4` (out of 5) | Convert to 1-5 scale |
| `count` | Count formula | `42` | Use directly as number |
| `button` | Interactive button | (action) | Skip in sync |

**Example Handling Each Type**:

```typescript
// Type-safe field extraction
interface AirtableRow {
  fields: Record<string, unknown>;
}

function extractAirtableFields(record: AirtableRow) {
  return {
    // Text fields
    name: String(record.fields['Name']),
    description: String(record.fields['Description'] || ''),

    // Numeric fields
    capacity: Number(record.fields['Capacity']),
    rating: Number(record.fields['Rating']),

    // Date fields
    performanceDate: new Date(String(record.fields['Date'])),

    // Time/Duration
    startTime: String(record.fields['Starttime']), // e.g., "19:30"

    // Selections
    status: String(record.fields['Status']), // Single select enum
    tags: Array.isArray(record.fields['Tags'])
      ? record.fields['Tags']
      : [], // Multiple select array

    // Boolean
    isActive: record.fields['Active'] === true,

    // Linked records
    cityId: record.fields['City_linked']?.[0] || null, // First linked record

    // Collaborators
    createdBy: record.fields['Created by']?.email || null,

    // Metadata (auto fields)
    createdAt: new Date(String(record.fields['Created time'])),
    updatedAt: new Date(String(record.fields['Last modified time']))
  };
}
```

#### Troubleshooting Discovery

**Error: "403 Forbidden"**

The API key lacks Metadata API access. Solution:

```bash
# Create new Personal Access Token with correct scopes:
1. Go to https://airtable.com/account/tokens
2. Create new token
3. Add scope: "schema.bases:read"
4. Also add: "data.records:read"
5. Copy and use new token
```

**Error: "401 Unauthorized"**

API key is invalid or expired. Solution:

```bash
# Check your token
echo $AIRTABLE_API_KEY  # Should start with "pat_" or "key_"

# If empty, set it
export AIRTABLE_API_KEY="your_token_here"
```

**No tables returned**

Base ID might be wrong. Solution:

```bash
# Verify base ID from Airtable URL
# https://airtable.com/appXXXXXXXXXXXXXX/...
# Extract: appXXXXXXXXXXXXXX

echo $AIRTABLE_BASE_ID  # Should match the app... from URL
```

### Accessing Fever Table

#### Field Mapping

The "Ballee Dates" table (Fever client) has the following field structure:

| Field Name | Type | Usage | Example |
|---|---|---|---|
| `Date` | Date | Event date | `2025-03-15` |
| `City_linked` | Linked Records | City identifier | Links to cities table |
| `Venue` | Text | Venue name | `Theatre Royal` |
| `Sub-Programm` | Text | Production name | `Swan Lake` |
| `Starttime: 1. Show` | Time | First show time | `19:30` |
| `Starttime: 2. Show` | Time (optional) | Second show time | `20:00` |
| `Status` | Single Select | Event status | `Live`, `Canceled` |

**UniqueID Generation** (from `constants.ts:86-92`):

```typescript
// Unique ID created from composite data
const uniqueId = `${date}_${venue}_${city}_${program}_${startTime1}`;

// Used for deduplication in airtable_entity_mapping
```

#### Reading Fever Table Data

```typescript
import { fetchAirtableData } from '~/app/admin/sync/_lib/server/airtable-api.service';

// Fetch all Fever dates from Ballee Dates table
const { shows, venues, productions } = await fetchAirtableData();

// Shows format: ParsedShow[]
shows.forEach(show => {
  console.log(`${show.date} @ ${show.venue} (${show.city})`);
  console.log(`  Program: ${show.program}`);
  console.log(`  Show 1: ${show.startTime1}`);
  if (show.startTime2) console.log(`  Show 2: ${show.startTime2}`);
  if (show.canceled) console.log(`  Status: CANCELED`);
});

// Venues format: Map<string, VenueWithCity>
// Key: "venueName_city"
venues.forEach((venue, key) => {
  console.log(`${venue.name} (${venue.city})`);
});

// Productions format: Set<string>
productions.forEach(prod => {
  console.log(`Production: ${prod}`);
});
```

#### Syncing Fever Table to Ballee

**Full Sync Workflow**:

```typescript
import { AirtableSyncService } from '~/app/admin/sync/_lib/server/airtable-sync.service';
import { ensureClient } from '~/app/admin/sync/_lib/server/client-manager';

// 1. Ensure Fever client exists in database
const feverClient = await ensureClient(supabaseClient, {
  slug: 'fever',
  name: 'Fever',
  email: 'contact@fever.co',
  type: 'agency',
  contactName: 'Fever Team'
});

// 2. Initialize sync service for Fever
const syncService = new AirtableSyncService(
  supabaseClient,
  feverClient.id
);

// 3. Execute full sync with change tracking
const result = await syncService.syncWithChangeTracking({
  clientId: feverClient.id,
  triggeredBy: currentUserId,        // Admin user ID
  triggerType: 'manual',             // 'manual' | 'cron' | 'webhook'
  dryRun: false,                     // Preview without applying
  notifyOnChanges: true              // Send Slack notifications
});

// 4. Check results
console.log(`
  ✅ Venues synced: ${result.venues.created} created, ${result.venues.updated} updated
  ✅ Productions synced: ${result.productions.created} created, ${result.productions.updated} updated
  ✅ Events synced: ${result.events.created} created, ${result.events.updated} updated
  ✅ Ratings synced: ${result.ratings.created} created, ${result.ratings.updated} updated
`);

if (result.errors.length > 0) {
  console.error('⚠️  Errors during sync:', result.errors);
  // Handle errors...
}
```

#### Testing Fever Table Access

**Verify Token Works** (before production sync):

```bash
# List all tables in base to verify access
pnpm tsx .claude/skills/production-database-query/scripts/discover-all-tables.ts

# Output:
# Tables in base appXXXXXX:
# - Ballee Dates (primary sync table)
# - Ratings (secondary table)
# - Cities (reference data)
```

**Check Field Names** (ensure schema matches):

```bash
# Inspect Ballee Dates table structure
pnpm tsx .claude/skills/airtable-sync-specialist/scripts/test-ratings-table-id.ts

# Validates:
# - Table exists and is accessible
# - All required fields present
# - Field names match constants.ts definitions
```

**Test Sync Without Applying Changes**:

```typescript
// Use dryRun mode to preview changes
const result = await syncService.syncWithChangeTracking({
  clientId: feverClient.id,
  dryRun: true,  // Preview only, no database changes
  notifyOnChanges: false
});

// Review what would be synced
console.log('Would create events:', result.events.created);
console.log('Would update events:', result.events.updated);
console.log('Changes:', result.changeLog);
```

### Troubleshooting Fever Table Access

| Issue | Cause | Solution |
|-------|-------|----------|
| "Missing Airtable configuration" | `AIRTABLE_API_KEY` or `AIRTABLE_BASE_ID` not set | Set environment variables |
| "Table not found" | `AIRTABLE_TABLE_NAME` wrong or doesn't exist | Verify exact table name in Airtable |
| "Field not found" | Field names don't match Airtable schema | Check `AIRTABLE_FIELDS` in constants.ts |
| "Permission denied" | API token lacks `data.records:read` | Create new token with correct scopes |
| "Invalid credentials" | Wrong API key for base | Verify key matches base ID |
| "Rate limited" | Too many requests to Airtable | Check `AIRTABLE_CONFIG.RATE_LIMIT_PER_SECOND` |

### API Token Permissions & Scopes

**Current Token Status**: 🔒 READ-ONLY (Limited Scope)

Actual Permissions (Tested):
```
✅ data.records:read     - Can read records from all tables
✅ schema.bases:read     - Can read table schema and metadata
❌ data.records:write    - Cannot create/update records
❌ data.records:delete   - Cannot delete records
```

**Why READ-ONLY?**
- Token scopes intentionally limited to data.records:read + schema.bases:read
- Prevents accidental data modifications in Fever Airtable base
- Maintains data integrity (one-way sync FROM Airtable TO Ballee)
- Safer for production environments

**What This Means for Syncing**:
- ✅ Can sync data FROM Airtable to Ballee database
- ✅ Can validate data against Airtable schema
- ❌ Cannot push changes back to Airtable
- ❌ Cannot delete Airtable records

If write access becomes necessary, contact Fever to:
1. Create new Personal Access Token with `data.records:write` scope
2. Update `AIRTABLE_API_KEY` environment variable
3. Test permissions with provided verification script

### Environment Variable Reference

```bash
# REQUIRED - API Authentication
AIRTABLE_API_KEY=patXXXXXXXXXXXXXX              # Personal access token

# REQUIRED - Base identification
AIRTABLE_BASE_ID=appwh9Xy2DZzbjg4J             # Fever base ID

# OPTIONAL - Table name (default: "Ballee Dates")
AIRTABLE_TABLE_NAME=Ballee Dates                # Primary sync table

# OPTIONAL - Fever client configuration
AIRTABLE_CLIENT_SLUG=fever                      # DB client slug
AIRTABLE_CLIENT_NAME=Fever                      # Display name
AIRTABLE_CLIENT_EMAIL=contact@fever.co          # Contact email
AIRTABLE_CLIENT_TYPE=agency                     # Client type
AIRTABLE_CLIENT_CONTACT_NAME=Fever Team         # Contact person

# OPTIONAL - Ratings table
RATING_TABLE_NAME=Ratings                       # Ratings sync table
```

## Reference Files

### Airtable Entity Sync
- Duplicate prevention: `apps/web/app/admin/sync/_lib/server/duplicate-prevention.service.ts`
- Change detection: `apps/web/app/admin/sync/_lib/server/change-detector.service.ts`
- Main sync: `apps/web/app/admin/sync/_lib/server/airtable-sync.service.ts`
- Client management: `apps/web/app/admin/sync/_lib/server/client-manager.ts`
- API service: `apps/web/app/admin/sync/_lib/server/airtable-api.service.ts`
- Constants & field mapping: `apps/web/app/admin/sync/_lib/server/constants.ts`
- Ratings sync: `apps/web/app/admin/sync/_lib/server/rating-sync.service.ts`
- Diagnostic scripts: `.claude/skills/airtable-sync-specialist/scripts/` folder
- WIP doc: `docs/wip/WIP_airtable_sync_stale_cache_diagnosis_2025_10_20.md`
- Infrastructure doc: `docs/infrastructure/integrations/airtable-sync.md`

### Dancer Deduplication System
- Service: `apps/web/app/admin/sync/_lib/server/dancer-deduplication.service.ts`
- Integration: `apps/web/app/admin/sync/_lib/server/dancer-data-sync.service.ts`
- Admin page: `apps/web/app/admin/sync/_components/dancer-links-page.tsx`
- Data table: `apps/web/app/admin/sync/_components/dancer-links-table.tsx`
- Review dialog: `apps/web/app/admin/sync/_components/dancer-link-review-dialog.tsx`
- Server actions: `apps/web/app/admin/sync/_lib/server/dancer-links.actions.ts`
- Query mutations: `apps/web/app/admin/sync/_lib/hooks/use-dancer-link-mutations.ts`
- Strategy doc: `docs/features/airtable-integration/dancer-deduplication-strategy.md`
- WIP doc: `docs/wip/active/WIP_implementing_dancer_deduplication_2025_11_24.md`
