---
name: better-auth
description: |
  Authentication patterns with Better Auth for this Next.js application.
  Covers session authentication, API key authentication, dual auth, OAuth, and testing.
  Use this skill when implementing or modifying authentication features.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Better Auth Skill

Authentication patterns and best practices for this Next.js application using Better Auth.

## Architecture Overview

```
core/lib/
├── auth.ts                   # Better Auth configuration
├── auth-client.ts            # Client-side auth utilities
└── api/auth/
    ├── dual-auth.ts          # Dual authentication (API Key + Session)
    ├── index.ts              # API key validation
    └── scopes.ts             # Permission scopes

app/hooks/
└── useAuth.ts                # Client-side auth hook

app/(auth)/
├── login/                    # Login page
├── register/                 # Registration page
├── verify-email/             # Email verification
└── forgot-password/          # Password reset
```

## When to Use This Skill

- Implementing authentication flows (login, register, logout)
- Adding API key authentication to endpoints
- Implementing role-based access control
- Setting up OAuth providers
- Testing authentication flows
- Securing API endpoints with dual auth

## Authentication Methods

### 1. Session Authentication (Dashboard)

Used for authenticated users in the dashboard UI.

```typescript
// Server-side session check
import { auth } from '@/core/lib/auth'

const session = await auth.api.getSession({
  headers: request.headers
})

if (!session?.user) {
  return redirect('/login')
}
```

```typescript
// Client-side with useAuth hook
import { useAuth } from '@/app/hooks/useAuth'

function Dashboard() {
  const { user, session, isLoading, isAuthenticated } = useAuth()

  if (isLoading) return <Loading />
  if (!isAuthenticated) return redirect('/login')

  return <div>Welcome, {user.name}</div>
}
```

### 2. API Key Authentication (External APIs)

Used for external integrations and programmatic access.

```typescript
// API Key headers
// Option 1: Authorization header
Authorization: Bearer sk_live_xxxxxxxxxxxxx

// Option 2: x-api-key header
x-api-key: sk_live_xxxxxxxxxxxxx

// CRITICAL: Always include team context
x-team-id: team-tmt-001
```

### 3. Dual Authentication (Unified Endpoints)

All `/api/v1/` endpoints support both authentication methods.

```typescript
import { authenticateRequest } from '@/core/lib/api/auth/dual-auth'

export async function GET(request: NextRequest) {
  // Tries API Key first, then Session
  const authResult = await authenticateRequest(request)

  if (!authResult.success) {
    return createAuthError('Unauthorized', 401)
  }

  // authResult contains:
  // - type: 'api-key' | 'session'
  // - user: { id, email, role, defaultTeamId }
  // - scopes: string[] (for API keys) or ['all'] (for sessions)
}
```

## User Roles vs Team Roles

### CRITICAL: Two Separate Role Systems

This application has **two completely separate role systems**:

| Aspect | User Roles (App-Level) | Team Roles (Team-Level) |
|--------|------------------------|-------------------------|
| **Stored in** | `user.role` column | `teamMembers.role` column |
| **Scope** | Global (entire app) | Per-team membership |
| **Extensible** | ❌ NO - Fixed in core | ✅ YES - Themes can add custom roles |
| **Purpose** | System access (routes) | Entity permissions within team |

### User Roles (App-Level, FIXED)

```typescript
// 3 fixed system roles - CANNOT be extended by themes
type UserRole = 'member' | 'superadmin' | 'developer'
```

| Role | Hierarchy | Access | Routes |
|------|-----------|--------|--------|
| `member` | 1 | Standard user | `/dashboard/*` |
| `superadmin` | 99 | System admin, bypasses team permissions | `/superadmin/*` |
| `developer` | 100 | Full access, debugging APIs | `/devtools/*` |

**Check user role:**
```typescript
import { roleHelpers } from '@/core/lib/role-helpers'

// CORRECT: Use roleHelpers for user roles
if (roleHelpers.isDeveloper(user.role)) {
  // Access to /devtools/*
}
if (roleHelpers.isSuperAdmin(user.role)) {
  // Access to /superadmin/*, bypass team checks
}

// WRONG: Don't check user roles like team roles
if (membership.hasRole('superadmin')) {} // Wrong context!
```

### Team Roles (Team-Level, EXTENSIBLE)

```typescript
// Core team roles (protected, always available)
type CoreTeamRole = 'owner' | 'admin' | 'member' | 'viewer'

// Theme can add custom roles
type TeamRole = CoreTeamRole | 'editor' | 'contributor' | string
```

| Role | Hierarchy | Description |
|------|-----------|-------------|
| `owner` | 100 | Team creator, all permissions, cannot be removed |
| `admin` | 50 | Team management, member roles, billing |
| `member` | 10 | Standard entity access |
| `viewer` | 1 | Read-only access |
| `editor`* | 5 | Theme-defined: Edit without delete |
| `contributor`* | 3 | Theme-defined: Limited create/edit |

*Custom roles defined in `permissions.config.ts`

**Check team role:**
```typescript
import { MembershipService } from '@/core/lib/services'

// Get membership context
const membership = await MembershipService.get(userId, teamId)

// Check team role
if (membership.hasRole('admin')) {
  // Can manage team members
}

// Check specific permission
if (membership.can('products.create')) {
  // Can create products in this team
}
```

### Why Two Systems?

| User Roles | Team Roles |
|------------|------------|
| Control **where** users can go | Control **what** users can do |
| Route-level access | Entity-level permissions |
| Fixed for security | Flexible for business logic |
| Checked by middleware | Checked by API/UI |

## User Metadata (users_metas)

User metadata is stored in a **separate table** (`users_metas`) using the standard entity meta pattern.

### Schema

```sql
-- core/migrations/003_user_metas.sql
CREATE TABLE "users_metas" (
  id TEXT PRIMARY KEY,
  "userId" TEXT NOT NULL REFERENCES "users"(id) ON DELETE CASCADE,
  "metaKey" TEXT NOT NULL,
  "metaValue" JSONB NOT NULL DEFAULT '{}',
  "dataType" TEXT,              -- 'string' | 'number' | 'boolean' | 'json'
  "isPublic" BOOLEAN DEFAULT FALSE,
  "isSearchable" BOOLEAN DEFAULT FALSE,
  CONSTRAINT users_metas_unique_key UNIQUE ("userId", "metaKey")
);
```

### Common Meta Keys

| Key | Type | Description | isPublic |
|-----|------|-------------|----------|
| `preferences.theme` | string | 'light' \| 'dark' \| 'system' | false |
| `preferences.language` | string | Locale code ('en', 'es') | false |
| `preferences.timezone` | string | Timezone identifier | false |
| `preferences.sidebarCollapsed` | boolean | UI state | false |
| `onboarding.completed` | boolean | Onboarding status | false |
| `onboarding.step` | number | Current onboarding step | false |
| `notifications.email` | boolean | Email notification preference | false |
| `profile.bio` | string | User biography | true |
| `profile.socialLinks` | json | Social media links | true |

### Usage

```typescript
import { MetaService } from '@/core/lib/services'

// Get user meta
const theme = await MetaService.get('users', userId, 'preferences.theme')

// Set user meta
await MetaService.set('users', userId, 'preferences.theme', 'dark')

// Get multiple metas
const prefs = await MetaService.getMany('users', userId, [
  'preferences.theme',
  'preferences.language'
])

// Delete meta
await MetaService.delete('users', userId, 'onboarding.step')
```

### Client-Side Hook

```typescript
import { useUserSettings } from '@/core/hooks/useUserSettings'

function SettingsPage() {
  const { settings, updateSetting, isLoading } = useUserSettings()

  const toggleTheme = () => {
    updateSetting('preferences.theme', settings.theme === 'dark' ? 'light' : 'dark')
  }

  return (
    <Button onClick={toggleTheme}>
      {settings.theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
    </Button>
  )
}
```

### RLS Policies

- **Owner access:** Users can read/write their own metas
- **Admin access:** Superadmins can read/write any user's metas
- **Public read:** Metas with `isPublic = true` are readable by anyone

## API Key Scopes

```typescript
// Scope format: {entity}:{action}
// Examples:
// - tasks:read     → Read tasks
// - tasks:write    → Create/update tasks
// - tasks:delete   → Delete tasks
// - tasks:*        → Full tasks access
// - *              → Superadmin full access

// Check scopes in API
const hasAccess = authResult.scopes?.includes('tasks:read') ||
                  authResult.scopes?.includes('tasks:*') ||
                  authResult.scopes?.includes('*')
```

## Test Users

### Theme Users (password: `Test1234`)

```typescript
DEFAULT_THEME_USERS = {
  OWNER: 'carlos.mendoza@tmt.dev',      // Everpoint Labs (owner)
  ADMIN: 'james.wilson@tmt.dev',        // Everpoint Labs (admin)
  MEMBER: 'emily.johnson@tmt.dev',      // Everpoint Labs (member)
  EDITOR: 'diego.ramirez@tmt.dev',      // Everpoint Labs (editor)
  VIEWER: 'sarah.davis@tmt.dev',        // Ironvale Global (viewer)
}
```

### Core Users (password: `Pandora1234`)

```typescript
CORE_USERS = {
  SUPERADMIN: 'superadmin@tmt.dev',     // Global superadmin
  DEVELOPER: 'developer@tmt.dev',       // Global developer
}
```

### Test Teams

| Team ID | Team Name | Description |
|---------|-----------|-------------|
| `team-tmt-001` | Everpoint Labs | Primary test team |
| `team-tmt-002` | Ironvale Global | Secondary test team |

## Registration Control

Registration behavior is configurable at the theme level via `auth` in `app.config.ts`.

### Registration Modes

| Mode | Email Signup | Google OAuth Signup | Email Login | Google Login | Signup Page |
|------|-------------|-------------------|-------------|-------------|-------------|
| `open` (default) | Yes | Yes | Yes | Yes | Visible |
| `domain-restricted` | No | Only allowed domains | No | Only allowed domains | Hidden |
| `domain-open` | Only allowed domains | Only allowed domains | Only allowed domains | Only allowed domains | Visible |
| `invitation-only` | Via invite | Via invite | Yes | Configurable | Invite only |

### Theme Configuration

```typescript
// contents/themes/my-theme/config/app.config.ts

// Option 1: Open registration (default, no config needed)
auth: {
  registration: { mode: 'open' },
}

// Option 2: Only Google OAuth for specific domains (no email+password)
auth: {
  registration: {
    mode: 'domain-restricted',
    allowedDomains: ['nextspark.dev', 'mycompany.com'],
  },
}

// Option 3: Email+password AND Google OAuth, restricted to specific domains
auth: {
  registration: {
    mode: 'domain-open',
    allowedDomains: ['nextspark.dev', 'mycompany.com'],
  },
}

// Option 4: Invitation-only (integrates with single-tenant teams mode)
auth: {
  registration: { mode: 'invitation-only' },
}
```

### Types

```typescript
// packages/core/src/lib/config/types.ts
type RegistrationMode = 'open' | 'domain-restricted' | 'domain-open' | 'invitation-only'

interface AuthConfig {
  registration: {
    mode: RegistrationMode
    allowedDomains?: string[]  // For 'domain-restricted' and 'domain-open' modes
  }
  providers?: {
    google?: { enabled?: boolean }
  }
}
```

### Helper Functions

```typescript
import {
  isRegistrationOpen,
  isDomainAllowed,
  isGoogleAuthEnabled,
  shouldBlockSignup,
  getPublicAuthConfig,
} from '@/core/lib/auth/registration-helpers'
```

### Enforcement Points

1. **Route handler** (`app/api/auth/[...all]/route.ts`): Blocks email signup for `domain-restricted` and `invitation-only` modes
2. **Database hook** (`auth.ts` → `databaseHooks.user.create.before`): Validates email domain for `domain-restricted` and `domain-open` modes; blocks signup in `invitation-only` mode when team exists
3. **Session hook** (`auth.ts` → `databaseHooks.session.create.before`): Validates email domain on every login for `domain-restricted` and `domain-open` modes
4. **Signup page** (`app/(auth)/signup/page.tsx`): Redirects to `/login` for `domain-restricted` and `invitation-only`
4. **LoginForm**: Hides Google OAuth button and signup link based on mode
5. **SignupForm**: Hides Google button when disabled

### Client-Side Config

Use `PUBLIC_AUTH_CONFIG` (from `config-sync.ts`) in client components. This strips `allowedDomains` for security.

```typescript
import { PUBLIC_AUTH_CONFIG } from '@/core/lib/config/config-sync'

// PUBLIC_AUTH_CONFIG.registration.mode → 'open' | 'domain-restricted' | 'domain-open' | 'invitation-only'
// PUBLIC_AUTH_CONFIG.providers.google.enabled → boolean
```

## Authentication Flows

### Email/Password Registration

```
1. User submits registration form
2. Validate email format and password strength
3. Create user with emailVerified = false
4. Send verification email with token
5. User clicks verification link
6. Set emailVerified = true
7. Redirect to login
```

### Email/Password Login

```
1. User submits login form
2. Validate credentials
3. Check emailVerified = true
4. Create session
5. Set HttpOnly cookie
6. Redirect to dashboard
```

### Google OAuth

```
1. User clicks "Sign in with Google"
2. Redirect to Google OAuth
3. Google returns profile data
4. Map profile to user (mapProfileToUser)
5. Create/update user record
6. Create session
7. Redirect to dashboard
```

### Password Reset

```
1. User requests password reset
2. Generate reset token (1-hour expiry)
3. Send reset email
4. User clicks reset link
5. Validate token
6. User enters new password
7. Update password hash (bcrypt)
8. Invalidate token
9. Redirect to login
```

## Security Rules

### Password Requirements

```typescript
// Minimum requirements
const passwordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .max(128, 'Password cannot exceed 128 characters')
  .regex(/[A-Z]/, 'Password must contain uppercase letter')
  .regex(/[0-9]/, 'Password must contain a number')
```

### Session Configuration

```typescript
// Session settings
const sessionConfig = {
  expiresIn: 60 * 60 * 24 * 7,  // 7 days
  updateAge: 60 * 60 * 24,      // Update every day
  cookieOptions: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax'
  }
}
```

### Rate Limiting

| Action | Limit | Window |
|--------|-------|--------|
| Login attempts | 5 | 15 minutes |
| Password reset | 3 | 1 hour |
| Verification email | 5 | 1 hour |
| API requests | 100 | 1 minute |

### Token Expiration

| Token Type | Expiration |
|------------|------------|
| Email verification | 24 hours |
| Password reset | 1 hour |
| Session | 7 days |
| API Key | No expiration (revocable) |

## useAuth Hook

```typescript
import { useAuth } from '@/app/hooks/useAuth'

function Component() {
  const {
    // State
    user,             // Current user object
    session,          // Session data
    isLoading,        // Loading state
    isAuthenticated,  // Boolean auth status

    // Actions
    signIn,           // (email, password) => Promise
    signUp,           // (email, password, name) => Promise
    signOut,          // () => Promise
    resetPassword,    // (email) => Promise
    updateProfile,    // (data) => Promise
  } = useAuth()

  // Example: Sign in
  const handleLogin = async () => {
    try {
      await signIn(email, password)
      router.push('/dashboard')
    } catch (error) {
      setError(error.message)
    }
  }
}
```

## Protected Routes

### Middleware Protection

```typescript
// middleware.ts
export { auth as middleware } from "@/core/lib/auth"

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/profile/:path*',
    '/api/user/:path*'
  ]
}
```

### Page-Level Protection

```typescript
// app/dashboard/page.tsx
import { auth } from '@/core/lib/auth'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: headers()
  })

  if (!session) {
    redirect('/login')
  }

  return <Dashboard user={session.user} />
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `AUTHENTICATION_REQUIRED` | 401 | No auth credentials provided |
| `INVALID_API_KEY` | 401 | API key invalid or expired |
| `INVALID_CREDENTIALS` | 401 | Wrong email/password |
| `EMAIL_NOT_VERIFIED` | 401 | User hasn't verified email |
| `SIGNUP_RESTRICTED` | 403 | Invitation-only / single-tenant mode (registration requires invite) |
| `INSUFFICIENT_PERMISSIONS` | 403 | User lacks required scope |
| `TEAM_CONTEXT_REQUIRED` | 400 | Missing x-team-id header |
| `SESSION_EXPIRED` | 401 | Session no longer valid |

## Testing Authentication

### Cypress Session Pattern

```typescript
describe('Authenticated Tests', () => {
  beforeEach(() => {
    cy.session('owner-session', () => {
      cy.visit('/login')
      cy.get('[data-cy="email-input"]').type('carlos.mendoza@tmt.dev')
      cy.get('[data-cy="password-input"]').type('Test1234')
      cy.get('[data-cy="login-submit"]').click()
      cy.url().should('include', '/dashboard')
    }, {
      validate: () => {
        cy.visit('/dashboard')
        cy.url().should('include', '/dashboard')
      }
    })
  })

  it('should access protected page', () => {
    cy.visit('/dashboard/tasks')
    cy.get('[data-cy="tasks-table"]').should('exist')
  })
})
```

### API Test Pattern

```typescript
describe('API Auth Tests', () => {
  const API_KEY = Cypress.env('SUPERADMIN_API_KEY')
  const TEAM_ID = 'team-tmt-001'

  it('should authenticate with API key', () => {
    cy.request({
      method: 'GET',
      url: '/api/v1/tasks',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'x-team-id': TEAM_ID
      }
    }).then((response) => {
      expect(response.status).to.eq(200)
    })
  })

  it('should reject without API key', () => {
    cy.request({
      method: 'GET',
      url: '/api/v1/tasks',
      failOnStatusCode: false
    }).then((response) => {
      expect(response.status).to.eq(401)
    })
  })
})
```

## OAuth Configuration

### Google OAuth

```typescript
// core/lib/auth.ts
socialProviders: {
  google: {
    clientId: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    mapProfileToUser: (profile) => ({
      email: profile.email,
      name: profile.name,
      image: profile.picture,
      emailVerified: profile.email_verified
    })
  }
}
```

### Environment Variables

```env
# Better Auth
BETTER_AUTH_SECRET=your-secret-key
NEXT_PUBLIC_APP_URL=http://localhost:5173

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

# Email (Resend)
RESEND_API_KEY=your-resend-key
RESEND_FROM_EMAIL=noreply@yourdomain.com
```

## Anti-Patterns

```typescript
// NEVER: Store passwords in plain text
user.password = 'plain-text-password'

// CORRECT: Use bcrypt via Better Auth
await auth.api.signUp({ email, password, name })

// NEVER: Skip email verification
if (!user.emailVerified) {
  // Allow access anyway... WRONG!
}

// CORRECT: Require verification
if (!user.emailVerified) {
  redirect('/verify-email')
}

// NEVER: Expose API keys in client code
const API_KEY = 'sk_live_xxxxx' // In browser!

// CORRECT: Use environment variables (server-side only)
const API_KEY = process.env.API_KEY // Server only

// NEVER: Skip team context for entity operations
// Missing x-team-id header

// CORRECT: Always include team context
headers: { 'x-team-id': teamId }

// NEVER: Trust client-provided user data
const userId = request.body.userId // User can fake this!

// CORRECT: Get user from authenticated session
const { user } = await authenticateRequest(request)
```

## Checklist

Before finalizing authentication code:

- [ ] Uses Better Auth for all auth operations
- [ ] Sessions use HttpOnly, Secure cookies
- [ ] Email verification required for email/password
- [ ] Password meets minimum requirements (8+ chars)
- [ ] API endpoints use dual auth pattern
- [ ] Protected routes redirect unauthenticated users
- [ ] Error responses use proper status codes
- [ ] Rate limiting implemented for sensitive endpoints
- [ ] OAuth profile mapping configured correctly
- [ ] Test users documented and working

## Related Skills

- `cypress-e2e` - UAT testing with session authentication
- `cypress-api` - API testing with API key authentication
- `nextjs-api-development` - API route patterns
