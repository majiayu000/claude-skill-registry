---
name: drizzle
description: Manage Drizzle ORM and drizzle-kit workflows for this repo, including schema generation, pushing migrations, and reset flows. Use when working with Drizzle, drizzle-kit, database schema changes, or migration resets.
---

# Drizzle

## Add a `drizzle.config.empty.ts` file

`drizzle.config.empty.ts` is a minimal drizzle-kit config that loads `DATABASE_URL` (preferring `.env.local` for non-production) and defines the target schema as itself. This config is used as a safe "empty schema" so `drizzle-kit push --force` can reset the database to no tables.

```ts
import * as dotenv from "dotenv"
import { defineConfig } from "drizzle-kit";

dotenv.config()

if (process.env.NODE_ENV !== "production") {
  dotenv.config({ path: ".env.local" })
}

if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL is not set")
}

export default defineConfig({
  dbCredentials: {
    url: process.env.DATABASE_URL,
  },
  dialect: "postgresql",
  schema: './drizzle.config.empty.ts',
});
```

Here's the script to reset the db then:
`npx drizzle-kit push --force --config ./drizzle.config.empty.ts`

## Quick Start

Use these scripts from `package.json`:
- `pnpm generate`: generate SQL migrations from the Drizzle schema
- `pnpm push`: push the current schema to the database
- `pnpm reset`: force-reset the database using `drizzle.config.empty.ts`
- `pnpm studio`: open Drizzle Studio

```json
{
  "scripts": {
    "generate": "drizzle-kit generate",
    "push": "drizzle-kit push",
    "reset": "npx drizzle-kit push --force --config ./drizzle.config.empty.ts",
    "studio": "drizzle-kit studio"
  }
}
```
