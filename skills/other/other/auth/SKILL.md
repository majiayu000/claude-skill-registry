---
name: auth
description: Authentication and access control skill for Next.js 15 + Supabase applications. Use when implementing user authentication, protecting routes, managing user sessions, enforcing role-based access control (admin/member), or working with multi-tenant family-based data isolation. Covers login/logout, registration with email verification, OAuth (GitHub), route protection for Server Components and Server Actions, admin-only features, and multi-tenant data access patterns.
---

# Authentication & Access Control

This skill provides workflows for implementing authentication and access control in this Next.js 15 + Supabase application using server-side auth with httpOnly cookies, hybrid route protection, and multi-tenant family-based data isolation.

## System Overview

- **Auth Provider**: Supabase Auth with httpOnly cookies
- **Architecture**: Next.js 15 App Router with Server Components and Server Actions
- **Route Protection**: Hybrid approach (page-level auth checks, not middleware-only)
- **Multi-Tenancy**: Family-based data isolation with RLS policies
- **Roles**: Admin (first user in family) and Member

## Core Workflows

### Protecting a New Route

To protect a route from unauthenticated users:

1. Import `requireAuthRedirect` from `@/lib/auth/server-auth`
2. Call `await requireAuthRedirect()` at the start of the component
3. User will be redirected to `/login` if not authenticated

```typescript
import { requireAuthRedirect } from '@/lib/auth/server-auth';

export default async function ProtectedPage() {
  await requireAuthRedirect();

  // User guaranteed authenticated here
  return <YourContent />;
}
```

To protect an entire route group, add this to the layout component. All child routes will inherit the protection.

### Protecting a Server Action

To require authentication in a Server Action:

1. Import `requireAuth` from `@/lib/auth/server-auth`
2. Call `const user = await requireAuth()` at the start of the action
3. Action will throw `UnauthorizedError` if user not authenticated

```typescript
'use server';
import { requireAuth } from '@/lib/auth/server-auth';

export async function myAction() {
  const user = await requireAuth();

  // Proceed with authenticated action
}
```

### Getting Current User Data

- `getCurrentUser()` - Auth user (email, id), returns null if not logged in
- `getUserData()` - Extended profile (role, familyId, firstName, lastName, active)
- `getCurrentFamilyId()` - Just the family ID

All use React `cache()` - multiple calls in same request return cached value.

### Implementing Admin-Only Features

To restrict a page to admins:

```typescript
import { requireAdminRedirect } from '@/lib/auth/server-auth';

export default async function AdminPage() {
  await requireAdminRedirect();

  // User guaranteed to be admin
  return <AdminPanel />;
}
```

To restrict a Server Action to admins:

```typescript
'use server';
import { requireAdmin } from '@/lib/auth/server-auth';

export async function adminAction() {
  await requireAdmin(); // Throws if not admin
  // Proceed
}
```

To conditionally show admin UI:

```typescript
import { isAdmin } from '@/lib/auth/server-auth';

export default async function Page() {
  const userIsAdmin = await isAdmin();

  return (
    <>
      <RegularContent />
      {userIsAdmin && <AdminControls />}
    </>
  );
}
```

### Enforcing Multi-Tenant Data Access

To ensure users only access their own family's data:

```typescript
'use server';
import { requireFamilyAccess } from '@/lib/auth/server-auth';

export async function updateFamilyData(familyId: string, data: any) {
  await requireFamilyAccess(familyId); // Throws if user not in this family

  // User guaranteed to belong to this family
  await updateDatabase(familyId, data);
}
```

When fetching current user's family data, use `getCurrentFamilyId()` instead - no need for `requireFamilyAccess` since it's their own family.

### Adding a New Authentication Page

To create a new auth page (login, register, password reset):

1. Create page under `src/app/(auth)/page-name/`
2. The `(auth)` group layout automatically redirects authenticated users to `/dashboard`
3. Create corresponding Server Action in `actions.ts` file
4. Import and use Supabase client: `const supabase = await createClient()`

Pages in `(auth)` group are automatically protected from authenticated users - they'll be redirected to dashboard if already logged in.

### Implementing Login/Logout

Use `supabase.auth.signInWithPassword()` for login and `supabase.auth.signOut()` for logout. See `references/patterns.md` for complete code examples.

### Adding OAuth Providers

1. Enable provider in Supabase Dashboard
2. Use `supabase.auth.signInWithOAuth({ provider: 'github', options: {...} })`
3. Callback handled automatically by `src/app/auth/callback/route.ts`

See `references/patterns.md` for full implementation examples.

## Security Requirements

### Token Validation
- Always use `supabase.auth.getUser()` to validate tokens (revalidates with server)
- Never use `supabase.auth.getSession()` in server code (can be spoofed)

### Server-Side Only
- All auth helpers in `src/lib/auth/server-auth.ts` are server-side only
- Never import these in Client Components
- Never add `'use server'` directive to `server-auth.ts` (breaks class exports)

### Middleware
- Middleware automatically refreshes tokens on every request
- Uses `updateSession()` from `src/lib/supabase/middleware.ts`
- Calls `getUser()` to revalidate tokens
- No additional token refresh logic needed

## Reference Files

For detailed information, see:
- `references/file-tree.md` - Complete file structure and organization
- `references/security.md` - Security best practices and requirements
- `references/patterns.md` - Code examples and common patterns
- `references/flows.md` - Authentication flow diagrams

## Quick Reference

**Key Files**: `src/lib/auth/server-auth.ts` (helpers), `src/middleware.ts` (token refresh), `src/app/dashboard/layout.tsx` (dashboard protection)

**Environment**: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`, `NEXT_PUBLIC_SITE_URL`

**Database**: `auth.users` (Supabase auth), `public.families` (households), `public.users` (profiles)

## Common Issues

**'use server' export error**: Remove `'use server'` from `server-auth.ts` - these are utilities, not actions

**Middleware redirect fails**: Use `requireAuth()` in Server Actions - middleware redirects don't work with POST

**Multi-tenant access denied**: Use `requireFamilyAccess(familyId)` to validate family ownership
