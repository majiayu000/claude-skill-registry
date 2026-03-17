---
name: backend-nodejs
description: |
  Modern Node.js backend stack: NestJS/Hono, Drizzle ORM, Vitest, TypeScript.
  Use when: building Node.js APIs, TypeScript backends, or serverless functions.
  Triggers: "nestjs", "node backend", "express", "hono", "drizzle", "vitest",
  "typescript api", "node api", "bun".
---

# Node.js Backend Stack

> **Live docs:** Add `use context7` to prompt for up-to-date Hono, Drizzle, Zod documentation.

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Testing | [testing.md](references/testing.md) — Vitest patterns, mocking, API tests |

## Tooling (2025)

| Tool | Purpose | Why |
|------|---------|-----|
| **pnpm** | Package manager | Fast, disk efficient |
| **Vitest** | Testing | Fast, ESM native, Jest compatible |
| **Drizzle** | ORM | Type-safe, lightweight, SQL-like |
| **Hono** | Web framework | Fast, lightweight, edge-ready |
| **NestJS** | Framework | Enterprise, DI, structured |
| **Zod** | Validation | Type inference, composable |
| **ESLint 9** | Linting | Flat config, modern |

## Project Setup

```bash
# Hono (lightweight)
pnpm create hono@latest my-api
cd my-api
pnpm add drizzle-orm postgres zod
pnpm add -D drizzle-kit vitest @types/node typescript

# NestJS (enterprise)
pnpm dlx @nestjs/cli new my-api
pnpm add drizzle-orm postgres
pnpm add -D drizzle-kit vitest
```

### TypeScript Config

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"]
}
```

### ESLint 9 Flat Config

```js
// eslint.config.js
import js from '@eslint/js';
import typescript from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';

export default [
  js.configs.recommended,
  {
    files: ['**/*.ts'],
    languageOptions: {
      parser: tsParser,
      parserOptions: { project: './tsconfig.json' },
    },
    plugins: { '@typescript-eslint': typescript },
    rules: {
      ...typescript.configs.recommended.rules,
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    },
  },
];
```

## Project Structure

```
src/
├── index.ts             # Entry point
├── config.ts            # Environment config
├── db/
│   ├── index.ts         # Drizzle client
│   ├── schema.ts        # Table definitions
│   └── migrate.ts       # Migration runner
├── routes/
│   ├── index.ts
│   ├── auth.ts
│   └── users.ts
├── services/
│   └── user.ts
├── middleware/
│   ├── auth.ts
│   └── error.ts
└── types/
    └── index.ts
tests/
├── setup.ts
└── users.test.ts
drizzle/
└── migrations/
```

## Hono Patterns

### Basic App

```typescript
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { HTTPException } from 'hono/http-exception';

const app = new Hono();

app.use('*', logger());
app.use('*', cors());

app.get('/', (c) => c.json({ status: 'ok' }));

app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return c.json({ error: err.message }, err.status);
  }
  console.error(err);
  return c.json({ error: 'Internal Server Error' }, 500);
});

export default app;
```

### Route with Validation

```typescript
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const users = new Hono();

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

users.post('/', zValidator('json', createUserSchema), async (c) => {
  const data = c.req.valid('json');
  const user = await userService.create(data);
  return c.json(user, 201);
});

users.get('/:id', async (c) => {
  const id = c.req.param('id');
  const user = await userService.findById(id);
  if (!user) {
    throw new HTTPException(404, { message: 'User not found' });
  }
  return c.json(user);
});

export default users;
```

### Auth Middleware

```typescript
import { createMiddleware } from 'hono/factory';
import { HTTPException } from 'hono/http-exception';
import { verify } from 'hono/jwt';

type Env = {
  Variables: { userId: string };
};

export const authMiddleware = createMiddleware<Env>(async (c, next) => {
  const header = c.req.header('Authorization');
  if (!header?.startsWith('Bearer ')) {
    throw new HTTPException(401, { message: 'Missing token' });
  }

  const token = header.slice(7);
  try {
    const payload = await verify(token, process.env.JWT_SECRET!);
    c.set('userId', payload.sub as string);
    await next();
  } catch {
    throw new HTTPException(401, { message: 'Invalid token' });
  }
});
```

## Drizzle ORM

### Schema Definition

```typescript
// src/db/schema.ts
import { pgTable, serial, varchar, timestamp, integer } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 100 }).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  userId: integer('user_id').references(() => users.id).notNull(),
  title: varchar('title', { length: 255 }).notNull(),
  body: varchar('body', { length: 10000 }),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

// Types
export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
```

### Database Client

```typescript
// src/db/index.ts
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

const client = postgres(process.env.DATABASE_URL!);
export const db = drizzle(client, { schema });
```

### Queries

```typescript
import { db } from '@/db';
import { users, posts } from '@/db/schema';
import { eq, desc } from 'drizzle-orm';

// Insert
const [user] = await db.insert(users)
  .values({ email: 'test@example.com', name: 'Test' })
  .returning();

// Select
const user = await db.query.users.findFirst({
  where: eq(users.email, 'test@example.com'),
});

// Select with relations
const userWithPosts = await db.query.users.findFirst({
  where: eq(users.id, userId),
  with: { posts: true },
});

// Update
await db.update(users)
  .set({ name: 'New Name' })
  .where(eq(users.id, userId));

// Delete
await db.delete(users).where(eq(users.id, userId));

// Pagination
const usersList = await db.select()
  .from(users)
  .orderBy(desc(users.createdAt))
  .limit(20)
  .offset(0);
```

### Migrations

```typescript
// drizzle.config.ts
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './drizzle/migrations',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

```bash
# Generate migration
pnpm drizzle-kit generate

# Apply migrations
pnpm drizzle-kit migrate

# Studio (GUI)
pnpm drizzle-kit studio
```

## Config with Zod

```typescript
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
});

export const env = envSchema.parse(process.env);
```

## Anti-patterns

| Don't | Do Instead |
|-------|------------|
| `npm` | `pnpm` |
| Jest | Vitest |
| Prisma (heavy) | Drizzle (lightweight) |
| Express (old) | Hono (modern, fast) |
| `.eslintrc` | `eslint.config.js` (flat config) |
| CommonJS | ESM (`"type": "module"`) |
| `any` types | Proper TypeScript types |
| Callback patterns | async/await |
