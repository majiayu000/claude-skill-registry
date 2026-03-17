---
name: architect-agent-skill
description: Technical workflow for architect-agent - PRD creation with mandatory database context, entity design with Zod, iteration review, and agent coordination in the iterative v2.0 system
---

# Architect Agent Skill

Complete technical workflow and best practices for the Chief Architect role.

---

## 6-PHASE WORKFLOW

### PHASE 0: Pre-Discovery Research (MANDATORY)

**⚠️ CRITICAL**: Query existing database context BEFORE asking user any questions.

**Why**: Understanding existing patterns allows you to ask INFORMED questions instead of generic ones.

#### Supabase MCP Research (REQUIRED)

```typescript
// 1. List all existing tables
mcp__supabase__list_tables({ schemas: ['public'] })

// 2. Check schema of related tables
mcp__supabase__execute_sql({
  query: `
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'existing_table'
    ORDER BY ordinal_position;
  `
})

// 3. Review foreign key relationships
mcp__supabase__execute_sql({
  query: `
    SELECT
      tc.table_name,
      kcu.column_name,
      ccu.table_name AS foreign_table_name
    FROM information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY'
      AND tc.table_schema = 'public';
  `
})

// 4. Review existing RLS policies
mcp__supabase__execute_sql({
  query: `SELECT * FROM pg_policies WHERE schemaname = 'public';`
})
```

**What to identify**:
- ✅ Multi-tenancy pattern (organization_id present?)
- ✅ Naming conventions (snake_case in DB → camelCase in TS)
- ✅ RLS patterns (auth.uid() usage)
- ✅ Foreign key patterns (ON DELETE CASCADE?)
- ✅ Similar features (avoid duplication)

**Output**: Notes on existing patterns to reference in questions.

---

### PHASE 1: Clarification Dialogue

**Objective**: Gather complete, unambiguous requirements using context from Phase 0.

#### Question Categories

**🔒 PERMISSIONS & AUTHORIZATION**
- Who can perform this action? (roles, user types)
- Organization-level or user-level access?
- Should RLS follow existing patterns?

**🔐 AUTHORIZATION IMPLEMENTATION** (If feature requires permissions)
- Does this feature require permission checks? (if yes, CASL needed)
- What actions need authorization? (create, read, update, delete, custom actions)
- What resources are being protected? (boards, cards, comments, etc.)
- Are there conditional permissions? (e.g., "can edit IF owner OR has editor role")
- Should Owner/Super Admin have special rules?
- Field-level permissions needed? (e.g., hide sensitive fields for certain roles)

**⚙️ FUNCTIONAL REQUIREMENTS**
- All CRUD operations needed?
- Edge cases to handle?
- Relationships with existing entities?

**📊 DATA REQUIREMENTS**
- Required vs optional fields?
- Validation rules (min/max, formats, regex)?
- Follow existing naming conventions?

**🔔 SIDE EFFECTS & INTEGRATION**
- Trigger notifications?
- Affect other features?
- External API integrations?

**⚡ PERFORMANCE & REAL-TIME**
- Real-time requirements?
- Expected data volume? (pagination?)
- Caching considerations?

#### Example Enhanced Question Flow

❌ **Without Phase 0 context** (Weak):
```
User: "Add comments to tasks"
You: "Who can add comments?"
```

✅ **With Phase 0 context** (Strong):
```
User: "Add comments to tasks"
You: "I reviewed the existing database. I found:
- tasks table uses organization_id for multi-tenancy
- RLS policies follow auth.uid() = user_id pattern
- Foreign keys use ON DELETE CASCADE
- Timestamps use TIMESTAMPTZ with DEFAULT NOW()

For comments, should we:
1. Follow the same organization_id isolation pattern?
2. Use CASCADE deletion when task is deleted?
3. Who can comment: task owner only, or all org members?
4. Can comments be edited/deleted? By whom?"
```

**Deliverable**: Complete requirement notes with all ambiguities resolved.

**Reference**: See `references/prd-template-guide.md` for section requirements.

---

### PHASE 2: Context7 Research (MANDATORY)

**⚠️ CRITICAL**: Consult latest best practices BEFORE designing entities or writing PRD.

#### Required Queries

**For Entity Design** (ALWAYS):
```typescript
// Query Zod best practices
mcp__context7__resolve_library_id({ libraryName: "zod" })
mcp__context7__get_library_docs({
  context7CompatibleLibraryID: "/colinhacks/zod",
  topic: "schema validation refinements transforms",
  tokens: 3000
})
```

**For API Specifications** (if feature has API):
```typescript
// Query Next.js App Router patterns
mcp__context7__resolve_library_id({ libraryName: "next.js" })
mcp__context7__get_library_docs({
  context7CompatibleLibraryID: "/vercel/next.js",
  topic: "app router route handlers request response",
  tokens: 2500
})
```

**For RLS Policies** (if feature has database):
```typescript
// Query Supabase RLS best practices
mcp__context7__resolve_library_id({ libraryName: "supabase" })
mcp__context7__get_library_docs({
  context7CompatibleLibraryID: "/supabase/supabase",
  topic: "row level security policies multi-tenant",
  tokens: 3000
})
```

**What to verify**:
- ✅ Latest Zod patterns (might be newer than training data)
- ✅ Current Next.js best practices
- ✅ Supabase RLS recommendations
- ✅ Any breaking changes or deprecations

**Deliverable**: Notes on patterns to use in PRD and entities.

**Reference**: See `references/entity-design-patterns.md` and `references/supabase-rls-patterns.md`.

---

### PHASE 3: Generate Master PRD

**Objective**: Create comprehensive, unambiguous PRD with 14 required sections.

#### PRD Structure (MANDATORY)

Copy template:
```bash
cp PRDs/_templates/00-master-prd-template.md PRDs/{domain}/{number}-{feature}/architect/00-master-prd.md
```

#### 14 Required Sections

1. **Executive Summary** (problem, solution, impact)
2. **Problem Statement** (current state, desired state, pain points)
3. **Goals and Success Metrics**
4. **User Stories** (with acceptance criteria)
5. **Functional Requirements** (CRUD operations detailed)
6. **Data Contracts** (Zod schemas + TypeScript types) ⭐ CRITICAL
7. **API Specifications** (all endpoints with request/response)
8. **Technical Architecture** (DB schema + RLS policies)
9. **Testing Strategy** (coverage targets by layer)
10. **Security Considerations** (auth, authorization, validation)
11. **Acceptance Criteria** (must have, should have, could have)
12. **Out of Scope** (explicitly excluded)
13. **Dependencies & Prerequisites**
14. **Timeline Estimate** (per agent phase)

#### Section 6: Data Contracts (Most Critical)

**Template**:
```typescript
import { z } from 'zod';

// Main entity schema
export const EntitySchema = z.object({
  id: z.string().uuid(),
  field1: z.string().min(1).max(200),
  field2: z.string().optional(),
  field3: z.enum(['value1', 'value2']),
  userId: z.string().uuid(),
  organizationId: z.string().uuid(),
  createdAt: z.coerce.date(),
  updatedAt: z.coerce.date(),
});

// Create schema (omit auto-generated)
export const EntityCreateSchema = EntitySchema.omit({
  id: true,
  createdAt: true,
  updatedAt: true,
});

// Update schema (partial)
export const EntityUpdateSchema = EntitySchema
  .omit({
    id: true,
    userId: true,
    organizationId: true,
    createdAt: true,
    updatedAt: true,
  })
  .partial();

// TypeScript types
export type Entity = z.infer<typeof EntitySchema>;
export type EntityCreate = z.infer<typeof EntityCreateSchema>;
export type EntityUpdate = z.infer<typeof EntityUpdateSchema>;
```

#### CASL Types (IF Authorization Required)

**When to include**: If the feature requires permission checks (e.g., "only owners can delete", "editors can modify", etc.)

**Add to entities.ts**:
```typescript
// ===== CASL Integration =====
import { MongoAbility } from '@casl/ability';

// Define subjects (resources being protected)
// IMPORTANT: Use PascalCase, singular form (boards → Board)
export type Subjects =
  | 'Board'    // Maps to database table 'boards'
  | 'Card'     // Maps to database table 'cards'
  | 'Comment'  // Maps to database table 'comments'
  | 'all';     // Special: represents all resources

// Define actions (what users can do)
export type Actions =
  | 'create'
  | 'read'
  | 'update'
  | 'delete'
  | 'move'     // Custom action example
  | 'archive'  // Custom action example
  | 'manage';  // Special: superuser action (all actions)

// Export ability type
export type AppAbility = MongoAbility<[Actions, Subjects]>;

// Define ability builder signature (Implementer will implement this)
export interface DefineAbilityInput {
  user: User;
  workspace: Workspace;
  permissions: Permission[];  // From RBAC system
}

export type DefineAbilityFunction = (input: DefineAbilityInput) => AppAbility;
```

**Critical CASL Design Rules**:
- ✅ Subjects are PascalCase, singular (`Board` not `boards`)
- ✅ Actions are lowercase verbs (`delete` not `Delete`)
- ✅ Include `'all'` subject for Owner/Super Admin bypass
- ✅ Include `'manage'` action for full access
- ✅ Custom actions OK (e.g., `'move'` for Kanban cards)
- ❌ DON'T implement the ability builder here (Implementer's job)
- ❌ DON'T add business logic to types (pure contracts only)

**Subject Mapping Convention**:
```
Database Table → CASL Subject
boards         → 'Board'
cards          → 'Card'
comments       → 'Comment'
custom_fields  → 'CustomField'
```

#### Section 8: RLS Policies

**Template**:
```sql
-- Enable RLS
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- Users can only see records from their organization
CREATE POLICY "Users can view own organization entities"
  ON table_name
  FOR SELECT
  USING (
    organization_id IN (
      SELECT organization_id
      FROM user_organizations
      WHERE user_id = auth.uid()
    )
  );

-- Users can create records for their organization
CREATE POLICY "Users can create entities for own organization"
  ON table_name
  FOR INSERT
  WITH CHECK (
    organization_id IN (
      SELECT organization_id
      FROM user_organizations
      WHERE user_id = auth.uid()
    )
  );

-- Users can update own records
CREATE POLICY "Users can update own entities"
  ON table_name
  FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

-- Users can delete own records
CREATE POLICY "Users can delete own entities"
  ON table_name
  FOR DELETE
  USING (user_id = auth.uid());
```

**Validation checklist**:
- [ ] All 14 sections completed
- [ ] Zod schemas defined with proper validations
- [ ] API specs include all CRUD operations
- [ ] Database schema includes RLS policies
- [ ] Acceptance criteria are testable
- [ ] Out of scope items documented

**Deliverable**: Complete `architect/00-master-prd.md`.

**Reference**: See `references/prd-template-guide.md` for detailed section breakdown.

---

### PHASE 4: Create Directory Structure & Entities

#### 4.1 Create Feature Directory

```bash
# Main feature directory
mkdir -p app/src/features/{feature-name}

# Subdirectories
mkdir -p app/src/features/{feature-name}/components
mkdir -p app/src/features/{feature-name}/use-cases
mkdir -p app/src/features/{feature-name}/services

# Create entities.ts (YOU implement this)
touch app/src/features/{feature-name}/entities.ts

# Create placeholder files for other agents
touch app/src/features/{feature-name}/use-cases/create{Entity}.test.ts
touch app/src/features/{feature-name}/use-cases/create{Entity}.ts
touch app/src/features/{feature-name}/services/{feature}.service.ts
touch app/src/features/{feature-name}/components/{Entity}Form.tsx

# API routes
mkdir -p app/src/app/api/{feature}
touch app/src/app/api/{feature}/route.ts
```

#### 4.2 Implement entities.ts (YOUR ONLY CODE)

**CRITICAL**: This is the ONLY functional code you write.

**Template** (full version in `assets/templates/entities-template.ts`):
```typescript
/**
 * {Feature Name} Entities
 *
 * Pure data contracts defined with Zod schemas.
 * NO business logic, NO external dependencies (except Zod).
 */

import { z } from 'zod';

// ============================================================================
// MAIN ENTITY SCHEMA
// ============================================================================

export const EntitySchema = z.object({
  id: z.string().uuid(),
  // ... fields from PRD Section 6
  createdAt: z.coerce.date(),
  updatedAt: z.coerce.date(),
});

// ============================================================================
// DERIVED SCHEMAS
// ============================================================================

export const EntityCreateSchema = EntitySchema.omit({
  id: true,
  createdAt: true,
  updatedAt: true,
});

export const EntityUpdateSchema = EntitySchema
  .omit({
    id: true,
    userId: true,
    organizationId: true,
    createdAt: true,
    updatedAt: true,
  })
  .partial();

// ============================================================================
// TYPESCRIPT TYPES
// ============================================================================

export type Entity = z.infer<typeof EntitySchema>;
export type EntityCreate = z.infer<typeof EntityCreateSchema>;
export type EntityUpdate = z.infer<typeof EntityUpdateSchema>;
```

**Validation**:
- [ ] entities.ts compiles without errors
- [ ] All schemas from PRD implemented
- [ ] TypeScript types exported
- [ ] JSDoc comments added
- [ ] NO business logic
- [ ] Only Zod import (no other dependencies)

**Reference**: See `references/entity-design-patterns.md` for advanced patterns.

---

### PHASE 5: Write Agent Request Documents

**Objective**: Translate PRD master into agent-specific, actionable requirements.

#### For Each Agent Phase

**Test Agent**:
```bash
cp PRDs/_templates/agent-request-template.md PRDs/{domain}/{feature}/test-agent/00-request.md
```

**Content to include**:
- **Context**: Why Test Agent is working on this
- **Objectives**: Create comprehensive failing test suite for ALL layers
- **Detailed Requirements**:
  - Entity validation tests (Zod schemas)
  - Use case tests (business logic with mocked services)
  - Service tests (data layer with mocked Supabase)
  - API tests (route handlers)
  - E2E tests (user flows with Playwright)
- **Technical Specifications**:
  - Mock configurations (Supabase client, etc.)
  - Test fixture factories
  - Expected function signatures
- **Expected Deliverables**:
  - Exact test files to create
  - Coverage target (>90%)
  - Iteration document structure
- **Limitations**:
  - NEVER implement functional logic
  - NEVER modify entities.ts
  - Tests must fail with "function not defined"

**Implementer**:
```bash
cp PRDs/_templates/agent-request-template.md PRDs/{domain}/{feature}/implementer/00-request.md
```

**Content to include**:
- Context, objectives, detailed requirements (use case implementation)
- Service interfaces needed (from PRD)
- Test compliance requirements
- Limitations (no data services, no entity modification)

**Supabase Agent**:
```bash
cp PRDs/_templates/agent-request-template.md PRDs/{domain}/{feature}/supabase-agent/00-request.md
```

**Content to include**:
- Context, objectives, detailed requirements (data services + DB schema)
- RLS policies from PRD
- Migration scripts needed
- Limitations (no business logic in services)

**UI/UX Expert**:
```bash
cp PRDs/_templates/agent-request-template.md PRDs/{domain}/{feature}/ui-ux-expert/00-request.md
```

**Content to include**:
- Context, objectives, detailed requirements (React components)
- E2E test requirements
- Accessibility requirements (WCAG 2.1 AA)
- Limitations (no business logic, no direct service calls)

**Deliverable**: `00-request.md` for each agent.

**Reference**: See `assets/examples/` for complete request examples.

---

### PHASE 6: Review Iterations & Approve/Reject

**Objective**: Act as quality gate, reviewing EVERY iteration before allowing progression.

#### When Agent Notifies Completion

**Step 1: Read their iteration**
```bash
# Agent creates:
PRDs/{domain}/{feature}/{agent}/01-iteration.md
```

**Step 2: Verify against requirements**

Load their `00-request.md` and check:
- [ ] All objectives from request completed?
- [ ] All deliverables present?
- [ ] Quality meets standards?
- [ ] No architectural violations?

**Step 3: Coordinate with Usuario**

Present iteration to user for business review:
```
"Test Agent has completed iteration 01. I've reviewed it against technical requirements.

**Summary**: [Brief overview of what was delivered]

**My Assessment**:
- ✅ All technical objectives met
- ✅ No architectural violations
- ⚠️ [Any concerns if present]

Please review for business approval before I allow progression to Implementer."
```

**Step 4: Make Decision**

#### ✅ IF APPROVED

Document in iteration file:
```markdown
## Review Status

**Submitted for Review**: YYYY-MM-DD HH:MM

### Architect Review
**Date**: YYYY-MM-DD HH:MM
**Status**: Approved ✅
**Feedback**:
- All requirements met
- Quality is acceptable
- Ready for next phase

### User Review
**Date**: YYYY-MM-DD HH:MM
**Status**: Approved ✅
**Feedback**:
- Business requirements satisfied
```

**Then**:
1. Update `_status.md`
2. Prepare `00-request.md` for NEXT agent
3. Notify user: "Test Agent approved, moving to Implementer"

#### ❌ IF REJECTED

Document in iteration file with SPECIFIC, ACTIONABLE feedback:
```markdown
## Review Status

**Submitted for Review**: YYYY-MM-DD HH:MM

### Architect Review
**Date**: YYYY-MM-DD HH:MM
**Status**: Rejected ❌
**Feedback**:

**Issues Found**:

1. **Missing E2E Tests for Delete Flow** (SEVERITY: HIGH)
   - **Location**: No file created for delete E2E test
   - **Problem**: 00-request.md required E2E tests for ALL CRUD operations, but delete flow is missing
   - **Required Fix**: Create `tests/e2e/comments-delete.spec.ts` with:
     - Navigate to task with comment
     - Click delete button
     - Confirm deletion
     - Verify comment removed from UI
     - Verify API DELETE call succeeded
   - **Example**: See `tests/e2e/comments-create.spec.ts` for structure

2. **Incomplete Mock Configuration** (SEVERITY: CRITICAL)
   - **Location**: `use-cases/createComment.test.ts:15-20`
   - **Problem**: Supabase client mock doesn't include `from().select()` chain
   - **Required Fix**: Update mock to:
     ```typescript
     vi.mock('@/lib/supabase', () => ({
       createClient: vi.fn(() => ({
         from: vi.fn(() => ({
           insert: vi.fn(),
           select: vi.fn(),  // ← ADD THIS
         })),
       })),
     }));
     ```

**Action Required**:
Please create iteration 02 addressing these 2 issues.

### User Review
**Date**: Pending
**Status**: Waiting for corrections
```

**Then**:
1. Agent creates `02-iteration.md` addressing issues
2. Review again when notified
3. Repeat until approved

**Reference**: See `references/iteration-review-checklist.md` for comprehensive criteria.

---

## OPTIONAL: Enable Parallelism via Handoffs

**When to use**: Interfaces are stable, want to accelerate delivery.

**Create handoff document**:
```bash
cp PRDs/_templates/agent-handoff-template.md PRDs/{domain}/{feature}/{current-agent}/handoff-001.md
```

**What to include**:
- **Stable interfaces** (function signatures that won't change)
- **Data contracts** (input/output schemas)
- **Service interfaces** (methods next agent will call)
- **Constraints** (what next agent can/cannot assume)
- **Coordination notes** (how to handle if interfaces change)

**Example scenario**:
```
Test Agent working on iteration 02 (corrections)
          ↓
   Interfaces are stable
          ↓
You create test-agent/handoff-001.md
          ↓
Implementer can start using handoff
          ↓
Both work in parallel
```

**Reference**: See `references/handoff-coordination.md` for detailed guide.

---

## PRE-HANDOFF VALIDATION CHECKLIST

Before handing off to first agent (Test Agent), verify:

### Context Research Completed
- [ ] Supabase MCP used to query existing schema
- [ ] Tables reviewed for similar features
- [ ] Patterns identified (multi-tenancy, naming)
- [ ] RLS policies examined
- [ ] Context7 consulted for latest patterns

### PRD Completeness
- [ ] All 14 sections completed
- [ ] Zod schemas defined with validations
- [ ] API specs include all CRUD operations
- [ ] Database schema includes RLS policies
- [ ] Acceptance criteria testable
- [ ] Out of scope documented

### Directory Structure
- [ ] Feature directory follows canonical structure
- [ ] All subdirectories created
- [ ] Placeholder files for other agents
- [ ] API routes created

### Entities Implementation
- [ ] entities.ts compiles without errors
- [ ] All schemas from PRD implemented
- [ ] TypeScript types exported
- [ ] JSDoc comments added
- [ ] NO business logic
- [ ] Only Zod import

### Consistency Checks
- [ ] Feature name consistent (PRD, directories, files)
- [ ] Entity names consistent (PascalCase in code, kebab-case in URLs)
- [ ] Schema fields match DB columns (camelCase ↔ snake_case)
- [ ] No circular dependencies

---

## HANDOFF PROTOCOL

```bash
# After completing all phases, execute:
/agent-handoff {feature-path} architect completed

# Then provide explicit handoff message
```

**Handoff message template**:
```markdown
## 🎯 HANDOFF TO TEST AGENT

**PRD Status**: ✅ Complete
**Feature**: `{feature-name}`
**Location**: `app/src/features/{feature-name}/`

### What I've Delivered

1. **Complete PRD**: `PRDs/{domain}/{number}-{feature}/architect/00-master-prd.md`
2. **Directory Structure**: All folders and placeholder files
3. **Entities**: `entities.ts` implemented with Zod schemas
4. **Request Document**: `test-agent/00-request.md` with your specific requirements

### What You Must Do

1. **Read**: `test-agent/00-request.md` for your detailed requirements
2. **Create Tests** for ALL layers (entities, use cases, services, API, E2E)
3. **Verify Tests FAIL**: All tests must fail with "function not defined"
4. **Document**: Create `test-agent/01-iteration.md` with your work

### Critical Requirements

- ❌ DO NOT implement any functional code
- ❌ DO NOT modify entities.ts
- ✅ MUST create comprehensive test coverage (>90%)
- ✅ Tests become IMMUTABLE SPECIFICATION

Ready to proceed?
```

---

## COMMON MISTAKES TO AVOID

**❌ Creating incomplete PRDs**
```markdown
"Add comments feature" [END OF DOCUMENT]
```

**✅ Complete 14-section PRD**
```markdown
# PRD: Task Comments System

## 1. Executive Summary
...
[Complete 14 sections]
```

**❌ Assuming requirements**
```
User: "Add notifications"
You: [Creates PRD immediately]
```

**✅ Clarify first**
```
User: "Add notifications"
You: "I reviewed the database. Let me clarify:
1. What events trigger notifications?
2. Delivery channels (in-app, email, push)?
..."
```

**❌ Implementing business logic**
```typescript
// entities.ts
export const validateComment = (comment: Comment) => {
  if (comment.content.length < 5) throw new Error('Too short');
}
```

**✅ Pure Zod schema only**
```typescript
// entities.ts
export const CommentSchema = z.object({
  content: z.string().min(5, 'Minimum 5 characters'),
});
```

**❌ Vague rejection feedback**
```
"Tests are incomplete. Please fix."
```

**✅ Specific, actionable feedback**
```
**Missing E2E Tests for Delete Flow** (SEVERITY: HIGH)
- **Location**: No file for delete E2E test
- **Problem**: 00-request.md required E2E for ALL CRUD
- **Required Fix**: Create tests/e2e/comments-delete.spec.ts with...
- **Example**: See tests/e2e/comments-create.spec.ts
```

---

## REFERENCES

Detailed technical guides (load on demand):

- **references/prd-template-guide.md** - Complete 14-section breakdown
- **references/entity-design-patterns.md** - Zod schema patterns
- **references/iteration-review-checklist.md** - Review criteria
- **references/supabase-rls-patterns.md** - RLS policy patterns
- **references/handoff-coordination.md** - Parallelism guide

---

**Last Updated**: 2025-10-24
