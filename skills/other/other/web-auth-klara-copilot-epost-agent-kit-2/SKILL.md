---
name: web-auth
description: Use when working with authentication, sessions, OAuth providers, feature flags, or provider nesting
user-invokable: false

metadata:
  agent-affinity: [epost-implementer]
  keywords: [auth, session, oauth, nextauth, feature-flag, jwt]
  platforms: [web]
  triggers: ["session", "auth", "oauth", "login", "feature flag", "provider"]
---

# Authentication — NextAuth + OAuth Provider Patterns

## Purpose

Authentication, session management, and feature flag patterns. Uses NextAuth v4 with your OAuth provider (e.g., Keycloak, Auth0, Azure AD).

## Auth Setup

### NextAuth Configuration

**Location**: `app/api/auth/[...nextauth]/auth-options.ts`

```typescript
import YourOAuthProvider from 'next-auth/providers/...'; // e.g., KeycloakProvider, Auth0Provider

export const Options: NextAuthOptions = {
  providers: [
    YourOAuthProvider({
      clientId: process.env.PROVIDER_CLIENT_ID!,
      clientSecret: process.env.PROVIDER_SECRET!,
      issuer: process.env.PROVIDER_ISSUER,
    }),
  ],
  pages: { signIn: '/login' },
  session: {
    strategy: 'jwt',
    maxAge: 12 * 60 * 60,  // 12 hours
    updateAge: 0,           // prevents automatic refresh
  },
};
```

### Token Refresh Logic

JWT callback handles refresh with two triggers:
- **5-minute buffer** before token expiry
- **30-minute interval** refresh regardless of expiry

```typescript
function shouldRefreshToken(decodedToken, lastRefreshed): boolean {
  const isTokenExpiring = decodedToken?.exp &&
    moment().isAfter(moment.unix(decodedToken.exp).subtract(5, 'minutes'));
  const shouldRefreshByInterval = lastRefreshed &&
    moment().isAfter(moment.unix(lastRefreshed).add(30, 'minutes'));
  return Boolean(isTokenExpiring || shouldRefreshByInterval);
}
```

## Session Extension

Extend `DefaultSession` with your custom fields. Common additions include tokens, user profile data, and role information:

```typescript
export interface ExtendedSession extends DefaultSession {
  accessToken: string;
  refreshToken: string;
  idToken: string;
  // Add your project-specific fields here:
  organizationId?: string;
  roles?: string[];
  firstName?: string;
  lastName?: string;
  error?: string;
}
```

## Session Access Patterns

### Pattern 1: Server Components

```typescript
// utils/session-server.ts
import { getServerSession } from 'next-auth';
import { Options, ExtendedSession } from '../api/auth/[...nextauth]/auth-options';

export async function getServerSessionData(): Promise<ExtendedSession> {
  const session = await getServerSession(Options);
  if (!session) throw new Error('Session not found');
  return session as ExtendedSession;
}
```

### Pattern 2: Client Components

```typescript
import { useSession } from 'next-auth/react';

export const useSessionData = () => {
  const session = useSession().data as ExtendedSession;
  return {
    isAuthenticated: !!session?.accessToken,
    roles: session?.roles ?? [],
    organizationId: session?.organizationId,
  };
};
```

### Pattern 3: Server Actions / Callers

```typescript
// _services/_actions/auth-session.action.ts
export const getAuthSession = async () => {
  const session: ExtendedSession | null = await getServerSession(Options);
  if (session) {
    return {
      accessToken: session.accessToken,
      userEmail: session.user?.email,
      // Extract the fields your callers need
    };
  }
  return null;
};
```

## Provider Nesting Order

```
<ReduxProvider>              {/* Global Redux + PersistGate */}
  <AuthProvider>             {/* SessionProvider (refetchInterval=300) + SessionHandler */}
    <NextIntlClientProvider>
      {children}
    </NextIntlClientProvider>
  </AuthProvider>
</ReduxProvider>
```

## Feature Flags

### Constants

Define your feature flags as a typed constant object:

```typescript
// libs/constants.ts
export const FEATURE_FLAGS = {
  MODULE_A_V2: 'app:module-a:v2',
  MODULE_B_V2: 'app:module-b:v2',
  // Add your feature flags here
} as const;
```

### Checking Feature Flags

```typescript
// service/feature-flag-service.ts
export const isFeatureFlagEnabled = async (
  authToken: string,
  userId: string,
  featureFlag: string,
): Promise<boolean> => {
  // LRU-cached (1h TTL), falls back to API call
  // Implement with your feature flag provider (LaunchDarkly, Unleash, custom, etc.)
  // ...
};
```

Feature flags are checked in middleware for route-level guards. See `web-nextjs` middleware reference.

## Rules

- Always use your extended session type — never raw `DefaultSession`
- Use the correct session access pattern for the context (server/client/action)
- Feature flags are LRU-cached — don't worry about repeated calls
- Token refresh happens automatically in JWT callback — don't manually refresh
