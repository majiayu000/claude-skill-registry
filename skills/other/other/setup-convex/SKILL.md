---
name: setup-convex
description: Setup Sigma Auth OAuth integration in a Convex application. Guides through installing @sigma-auth/better-auth-plugin, configuring Convex environment variables, and setting up the auth server.
allowed-tools: "Bash(bun:*)"
---

# Setup Convex with Sigma Auth

Guide for integrating Sigma Auth (Bitcoin-native authentication) into a Convex application using the `@sigma-auth/better-auth-plugin` package with `@convex-dev/better-auth`.

> For general Better Auth concepts (session management, plugins, hooks), see `Skill(better-auth-best-practices)`. This skill covers Convex + Sigma specific wiring and deployment pitfalls.

## When to Use

- Building a Convex backend with Better Auth
- Adding Bitcoin-native auth to a Convex app
- Implementing OAuth flow with auth.sigmaidentity.com
- Integrating BAP (Bitcoin Attestation Protocol) identity
- If you are **not** using Convex, follow Mode B in `setup-nextjs` instead

## Installation

```bash
bun add @convex-dev/better-auth@0.10.10 better-auth@1.4.9 @sigma-auth/better-auth-plugin
```

> `@convex-dev/better-auth@0.10.10` has a strict peer dependency on `better-auth@1.4.9`.

## Quick Start

### 1. Convex Component Registration (`convex/convex.config.ts`)

Register the Better Auth component. Its tables (user, session, account, verification) are isolated from your app tables.

```typescript
import betterAuth from "@convex-dev/better-auth/convex.config";
import { defineApp } from "convex/server";

const app = defineApp();
app.use(betterAuth);

export default app;
```

### 2. Convex Auth Config (`convex/auth.config.ts`)

```typescript
import { getAuthConfigProvider } from "@convex-dev/better-auth/auth-config";
import type { AuthConfig } from "convex/server";

export default {
  providers: [getAuthConfigProvider()],
} satisfies AuthConfig;
```

### 3. Environment Variables

**Next.js app (`.env.local`)**

```bash
NEXT_PUBLIC_CONVEX_URL=https://your-deployment.convex.cloud
NEXT_PUBLIC_CONVEX_SITE_URL=https://your-deployment.convex.site
NEXT_PUBLIC_SIGMA_CLIENT_ID=your-app-name
NEXT_PUBLIC_SIGMA_AUTH_URL=https://auth.sigmaidentity.com
```

**Convex deployment (CLI)**

```bash
npx convex env set BETTER_AUTH_URL "https://your-site-url"
npx convex env set BETTER_AUTH_SECRET "your-random-secret"
npx convex env set NEXT_PUBLIC_SIGMA_CLIENT_ID "your-app-name"
npx convex env set NEXT_PUBLIC_SIGMA_AUTH_URL "https://auth.sigmaidentity.com"
npx convex env set SIGMA_MEMBER_PRIVATE_KEY "your-member-wif-key"
```

> Use `--prod` for production: `npx convex env set VAR "value" --prod`

### 4. Server Configuration (`convex/auth.ts`)

Add the `sigmaCallbackPlugin` to your Better Auth server configuration. This runs inside the Convex environment.

```typescript
import { createClient, type GenericCtx } from "@convex-dev/better-auth";
import { convex } from "@convex-dev/better-auth/plugins";
import { sigmaCallbackPlugin } from "@sigma-auth/better-auth-plugin/server";
import { betterAuth } from "better-auth/minimal";
import { components } from "./_generated/api";
import type { DataModel } from "./_generated/dataModel";
import { query } from "./_generated/server";
import authConfig from "./auth.config";

export const authComponent = createClient<DataModel>(components.betterAuth);

export const createAuth = (ctx: GenericCtx<DataModel>) => {
  const siteUrl = process.env.BETTER_AUTH_URL!;

  return betterAuth({
    baseURL: siteUrl,
    secret: process.env.BETTER_AUTH_SECRET,
    database: authComponent.adapter(ctx),
    trustedOrigins: [siteUrl],
    plugins: [
      convex({ authConfig }),
      sigmaCallbackPlugin(),
    ],
  });
};

export const getCurrentUser = query({
  args: {},
  handler: async (ctx) => {
    return authComponent.getAuthUser(ctx);
  },
});
```

> **Important**: Use `"better-auth/minimal"` (NOT `"better-auth"`) for the Convex runtime.

### 5. Next.js Auth Handler (`lib/auth-server.ts`)

Proxy `/api/auth/*` requests to Convex.

```typescript
import { convexBetterAuthNextJs } from "@convex-dev/better-auth/nextjs";

const convexUrl = process.env.NEXT_PUBLIC_CONVEX_URL!;
const convexSiteUrl = process.env.NEXT_PUBLIC_CONVEX_SITE_URL!;

export const {
  handler,
  preloadAuthQuery,
  isAuthenticated,
  getToken,
  fetchAuthQuery,
  fetchAuthMutation,
  fetchAuthAction,
} = convexBetterAuthNextJs({ convexUrl, convexSiteUrl });
```

### 6. API Route (`app/api/auth/[...all]/route.ts`)

```typescript
import { handler } from "@/lib/auth-server";

export const { GET, POST } = handler;
```

### 7. Client Configuration (`lib/auth-client.ts`)

```typescript
import { convexClient } from "@convex-dev/better-auth/client/plugins";
import { sigmaClient } from "@sigma-auth/better-auth-plugin/client";
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  plugins: [convexClient(), sigmaClient()],
});

export const { signIn, signOut, useSession } = authClient;
```

### 8. Convex Provider (`components/convex-provider.tsx`)

Replace the standard `ConvexProvider` with the auth-aware provider.

```typescript
"use client";

import { ConvexBetterAuthProvider } from "@convex-dev/better-auth/react";
import { ConvexReactClient } from "convex/react";
import type { ReactNode } from "react";
import { authClient } from "@/lib/auth-client";

const convexUrl = process.env.NEXT_PUBLIC_CONVEX_URL!;
const convex = new ConvexReactClient(convexUrl);

export function ConvexClientProvider({
  children,
  initialToken,
}: {
  children: ReactNode;
  initialToken?: string | null;
}) {
  return (
    <ConvexBetterAuthProvider
      client={convex}
      authClient={authClient}
      initialToken={initialToken}
    >
      {children}
    </ConvexBetterAuthProvider>
  );
}
```

### 9. Sign-In Component

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

## How It Works

1. **Client**: The `sigmaClient` initiates the OAuth flow, redirecting to `auth.sigmaidentity.com`.
2. **Next.js Proxy**: The `convexBetterAuthNextJs` handler proxies `/api/auth/*` requests to Convex HTTP actions.
3. **Convex Plugin**: The `sigmaCallbackPlugin` running in Convex:
   - Intercepts the callback.
   - Exchanges the authorization code for tokens using the server-side `SIGMA_MEMBER_PRIVATE_KEY`.
   - Creates or updates the user in the Convex database (via Better Auth's internal adapter).
   - Establishes a session.
4. **Session**: The `ConvexBetterAuthProvider` reads session state and provides it to your app via `useSession()`.

## Local Install (Admin & Organization Plugins)

The default "supported plugins" for `@convex-dev/better-auth` do **not** include `admin` or `organization`. To use these plugins, you must use the **Local Install** approach, which replaces the npm component with a local component definition that you control.

Full documentation: https://labs.convex.dev/better-auth/features/local-install

### Why Local Install?

The standard `@convex-dev/better-auth` component ships a fixed schema. Plugins like `admin` and `organization` add additional tables and fields that the standard component does not know about. The local install lets you generate a schema that includes these plugin tables, then wire up the adapter yourself.

### Step-by-Step

#### a. Create Local Component Config (`convex/betterAuth/convex.config.ts`)

Replace the npm component with a local component definition:

```typescript
import { defineComponent } from "convex/server";
const component = defineComponent("betterAuth");
export default component;
```

#### b. Update App Config (`convex/convex.config.ts`)

Point the app at your local component instead of the npm package:

```typescript
import { defineApp } from "convex/server";
import betterAuth from "./betterAuth/convex.config";

const app = defineApp();
app.use(betterAuth);

export default app;
```

#### c. Refactor Auth Config (`convex/auth.ts`)

Split into two functions: `createAuthOptions` (safe for module-load analysis) and `createAuth` (validates env vars at runtime).

**Critical pattern -- `env()` vs `must()`**: The `createApi` call in the adapter imports `createAuthOptions` at module load time, before Convex env vars are available. If `createAuthOptions` throws on a missing env var, the push will fail. Use an `env()` helper that returns `""` instead of throwing. The `createAuth` function runs at request time, so it can validate with `must()`.

```typescript
import { createClient, type GenericCtx } from "@convex-dev/better-auth";
import { convex } from "@convex-dev/better-auth/plugins";
import { sigmaCallbackPlugin } from "@sigma-auth/better-auth-plugin/server";
import { betterAuth } from "better-auth/minimal";
import { admin } from "better-auth/plugins/admin";
import { organization } from "better-auth/plugins/organization";
import { components } from "./_generated/api";
import type { DataModel } from "./_generated/dataModel";
import { query } from "./_generated/server";
import authConfig from "./auth.config";
import authSchema from "./betterAuth/schema";

// Returns "" instead of throwing -- safe for module-load analysis
function env(name: string): string {
  return process.env[name] ?? "";
}

// Throws if missing -- use only at request time
function must(name: string): string {
  const v = process.env[name];
  if (!v) throw new Error(`Missing env var: ${name}`);
  return v;
}

export const authComponent = createClient<DataModel, typeof authSchema>(
  components.betterAuth,
  { local: { schema: authSchema } },
);

// Safe for module-load: never throws on missing env vars
export function createAuthOptions(ctx?: GenericCtx<DataModel>) {
  const siteUrl = env("BETTER_AUTH_URL");
  return {
    baseURL: siteUrl,
    secret: env("BETTER_AUTH_SECRET"),
    database: ctx ? authComponent.adapter(ctx) : undefined,
    trustedOrigins: [siteUrl, "http://localhost:3000"].filter(Boolean),
    plugins: [
      convex({ authConfig }),
      sigmaCallbackPlugin(),
      admin(),
      organization(),
    ],
  };
}

// Request-time only: validates env vars, then creates the auth instance
export const createAuth = (ctx: GenericCtx<DataModel>) => {
  must("BETTER_AUTH_URL");
  must("BETTER_AUTH_SECRET");
  return betterAuth({
    ...createAuthOptions(ctx),
    database: authComponent.adapter(ctx),
  });
};

export const getCurrentUser = query({
  args: {},
  handler: async (ctx) => {
    return authComponent.getAuthUser(ctx);
  },
});
```

#### d. Generate the Schema

Create a temporary file `convex/betterAuth/auth.ts` for schema generation:

```typescript
import { createAuth } from "../auth";
export const auth = createAuth({} as any);
```

Then generate the schema:

```bash
cd convex/betterAuth
BETTER_AUTH_URL=http://localhost:3000 BETTER_AUTH_SECRET=dummy npx @better-auth/cli generate -y
```

**Delete the temporary file immediately after generation:**

```bash
rm convex/betterAuth/auth.ts
```

> Convex analyzes all `.ts` files in the `convex/` tree at push time. If `auth.ts` remains, the push will fail because `createAuth({} as any)` triggers env var access during module analysis.

#### e. Create the Adapter (`convex/betterAuth/adapter.ts`)

Wire the generated schema to the auth options:

```typescript
import { createApi } from "@convex-dev/better-auth";
import { createAuthOptions } from "../auth";
import schema from "./schema";

export const {
  create,
  findOne,
  findMany,
  updateOne,
  updateMany,
  deleteOne,
  deleteMany,
} = createApi(schema, createAuthOptions);
```

#### f. Client-Side Plugins (`lib/auth-client.ts`)

Add the admin and organization client plugins:

```typescript
import { convexClient } from "@convex-dev/better-auth/client/plugins";
import { sigmaClient } from "@sigma-auth/better-auth-plugin/client";
import { createAuthClient } from "better-auth/react";
import { adminClient } from "better-auth/client/plugins";
import { organizationClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [
    convexClient(),
    sigmaClient(),
    adminClient(),
    organizationClient(),
  ],
});

export const { signIn, signOut, useSession } = authClient;
```

### Regenerating the Schema After Plugin Changes

Whenever you add, remove, or update plugins, regenerate the schema:

```bash
# Re-create the temporary auth.ts
cat > convex/betterAuth/auth.ts << 'EOF'
import { createAuth } from "../auth";
export const auth = createAuth({} as any);
EOF

# Generate
cd convex/betterAuth
BETTER_AUTH_URL=http://localhost:3000 BETTER_AUTH_SECRET=dummy npx @better-auth/cli generate -y

# Clean up
rm convex/betterAuth/auth.ts
```

## Critical Deployment Checklist

Before going live, verify ALL of these. Missing any one causes silent auth failures:

### 1. Understand the Two Convex URLs (They Are Different!)

| Variable | Value | Purpose |
|----------|-------|---------|
| `NEXT_PUBLIC_CONVEX_URL` | `https://<deployment>.convex.cloud` | Client SDK connection (queries, mutations, subscriptions) |
| `NEXT_PUBLIC_CONVEX_SITE_URL` | `https://<deployment>.convex.site` | HTTP actions URL (auth proxy forwards requests here) |

**CRITICAL**: `NEXT_PUBLIC_CONVEX_SITE_URL` must be the `.convex.site` URL. If you set it to your app domain (e.g., `https://myapp.com`), the auth proxy (`convexBetterAuthNextJs`) will loop back to itself instead of forwarding to Convex. This causes infinite redirects or timeouts during sign-in.

### 2. Set ALL Env Vars on Convex PRODUCTION

`bunx convex env set` targets the **DEV** deployment by default. Production requires `--prod`:

```bash
# PRODUCTION (the deployed app uses these)
bunx convex env set BETTER_AUTH_URL "https://your-domain.com" --prod
bunx convex env set BETTER_AUTH_SECRET "$(openssl rand -hex 32)" --prod
bunx convex env set NEXT_PUBLIC_SIGMA_CLIENT_ID "your-app-name" --prod
bunx convex env set NEXT_PUBLIC_SIGMA_AUTH_URL "https://auth.sigmaidentity.com" --prod
bunx convex env set SIGMA_MEMBER_PRIVATE_KEY "your-wif-key" --prod

# Verify they're actually set
bunx convex env list --prod
```

Without `--prod`, your production app has NO env vars and auth silently fails.

### 3. Deploy Convex Functions to Production

Running `bunx convex dev` only pushes functions to the dev deployment. Production needs:

```bash
bunx convex deploy --yes
```

Without this, your production Convex deployment has no functions, queries, or HTTP actions.

### 4. Set Vercel Env Vars Correctly

On Vercel (Settings > Environment Variables), set:

```
NEXT_PUBLIC_CONVEX_URL=https://<deployment>.convex.cloud
NEXT_PUBLIC_CONVEX_SITE_URL=https://<deployment>.convex.site
```

**Common mistake**: Setting `NEXT_PUBLIC_CONVEX_SITE_URL` to your app domain (`https://myapp.com`). This breaks the auth proxy.

### 5. Better Auth `baseURL` = Your App Domain

In `convex/auth.ts`, `baseURL` (from `BETTER_AUTH_URL`) must be your user-facing domain:

```typescript
baseURL: process.env.BETTER_AUTH_URL, // e.g., "https://myapp.com"
```

NOT the `.convex.site` URL. This is used for OAuth redirect URIs.

### 6. Use Lazy Handler Initialization

The auth route handler must defer env var access to request time:

```typescript
// src/app/api/auth/[...all]/route.ts
import { convexBetterAuthNextJs } from "@convex-dev/better-auth/nextjs";

function createHandler() {
  const convexUrl = process.env.NEXT_PUBLIC_CONVEX_URL;
  const convexSiteUrl = process.env.NEXT_PUBLIC_CONVEX_SITE_URL;
  if (!convexUrl || !convexSiteUrl) {
    throw new Error(
      "NEXT_PUBLIC_CONVEX_URL and NEXT_PUBLIC_CONVEX_SITE_URL must be set",
    );
  }
  return convexBetterAuthNextJs({ convexUrl, convexSiteUrl }).handler;
}

export const GET = async (req: Request) => {
  const { GET } = createHandler();
  return GET(req);
};

export const POST = async (req: Request) => {
  const { POST } = createHandler();
  return POST(req);
};
```

Without this, `convexBetterAuthNextJs` throws at build time when env vars aren't available yet.

### 7. Auth UI Must Exist

A bare sign-in button is not sufficient. Set up proper auth pages:

```bash
bunx shadcn@latest add login-05 signup-05
```

Then adapt for Sigma auth: remove email/password fields, keep the branded layout. Use your project logo, not the default icons.

Also add sign-in/sign-out controls to the app shell (sidebar footer, header) so users can access auth from anywhere.

### 8. Protect Routes from Unauthenticated Access

Don't blindly redirect unauthenticated users into the app. Use Next.js middleware to check auth and redirect to `/login`. See `Skill(better-auth-best-practices)` for the middleware pattern. Key: use `betterFetch("/api/auth/get-session", { baseURL: request.nextUrl.origin })` and match all routes except `api`, `_next`, `login`, `signup`.

---

## Troubleshooting

### 403 on Token Exchange (CSRF / trustedOrigins)

**Symptom**: OAuth flow succeeds but callback returns "Token Exchange Failed - Server returned 403". Better Auth logs: `Invalid origin: https://your-preview-url.vercel.app`

**Root Cause**: Better Auth's CSRF protection rejects POST requests from origins not in `trustedOrigins`. This is common on Vercel preview deployments with dynamic URLs.

**Fix**: Add Vercel's auto-set env vars to your Better Auth config's `trustedOrigins` in `convex/auth.ts`. You'll need to set `VERCEL_URL` and `VERCEL_BRANCH_URL` as Convex env vars (Convex doesn't get these automatically like Vercel does):

```typescript
trustedOrigins: [
  siteUrl,
  process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "",
  process.env.VERCEL_BRANCH_URL ? `https://${process.env.VERCEL_BRANCH_URL}` : "",
  "http://localhost:3000",
].filter(Boolean),
```

### Missing Convex Env Vars

Convex env vars are separate from Vercel env vars. Set them with:

```bash
npx convex env set VAR_NAME "value"          # Dev deployment
npx convex env set VAR_NAME "value" --prod   # Production deployment
npx convex env list                          # Verify dev
npx convex env list --prod                   # Verify production
```

### Callback URL Mismatch

Ensure your callback URL is registered in Sigma for every domain you deploy to:
- `http://localhost:3000/auth/sigma/callback` (local dev)
- `https://your-domain.com/auth/sigma/callback` (production)
- Vercel preview URLs as needed

## Security

- **Private Key**: The `SIGMA_MEMBER_PRIVATE_KEY` is critical for signing token exchange requests. Ensure it is stored securely in Convex environment variables and never exposed to the client.
- **PKCE**: Handled automatically by the client/server plugin combination.
- **Component Isolation**: Better Auth tables (user, session, account, verification) are isolated from your app tables via the Convex component system.

## Reference

Full documentation: https://github.com/b-open-io/better-auth-plugin
