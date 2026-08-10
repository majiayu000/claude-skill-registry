---
name: software-ai-integration
description: "Applies production AI integration patterns for chat, structured output, guardrails, provider routing, and AI UX. Use when adding LLM-powered features to an application."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# AI-Augmented Product Engineering

Integrate LLMs and AI capabilities into production applications with clean architecture, cost discipline, and reliable user experience.

## Quick Reference

| Concern | Defaults |
|---|---|
| LLM API integration | Anthropic SDK, OpenAI SDK, Vercel AI SDK |
| Streaming responses | SSE / ReadableStream + AI SDK streamText/streamObject |
| Structured output | JSON mode, tool_use/function calling, Zod schemas |
| Chat interface | AI SDK useChat hook, custom streaming UI |
| AI-assisted forms | Inline suggestions, auto-complete, content generation |
| Guardrails | Input/output filtering, content moderation, PII detection |
| Cost management | Token counting, caching (semantic + exact), model routing |
| Multi-provider | AI SDK provider abstraction, Portkey, LiteLLM, or a thin internal router |
| Evaluation | Human feedback, LLM-as-judge, A/B testing AI variants |
| RAG in products | Vector search + context injection (see also ai-rag for deeper patterns) |

## When to Use This Skill

- Adding AI-powered features to an existing product (chat, generation, suggestions)
- Building streaming UI for LLM responses in web or mobile applications
- Implementing structured output with schema validation from LLM calls
- Designing cost control and caching strategies for AI features
- Building multi-provider fallback and model routing logic
- Implementing guardrails, content moderation, and safety layers
- Choosing AI UX patterns (loading states, regenerate, feedback, attribution)

## When NOT to Use This Skill

- **LLM lifecycle management (fine-tuning, deployment, monitoring)** → [ai-llm](../ai-llm/SKILL.md)
- **Agent system architecture and orchestration** → [ai-agents](../ai-agents/SKILL.md)
- **Prompt engineering techniques and patterns** → [ai-prompt-engineering](../ai-prompt-engineering/SKILL.md)
- **RAG system architecture (indexing, retrieval, chunking)** → [ai-rag](../ai-rag/SKILL.md)
- **ML model training and data science** → [ai-ml-data-science](../ai-ml-data-science/SKILL.md)
- **MLOps and model serving infrastructure** → [ai-mlops](../ai-mlops/SKILL.md)
- **Building MCP servers and tool protocols** → [agents-mcp](../agents-mcp/SKILL.md)

## When NOT to Add AI At All

Not every "AI feature" request should become one. Apply this filter before the decision tree below:

- **Deterministic logic solves it.** If the mapping from input to output is a rule, a regex, a lookup table, or a small classifier that can be trained offline, an LLM call adds latency, cost, and non-determinism for no accuracy gain. Reach for an LLM when the input space is open-ended natural language or the task requires judgment a rule set cannot encode.
- **The eval bar cannot be met.** If nobody can articulate what "correct" looks like well enough to write 20-50 test cases with expected outputs, the team cannot tell if the feature works, regresses, or is safe to ship. Build the eval set before writing the first prompt (see [ai-evals](../ai-evals/SKILL.md)) — "we'll know it when we see it" is not a launch gate.
- **The failure mode is unacceptable and unrecoverable.** High-stakes one-shot actions (irreversible financial transfers, medical dosing, legal filings) need a human-in-the-loop confirmation step even when the model is highly accurate; if the product cannot afford *any* rate of wrong output and cannot insert a checkpoint, do not automate that step with an LLM.
- **A cheaper, boring solution already ships the value.** Autocomplete from historical data, templated responses, or a search index often satisfy the underlying user need without a model call. Prototype the non-AI version first if it is cheap to build — it is also the fallback path required by the guardrail rules below.

## Build vs. Buy

| Decide | Build | Buy / integrate |
|---|---|---|
| Chat UI, streaming, structured output | Build on Vercel AI SDK or a provider SDK — this is commodity glue code now, not a differentiator | — |
| In-app copilot UI shell | Consider CopilotKit if the UI shell itself is not the differentiator | Build custom only if the copilot surface *is* the product |
| Prompt injection / content moderation detection | — | Use provider moderation endpoints or a dedicated vendor (e.g. Lakera-class runtime guard) first; building a custom classifier is a multi-quarter investment that duplicates adversarially-trained vendor models |
| Eval/tracing/observability | — | Use an LLM observability vendor (Langfuse-, Humanloop-class) before building an in-house trace store; the differentiator is your eval *criteria*, not the pipeline plumbing |
| Multi-provider routing/governance | Thin internal router for a single product | Buy a gateway (Portkey-class) once more than one team or product needs shared routing, budgets, or policy |

The recurring judgment call: build the thin layer that encodes *your* product's specific logic (prompts, schemas, eval criteria, business rules); buy the generic infrastructure (streaming plumbing, moderation classifiers, tracing storage) that every AI product needs and that a vendor has already hardened against edge cases you have not seen yet.

## Workflow

1. Classify the feature shape: chat, generation, extraction, search, or agent-adjacent UX.
2. Confirm the product boundary and route architecture-heavy or retrieval-heavy work to the adjacent skill when needed.
3. Pick the primary pattern from the decision tree, then define the request contract, latency target, and safety checks.
4. Apply the relevant implementation guidance for streaming, structure, cost, and guardrails.
5. Verify current provider capabilities with the navigation references and fact-checking rules before final recommendations.

## ASCII Flow

```text
AI feature request
  -> Classify: chat, generation, extraction, search, or agent-adjacent UX
  -> Route architecture, RAG, or agent-heavy work to companion skills
  -> Define typed request and response contract
  -> Choose provider, streaming, safety, and cost controls
  -> Implement product UX states and observability
  -> Verify provider behavior and eval evidence
```

## Decision Tree

```text
What kind of AI feature?
├─ Chat / conversational UI
│  ├─ Web app → Vercel AI SDK (useChat + streamText)
│  │  ├─ Conversation history → Store in DB, not just client state
│  │  ├─ Streaming markdown → Progressive render with remark/rehype
│  │  └─ Multi-turn with tools → Tool results in message history
│  └─ Mobile / native → Direct SSE consumption + custom UI
├─ Content generation ("write for me")
│  ├─ Short-form (titles, descriptions) → Single generation + schema
│  └─ Long-form (articles, reports)
│     └─ Draft → Review → Edit → Apply pattern with undo support
├─ Inline suggestions (autocomplete)
│  ├─ Latency-critical → Use fastest model (Haiku-class)
│  ├─ UI pattern → Ghost text, accept with Tab, dismiss with Esc
│  └─ Trigger → Debounce input (300-500ms), cancel in-flight requests
├─ Data extraction / classification
│  ├─ Structured output with Zod schema validation
│  ├─ Batch processing → Queue + worker pattern
│  └─ Confidence scores → Include in schema, filter by threshold
├─ Search / Q&A over content
│  └─ RAG pattern (see ai-rag) + this skill for product integration
└─ Agent features (multi-step autonomous)
   └─ ai-agents for architecture, this skill for product UX integration
```

## Framework And Gateway Choice

The repo source list highlighted a practical split that belongs in this skill:

| Need | Default choice | Why |
|------|----------------|-----|
| Ship AI inside an existing app | Vercel AI SDK or direct provider SDK | Best fit for streaming UI, structured output, and product-owned flows |
| Embed a visible in-app copilot | CopilotKit | Useful when the product needs opinionated copilot UI primitives in React |
| Orchestrate long-running agent workflows | LangGraph or CrewAI | Use when the feature is truly workflow/agent shaped, not just one request/response UI |
| Centralize routing, logging, and provider policy | Portkey or a thin internal gateway | Best fit for multi-provider control planes and cross-feature governance |

Rules:

- Do not reach for LangGraph or CrewAI just because a feature uses a model. Most product AI flows are still request/response plus tools.
- Use a gateway only when multiple products, models, or policy layers need a shared control point.
- If the problem is agent architecture first, route to [ai-agents](../ai-agents/SKILL.md). If the implementation is specifically bots or LangGraph, use `ai-bot-builder`. If it is product integration first, stay here.

## Streaming Architecture

Never buffer a full LLM response and then send it. Always stream to the user.

- **Server-side**: use SDK streaming functions (`streamText`, `streamObject` in AI SDK, or native SDK streaming). Pipe the stream directly to the HTTP response as Server-Sent Events or a ReadableStream.
- **Client-side**: consume the ReadableStream, render text progressively as tokens arrive. For structured output, handle partial JSON gracefully — do not parse until a complete object boundary.
- **Error handling in streams**: the stream can error mid-response. Handle connection drops, timeouts, and model errors. Surface errors to the user inline (not as a separate error page). Provide a "retry" action that preserves conversation context.
- **Cancellation**: support "stop generating" — abort the fetch on the client, which should propagate to cancel the upstream API call. Do not charge for tokens you did not use.
- **Backpressure**: if the client cannot consume tokens fast enough (slow rendering, network congestion), the server should respect backpressure rather than buffering unboundedly.

## Structured Output Patterns

When you need the LLM to return data, not prose.

- **Structured output (strict/schema-constrained mode) vs. tool_use / function calling**: both achieve near-perfect schema adherence on current frontier-tier models, but they answer different questions. Use structured output when there is no decision to make — the model's terminal answer must simply match a shape (e.g., "extract these fields"). Use tool/function calling when the model must decide *whether and which* action to take, and the schema is the arguments to that action. Prefer either over legacy unconstrained JSON mode or regex-parsed prose — schema-constrained modes are the current baseline, not an upgrade path.
- **Zod schemas**: define your expected output shape with Zod. Use with AI SDK `generateObject` / `streamObject` for automatic validation. Zod gives you TypeScript types and runtime validation from one definition.
- **Fallback parsing**: for models that occasionally break schema, implement graceful fallback — attempt parse, if it fails try to extract partial data, log the failure for monitoring, and retry once with a more explicit prompt.
- **Discriminated unions**: when the AI can return different types of responses (e.g., "answer" vs. "clarification_needed" vs. "refused"), use discriminated union schemas. The `type` field tells your code which branch to handle.
- **Streaming structured output**: `streamObject` delivers partial objects as they generate. Use for progressive UI updates (show fields as they arrive), but validate the complete object before persisting.

## Conversation & Context Management

- **Message history storage**: store in a database, not just client state. Users expect conversations to persist across sessions and devices. Schema: `{ id, conversationId, role, content, toolCalls, toolResults, createdAt }`.
- **Context window management**: LLMs have finite context. Choose a strategy: sliding window (drop oldest messages), summarization (compress old messages into a summary), or hard truncation with a warning. Track token usage per conversation.
- **System prompts**: version them in code, do not hardcode strings. System prompts are product logic — they should go through code review, have tests, and be deployable independently when possible.
- **Multi-turn with tools**: when the model calls a tool, execute it and include the result in the message history. The model needs to see previous tool results to maintain coherent multi-step reasoning.
- **Conversation branching**: when a user "regenerates" a response, you are branching the conversation. Decide: replace the last message (simpler) or maintain a tree of branches (more flexible, more complex).

## Cost Control

| Control | Default rule |
|---------|-------------|
| Token estimation | Estimate input tokens before sending; warn or truncate at budget threshold; use tiktoken or provider tokenizer |
| Caching | Exact-match cache for deterministic queries; semantic cache (embeddings) for FAQ-style; set TTLs |
| Model routing | Haiku-class for classification/extraction/autocomplete; Sonnet/Opus-class for complex reasoning/long-form |
| Usage tracking | Track tokens per user, per feature, per model; budget alerts at 70% and 90% of monthly allocation |
| Rate limiting | Apply per user tier at the application layer; return clear error messages with upgrade paths |
| Prompt optimization | Audit system prompts for verbosity; measure quality vs. length trade-offs |

See [references/rollout-and-observability.md](references/rollout-and-observability.md) for cost dashboards, eval loops, and feature-flag rollout patterns.

### Worked example: is caching worth it?

Exact per-token prices change often — pull current numbers from the provider pricing page before using this in a real budget. The *method* below is what matters and stays stable: prompt caching only pays for itself once a cached prefix is reused enough times to amortize the cache-write premium.

Providers commonly price cache writes at a premium over a normal input token (e.g., roughly 1.25x for a short-TTL cache, ~2x for a longer-TTL cache) and cache reads at a steep discount off the normal input price (commonly ~0.1x, i.e. a ~90% discount). Given:

- `P` = normal input token price
- `w` = cache-write multiplier (e.g., 1.25)
- `r` = cache-read multiplier (e.g., 0.1)
- `N` = number of times the cached prefix is reused before it expires or changes

Break-even reuse count `N* = (w - r) / (1 - r)`. With `w = 1.25`, `r = 0.1`: `N* = 1.15 / 0.9 ≈ 1.28` — so caching a stable system prompt or long tool-definition block pays for itself after roughly the *second* reuse, not after dozens of reuses as intuition might suggest. This is why caching large, stable prefixes (system prompts, tool schemas, few-shot examples, retrieved document sets reused across a session) is close to a free win in most chat and agent architectures — the failure mode is forgetting to structure prompts so the stable part is a shared, byte-identical prefix, which breaks cache hits.

Apply the same break-even logic before adopting batch-API discounts (commonly ~50% off both directions) versus real-time calls: batch trades latency for cost, so it is only a substitute for interactive features, not a default.

## AI UX Patterns

| Pattern | Rule |
|---------|------|
| Loading states | Show tokens as they arrive; never buffer; streaming feels faster even at equal total time |
| Regenerate + stop | Always provide both controls — AI equivalents of "refresh" and "cancel" |
| Confidence | Label AI output; use qualifiers for uncertain responses; never present with same certainty as DB reads |
| Feedback | Thumbs up/down minimum; corrections more valuable; route both into eval pipelines |
| Graceful degradation | Core product must work when AI provider is down — cache, fallback, or queue |
| Attribution | Clearly label AI-generated content; Art. 50 EU AI Act requires disclosure for interactive systems |
| Undo / edit | Allow editing before AI output takes effect; require confirmation for destructive actions |

## Guardrails & Safety

| Layer | Rule |
|-------|------|
| Input | Enforce length limits; detect instruction-override patterns; sanitize before prompt injection |
| Output | Scan for PII (names, emails, SSNs); use moderation APIs (Anthropic, OpenAI, or Lakera) |
| High-stakes | Route medical/legal/financial AI output through human review; track review latency |
| Audit logging | Log prompts + responses separately from app logs; mask PII; set retention policy |
| Rate limiting | Rate limit to prevent abuse (injection attempts, data extraction) — beyond cost control |
| Fail closed | When guardrails timeout or fail, block the response and log; never pass unfiltered |

## Multi-Provider Strategy

Abstract provider calls behind a single `AIProvider` interface (AI SDK's provider pattern achieves this). Never swap models for all users at once — use feature flags and circuit breakers.

| Step | Implementation |
|------|---------------|
| Abstraction | `anthropic('<mid-tier-model-id>')` swappable for `openai('<comparable-tier-model-id>')` without changing call sites — resolve the exact current model IDs at each provider's docs at use-time, never hardcode a "best model" from memory |
| Fallback chain | Primary → fallback → degraded mode; circuit breaker after N failures in M seconds |
| Model variants | Maintain per-model prompt variants when quality differs; test before switching traffic |
| A/B rollout | Route % of traffic to new model; gate on user feedback, task completion, error rates |

See [references/rollout-and-observability.md](references/rollout-and-observability.md) for full rollout and eval loop patterns.

## Do / Avoid

| Do | Avoid |
|----|-------|
| Stream from first token — never buffer | Hardcoding system prompts as string literals |
| Store conversation history server-side in DB | Sending unbounded user input without token estimation |
| Version system prompts in code, treat as product logic | Treating AI provider uptime as guaranteed |
| Build cost tracking per user and per feature from day one | Logging full prompts/responses without PII and retention policy |
| Provide "regenerate", "stop generating", and "undo" on every AI output | Swapping models for all users at once without A/B gates |
| Clearly label AI-generated content for users and audit trails | Parsing LLM text with regex when tool_use/JSON mode is available |
| Test with mocked LLM responses (unit) and real calls (integration) | Ignoring thumbs-down/correction signals — route them to eval pipelines |
| Implement graceful degradation so core product works when AI is down | Building AI features without per-user rate limiting |
| Use tool_use/function calling for structured output | Buffering a full response before sending to the user |

## Known Traps

- Treating graceful degradation as a diagram-only requirement instead of proving the fallback path under real provider failure.
- Keeping conversation history only in browser or mobile client state, then discovering regeneration, resume, and support workflows have no canonical record.
- Assuming schema-shaped output is safe because the model usually behaves, without validating every response before persistence or side effects.
- Swapping models or providers behind the same endpoint without re-running prompt, latency, and evaluation gates.
- Capturing user feedback but never routing it into prompt, model, or retrieval evaluation loops.

## Common Anti-Patterns

| Anti-Pattern | Reason |
|---|---|
| Making the model call the core product workflow | Product loses ownership; the model becomes a single point of failure and a hard-to-audit orchestrator. |
| Trust tool outputs as instructions | Tool results are an indirect prompt injection vector. Attacker-controlled data returned by any tool can direct agent actions including destructive write and send operations. Always treat tool output as untrusted data; parse and validate before acting. |
| Hiding weak application contracts behind longer prompts | Prompt length does not fix broken validation, state, or orchestration — it hides it and makes it harder to debug. |
| Treating client-visible streaming as sufficient observability | No durable record of prompts, tool calls, or failures means incidents cannot be investigated or attributed. |
| Letting the AI path directly mutate durable product state | Without confirmation, undo, or compensating logic, a bad model output or injected instruction causes irreversible harm. |
| Expanding one AI service into a catch-all abstraction | Mixing routing, prompt logic, persistence, moderation, and analytics in one service eliminates clear ownership and makes the injection attack surface unbounded. |

## Scenarios

Recipes keyed to symptoms or integration moments. Each lists the shortest path to a working, production-safe implementation.

### S1 — Streaming chat with citations

1. Define the server endpoint using `streamText` (AI SDK) with the chosen provider.
2. Include a `citations` tool or instruct the model to embed `[source:N]` markers in prose.
3. Pipe the `ReadableStream` to the HTTP response as SSE; never buffer the full response.
4. On the client, use `useChat` to render tokens progressively; parse `[source:N]` markers into inline links.
5. Handle mid-stream errors with a visible inline retry control that preserves conversation context.
6. Log each completed turn with `{ conversationId, model, inputTokens, outputTokens, latencyMs }` for cost tracking.

### S2 — Structured extraction with Zod + retry-on-schema-fail

1. Define the target shape as a Zod schema; use `generateObject` (AI SDK) to bind schema to the model call.
2. On `ZodError`, log the raw response and retry once with a more explicit prompt that names the failing field.
3. Use discriminated unions (`{ type: "success" | "parse_error" | "refused" }`) to handle all branches.
4. Validate the complete object before any persistence or side-effect call.
5. Track schema-fail rate per endpoint; alert if it exceeds 1% — signals prompt drift or model regression.

### S3 — Tool-calling agent with indirect-prompt-injection guard

1. Define tools with minimal, read-only side effects; server owns writes, model only requests them.
2. Add an input-sanitization step: strip `\nAssistant:`, `\nHuman:`, and instruction-override patterns before injecting user input into prompts.
3. After each tool call, verify the returned result matches the declared tool schema before passing back to the model.
4. Audit-log every tool call with `{ tool, args, result, conversationId }` for post-incident tracing.
5. Add an output filter that refuses responses containing suspicious lateral instructions or role-change attempts.

### S4 — Multi-provider routing on rate-limit

1. Abstract provider calls behind a single `AIProvider` interface; swap implementations without changing call sites.
2. Implement a circuit breaker: after N `429` responses in M seconds, route to the fallback provider.
3. Maintain per-model prompt variants; run quality gates before switching traffic to an alternate model.
4. Alert on circuit-breaker activation; log which provider is active per request for cost attribution.
5. Add a `--dry-run` mode in staging that exercises the fallback path without real traffic.

### S5 — RAG with stale-cache invalidation

1. Cache retrieval results with a `content_hash` and `retrieved_at` timestamp in the cache key.
2. On each query, compare the source document's `updated_at` against cached `retrieved_at`; evict on mismatch.
3. Build a background job to re-index documents when source content changes; see [ai-rag](../ai-rag/SKILL.md) for chunking strategy.
4. Return `{ answer, sources[{ id, title, url, retrieved_at }] }` to the UI for attribution.
5. Track cache-hit rate and stale-eviction rate; tune TTL to balance freshness against provider cost.

## Navigation

### References
- [references/product-integration-patterns.md](references/product-integration-patterns.md) — streaming UX, structured output, persistence, and degraded-mode patterns
- [references/framework-and-gateway-patterns.md](references/framework-and-gateway-patterns.md) — app SDK vs copilot framework vs agent framework vs gateway choice
- [references/rollout-and-observability.md](references/rollout-and-observability.md) — cost controls, feature flags, evaluation loops, and operations
- [references/prompt-injection-and-ai-act.md](references/prompt-injection-and-ai-act.md) — direct/indirect prompt injection taxonomy, multi-hop agent attacks, defenses, model version pin strategy, and the full EU AI Act compliance treatment (obligation timeline, prohibited practices, provider/operator boundary, Article 50 disclosure, high-risk Annex III, Article 12 logging, enforcement and fines)
- [data/sources.json](data/sources.json) — official SDK, provider, and safety/eval sources

### Related Skills

- [ai-llm](../ai-llm/SKILL.md) — LLM lifecycle, fine-tuning, and deployment
- [ai-agents](../ai-agents/SKILL.md) — Agent system architecture and orchestration
- [ai-prompt-engineering](../ai-prompt-engineering/SKILL.md) — Prompt design techniques and patterns
- [ai-rag](../ai-rag/SKILL.md) — RAG system architecture and retrieval patterns
- [software-backend](../software-backend/SKILL.md) — Backend service patterns
- [software-frontend](../software-frontend/SKILL.md) — Frontend application development
- [software-realtime](../software-realtime/SKILL.md) — Real-time communication and streaming
- [software-security-appsec](../software-security-appsec/SKILL.md) — Application security and threat modeling

## Freshness Protocol

AI integration tooling changes rapidly. Freshness-check before answering questions about SDKs, model capabilities, or provider-specific patterns.

Triggers: SDK version questions, "is X still recommended?", streaming API changes, provider capability changes, new model releases.

Process: start from [data/sources.json](data/sources.json), run a targeted web search, check SDK changelogs (Vercel AI SDK, Anthropic SDK, and OpenAI SDK all release frequently with breaking changes).

## Regulatory Traps

*Verify current obligation timelines at official EU AI Act sources at use-time — the Digital Omnibus on AI (political agreement reached 7 May 2026, EU Parliament endorsed 16 June 2026, Council final sign-off 29 June 2026) pushed the Annex III high-risk deadline from 2 August 2026 to 2 December 2027; confirm formal Official Journal publication and effective date at eur-lex.europa.eu before relying on either date as of 2026-07-11.*

| Obligation | When it applies | Action |
|------------|-----------------|--------|
| Prohibited practices (Ch. II) | Any LLM feature using subliminal manipulation, social scoring, or real-time biometric ID in public | Remove before EU deployment (in force since 2 Feb 2025, unaffected by the Omnibus delay) |
| Transparency labelling (Art. 50) | Any system interacting with natural persons | Disclose AI nature; watermark generated images/audio/video — **not delayed by the Omnibus**, still targeted for 2 August 2026 (existing systems get a watermarking grace period to ~Dec 2026 per the agreed text; verify final text) |
| High-risk classification (Annex III) | Employment screening, credit scoring, biometric ID, education gating, essential-services access | Conformity assessment + human oversight — deadline **deferred to 2 December 2027** under the Digital Omnibus (was 2 August 2026); do not assume the old date without checking final publication |
| Operator obligations | Deploying a third-party GPAI model for a specific purpose | Document purpose, implement usage policies, retain logs |
| GPAI systemic risk (Arts. 51–56) | Building on any GPAI model whose provider discloses ≥10^25 training FLOPs (rebuttable presumption, not automatic) | Technical documentation, copyright compliance, training data summaries; do not assume any single named model is or isn't in scope — check the provider's published systemic-risk designation |
| Enforcement | Prohibited-practice violations | Fines up to €35M or 7% of global turnover |

**Indirect prompt injection** is the primary exploit path: attacker-controlled data in retrieved documents, tool outputs, or web results overrides system instructions. Mitigations: isolate retrieved content with structural tags, enforce least-privilege tool scopes, validate model output before write/send operations, and test with adversarial documents in CI. Defense must be architectural — model-side mitigations reduce but do not eliminate risk.

See [references/prompt-injection-and-ai-act.md](references/prompt-injection-and-ai-act.md) for full obligation timelines and injection defence patterns.

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Use web search/web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

