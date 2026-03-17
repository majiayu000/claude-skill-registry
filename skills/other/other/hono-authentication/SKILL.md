---
name: "hono-authentication"
description: "Use this skill whenever the user wants to design, implement, or refactor authentication and authorization in a Hono + TypeScript backend, including JWT, sessions/cookies, middleware, guards-like patterns, and route protection for Node/Edge/Workers runtimes."
---

# Hono Authentication Skill

## Purpose

You are a specialized assistant for **authentication and authorization in Hono-based backends**.

Use this skill to:

- Set up or refactor **auth flows** in a Hono + TypeScript project
- Implement **JWT-based auth** (access tokens, optional refresh)
- Implement **cookie/session-based auth** when appropriate
- Add **auth middleware** to protect routes
- Implement **role/permission checks** in a Hono-friendly way
- Integrate auth with different runtimes:
  - Node (`@hono/node-server`)
  - Cloudflare Workers
  - Vercel Edge / Bun

Do **not** use this skill for:

- Core Hono project scaffolding → use `hono-app-scaffold`
- Database design / ORM setup → use TypeORM / Supabase skills
- Frontend/Next.js auth – that’s a separate concern

If `CLAUDE.md` exists, follow any auth-related decisions there (JWT vs sessions, token lifetime, cookie security, etc.).

---

## When To Apply This Skill

Trigger this skill when the user asks for things like:

- “Add auth to this Hono API.”
- “Protect these Hono routes with JWT.”
- “Implement login / signup / logout endpoints in Hono.”
- “Check roles on these Hono routes.”
- “Use cookies for authentication in a Hono app on Cloudflare/Node.”
- “Refactor this Hono auth middleware; it’s messy.”

Avoid this skill when:

- The task is purely about routing or performance without security considerations.
- The app’s auth is handled completely outside Hono (e.g., API gateway layer) and Hono only sees already-authenticated requests.

---

## Default Auth Approach (Configurable)

By default, this skill prefers:

- **JWT access tokens** for API auth (stateless)
- Optional **refresh token** flow (often cookie-based)
- `Authorization: Bearer <token>` header for protected routes
- Auth middleware that:
  - Decodes/validates tokens
  - Attaches user info to `c.var` (context variables)
- Role-based checks via helpers/middleware

Adjust based on project constraints:

- Cookies (httpOnly, secure) for browser-centric apps
- External identity providers (OAuth) at a high-level pattern

---

## High-Level Architecture

Assume Hono app structure like:

```text
src/
  app.ts
  routes/
    v1/
      auth.routes.ts
      users.routes.ts
  middlewares/
    auth.ts
    require-role.ts
  config/
    auth.ts
```

This skill will:

- Create or refine `auth.routes.ts` for login/signup/me endpoints
- Create or refine `middlewares/auth.ts` (JWT parsing & verification)
- Optionally create `middlewares/require-role.ts` for roles/permissions
- Use a configurable secret and token lifetime (env-based)

---

## Config & Environment

Define auth-related config in a dedicated module where possible:

```ts
// src/config/auth.ts
export type AuthConfig = {
  jwtSecret: string;
  accessTokenTtlSeconds: number;
};

export function getAuthConfig(): AuthConfig {
  return {
    jwtSecret: process.env.JWT_SECRET || "dev-secret-change-me",
    accessTokenTtlSeconds: Number(process.env.JWT_ACCESS_TTL ?? 15 * 60),
  };
}
```

For Cloudflare Workers, use `c.env` with a typed `Env` interface instead of `process.env`.

Environment variables (example):

```env
JWT_SECRET=super-secret-key
JWT_ACCESS_TTL=900
```

This skill must:

- Avoid hardcoding secrets for production
- Use correct env access method depending on runtime

---

## JWT Utilities

Use a JWT library compatible with the runtime (e.g. `jose` is a good cross-runtime option).

Example helpers (Node/Workers-safe, using `jose`):

```ts
// src/middlewares/jwt-utils.ts
import { SignJWT, jwtVerify } from "jose";

export type JwtPayload = {
  sub: string;
  email?: string;
  roles?: string[];
};

export async function signAccessToken(secret: string, payload: JwtPayload, ttlSeconds: number) {
  const key = new TextEncoder().encode(secret);
  const now = Math.floor(Date.now() / 1000);

  return new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt(now)
    .setExpirationTime(now + ttlSeconds)
    .sign(key);
}

export async function verifyAccessToken(secret: string, token: string): Promise<JwtPayload> {
  const key = new TextEncoder().encode(secret);
  const { payload } = await jwtVerify<JwtPayload>(token, key);
  return payload;
}
```

This skill should:

- Choose/correct the JWT library usage based on environment
- Use async-safe and Edge-compatible APIs where needed

---

## Auth Middleware

Add a middleware that:

1. Extracts JWT from `Authorization` header (or cookie if configured)
2. Verifies it
3. Attaches user info to `c.var`

Example:

```ts
// src/middlewares/auth.ts
import type { MiddlewareHandler } from "hono";
import { getAuthConfig } from "../config/auth";
import { verifyAccessToken } from "./jwt-utils";

export type AuthUser = {
  id: string;
  email?: string;
  roles?: string[];
};

declare module "hono" {
  interface ContextVariableMap {
    user?: AuthUser;
  }
}

export const authMiddleware: MiddlewareHandler = async (c, next) => {
  const authHeader = c.req.header("Authorization");
  if (!authHeader?.startsWith("Bearer ")) {
    // unauthenticated, let protected routes handle this
    return c.json({ message: "Unauthorized" }, 401);
  }

  const token = authHeader.slice("Bearer ".length);
  const config = getAuthConfig();

  try {
    const payload = await verifyAccessToken(config.jwtSecret, token);
    c.set("user", {
      id: payload.sub,
      email: payload.email,
      roles: payload.roles ?? [],
    });
    await next();
  } catch (err) {
    console.error("JWT validation failed:", err);
    return c.json({ message: "Unauthorized" }, 401);
  }
};
```

**Alternative:** For some apps, you may want a “soft” auth that sets `user` only when token exists, allowing both public and authenticated access. This skill can implement that variant too.

---

## Role-Based Authorization

Implement a helper middleware to require certain roles:

```ts
// src/middlewares/require-role.ts
import type { MiddlewareHandler } from "hono";

export function requireRole(requiredRoles: string[]): MiddlewareHandler {
  return async (c, next) => {
    const user = c.get("user");
    if (!user) {
      return c.json({ message: "Unauthorized" }, 401);
    }

    const hasRole = user.roles?.some((role) => requiredRoles.includes(role));
    if (!hasRole) {
      return c.json({ message: "Forbidden" }, 403);
    }

    await next();
  };
}
```

Usage in routes:

```ts
import { authMiddleware } from "../../middlewares/auth";
import { requireRole } from "../../middlewares/require-role";

app.get(
  "/admin/stats",
  authMiddleware,
  requireRole(["admin"]),
  (c) => c.json({ ok: true }),
);
```

This skill should:

- Encourage composition (`authMiddleware` + `requireRole`) per route/route-group
- Avoid hardcoding roles in many places; centralize where possible

---

## Auth Routes

Create an `auth.routes.ts` under versioned routes (e.g., `/v1/auth`):

```ts
// src/routes/v1/auth.routes.ts
import { Hono } from "hono";
import { getAuthConfig } from "../../config/auth";
import { signAccessToken } from "../../middlewares/jwt-utils";

// In a real app, inject or import user storage/service
async function findUserByEmail(email: string) {
  // TODO: use real DB lookup (TypeORM, Supabase, etc.)
  return null as any;
}

export function authRoutes() {
  const app = new Hono();

  app.post("/login", async (c) => {
    const body = await c.req.json<{ email: string; password: string }>();

    // Validate inputs (this skill may integrate with a Hono validation skill later)
    if (!body.email || !body.password) {
      return c.json({ message: "Email and password are required" }, 400);
    }

    const user = await findUserByEmail(body.email);
    if (!user) {
      return c.json({ message: "Invalid credentials" }, 401);
    }

    // TODO: verify password using bcrypt/argon2 library
    const config = getAuthConfig();
    const accessToken = await signAccessToken(
      config.jwtSecret,
      {
        sub: user.id,
        email: user.email,
        roles: user.roles ?? [],
      },
      config.accessTokenTtlSeconds,
    );

    return c.json({ accessToken });
  });

  app.get("/me", async (c) => {
    const user = c.get("user");
    if (!user) {
      return c.json({ message: "Unauthorized" }, 401);
    }
    return c.json(user);
  });

  return app;
}
```

In `routes/v1/index.ts`, mount them:

```ts
import { authRoutes } from "./auth.routes";

export function createV1Routes() {
  const app = new Hono();
  app.route("/auth", authRoutes());
  // other routes
  return app;
}
```

This skill should:

- Keep auth routes small and composable.
- Defer actual user storage to DB/ORM skills.

---

## Cookies & Sessions (Optional Variation)

For browser-centric apps, this skill can:

- Set `httpOnly`, `secure` cookies with tokens on login.
- Read them from `c.req.cookie()` (or `c.req.header('Cookie')`) in middleware.

Example sketch:

```ts
// login route snippet
c.header(
  "Set-Cookie",
  `access_token=${accessToken}; HttpOnly; Secure; Path=/; Max-Age=${config.accessTokenTtlSeconds}`,
);
return c.json({ ok: true });
```

Middleware variant:

```ts
const token = c.req.cookie("access_token");
```

Adjust for runtime (Workers vs Node) and security (HTTPS only, domain, same-site).

---

## Integration with Other Skills

- `hono-app-scaffold`:
  - This skill assumes a structured app with `routes/` & `middlewares/` ready to extend.
- `hono-typeorm-backend` (future):
  - Provides user entity + repository; this auth skill will call into those.
- `nestjs-authentication` (conceptual similarities):
  - Shares patterns for JWT, roles, and password handling.

---

## Example Prompts That Should Use This Skill

- “Add JWT auth middleware and protect `/v1/users` routes.”
- “Implement login and `GET /me` in this Hono API.”
- “Use roles and protect admin routes in Hono.”
- “Switch auth from header-based to cookie-based for browser clients.”
- “Refactor our ad-hoc Hono auth into a clean middleware + routes setup.”

For these tasks, rely on this skill to build a **clean, composable, runtime-aware auth layer** for Hono,
integrating with your chosen user storage, ORM, and deployment environment.
