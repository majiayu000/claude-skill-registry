---
name: Platform
description: This skill should be used when the user asks about "@effect/platform", "Effect HTTP client", "Effect HTTP server", "FileSystem", "KeyValueStore", "Terminal", "platform services", "HttpClient", "HttpServer", "Effect file operations", "Effect networking", or needs to understand Effect's platform-agnostic I/O capabilities.
version: 1.0.0
---

# Effect Platform

## Overview

`@effect/platform` provides cross-platform abstractions for:

- **HTTP Client** - Make HTTP requests
- **HTTP Server** - Build HTTP servers
- **FileSystem** - File operations
- **KeyValueStore** - Persistent storage
- **Terminal** - CLI interactions
- **Worker** - Background workers

## HTTP Client

### Installation

```bash
npm install @effect/platform
# For Node.js:
npm install @effect/platform-node
# For Bun:
npm install @effect/platform-bun
```

### Basic Requests

```typescript
import { HttpClient } from "@effect/platform"
import { NodeHttpClient } from "@effect/platform-node"
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const client = yield* HttpClient.HttpClient

  // GET request
  const response = yield* client.get("https://api.example.com/users")
  const data = yield* response.json

  return data
}).pipe(
  Effect.provide(NodeHttpClient.layer)
)
```

### Request Configuration

```typescript
const program = Effect.gen(function* () {
  const client = yield* HttpClient.HttpClient

  // POST with body
  const response = yield* client.post("https://api.example.com/users", {
    body: HttpClientRequest.jsonBody({ name: "Alice", email: "alice@example.com" })
  })

  // With headers
  const response = yield* client.get("https://api.example.com/protected", {
    headers: { Authorization: "Bearer token123" }
  })

  // With timeout
  const response = yield* client.get("https://api.example.com/slow").pipe(
    Effect.timeout("5 seconds")
  )
})
```

### Response Handling

```typescript
const program = Effect.gen(function* () {
  const client = yield* HttpClient.HttpClient
  const response = yield* client.get("https://api.example.com/data")

  // Parse as JSON
  const json = yield* response.json

  // Parse as text
  const text = yield* response.text

  // Get status
  const status = response.status

  // Get headers
  const contentType = response.headers["content-type"]
})
```

### Schema Validation

```typescript
import { HttpClient, HttpClientResponse } from "@effect/platform"
import { Schema } from "effect"

const User = Schema.Struct({
  id: Schema.Number,
  name: Schema.String,
  email: Schema.String
})

const program = Effect.gen(function* () {
  const client = yield* HttpClient.HttpClient
  const response = yield* client.get("https://api.example.com/users/1")

  // Validate response with schema
  const user = yield* HttpClientResponse.schemaBodyJson(User)(response)
  return user
})
```

## HTTP Server

### Basic Server

```typescript
import { HttpServer, HttpServerResponse } from "@effect/platform"
import { NodeHttpServer } from "@effect/platform-node"
import { Effect, Layer } from "effect"
import { createServer } from "node:http"

const app = HttpServer.router.empty.pipe(
  HttpServer.router.get("/", HttpServerResponse.text("Hello, World!")),
  HttpServer.router.get("/users", HttpServerResponse.json([
    { id: 1, name: "Alice" },
    { id: 2, name: "Bob" }
  ]))
)

const ServerLive = NodeHttpServer.layer(createServer, { port: 3000 })

const program = Effect.gen(function* () {
  yield* Effect.log("Server starting on port 3000")
  yield* Effect.never // Keep running
}).pipe(
  Effect.provide(HttpServer.router.Live(app)),
  Effect.provide(ServerLive)
)
```

### Route Parameters

```typescript
const app = HttpServer.router.empty.pipe(
  HttpServer.router.get(
    "/users/:id",
    Effect.gen(function* () {
      const params = yield* HttpServer.router.params
      const id = params.id
      return HttpServerResponse.json({ id, name: "User " + id })
    })
  )
)
```

### Request Body

```typescript
import { HttpServerRequest } from "@effect/platform"

const app = HttpServer.router.empty.pipe(
  HttpServer.router.post(
    "/users",
    Effect.gen(function* () {
      const request = yield* HttpServerRequest.HttpServerRequest
      const body = yield* request.json

      // Or with schema validation
      const validated = yield* HttpServerRequest.schemaBodyJson(CreateUser)(request)

      return HttpServerResponse.json({ created: true, user: validated })
    })
  )
)
```

## FileSystem

### Reading Files

```typescript
import { FileSystem } from "@effect/platform"
import { NodeFileSystem } from "@effect/platform-node"

const program = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem

  const content = yield* fs.readFileString("./config.json")

  const bytes = yield* fs.readFile("./image.png")

  const exists = yield* fs.exists("./file.txt")
}).pipe(
  Effect.provide(NodeFileSystem.layer)
)
```

### Writing Files

```typescript
const program = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem

  yield* fs.writeFileString("./output.txt", "Hello, World!")

  yield* fs.writeFile("./data.bin", new Uint8Array([1, 2, 3]))

  yield* fs.appendFileString("./log.txt", "New log entry\n")
})
```

### Directory Operations

```typescript
const program = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem

  yield* fs.makeDirectory("./new-dir", { recursive: true })

  const files = yield* fs.readDirectory("./src")

  yield* fs.remove("./temp", { recursive: true })

  yield* fs.copy("./source.txt", "./dest.txt")

  yield* fs.rename("./old.txt", "./new.txt")
})
```

### File Info

```typescript
const program = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem

  const stat = yield* fs.stat("./file.txt")

  console.log({
    size: stat.size,
    isFile: stat.type === "File",
    isDirectory: stat.type === "Directory",
    modified: stat.mtime
  })
})
```

## KeyValueStore

Persistent key-value storage:

```typescript
import { KeyValueStore } from "@effect/platform"
import { NodeKeyValueStore } from "@effect/platform-node"

const program = Effect.gen(function* () {
  const store = yield* KeyValueStore.KeyValueStore

  yield* store.set("user:1", JSON.stringify({ name: "Alice" }))

  const value = yield* store.get("user:1")

  yield* store.remove("user:1")

  const exists = yield* store.has("user:1")
}).pipe(
  Effect.provide(NodeKeyValueStore.layerFileSystem("./data"))
)
```

## Terminal

CLI interactions:

```typescript
import { Terminal } from "@effect/platform"
import { NodeTerminal } from "@effect/platform-node"

const program = Effect.gen(function* () {
  const terminal = yield* Terminal.Terminal

  const name = yield* terminal.readLine

  yield* terminal.display(`Hello, ${name}!`)
}).pipe(
  Effect.provide(NodeTerminal.layer)
)
```

## Complete Example: REST API

```typescript
import { HttpServer, HttpServerResponse, HttpServerRequest } from "@effect/platform"
import { NodeHttpServer } from "@effect/platform-node"
import { Effect, Layer, Schema } from "effect"
import { createServer } from "node:http"

// Schemas
const CreateUser = Schema.Struct({
  name: Schema.String,
  email: Schema.String
})

const User = Schema.Struct({
  id: Schema.Number,
  name: Schema.String,
  email: Schema.String
})

// In-memory store
let users: Schema.Schema.Type<typeof User>[] = []
let nextId = 1

// Routes
const app = HttpServer.router.empty.pipe(
  HttpServer.router.get("/users", HttpServerResponse.json(users)),

  HttpServer.router.post("/users", Effect.gen(function* () {
    const body = yield* HttpServerRequest.schemaBodyJson(CreateUser)
    const user = { id: nextId++, ...body }
    users.push(user)
    return HttpServerResponse.json(user, { status: 201 })
  })),

  HttpServer.router.get("/users/:id", Effect.gen(function* () {
    const { id } = yield* HttpServer.router.params
    const user = users.find(u => u.id === parseInt(id))
    return user
      ? HttpServerResponse.json(user)
      : HttpServerResponse.json({ error: "Not found" }, { status: 404 })
  }))
)

// Server
const ServerLive = NodeHttpServer.layer(createServer, { port: 3000 })

const main = HttpServer.serve(app).pipe(
  Effect.provide(ServerLive),
  Effect.catchAllCause(Effect.logError)
)

Effect.runPromise(main)
```

## Best Practices

1. **Use Schema validation** - Validate all external data
2. **Provide platform layers** - NodeHttpClient.layer, etc.
3. **Handle errors** - Network failures, file not found, etc.
4. **Use Effect.scoped for resources** - Files, connections
5. **Configure timeouts** - Prevent hanging requests

## Additional Resources

For comprehensive platform documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "HTTP Client" for making requests
- "HTTP Server" for building servers
- "FileSystem" for file operations
- "KeyValueStore" for persistent storage
- "Terminal" for CLI interactions
