---
name: supabase-to-convex-migration
description: Migrate ANY Supabase project to Convex with exact feature/design/architecture parity. Complete database schema translation, function migration, authentication, real-time queries, RLS replacement, and storage migration. Use when converting Supabase backends to Convex or planning Supabase-to-Convex migrations.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, WebSearch, WebFetch
---

# Supabase to Convex Migration Skill

## Overview

This skill provides systematic, comprehensive guidance for migrating any Supabase project to Convex with **exact feature parity**. Every Supabase capability is mapped to its Convex equivalent.

**Core Promise:** After migration, your application will have identical functionality, improved real-time performance, and type-safe backend operations.

## When to Use This Skill

Use this skill when:
- Planning or executing a Supabase → Convex migration
- Need to translate PostgreSQL schemas to Convex tables
- Converting Supabase Edge Functions to Convex functions
- Replacing RLS policies with Convex permission checks
- Migrating Supabase Auth to Convex Auth
- Setting up real-time subscriptions (Convex native)
- Converting Supabase Storage to Convex file storage
- Validating migration completeness

## Feature Parity Matrix

| Supabase Feature | Convex Equivalent | Migration Complexity |
|------------------|-------------------|---------------------|
| PostgreSQL Tables | Convex Tables (schema.ts) | Medium |
| Row Level Security (RLS) | Server-side auth checks | High |
| Edge Functions | Convex Functions (query/mutation/action) | Medium |
| Realtime Subscriptions | Native reactive queries | Low |
| Auth (email/OAuth) | Convex Auth / custom auth | Medium |
| Storage (buckets) | Convex File Storage | Medium |
| Database Functions | Convex internal functions | Medium |
| Triggers | Scheduled functions / hooks | Medium |
| Foreign Keys | Document references + indexes | Low |
| Views | Query functions | Low |
| RPC endpoints | Public mutations/actions | Low |

## Migration Phases Overview

### Phase 1: Audit & Discovery
- Extract complete Supabase schema
- Document all RLS policies
- List Edge Functions and triggers
- Map auth flows
- Identify storage usage

### Phase 2: Schema Translation
- Convert PostgreSQL types to Convex validators
- Design table relationships
- Create indexes for query patterns
- Plan data transformation

### Phase 3: Function Migration
- Convert Edge Functions to Convex functions
- Translate SQL queries to Convex queries
- Implement RLS as permission checks
- Set up scheduled functions

### Phase 4: Authentication Migration
- Configure Convex Auth
- Migrate user data
- Update client auth flow
- Test OAuth providers

### Phase 5: Data Migration
- Export Supabase data
- Transform to Convex format
- Bulk import with validation
- Verify data integrity

### Phase 6: Storage Migration
- Export files from Supabase Storage
- Upload to Convex File Storage
- Update file references
- Verify access controls

### Phase 7: Client Integration
- Update Supabase client calls to Convex
- Implement reactive queries
- Test real-time updates
- Update error handling

### Phase 8: Testing & Deployment
- Comprehensive test coverage
- Performance benchmarks
- Staged rollout
- Monitoring setup

## Quick Reference: Type Mappings

```typescript
// Supabase PostgreSQL → Convex Validators
text/varchar       → v.string()
integer/bigint     → v.number() or v.int64()
boolean            → v.boolean()
uuid               → v.id("tableName") or v.string()
timestamp/timestamptz → v.number() (Unix ms)
jsonb              → v.any() or v.object({...})
array              → v.array(v.type())
numeric/decimal    → v.number() or v.float64()
bytea              → v.bytes()
```

## Detailed Guidance

See [PHASES.md](PHASES.md) for step-by-step phase execution
See [CHECKLISTS.md](CHECKLISTS.md) for comprehensive migration checklists
See [REFERENCE.md](REFERENCE.md) for code examples and conversion patterns

## Critical Success Factors

1. **Complete Schema Audit** - Miss nothing from Supabase
2. **RLS Parity** - Every policy must have Convex equivalent
3. **Data Integrity** - Zero data loss, verified checksums
4. **Auth Continuity** - Users seamlessly authenticate
5. **Real-time Parity** - All subscriptions working
6. **Performance Baseline** - Meet or exceed Supabase latency

## Execution Command

To start migration, use:
```
/migrate-to-convex [phase-name]
```

Or ask: "Help me migrate my Supabase project to Convex"
