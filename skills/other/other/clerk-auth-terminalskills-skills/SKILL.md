---
name: clerk-auth
description: >-
  Add authentication to web apps with Clerk — social login, email/password,
  magic links, organizations, RBAC, session management, webhooks, and
  multi-framework support. Use when tasks involve user authentication, team/org
  management, role-based access control, or integrating auth into Next.js,
  React, Remix, or Express applications.
license: Apache-2.0
compatibility: "Requires Node.js 16+"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags: ["clerk", "authentication", "nextjs", "react", "rbac"]
---

# Clerk Authentication

Drop-in authentication for modern web apps. Handles login UI, social providers, session management, organizations, and RBAC.

## Setup (Next.js)

```bash
npm install @clerk/nextjs
```

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_...
CLERK_SECRET_KEY=sk_live_...
```

```typescript
// app/layout.tsx — Wrap app in ClerkProvider
import { ClerkProvider } from '@clerk/nextjs';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html><body>{children}</body></html>
    </ClerkProvider>
  );
}
```

## Middleware (Route Protection)

```typescript
// middleware.ts — Protect routes at the edge
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isPublicRoute = createRouteMatcher([
  '/',
  '/pricing',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/api/webhooks(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
  if (!isPublicRoute(req)) {
    await auth.protect();
  }
});

export const config = {
  matcher: ['/((?!.*\\..*|_next).*)', '/', '/(api|trpc)(.*)'],
};
```

## Server-Side Auth

### Server Components (App Router)

```typescript
import { auth, currentUser } from '@clerk/nextjs/server';

export default async function Page() {
  // Quick access to IDs and role
  const { userId, orgId, orgRole } = await auth();

  // Full user object when needed
  const user = await currentUser();

  return <p>Hello {user?.firstName}</p>;
}
```

### API Routes

```typescript
import { auth } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

export async function GET() {
  const { userId, orgId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  // ... fetch data scoped to orgId
}
```

### Server Actions

```typescript
'use server';
import { auth } from '@clerk/nextjs/server';

export async function createProject(name: string) {
  const { userId, orgId, orgRole } = await auth();
  if (!orgId || (orgRole !== 'org:admin' && orgRole !== 'org:owner')) {
    throw new Error('Forbidden');
  }
  return db.projects.create({ data: { name, orgId, createdBy: userId } });
}
```

## Client-Side Auth

```typescript
'use client';
import { useAuth, useUser, useOrganization } from '@clerk/nextjs';

export function ProfileCard() {
  const { isSignedIn, userId } = useAuth();
  const { user } = useUser();
  const { organization, membership } = useOrganization();

  if (!isSignedIn) return <p>Not signed in</p>;

  return (
    <div>
      <p>{user?.fullName}</p>
      <p>Org: {organization?.name}</p>
      <p>Role: {membership?.role}</p>
    </div>
  );
}
```

## Pre-Built Components

```typescript
import {
  SignIn,             // Full sign-in page
  SignUp,             // Full sign-up page
  UserButton,         // Avatar dropdown (profile, sign out)
  UserProfile,        // Full profile management page
  OrganizationSwitcher,  // Org dropdown + create org
  OrganizationList,      // List orgs + join/create
  OrganizationProfile,   // Org settings (members, roles)
} from '@clerk/nextjs';

// Sign-in page
// app/sign-in/[[...sign-in]]/page.tsx
export default function SignInPage() {
  return <SignIn />;
}

// Header with org switcher and user menu
export function Header() {
  return (
    <nav>
      <OrganizationSwitcher hidePersonal={true} />
      <UserButton afterSignOutUrl="/" />
    </nav>
  );
}
```

## Organizations (Multi-Tenant)

Enable at dashboard.clerk.com → Organizations.

### Create Organization

```typescript
import { auth, clerkClient } from '@clerk/nextjs/server';

async function createOrg(name: string) {
  const { userId } = await auth();
  const client = await clerkClient();
  return client.organizations.createOrganization({
    name,
    createdBy: userId!,
  });
}
```

### Invite Members

```typescript
async function inviteMember(orgId: string, email: string, role: string) {
  const client = await clerkClient();
  return client.organizations.createOrganizationInvitation({
    organizationId: orgId,
    emailAddress: email,
    role,  // 'org:admin', 'org:member', or custom roles
    inviterUserId: (await auth()).userId!,
  });
}
```

### Custom Roles

Define at dashboard.clerk.com → Organizations → Roles:

```
org:owner    — Full access, can delete org
org:admin    — Manage members, settings
org:member   — Standard access
org:viewer   — Read-only (custom)
org:billing  — Billing management only (custom)
```

Check roles in code:

```typescript
const { orgRole, has } = await auth();

// Direct role check
if (orgRole === 'org:admin') { ... }

// Permission-based check (preferred — decouples code from role names)
if (has({ permission: 'org:projects:manage' })) { ... }
```

## Webhooks

Sync Clerk events to your database:

```typescript
// app/api/webhooks/clerk/route.ts
import { Webhook } from 'svix';
import { WebhookEvent } from '@clerk/nextjs/server';

export async function POST(req: Request) {
  const wh = new Webhook(process.env.CLERK_WEBHOOK_SECRET!);
  const body = await req.text();
  const svixHeaders = {
    'svix-id': req.headers.get('svix-id')!,
    'svix-timestamp': req.headers.get('svix-timestamp')!,
    'svix-signature': req.headers.get('svix-signature')!,
  };

  const event = wh.verify(body, svixHeaders) as WebhookEvent;

  switch (event.type) {
    case 'user.created':
      await db.users.create({ data: {
        clerkId: event.data.id,
        email: event.data.email_addresses[0]?.email_address,
        name: `${event.data.first_name} ${event.data.last_name}`.trim(),
      }});
      break;
    case 'user.deleted':
      await db.users.delete({ where: { clerkId: event.data.id } });
      break;
    case 'organization.created':
      await db.orgs.create({ data: {
        clerkOrgId: event.data.id,
        name: event.data.name,
        slug: event.data.slug,
      }});
      break;
  }

  return new Response('OK');
}
```

Key events: `user.created`, `user.updated`, `user.deleted`, `organization.created`, `organization.updated`, `organizationMembership.created`, `organizationMembership.deleted`.

## JWT Templates (API Auth)

For external APIs or microservices that need to verify Clerk tokens:

```typescript
// Configure at dashboard.clerk.com → JWT Templates
// Template name: "api-token"
// Claims: { "userId": "{{user.id}}", "orgId": "{{org.id}}", "role": "{{org.role}}" }

// Client: get a custom JWT
const { getToken } = useAuth();
const token = await getToken({ template: 'api-token' });

// External API: verify the JWT
import { createClerkClient } from '@clerk/backend';
const clerk = createClerkClient({ secretKey: process.env.CLERK_SECRET_KEY });

async function verifyRequest(req: Request) {
  const token = req.headers.get('Authorization')?.replace('Bearer ', '');
  if (!token) throw new Error('No token');
  return clerk.verifyToken(token);
}
```

## Express.js

```typescript
import { ClerkExpressRequireAuth } from '@clerk/clerk-sdk-node';

// Protect routes
app.use('/api', ClerkExpressRequireAuth());

app.get('/api/me', (req, res) => {
  res.json({ userId: req.auth.userId, orgId: req.auth.orgId });
});
```

## Guidelines

- **Middleware is the primary protection layer** — don't rely on component-level checks alone. Middleware runs at the edge before any page code.
- **Use `auth()` in server components, not `useAuth()`** — server-side checks can't be bypassed by the client
- **Webhook signature verification is mandatory** — use `svix` library to verify every webhook payload
- **Sync to your database via webhooks** — don't query Clerk's API for every database operation. Keep a local copy of users and orgs.
- **Use organizations for B2B** — even if you think you only need simple auth now. Adding multi-tenancy later is much harder than starting with it.
- **Permission-based checks over role checks** — `has({ permission: 'X' })` is more maintainable than `role === 'org:admin'`
- **`hidePersonal={true}` for B2B apps** — personal workspaces confuse users in team-based products
- **Configure sign-in/up URLs in env vars** — Clerk uses these for redirects after auth flows
