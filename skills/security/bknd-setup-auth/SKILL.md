---
name: bknd-setup-auth
description: Use when initializing or configuring the Bknd authentication system. Covers enabling auth, configuring password strategy, setting up JWT and cookie options, defining roles, and production security settings.
---

# Setup Authentication

Initialize and configure the Bknd authentication system with strategies, JWT, cookies, and roles.

## Prerequisites

- Bknd project initialized
- Code-first configuration (auth config is code-only)
- For OAuth: provider credentials (client ID, client secret)

## When to Use UI Mode

- Viewing current auth configuration
- Toggling strategies on/off
- Testing auth endpoints via admin panel

**UI steps:** Admin Panel > Auth > Settings

**Note:** Full auth configuration requires code mode. UI only shows/toggles existing settings.

## When to Use Code Mode

- Initial authentication setup
- Configuring JWT secrets and expiry
- Setting up password hashing
- Defining roles and permissions
- Production security hardening

## Code Approach

### Step 1: Enable Auth with Minimal Config

Start with basic password authentication:

```typescript
import { serve } from "bknd/adapter/bun";
import { em, entity, text } from "bknd";

const schema = em({
  posts: entity("posts", { title: text().required() }),
});

serve({
  connection: { url: "file:data.db" },
  config: {
    data: schema.toJSON(),
    auth: {
      enabled: true,
    },
  },
});
```

This enables:
- Password strategy (default)
- Auto-created `users` entity
- JWT-based sessions
- `/api/auth/*` endpoints

### Step 2: Configure JWT Settings

JWT tokens authenticate API requests. Configure for security:

```typescript
{
  auth: {
    enabled: true,
    jwt: {
      secret: process.env.JWT_SECRET,  // Required in production
      alg: "HS256",                     // Algorithm: HS256, HS384, HS512
      expires: 604800,                  // Expiry in seconds (7 days)
      issuer: "my-app",                 // Optional issuer claim
      fields: ["id", "email", "role"],  // Fields included in token
    },
  },
}
```

**JWT options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `secret` | string | `""` | Signing secret (256-bit minimum for production) |
| `alg` | string | `"HS256"` | Algorithm: HS256, HS384, HS512 |
| `expires` | number | - | Token expiry in seconds |
| `issuer` | string | - | Token issuer claim (iss) |
| `fields` | string[] | `["id", "email", "role"]` | User fields in payload |

### Step 3: Configure Cookie Settings

Auth cookies store JWT tokens for browser sessions:

```typescript
{
  auth: {
    enabled: true,
    jwt: { secret: process.env.JWT_SECRET },
    cookie: {
      secure: true,           // HTTPS only (set false for local dev)
      httpOnly: true,         // Block JavaScript access
      sameSite: "lax",        // CSRF protection: "strict" | "lax" | "none"
      expires: 604800,        // Cookie expiry in seconds (7 days)
      path: "/",              // Cookie path scope
      renew: true,            // Auto-extend on requests
      pathSuccess: "/",       // Redirect after login
      pathLoggedOut: "/",     // Redirect after logout
    },
  },
}
```

**Cookie options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `secure` | boolean | `true` | HTTPS-only flag |
| `httpOnly` | boolean | `true` | Block JS access |
| `sameSite` | string | `"lax"` | CSRF protection |
| `expires` | number | `604800` | Expiry in seconds |
| `renew` | boolean | `true` | Auto-extend expiry |
| `pathSuccess` | string | `"/"` | Post-login redirect |
| `pathLoggedOut` | string | `"/"` | Post-logout redirect |

### Step 4: Configure Password Strategy

Set up password hashing and requirements:

```typescript
{
  auth: {
    enabled: true,
    jwt: { secret: process.env.JWT_SECRET },
    strategies: {
      password: {
        type: "password",
        enabled: true,
        config: {
          hashing: "bcrypt",   // "plain" | "sha256" | "bcrypt"
          rounds: 4,           // bcrypt rounds (1-10)
          minLength: 8,        // Minimum password length
        },
      },
    },
  },
}
```

**Hashing options:**

| Option | Security | Performance | Use Case |
|--------|----------|-------------|----------|
| `plain` | None | Fastest | Development only, never production |
| `sha256` | Good | Fast | Default, suitable for most cases |
| `bcrypt` | Best | Slower | Recommended for production |

### Step 5: Define Roles

Configure roles for authorization:

```typescript
{
  auth: {
    enabled: true,
    jwt: { secret: process.env.JWT_SECRET },
    roles: {
      admin: {
        implicit_allow: true,  // Can do everything
      },
      editor: {
        implicit_allow: false,
        permissions: [
          { permission: "data.posts.read", effect: "allow" },
          { permission: "data.posts.create", effect: "allow" },
          { permission: "data.posts.update", effect: "allow" },
        ],
      },
      user: {
        implicit_allow: false,
        is_default: true,  // Default role for new registrations
        permissions: [
          { permission: "data.posts.read", effect: "allow" },
        ],
      },
    },
    default_role_register: "user",  // Role assigned on registration
  },
}
```

### Step 6: Configure Registration

Control user self-registration:

```typescript
{
  auth: {
    enabled: true,
    allow_register: true,           // Enable/disable registration
    default_role_register: "user",  // Role for new users
    entity_name: "users",           // User entity name (default: "users")
    basepath: "/api/auth",          // Auth API base path
  },
}
```

## Full Production Example

Complete auth setup with security best practices:

```typescript
import { serve, type BunBkndConfig } from "bknd/adapter/bun";
import { em, entity, text, date } from "bknd";

const schema = em({
  users: entity("users", {
    email: text().required().unique(),
    name: text(),
    avatar: text(),
    created_at: date({ default_value: "now" }),
  }),
  posts: entity("posts", {
    title: text().required(),
    content: text(),
  }),
});

type Database = (typeof schema)["DB"];
declare module "bknd" {
  interface DB extends Database {}
}

const config: BunBkndConfig = {
  connection: { url: process.env.DB_URL || "file:data.db" },
  config: {
    data: schema.toJSON(),
    auth: {
      enabled: true,
      basepath: "/api/auth",
      entity_name: "users",
      allow_register: true,
      default_role_register: "user",

      // JWT configuration
      jwt: {
        secret: process.env.JWT_SECRET!,
        alg: "HS256",
        expires: 604800,  // 7 days
        issuer: "my-app",
        fields: ["id", "email", "role"],
      },

      // Cookie configuration
      cookie: {
        secure: process.env.NODE_ENV === "production",
        httpOnly: true,
        sameSite: "lax",
        expires: 604800,
        renew: true,
        pathSuccess: "/dashboard",
        pathLoggedOut: "/login",
      },

      // Password strategy
      strategies: {
        password: {
          type: "password",
          enabled: true,
          config: {
            hashing: "bcrypt",
            rounds: 4,
            minLength: 8,
          },
        },
      },

      // Roles
      roles: {
        admin: {
          implicit_allow: true,
        },
        editor: {
          implicit_allow: false,
          permissions: [
            { permission: "data.posts.read", effect: "allow" },
            { permission: "data.posts.create", effect: "allow" },
            { permission: "data.posts.update", effect: "allow" },
            { permission: "data.posts.delete", effect: "allow" },
          ],
        },
        user: {
          implicit_allow: false,
          is_default: true,
          permissions: [
            { permission: "data.posts.read", effect: "allow" },
          ],
        },
      },
    },
  },
  options: {
    seed: async (ctx) => {
      // Create initial admin on first run
      const adminExists = await ctx.em.repo("users").findOne({
        where: { email: { $eq: "admin@example.com" } },
      });

      if (!adminExists) {
        await ctx.app.module.auth.createUser({
          email: "admin@example.com",
          password: process.env.ADMIN_PASSWORD || "changeme123",
          role: "admin",
        });
        console.log("Admin user created");
      }
    },
  },
};

serve(config);
```

## Auth Endpoints

After setup, these endpoints are available:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/password/login` | Login with email/password |
| POST | `/api/auth/password/register` | Register new user |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/auth/logout` | Log out (clear cookie) |
| GET | `/api/auth/strategies` | List enabled strategies |

## Environment Variables

Recommended env vars for auth:

```bash
# .env
JWT_SECRET=your-256-bit-secret-minimum-32-characters-long
ADMIN_PASSWORD=secure-initial-admin-password
```

Generate a secure secret:

```bash
# Generate 64-character random string
openssl rand -hex 32
```

## Development vs Production

| Setting | Development | Production |
|---------|-------------|------------|
| `jwt.secret` | Can use placeholder | **Required**, strong secret |
| `cookie.secure` | `false` | `true` (HTTPS only) |
| `strategies.password.config.hashing` | `sha256` | `bcrypt` |
| `allow_register` | `true` | Consider `false` for closed systems |

**Dev config shortcut:**

```typescript
const isDev = process.env.NODE_ENV !== "production";

{
  auth: {
    enabled: true,
    jwt: {
      secret: isDev ? "dev-secret-not-for-production" : process.env.JWT_SECRET!,
      expires: isDev ? 86400 * 30 : 604800,  // 30 days dev, 7 days prod
    },
    cookie: {
      secure: !isDev,
    },
    strategies: {
      password: {
        type: "password",
        config: {
          hashing: isDev ? "sha256" : "bcrypt",
        },
      },
    },
  },
}
```

## Common Pitfalls

### Missing JWT Secret in Production

**Problem:** `Cannot sign JWT without secret` error

**Fix:** Set JWT secret via environment variable:

```typescript
{
  auth: {
    jwt: {
      secret: process.env.JWT_SECRET,  // Never hardcode in production
    },
  },
}
```

### Cookie Not Set (HTTPS Issues)

**Problem:** Auth cookie not set in browser

**Fix:** Set `secure: false` for local development:

```typescript
{
  auth: {
    cookie: {
      secure: process.env.NODE_ENV === "production",  // false for localhost
    },
  },
}
```

### Role Not Found

**Problem:** `Role "admin" not found` when creating users

**Fix:** Define roles before referencing them:

```typescript
{
  auth: {
    roles: {
      admin: { implicit_allow: true },  // Define first
      user: { implicit_allow: false },
    },
    default_role_register: "user",  // Now can reference
  },
}
```

### Registration Disabled

**Problem:** `Registration not allowed` error

**Fix:** Enable registration:

```typescript
{
  auth: {
    allow_register: true,  // Default is true, but check if explicitly disabled
  },
}
```

### Weak Password Hashing

**Problem:** Using `plain` or `sha256` in production

**Fix:** Use bcrypt for production:

```typescript
{
  auth: {
    strategies: {
      password: {
        config: {
          hashing: "bcrypt",
          rounds: 4,  // Balance security and performance
        },
      },
    },
  },
}
```

## Verification

After setup, verify auth works:

**1. Check enabled strategies:**

```bash
curl http://localhost:7654/api/auth/strategies
```

**2. Register a test user:**

```bash
curl -X POST http://localhost:7654/api/auth/password/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

**3. Login:**

```bash
curl -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

**4. Check current user (with token):**

```bash
curl http://localhost:7654/api/auth/me \
  -H "Authorization: Bearer <token-from-login>"
```

## Security Checklist

Before deploying to production:

- [ ] Set strong `jwt.secret` (256-bit minimum)
- [ ] Use `hashing: "bcrypt"` for password strategy
- [ ] Set `cookie.secure: true` (HTTPS only)
- [ ] Set `cookie.httpOnly: true` (default)
- [ ] Set `cookie.sameSite: "lax"` or `"strict"`
- [ ] Configure `jwt.expires` (don't leave unlimited)
- [ ] Review `allow_register` setting
- [ ] Create admin user via seed (not via public registration)
- [ ] Store secrets in environment variables

## DOs and DON'Ts

**DO:**
- Use environment variables for secrets
- Use bcrypt hashing in production
- Set JWT expiry times
- Define roles before assigning them
- Test auth flow after configuration changes

**DON'T:**
- Hardcode JWT secrets in code
- Use `plain` hashing in production
- Skip setting `cookie.secure` in production
- Leave registration open if not needed
- Forget to create initial admin user

## Related Skills

- **bknd-create-user** - Create user accounts programmatically
- **bknd-login-flow** - Implement login/logout functionality
- **bknd-registration** - Set up user registration flows
- **bknd-oauth-setup** - Configure OAuth providers (Google, GitHub)
- **bknd-create-role** - Define roles for authorization
- **bknd-session-handling** - Manage user sessions
