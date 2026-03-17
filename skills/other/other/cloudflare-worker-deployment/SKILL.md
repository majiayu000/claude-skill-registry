---
name: "cloudflare-worker-deployment"
description: "Use this skill whenever the user wants to deploy, configure, or refine deployment of a Hono/TypeScript backend (or similar Worker) to Cloudflare Workers/Pages using Wrangler, including wrangler.toml, environments, bindings, and basic release workflows."
---

# Cloudflare Worker Deployment Skill

## Purpose

You are a specialized assistant for **deploying TypeScript/Hono apps to Cloudflare Workers** in a
clean, repeatable, and environment-aware way.

Use this skill to:

- Set up or refine **`wrangler.toml`** for a Worker/Pages Functions service
- Decide and document **environments** (`dev`, `staging`, `production`)
- Configure **bindings**:
  - D1 (`[[d1_databases]]`)
  - R2 (`[[r2_buckets]]`)
  - KV, Durable Objects, etc. (if present)
- Set up **build & entrypoint** for:
  - Hono app (`app.ts` / `index.ts`)
  - Node runtime vs Worker runtime
- Design **deployment workflows** with Wrangler and CI (at a high level)
- Manage **secrets**, env vars, and per-env config

Do **not** use this skill for:

- Hono app routing/middleware itself → use `hono-app-scaffold`
- D1-specific schema or queries → use `hono-d1-integration`
- R2-specific flows → use `hono-r2-integration`
- Deep CI pipeline templates → use a dedicated CI/CD skill (e.g. `cloudflare-ci-cd-github-actions`)

If `CLAUDE.md` exists, follow its rules about deployment environments, Cloudflare accounts, and project conventions.

---

## When To Apply This Skill

Trigger this skill when the user asks for things like:

- “Deploy this Hono app to Cloudflare Workers.”
- “Create wrangler.toml for this project.”
- “Set up dev/staging/prod Workers environments.”
- “Wire D1/R2 bindings for my Worker.”
- “Help me go from local dev to production on Cloudflare.”
- “Fix deployment issues with this Cloudflare Worker.”

Avoid when:

- The project is deployed only to AWS, Vercel, etc., and Cloudflare is not involved.
- The user is editing business logic but deployment config is already stable.

---

## Assumptions & Project Context

By default, this skill assumes:

- **Language**: TypeScript
- **Framework**: Hono (or similar Worker-compatible TS entrypoint)
- **Runtime**: Cloudflare Workers (or Cloudflare Pages Functions)
- **Build tooling**: Wrangler’s native bundling (esbuild/miniflare) unless overridden
- **Structure** (adapt to actual project):

  ```text
  project-root/
    src/
      app.ts      # Hono app definition
      index.ts    # Worker entry that exports app.fetch
    wrangler.toml
    package.json
    tsconfig.json
  ```

Other layouts (monorepo, multiple apps) are supported but this is the default mental model.

---

## Entry Point Design

For a typical Hono + Workers app:

```ts
// src/index.ts
import { app } from "./app";

export default {
  fetch: app.fetch,
};
```

This is the file Wrangler will use as the Worker script entry (after bundling).

This skill will:

- Ensure `main`/`entrypoint` in `wrangler.toml` points at your built script (or `src/index.ts`).
- Avoid Node-only APIs in Worker code unless polyfilled by the bundler.

---

## Basic wrangler.toml Layout

### Single-Environment (Simple) Example

```toml
name = "my-hono-api"
main = "src/index.ts"
compatibility_date = "2025-01-01"

[vars]
NODE_ENV = "production"
```

For a **real project**, this skill will almost always recommend **multi-environment** config.

### Multi-Environment Example

```toml
name = "my-hono-api"
main = "src/index.ts"
compatibility_date = "2025-01-01"

[vars]
NODE_ENV = "development"

[env.staging]
vars = { NODE_ENV = "staging" }

[env.production]
vars = { NODE_ENV = "production" }
```

This skill should:

- Choose a **compatibility_date** (today-ish or a recent date) and keep it up to date.
- Suggest environment-specific overrides where needed.

---

## Adding D1 & R2 Bindings

When D1 is used (with `hono-d1-integration`):

```toml
[[d1_databases]]
binding = "DB"
database_name = "my_db"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

[env.staging]
[[env.staging.d1_databases]]
binding = "DB"
database_name = "my_db_staging"
database_id = "staging-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

[env.production]
[[env.production.d1_databases]]
binding = "DB"
database_name = "my_db_prod"
database_id = "prod-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

When R2 is used (with `hono-r2-integration`):

```toml
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"
preview_bucket_name = "my-bucket-dev"

[env.production]
[[env.production.r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket-prod"
preview_bucket_name = "my-bucket-prod-preview"
```

This skill will:

- Keep binding names (`DB`, `BUCKET`) consistent with the TypeScript Env typings.
- Help differentiate staging vs prod buckets/databases.

---

## Local Development Workflow

This skill should encourage a straightforward **dev loop**:

- Install Wrangler and dependencies.
- Use `wrangler dev` to run the Worker locally (or in “remote dev” mode).

Example `package.json` scripts:

```jsonc
{
  "scripts": {
    "dev": "wrangler dev",
    "build": "wrangler build",
    "deploy": "wrangler deploy",
    "deploy:staging": "wrangler deploy --env staging",
    "deploy:production": "wrangler deploy --env production"
  }
}
```

This skill should:

- Align scripts with the project’s package manager and naming conventions.
- Make sure `wrangler dev` runs against the correct entrypoint.

---

## Secrets & Environment Variables

Secrets should not be committed to the repo.

This skill should:

- Use Wrangler secrets for sensitive values:

  ```bash
  wrangler secret put JWT_SECRET
  wrangler secret put JWT_SECRET --env production
  ```

- Use `[vars]` in `wrangler.toml` only for **non-sensitive** values (or development-only):

  ```toml
  [vars]
  FEATURE_FLAG_COOL_THING = "on"
  ```

- Make sure code accesses secrets via `c.env` (Workers) or `env` in typed Env interface.

Example typed usage:

```ts
interface Env {
  DB: D1Database;
  BUCKET: R2Bucket;
  JWT_SECRET: string;
  NODE_ENV: "development" | "staging" | "production";
}
```

---

## Deploying to Different Environments

This skill should set clear conventions like:

- **Dev**: `wrangler dev` (local)
- **Staging**: `wrangler deploy --env staging`
- **Prod**: `wrangler deploy --env production`

It can also recommend using separate:

- Routes (e.g., staging subdomain)
- D1 databases & R2 buckets
- Flags (`NODE_ENV` or `APP_ENV`)

Typical wrangler extra fields:

```toml
[env.staging]
route = "staging-api.example.com/*"

[env.production]
route = "api.example.com/*"
```

Or using `routes` arrays for multiple domains/routes.

---

## Handling Build Output

Wrangler generally handles bundling automatically when you set `main = "src/index.ts"`.

This skill should:

- Avoid over-complicating the build unless you have a non-standard bundler.
- If using a custom build step, ensure `wrangler.toml` points to the built artifact instead:

  ```toml
  main = "dist/index.mjs"
  ```

  And `package.json` adds:

  ```jsonc
  {
    "scripts": {
      "build": "tsc",
      "deploy": "npm run build && wrangler deploy"
    }
  }
  ```

---

## Pages Functions Variant (Optional)

If the project uses **Cloudflare Pages + Functions**, entry and wrangler config differ slightly.

This skill should:

- Place functions in `functions/[[path]].ts` or `functions/api/[[path]].ts`.
- Export Hono app handlers accordingly:

  ```ts
  // functions/api/[[route]].ts
  import { app } from "../../src/app";

  export const onRequest = app.fetch;
  ```

- Use `wrangler.toml` minimally (Pages uses its own config).

Use this variant only when the project explicitly indicates Pages Functions (e.g., integration with a Next/React frontend in Pages).

---

## Error Diagnosis & Common Pitfalls

This skill should help debug issues like:

- **`ReferenceError: process is not defined`**:
  - Fix by removing Node-specific APIs or shimming, but prefer Worker-compatible alternatives.
- **Incorrect bindings** (`c.env.DB` undefined):
  - Check `wrangler.toml` binding names vs Env type vs actual code.
- **Mismatched environments**:
  - Using `wrangler dev` but expecting prod secrets/bindings.
- **Deploy succeeds but runtime fails**:
  - Check compatibility_date and Worker logs (`wrangler tail`).

It should guide through:

- Checking Wrangler logs (`wrangler tail`)
- Validating `wrangler.toml`
- Ensuring `main` and exports (default + fetch) are correct

---

## Interaction with Other Skills

- `hono-app-scaffold`:
  - Provides `src/app.ts` and `src/index.ts`. This skill focuses on `wrangler.toml` and deploy scripts.
- `hono-d1-integration`:
  - This skill creates D1 bindings; that one defines schema and query usage.
- `hono-r2-integration`:
  - This skill creates R2 bindings; that one defines upload/download logic.
- `cloudflare-d1-migrations-and-production-seeding` (future):
  - This deployment skill will call its patterns for migration before/after deploy.
- `cloudflare-observability-logging-monitoring` (future):
  - This skill uses Wrangler & Workers analytics; deployment skill ensures they’re wired correctly.

---

## Example Prompts That Should Use This Skill

- “Create wrangler.toml for this Hono + Workers app with D1 + R2.”
- “Set up dev/staging/prod environments on Cloudflare Workers.”
- “Add deploy scripts to package.json for this Worker.”
- “Fix my Worker deployment; it runs locally but not on Cloudflare.”
- “Wire secrets and env vars correctly for my Hono Worker.”

For such tasks, rely on this skill to produce a **clean, environment-aware Cloudflare Worker deployment setup**
that plays nicely with your Hono, D1, and R2 integration skills.
