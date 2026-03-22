---
name: api-auth-clerk
description: Clerk managed authentication - ClerkProvider, middleware, pre-built components, hooks, server-side auth, organizations, webhooks
---

# Clerk Authentication Patterns

> **Quick Guide:** Clerk provides managed authentication with pre-built UI components, server-side helpers, and organization-based multi-tenancy. Use `clerkMiddleware()` for route protection, `<Show>` for conditional rendering, hooks for client state, and `auth()`/`currentUser()` for server-side auth. Clerk Core 3 (2026) replaces `<SignedIn>`/`<SignedOut>` with `<Show>`, renames the middleware file to `proxy.ts` (Next.js 16+), and consolidates packages.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `@clerk/nextjs/server` for ALL server-side imports -- NEVER import server helpers from `@clerk/nextjs`)**

**(You MUST verify webhooks using Clerk's `verifyWebhook` helper -- NEVER trust unverified webhook payloads)**

**(You MUST use `<Show>` component instead of deprecated `<SignedIn>`/`<SignedOut>`/`<Protect>` -- these are removed in Core 3)**

**(You MUST NOT pass the full `currentUser()` object to the client -- it contains `privateMetadata` that must stay server-side)**

**(You MUST protect routes in BOTH middleware AND data access layer -- middleware alone is insufficient)**

</critical_requirements>

---

**Auto-detection:** Clerk, ClerkProvider, clerkMiddleware, @clerk/nextjs, useUser, useAuth, useClerk, useSession, useOrganization, SignIn, SignUp, UserButton, UserProfile, OrganizationSwitcher, auth(), currentUser(), CLERK_SECRET_KEY, NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY, Show when="signed-in"

**When to use:**

- Adding authentication and user management to an application
- Building multi-tenant B2B apps with organization-based access control
- Using pre-built sign-in/sign-up UI components with customizable theming
- Protecting routes with middleware and server-side authorization checks
- Syncing Clerk user data to your database via webhooks

**Key patterns covered:**

- ClerkProvider setup, environment variables, middleware configuration
- Pre-built UI components (`<SignIn>`, `<SignUp>`, `<UserButton>`, `<Show>`)
- Client-side hooks (`useUser`, `useAuth`, `useSession`, `useOrganization`)
- Server-side auth (`auth()`, `currentUser()`) in Server Components, Route Handlers, Server Actions
- Middleware route protection with `clerkMiddleware()` and `createRouteMatcher()`
- Organization-based multi-tenancy with roles and permissions
- Webhook handling with Svix signature verification

**When NOT to use:**

- Self-hosted auth requirement (need full control over auth data storage)
- Cannot use a third-party auth service (compliance/regulatory constraints)
- Simple API key authentication (custom middleware is sufficient)
- Budget constraints prevent using a managed service

**Detailed Resources:**

- [reference.md](reference.md) - Decision frameworks, hooks quick reference, Core 3 migration cheat sheet
- [examples/core.md](examples/core.md) - ClerkProvider, environment variables, middleware configuration
- [examples/components.md](examples/components.md) - Pre-built components, customization, appearance prop
- [examples/hooks.md](examples/hooks.md) - useUser, useAuth, useSession, loading states, conditional rendering
- [examples/server.md](examples/server.md) - Server Components, API routes, Server Actions, webhook handling
- [examples/organizations.md](examples/organizations.md) - Organization management, roles, permissions, RBAC

---

<philosophy>

## Philosophy

Clerk is a **managed authentication platform** that handles the entire auth lifecycle: sign-up, sign-in, session management, user profiles, organizations, and MFA. Instead of building auth from scratch, you integrate Clerk's SDK and pre-built components.

**Core principles:**

1. **Defense in depth** -- Protect routes at the middleware layer AND verify auth at every data access point. Middleware alone is insufficient (CVE-2025-29927 demonstrated middleware bypass vulnerabilities).
2. **Server-first auth** -- Use `auth()` and `currentUser()` in Server Components and Route Handlers. Only use client hooks (`useUser`, `useAuth`) when you need reactive client-side state.
3. **Pre-built over custom** -- Use Clerk's `<SignIn>`, `<SignUp>`, `<UserButton>` components. Only build custom flows when the pre-built components genuinely cannot meet requirements.
4. **Organizations for multi-tenancy** -- Use Clerk Organizations with roles and permissions for B2B apps. Do not build custom tenant systems on top of Clerk's user model.
5. **Webhook-driven sync** -- Sync Clerk data to your database via webhooks, not by polling. Always verify webhook signatures with `verifyWebhook`.

**When to use Clerk:**

- You need auth quickly with minimal custom code
- You want pre-built UI components for sign-in/sign-up/user management
- You need organization-based multi-tenancy with RBAC
- You want managed MFA, SSO (SAML/OIDC), and social login

**When NOT to use Clerk:**

- You need full control over auth data storage (self-hosted requirement)
- You cannot use a third-party auth service (compliance/regulatory)
- Your app only needs simple API key authentication
- Budget constraints prevent using a managed service

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: ClerkProvider and Middleware Setup

Every Clerk app needs `<ClerkProvider>` wrapping the app and `clerkMiddleware()` protecting routes. See [examples/core.md](examples/core.md) for full setup examples.

**Key rules:**

- `ClerkProvider` goes inside `<body>`, not wrapping `<html>` -- Core 3 requires this
- Use `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` env var, never hardcode keys
- Middleware file is `proxy.ts` on Next.js 16+ or `middleware.ts` on Next.js <=15
- Webhook endpoint must be in the public routes list (verified separately by `verifyWebhook`)
- `CLERK_WEBHOOK_SIGNING_SECRET` is the env var for webhook signing (not `CLERK_WEBHOOK_SECRET`)

```ts
// proxy.ts (Next.js 16+) or middleware.ts (Next.js <=15)
const isPublicRoute = createRouteMatcher([
  "/",
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/api/webhooks(.*)",
]);

export default clerkMiddleware(async (auth, req) => {
  if (!isPublicRoute(req)) {
    await auth.protect();
  }
});
```

**Why good:** Public routes explicitly whitelisted, everything else requires auth, webhook endpoint is public (verified separately)

```ts
// BAD: clerkMiddleware() with no callback
export default clerkMiddleware(); // All routes are PUBLIC by default!
```

**Why bad:** `clerkMiddleware()` without callback attaches auth data but does not protect any route

---

### Pattern 2: Pre-Built UI Components and `<Show>`

Use `<Show>` for conditional rendering (Core 3 replacement for `<SignedIn>`/`<SignedOut>`/`<Protect>`). See [examples/components.md](examples/components.md) for full examples.

```tsx
<Show when="signed-out"><SignInButton /></Show>
<Show when="signed-in"><UserButton /></Show>
<Show when={{ role: "org:admin" }}><AdminPanel /></Show>
<Show when={(has) => has({ permission: "org:invoices:manage" })}><InvoiceManager /></Show>
```

**Why good:** `<Show>` is the Core 3 API, supports string/object/callback conditions, `fallback` prop for unauthorized

```tsx
// BAD: Deprecated -- removed in Core 3
<SignedIn>...</SignedIn>
<SignedOut>...</SignedOut>
<Protect role="admin">...</Protect>
```

**Why bad:** `<SignedIn>`, `<SignedOut>`, `<Protect>` removed in Core 3, use `<Show>` with `when` prop

Sign-in/sign-up pages require catch-all route segments `[[...sign-in]]` for multi-step flows (MFA, OAuth callbacks).

---

### Pattern 3: Client-Side Hooks

Use hooks in Client Components for reactive auth state. **Always check `isLoaded` before accessing data.** See [examples/hooks.md](examples/hooks.md) for complete examples.

```tsx
"use client";
const { isLoaded, isSignedIn, user } = useUser();
if (!isLoaded) return <div>Loading...</div>;
if (!isSignedIn) return <div>Please sign in</div>;
// Now safe to access user.firstName, user.emailAddresses, etc.
```

**Why good:** Prevents hydration errors from accessing `undefined` during init, prevents TypeError from accessing `null` when signed out

```tsx
// BAD: Accessing user without guards
const { user } = useUser();
return <p>{user.firstName}</p>; // Runtime error when isLoaded=false or isSignedIn=false
```

**Why bad:** `user` is `undefined` until loaded and `null` when signed out

**Key hooks:**

- `useUser()` -- user profile data (name, email, avatar)
- `useAuth()` -- session tokens (`getToken()`), `userId`, `orgId`, `has()` for authorization
- `useOrganization()` -- active org data, membership, paginated members list
- `useReverification()` -- re-authenticate before sensitive actions (Core 3)

In Core 3, `getToken()` throws `ClerkOfflineError` when offline instead of returning null -- always wrap in try/catch.

---

### Pattern 4: Server-Side Authentication

Use `auth()` and `currentUser()` from `@clerk/nextjs/server`. See [examples/server.md](examples/server.md) for complete examples.

**`auth()` -- lightweight, no API call, reads session claims:**

```tsx
import { auth } from "@clerk/nextjs/server";
const { userId, orgId, isAuthenticated, redirectToSignIn } = await auth();
if (!isAuthenticated) return redirectToSignIn();
```

**`currentUser()` -- full user object, makes Backend API call:**

```tsx
import { currentUser } from "@clerk/nextjs/server";
const user = await currentUser();
// CRITICAL: Pick safe fields before passing to client components
const safeData = { firstName: user.firstName, imageUrl: user.imageUrl };
```

**Why critical:** `currentUser()` returns `privateMetadata` that must never reach the client. Explicitly pick fields.

**Defense in depth:** Auth MUST be checked in every Server Action and Route Handler, not just middleware:

```ts
"use server";
const { userId } = await auth();
if (!userId) throw new Error("Unauthorized");
// userId scopes all queries/mutations to current user
```

---

### Pattern 5: Authorization with Roles and Permissions

Use `auth.protect()` or `has()` for granular access control. See [examples/organizations.md](examples/organizations.md) for RBAC patterns.

```ts
// Middleware: role-based route protection
await auth.protect((has) => has({ role: "org:admin" }));

// Server Component: permission check
const { has } = await auth();
if (!has({ permission: "org:invoices:delete" })) redirect("/dashboard");

// Client: conditional rendering by role
<Show when={{ role: "org:admin" }}><AdminPanel /></Show>
```

**Permission format:** `org:<feature>:<action>` (e.g., `org:invoices:create`, `org:reports:read`)

**Default roles:** `org:admin` (all permissions), `org:member` (read-only). Custom roles configured in Clerk Dashboard.

---

### Pattern 6: Webhook Handling

Use Clerk webhooks (via Svix) to sync user data to your database. See [examples/server.md](examples/server.md) for complete handler.

```ts
import { verifyWebhook } from "@clerk/nextjs/webhooks";

export async function POST(req: Request) {
  const evt = await verifyWebhook(req); // reads CLERK_WEBHOOK_SIGNING_SECRET env var
  // evt.type: "user.created" | "user.updated" | "user.deleted" | "organization.*" | ...
  // evt.data: UserJSON | OrganizationJSON | etc.
}
```

**Why good:** `verifyWebhook` validates Svix signature, always returns 200 to prevent retries, webhook route is public in middleware (verified by signature not by auth)

```ts
// BAD: No signature verification
const body = await req.json(); // Anyone can POST fake data!
await db.insert(users).values(body.data); // Security vulnerability
```

**Why bad:** No signature verification means anyone can send fake webhook events to your endpoint

**Import types from `@clerk/shared/types` (Core 3):** `UserJSON`, `OrganizationJSON`, `OrganizationMembershipJSON`

</patterns>

---

<decision_framework>

## Decision Framework

### Client vs Server Auth

```
Where do you need auth data?
|-- Server Component, Route Handler, Server Action
|   |-- Need just userId/sessionId? --> auth()
|   |-- Need full user object? --> currentUser()
|   |-- Need to protect the route? --> auth().protect()
|   +-- Need org context? --> auth() returns orgId, orgRole
|
+-- Client Component (interactive UI)
    |-- Need user profile data? --> useUser()
    |-- Need session/token data? --> useAuth()
    |-- Need org data? --> useOrganization()
    +-- Need low-level Clerk API? --> useClerk()
```

### Route Protection Strategy

```
What kind of route is it?
|-- Public (landing, sign-in, sign-up, webhooks)
|   +-- Add to isPublicRoute matcher, skip auth.protect()
|
|-- Authenticated (dashboard, profile, settings)
|   +-- auth.protect() in middleware + auth() check in data layer
|
+-- Authorized (admin, org-specific, permission-gated)
    |-- Role-based? --> auth.protect({ role: "org:admin" })
    +-- Permission-based? --> auth.protect((has) => has({ permission: "org:feature:action" }))
```

### Component Choice

```
What auth UI do you need?
|-- Full sign-in page --> <SignIn /> on catch-all route
|-- Full sign-up page --> <SignUp /> on catch-all route
|-- Sign-in button (modal) --> <SignInButton />
|-- User avatar + menu --> <UserButton />
|-- Full profile editor --> <UserProfile />
|-- Org switcher --> <OrganizationSwitcher />
+-- Conditional content --> <Show when="signed-in"> or <Show when={{ role: "..." }}>
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Importing server helpers from `@clerk/nextjs` instead of `@clerk/nextjs/server` (breaks in Server Components)
- Using deprecated `<SignedIn>`/`<SignedOut>`/`<Protect>` components (removed in Core 3)
- Passing full `currentUser()` object to client components (leaks `privateMetadata`)
- Trusting webhook payloads without `verifyWebhook` signature verification
- Relying solely on middleware for route protection (middleware can be bypassed)
- Importing types from `@clerk/types` instead of `@clerk/shared/types` (Core 3 rename)

**Medium Priority Issues:**

- Not checking `isLoaded` before accessing hook data (causes hydration errors)
- Using `currentUser()` on the client side (it is server-only)
- Hardcoding Clerk keys instead of using environment variables
- Using `authMiddleware()` (deprecated, replaced by `clerkMiddleware()`)
- Not making webhook endpoint public in middleware matcher
- Using `CLERK_WEBHOOK_SECRET` instead of `CLERK_WEBHOOK_SIGNING_SECRET`

**Common Mistakes:**

- Naming middleware file `middleware.ts` on Next.js 16+ (should be `proxy.ts`) or `proxy.ts` on Next.js <=15 (should be `middleware.ts`)
- Forgetting catch-all segments `[[...sign-in]]` on sign-in/sign-up pages (breaks multi-step flows)
- Using `getToken()` without try/catch in Core 3 (throws `ClerkOfflineError` when offline instead of returning null)
- Not adding `prefetch={false}` to `<Link>` components pointing at protected routes from public pages

**Gotchas & Edge Cases:**

- `currentUser()` counts against Backend API rate limits -- prefer `useUser()` hook on the client when possible
- `auth()` in Server Components is deduplicated per request (safe to call multiple times)
- `<Show when={{ role: "org:admin" }}>` requires an active organization in the session
- Organization roles use the `org:` prefix (e.g., `org:admin`, `org:member`, `org:billing`)
- Clerk Core 3 requires Node.js 20.9.0+, Next.js 15.2.3+
- `@clerk/clerk-react` renamed to `@clerk/react` in Core 3 -- update imports after upgrade

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `@clerk/nextjs/server` for ALL server-side imports -- NEVER import server helpers from `@clerk/nextjs`)**

**(You MUST verify webhooks using Clerk's `verifyWebhook` helper -- NEVER trust unverified webhook payloads)**

**(You MUST use `<Show>` component instead of deprecated `<SignedIn>`/`<SignedOut>`/`<Protect>` -- these are removed in Core 3)**

**(You MUST NOT pass the full `currentUser()` object to the client -- it contains `privateMetadata` that must stay server-side)**

**(You MUST protect routes in BOTH middleware AND data access layer -- middleware alone is insufficient)**

**Failure to follow these rules will create authentication vulnerabilities or break on Clerk Core 3.**

</critical_reminders>
