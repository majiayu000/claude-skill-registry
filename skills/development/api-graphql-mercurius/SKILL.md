---
name: api-graphql-mercurius
description: GraphQL server for Fastify with Mercurius — loaders, subscriptions, federation, JIT compilation
---

# GraphQL with Mercurius

> **Quick Guide:** Use Mercurius as a Fastify plugin for GraphQL APIs with built-in loader batching (solves N+1), JIT query compilation, subscriptions via WebSocket, and federation support. Register with `app.register(mercurius, { schema, resolvers, loaders })`. Loaders are Mercurius's killer feature: define them per-type to batch field resolution automatically. Use `jit: 1` to enable query compilation for production performance.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define loaders for any field that fetches related data — loaders solve the N+1 problem automatically through batching)**

**(You MUST use named constants for all numeric values — JIT thresholds, query depth limits, port numbers)**

**(You MUST return an array from loaders matching the exact length and order of the `queries` parameter)**

**(You MUST use `fastify.graphql.pubsub.publish()` inside mutations to trigger subscriptions — not external pubsub directly)**

</critical_requirements>

---

**Auto-detection:** Mercurius, mercurius, app.graphql, fastify.graphql, mercurius loaders, mercurius subscription, pubsub.publish, pubsub.subscribe, @mercuriusjs/federation, @mercuriusjs/gateway, mercurius-codegen, MercuriusContext, graphql-jit, withFilter, preParsing, preValidation, preExecution, onResolution

**When to use:**

- Building GraphQL APIs on Fastify (Mercurius is Fastify-native)
- Need automatic batching/caching for N+1 query prevention (loader system)
- Want JIT query compilation for production performance
- Building federated GraphQL services with `@mercuriusjs/federation`
- Need real-time subscriptions via WebSocket with built-in pubsub
- Want GraphQL lifecycle hooks (preParsing, preValidation, preExecution, onResolution)

**When NOT to use:**

- Not using Fastify (Mercurius is Fastify-only)
- Need a framework-agnostic GraphQL server
- Building a standalone schema-first design tool (use the schema library directly)
- Simple REST endpoints without GraphQL requirements

**Key patterns covered:**

- Plugin registration with schema, resolvers, and loaders
- Loader system for batched data fetching (the core differentiator)
- JIT compilation configuration for production performance
- Subscriptions with built-in pubsub and `withFilter`
- Federation services and gateway composition
- TypeScript context typing with `MercuriusContext` augmentation
- GraphQL lifecycle hooks for cross-cutting concerns

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Registration, resolvers, loaders, context, error handling, testing
- [examples/subscriptions.md](examples/subscriptions.md) - Pubsub, subscription resolvers, withFilter, WebSocket config
- [examples/federation.md](examples/federation.md) - Federated services, gateway, \_\_resolveReference as loader
- [reference.md](reference.md) - Decision frameworks, hook lifecycle, plugin options, anti-patterns

---

<philosophy>

## Philosophy

**Fastify-native GraphQL.** Mercurius is not a standalone server bolted onto Fastify — it is a Fastify plugin that deeply integrates with Fastify's lifecycle, encapsulation model, and plugin system. This means your GraphQL API inherits Fastify's performance characteristics and plugin architecture naturally.

**Loaders over DataLoader.** Instead of requiring a separate DataLoader library, Mercurius provides a built-in loader system. Loaders are defined per-type/per-field and receive batched queries automatically. This is simpler than manually instantiating DataLoader instances per-request and is the primary mechanism for solving the N+1 problem.

**JIT for production.** Mercurius uses graphql-jit to compile frequently-executed queries into optimized V8 functions. After a configurable threshold of executions, subsequent runs of the same query bypass the GraphQL execution engine entirely — delivering significant performance gains for repeated queries.

**Federation as a plugin.** Federation support is split into separate packages (`@mercuriusjs/federation` for services, `@mercuriusjs/gateway` for composition), keeping the core library lean for non-federated use cases.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Plugin Registration

Register Mercurius as a Fastify plugin with schema (SDL string), resolvers, and optional loaders.

```typescript
import Fastify from "fastify";
import mercurius from "mercurius";

const JIT_THRESHOLD = 1;
const SERVER_PORT = 3000;

const app = Fastify({ logger: true });

const schema = `
  type Query {
    user(id: ID!): User
    users: [User!]!
  }

  type User {
    id: ID!
    name: String!
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
  }
`;

app.register(mercurius, {
  schema,
  resolvers,
  loaders,
  jit: JIT_THRESHOLD,
  graphiql: process.env.NODE_ENV !== "production",
});
```

**Why good:** JIT threshold as named constant, GraphiQL disabled in production, loaders passed at registration level alongside resolvers

> Full registration with context, error handling, and all options: [examples/core.md](examples/core.md)

---

### Pattern 2: Loaders (N+1 Prevention)

Loaders are Mercurius's primary mechanism for batch data fetching. Define them per-type per-field. Each loader receives an array of `queries` (batched requests) and must return an array of results in the same order.

```typescript
const loaders = {
  User: {
    async posts(
      queries: Array<{ obj: User; params: Record<string, unknown> }>,
      context: MercuriusContext,
    ) {
      const userIds = queries.map(({ obj }) => obj.id);
      const allPosts = await fetchPostsByUserIds(userIds);
      // Return array matching queries order
      return queries.map(({ obj }) =>
        allPosts.filter((post) => post.authorId === obj.id),
      );
    },
  },
};
```

**Why good:** Single bulk query replaces N individual queries, result array matches input order (required), batching is automatic per-request

**Gotcha:** The returned array MUST match the length and order of `queries` — Mercurius maps results by index, not by key.

> Full loader patterns with caching options: [examples/core.md](examples/core.md)

---

### Pattern 3: Resolver Structure

Resolvers follow the standard GraphQL signature: `(parent, args, context, info)`. The context includes the Fastify `reply` object for accessing Fastify decorators.

```typescript
const resolvers = {
  Query: {
    user: async (
      _parent: unknown,
      args: { id: string },
      context: MercuriusContext,
    ) => {
      return context.reply.server.db.findUser(args.id);
    },
    users: async (
      _parent: unknown,
      _args: unknown,
      context: MercuriusContext,
    ) => {
      return context.reply.server.db.listUsers();
    },
  },
};
```

**Why good:** Accesses Fastify decorators via `context.reply.server`, standard GraphQL resolver signature

> Complete resolver examples with mutations: [examples/core.md](examples/core.md)

---

### Pattern 4: TypeScript Context Typing

Augment the `MercuriusContext` interface to get type-safe context in resolvers and loaders.

```typescript
import type { FastifyRequest, FastifyReply } from "fastify";

const buildContext = async (req: FastifyRequest, _reply: FastifyReply) => {
  return {
    userId: req.headers["x-user-id"] as string | undefined,
  };
};

type PromiseType<T> = T extends PromiseLike<infer U> ? U : T;

declare module "mercurius" {
  interface MercuriusContext extends PromiseType<
    ReturnType<typeof buildContext>
  > {}
}

// Registration
app.register(mercurius, {
  schema,
  resolvers,
  context: buildContext,
});
```

**Why good:** Context type is derived from the builder function, no manual interface duplication, resolvers get full type inference on `ctx.userId`

> Full TypeScript patterns with codegen: [examples/core.md](examples/core.md)

---

### Pattern 5: Subscriptions with PubSub

Enable subscriptions for real-time data. Mercurius provides a built-in pubsub system accessible via context.

```typescript
const NOTIFICATION_TOPIC = "NOTIFICATION_ADDED";

const resolvers = {
  Mutation: {
    addNotification: async (
      _parent: unknown,
      args: { message: string },
      context: MercuriusContext,
    ) => {
      const notification = { id: generateId(), message: args.message };
      await context.pubsub.publish({
        topic: NOTIFICATION_TOPIC,
        payload: { notificationAdded: notification },
      });
      return notification;
    },
  },
  Subscription: {
    notificationAdded: {
      subscribe: async (
        _parent: unknown,
        _args: unknown,
        context: MercuriusContext,
      ) => {
        return context.pubsub.subscribe(NOTIFICATION_TOPIC);
      },
    },
  },
};
```

**Why good:** Topic as named constant, pubsub accessed from context (Mercurius-managed), subscribe returns async iterator

> Full subscription patterns with withFilter and Redis: [examples/subscriptions.md](examples/subscriptions.md)

---

### Pattern 6: Federation Services

Build federated services with `@mercuriusjs/federation`. Define `__resolveReference` as a **loader** for batch entity resolution.

```typescript
import mercuriusFederation from "@mercuriusjs/federation";

const schema = `
  extend type Query {
    me: User
  }

  type User @key(fields: "id") {
    id: ID!
    name: String!
  }
`;

const loaders = {
  User: {
    async __resolveReference(queries: Array<{ obj: { id: string } }>) {
      const ids = queries.map(({ obj }) => obj.id);
      const users = await fetchUsersByIds(ids);
      return queries.map(({ obj }) => users.find((u) => u.id === obj.id));
    },
  },
};

app.register(mercuriusFederation, { schema, resolvers, loaders });
```

**Why good:** `__resolveReference` as loader prevents N+1 on entity resolution (strongly recommended by Mercurius docs), batch fetches all referenced entities at once

> Full federation with gateway: [examples/federation.md](examples/federation.md)

---

### Pattern 7: GraphQL Lifecycle Hooks

Mercurius provides hooks for cross-cutting concerns at specific points in the GraphQL execution lifecycle.

**Hook execution order:**

1. `preParsing` - Before query string parsing (tracing, query preprocessing)
2. `preValidation` - After parsing, before validation (skipped for cached queries)
3. `preExecution` - Before execution (auth, rate limiting, query modification)
4. `onResolution` - After execution completes (metrics, response logging)

```typescript
app.graphql.addHook("preExecution", async (schema, document, context) => {
  const startTime = performance.now();
  context.startTime = startTime;
});

app.graphql.addHook("onResolution", async (execution, context) => {
  const duration = performance.now() - context.startTime;
  context.reply.server.log.info({ duration }, "GraphQL query executed");
});
```

**Why good:** Hooks integrate with Fastify's logging, run at precise lifecycle points, can modify schema/document/variables in preExecution

**Warning:** Modifying `schema` or `document` in `preExecution` disables JIT compilation for that query.

> Full hook patterns: [reference.md](reference.md)

---

### Pattern 8: JIT Compilation Configuration

Enable JIT to compile frequently-executed queries into optimized V8 functions.

```typescript
const JIT_THRESHOLD = 1;
const MAX_QUERY_DEPTH = 10;

app.register(mercurius, {
  schema,
  resolvers,
  jit: JIT_THRESHOLD,
  queryDepth: MAX_QUERY_DEPTH,
});
```

**Why good:** `jit: 1` compiles after first execution (suitable for production with repeated queries), `queryDepth` prevents abuse, both values as named constants

**Gotcha:** JIT is disabled (default `0`) out of the box. Set `jit: 1` for production. Setting it higher (e.g., `5`) delays compilation until the query has been seen N times, which helps avoid compiling one-off queries.

</patterns>

---

<red_flags>

## RED FLAGS

### High Priority Issues

- **No loaders defined for related data fields** — Every field that fetches associated data (e.g., `User.posts`, `Post.author`) should use a loader, not inline resolver queries. Without loaders, you get the classic N+1 problem.
- **Loader returns wrong length/order** — The returned array MUST match the `queries` array by index. Returning fewer/more items or in wrong order corrupts the response silently.
- **`__resolveReference` as resolver instead of loader in federation** — Causes N+1 on entity resolution across services. The docs strongly recommend defining it as a loader.
- **JIT left at default (disabled)** — `jit: 0` means no JIT compilation. Set `jit: 1` for production workloads with repeated queries.

### Medium Priority Issues

- **Not using `context` function for per-request data** — Accessing request headers or auth tokens requires a context builder function, not Fastify decorators alone
- **GraphiQL enabled in production** — Set `graphiql: false` or conditionally disable based on `NODE_ENV`
- **Missing `queryDepth` limit** — Without depth limiting, deeply nested queries can exhaust server resources
- **Modifying schema/document in `preExecution`** — Disables JIT compilation for that query execution

### Common Mistakes

- **Using external DataLoader instead of Mercurius loaders** — Mercurius loaders are built-in and request-scoped by default; no need for manual DataLoader instantiation
- **Forgetting `subscription: true` in registration** — Subscriptions are disabled by default; subscription resolvers silently fail without this option
- **Publishing with wrong payload shape** — The `payload` in `pubsub.publish()` must match the subscription field name exactly (e.g., `{ notificationAdded: data }` for a `notificationAdded` subscription)
- **Calling `addHook` before `app.ready()`** — GraphQL hooks must be registered after `app.ready()` or inside a Fastify plugin that ensures readiness

> Detailed anti-pattern code examples: [reference.md](reference.md#anti-patterns-to-avoid)

### Gotchas & Edge Cases

- **Loader caching is enabled by default** — Within a single request, identical loader calls return cached results. Disable with `opts: { cache: false }` when data changes mid-request
- **`preValidation` is skipped for cached queries** — If a query is parsed from cache, validation hooks do not fire
- **Subscription context is different from query context** — Subscription context receives the WebSocket connection info, not the HTTP request. Use `subscription.context` option for custom subscription context
- **`connection_init` payload goes into `request.headers`** — During WebSocket handshake, properties from the client's `connection_init` payload are copied into request headers automatically
- **Gateway mode disables local schema/resolvers/loaders** — When running as a gateway, you cannot define `schema`, `resolvers`, or `loaders` on the gateway instance
- **`queryDepth` must be at least 7 for GraphiQL** — GraphiQL's introspection query requires depth 7+; lower values break the IDE

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST define loaders for any field that fetches related data — loaders solve the N+1 problem automatically through batching)**

**(You MUST use named constants for all numeric values — JIT thresholds, query depth limits, port numbers)**

**(You MUST return an array from loaders matching the exact length and order of the `queries` parameter)**

**(You MUST use `fastify.graphql.pubsub.publish()` inside mutations to trigger subscriptions — not external pubsub directly)**

**Failure to follow these rules will cause N+1 performance problems, corrupted GraphQL responses, and broken subscriptions.**

</critical_reminders>
