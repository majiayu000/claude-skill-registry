---
name: supabase-expert-skill
description: Complete workflow for implementing data services and database architecture after the Implementer Agent has completed use cases. Provides rigorous step-by-step processes for making data service tests pass through pure database implementations, RLS policy optimization, and schema design. Use when implementing data layer, configuring Row Level Security, designing database schemas, or optimizing query performance. Mandatory Context7 consultation for latest Supabase best practices.
---

# Supabase Expert Skill

## Purpose

This skill provides the **complete technical workflow** for implementing pure data services, designing optimized database schemas, and configuring high-performance Row Level Security policies in Supabase/PostgreSQL environments.

## When to Use

**MANDATORY** when working as Supabase Expert agent:
- Implementing data services after Implementer Agent completes use cases
- Designing database schemas with proper constraints, indexes, and relationships
- Configuring Row Level Security (RLS) policies for multi-tenant isolation
- Optimizing database queries and performance
- Creating database migrations

**Prerequisites**:
- Architect has created `entities.ts` with Zod schemas
- Test Agent has created failing service tests
- Implementer Agent has completed use cases
- You have `supabase-agent/00-request.md` from Architect

---

## 6-Phase Workflow

Your work follows **6 mandatory sequential phases**:

### Phase 0: Pre-Implementation Research ⚠️ MANDATORY

**CRITICAL**: Before ANY implementation, consult Context7 for latest patterns.

**Required Context7 queries**:
```typescript
// Query 1: RLS best practices (CRITICAL - prevents 80% of issues)
mcp__context7__get_library_docs({
  context7CompatibleLibraryID: "/supabase/supabase",
  topic: "RLS row level security policies performance joins security definer circular",
  tokens: 3000
})

// Query 2: Schema design patterns
mcp__context7__get_library_docs({
  context7CompatibleLibraryID: "/supabase/supabase",
  topic: "schema design indexes foreign keys constraints multi-tenancy organization",
  tokens: 2500
})

// Query 3: TypeScript client patterns
mcp__context7__get_library_docs({
  context7CompatibleLibraryID: "/supabase/supabase",
  topic: "TypeScript client queries CRUD error handling data transformations",
  tokens: 2000
})
```

**Document your findings** before proceeding to Phase 1.

**Full workflow**: See [references/PHASE-0-RESEARCH.md](references/PHASE-0-RESEARCH.md)

---

### Phase 1: Database Schema Design

Design optimized schemas with proper multi-tenancy, indexes, and constraints.

**Key activities**:
- Create table DDL with proper types and constraints
- Add indexes (MANDATORY on all RLS-filtered columns)
- Configure foreign keys with CASCADE rules
- Add triggers for `updated_at` auto-update
- Document schema decisions

**Full workflow**: See [references/PHASE-1-SCHEMA.md](references/PHASE-1-SCHEMA.md)

**Templates**: See [assets/schema-template.sql](assets/schema-template.sql)

---

### Phase 2: RLS Policy Implementation ⚠️ MOST CRITICAL

Configure Row Level Security policies following best practices to avoid circular dependencies and performance issues.

**⚠️ PRE-FLIGHT CHECKLIST** (verify before ANY policy):
- [ ] Context7 consultation complete (Phase 0)
- [ ] Understand circular policy anti-patterns
- [ ] Know security definer function patterns
- [ ] Schema indexes exist on RLS columns

**Critical rules**:
1. **Wrap auth.uid() in SELECT** - `(SELECT auth.uid())` enables caching
2. **Always specify TO role** - `TO authenticated` prevents wasteful evaluation
3. **Avoid joins to source table** - Prevents circular policies
4. **Use security definer functions** - For complex logic
5. **Index ALL RLS columns** - MANDATORY for performance

**Full workflow**: See [references/PHASE-2-RLS.md](references/PHASE-2-RLS.md)

**Anti-patterns guide**: See [references/RLS-ANTI-PATTERNS.md](references/RLS-ANTI-PATTERNS.md) ⚠️ READ FIRST

**Templates**: See [assets/rls-template.sql](assets/rls-template.sql)

---

### Phase 3: Data Services Implementation

Implement pure CRUD services that make tests pass WITHOUT modifying them.

**Key principles**:
- Services must be PURE: `input → database operation → output`
- NO business logic (Implementer's responsibility)
- snake_case ↔ camelCase transformations in service layer
- Proper error handling with context
- Type-safe with generated Database types

**Full workflow**: See [references/PHASE-3-SERVICES.md](references/PHASE-3-SERVICES.md)

**Templates**: See [assets/service-template.ts](assets/service-template.ts)

---

### Phase 4: TypeScript Type Generation

Generate and validate TypeScript types from database schema.

**Commands**:
```bash
# Generate types from Supabase
npx supabase gen types typescript --project-id "$PROJECT_ID" > app/src/lib/database.types.ts

# Verify compilation
cd app && npx tsc --noEmit
```

**Full workflow**: See [references/PHASE-4-TYPES.md](references/PHASE-4-TYPES.md)

---

### Phase 5: Performance Verification & Handoff

Validate implementation and prepare handoff to UI/UX Expert.

**Validation checklist**:
- [ ] All service tests pass (100%)
- [ ] RLS policies validated (no circular dependencies)
- [ ] EXPLAIN ANALYZE shows index usage (no sequential scans)
- [ ] Query performance < 50ms for simple operations
- [ ] Types generated and imported correctly
- [ ] Iteration document created

**Full workflow**: See [references/PHASE-5-VALIDATION.md](references/PHASE-5-VALIDATION.md)

---

## Critical Anti-Patterns

**RLS FAILURES** (cause 80% of production issues):

❌ **Circular policies** - Joining to source table
❌ **Missing TO clause** - Evaluates for all roles
❌ **Missing indexes** - RLS columns without indexes
❌ **Business logic in services** - Services must be pure CRUD
❌ **auth.uid() without SELECT** - Prevents caching

**Complete guide**: [references/RLS-ANTI-PATTERNS.md](references/RLS-ANTI-PATTERNS.md)

---

## CASL and RLS Coordination (Defense in Depth)

**CRITICAL**: If the feature uses CASL for client-side authorization, your RLS policies must implement THE SAME authorization logic.

### Your Responsibility

You are **NOT responsible for implementing CASL** (Implementer Agent handles that). However, you **MUST ensure RLS policies mirror CASL logic** for defense in depth.

### How CASL and RLS Work Together

**CASL (Client-Side - UX Layer)**:
- Purpose: Hide/show UI elements, prevent unnecessary API calls
- Implementation: Implementer Agent implements `defineAbilitiesFor()`
- Security Level: NOT trusted (client can manipulate)
- Performance: Prevents unnecessary API calls

**RLS (Server-Side - Security Layer)**:
- Purpose: Actual security enforcement at database level
- Implementation: YOU implement PostgreSQL policies
- Security Level: TRUSTED (cannot be bypassed)
- Performance: Executes on every query

### Coordination Requirements

**CRITICAL RULES**:
- ✅ Your RLS policies MUST implement the SAME logic as CASL
- ✅ Compare RLS SQL to `defineAbilitiesFor()` implementation before completing
- ✅ Test that bypassing CASL cannot bypass RLS (defense in depth)
- ❌ NEVER assume CASL protects data (it only improves UX)
- ❌ NEVER implement looser RLS than CASL (security gap)
- ❌ NEVER implement stricter RLS than CASL without coordinating (UX breaks)

### Example Alignment

**CASL Logic (from Implementer Agent)**:
```typescript
// defineAbilitiesFor() in features/{feature}/abilities/defineAbility.ts
if (user.id === workspace.owner_id) {
  can('delete', 'Board');
}

permissions.forEach((perm) => {
  if (perm.full_name === 'boards.delete') {
    can('delete', 'Board');
  }
});
```

**RLS Policy (YOUR implementation)**:
```sql
-- mirrors the same Owner + Permission logic
CREATE POLICY "Users can delete boards"
  ON boards
  FOR DELETE
  USING (
    -- Owner can delete
    auth.uid() = (
      SELECT owner_id FROM workspaces
      WHERE id = boards.workspace_id
    )
    OR
    -- User with boards.delete permission can delete
    EXISTS (
      SELECT 1 FROM permissions p
      JOIN workspace_roles wr ON wr.role_id = p.role_id
      WHERE wr.user_id = auth.uid()
        AND wr.workspace_id = boards.workspace_id
        AND p.full_name = 'boards.delete'
    )
  );
```

### Validation Checklist

Before marking your iteration complete:

- [ ] ✅ Read `features/{feature}/abilities/defineAbility.ts` (if it exists)
- [ ] ✅ Compare CASL Owner bypass logic to RLS Owner checks
- [ ] ✅ Compare CASL Super Admin restrictions to RLS restrictions
- [ ] ✅ Compare CASL permission mapping to RLS permission checks
- [ ] ✅ Verify conditional permissions match in both layers
- [ ] ✅ Test that CASL saying "YES" → RLS also allows (UX works)
- [ ] ✅ Test that CASL saying "NO" → API call fails at RLS (security works)

### Communication with Implementer

**If you find misalignment**:
1. Document the discrepancy in your iteration document
2. Ask Architect to clarify authorization requirements
3. Coordinate with Implementer to align both layers
4. DO NOT proceed with conflicting logic

**Example discrepancy**:
```
ISSUE: CASL allows Super Admin to delete Organizations,
but PRD says Super Admin should NOT be able to delete Organizations.

ACTION: Asked Architect to clarify. Waiting for confirmation before implementing RLS.
```

---

## Reference Files (Load on Demand)

**Core Workflow** (read sequentially):
- [PHASE-0-RESEARCH.md](references/PHASE-0-RESEARCH.md) - Mandatory Context7 research
- [PHASE-1-SCHEMA.md](references/PHASE-1-SCHEMA.md) - Database schema design
- [PHASE-2-RLS.md](references/PHASE-2-RLS.md) - RLS policies ⚠️ CRITICAL
- [PHASE-3-SERVICES.md](references/PHASE-3-SERVICES.md) - Pure data services
- [PHASE-4-TYPES.md](references/PHASE-4-TYPES.md) - Type generation
- [PHASE-5-VALIDATION.md](references/PHASE-5-VALIDATION.md) - Testing & handoff

**Critical References** (load when implementing RLS):
- [RLS-ANTI-PATTERNS.md](references/RLS-ANTI-PATTERNS.md) - What NOT to do
- [RLS-BEST-PRACTICES.md](references/RLS-BEST-PRACTICES.md) - Proven patterns

**Supporting**:
- [TEMPLATES.md](references/TEMPLATES.md) - Complete code templates
- [ITERATION-TEMPLATE.md](references/ITERATION-TEMPLATE.md) - Iteration documentation
- [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) - Common issues

---

## Success Criteria

Your iteration is complete when:

✅ All service tests pass (100% - no test modifications)
✅ RLS policies validated (no circular dependencies, performance verified)
✅ Schema optimized (indexes on RLS columns, proper constraints)
✅ Services are pure (no business logic, only CRUD)
✅ Types generated (database.types.ts up to date)
✅ Performance verified (EXPLAIN ANALYZE shows index usage)

---

## Quick Reference

**Mandatory first step**: Phase 0 - Context7 consultation
**Most critical phase**: Phase 2 - RLS implementation
**Most common mistake**: Circular RLS policies (joining to source table)
**Performance killer**: Missing indexes on RLS-filtered columns
**Architecture violation**: Business logic in data services

---

**Remember**: You work in isolation. Tests are immutable. Make them pass through pure database implementations. Architect reviews everything before approval.
