---
name: inngest-setup
description: Set up Inngest in a TypeScript project. Install the SDK, create a client, configure environment variables, serve endpoints or connect as a worker, and run the local dev server.
---

# Inngest Setup

This skill sets up Inngest in a TypeScript project from scratch, covering installation, client configuration, connection modes, and local development.

> **These skills are focused on TypeScript.** For Python or Go, refer to the [Inngest documentation](https://www.inngest.com/llms.txt) for language-specific guidance. Core concepts apply across all languages.

## Prerequisites

- Node.js 18+ (Node.js 22.4+ r ecommended for WebSocket support)
- TypeScript project
- Package manager (npm, yarn, pnpm, or bun)

## Step 1: Install the Inngest SDK

Install the `inngest` npm package in your project:

```bash
npm install inngest
# or
yarn add inngest
# or
pnpm add inngest
# or
bun add inngest
```

## Step 2: Create an Inngest Client

Create a shared client file that you'll import throughout your codebase:

```typescript
// src/inngest/client.ts
import { Inngest } from "inngest";

export const inngest = new Inngest({
  id: "my-app" // Unique identifier for your application (hyphenated slug)
});
```

### Key Configuration Options

- **`id`** (required): Unique identifier for your app. Use a hyphenated slug like `"my-app"` or `"user-service"`
- **`eventKey`**: Event key for sending events (prefer `INNGEST_EVENT_KEY` env var)
- **`env`**: Environment name for Branch Environments
- **`isDev`**: Force Dev mode (`true`) or Cloud mode (`false`)
- **`logger`**: Custom logger instance (e.g. winston, pino) — enables `logger` in function context
- **`middleware`**: Array of middleware (see **inngest-middleware** skill)
- **`schemas`**: Use `EventSchemas` for typed events (see **inngest-events** skill)

### Typed Events with EventSchemas

```typescript
import { Inngest, EventSchemas } from "inngest";

type Events = {
  "user/signup.completed": {
    data: {
      userId: string;
      email: string;
      plan: "free" | "pro";
    };
  };
  "order/placed": {
    data: {
      orderId: string;
      amount: number;
    };
  };
};

export const inngest = new Inngest({
  id: "my-app",
  schemas: new EventSchemas().fromRecord<Events>()
});

// Now event data is fully typed in functions:
// inngest.createFunction({ id: "handle-signup" }, { event: "user/signup.completed" },
//   async ({ event }) => { event.data.userId /* typed as string */ }
// );
```

### Environment Variables Setup

Set these environment variables in your `.env` file or deployment environment:

```env
# Required for production
INNGEST_EVENT_KEY=your-event-key-here
INNGEST_SIGNING_KEY=your-signing-key-here

# Force dev mode during local development
INNGEST_DEV=1

# Optional - custom dev server URL (default: http://localhost:8288)
INNGEST_BASE_URL=http://localhost:8288
```

**⚠️ Common Gotcha**: Never hardcode keys in your source code. Always use environment variables for `INNGEST_EVENT_KEY` and `INNGEST_SIGNING_KEY`.

## Step 3: Choose Your Connection Mode

Inngest supports two connection modes:

### Mode A: Serve Endpoint (HTTP)

Best for serverless platforms (Vercel, Lambda, etc.) and existing APIs.

### Mode B: Connect (WebSocket)

Best for container runtimes (Kubernetes, Docker) and long-running processes.

## Step 4A: Serving an Endpoint (HTTP Mode)

Create an API endpoint that exposes your functions to Inngest:

```typescript
// For Next.js App Router: src/app/api/inngest/route.ts
import { serve } from "inngest/next";
import { inngest } from "../../../inngest/client";
import { myFunction } from "../../../inngest/functions";

export const { GET, POST, PUT } = serve({
  client: inngest,
  functions: [myFunction]
});
```

```typescript
// For Next.js Pages Router: pages/api/inngest.ts
import { serve } from "inngest/next";
import { inngest } from "../../inngest/client";
import { myFunction } from "../../inngest/functions";

export default serve({
  client: inngest,
  functions: [myFunction]
});
```

```typescript
// For Express.js
import express from "express";
import { serve } from "inngest/express";
import { inngest } from "./inngest/client";
import { myFunction } from "./inngest/functions";

const app = express();
app.use(express.json({ limit: "10mb" })); // Required for Inngest, increase limit for larger function state

app.use(
  "/api/inngest",
  serve({
    client: inngest,
    functions: [myFunction]
  })
);
```

**🔧 Framework-Specific Notes**:

- **Express**: Must use `express.json({ limit: "10mb" })` middleware to support larger function state.
- **Fastify**: Use `fastifyPlugin` from `inngest/fastify`
- **Cloudflare Workers**: Use `inngest/cloudflare`
- **AWS Lambda**: Use `inngest/lambda`
- For all other frameworks, check the `serve` reference here: https://www.inngest.com/docs-markdown/learn/serving-inngest-functions

**⚠️ Common Gotcha**: Always use `/api/inngest` as your endpoint path. This enables automatic discovery. If you must use a different path, you'll need to configure discovery manually with the `-u` flag.

## Step 4B: Connect as Worker (WebSocket Mode)

For long-running applications that maintain persistent connections:

```typescript
// src/worker.ts
// Note: inngest/connect requires inngest SDK v3.27+
import { connect } from "inngest/connect";
import { inngest } from "./inngest/client";
import { myFunction } from "./inngest/functions";

(async () => {
  const connection = await connect({
    apps: [{ client: inngest, functions: [myFunction] }],
    instanceId: process.env.HOSTNAME, // Unique worker identifier
    maxWorkerConcurrency: 10 // Max concurrent steps
  });

  console.log("Worker connected:", connection.state);

  // Graceful shutdown handling
  await connection.closed;
  console.log("Worker shut down");
})();
```

**Requirements for Connect Mode**:

- Node.js 22.4+ (or Deno 1.4+, Bun 1.1+) for WebSocket support
- Long-running server environment (not serverless)
- `INNGEST_SIGNING_KEY` and `INNGEST_EVENT_KEY` for production
- Set the `appVersion` parameter on the `Inngest` client for production to support rolling deploys

## Step 5: Organizing with Apps

As your system grows, organize functions into logical apps:

```typescript
// User service
const userService = new Inngest({ id: "user-service" });

// Payment service
const paymentService = new Inngest({ id: "payment-service" });

// Email service
const emailService = new Inngest({ id: "email-service" });
```

Each app gets its own section in the Inngest dashboard and can be deployed independently. Use descriptive, hyphenated IDs that match your service architecture.

**⚠️ Common Gotcha**: Changing an app's `id` creates a new app in Inngest. Keep IDs consistent across deployments.

## Step 6: Local Development with inngest-cli

Start the Inngest Dev Server for local development:

```bash
# Auto-discover your app on common ports/endpoints
npx --ignore-scripts=false inngest-cli@latest dev

# Specify your app's URL manually
npx --ignore-scripts=false inngest-cli@latest dev -u http://localhost:3000/api/inngest

# Custom port for dev server
npx --ignore-scripts=false inngest-cli@latest dev -p 9999

# Disable auto-discovery
npx --ignore-scripts=false inngest-cli@latest dev --no-discovery -u http://localhost:3000/api/inngest

# Multiple apps
npx --ignore-scripts=false inngest-cli@latest dev -u http://localhost:3000/api/inngest -u http://localhost:4000/api/inngest
```

The dev server will be available at `http://localhost:8288` by default.

### Configuration File (Optional)

Create `inngest.json` for complex setups:

```json
{
  "sdk-url": [
    "http://localhost:3000/api/inngest",
    "http://localhost:4000/api/inngest"
  ],
  "port": 8289,
  "no-discovery": true
}
```

## Environment-Specific Setup

### Local Development

```env
INNGEST_DEV=1
# No keys required in dev mode
```

### Production

```env
INNGEST_EVENT_KEY=evt_your_production_event_key
INNGEST_SIGNING_KEY=signkey_your_production_signing_key
```

### Custom Dev Server Port

```env
INNGEST_DEV=1
INNGEST_BASE_URL=http://localhost:9999
```

If your app runs on a non-standard port (not 3000), make sure the dev server can reach it by specifying the URL with `-u` flag.

## Common Issues & Solutions

**Port Conflicts**: If port 8288 is in use, specify a different port: `-p 9999`

**Auto-discovery Not Working**: Use manual URL specification: `-u http://localhost:YOUR_PORT/api/inngest`

**Signature Verification Errors**: Ensure `INNGEST_SIGNING_KEY` is set correctly in production

**WebSocket Connection Issues**: Verify Node.js version 22.4+ for connect mode

**Docker Development**: Use `host.docker.internal` for app URLs when running dev server in Docker

## Next Steps

1. Create your first Inngest function with `inngest.createFunction()`
2. Test functions using the dev server's "Invoke" button
3. Send events with `inngest.send()` to trigger functions
4. Deploy to production with proper environment variables
5. See **inngest-middleware** for adding logging, error tracking, and other cross-cutting concerns
6. Monitor functions in the Inngest dashboard

The dev server automatically reloads when you change functions, making development fast and iterative.
