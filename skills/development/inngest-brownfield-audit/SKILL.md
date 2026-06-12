---
name: inngest-brownfield-audit
description: Use when analyzing an existing TypeScript or JavaScript codebase to decide where and how to introduce Inngest. Covers repository discovery, framework and package detection, finding durability gaps in HTTP handlers, webhooks, cron jobs, queues, long-running jobs, AI agents, polling loops, and side-effect-heavy code, then producing and implementing an incremental integration plan.
---

# Inngest Brownfield Audit

Use this skill when asked to inspect an existing codebase, add
Inngest "where it makes sense", migrate fragile background work, or find
durability gaps before making changes.

This is an agent-first workflow. Do the audit from evidence in the repo, name
the specific files and call sites that drove each conclusion, and make small
integration moves that preserve current behavior.

## When to Trigger

Use this skill for requests like:

- "Audit this repo for Inngest opportunities"
- "Add Inngest to this codebase"
- "Make our webhooks / cron jobs / background tasks reliable"
- "Find places where work can be lost on deploy or process crash"
- "Replace fragile polling, delayed jobs, or fire-and-forget promises"
- "Make this AI workflow / agent durable"

If the user is starting from scratch instead of a brownfield repo, use
`inngest-setup`, `inngest-durable-functions`, `inngest-events`,
`inngest-steps`, and, for AI workflows, the agent patterns in this skill.

## Audit Loop

1. **Map the project shape.**
   - Read `package.json`, workspace files, app/router structure, server entry
     points, deployment config, and test scripts.
   - Identify framework: Next.js App Router, Next.js Pages Router, Express,
     Hono, Fastify, Remix, SvelteKit, Astro, NestJS, worker-only service, or
     other.
   - Detect package manager and TypeScript conventions before adding files.

2. **Find existing Inngest usage.**
   - Search for `inngest`, `createFunction`, `serve(`, `/api/inngest`,
     `INNGEST_`, `step.run`, `step.sleep`, `step.waitForEvent`,
     `step.sendEvent`, `step.invoke`, `step.ai`, `inngest.send`, and
     `@inngest/realtime`.
   - If Inngest exists, inspect version, client config, serve endpoint,
     registered functions, event naming, env vars, and v3/v4 API shape before
     changing anything.

3. **Find durability gaps.**
   - Search for fire-and-forget work: `void someAsync()`, un-awaited promises,
     `.then(` chains, `setTimeout`, `setInterval`, detached jobs after HTTP
     response, and background work in route handlers.
   - Search for cron and schedulers: `cron`, `node-cron`, `agenda`, `bull`,
     `bullmq`, `bee-queue`, `qstash`, `sqs`, `temporal`, `trigger.dev`,
     deployment cron config, and scheduled API routes.
   - Search for webhooks and at-least-once producers: Stripe, Clerk, GitHub,
     Slack, Shopify, HubSpot, Linear, Svix, and generic `webhook`.
   - Search for long-running work: PDF generation, exports, video/image
     processing, embeddings, bulk email, imports, ETL, sync jobs, polling loops,
     retries, and external API calls.
   - Search for AI agent shapes: tool loops, LLM calls, streaming tokens,
     human approval, multi-step reasoning, vector search, eval loops, and
     provider calls that need rate limits or retry-safe state.

4. **Classify each candidate.**
   - **P0:** user-visible loss, duplicate charge/email/action, timeout, missed
     webhook, or crash-prone workflow.
   - **P1:** fragile but recoverable background work, manual retry burden,
     noisy 429s, or poor observability.
   - **P2:** cleanup, ergonomics, or future migration opportunity.
   - For each candidate, record: file, current trigger, side effects,
     idempotency key, failure mode, recommended Inngest primitive, migration
     size, and confidence.

5. **Choose the smallest safe integration.**
   - Prefer one vertical slice over a wide rewrite.
   - Keep existing domain functions and data models where possible.
   - Add an Inngest client and serve endpoint only once.
   - Move side effects into `step.run` one boundary at a time.
   - Make event IDs and database writes idempotent before adding retries.
   - Add tests around existing behavior and the new event/function boundary.

## Useful Discovery Commands

Run commands that fit the repo. Prefer `rg`; keep output focused.

```bash
rg -n "inngest|createFunction|step\\.|serve\\(|/api/inngest|INNGEST_" .
rg -n "setTimeout|setInterval|Promise\\.all|void [a-zA-Z0-9_]+\\(|\\.then\\(" .
rg -n "cron|node-cron|schedule|bull|bullmq|bee-queue|agenda|qstash|sqs" .
rg -n "webhook|stripe|svix|clerk|github|shopify|slack|hubspot|linear" .
rg -n "retry|backoff|poll|status|timeout|429|rate limit|rate-limit" .
rg -n "openai|anthropic|ai\\.|generateText|streamText|tool|agent|embedding" .
```

When the repo is large, narrow searches to app source directories and exclude
generated/vendor folders.

## Brownfield Decision Matrix

| Existing shape | Inngest fit | Primary primitives |
|---|---|---|
| HTTP handler does slow side effects before responding | Emit event, return fast | `inngest.send`, event trigger, `step.run` |
| Webhook must acknowledge quickly but process reliably | Verify signature, emit idempotent event | Event ID, `step.run`, retries |
| Cron job loses progress midway | Cron-triggered durable function | Cron trigger, page-level `step.run`, flow control |
| Polling loop waits for external async work | Durable wait or durable poll | `step.waitForEvent`, `step.sleep`, `step.run` |
| Large fan-out exceeds request/serverless limits | Split orchestration and item work | `step.sendEvent`, per-item function, concurrency |
| External API hits 429s | Move limits to function config | `throttle`, `rateLimit`, `concurrency` |
| Human review can take days | Persist the wait in Inngest | `step.waitForEvent`, timeout, realtime |
| AI agent/tool loop needs retry-safe progress | One step per tool/model boundary | `step.ai`, `step.run`, `step.sleep`, realtime |
| Existing queue only hides fragile work | Replace queue boundary gradually | Event trigger, idempotency, function-level retries |

## Integration Plan Format

Before editing, summarize findings in this compact shape:

```text
Inngest audit:
- Existing Inngest: none / partial / healthy / risky
- Framework: <framework and evidence>
- Best first slice: <file + workflow>
- Why: <loss/timeout/retry/idempotency failure>
- Proposed primitives: <event, steps, flow control, waits, realtime>
- Idempotency key: <source of truth>
- Files likely touched: <short list>
- Tests/checks: <commands or focused cases>
```

Then implement unless the user asked for audit-only.

## Existing Inngest Checklist

If Inngest is already present, verify:

- A single shared client is exported from a stable module.
- The app `id` is a stable slug and is not derived from deploy-specific data.
- v4 local development uses `INNGEST_DEV=1`; production uses
  `INNGEST_SIGNING_KEY`.
- Serve endpoint path is discoverable, usually `/api/inngest`.
- The serve handler registers all functions that should sync.
- Side effects and non-deterministic work are inside steps.
- Step IDs are stable and descriptive.
- Event names follow `domain/noun.verb`.
- Events that may be replayed use deterministic IDs.
- Webhook handlers verify signatures before emitting events.
- Flow control is configured where external APIs have limits.
- Realtime uses v4 native `inngest/realtime`, not the v3
  `@inngest/realtime` package.

## Durable Agent Patterns

Use Inngest when an AI or agent workflow needs durable progress across model
calls, tool calls, waits, approvals, or streaming UI updates.

Good candidates:

- Multi-step agent that calls tools or external APIs.
- LLM workflow that may exceed one HTTP request lifetime.
- Human-in-the-loop review, approval, correction, or escalation.
- Agent that must pause for an external event or scheduled follow-up.
- Bulk AI work that needs provider-level rate limits and cost protection.
- User-visible agent progress that should stream from durable execution.

Recommended shape:

1. HTTP/UI request stores the user intent and emits an event with a stable
   `id`.
2. Inngest function loads state inside `step.run`.
3. Each model call, tool call, vector search, and external side effect lives in
   its own `step.ai` or `step.run` boundary.
4. Human pauses use `step.waitForEvent` or `step.waitForSignal` with a timeout.
5. Progress updates use `step.realtime.publish` between steps, or
   `inngest.realtime.publish` inside an existing `step.run`.
6. Provider rate limits use `concurrency`, `throttle`, or `rateLimit`, not
   ad hoc in-process throttlers.

Avoid:

- Keeping agent state only in memory.
- Retrying whole agent loops after a single tool failure.
- Charging for repeated successful model calls because the result was not
  memoized.
- Using `setTimeout` or a cron poller for follow-ups and approvals.
- Streaming progress from a process-local WebSocket server when the workflow
  itself is durable elsewhere.

## Implementation Guardrails

- Do not replace working queues, crons, or webhooks blindly. First preserve
  behavior with a thin Inngest slice.
- Do not create duplicate clients or serve endpoints if the repo already has
  them.
- Do not put database writes, API calls, random IDs, timestamps, or LLM calls
  outside steps in the new function.
- Do not hide missing idempotency behind retries. Retries require idempotent
  side effects.
- Do not hardcode secrets or dev-mode flags in source.
- Do not leave the app unable to sync: register new functions with the serve
  endpoint and run available type/tests.

## Verification

Pick checks that prove the integration path:

- Typecheck/build/lint the touched app.
- Run existing tests around the migrated handler or workflow.
- Add focused tests for "handler emits event and returns fast" and "function
  calls the same domain operations in step boundaries" where the repo supports
  it.
- If local runtime is available, start the app and Inngest dev server, confirm
  the function syncs, then send a sample event.
- If only static checks are available, explicitly state that runtime sync was
  not verified.
