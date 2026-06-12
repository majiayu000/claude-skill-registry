---
name: inngest-v3-v4-migration
description: Use when upgrading an existing TypeScript codebase from Inngest SDK v3 to v4, or when fixing mixed v3/v4 API usage. Covers detecting current SDK usage, moving triggers into createFunction options, replacing EventSchemas with eventType/staticSchema, moving serve options to the client, updating realtime imports, rewriting step.invoke string IDs, checkpointing/serverless runtime settings, Connect option changes, and verification.
---

# Inngest v3 to v4 Migration

Use this skill when the user asks to upgrade Inngest, fix v3/v4 errors, migrate
realtime, or clean up a codebase that has mixed SDK patterns.

Primary reference:
https://www.inngest.com/docs/reference/typescript/v4/migrations/v3-to-v4

This skill is agent-first: detect actual usage first, make mechanical API
changes in a controlled order, then typecheck and run focused tests.

## When to Trigger

Use this skill for requests like:

- "Upgrade Inngest from v3 to v4"
- "Fix our Inngest v4 migration"
- "We're getting signing key required / cloud mode errors after upgrading"
- "`step.invoke` with a string function ID stopped working"
- "`@inngest/realtime` broke after installing `inngest@4`"
- "Move from EventSchemas to eventType"
- "Make this existing Inngest repo v4-compatible"

If the user asks for a broad codebase reliability audit first, use
`inngest-brownfield-audit` to choose scope, then return here for the v4 changes.

## Migration Scan

Start by locating all Inngest surfaces:

```bash
rg -n '"inngest"|"@inngest/realtime"|"@inngest/agent-kit"' package.json **/package.json
rg -n 'new Inngest|EventSchemas|eventType|staticSchema|createFunction\\(|serve\\(|connect\\(|step\\.invoke|referenceFunction|@inngest/realtime|realtimeMiddleware|useInngestSubscription|serveHost|rewriteGatewayEndpoint|logLevel|streaming:|signingKey|signingKeyFallback|baseUrl|INNGEST_DEV|INNGEST_SIGNING_KEY' .
```

Then classify the repo:

- **No Inngest yet:** use `inngest-setup`, not this migration skill.
- **v3 only:** migrate the SDK and all breaking changes together.
- **mixed v3/v4:** prioritize removing broken v3 APIs from v4 code.
- **v4 mostly done:** focus on missed runtime gotchas like local dev mode,
  serverless `maxRuntime`, realtime package imports, and string `step.invoke`.

Before editing, record:

```text
Inngest migration scan:
- Current package versions:
- Client files:
- Serve/connect entrypoints:
- Functions using old trigger syntax:
- EventSchemas usage:
- Realtime v3 package usage:
- step.invoke string IDs:
- Serverless runtime constraints:
- Tests/checks available:
```

## Upgrade Order

1. Update package versions.
2. Fix client construction and local/prod mode.
3. Move serve options to the client.
4. Move triggers into `createFunction` options.
5. Replace `EventSchemas` with `eventType()` / `staticSchema()`.
6. Rewrite `step.invoke()` string IDs.
7. Migrate realtime from `@inngest/realtime` to v4 native APIs.
8. Update middleware and logging.
9. Configure checkpointing/serverless runtime.
10. Typecheck, run tests, and optionally sync with the dev server.

## Package and Environment

Install the latest v4 SDK:

```bash
npm install inngest@latest
# or pnpm add inngest@latest
# or yarn add inngest@latest
```

If the repo uses v3 realtime, remove `@inngest/realtime`; v4 realtime lives in
the `inngest` package and subpaths such as `inngest/realtime`, `inngest/react`,
and native `step.realtime` / `inngest.realtime`.

v4 defaults to Cloud mode. For local development, use an env var:

```bash
INNGEST_DEV=1 npm run dev
```

Do not hardcode `isDev: true` in source unless the repo's existing environment
pattern clearly scopes it to local-only code. Production should use
`INNGEST_SIGNING_KEY`.

## Client and Serve Options

In v4, options such as `signingKey`, `signingKeyFallback`, and `baseUrl` belong
on `new Inngest(...)`, not on `serve(...)`.

```typescript
// Old v3
app.use(
  "/api/inngest",
  serve({
    client: inngest,
    functions,
    signingKey: process.env.INNGEST_SIGNING_KEY,
    baseUrl: process.env.INNGEST_BASE_URL,
  })
);

// New v4
export const inngest = new Inngest({
  id: "my-app",
  signingKey: process.env.INNGEST_SIGNING_KEY,
  baseUrl: process.env.INNGEST_BASE_URL,
});

app.use("/api/inngest", serve({ client: inngest, functions }));
```

If the repo already relies on supported environment variables and does not pass
serve options explicitly, no code change may be required for those keys.

Other renames:

- `serveHost` -> `serveOrigin`
- `streaming: "force"` -> `streaming: true`
- `streaming: "allow"` -> `streaming: true`
- `streaming: false` stays `false`
- `logLevel` is removed; pass a `logger` such as `new ConsoleLogger({ level })`

## createFunction Triggers

Triggers move into the first argument's options object.

```typescript
// Old v3
inngest.createFunction(
  { id: "send-welcome" },
  { event: "user/created" },
  async ({ event, step }) => {}
);

// New v4
inngest.createFunction(
  { id: "send-welcome", triggers: [{ event: "user/created" }] },
  async ({ event, step }) => {}
);
```

Cron triggers move the same way:

```typescript
inngest.createFunction(
  { id: "nightly-sync", triggers: [{ cron: "0 2 * * *" }] },
  async ({ step }) => {}
);
```

If a function is invoked only via `step.invoke`, it may be triggerless.

## EventSchemas to eventType/staticSchema

Replace centralized `EventSchemas` with event-specific definitions.

```typescript
import { Inngest, eventType, staticSchema } from "inngest";
import { z } from "zod";

export const userCreated = eventType("user/created", {
  schema: z.object({
    userId: z.string(),
    email: z.string().email(),
  }),
});

type InvoicePaid = {
  invoiceId: string;
  customerId: string;
};

export const invoicePaid = eventType("billing/invoice.paid", {
  schema: staticSchema<InvoicePaid>(),
});
```

Use event types consistently:

```typescript
await inngest.send(userCreated.create({ userId, email }));

inngest.createFunction(
  { id: "on-user-created", triggers: [userCreated] },
  async ({ event }) => {}
);

await step.waitForEvent("wait-for-invoice", {
  event: invoicePaid,
  timeout: "7d",
});
```

Important: `staticSchema` expects a type, not an interface. Convert interfaces
to type aliases when needed.

## step.invoke

v4 no longer accepts raw string function IDs. Use an imported function
reference or `referenceFunction()`.

```typescript
import { referenceFunction } from "inngest";

await step.invoke("run-report", {
  function: referenceFunction({
    appId: "analytics-app",
    functionId: "generate-report",
  }),
  data: { reportId },
});
```

If the target function is in the same codebase, prefer passing the imported
function itself:

```typescript
await step.invoke("run-report", {
  function: generateReport,
  data: { reportId },
});
```

## Realtime Migration

v3 realtime used `@inngest/realtime` and middleware-injected `publish`.
v4 realtime is native.

Replace:

- `@inngest/realtime` package
- `realtimeMiddleware()`
- handler args such as `{ publish }`
- v3 React hooks such as `useInngestSubscription()`

With:

- channel definitions from `inngest/realtime`
- `step.realtime.publish` between steps
- `inngest.realtime.publish` inside an existing `step.run`
- subscription helpers/hooks from current v4 APIs

Use `inngest-realtime` for detailed patterns. Do not call
`step.realtime.publish` from inside `step.run`; use `inngest.realtime.publish`
there to avoid step-in-step behavior.

## Parallelism and Checkpointing

v4 enables optimized parallelism and checkpointing by default.

Watch for `Promise.race` over steps. With optimized parallelism, `Promise.race`
waits for all step promises to settle. If the repo relies on first-winner
behavior, use `group.parallel()`.

For serverless platforms, configure checkpointing `maxRuntime` slightly below
the platform limit:

```typescript
export const inngest = new Inngest({
  id: "my-app",
  checkpointing: {
    maxRuntime: "50s",
  },
});
```

On Vercel or similar frameworks, also set the route handler's max duration
where the platform supports it.

## Connect Changes

If the repo uses Connect:

- `rewriteGatewayEndpoint` is replaced by `gatewayUrl`.
- Connect may use worker-thread isolation. If integration issues appear, check
  `isolateExecution: false` or `INNGEST_CONNECT_ISOLATE_EXECUTION=false`.
- Keep target URLs and signing/event keys in env vars.

## Verification

Run checks in increasing confidence:

1. Package manager install/update.
2. Typecheck.
3. Unit/integration tests around migrated functions.
4. Start the app with `INNGEST_DEV=1`.
5. Run `npx inngest-cli@latest dev` and confirm function discovery.
6. Send one representative event and inspect the run.

If local dev-server verification is not possible, state exactly which static
checks passed and what runtime verification remains.

## Common Failure Messages

- **"A signing key is required to run in Cloud mode"**: set `INNGEST_DEV=1` for
  local development or configure `INNGEST_SIGNING_KEY` for production.
- **`Cls is not a constructor` on `/api/inngest`**: likely v3
  `@inngest/realtime` middleware in a v4 app. Remove the package and migrate to
  native realtime.
- **`step.invoke` fails with string function ID**: replace strings with
  imported function references or `referenceFunction()`.
- **Type errors around schemas**: replace `EventSchemas` with `eventType()` and
  `staticSchema()`.
- **Unexpected `Promise.race` behavior**: use `group.parallel()` for first-winner
  step races or disable optimized parallelism only when necessary.

## Anti-Patterns

- Mixing v3 realtime middleware with `inngest@4`.
- Passing `signingKey`, `baseUrl`, or `signingKeyFallback` to `serve()`.
- Moving event trigger syntax but forgetting cron/invoke-triggered functions.
- Replacing `EventSchemas` with untyped string events everywhere.
- Hardcoding `isDev: true` in production-bound source.
- Leaving string IDs in `step.invoke`.
- Skipping typecheck after mechanical migration.
