---
name: convex-clerk
description: 'Clerk authentication integration for Convex. Use when setting up Clerk auth, configuring ConvexProviderWithClerk, implementing Clerk webhooks for user sync, or troubleshooting Clerk-specific auth issues.'
---

# Convex + Clerk Authentication

Provider-specific patterns for integrating Clerk with Convex.

## Required Configuration

### 1. auth.config.ts

```typescript
// convex/auth.config.ts
import { AuthConfig } from 'convex/server';

export default {
  providers: [
    {
      domain: process.env.CLERK_JWT_ISSUER_DOMAIN!,
      applicationID: 'convex'
    }
  ]
} satisfies AuthConfig;
```

**CRITICAL:** JWT template in Clerk MUST be named exactly `convex`.

### 2. Environment Variables

```bash
# .env.local (Vite)
VITE_CLERK_PUBLISHABLE_KEY=pk_test_...

# .env.local (Next.js)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Convex Dashboard Environment Variables
CLERK_JWT_ISSUER_DOMAIN=https://verb-noun-00.clerk.accounts.dev
CLERK_WEBHOOK_SECRET=whsec_... # If using webhooks
```

## Client Setup

### React (Vite)

```typescript
// src/main.tsx
import { ClerkProvider, useAuth } from "@clerk/clerk-react";
import { ConvexProviderWithClerk } from "convex/react-clerk";
import { ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <ClerkProvider publishableKey={import.meta.env.VITE_CLERK_PUBLISHABLE_KEY}>
    <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
      <App />
    </ConvexProviderWithClerk>
  </ClerkProvider>
);
```

### Next.js App Router

```typescript
// components/ConvexClientProvider.tsx
'use client';

import { ReactNode } from 'react';
import { ConvexReactClient } from 'convex/react';
import { ConvexProviderWithClerk } from 'convex/react-clerk';
import { useAuth } from '@clerk/nextjs';

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export default function ConvexClientProvider({ children }: { children: ReactNode }) {
  return (
    <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
      {children}
    </ConvexProviderWithClerk>
  );
}
```

```typescript
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs';
import ConvexClientProvider from '@/components/ConvexClientProvider';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <ClerkProvider>
          <ConvexClientProvider>{children}</ConvexClientProvider>
        </ClerkProvider>
      </body>
    </html>
  );
}
```

### Next.js Middleware

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isProtectedRoute = createRouteMatcher(['/dashboard(.*)']);

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect();
  }
});

export const config = {
  matcher: ['/((?!.*\\..*|_next).*)', '/', '/(api|trpc)(.*)']
};
```

## UI Components

Use Convex auth components, NOT Clerk's:

```typescript
// ✅ Correct
import { Authenticated, Unauthenticated, AuthLoading } from 'convex/react';

// ❌ Don't use these for conditional rendering
import { SignedIn, SignedOut } from '@clerk/clerk-react';
```

```typescript
import { SignInButton, UserButton } from "@clerk/clerk-react";
import { Authenticated, Unauthenticated } from "convex/react";

function App() {
  return (
    <>
      <Authenticated>
        <UserButton />
        <Content />
      </Authenticated>
      <Unauthenticated>
        <SignInButton />
      </Unauthenticated>
    </>
  );
}
```

## Clerk Webhooks for User Sync

See [WEBHOOKS.md](references/WEBHOOKS.md) for complete implementation.

**Setup in Clerk Dashboard:**

1. Webhooks > Add Endpoint
2. URL: `https://your-deployment.convex.site/clerk-users-webhook`
3. Events: Select all `user.*` events
4. Copy Signing Secret → Convex Dashboard env vars as `CLERK_WEBHOOK_SECRET`

## Accessing User Info

### Client-side (Clerk SDK)

```typescript
import { useUser } from "@clerk/clerk-react";

function Profile() {
  const { user } = useUser();
  return <span>Hello, {user?.fullName}</span>;
}
```

### Server-side (Convex functions)

```typescript
export const myQuery = query({
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    // identity.name, identity.email, etc.
    // Fields depend on Clerk JWT template claims config
  }
});
```

## Dev vs Prod Configuration

| Environment | Publishable Key | Issuer Domain                             |
| ----------- | --------------- | ----------------------------------------- |
| Development | `pk_test_...`   | `https://verb-noun-00.clerk.accounts.dev` |
| Production  | `pk_live_...`   | `https://clerk.your-domain.com`           |

Set different values in Convex Dashboard for dev vs prod deployments.

## Clerk-Specific Troubleshooting

| Issue               | Cause                           | Fix                                    |
| ------------------- | ------------------------------- | -------------------------------------- |
| Token not generated | JWT template not named "convex" | Rename template to exactly `convex`    |
| `aud` mismatch      | Wrong applicationID             | Use `applicationID: "convex"`          |
| `iss` mismatch      | Wrong domain                    | Copy Frontend API URL from Clerk       |
| Webhook fails       | Wrong secret                    | Copy Signing Secret from Clerk webhook |

## DO ✅

- Name JWT template exactly `convex`
- Use `ConvexProviderWithClerk` with `useAuth` from Clerk
- Use `useConvexAuth()` not Clerk's `useAuth()` for auth state
- Use Convex's `<Authenticated>` not Clerk's `<SignedIn>`
- Set CLERK_JWT_ISSUER_DOMAIN in Convex Dashboard

## DON'T ❌

- Rename the JWT template from "convex"
- Use Clerk's auth hooks to gate Convex queries
- Hardcode the issuer domain (use env var)
- Forget to deploy after changing auth.config.ts
