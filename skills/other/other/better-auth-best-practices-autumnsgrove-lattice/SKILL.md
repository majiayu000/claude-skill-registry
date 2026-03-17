---
name: better-auth-best-practices
description: Better Auth framework reference — configuration, security, rate limiting, sessions, plugins, and production hardening. Use when configuring Better Auth, auditing auth security, adding plugins, or troubleshooting Heartwood.
---

# Better Auth Best Practices

Comprehensive reference for the Better Auth framework. Covers configuration, security hardening, rate limiting, session management, plugins, and production deployment patterns.

**Canonical docs:** [better-auth.com/docs](https://better-auth.com/docs)
**Source:** Synthesized from [better-auth/skills](https://github.com/better-auth/skills) (official upstream) + Grove production experience.

## When to Activate

- Configuring or modifying Better Auth server/client setup
- Auditing auth security (pair with `raccoon-audit`, `turtle-harden`)
- Adding or configuring rate limiting
- Setting up session management, cookie caching, or secondary storage
- Adding plugins (2FA, organizations, passkeys, etc.)
- Troubleshooting auth issues on Heartwood or any Better Auth deployment
- Reviewing security posture before production deploy

**Pair with:** `heartwood-auth` (Grove-specific integration), `spider-weave` (auth architecture), `turtle-harden` (deep security)

---

## Grove Context: Heartwood

Heartwood is Grove's auth service, powered by Better Auth on Cloudflare Workers.

| Component | Detail |
|-----------|--------|
| Frontend | `heartwood.grove.place` |
| API | `auth-api.grove.place` |
| Database | Cloudflare D1 (SQLite) |
| Session cache | Cloudflare KV (`SESSION_KV`) |
| Providers | Google OAuth, Magic Links, Passkeys |
| Cookie domain | `.grove.place` (cross-subdomain SSO) |

Everything in this skill applies directly to Heartwood. The `heartwood-auth` skill covers Grove-specific integration patterns (client setup, route protection, error codes). This skill covers the framework itself.

---

## Quick Reference

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `BETTER_AUTH_SECRET` | Encryption secret (min 32 chars). Generate: `openssl rand -base64 32` |
| `BETTER_AUTH_URL` | Base URL (e.g., `https://auth-api.grove.place`) |
| `BETTER_AUTH_TRUSTED_ORIGINS` | Comma-separated trusted origins |

Only define `baseURL`/`secret` in config if env vars are NOT set.

### File Location

CLI looks for `auth.ts` in: `./`, `./lib`, `./utils`, or under `./src`. Use `--config` for custom path.

### CLI Commands

```bash
npx @better-auth/cli@latest migrate    # Apply schema (built-in adapter)
npx @better-auth/cli@latest generate   # Generate schema for Prisma/Drizzle
```

**Re-run after adding/changing plugins.**

---

## Core Configuration

| Option | Notes |
|--------|-------|
| `appName` | Display name (used in 2FA issuer, emails) |
| `baseURL` | Only if `BETTER_AUTH_URL` not set |
| `basePath` | Default `/api/auth`. Set `/` for root |
| `secret` | Only if `BETTER_AUTH_SECRET` not set |
| `database` | Required. Connection or adapter instance |
| `secondaryStorage` | Redis/KV for sessions & rate limits |
| `emailAndPassword` | `{ enabled: true }` to activate |
| `socialProviders` | `{ google: { clientId, clientSecret }, ... }` |
| `plugins` | Array of plugins |
| `trustedOrigins` | CSRF whitelist (baseURL auto-trusted) |

---

## Database

**Direct connections:** Pass `pg.Pool`, `mysql2` pool, `better-sqlite3`, or `bun:sqlite` instance.

**ORM adapters:** Import from `better-auth/adapters/drizzle`, `better-auth/adapters/prisma`, `better-auth/adapters/mongodb`.

**Critical gotcha:** Better Auth uses adapter model names, NOT underlying table names. If Prisma model is `User` mapping to table `users`, use `modelName: "user"` (Prisma reference), not `"users"`.

---

## Rate Limiting

Better Auth has **built-in rate limiting** — enabled by default in production, disabled in development.

### Why This Matters for Grove

Better Auth's rate limiter can replace custom threshold SDKs for auth endpoints. It's battle-tested, configurable per-endpoint, and integrates directly with the auth layer where it matters most.

### Default Configuration

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  rateLimit: {
    enabled: true,       // Default: true in production
    window: 10,          // Time window in seconds (default: 10)
    max: 100,            // Max requests per window (default: 100)
  },
});
```

### Storage Options

```typescript
rateLimit: {
  storage: "secondary-storage", // Best for production
}
```

| Storage | Behavior |
|---------|----------|
| `"memory"` | Fast, resets on restart. **Not recommended for serverless.** |
| `"database"` | Persistent, adds DB load |
| `"secondary-storage"` | Uses configured KV/Redis. **Default when available.** |

**For Heartwood:** Use `"secondary-storage"` backed by Cloudflare KV.

### Per-Endpoint Rules

Better Auth applies stricter defaults to sensitive endpoints:
- `/sign-in`, `/sign-up`, `/change-password`, `/change-email`: **3 requests per 10 seconds**

Override for specific paths:

```typescript
rateLimit: {
  customRules: {
    "/api/auth/sign-in/email": {
      window: 60,  // 1 minute
      max: 5,      // 5 attempts
    },
    "/api/auth/sign-up/email": {
      window: 60,
      max: 3,      // Very strict for registration
    },
    "/api/auth/some-safe-endpoint": false, // Disable rate limiting
  },
}
```

### Custom Storage

For non-standard backends:

```typescript
rateLimit: {
  customStorage: {
    get: async (key) => {
      // Return { count: number, expiresAt: number } or null
    },
    set: async (key, data) => {
      // Store the rate limit data
    },
  },
}
```

Each plugin can optionally define its own rate-limit rules per endpoint.

---

## Session Management

### Storage Priority

1. If `secondaryStorage` defined → sessions go there (not DB)
2. Set `session.storeSessionInDatabase: true` to also persist to DB
3. No database + `cookieCache` → fully stateless mode

### Key Options

```typescript
session: {
  expiresIn: 60 * 60 * 24 * 7,   // 7 days (default)
  updateAge: 60 * 60 * 24,        // Refresh every 24 hours (default)
  freshAge: 60 * 60 * 24,         // 24 hours for sensitive actions (default)
}
```

**`freshAge`** — defines how recently a user must have authenticated to perform sensitive operations. Use to require re-auth for password changes, viewing sensitive data, etc.

### Cookie Cache Strategies

Cache session data in cookies to reduce DB/KV queries:

```typescript
session: {
  cookieCache: {
    enabled: true,
    maxAge: 60 * 5,        // 5 minutes
    strategy: "compact",   // Options: "compact", "jwt", "jwe"
    version: 1,            // Change to invalidate all sessions
  },
}
```

| Strategy | Description |
|----------|-------------|
| `compact` | Base64url + HMAC. Smallest size. Default. |
| `jwt` | Standard HS256 JWT. Readable but signed. |
| `jwe` | A256CBC-HS512 encrypted. Maximum security. |

**Gotcha:** Custom session fields are NOT cached — they're always re-fetched from storage.

---

## Security Configuration

### Secret Management

Better Auth looks for secrets in order:
1. `options.secret` in config
2. `BETTER_AUTH_SECRET` env var
3. `AUTH_SECRET` env var

Requirements:
- **Rejects** default/placeholder secrets in production
- **Warns** if shorter than 32 characters
- **Warns** if entropy below 120 bits

### CSRF Protection

Multi-layered by default:
1. **Origin header validation** — `Origin`/`Referer` must match trusted origins
2. **Fetch metadata** — Uses `Sec-Fetch-Site`, `Sec-Fetch-Mode`, `Sec-Fetch-Dest` headers
3. **First-login protection** — Validates origin even without cookies

```typescript
advanced: {
  disableCSRFCheck: false,  // KEEP THIS FALSE
}
```

### Trusted Origins

```typescript
trustedOrigins: [
  "https://app.grove.place",
  "https://*.grove.place",          // Wildcard subdomain
  "exp://192.168.*.*:*/*",          // Custom schemes (Expo)
]
```

Dynamic computation:

```typescript
trustedOrigins: async (request) => {
  const tenant = getTenantFromRequest(request);
  return [`https://${tenant}.grove.place`];
}
```

Validated parameters: `callbackURL`, `redirectTo`, `errorCallbackURL`, `newUserCallbackURL`, `origin`, and more. Invalid URLs get 403.

### Cookie Security

Defaults are secure:
- `secure: true` when baseURL uses HTTPS or in production
- `sameSite: "lax"` (CSRF prevention while allowing navigation)
- `httpOnly: true` (no JavaScript access)
- `__Secure-` prefix when secure is enabled

```typescript
advanced: {
  useSecureCookies: true,
  cookiePrefix: "better-auth",
  defaultCookieAttributes: {
    sameSite: "lax",
  },
  crossSubDomainCookies: {
    enabled: true,
    domain: ".grove.place",  // Note the leading dot
    additionalCookies: ["session_token", "session_data"],
  },
}
```

**Warning:** Cross-subdomain cookies expand attack surface. Only enable if you trust all subdomains.

### IP-Based Security

```typescript
advanced: {
  ipAddress: {
    ipAddressHeaders: ["x-forwarded-for", "x-real-ip"],
    ipv6Subnet: 64,            // Group IPv6 by /64
    disableIpTracking: false,  // Keep enabled for rate limiting
  },
  trustedProxyHeaders: true,   // Only if behind a trusted proxy
}
```

### Background Tasks (Timing Attack Prevention)

Sensitive operations should complete in constant time. The `handler` callback receives a promise that must outlive the response — on serverless platforms, you need the platform's `waitUntil` to keep it alive.

**Cloudflare Workers:** Capture `ExecutionContext` from the fetch handler and close over it:

```typescript
// In your Worker fetch handler:
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    // Create auth with ctx in scope
    const auth = createAuth(env, ctx);
    return auth.handler(request);
  },
};

// In your auth config factory:
function createAuth(env: Env, ctx: ExecutionContext) {
  return betterAuth({
    // ...
    advanced: {
      backgroundTasks: {
        handler: (promise) => ctx.waitUntil(promise),
      },
    },
  });
}
```

**Vercel/Next.js:** Use the `waitUntil` export from `@vercel/functions`:

```typescript
import { waitUntil } from "@vercel/functions";

advanced: {
  backgroundTasks: {
    handler: (promise) => waitUntil(promise),
  },
}
```

Ensures email sending doesn't leak information about whether a user exists.

### Account Enumeration Prevention

Built-in protections:
1. **Consistent response messages** — Password reset always returns generic message
2. **Dummy operations** — When user isn't found, still performs token generation + DB lookups
3. **Background email sending** — Async to prevent timing differences

---

## OAuth / Social Provider Security

### PKCE (Automatic)

Better Auth automatically uses PKCE for all OAuth flows:
1. Generates 128-character random `code_verifier`
2. Creates `code_challenge` using S256 (SHA-256)
3. Validates code exchange with original verifier

### State Parameter

```typescript
account: {
  storeStateStrategy: "cookie",  // "cookie" (default) or "database"
}
```

State tokens: 32-character random strings, expire after 10 minutes, contain encrypted callback URLs + PKCE verifier.

### Encrypt Stored OAuth Tokens

```typescript
account: {
  encryptOAuthTokens: true,  // AES-256-GCM
}
```

Enable if you store OAuth tokens for API access on behalf of users.

---

## Email & Password

### Email Verification

```typescript
emailVerification: {
  sendVerificationEmail: async ({ user, url }) => {
    await sendEmail({ to: user.email, subject: "Verify your email", url });
  },
  sendOnSignUp: true,
  requireEmailVerification: true,  // Blocks sign-in until verified
}
```

### Password Reset

```typescript
emailAndPassword: {
  sendResetPassword: async ({ user, url }) => {
    await sendEmail({ to: user.email, subject: "Reset your password", url });
  },
  password: {
    minLength: 8,   // Default
    maxLength: 128,  // Default
  },
  revokeSessionsOnPasswordReset: true,  // Log out all sessions
}
```

**Security:** Reset tokens are 24-character alphanumeric strings, expire after 1 hour, single-use.

### Password Hashing

Default: scrypt. For Argon2id, provide custom `hash` and `verify` functions.

---

## Two-Factor Authentication

### Setup

```typescript
import { twoFactor } from "better-auth/plugins";

// Server
plugins: [
  twoFactor({
    issuer: "Grove",  // Shown in authenticator apps
    totpOptions: { digits: 6, period: 30 },
    backupCodeOptions: { amount: 10, length: 10, storeBackupCodes: "encrypted" },
  }),
]

// Client
plugins: [
  twoFactorClient({
    onTwoFactorRedirect() {
      window.location.href = "/2fa";
    },
  }),
]
```

**Run migrations after adding.** The `twoFactorEnabled` flag only activates after successful TOTP verification.

### Sign-In Flow with 2FA

1. User signs in with credentials
2. Response includes `twoFactorRedirect: true`
3. Session cookie removed temporarily
4. Two-factor cookie set (10-minute expiration)
5. User verifies via TOTP/OTP/backup code
6. Session cookie restored

### Trusted Devices

Skip 2FA on subsequent sign-ins:

```typescript
twoFactor({
  trustDeviceMaxAge: 30 * 24 * 60 * 60,  // 30 days
})

// During verification:
await authClient.twoFactor.verifyTotp({ code, trustDevice: true });
```

### OTP (Email/SMS)

```typescript
twoFactor({
  otpOptions: {
    sendOTP: async ({ user, otp }) => {
      await sendEmail({ to: user.email, subject: "Your code", text: `Code: ${otp}` });
    },
    period: 5,            // Minutes
    digits: 6,
    allowedAttempts: 5,
    storeOTP: "encrypted",
  },
})
```

### Built-in 2FA Protections

- Rate limiting: 3 requests per 10 seconds on 2FA endpoints
- OTP attempt limiting: configurable max attempts
- Constant-time comparison prevents timing attacks
- TOTP secrets encrypted with symmetric encryption
- Backup codes encrypted by default
- **Limitation:** 2FA requires credential accounts — social-only accounts can't enable it

---

## Organizations Plugin

Multi-tenant organization support:

```typescript
import { organization } from "better-auth/plugins";

plugins: [
  organization({
    // Limit who can create orgs
    allowUserToCreateOrganization: async (user) => {
      return user.emailVerified;
    },
  }),
]
```

### Key Concepts

- **Active organization** stored in session — scopes API calls after `setActive()`
- **Default roles:** owner (full), admin (management), member (basic)
- **Dynamic access control** for custom runtime permissions
- **Teams** group members within organizations
- **Invitations** expire after 48 hours (configurable), email-specific
- **Safety:** Last owner cannot be removed or leave

---

## Plugins Reference

```typescript
import { twoFactor, organization } from "better-auth/plugins";
```

| Plugin | Purpose | Scoped Package? |
|--------|---------|-----------------|
| `twoFactor` | TOTP/OTP/backup codes | No |
| `organization` | Teams & multi-tenant | No |
| `passkey` | WebAuthn | `@better-auth/passkey` |
| `magicLink` | Passwordless email | No |
| `emailOtp` | Email-based OTP | No |
| `username` | Username auth | No |
| `phoneNumber` | Phone auth | No |
| `admin` | User management | No |
| `apiKey` | API key auth | No |
| `bearer` | Bearer token auth | No |
| `jwt` | JWT tokens | No |
| `multiSession` | Multiple sessions | No |
| `sso` | SAML/OIDC enterprise | `@better-auth/sso` |
| `oauthProvider` | Be an OAuth provider | No |
| `oidcProvider` | Be an OIDC provider | No |
| `openAPI` | API documentation | No |
| `genericOAuth` | Custom OAuth provider | No |

Client plugins go in `createAuthClient({ plugins: [...] })`.

**Always run migrations after adding plugins.**

---

## Client Setup

Import by framework:

| Framework | Import |
|-----------|--------|
| React/Next.js | `better-auth/react` |
| Svelte/SvelteKit | `better-auth/svelte` |
| Vue/Nuxt | `better-auth/vue` |
| Solid | `better-auth/solid` |
| Vanilla JS | `better-auth/client` |

Key methods: `signUp.email()`, `signIn.email()`, `signIn.social()`, `signOut()`, `useSession()`, `getSession()`, `revokeSession()`, `revokeSessions()`.

### Type Safety

```typescript
// Infer types from server config
type Session = typeof auth.$Infer.Session;
type User = typeof auth.$Infer.Session.user;

// For separate client/server projects
createAuthClient<typeof auth>();
```

---

## Hooks

### Endpoint Hooks

```typescript
hooks: {
  before: [
    {
      matcher: (ctx) => ctx.path === "/sign-in/email",
      handler: createAuthMiddleware(async (ctx) => {
        // Access: ctx.path, ctx.context.session, ctx.context.secret
        // Return modified context or void
      }),
    },
  ],
  after: [
    {
      matcher: (ctx) => true,
      handler: createAuthMiddleware(async (ctx) => {
        // Access: ctx.context.returned (response data)
      }),
    },
  ],
}
```

### Database Hooks

```typescript
databaseHooks: {
  user: {
    create: {
      before: async ({ data }) => { /* add defaults, return false to block */ },
      after: async ({ data }) => { /* audit log, send welcome email */ },
    },
  },
  session: {
    create: {
      after: async ({ data, ctx }) => {
        await auditLog("session.created", {
          userId: data.userId,
          ip: ctx?.request?.headers.get("x-forwarded-for"),
        });
      },
    },
  },
}
```

**Hook context (`ctx.context`):** `session`, `secret`, `authCookies`, `password.hash()`/`verify()`, `adapter`, `internalAdapter`, `generateId()`, `tables`, `baseURL`.

---

## Common Gotchas

1. **Model vs table name** — Config uses ORM model name, not DB table name
2. **Plugin schema** — Re-run CLI after adding plugins (always!)
3. **Secondary storage** — Sessions go there by default, not DB
4. **Cookie cache** — Custom session fields NOT cached, always re-fetched
5. **Stateless mode** — No DB = session in cookie only, logout on cache expiry
6. **Change email flow** — Sends to current email first, then new email
7. **2FA + social** — 2FA only works on credential accounts, not social-only
8. **Last owner** — Cannot be removed from or leave an organization
9. **Rate limit memory** — Memory storage resets on restart, bad for serverless

---

## Production Security Checklist

- [ ] `BETTER_AUTH_SECRET` set (32+ chars, high entropy)
- [ ] `BETTER_AUTH_URL` uses HTTPS
- [ ] `trustedOrigins` configured for all valid origins
- [ ] Rate limiting enabled with appropriate per-endpoint limits
- [ ] Rate limit storage set to `"secondary-storage"` or `"database"` (not memory)
- [ ] CSRF protection enabled (`disableCSRFCheck: false`)
- [ ] Secure cookies enabled (automatic with HTTPS)
- [ ] `account.encryptOAuthTokens: true` if storing tokens
- [ ] Background tasks configured for serverless (capture `ExecutionContext` from fetch handler)
- [ ] Audit logging via `databaseHooks` or `hooks`
- [ ] IP tracking headers configured if behind proxy
- [ ] Email verification enabled
- [ ] Password reset implemented
- [ ] 2FA available for sensitive apps
- [ ] Session expiry and refresh intervals reviewed
- [ ] Cookie cache strategy chosen (`jwe` for sensitive session data)
- [ ] `account.accountLinking` reviewed

---

## Complete Production Config Example

```typescript
import { betterAuth } from "better-auth";
import { twoFactor, organization } from "better-auth/plugins";

// Factory pattern — ctx comes from the Worker fetch handler
export function createAuth(env: Env, ctx: ExecutionContext) {
  return betterAuth({
    appName: "Grove",
    secret: env.BETTER_AUTH_SECRET,
    baseURL: "https://auth-api.grove.place",
    trustedOrigins: [
      "https://heartwood.grove.place",
      "https://*.grove.place",
    ],

    database: d1Adapter(env),
    secondaryStorage: kvAdapter(env),

    // Rate limiting (replaces custom threshold SDK for auth)
    rateLimit: {
      enabled: true,
      storage: "secondary-storage",
      customRules: {
        "/api/auth/sign-in/email": { window: 60, max: 5 },
        "/api/auth/sign-up/email": { window: 60, max: 3 },
        "/api/auth/change-password": { window: 60, max: 3 },
      },
    },

    // Sessions
    session: {
      expiresIn: 60 * 60 * 24 * 7,    // 7 days
      updateAge: 60 * 60 * 24,         // 24 hours
      freshAge: 60 * 60,               // 1 hour for sensitive actions
      cookieCache: {
        enabled: true,
        maxAge: 300,
        strategy: "jwe",
      },
    },

    // OAuth
    account: {
      encryptOAuthTokens: true,
      storeStateStrategy: "cookie",
    },

    // Security
    advanced: {
      useSecureCookies: true,
      crossSubDomainCookies: {
        enabled: true,
        domain: ".grove.place",
      },
      ipAddress: {
        ipAddressHeaders: ["x-forwarded-for"],
        ipv6Subnet: 64,
      },
      backgroundTasks: {
        handler: (promise) => ctx.waitUntil(promise),  // ctx captured from fetch handler
      },
    },

    // Plugins
    plugins: [
      twoFactor({
        issuer: "Grove",
        backupCodeOptions: { storeBackupCodes: "encrypted" },
      }),
      organization(),
    ],

    // Audit hooks
    databaseHooks: {
      session: {
        create: {
          after: async ({ data, ctx: hookCtx }) => {
            console.log(`[audit] session created: user=${data.userId}`);
          },
        },
      },
    },
  });
}
```

---

## Resources

- [Better Auth Docs](https://better-auth.com/docs)
- [Options Reference](https://better-auth.com/docs/reference/options)
- [LLMs.txt](https://better-auth.com/llms.txt)
- [GitHub](https://github.com/better-auth/better-auth)
- [Official Skills](https://github.com/better-auth/skills)
- [Init Options Source](https://github.com/better-auth/better-auth/blob/main/packages/core/src/types/init-options.ts)
