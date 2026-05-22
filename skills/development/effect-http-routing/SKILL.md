---
name: effect-http-routing
description: HTTP server, routing, JSON responses and dependencies via layers. Use when wiring endpoints and services.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# HTTP & Routing

## When to use
- Adding HTTP routes, path params, JSON responses
- Wiring handlers to services via layers
- Implementing small proxy/adapter endpoints

## Minimal Handler
```ts
import * as HttpRouter from "@effect/platform/HttpRouter"
import * as HttpServer from "@effect/platform/HttpServer"
import * as HttpResponse from "@effect/platform/HttpServerResponse"

const app = HttpRouter.empty.pipe(
  HttpRouter.get("/ping", Effect.succeed(HttpResponse.text("pong")))
)
```

## JSON
```ts
const userHandler = Effect.flatMap(HttpRouter.params, (p) =>
  Effect.flatMap(UserRepo, (r) => r.get(p["id"] ?? "")).pipe(
    Effect.flatMap(HttpResponse.json)
  )
)
```

## Serve (Node)
```ts
const server = HttpServer.serve(app)
// provide NodeHttpServer.layer(...) and dependencies
```

## Guidance
- Keep handlers thin: decode/validate, call service, encode response
- Use Schema for body/param validation; return structured errors
- Provide dependencies once via composed App layer

## Pitfalls
- Skipping validation on inputs → use Schema
- Doing heavy work in handler → push into services (layers)

## Cross-links
- Config & Schema for validation
- Layers & Services for DI wiring

## Local Source Reference

**CRITICAL: Search local Effect source before implementing**

The full Effect source code is available at `docs/effect-source/`. Always search the actual implementation before writing Effect code.

### Key Source Files
- HttpRouter: `docs/effect-source/platform/src/HttpRouter.ts`
- HttpServer: `docs/effect-source/platform/src/HttpServer.ts`
- HttpServerResponse: `docs/effect-source/platform/src/HttpServerResponse.ts`
- HttpServerRequest: `docs/effect-source/platform/src/HttpServerRequest.ts`

### Example Searches
```bash
# Find routing patterns
grep -F "HttpRouter.get" docs/effect-source/platform/src/HttpRouter.ts
grep -F "HttpRouter.post" docs/effect-source/platform/src/HttpRouter.ts

# Study response helpers
grep -F "json" docs/effect-source/platform/src/HttpServerResponse.ts
grep -F "text" docs/effect-source/platform/src/HttpServerResponse.ts
grep -F "html" docs/effect-source/platform/src/HttpServerResponse.ts

# Find server setup
grep -F "serve" docs/effect-source/platform/src/HttpServer.ts
grep -F "listen" docs/effect-source/platform/src/HttpServer.ts

# Look at request handling
grep -F "params" docs/effect-source/platform/src/HttpServerRequest.ts
grep -F "body" docs/effect-source/platform/src/HttpServerRequest.ts
grep -F "headers" docs/effect-source/platform/src/HttpServerRequest.ts
```

### Workflow
1. Identify the HTTP API you need (e.g., routing, responses)
2. Search `docs/effect-source/platform/src/` for the implementation
3. Study the types and routing patterns
4. Look at test files for usage examples
5. Write your code based on real implementations

**Real source code > documentation > assumptions**

## Real-world snippet: Compose Http API with Layer
```ts
import { HttpApiBuilder } from "@effect/platform"
import { Layer } from "effect"

// Bind feature-specific HTTP into the main API contract using a Layer
export const HttpLive = HttpApiBuilder.api(ApiContract).pipe(
  Layer.provide(FeatureHttpLive)
)
```

## References
- Agent Skills overview: https://www.anthropic.com/news/skills
- Skills guide: https://docs.claude.com/en/docs/claude-code/skills

