---
name: infra-platform-aws-sdk
description: AWS SDK v3 for TypeScript — modular clients, command pattern, S3, DynamoDB, SQS, Lambda, SNS, Secrets Manager
---

# AWS SDK v3 Patterns

> **Quick Guide:** AWS SDK v3 for JavaScript/TypeScript uses modular packages (`@aws-sdk/client-*`) with a command pattern: create a client, instantiate a command, call `client.send(command)`. Import only the services you need for tree-shaking. Use `DynamoDBDocumentClient` for native JS types. Use `getSignedUrl` from `@aws-sdk/s3-request-presigner` for presigned URLs. Handle errors with `instanceof` specific exception classes. Use built-in paginators (`paginate*`) with `for await...of`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use AWS SDK v3 modular packages (`@aws-sdk/client-*`) — NEVER the monolithic `aws-sdk` v2 package)**

**(You MUST use the command pattern: `client.send(new XxxCommand({...}))` — NEVER call methods directly on the client)**

**(You MUST use `DynamoDBDocumentClient` from `@aws-sdk/lib-dynamodb` for DynamoDB — it auto-marshalls native JS types)**

**(You MUST handle errors with `instanceof` specific exception classes — NEVER catch generic `Error` and check `.code`)**

**(You MUST use built-in paginators (`paginate*` functions) for paginated APIs — NEVER manually track continuation tokens)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) — Client setup, S3 operations, DynamoDB basics, credential providers, error handling, pagination
- [Messaging](examples/messaging.md) — SQS send/receive/delete, SNS publish, FIFO queues, dead-letter patterns
- [Advanced](examples/advanced.md) — Lambda invocation, Secrets Manager, presigned URLs, middleware, streaming
- [Quick Reference](reference.md) — Package cheat sheet, import patterns, error handling decision tree, credential provider chain

---

**Auto-detection:** AWS SDK, @aws-sdk/client, S3Client, DynamoDBClient, DynamoDBDocumentClient, SQSClient, LambdaClient, SNSClient, SecretsManagerClient, PutObjectCommand, GetObjectCommand, GetCommand, PutCommand, QueryCommand, SendMessageCommand, InvokeCommand, GetSecretValueCommand, getSignedUrl, s3-request-presigner, credential-providers, fromEnv, fromIni, paginateListObjectsV2, aws-sdk-client-mock

**When to use:**

- Interacting with any AWS service from TypeScript/JavaScript
- S3 file operations (upload, download, presigned URLs, listings)
- DynamoDB CRUD operations and queries
- SQS message sending, receiving, and queue management
- Lambda function invocation from other services
- SNS topic publishing and notifications
- Secrets Manager secret retrieval
- Custom middleware for request/response modification

**When NOT to use:**

- Infrastructure provisioning (use an IaC tool)
- AWS console-only operations with no SDK equivalent
- Simple CLI-only tasks better served by the AWS CLI directly

**Key patterns covered:**

- Modular client setup with typed configuration
- Command pattern (`client.send(new Command({...}))`)
- S3: upload, download, delete, list, presigned URLs, streaming
- DynamoDB: `DynamoDBDocumentClient` with `Get`, `Put`, `Query`, `Update`, `Delete`
- SQS: send, receive, delete messages, long polling, FIFO
- SNS: publish to topics, message attributes
- Lambda: synchronous and asynchronous invocation
- Secrets Manager: secret retrieval with caching
- Credential provider chain and explicit providers
- Error handling with `instanceof` exception classes and `$metadata`
- Pagination with async iterators
- Middleware stack customization
- Retry configuration

---

<philosophy>

## Philosophy

AWS SDK v3 is a ground-up rewrite of the v2 SDK for modern JavaScript/TypeScript. The core design principles:

1. **Modular packages** — Each service is a separate npm package (`@aws-sdk/client-s3`, `@aws-sdk/client-dynamodb`). Import only what you use. This reduces bundle size by up to 90% compared to the monolithic v2 `aws-sdk` package.

2. **Command pattern** — Every API call is a Command object sent through a Client. This enables middleware, type safety, and testability. The client handles serialization, signing, retries, and deserialization.

3. **First-class TypeScript** — Every command input and output is fully typed. Use the types to avoid runtime errors.

4. **Middleware stack** — Customize request/response handling at various stages (serialize, build, finalize, deserialize) without monkey-patching.

5. **Built-in pagination** — Paginator functions return async iterators, eliminating manual token tracking.

**When to use AWS SDK v3:**

- Any server-side or serverless TypeScript/JavaScript that interacts with AWS services
- Frontend applications that need direct AWS access (with appropriate auth)
- Lambda functions (SDK v3 is included in Node.js 18+ Lambda runtimes)

**When NOT to use:**

- Infrastructure provisioning and management (use an IaC tool)
- One-off tasks better served by the AWS CLI
- Languages other than JavaScript/TypeScript

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup and Command Pattern

Every AWS service follows the same pattern: import the client and command, create a client instance, send the command.

```typescript
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const s3 = new S3Client({ region: "us-east-1" });
await s3.send(
  new PutObjectCommand({
    Bucket: "my-bucket",
    Key: "data.json",
    Body: JSON.stringify({ hello: "world" }),
    ContentType: "application/json",
  }),
);
```

**Why good:** modular import keeps bundle small, command pattern enables middleware and type safety, region is explicit

Create clients once and reuse them — they manage connection pooling internally. In Lambda, create clients outside the handler for connection reuse across invocations.

See [examples/core.md](examples/core.md) for client reuse patterns and configuration options.

---

### Pattern 2: S3 Operations

S3 is the most commonly used service. Key operations: `PutObject`, `GetObject`, `DeleteObject`, `ListObjectsV2`, and presigned URLs via `@aws-sdk/s3-request-presigner`.

```typescript
import { GetObjectCommand, NoSuchKey } from "@aws-sdk/client-s3";

const response = await s3.send(
  new GetObjectCommand({
    Bucket: "my-bucket",
    Key: "data.json",
  }),
);
const body = await response.Body?.transformToString();
```

For presigned URLs, use the separate `@aws-sdk/s3-request-presigner` package:

```typescript
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const PRESIGN_EXPIRY_SECONDS = 3_600;
const url = await getSignedUrl(
  s3,
  new GetObjectCommand({
    Bucket: "my-bucket",
    Key: "file.pdf",
  }),
  { expiresIn: PRESIGN_EXPIRY_SECONDS },
);
```

See [examples/core.md](examples/core.md) for upload, download, delete, list, and streaming patterns.

---

### Pattern 3: DynamoDB with Document Client

Use `DynamoDBDocumentClient` from `@aws-sdk/lib-dynamodb` — it automatically marshalls/unmarshalls between native JS types and DynamoDB's `AttributeValue` format.

```typescript
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  GetCommand,
  PutCommand,
} from "@aws-sdk/lib-dynamodb";

const ddbDocClient = DynamoDBDocumentClient.from(new DynamoDBClient({}));

const { Item } = await ddbDocClient.send(
  new GetCommand({
    TableName: "users",
    Key: { userId: "abc-123" },
  }),
);
```

**Why good:** no manual `marshall()`/`unmarshall()` calls, native JS objects in and out, full type safety

**Gotcha:** Import commands from `@aws-sdk/lib-dynamodb` (not `@aws-sdk/client-dynamodb`) when using the document client — the lib-dynamodb commands accept native JS types.

See [examples/core.md](examples/core.md) for Put, Query, Update, Delete, and batch operations.

---

### Pattern 4: Error Handling

AWS SDK v3 errors extend service-specific base classes (e.g., `S3ServiceException`). Use `instanceof` for typed error handling.

```typescript
import {
  GetObjectCommand,
  NoSuchKey,
  S3ServiceException,
} from "@aws-sdk/client-s3";

try {
  await s3.send(new GetObjectCommand({ Bucket: "b", Key: "k" }));
} catch (error) {
  if (error instanceof NoSuchKey) {
    // Typed: error.name === "NoSuchKey", error.$metadata.httpStatusCode === 404
    return null;
  }
  if (error instanceof S3ServiceException) {
    // Any S3 service error — check error.$metadata.httpStatusCode
    throw error;
  }
  throw error; // Non-AWS error (network, etc.)
}
```

**Why good:** `instanceof` gives TypeScript type narrowing, exception classes are exported from the client package, `$metadata` provides HTTP status and request ID for debugging

See [examples/core.md](examples/core.md) for the full error handling decision tree and retry patterns.

---

### Pattern 5: Pagination with Async Iterators

Use built-in paginator functions for any paginated API. They return async iterators that handle continuation tokens automatically.

```typescript
import { paginateListObjectsV2 } from "@aws-sdk/client-s3";

for await (const page of paginateListObjectsV2(
  { client: s3 },
  { Bucket: "my-bucket" },
)) {
  // page.Contents is an array of objects for this page
}
```

**Why good:** no manual token tracking, clean `for await...of` loop, handles all edge cases (empty pages, token format)

See [examples/core.md](examples/core.md) for full S3 list, DynamoDB pagination, and good/bad comparison with manual token tracking.

---

### Pattern 6: SQS Messaging

SQS uses `SendMessageCommand`, `ReceiveMessageCommand`, and `DeleteMessageCommand`. Always delete messages after processing.

```typescript
import { SQSClient, SendMessageCommand } from "@aws-sdk/client-sqs";

const sqs = new SQSClient({});
await sqs.send(
  new SendMessageCommand({
    QueueUrl: QUEUE_URL,
    MessageBody: JSON.stringify({ orderId: "order-123" }),
  }),
);
```

See [examples/messaging.md](examples/messaging.md) for receive/delete, long polling, FIFO queues, and dead-letter patterns.

---

### Pattern 7: SNS Publishing

SNS publishes messages to topics. Subscribers receive messages on their configured endpoints.

```typescript
import { SNSClient, PublishCommand } from "@aws-sdk/client-sns";

const sns = new SNSClient({});
await sns.send(
  new PublishCommand({
    TopicArn: TOPIC_ARN,
    Message: JSON.stringify({ event: "order.created", orderId: "order-123" }),
    MessageAttributes: {
      eventType: { DataType: "String", StringValue: "order.created" },
    },
  }),
);
```

See [examples/messaging.md](examples/messaging.md) for topic management and message filtering.

---

### Pattern 8: Lambda Invocation and Secrets Manager

Invoke Lambda functions synchronously or asynchronously. Retrieve secrets from Secrets Manager with caching.

```typescript
import { LambdaClient, InvokeCommand } from "@aws-sdk/client-lambda";

const lambda = new LambdaClient({});
const response = await lambda.send(
  new InvokeCommand({
    FunctionName: "process-order",
    InvocationType: "RequestResponse", // synchronous
    Payload: JSON.stringify({ orderId: "order-123" }),
  }),
);
const result = JSON.parse(new TextDecoder().decode(response.Payload));
```

See [examples/advanced.md](examples/advanced.md) for async invocation, Secrets Manager retrieval, and caching patterns.

</patterns>

---

<decision_framework>

## Decision Framework

### Choosing the Right DynamoDB Client

```
Are you working with DynamoDB?
  |
  +-- Need native JS objects (recommended) --> DynamoDBDocumentClient from @aws-sdk/lib-dynamodb
  |     +-- Import Get/Put/Query/Update/Delete Commands from @aws-sdk/lib-dynamodb
  |
  +-- Need raw AttributeValue format --> DynamoDBClient from @aws-sdk/client-dynamodb
        +-- Import commands from @aws-sdk/client-dynamodb
        +-- Manually marshall/unmarshall with @aws-sdk/util-dynamodb
```

### Choosing Between Synchronous and Async Lambda Invocation

```
Do you need the Lambda response immediately?
  |
  +-- YES --> InvocationType: "RequestResponse" (synchronous, waits for result)
  |
  +-- NO  --> InvocationType: "Event" (async, returns immediately, 3 retries)
```

### Credential Provider Selection

```
Where is this code running?
  |
  +-- Lambda / ECS / EC2 --> Default chain (auto-detects IAM role) — no config needed
  |
  +-- Local development --> fromIni() (reads ~/.aws/credentials) or fromEnv()
  |
  +-- CI/CD pipeline --> fromEnv() with AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
  |
  +-- Cross-account access --> fromTemporaryCredentials() with STS AssumeRole
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using the monolithic `aws-sdk` v2 package — it ships the entire SDK (~70 MB). Use modular `@aws-sdk/client-*` packages.
- Calling methods directly on the client (v2 style: `s3.getObject()`) — use the command pattern: `s3.send(new GetObjectCommand({...}))`.
- Using raw `DynamoDBClient` commands with manual `marshall()`/`unmarshall()` — use `DynamoDBDocumentClient` from `@aws-sdk/lib-dynamodb`.
- Catching errors with `.code` string comparison (v2 style) — use `instanceof` with typed exception classes.
- Manually tracking pagination tokens in a while loop — use built-in `paginate*` functions with `for await...of`.
- Hardcoding AWS credentials in source code — use the credential provider chain or environment variables.

**Medium Priority Issues:**

- Creating a new client instance per request — create clients once and reuse them (they manage connection pooling).
- Not setting a region explicitly — defaults vary by environment and cause confusing errors.
- Mixing `@aws-sdk/client-dynamodb` and `@aws-sdk/lib-dynamodb` command imports — pick one approach per codebase.
- Missing `ContentType` on S3 `PutObject` — S3 defaults to `application/octet-stream`, breaking browser downloads.
- Not buffering the S3 `GetObject` response body — `response.Body` is a stream; call `.transformToString()` or `.transformToByteArray()`.

**Gotchas and Edge Cases:**

- `GetObject` response body is a `ReadableStream` (not a string) — you must consume it with `.transformToString()`, `.transformToByteArray()`, or pipe it to a writable stream.
- `DynamoDBDocumentClient` commands come from `@aws-sdk/lib-dynamodb`, NOT `@aws-sdk/client-dynamodb` — importing from the wrong package gives you raw `AttributeValue` types.
- Presigned URLs require the separate `@aws-sdk/s3-request-presigner` package — it is NOT included in `@aws-sdk/client-s3`.
- `InvokeCommand` returns `Payload` as a `Uint8Array` — decode with `new TextDecoder().decode(response.Payload)` before `JSON.parse`.
- SDK v3 version mismatches across client packages cause TypeScript errors — pin all `@aws-sdk/*` packages to the same version range.
- In Lambda, the SDK is bundled in the runtime but may be outdated — bundle your own version for latest features.
- `SQS ReceiveMessageCommand` may return `Messages: undefined` (not empty array) when no messages are available — always use `response.Messages ?? []`.
- Presigned URL expiry is capped at 7 days, but temporary credentials may expire sooner — the URL stops working when the signing credentials expire.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use AWS SDK v3 modular packages (`@aws-sdk/client-*`) — NEVER the monolithic `aws-sdk` v2 package)**

**(You MUST use the command pattern: `client.send(new XxxCommand({...}))` — NEVER call methods directly on the client)**

**(You MUST use `DynamoDBDocumentClient` from `@aws-sdk/lib-dynamodb` for DynamoDB — it auto-marshalls native JS types)**

**(You MUST handle errors with `instanceof` specific exception classes — NEVER catch generic `Error` and check `.code`)**

**(You MUST use built-in paginators (`paginate*` functions) for paginated APIs — NEVER manually track continuation tokens)**

**Failure to follow these rules will cause bloated bundles (v2), lost type safety (direct calls), marshalling bugs (raw DynamoDB), and fragile error handling (string comparison).**

</critical_reminders>
