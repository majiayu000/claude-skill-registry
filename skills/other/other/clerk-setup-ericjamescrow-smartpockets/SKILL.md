---
name: clerk-setup
description: Add Clerk authentication to any project by following the official quickstart guides.
license: MIT
allowed-tools: WebFetch
metadata:
  author: clerk
  version: "1.0.0"
---

# Adding Clerk

This skill sets up Clerk for authentication by following the official quickstart documentation.

## Quick Reference

| Step | Action |
|------|--------|
| 1. Detect framework | Check `package.json` dependencies |
| 2. Fetch quickstart | Use WebFetch on the appropriate docs URL |
| 3. Follow instructions | Execute the steps from the official guide |
| 4. Get API keys | From [dashboard.clerk.com](https://dashboard.clerk.com/last-active?path=api-keys) |

## Framework Detection

Check `package.json` to identify the framework:

| Dependency | Framework | Quickstart URL |
|------------|-----------|----------------|
| `next` | Next.js | `https://clerk.com/docs/nextjs/getting-started/quickstart` |
| `@remix-run/react` | Remix | `https://clerk.com/docs/remix/getting-started/quickstart` |
| `astro` | Astro | `https://clerk.com/docs/astro/getting-started/quickstart` |
| `nuxt` | Nuxt | `https://clerk.com/docs/nuxt/getting-started/quickstart` |
| `react-router` | React Router | `https://clerk.com/docs/react-router/getting-started/quickstart` |
| `@tanstack/react-start` | TanStack Start | `https://clerk.com/docs/tanstack-react-start/getting-started/quickstart` |
| `react` (no framework) | React SPA | `https://clerk.com/docs/react/getting-started/quickstart` |
| `vue` | Vue | `https://clerk.com/docs/vue/getting-started/quickstart` |
| `express` | Express | `https://clerk.com/docs/expressjs/getting-started/quickstart` |
| `fastify` | Fastify | `https://clerk.com/docs/fastify/getting-started/quickstart` |
| `expo` | Expo | `https://clerk.com/docs/expo/getting-started/quickstart` |

For other platforms:
- **Chrome Extension**: `https://clerk.com/docs/chrome-extension/getting-started/quickstart`
- **Android**: `https://clerk.com/docs/android/getting-started/quickstart`
- **iOS**: `https://clerk.com/docs/ios/getting-started/quickstart`
- **Vanilla JavaScript**: `https://clerk.com/docs/js-frontend/getting-started/quickstart`

## Decision Tree

```
User Request: "Add Clerk" / "Add authentication"
    │
    ├─ Read package.json
    │
    ├─ Existing auth detected?
    │   │
    │   ├─ YES → Audit current auth → Create migration plan
    │   │        → See "Migrating from Another Auth Provider"
    │   │
    │   └─ NO → Fresh install
    │
    ├─ Identify framework from dependencies
    │
    ├─ WebFetch the appropriate quickstart URL
    │
    └─ Follow the official instructions step-by-step
```

## Setup Process

### 1. Detect the Framework

Read the project's `package.json` and match dependencies to the table above.

### 2. Fetch the Quickstart Guide

Use WebFetch to retrieve the official quickstart for the detected framework:

```
WebFetch: https://clerk.com/docs/{framework}/getting-started/quickstart
Prompt: "Extract the complete setup instructions including all code snippets, file paths, and configuration steps."
```

### 3. Follow the Instructions

Execute each step from the quickstart guide:
- Install the required packages
- Set up environment variables
- Add the provider/middleware
- Create sign-in/sign-up routes if needed
- Test the integration

### 4. Get API Keys

Two paths for development API keys:

**Keyless (Automatic)**
- On first SDK initialization, Clerk auto-generates dev keys and shows "Claim your application" popover
- No manual key setup required—keys are created and injected automatically
- Simplest path for new projects

**Manual (Dashboard)**
- Get keys from [dashboard.clerk.com](https://dashboard.clerk.com/last-active?path=api-keys) if Keyless doesn't trigger
- **Publishable Key**: Starts with `pk_test_` or `pk_live_`
- **Secret Key**: Starts with `sk_test_` or `sk_live_`
- Set as environment variables: `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY`

## Migrating from Another Auth Provider

If the project already has authentication, create a migration plan before replacing it.

### Detect Existing Auth

Check `package.json` for existing auth libraries:
- `next-auth` / `@auth/core` → NextAuth/Auth.js
- `@supabase/supabase-js` → Supabase Auth
- `firebase` / `firebase-admin` → Firebase Auth
- `@aws-amplify/auth` → AWS Cognito
- `auth0` / `@auth0/nextjs-auth0` → Auth0
- `passport` → Passport.js
- Custom JWT/session implementation

### Migration Process

1. **Audit current auth** - Identify all auth touchpoints:
   - Sign-in/sign-up pages
   - Session/token handling
   - Protected routes and middleware
   - User data storage (database tables, external IDs)
   - OAuth providers configured

2. **Create migration plan** - Consider:
   - **User data export** - Export users and import via Clerk's Backend API
   - **Password hashes** - Clerk can upgrade hashes to Bcrypt transparently
   - **External IDs** - Store legacy user IDs as `external_id` in Clerk
   - **Session handling** - Existing sessions will terminate on switch

3. **Choose migration strategy**:
   - **Big bang** - Switch all users at once (simpler, requires maintenance window)
   - **Trickle migration** - Run both systems temporarily (lower risk, higher complexity)

### Migration Reference

- **Migration Overview**: https://clerk.com/docs/guides/development/migrating/overview

## Common Pitfalls

| Level | Issue | Solution |
|-------|-------|----------|
| CRITICAL | Missing `await` on `auth()` | In Next.js 15+, `auth()` is async: `const { userId } = await auth()` |
| CRITICAL | Exposing `CLERK_SECRET_KEY` | Never use secret key in client code; only `NEXT_PUBLIC_*` keys are safe |
| HIGH | Missing middleware matcher | Include API routes: `matcher: ['/((?!.*\\..*|_next).*)', '/']` |
| HIGH | ClerkProvider not at root | Must wrap entire app in root layout/App component |
| HIGH | Auth routes not public | Allow `/sign-in`, `/sign-up` in middleware config |
| HIGH | Landing page requires auth | To keep "/" public, exclude it: `matcher: ['/((?!.*\\..*|_next|^/$).*)', '/api/(.*)']` |
| MEDIUM | Wrong import path | Server code uses `@clerk/nextjs/server`, client uses `@clerk/nextjs` |

## See Also

- `custom-flows/` - Custom sign-in/up components
- `syncing-users/` - Webhook → database sync
- `managing-orgs/` - B2B multi-tenant organizations
- `testing/` - E2E testing setup
- `nextjs-patterns/` - Advanced Next.js patterns

## Documentation

- **Quickstart Overview**: https://clerk.com/docs/getting-started/quickstart/overview
- **Migration Guide**: https://clerk.com/docs/guides/development/migrating/overview
- **Full Documentation**: https://clerk.com/docs
