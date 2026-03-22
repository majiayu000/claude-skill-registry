---
name: permissions-system
description: |
  Three-layer permission system (Team Roles + Plans + Quotas) for this Next.js application.
  Covers user roles, team roles, theme extensions, permission checking, and RLS integration.
  Use this skill when implementing or modifying access control features.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Permissions System Skill

Three-layer permission architecture for role-based access control, feature gating, and usage limits.

## Architecture Overview

```
THREE-LAYER PERMISSION SYSTEM:

Layer 1: Team Roles (RBAC)
├── Core roles: owner (100), admin (50), member (10), viewer (1)
├── Theme can extend: editor, contributor, moderator, etc.
└── Permissions defined in permissions.config.ts

Layer 2: Plans (Feature Gating)
├── Subscription-based feature access
├── Plan features defined in plans.config.ts
└── Checked via membership.hasFeature()

Layer 3: Quotas (Usage Limits)
├── Per-plan usage tracking
├── Enforced via membership.checkQuota()
└── Tracked in usage table

core/lib/permissions/
├── types.ts           # Permission type definitions
├── check.ts           # Server-side permission checks
├── hooks.ts           # Frontend permission hooks
├── system.ts          # Core system permissions
└── merge.ts           # Configuration merging

core/lib/services/
├── permission.service.ts   # O(1) permission lookups
└── membership.service.ts   # Complete membership context
```

## When to Use This Skill

- Implementing role-based access control
- Adding entity permissions
- Extending team roles in themes
- Checking permissions in API routes
- Rendering UI based on permissions
- Working with feature flags and quotas

## User Roles vs Team Roles

### CRITICAL: Understanding the Two Role Systems

This application uses **two completely separate role systems** for different purposes:

| Aspect | User Roles | Team Roles |
|--------|------------|------------|
| **Storage** | `user.role` column | `teamMembers.role` column |
| **Scope** | Global (entire app) | Per-team membership |
| **Extensible** | ❌ **NO** - Hardcoded in core | ✅ **YES** - Themes add custom roles |
| **Purpose** | Route access control | Entity permissions |
| **Checked by** | Middleware, roleHelpers | MembershipService |

### User Roles (App-Level, FIXED - NOT Extensible)

```typescript
// 3 fixed system roles - CANNOT be extended by themes
// Defined in: core/types/user.types.ts
type UserRole = 'member' | 'superadmin' | 'developer'
```

| Role | Hierarchy | Access | Routes |
|------|-----------|--------|--------|
| `member` | 1 | Standard authenticated user | `/dashboard/*` |
| `superadmin` | 99 | System admin, bypasses team permissions | `/superadmin/*` |
| `developer` | 100 | Full access, debugging APIs | `/devtools/*` |

**Why NOT extensible:**
- Security: Route protection must be predictable
- Core functionality: Middleware relies on fixed set
- System integrity: Themes cannot grant system-level access

**Check user role:**
```typescript
import { roleHelpers } from '@/core/lib/role-helpers'

// CORRECT: Use roleHelpers for user roles
if (roleHelpers.isDeveloper(user.role)) {
  // Access to /devtools/*
}
if (roleHelpers.isSuperAdmin(user.role)) {
  // Access to /superadmin/*, bypasses team checks
}

// WRONG: Never check user roles via membership
if (membership.hasRole('superadmin')) {} // This checks TEAM role, not user role!
```

### Team Roles (Team-Level, EXTENSIBLE by Themes)

```typescript
// Core team roles (protected, always available)
type CoreTeamRole = 'owner' | 'admin' | 'member' | 'viewer'

// Theme can add custom roles
type TeamRole = CoreTeamRole | 'editor' | 'contributor' | 'moderator' | string
```

| Role | Hierarchy | Description | Extensible |
|------|-----------|-------------|------------|
| `owner` | 100 | Team creator, all permissions, cannot be removed | ❌ Core |
| `admin` | 50 | Team management, member roles, billing | ❌ Core |
| `member` | 10 | Standard entity access | ❌ Core |
| `viewer` | 1 | Read-only access | ❌ Core |
| `editor` | 5 | Theme-defined: Edit without delete | ✅ Theme |
| `contributor` | 3 | Theme-defined: Limited create/edit | ✅ Theme |
| `moderator` | 7 | Theme-defined: Content moderation | ✅ Theme |

### Complete Example: Adding Custom Team Roles

```typescript
// contents/themes/your-theme/config/permissions.config.ts
import type { ThemePermissionsConfig } from '@/core/lib/permissions/types'

export const PERMISSIONS_CONFIG_OVERRIDES: ThemePermissionsConfig = {
  // 1. Define custom team roles
  roles: {
    additionalRoles: ['editor', 'contributor', 'moderator'] as const,
    hierarchy: {
      editor: 5,        // Between viewer (1) and member (10)
      contributor: 3,   // Above viewer, below editor
      moderator: 7,     // Above editor, below member
    },
    displayNames: {
      editor: 'common.teamRoles.editor',           // i18n key
      contributor: 'common.teamRoles.contributor',
      moderator: 'common.teamRoles.moderator',
    },
    descriptions: {
      editor: 'Can view and edit content without delete access',
      contributor: 'Can create and edit own content only',
      moderator: 'Can moderate content and manage comments',
    },
  },

  // 2. Define which roles can perform which actions (object format, not array)
  entities: {
    products: [
      { action: 'read', roles: ['owner', 'admin', 'member', 'editor', 'contributor', 'moderator', 'viewer'] },
      { action: 'create', roles: ['owner', 'admin', 'member', 'editor', 'contributor'] },
      { action: 'update', roles: ['owner', 'admin', 'member', 'editor'] },
      { action: 'delete', roles: ['owner', 'admin'] },
      { action: 'moderate', roles: ['owner', 'admin', 'moderator'] },
    ],
  },

  // 3. Define team-level permissions
  teams: [
    { action: 'team.view', roles: ['owner', 'admin', 'member', 'editor', 'contributor', 'moderator', 'viewer'] },
    { action: 'team.edit', roles: ['owner', 'admin'] },
    { action: 'team.members.invite', roles: ['owner', 'admin'] },
    { action: 'team.members.remove', roles: ['owner', 'admin'] },
    { action: 'team.members.changeRole', roles: ['owner', 'admin'] },
    { action: 'team.delete', roles: ['owner'], dangerous: true },
  ],
}
```

### Translations for Custom Roles

```json
// contents/themes/your-theme/messages/en.json
{
  "common": {
    "teamRoles": {
      "editor": "Editor",
      "contributor": "Contributor",
      "moderator": "Moderator"
    }
  }
}

// contents/themes/your-theme/messages/es.json
{
  "common": {
    "teamRoles": {
      "editor": "Editor",
      "contributor": "Colaborador",
      "moderator": "Moderador"
    }
  }
}
```

**IMPORTANT:** Core roles (`owner`, `admin`, `member`, `viewer`) translations are in `core/messages/`. Theme MUST NOT redefine them.

## Permission Format

```typescript
// Pattern: "[scope].[action]"
type Permission = `${string}.${string}`

// Entity permissions
'customers.create'
'customers.read'
'customers.update'
'customers.delete'

// Team permissions
'team.view'
'team.edit'
'team.members.invite'
'team.members.remove'
'team.delete'

// Feature permissions
'page-builder.access'
'page-builder.custom-css'
'api-keys.manage'
```

## Theme Extension Pattern

### permissions.config.ts

```typescript
// contents/themes/default/config/permissions.config.ts
import type { ThemePermissionsConfig } from '@/core/lib/permissions/types'

export const PERMISSIONS_CONFIG_OVERRIDES: ThemePermissionsConfig = {
  // 1. Add custom team roles
  roles: {
    additionalRoles: ['editor'] as const,
    hierarchy: { editor: 5 },  // Between viewer (1) and member (10)
    displayNames: {
      editor: 'common.teamRoles.editor',  // i18n key
    },
    descriptions: {
      editor: 'Can view and edit content with limited access',
    },
  },

  // 2. Team-level permissions
  teams: [
    { action: 'team.view', roles: ['owner', 'admin', 'member', 'viewer', 'editor'] },
    { action: 'team.edit', roles: ['owner', 'admin'] },
    { action: 'team.members.invite', roles: ['owner', 'admin'] },
    { action: 'team.members.remove', roles: ['owner', 'admin'] },
    { action: 'team.delete', roles: ['owner'], dangerous: true },
  ],

  // 3. Entity permissions (entity.action format)
  entities: {
    customers: [
      { action: 'create', roles: ['owner', 'admin'], label: 'Create customers' },
      { action: 'read', roles: ['owner', 'admin', 'member', 'editor'] },
      { action: 'update', roles: ['owner', 'admin', 'member'] },
      { action: 'delete', roles: ['owner'], dangerous: true },
    ],
    tasks: [
      { action: 'create', roles: ['owner', 'admin', 'member'] },
      { action: 'read', roles: ['owner', 'admin', 'member'] },
      { action: 'update', roles: ['owner', 'admin', 'member'] },
      { action: 'delete', roles: ['owner', 'admin'] },
      // Note: 'editor' intentionally excluded from tasks
    ],
  },

  // 4. Feature permissions
  features: [
    {
      action: 'page-builder.access',
      roles: ['owner', 'admin', 'editor', 'member'],
      label: 'Access Page Builder',
    },
    {
      action: 'page-builder.custom-css',
      roles: ['owner', 'admin'],
      dangerous: true,
      label: 'Use custom CSS',
    },
  ],

  // 5. Override or disable core permissions (optional)
  // Example: extend core media permissions with theme-specific roles
  overrides: {
    'media.read': { roles: ['owner', 'admin', 'editor', 'member', 'viewer'] },
    'media.upload': { roles: ['owner', 'admin', 'editor'] },
    'media.update': { roles: ['owner', 'admin', 'editor'] },
  },
  disabled: [
    // Disable specific core permissions
  ],
}
```

## PermissionService

```typescript
// core/lib/services/permission.service.ts

export class PermissionService {
  // Check single permission - O(1)
  static hasPermission(role: string, permission: Permission): boolean

  // Check any action format (teams.*, entities.*, features.*)
  static canDoAction(role: string, action: string): boolean

  // Get all permissions for role - O(1)
  static getRolePermissions(role: string): Permission[]

  // Check multiple permissions
  static hasAnyPermission(role: string, permissions: Permission[]): boolean
  static hasAllPermissions(role: string, permissions: Permission[]): boolean

  // Get permission configuration
  static getConfig(permission: Permission): ResolvedPermission | undefined

  // Full matrix for admin UI
  static getMatrix(): { permissions, matrix, sections, roles }
}
```

**Usage:**
```typescript
import { PermissionService } from '@/core/lib/services/permission.service'

// Check if admin can create customers
PermissionService.hasPermission('admin', 'customers.create')  // true

// Check if editor can access tasks
PermissionService.canDoAction('editor', 'tasks.read')  // false
```

## MembershipService

```typescript
// core/lib/services/membership.service.ts

// TeamMembership class - returned by MembershipService.get()
export class TeamMembership {
  // Role checks
  hasMinHierarchy(level: number): boolean
  hasRole(role: string): boolean
  hasAnyRole(roles: string[]): boolean

  // Permission checks
  hasPermission(permission: Permission): boolean
  hasFeature(feature: string): boolean

  // Quota checks
  checkQuota(limitSlug: string, increment?: number): { allowed, remaining }

  // Comprehensive action check (combines all layers)
  canPerformAction(action: string, options?): ActionResult
}

export class MembershipService {
  // Get complete membership context
  static async get(userId: string, teamId: string): Promise<TeamMembership>
}
```

**Usage:**
```typescript
import { MembershipService } from '@/core/lib/services/membership.service'

const membership = await MembershipService.get(userId, teamId)

// Layer 1: RBAC
if (membership.hasPermission('customers.delete')) {
  // Can delete customers
}

// Layer 2: Plan features
if (membership.hasFeature('advanced_analytics')) {
  // Show analytics dashboard
}

// Layer 3: Quotas
const quota = membership.checkQuota('projects', 1)
if (!quota.allowed) {
  throw new Error('Project limit reached')
}

// Comprehensive check
const result = membership.canPerformAction('customers.create')
if (!result.allowed) {
  // result.reason: 'permission_denied' | 'quota_exceeded' | 'feature_disabled'
  throw new Error(result.message)
}
```

## Server-Side Permission Checks

```typescript
// core/lib/permissions/check.ts

// Single permission check
export async function checkPermission(
  userId: string,
  teamId: string,
  permission: Permission
): Promise<boolean>

// Multiple permissions (AND - all required)
export async function checkPermissions(
  userId: string,
  teamId: string,
  permissions: Permission[]
): Promise<boolean>

// Multiple permissions (OR - any sufficient)
export async function checkAnyPermission(
  userId: string,
  teamId: string,
  permissions: Permission[]
): Promise<boolean>

// Synchronous check (when role is known)
export function hasPermissionSync(
  teamRole: TeamRole,
  permission: Permission
): boolean
```

**API Route Usage:**
```typescript
import { checkPermission } from '@/core/lib/permissions/check'
import { createApiError } from '@/core/lib/api/response'

export async function DELETE(request: NextRequest, { params }) {
  const { userId, teamId } = await getAuthContext(request)

  // Check permission before action
  const canDelete = await checkPermission(userId, teamId, 'customers.delete')
  if (!canDelete) {
    return createApiError('Permission denied', 403)
  }

  // Proceed with deletion
  await CustomerService.delete(params.id, userId)
  return createApiResponse({ success: true })
}
```

## Frontend Permission Hooks

```typescript
// core/lib/permissions/hooks.ts
'use client'

// Single permission check
export function usePermission(permission: Permission): boolean

// Multiple permissions (returns object)
export function usePermissions<T extends Record<string, Permission>>(
  permissions: T
): Record<keyof T, boolean>

// Get all user permissions in team
export function useAllPermissions(): Permission[]

// Get current team role
export function useTeamRole(): TeamRole | null
```

**Component Usage:**
```typescript
import { usePermission, usePermissions, useTeamRole } from '@/core/lib/permissions/hooks'

function CustomerActions({ customerId }) {
  // Single permission
  const canDelete = usePermission('customers.delete')

  // Multiple permissions
  const { canEdit, canExport } = usePermissions({
    canEdit: 'customers.update',
    canExport: 'customers.export',
  })

  // Role-based rendering
  const role = useTeamRole()

  return (
    <>
      {canEdit && <EditButton id={customerId} />}
      {canDelete && <DeleteButton id={customerId} />}
      {role === 'owner' && <OwnerOnlySettings />}
    </>
  )
}
```

## Entity Permission Actions

```typescript
// Standard entity actions
type EntityAction =
  | 'create'   // Create new record
  | 'read'     // View individual record
  | 'list'     // List records
  | 'update'   // Edit record
  | 'delete'   // Delete record
  | 'export'   // Export data
  | 'import'   // Import data
  | 'assign'   // Assign to user
  | 'publish'  // Publish record
  | 'archive'  // Archive record

// Permission action definition
interface EntityPermissionAction {
  action: EntityAction | string
  label: string
  description?: string
  roles: TeamRole[]
  dangerous?: boolean
}
```

## RLS Integration

Permissions work with Row Level Security at the database level:

```typescript
// RLS policies use team membership
CREATE POLICY "users_can_view_own_team_data"
ON customers
FOR SELECT
USING (
  "teamId" IN (
    SELECT "teamId" FROM "teamMembers"
    WHERE "userId" = current_setting('app.user_id')
  )
);
```

**Service layer sets RLS context:**
```typescript
import { queryWithRLS } from '@/core/lib/db'

// userId passed to set app.user_id for RLS
const customers = await queryWithRLS(
  'SELECT * FROM customers WHERE status = $1',
  ['active'],
  userId  // Sets app.user_id
)
```

## Build-Time Registry

```typescript
// core/lib/registries/permissions-registry.ts (AUTO-GENERATED)

// Pre-computed at build time for O(1) lookups
export const ALL_PERMISSIONS: Permission[]
export const PERMISSIONS_BY_ROLE: Record<TeamRole, Set<Permission>>
export const PERMISSIONS_BY_CATEGORY: Record<string, ResolvedPermission[]>
export const TEAM_PERMISSIONS_BY_ROLE: Record<TeamRole, Permission[]>
```

**Rebuild registry:**
```bash
node core/scripts/build/registry.mjs
```

## Anti-Patterns

```typescript
// NEVER: Hardcode role checks
if (user.role === 'admin') { /* access */ }

// CORRECT: Use permission checks
if (await checkPermission(userId, teamId, 'customers.delete')) {}

// NEVER: Skip permission check on destructive actions
await CustomerService.delete(id, userId)  // Missing permission check!

// CORRECT: Always check before destructive actions
const canDelete = await checkPermission(userId, teamId, 'customers.delete')
if (!canDelete) throw new Error('Permission denied')
await CustomerService.delete(id, userId)

// NEVER: Mix user roles and team roles
if (membership.hasRole('superadmin')) {}  // Wrong context!

// CORRECT: Use appropriate role type
if (roleHelpers.isSuperAdmin(user.role)) {}       // User role
if (membership.hasRole('admin')) {}               // Team role

// NEVER: Check permissions client-side only
// Client checks are for UI, server MUST re-validate

// CORRECT: Always validate on server
// Client: usePermission() for UI
// Server: checkPermission() for action
```

## Checklist

Before finalizing permission implementation:

- [ ] Uses three-layer check when appropriate (permission + feature + quota)
- [ ] Server-side checks on all protected routes
- [ ] Frontend hooks for conditional UI rendering
- [ ] Entity permissions defined in theme's permissions.config.ts
- [ ] Custom roles include hierarchy and display names
- [ ] Dangerous actions marked with `dangerous: true`
- [ ] RLS policies align with permission model
- [ ] Registry rebuilt after config changes

## Related Skills

- `better-auth` - Authentication patterns
- `entity-api` - API endpoint patterns
- `service-layer` - Service patterns with RLS
