---
name: infra-iac-sst
description: SST (Ion) infrastructure-as-code — TypeScript-first serverless on AWS with Pulumi, resource linking, and live Lambda dev
---

# SST (Ion) Patterns

> **Quick Guide:** SST v3 (Ion) is TypeScript-first infrastructure-as-code for AWS, powered by Pulumi/Terraform (not CDK/CloudFormation). Define your entire app in `sst.config.ts` using high-level components (`sst.aws.Function`, `sst.aws.ApiGatewayV2`, `sst.aws.Bucket`, `sst.aws.Dynamo`, etc.). Use **resource linking** (`link: [bucket]` + `Resource.MyBucket.name`) for type-safe, permission-aware access between components. Use `sst dev` for live Lambda development with sub-10ms reloads. Use `$app.stage` for multi-environment isolation. Use `transform` to customize underlying Pulumi resources.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use resource linking (`link` + `Resource.*`) to connect components — NEVER hardcode ARNs, table names, or bucket names)**

**(You MUST use `$app.stage` for environment isolation — NEVER share resources across stages without explicit intent)**

**(You MUST use `sst dev` for local development — it provides live Lambda proxying with sub-10ms reloads against real AWS resources)**

**(You MUST use `sst secret set` for secrets — NEVER put secrets in `sst.config.ts`, `.env` files committed to git, or environment variables)**

**(You MUST use `transform` to customize underlying resources — NEVER reach for raw Pulumi resources when an SST component exists)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) — sst.config.ts structure, Function, resource linking, $app globals, secrets, multi-stage
- [API & Data](examples/api-data.md) — ApiGatewayV2, Dynamo, Bucket, Queue, Topic, Cron, authorization
- [Deployment & DevOps](examples/deployment.md) — sst deploy, CI/CD, removal policies, transforms, Vpc, Cluster, frontend frameworks
- [Quick Reference](reference.md) — CLI commands, component cheat sheet, global helpers, named constants

---

**Auto-detection:** SST, sst.config.ts, sst.aws.Function, sst.aws.ApiGatewayV2, sst.aws.Bucket, sst.aws.Dynamo, sst.aws.Queue, sst.aws.Topic, sst.aws.Cron, sst.aws.Nextjs, sst.aws.Remix, sst.aws.Astro, sst.aws.StaticSite, sst.aws.Vpc, sst.aws.Cluster, sst.aws.Postgres, sst.aws.Router, sst.Linkable, Resource from sst, sst dev, sst deploy, sst remove, sst secret, $app.stage, $transform, $concat, $interpolate, resource linking, live Lambda, Ion

**When to use:**

- Defining AWS infrastructure in TypeScript with high-level components
- Deploying serverless applications (Lambda, API Gateway, DynamoDB, S3, SQS, SNS)
- Deploying full-stack apps (Next.js, Remix, Astro, SvelteKit, SolidStart on AWS)
- Setting up live Lambda development with real AWS resources
- Managing multi-stage environments (dev, staging, production)
- Connecting infrastructure components with type-safe resource linking

**When NOT to use:**

- Multi-cloud infrastructure spanning many providers (SST is AWS-focused with limited Cloudflare support)
- Existing Terraform/Pulumi codebases where SST abstraction adds no value
- Projects that need container-only deployments without serverless components

**Key patterns covered:**

- `sst.config.ts` structure (`app()` + `run()` functions)
- Resource linking: `link` property + `Resource.*` SDK
- Live Lambda development with `sst dev`
- AWS components: Function, ApiGatewayV2, Dynamo, Bucket, Queue, Topic, Cron
- Frontend deployments: Nextjs, Remix, Astro, StaticSite
- Multi-stage isolation with `$app.stage`
- Transforms for customizing underlying Pulumi resources
- Secrets management with `sst secret`
- Custom linkables with `sst.Linkable` and `Linkable.wrap`
- Global helpers: `$app`, `$dev`, `$concat`, `$interpolate`, `$resolve`, `$transform`

---

<philosophy>

## Philosophy

SST v3 (Ion) replaces CDK/CloudFormation with Pulumi/Terraform for dramatically faster deployments and a simpler programming model. The core ideas:

1. **One config file** — Your entire app is defined in `sst.config.ts`. Infrastructure, frontends, and functions all declared together in TypeScript with loops, conditionals, and functions.
2. **Components over constructs** — High-level `sst.aws.*` components encapsulate best practices (IAM, logging, monitoring). Use `transform` to reach into underlying resources when defaults aren't enough.
3. **Resource linking** — The killer feature. `link: [bucket]` automatically grants IAM permissions and injects type-safe references. Access via `Resource.MyBucket.name` at runtime. No manual ARN passing or environment variable wiring.
4. **Stage-based isolation** — Every developer gets their own stage (`sst dev` creates a personal stack). `$app.stage` drives resource naming. Production uses `sst deploy --stage production`.
5. **Live dev against real AWS** — `sst dev` replaces Lambda functions with stubs that proxy to your local machine. Changes reload in under 10ms. No local emulation — your code runs against real DynamoDB, S3, SQS.

**When to use SST:**

- Serverless-first applications on AWS (Lambda, API Gateway, DynamoDB, S3, SQS, SNS)
- Full-stack apps deploying frontend frameworks (Next.js, Remix, Astro) to AWS
- Teams that want TypeScript infrastructure with minimal AWS boilerplate
- Projects needing fast local development loops against real cloud resources

**When NOT to use SST:**

- Multi-cloud infrastructure beyond AWS + Cloudflare (SST's multi-cloud support is limited)
- Container-only workloads with no serverless components (use raw Pulumi or Terraform)
- Existing large Terraform/Pulumi codebases where SST abstraction adds migration cost

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: sst.config.ts Structure

Every SST app has a single `sst.config.ts` with two functions: `app()` for metadata and `run()` for resources.

```typescript
/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "my-app",
      home: "aws",
      removal: input.stage === "production" ? "retain" : "remove",
      protect: input.stage === "production",
      providers: {
        aws: { region: "us-east-1" },
      },
    };
  },
  async run() {
    const bucket = new sst.aws.Bucket("Uploads");
    const api = new sst.aws.Function("Api", {
      handler: "src/api.handler",
      link: [bucket],
    });
    return { apiUrl: api.url };
  },
});
```

**Why good:** `app()` handles metadata and stage-specific policies, `run()` defines all resources, `removal: "retain"` protects production data, returned values become outputs in `.sst/outputs.json`

See [examples/core.md](examples/core.md) for full config with multi-stage, providers, and protect patterns.

---

### Pattern 2: Resource Linking

The defining SST feature. Link resources to grant permissions and type-safe access automatically.

```typescript
// In sst.config.ts
const table = new sst.aws.Dynamo("Notes", {
  fields: { userId: "string", noteId: "string" },
  primaryIndex: { hashKey: "userId", rangeKey: "noteId" },
});

new sst.aws.Function("Api", {
  handler: "src/api.handler",
  link: [table],
});
```

```typescript
// In src/api.ts — runtime code
import { Resource } from "sst";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({});
// Resource.Notes.name is the table name — type-safe, auto-generated
console.log(Resource.Notes.name);
```

**Why good:** No manual ARN passing, IAM permissions granted automatically, type-safe access via generated `sst-env.d.ts`, works across Functions, frontends, and containers

See [examples/core.md](examples/core.md) for linking patterns including custom linkables.

---

### Pattern 3: Live Lambda Development

`sst dev` proxies Lambda invocations to your local machine for sub-10ms reload cycles.

```bash
# Start live dev — deploys infra, proxies Lambda to local machine
sst dev

# Opens multiplexer: deploys resources, starts frontends, tunnels VPC
```

```typescript
// Detect dev mode in handler code
const isLocal = process.env.SST_DEV === "true";
```

**Key behavior:** Functions are replaced with stubs that forward events via AppSync to your local machine. Your local code runs as Node.js Workers. Changes reload instantly — no redeploy needed.

**Gotcha:** Killing `sst dev` leaves stubs deployed. Subsequent Lambda invocations will timeout until you run `sst dev` again or `sst deploy` to replace stubs with real code.

See [examples/core.md](examples/core.md) for dev workflow and debugging setup.

---

### Pattern 4: AWS Components

SST provides high-level components for common AWS services. Each handles IAM, logging, and configuration automatically.

| Component              | AWS Service         | Use Case              |
| ---------------------- | ------------------- | --------------------- |
| `sst.aws.Function`     | Lambda              | Serverless functions  |
| `sst.aws.ApiGatewayV2` | API Gateway v2      | HTTP APIs with routes |
| `sst.aws.Dynamo`       | DynamoDB            | NoSQL database        |
| `sst.aws.Bucket`       | S3                  | Object storage        |
| `sst.aws.Queue`        | SQS                 | Message queues        |
| `sst.aws.Topic`        | SNS                 | Pub/sub messaging     |
| `sst.aws.Cron`         | EventBridge         | Scheduled tasks       |
| `sst.aws.Vpc`          | VPC                 | Network isolation     |
| `sst.aws.Cluster`      | ECS                 | Container workloads   |
| `sst.aws.Postgres`     | RDS Postgres        | Relational database   |
| `sst.aws.Nextjs`       | Lambda + CloudFront | Next.js deployment    |
| `sst.aws.Remix`        | Lambda + CloudFront | Remix deployment      |
| `sst.aws.Astro`        | Lambda + CloudFront | Astro deployment      |
| `sst.aws.StaticSite`   | S3 + CloudFront     | Static site hosting   |
| `sst.aws.Router`       | CloudFront          | URL routing           |

See [examples/api-data.md](examples/api-data.md) for API, database, storage, queue, and cron patterns.

---

### Pattern 5: Secrets Management

Secrets are encrypted and stored in S3, injected into function bundles at deploy time.

```bash
# Set a secret (prompts for value)
sst secret set DATABASE_URL

# Set a secret with value inline
sst secret set STRIPE_KEY sk_live_xxx

# Load secrets from a file
sst secret load .env.production

# List all secrets
sst secret list
```

```typescript
// Access secrets via resource linking
import { Resource } from "sst";
const stripeKey = Resource.StripeKey.value;
```

**Gotcha:** Secrets are per-stage. Set them for each stage separately. Use `--fallback` to set a default across all stages.

See [examples/core.md](examples/core.md) for secrets with Linkable pattern.

---

### Pattern 6: Transforms

Customize underlying Pulumi resources when SST defaults aren't enough.

```typescript
// Per-component transform
new sst.aws.Function("Api", {
  handler: "src/api.handler",
  transform: {
    function: (args) => {
      args.tracingConfig = { mode: "Active" };
    },
  },
});

// Global transform — applies to ALL components of a type
$transform(sst.aws.Function, (args) => {
  args.environment ??= {};
  args.environment.variables ??= {};
  args.environment.variables.STAGE = $app.stage;
});
```

**Why good:** Transforms let you customize any underlying resource property without abandoning SST's abstractions. Global transforms set defaults across all components.

See [examples/deployment.md](examples/deployment.md) for transform patterns.

---

### Pattern 7: Multi-Stage Environments

Every stage is a fully isolated deployment. Use `$app.stage` for conditional configuration.

```typescript
async run() {
  const isProd = $app.stage === "production";

  const table = new sst.aws.Dynamo("Notes", {
    fields: { userId: "string", noteId: "string" },
    primaryIndex: { hashKey: "userId", rangeKey: "noteId" },
    deletionProtection: isProd,
  });
}
```

```bash
# Personal dev stage (default)
sst dev

# Deploy to staging
sst deploy --stage staging

# Deploy to production
sst deploy --stage production
```

See [examples/deployment.md](examples/deployment.md) for multi-stage patterns with removal policies.

</patterns>

---

<decision_framework>

## Decision Framework

### Choosing an SST Component

```
What are you building?
  |
  +-- HTTP API
  |     +-- Simple routes with Lambda handlers --> sst.aws.ApiGatewayV2
  |     +-- Need WebSocket support --> sst.aws.ApiGatewayWebSocket
  |     +-- URL routing / CDN --> sst.aws.Router
  |
  +-- Data storage
  |     +-- Key-value / document data --> sst.aws.Dynamo
  |     +-- Relational data with SQL --> sst.aws.Postgres
  |     +-- File/blob storage --> sst.aws.Bucket
  |
  +-- Async processing
  |     +-- Point-to-point messaging --> sst.aws.Queue (SQS)
  |     +-- Fan-out to multiple subscribers --> sst.aws.Topic (SNS)
  |     +-- Scheduled tasks --> sst.aws.Cron
  |
  +-- Compute
  |     +-- Serverless function --> sst.aws.Function
  |     +-- Container workload --> sst.aws.Cluster + sst.aws.Service
  |     +-- Long-running background job --> sst.aws.Function (up to 15min)
  |
  +-- Full-stack frontend
        +-- Next.js --> sst.aws.Nextjs
        +-- Remix --> sst.aws.Remix
        +-- Astro --> sst.aws.Astro
        +-- SvelteKit --> sst.aws.SvelteKit
        +-- SolidStart --> sst.aws.SolidStart
        +-- Static HTML/JS --> sst.aws.StaticSite
```

### When to Use Transforms vs Raw Pulumi

```
Need to set a property on an SST component?
  |
  +-- Property exists on the SST component args --> Use the SST property directly
  |
  +-- Property exists only on the underlying AWS resource --> Use transform
  |
  +-- Need to set a default across ALL instances of a component --> Use $transform()
  |
  +-- No SST component exists for this AWS service --> Use raw Pulumi resource
        +-- Need to link it? --> Use sst.Linkable.wrap() or new sst.Linkable()
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Hardcoding ARNs, table names, or bucket names instead of using resource linking (`link` + `Resource.*`) — defeats SST's type-safe wiring and breaks across stages
- Sharing resource names across stages without `$app.stage` prefix — causes resource conflicts and accidental cross-stage access
- Putting secrets in `sst.config.ts` or committed `.env` files instead of using `sst secret set` — secrets leak to version control
- Using `sst dev` for shared environments (staging, production) — stubs proxy to a single developer's machine, breaking for everyone else
- Creating raw Pulumi resources when an equivalent `sst.aws.*` component exists — loses SST's linking, permissions, and defaults

**Medium Priority Issues:**

- Not setting `removal: "retain"` and `protect: true` for production stages — accidental `sst remove` deletes all data
- Missing `/// <reference path="./.sst/platform/config.d.ts" />` at top of `sst.config.ts` — loses type checking for `$app`, `$transform`, etc.
- Using `.env` files for secrets instead of `sst secret` — `.env` files aren't encrypted and must be managed manually per stage
- Not running `sst deploy` after finishing `sst dev` session — stubs remain deployed and Lambda invocations timeout

**Common Mistakes:**

- Forgetting that `sst dev` stubs persist after you stop the process — always redeploy or re-run `sst dev`
- Using `$app.stage` in runtime code — it's only available in `sst.config.ts`, use `Resource.*` or env vars for runtime stage awareness
- Trying to use SST resource linking in client-side frontend code — links are server-side only (SSR functions, API routes)
- Expecting `sst dev` to emulate AWS locally — it doesn't; it proxies to real AWS resources in your account

**Gotchas & Edge Cases:**

- Pulumi Outputs cannot be used directly in string templates — use `$concat()` or `$interpolate` instead of template literals
- `sst dev` multiplexer starts frontends automatically — you don't need to run `next dev` or `vite dev` separately
- FIFO queues require `.fifo` suffix in names — SST handles this automatically but be aware when referencing externally
- `.env` and `.env.<stage>` files are loaded automatically — `.env` takes precedence over stage-specific files
- Frontend framework links (Next.js, Remix) only work server-side — client components cannot access `Resource.*`
- Layers specified in Function config are not applied during `sst dev` — local execution skips layers
- The `removal` setting in `app()` controls what happens when you run `sst remove` — `"remove"` deletes resources, `"retain"` keeps them, `"retain-all"` keeps everything including logs

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use resource linking (`link` + `Resource.*`) to connect components — NEVER hardcode ARNs, table names, or bucket names)**

**(You MUST use `$app.stage` for environment isolation — NEVER share resources across stages without explicit intent)**

**(You MUST use `sst dev` for local development — it provides live Lambda proxying with sub-10ms reloads against real AWS resources)**

**(You MUST use `sst secret set` for secrets — NEVER put secrets in `sst.config.ts`, `.env` files committed to git, or environment variables)**

**(You MUST use `transform` to customize underlying resources — NEVER reach for raw Pulumi resources when an SST component exists)**

**Failure to follow these rules will cause cross-stage resource conflicts, leaked secrets, broken type safety, and unnecessary infrastructure complexity.**

</critical_reminders>
