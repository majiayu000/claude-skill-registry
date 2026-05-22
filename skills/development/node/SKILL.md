---
name: node
description: |
  Node.js LTS runtime and server-side JavaScript patterns for INVOOPAY backend.
  Use when: working with backend services, async operations, crypto, Buffer handling, or Node.js APIs.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Node Skill

Node.js 20 LTS runtime powering Express + TypeScript backend. Uses ES modules (`"type": "module"`) with tsx for development. PostgreSQL via `pg` with connection pooling. Sharp for image processing.

## Quick Start

### Module System (ESM)

```typescript
// backend/src/server.ts - Entry point
import app from './app.js';           // .js extension required for ESM
import { env } from './config/env.js';

app.listen(env.port, () => {
  console.log(`Backend listening on port ${env.port}`);
});
```

### Environment Configuration

```typescript
// backend/src/config/env.ts - Validated env with defaults
import dotenv from 'dotenv';
dotenv.config();

const required = (value: string | undefined, fallback?: string) => {
  if (value) return value;
  if (fallback !== undefined) return fallback;
  throw new Error('Missing required environment variable');
};

export const env = {
  port: Number(process.env.PORT ?? 4000),
  dbHost: process.env.DB_HOST ?? 'localhost',
  jwtSecret: required(process.env.JWT_SECRET, 'dev-only-secret'),
  nodeEnv: process.env.NODE_ENV ?? 'development',
};
```

### Database Connection Pool

```typescript
// backend/src/db/client.ts
import pg from 'pg';
const { Pool } = pg;

export const pool = new Pool({
  host: env.dbHost,
  max: 20,                    // Max connections
  idleTimeoutMillis: 30000,   // Close idle after 30s
  connectionTimeoutMillis: 2000,
});

pool.on('error', (err) => {
  console.error('Unexpected error on idle client', err);
  process.exit(-1);           // Crash on pool errors
});
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| ESM imports | Always use `.js` extension | `import { x } from './mod.js'` |
| `__dirname` | Use `import.meta.url` | `path.dirname(fileURLToPath(import.meta.url))` |
| Async/await | All I/O operations | `await pool.query(...)` |
| Buffer | Binary data handling | `Buffer.from(data, 'hex')` |
| crypto | Encryption/hashing | `crypto.randomBytes(32)` |

## Common Patterns

### Async Service Method

```typescript
export const productService = {
  async get(id: number, language: string = 'en') {
    const result = await pool.query(
      'SELECT * FROM products WHERE id = $1', [id]
    );
    if (!result.rows[0]) return null;
    return mapProduct(result.rows[0]);
  }
};
```

### Transaction with Rollback

```typescript
const client = await pool.connect();
try {
  await client.query('BEGIN');
  await client.query('INSERT ...', [...]);
  await client.query('UPDATE ...', [...]);
  await client.query('COMMIT');
} catch (error) {
  await client.query('ROLLBACK');
  throw error;
} finally {
  client.release();  // Always release!
}
```

## See Also

- [patterns](references/patterns.md) - Async patterns, error handling
- [types](references/types.md) - TypeScript integration
- [modules](references/modules.md) - Project structure, imports
- [errors](references/errors.md) - Error handling patterns

## Related Skills

For Express routes and middleware, see the **express** skill. For database queries, see the **postgresql** skill. For TypeScript patterns, see the **typescript** skill.