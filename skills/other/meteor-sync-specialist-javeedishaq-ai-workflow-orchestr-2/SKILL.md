---
name: "meteor-sync-specialist"
description: "Sync data from Meteor MongoDB to Supabase; use when running syncs, debugging sync failures, investigating entity mapping issues, or implementing new mappers"
version: "1.1.0"
last_updated: "2025-12-10"
---

# Meteor Sync Specialist

## When to Use This Skill

Use this skill when:
- Running Meteor to Supabase data sync (full, incremental, or entity-specific)
- **Migrating MongoDB users to Supabase auth.users**
- Syncing media (dancer, organization, profile, post media)
- Debugging sync failures or entity creation errors
- Investigating duplicate entities or stale cache issues
- Implementing new entity mappers
- Analyzing change detection logic
- Working with `meteor_entity_mapping` table
- Resuming failed sync runs
- Comparing MongoDB vs Supabase record counts

**DO NOT use** for:
- Querying MongoDB directly (use `mongodb-production-query` skill)
- Airtable sync issues (use `airtable-sync-specialist` skill)
- General database migrations (use `database-migration-manager` skill)

## Connection Configuration

### Environment Variables (Required)

```bash
# MongoDB connection (Meteor production database)
export METEOR_MONGO_URL="mongodb://root:<password>@mdb-p-0.ballee.db-eu2.zcloud.ws:60601,mdb-p-1.ballee.db-eu2.zcloud.ws:60602,mdb-p-2.ballee.db-eu2.zcloud.ws:60603/meteor?authSource=admin&ssl=true&tlsInsecure=true&replicaSet=mdb-p"

# Supabase staging database
export SUPABASE_DB_PASSWORD_STAGING="<password>"
export SUPABASE_DB_HOST="db.hxpcknyqswetsqmqmeep.supabase.co"  # Optional, has default

# Supabase production database (use with caution)
export SUPABASE_DB_PASSWORD_PROD="<password>"
```

### S3 Configuration (Media URLs)

```typescript
const S3_REGION = 'eu-central-1';
const S3_BUCKET = 'ch.akson.dance.bucket';

// URL format for media files
const mediaUrl = `https://s3.${S3_REGION}.amazonaws.com/${S3_BUCKET}/${s3Key}`;
```

### R2 Configuration (Newer media)

```typescript
// R2 URLs follow this pattern
const r2Url = 'https://pub-2541aa5053334bd4bcd4a619e7ad3428.r2.dev/...';
```

## Migration Statistics (2025-12-09)

### Final Entity Counts

| Entity Type | Count | Notes |
|-------------|-------|-------|
| auth.users | 14,864 | Migrated from MongoDB users |
| profiles | 14,864 | Auto-created by trigger |
| profiles with meteor_id | 14,819 | Linked to MongoDB |
| professional_profiles with user_id | 14,603 | Linked to auth users |
| dancer_media | 47,156 | photos: 37,822, headers: 7,251, videos: 2,079 |
| organization_media | 3,809 | Logos and headers |
| profile_media | 2,283 | User-uploaded media (orphan media) |
| post_media | 1,631 | Media attached to posts |
| profile_posts | 1,491 | Community posts |
| community_events | 293 | Community events |

### Media URL Verification

All media URLs have been verified functional (HTTP 200):
- **S3 URLs**: `https://s3.eu-central-1.amazonaws.com/ch.akson.dance.bucket/...`
- **R2 URLs**: `https://pub-2541aa5053334bd4bcd4a619e7ad3428.r2.dev/...`
- **YouTube embeds**: `https://www.youtube.com/embed/...`

## Architecture Overview

### Core Components

1. **MeteorSyncService** (`meteor-sync.service.ts`)
   - Main orchestration service
   - Coordinates mappers, deduplication, change detection
   - Manages sync runs and metrics

2. **MeteorDuplicatePreventionService** (`meteor-duplicate-prevention.service.ts`)
   - Prevents duplicate entities using MongoDB `_id`
   - Validates cached entities still exist
   - Auto-cleanup of stale cache entries

3. **MeteorChangeDetectorService** (`meteor-change-detector.service.ts`)
   - Hash-based change detection (MD5)
   - Field-level change tracking
   - Incremental sync filtering

4. **Entity Mappers** (`mappers/`)
   - Transform MongoDB documents to Supabase format
   - Handle field mapping, type conversion, FK resolution

5. **Media Transfer Service** (`media-transfer.service.ts`)
   - Transfers files from Meteor S3 to Supabase Storage
   - Handles media URL generation

### Database Tables

```sql
-- Entity mapping cache (deduplication)
CREATE TABLE meteor_entity_mapping (
  meteor_id text PRIMARY KEY,
  entity_type text NOT NULL,
  entity_id uuid NOT NULL,
  source_hash text,           -- MD5 hash for change detection
  source_data jsonb,          -- Cached MongoDB document
  first_synced_at timestamptz,
  last_synced_at timestamptz,
  sync_count integer DEFAULT 1,
  sync_status text DEFAULT 'synced', -- synced | pending | error | skipped
  error_message text
);

-- Sync run tracking
CREATE TABLE meteor_sync_runs (
  id uuid PRIMARY KEY,
  sync_type text NOT NULL,    -- full | incremental | entity | resume
  status text NOT NULL,       -- running | completed | failed | partial
  trigger_type text,          -- manual | cron | script | webhook
  triggered_by uuid,
  started_at timestamptz,
  completed_at timestamptz,
  duration_seconds integer,
  metrics jsonb               -- created, updated, skipped, failed counts
);

-- Change tracking
CREATE TABLE meteor_sync_changes (
  id uuid PRIMARY KEY,
  sync_run_id uuid REFERENCES meteor_sync_runs(id),
  meteor_id text,
  entity_type text,
  operation text,             -- created | updated | skipped | error
  changed_fields jsonb,       -- Array of field changes
  error_message text,
  created_at timestamptz
);

-- Sync state (for incremental sync)
CREATE TABLE meteor_sync_state (
  entity_type text PRIMARY KEY,
  last_sync_at timestamptz,
  last_meteor_id text,        -- For resume capability
  checkpoint_data jsonb
);
```

## Quick Commands Reference

### Local Sync (Direct MongoDB Access)

```bash
# Full sync of all entities
pnpm meteor:sync --full

# Incremental sync since last run
pnpm meteor:sync --incremental

# Sync specific entity type
pnpm meteor:sync --entity organization
pnpm meteor:sync --entity candidate
pnpm meteor:sync --entity media

# Preview changes without applying
pnpm meteor:sync --dry-run

# Resume a failed sync
pnpm meteor:sync --resume <run-id>
```

**Requirements:**
- `METEOR_MONGO_URL` - MongoDB connection string
- `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` environment variables

### Staging/Production Sync (Remote via API)

```bash
# Check sync status
pnpm meteor:staging status

# Trigger a full sync
pnpm meteor:staging trigger

# Trigger incremental sync
pnpm meteor:staging trigger --type incremental

# Sync specific entity type
pnpm meteor:staging trigger --entity organization

# Dry run (preview only)
pnpm meteor:staging trigger --dry-run

# View sync history
pnpm meteor:staging history
pnpm meteor:staging history --limit 20

# View detailed logs for a specific run
pnpm meteor:staging logs <run-id>

# View sync statistics
pnpm meteor:staging stats

# Watch sync status in real-time
pnpm meteor:staging watch
pnpm meteor:staging watch --interval 3
```

**Requirements:**
- `METEOR_SYNC_API_KEY` - API key for authentication
- `STAGING_URL` (optional) - defaults to `https://staging.ballee.app`

## User Migration

### migrate-users.ts

Migrates MongoDB users to Supabase auth.users with bcrypt password hash preservation:

```bash
# From skill scripts folder
cd .claude/skills/meteor-sync-specialist/scripts

# Preview migration (no changes)
npx tsx migrate-users.ts --dry-run

# Run full migration
npx tsx migrate-users.ts
```

**What it does:**
1. Fetches all MongoDB users
2. Creates auth.users entries (preserving bcrypt hashes for seamless login)
3. Creates auth.identities for email provider
4. Triggers create profiles via `on_auth_user_created` trigger
5. Updates profiles with `meteor_id` for linking
6. Links `professional_profiles.user_id` via `preferredUserCandidateId`
7. Removes duplicate profiles created by trigger

**Important**: Before running, ensure trigger functions use `public.` schema prefix (see Troubleshooting section).

### sync-orphan-media.ts

Syncs media that only has `userId` (no candidateId/organizationId) to `profile_media`:

```bash
# Preview sync
npx tsx sync-orphan-media.ts --dry-run

# Run sync
npx tsx sync-orphan-media.ts
```

**Prerequisites**: Users must be migrated first (`migrate-users.ts`)

### sync-post-media.ts

Syncs media references from MongoDB Posts to `post_media` table:

```bash
# Preview sync
npx tsx sync-post-media.ts --dry-run

# Run sync
npx tsx sync-post-media.ts
```

**Prerequisites**: Posts must be synced first (`profile_posts` populated)

## Entity Mappers Reference

### Mapper Overview

| Mapper | MongoDB Collection | Supabase Table(s) | Status |
|--------|-------------------|-------------------|--------|
| `OrganizationMapper` | Organizations | organizations | Active |
| `OrganizationMediaMapper` | Media | organization_media | Active |
| `CandidateMapper` | Candidates | profiles + professional_profiles + dancer_profiles | Active |
| `DancerMediaMapper` | Media | dancer_media | Active |
| `ExperienceMapper` | Experiences | experiences | Active |
| `PostMapper` | Posts | posts | Active |
| `LikeMapper` | Likes | likes | Active |
| `FollowMapper` | Follows | follows | Active |
| `AuditionMapper` | VacanciesCollection | auditions | Planned |
| `AuditionApplicationMapper` | Applications | audition_applications | Planned |

### Entity Types

```typescript
type MeteorEntityType =
  | 'organization'
  | 'organization_media'
  | 'candidate'
  | 'media'
  | 'experience'
  | 'post'
  | 'follow'
  | 'like'
  | 'application'
  | 'offer'
  | 'user'
  | 'audition'
  | 'audition_application';
```

### Sync Order (Dependencies)

Entities must be synced in this order to resolve foreign keys:

```
Level 1 (No dependencies):
├── organization
├── organization_media
├── candidate
└── media (dancer_media)

Level 2 (Depends on Level 1):
├── experience (refs: organization, candidate)
├── audition (refs: organization)
└── post (refs: candidate, organization)

Level 3 (Depends on Level 2):
├── audition_application (refs: audition, candidate)
├── like (refs: post, candidate)
├── follow (refs: candidate, organization)
└── comment (refs: post, candidate)
```

### Field Mapping Conventions

| MongoDB Field | Supabase Field | Transform |
|---------------|----------------|-----------|
| `_id` | `meteor_id` | Store for deduplication |
| `meta.createdAt` | `created_at` | ISO timestamp |
| `meta.modifiedAt` | `updated_at` | ISO timestamp |
| `meta.createdBy` | `created_by` | Resolve to user_id |
| camelCase | snake_case | Field name transform |
| ObjectId refs | UUID | Resolve via entity_mapping |

### CandidateMapper (Complex - 3 Tables)

The candidate mapper splits MongoDB documents across 3 Supabase tables:

```typescript
// MongoDB Candidate document
{
  _id: ObjectId,
  userId: ObjectId,
  firstName: string,
  lastName: string,
  stageName: string,
  birthdate: Date,
  bio: string,
  danceStyles: string[],
  height: number,
  weight: number,
  availableForHire: boolean,
  // ... 30+ more fields
}

// Supabase Tables:
// 1. profiles (basic user info)
{
  id: uuid,
  display_name: string,
  first_name: string,
  last_name: string,
  birthdate: date
}

// 2. professional_profiles (career info)
{
  id: uuid,
  user_id: uuid,
  stage_name: string,
  bio: text,
  dance_styles: text[],
  available_for_hire: boolean,
  social_handles: jsonb
}

// 3. dancer_profiles (physical attributes)
{
  id: uuid,
  professional_profile_id: uuid,
  height_cm: integer,
  weight_kg: integer,
  pointe_work: boolean,
  acrobatics: boolean
}
```

### OrganizationMapper

```typescript
// MongoDB → Supabase
{
  _id: ObjectId,          // → meteor_id
  name: string,           // → name
  type: 'school' | 'company' | 'agency', // → type
  logoMediaId: ObjectId,  // → logo_media_id (resolve via mapping)
  headerMediaId: ObjectId, // → header_media_id
  bio: string,            // → description
  website: string,        // → website
  location: {             // → address, city, country
    city: string,
    country: string
  }
}
```

## Sync Modes

### Full Sync

Syncs all documents from MongoDB regardless of previous sync state:

```bash
pnpm meteor:sync --full
```

- Fetches all documents from each collection
- Skips unchanged documents (via hash comparison)
- Updates metrics for all operations
- Use for: Initial migration, data recovery, full refresh

### Incremental Sync

Only syncs documents modified since last successful sync:

```bash
pnpm meteor:sync --incremental
```

- Uses `meta.modifiedAt` > last sync timestamp
- Much faster for routine updates
- Requires `meteor_sync_state` to track last sync
- Use for: Daily/hourly sync jobs

### Entity Sync

Syncs specific entity types only:

```bash
pnpm meteor:sync --entity organization
pnpm meteor:sync --entity candidate
```

- Useful for targeted updates
- Respects dependency order if syncing multiple
- Use for: Fixing specific entity sync issues

### Resume Sync

Continues a failed sync from the last checkpoint:

```bash
pnpm meteor:sync --resume <run-id>
```

- Reads checkpoint from `meteor_sync_state`
- Skips already-synced entities
- Use for: Recovering from network/timeout failures

## Troubleshooting

### Issue 0: User Migration Fails with "relation does not exist"

**Symptoms:**
- Migration fails with errors like `relation "profiles" does not exist`
- Or `relation "professional_profiles" does not exist`

**Cause:**
Trigger functions on `auth.users` reference tables without `public.` schema prefix.
When running outside the normal application context, PostgreSQL can't find the tables.

**Solution:**
Fix the trigger functions to use fully qualified table names:

```sql
-- Fix trigger_generate_profile_slug
CREATE OR REPLACE FUNCTION public.trigger_generate_profile_slug()
RETURNS TRIGGER AS $$
DECLARE
  v_base_slug TEXT;
  v_slug TEXT;
  v_counter INTEGER := 0;
  v_user_row RECORD;
BEGIN
  -- Get user info - USE public.profiles instead of profiles
  SELECT first_name, last_name, display_name INTO v_user_row
  FROM public.profiles WHERE id = NEW.user_id;

  -- ... rest of function
  -- Replace all 'profiles' with 'public.profiles'
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fix create_dancer_profile_on_signup
CREATE OR REPLACE FUNCTION public.create_dancer_profile_on_signup()
RETURNS TRIGGER AS $$
BEGIN
  -- Use public.professional_profiles and public.dancer_profiles
  INSERT INTO public.professional_profiles (id, user_id, profile_type, ...)
  VALUES (gen_random_uuid(), NEW.id, 'dancer', ...);

  INSERT INTO public.dancer_profiles (id, ...)
  VALUES (...);

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fix setup_new_user
CREATE OR REPLACE FUNCTION public.setup_new_user()
RETURNS TRIGGER AS $$
BEGIN
  -- Use public.accounts
  INSERT INTO public.accounts (id, name, slug, ...)
  VALUES (...);

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

**Key tables to prefix with `public.`:**
- `profiles` → `public.profiles`
- `professional_profiles` → `public.professional_profiles`
- `dancer_profiles` → `public.dancer_profiles`
- `accounts` → `public.accounts`
- `accounts_memberships` → `public.accounts_memberships`

### Issue 1: Duplicate Entities Created

**Symptoms:**
- Multiple Supabase records for same MongoDB document
- `meteor_entity_mapping` has duplicate entries

**Debugging:**
```sql
-- Check for duplicate mappings
SELECT meteor_id, entity_type, COUNT(*)
FROM meteor_entity_mapping
GROUP BY meteor_id, entity_type
HAVING COUNT(*) > 1;

-- Find entities without meteor_id
SELECT id, name, created_at
FROM organizations
WHERE meteor_id IS NULL
  AND created_at > NOW() - INTERVAL '1 day';
```

**Solution:**
1. Review `MeteorDuplicatePreventionService.findExistingEntity()`
2. Ensure MongoDB `_id` is correctly passed
3. Check for race conditions in parallel sync

### Issue 2: Stale Cache Entries

**Symptoms:**
- Sync skips creating entities but they don't exist
- Cache shows entity_id but Supabase query returns null

**Debugging:**
```sql
-- Find stale cache entries
SELECT mem.meteor_id, mem.entity_type, mem.entity_id
FROM meteor_entity_mapping mem
LEFT JOIN organizations o ON o.id = mem.entity_id
WHERE mem.entity_type = 'organization'
  AND o.id IS NULL;
```

**Solution:**
```sql
-- Clean up stale entries
DELETE FROM meteor_entity_mapping mem
WHERE NOT EXISTS (
  SELECT 1 FROM organizations WHERE id = mem.entity_id
)
AND entity_type = 'organization';
```

### Issue 3: Foreign Key Resolution Failed

**Symptoms:**
- Sync fails with "constraint violation" errors
- Entity references non-existent foreign key

**Debugging:**
```bash
# Check sync order
pnpm meteor:staging logs <run-id>

# Verify dependency exists
pnpm sql:local "SELECT * FROM organizations WHERE meteor_id = '<org_meteor_id>'"
```

**Solution:**
1. Ensure entities are synced in correct dependency order
2. Check if referenced entity was skipped due to error
3. Re-run sync for dependent entity type first

### Issue 4: Change Detection Not Working

**Symptoms:**
- Sync doesn't update entities when MongoDB data changes
- Entities stuck with old data

**Debugging:**
```sql
-- Check source_hash in mapping
SELECT meteor_id, source_hash, last_synced_at
FROM meteor_entity_mapping
WHERE meteor_id = '<meteor_id>';
```

**Solution:**
1. Review `MeteorChangeDetectorService.hasChanges()`
2. Ensure hash excludes volatile fields (`_id`, `meta`)
3. Force update by deleting cache entry

### Issue 5: Sync Run Stuck in "Running"

**Symptoms:**
- Sync status shows "running" but no progress
- API returns timeout errors

**Debugging:**
```sql
-- Check for stuck runs
SELECT id, sync_type, status, started_at,
       NOW() - started_at as duration
FROM meteor_sync_runs
WHERE status = 'running'
ORDER BY started_at DESC;
```

**Solution:**
```sql
-- Mark stuck run as failed
UPDATE meteor_sync_runs
SET status = 'failed',
    completed_at = NOW(),
    duration_seconds = EXTRACT(EPOCH FROM NOW() - started_at)::integer
WHERE status = 'running'
  AND started_at < NOW() - INTERVAL '30 minutes';
```

## API Endpoint Reference

**Endpoint:** `/api/sync/meteor`

### Authentication

All requests require `Authorization: Bearer <METEOR_SYNC_API_KEY>` header.

### GET Endpoints

| Action | Description |
|--------|-------------|
| `?action=status` | Check MongoDB connection and environment |
| `?action=history&limit=10` | Get sync run history |
| `?action=stats` | Get entity sync statistics |
| `?action=logs&runId=<id>` | Get detailed logs for a sync run |

### POST Endpoint

Trigger a sync:

```json
{
  "syncType": "full|incremental|entity",
  "entityTypes": ["organization", "candidate"],
  "dryRun": false,
  "batchSize": 100,
  "continueOnError": true
}
```

**Response:**
```json
{
  "success": true,
  "syncRunId": "uuid",
  "status": "running",
  "startedAt": "2025-12-09T10:00:00Z"
}
```

## Diagnostic Scripts

### diagnose-sync-status (meteor-diagnose.cjs)

Check overall sync health:

```bash
# From apps/web directory
cd apps/web && node scripts/meteor-diagnose.cjs
```

**Checks:**
- MongoDB connection status
- Recent sync runs and their status
- Entity mapping statistics
- Stale cache entries
- Stuck running syncs
- Entities with errors
- Sync state for incremental sync

### validate-entity-mapping.ts

Validate cache integrity (TypeScript version in skill folder):

```bash
# From apps/web directory with tsx available
cd apps/web && npx tsx ../../.claude/skills/meteor-sync-specialist/scripts/validate-entity-mapping.ts
```

**Checks:**
- Cache entries pointing to deleted entities
- Orphaned cache entries
- Duplicate mappings

### compare-counts.ts

Compare MongoDB vs Supabase counts:

```bash
cd apps/web && npx tsx ../../.claude/skills/meteor-sync-specialist/scripts/compare-counts.ts
```

**Output:**
```
Entity Type         MongoDB    Supabase   Diff    Synced%
─────────────────────────────────────────────────────────
organization        428        425        -3      99.3%
candidate           20018      19854      -164    99.2%
media               75140      73278      -1862   97.5%
post                1492       1490       -2      99.9%
```

## Best Practices

### Duplicate Prevention

1. **Always use MongoDB `_id`** - Never rely on name/email matching
2. **Validate cached entities** - Check entity exists before trusting cache
3. **Auto-cleanup stale entries** - Remove cache when entity deleted
4. **Log all cache operations** - Aids debugging

### Change Detection

1. **Exclude volatile fields** - Don't hash `_id`, `meta.*`
2. **Use consistent ordering** - Sort keys before hashing
3. **Log detected changes** - Show what triggered update
4. **Batch updates** - Don't update one field at a time

### Error Handling

1. **Continue on error** - Don't stop sync for one bad document
2. **Track failed entities** - Record in `meteor_sync_changes`
3. **Log with context** - Include meteor_id, entity_type
4. **Allow resume** - Save checkpoint for recovery

### Performance

1. **Batch size** - Default 100 documents per batch
2. **Parallel where possible** - Independent entity types can run in parallel
3. **Index meteor_id** - Ensure B-tree index on `meteor_id` columns
4. **Incremental preferred** - Use incremental sync for routine updates

## Common Code Patterns

### Safe Entity Lookup

```typescript
// CORRECT - Validates entity exists
const existingId = await duplicatePrevention.findExistingEntity(
  meteorId,
  'organization'
);

if (existingId) {
  // Entity exists and is valid
  const hasChanges = changeDetector.hasChanges(newData, cachedData);
  if (hasChanges) {
    await updateEntity(existingId, newData);
  }
} else {
  // Create new entity
  await createEntity(newData);
}
```

### Idempotent Sync

```typescript
async function syncDocument(doc: MeteorDocument) {
  const meteorId = doc._id.toString();

  // Check if exists (validates entity still exists)
  const existingId = await duplicatePrevention.findExistingEntity(
    meteorId,
    entityType
  );

  if (existingId) {
    // Get cached data for comparison
    const cachedData = await duplicatePrevention.getCachedSourceData(meteorId);

    if (changeDetector.hasChanges(doc, cachedData)) {
      await updateEntity(existingId, mapper.mapToSupabase(doc));
      await duplicatePrevention.updateEntityMapping(meteorId, doc);
      return { operation: 'updated' };
    }
    return { operation: 'skipped' };
  } else {
    const newId = await createEntity(mapper.mapToSupabase(doc));
    await duplicatePrevention.registerEntity(meteorId, entityType, newId, doc);
    return { operation: 'created' };
  }
}
```

### Batch Processing with Error Handling

```typescript
async function syncBatch(documents: MeteorDocument[]) {
  const results = {
    created: 0,
    updated: 0,
    skipped: 0,
    failed: 0,
    errors: [] as Array<{ meteorId: string; error: string }>
  };

  for (const doc of documents) {
    try {
      const result = await syncDocument(doc);
      results[result.operation]++;
    } catch (error) {
      results.failed++;
      results.errors.push({
        meteorId: doc._id.toString(),
        error: error.message
      });

      // Mark in entity mapping for retry
      await duplicatePrevention.markEntityError(
        doc._id.toString(),
        entityType,
        error.message
      );

      // Continue processing other documents
      console.error(`Failed to sync ${doc._id}:`, error);
    }
  }

  return results;
}
```

## Reference Files

### Core Sync Infrastructure
- Main service: `apps/web/app/admin/sync/_lib/server/meteor/meteor-sync.service.ts`
- Duplicate prevention: `apps/web/app/admin/sync/_lib/server/meteor/meteor-duplicate-prevention.service.ts`
- Change detector: `apps/web/app/admin/sync/_lib/server/meteor/meteor-change-detector.service.ts`
- Media transfer: `apps/web/app/admin/sync/_lib/server/meteor/media-transfer.service.ts`

### Entity Mappers
- Mapper index: `apps/web/app/admin/sync/_lib/server/meteor/mappers/index.ts`
- Organization: `apps/web/app/admin/sync/_lib/server/meteor/mappers/organization.mapper.ts`
- Candidate: `apps/web/app/admin/sync/_lib/server/meteor/mappers/candidate.mapper.ts`
- Experience: `apps/web/app/admin/sync/_lib/server/meteor/mappers/experience.mapper.ts`
- Dancer media: `apps/web/app/admin/sync/_lib/server/meteor/mappers/dancer-media.mapper.ts`
- Organization media: `apps/web/app/admin/sync/_lib/server/meteor/mappers/organization-media.mapper.ts`
- Post: `apps/web/app/admin/sync/_lib/server/meteor/mappers/post.mapper.ts`
- Like: `apps/web/app/admin/sync/_lib/server/meteor/mappers/like.mapper.ts`
- Follow: `apps/web/app/admin/sync/_lib/server/meteor/mappers/follow.mapper.ts`

### CLI Scripts
- Local sync: `scripts/meteor-sync/run-sync.ts`
- Staging sync: `scripts/meteor-sync/staging-sync.ts`
- Media sync: `scripts/sync-remaining-media.ts`

### Migration Scripts (in skill folder)
- User migration: `.claude/skills/meteor-sync-specialist/scripts/migrate-users.ts`
- Orphan media: `.claude/skills/meteor-sync-specialist/scripts/sync-orphan-media.ts`
- Post media: `.claude/skills/meteor-sync-specialist/scripts/sync-post-media.ts`
- Entity validation: `.claude/skills/meteor-sync-specialist/scripts/validate-entity-mapping.ts`
- Count comparison: `.claude/skills/meteor-sync-specialist/scripts/compare-counts.ts`
- Sync diagnostics: `.claude/skills/meteor-sync-specialist/scripts/diagnose-sync-status.ts`

### API & Admin UI
- API route: `apps/web/app/api/sync/meteor/route.ts`
- Admin page: `apps/web/app/admin/sync/meteor/page.tsx`
- Trigger panel: `apps/web/app/admin/sync/meteor/_components/meteor-sync-trigger-panel.tsx`
- History component: `apps/web/app/admin/sync/meteor/_components/meteor-sync-history.tsx`
- Stats component: `apps/web/app/admin/sync/meteor/_components/meteor-sync-stats.tsx`

### Server Actions
- Sync actions: `apps/web/app/admin/sync/meteor/_actions/meteor-sync.actions.ts`
- User sync: `apps/web/app/admin/sync/meteor/_actions/meteor-user-sync.actions.ts`

### Database Migrations
- Infrastructure: `apps/web/supabase/migrations/20251207131700_create_meteor_sync_infrastructure.sql`
- Media meteor_id: `apps/web/supabase/migrations/20251207145437_add_meteor_id_to_media_and_comments.sql`
- Community meteor_id: `apps/web/supabase/migrations/20251207160100_add_meteor_id_to_community_tables.sql`
- Dancer media meteor_id: `apps/web/supabase/migrations/20251208183601_add_meteor_id_to_dancer_media.sql`

### Documentation
- Sync README: `scripts/meteor-sync/README.md`
- Migration README: `scripts/migration/README.md`
- WIP - Meteor parity: `docs/wip/active/WIP_achieving_100_percent_meteor_parity_2025_12_09.md`
- WIP - Media sync: `docs/wip/active/WIP_syncing_remaining_mongodb_media_2025_12_09.md`

### Related Skills
- MongoDB queries: `.claude/skills/mongodb-production-query/SKILL.md`
- Airtable sync: `.claude/skills/airtable-sync-specialist/SKILL.md`
