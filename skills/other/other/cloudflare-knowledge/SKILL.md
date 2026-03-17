---
name: cloudflare-knowledge
description: Comprehensive Cloudflare platform knowledge covering Workers, storage (R2/D1/KV/Durable Objects/Queues), AI Workers, Hyperdrive, Zero Trust, MCP servers, Workflows, and all platform features
---

# Cloudflare Knowledge Skill

Comprehensive Cloudflare platform knowledge covering all features, pricing, and best practices. Activate this skill when users need detailed information about Cloudflare's edge computing platform.

## Activation Triggers

Activate this skill when users ask about:
- Cloudflare Workers development
- Wrangler CLI commands and configuration
- Storage services (R2, D1, KV, Durable Objects, Queues)
- Hyperdrive database connection pooling
- AI Workers (TTS, STT, LLM, image models)
- Zero Trust (tunnels, WARP, access policies)
- MCP server development and integration
- Workflows and durable execution
- Vectorize vector database
- Pages and static site deployment
- CI/CD with GitHub Actions or Workers Builds
- Observability (logs, traces, OpenTelemetry)
- Load balancing and health checks
- Cron triggers and scheduled tasks
- Cost optimization and pricing

---

## Platform Overview

Cloudflare is a global edge computing platform with 300+ data centers providing:

- **Workers**: Serverless JavaScript/TypeScript/Python/WASM at the edge
- **Pages**: Static site and full-stack app hosting
- **R2**: S3-compatible object storage with zero egress fees
- **D1**: Serverless SQLite database
- **KV**: Eventually consistent key-value store
- **Durable Objects**: Stateful coordination with WebSocket support
- **Queues**: Async message processing
- **Hyperdrive**: Database connection pooling
- **AI Workers**: Inference at the edge (LLM, TTS, STT, image)
- **Zero Trust**: Identity-based security platform
- **Vectorize**: Vector database for RAG applications
- **Workflows**: Durable multi-step execution

---

## Wrangler CLI Reference

### Project Setup

```bash
# Create new project
npm create cloudflare@latest my-worker

# Initialize in existing directory
npx wrangler init

# Login
npx wrangler login
npx wrangler whoami
```

### Development

```bash
# Local development
npx wrangler dev
npx wrangler dev --remote    # Use remote bindings
npx wrangler dev --local     # Fully local

# Test cron trigger locally
curl "http://localhost:8787/__scheduled?cron=*+*+*+*+*"
```

### Deployment

```bash
# Deploy to production
npx wrangler deploy

# Deploy to environment
npx wrangler deploy --env staging

# List versions
npx wrangler versions list

# Rollback
npx wrangler rollback
```

### D1 Database

```bash
# Create database
npx wrangler d1 create my-database

# Execute SQL
npx wrangler d1 execute my-database --local --file=schema.sql
npx wrangler d1 execute my-database --remote --command="SELECT * FROM users"

# Interactive shell
npx wrangler d1 execute my-database --local --command=".tables"

# Export
npx wrangler d1 export my-database --remote --output=backup.sql
```

### R2 Buckets

```bash
# Create bucket
npx wrangler r2 bucket create my-bucket

# List buckets
npx wrangler r2 bucket list

# Upload/download
npx wrangler r2 object put my-bucket/file.txt --file=local.txt
npx wrangler r2 object get my-bucket/file.txt --file=download.txt

# Delete
npx wrangler r2 object delete my-bucket/file.txt
```

### KV Namespaces

```bash
# Create namespace
npx wrangler kv namespace create MY_KV
npx wrangler kv namespace create MY_KV --preview  # Preview namespace

# List namespaces
npx wrangler kv namespace list

# Key operations
npx wrangler kv key put --binding MY_KV key "value"
npx wrangler kv key get --binding MY_KV key
npx wrangler kv key list --binding MY_KV
npx wrangler kv key delete --binding MY_KV key

# Bulk upload
npx wrangler kv bulk put --binding MY_KV data.json
```

### Secrets

```bash
# Set secret
npx wrangler secret put API_KEY
# (prompts for value)

# List secrets
npx wrangler secret list

# Delete secret
npx wrangler secret delete API_KEY
```

### Queues

```bash
# Create queue
npx wrangler queues create my-queue

# List queues
npx wrangler queues list
```

### Hyperdrive

```bash
# Create Hyperdrive config
npx wrangler hyperdrive create my-hyperdrive --connection-string="postgres://..."

# List configs
npx wrangler hyperdrive list

# Update
npx wrangler hyperdrive update my-hyperdrive --connection-string="postgres://..."
```

---

## Wrangler Configuration (wrangler.jsonc)

### Complete Configuration Reference

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-01-01",
  "compatibility_flags": ["nodejs_compat"],

  // Account settings
  "account_id": "<optional-account-id>",

  // Build settings
  "minify": true,
  "node_compat": true,

  // Environment variables
  "vars": {
    "API_URL": "https://api.example.com"
  },

  // KV Namespaces
  "kv_namespaces": [
    {
      "binding": "MY_KV",
      "id": "<namespace-id>",
      "preview_id": "<preview-namespace-id>"
    }
  ],

  // R2 Buckets
  "r2_buckets": [
    {
      "binding": "MY_BUCKET",
      "bucket_name": "my-bucket",
      "preview_bucket_name": "my-bucket-preview",
      "jurisdiction": "eu"
    }
  ],

  // D1 Databases
  "d1_databases": [
    {
      "binding": "DB",
      "database_id": "<database-id>",
      "database_name": "my-database"
    }
  ],

  // Durable Objects
  "durable_objects": {
    "bindings": [
      {
        "name": "MY_DO",
        "class_name": "MyDurableObject"
      }
    ]
  },
  "migrations": [
    {
      "tag": "v1",
      "new_classes": ["MyDurableObject"]
    },
    {
      "tag": "v2",
      "new_sqlite_classes": ["MyDurableObjectWithSQL"]
    }
  ],

  // Queues
  "queues": {
    "producers": [
      {
        "binding": "MY_QUEUE",
        "queue": "my-queue"
      }
    ],
    "consumers": [
      {
        "queue": "my-queue",
        "max_batch_size": 10,
        "max_batch_timeout": 30,
        "max_retries": 3,
        "dead_letter_queue": "my-dlq"
      }
    ]
  },

  // Hyperdrive
  "hyperdrive": [
    {
      "binding": "MY_DB_POOL",
      "id": "<hyperdrive-config-id>"
    }
  ],

  // Workers AI
  "ai": {
    "binding": "AI"
  },

  // Vectorize
  "vectorize": [
    {
      "binding": "MY_VECTORS",
      "index_name": "my-index"
    }
  ],

  // Browser Rendering
  "browser": {
    "binding": "BROWSER"
  },

  // Service Bindings (Worker-to-Worker)
  "services": [
    {
      "binding": "OTHER_WORKER",
      "service": "other-worker-name"
    }
  ],

  // Cron Triggers
  "triggers": {
    "crons": ["0 * * * *", "0 6 * * *"]
  },

  // Routes
  "routes": [
    {
      "pattern": "example.com/*",
      "zone_name": "example.com"
    }
  ],

  // Observability
  "observability": {
    "logs": {
      "enabled": true,
      "invocation_logs": true,
      "head_sampling_rate": 1
    }
  },

  // Environments
  "env": {
    "staging": {
      "name": "my-worker-staging",
      "vars": {
        "API_URL": "https://staging-api.example.com"
      }
    },
    "production": {
      "name": "my-worker-production",
      "routes": [
        {
          "pattern": "api.example.com/*",
          "zone_name": "example.com"
        }
      ]
    }
  }
}
```

---

## Storage Services Deep Dive

### KV (Key-Value Store)

**Characteristics:**
- Eventually consistent (up to 60s propagation)
- Max value size: 25 MiB
- Max key size: 512 bytes
- Best for: Configuration, session data, caching
- Free tier: 100,000 reads/day, 1,000 writes/day

```typescript
interface Env {
  MY_KV: KVNamespace;
}

// Write operations
await env.MY_KV.put("key", "string value");
await env.MY_KV.put("key", JSON.stringify(object));
await env.MY_KV.put("key", arrayBuffer);

// With TTL (seconds)
await env.MY_KV.put("session", data, { expirationTtl: 3600 });

// With absolute expiration
await env.MY_KV.put("session", data, { expiration: Math.floor(Date.now() / 1000) + 3600 });

// With metadata
await env.MY_KV.put("user:123", userData, {
  metadata: { type: "user", version: 2 }
});

// Read operations
const value = await env.MY_KV.get("key");  // Returns string or null
const json = await env.MY_KV.get("key", "json");  // Parses JSON
const buffer = await env.MY_KV.get("key", "arrayBuffer");
const stream = await env.MY_KV.get("key", "stream");

// With metadata
const { value, metadata } = await env.MY_KV.getWithMetadata("key");

// List keys
const list = await env.MY_KV.list();
const filtered = await env.MY_KV.list({ prefix: "user:", limit: 100 });
// Pagination: use list.cursor for next page

// Delete
await env.MY_KV.delete("key");
```

### R2 (Object Storage)

**Characteristics:**
- S3-compatible API
- Zero egress fees
- Max object size: 5 TB
- Single upload max: 5 GB (use multipart for larger)
- Best for: Media files, backups, data lakes, large files

```typescript
interface Env {
  MY_BUCKET: R2Bucket;
}

// Put object
await env.MY_BUCKET.put("path/to/file.json", JSON.stringify(data), {
  httpMetadata: {
    contentType: "application/json",
    cacheControl: "max-age=3600",
  },
  customMetadata: {
    uploadedBy: "worker",
    version: "1.0",
  },
});

// Put with checksums
await env.MY_BUCKET.put("file.bin", data, {
  md5: expectedMd5,  // Validates on upload
  sha256: expectedSha256,
});

// Get object
const object = await env.MY_BUCKET.get("path/to/file.json");
if (object) {
  const text = await object.text();
  const json = await object.json();
  const buffer = await object.arrayBuffer();
  const blob = await object.blob();
  const stream = object.body;  // ReadableStream

  // Metadata
  console.log(object.key, object.size, object.etag);
  console.log(object.httpMetadata.contentType);
  console.log(object.customMetadata.uploadedBy);
}

// Head (metadata only)
const head = await env.MY_BUCKET.head("path/to/file.json");

// List objects
const list = await env.MY_BUCKET.list();
const filtered = await env.MY_BUCKET.list({
  prefix: "uploads/",
  delimiter: "/",
  limit: 1000,
});

// Delete
await env.MY_BUCKET.delete("path/to/file.json");
await env.MY_BUCKET.delete(["file1.json", "file2.json"]);  // Batch delete

// Multipart upload (for files > 5GB)
const upload = await env.MY_BUCKET.createMultipartUpload("large-file.zip");
const part1 = await upload.uploadPart(1, chunk1);
const part2 = await upload.uploadPart(2, chunk2);
await upload.complete([part1, part2]);

// Or abort
await upload.abort();
```

### D1 (SQLite Database)

**Characteristics:**
- Serverless SQLite
- Strong consistency
- Max database size: 10 GB (GA)
- Best for: Relational data, complex queries, ACID transactions

```typescript
interface Env {
  DB: D1Database;
}

// Prepared statements (recommended)
const stmt = env.DB.prepare("SELECT * FROM users WHERE id = ?");
const { results } = await stmt.bind(userId).all();
const user = await stmt.bind(userId).first();
const value = await stmt.bind(userId).first("name");  // Single column

// Insert/Update
const { meta } = await env.DB.prepare(
  "INSERT INTO users (name, email) VALUES (?, ?)"
).bind(name, email).run();
console.log(meta.last_row_id, meta.changes);

// Batch operations (single transaction)
const results = await env.DB.batch([
  env.DB.prepare("INSERT INTO users (name) VALUES (?)").bind("Alice"),
  env.DB.prepare("INSERT INTO users (name) VALUES (?)").bind("Bob"),
  env.DB.prepare("UPDATE counters SET value = value + 1 WHERE name = 'users'"),
]);

// Raw execution
await env.DB.exec("PRAGMA table_info(users)");

// Transaction pattern (using batch)
await env.DB.batch([
  env.DB.prepare("UPDATE accounts SET balance = balance - ? WHERE id = ?").bind(100, fromId),
  env.DB.prepare("UPDATE accounts SET balance = balance + ? WHERE id = ?").bind(100, toId),
]);
```

**D1 Best Practices:**
```sql
-- Create indexes for WHERE clause columns
CREATE INDEX idx_users_email ON users(email);

-- Use EXPLAIN QUERY PLAN to verify index usage
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'test@example.com';

-- Batch large migrations
DELETE FROM logs WHERE created_at < '2024-01-01' LIMIT 1000;

-- Run after schema changes
PRAGMA optimize;
```

### Durable Objects

**Characteristics:**
- Single-threaded, globally unique instances
- Built-in SQLite storage
- WebSocket support with Hibernation
- Best for: Real-time coordination, chat, games, counters

```typescript
// Durable Object class
export class Counter {
  state: DurableObjectState;
  value: number = 0;

  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
    // Restore state from storage
    this.state.blockConcurrencyWhile(async () => {
      this.value = (await this.state.storage.get("value")) || 0;
    });
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    switch (url.pathname) {
      case "/increment":
        this.value++;
        await this.state.storage.put("value", this.value);
        return Response.json({ value: this.value });

      case "/value":
        return Response.json({ value: this.value });

      default:
        return new Response("Not found", { status: 404 });
    }
  }
}

// Worker that uses the Durable Object
export default {
  async fetch(request: Request, env: Env) {
    const id = env.COUNTER.idFromName("global");
    const stub = env.COUNTER.get(id);
    return stub.fetch(request);
  },
};
```

**WebSocket Hibernation:**
```typescript
export class ChatRoom {
  state: DurableObjectState;

  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
  }

  async fetch(request: Request): Promise<Response> {
    if (request.headers.get("Upgrade") === "websocket") {
      const pair = new WebSocketPair();
      const [client, server] = Object.values(pair);

      // Use Hibernation API
      this.state.acceptWebSocket(server);

      return new Response(null, { status: 101, webSocket: client });
    }
    return new Response("Expected WebSocket", { status: 400 });
  }

  // Called when hibernated DO receives WebSocket message
  async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer) {
    // Broadcast to all connected clients
    for (const client of this.state.getWebSockets()) {
      if (client !== ws && client.readyState === WebSocket.READY_STATE_OPEN) {
        client.send(message);
      }
    }
  }

  async webSocketClose(ws: WebSocket, code: number, reason: string) {
    // Handle disconnect
  }

  async webSocketError(ws: WebSocket, error: unknown) {
    // Handle error
    ws.close(1011, "Internal error");
  }
}
```

### Queues

**Characteristics:**
- Async message processing
- At-least-once delivery
- Automatic retries with dead letter queues
- Best for: Decoupling, background jobs, event processing

```typescript
// Producer
interface Env {
  MY_QUEUE: Queue;
}

export default {
  async fetch(request: Request, env: Env) {
    // Send single message
    await env.MY_QUEUE.send({ type: "email", to: "user@example.com" });

    // Send with options
    await env.MY_QUEUE.send(
      { type: "process", id: 123 },
      { contentType: "json" }
    );

    // Batch send
    await env.MY_QUEUE.sendBatch([
      { body: { id: 1 } },
      { body: { id: 2 } },
      { body: { id: 3 } },
    ]);

    return new Response("Queued");
  },
};

// Consumer
interface QueueMessage {
  type: string;
  id?: number;
  to?: string;
}

export default {
  async queue(batch: MessageBatch<QueueMessage>, env: Env): Promise<void> {
    for (const message of batch.messages) {
      try {
        console.log(`Processing: ${JSON.stringify(message.body)}`);
        await processMessage(message.body);
        message.ack();  // Mark as processed
      } catch (e) {
        console.error(`Failed: ${e}`);
        message.retry();  // Will retry (up to max_retries)
      }
    }
  },
};
```

---

## AI Workers Reference

### Available Models (2025-2026)

**Text Generation:**
| Model | Context | Best For |
|-------|---------|----------|
| @cf/meta/llama-3.3-70b-instruct-fp8-fast | 128K | General, reasoning |
| @cf/mistral/mistral-7b-instruct-v0.2 | 32K | Fast, efficient |
| @cf/qwen/qwen2.5-72b-instruct | 128K | Multilingual |
| @cf/deepseek/deepseek-r1-distill-llama-70b | 64K | Complex reasoning |

**Text-to-Speech (TTS):**
| Model | Languages | Notes |
|-------|-----------|-------|
| @deepgram/aura-2-en | English | Best quality, context-aware |
| @deepgram/aura-1 | English | Fast, good quality |
| @cf/myshell-ai/melotts | en, fr, es, zh, ja, ko | Multi-lingual |

**Speech-to-Text (STT):**
| Model | Languages | Notes |
|-------|-----------|-------|
| @cf/openai/whisper-large-v3-turbo | 100+ | Fast, accurate |
| @cf/openai/whisper | 100+ | Original Whisper |

**Image Generation:**
| Model | Resolution | Notes |
|-------|------------|-------|
| @cf/black-forest-labs/flux-1-schnell | Up to 1024x1024 | Fast |
| @cf/stabilityai/stable-diffusion-xl-base-1.0 | Up to 1024x1024 | Detailed |

**Vision/Captioning:**
| Model | Capabilities |
|-------|--------------|
| @cf/meta/llama-3.2-11b-vision-instruct | Image understanding, captioning |
| @cf/llava-hf/llava-1.5-7b-hf | Visual Q&A |

**Embeddings:**
| Model | Dimensions | Notes |
|-------|------------|-------|
| @cf/baai/bge-large-en-v1.5 | 1024 | Best quality |
| @cf/baai/bge-small-en-v1.5 | 384 | Faster |

### Usage Examples

```typescript
interface Env {
  AI: Ai;
}

// Text generation
const response = await env.AI.run("@cf/meta/llama-3.3-70b-instruct-fp8-fast", {
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "What is Cloudflare?" },
  ],
  max_tokens: 512,
  temperature: 0.7,
});

// Streaming
const stream = await env.AI.run("@cf/meta/llama-3.3-70b-instruct-fp8-fast", {
  messages: [...],
  stream: true,
});
return new Response(stream, {
  headers: { "Content-Type": "text/event-stream" },
});

// Text-to-Speech
const audio = await env.AI.run("@deepgram/aura-2-en", {
  text: "Hello, this is a test.",
});
return new Response(audio, {
  headers: { "Content-Type": "audio/wav" },
});

// Speech-to-Text
const transcript = await env.AI.run("@cf/openai/whisper-large-v3-turbo", {
  audio: audioArrayBuffer,
});
// Returns { text: "...", segments: [...] }

// Image generation
const image = await env.AI.run("@cf/black-forest-labs/flux-1-schnell", {
  prompt: "A futuristic cityscape at sunset",
  num_steps: 4,
});
return new Response(image, {
  headers: { "Content-Type": "image/png" },
});

// Embeddings
const embeddings = await env.AI.run("@cf/baai/bge-large-en-v1.5", {
  text: ["Hello world", "Cloudflare Workers"],
});
// Returns { data: [{ embedding: [...] }, { embedding: [...] }] }

// Image captioning
const caption = await env.AI.run("@cf/meta/llama-3.2-11b-vision-instruct", {
  image: imageArrayBuffer,
  prompt: "Describe this image in detail.",
});
```

---

## Hyperdrive Deep Dive

Hyperdrive accelerates database connections by maintaining connection pools close to your database.

### Setup

```bash
# Create Hyperdrive config
npx wrangler hyperdrive create my-db \
  --connection-string="postgres://user:pass@host:5432/database"

# Add to wrangler.jsonc
```

### Usage

```typescript
import { Client } from "pg";

interface Env {
  MY_DB: Hyperdrive;
}

export default {
  async fetch(request: Request, env: Env) {
    // Connect using Hyperdrive connection string
    const client = new Client({
      connectionString: env.MY_DB.connectionString,
    });

    await client.connect();
    const result = await client.query("SELECT * FROM users WHERE id = $1", [1]);

    // No need to call client.end() - Hyperdrive manages pooling
    return Response.json(result.rows);
  },
};
```

### When to Use Hyperdrive

**Use Hyperdrive when:**
- Connecting to remote PostgreSQL/MySQL databases
- High-latency database connections (different regions)
- Frequent identical read queries (caching)
- Many concurrent database connections needed

**Don't use Hyperdrive when:**
- Using D1 (already edge-native)
- Local development (use direct connection)
- Need prepared statements across requests (transaction mode limitation)
- Using Durable Objects storage

### Performance Benefits

Without Hyperdrive:
```
Worker -> TCP handshake (1 RTT)
       -> TLS negotiation (3 RTTs)
       -> DB authentication (3 RTTs)
       -> Query (1 RTT)
Total: 8 round-trips before first query
```

With Hyperdrive:
```
Worker -> Hyperdrive pool (cached connection)
       -> Query (1 RTT to pool, reuses DB connection)
Total: 1 round-trip to query
```

---

## Zero Trust Reference

### Cloudflare Tunnel

Expose internal services securely without opening firewall ports.

**Installation:**
```bash
# macOS
brew install cloudflared

# Windows
winget install Cloudflare.cloudflared

# Linux
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
sudo chmod +x cloudflared && sudo mv cloudflared /usr/local/bin/
```

**Setup:**
```bash
# Login
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create my-tunnel

# Create config file (~/.cloudflared/config.yml)
cat << EOF > ~/.cloudflared/config.yml
tunnel: <tunnel-id>
credentials-file: $HOME/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: app.example.com
    service: http://localhost:3000
  - hostname: api.example.com
    service: http://localhost:8080
  - service: http_status:404
EOF

# Add DNS
cloudflared tunnel route dns my-tunnel app.example.com

# Run
cloudflared tunnel run my-tunnel
```

**Run as Service:**
```bash
# Linux
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared

# macOS
sudo cloudflared service install
sudo launchctl load /Library/LaunchDaemons/com.cloudflare.cloudflared.plist
```

### Access Policies

Configure in Cloudflare dashboard (Zero Trust > Access > Applications):

```yaml
Application:
  name: Internal App
  type: Self-hosted
  domain: app.example.com

Policy:
  name: Allow Company
  action: Allow
  include:
    - email_domain: company.com
  require:
    - country: US
```

### WARP Client

- Device client for Zero Trust enrollment
- Routes traffic through Cloudflare network
- Enables identity-based access policies
- Split tunneling for selective routing

---

## MCP Servers Reference

### Building MCP Server on Workers

```typescript
import { McpServer } from "@cloudflare/mcp-server";

interface Env {
  DB: D1Database;
}

const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0",
});

// Define tools
server.addTool({
  name: "query_database",
  description: "Query the D1 database",
  parameters: {
    type: "object",
    properties: {
      query: { type: "string", description: "SQL query to execute" },
    },
    required: ["query"],
  },
  handler: async ({ query }, { env }) => {
    const result = await env.DB.prepare(query).all();
    return {
      content: [{ type: "text", text: JSON.stringify(result.results) }],
    };
  },
});

// Define resources
server.addResource({
  uri: "db://tables",
  name: "Database Tables",
  description: "List of all tables",
  handler: async ({ env }) => {
    const tables = await env.DB.prepare(
      "SELECT name FROM sqlite_master WHERE type='table'"
    ).all();
    return {
      contents: [{ uri: "db://tables", text: JSON.stringify(tables.results) }],
    };
  },
});

export default {
  async fetch(request: Request, env: Env) {
    return server.handleRequest(request, env);
  },
};
```

### MCP Transport Types

1. **Streamable HTTP** (Recommended, March 2025+)
   - Single HTTP endpoint
   - Bidirectional messaging
   - Standard for remote MCP

2. **stdio** (Local only)
   - Standard input/output
   - For local MCP connections

3. **SSE** (Deprecated)
   - Use Streamable HTTP instead

### Cloudflare's Managed MCP Servers

Available at `https://mcp.cloudflare.com/`:
- Workers management
- R2 bucket operations
- D1 database queries
- DNS management
- Analytics access

**Connect from Claude/Cursor:**
```json
{
  "mcpServers": {
    "cloudflare": {
      "url": "https://mcp.cloudflare.com/sse",
      "transport": "sse"
    }
  }
}
```

---

## CI/CD Reference

### GitHub Actions

```yaml
name: Deploy Worker

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Deploy to Cloudflare
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

### Workers Builds (Native Git Integration)

1. Connect GitHub/GitLab in Cloudflare dashboard
2. Select repository and branch
3. Configure build command (optional)
4. Automatic deployment on push
5. Preview URLs for pull requests

---

## Pricing Reference (2025-2026)

### Workers

| Plan | Price | Requests | CPU Time |
|------|-------|----------|----------|
| Free | $0 | 100K/day | 10ms/invocation |
| Paid | $5/mo | 10M included | 30s/invocation |
| Usage | +$0.30/M requests | - | $0.02/M ms |

### Storage

| Service | Free Tier | Paid |
|---------|-----------|------|
| KV | 100K reads, 1K writes/day | $0.50/M reads, $5/M writes |
| R2 | 10GB storage, 10M Class A ops | $0.015/GB, $4.50/M Class A |
| D1 | 5M rows read, 100K writes/day | $0.001/M rows, $1/M writes |
| Durable Objects | 1M requests | $0.15/M requests |
| Queues | 1M messages | $0.40/M messages |

### AI Workers

- Pay per inference
- Varies by model (check dashboard for current pricing)
- Free tier includes limited inferences

---

## Best Practices

### Performance

1. **Use edge caching**: Cache API responses with `caches.default`
2. **Minimize cold starts**: Keep Workers small, use dynamic imports
3. **Use Service Bindings**: Zero-cost Worker-to-Worker calls
4. **Batch operations**: Combine KV/R2/D1 operations
5. **Use Hyperdrive**: For remote database connections

### Security

1. **Use secrets**: Never hardcode credentials
2. **Validate input**: Sanitize all user input
3. **Use HTTPS**: Always use secure connections
4. **Implement rate limiting**: Protect against abuse
5. **Use Zero Trust**: For internal service access

### Cost Optimization

1. **Use Static Assets**: Free, unlimited static file serving
2. **Sample logs**: Use `head_sampling_rate` for high-traffic Workers
3. **Use KV for caching**: Reduce D1/external API calls
4. **Batch queue messages**: Reduce per-message overhead
5. **Use GPU-appropriate models**: Don't overprovision AI

---

## Quick Reference

| Task | Command/Code |
|------|--------------|
| New project | `npm create cloudflare@latest` |
| Local dev | `npx wrangler dev` |
| Deploy | `npx wrangler deploy` |
| Create D1 | `npx wrangler d1 create name` |
| Create KV | `npx wrangler kv namespace create NAME` |
| Create R2 | `npx wrangler r2 bucket create name` |
| Set secret | `npx wrangler secret put NAME` |
| Create queue | `npx wrangler queues create name` |
| Create tunnel | `cloudflared tunnel create name` |
