---
name: agent-backend
description: Fastify Node.js expert for .ts API files, REST endpoints, routes, middleware, handlers, PostgreSQL, SQL queries, pg.Pool, Zod schemas, validation, authentication, authorization, async/await, database connections, camelCase, type safety, error handling
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Backend Development Skill

Expert in Fastify backend API development following project conventions.

## When to Use This Skill

Use this skill when:

- Implementing API endpoints
- Creating or modifying business logic
- Working with middleware or authentication
- Database query implementation
- Any backend-related task

## CRITICAL: camelCase Everywhere (UNBREAKABLE RULE)

**ALL code, schemas, database columns, API requests/responses MUST use camelCase.**

### ✅ CORRECT

```typescript
interface User {
  id: string;
  firstName: string;      // camelCase
  lastName: string;
  createdAt: Date;        // camelCase
}

// Database queries - use camelCase columns
SELECT id, "firstName", "createdAt" FROM users;
```

### ❌ FORBIDDEN

```typescript
interface User {
  first_name: string; // NO snake_case!
  last_name: string; // NO snake_case!
}
```

**No Exceptions.** This applies to ALL new code.

## Schema-Query Alignment (CRITICAL)

**Before ANY endpoint is complete:**

### 1. Verify Schema Matches Query

```typescript
// ❌ WRONG - Schema requires field not in SELECT
const HouseholdSchema = z.object({
  id: z.string(),
  name: z.string(),
  adminUserId: z.string(), // ← Required but missing from query!
});

const result = await pool.query(
  'SELECT id, name FROM households', // ← Missing adminUserId
);

// ✅ CORRECT - Schema matches query
const HouseholdSchema = z.object({
  id: z.string(),
  name: z.string(),
  adminUserId: z.string().optional(), // ← Optional or included in query
});

const result = await pool.query('SELECT id, name, "adminUserId" FROM households');
```

### 2. Check Database Schema First

**ALWAYS read the database schema before writing Zod schemas:**

```bash
# Check what columns exist and if they're nullable
cat docker/postgres/init.sql | grep -A 20 "CREATE TABLE users"
```

**Make schema fields optional if:**

- Column is nullable in database
- Column doesn't exist in table yet
- SELECT query doesn't include the column

## Mandatory Local Testing (CRITICAL)

**BEFORE EVERY PUSH, run ALL checks from apps/backend:**

```bash
cd apps/backend

# 1. Type check
npm run type-check

# 2. Format check
npm run format:check

# 3. Tests
npm run test

# 4. Build
npm run build
```

**If ANY check fails:**

1. STOP - Do not proceed
2. Fix the issue
3. Re-run ALL checks
4. Only push when ALL pass

**Why:** CI feedback loop takes 3-5 minutes vs local checks in <1 minute. Type errors in production cause runtime failures.

## API Development Patterns

### Route Handler Template

```typescript
import { FastifyRequest, FastifyReply } from 'fastify';
import { z } from 'zod';
import { pool } from '../db';

// Define schemas with camelCase
const RequestSchema = z.object({
  userId: z.string(),
  taskName: z.string(),
});

const ResponseSchema = z.object({
  id: z.string(),
  taskName: z.string(),
  createdAt: z.string(),
});

export async function createTask(
  request: FastifyRequest<{ Body: z.infer<typeof RequestSchema> }>,
  reply: FastifyReply,
) {
  // Validate request
  const body = RequestSchema.parse(request.body);

  // Database query with camelCase columns
  const result = await pool.query(
    `INSERT INTO tasks ("userId", "taskName", "createdAt")
     VALUES ($1, $2, NOW())
     RETURNING id, "taskName", "createdAt"`,
    [body.userId, body.taskName],
  );

  // Validate response
  const task = ResponseSchema.parse(result.rows[0]);

  return reply.code(201).send(task);
}
```

### Error Handling

```typescript
export async function getUser(
  request: FastifyRequest<{ Params: { id: string } }>,
  reply: FastifyReply,
) {
  try {
    const result = await pool.query('SELECT id, "firstName", email FROM users WHERE id = $1', [
      request.params.id,
    ]);

    if (result.rows.length === 0) {
      return reply.code(404).send({ error: 'User not found' });
    }

    const user = UserSchema.parse(result.rows[0]);
    return reply.send(user);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return reply.code(500).send({ error: 'Data validation failed' });
    }
    throw error;
  }
}
```

## Database Query Best Practices

### Always Use Parameterized Queries

```typescript
// ✅ CORRECT - Prevents SQL injection
await pool.query('SELECT * FROM users WHERE id = $1', [userId]);

// ❌ WRONG - SQL injection vulnerability
await pool.query(`SELECT * FROM users WHERE id = '${userId}'`);
```

### Use camelCase Column Aliases

```typescript
// When querying snake_case columns (legacy), alias to camelCase
await pool.query(`
  SELECT
    id,
    first_name as "firstName",
    last_name as "lastName",
    created_at as "createdAt"
  FROM users
`);

// Or better: use camelCase columns in database
await pool.query(`
  SELECT id, "firstName", "lastName", "createdAt"
  FROM users
`);
```

## Validation Checklist

Before completing ANY endpoint:

- [ ] Read database schema (init.sql or SCHEMA.md)
- [ ] Compare schema fields with SELECT columns
- [ ] All required fields in Zod schema are in SELECT
- [ ] Optional fields marked as `.optional()` if nullable or not in table
- [ ] Test endpoint locally (no serialization errors)
- [ ] Run type-check, format-check, tests, build
- [ ] All checks pass

## Common Mistakes That Cause Runtime Errors

### Mistake 1: Required field not in database

```typescript
// ❌ Schema says required, but column doesn't exist
adminUserId: z.string();

// ✅ Check database first, make optional if needed
adminUserId: z.string().optional();
```

### Mistake 2: Nullable field required

```typescript
// ❌ Database column is nullable, schema requires it
description: z.string();

// ✅ Make it optional
description: z.string().optional();
```

### Mistake 3: SELECT doesn't match schema

```typescript
// ❌ Schema has fields not in SELECT
const schema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string(), // ← Not in SELECT!
});

await pool.query('SELECT id, name FROM users');

// ✅ Add to SELECT or make optional
await pool.query('SELECT id, name, email FROM users');
```

## Workflow

1. **Read** the optimized agent spec: `.claude/agents/agent-backend.md`
2. **Check** database schema for column names and types
3. **Implement** endpoint with camelCase throughout
4. **Validate** schema-query alignment
5. **Test** locally with ALL checks (type-check, format, tests, build)
6. **Test** endpoint manually (verify no errors)
7. **Only then** commit and push

## Reference Files

For detailed patterns and examples:

- `.claude/agents/agent-backend.md` - Complete agent specification
- `apps/backend/AGENTS.md` - Project-specific patterns (if exists)
- `CLAUDE.md` - Project-wide conventions
- `docker/postgres/init.sql` - Database schema

## Success Criteria

Before marking work complete:

- [ ] All local checks pass (type-check, format, tests, build)
- [ ] Endpoint tested locally (no errors)
- [ ] camelCase naming throughout
- [ ] Schema-query alignment verified
- [ ] Parameterized queries used
- [ ] Error handling implemented
