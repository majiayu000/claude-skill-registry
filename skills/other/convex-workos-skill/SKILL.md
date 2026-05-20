---
name: convex-workos
description: 'WorkOS AuthKit authentication integration for Convex. Use when setting up WorkOS AuthKit, configuring ConvexProviderWithAuthKit, handling auto-provisioning, or troubleshooting WorkOS-specific auth issues.'
---

# Convex + WorkOS AuthKit

Provider-specific patterns for integrating WorkOS AuthKit with Convex.

## Required Configuration

### 1. auth.config.ts

```typescript
// convex/auth.config.ts
const clientId = process.env.WORKOS_CLIENT_ID;

export default {
  providers: [
    {
      type: 'customJwt',
      issuer: 'https://api.workos.com/',
      algorithm: 'RS256',
      applicationID: clientId,
      jwks: `https://api.workos.com/sso/jwks/${clientId}`
    },
    {
      type: 'customJwt',
      issuer: `https://api.workos.com/user_management/${clientId}`,
      algorithm: 'RS256',
      jwks: `https://api.workos.com/sso/jwks/${clientId}`
    }
  ]
};
```

**Note:** WorkOS requires TWO provider entries for different JWT issuers.

### 2. Environment Variables

```bash
# .env.local (Vite/React)
VITE_WORKOS_CLIENT_ID=client_01...
VITE_WORKOS_REDIRECT_URI=http://localhost:5173/callback

# .env.local (Next.js)
WORKOS_CLIENT_ID=client_01...
WORKOS_API_KEY=sk_test_...
WORKOS_COOKIE_PASSWORD=your_32_char_minimum_password_here
NEXT_PUBLIC_WORKOS_REDIRECT_URI=http://localhost:3000/callback

# Convex Dashboard Environment Variables
WORKOS_CLIENT_ID=client_01...
```

## Client Setup

### React (Vite)

```typescript
// src/main.tsx
import { AuthKitProvider, useAuth } from "@workos-inc/authkit-react";
import { ConvexProviderWithAuthKit } from "@convex-dev/workos";
import { ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <AuthKitProvider
    clientId={import.meta.env.VITE_WORKOS_CLIENT_ID}
    redirectUri={import.meta.env.VITE_WORKOS_REDIRECT_URI}
  >
    <ConvexProviderWithAuthKit client={convex} useAuth={useAuth}>
      <App />
    </ConvexProviderWithAuthKit>
  </AuthKitProvider>
);
```

**Install:** `npm install @workos-inc/authkit-react @convex-dev/workos`

### Next.js App Router

```typescript
// components/ConvexClientProvider.tsx
'use client';

import { ReactNode, useCallback, useRef } from 'react';
import { ConvexReactClient, ConvexProviderWithAuth } from 'convex/react';
import { AuthKitProvider, useAuth, useAccessToken } from '@workos-inc/authkit-nextjs/components';

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({ children }: { children: ReactNode }) {
  return (
    <AuthKitProvider>
      <ConvexProviderWithAuth client={convex} useAuth={useAuthFromAuthKit}>
        {children}
      </ConvexProviderWithAuth>
    </AuthKitProvider>
  );
}

function useAuthFromAuthKit() {
  const { user, loading: isLoading } = useAuth();
  const { accessToken, loading: tokenLoading, error: tokenError } = useAccessToken();

  const loading = (isLoading ?? false) || (tokenLoading ?? false);
  const authenticated = !!user && !!accessToken && !loading;

  const stableAccessToken = useRef<string | null>(null);
  if (accessToken && !tokenError) {
    stableAccessToken.current = accessToken;
  }

  const fetchAccessToken = useCallback(async () => {
    if (stableAccessToken.current && !tokenError) {
      return stableAccessToken.current;
    }
    return null;
  }, [tokenError]);

  return {
    isLoading: loading,
    isAuthenticated: authenticated,
    fetchAccessToken,
  };
}
```

**Install:** `npm install @workos-inc/authkit-nextjs @convex-dev/workos`

### Next.js Middleware

```typescript
// middleware.ts
import { authkitMiddleware } from '@workos-inc/authkit-nextjs';

export default authkitMiddleware({
  middlewareAuth: {
    enabled: true,
    unauthenticatedPaths: ['/', '/sign-in', '/sign-up']
  }
});

export const config = {
  matcher: ['/((?!.*\\..*|_next).*)', '/', '/(api|trpc)(.*)']
};
```

### Next.js Auth Routes

```typescript
// app/callback/route.ts
import { handleAuth } from '@workos-inc/authkit-nextjs';
export const GET = handleAuth();

// app/sign-in/route.ts
import { redirect } from 'next/navigation';
import { getSignInUrl } from '@workos-inc/authkit-nextjs';
export async function GET() {
  return redirect(await getSignInUrl());
}

// app/sign-up/route.ts
import { redirect } from 'next/navigation';
import { getSignUpUrl } from '@workos-inc/authkit-nextjs';
export async function GET() {
  return redirect(await getSignUpUrl());
}
```

## CORS Configuration (React/Vite only)

For React apps, configure CORS in WorkOS Dashboard:

1. **Authentication** > **Sessions** > **Cross-Origin Resource Sharing (CORS)**
2. Click **Manage**
3. Add your dev domain: `http://localhost:5173`
4. Add your prod domain when deploying

## UI Components

```typescript
import { useAuth } from "@workos-inc/authkit-react"; // or authkit-nextjs/components
import { Authenticated, Unauthenticated } from "convex/react";

function App() {
  const { user, signIn, signOut } = useAuth();

  return (
    <>
      <Authenticated>
        <button onClick={() => signOut()}>Sign out</button>
        <Content />
      </Authenticated>
      <Unauthenticated>
        <button onClick={() => signIn()}>Sign in</button>
      </Unauthenticated>
    </>
  );
}
```

## Auto-Provisioning (Development)

Convex can auto-create WorkOS environments for development:

1. Run template: `npm create convex@latest -- -t react-vite-authkit`
2. Follow prompts to link Convex team with WorkOS
3. Dev deployments auto-provision WorkOS environments

**Configured automatically:**

- Redirect URI
- CORS origin
- Local environment variables in `.env.local`

**Limitations:**

- Only works for dev deployments
- Production must be manually configured

## Dev vs Prod Configuration

| Environment | API Key       | Redirect URI                       |
| ----------- | ------------- | ---------------------------------- |
| Development | `sk_test_...` | `http://localhost:3000/callback`   |
| Production  | `sk_live_...` | `https://your-domain.com/callback` |

Set different WORKOS_CLIENT_ID in Convex Dashboard for dev vs prod deployments.

## WorkOS-Specific Troubleshooting

| Issue                     | Cause              | Fix                                                                       |
| ------------------------- | ------------------ | ------------------------------------------------------------------------- |
| CORS error                | Domain not added   | Add domain in WorkOS Dashboard > Sessions > CORS                          |
| Token validation fails    | Wrong issuer       | Check BOTH providers in auth.config.ts                                    |
| Missing `aud` claim       | JWT config         | Check WorkOS JWT configuration                                            |
| "Platform not authorized" | Workspace unlinked | Run `npx convex integration workos disconnect-team` then `provision-team` |

### "Platform not authorized" Error

```bash
npx convex integration workos disconnect-team
npx convex integration workos provision-team
```

Note: Use a different email if creating new WorkOS workspace.

## DO ✅

- Include BOTH provider entries in auth.config.ts (different issuers)
- Configure CORS for React/Vite apps
- Use `useConvexAuth()` not WorkOS's `useAuth()` for auth state
- Set WORKOS_CLIENT_ID in Convex Dashboard
- Use 32+ char WORKOS_COOKIE_PASSWORD for Next.js

## DON'T ❌

- Forget the second provider entry (user_management issuer)
- Skip CORS configuration for browser-based apps
- Use WorkOS auth hooks to gate Convex queries
- Hardcode the client ID (use env var)
- Use same WorkOS env for dev and prod
