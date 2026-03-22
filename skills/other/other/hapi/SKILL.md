---
name: hapi
description: "Use when building @hapi/hapi servers, routes, plugins, auth schemes, HTTP APIs, request lifecycle, caching, stale-while-revalidate, server methods, views, startup sequences, or response marshalling."
---

# Hapi


## Quick Start

    const server = Hapi.server({ port: 3000 });
    server.route({ method: 'GET', path: '/', handler: () => 'ok' });
    await server.start();


## Critical Rules

1. **Compose with decorations & methods** - Expose services via [decorations](reference/server/decorations.md) and reusable logic via [methods](reference/server/methods.md)
2. **Follow the lifecycle** - 24-step request flow; see [lifecycle overview](reference/lifecycle/overview.md)
3. **Auth is three layers** - scheme → strategy → default; see [server auth](reference/server/auth.md)
4. **Validate at the route** - Use joi schemas on params, query, payload, headers; see [validation](reference/route/validation.md)
5. **Type routes with Refs** - Use `ServerRoute<Refs>` pattern; see [route scaffold](reference/typescript/route-scaffold.md)


## Workflow

1. **Create server** - [server overview](reference/server/overview.md) for constructor options
2. **Register plugins** - [plugins](reference/server/plugins.md) and [plugin structure](reference/plugins/overview.md)
3. **Configure auth** - [auth schemes](reference/server/auth.md) and [route auth](reference/route/auth.md)
4. **Define routes** - [route overview](reference/route/overview.md) with [handlers](reference/route/handler.md)
5. **Add extensions** - [lifecycle hooks](reference/server/extensions.md) and [pre-handlers](reference/route/pre.md)


## Key Patterns

| Topic                    | Reference                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------ |
| Request/response objects | [request](reference/lifecycle/request-object.md), [response](reference/lifecycle/response-object.md)   |
| Response toolkit (h)     | [toolkit](reference/lifecycle/response-toolkit.md)                                                     |
| Sessions (yar)           | [sessions](reference/server/sessions.md)                                                                                                                                        |
| Caching & CORS           | [cache-cors](reference/route/cache-cors.md), [server cache](reference/server/cache.md), [catbox-memory engine](reference/server/catbox-memory.md), [catbox-fs engine](reference/server/catbox-fs.md), [catbox-redis engine](reference/server/catbox-redis.md) |
| Security headers         | [security](reference/route/security.md)                                                                |
| Payload parsing          | [payload](reference/route/payload.md)                                                                  |
| Decorations & methods    | [decorations](reference/server/decorations.md), [methods](reference/server/methods.md)                 |
| MIME types (mimos)       | [mimos](reference/server/mimos.md)                                                                     |
| Realms & plugin scoping  | [realm](reference/server/realm.md)                                                                     |
| Response marshalling      | [marshal pipeline](reference/lifecycle/response-marshal.md)                                            |
| File serving (inert)     | [overview](reference/file-serving/overview.md), [file handler](reference/file-serving/file-handler.md), [directory handler](reference/file-serving/directory-handler.md) |
| Basic authentication     | [basic auth](reference/auth/basic.md)                                                                   |
| Error handling (Boom)    | [boom errors](reference/lifecycle/boom.md)                                                              |
| Error filtering (Bounce) | [bounce utility](reference/lifecycle/bounce.md)                                                         |
| WebSockets (nes)         | [overview](reference/websockets/overview.md), [subscriptions](reference/websockets/subscriptions.md), [client](reference/websockets/client.md) |
| Startup & shutdown       | [startup lifecycle](reference/server/startup-lifecycle.md)                                              |
| Events                   | [events](reference/server/events.md)                                                                   |
| Testing (server.inject)  | [network](reference/server/network.md)                                                                 |
| TypeScript overview       | [typescript](reference/typescript.md)                                                                  |
| TypeScript auth typing   | [auth-scheme](reference/typescript/auth-scheme.md), [type-author](reference/typescript/type-author.md) |
| JWT authentication       | [jwt overview](reference/jwt-auth/overview.md), [validate function](reference/jwt-auth/validate.md), [token API](reference/jwt-auth/token-api.md) |
| TypeScript plugins       | [plugin-scaffold](reference/typescript/plugin-scaffold.md)                                             |
| Views & templates        | [vision overview](reference/views/overview.md), [engines](reference/views/engines.md), [context & layouts](reference/views/context.md) |
