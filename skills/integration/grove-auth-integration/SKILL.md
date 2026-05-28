---
name: grove-auth-integration
description: Integrate Heartwood authentication into a new or existing Grove property. Covers client registration, PKCE OAuth flow, SvelteKit route setup, session validation, and wrangler configuration. Use when adding auth to any Grove site.
---

# Grove Auth Integration

Add Heartwood authentication to a Grove property — from client registration through production deployment.

## When to Activate

- User says "add auth to this project" or "wire up Heartwood"
- User is building a new Grove property that needs login
- User needs to register a new OAuth client with Heartwood
- User explicitly calls `/grove-auth-integration`
- User mentions needing sign-in, protected routes, or session validation
- User says "integrate GroveAuth" or "add login"

---

## Key URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Login UI** | `https://heartwood.grove.place` | Where users authenticate |
| **API** | `https://auth-api.grove.place` | Token exchange, verify, sessions |
| **D1 Database** | `groveauth` (via wrangler) | Client registration |

---

## The Pipeline

```
Identify → Register Client → Configure Secrets → Write Code → Wire Wrangler → Test
```

---

### Step 1: Identify the Integration

Ask the user (or determine from context):

1. **Project name** — The Cloudflare Pages/Workers project name
2. **Client ID** — A simple slug (e.g., `grove-plant`, `grove-domains`, `arbor-admin`)
3. **Site URL** — Production URL (e.g., `https://plant.grove.place`)
4. **Callback path** — Usually `/auth/callback`
5. **Project type** — SvelteKit Pages (most common), Workers, or other
6. **Session approach** — OAuth tokens (standard) or SessionDO (faster, same-account only)

---

### Step 2: Register the OAuth Client

#### 2a. Generate client secret

```bash
CLIENT_SECRET=$(openssl rand -base64 32)
echo "Client Secret: $CLIENT_SECRET"
```

Save this value — you'll need it for both the client secrets AND the database hash.

#### 2b. Generate base64url hash

**CRITICAL**: Heartwood uses **base64url encoding** — dashes (`-`), underscores (`_`), NO padding (`=`).

```bash
CLIENT_SECRET_HASH=$(echo -n "$CLIENT_SECRET" | openssl dgst -sha256 -binary | base64 | tr '+/' '-_' | tr -d '=')
echo "Secret Hash: $CLIENT_SECRET_HASH"
```

| Format | Example | Correct? |
|--------|---------|----------|
| **base64url** | `Sdgtaokie8-H7GKw-tn0S_6XNSh1rdv` | YES |
| base64 | `Sdgtaokie8+H7GKw+tn0S/6XNSh1rdv=` | NO |
| hex | `49d82d6a89227bcf87ec62b0...` | NO |

#### 2c. Insert into Heartwood database

```bash
wrangler d1 execute groveauth --remote --command="
INSERT INTO clients (id, name, client_id, client_secret_hash, redirect_uris, allowed_origins)
VALUES (
  '$(uuidgen | tr '[:upper:]' '[:lower:]')',
  'DISPLAY_NAME',
  'CLIENT_ID',
  'BASE64URL_HASH',
  '[\"https://SITE_URL/auth/callback\", \"http://localhost:5173/auth/callback\"]',
  '[\"https://SITE_URL\", \"http://localhost:5173\"]'
)
ON CONFLICT(client_id) DO UPDATE SET
  client_secret_hash = excluded.client_secret_hash,
  redirect_uris = excluded.redirect_uris,
  allowed_origins = excluded.allowed_origins;
"
```

**Always include localhost** in redirect_uris and allowed_origins for development.

---

### Step 3: Configure Secrets on the Client

#### For Pages projects (SvelteKit):

```bash
echo "CLIENT_ID" | wrangler pages secret put GROVEAUTH_CLIENT_ID --project PROJECT_NAME
echo "CLIENT_SECRET" | wrangler pages secret put GROVEAUTH_CLIENT_SECRET --project PROJECT_NAME
echo "https://SITE_URL/auth/callback" | wrangler pages secret put GROVEAUTH_REDIRECT_URI --project PROJECT_NAME
echo "https://auth-api.grove.place" | wrangler pages secret put GROVEAUTH_URL --project PROJECT_NAME
```

#### For Workers projects:

```bash
cd worker-directory
echo "CLIENT_ID" | wrangler secret put GROVEAUTH_CLIENT_ID
echo "CLIENT_SECRET" | wrangler secret put GROVEAUTH_CLIENT_SECRET
```

---

### Step 4: Write the Auth Code (SvelteKit)

Create these files in the SvelteKit project:

#### 4a. Login initiation route: `src/routes/auth/+server.ts`

```typescript
/**
 * OAuth Initiation - Start Heartwood OAuth flow
 * Redirects to GroveAuth with PKCE parameters.
 */
import { redirect } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

function generateRandomString(length: number): string {
  const charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~";
  const randomValues = crypto.getRandomValues(new Uint8Array(length));
  return Array.from(randomValues, (v) => charset[v % charset.length]).join("");
}

async function generatePKCE(): Promise<{ verifier: string; challenge: string }> {
  const verifier = generateRandomString(64);
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const hash = await crypto.subtle.digest("SHA-256", data);
  const challenge = btoa(String.fromCharCode(...new Uint8Array(hash)))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=/g, "");
  return { verifier, challenge };
}

export const GET: RequestHandler = async ({ url, cookies, platform }) => {
  const env = platform?.env as Record<string, string> | undefined;
  const authBaseUrl = env?.GROVEAUTH_URL || "https://auth-api.grove.place";
  const clientId = env?.GROVEAUTH_CLIENT_ID || "YOUR_CLIENT_ID";
  const appBaseUrl = env?.PUBLIC_APP_URL || "https://YOUR_SITE_URL";
  const redirectUri = `${appBaseUrl}/auth/callback`;

  const { verifier, challenge } = await generatePKCE();
  const state = generateRandomString(32);

  const isProduction = url.hostname !== "localhost" && url.hostname !== "127.0.0.1";
  const cookieOptions = {
    path: "/",
    httpOnly: true,
    secure: isProduction,
    sameSite: "lax" as const,
    maxAge: 60 * 10, // 10 minutes
  };

  cookies.set("auth_state", state, cookieOptions);
  cookies.set("auth_code_verifier", verifier, cookieOptions);

  const authUrl = new URL(`${authBaseUrl}/login`);
  authUrl.searchParams.set("client_id", clientId);
  authUrl.searchParams.set("redirect_uri", redirectUri);
  authUrl.searchParams.set("response_type", "code");
  authUrl.searchParams.set("scope", "openid profile email");
  authUrl.searchParams.set("state", state);
  authUrl.searchParams.set("code_challenge", challenge);
  authUrl.searchParams.set("code_challenge_method", "S256");

  redirect(302, authUrl.toString());
};
```

#### 4b. Callback handler: `src/routes/auth/callback/+server.ts`

```typescript
/**
 * OAuth Callback - Handle Heartwood OAuth response
 * Exchanges authorization code for tokens and creates session.
 */
import { redirect } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

export const GET: RequestHandler = async ({ url, cookies, platform }) => {
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const errorParam = url.searchParams.get("error");

  if (errorParam) {
    redirect(302, `/?error=${encodeURIComponent(errorParam)}`);
  }

  // Validate state (CSRF protection)
  const savedState = cookies.get("auth_state");
  if (!state || state !== savedState) {
    redirect(302, "/?error=invalid_state");
  }

  // Get PKCE verifier
  const codeVerifier = cookies.get("auth_code_verifier");
  if (!codeVerifier || !code) {
    redirect(302, "/?error=missing_credentials");
  }

  // Clear auth cookies immediately
  cookies.delete("auth_state", { path: "/" });
  cookies.delete("auth_code_verifier", { path: "/" });

  const env = platform?.env as Record<string, string> | undefined;
  const authBaseUrl = env?.GROVEAUTH_URL || "https://auth-api.grove.place";
  const clientId = env?.GROVEAUTH_CLIENT_ID || "YOUR_CLIENT_ID";
  const clientSecret = env?.GROVEAUTH_CLIENT_SECRET || "";
  const appBaseUrl = env?.PUBLIC_APP_URL || "https://YOUR_SITE_URL";
  const redirectUri = `${appBaseUrl}/auth/callback`;

  try {
    // Exchange code for tokens
    const tokenResponse = await fetch(`${authBaseUrl}/token`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        grant_type: "authorization_code",
        code,
        redirect_uri: redirectUri,
        client_id: clientId,
        client_secret: clientSecret,
        code_verifier: codeVerifier,
      }),
    });

    if (!tokenResponse.ok) {
      redirect(302, "/?error=token_exchange_failed");
    }

    const tokens = await tokenResponse.json() as {
      access_token: string;
      refresh_token?: string;
      expires_in?: number;
    };

    // Fetch user info
    const userinfoResponse = await fetch(`${authBaseUrl}/userinfo`, {
      headers: { Authorization: `Bearer ${tokens.access_token}` },
    });

    if (!userinfoResponse.ok) {
      redirect(302, "/?error=userinfo_failed");
    }

    const userinfo = await userinfoResponse.json() as {
      sub?: string;
      id?: string;
      email: string;
      name?: string;
      email_verified?: boolean;
    };

    const userId = userinfo.sub || userinfo.id;
    const email = userinfo.email;

    if (!userId || !email) {
      redirect(302, "/?error=incomplete_profile");
    }

    // Set session cookies
    const isProduction = url.hostname !== "localhost" && url.hostname !== "127.0.0.1";
    const cookieOptions = {
      path: "/",
      httpOnly: true,
      secure: isProduction,
      sameSite: "lax" as const,
      maxAge: 60 * 60 * 24 * 7, // 7 days
    };

    cookies.set("access_token", tokens.access_token, {
      ...cookieOptions,
      maxAge: tokens.expires_in || 3600,
    });

    if (tokens.refresh_token) {
      cookies.set("refresh_token", tokens.refresh_token, {
        ...cookieOptions,
        maxAge: 60 * 60 * 24 * 30, // 30 days
      });
    }

    // TODO: Create local session or onboarding record as needed
    // This varies by property — adapt to your app's needs

    redirect(302, "/dashboard"); // Or wherever authenticated users go
  } catch (err) {
    if (err && typeof err === "object" && "status" in err && err.status === 302) {
      throw err; // Re-throw redirects
    }
    redirect(302, "/?error=auth_failed");
  }
};
```

#### 4c. Session validation hook: `src/hooks.server.ts`

Choose ONE approach:

**Option A: Token verification (works cross-account)**

```typescript
import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
  const accessToken = event.cookies.get("access_token");

  if (accessToken) {
    try {
      const env = event.platform?.env as Record<string, string> | undefined;
      const authBaseUrl = env?.GROVEAUTH_URL || "https://auth-api.grove.place";

      const response = await fetch(`${authBaseUrl}/verify`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });

      if (response.ok) {
        const result = await response.json();
        if (result.active) {
          event.locals.user = {
            id: result.sub,
            email: result.email,
            name: result.name,
          };
        }
      }
    } catch {
      // Token invalid or expired — user remains unauthenticated
    }
  }

  return resolve(event);
};
```

**Option B: SessionDO validation (faster, same Cloudflare account only)**

Requires a service binding in wrangler.toml (see Step 5).

```typescript
import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
  const cookieHeader = event.request.headers.get("Cookie") || "";

  // Only validate if grove_session or access_token cookie exists
  if (cookieHeader.includes("grove_session") || cookieHeader.includes("access_token")) {
    try {
      const env = event.platform?.env as any;

      // Use service binding for sub-100ms validation
      const response = await env.AUTH.fetch("https://auth-api.grove.place/session/validate", {
        method: "POST",
        headers: { Cookie: cookieHeader },
      });

      if (response.ok) {
        const { valid, user } = await response.json();
        if (valid && user) {
          event.locals.user = {
            id: user.id,
            email: user.email,
            name: user.name,
          };
        }
      }
    } catch {
      // Session invalid — user remains unauthenticated
    }
  }

  return resolve(event);
};
```

#### 4d. Type definitions: `src/app.d.ts`

```typescript
declare global {
  namespace App {
    interface Locals {
      user?: {
        id: string;
        email: string;
        name?: string | null;
      };
    }
    interface Platform {
      env?: {
        GROVEAUTH_URL?: string;
        GROVEAUTH_CLIENT_ID?: string;
        GROVEAUTH_CLIENT_SECRET?: string;
        PUBLIC_APP_URL?: string;
        AUTH?: Fetcher; // Service binding (Option B only)
        DB?: D1Database;
        [key: string]: unknown;
      };
    }
  }
}

export {};
```

#### 4e. Protected route layout: `src/routes/admin/+layout.server.ts`

```typescript
import { redirect } from "@sveltejs/kit";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ locals }) => {
  if (!locals.user) {
    redirect(302, "/auth");
  }
  return { user: locals.user };
};
```

#### 4f. Logout route: `src/routes/auth/logout/+server.ts`

```typescript
import { redirect } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

export const POST: RequestHandler = async ({ cookies, platform }) => {
  const accessToken = cookies.get("access_token");

  if (accessToken) {
    const env = platform?.env as Record<string, string> | undefined;
    const authBaseUrl = env?.GROVEAUTH_URL || "https://auth-api.grove.place";

    // Revoke token at Heartwood
    await fetch(`${authBaseUrl}/logout`, {
      method: "POST",
      headers: { Authorization: `Bearer ${accessToken}` },
    }).catch(() => {}); // Best-effort
  }

  // Clear all auth cookies
  cookies.delete("access_token", { path: "/" });
  cookies.delete("refresh_token", { path: "/" });

  redirect(302, "/");
};
```

---

### Step 5: Wire Up wrangler.toml

Add these to the project's `wrangler.toml`:

```toml
# Heartwood (GroveAuth) - Service Binding for fast session validation
# Only works for projects in the same Cloudflare account
[[services]]
binding = "AUTH"
service = "groveauth"

# Secrets (configured via wrangler pages secret / Cloudflare Dashboard):
# - GROVEAUTH_URL = https://auth-api.grove.place
# - GROVEAUTH_CLIENT_ID = your-client-id
# - GROVEAUTH_CLIENT_SECRET = (generated in Step 2)
# - GROVEAUTH_REDIRECT_URI = https://yoursite.com/auth/callback
# - PUBLIC_APP_URL = https://yoursite.com
```

---

### Step 6: Test the Flow

1. Deploy the project (or run locally with `pnpm dev`)
2. Navigate to `/auth` — should redirect to Heartwood login
3. Authenticate with Google (or other configured provider)
4. Should redirect back to `/auth/callback`
5. Should set cookies and redirect to protected area
6. Visit `/admin` (protected) — should show authenticated content
7. Logout via POST to `/auth/logout` — should clear session

---

## Token Lifecycle

| Token | Lifetime | Storage | Refresh |
|-------|----------|---------|---------|
| Access Token | 1 hour | httpOnly cookie | Via refresh token |
| Refresh Token | 30 days | httpOnly cookie | Re-login required |
| PKCE Verifier | 10 minutes | httpOnly cookie | Single-use |
| State | 10 minutes | httpOnly cookie | Single-use |

---

## Session Validation Approaches

| Approach | Speed | Requirement | Use When |
|----------|-------|-------------|----------|
| **Token Verify** (`/verify`) | ~50-150ms | Network call | Cross-account, external services |
| **SessionDO** (`/session/validate`) | ~5-20ms | Service binding | Same Cloudflare account (recommended) |
| **Cookie SSO** (`.grove.place`) | ~0ms (local) | Same domain | All `*.grove.place` properties |

For Grove properties on `.grove.place` subdomains, the `grove_session` cookie is shared automatically across all subdomains.

---

## Checklist

Before going live, verify:

- [ ] Client registered in Heartwood D1 (`clients` table)
- [ ] Secret hash uses **base64url** encoding (dashes, underscores, no padding)
- [ ] `redirect_uris` includes BOTH production AND localhost
- [ ] `allowed_origins` includes BOTH production AND localhost
- [ ] Secrets set via `wrangler pages secret put` (NOT in wrangler.toml!)
- [ ] PKCE flow generates fresh verifier per login attempt
- [ ] State parameter validated in callback (CSRF protection)
- [ ] Auth cookies cleared immediately after code exchange
- [ ] Protected routes check `locals.user` and redirect if missing
- [ ] Logout revokes token at Heartwood AND clears local cookies
- [ ] Cookie `secure` flag is true in production, false in localhost

---

## Troubleshooting

### "Invalid client credentials" (401)
Almost always a **hash format mismatch**. Regenerate with the exact base64url command in Step 2b.

### "Invalid redirect_uri"
The callback URL must EXACTLY match what's in the `redirect_uris` JSON array in the database. Check trailing slashes, protocol, and port.

### "Invalid state" on callback
The state cookie expired (10min TTL) or was lost. Check:
- Cookie domain matches the callback domain
- No redirect loops between domains consuming the cookie early

### "Code verifier required"
The PKCE verifier cookie wasn't sent with the callback request. Ensure:
- Cookie `path` is `/` (not `/auth`)
- Cookie domain matches callback domain
- No third-party cookie blocking

### Session validation returns 401
- Token may have expired (1hr lifetime) — implement refresh logic
- Service binding may not be configured — check wrangler.toml
- Cookie domain mismatch — `.grove.place` cookies only work on subdomains

### "CORS error" on auth API calls
Add your domain to `allowed_origins` in the Heartwood `clients` table.

---

## Anti-Patterns

**Don't do these:**

- Don't store `client_secret` in wrangler.toml or source code
- Don't skip PKCE — it's required, not optional
- Don't reuse state or verifier values across login attempts
- Don't store tokens in localStorage (XSS-vulnerable)
- Don't skip state validation in the callback (enables CSRF)
- Don't hard-code `auth-api.grove.place` — use the env var for flexibility
- Don't forget localhost in redirect_uris (you'll need it for dev)

---

*Authentication should be invisible until it's needed. Let Heartwood handle the complexity.*
