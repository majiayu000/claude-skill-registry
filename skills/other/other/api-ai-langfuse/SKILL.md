---
name: api-ai-langfuse
description: LLM observability with Langfuse — OpenTelemetry-based tracing, evaluations, prompt management, datasets, and production best practices
---

# Langfuse Observability Patterns

> **Quick Guide:** Use the Langfuse TypeScript SDK (built on OpenTelemetry) to add observability to LLM applications. Install `@langfuse/tracing`, `@langfuse/otel`, and `@opentelemetry/sdk-node` for core tracing. Use `startActiveObservation()` for automatic context propagation or `observe()` to wrap functions. Use `@langfuse/openai` with `observeOpenAI()` for zero-config OpenAI tracing. Use `LangfuseClient` from `@langfuse/client` for prompt management, scores, and datasets. Always call `forceFlush()` or `sdk.shutdown()` in short-lived processes.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST import and register `instrumentation.ts` at the top of your entry point BEFORE any other imports -- OpenTelemetry must instrument modules before they are loaded)**

**(You MUST call `forceFlush()` or `sdk.shutdown()` in short-lived processes (serverless, scripts, CLI tools) -- events are batched and will be lost without explicit flushing)**

**(You MUST use `@langfuse/openai` with `observeOpenAI()` for OpenAI SDK tracing -- do NOT manually create generation observations for OpenAI calls when the wrapper handles it automatically)**

**(You MUST set `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`, and `LANGFUSE_BASE_URL` via environment variables -- never hardcode credentials)**

**(You MUST use `startActiveObservation()` or `observe()` for nested tracing -- manual `startObservation()` requires explicit `.end()` calls and does NOT propagate context automatically)**

</critical_requirements>

---

**Auto-detection:** Langfuse, langfuse, @langfuse/tracing, @langfuse/otel, @langfuse/client, @langfuse/openai, LangfuseSpanProcessor, LangfuseClient, startActiveObservation, startObservation, observeOpenAI, langfuse.score, langfuse.prompt, langfuse.dataset, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, forceFlush

**When to use:**

- Adding observability and tracing to LLM application code (any provider)
- Wrapping OpenAI SDK calls for automatic token/cost tracking
- Managing prompt templates with versioning, labels, and variable compilation
- Evaluating LLM output quality with scores (numeric, categorical, boolean)
- Running experiments against datasets for regression testing
- Tracking sessions, users, and metadata across multi-turn conversations
- Monitoring LLM costs and token usage in production

**Key patterns covered:**

- OpenTelemetry setup with `LangfuseSpanProcessor`
- Tracing with `startActiveObservation`, `observe`, and manual `startObservation`
- Observation types (span, generation, agent, tool, retriever, evaluator, embedding, chain, guardrail)
- OpenAI SDK auto-instrumentation with `observeOpenAI()`
- Prompt management (get, compile, text vs chat prompts, versioning)
- Scores and evaluations (numeric, categorical, boolean)
- Datasets and experiments for testing
- Flush, shutdown, and lifecycle management

**When NOT to use:**

- You only need basic `console.log` debugging -- Langfuse is for structured production observability
- You want provider-specific tracing built into an AI SDK -- check if your framework has native observability
- You need APM/infrastructure monitoring (CPU, memory, HTTP latency) -- use a general-purpose observability tool

---

## Examples Index

- [Core: Setup & Configuration](examples/core.md) -- OpenTelemetry setup, instrumentation file, client init, flush/shutdown
- [Tracing](examples/tracing.md) -- startActiveObservation, observe, manual tracing, nesting, observation types, metadata
- [OpenAI Integration](examples/openai-integration.md) -- observeOpenAI wrapper, streaming, token tracking, custom attributes
- [Prompt Management](examples/prompt-management.md) -- getPrompt, compile, text vs chat, versioning, caching
- [Scores & Datasets](examples/scores-datasets.md) -- Numeric/categorical/boolean scores, datasets, experiments
- [Quick API Reference](reference.md) -- Package index, environment variables, observation types, score methods

---

<philosophy>

## Philosophy

Langfuse provides **open-source LLM observability** built on OpenTelemetry. The SDK (v4+, August 2025) is a ground-up rewrite using OTel as the tracing backbone, meaning traces integrate naturally with the broader observability ecosystem.

**Core principles:**

1. **OpenTelemetry-native** -- Built on OTel spans and context propagation. Langfuse observations are wrappers around OTel spans with LLM-specific attributes (model, tokens, cost). This means any OTel-compatible instrumentation library works alongside Langfuse.
2. **Zero-latency tracing** -- All trace events are queued locally and flushed in background batches. Your application's response time is not affected by observability.
3. **Modular packages** -- `@langfuse/tracing` for instrumentation, `@langfuse/client` for prompts/scores/datasets, `@langfuse/openai` for OpenAI auto-instrumentation. Install only what you need.
4. **Context-first** -- `startActiveObservation()` automatically propagates parent-child relationships. Nested observations inherit context without manual ID threading.
5. **Observation types** -- LLM-specific types (`generation`, `agent`, `tool`, `retriever`, `evaluator`, `embedding`) provide semantic meaning to traces, enabling richer dashboard views and filtering.

**When to use Langfuse:**

- You need production-grade LLM observability with tracing, cost tracking, and evaluations
- You want prompt management with versioning, A/B testing via labels, and variable compilation
- You need dataset-driven testing and experiment tracking for LLM quality assurance
- You want an open-source, self-hostable alternative to proprietary LLM observability platforms

**When NOT to use:**

- Simple debugging -- `console.log` is sufficient for local development
- Infrastructure monitoring -- use Datadog, Grafana, etc. for APM
- You need a complete AI agent framework -- Langfuse is observability, not orchestration

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: OpenTelemetry Setup

Create an `instrumentation.ts` file and import it at the top of your entry point.

```typescript
// instrumentation.ts
import { NodeSDK } from "@opentelemetry/sdk-node";
import { LangfuseSpanProcessor } from "@langfuse/otel";

const sdk = new NodeSDK({
  spanProcessors: [new LangfuseSpanProcessor()],
});

sdk.start();

export { sdk };
```

```typescript
// index.ts -- import instrumentation FIRST
import "./instrumentation";
// All other imports AFTER instrumentation
import { startActiveObservation } from "@langfuse/tracing";
```

**Why good:** OTel must instrument modules before they are loaded; importing instrumentation first ensures all subsequent imports are traced automatically

```typescript
// BAD: importing instrumentation after other modules
import { startActiveObservation } from "@langfuse/tracing";
import "./instrumentation"; // TOO LATE -- tracing won't capture earlier imports
```

**Why bad:** OpenAI/LangChain auto-instrumentation requires OTel to be initialized before those SDKs are imported

**See:** [examples/core.md](examples/core.md) for environment variables, sampling, masking, and production configuration

---

### Pattern 2: Tracing with startActiveObservation

The primary instrumentation pattern. Creates an observation, makes it the active context, and automatically ends it when the callback completes.

```typescript
import { startActiveObservation } from "@langfuse/tracing";

async function handleRequest(query: string): Promise<string> {
  return await startActiveObservation("handle-request", async (span) => {
    span.update({ input: { query } });

    // Nested observation -- automatically becomes a child
    const result = await startActiveObservation(
      "process-query",
      async (child) => {
        child.update({ input: { query } });
        const answer = await callLLM(query);
        child.update({ output: { answer } });
        return answer;
      },
    );

    span.update({ output: { result } });
    return result;
  });
}
```

**Why good:** Automatic context propagation, automatic end on callback completion, nesting creates parent-child hierarchy without manual ID management

```typescript
// BAD: using startObservation without ending it
import { startObservation } from "@langfuse/tracing";

const span = startObservation("my-span");
await doWork();
// span.end() never called -- observation stays open forever
```

**Why bad:** Manual `startObservation` requires explicit `.end()` calls; forgetting creates open-ended observations

**See:** [examples/tracing.md](examples/tracing.md) for observe wrapper, observation types, metadata, and manual tracing

---

### Pattern 3: The observe() Wrapper

Wraps a function to automatically capture inputs, outputs, timings, and errors.

```typescript
import { observe } from "@langfuse/tracing";

const classifyIntent = observe(
  async (query: string) => {
    const result = await callLLM(query);
    return result.intent;
  },
  { name: "classify-intent", asType: "generation" },
);

// Usage -- automatically traced
const intent = await classifyIntent("Book a flight to Paris");
```

**Why good:** Declarative tracing, inputs/outputs captured automatically, `asType` tags the observation type for richer dashboard filtering

---

### Pattern 4: OpenAI Auto-Instrumentation

Use `observeOpenAI()` to wrap the OpenAI client for automatic tracing of all calls.

```typescript
import OpenAI from "openai";
import { observeOpenAI } from "@langfuse/openai";

const openai = observeOpenAI(new OpenAI());

// All calls automatically traced with model, tokens, cost
const completion = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Hello" }],
});
```

**Why good:** Zero manual instrumentation, captures model name, token counts, estimated costs, latency, and streaming metrics automatically

```typescript
// BAD: manually creating generation observations for OpenAI calls
await startActiveObservation("openai-call", async (span) => {
  const result = await rawOpenai.chat.completions.create({ ... });
  span.update({
    model: "gpt-4o",
    input: messages,
    output: result.choices[0].message.content,
  });
}, { asType: "generation" });
```

**Why bad:** `observeOpenAI` handles all of this automatically with more accurate token/cost data; manual tracking is error-prone and duplicates effort

**See:** [examples/openai-integration.md](examples/openai-integration.md) for streaming, custom attributes, and token tracking on streams

---

### Pattern 5: Prompt Management

Fetch versioned prompts, compile with variables, and link to traces.

```typescript
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

// Fetch a text prompt (production label by default)
const prompt = await langfuse.prompt.get("summarize-article");
const compiled = prompt.compile({ topic: "AI safety", length: "brief" });
// -> "Write a brief summary about AI safety."

// Fetch a chat prompt
const chatPrompt = await langfuse.prompt.get("assistant-v2", { type: "chat" });
const messages = chatPrompt.compile({ userName: "Alice" });
// -> [{ role: "system", content: "You are helping Alice..." }, ...]
```

**Why good:** Centralized prompt management with versioning, labels for A/B testing, variable compilation, and built-in caching

**See:** [examples/prompt-management.md](examples/prompt-management.md) for versioning, labels, cache control, and linking prompts to traces

---

### Pattern 6: Scores and Evaluations

Attach quality measurements to traces and observations.

```typescript
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

// Numeric score
langfuse.score.create({
  traceId: "trace-123",
  name: "relevance",
  value: 0.95,
  dataType: "NUMERIC",
});

// Categorical score
langfuse.score.create({
  traceId: "trace-123",
  name: "quality",
  value: "good",
  dataType: "CATEGORICAL",
});

// Boolean score (0 or 1)
langfuse.score.create({
  traceId: "trace-123",
  name: "contains-hallucination",
  value: 0,
  dataType: "BOOLEAN",
});

// Score a specific observation within a trace
langfuse.score.create({
  traceId: "trace-123",
  observationId: "obs-456",
  name: "accuracy",
  value: 0.88,
  dataType: "NUMERIC",
});

// Flush in short-lived processes
await langfuse.score.flush();
```

**Why good:** Three data types cover all evaluation needs, scores attach at trace or observation level, fire-and-forget API with batching

**See:** [examples/scores-datasets.md](examples/scores-datasets.md) for active observation scoring, session scores, datasets, and experiments

---

### Pattern 7: Flush and Shutdown

Always flush in short-lived processes. The SDK batches events and sends them asynchronously.

```typescript
import { sdk } from "./instrumentation";
import { LangfuseClient } from "@langfuse/client";
import { LangfuseSpanProcessor } from "@langfuse/otel";

const langfuse = new LangfuseClient();

async function main() {
  // ... do work ...

  // Flush scores
  await langfuse.score.flush();

  // Shutdown OTel SDK (flushes all pending spans)
  await sdk.shutdown();
}

main();
```

**Why good:** Explicit flush/shutdown ensures all events are sent before the process exits; without this, data is silently lost in serverless and scripts

```typescript
// BAD: exiting without flushing
async function handler() {
  await startActiveObservation("my-trace", async (span) => {
    span.update({ output: "done" });
  });
  // Process exits -- batched events never sent
}
```

**Why bad:** Langfuse batches events locally; if the process exits before the flush interval, events are lost

</patterns>

---

<performance>

## Performance Optimization

### Sampling for High-Volume Applications

Reduce costs by sampling a subset of traces:

```typescript
import { TraceIdRatioBasedSampler } from "@opentelemetry/sdk-trace-base";

const sdk = new NodeSDK({
  sampler: new TraceIdRatioBasedSampler(0.2), // Sample 20% of traces
  spanProcessors: [new LangfuseSpanProcessor()],
});
```

Or via environment variable: `LANGFUSE_SAMPLE_RATE=0.2`

### Key Optimization Patterns

- **Batch flush tuning** -- Configure `LANGFUSE_FLUSH_AT` (default 10) and `LANGFUSE_FLUSH_INTERVAL` (default 1s) for your workload
- **Span filtering** -- Use `shouldExportSpan` on `LangfuseSpanProcessor` to drop noisy non-LLM spans
- **Data masking** -- Redact PII before transmission with the `mask` option to avoid storing sensitive data
- **Stream token tracking** -- Set `stream_options: { include_usage: true }` on OpenAI streaming calls so `observeOpenAI` captures token counts

</performance>

---

<decision_framework>

## Decision Framework

### Which Packages to Install

```
What do you need?
+-- Tracing LLM calls?
|   +-- YES -> npm install @langfuse/tracing @langfuse/otel @opentelemetry/sdk-node
|   +-- Also using OpenAI SDK?
|       +-- YES -> npm install @langfuse/openai
+-- Prompt management, scores, or datasets?
|   +-- YES -> npm install @langfuse/client
+-- Both tracing AND client features?
    +-- YES -> Install all: @langfuse/tracing @langfuse/otel @opentelemetry/sdk-node @langfuse/client
```

### Which Tracing Method to Use

```
How do you want to instrument?
+-- Wrapping a function? -> observe() (declarative, auto-captures inputs/outputs)
+-- Block of code with nesting? -> startActiveObservation() (context propagation, auto-end)
+-- Need manual start/end control? -> startObservation() (requires explicit .end())
+-- OpenAI SDK calls? -> observeOpenAI() (zero-config auto-instrumentation)
+-- Update active span without reference? -> updateActiveObservation()
```

### Which Observation Type (asType)

```
What is this observation?
+-- LLM call (prompt -> completion) -> "generation"
+-- AI agent decision-making step -> "agent"
+-- External API or function call -> "tool"
+-- Vector store or DB retrieval -> "retriever"
+-- Quality assessment step -> "evaluator"
+-- Embedding creation -> "embedding"
+-- Link between application steps -> "chain"
+-- Content safety / jailbreak check -> "guardrail"
+-- Generic duration operation -> "span" (default)
+-- Point-in-time event -> "event"
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Not importing `instrumentation.ts` before other modules (auto-instrumentation silently fails)
- Exiting short-lived processes without `forceFlush()` or `sdk.shutdown()` (events are silently lost)
- Hardcoding `LANGFUSE_SECRET_KEY` or `LANGFUSE_PUBLIC_KEY` in source code (credential exposure)
- Using manual generation observations when `observeOpenAI()` would handle it automatically (duplicated effort, less accurate data)
- Using `startObservation()` without calling `.end()` (observation stays open indefinitely)

**Medium Priority Issues:**

- Not setting `stream_options: { include_usage: true }` on OpenAI streaming calls (token counts missing from `observeOpenAI` traces)
- Forgetting to call `langfuse.score.flush()` in short-lived processes (scores are batched and may be lost)
- Using `startObservation()` when `startActiveObservation()` would work (no automatic context propagation or auto-end)
- Not using `asType` on observations (all observations appear as generic spans, losing semantic meaning)
- Not setting `LANGFUSE_BASE_URL` for self-hosted instances (defaults to cloud.langfuse.com)

**Common Mistakes:**

- Importing `@langfuse/openai` without setting up the OTel `NodeSDK` first -- the OpenAI wrapper requires OTel context to send traces
- Confusing `LangfuseClient` (from `@langfuse/client`, for prompts/scores/datasets) with the OTel tracing functions (from `@langfuse/tracing`)
- Using `prompt.compile()` without matching all `{{variable}}` placeholders -- unmatched variables remain as literal `{{name}}` in output
- Calling `langfuse.score.create()` with a `value` of type `string` for `NUMERIC` scores or `number` for `CATEGORICAL` scores (type mismatch)
- Running dataset experiments without OTel setup -- experiment tasks run inside `startActiveObservation` which requires OTel

**Gotchas & Edge Cases:**

- `observeOpenAI()` does NOT support the OpenAI Assistants API -- only Chat Completions and Responses API
- The SDK's default span filter only exports Langfuse and GenAI spans. If you use a custom instrumentation library, you must configure `shouldExportSpan` to include it.
- `LangfuseClient.prompt.get()` caches prompts with a default TTL. If you update a prompt and don't see changes, set `cacheTtlSeconds: 0` to bypass caching.
- Boolean scores use float values (`0` or `1`), not JavaScript booleans (`true`/`false`).
- Self-hosted Langfuse requires platform version >= 3.95.0 for TypeScript SDK v4 compatibility.
- `score.create()` is fire-and-forget (synchronous) -- it queues the score for batched delivery. You only need `await` on `flush()`.
- Dataset names with slashes (`evaluation/qa-dataset`) must be URL-encoded when used as path parameters.
- The v4+ SDK is a complete rewrite from v3 -- `Langfuse` class, `trace()`, `span()`, `generation()` from v3 are replaced by OTel-based APIs.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST import and register `instrumentation.ts` at the top of your entry point BEFORE any other imports -- OpenTelemetry must instrument modules before they are loaded)**

**(You MUST call `forceFlush()` or `sdk.shutdown()` in short-lived processes (serverless, scripts, CLI tools) -- events are batched and will be lost without explicit flushing)**

**(You MUST use `@langfuse/openai` with `observeOpenAI()` for OpenAI SDK tracing -- do NOT manually create generation observations for OpenAI calls when the wrapper handles it automatically)**

**(You MUST set `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`, and `LANGFUSE_BASE_URL` via environment variables -- never hardcode credentials)**

**(You MUST use `startActiveObservation()` or `observe()` for nested tracing -- manual `startObservation()` requires explicit `.end()` calls and does NOT propagate context automatically)**

**Failure to follow these rules will produce silent data loss, missing traces, or credential exposure in LLM observability.**

</critical_reminders>
