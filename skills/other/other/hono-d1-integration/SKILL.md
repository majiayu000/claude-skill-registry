---
name: "hono-d1-integration"
description: "Use this skill whenever the user wants to design, set up, or refactor Cloudflare D1 database usage in a Hono + TypeScript app running on Cloudflare Workers/Pages, including schema management, bindings, query patterns, and data-access structure."
---

# Hono + Cloudflare D1 Integration Skill

## Purpose

You are a specialized assistant for using **Cloudflare D1** as the database layer in
a **Hono + TypeScript** app running on **Cloudflare Workers / Pages**.

Use this skill to:

- Wire **D1 bindings** into a Hono app (`c.env.DB`)
- Design **schema and migrations** for D1 (via Wrangler)
- Implement **query helpers** and data-access patterns
- Structure **repositories/services** on top of D1
- Use **prepared statements**, parameters, and minimal ORM-style helpers
- Handle **migrations and seeding** for local/dev/test
- Keep D1 usage **runtime-safe** and **type-friendly**

Do **not** use this skill for:

- Hono app scaffolding → use `hono-app-scaffold`
- Non-D1 databases (Postgres/MySQL/etc.) → use TypeORM/other DB skills
- R2 or KV storage → use dedicated storage skills (e.g. `hono-r2-integration`)

If `CLAUDE.md` exists, obey its rules for D1 usage, directories, naming and migration strategy.

---

## When To Apply This Skill

Trigger this skill when the user asks for things like:

- “Use D1 as DB for this Hono API on Cloudflare.”
- “Wire up Hono routes to Cloudflare D1.”
- “Design tables and queries for D1 in this Worker.”
- “Refactor my raw D1 queries into a cleaner structure.”
- “Add migrations/seeding for D1 in this Hono app.”

Avoid this skill when:

- The Hono app is *not* running on Cloudflare Workers / Pages.
- The project has chosen a different DB for this service (e.g. PlanetScale, Supabase).

---

## Runtime & Binding Assumptions

This skill assumes:

- The app runs on **Cloudflare Workers** or **Pages Functions**.
- D1 is configured as a binding in `wrangler.toml`, e.g.:

  ```toml
  [[d1_databases]]
  binding = "DB"
  database_name = "my_db"
  database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  ```

- In code, D1 is available as `c.env.DB`.

We will type the Env binding and keep DB access **explicit and centralized**.

---

## Project Structure

This skill works best with a structure like:

```text
src/
  app.ts
  index.ts
  routes/
    v1/
      users.routes.ts
      posts.routes.ts
  db/
    schema.sql
    migrations/
      0001_init.sql
      0002_add_posts.sql
    d1.ts           # D1 helpers and typed Env
  services/
    user.service.ts
    post.service.ts
  types/
    env.d.ts        # Env interface with DB binding
```

Adjust paths to match the project, but keep D1-related files under a `db/` or `infrastructure/` style folder.

---

## Typing Env and D1 Binding

Create a shared Env type for Workers:

```ts
// src/types/env.d.ts
export interface Env {
  DB: D1Database;
  // other bindings e.g. R2, KV, etc.
}
```

Then in routes/services:

```ts
import type { Env } from "../types/env";

export type AppContext = {
  Bindings: Env;
};
```

Usage with Hono:

```ts
import { Hono } from "hono";
import type { AppContext } from "./types";
export const app = new Hono<AppContext>();
```

This ensures `c.env.DB` is correctly typed.

---

## D1 Helper Module

Create a small helper for D1 access and typed operations:

```ts
// src/db/d1.ts
import type { Env } from "../types/env";

export type D1 = D1Database;

export function getDb(env: Env): D1 {
  return env.DB;
}

export async function runQuery<T = unknown>(
  db: D1,
  sql: string,
  params: unknown[] = [],
): Promise<T[]> {
  const stmt = db.prepare(sql);
  const result = await stmt.bind(...params).all<T>();
  return result.results ?? [];
}
```

For single-row helpers:

```ts
export async function runOne<T = unknown>(
  db: D1,
  sql: string,
  params: unknown[] = [],
): Promise<T | null> {
  const rows = await runQuery<T>(db, sql, params);
  return rows[0] ?? null;
}
```

This skill should:

- Encourage **parameterized queries** via `.bind(...)`
- Avoid string interpolation that can cause SQL injection

---

## Schema & Migrations

D1 uses `schema.sql` and migrations managed via Wrangler.

### Basic Schema Layout

```sql
-- src/db/schema.sql
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE TABLE IF NOT EXISTS posts (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

Migrations are usually created & applied using commands like:

- `wrangler d1 execute <db_name> --file=src/db/schema.sql --local`
- `wrangler d1 migrations create <db_name> <name>`
- `wrangler d1 migrations apply <db_name> --local`

This skill should:

- Suggest migration commands but **not** assume CLI access inside code.
- Encourage keeping schema & migration SQL in version control.

---

## Service-Level Access Pattern

Design small services using `getDb` & query helpers.

Example `user.service.ts`:

```ts
// src/services/user.service.ts
import type { Env } from "../types/env";
import { getDb, runOne, runQuery } from "../db/d1";
import { nanoid } from "nanoid"; // if project uses this for IDs

export type User = {
  id: string;
  email: string;
  password_hash: string;
  created_at: string;
};

export class UserService {
  constructor(private env: Env) {}

  private db() {
    return getDb(this.env);
  }

  async createUser(email: string, passwordHash: string): Promise<User> {
    const id = nanoid();
    const db = this.db();

    await db
      .prepare("INSERT INTO users (id, email, password_hash) VALUES (?, ?, ?)")
      .bind(id, email, passwordHash)
      .run();

    const user = await runOne<User>(db, "SELECT * FROM users WHERE id = ?", [id]);
    if (!user) throw new Error("Failed to load just-created user");

    return user;
  }

  async findByEmail(email: string): Promise<User | null> {
    const db = this.db();
    return runOne<User>(db, "SELECT * FROM users WHERE email = ?", [email]);
  }

  async listUsers(): Promise<User[]> {
    const db = this.db();
    return runQuery<User>(db, "SELECT * FROM users ORDER BY created_at DESC");
  }
}
```

This skill should:

- Keep SQL in **small, readable strings**.
- Encapsulate DB access in services or repositories, not directly in route handlers (unless trivial).

---

## Using D1 in Hono Routes

Example: a simple users route using `UserService`:

```ts
// src/routes/v1/users.routes.ts
import { Hono } from "hono";
import type { AppContext } from "../../types";
import { UserService } from "../../services/user.service";

export function usersRoutes() {
  const app = new Hono<AppContext>();

  app.get("/", async (c) => {
    const service = new UserService(c.env);
    const users = await service.listUsers();
    return c.json(users);
  });

  app.post("/", async (c) => {
    const body = await c.req.json<{ email: string; password: string }>();
    // Validate body with a validation skill if present

    const service = new UserService(c.env);
    // Password hashing is done via auth skill (bcrypt/argon2) – here we assume `passwordHash`
    const passwordHash = "TODO"; // placeholder

    const user = await service.createUser(body.email, passwordHash);
    return c.json(user, 201);
  });

  return app;
}
```

This skill should:

- Encourage injecting `env` into services (no global state).
- Allow composition with `hono-authentication` (e.g., using D1 to fetch user in login).

---

## Transactions and Limits

D1 has more limited transaction semantics than full-blown SQL servers.

This skill should:

- Prefer simple, single-statement operations where possible.
- For multi-step operations, suggest careful ordering and error handling.
- Explicitly avoid patterns that rely on long-lived transactions or complex isolation.

---

## Type Safety Strategies

D1 returns rows as plain JS objects. This skill should:

- Define TypeScript types (`User`, `Post`, etc.) that match the schema.
- Use generic helpers (`runQuery<T>`) to type results.
- Optionally validate results in service logic (e.g., Zod) if project wants stronger runtime guarantees.

---

## Local Development & Testing

This skill can suggest:

- Using `wrangler d1` with `--local` for dev.
- Seeding data via SQL files or small scripts.
- For unit tests, mocking D1 methods instead of hitting real DB:

```ts
const mockDb: Partial<D1Database> = {
  prepare: jest.fn().mockReturnValue({
    bind: jest.fn().mockReturnThis(),
    all: jest.fn().mockResolvedValue({ results: [] }),
    run: jest.fn().mockResolvedValue({}),
  }),
};
```

- For integration tests in Workers env, tests can use `wrangler d1` to prepare DB before running.

When combined with a Hono testing skill, this gives end-to-end coverage.

---

## Error Handling

This skill must:

- Wrap database errors with useful messages when needed.
- Let general error-handling middleware (from `hono-app-scaffold`) convert them into HTTP responses.
- Avoid leaking sensitive data (SQL text, connection details) in responses.

Example pattern:

```ts
try {
  // D1 call
} catch (err) {
  console.error("D1 query failed:", err);
  throw new Error("Database error");
}
```

The error-handler middleware can then map `Error("Database error")` to a 500 JSON payload.

---

## Example Prompts That Should Use This Skill

- “Use Cloudflare D1 for persistence in this Hono API.”
- “Create D1 schema and wire up user routes in Hono.”
- “Refactor my raw D1 queries into a service layer.”
- “Help me design D1 tables + queries for this feature.”
- “Make D1 usage type-safe and structured in this Worker.”

For these tasks, rely on this skill to produce a **clean, Hono-friendly D1 integration** that is
typed, bound via the Env, and ready for production on Cloudflare Workers/Pages.
