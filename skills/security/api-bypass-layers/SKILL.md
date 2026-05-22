---
name: api-bypass-layers
description: |
  Multi-layer security architecture for API bypass (superadmin/developer).
  Covers authentication layers, authorization, team context, RLS policies, and three-layer bypass validation.
  Use this skill when implementing admin bypass features or validating security architecture.
allowed-tools: Read, Glob, Grep
version: 1.1.0
---

# API Bypass Layers Skill

Security architecture for superadmin and developer bypass access in the API layer.

## File References

| File | Purpose |
|------|---------|
| `packages/core/src/lib/api/auth/dual-auth.ts` | App-level bypass (canBypassTeamContext) |
| `packages/core/src/lib/api/entity/generic-handler.ts` | CRUD handler (validateTeamContextWithBypass) |
| `packages/core/migrations/001_better_auth_and_functions.sql` | get_auth_user_id() function |
| `packages/core/migrations/010_teams_functions_triggers.sql` | can_bypass_rls(), get_user_team_ids(), RLS policies |
| `packages/core/migrations/090_sample_data.sql` | System Admin Team (team-nextspark-001) |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 1: AUTHENTICATION                       │
├─────────────────────────────────────────────────────────────────┤
│  API Key Auth              │  Session Auth                      │
│  ├─ x-api-key header       │  ├─ Browser cookies                │
│  ├─ Constant-time delay    │  ├─ Better Auth framework          │
│  ├─ Key expiration check   │  └─ Full access (scopes: ['all'])  │
│  ├─ Failed attempt lockout │                                    │
│  └─ Scoped permissions     │                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 2: AUTHORIZATION                        │
├─────────────────────────────────────────────────────────────────┤
│  Admin Bypass Check (Three-Layer Validation)                    │
│  ├─ LAYER 1: Role check (superadmin OR developer)               │
│  ├─ LAYER 2: Header confirmation (x-admin-bypass)               │
│  └─ LAYER 3: System Admin Team membership (team-nextspark-001)  │
│                                                                  │
│  Permission Check                                                │
│  ├─ Entity-level permissions (entity.action format)             │
│  ├─ Team role hierarchy (owner > admin > member > viewer)       │
│  └─ Scope validation for API keys                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 3: TEAM CONTEXT                         │
├─────────────────────────────────────────────────────────────────┤
│  Normal Mode (isBypass = false)                                 │
│  ├─ x-team-id header REQUIRED                                   │
│  ├─ Validate user is team member                                │
│  ├─ Filter by teamId AND userId                                 │
│  └─ Reject if not member (403 TEAM_ACCESS_DENIED)               │
│                                                                  │
│  Bypass Mode (isBypass = true)                                  │
│  ├─ x-team-id header OPTIONAL                                   │
│  ├─ Skip membership validation                                  │
│  ├─ Skip userId filter                                          │
│  └─ Cross-team or specific team access                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 4: DATABASE RLS                         │
├─────────────────────────────────────────────────────────────────┤
│  PostgreSQL Row Level Security (Final Defense)                  │
│  ├─ can_bypass_rls() - superadmin ALWAYS, developer IF member   │
│  ├─ get_auth_user_id() - reads from app.user_id GUC             │
│  ├─ get_user_team_ids() - array of user's teams                 │
│  └─ Policies: SELECT/INSERT/UPDATE/DELETE per table             │
│                                                                  │
│  Example Policy:                                                 │
│  can_bypass_rls() OR teamId = ANY(get_user_team_ids())          │
└─────────────────────────────────────────────────────────────────┘
```

## When to Use This Skill

- Understanding the multi-layer security model
- Implementing admin bypass for new features
- Debugging authorization issues
- Validating RLS policies work correctly
- Adding new bypass-protected endpoints
- Testing cross-team access scenarios

## Constants

**File:** `packages/core/src/lib/api/auth/dual-auth.ts:13-31`

```typescript
// System Admin Team - Members can bypass team context validation
export const SYSTEM_ADMIN_TEAM_ID = 'team-nextspark-001'

// Header required to confirm cross-team access intention
export const ADMIN_BYPASS_HEADER = 'x-admin-bypass'
export const ADMIN_BYPASS_VALUE = 'confirm-cross-team-access'

// Roles that can potentially bypass team context
const ELEVATED_ROLES = ['superadmin', 'developer'] as const
```

## App-Level Bypass: canBypassTeamContext()

**File:** `packages/core/src/lib/api/auth/dual-auth.ts:205-226`

Three-layer validation for admin bypass at the application level:

```typescript
export async function canBypassTeamContext(
  authResult: DualAuthResult,
  request: NextRequest
): Promise<boolean> {
  // LAYER 1: Must have elevated role
  if (!authResult.success || !authResult.user) return false
  const hasElevatedRole = ELEVATED_ROLES.includes(
    authResult.user.role as typeof ELEVATED_ROLES[number]
  )
  if (!hasElevatedRole) return false

  // LAYER 2: Must include confirmation header
  const bypassHeader = request.headers.get(ADMIN_BYPASS_HEADER)
  if (bypassHeader !== ADMIN_BYPASS_VALUE) return false

  // LAYER 3: Must be member of System Admin Team
  const isMember = await checkSystemAdminMembership(authResult.user.id)
  if (!isMember) {
    console.log('[dual-auth] User has elevated role but is not member of System Admin Team')
  }
  return isMember
}
```

### Three-Layer Validation Table

| Layer | Check | Requirement |
|-------|-------|-------------|
| 1 | Role | `user.role` is `superadmin` OR `developer` |
| 2 | Header | `x-admin-bypass: confirm-cross-team-access` |
| 3 | Membership | User belongs to `team-nextspark-001` |

## Team Context Validation: validateTeamContextWithBypass()

**File:** `packages/core/src/lib/api/entity/generic-handler.ts:267-309`

```typescript
async function validateTeamContextWithBypass(
  request: NextRequest,
  authResult: DualAuthResult,
  userId: string
): Promise<{ valid: true; teamId: string | null; isBypass: boolean } | { valid: false; error: NextResponse }> {
  const teamId = getTeamIdFromRequest(request)

  // Check if user can bypass team validation
  const canBypass = await canBypassTeamContext(authResult, request)

  if (canBypass) {
    // Admin bypass: teamId is optional
    // - If provided: filter by that team (no membership check)
    // - If not provided: cross-team access (all teams)
    // isBypass = true means skip userId filter too (see all records)
    console.log('[GenericHandler] Admin bypass active:', { userId, teamId: teamId || 'cross-team' })
    return { valid: true, teamId, isBypass: true }
  }

  // Normal flow: require teamId and membership
  if (!teamId) {
    const response = createApiError(
      'Team context required. Include x-team-id header.',
      400,
      undefined,
      'TEAM_CONTEXT_REQUIRED'
    )
    return { valid: false, error: await addCorsHeaders(response) }
  }

  const isMember = await validateTeamMembership(userId, teamId)
  if (!isMember) {
    const response = createApiError(
      'Access denied: You are not a member of this team',
      403,
      undefined,
      'TEAM_ACCESS_DENIED'
    )
    return { valid: false, error: await addCorsHeaders(response) }
  }

  return { valid: true, teamId, isBypass: false }
}
```

## isBypass Flag Usage

**File:** `packages/core/src/lib/api/entity/generic-handler.ts`

The `isBypass` flag controls userId filtering in queries:

```typescript
// Line ~509, 538, 563, 1138
if (userId && !entityConfig.access?.shared && !skipUserFilter && !isBypass) {
  // Apply userId filter - only see own records
}
// When isBypass = true, this filter is skipped, allowing cross-user access
```

## Database-Level Bypass: can_bypass_rls()

**File:** `packages/core/migrations/010_teams_functions_triggers.sql:115-147`

**CRITICAL DIFFERENCE from App-Level:**
- **Superadmin:** ALWAYS bypasses RLS (no team membership check)
- **Developer:** Only bypasses IF member of System Admin Team

```sql
CREATE OR REPLACE FUNCTION public.can_bypass_rls()
RETURNS BOOLEAN AS $$
DECLARE
  current_user_id TEXT;
  user_role TEXT;
  is_system_admin_member BOOLEAN;
BEGIN
  current_user_id := public.get_auth_user_id();

  -- Get user role
  SELECT role INTO user_role
  FROM public."users"
  WHERE id = current_user_id;

  -- Superadmin ALWAYS bypasses (no team membership check)
  IF user_role = 'superadmin' THEN
    RETURN TRUE;
  END IF;

  -- Developer can bypass ONLY if member of System Admin Team
  IF user_role = 'developer' THEN
    SELECT EXISTS(
      SELECT 1 FROM public."team_members"
      WHERE "userId" = current_user_id
        AND "teamId" = 'team-nextspark-001'
    ) INTO is_system_admin_member;

    RETURN is_system_admin_member;
  END IF;

  RETURN FALSE;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;
```

## App vs DB Bypass Logic Comparison

| Role | App-Level (canBypassTeamContext) | DB-Level (can_bypass_rls) |
|------|----------------------------------|---------------------------|
| superadmin | Needs header + team membership | ALWAYS bypasses |
| developer | Needs header + team membership | Only with team membership |
| member | Cannot bypass | Cannot bypass |

**Why the difference?**
- App-level: Requires explicit intent (header) to prevent accidents
- DB-level: Final defense, superadmin always trusted at data layer

## RLS Helper Functions

### get_auth_user_id()

**File:** `packages/core/migrations/001_better_auth_and_functions.sql:10-24`

```sql
CREATE OR REPLACE FUNCTION public.get_auth_user_id()
RETURNS TEXT
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE v TEXT;
BEGIN
  v := current_setting('app.user_id', true);
  IF v IS NULL OR v = '' THEN
    RETURN NULL;
  END IF;
  RETURN v;
END;
$$;
```

### get_user_team_ids()

**File:** `packages/core/migrations/010_teams_functions_triggers.sql:98-109`

```sql
CREATE OR REPLACE FUNCTION public.get_user_team_ids()
RETURNS TEXT[] AS $$
DECLARE
  user_teams TEXT[];
BEGIN
  SELECT ARRAY_AGG(tm."teamId") INTO user_teams
  FROM public."team_members" tm
  WHERE tm."userId" = public.get_auth_user_id();

  RETURN COALESCE(user_teams, ARRAY[]::TEXT[]);
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;
```

## RLS Policy Pattern

**File:** `packages/core/migrations/010_teams_functions_triggers.sql:164-208`

```sql
-- SELECT policy
CREATE POLICY "teams_select_policy" ON public."teams"
  FOR SELECT TO authenticated
  USING (
    public.is_superadmin()  -- Alias for can_bypass_rls()
    OR
    id IN (
      SELECT "teamId" FROM public."team_members"
      WHERE "userId" = public.get_auth_user_id()
    )
  );

-- UPDATE policy
CREATE POLICY "teams_update_policy" ON public."teams"
  FOR UPDATE TO authenticated
  USING (
    public.is_superadmin()
    OR
    "ownerId" = public.get_auth_user_id()
  )
  WITH CHECK (
    public.is_superadmin()
    OR
    "ownerId" = public.get_auth_user_id()
  );

-- DELETE policy
CREATE POLICY "teams_delete_policy" ON public."teams"
  FOR DELETE TO authenticated
  USING (
    public.is_superadmin()
    OR
    "ownerId" = public.get_auth_user_id()
  );
```

## Error Codes

| Code | HTTP Status | Trigger |
|------|-------------|---------|
| `TEAM_CONTEXT_REQUIRED` | 400 | Missing `x-team-id` header (non-bypass mode) |
| `TEAM_ACCESS_DENIED` | 403 | User not member of specified team |
| `AUTHENTICATION_FAILED` | 401 | Invalid credentials |

## Normal Mode vs Bypass Mode

### Normal Mode (Default)

```typescript
// Headers required
const headers = {
  'x-team-id': 'team-xxx'  // REQUIRED
}

// Behavior
// - teamId is REQUIRED
// - Validate user is team member
// - Filter results by teamId AND userId
// - Return 403 TEAM_ACCESS_DENIED if not member
```

### Bypass Mode (Admin)

```typescript
// Headers required
const headers = {
  'x-admin-bypass': 'confirm-cross-team-access',  // REQUIRED
  'x-team-id': 'team-xxx'  // OPTIONAL (for filtering)
}

// Behavior
// - teamId is OPTIONAL
// - Skip membership validation
// - Skip userId filter (isBypass = true)
// - Access all teams or specific team
```

## Request Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                              API REQUEST                                  │
├──────────────────────────────────────────────────────────────────────────┤
│  Headers:                                                                 │
│  ├─ Authorization: Bearer <api-key>  OR  Cookie: session=...             │
│  ├─ x-team-id: team-xxx              (required in normal mode)           │
│  └─ x-admin-bypass: confirm-...      (enables bypass mode)               │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        BACKEND SECURITY LAYERS                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  LAYER 1: Authentication (dual-auth.ts:71-89)                            │
│  └─ authenticateRequest() → DualAuthResult                               │
│                                                                           │
│  LAYER 2: Authorization (dual-auth.ts:205-226)                           │
│  └─ canBypassTeamContext() → role + header + team check                  │
│                                                                           │
│  LAYER 3: Team Context (generic-handler.ts:267-309)                      │
│  └─ validateTeamContextWithBypass() → { teamId, isBypass }               │
│                                                                           │
│  LAYER 4: Query Building (generic-handler.ts:509+)                       │
│  └─ Add teamId/userId filters based on isBypass flag                     │
│                                                                           │
│  LAYER 5: Database RLS (010_teams_functions_triggers.sql:115-147)        │
│  └─ can_bypass_rls() OR teamId = ANY(get_user_team_ids())                │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           FILTERED RESPONSE                               │
├──────────────────────────────────────────────────────────────────────────┤
│  { success: true, data: [...filtered results...], info: { total: N } }   │
└──────────────────────────────────────────────────────────────────────────┘
```

## Testing Bypass Mode

### Cypress API Test

```typescript
describe('Admin Bypass', () => {
  const SUPERADMIN_KEY = Cypress.env('SUPERADMIN_API_KEY')

  it('should allow cross-team access with bypass', () => {
    cy.request({
      method: 'GET',
      url: '/api/v1/products',
      headers: {
        'Authorization': `Bearer ${SUPERADMIN_KEY}`,
        'x-admin-bypass': 'confirm-cross-team-access'
        // No x-team-id = cross-team mode
      }
    }).then((response) => {
      expect(response.status).to.eq(200)
      // Returns data from ALL teams
    })
  })

  it('should filter to specific team with bypass', () => {
    cy.request({
      method: 'GET',
      url: '/api/v1/products',
      headers: {
        'Authorization': `Bearer ${SUPERADMIN_KEY}`,
        'x-admin-bypass': 'confirm-cross-team-access',
        'x-team-id': 'team-tmt-002'  // Filter to specific team
      }
    }).then((response) => {
      expect(response.status).to.eq(200)
      // Returns data only from team-tmt-002
    })
  })

  it('should reject bypass without header', () => {
    cy.request({
      method: 'GET',
      url: '/api/v1/products',
      headers: {
        'Authorization': `Bearer ${SUPERADMIN_KEY}`
        // Missing x-admin-bypass and x-team-id
      },
      failOnStatusCode: false
    }).then((response) => {
      expect(response.status).to.eq(400)
      expect(response.body.code).to.eq('TEAM_CONTEXT_REQUIRED')
    })
  })
})
```

## Security Strengths

| Feature | Implementation | Benefit |
|---------|----------------|---------|
| **Dual Authentication** | API Key + Session | Flexibility for different use cases |
| **Three-Layer App Bypass** | Role + Header + Team | Defense in depth, prevents accidents |
| **RLS Final Defense** | PostgreSQL policies | Data isolation even if app bypassed |
| **Team Isolation** | App + DB checks | Multi-tenant security |
| **System Admin Team** | Hardcoded ID | Prevents privilege escalation |
| **isBypass Flag** | Skip userId filter | Cross-user visibility for admins |

## Anti-Patterns

```typescript
// NEVER: Allow bypass based on role alone at app level
if (user.role === 'superadmin') {
  return true  // WRONG! Missing header and team checks at app level
}

// CORRECT: Use the three-layer function
const isBypass = await canBypassTeamContext(authResult, request)

// NEVER: Trust client-provided bypass status
const isBypass = request.body.isBypass  // User can fake this!

// CORRECT: Validate bypass on server
const isBypass = await canBypassTeamContext(authResult, request)

// NEVER: Skip userId filter without checking bypass
if (user.role === 'superadmin') {
  skipUserFilter = true  // WRONG! Should use isBypass from validation
}

// CORRECT: Use the isBypass flag from validateTeamContextWithBypass
const { teamId, isBypass } = await validateTeamContextWithBypass(request, authResult, userId)
if (!isBypass) {
  // Apply userId filter
}
```

## Checklist

Before finalizing bypass implementation:

- [ ] App-level uses three-layer validation (role + header + team)
- [ ] `x-admin-bypass` header value is exactly `confirm-cross-team-access`
- [ ] System Admin Team ID is `team-nextspark-001` (hardcoded)
- [ ] RLS policies use `can_bypass_rls()` function
- [ ] Superadmin always bypasses RLS (no team check at DB level)
- [ ] Developer requires System Admin Team membership for RLS bypass
- [ ] `isBypass` flag controls userId filter in queries
- [ ] Normal mode requires `x-team-id` header
- [ ] Bypass mode makes `x-team-id` optional
- [ ] Error codes: `TEAM_CONTEXT_REQUIRED` (400), `TEAM_ACCESS_DENIED` (403)

## Related Skills

- `better-auth` - Authentication patterns and session management
- `permissions-system` - RBAC + Features + Quotas permission model
- `database-migrations` - PostgreSQL RLS policies
- `nextjs-api-development` - API route patterns with dual auth
- `cypress-api` - API testing with bypass scenarios
