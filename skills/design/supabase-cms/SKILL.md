---
name: supabase-cms
description: Supabase CMS integration patterns, schema design, RLS policies, and content
  management for Astro websites. Use when building CMS systems, setting up Supabase
  backends, creating content schemas, implem
---

---
name: supabase-cms
description: Supabase CMS integration patterns, schema design, RLS policies, and content management for Astro websites. Use when building CMS systems, setting up Supabase backends, creating content schemas, implementing RLS security, or when user mentions Supabase CMS, headless CMS, content management, database schemas, or Row Level Security.
allowed-tools: - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - mcp__figma-design-system
---

# Supabase CMS Integration for Astro

Complete Supabase CMS integration for Astro websites, including database schema design, RLS policies, content management workflows, and client setup.

## Overview

This skill provides comprehensive Supabase CMS support:
- Database schema design for content types
- Row Level Security (RLS) policies
- Draft/publish workflows
- Content versioning patterns
- Supabase client integration with Astro
- Real-time content updates

## Instructions

### 1. Initial Setup

Run the setup script to initialize Supabase CMS in an Astro project:

```bash
bash scripts/setup-supabase-cms.sh [project-path]
```

This script:
- Creates Supabase client configuration
- Sets up environment variables
- Installs @supabase/supabase-js
- Creates database migration template
- Adds TypeScript types generation

### 2. Design Content Schema

Use schema templates to design content tables:

**Blog/Posts Schema:**
```bash
# Read template for blog content
Read: templates/schemas/blog-schema.sql
Read: templates/schemas/blog-with-categories.sql
```

**Pages Schema:**
```bash
# Read template for static pages
Read: templates/schemas/pages-schema.sql
```

**Media/Assets Schema:**
```bash
# Read template for media management
Read: templates/schemas/media-schema.sql
```

**Multi-tenant Schema:**
```bash
# Read template for multi-tenant content
Read: templates/schemas/multi-tenant-schema.sql
```

### 3. Apply Database Migrations

Apply schema migrations to Supabase:

```bash
bash scripts/apply-migration.sh [migration-file]
```

This script:
- Validates SQL syntax
- Applies migration via Supabase CLI
- Generates TypeScript types
- Updates local schema cache

### 4. Configure RLS Policies

Implement Row Level Security policies:

**Basic RLS Templates:**
```bash
Read: templates/rls/basic-policies.sql
Read: templates/rls/multi-tenant-policies.sql
Read: templates/rls/draft-publish-policies.sql
```

**Apply RLS Policies:**
```bash
bash scripts/apply-rls-policies.sh [table-name] [policy-type]
```

Policy types:
- `public-read`: Anyone can read, authenticated can write
- `owner-only`: Only owner can read/write
- `draft-publish`: Public reads published, owner manages drafts
- `multi-tenant`: Tenant isolation with RLS

### 5. Setup Content Management Workflows

Use workflow templates for content operations:

**Draft/Publish Workflow:**
```bash
Read: templates/workflows/draft-publish.ts
```

Features:
- Draft creation and editing
- Publish/unpublish actions
- Version history tracking
- Scheduled publishing

**Content Versioning:**
```bash
Read: templates/workflows/versioning.ts
```

Features:
- Version snapshots
- Rollback capabilities
- Diff viewing
- Audit trails

### 6. Integrate Supabase Client

Setup Supabase client in Astro:

**Client Configuration:**
```bash
Read: templates/client/supabase-client.ts
Read: templates/client/server-client.ts
```

**Query Patterns:**
```bash
Read: templates/queries/content-queries.ts
Read: templates/queries/filtered-queries.ts
Read: templates/queries/paginated-queries.ts
```

### 7. Generate TypeScript Types

Generate types from database schema:

```bash
bash scripts/generate-supabase-types.sh [project-path]
```

This creates:
- TypeScript definitions for all tables
- Type-safe query builders
- Auto-completion for content fields

### 8. Setup Real-time Subscriptions

Enable real-time content updates:

**Realtime Templates:**
```bash
Read: templates/realtime/content-subscription.ts
Read: templates/realtime/live-preview.ts
```

Features:
- Live content updates
- Collaborative editing indicators
- Real-time notifications

## Best Practices

### Schema Design
- Use `created_at`, `updated_at` timestamps
- Add `slug` fields with unique constraints
- Include `status` enum for draft/published states
- Use `published_at` for scheduling
- Add `metadata` JSONB for flexible fields

### RLS Security
- Enable RLS on all content tables
- Test policies with different user roles
- Use service role key only on server-side
- Implement tenant isolation for multi-tenant apps
- Add audit logging for content changes

### Content Management
- Implement draft/publish workflows
- Add version history for important content
- Use soft deletes instead of hard deletes
- Index frequently queried fields
- Optimize images before storing

### Performance
- Use select() to fetch only needed columns
- Implement pagination for large lists
- Cache frequently accessed content
- Use CDN for published content
- Enable Supabase caching headers

## Examples

### Create Content Table Migration

```bash
# Use blog schema template
Read: templates/schemas/blog-schema.sql

# Customize for your needs, then apply
bash scripts/apply-migration.sh migrations/001_create_posts.sql
```

### Setup RLS for Blog Posts

```bash
# Apply draft-publish policies
bash scripts/apply-rls-policies.sh posts draft-publish

# Test policies
bash scripts/test-rls-policies.sh posts
```

### Query Content in Astro

```typescript
// Read query template
Read: templates/queries/content-queries.ts

// Use in Astro page
import { supabase } from '@/lib/supabase'

const { data: posts } = await supabase
  .from('posts')
  .select('*')
  .eq('status', 'published')
  .order('published_at', { ascending: false })
```

### Enable Real-time Updates

```typescript
// Read realtime template
Read: templates/realtime/content-subscription.ts

// Subscribe to content changes
const subscription = supabase
  .channel('content-changes')
  .on('postgres_changes'
    { event: '*', schema: 'public', table: 'posts' }
    handleContentChange
  )
  .subscribe()
```

## Troubleshooting

### Migration Fails
- Check SQL syntax with `supabase db lint`
- Verify table/column names don't conflict
- Ensure proper data types used
- Check for missing foreign key constraints

### RLS Policies Not Working
- Verify RLS is enabled: `ALTER TABLE posts ENABLE ROW LEVEL SECURITY;`
- Test with different user contexts
- Check policy conditions are correct
- Use `auth.uid()` for user-specific policies

### TypeScript Types Out of Sync
- Run `bash scripts/generate-supabase-types.sh`
- Restart TypeScript server
- Clear `.astro` cache directory
- Verify Supabase CLI is up to date

### Real-time Not Updating
- Enable realtime on table in Supabase dashboard
- Check websocket connection
- Verify RLS policies allow reading
- Monitor Supabase logs for errors

## Additional Resources

- [Supabase Database Docs](https://supabase.com/docs/guides/database)
- [RLS Policies Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [Astro + Supabase Guide](https://docs.astro.build/en/guides/backend/supabase/)
- [TypeScript Type Generation](https://supabase.com/docs/guides/api/generating-types)
