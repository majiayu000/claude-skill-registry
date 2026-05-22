---
name: rbac-permissions-architect
description: Use this skill when architecting new features within the RBAC modular permissions system. Guides architects through workspace design, feature definition, permission mapping, and role hierarchy. Critical for understanding Owner/Super Admin special roles, feature independence, and multi-tenant context isolation. Invoke when creating PRDs that involve permissions, workspaces, features, or role-based access control.
---

# RBAC Permissions Architect

## Purpose

This skill enables the Architect Agent to design features that correctly integrate with the project's **RBAC modular permissions system** defined in `concepto-base.md`. It provides the necessary understanding of workspaces, features, permissions, and special roles to create compliant PRDs and entity designs.

## When to Use This Skill

Use this skill when:
- Creating a new feature that involves permissions or access control
- Designing features that operate within workspaces (organizations or projects)
- Defining resources and permissions for a new feature module
- Creating entities that need to respect workspace boundaries
- Architecting features that interact with Owner/Super Admin roles
- Any PRD that mentions: permissions, roles, access, workspaces, features, RLS

## Core Understanding Required

Before architecting any feature, understand these **immutable principles**:

### 1. The Three Pillars (Independent but Interconnected)

```
WORKSPACES (Containers)
    ↓
FEATURES (Modules)
    ↓
RBAC (Access Control)
```

- **Workspaces**: Organizations (root) and Projects (children)
- **Features**: Activatable modules with their own resources/permissions
- **RBAC**: Granular permissions grouped into roles

### 2. Critical Rules

- **NO inheritance**: Features and permissions DO NOT inherit between workspaces
- **Contextual permissions**: Permissions only apply in the workspace where assigned
- **Special roles**: Owner and Super Admin transcend normal permission rules
- **Mandatory feature**: `permissions-management` is always active
- **Independence**: Each workspace activates features explicitly

## Architect Workflow for RBAC-Aware Features

### Phase 1: Feature Scope Definition

**Questions to answer:**

1. **Workspace scope**: Does this feature apply to organizations, projects, or both?
2. **Resource identification**: What entities will users interact with?
3. **Permission granularity**: What actions can users perform on each resource?
4. **Role requirements**: Are there default roles needed for this feature?
5. **Special role interaction**: How do Owner/Super Admin interact with this feature?

**Reference files to consult:**
- **Basic concepts**: [CONCEPTS.md](references/CONCEPTS.md) - Workspace, Feature, Resource, Permission, Role definitions
- **Workspace architecture**: [WORKSPACES.md](references/WORKSPACES.md) - Organization vs Project behavior

### Phase 2: Permission Matrix Design

**Steps:**

1. **List all resources** in your feature (e.g., `boards`, `cards`, `comments`)
2. **Define CRUD+ actions** for each resource (create, read, update, delete, custom actions)
3. **Map to permission format**: `{resource}.{action}` (e.g., `boards.create`, `cards.move`)
4. **Consider visibility**: Which permission grants UI visibility? (usually `.read`)
5. **Document restrictions**: What can Owner/Super Admin do that normal users cannot?

**Example permission matrix:**

```
Feature: kanban

Resources:
├─ boards
├─ cards
└─ card_comments

Permissions:
├─ boards.create
├─ boards.read      ← Grants visibility of Kanban in UI
├─ boards.update
├─ boards.delete
├─ cards.create
├─ cards.read
├─ cards.update
├─ cards.delete
├─ cards.move       ← Custom action
├─ card_comments.create
└─ card_comments.delete
```

**Reference file to consult:**
- **Permission system**: [PERMISSIONS.md](references/PERMISSIONS.md) - Granular permissions, roles, verification flows

### Phase 2.5: CASL Ability Definition

**⚡ NEW: Authorization Layer Integration**

After defining the permission matrix, specify how CASL (the project's authorization library) will implement these permissions.

**Questions to answer:**

1. **Subject mapping**: What are the CASL subjects for each resource?
2. **Action alignment**: Do CASL actions match permission actions perfectly?
3. **Conditional rules**: Are there context-dependent rules (e.g., "own resources only")?
4. **Type safety**: How do we enforce TypeScript types for subjects and actions?

**CASL Subjects (PascalCase, Singular):**

Map each database resource to a CASL subject:

```typescript
// Database resources → CASL subjects
'boards'        → 'Board'
'cards'         → 'Card'
'card_comments' → 'Comment'
```

**Rules:**
- Use **PascalCase** for subjects (CASL convention)
- Use **singular** form (Board, not Boards)
- One resource = one subject (1:1 mapping)

**CASL Actions:**

Standard actions align with permissions:
```typescript
'create' → boards.create
'read'   → boards.read
'update' → boards.update
'delete' → boards.delete
```

Custom actions:
```typescript
'move'   → cards.move
'assign' → cards.assign
```

**Ability Builder Template:**

Include this in your PRD's `entities.ts`:

```typescript
// ===== CASL Integration =====
import { AbilityBuilder, createMongoAbility, MongoAbility } from '@casl/ability';

// Define CASL types
type Subjects = 'Board' | 'Card' | 'Comment' | 'all';
type Actions = 'create' | 'read' | 'update' | 'delete' | 'move' | 'manage';
export type AppAbility = MongoAbility<[Actions, Subjects]>;

/**
 * Build CASL ability from user permissions
 *
 * @param user - Current user
 * @param workspace - Current workspace context
 * @param permissions - User's permissions in this workspace
 */
export function defineAbilitiesFor(
  user: User,
  workspace: Workspace,
  permissions: Permission[]
): AppAbility {
  const { can, cannot, build } = new AbilityBuilder<AppAbility>(createMongoAbility);

  // ===== Owner: Full access bypass =====
  if (user.id === workspace.owner_id) {
    can('manage', 'all');
    return build();
  }

  // ===== Super Admin: Full access with restrictions =====
  const orgId = workspace.parent_id || workspace.id;
  const isSuperAdmin = user.superAdminOrgs?.includes(orgId);

  if (isSuperAdmin) {
    can('manage', 'all');

    // Explicit restrictions (Super Admin CANNOT do these)
    cannot('delete', 'Organization');
    cannot('modify', 'User', { isOwner: true });
    cannot('assign', 'SuperAdminRole');

    return build();
  }

  // ===== Normal users: Map granular permissions =====
  permissions.forEach(perm => {
    const [resource, action] = perm.full_name.split('.');
    const subject = mapResourceToSubject(resource);
    can(action as Actions, subject);
  });

  return build();
}

/**
 * Map database resources to CASL subjects
 */
function mapResourceToSubject(resource: string): Subjects {
  const mapping: Record<string, Subjects> = {
    'boards': 'Board',
    'cards': 'Card',
    'card_comments': 'Comment',
  };
  return mapping[resource] || 'all';
}
```

**React Integration Pattern:**

Specify how UI components will use CASL:

```typescript
// ===== React Context (features/rbac/context/AbilityContext.tsx) =====
import { createContext } from 'react';
import { AppAbility } from '../entities';

export const AbilityContext = createContext<AppAbility | null>(null);

// ===== Custom Hook (features/rbac/hooks/useAppAbility.ts) =====
import { useContext } from 'react';
import { AbilityContext } from '../context/AbilityContext';

export function useAppAbility() {
  const ability = useContext(AbilityContext);
  if (!ability) throw new Error('AbilityContext not provided');
  return ability;
}

// ===== Usage in Components =====
import { Can } from '@casl/react';
import { useAppAbility } from '@/features/rbac/hooks/useAppAbility';

function KanbanBoard() {
  const ability = useAppAbility();

  return (
    <div>
      {/* Declarative visibility with Can component */}
      <Can I="create" a="Board" ability={ability}>
        <CreateBoardButton />
      </Can>

      {/* Programmatic check */}
      {ability.can('delete', 'Board') && (
        <DeleteBoardButton />
      )}
    </div>
  );
}
```

**⚠️ CRITICAL: CASL vs RLS**

CASL and RLS serve **different purposes**:

```
┌─────────────────────────────────────────┐
│  CLIENT-SIDE (CASL)                     │
│  - UX authorization                      │
│  - Show/hide UI elements                │
│  - Enable/disable actions                │
│  - NOT security (can be bypassed)        │
└─────────────────────────────────────────┘
              ↓ HTTP Request
┌─────────────────────────────────────────┐
│  SERVER-SIDE (RLS)                      │
│  - REAL security                         │
│  - Database-level enforcement            │
│  - Cannot be bypassed                    │
│  - Final source of truth                 │
└─────────────────────────────────────────┘
```

**Both are mandatory.** CASL improves UX, RLS enforces security.

**Deliverables for Phase 2.5:**

In your PRD, include:

- [ ] CASL subject mapping table
- [ ] AppAbility type definition
- [ ] `defineAbilitiesFor()` function in entities.ts
- [ ] Owner bypass logic
- [ ] Super Admin bypass + restrictions
- [ ] Normal user permission mapping
- [ ] `mapResourceToSubject()` helper
- [ ] React integration examples (`<Can>`, hooks)
- [ ] Explanation of CASL vs RLS roles

**Reference:**
- **CASL Official Docs**: https://casl.js.org/v6/en/guide/intro
- **CASL React Integration**: https://casl.js.org/v6/en/package/casl-react

### Phase 3: Special Roles Integration

**Questions to answer:**

1. **Owner access**: Does Owner have automatic full access? (Usually yes)
2. **Super Admin access**: Does Super Admin have full access? (Usually yes, with restrictions)
3. **Protected actions**: Are there actions only Owner can perform?
4. **Project creation**: If this is an org-level feature, can it create projects?

**Critical rules:**

- Owner and Super Admin **bypass normal permission checks**
- Owner can **always** manage Super Admins
- Super Admin **cannot** modify Owner or other Super Admins
- Super Admin **cannot** assign Super Admin role
- Only Owner can delete organizations

**Reference file to consult:**
- **Special roles**: [SPECIAL_ROLES.md](references/SPECIAL_ROLES.md) - Owner and Super Admin privileges, restrictions, hierarchy

### Phase 4: Feature Activation Strategy

**Questions to answer:**

1. **Default activation**: Should this feature auto-activate in new workspaces?
2. **Mandatory feature**: Is this feature required system-wide? (Rare, only `permissions-management`)
3. **Configuration options**: Does the feature need workspace-specific config?
4. **Dependencies**: Does this feature require other features to be active?

**Implementation in entities.ts:**

```typescript
// Feature definition (goes in global features catalog)
export const KanbanFeatureSchema = z.object({
  id: z.string().uuid(),
  slug: z.literal('kanban'),
  name: z.string(),
  description: z.string(),
  category: z.string(),
  is_mandatory: z.boolean().default(false),
});

// Workspace feature activation
export const WorkspaceFeatureSchema = z.object({
  workspace_id: z.string().uuid(),
  feature_id: z.string().uuid(),
  enabled: z.boolean().default(true),
  config: z.record(z.unknown()).optional(), // JSONB config
});
```

**Reference file to consult:**
- **Feature system**: [FEATURES.md](references/FEATURES.md) - Feature catalog, activation, independence

### Phase 5: Visibility Rules with CASL

**Design how users see this feature in the UI:**

1. **Minimum permission**: What's the least permission needed to see the feature?
2. **Owner/Super Admin**: Always visible if feature is active
3. **Normal users**: Visible only if they have at least one permission
4. **Component-level**: Which UI elements require specific permissions?

**CASL Integration for Visibility:**

Use CASL's `<Can>` component and `ability.can()` checks for UI visibility:

```typescript
// ===== Feature-Level Visibility =====
import { useAppAbility } from '@/features/rbac/hooks/useAppAbility';

function useFeatureVisibility(featureSlug: string) {
  const { user, workspace } = useWorkspace();
  const ability = useAppAbility();

  // Owner/Super Admin bypass
  if (user.isOwner || user.isSuperAdmin) {
    return isFeatureActive(featureSlug, workspace);
  }

  // Check if user has ANY permission from feature
  const feature = getFeature(featureSlug);
  const hasPermission = feature.resources.some(resource => {
    const subject = mapResourceToSubject(resource);
    return ability.can('read', subject);
  });

  return hasPermission;
}

// ===== Usage in Navigation =====
function Navigation() {
  const showKanban = useFeatureVisibility('kanban');

  return (
    <nav>
      {showKanban && (
        <NavItem href="/kanban">Kanban</NavItem>
      )}
    </nav>
  );
}
```

**Component-Level Visibility with `<Can>`:**

```typescript
import { Can } from '@casl/react';
import { useAppAbility } from '@/features/rbac/hooks/useAppAbility';

function KanbanBoard({ board }: { board: Board }) {
  const ability = useAppAbility();

  return (
    <div>
      <h1>{board.name}</h1>

      {/* Declarative: Create Button */}
      <Can I="create" a="Card" ability={ability}>
        <CreateCardButton boardId={board.id} />
      </Can>

      {/* Declarative: Delete Button */}
      <Can I="delete" a="Board" ability={ability}>
        <DeleteBoardButton boardId={board.id} />
      </Can>

      {/* Programmatic: Conditional UI */}
      <div className="actions">
        {ability.can('update', 'Board') && (
          <EditBoardButton board={board} />
        )}
        {ability.can('move', 'Card') && (
          <DragAndDropHandle />
        )}
      </div>

      {/* Inverted: Show message when user CANNOT do something */}
      <Can not I="create" a="Card" ability={ability}>
        <p className="text-muted">
          You don't have permission to create cards
        </p>
      </Can>
    </div>
  );
}
```

**Field-Level Visibility (Advanced):**

CASL supports field-level permissions for fine-grained visibility:

```typescript
// Define field-level permissions in ability
can('read', 'Board', ['name', 'description']); // Can see name and description
can('read', 'Board', ['budget'], { isOwner: true }); // Only owners see budget

// Check field access
const canSeeBudget = ability.can('read', 'Board', 'budget');

// UI implementation
function BoardDetails({ board }: { board: Board }) {
  const ability = useAppAbility();

  return (
    <div>
      <h2>{board.name}</h2>
      <p>{board.description}</p>

      {/* Budget only visible to owners */}
      {ability.can('read', subject('Board', board), 'budget') && (
        <div>Budget: ${board.budget}</div>
      )}
    </div>
  );
}
```

**Loading State Pattern:**

While abilities are loading, show skeleton UI:

```typescript
function ProtectedPage() {
  const { ability, isLoading } = useAbilityWithLoading();

  if (isLoading) {
    return <SkeletonLoader />;
  }

  return (
    <Can I="read" a="Board" ability={ability}>
      <BoardList />
    </Can>
  );
}
```

**Example visibility logic (CASL version):**

```typescript
// User sees "Kanban" in menu if:
// - Owner/Super Admin (ability.can('manage', 'all') === true), OR
// - Has ANY permission: ability.can('read', 'Board') || ability.can('create', 'Board') || ...

// User sees "Create Board" button if:
// - ability.can('create', 'Board') === true
```

**Deliverables for Phase 5:**

In your PRD, include:

- [ ] Feature-level visibility hook using CASL
- [ ] `<Can>` component usage examples for all major actions
- [ ] Programmatic `ability.can()` checks for conditional UI
- [ ] Field-level visibility examples (if applicable)
- [ ] Loading states while abilities are fetched
- [ ] Inverted checks (`<Can not>`) for permission denial messages

**Reference file to consult:**
- **Visibility system**: [VISIBILITY.md](references/VISIBILITY.md) - UI visibility, feature gates, permission-based rendering
- **CASL React Docs**: https://casl.js.org/v6/en/package/casl-react

### Phase 6: Database Schema and Security Layers

**Design RLS-ready schema:**

1. **Workspace foreign key**: All feature tables MUST reference `workspaces.id`
2. **RLS policies**: Plan policies for Owner, Super Admin, and normal users
3. **Multi-tenancy**: Ensure workspace_id filters prevent cross-workspace access
4. **Cascading deletes**: Plan what happens when workspace is deleted

**Example schema pattern:**

```sql
CREATE TABLE kanban_boards (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  created_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policy
CREATE POLICY "Users can access boards in their workspaces"
ON kanban_boards FOR SELECT
TO authenticated
USING (
  -- Owner bypass
  workspace_id IN (
    SELECT id FROM workspaces
    WHERE owner_id = auth.uid()
  )
  OR
  -- Super Admin bypass
  workspace_id IN (
    SELECT organization_id FROM organization_super_admins
    WHERE user_id = auth.uid()
  )
  OR
  -- Normal user with permission
  user_can(auth.uid(), 'read', 'boards', workspace_id)
);
```

**⚡ Security Layers: CASL + RLS Coordination**

CASL and RLS work together as **defense in depth**:

```
┌──────────────────────────────────────────────────────────┐
│                    USER INTERACTION                       │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│  LAYER 1: CASL (Client-Side Authorization)               │
│  Purpose: UX optimization                                 │
│  - Shows/hides UI elements                                │
│  - Disables buttons for unauthorized actions              │
│  - Prevents unnecessary API calls                         │
│  - Improves user experience                               │
│                                                            │
│  Security: ❌ NOT REAL SECURITY (can be bypassed)         │
└──────────────────────────────────────────────────────────┘
                           ↓
                    HTTP Request Sent
                           ↓
┌──────────────────────────────────────────────────────────┐
│  LAYER 2: RLS (Server-Side Security)                     │
│  Purpose: REAL security enforcement                       │
│  - Database-level access control                          │
│  - Cannot be bypassed by client                           │
│  - Enforced even if CASL is disabled/hacked               │
│  - Multi-tenant data isolation                            │
│                                                            │
│  Security: ✅ FINAL SOURCE OF TRUTH                       │
└──────────────────────────────────────────────────────────┘
```

**Example Flow:**

```typescript
// ===== CLIENT SIDE =====
// Step 1: User clicks "Delete Board"
function BoardActions({ board }) {
  const ability = useAppAbility();

  // CASL check: Should we even show the button?
  if (!ability.can('delete', 'Board')) {
    return null; // Button not rendered
  }

  async function handleDelete() {
    // CASL check passed, send request
    const response = await fetch(`/api/boards/${board.id}`, {
      method: 'DELETE',
    });

    // If RLS denies, we get 403 error here
    if (!response.ok) {
      alert('Permission denied');
    }
  }

  return <button onClick={handleDelete}>Delete</button>;
}

// ===== SERVER SIDE (RLS) =====
-- Step 2: Supabase receives DELETE query
DELETE FROM kanban_boards WHERE id = '...';

-- Step 3: RLS policy checks
-- Policy evaluates:
-- 1. Is user the owner? workspace_id IN (SELECT ...)
-- 2. Is user super admin? workspace_id IN (SELECT ...)
-- 3. Does user have permission? user_can(auth.uid(), 'delete', 'boards', ...)

-- If ANY condition is true → DELETE succeeds
-- If ALL conditions are false → ERROR: permission denied
```

**Why Both Layers?**

| Scenario | CASL Only | RLS Only | CASL + RLS (Recommended) |
|----------|-----------|----------|--------------------------|
| Authorized user | ✅ Button shown | ✅ DELETE succeeds | ✅ Button shown, DELETE succeeds |
| Unauthorized user | ✅ Button hidden | ✅ DELETE blocked | ✅ Button hidden, DELETE blocked (if bypassed) |
| Attacker bypasses CASL | ❌ Button shown via DevTools | ✅ DELETE blocked | ✅ DELETE blocked (RLS protects) |
| Performance | ✅ No unnecessary requests | ❌ Sends request then fails | ✅ No unnecessary requests |
| UX | ✅ Clean UI | ❌ Buttons shown, fail on click | ✅ Clean UI |

**Architectural Rules:**

1. **CASL mirrors RLS**: CASL permissions should match what RLS allows
2. **RLS is source of truth**: If there's a conflict, RLS wins
3. **Both are mandatory**: Never rely on CASL alone for security
4. **Test RLS independently**: Assume CASL can be bypassed
5. **Keep them in sync**: When RLS changes, update CASL definitions

**In Your PRD:**

Document both layers:

```markdown
## Security Architecture

### Client-Side Authorization (CASL)
- Users with `boards.create` permission see "Create Board" button
- Implemented via `<Can I="create" a="Board">`

### Server-Side Security (RLS)
- PostgreSQL policy enforces permission check
- Queries auth.uid() from JWT
- Calls user_can() function for verification

### Sync Strategy
- CASL abilities loaded from same permissions table as RLS
- Permissions cached for 5 minutes in TanStack Query
- Realtime invalidation ensures <500ms sync
```

**Reference file to consult:**
- **Data model**: [DATA_MODEL.md](references/DATA_MODEL.md) - Tables, RLS patterns, database functions

### Phase 7: PRD Documentation

**Include in your PRD (`00-master-prd.md`):**

1. **Feature Metadata**
   - Feature slug (e.g., `kanban`)
   - Feature category (e.g., `productivity`)
   - Target workspaces (organization, project, or both)

2. **Permission Matrix**
   - Complete list of resources
   - All permissions with format `resource.action`
   - Visibility permission (usually `{primary_resource}.read`)

3. **Role Definitions** (if creating default roles)
   - Role name and scope (organization/project)
   - Permissions assigned to each role
   - Use cases for each role

4. **Special Role Behavior**
   - What Owner can do
   - What Super Admin can do
   - Any restrictions or protected actions

5. **Workspace Integration**
   - How feature activates
   - Configuration options
   - Dependencies on other features

6. **Data Contracts** (in entities.ts)
   - Zod schemas for all resources
   - Feature definition schema
   - Permission schemas

**Reference file to consult:**
- **Business rules**: [BUSINESS_RULES.md](references/BUSINESS_RULES.md) - Complete ruleset for workspaces, features, permissions, roles

## Common Architect Mistakes to Avoid

### General RBAC Mistakes

❌ **Assuming feature inheritance** between org and projects
✅ Each workspace activates features independently

❌ **Creating "Owner of project"** role
✅ Owner only exists at organization level

❌ **Hardcoding Owner/Super Admin permissions** in permission tables
✅ Owner/Super Admin use bypass logic, not permission tables

❌ **Mixing business logic with permissions**
✅ Permissions are pure access control; business rules go in use cases

❌ **Forgetting workspace_id in entities**
✅ All feature entities must reference workspace

❌ **Creating permissions without resources**
✅ Always define resources first, then permissions on those resources

❌ **Ignoring RLS in schema design**
✅ Plan RLS policies during entity design

### CASL-Specific Mistakes

❌ **Treating CASL as security**
✅ CASL is UX authorization; RLS is real security

❌ **Not defining CASL subjects in PRD**
✅ Architect must specify subject mapping for each resource

❌ **Using different permission formats in CASL vs database**
✅ Maintain consistent `resource.action` format everywhere

❌ **Forgetting `cannot()` rules for Super Admin restrictions**
✅ Define explicit restrictions: `cannot('delete', 'Organization')`

❌ **Not syncing CASL with RLS changes**
✅ When RLS policies change, update `defineAbilitiesFor()` accordingly

❌ **Hardcoding abilities instead of loading from database**
✅ Load permissions from Supabase, then build CASL abilities dynamically

❌ **Missing type safety for subjects and actions**
✅ Define TypeScript types: `type AppAbility = MongoAbility<[Actions, Subjects]>`

❌ **Not handling ability loading states**
✅ Show skeleton UI while abilities are being fetched

## Quick Reference Checklist

Before delivering PRD, verify:

### Core RBAC
- [ ] Feature slug is unique and descriptive
- [ ] All resources identified and documented
- [ ] Permissions follow `resource.action` format
- [ ] Visibility permission clearly identified
- [ ] Owner behavior documented
- [ ] Super Admin restrictions documented
- [ ] Workspace scope defined (org/project/both)
- [ ] entities.ts includes all Zod schemas
- [ ] Schema includes workspace_id foreign keys
- [ ] RLS policies planned for all tables
- [ ] No assumptions about feature inheritance
- [ ] No "Owner of project" concepts

### CASL Integration ⚡
- [ ] CASL subjects mapped (PascalCase, singular)
- [ ] `AppAbility` type defined with Actions and Subjects
- [ ] `defineAbilitiesFor()` function in entities.ts
- [ ] Owner bypass logic: `can('manage', 'all')`
- [ ] Super Admin restrictions: `cannot()` rules documented
- [ ] Normal user permission mapping implemented
- [ ] `mapResourceToSubject()` helper function included
- [ ] React integration examples (`<Can>`, `useAppAbility`)
- [ ] CASL vs RLS roles explained in PRD
- [ ] Loading states for abilities considered
- [ ] Type safety enforced for subjects and actions

## Reference Files

Load these files as needed for detailed information:

- **[CONCEPTS.md](references/CONCEPTS.md)**: Core definitions (Workspace, Feature, Resource, Permission, Role)
- **[WORKSPACES.md](references/WORKSPACES.md)**: Organization vs Project architecture, independence rules
- **[FEATURES.md](references/FEATURES.md)**: Feature catalog, activation, configuration, independence
- **[PERMISSIONS.md](references/PERMISSIONS.md)**: Granular permissions, roles, assignment, verification
- **[SPECIAL_ROLES.md](references/SPECIAL_ROLES.md)**: Owner and Super Admin privileges, restrictions, hierarchy
- **[VISIBILITY.md](references/VISIBILITY.md)**: UI visibility system, feature gates, permission-based rendering
- **[DATA_MODEL.md](references/DATA_MODEL.md)**: Database schema patterns, RLS policies, functions
- **[BUSINESS_RULES.md](references/BUSINESS_RULES.md)**: Complete ruleset (all RN-* rules from concepto-base.md)

## Output Format

When using this skill, structure your PRD with these sections:

```markdown
## Feature Metadata
- Slug: [feature-slug]
- Category: [category]
- Workspace Scope: [organization|project|both]
- Mandatory: [yes|no]

## Resources and Permissions

### Resources
- [resource-name]: [description]

### Permissions
- [resource].[action]: [description]

### Visibility Permission
- [resource].[action]: Grants UI visibility

## CASL Integration ⚡

### Subject Mapping
| Database Resource | CASL Subject |
|-------------------|--------------|
| boards            | Board        |
| cards             | Card         |
| card_comments     | Comment      |

### Actions
- Standard: `create`, `read`, `update`, `delete`
- Custom: `move`, `assign` (if applicable)

### Type Definition
```typescript
type Subjects = 'Board' | 'Card' | 'Comment' | 'all';
type Actions = 'create' | 'read' | 'update' | 'delete' | 'move' | 'manage';
export type AppAbility = MongoAbility<[Actions, Subjects]>;
```

### Ability Builder
- Owner: `can('manage', 'all')`
- Super Admin: `can('manage', 'all')` + restrictions
- Normal users: Map from permissions table

### React Integration
- Components use `<Can I="action" a="Subject">`
- Hooks use `useAppAbility()`

## Role Definitions (if applicable)

### [Role Name]
- Scope: [organization|project]
- Permissions: [list]
- Use Case: [description]

## Special Role Behavior

### Owner
- [specific behaviors]
- CASL: Full bypass via `can('manage', 'all')`

### Super Admin
- [specific behaviors]
- Restrictions: [what they cannot do]
- CASL: `cannot('delete', 'Organization')`, etc.

## Security Architecture

### Client-Side Authorization (CASL)
- [How CASL controls UI visibility]
- Implemented via `<Can>` components and `ability.can()` checks

### Server-Side Security (RLS)
- [How RLS enforces access control]
- PostgreSQL policies using `user_can()` function

### Sync Strategy
- Permissions loaded from database
- CASL abilities built dynamically
- TanStack Query caching (5min stale time)
- Realtime invalidation (<500ms sync)

## Workspace Integration
- Activation: [automatic|manual]
- Configuration: [config options]
- Dependencies: [required features]

## Data Contracts (entities.ts)

[Zod schemas + CASL ability builder function]
```

## Final Note

This system is **highly modular and flexible**. The key is understanding that:

1. **Workspaces are independent** - No sharing, no inheritance
2. **Features are modular** - Can be activated anywhere
3. **Permissions are contextual** - Only apply in specific workspace
4. **Owner/Super Admin are special** - Bypass normal rules with specific restrictions

When in doubt, consult the reference files and remember: **explicit is better than implicit**.
