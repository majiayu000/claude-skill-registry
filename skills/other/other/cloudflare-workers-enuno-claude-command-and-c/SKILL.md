---
name: cloudflare-workers
version: 1.4.0
description: Cloudflare Workers serverless platform for edge computing with workerd runtime, Wrangler CLI, Miniflare, Rust SDK (workers-rs), and official templates
---

# Cloudflare Workers Skill

Comprehensive assistance with Cloudflare Workers development, including the workerd runtime, Wrangler CLI, Miniflare local development, C3 project scaffolding, Rust SDK (workers-rs), and official starter templates.

## When to Use This Skill

This skill should be triggered when:
- Creating new Cloudflare Workers projects
- Working with Wrangler CLI commands
- Developing Workers locally with Miniflare
- Deploying Workers to Cloudflare's edge network
- Configuring Workers KV, Durable Objects, R2, D1, or Queues
- Debugging and testing Workers
- Setting up CI/CD for Workers
- Writing Workers in Rust with workers-rs
- Building WebAssembly-based Workers
- Self-hosting Workers with workerd runtime
- Understanding the Workers runtime architecture

## Quick Start

### Create a New Project (C3)

```bash
# Interactive project creation
npm create cloudflare@latest

# Create with specific framework
npm create cloudflare@latest my-app -- --framework=next
npm create cloudflare@latest my-api -- --framework=hono

# Accept defaults (quick start)
npm create cloudflare@latest my-worker -- -y

# TypeScript or JavaScript
npm create cloudflare@latest my-worker -- --lang=ts
npm create cloudflare@latest my-worker -- --lang=js
```

### Supported Frameworks

C3 supports: **Angular, Astro, Docusaurus, Gatsby, Hono, Next.js, Nuxt, Qwik, React, Remix, SolidStart, SvelteKit, Vue**

### C3 Options

| Option | Description |
|--------|-------------|
| `--framework` | Specify web framework (next, react, svelte, etc.) |
| `--type` | hello-world, hello-world-durable-object, scheduled, queues, openapi |
| `--category` | hello-world, web-framework, demo, remote-template |
| `--template` | Use external Git-hosted template |
| `--lang` | ts, js, or python |
| `--deploy` | Enable/disable automatic deployment (default: true) |
| `--git` | Initialize Git repository (default: true) |
| `-y` | Accept all defaults |

---

## Wrangler CLI Reference

### Authentication

```bash
# Login to Cloudflare (opens browser)
wrangler login

# Logout
wrangler logout

# Check current user
wrangler whoami
```

### Development

```bash
# Start local dev server with hot reload
wrangler dev

# Dev with specific config
wrangler dev --config wrangler.staging.toml

# Dev on specific port
wrangler dev --port 3000

# Local mode (no Cloudflare connection)
wrangler dev --local
```

### Deployment

```bash
# Deploy to Cloudflare
wrangler deploy

# Deploy to specific environment
wrangler deploy --env staging

# Deploy with dry run
wrangler deploy --dry-run

# Delete a Worker
wrangler delete

# Delete from specific environment
wrangler delete --env staging
```

### Version Management

```bash
# Upload version without deploying
wrangler versions upload

# Deploy version with gradual rollout
wrangler versions deploy

# List deployments
wrangler deployments list

# View deployment status
wrangler deployments status

# Rollback to previous version
wrangler rollback
```

### Monitoring & Logs

```bash
# Stream real-time logs
wrangler tail

# Filter by HTTP status
wrangler tail --status 500

# Filter by HTTP method
wrangler tail --method POST

# Filter by IP address
wrangler tail --ip-address 192.168.1.1

# Sample rate (0-1)
wrangler tail --sampling-rate 0.1
```

### KV Commands

```bash
# Create namespace
wrangler kv namespace create MY_KV

# List namespaces
wrangler kv namespace list

# Put a value
wrangler kv key put --binding=MY_KV "key" "value"

# Get a value
wrangler kv key get --binding=MY_KV "key"

# List keys
wrangler kv key list --binding=MY_KV

# Delete key
wrangler kv key delete --binding=MY_KV "key"

# Bulk operations (from JSON file)
wrangler kv bulk put --binding=MY_KV data.json
wrangler kv bulk delete --binding=MY_KV keys.json
```

### R2 Storage Commands

```bash
# Create bucket
wrangler r2 bucket create my-bucket

# List buckets
wrangler r2 bucket list

# Upload object
wrangler r2 object put my-bucket/path/file.txt --file=./local-file.txt

# Download object
wrangler r2 object get my-bucket/path/file.txt

# Delete object
wrangler r2 object delete my-bucket/path/file.txt

# Configure CORS
wrangler r2 bucket cors set my-bucket --rules='[{"origins":["*"]}]'

# Custom domain
wrangler r2 bucket domain add my-bucket my-cdn.example.com
```

### D1 Database Commands

```bash
# Create database
wrangler d1 create my-database

# List databases
wrangler d1 list

# Execute SQL
wrangler d1 execute my-database --command="SELECT * FROM users"

# Execute from file
wrangler d1 execute my-database --file=./schema.sql

# Create migration
wrangler d1 migrations create my-database migration-name

# Apply migrations
wrangler d1 migrations apply my-database

# Time travel (point-in-time recovery)
wrangler d1 time-travel info my-database
wrangler d1 time-travel restore my-database --timestamp=2024-01-01T00:00:00Z
```

### Secrets Management

```bash
# Add secret (interactive prompt)
wrangler secret put MY_SECRET

# Delete secret
wrangler secret delete MY_SECRET

# List secrets
wrangler secret list

# Bulk upload from file
wrangler secret bulk secrets.json
```

### Queues Commands

```bash
# Create queue
wrangler queues create my-queue

# List queues
wrangler queues list

# Add consumer
wrangler queues consumer add my-queue my-worker
```

### TypeScript Types

```bash
# Generate types from wrangler.toml bindings
wrangler types

# Include runtime types
wrangler types --include-runtime
```

### Global Options

| Option | Description |
|--------|-------------|
| `--config` | Specify custom config file |
| `--env` | Target specific environment |
| `--cwd` | Run from different directory |
| `--env-file` | Load environment variables from file |
| `--help` | Show command help |

---

## Configuration (wrangler.toml)

### Basic Configuration

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# Enable workers.dev subdomain
workers_dev = true

# Account ID (or use CLOUDFLARE_ACCOUNT_ID env var)
account_id = "your-account-id"
```

### Routes & Domains

```toml
# Single route
route = { pattern = "example.com/*", zone_name = "example.com" }

# Multiple routes
routes = [
  { pattern = "example.com/api/*", zone_name = "example.com" },
  { pattern = "api.example.com/*", zone_name = "example.com" }
]

# Custom domain
routes = [
  { pattern = "api.example.com", custom_domain = true }
]
```

### KV Bindings

```toml
[[kv_namespaces]]
binding = "MY_KV"
id = "abc123..."

# Preview namespace (for wrangler dev)
[[kv_namespaces]]
binding = "MY_KV"
id = "abc123..."
preview_id = "def456..."
```

### R2 Buckets

```toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"
```

### D1 Databases

```toml
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "abc123..."
```

### Durable Objects

```toml
[durable_objects]
bindings = [
  { name = "MY_DO", class_name = "MyDurableObject" }
]

[[migrations]]
tag = "v1"
new_classes = ["MyDurableObject"]
```

### Queues

```toml
# Producer
[[queues.producers]]
binding = "MY_QUEUE"
queue = "my-queue"

# Consumer
[[queues.consumers]]
queue = "my-queue"
max_batch_size = 10
max_batch_timeout = 30
```

### Environment Variables

```toml
[vars]
API_URL = "https://api.example.com"
DEBUG = "false"
```

### Scheduled Triggers (Cron)

```toml
[triggers]
crons = [
  "0 * * * *",      # Every hour
  "0 0 * * *",      # Daily at midnight
  "*/5 * * * *"     # Every 5 minutes
]
```

### Development Settings

```toml
[dev]
ip = "localhost"
port = 8787
local_protocol = "http"
```

### Environment-Specific Configuration

```toml
# Staging environment
[env.staging]
name = "my-worker-staging"
vars = { DEBUG = "true" }

[env.staging.routes]
pattern = "staging.example.com/*"
zone_name = "example.com"

# Production environment
[env.production]
name = "my-worker-production"
vars = { DEBUG = "false" }
```

### Resource Limits

```toml
[limits]
cpu_ms = 50
```

### Observability

```toml
[observability]
enabled = true

[observability.logs]
enabled = true
invocation_logs = true
head_sampling_rate = 1
```

---

## Miniflare (Local Development)

Miniflare is a local simulator for Cloudflare Workers using the `workerd` runtime.

### Installation

```bash
npm install miniflare --save-dev
```

### Programmatic Usage

```typescript
import { Miniflare } from "miniflare";

const mf = new Miniflare({
  script: `
    export default {
      async fetch(request, env) {
        return new Response("Hello from Miniflare!");
      }
    }
  `,
  modules: true,
});

// Dispatch a request
const response = await mf.dispatchFetch("http://localhost/");
console.log(await response.text());

// Cleanup
await mf.dispose();
```

### With Bindings

```typescript
const mf = new Miniflare({
  scriptPath: "./src/index.ts",
  modules: true,
  kvNamespaces: ["MY_KV"],
  r2Buckets: ["MY_BUCKET"],
  d1Databases: ["DB"],
  durableObjects: {
    MY_DO: "MyDurableObject"
  },
  bindings: {
    API_KEY: "secret-key"
  }
});

// Access bindings
const bindings = await mf.getBindings();
await bindings.MY_KV.put("key", "value");
```

### Persistence Options

```typescript
const mf = new Miniflare({
  scriptPath: "./src/index.ts",
  modules: true,
  kvPersist: true,           // Persist to .mf/kv
  r2Persist: "./data/r2",    // Custom path
  d1Persist: true,
  cachePersist: true,
});
```

### Multiple Workers

```typescript
const mf = new Miniflare({
  workers: [
    {
      name: "api",
      scriptPath: "./api/index.ts",
      modules: true,
      routes: ["*/api/*"]
    },
    {
      name: "frontend",
      scriptPath: "./frontend/index.ts",
      modules: true,
      routes: ["*"]
    }
  ]
});
```

### Debugging with Inspector

```typescript
const mf = new Miniflare({
  scriptPath: "./src/index.ts",
  modules: true,
  inspectorPort: 9229,  // Connect Chrome DevTools
  verbose: true,        // Detailed logging
});
```

### Core API Methods

| Method | Description |
|--------|-------------|
| `dispatchFetch(url, init?)` | Send HTTP request to worker |
| `getBindings()` | Get all worker bindings |
| `getWorker(name?)` | Get specific worker instance |
| `getCaches()` | Get CacheStorage instance |
| `getD1Database(binding)` | Get D1 database instance |
| `dispose()` | Cleanup and shutdown |

---

## Common Patterns

### Basic Fetch Handler

```javascript
export default {
  async fetch(request, env, ctx) {
    return new Response('Hello World!', {
      headers: { 'Content-Type': 'text/plain' }
    });
  }
};
```

### JSON API Response

```javascript
export default {
  async fetch(request, env, ctx) {
    const data = { message: 'Hello from Workers', timestamp: Date.now() };
    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
```

### Router Pattern

```javascript
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    switch (url.pathname) {
      case '/api/users':
        return handleUsers(request, env);
      case '/api/posts':
        return handlePosts(request, env);
      default:
        return new Response('Not Found', { status: 404 });
    }
  }
};
```

### Request Method Handling

```javascript
export default {
  async fetch(request, env, ctx) {
    switch (request.method) {
      case 'GET':
        return handleGet(request, env);
      case 'POST':
        const body = await request.json();
        return handlePost(body, env);
      case 'PUT':
        return handlePut(request, env);
      case 'DELETE':
        return handleDelete(request, env);
      default:
        return new Response('Method Not Allowed', { status: 405 });
    }
  }
};
```

### Workers KV Storage

```javascript
export default {
  async fetch(request, env, ctx) {
    // Write to KV
    await env.MY_KV.put('key', 'value', { expirationTtl: 3600 });

    // Read from KV
    const value = await env.MY_KV.get('key');

    // Read as JSON
    const data = await env.MY_KV.get('data', { type: 'json' });

    // Delete from KV
    await env.MY_KV.delete('key');

    // List keys
    const list = await env.MY_KV.list({ prefix: 'user:' });

    return new Response(value);
  }
};
```

### D1 Database

```javascript
export default {
  async fetch(request, env, ctx) {
    // Query
    const { results } = await env.DB.prepare(
      "SELECT * FROM users WHERE id = ?"
    ).bind(1).all();

    // Insert
    await env.DB.prepare(
      "INSERT INTO users (name, email) VALUES (?, ?)"
    ).bind("John", "john@example.com").run();

    // Batch
    const batch = await env.DB.batch([
      env.DB.prepare("INSERT INTO users (name) VALUES (?)").bind("Alice"),
      env.DB.prepare("INSERT INTO users (name) VALUES (?)").bind("Bob"),
    ]);

    return Response.json(results);
  }
};
```

### R2 Object Storage

```javascript
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);

    switch (request.method) {
      case 'PUT':
        await env.MY_BUCKET.put(key, request.body, {
          httpMetadata: {
            contentType: request.headers.get('Content-Type')
          }
        });
        return new Response('Uploaded');

      case 'GET':
        const object = await env.MY_BUCKET.get(key);
        if (!object) return new Response('Not Found', { status: 404 });
        return new Response(object.body, {
          headers: { 'Content-Type': object.httpMetadata.contentType }
        });

      case 'DELETE':
        await env.MY_BUCKET.delete(key);
        return new Response('Deleted');
    }
  }
};
```

### Durable Objects

```javascript
// Worker entry point
export default {
  async fetch(request, env, ctx) {
    const id = env.COUNTER.idFromName('global');
    const stub = env.COUNTER.get(id);
    return stub.fetch(request);
  }
};

// Durable Object class
export class Counter {
  constructor(state, env) {
    this.state = state;
  }

  async fetch(request) {
    let count = (await this.state.storage.get('count')) || 0;

    if (request.method === 'POST') {
      count++;
      await this.state.storage.put('count', count);
    }

    return Response.json({ count });
  }
}
```

### Queues Producer/Consumer

```javascript
// Producer
export default {
  async fetch(request, env, ctx) {
    await env.MY_QUEUE.send({
      type: 'email',
      to: 'user@example.com',
      subject: 'Hello'
    });
    return new Response('Queued');
  }
};

// Consumer
export default {
  async queue(batch, env, ctx) {
    for (const message of batch.messages) {
      console.log('Processing:', message.body);
      // Process message
      message.ack();
    }
  }
};
```

### CORS Headers

```javascript
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization'
};

export default {
  async fetch(request, env, ctx) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    const response = await handleRequest(request, env);
    return new Response(response.body, {
      ...response,
      headers: { ...response.headers, ...corsHeaders }
    });
  }
};
```

### Caching with Cache API

```javascript
export default {
  async fetch(request, env, ctx) {
    const cache = caches.default;

    // Try cache first
    let response = await cache.match(request);

    if (!response) {
      // Cache miss - fetch from origin
      response = await fetch(request);

      // Cache for 1 hour
      response = new Response(response.body, response);
      response.headers.set('Cache-Control', 'max-age=3600');

      ctx.waitUntil(cache.put(request, response.clone()));
    }

    return response;
  }
};
```

### Scheduled Events (Cron)

```javascript
export default {
  async scheduled(event, env, ctx) {
    console.log('Cron executed at:', new Date(event.scheduledTime));

    // Perform background task
    await env.MY_KV.put('last_run', event.scheduledTime.toString());

    // Make external API call
    await fetch('https://api.example.com/webhook', {
      method: 'POST',
      body: JSON.stringify({ timestamp: event.scheduledTime })
    });
  }
};
```

### Error Handling

```javascript
export default {
  async fetch(request, env, ctx) {
    try {
      const data = await env.MY_KV.get('key');

      if (!data) {
        return Response.json(
          { error: 'Not Found' },
          { status: 404 }
        );
      }

      return Response.json({ data });

    } catch (error) {
      console.error('Worker error:', error);

      return Response.json(
        { error: 'Internal Server Error' },
        { status: 500 }
      );
    }
  }
};
```

### Environment Variables & Secrets

```javascript
export default {
  async fetch(request, env, ctx) {
    // Access variables from wrangler.toml [vars]
    const apiUrl = env.API_URL;

    // Access secrets (wrangler secret put)
    const apiKey = env.API_KEY;

    const response = await fetch(`${apiUrl}/data`, {
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    });

    return response;
  }
};
```

---

## TypeScript Support

### Type Generation

```bash
# Generate types from wrangler.toml
wrangler types

# Output to custom file
wrangler types --outdir ./types
```

### worker-configuration.d.ts

```typescript
// Auto-generated by wrangler types
interface Env {
  MY_KV: KVNamespace;
  MY_BUCKET: R2Bucket;
  DB: D1Database;
  MY_DO: DurableObjectNamespace;
  API_KEY: string;
}
```

### Typed Handler

```typescript
export default {
  async fetch(
    request: Request,
    env: Env,
    ctx: ExecutionContext
  ): Promise<Response> {
    const value = await env.MY_KV.get('key');
    return new Response(value);
  }
};
```

---

## Official Templates

Cloudflare provides production-ready templates at [github.com/cloudflare/templates](https://github.com/cloudflare/templates).

### Using Templates

```bash
# Clone any template with C3
npm create cloudflare@latest my-app -- --template cloudflare/templates/<template-name>

# Examples
npm create cloudflare@latest my-db -- --template cloudflare/templates/d1-template
npm create cloudflare@latest my-chat -- --template cloudflare/templates/durable-chat-template
npm create cloudflare@latest my-ai -- --template cloudflare/templates/llm-chat-app-template
```

### Full-Stack & Framework Templates

| Template | Description |
|----------|-------------|
| `next-starter-template` | Next.js starter application |
| `remix-starter-template` | Remix framework starter |
| `astro-blog-starter-template` | Blog platform using Astro |
| `vite-react-template` | Vite with React configuration |
| `react-router-starter-template` | React Router basic setup |
| `react-router-hono-fullstack-template` | Full-stack React Router + Hono backend |
| `react-router-postgres-ssr-template` | SSR with PostgreSQL integration |
| `react-postgres-fullstack-template` | React frontend with PostgreSQL backend |

### Data & Storage Templates

| Template | Description |
|----------|-------------|
| `d1-template` | D1 SQL database starter with migrations |
| `d1-starter-sessions-api-template` | Session management using D1 |
| `to-do-list-kv-template` | Key-Value storage demonstration |
| `postgres-hyperdrive-template` | PostgreSQL via Hyperdrive connection pooling |
| `mysql-hyperdrive-template` | MySQL via Hyperdrive |
| `r2-explorer-template` | R2 object storage interface |

### Real-Time & Durable Objects Templates

| Template | Description |
|----------|-------------|
| `durable-chat-template` | Real-time chat with WebSockets and PartyKit |
| `hello-world-do-template` | Durable Objects introduction |
| `multiplayer-globe-template` | Real-time collaborative mapping |

### AI & LLM Templates

| Template | Description |
|----------|-------------|
| `llm-chat-app-template` | AI chatbot with Workers AI streaming |
| `text-to-image-template` | Image generation with Workers AI |

### Enterprise & SaaS Templates

| Template | Description |
|----------|-------------|
| `saas-admin-template` | SaaS dashboard with Astro, D1, and Workflows |
| `openauth-template` | Authentication implementation |
| `workers-for-platforms-template` | Platform-as-a-service architecture |

### Advanced Patterns

| Template | Description |
|----------|-------------|
| `workflows-starter-template` | Workflow orchestration with Durable Objects |
| `microfrontend-template` | Micro frontend architecture |
| `containers-template` | Containerized deployment |
| `chanfana-openapi-template` | OpenAPI documentation generation |
| `worker-publisher-template` | Publishing service pattern |

### Template Deep Dives

#### D1 Database Template

```javascript
// Query D1 database
export default {
  async fetch(request, env) {
    const { results } = await env.DB.prepare(
      "SELECT * FROM comments LIMIT 3"
    ).all();

    return Response.json(results);
  }
};
```

Setup steps:
1. `npm install`
2. `wrangler d1 create d1-template-database`
3. Update `wrangler.json` with database ID
4. `wrangler d1 migrations apply d1-template-database`
5. `wrangler deploy`

#### Durable Chat Template (Real-Time)

Uses PartyKit Server API with Durable Objects:

```javascript
// Chat room Durable Object
export class ChatRoom {
  connections = new Set();

  async onConnect(connection, ctx) {
    this.connections.add(connection);
    // Load chat history from SQL storage
    const history = await this.ctx.storage.sql.exec(
      "SELECT * FROM messages ORDER BY timestamp DESC LIMIT 50"
    );
    connection.send(JSON.stringify({ type: 'history', messages: history }));
  }

  async onMessage(message, connection) {
    // Store message
    await this.ctx.storage.sql.exec(
      "INSERT INTO messages (author, text, timestamp) VALUES (?, ?, ?)",
      [message.author, message.text, Date.now()]
    );
    // Broadcast to all connections
    for (const conn of this.connections) {
      conn.send(JSON.stringify(message));
    }
  }
}
```

#### LLM Chat App Template (Workers AI)

```javascript
// Streaming AI responses with SSE
export default {
  async fetch(request, env) {
    if (request.method === 'POST' && new URL(request.url).pathname === '/api/chat') {
      const { messages } = await request.json();

      const stream = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
        messages: [
          { role: 'system', content: 'You are a helpful assistant.' },
          ...messages
        ],
        stream: true
      });

      return new Response(stream, {
        headers: { 'Content-Type': 'text/event-stream' }
      });
    }
  }
};
```

Customization points:
- `MODEL_ID`: Swap between Workers AI models
- `SYSTEM_PROMPT`: Adjust AI behavior
- Optional AI Gateway for rate limiting and analytics

#### Workflows Starter Template

```javascript
// Define a workflow with steps
export class MyWorkflow extends WorkflowEntrypoint {
  async run(event, step) {
    // Step 1: Process input
    const processed = await step.do('process', async () => {
      return processData(event.payload);
    });

    // Step 2: Wait for time or event
    await step.sleep('wait', '1 hour');

    // Step 3: Continue processing
    const result = await step.do('finalize', async () => {
      return finalizeData(processed);
    });

    return result;
  }
}
```

Features:
- Time-based execution with delays
- Event-driven pauses
- Real-time status via WebSockets
- Durable state management

#### SaaS Admin Template

Stack: Astro + Shadcn UI + D1 + Workflows

```javascript
// API with token authentication
export default {
  async fetch(request, env) {
    const token = request.headers.get('Authorization')?.replace('Bearer ', '');

    if (token !== env.API_TOKEN) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Handle customer/subscription management
    const url = new URL(request.url);

    if (url.pathname === '/api/customers') {
      const customers = await env.DB.prepare(
        "SELECT * FROM customers"
      ).all();
      return Response.json(customers.results);
    }
  }
};
```

Features:
- Token-based authentication
- Customer management
- Subscription tracking
- Zod validation
- Background task processing with Workflows

---

## Rust SDK (workers-rs)

The `workers-rs` crate provides ergonomic Rust bindings for building Cloudflare Workers compiled to WebAssembly.

### Quick Start (Rust)

```bash
# Install prerequisites
rustup target add wasm32-unknown-unknown
cargo install cargo-generate

# Generate new Rust Worker project
cargo generate cloudflare/workers-rs

# Development
npx wrangler dev

# Deploy
npx wrangler deploy
```

### Project Structure

```
my-rust-worker/
├── Cargo.toml          # Rust dependencies
├── wrangler.toml       # Wrangler configuration
└── src/
    └── lib.rs          # Worker entry point
```

### Cargo.toml Configuration

```toml
[package]
name = "my-worker"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
worker = "0.4"
worker-macros = "0.4"
console_error_panic_hook = "0.1"

# Optional features
[dependencies.worker]
version = "0.4"
features = ["http", "d1", "queue"]

[profile.release]
opt-level = "s"      # Optimize for size
lto = true           # Link-time optimization
strip = true         # Strip symbols
codegen-units = 1    # Single codegen unit
```

### Basic Fetch Handler

```rust
use worker::*;

#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    Response::ok("Hello from Rust Worker!")
}
```

### Router Pattern

```rust
use worker::*;

#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    let router = Router::new();

    router
        .get("/", |_, _| Response::ok("Home"))
        .get_async("/users/:id", handle_user)
        .post_async("/users", create_user)
        .run(req, env)
        .await
}

async fn handle_user(req: Request, ctx: RouteContext<()>) -> Result<Response> {
    let id = ctx.param("id").unwrap();
    Response::ok(format!("User ID: {}", id))
}

async fn create_user(mut req: Request, ctx: RouteContext<()>) -> Result<Response> {
    let body: serde_json::Value = req.json().await?;
    Response::from_json(&body)
}
```

### Request/Response Handling

```rust
use worker::*;

#[event(fetch)]
async fn main(mut req: Request, env: Env, _ctx: Context) -> Result<Response> {
    // Request info
    let method = req.method();
    let path = req.path();
    let url = req.url()?;

    // Headers
    let headers = req.headers();
    let auth = headers.get("Authorization")?.unwrap_or_default();

    // Query parameters
    let query: HashMap<String, String> = url.query_pairs().into_owned().collect();

    // Body parsing
    let json_body: serde_json::Value = req.json().await?;
    let text_body = req.text().await?;
    let bytes = req.bytes().await?;

    // Build response
    let mut headers = Headers::new();
    headers.set("Content-Type", "application/json")?;
    headers.set("X-Custom-Header", "value")?;

    Ok(Response::ok("Hello")?
        .with_headers(headers)
        .with_status(200))
}
```

### JSON API

```rust
use serde::{Deserialize, Serialize};
use worker::*;

#[derive(Serialize, Deserialize)]
struct User {
    id: u32,
    name: String,
    email: String,
}

#[event(fetch)]
async fn main(mut req: Request, env: Env, _ctx: Context) -> Result<Response> {
    match req.method() {
        Method::Get => {
            let user = User {
                id: 1,
                name: "Alice".into(),
                email: "alice@example.com".into(),
            };
            Response::from_json(&user)
        }
        Method::Post => {
            let user: User = req.json().await?;
            Response::from_json(&user)
        }
        _ => Response::error("Method not allowed", 405),
    }
}
```

### KV Storage

```rust
use worker::*;

#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    let kv = env.kv("MY_KV")?;

    // Put value
    kv.put("key", "value")?.execute().await?;

    // Put with expiration (seconds)
    kv.put("temp_key", "value")?
        .expiration_ttl(3600)
        .execute()
        .await?;

    // Put JSON
    let data = serde_json::json!({"foo": "bar"});
    kv.put("json_key", data)?.execute().await?;

    // Get value
    let value = kv.get("key").text().await?;

    // Get as JSON
    let json_value: Option<serde_json::Value> = kv.get("json_key").json().await?;

    // List keys
    let list = kv.list().prefix("user:").execute().await?;
    for key in list.keys {
        console_log!("Key: {}", key.name);
    }

    // Delete
    kv.delete("key").await?;

    Response::ok("KV operations complete")
}
```

### Durable Objects

```rust
use worker::*;

// Define the Durable Object
#[durable_object]
pub struct Counter {
    state: State,
    env: Env,
}

#[durable_object]
impl DurableObject for Counter {
    fn new(state: State, env: Env) -> Self {
        Self { state, env }
    }

    async fn fetch(&mut self, req: Request) -> Result<Response> {
        // Get current count from storage
        let mut count: u64 = self.state.storage().get("count").await.unwrap_or(0);

        match req.method() {
            Method::Post => {
                count += 1;
                self.state.storage().put("count", count).await?;
            }
            Method::Delete => {
                count = 0;
                self.state.storage().put("count", count).await?;
            }
            _ => {}
        }

        Response::from_json(&serde_json::json!({ "count": count }))
    }
}

// Worker entry point
#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    let namespace = env.durable_object("COUNTER")?;
    let id = namespace.id_from_name("global")?;
    let stub = id.get_stub()?;

    stub.fetch_with_request(req).await
}
```

**wrangler.toml for Durable Objects:**

```toml
[durable_objects]
bindings = [
  { name = "COUNTER", class_name = "Counter" }
]

[[migrations]]
tag = "v1"
new_classes = ["Counter"]
```

### Durable Objects with SQLite Storage

```rust
#[durable_object]
impl DurableObject for MyObject {
    async fn fetch(&mut self, req: Request) -> Result<Response> {
        let sql = self.state.storage().sql();

        // Create table
        sql.exec(
            "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)",
            vec![],
        )?;

        // Insert
        sql.exec(
            "INSERT INTO items (name) VALUES (?)",
            vec![JsValue::from_str("item1")],
        )?;

        // Query
        let cursor = sql.exec("SELECT * FROM items", vec![])?;
        let rows: Vec<serde_json::Value> = cursor.to_array()?;

        Response::from_json(&rows)
    }
}
```

**wrangler.toml for SQLite in Durable Objects:**

```toml
[[migrations]]
tag = "v2"
new_sqlite_classes = ["MyObject"]
```

### D1 Database

Enable with `features = ["d1"]`:

```rust
use worker::*;

#[derive(Deserialize, Serialize)]
struct User {
    id: i32,
    name: String,
    email: String,
}

#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    let db = env.d1("DB")?;

    // Query all
    let stmt = db.prepare("SELECT * FROM users");
    let result = stmt.all().await?;
    let users: Vec<User> = result.results()?;

    // Query with parameters
    let stmt = db.prepare("SELECT * FROM users WHERE id = ?1");
    let user: Option<User> = stmt.bind(&[1.into()])?.first(None).await?;

    // Insert
    let stmt = db.prepare("INSERT INTO users (name, email) VALUES (?1, ?2)");
    stmt.bind(&["Alice".into(), "alice@example.com".into()])?
        .run()
        .await?;

    // Batch operations
    let results = db.batch(vec![
        db.prepare("INSERT INTO users (name) VALUES (?1)").bind(&["Bob".into()])?,
        db.prepare("INSERT INTO users (name) VALUES (?1)").bind(&["Charlie".into()])?,
    ]).await?;

    Response::from_json(&users)
}
```

### Queues

Enable with `features = ["queue"]`:

```rust
use worker::*;

#[derive(Serialize, Deserialize)]
struct Task {
    task_type: String,
    payload: String,
}

// Producer
#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    let queue = env.queue("MY_QUEUE")?;

    let task = Task {
        task_type: "email".into(),
        payload: "user@example.com".into(),
    };

    queue.send(task).await?;

    Response::ok("Task queued")
}

// Consumer
#[event(queue)]
async fn queue_handler(batch: MessageBatch<Task>, env: Env, _ctx: Context) -> Result<()> {
    for message in batch.messages()? {
        let task = message.body();
        console_log!("Processing: {:?}", task.task_type);

        // Process the task...

        message.ack();  // Acknowledge successful processing
        // or message.retry(); // Retry later
    }

    // Or acknowledge all at once
    // batch.ack_all();

    Ok(())
}
```

**wrangler.toml for Queues:**

```toml
[[queues.producers]]
queue = "my-queue"
binding = "MY_QUEUE"

[[queues.consumers]]
queue = "my-queue"
max_batch_size = 10
max_batch_timeout = 30
```

### R2 Object Storage

```rust
use worker::*;

#[event(fetch)]
async fn main(mut req: Request, env: Env, _ctx: Context) -> Result<Response> {
    let bucket = env.bucket("MY_BUCKET")?;
    let url = req.url()?;
    let key = url.path().trim_start_matches('/');

    match req.method() {
        Method::Put => {
            let body = req.bytes().await?;
            bucket.put(key, body)
                .http_metadata(HttpMetadata {
                    content_type: Some("application/octet-stream".into()),
                    ..Default::default()
                })
                .execute()
                .await?;
            Response::ok("Uploaded")
        }
        Method::Get => {
            match bucket.get(key).execute().await? {
                Some(object) => {
                    let body = object.body().unwrap().bytes().await?;
                    Ok(Response::from_bytes(body)?)
                }
                None => Response::error("Not found", 404),
            }
        }
        Method::Delete => {
            bucket.delete(key).await?;
            Response::ok("Deleted")
        }
        _ => Response::error("Method not allowed", 405),
    }
}
```

### Scheduled Events (Cron)

```rust
use worker::*;

#[event(scheduled)]
async fn scheduled(_event: ScheduledEvent, env: Env, _ctx: ScheduleContext) -> Result<()> {
    console_log!("Cron job executed!");

    let kv = env.kv("MY_KV")?;
    kv.put("last_run", chrono::Utc::now().to_rfc3339())?
        .execute()
        .await?;

    Ok(())
}

// Can combine with fetch handler
#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    Response::ok("Worker with scheduled event")
}
```

### HTTP Feature (Standard http Crate Compatibility)

Enable with `features = ["http"]` for compatibility with Axum, Hyper, etc:

```rust
use worker::*;

#[event(fetch)]
async fn main(req: HttpRequest, env: Env, _ctx: Context) -> Result<HttpResponse> {
    // req is now http::Request<worker::Body>
    let method = req.method();
    let uri = req.uri();
    let headers = req.headers();

    // Build standard http response
    let response = http::Response::builder()
        .status(200)
        .header("Content-Type", "application/json")
        .body(worker::Body::from(r#"{"status":"ok"}"#))?;

    Ok(response)
}
```

### Axum Integration

```rust
use axum::{routing::get, Router};
use tower_service::Service;
use worker::*;

fn router() -> Router {
    Router::new()
        .route("/", get(|| async { "Hello from Axum on Workers!" }))
        .route("/users/:id", get(get_user))
}

async fn get_user(axum::extract::Path(id): axum::extract::Path<String>) -> String {
    format!("User: {}", id)
}

#[event(fetch)]
async fn main(req: HttpRequest, env: Env, _ctx: Context) -> Result<HttpResponse> {
    Ok(router().call(req).await?)
}
```

### Environment Variables & Secrets

```rust
use worker::*;

#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    // Environment variables from wrangler.toml [vars]
    let api_url = env.var("API_URL")?.to_string();

    // Secrets (wrangler secret put)
    let api_key = env.secret("API_KEY")?.to_string();

    // Use in fetch
    let mut headers = Headers::new();
    headers.set("Authorization", &format!("Bearer {}", api_key))?;

    let mut init = RequestInit::new();
    init.with_headers(headers);

    let response = Fetch::Request(Request::new_with_init(&api_url, &init)?)
        .send()
        .await?;

    Ok(response)
}
```

### Error Handling

```rust
use worker::*;

#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    // Set up panic hook for better error messages
    console_error_panic_hook::set_once();

    match handle_request(req, env).await {
        Ok(response) => Ok(response),
        Err(e) => {
            console_error!("Error: {:?}", e);
            Response::error(format!("Internal error: {}", e), 500)
        }
    }
}

async fn handle_request(req: Request, env: Env) -> Result<Response> {
    let kv = env.kv("MY_KV")?;

    let value = kv.get("key").text().await?
        .ok_or_else(|| Error::from("Key not found"))?;

    Response::ok(value)
}
```

### Form Data & File Uploads

```rust
use worker::*;

#[event(fetch)]
async fn main(mut req: Request, env: Env, _ctx: Context) -> Result<Response> {
    let form = req.form_data().await?;

    for (name, entry) in form.entries() {
        match entry {
            FormEntry::Field(value) => {
                console_log!("Field {}: {}", name, value);
            }
            FormEntry::File(file) => {
                console_log!("File {}: {} bytes", file.name(), file.size());
                let bytes = file.bytes().await?;
                // Process file...
            }
        }
    }

    Response::ok("Form processed")
}
```

### WebSockets

```rust
use worker::*;

#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    let upgrade = req.headers().get("Upgrade")?;

    if upgrade.as_deref() == Some("websocket") {
        let pair = WebSocketPair::new()?;
        let server = pair.server;
        let client = pair.client;

        server.accept()?;

        wasm_bindgen_futures::spawn_local(async move {
            let mut event_stream = server.events().unwrap();

            while let Some(event) = event_stream.next().await {
                match event.unwrap() {
                    WebsocketEvent::Message(msg) => {
                        if let Some(text) = msg.text() {
                            server.send_with_str(&format!("Echo: {}", text)).unwrap();
                        }
                    }
                    WebsocketEvent::Close(_) => break,
                }
            }
        });

        Response::from_websocket(client)
    } else {
        Response::ok("WebSocket endpoint")
    }
}
```

### Testing Rust Workers with Miniflare

```javascript
// test.mjs
import { Miniflare } from "miniflare";

const mf = new Miniflare({
  scriptPath: "./build/worker/shim.mjs",
  modules: true,
  modulesRules: [
    { type: "CompiledWasm", include: ["**/*.wasm"] }
  ],
  kvNamespaces: ["MY_KV"],
  d1Databases: ["DB"],
});

// Run tests
const response = await mf.dispatchFetch("http://localhost/api/users");
console.log(await response.json());

await mf.dispose();
```

### Rust Worker Limitations

- **No threading**: Tokio/async_std not supported (no multi-threaded runtimes)
- **WASM target**: All dependencies must compile to `wasm32-unknown-unknown`
- **Bundle size limits**: Optimize with release profile settings
- **Edition 2021+**: Required for workers-rs v0.0.18+

### Debugging Tips

```rust
use worker::*;

#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    // Console logging
    console_log!("Request path: {}", req.path());
    console_error!("This is an error message");

    // Debug with serde_json
    console_log!("Request: {:?}", serde_json::to_string(&req.headers()));

    Response::ok("Debug complete")
}
```

---

## workerd Runtime

workerd is the open-source JavaScript/WebAssembly runtime that powers Cloudflare Workers. It can be self-hosted for local development, testing, or running Workers outside Cloudflare's network.

### What is workerd?

```
┌─────────────────────────────────────────────────────────┐
│                    workerd Runtime                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │     V8      │  │   WASM      │  │   Cap'n Proto   │ │
│  │  JavaScript │  │   Runtime   │  │  Configuration  │ │
│  │   Engine    │  │             │  │                 │ │
│  └──────┬──────┘  └──────┬──────┘  └────────┬────────┘ │
│         │                │                   │          │
│  ┌──────┴────────────────┴───────────────────┴────────┐ │
│  │              Service Mesh / Bindings                │ │
│  │    (KV, D1, R2, Queues, External Services, etc.)   │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Use Cases

| Use Case | Description |
|----------|-------------|
| **Application Server** | Self-host Workers in your own infrastructure |
| **Development Tool** | Local testing with production-identical runtime |
| **HTTP Proxy** | Programmable request interception and routing |
| **Edge Computing** | Deploy Workers to your own edge locations |

### Installation

```bash
# macOS (Homebrew)
brew install workerd

# From source (requires Bazel)
git clone https://github.com/cloudflare/workerd
cd workerd
bazel build //src/workerd/server:workerd

# Binary releases available for:
# - Linux x86-64, ARM64 (glibc 2.35+)
# - macOS x86-64, ARM64 (13.5+)
# - Windows x86-64
```

### Configuration (Cap'n Proto)

workerd uses Cap'n Proto text format for configuration:

```capnp
# workerd.capnp
using Workerd = import "/workerd/workerd.capnp";

const config :Workerd.Config = (
  services = [
    (name = "main", worker = .mainWorker),
  ],

  sockets = [
    (name = "http", address = "*:8080", http = (), service = "main"),
  ],
);

const mainWorker :Workerd.Worker = (
  modules = [
    (name = "worker", esModule = embed "worker.js"),
  ],
  compatibilityDate = "2024-01-01",
);
```

### Running workerd

```bash
# Start with configuration file
workerd serve config.capnp

# With socket activation (systemd)
workerd serve config.capnp --socket-fd http=3

# Validate configuration
workerd validate config.capnp

# Compile configuration (for deployment)
workerd compile config.capnp > compiled.bin
```

### Worker Configuration

```capnp
const myWorker :Workerd.Worker = (
  # ES Modules (recommended)
  modules = [
    (name = "main", esModule = embed "src/index.js"),
    (name = "utils", esModule = embed "src/utils.js"),
  ],

  # Or Service Worker syntax
  # serviceWorkerScript = embed "worker.js",

  # Compatibility settings
  compatibilityDate = "2024-01-01",
  compatibilityFlags = ["nodejs_compat"],

  # Bindings
  bindings = [
    (name = "MY_KV", kvNamespace = "kv-namespace-id"),
    (name = "MY_VAR", text = "hello"),
    (name = "MY_SECRET", text = "secret-value"),
    (name = "BACKEND", service = "backend-service"),
  ],

  # Durable Objects
  durableObjectNamespaces = [
    (className = "Counter", uniqueKey = "counter-ns"),
  ],
  durableObjectStorage = (localDisk = "do-storage"),
);
```

### Service Types

```capnp
const config :Workerd.Config = (
  services = [
    # Worker service
    (name = "api", worker = .apiWorker),

    # External HTTP backend
    (name = "backend", external = (
      address = "backend.example.com:443",
      http = (style = host),
      tls = (certificateAuthority = embed "ca.pem"),
    )),

    # Network access
    (name = "internet", network = (
      allow = ["public"],
      deny = ["10.0.0.0/8", "192.168.0.0/16"],
    )),

    # Disk directory
    (name = "static", disk = (
      path = "./public",
      writable = false,
    )),
  ],
);
```

### Socket Configuration

```capnp
const config :Workerd.Config = (
  sockets = [
    # HTTP socket
    (
      name = "http",
      address = "*:8080",
      http = (),
      service = "main",
    ),

    # HTTPS socket with TLS
    (
      name = "https",
      address = "*:8443",
      http = (),
      service = "main",
      tls = (
        certificateChain = embed "cert.pem",
        privateKey = embed "key.pem",
      ),
    ),

    # Unix socket
    (
      name = "unix",
      address = "unix:/var/run/workerd.sock",
      http = (),
      service = "main",
    ),
  ],
);
```

### Binding Types

```capnp
bindings = [
  # Text/string binding
  (name = "API_URL", text = "https://api.example.com"),

  # JSON binding
  (name = "CONFIG", json = "{\"debug\": true}"),

  # Binary data
  (name = "WASM_MODULE", wasmModule = embed "module.wasm"),

  # Cryptographic key
  (name = "SIGNING_KEY", cryptoKey = (
    raw = embed "key.bin",
    algorithm = (name = "HMAC", hash = "SHA-256"),
    usages = ["sign", "verify"],
  )),

  # Service binding (inter-worker communication)
  (name = "AUTH_SERVICE", service = "auth"),

  # KV namespace
  (name = "CACHE", kvNamespace = "cache-ns-id"),

  # R2 bucket
  (name = "STORAGE", r2Bucket = "my-bucket"),

  # D1 database
  (name = "DB", d1Database = "database-id"),

  # Queue
  (name = "TASK_QUEUE", queue = "tasks"),

  # Analytics Engine
  (name = "ANALYTICS", analyticsEngine = "my-dataset"),
],
```

### Durable Objects (Self-Hosted)

```capnp
const myWorker :Workerd.Worker = (
  modules = [
    (name = "main", esModule = embed "worker.js"),
  ],

  # Define DO classes
  durableObjectNamespaces = [
    (className = "Counter", uniqueKey = "counter"),
    (className = "ChatRoom", uniqueKey = "chat"),
  ],

  # Local disk storage for DO state
  durableObjectStorage = (
    localDisk = "./do-data",
  ),

  compatibilityDate = "2024-01-01",
);
```

**worker.js with Durable Object:**

```javascript
export class Counter {
  constructor(state, env) {
    this.state = state;
  }

  async fetch(request) {
    let count = (await this.state.storage.get("count")) || 0;
    count++;
    await this.state.storage.put("count", count);
    return new Response(JSON.stringify({ count }));
  }
}

export default {
  async fetch(request, env) {
    const id = env.COUNTER.idFromName("global");
    const stub = env.COUNTER.get(id);
    return stub.fetch(request);
  }
};
```

### Network Configuration

```capnp
# Allow outbound to public internet only
(name = "internet", network = (
  allow = ["public"],
)),

# Allow specific CIDRs
(name = "internal", network = (
  allow = ["10.0.0.0/8", "172.16.0.0/12"],
  deny = ["10.0.0.1/32"],  # Except this IP
)),

# Allow all (not recommended for production)
(name = "all", network = (
  allow = ["0.0.0.0/0", "::/0"],
)),
```

### TLS Configuration

```capnp
# Client TLS (for external services)
(name = "secure-backend", external = (
  address = "api.example.com:443",
  http = (),
  tls = (
    certificateAuthority = embed "ca-bundle.pem",
    minVersion = "TLSv1.3",
  ),
)),

# Server TLS (for sockets)
(
  name = "https",
  address = "*:443",
  http = (),
  service = "main",
  tls = (
    certificateChain = embed "fullchain.pem",
    privateKey = embed "privkey.pem",
    minVersion = "TLSv1.2",
    # OCSP stapling
    ocspResponse = embed "ocsp.der",
  ),
),
```

### Using with Wrangler (Local Dev)

```bash
# Set workerd path for wrangler dev
export MINIFLARE_WORKERD_PATH="/usr/local/bin/workerd"

# Run local development
wrangler dev

# Or explicitly use local mode
wrangler dev --local
```

### systemd Integration

```ini
# /etc/systemd/system/workerd.socket
[Unit]
Description=workerd HTTP Socket

[Socket]
ListenStream=80
ListenStream=443

[Install]
WantedBy=sockets.target
```

```ini
# /etc/systemd/system/workerd.service
[Unit]
Description=workerd Server
Requires=workerd.socket

[Service]
Type=simple
User=workerd
Group=workerd
ExecStart=/usr/local/bin/workerd serve /etc/workerd/config.capnp \
  --socket-fd http=3 --socket-fd https=4
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable workerd.socket
sudo systemctl start workerd.socket
```

### Docker Deployment

```dockerfile
FROM ghcr.io/cloudflare/workerd:latest

COPY config.capnp /etc/workerd/
COPY src/ /app/src/

EXPOSE 8080

CMD ["serve", "/etc/workerd/config.capnp"]
```

```yaml
# docker-compose.yml
services:
  workerd:
    image: ghcr.io/cloudflare/workerd:latest
    ports:
      - "8080:8080"
    volumes:
      - ./config.capnp:/etc/workerd/config.capnp:ro
      - ./src:/app/src:ro
      - ./do-data:/var/lib/workerd/do
    command: serve /etc/workerd/config.capnp
```

### Compatibility Dates

workerd maintains backward compatibility through date-based versioning:

```capnp
const myWorker :Workerd.Worker = (
  # Use APIs as they existed on this date
  compatibilityDate = "2024-01-01",

  # Enable specific compatibility flags
  compatibilityFlags = [
    "nodejs_compat",           # Node.js API compatibility
    "streams_enable_constructors",
    "transformstream_enable_standard_constructor",
  ],
);
```

### Runtime APIs

workerd implements web-standard APIs:

| Category | APIs |
|----------|------|
| **Fetch** | fetch(), Request, Response, Headers |
| **Streams** | ReadableStream, WritableStream, TransformStream |
| **Crypto** | crypto.subtle, crypto.getRandomValues() |
| **Encoding** | TextEncoder, TextDecoder, atob(), btoa() |
| **Timers** | setTimeout(), setInterval(), scheduler.wait() |
| **URL** | URL, URLSearchParams, URLPattern |
| **Cache** | caches.default, caches.open() |
| **WebSocket** | WebSocket, WebSocketPair |
| **Console** | console.log(), console.error(), etc. |

### Limitations (Self-Hosted)

- **Single-threaded**: One event loop per process; scale with multiple instances
- **Durable Objects**: Local disk only (no distributed storage)
- **No hardened sandbox**: Run in VM for untrusted code
- **Feature parity**: Some Cloudflare-specific features unavailable

### Security Considerations

```
⚠️  workerd provides logical isolation but is NOT a security sandbox.

For untrusted code:
- Run inside a VM (firecracker, gVisor, etc.)
- Use container isolation (Docker with seccomp)
- Network namespace isolation
- Resource limits (cgroups)
```

---

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **configuration.md** - Detailed wrangler.toml reference
- **getting_started.md** - Setup and first Worker guide
- **platform.md** - Platform capabilities and limits
- **runtime_apis.md** - Web APIs and Workers-specific APIs

Use `view` to read specific reference files when detailed information is needed.

---

## Resources

- [Workers Documentation](https://developers.cloudflare.com/workers/)
- [Wrangler CLI Reference](https://developers.cloudflare.com/workers/wrangler/commands/)
- [Wrangler Configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)
- [Workers Examples](https://developers.cloudflare.com/workers/examples/)
- [Workers SDK GitHub](https://github.com/cloudflare/workers-sdk)
- [Official Templates](https://github.com/cloudflare/templates)
- [Miniflare](https://miniflare.dev/)
- [Workers AI Models](https://developers.cloudflare.com/workers-ai/models/)
- [workers-rs (Rust SDK)](https://github.com/cloudflare/workers-rs)
- [Rust Workers Guide](https://developers.cloudflare.com/workers/languages/rust/)
- [workerd Runtime](https://github.com/cloudflare/workerd)
- [Runtime APIs Reference](https://developers.cloudflare.com/workers/runtime-apis/)

---

## Notes

- Enhanced from workers-sdk, templates, workers-rs, and workerd repositories
- Includes Wrangler CLI, Miniflare, C3 scaffolding, Rust SDK, workerd runtime, and official templates
- JavaScript/TypeScript examples use ES modules format (recommended)
- Rust examples use async/await with workers-rs macros
- workerd configuration uses Cap'n Proto text format
- wrangler.toml examples can also use wrangler.jsonc format
- Templates cover full-stack, databases, real-time, AI, and enterprise patterns
- Rust Workers compile to WASM and require `wasm32-unknown-unknown` target
- workerd can be self-hosted for local development or production deployment
