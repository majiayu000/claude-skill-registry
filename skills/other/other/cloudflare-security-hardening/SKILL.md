---
name: "cloudflare-security-hardening"
description: "Use this skill whenever the user wants to harden security for Cloudflare Workers/Pages APIs (e.g. Hono + TypeScript), including WAF-style protections, rate limiting, IP restrictions, secrets handling, and secure headers."
---

# Cloudflare Security Hardening Skill

## Purpose

You are a specialized assistant for **hardening Cloudflare-based backends** — especially
Hono + TypeScript apps running on **Cloudflare Workers/Pages**.

Use this skill to:

- Design or refine **security posture** for APIs on Cloudflare
- Configure or suggest:
  - Rate limiting / flood protection (app-level + Cloudflare edge)
  - IP allow/deny lists (where appropriate)
  - WAF-style protections (bot protection, OWASP filters, etc.)
  - Secure handling of secrets and env variables
  - CORS & cookie security options
  - Secure response headers (where relevant)
- Ensure the Hono/Worker code is **defensive by default**

Do **not** use this skill for:

- Business auth logic (login, JWT creation, roles) → use `hono-authentication` / auth skills
- Observability & logging → `cloudflare-observability-logging-monitoring`
- D1/R2 structural design → `hono-d1-integration`, `hono-r2-integration`

If `CLAUDE.md` defines security standards (CORS policy, rate limits, allowed IP ranges), obey them.

---

## When To Apply This Skill

Trigger this skill when the user asks for things like:

- “Harden security for my Cloudflare Worker API.”
- “Add rate limiting / abuse protection.”
- “Restrict access to specific IPs / regions.”
- “Secure CORS, cookies, and headers.”
- “Make sure secrets are handled safely with Workers.”

Avoid when:

- The question is purely business logic with no security angle.
- Security is enforced entirely by external infra (e.g. dedicated API gateway), and this Worker is a private backend behind that.

---

## Threat Model & Principles

This skill assumes:

- Your Hono + Workers API is **internet-exposed**.
- You want to protect against:
  - Brute-force / credential stuffing
  - Basic DDoS/flooding at the application level
  - Abuse of public endpoints (scrapers, bots, etc.)
  - CSRF / CORS misconfigurations for browser clients
  - Leaking secrets via logs or error responses

Guiding principles:

1. **Least privilege** – only expose necessary endpoints and data.
2. **Defense in depth** – combine Cloudflare edge protections + app-level checks.
3. **Secure defaults** – default to deny, then explicitly allow as needed.
4. **No secrets in code** – always use env/bindings for secrets.

---

## Edge-Level Protections (Cloudflare Dashboard)

Even though this skill cannot click the dashboard, it should **guide configuration**:

- **WAF / Security Center**:
  - Enable OWASP ModSecurity core rules (if available).
  - Turn on basic bot protection for public APIs.
- **Rate Limiting Rules**:
  - Example: limit `/auth/login` to N requests per minute per IP.
- **IP Access Rules**:
  - Allowlist internal tools (admin panels, /internal endpoints).
  - Block known bad IP ranges or countries where appropriate.

Example conceptual rule:

- Limit `POST /v1/auth/login` to **5 requests per minute per IP**.
- Block IPs that exceed that limit repeatedly.

This skill will describe how to **combine** these with app-level limits.

---

## App-Level Rate Limiting

Inside Hono/Workers, implement **additional rate protection** for critical routes:

- **Option A**: Use Cloudflare KV for simple counters.
- **Option B**: Use D1 or Durable Objects for more advanced needs.

Example KV-based simple limiter:

```ts
// src/middlewares/rate-limit.ts
import type { MiddlewareHandler } from "hono";

export function createRateLimitMiddleware(options: {
  kvBindingName: keyof Env;
  limit: number;
  windowSeconds: number;
  keyBuilder?: (c: any) => string;
}): MiddlewareHandler {
  return async (c, next) => {
    const kv = (c.env as any)[options.kvBindingName] as KVNamespace;
    const ip = c.req.header("CF-Connecting-IP") ?? "unknown";
    const keyBase = options.keyBuilder ? options.keyBuilder(c) : c.req.path;
    const key = `rate:${keyBase}:${ip}`;

    const currentRaw = await kv.get(key);
    const current = currentRaw ? parseInt(currentRaw, 10) : 0;

    if (current >= options.limit) {
      return c.json({ message: "Too Many Requests" }, 429);
    }

    if (!currentRaw) {
      await kv.put(key, "1", { expirationTtl: options.windowSeconds });
    } else {
      await kv.put(key, String(current + 1), { expirationTtl: options.windowSeconds });
    }

    await next();
  };
}
```

Attach to sensitive routes (login, signup, password reset):

```ts
app.post("/v1/auth/login", createRateLimitMiddleware({
  kvBindingName: "RATE_LIMIT_KV",
  limit: 5,
  windowSeconds: 60,
}), loginHandler);
```

This skill will:

- Emphasize that KV-based rate limiting is **best-effort** (not perfect under heavy concurrency).
- Suggest Cloudflare’s native rate limiting at edge as an additional layer.

---

## IP-based Restrictions (App Layer)

For admin or internal routes, add IP allowlisting:

```ts
// src/middlewares/ip-allowlist.ts
import type { MiddlewareHandler } from "hono";

export function ipAllowlist(allowedIps: string[]): MiddlewareHandler {
  return async (c, next) => {
    const ip = c.req.header("CF-Connecting-IP");
    if (!ip || !allowedIps.includes(ip)) {
      return c.json({ message: "Forbidden" }, 403);
    }
    await next();
  };
}
```

Usage:

```ts
app.route("/admin", (admin) => {
  admin.use("*", ipAllowlist(["1.2.3.4", "5.6.7.8"]));
  admin.get("/stats", statsHandler);
});
```

This skill should:

- Warn that IP allowlists break for users behind VPNs / mobile networks unless you control the infra.
- Suggest using **zero-trust** or identity-aware proxies for high-security use cases.

---

## CORS & Browser Security

For browser clients, configure CORS carefully:

- Default to **deny-all** unless explicitly needed.
- For allowed origins, specify exact domains (no `*` unless truly public APIs).

Example Hono CORS setup:

```ts
// src/middlewares/cors.ts
import { cors } from "hono/cors";

export const corsMiddleware = cors({
  origin: (origin) => {
    const allowed = [
      "https://app.example.com",
      "https://staging-app.example.com",
    ];
    if (!origin) return ""; // no origin (e.g., curl)
    return allowed.includes(origin) ? origin : "";
  },
  allowMethods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
  allowHeaders: ["Content-Type", "Authorization"],
  credentials: true,
});
```

This skill will:

- Ensure you don’t accidentally allow cross-site credential sharing with `origin: "*"`, `credentials: true`.
- Advise per-env origin lists (dev vs prod).

---

## Cookie & Session Security

When using cookies (e.g. for auth tokens), enforce:

- `HttpOnly` – prevent JS access.
- `Secure` – only over HTTPS.
- `SameSite` – `Lax` or `Strict` unless you require cross-site flows.

Example cookie header for Workers:

```ts
const token = "jwt-token-here";
c.header("Set-Cookie",
  `access_token=${token}; HttpOnly; Secure; Path=/; SameSite=Lax; Max-Age=900`,
);
```

This skill should:

- Discourage storing sensitive tokens in localStorage.
- Encourage short-lived access tokens + robust refresh strategy when needed (handled in auth skill).

---

## Secrets Management

This skill must enforce:

- All secrets are stored in Cloudflare **Worker secrets**, NOT in source code.

Use Wrangler:

```bash
wrangler secret put JWT_SECRET
wrangler secret put SENTRY_DSN
```

Then access via `c.env.JWT_SECRET`, `c.env.SENTRY_DSN` with proper typing in the `Env` interface.

It should:

- Warn against logging secrets or including them in error messages.
- Keep secrets **env-specific** if necessary (different keys per env).

---

## Secure Response Headers

Even though Workers don’t control all headers like a full web server, this skill can help add:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` (if no framing required)
- `Referrer-Policy: no-referrer` or similar
- `Strict-Transport-Security` *(only when behind HTTPS and with care)*

Example Hono middleware:

```ts
// src/middlewares/security-headers.ts
import type { MiddlewareHandler } from "hono";

export const securityHeaders: MiddlewareHandler = async (c, next) => {
  await next();
  c.header("X-Content-Type-Options", "nosniff");
  c.header("X-Frame-Options", "DENY");
  c.header("Referrer-Policy", "no-referrer");
  // HSTS usually added at the CDN/edge; be careful adding it here blindly.
};
```

Attach globally or per route group, depending on needs.

---

## Input Validation & Sanitization

This skill will **coordinate with validation skills** (Nest/Hono validation, DTOs, pipes) but also:

- Ensure inbound JSON is parsed safely.
- Encourage validation of all external input (query, path, body).
- Make sure DB queries are parameterized (D1) and object keys normalized in R2.

Example pattern (high-level):

- Validate `id` path params (UUID, numeric, etc.).
- Validate file types and size limits for uploads before hitting R2.

---

## Upload & Download Security for R2

When working with R2 (via `hono-r2-integration` + `cloudflare-r2-bucket-management-and-access`), this skill should:

- Enforce **allowed MIME types** for uploads.
- Enforce **max file size** (either at app level or via Cloudflare limits).
- Prevent directory traversal via keys — treat keys as opaque and sanitized.

Example in upload handler:

```ts
const allowedTypes = ["image/jpeg", "image/png"];
if (!allowedTypes.includes(file.type)) {
  return c.json({ message: "Unsupported file type" }, 415);
}

if (file.size > 5 * 1024 * 1024) {
  return c.json({ message: "File too large" }, 413);
}
```

---

## Admin & Debug Endpoint Lockdown

This skill will recommend:

- Protecting any admin/debug endpoints (`/admin`, `/metrics`, `/debug`) with:
  - Strong authentication (JWT/roles).
  - Optional IP allowlists.
- Never exposing:
  - Raw logs.
  - Environment variables.
  - Internal debug dumps to the public.

Example:

```ts
app.get("/admin/health", authMiddleware, requireRole(["admin"]), healthHandler);
```

---

## Security Review Checklist

When this skill is active, it can apply a checklist over the project:

1. **Secrets**: stored only in `c.env.*`, not in code/logs.
2. **Auth**: all protected routes use auth middleware.
3. **Admin**: admin-only endpoints have auth + optional IP lock.
4. **Rate limit**: login & other sensitive routes protected.
5. **CORS**: strict origins, correct credentials settings.
6. **Uploads**: type/size validation, safe key naming.
7. **Headers**: security headers present for browser-facing responses.
8. **Error messages**: no leakage of internals or stack traces to clients in prod.
9. **WAF / Edge rules**: Cloudflare edge configured where possible.

---

## Interaction With Other Skills

- `cloudflare-worker-deployment`:
  - This skill depends on its wrangler/env setup to choose policies per environment.
- `hono-authentication`:
  - Works together to ensure route-level auth + role enforcement.
- `hono-d1-integration` & `cloudflare-d1-migrations-and-production-seeding`:
  - Enforces parameterized queries and safe schema changes.
- `hono-r2-integration` & `cloudflare-r2-bucket-management-and-access`:
  - Secures upload/download logic and bucket-level access patterns.
- `cloudflare-observability-logging-monitoring`:
  - Observability for security logs (rate limit hits, blocked IPs, etc.).

---

## Example Prompts That Should Use This Skill

- “Harden security on my Hono API running on Cloudflare Workers.”
- “Add rate limiting and IP allowlists to sensitive routes.”
- “Lock down CORS and cookie security for my app.”
- “Secure R2 uploads and prevent abuse.”
- “Give me a security checklist for my Cloudflare Worker before going to prod.”

For such tasks, rely on this skill to push your Cloudflare Workers/Pages APIs towards a
**robust, production-ready security posture**, coordinated with auth, storage, and deployment skills.
