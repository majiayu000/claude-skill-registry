---
name: postgres-nanoid
description: This skill should be used when the user asks to "generate IDs", "create identifiers", "use nanoid", "add public_id", "prefixed identifiers", "short IDs", or discusses ID generation strategies, public vs internal IDs, or URL-friendly identifiers. Use nanoid for public identifiers and UUID for auth.users references.
version: 1.0.0
---

# PostgreSQL Nanoid Identifiers

This skill provides guidance for implementing nanoid-based identifiers in PostgreSQL, with a focus on Supabase integration.

> **Philosophy:** Use nanoid for public-facing identifiers (URLs, APIs, exports). Use UUID for internal references to auth.users. Prefixes provide context and prevent ID collisions across entities.

## Quick Reference

| Use Case | ID Type | Example |
|----------|---------|---------|
| Public API/URLs | nanoid with prefix | `usr_V1StGXR8_Z5jdHi` |
| Primary key (user tables) | UUID | `auth.users.id` as PK+FK |
| Primary key (other tables) | UUID or nanoid | Context-dependent |
| Join tables | UUID FK | Reference auth.users directly |

## Core Principle: Hybrid ID Approach

```
+-------------------+     +------------------+
|     profiles      |     |   auth.users     |
+-------------------+     +------------------+
| user_id (UUID) PK |---->| id (UUID)    PK  |
| public_id (nanoid)|     |                  |
+-------------------+     +------------------+
```

- **`user_id`**: Primary key AND foreign key to auth.users (UUID) - used for RLS and joins
- **`public_id`**: Exposed in URLs, APIs, exports (nanoid with prefix)

This approach provides:
- Direct RLS policies using `auth.uid() = user_id`
- Clean foreign key relationship
- URL-friendly public identifiers
- Clear separation of internal vs public identity

## Standard Prefixes

| Entity | Prefix | Length | Example | Regex Pattern |
|--------|--------|--------|---------|---------------|
| User (profile) | `usr_` | 21 | `usr_V1StGXR8_Z5jdHi` | `^usr_[0-9a-zA-Z]{17}$` |
| Organization | `org_` | 21 | `org_kJ7mNpQ2xWzL9aB` | `^org_[0-9a-zA-Z]{17}$` |
| Team | `team_` | 22 | `team_uV4wX7yZaB3cD` | `^team_[0-9a-zA-Z]{17}$` |
| Customer | `cus_` | 21 | `cus_oP8qR1sTuV4wX` | `^cus_[0-9a-zA-Z]{17}$` |
| Product | `prd_` | 21 | `prd_mN3kL9pQwE7rT` | `^prd_[0-9a-zA-Z]{17}$` |
| Order | `ord_` | 21 | `ord_xYz7aBcDeF2gH` | `^ord_[0-9a-zA-Z]{17}$` |
| Invoice | `inv_` | 21 | `inv_9sK3pLmNqR5tU` | `^inv_[0-9a-zA-Z]{17}$` |
| Subscription | `sub_` | 21 | `sub_gH2iJ5kL8mN9` | `^sub_[0-9a-zA-Z]{17}$` |
| Transaction | `txn_` | 21 | `txn_aB4cD7eF0gH3` | `^txn_[0-9a-zA-Z]{17}$` |
| Session | `ses_` | 21 | `ses_rT5vU8wX2zY4` | `^ses_[0-9a-zA-Z]{17}$` |
| Project | `proj_` | 22 | `proj_aB3cD6eF9gH` | `^proj_[0-9a-zA-Z]{17}$` |
| Workspace | `ws_` | 20 | `ws_kL2mN5pQ8rS1tU` | `^ws_[0-9a-zA-Z]{17}$` |
| File | `file_` | 22 | `file_vW4xY7zA0bC` | `^file_[0-9a-zA-Z]{17}$` |
| API Key | `key_` | 21 | `key_dE3fG6hI9jK2` | `^key_[0-9a-zA-Z]{17}$` |
| Webhook | `whk_` | 21 | `whk_lM4nO7pQ0rS` | `^whk_[0-9a-zA-Z]{17}$` |

## Table Definition Patterns

### Pattern 1: User-Linked Tables (Recommended)

For tables with 1:1 relationship to auth.users:

```sql
-- Hybrid approach: UUID as PK, nanoid as public_id
CREATE TABLE public.profiles (
  -- Primary key is also foreign key to auth.users
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Public identifier for URLs/APIs
  public_id TEXT UNIQUE NOT NULL DEFAULT nanoid('usr_'),

  -- Profile data
  display_name TEXT,
  avatar_url TEXT,

  -- Timestamps
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

  -- Constraints
  CONSTRAINT profiles_public_id_format CHECK (public_id ~ '^usr_[0-9a-zA-Z]{17}$')
);

COMMENT ON COLUMN public.profiles.user_id IS 'Internal ID - use for RLS and joins';
COMMENT ON COLUMN public.profiles.public_id IS 'Public ID - use in URLs and APIs';

-- Index for public_id lookups (user_id already indexed as PK)
CREATE INDEX profiles_public_id_idx ON public.profiles(public_id);
```

### Pattern 2: Standalone Tables

For tables not directly linked to auth.users:

```sql
CREATE TABLE public.products (
  -- nanoid as primary key
  id TEXT PRIMARY KEY DEFAULT nanoid('prd_'),

  -- Data
  name TEXT NOT NULL,
  price NUMERIC(10,2) NOT NULL,

  -- Ownership (if needed)
  created_by UUID REFERENCES auth.users(id),

  -- Timestamps
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

  -- Constraints
  CONSTRAINT products_id_format CHECK (id ~ '^prd_[0-9a-zA-Z]{17}$')
);
```

## Migration Pattern

```sql
-- Migration: Add nanoid to existing table
-- Step 1: Add the column
ALTER TABLE public.customers
ADD COLUMN public_id TEXT;

-- Step 2: Generate IDs for existing rows
UPDATE public.customers
SET public_id = nanoid('cus_')
WHERE public_id IS NULL;

-- Step 3: Add constraints
ALTER TABLE public.customers
ALTER COLUMN public_id SET NOT NULL,
ADD CONSTRAINT customers_public_id_unique UNIQUE (public_id),
ADD CONSTRAINT customers_public_id_format CHECK (public_id ~ '^cus_[0-9a-zA-Z]{17}$');

-- Step 4: Set default for new rows
ALTER TABLE public.customers
ALTER COLUMN public_id SET DEFAULT nanoid('cus_');
```

## API Response Pattern

Always return public_id in API responses, never internal UUIDs:

```typescript
// Good: Return public_id
return {
  id: profile.public_id,    // usr_V1StGXR8_Z5jdHi
  name: profile.display_name,
  // Never expose user_id (UUID) in API
}

// Bad: Exposing internal UUID
return {
  id: profile.user_id,      // Don't do this!
  ...
}
```

## Query Patterns

```typescript
// Lookup by public_id (for API routes)
const { data } = await supabase
  .from('profiles')
  .select('*')
  .eq('public_id', 'usr_V1StGXR8_Z5jdHi')
  .single()

// Current user's profile (RLS handles auth)
const { data } = await supabase
  .from('profiles')
  .select('*')
  .single()  // RLS filters to current user
```

## TypeScript Types

```typescript
// Type-safe prefixed IDs
type UserPublicId = `usr_${string}`
type OrgId = `org_${string}`
type OrderId = `ord_${string}`

interface Profile {
  user_id: string        // UUID - internal use only
  public_id: UserPublicId  // nanoid - for APIs
  displayName: string
}

// Validation helper
function isValidUserPublicId(id: string): id is UserPublicId {
  return /^usr_[0-9a-zA-Z]{17}$/.test(id)
}

// API response type (excludes internal IDs)
interface ProfileResponse {
  id: UserPublicId  // Map public_id to 'id' in response
  displayName: string
}
```

## When to Use What

| Scenario | Use |
|----------|-----|
| User profile table PK | UUID (from auth.users) |
| User profile public ID | nanoid with prefix |
| Standalone table PK | nanoid with prefix |
| Foreign key to auth.users | UUID |
| Public API endpoint | nanoid (public_id) |
| Internal service-to-service | UUID |
| URL slugs | nanoid (URL-safe by default) |
| Export/Import IDs | nanoid (human-readable) |
| Legacy table migration | Add public_id column |

## Common Mistakes

1. **Exposing auth.users UUID in APIs** - Always use nanoid public_id
2. **Using nanoid as PK for user tables** - Use UUID from auth.users as PK
3. **Inconsistent prefix lengths** - Keep random part at 17 chars
4. **Missing CHECK constraints** - Always validate format
5. **Not indexing public_id** - Add index for lookup performance
6. **Using nanoid for auth FK** - Use UUID for auth.users references

## Performance Notes

- nanoid generation: ~110,000 IDs/second
- Collision probability: Negligible at 17 random chars
- Index performance: Comparable to UUID
- Storage: ~21 bytes vs 16 bytes for UUID (minimal difference)

## Additional Resources

For detailed implementation, see reference files:
- **`references/installation.md`** - PostgreSQL function setup
- **`references/prefix-conventions.md`** - Complete prefix guidelines
