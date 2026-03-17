---
name: fastify
description: Builds high-performance Node.js APIs with Fastify, TypeScript, schema validation, and plugins. Use when building fast REST APIs, microservices, or needing schema-based validation.
---

# Fastify

Fastify is a high-performance Node.js web framework. It's TypeScript-first, schema-driven, and can handle 76k+ requests/second.

## Quick Start

```bash
npm install fastify
npm install -D typescript @types/node
```

### Basic Server

```typescript
import Fastify from 'fastify'

const fastify = Fastify({
  logger: true
})

fastify.get('/', async (request, reply) => {
  return { hello: 'world' }
})

const start = async () => {
  try {
    await fastify.listen({ port: 3000 })
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}

start()
```

## TypeScript Setup

### Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "outDir": "./dist",
    "declaration": true
  }
}
```

### Typed Routes

```typescript
import Fastify, { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify'

const fastify: FastifyInstance = Fastify()

// Route with typed params
interface UserParams {
  id: string
}

fastify.get<{ Params: UserParams }>('/users/:id', async (request, reply) => {
  const { id } = request.params // typed as string
  return { userId: id }
})

// Route with typed body
interface CreateUserBody {
  email: string
  name?: string
}

fastify.post<{ Body: CreateUserBody }>('/users', async (request, reply) => {
  const { email, name } = request.body
  return { email, name }
})

// Route with typed query
interface ListUsersQuery {
  page?: number
  limit?: number
}

fastify.get<{ Querystring: ListUsersQuery }>('/users', async (request, reply) => {
  const { page = 1, limit = 10 } = request.query
  return { page, limit }
})
```

## Schema Validation

### JSON Schema

```typescript
const getUserSchema = {
  params: {
    type: 'object',
    properties: {
      id: { type: 'string' }
    },
    required: ['id']
  },
  response: {
    200: {
      type: 'object',
      properties: {
        id: { type: 'string' },
        email: { type: 'string' },
        name: { type: 'string' }
      }
    }
  }
}

fastify.get('/users/:id', { schema: getUserSchema }, async (request, reply) => {
  const { id } = request.params as { id: string }
  return db.users.findById(id)
})
```

### TypeBox (Recommended)

```bash
npm install @sinclair/typebox @fastify/type-provider-typebox
```

```typescript
import Fastify from 'fastify'
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'
import { Type, Static } from '@sinclair/typebox'

const fastify = Fastify().withTypeProvider<TypeBoxTypeProvider>()

// Define schemas
const UserSchema = Type.Object({
  id: Type.String(),
  email: Type.String({ format: 'email' }),
  name: Type.Optional(Type.String())
})

const CreateUserSchema = Type.Object({
  email: Type.String({ format: 'email' }),
  name: Type.Optional(Type.String())
})

type User = Static<typeof UserSchema>
type CreateUser = Static<typeof CreateUserSchema>

// Route with TypeBox
fastify.post('/users', {
  schema: {
    body: CreateUserSchema,
    response: {
      201: UserSchema
    }
  }
}, async (request, reply) => {
  // request.body is typed as CreateUser
  const user = await db.users.create(request.body)
  reply.status(201)
  return user
})
```

### Zod

```bash
npm install zod fastify-type-provider-zod
```

```typescript
import Fastify from 'fastify'
import { serializerCompiler, validatorCompiler, ZodTypeProvider } from 'fastify-type-provider-zod'
import { z } from 'zod'

const fastify = Fastify().withTypeProvider<ZodTypeProvider>()
fastify.setValidatorCompiler(validatorCompiler)
fastify.setSerializerCompiler(serializerCompiler)

const UserSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  name: z.string().optional()
})

fastify.post('/users', {
  schema: {
    body: z.object({
      email: z.string().email(),
      name: z.string().optional()
    }),
    response: {
      201: UserSchema
    }
  }
}, async (request, reply) => {
  const user = await db.users.create(request.body)
  reply.status(201)
  return user
})
```

## Plugins

### Creating Plugins

```typescript
import { FastifyPluginAsync } from 'fastify'
import fp from 'fastify-plugin'

interface PluginOptions {
  prefix?: string
}

const myPlugin: FastifyPluginAsync<PluginOptions> = async (fastify, options) => {
  fastify.decorate('utility', () => 'hello')

  fastify.addHook('onRequest', async (request, reply) => {
    request.startTime = Date.now()
  })
}

export default fp(myPlugin, {
  name: 'my-plugin',
  fastify: '5.x'
})
```

### Using Plugins

```typescript
import myPlugin from './plugins/my-plugin'
import dbPlugin from './plugins/db'

await fastify.register(myPlugin, { prefix: '/api' })
await fastify.register(dbPlugin)

// Scoped plugins
await fastify.register(async (instance) => {
  // Plugins registered here only affect this scope
  await instance.register(authPlugin)

  instance.get('/protected', async (request) => {
    return { user: request.user }
  })
}, { prefix: '/api' })
```

### Common Plugins

```typescript
// CORS
import cors from '@fastify/cors'
await fastify.register(cors, {
  origin: ['https://app.example.com'],
  credentials: true
})

// Helmet (security headers)
import helmet from '@fastify/helmet'
await fastify.register(helmet)

// Rate limiting
import rateLimit from '@fastify/rate-limit'
await fastify.register(rateLimit, {
  max: 100,
  timeWindow: '1 minute'
})

// JWT
import jwt from '@fastify/jwt'
await fastify.register(jwt, {
  secret: process.env.JWT_SECRET
})

// Cookie
import cookie from '@fastify/cookie'
await fastify.register(cookie, {
  secret: process.env.COOKIE_SECRET
})

// Multipart
import multipart from '@fastify/multipart'
await fastify.register(multipart)
```

## Hooks

### Request Lifecycle

```typescript
// Before routing
fastify.addHook('onRequest', async (request, reply) => {
  // Parse token, log request, etc.
})

// Before validation
fastify.addHook('preValidation', async (request, reply) => {
  // Modify request before validation
})

// Before handler
fastify.addHook('preHandler', async (request, reply) => {
  // Auth check, load data, etc.
})

// Before serialization
fastify.addHook('preSerialization', async (request, reply, payload) => {
  // Modify payload before JSON serialization
  return payload
})

// Before sending response
fastify.addHook('onSend', async (request, reply, payload) => {
  // Modify final response
  return payload
})

// After response sent
fastify.addHook('onResponse', async (request, reply) => {
  // Log response time, metrics, etc.
  const responseTime = Date.now() - request.startTime
  console.log(`${request.method} ${request.url} - ${responseTime}ms`)
})

// On error
fastify.addHook('onError', async (request, reply, error) => {
  // Log errors
  console.error(error)
})
```

### Route-Level Hooks

```typescript
fastify.route({
  method: 'GET',
  url: '/protected',
  preHandler: async (request, reply) => {
    const user = await verifyToken(request.headers.authorization)
    if (!user) {
      reply.code(401).send({ error: 'Unauthorized' })
      return
    }
    request.user = user
  },
  handler: async (request, reply) => {
    return { user: request.user }
  }
})
```

## Error Handling

### Error Handler

```typescript
fastify.setErrorHandler((error, request, reply) => {
  // Log error
  request.log.error(error)

  // Validation error
  if (error.validation) {
    return reply.status(400).send({
      error: 'VALIDATION_ERROR',
      message: 'Request validation failed',
      details: error.validation
    })
  }

  // Custom errors
  if (error.statusCode) {
    return reply.status(error.statusCode).send({
      error: error.code || 'ERROR',
      message: error.message
    })
  }

  // Internal error
  reply.status(500).send({
    error: 'INTERNAL_ERROR',
    message: 'Internal server error'
  })
})
```

### Custom Errors

```typescript
import createError from '@fastify/error'

const NotFoundError = createError('NOT_FOUND', 'Resource not found', 404)
const UnauthorizedError = createError('UNAUTHORIZED', 'Authentication required', 401)

fastify.get('/users/:id', async (request, reply) => {
  const user = await db.users.findById(request.params.id)
  if (!user) {
    throw new NotFoundError()
  }
  return user
})
```

## Authentication

### JWT Authentication

```typescript
import jwt from '@fastify/jwt'

await fastify.register(jwt, {
  secret: process.env.JWT_SECRET!
})

// Decorate with authenticate method
fastify.decorate('authenticate', async (request: FastifyRequest, reply: FastifyReply) => {
  try {
    await request.jwtVerify()
  } catch (err) {
    reply.send(err)
  }
})

// Protected route
fastify.get('/me', {
  onRequest: [fastify.authenticate]
}, async (request, reply) => {
  return request.user
})

// Login
fastify.post('/login', async (request, reply) => {
  const { email, password } = request.body as { email: string; password: string }

  const user = await db.users.findByEmail(email)
  if (!user || !await verifyPassword(password, user.passwordHash)) {
    reply.code(401).send({ error: 'Invalid credentials' })
    return
  }

  const token = fastify.jwt.sign({ id: user.id, email: user.email })
  return { token }
})
```

## Decorators

### Request Decorators

```typescript
// Extend FastifyRequest type
declare module 'fastify' {
  interface FastifyRequest {
    user?: { id: string; email: string }
    startTime?: number
  }
}

// Add to request
fastify.decorateRequest('user', null)
fastify.decorateRequest('startTime', 0)

// Use in hooks
fastify.addHook('onRequest', async (request) => {
  request.startTime = Date.now()
})
```

### Instance Decorators

```typescript
// Extend Fastify type
declare module 'fastify' {
  interface FastifyInstance {
    db: Database
    authenticate: (request: FastifyRequest, reply: FastifyReply) => Promise<void>
  }
}

fastify.decorate('db', database)
fastify.decorate('authenticate', authMiddleware)
```

## File Organization

### Autoload Plugins

```bash
npm install @fastify/autoload
```

```typescript
import autoLoad from '@fastify/autoload'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// Load all plugins from directory
await fastify.register(autoLoad, {
  dir: join(__dirname, 'plugins')
})

// Load all routes from directory
await fastify.register(autoLoad, {
  dir: join(__dirname, 'routes'),
  options: { prefix: '/api' }
})
```

### Route File Structure

```typescript
// routes/users/index.ts
import { FastifyPluginAsync } from 'fastify'

const users: FastifyPluginAsync = async (fastify) => {
  fastify.get('/', async (request, reply) => {
    return fastify.db.users.findMany()
  })

  fastify.get('/:id', async (request, reply) => {
    const { id } = request.params as { id: string }
    return fastify.db.users.findById(id)
  })

  fastify.post('/', async (request, reply) => {
    const user = await fastify.db.users.create(request.body)
    reply.code(201)
    return user
  })
}

export default users
```

## Testing

```bash
npm install -D tap
```

```typescript
import { test } from 'tap'
import build from './app'

test('GET /users returns users', async (t) => {
  const app = build()

  const response = await app.inject({
    method: 'GET',
    url: '/users'
  })

  t.equal(response.statusCode, 200)
  t.ok(Array.isArray(response.json()))
})

test('POST /users creates user', async (t) => {
  const app = build()

  const response = await app.inject({
    method: 'POST',
    url: '/users',
    payload: {
      email: 'test@example.com',
      name: 'Test User'
    }
  })

  t.equal(response.statusCode, 201)
  t.equal(response.json().email, 'test@example.com')
})
```

## Best Practices

1. **Use schema validation** - TypeBox or Zod for type safety
2. **Organize with plugins** - Encapsulate related functionality
3. **Use autoload** - Automatic plugin/route loading
4. **Handle errors properly** - Custom error handler
5. **Add request logging** - Built-in Pino logger
6. **Decorate for DI** - Add db, services to instance

## References

- [Plugins](references/plugins.md)
- [Performance](references/performance.md)
