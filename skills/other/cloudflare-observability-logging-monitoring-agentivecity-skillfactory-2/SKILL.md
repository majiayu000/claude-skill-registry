---
name: "cloudflare-observability-logging-monitoring"
description: "Use this skill whenever the user wants to improve or set up logging, tracing, metrics, and monitoring for Cloudflare Workers/Pages (e.g. Hono + TypeScript), including Wrangler tail, Workers Analytics, log structure, and integration with external tools like Sentry."
---

# Cloudflare Observability, Logging & Monitoring Skill

## Purpose

You are a specialized assistant for making **Cloudflare Workers/Pages apps observable**:

- Helpful, structured **logging**
- Convenient **local + remote debugging**
- Basic **metrics & analytics**
- Integration with external tools for **error tracking** (e.g. Sentry)
- Production-safe **log practices** (no secrets, PII minimization)

Use this skill to:

- Design and improve logging strategy in Workers/Hono apps
- Configure **Wrangler tail** workflows and filters
- Suggest **Workers Analytics** / dashboards usage
- Integrate **error reporting** into deployment (e.g., Sentry capture)
- Make it easy to **debug production issues quickly**

Do **not** use this skill for:

- Deployment & CI/CD itself → use `cloudflare-worker-deployment`, `cloudflare-ci-cd-github-actions`
- Application-level auth logic or DB schema → use Hono/D1 skills
- Deep vendor-specific APM setup outside the Cloudflare/Workers context

If `CLAUDE.md` has logging or observability standards (log format, correlation IDs, tools), follow them.

---

## When To Apply This Skill

Trigger this skill when the user says things like:

- “I want better logging for my Cloudflare Worker.”
- “How do I debug errors in production Workers?”
- “Add structured logs and correlation IDs to my Hono app.”
- “Integrate Sentry with my Cloudflare Worker.”
- “Help me use Wrangler tail and Workers Analytics.”

Avoid when:

- You’re only dealing with pure business logic and no operational concerns.
- Logging/monitoring is handled entirely upstream (e.g., API Gateway with its own tooling).

---

## Logging Basics in Cloudflare Workers

Workers use `console.log`, `console.error`, etc., with output viewable via:

- `wrangler dev` (local)
- `wrangler tail` (live logs from deployed Worker)
- Cloudflare dashboard (Workers → Logs / Tail)

This skill should:

- Prefer **structured logs** (objects) over plain strings when useful.
- Include relevant context: method, path, request id, user id (if authenticated).

Example structured log in a Hono handler:

```ts
app.use("*", async (c, next) => {
  const start = Date.now();
  const requestId = crypto.randomUUID();

  c.set("requestId", requestId);

  await next();

  const ms = Date.now() - start;
  console.log(
    JSON.stringify({
      level: "info",
      msg: "request_completed",
      requestId,
      method: c.req.method,
      path: c.req.path,
      status: c.res.status,
      durationMs: ms,
    }),
  );
});
```

This skill will:

- Encourage use of a **request ID** to correlate logs.
- Suggest using `JSON.stringify` for log messages where structured parsing is helpful.

---

## Error Logging & Global Error Handler

Combine `hono-app-scaffold` error middleware with structured logging.

Example error handler middleware:

```ts
// src/middlewares/error-handler.ts
import type { MiddlewareHandler } from "hono";

export const errorHandler: MiddlewareHandler = async (c, next) => {
  try {
    await next();
  } catch (err) {
    const requestId = c.get("requestId");
    console.error(
      JSON.stringify({
        level: "error",
        msg: "unhandled_error",
        requestId,
        error: String(err),
        stack: err instanceof Error ? err.stack : undefined,
      }),
    );

    return c.json(
      {
        message: "Internal Server Error",
        requestId,
      },
      500,
    );
  }
};
```

This skill should:

- Ensure sensitive info (passwords, tokens, full request bodies) is NOT logged.
- Provide consistent error response patterns including `requestId` to aid debugging.

---

## Using Wrangler Tail

This skill helps you leverage `wrangler tail` effectively:

- To view logs from live Workers:

  ```bash
  wrangler tail
  ```

- With environment:

  ```bash
  wrangler tail --env production
  ```

- With log formatting or filters (where available) to focus on errors.

It should recommend typical debugging flow:

1. Reproduce problem in staging or dev env.
2. Use `wrangler tail --env staging` while hitting the endpoint.
3. Look for `requestId` from client error to find matching logs.

---

## Workers Analytics & Metrics

Cloudflare provides Workers metrics (requests, errors, duration, CPU time).

This skill should:

- Recommend checking **Workers Analytics** in the Cloudflare dashboard.
- Use metrics to spot:
  - Error spikes
  - Latency trends
  - Hot routes (high traffic)
- Combine with log insights to identify problematic endpoints.

Where appropriate, this skill can suggest exporting analytics via:

- Cloudflare Analytics APIs
- External dashboards (e.g., Grafana, if configured) – but details belong to another skill.

---

## Custom Application Metrics (Lightweight)

Workers don’t have built-in Prometheus-style counters, but this skill can suggest:

- Simple **log-based metrics** (structured logs with `metric:` fields).
- Using KV or D1 for aggregated counters in low-volume scenarios (with caution).

Example metric event in logs:

```ts
console.log(
  JSON.stringify({
    level: "info",
    metric: "user_signup",
    userId: newUser.id,
  }),
);
```

Then logs can be filtered or exported to build dashboards.

For heavier metrics, this skill may suggest specialized observability tools rather than re-inventing a metrics store inside Workers.

---

## Integration With Sentry (or Similar)

For error tracking, this skill can sketch a Sentry integration pattern:

1. Use Sentry’s JavaScript SDK compatible with Workers (or a minimal custom HTTP client to send events).
2. Initialize Sentry at the top-level or in middleware.
3. Capture exceptions in the error handler.

Pseudo-example:

```ts
import * as Sentry from "@sentry/browser"; // or Workers-compatible SDK

Sentry.init({
  dsn: c.env.SENTRY_DSN,
  tracesSampleRate: 0.1,
});

export const errorHandler: MiddlewareHandler = async (c, next) => {
  try {
    await next();
  } catch (err) {
    Sentry.captureException(err);
    console.error("Unhandled error", err);
    return c.json({ message: "Internal Server Error" }, 500);
  }
};
```

This skill will:

- Remind to keep DSN and other secrets in Workers env (`c.env.SENTRY_DSN`), not in source.
- Keep Sentry optional and pluggable, not hardwired.

For other providers (e.g., Logflare, Datadog, Honeycomb), use a similar pattern: emit HTTP events from Workers using fetch, observing rate limits and privacy constraints.

---

## Redacting Sensitive Data

This skill must emphasize:

- Never log raw passwords, access tokens, refresh tokens, SSH keys, etc.
- Be cautious with logging full headers or bodies; if necessary, sanitize them.

Example sanitization helper:

```ts
function safeLogRequest(c: any) {
  const url = new URL(c.req.url);
  console.log(
    JSON.stringify({
      level: "info",
      msg: "request",
      method: c.req.method,
      path: url.pathname,
      // DO NOT log full body or sensitive headers by default
    }),
  );
}
```

Use this in middleware when you need to log incoming request metadata.

---

## Observability for D1 & R2 Operations

When using `hono-d1-integration` and `hono-r2-integration`, this skill can:

- Suggest logging queries at a high level (not full SQL with params in prod).
- Log key metadata for R2 operations:

  ```ts
  console.log(
    JSON.stringify({
      level: "info",
      msg: "r2_put",
      key,
      size: fileSize,
      requestId,
    }),
  );
  ```

- For D1, log slow queries and errors with `durationMs` and table names.

Ensure logs remain **high-level** and don’t leak personal data.

---

## Observability in CI/CD

This skill can connect with `cloudflare-ci-cd-github-actions` by:

- Recommending that `deploy` workflows:

  - Output Worker version / commit SHA.
  - Optionally ping an external “deployment log” (Sentry Release, Slack message, etc.).

- This helps correlate incidents with releases.

Example: log release info in Worker startup or CI:

```ts
console.log(
  JSON.stringify({
    level: "info",
    msg: "worker_deployed",
    commit: process.env.GIT_COMMIT ?? "unknown",
    env: process.env.NODE_ENV,
  }),
);
```

In Workers, use `vars` from `wrangler.toml` like `GIT_COMMIT` set during CI.

---

## Local vs Production Logging Modes

This skill can support:

- **Verbose logging** in dev:
  - More detailed logs, possibly including body snippets.
- **Minimal logging** in production:
  - Only errors + key request metrics.

So code can branch based on `NODE_ENV` or `APP_ENV` from `c.env`.

Example:

```ts
const isDev = c.env.NODE_ENV === "development";
if (isDev) {
  console.log("Debug info:", { body: await c.req.text() });
}
```

Be extra careful not to ship verbose logging into production accidentally.

---

## Troubleshooting Patterns

When something goes wrong in prod, this skill should guide the steps:

1. Identify the failing endpoint & approximate timestamp.
2. Get the `requestId` if the client saw a structured error.
3. Run `wrangler tail --env production` and filter by `requestId`.
4. Inspect logs for stack trace & upstream/downstream failures (D1/R2).
5. Use Workers Analytics to see if the issue is systemic or localized.
6. If using Sentry/other tool, cross-reference alerts with logs.

This gives a repeatable **incident debugging recipe**.

---

## Interaction With Other Skills

- `hono-app-scaffold`:
  - This skill plugs into middlewares and `app` setup to add logging & error-handling.
- `cloudflare-worker-deployment`:
  - Uses its environment setup to decide logging verbosity and env names.
- `cloudflare-ci-cd-github-actions`:
  - Can add deploy logs and release annotations.
- `hono-d1-integration` / `hono-r2-integration`:
  - Observability skill adds light logging around DB & storage operations.

---

## Example Prompts That Should Use This Skill

- “Improve logging and error handling in my Hono Worker.”
- “Help me debug an issue using wrangler tail and request IDs.”
- “Add structured logs to all requests and responses.”
- “Integrate Sentry with my Cloudflare Worker for error tracking.”
- “Make sure we don’t log sensitive data but still have enough info to debug.”

For such tasks, rely on this skill to make your Cloudflare Workers **observable, debuggable, and safe** in production,
without overwhelming you with noisy or sensitive logs.
