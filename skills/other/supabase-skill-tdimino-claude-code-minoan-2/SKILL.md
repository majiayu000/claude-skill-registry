---
name: supabase-skill
description: Configure and manage Supabase projects using MCP (Model Context Protocol). Use this skill when working with Supabase databases, setting up MCP servers, designing database schemas, implementing Row Level Security, managing migrations, or building modern data architectures with PostgreSQL. Essential for Supabase development, database design, and AI-powered database operations.
---

# Supabase MCP Skill

## Overview

This skill provides comprehensive guidance for working with Supabase through the Model Context Protocol (MCP), enabling AI-powered database operations, modern schema design, and production-ready database architectures.

## When to Use This Skill

Use this skill when you encounter ANY of the following:

### Setup & Configuration
- Setting up or configuring Supabase MCP servers (Cursor, Claude Desktop, Claude Code CLI)
- Connecting AI tools to Supabase projects
- Debugging MCP connection issues
- Configuring read-only mode, project scoping, or feature groups

### Database Design
- Designing database schemas following best practices
- Implementing table relationships (one-to-many, many-to-many, polymorphic)
- Choosing between normalization patterns (single table vs class table inheritance)
- Designing for multi-tenancy or microservices
- Working with temporal data or audit logging

### Security & Access Control
- Implementing Row Level Security (RLS) policies
- Setting up authentication integration with `auth.users`
- Building role-based access control (RBAC)
- Securing multi-tenant applications
- Preventing unauthorized data access

### Migrations & Schema Evolution
- Creating and managing database migrations
- Evolving schemas without breaking changes
- Handling backward compatibility
- Using Supabase branching for testing

### Production Patterns
- Session management with timeout logic
- Memory persistence patterns (dual persistence with soul + process memory)
- Message storage with region-based organization
- State management with validation
- Error handling and graceful degradation

### Performance & Optimization
- Indexing strategies for query performance
- Query optimization with EXPLAIN ANALYZE
- Connection pooling configuration
- Read replica setup for scaling

## Quick Reference Examples

### 1. MCP Server Setup (Claude Code CLI)

```bash
# Basic installation with project scoping
claude mcp add --transport stdio \
  --env SUPABASE_ACCESS_TOKEN=your_personal_access_token \
  --scope local \
  supabase -- npx -y @supabase/mcp-server-supabase@latest \
  --project-ref=your_project_ref

# With read-only mode (safe for exploration)
claude mcp add --transport stdio \
  --env SUPABASE_ACCESS_TOKEN=your_token \
  --scope local \
  supabase -- npx -y @supabase/mcp-server-supabase@latest \
  --project-ref=your_project_ref \
  --read-only
```

### 2. Singleton Supabase Client (TypeScript)

```typescript
import { createClient, SupabaseClient } from '@supabase/supabase-js';

let supabaseClient: SupabaseClient | null = null;

export function getSupabaseClient(): SupabaseClient {
  if (!supabaseClient) {
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseServiceKey = process.env.SUPABASE_SERVICE_KEY;

    if (!supabaseUrl || !supabaseServiceKey) {
      throw new Error('Missing Supabase environment variables');
    }

    supabaseClient = createClient(supabaseUrl, supabaseServiceKey, {
      auth: {
        autoRefreshToken: false,  // Server-side: no refresh needed
        persistSession: false,     // Server-side: no persistence
      },
    });
  }

  return supabaseClient;
}
```

### 3. User Profile with RLS (SQL)

```sql
-- Create profiles table linked to auth.users
create table public.profiles (
  id uuid references auth.users(id) primary key,
  username text unique not null,
  full_name text,
  avatar_url text,
  created_at timestamptz default now()
);

-- Enable RLS
alter table public.profiles enable row level security;

-- Allow anyone to view profiles
create policy "Users can view all profiles"
  on public.profiles for select
  using (true);

-- Users can only update their own profile
create policy "Users can update own profile"
  on public.profiles for update
  using (auth.uid() = id);
```

### 4. Multi-Tenant Organizations with RLS

```sql
-- Organizations table
create table public.organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  slug text unique not null
);

-- Organization members junction table
create table public.org_members (
  org_id uuid references public.organizations(id) on delete cascade,
  user_id uuid references auth.users(id) on delete cascade,
  role text not null check (role in ('owner', 'admin', 'member')),
  primary key (org_id, user_id)
);

-- RLS: Users can only see organizations they're members of
alter table public.organizations enable row level security;

create policy "Users can view own organizations"
  on public.organizations for select
  using (
    exists (
      select 1 from public.org_members
      where org_members.org_id = organizations.id
      and org_members.user_id = auth.uid()
    )
  );
```

### 5. Session Load-or-Create Pattern

```typescript
// Load existing session or create new one
const { data: existing, error: fetchError } = await supabase
  .from('user_sessions')
  .select('*')
  .eq('phone_number', phoneNumber)
  .single();

// Handle "no rows returned" as valid (not an error)
if (fetchError && fetchError.code !== 'PGRST116') {
  throw new Error(`Failed to load session: ${fetchError.message}`);
}

if (existing) {
  // Update existing session
  await supabase
    .from('user_sessions')
    .update({ last_active_at: new Date().toISOString() })
    .eq('id', existing.id);

  return existing;
}

// Create new session if none exists
const { data: newSession } = await supabase
  .from('user_sessions')
  .insert({ phone_number: phoneNumber })
  .select()
  .single();

return newSession;
```

### 6. Upsert Pattern for Key-Value Storage

```typescript
// Save or update soul memory (upsert pattern)
const { data, error } = await supabase
  .from('soul_memories')
  .upsert(
    {
      session_id: sessionId,
      key: 'user_name',
      value: { firstName: 'Alice', lastName: 'Smith' },
      updated_at: new Date().toISOString(),
    },
    { onConflict: 'session_id,key' }  // Composite unique constraint
  )
  .select()
  .single();
```

### 7. Temporal Data Pattern (History Tracking)

```sql
-- Products with full history tracking
create table public.products_history (
  id uuid not null,
  name text not null,
  price numeric(10,2) not null,

  -- Temporal columns
  valid_from timestamptz not null default now(),
  valid_to timestamptz,  -- null = current version

  -- Audit columns
  changed_by uuid references auth.users(id),
  change_reason text,

  primary key (id, valid_from)
);

-- View for current products only
create view public.products as
select id, name, price
from public.products_history
where valid_to is null;
```

### 8. Materialized View for Analytics

```sql
-- Aggregate analytics data for fast queries
create materialized view public.orders_analytics as
select
  date_trunc('day', created_at) as order_date,
  count(*) as total_orders,
  sum(total) as revenue,
  avg(total) as avg_order_value
from public.orders
where status = 'completed'
group by date_trunc('day', created_at);

-- Refresh function
create or replace function refresh_analytics()
returns void as $$
begin
  refresh materialized view public.orders_analytics;
end;
$$ language plpgsql;
```

### 9. Audit Logging with Triggers

```sql
-- Audit logs table
create table public.audit_logs (
  id bigint generated always as identity primary key,
  table_name text not null,
  record_id uuid not null,
  action text not null check (action in ('insert', 'update', 'delete')),
  old_data jsonb,
  new_data jsonb,
  user_id uuid references auth.users(id),
  created_at timestamptz default now()
);

-- Trigger function for automatic auditing
create or replace function public.audit_trigger()
returns trigger as $$
begin
  insert into public.audit_logs (
    table_name, record_id, action, old_data, new_data, user_id
  ) values (
    TG_TABLE_NAME,
    coalesce(NEW.id, OLD.id),
    lower(TG_OP),
    to_jsonb(OLD),
    to_jsonb(NEW),
    auth.uid()
  );
  return NEW;
end;
$$ language plpgsql security definer;
```

### 10. Event-Driven Pattern with pg_notify

```sql
-- Publish events using PostgreSQL NOTIFY
create or replace function orders_service.notify_order_created()
returns trigger as $$
begin
  perform pg_notify(
    'order_created',
    json_build_object(
      'order_id', NEW.id,
      'user_id', NEW.user_id,
      'total', NEW.total
    )::text
  );
  return NEW;
end;
$$ language plpgsql;

create trigger order_created_trigger
after insert on orders_service.orders
for each row execute function orders_service.notify_order_created();
```

## Key Concepts

### Row Level Security (RLS)
PostgreSQL feature that restricts which rows users can access based on policies. Essential for multi-tenant applications and user data isolation.

### MCP (Model Context Protocol)
Protocol enabling AI assistants to interact with external services like Supabase. Provides natural language querying and schema operations.

### Upsert Pattern
Insert a new row or update if it already exists, using `onConflict`. Atomic operation preventing race conditions.

### Composite Keys
Unique constraints across multiple columns (e.g., `session_id,key`). Used for scoping data within contexts.

### JSONB Storage
PostgreSQL's binary JSON storage format. Allows flexible schemas while maintaining query performance.

### Temporal Data
Tracking historical changes with `valid_from` and `valid_to` timestamps. Enables point-in-time queries.

### Service Role vs Anon Key
- **Service Role**: Admin access, bypasses RLS (use server-side only)
- **Anon Key**: User access, subject to RLS (safe for client-side)

## Reference Files

### Core References

#### `references/mcp-setup.md` - MCP Server Configuration
Complete guide for setting up Supabase MCP servers:
- Remote (hosted) vs Local (self-hosted) installation
- Configuration for Cursor, Claude Desktop, Claude Code CLI
- Authentication with OAuth and Personal Access Tokens
- Security best practices (read-only mode, project scoping)
- Troubleshooting connection and auth issues

#### `references/database-patterns.md` - Modern Database Design
Architectural patterns for scalable applications:
- Data Lakehouse Pattern (OLTP + OLAP in one system)
- Microservices Pattern (database per service)
- Event Sourcing Pattern (complete audit trail)
- CQRS Pattern (separate read/write models)
- Inheritance patterns (single table vs class table)
- Polymorphic associations
- Temporal data patterns (SCD Type 2)

#### `references/schema-design.md` - PostgreSQL Best Practices
Guidelines for robust schema design:
- Primary key strategies (UUID vs serial)
- Foreign key relationships and cascading
- Index design for query optimization
- Constraint enforcement
- Default values and computed columns
- JSON/JSONB usage patterns
- Normalization strategies

#### `references/security.md` - RLS and Authentication
Production-grade security implementation:
- Row Level Security policy patterns
- Authentication integration with auth.users
- Role-based access control (RBAC)
- Data encryption strategies
- Audit logging patterns
- Multi-tenancy security models

#### `references/tools-reference.md` - MCP Tools
Complete documentation of available MCP tools:
- Natural language querying
- Schema introspection
- Migration management
- Project configuration retrieval
- Database branching (experimental)
- Log analysis and debugging

### Official Supabase Documentation

#### `references/official-docs/row-level-security.md`
Complete RLS guide from official Supabase docs:
- 10+ RLS policy patterns
- Production examples from real repositories
- Common pitfalls and solutions
- Testing RLS policies
- Performance considerations

#### `references/official-docs/migrations.md`
Database migrations guide:
- Imperative migrations (SQL files)
- Declarative schemas (schema.yml)
- Migration workflow and best practices
- Handling breaking changes
- Using Supabase branches for testing

### Production Patterns

#### `references/production-patterns.md`
Real-world patterns from Twilio-Aldea (production SMS AI platform):
- Session management with timeout logic
- Dual persistence (soul + process memory)
- Message storage with region-based organization
- State management with validation
- Error handling and graceful degradation
- Load-or-create patterns

### Code Examples

#### `assets/examples/supabase-client.ts`
Client initialization with singleton pattern for server-side applications

#### `assets/examples/session-management.ts`
Session management with automatic timeout and state reset

#### `assets/examples/memory-store.ts`
Dual persistence pattern (soul memory + process memory)

#### `assets/examples/rls-policies.sql`
10 production-ready RLS policy patterns covering common use cases

### GitHub Repository (NEW)

#### `references/github/README.md`
Official Supabase JS client README from GitHub (supabase/supabase-js, 4,045 stars)

#### `references/github/issues.md`
38 GitHub issues showing common problems and solutions:
- JWT token validation issues
- Next.js cache integration
- BigInt ID handling
- WebSocket race conditions
- RLS header propagation
- Realtime subscription bugs

#### `references/github/CHANGELOG.md`
Complete version history with breaking changes and migrations

#### `references/github/releases.md`
410 GitHub releases with detailed release notes and migration guides

#### `references/github/file_structure.md`
Repository structure (521 files) showing source code organization

## Working with This Skill

### For Beginners

**Start Here:**
1. Read `references/mcp-setup.md` for initial MCP configuration
2. Review `assets/examples/supabase-client.ts` for client setup basics
3. Study `references/official-docs/migrations.md` for schema management
4. Practice simple CRUD operations through MCP
5. Review Quick Reference Examples #1-3 above

**First Project:**
- Set up MCP in read-only mode to explore safely
- Create a simple user profiles table with RLS
- Practice natural language queries through MCP
- Create your first migration

### For Intermediate Users

**Deepen Your Knowledge:**
1. Study `references/official-docs/row-level-security.md` for comprehensive RLS patterns
2. Review `assets/examples/rls-policies.sql` for production-ready policies
3. Implement session management using `assets/examples/session-management.ts`
4. Explore `references/database-patterns.md` for advanced designs
5. Review Quick Reference Examples #4-7 above

**Practice Projects:**
- Multi-tenant SaaS application with organizations + members + RLS
- Audit logging system with triggers
- Session-based state management with timeout logic
- Temporal data tracking (product price history)

### For Advanced Users

**Master Production Patterns:**
1. Study `references/production-patterns.md` for real-world patterns
2. Implement dual persistence with `assets/examples/memory-store.ts`
3. Design microservices architecture with database-per-service
4. Optimize performance with indexing strategies and query analysis
5. Review Quick Reference Examples #8-10 above

**Advanced Challenges:**
- Event sourcing with CQRS pattern
- Multi-region replication and consistency
- High-availability MCP deployment with load balancing
- Complex RLS policies with dynamic role assignment
- Performance optimization for million-row tables

### Navigation Tips

**Finding the Right Documentation:**
- **MCP setup issues?** → `references/mcp-setup.md`
- **Security/RLS questions?** → `references/official-docs/row-level-security.md` or `references/security.md`
- **Schema design decisions?** → `references/database-patterns.md` or `references/schema-design.md`
- **Production examples?** → `references/production-patterns.md` or `assets/examples/`
- **Migration strategies?** → `references/official-docs/migrations.md`

**Quick Lookups:**
Use Quick Reference Examples section for immediate code snippets without diving into full docs.

## Best Practices Summary

### Database Design
1. **Start Simple, Evolve Gradually** - Begin normalized, denormalize based on usage
2. **Use UUIDs for Primary Keys** - Better for distributed systems, prevents enumeration
3. **Leverage JSONB Sparingly** - Prefer typed columns for known fields
4. **Implement RLS from Day One** - Security built-in, not bolted-on
5. **Version Your Schema** - Use migrations for all changes

### MCP Usage
1. **Use Project Scoping** - Limit access to specific projects
2. **Enable Read-Only Mode** - For development/exploration
3. **Manual Tool Approval** - Keep enabled in production contexts
4. **Monitor API Usage** - Track operations through dashboard
5. **Test in Branching** - Use branches for testing schema changes

### Security
1. **Implement RLS Policies** - Never rely on application-level security alone
2. **Use Service Role Keys Carefully** - Bypass RLS only when necessary
3. **Audit All Operations** - Log administrative database operations
4. **Encrypt Sensitive Data** - Use PostgreSQL encryption for PII
5. **Regular Security Reviews** - Periodically audit RLS policies

### Performance
1. **Index Foreign Keys** - Always index columns used in joins
2. **Use EXPLAIN ANALYZE** - Understand query execution plans
3. **Avoid N+1 Queries** - Use joins or batch fetching
4. **Materialized Views** - For expensive analytical queries
5. **Connection Pooling** - Use pgBouncer for high-concurrency

## Common Workflows

### Natural Language Database Queries
```
Ask Claude: "Show me all users who signed up last month but haven't completed their profile"
```

### Schema Design with AI
```
Ask Claude: "Design a schema for a multi-tenant SaaS application with organizations, users, and billing"
```

### Migration Generation
```
Ask Claude: "Generate a migration to add a 'status' column to the posts table with an enum type"
```

### RLS Policy Creation
```
Ask Claude: "Create RLS policies so users can only see posts from organizations they're members of"
```

### Query Optimization
```
Ask Claude: "Analyze this query and suggest optimizations: SELECT * FROM orders WHERE user_id = '...' AND created_at > '2024-01-01'"
```

## Troubleshooting Quick Reference

### MCP Connection Failures
- Verify API keys are correct and not expired
- Check network connectivity to MCP endpoints
- Ensure organization permissions are properly set
- Try: `claude mcp list` to see configured servers

### RLS Policy Errors
- Test policies with different user contexts
- Use `auth.uid()` for current user checks
- Remember service role keys bypass RLS
- Check policy using EXPLAIN: `EXPLAIN SELECT * FROM table_name;`

### Migration Failures
- Always test migrations on branches first
- Check for dependency issues (foreign keys, triggers)
- Verify data compatibility before schema changes
- Use `supabase db reset` locally to test from scratch

### Performance Issues
- Review query plans with EXPLAIN ANALYZE
- Check for missing indexes on foreign keys
- Monitor connection pool utilization
- Use `pg_stat_user_indexes` to track index usage

## Version History

- **v2.0** (2025-11-01) - Enhanced with official Supabase documentation, production patterns from Twilio-Aldea, TypeScript/SQL examples, and comprehensive RLS guide
- **v1.0** - Initial skill creation with MCP setup, database patterns, schema design, security, and tools reference
