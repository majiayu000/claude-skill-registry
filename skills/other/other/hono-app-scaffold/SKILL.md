---
name: "hono-app-scaffold"
description: "Use this skill whenever the user wants to create, restructure, or standardize a Hono + TypeScript backend/API project, including project layout, runtime targeting (Node/Cloudflare/Vercel Edge), routing structure, middleware, env handling, and basic error handling."
---

# Hono App Scaffold Skill

## Purpose

You are a specialized assistant for **bootstrapping and reshaping Hono-based backends/APIs** in
TypeScript.

Use this skill to:

- Scaffold a **new Hono app** (standalone or part of a monorepo)
- Restructure an **existing Hono project** into a clean, feature-oriented layout
- Set up **runtime targeting** (Node, Cloudflare Workers, Vercel Edge, Bun)
- Wire up:
  - Basic routing structure (`routes/`)
  - Middleware: logging, CORS, error handling
  - Env management for the chosen runtime
- Prepare the project to later integrate:
  - Auth
  - TypeORM or other persistence
  - Cloudflare Workers / Edge deploy flows
  - API versioning

Do **not** use this skill for:

- Writing complex business logic → use feature-specific skills
- Detailed auth flows → use `hono-authentication` (once defined)
- Database/ORM design → use TypeORM-specific skills (`typeorm-*`)
- Frontend code or Next.js routing (covered by other skills)

If `CLAUDE.md` exists, follow its conventions (runtime choice, folder structure, linting tools, etc.).

---

## When To Apply This Skill

Trigger this skill when the user asks for something like:

- “Create a Hono API project.”
- “Move this ad-hoc Hono server into a proper structure.”
- “Set up a Hono app for Cloudflare Workers / Node / Bun.”
- “Give me a clean Hono + TS scaffold to build APIs on.”
- “Refactor this Hono file into routes + middlewares.”

Avoid when:

- The project is clearly NestJS-only or uses a different backend framework.
- We’re only adding one route to an already well-structured Hono project.

---

## Project Assumptions

Unless the project or `CLAUDE.md` says otherwise, assume:

- Language: **TypeScript**
- Package manager preference:
  1. `pnpm` if `pnpm-lock.yaml` exists
  2. `yarn` if `yarn.lock` exists
  3. otherwise `npm`
- Runtime: depends on context; default to **Node** when not specified,
  but be ready to target:
  - Node (Express-style server, `serve`/`listen`)
  - Cloudflare Workers / Pages
  - Vercel Edge / Node runtimes
  - Bun

- Testing: may be added later (Vitest/Jest + supertest/undici)

This skill should tailor the scaffold to the **declared runtime** when it’s clear.

---

## Target Project Structure

This skill aims to create or converge towards something like:

```text
project-root/
  src/
    app.ts              # main Hono app builder (routes + middleware)
    index.ts            # runtime-specific entry (Node, Cloudflare, etc.)
    routes/
      index.ts          # main router aggregator
      health.routes.ts
      v1/
        users.routes.ts
        auth.routes.ts
    middlewares/
      logger.ts
      error-handler.ts
      cors.ts
    config/
      env.ts            # env loading per runtime
      runtime.ts        # runtime-specific helpers if needed
    types/
      env.d.ts          # bindings/env typing for Workers/Cloudflare
  test/
    app.spec.ts         # basic smoke/e2e tests (optional stub)
  .env.example          # for Node/Bun/Vercel environments
  tsconfig.json
  package.json
  README.md
```

For Cloudflare Workers, also expect:

```text
  wrangler.toml
```

This layout can be adjusted to fit monorepos (e.g. `apps/hono-api/`), but the internal structure
under `src/` should remain consistent.

---

## High-Level Workflow

When this skill is active, follow this process:

### 1. Detect or create a Hono project

- If Hono is not installed / no project exists:
  - Install `hono` and runtime-specific packages (e.g. `@hono/node-server`, `@cloudflare/workers-types` if needed).
  - Create `src/` with `app.ts`, `routes/`, `middlewares/`, `config/`.
- If a Hono project exists as a single file (e.g. `index.ts`):
  - Refactor into `src/app.ts` + `src/routes/*` + `src/middlewares/*`.
  - Keep behavior equivalent but structure improved.

### 2. Choose runtime & entrypoint

Depending on context:

#### Node runtime (default):

- Use `@hono/node-server`:

  ```ts
  // src/index.ts
  import { serve } from "@hono/node-server";
  import { app } from "./app";

  const port = Number(process.env.PORT ?? 3000);
  console.log(`Listening on http://localhost:${port}`);

  serve({
    fetch: app.fetch,
    port,
  });
  ```

#### Cloudflare Workers:

- Export `app.fetch` as the Worker handler:

  ```ts
  // src/index.ts
  import { app } from "./app";

  export default {
    fetch: app.fetch,
  };
  ```

- Configure `wrangler.toml` outside this skill or with minimal defaults if necessary.

This skill should pick the right pattern based on what’s already present or user preference.

### 3. Build the main app (`app.ts`)

Create a central Hono app with basic middleware + routes:

```ts
// src/app.ts
import { Hono } from "hono";
import { loggerMiddleware } from "./middlewares/logger";
import { errorHandler } from "./middlewares/error-handler";
import { corsMiddleware } from "./middlewares/cors";
import { bindRoutes } from "./routes";

export const app = new Hono();

app.use("*", loggerMiddleware);
app.use("*", corsMiddleware);
app.use("*", errorHandler);

bindRoutes(app);
```

Or, if project prefers, mount middleware per route group instead of globally.

### 4. Routes Organization

Use `routes/index.ts` as a router aggregator:

```ts
// src/routes/index.ts
import type { Hono } from "hono";
import { healthRoutes } from "./health.routes";
import { createV1Routes } from "./v1";

export function bindRoutes(app: Hono) {
  app.route("/health", healthRoutes());

  app.route("/v1", createV1Routes());
}
```

Example `health.routes.ts`:

```ts
// src/routes/health.routes.ts
import { Hono } from "hono";

export function healthRoutes() {
  const app = new Hono();

  app.get("/", (c) => c.json({ status: "ok" }));

  return app;
}
```

Example `/v1` router:

```ts
// src/routes/v1/index.ts
import { Hono } from "hono";
import { usersRoutes } from "./users.routes";

export function createV1Routes() {
  const app = new Hono();

  app.route("/users", usersRoutes());

  return app;
}
```

Example users routes skeleton:

```ts
// src/routes/v1/users.routes.ts
import { Hono } from "hono";

export function usersRoutes() {
  const app = new Hono();

  app.get("/", async (c) => {
    // list users
    return c.json([]);
  });

  app.post("/", async (c) => {
    // create user
    const body = await c.req.json();
    return c.json({ id: "1", ...body }, 201);
  });

  app.get("/:id", async (c) => {
    const id = c.req.param("id");
    return c.json({ id });
  });

  return app;
}
```

This skill should keep routes small and composable.

### 5. Middleware Setup

#### Logger Middleware

```ts
// src/middlewares/logger.ts
import type { MiddlewareHandler } from "hono";

export const loggerMiddleware: MiddlewareHandler = async (c, next) => {
  const start = Date.now();
  await next();
  const ms = Date.now() - start;
  console.log(`${c.req.method} ${c.req.path} - ${ms}ms`);
};
```

#### Error Handler

```ts
// src/middlewares/error-handler.ts
import type { MiddlewareHandler } from "hono";

export const errorHandler: MiddlewareHandler = async (c, next) => {
  try {
    await next();
  } catch (err: any) {
    console.error("Unhandled error:", err);

    return c.json(
      {
        message: "Internal Server Error",
      },
      500,
    );
  }
};
```

#### CORS Middleware

Either a custom or `hono/cors` helper:

```ts
// src/middlewares/cors.ts
import type { MiddlewareHandler } from "hono";
import { cors } from "hono/cors";

// If project is fine with the helper:
export const corsMiddleware: MiddlewareHandler = cors({
  origin: "*", // adjust for security
  allowMethods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
});
```

This skill should:

- Set **secure defaults** where possible (explicit origins in production).
- Ensure order of middleware is appropriate (e.g., error handler should wrap downstream).

### 6. Env & Config Management

For Node/Vercel/Bun env:

```ts
// src/config/env.ts
export type AppEnv = {
  NODE_ENV: "development" | "test" | "production";
  PORT?: string;
  DATABASE_URL?: string;
};

export function getEnv(): AppEnv {
  return {
    NODE_ENV: (process.env.NODE_ENV as AppEnv["NODE_ENV"]) ?? "development",
    PORT: process.env.PORT,
    DATABASE_URL: process.env.DATABASE_URL,
  };
}
```

For Cloudflare Workers:

- Provide typed access to `env` via `c.env` and `Env` interface:

```ts
// src/types/env.d.ts
export interface Env {
  DATABASE_URL: string;
  // other bindings like R2, KV, etc.
}
```

```ts
// usage in route
app.get("/config", (c) => {
  const env = c.env as Env;
  return c.json({ db: env.DATABASE_URL });
});
```

This skill should:

- Avoid mixing Node-style `process.env` in Workers-only code.
- Encourage typed env where possible.

### 7. README & Scripts

Add or update `README.md` with:

- How to run in dev
- How to build
- How to deploy (basic notes for Node/Workers/Vercel)

Add `package.json` scripts (example for Node):

```jsonc
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc -p tsconfig.json",
    "start": "node dist/index.js",
    "lint": "eslint ."
  }
}
```

For Workers, may add `wrangler dev` and `wrangler publish` scripts.

---

## Integration with Other Skills

This skill prepares the ground for:

- `hono-authentication`:
  - Mount auth routes & middleware under `/v1/auth`.
- `hono-typeorm-backend`:
  - Add DB access to routes; integrate TypeORM or another ORM.
- `hono-edge-and-workers`:
  - Production-ready Cloudflare/Vercel Edge deployment config.
- TypeORM and caching skills:
  - DB caching logic within routes/services built on this scaffold.

---

## Example Prompts That Should Use This Skill

- “Create a new Hono API ready for Node/Cloudflare, with proper structure.”
- “Refactor this single-file Hono server into a clean modules/routes layout.”
- “Set up middlewares and basic routes for a Hono TS backend.”
- “Scaffold Hono app that I can later add auth and DB to.”

For these prompts, rely on this skill to generate or refactor a **clean, extensible Hono app skeleton**
that other backend skills can build on.
