---
name: better-auth-setup
description: Guide implementation of OAuth 2.1 / OIDC authentication using Better Auth with the OIDC Provider plugin. Use this skill when setting up centralized authentication for multiple apps, implementing SSO across a platform, creating an OAuth authorization server, or integrating Better Auth as an identity provider. Covers PKCE for public clients, JWKS configuration, token management, email verification, and common pitfalls like preserving PKCE parameters during sign-in redirects.
---

# Better Auth OAuth/OIDC Setup Skill

## Purpose
Guide implementation of OAuth 2.1 / OIDC authentication using Better Auth with the OIDC Provider plugin.

## When to Use
- Setting up centralized authentication for multiple apps
- Implementing SSO (Single Sign-On) across a platform
- Creating an OAuth authorization server
- Integrating Better Auth as an identity provider

## Key Questions to Ask

1. **Architecture**
   - How many apps will use this auth server?
   - Is this for first-party apps only or third-party OAuth clients too?
   - Do you need dynamic client registration?

2. **Database**
   - Which database? (Postgres recommended with Neon for serverless)
   - Need user profiles beyond core auth fields?

3. **Features**
   - Role-based access control needed?
   - Admin dashboard for user management?
   - Consent screen for third-party apps?

## Implementation Checklist

### 1. Auth Server Setup (Public Client with PKCE)

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { oidcProvider } from "better-auth/plugins/oidc-provider";
import { admin } from "better-auth/plugins/admin";

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: "pg", schema }),

  emailAndPassword: { enabled: true },

  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24,     // Refresh daily
  },

  trustedOrigins: process.env.ALLOWED_ORIGINS?.split(","),

  plugins: [
    oidcProvider({
      loginPage: "/auth/sign-in",
      consentPage: "/auth/consent",
      trustedClients: [{
        clientId: "your-app",
        // No clientSecret for public clients - use PKCE instead
        type: "public",  // Public client for SPAs
        redirectUrls: ["http://localhost:3000/auth/callback"],  // Note: lowercase 'urls'
        skipConsent: true,  // First-party apps
      }],
      // Add custom claims to userinfo
      async getAdditionalUserInfoClaim(user) {
        return { role: user.role };
      },
    }),
    admin({
      defaultRole: "user",
      adminRoles: ["admin"],
    }),
  ],
});
```

### 2. OAuth Client with PKCE (Recommended for SPAs)

```typescript
// Client app: src/lib/auth-client.ts

// PKCE helpers
function generateCodeVerifier(): string {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return base64UrlEncode(array);
}

async function generateCodeChallenge(verifier: string): Promise<string> {
  const hash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(verifier));
  return base64UrlEncode(new Uint8Array(hash));
}

// Authorization URL with PKCE
export async function getOAuthAuthorizationUrl(state: string) {
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = await generateCodeChallenge(codeVerifier);

  // Store verifier for token exchange
  sessionStorage.setItem('pkce_code_verifier', codeVerifier);

  const params = new URLSearchParams({
    client_id: 'your-app',
    redirect_uri: 'http://localhost:3000/auth/callback',
    response_type: 'code',
    scope: 'openid profile email',
    state,
    code_challenge: codeChallenge,
    code_challenge_method: 'S256',
  });
  return `${AUTH_SERVER_URL}/api/auth/oauth2/authorize?${params}`;
}

// Callback: exchange code for tokens with PKCE (no client_secret!)
const codeVerifier = sessionStorage.getItem('pkce_code_verifier');
const tokenResponse = await fetch(`${AUTH_SERVER_URL}/api/auth/oauth2/token`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code,
    redirect_uri: 'http://localhost:3000/auth/callback',
    client_id: 'your-app',
    code_verifier: codeVerifier,  // PKCE: verifier instead of secret
  }),
});
sessionStorage.removeItem('pkce_code_verifier');
```

### 3. Session Management (Client)

```typescript
// AuthContext.tsx pattern
const checkSession = async () => {
  const accessToken = localStorage.getItem('access_token');
  if (accessToken) {
    const response = await fetch(`${AUTH_URL}/api/auth/oauth2/userinfo`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    if (response.ok) {
      setSession({ user: await response.json() });
    } else {
      localStorage.removeItem('access_token');
    }
  }
};

const signOut = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  setSession(null);
  window.location.href = '/';
};
```

### 4. Admin-Only Client Registration (Custom Endpoint)

Better Auth's built-in `/api/auth/oauth2/register` endpoint allows dynamic client registration but doesn't enforce admin-only access. For production environments where you want to control who can register OAuth clients, create a custom admin-only endpoint:

```typescript
// src/app/api/admin/clients/register/route.ts
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { db } from "@/lib/db";
import { oauthApplication } from "@/lib/db/schema";
import crypto from "crypto";

function generateClientId(): string {
  return crypto.randomBytes(24).toString("base64url");
}

function generateClientSecret(): string {
  return crypto.randomBytes(32).toString("base64url");
}

export async function POST(request: NextRequest) {
  // Check if user is authenticated and is admin
  const session = await auth.api.getSession({ headers: await headers() });

  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  if (session.user.role !== "admin") {
    return NextResponse.json({ error: "Forbidden - admin only" }, { status: 403 });
  }

  const { name, redirectUrls, clientType } = await request.json();
  const isPublic = clientType === "public";

  const newClient = {
    id: crypto.randomUUID(),
    clientId: generateClientId(),
    clientSecret: isPublic ? null : generateClientSecret(), // null for public
    name,
    redirectURLs: redirectUrls.join(","), // Note: capital URLs
    type: isPublic ? "public" : "confidential",
    disabled: false,
    metadata: JSON.stringify({
      token_endpoint_auth_method: isPublic ? "none" : "client_secret_post",
      grant_types: ["authorization_code", "refresh_token"],
    }),
    createdAt: new Date(),
    updatedAt: new Date(),
  };

  await db.insert(oauthApplication).values(newClient);

  return NextResponse.json({
    client_id: newClient.clientId,
    client_secret: isPublic ? null : newClient.clientSecret,
    client_type: isPublic ? "public" : "confidential",
  });
}
```

**Usage**: Admin users can now register clients via:
```bash
curl -X POST http://localhost:3001/api/admin/clients/register \
  -H "Content-Type: application/json" \
  -H "Cookie: session-cookie" \
  -d '{
    "name": "My New App",
    "redirectUrls": ["http://localhost:4000/callback"],
    "clientType": "public"
  }'
```

### 5. Seeding Trusted Public Client

For first-party apps (like robolearn-interface), you'll want to seed a trusted public client during setup. Provide three methods:

**Option 1: SQL Script (Recommended for production)**
```sql
-- scripts/seed-public-client.sql
INSERT INTO oauth_application (
  id, client_id, client_secret, name, redirect_urls,
  type, disabled, metadata, created_at, updated_at
) VALUES (
  'robolearn-public-client-id',
  'robolearn-public-client',
  NULL, -- No secret for public client (PKCE only)
  'RoboLearn Public Client',
  'http://localhost:3000/auth/callback',
  'public',
  false,
  '{"token_endpoint_auth_method":"none","grant_types":["authorization_code","refresh_token"]}',
  NOW(),
  NOW()
)
ON CONFLICT (client_id) DO UPDATE SET
  name = EXCLUDED.name,
  redirect_urls = EXCLUDED.redirect_urls,
  updated_at = NOW();
```

**Option 2: TypeScript Seed Script**
```typescript
// scripts/seed-public-client.ts
import { drizzle } from "drizzle-orm/neon-serverless";
import { neonConfig, Pool } from "@neondatabase/serverless";
import { oauthApplication } from "../src/lib/db/schema";
import ws from "ws";

neonConfig.webSocketConstructor = ws;

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const db = drizzle(pool);

await db.insert(oauthApplication).values({
  id: "robolearn-public-client-id",
  clientId: "robolearn-public-client",
  clientSecret: null,
  name: "RoboLearn Public Client",
  redirectURLs: "http://localhost:3000/auth/callback",
  type: "public",
  disabled: false,
  metadata: JSON.stringify({
    token_endpoint_auth_method: "none",
    grant_types: ["authorization_code", "refresh_token"],
  }),
  createdAt: new Date(),
  updatedAt: new Date(),
}).onConflictDoUpdate({
  target: oauthApplication.clientId,
  set: { name: "RoboLearn Public Client", updatedAt: new Date() },
});

console.log("✓ Seeded robolearn-public-client");
await pool.end();
```

Run: `npx tsx scripts/seed-public-client.ts`

**Option 3: Admin API Endpoint**
```typescript
// src/app/api/admin/seed-public-client/route.ts
export async function POST(request: NextRequest) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (session?.user.role !== "admin") {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  // Same seed logic as TypeScript script above
  // ...

  return NextResponse.json({ success: true });
}
```

### 6. Email Verification Setup (Optional but Recommended)

Better Auth supports email verification via multiple providers. Use a fallback strategy for reliability:

```typescript
// src/lib/auth.ts
import { Resend } from "resend";
import * as nodemailer from "nodemailer";

// Email configuration - supports multiple providers
const EMAIL_FROM = process.env.EMAIL_FROM ||
                   process.env.RESEND_FROM_EMAIL ||
                   process.env.SMTP_FROM;

// Provider 1: SMTP (Google Gmail, custom SMTP)
const smtpConfigured = !!(
  process.env.SMTP_HOST &&
  process.env.SMTP_USER &&
  process.env.SMTP_PASS
);

const smtpTransport = smtpConfigured
  ? nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: parseInt(process.env.SMTP_PORT || "587"),
      secure: process.env.SMTP_SECURE === "true",
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS,
      },
    })
  : null;

// Provider 2: Resend
const resend = process.env.RESEND_API_KEY
  ? new Resend(process.env.RESEND_API_KEY)
  : null;

const emailEnabled = !!(EMAIL_FROM && (smtpTransport || resend));

// Generic email sender - tries SMTP first, then Resend
async function sendEmail({ to, subject, html }: {
  to: string;
  subject: string;
  html: string
}) {
  if (!emailEnabled || !EMAIL_FROM) {
    console.warn("[Auth] Email not configured - skipping");
    return;
  }

  // Priority 1: SMTP
  if (smtpTransport) {
    await smtpTransport.sendMail({ from: EMAIL_FROM, to, subject, html });
    return;
  }

  // Priority 2: Resend
  if (resend) {
    await resend.emails.send({ from: EMAIL_FROM, to, subject, html });
    return;
  }
}

export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
    ...(emailEnabled && {
      sendResetPassword: async ({ user, url }) => {
        await sendEmail({
          to: user.email,
          subject: "Reset your password",
          html: `<a href="${url}">Reset Password</a>`,
        });
      },
    }),
  },

  emailVerification: {
    sendOnSignUp: true,
    autoSignInAfterVerification: true,
    expiresIn: 3600, // 1 hour
    sendVerificationEmail: async ({ user, url }) => {
      await sendEmail({
        to: user.email,
        subject: "Verify your email",
        html: `<a href="${url}">Verify Email</a>`,
      });
    },
  },
});
```

**Environment Variables**:
```env
# Option 1: Resend (free tier: 100/day)
RESEND_API_KEY=re_xxxxxxxxx
RESEND_FROM_EMAIL=onboarding@resend.dev

# Option 2: SMTP (Gmail - requires app password)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASS=app-password
EMAIL_FROM=your@gmail.com
```

**Gmail App Password**: https://myaccount.google.com/apppasswords

## JWKS (JSON Web Key Set) Configuration

For production-scale deployments, enable JWKS for client-side token verification:

```typescript
import { jwt } from "better-auth/plugins";

plugins: [
  // JWT Plugin - Enables JWKS endpoint for asymmetric key signing (RS256)
  jwt({
    jwks: {
      keyPairConfig: {
        alg: "RS256", // RSA with SHA-256 - standard for OIDC/JWKS
      },
      disablePrivateKeyEncryption: true, // Disable encryption for simplicity
    },
  }),
  
  oidcProvider({
    useJWTPlugin: true, // Enable JWT plugin integration
    accessTokenExpiresIn: 60 * 60 * 6, // 6 hours
    refreshTokenExpiresIn: 60 * 60 * 24 * 7, // 7 days
    codeExpiresIn: 600, // 10 minutes
    // ... other config
  }),
]
```

**Benefits**:
- **Offline token verification**: Clients verify ID tokens locally using JWKS public keys
- **Reduced server load**: No per-request userinfo calls needed
- **Better scalability**: Handles 10,000+ users per app without hitting auth server
- **OIDC compliant**: Standard RS256 signing with JWKS endpoint

**Client-side implementation**:
```typescript
// Client verifies ID token using JWKS (no server call!)
const payload = await verifyIDToken(idToken, authUrl, clientId);
if (payload) {
  // Token is valid, extract user info from token
  const user = extractUserFromToken(payload);
  // No need to call /userinfo endpoint!
}
```

## Token Expiry Configuration

Configure OAuth token expiration times:

```typescript
oidcProvider({
  accessTokenExpiresIn: 60 * 60 * 6,        // 6 hours (21600 seconds)
  refreshTokenExpiresIn: 60 * 60 * 24 * 7,  // 7 days (604800 seconds)
  codeExpiresIn: 600,                        // 10 minutes (authorization code)
})
```

**Recommendations**:
- **Access tokens**: 1-6 hours (balance security vs. refresh frequency)
- **Refresh tokens**: 7-30 days (longer for better UX)
- **Authorization codes**: 10 minutes (OAuth standard)

## Common Pitfalls

### 1. PKCE Parameters Lost During Sign-In Redirect

When the OAuth authorization endpoint redirects to a sign-in page, the sign-in form must preserve PKCE parameters and forward them after successful authentication:

```typescript
// In sign-in-form.tsx - MUST extract and preserve PKCE params
const codeChallenge = searchParams.get("code_challenge");
const codeChallengeMethod = searchParams.get("code_challenge_method");

// After successful sign-in, rebuild OAuth URL WITH PKCE params
if (clientId && redirectUri && responseType) {
  const oauthParams = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    response_type: responseType,
    ...(scope && { scope }),
    ...(state && { state }),
    ...(codeChallenge && { code_challenge: codeChallenge }),  // CRITICAL!
    ...(codeChallengeMethod && { code_challenge_method: codeChallengeMethod }),
  });
  window.location.href = `/api/auth/oauth2/authorize?${oauthParams.toString()}`;
}
```

**Symptom**: "code verification failed" error on first login or after logout
**Cause**: Sign-in form drops PKCE parameters when rebuilding OAuth URL
**Fix**: Extract and include code_challenge and code_challenge_method in redirect

### 2. Wrong Property Name
```typescript
// WRONG - causes "Cannot read properties of undefined (reading 'find')"
redirectURLs: ["http://..."]

// CORRECT
redirectUrls: ["http://..."]
```

### 3. Cookie vs Token Auth Confusion
- OAuth clients should ONLY use tokens from localStorage
- Don't fall back to cookie-based session checking
- Cookie sessions are for the auth server itself

### 4. CORS Configuration
```typescript
// Auth server must trust client origins
trustedOrigins: ["http://localhost:3000", "https://your-app.com"]

// Environment variable
ALLOWED_ORIGINS=http://localhost:3000,https://your-app.com
```

### 5. Logout Scope
- OAuth standard: client clears its own tokens
- Auth server session stays active (SSO pattern)
- Don't try to clear auth server session from client

## Database Schema (Drizzle)

Required tables for OIDC Provider:
- `user` - Core user data
- `session` - Server sessions
- `account` - Auth provider accounts
- `oauth_application` - Registered OAuth clients
- `oauth_access_token` - Issued tokens
- `oauth_consent` - User consent records

## Testing Checklist

1. [ ] OIDC Discovery endpoint works: `GET /.well-known/openid-configuration`
2. [ ] Authorization redirects to login when unauthenticated
3. [ ] Authorization returns code after login
4. [ ] Token exchange returns access_token
5. [ ] UserInfo returns user data with valid token
6. [ ] Sign out clears tokens and redirects

## Security Checklist

- [ ] HTTPS in production
- [ ] Strong BETTER_AUTH_SECRET (32+ chars)
- [ ] PKCE enabled for public clients (SPAs, mobile apps)
- [ ] No client secrets in browser code (use PKCE instead)
- [ ] Exact redirect URI matching
- [ ] Rate limiting enabled
- [ ] CORS properly configured via `trustedOrigins`
- [ ] Token refresh implemented for long sessions
- [ ] Global logout option for multi-app SSO
- [ ] Email verification required (`requireEmailVerification: true`)
- [ ] Admin-only client registration endpoint
- [ ] Public clients have `clientSecret = null` in database
- [ ] JWKS keys rotated periodically (automatic with Better Auth)
- [ ] JWKS endpoint accessible at `/api/auth/jwks`
- [ ] Client-side token verification implemented (reduces server load)
- [ ] Token expiry configured appropriately (6h access, 7d refresh)
