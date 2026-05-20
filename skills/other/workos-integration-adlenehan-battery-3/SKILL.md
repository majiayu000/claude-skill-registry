---
name: workos-integration
description: Patterns for WorkOS SSO integration in Battery. Use this skill when implementing authentication, organization management, directory sync, or session handling.
---

# WorkOS Integration Patterns

## Overview

Battery uses WorkOS for:
- SSO federation (customers connect their Okta/Azure AD)
- Organization management (multi-tenancy)
- Directory sync (user provisioning)

## SDK Setup

```typescript
import { WorkOS } from '@workos-inc/node'

const workos = new WorkOS(process.env.WORKOS_API_KEY!)
```

## SSO Authentication

### Authorization URL

```typescript
// Generate SSO login URL
async function getAuthorizationUrl(
  organizationId: string,
  redirectUri: string
) {
  const authorizationUrl = workos.sso.getAuthorizationUrl({
    organization: organizationId,
    redirectUri,
    clientId: process.env.WORKOS_CLIENT_ID!,
  })

  return authorizationUrl
}
```

### Handle Callback

```typescript
// app/api/auth/callback/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const code = request.nextUrl.searchParams.get('code')

  if (!code) {
    return NextResponse.redirect('/login?error=missing_code')
  }

  try {
    const { profile } = await workos.sso.getProfileAndToken({
      code,
      clientId: process.env.WORKOS_CLIENT_ID!,
    })

    // Create session, set cookies, etc.
    // profile contains: id, email, firstName, lastName, organizationId

    return NextResponse.redirect('/dashboard')
  } catch (error) {
    return NextResponse.redirect('/login?error=auth_failed')
  }
}
```

## Organization Management

### Create Organization

```typescript
async function createOrganization(name: string, domains: string[]) {
  const org = await workos.organizations.createOrganization({
    name,
    allowProfilesOutsideOrganization: false,
    domains,
  })

  return org
}
```

### List Organizations

```typescript
async function listOrganizations() {
  const { data: organizations } = await workos.organizations.listOrganizations({
    limit: 100,
  })

  return organizations
}
```

### Get Organization

```typescript
async function getOrganization(orgId: string) {
  return workos.organizations.getOrganization(orgId)
}
```

## SSO Connection Setup

### List Connections

```typescript
async function getOrgConnections(organizationId: string) {
  const { data: connections } = await workos.sso.listConnections({
    organizationId,
  })

  return connections
}
```

### Admin Portal Link

Generate a link for IT admins to configure SSO:

```typescript
async function getAdminPortalLink(organizationId: string) {
  const { link } = await workos.portal.generateLink({
    organization: organizationId,
    intent: 'sso', // or 'dsync' for directory sync
    returnUrl: `${process.env.APP_URL}/settings/sso`,
  })

  return link
}
```

## Directory Sync

### List Directory Users

```typescript
async function listDirectoryUsers(directoryId: string) {
  const { data: users } = await workos.directorySync.listUsers({
    directory: directoryId,
  })

  return users
}
```

### Webhook Events

Handle directory sync webhooks:

```typescript
// app/api/webhooks/workos/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const payload = await request.text()
  const sigHeader = request.headers.get('workos-signature')!

  const webhook = workos.webhooks.constructEvent({
    payload,
    sigHeader,
    secret: process.env.WORKOS_WEBHOOK_SECRET!,
  })

  switch (webhook.event) {
    case 'dsync.user.created':
      await handleUserCreated(webhook.data)
      break
    case 'dsync.user.deleted':
      await handleUserDeleted(webhook.data)
      break
    case 'dsync.group.user_added':
      await handleUserAddedToGroup(webhook.data)
      break
  }

  return NextResponse.json({ received: true })
}
```

## Session Management

### Session Token

```typescript
interface BatterySession {
  userId: string
  email: string
  organizationId: string
  role: 'admin' | 'member'
  expiresAt: number
}

// Create session after SSO callback
async function createSession(profile: Profile): Promise<string> {
  const session: BatterySession = {
    userId: profile.id,
    email: profile.email,
    organizationId: profile.organizationId,
    role: await getUserRole(profile.id, profile.organizationId),
    expiresAt: Date.now() + 24 * 60 * 60 * 1000, // 24 hours
  }

  return signJWT(session)
}
```

### Middleware

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'
import { verifySession } from '@/lib/auth'

export async function middleware(request: NextRequest) {
  const session = await verifySession(request)

  if (!session) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Add session to request headers for server components
  const requestHeaders = new Headers(request.headers)
  requestHeaders.set('x-battery-user-id', session.userId)
  requestHeaders.set('x-battery-org-id', session.organizationId)

  return NextResponse.next({
    request: { headers: requestHeaders },
  })
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
}
```

## Auth Gateway Pattern

Battery wraps deployed apps with an auth proxy:

```typescript
// Deployed app requests flow through Battery auth gateway
// 1. User hits {app}.{org}.battery.app
// 2. Battery checks for valid session cookie
// 3. If no session, redirect to WorkOS SSO
// 4. After SSO, set session cookie and proxy to Vercel app

interface AuthGatewayConfig {
  appId: string
  organizationId: string
  allowedRoles?: string[]
}
```

## Key Patterns

1. **Organization-first**: Always scope operations to an organization
2. **Admin Portal**: Let IT admins self-service SSO setup
3. **Webhook reliability**: Use idempotency keys, handle retries
4. **Session security**: Short-lived tokens, secure cookies
5. **Role mapping**: Map IdP groups to Battery roles via directory sync
