---
name: elysia-llm-docs
description: ElysiaJS framework for building type-safe, high-performance backend servers with Bun
agents: [nova]
triggers: [elysia, bun server, typescript backend, eden, end-to-end type safety]
llm_docs_url: https://elysiajs.com/llms.txt
---

# ElysiaJS Development Skill

Always consult [elysiajs.com/llms.txt](https://elysiajs.com/llms.txt) for code examples and latest API.

## Overview

ElysiaJS is a TypeScript framework for building Bun-first (but not limited to Bun) type-safe, high-performance backend servers. This skill provides comprehensive guidance for developing with Elysia, including routing, validation, authentication, plugins, integrations, and deployment.

## When to Use This Skill

Trigger this skill when the user asks to:

- Create or modify ElysiaJS routes, handlers, or servers
- Setup validation with TypeBox or other schema libraries (Zod, Valibot)
- Implement authentication (JWT, session-based, macros, guards)
- Add plugins (CORS, OpenAPI, Static files, JWT)
- Integrate with external services (Drizzle ORM, Better Auth, Next.js, Eden Treaty)
- Setup WebSocket endpoints for real-time features
- Create unit tests for Elysia instances
- Deploy Elysia servers to production

## Quick Start

Quick scaffold:

```bash
bun create elysia app
```

### Basic Server

```typescript
import { Elysia, t, status } from 'elysia'

const app = new Elysia()
    .get('/', () => 'Hello World')
    .post('/user', ({ body }) => body, {
      body: t.Object({
        name: t.String(),
        age: t.Number()
      })
    })
    .get('/id/:id', ({ params: { id } }) => {
      if(id > 1_000_000) return status(404, 'Not Found')
      return id
    }, {
      params: t.Object({
        id: t.Number({
          minimum: 1
        })
      }),
      response: {
        200: t.Number(),
        404: t.Literal('Not Found')
      }
    })
    .listen(3000)
```

## HTTP Methods

```typescript
import { Elysia } from 'elysia'

new Elysia()
  .get('/', 'GET')
  .post('/', 'POST')
  .put('/', 'PUT')
  .patch('/', 'PATCH')
  .delete('/', 'DELETE')
  .options('/', 'OPTIONS')
  .head('/', 'HEAD')
```

## TypeBox Validation

### Basic Types

```typescript
import { Elysia, t } from 'elysia'

.post('/user', ({ body }) => body, {
  body: t.Object({
    name: t.String(),
    age: t.Number(),
    email: t.String({ format: 'email' }),
    website: t.Optional(t.String({ format: 'uri' }))
  })
})
```

### File Upload

```typescript
.post('/upload', ({ body }) => body.file, {
  body: t.Object({
    file: t.File({
      type: 'image',
      maxSize: '5m'
    }),
    files: t.Files({
      type: ['image/png', 'image/jpeg']
    })
  })
})
```

### Response Validation

```typescript
.get('/user/:id', ({ params: { id } }) => ({
  id,
  name: 'John',
  email: 'john@example.com'
}), {
  params: t.Object({
    id: t.Number()
  }),
  response: {
    200: t.Object({
      id: t.Number(),
      name: t.String(),
      email: t.String()
    }),
    404: t.String()
  }
})
```

## Error Handling

```typescript
.get('/user/:id', ({ params: { id }, status }) => {
  const user = findUser(id)
  if (!user) {
    return status(404, 'User not found')
  }
  return user
})
```

## Guards (Apply to Multiple Routes)

```typescript
.guard({
  params: t.Object({
    id: t.Number()
  })
}, app => app
  .get('/user/:id', ({ params: { id } }) => id)
  .delete('/user/:id', ({ params: { id } }) => id)
)
```

## Macro

```typescript
.macro({
  hi: (word: string) => ({
    beforeHandle() { console.log(word) }
  })
})
.get('/', () => 'hi', { hi: 'Elysia' })
```

## Project Structure (Recommended)

```text
src/
├── index.ts              # Main server entry
├── modules/
│   ├── auth/
│   │   ├── index.ts      # Auth routes (Elysia instance)
│   │   ├── service.ts    # Business logic
│   │   └── model.ts      # TypeBox schemas/DTOs
│   └── user/
│       ├── index.ts
│       ├── service.ts
│       └── model.ts
└── plugins/
    └── custom.ts

public/                   # Static files (if using static plugin)
test/                     # Unit tests
```

## Key Concepts

### Encapsulation - Isolates by Default

Lifecycles (hooks, middleware) **don't leak** between instances unless scoped.

**Scope levels:**

- `local` (default) - current instance + descendants
- `scoped` - parent + current + descendants
- `global` - all instances

```ts
.onBeforeHandle(() => {}) // only local instance
.onBeforeHandle({ as: 'global' }, () => {}) // exports to all
```

### Method Chaining - Required for Types

**Must chain**. Each method returns new type reference.

❌ Don't:

```ts
const app = new Elysia()
app.state('build', 1) // loses type
app.get('/', ({ store }) => store.build) // build doesn't exist
```

✅ Do:

```ts
new Elysia()
  .state('build', 1)
  .get('/', ({ store }) => store.build)
```

### Explicit Dependencies

Each instance independent. **Declare what you use.**

```ts
const auth = new Elysia()
  .decorate('Auth', Auth)
  .model(Auth.models)

new Elysia()
  .use(auth) // must declare
  .get('/', ({ Auth }) => Auth.getProfile())
```

### Reference Model

Model can be referenced by name:

```ts
new Elysia()
  .model({
    book: t.Object({
      name: t.String()
    })
  })
  .post('/', ({ body }) => body.name, {
    body: 'book'
  })
```

Model can be renamed using `.prefix` / `.suffix`:

```ts
new Elysia()
  .model({
    book: t.Object({
      name: t.String()
    })
  })
  .prefix('model', 'Namespace')
  .post('/', ({ body }) => body.name, {
    body: 'Namespace.Book'
  })
```

## Best Practices

- **Controller**: Prefer Elysia as a controller for HTTP-dependent logic
- **Service**: Prefer class (or abstract class if possible), return `status` for errors
- **Models**: Always export validation model and type of validation model
- Prefer `return Error` instead of `throw Error`
- Use `onError` to handle local custom errors
- Register Model to Elysia instance via `Elysia.models({ ...models })`

## Integrations

- **Better Auth**: Authentication framework integration
- **Drizzle ORM**: Database ORM integration
- **Next.js**: API route integration
- **Expo**: Mobile API route integration
- **Cloudflare Workers**: Edge deployment

## Related Skills

- `effect-patterns` - Effect TypeScript integration
- `better-auth` - Authentication framework
- `bun-llm-docs` - Bun runtime documentation
