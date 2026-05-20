---
name: auth-handler
description: Manage authentication, authorization, and user sessions. Use when dealing with login, sign-up, API protection, middleware, or user data fetching.
tools: Read, Write, Edit
model: inherit
---

# Auth Handler

## Instructions

### 1. API Route Protection
- **Standard Routes**: Use `withAuthRequired`.
  ```typescript
  export default withAuthRequired(async (req, { session, getUser }) => { ... })
  ```
- **Super Admin Routes**: Use `withSuperAdminAuthRequired`.
- **Cron Jobs**: Use `cronAuthRequired`.
- **Defense in Depth**: Do NOT rely solely on middleware. Always implement individual route protection.

### 2. Frontend Data Access
- **Client Components**: Use `useUser()` hook (SWR).
- **Restriction**: NEVER use `useSession` from `next-auth/react`.

### 3. Server-Side Data Access
- **Check Auth**: Import `auth` from `@/auth`.
- **Get Plan**: Use `getUserPlan(session.user.id)`. `session.user` is minimal.

## Reference
For architecture details, key files, and debugging tips, see [reference.md](reference.md).

