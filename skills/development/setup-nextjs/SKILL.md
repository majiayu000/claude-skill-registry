---
name: setup-nextjs
description: Setup Sigma Auth OAuth integration in a Next.js application. Guides through installing @sigma-auth/better-auth-plugin, configuring environment variables, creating auth client, implementing sign-in flow, and setting up API routes for token exchange with Bitcoin-native authentication.
allowed-tools: "Bash(bun:*)"
---

# Setup Next.js with Sigma Auth

Guide for integrating Sigma Auth (Bitcoin-native authentication) into a Next.js application using the @sigma-auth/better-auth-plugin package.

## When to Use

- Setting up new Next.js app with Sigma Identity authentication
- Adding Bitcoin-native auth to existing Next.js project
- Implementing OAuth flow with auth.sigmaidentity.com
- Integrating BAP (Bitcoin Attestation Protocol) identity

## Scripts

### detect.ts - Project Analysis

Analyzes your project structure and provides setup recommendations.

```bash
# Analyze current directory
bun run scripts/detect.ts

# Analyze specific project
bun run scripts/detect.ts /path/to/project
```

**Output:** JSON report including:
- Framework detection (Next.js App Router, Pages Router, Payload CMS)
- Package manager detection
- Directory structure
- Existing auth configuration
- Recommendations for setup

### validate-env.ts - Environment Validation

Validates required environment variables and checks WIF format.

```bash
# Check environment from .env.local or .env
bun run scripts/validate-env.ts

# Check specific env file
bun run scripts/validate-env.ts .env.production
```

**Output:** JSON report with status of each required variable.

### health-check.ts - Integration Health Check

Tests connection to Sigma Auth server and validates OAuth configuration.

```bash
# Check default auth server
bun run scripts/health-check.ts

# Check specific auth server
bun run scripts/health-check.ts https://auth.sigmaidentity.com
```

**Output:** JSON report including:
- Auth server connectivity
- OpenID configuration availability
- JWKS endpoint status
- Response latency

## Installation

```bash
bun add @sigma-auth/better-auth-plugin
```

## Quick Start

### Choose Your Integration Mode

- **Mode A — OAuth client (cross-domain)**: Your app is **not** the auth server. You handle tokens locally.
- **Mode B — Same-domain Better Auth server**: You run Better Auth (or proxy to Convex/another backend) on your own domain and can use sessions.

---

### Mode A — OAuth Client (Cross-Domain)

Use this when your users authenticate against `auth.sigmaidentity.com` (or another Better Auth server) on a **different** domain.

#### 1. Environment Variables (`.env.local`)

```bash
# Public variables
NEXT_PUBLIC_SIGMA_CLIENT_ID=your-app-name
NEXT_PUBLIC_SIGMA_AUTH_URL=https://auth.sigmaidentity.com

# Private variables (server-only)
SIGMA_MEMBER_PRIVATE_KEY=your-member-wif-key

# Optional (needed behind proxies for correct redirect_uri)
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

#### 2. Client Configuration (`lib/auth-client.ts`)

```typescript
import { createAuthClient } from "better-auth/react";
import { sigmaClient } from "@sigma-auth/better-auth-plugin/client";

export const authClient = createAuthClient({
  baseURL: "/api/auth", // default; points to your app's API routes
  plugins: [sigmaClient()],
});

export const { signIn } = authClient;
```

> If you are **not** using React hooks, import `createAuthClient` from `"better-auth/client"` instead.
>
> For cross-domain OAuth, manage user state locally (cookies/local state). `useSession` only works in Mode B.

#### 3. Token Exchange API (`app/api/auth/sigma/callback/route.ts`)

```typescript
import { createCallbackHandler } from "@sigma-auth/better-auth-plugin/next";

export const runtime = "nodejs";
export const POST = createCallbackHandler();
```

#### 4. OAuth Callback Page (`app/auth/sigma/callback/page.tsx`)

This page handles the OAuth redirect and stores tokens locally.

```typescript
const result = await authClient.sigma.handleCallback(searchParams);
// result contains { access_token, user, ... } - store manually
```

#### 5. Sign-In Component

```typescript
"use client";
import { signIn } from "@/lib/auth-client";

export function SignInButton() {
  return (
    <button onClick={() => signIn.sigma({
      clientId: process.env.NEXT_PUBLIC_SIGMA_CLIENT_ID!,
      // callbackURL defaults to /auth/sigma/callback
    })}>
      Sign in with Sigma
    </button>
  );
}
```

---

### Mode B — Same-Domain Better Auth Server (Prisma/Convex/Other)

Use this when your app runs Better Auth on the **same domain** (or proxies to it).
If you're using **Convex**, follow `setup-convex` for the exact wiring.

#### 1. Environment Variables (`.env.local`)

```bash
NEXT_PUBLIC_SIGMA_CLIENT_ID=your-app-name
NEXT_PUBLIC_SIGMA_AUTH_URL=https://auth.sigmaidentity.com
SIGMA_MEMBER_PRIVATE_KEY=your-member-wif-key
```

#### 2. Server Configuration (`lib/auth.ts`)

Add `sigmaCallbackPlugin` to your Better Auth server config. It registers `POST /sigma/callback` inside Better Auth.

```typescript
import { betterAuth } from "better-auth";
import { sigmaCallbackPlugin } from "@sigma-auth/better-auth-plugin/server";

export const auth = betterAuth({
  plugins: [
    sigmaCallbackPlugin({
      // Optional overrides (defaults to env vars)
      // clientId: process.env.NEXT_PUBLIC_SIGMA_CLIENT_ID,
      // memberPrivateKey: process.env.SIGMA_MEMBER_PRIVATE_KEY,
    })
  ],
  // ... other config (database, etc.)
});
```

#### 3. API Route (`app/api/auth/[...all]/route.ts`)

Expose Better Auth in Next.js. The plugin endpoint becomes `/api/auth/sigma/callback`.

```typescript
import { toNextJsHandler } from "better-auth/next-js";
import { auth } from "@/lib/auth";

export const { POST, GET } = toNextJsHandler(auth);
```

#### 4. Client Configuration (`lib/auth-client.ts`)

```typescript
import { createAuthClient } from "better-auth/react";
import { sigmaClient } from "@sigma-auth/better-auth-plugin/client";

export const authClient = createAuthClient({
  baseURL: "/api/auth",
  plugins: [sigmaClient()],
});

export const { signIn, useSession } = authClient;
```

#### 5. OAuth Callback Page (`app/auth/sigma/callback/page.tsx`)

Still required because OAuth redirects are GETs. In this mode you can rely on session cookies instead of storing tokens manually.

---

## Troubleshooting

### 403 on Token Exchange (CSRF / trustedOrigins)

**Symptom**: OAuth flow succeeds (user authenticates, code is returned in redirect), but the callback page shows "Token Exchange Failed - Server returned 403". Better Auth logs: `Invalid origin: https://your-preview-url.vercel.app`

**Root Cause**: Better Auth's CSRF protection rejects POST requests from origins not listed in `trustedOrigins`. This commonly happens on Vercel preview deployments (e.g. `your-app-git-branch-team.vercel.app`) which have dynamic URLs that don't match your hardcoded production domain.

**Fix (Mode B)**: Add Vercel's auto-set environment variables to your `trustedOrigins` in `lib/auth.ts`:

```typescript
const vercelUrl = process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : "";
const vercelBranchUrl = process.env.VERCEL_BRANCH_URL
  ? `https://${process.env.VERCEL_BRANCH_URL}`
  : "";

export const auth = betterAuth({
  trustedOrigins: [
    "https://your-production-domain.com",
    vercelUrl,
    vercelBranchUrl,
    "http://localhost:3000",
  ].filter(Boolean),
  // ...
});
```

`VERCEL_URL` and `VERCEL_BRANCH_URL` are automatically set by Vercel on every deployment (without the `https://` protocol prefix). This covers all preview, branch, and production deployments.

**Fix (Mode A)**: If using the standalone `createCallbackHandler()`, the POST to your own `/api/auth/sigma/callback` route may also be subject to your framework's CSRF protections. Ensure the callback origin is trusted.

**Important**: This is a Better Auth configuration issue, not a Sigma plugin issue. The OAuth flow (redirect to Sigma, user auth, redirect back with code) works correctly. The 403 happens on the subsequent local POST that exchanges the code for tokens.

### Missing Environment Variables

Run the validation script to check all required env vars:

```bash
bun run scripts/validate-env.ts
```

Required variables:
- `NEXT_PUBLIC_SIGMA_CLIENT_ID` - Your app's client ID registered with Sigma
- `NEXT_PUBLIC_SIGMA_AUTH_URL` - The Sigma auth server URL (e.g. `https://auth.sigmaidentity.com`)
- `SIGMA_MEMBER_PRIVATE_KEY` - Server-only WIF key for signing token exchange requests

### Callback URL Mismatch

**Symptom**: OAuth redirect fails or returns an error before reaching your callback page.

**Root Cause**: The redirect URI sent during the OAuth flow doesn't match the allowed callback URLs configured in your Sigma client registration.

**Fix**: Ensure your callback URL is registered in Sigma for every domain you deploy to:
- `http://localhost:3000/auth/sigma/callback` (local dev)
- `https://your-domain.com/auth/sigma/callback` (production)
- `https://your-app-git-branch-team.vercel.app/auth/sigma/callback` (Vercel previews)

### auth-client baseURL Misconfiguration

**Symptom**: Sign-in button does nothing, or token exchange POSTs go to the wrong URL.

**Root Cause**: The `baseURL` in `createAuthClient()` must point to your own app's API routes, not the Sigma auth server.

```typescript
// Mode A: Points to YOUR app's API routes
export const authClient = createAuthClient({
  baseURL: "/api/auth", // Relative to your app
  plugins: [sigmaClient()],
});

// Mode B: Same pattern - YOUR app serves Better Auth
export const authClient = createAuthClient({
  baseURL: "/api/auth", // Relative to your app
  plugins: [sigmaClient()],
});
```

### 400 "Missing a required credential value" (PKCE code_verifier)

**Symptom**: OAuth flow reaches the callback page, the callback handler calls the auth server's token endpoint, but gets 400: `"Missing a required credential value for authorization_code grant"`.

**Root Cause**: The auth server's `@better-auth/oauth-provider` requires either `code_verifier` (PKCE) or `client_secret` for the authorization_code grant. The sigma plugin uses PKCE, storing `code_verifier` in sessionStorage during `signIn.sigma()` and reading it back in `handleCallback()`. If the verifier is missing from the token exchange, this error occurs.

**Common causes:**
1. **Cross-domain detection failure** (fixed in v0.0.74): Plugin v0.0.73 used `String.includes()` which incorrectly matched subdomains (`"auth.sigmaidentity.com".includes("sigmaidentity.com")` = true). This made the plugin think it was same-domain when it was cross-domain, causing it to use `$fetch` instead of the local API proxy.
2. **Mode B baseURL remnant**: If `createAuthClient({ baseURL: 'https://auth.sigmaidentity.com' })` is set (Mode B pattern), Better Auth's `$fetch` calls go to the auth server. While this doesn't directly affect PKCE (handleCallback uses native `fetch` for cross-domain), it can cause other issues.
3. **sessionStorage cleared**: The code_verifier is stored in sessionStorage which is per-origin and per-tab. If the sign-in opens in a different tab or the session is cleared, the verifier is lost.

**Fix**: Ensure plugin is v0.0.74+, remove any `baseURL` pointing to the auth server, and verify the callback handler logs show `hasCodeVerifier: true`.

### Migrating from Mode B to Mode A

**Symptom**: Various auth failures after switching from same-domain (Mode B) to cross-domain (Mode A) OAuth.

**Common leftover issues:**
1. **`baseURL` still pointing to auth server**: In Mode A, either omit `baseURL` (defaults to current origin) or set it to your app's own API path (e.g., `/api/auth`). Never point it to the auth server for Mode A.
2. **Missing API route**: Mode A requires `app/api/auth/sigma/callback/route.ts` with `createCallbackHandler()`. Mode B uses Better Auth's built-in routing.
3. **Catch-all route conflict**: If you had `app/api/auth/[...all]/route.ts` for Mode B, it may conflict with the explicit `app/api/auth/sigma/callback/route.ts` in Mode A. Remove the catch-all or ensure the explicit route takes precedence.
4. **`signOut()` calling auth server**: `authClient.signOut()` uses the `baseURL`. In Mode A, this should go to your app (or be handled locally), not the auth server.

**Checklist for Mode B to Mode A migration:**
- [ ] Remove `baseURL` from `createAuthClient()` (or set to own app URL)
- [ ] Add `app/api/auth/sigma/callback/route.ts` with `createCallbackHandler()`
- [ ] Remove `app/api/auth/[...all]/route.ts` (if it was for Mode B)
- [ ] Remove server-side `betterAuth()` config and `sigmaCallbackPlugin` (not needed in Mode A)
- [ ] Update sign-out to clear local state only (no server session to invalidate in Mode A)
- [ ] Verify `NEXT_PUBLIC_SIGMA_CLIENT_ID` and `SIGMA_MEMBER_PRIVATE_KEY` env vars are set

### Plugin Version Pinning

**Symptom**: After updating the plugin, `node_modules` still has the old version.

**Root Cause**: Bun's lockfile or cache may resolve to an older version, especially with caret (`^`) ranges.

**Fix**: Pin the exact version in package.json (no caret):
```json
"@sigma-auth/better-auth-plugin": "0.0.74"
```

Then run:
```bash
bun add @sigma-auth/better-auth-plugin@0.0.74
```

Verify with:
```bash
cat node_modules/@sigma-auth/better-auth-plugin/package.json | grep version
```

### React Hooks Violation in Callback Page

**Symptom**: React error about hooks being called conditionally, or callback page not rendering properly.

**Root Cause**: `useState` or other hooks called inside conditional blocks (e.g., `if (error) { const [copied, setCopied] = useState(false); }`). This violates the Rules of Hooks.

**Fix**: Move ALL hooks to the top level of the component function. Use conditional rendering in JSX instead of conditional hook calls.

## Security Considerations

- **Environment Variables**: Never expose `SIGMA_MEMBER_PRIVATE_KEY` to the client. It is required only on the server for signing token exchange requests.
- **Token Storage**: In Mode A, store tokens securely (avoid `localStorage` for refresh tokens in production).
- **Same-Domain Sessions**: `useSession` only works when your auth server is on the same domain (Mode B).
- **Wallet Unlock Gate**: Plugin ensures wallet access before authentication (session -> local backup -> cloud backup -> signup).
- **PKCE**: The client plugin automatically handles PKCE (Proof Key for Code Exchange) for secure OAuth flows.

## BRC-100 Wallet Compatibility

BAP key derivation uses **BRC-42 (Type42 BKDS)** and **BRC-43 (security levels, protocol IDs)** — the same key derivation primitives as the BRC-100 unified wallet standard. This means:

- BAP identities are compatible with any BRC-100 conformant wallet
- The signing key invoice number follows BRC-43 format: `{securityLevel}-{protocolID}-{keyID}`
- Future embedded wallet support will use `@bsv/wallet-toolbox` (BRC-100 reference implementation)
- BRC-52 identity certificates can attest attributes about BAP identities

## Reference

Full documentation: https://github.com/b-open-io/better-auth-plugin
