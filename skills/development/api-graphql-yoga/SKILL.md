---
name: api-graphql-yoga
description: GraphQL Yoga v5 server, Envelop plugins, subscriptions, error masking
---

# GraphQL Yoga Patterns

> **Quick Guide:** Use `createYoga` + `createSchema` for a Fetch API-compatible GraphQL server that runs on any JS runtime. Yoga v5 uses Envelop for plugin composition, SSE for subscriptions by default, built-in error masking, and CORS out of the box. Import `GraphQLError` from `graphql` (not `graphql-yoga`) for intentional client-facing errors. Prefer Yoga-specific plugins over Envelop equivalents for HTTP-level optimizations.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST import `GraphQLError` from `'graphql'`, NOT from `'graphql-yoga'` -- it is the standard graphql-js export)**

**(You MUST prefer Yoga-specific plugins over Envelop equivalents -- Yoga plugins operate at the HTTP layer and can skip GraphQL execution entirely for cached/persisted results)**

**(You MUST use `createSchema` from `'graphql-yoga'` for schema-first -- passing raw `typeDefs`/`resolvers` objects directly to `createYoga` is not supported in v5)**

**(You MUST use named constants for all numeric values -- timeouts, TTLs, port numbers, limits)**

</critical_requirements>

---

**Auto-detection:** GraphQL Yoga, graphql-yoga, createYoga, createSchema, createPubSub, Envelop, useResponseCache, useCSRFPrevention, usePersistedOperations, GraphQL subscriptions SSE, error masking, maskedErrors, graphql-ws, Yoga plugin hooks, onRequest, onParams

**When to use:**

- Building a GraphQL server that needs to run on Node.js, Bun, Deno, or Cloudflare Workers
- APIs requiring subscriptions via SSE (default) or WebSocket
- Extending GraphQL execution with Envelop plugins (caching, auth, logging)
- File uploads using the GraphQL Multipart Request spec
- Production APIs needing error masking, CORS, and CSRF protection

**When NOT to use:**

- REST-only APIs without GraphQL needs
- Simple CRUD where a framework's built-in route handlers suffice
- When you need a federated gateway (consider a dedicated gateway solution)

**Key patterns covered:**

- Server setup with `createYoga` and `createSchema` (schema-first)
- Type-safe context with generics on `createYoga<ServerContext>`
- Envelop plugin system: lifecycle hooks, custom plugins, Yoga-specific plugins
- Subscriptions: SSE (default), WebSocket via `graphql-ws`, built-in PubSub
- Error masking and intentional `GraphQLError` exposure
- File uploads with WHATWG `File` scalar
- Production hardening: CORS, CSRF prevention, GraphQL Armor, logging
- Cross-runtime deployment: Node.js, Bun, Deno, Cloudflare Workers

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Server setup, schema, context, resolvers, cross-runtime deployment
- [examples/plugins.md](examples/plugins.md) - Envelop plugins, custom plugins, lifecycle hooks
- [examples/subscriptions.md](examples/subscriptions.md) - SSE, WebSocket, PubSub, filtering
- [examples/error-handling.md](examples/error-handling.md) - Error masking, GraphQLError, custom masking
- [examples/production.md](examples/production.md) - CORS, CSRF, response caching, persisted operations, logging
- [reference.md](reference.md) - Decision frameworks, plugin reference, production checklist

---

<philosophy>

## Philosophy

GraphQL Yoga is a **batteries-included, Fetch API-compatible GraphQL server**. Its core is built on the WHATWG Fetch API (`Request`/`Response`), making it runtime-agnostic -- the same server code deploys to Node.js, Bun, Deno, and edge runtimes. The Envelop plugin system provides composable middleware at both the HTTP and GraphQL execution layers.

**Schema approach:** Yoga is schema-library agnostic. Use `createSchema` (schema-first SDL), Pothos (code-first), or vanilla `graphql-js` -- anything that produces a `GraphQLSchema` works.

**Plugin priority:** When both an Envelop plugin and a Yoga-specific plugin exist for the same feature (caching, persisted operations, defer/stream), always choose the Yoga variant. Yoga plugins hook into the HTTP layer and can short-circuit before GraphQL execution begins, skipping parsing and validation entirely for cached or persisted results.

**Error philosophy:** All unexpected errors are masked by default in production. Intentional errors are thrown as `GraphQLError` from the `graphql` package -- these bypass masking and reach clients with their message and extensions intact.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Server Setup with createYoga

Create a Yoga instance with `createSchema` for SDL-based schemas. The yoga instance IS a Fetch API handler -- pass it directly to any runtime's HTTP server.

```typescript
import { createYoga, createSchema } from "graphql-yoga";
import { createServer } from "node:http";

const PORT = 4000;

const yoga = createYoga({
  schema: createSchema({
    typeDefs: /* GraphQL */ `
      type Query {
        greeting(name: String!): String!
      }
    `,
    resolvers: {
      Query: {
        greeting: (_, { name }) => `Hello, ${name}!`,
      },
    },
  }),
});

const server = createServer(yoga);
server.listen(PORT, () => {
  console.info(`Server running on http://localhost:${PORT}/graphql`);
});
```

**Why good:** `createSchema` wraps `makeExecutableSchema`, yoga instance is a standard Fetch handler, works on any runtime

See [examples/core.md](examples/core.md) for complete setup, cross-runtime deployment, and type-safe context.

---

### Pattern 2: Type-Safe Context

Pass a generic to `createYoga` for server-specific context typing. The `context` factory receives `YogaInitialContext` (containing `request` and `params`) and returns your custom context.

```typescript
import { createYoga, type YogaInitialContext } from "graphql-yoga";

interface ServerContext {
  req: IncomingMessage;
  res: ServerResponse;
}

const yoga = createYoga<ServerContext>({
  schema,
  context: async ({ request }: YogaInitialContext) => {
    const token = request.headers.get("authorization");
    return { user: token ? await verifyToken(token) : null };
  },
});
```

**Why good:** generic types flow to resolver context parameter, `request` uses standard Fetch API (not framework-specific `req`/`res`)

See [examples/core.md](examples/core.md) for full context patterns.

---

### Pattern 3: Envelop Plugin System

Plugins are passed in the `plugins` array. Use Yoga-specific plugins when available -- they operate at the HTTP layer and can skip GraphQL execution entirely.

```typescript
import { createYoga } from "graphql-yoga";
import { useResponseCache } from "@graphql-yoga/plugin-response-cache";

const CACHE_TTL_MS = 2_000;

const yoga = createYoga({
  schema,
  plugins: [
    useResponseCache({
      session: () => null,
      ttl: CACHE_TTL_MS,
    }),
  ],
});
```

**Why good:** Yoga response cache skips parsing/validation for cached results (Envelop equivalent cannot), plugins compose without conflicts

See [examples/plugins.md](examples/plugins.md) for custom plugins, lifecycle hooks, and all Yoga-specific plugins.

---

### Pattern 4: Subscriptions with SSE (Default)

Yoga uses Server-Sent Events by default for subscriptions -- no WebSocket setup needed. Use `AsyncGenerator` syntax in subscription resolvers.

```typescript
const schema = createSchema({
  typeDefs: /* GraphQL */ `
    type Subscription {
      countdown(from: Int!): Int!
    }
  `,
  resolvers: {
    Subscription: {
      countdown: {
        subscribe: async function* (_, { from }) {
          for (let i = from; i >= 0; i--) {
            await new Promise((resolve) => setTimeout(resolve, 1_000));
            yield { countdown: i };
          }
        },
      },
    },
  },
});
```

**Why good:** no WebSocket infrastructure needed, works through HTTP proxies and load balancers, `graphql-sse` library for clients

See [examples/subscriptions.md](examples/subscriptions.md) for PubSub, WebSocket setup, and filtering.

---

### Pattern 5: Error Masking and GraphQLError

Yoga masks all unexpected errors by default. Throw `GraphQLError` (from `graphql`) for intentional client-facing errors -- these bypass masking.

```typescript
import { GraphQLError } from "graphql";

const NOT_FOUND_CODE = "USER_NOT_FOUND";

throw new GraphQLError("User not found", {
  extensions: { code: NOT_FOUND_CODE },
});
```

**Why good:** unexpected errors never leak internals (database details, stack traces), intentional errors pass through with message + extensions

See [examples/error-handling.md](examples/error-handling.md) for custom masking, disabling masking, and development mode.

---

### Pattern 6: File Uploads

Yoga supports the GraphQL Multipart Request spec. Add a `File` scalar and receive WHATWG `File` objects in resolvers.

```typescript
const schema = createSchema({
  typeDefs: /* GraphQL */ `
    scalar File
    type Mutation {
      uploadFile(file: File!): Boolean!
    }
  `,
  resolvers: {
    Mutation: {
      uploadFile: async (_, { file }: { file: File }) => {
        const content = await file.arrayBuffer();
        // Process file content
        return true;
      },
    },
  },
});
```

**Why good:** uses standard WHATWG File API (same as browser), no extra packages needed, disable with `multipart: false`

See [examples/core.md](examples/core.md) for complete file upload patterns.

</patterns>

---

<decision_framework>

## Decision Framework

### Schema Approach

```
Need auto-generated types from SDL?
+-- YES --> createSchema (schema-first with typeDefs + resolvers)
+-- NO  --> Want full TypeScript inference in schema definition?
    +-- YES --> Code-first library (e.g. Pothos) -- pass resulting GraphQLSchema to Yoga
    +-- NO  --> Vanilla graphql-js GraphQLSchema
```

### Subscription Transport

```
Need subscriptions?
+-- YES --> Do clients need bidirectional communication?
|   +-- YES --> WebSocket via graphql-ws (add ws + graphql-ws packages)
|   +-- NO  --> SSE (default, zero config, works through proxies)
+-- NO  --> No subscription setup needed
```

### Plugin Selection

```
Feature available as Yoga-specific plugin?
+-- YES --> Use Yoga plugin (HTTP-level hooks, can skip execution)
+-- NO  --> Use Envelop plugin (GraphQL execution-level hooks)
```

### Yoga-Specific Plugins (Prefer Over Envelop)

| Plugin               | Package                                     | Why Yoga-specific                        |
| -------------------- | ------------------------------------------- | ---------------------------------------- |
| Response Cache       | `@graphql-yoga/plugin-response-cache`       | Skips execution for cached queries       |
| Persisted Operations | `@graphql-yoga/plugin-persisted-operations` | Rejects unknown operations at HTTP layer |
| Defer/Stream         | `@graphql-yoga/plugin-defer-stream`         | Streams via HTTP chunked encoding        |
| CSRF Prevention      | `@graphql-yoga/plugin-csrf-prevention`      | Requires custom header before parsing    |
| GraphQL SSE          | `@graphql-yoga/plugin-graphql-sse`          | Single-connection SSE mode               |

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority:**

- Importing `GraphQLError` from `graphql-yoga` instead of `graphql` -- wrong package, will fail
- Passing `typeDefs`/`resolvers` object directly to `createYoga` without `createSchema` -- not supported in v5
- Using an Envelop plugin when a Yoga-specific equivalent exists -- misses HTTP-level optimizations (the Yoga response cache skips parsing entirely; the Envelop equivalent cannot)
- Throwing plain `Error` in resolvers expecting clients to see the message -- masked to "Unexpected error." in production

**Medium Priority:**

- Not configuring CORS origins for production -- default is `*`, which should be locked down
- Using in-memory PubSub across multiple server instances -- events won't propagate (use Redis-backed `createRedisEventTarget`)
- Missing `graphql` peer dependency -- `graphql-yoga` requires `graphql` as a peer, install both
- Calling `createSchema` with no schema at all -- Yoga requires a schema; it does not infer one

**Gotchas & Edge Cases:**

- `YogaInitialContext.request` is a Fetch API `Request`, not a Node.js `IncomingMessage` -- use `request.headers.get()`, not `req.headers`
- Plugin execution order changed in v5 -- plugins added via `addPlugin` in `onPluginInit` now execute immediately after the adding plugin, not last
- `useResponseCache` `session` callback must return a string (user ID) for PRIVATE scope or `null` for public -- returning `undefined` breaks caching
- SSE subscriptions go through HTTP (text/event-stream) -- some proxies may buffer events; set `X-Accel-Buffering: no` for Nginx
- `File` scalar in uploads gives you a WHATWG `File` object -- use `.text()`, `.arrayBuffer()`, or `.stream()` methods (not Node.js `Buffer` directly)
- Yoga's built-in GraphiQL is enabled by default -- disable with `graphiql: false` in production
- `maskedErrors` set to `false` disables ALL masking including stack traces -- use custom `maskError` function instead for selective exposure
- CORS `credentials: true` with `origin: '*'` is rejected by browsers per the Fetch spec -- specify exact origins

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST import `GraphQLError` from `'graphql'`, NOT from `'graphql-yoga'` -- it is the standard graphql-js export)**

**(You MUST prefer Yoga-specific plugins over Envelop equivalents -- Yoga plugins operate at the HTTP layer and can skip GraphQL execution entirely for cached/persisted results)**

**(You MUST use `createSchema` from `'graphql-yoga'` for schema-first -- passing raw `typeDefs`/`resolvers` objects directly to `createYoga` is not supported in v5)**

**(You MUST use named constants for all numeric values -- timeouts, TTLs, port numbers, limits)**

**Failure to follow these rules will cause import errors, missed performance optimizations, and information leakage through unmasked errors.**

</critical_reminders>
