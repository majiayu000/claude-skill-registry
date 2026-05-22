---
name: api-ai-litellm
description: LiteLLM proxy server setup, TypeScript client patterns via OpenAI SDK, model routing, fallbacks, load balancing, spend tracking, virtual keys, and production deployment
---

# LiteLLM Proxy Patterns

> **Quick Guide:** LiteLLM is an OpenAI-compatible proxy (AI gateway) that routes requests to 100+ LLM providers. TypeScript clients connect via the standard OpenAI SDK with `baseURL` pointed at the proxy. Configure models, fallbacks, load balancing, and budgets in `config.yaml`. Use `provider/model-name` format in `litellm_params.model` (e.g., `anthropic/claude-sonnet-4-20250514`). The `model_name` in config is the user-facing alias clients request. Virtual keys require PostgreSQL. Master key must start with `sk-`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the `provider/model-name` format in `litellm_params.model` -- e.g., `anthropic/claude-sonnet-4-20250514`, `openai/gpt-4o`, `azure/my-deployment` -- the provider prefix is how LiteLLM routes to the correct API)**

**(You MUST set `model_name` as the user-facing alias that clients request -- this is NOT the provider model ID, it is the name your TypeScript client passes as `model`)**

**(You MUST point the OpenAI SDK `baseURL` at the proxy URL (e.g., `http://localhost:4000`) and pass the proxy key as `apiKey` -- do NOT use provider API keys directly in client code)**

**(You MUST start master keys with `sk-` -- LiteLLM rejects master keys that do not follow this prefix convention)**

**(You MUST configure `database_url` pointing to PostgreSQL before using virtual keys, spend tracking, or team/user management -- these features require persistent storage)**

</critical_requirements>

---

**Auto-detection:** LiteLLM, litellm, litellm_params, litellm_settings, LLM proxy, LLM gateway, model_list, master_key, virtual keys, model fallback, load balancing LLM, provider/model, anthropic/claude, openai/gpt, azure/, litellm --config, LITELLM_MASTER_KEY, LITELLM_SALT_KEY

**When to use:**

- Running a unified LLM gateway that routes to multiple providers (OpenAI, Anthropic, Azure, Bedrock, etc.)
- Configuring model fallbacks, load balancing, or routing strategies across deployments
- Managing API key access with virtual keys, per-key budgets, and rate limits
- Tracking spend across models, teams, users, and tags
- Deploying a self-hosted OpenAI-compatible proxy with Docker

**Key patterns covered:**

- Proxy server config.yaml structure (model_list, litellm_settings, router_settings, general_settings)
- TypeScript client setup via OpenAI SDK pointed at proxy
- Model routing with provider prefixes and user-facing aliases
- Fallback chains (regular, context window, content policy, default)
- Load balancing strategies (simple-shuffle, least-busy, usage-based, latency-based, cost-based)
- Virtual keys with budgets, rate limits, and model restrictions
- Spend tracking per key, user, team, and tag
- Docker Compose production deployment

**When NOT to use:**

- Calling a single LLM provider directly with no proxy layer -- use the provider's SDK directly
- Building a Python application that calls LiteLLM as a library -- this skill covers the proxy server + TypeScript client pattern
- When you need React-specific chat UI hooks -- use a framework-integrated AI SDK

---

## Examples Index

- [Core: Config & Client Setup](examples/core.md) -- config.yaml structure, TypeScript OpenAI SDK client, model routing, Docker deployment
- [Routing & Reliability](examples/routing.md) -- Fallbacks, load balancing, cooldowns, retries, priority routing
- [Keys & Spend](examples/keys-and-spend.md) -- Virtual keys, budgets, rate limits, spend tracking, team management

---

<philosophy>

## Philosophy

LiteLLM Proxy is an **AI gateway** -- a single OpenAI-compatible endpoint that routes to 100+ LLM providers. TypeScript applications never talk to providers directly; they talk to the proxy using the standard OpenAI SDK.

**Core principles:**

1. **Provider abstraction** -- Client code uses a single `baseURL` and standard OpenAI SDK. Switching providers means changing `config.yaml`, not application code.
2. **Two-layer naming** -- `model_name` is what clients request (e.g., `"claude-sonnet"`). `litellm_params.model` is the actual provider routing (e.g., `"anthropic/claude-sonnet-4-20250514"`). This decouples client code from provider specifics.
3. **Resilience via config** -- Fallbacks, retries, load balancing, and cooldowns are all declared in `config.yaml`. No application-level retry logic needed.
4. **Spend governance** -- Virtual keys, per-key budgets, rate limits, and tag-based tracking give fine-grained cost control without changing client code.
5. **OpenAI compatibility** -- Any client, SDK, or tool that works with OpenAI's API works with LiteLLM. No custom SDK required.

**When to use LiteLLM Proxy:**

- You call multiple LLM providers and want a single API surface
- You need centralized spend tracking, budgets, and rate limiting
- You want model fallbacks and load balancing without client-side logic
- You need to distribute virtual API keys to teams with per-key controls

**When NOT to use:**

- Single-provider apps with no need for routing, budgets, or fallbacks -- use the provider SDK directly
- Python-only applications -- consider using LiteLLM as a library instead of a proxy
- You need sub-millisecond latency -- the proxy adds a network hop

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Minimal config.yaml

The proxy needs a `config.yaml` with at least one model defined. `model_name` is client-facing; `litellm_params.model` is the provider route.

```yaml
# config.yaml
model_list:
  - model_name: claude-sonnet # What clients request
    litellm_params:
      model: anthropic/claude-sonnet-4-20250514 # Provider/model route
      api_key: os.environ/ANTHROPIC_API_KEY # Never hardcode keys

  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
```

**Why good:** Two-layer naming decouples clients from providers, `os.environ/` syntax reads secrets from environment at runtime

```yaml
# BAD: Missing provider prefix, hardcoded key
model_list:
  - model_name: claude-sonnet-4-20250514 # Using provider model ID as name
    litellm_params:
      model: claude-sonnet-4-20250514 # No provider prefix -- routing fails
      api_key: sk-ant-abc123 # Hardcoded API key
```

**Why bad:** Without `anthropic/` prefix, LiteLLM cannot route to the correct provider; hardcoded keys are a security risk; using the provider model ID as `model_name` couples clients to provider naming

**See:** [examples/core.md](examples/core.md) for complete config with general_settings, Docker setup

---

### Pattern 2: TypeScript Client via OpenAI SDK

Connect to the proxy using the standard OpenAI SDK. Point `baseURL` at the proxy, use the proxy key as `apiKey`.

```typescript
// lib/llm-client.ts
import OpenAI from "openai";

const PROXY_URL = "http://localhost:4000";

const client = new OpenAI({
  baseURL: PROXY_URL,
  apiKey: process.env.LITELLM_API_KEY, // Virtual key or master key
});

export { client };
```

```typescript
// usage.ts
import { client } from "./lib/llm-client.js";

const completion = await client.chat.completions.create({
  model: "claude-sonnet", // model_name from config.yaml, NOT provider model ID
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Explain TypeScript generics." },
  ],
});

console.log(completion.choices[0].message.content);
```

**Why good:** Standard OpenAI SDK, no custom dependencies; model name matches config.yaml `model_name`; proxy key keeps provider keys server-side

```typescript
// BAD: Using provider model ID, provider API key
const client = new OpenAI({
  baseURL: "http://localhost:4000",
  apiKey: process.env.ANTHROPIC_API_KEY, // Wrong -- use proxy key
});

const completion = await client.chat.completions.create({
  model: "anthropic/claude-sonnet-4-20250514", // Wrong -- use model_name alias
  messages: [{ role: "user", content: "Hello" }],
});
```

**Why bad:** Provider API key bypasses proxy auth and virtual key controls; using provider model ID instead of alias couples client to provider naming and bypasses proxy routing logic

**See:** [examples/core.md](examples/core.md) for streaming, metadata tagging

---

### Pattern 3: Fallback Chains

Configure model fallbacks so requests automatically retry on a different model when the primary fails.

```yaml
# config.yaml
model_list:
  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-sonnet-4-20250514
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY

litellm_settings:
  num_retries: 2 # Retries per model before fallback
  fallbacks: [{ "claude-sonnet": ["gpt-4o"] }] # General fallback chain
  context_window_fallbacks: [{ "gpt-4o": ["claude-sonnet"] }] # Context overflow fallback
  default_fallbacks: ["gpt-4o"] # Catch-all for any model failure
```

**Why good:** Fallbacks use `model_name` aliases (not provider IDs), ordered chains tried sequentially, separate chains for context overflow vs general errors

**See:** [examples/routing.md](examples/routing.md) for content policy fallbacks, combining with load balancing

---

### Pattern 4: Load Balancing Across Deployments

Multiple entries with the same `model_name` create a load-balanced group. The proxy distributes requests using the configured strategy.

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: azure/gpt-4o-eastus
      api_base: https://eastus.openai.azure.com/
      api_key: os.environ/AZURE_EASTUS_KEY
      rpm: 100 # Requests per minute for this deployment

  - model_name: gpt-4o
    litellm_params:
      model: azure/gpt-4o-westus
      api_base: https://westus.openai.azure.com/
      api_key: os.environ/AZURE_WESTUS_KEY
      rpm: 100

router_settings:
  routing_strategy: usage-based-routing # Route to deployment with lowest RPM/TPM usage
  num_retries: 2
  timeout: 30
```

**Why good:** Same `model_name` across entries creates automatic load balancing, `rpm`/`tpm` limits per deployment enable usage-aware routing

**See:** [examples/routing.md](examples/routing.md) for all five routing strategies, priority routing with `order`

---

### Pattern 5: Virtual Keys with Budgets

Virtual keys let you distribute access with per-key budgets, rate limits, and model restrictions. Requires PostgreSQL.

```yaml
# config.yaml
general_settings:
  master_key: sk-litellm-master-key-change-me # Must start with sk-
  database_url: os.environ/DATABASE_URL # PostgreSQL required
```

```bash
# Generate a virtual key via API
curl 'http://localhost:4000/key/generate' \
  -H 'Authorization: Bearer sk-litellm-master-key-change-me' \
  -H 'Content-Type: application/json' \
  -d '{
    "models": ["claude-sonnet", "gpt-4o"],
    "max_budget": 50.0,
    "duration": "30d",
    "metadata": {"team": "backend", "project": "search"}
  }'
# Returns: { "key": "sk-generated-key-abc123", ... }
```

**Why good:** Per-key model restrictions, budget caps, and expiry; metadata enables tag-based spend tracking; master key authentication protects key generation

**See:** [examples/keys-and-spend.md](examples/keys-and-spend.md) for team management, spend queries, rate limit tiers

---

### Pattern 6: Spend Tracking with Tags

Attach metadata tags to requests for granular cost attribution. The proxy tracks spend automatically per key, user, team, and tag.

```typescript
// Tag requests for cost attribution
const completion = await client.chat.completions.create({
  model: "claude-sonnet",
  messages: [{ role: "user", content: "Summarize this document." }],
  // LiteLLM-specific: pass metadata for spend tracking
  metadata: {
    tags: ["project:search", "team:backend"],
    trace_user_id: "user-123",
  },
} as any); // metadata is a LiteLLM extension, not in OpenAI types
```

**Why good:** Tags enable cost attribution by project, team, or feature without changing model routing; cost appears in `x-litellm-response-cost` response header

**When to use:** When you need cost visibility across teams, projects, or features

**See:** [examples/keys-and-spend.md](examples/keys-and-spend.md) for querying spend by tag, user, and team

</patterns>

---

<decision_framework>

## Decision Framework

### Do You Need a Proxy?

```
Do you call multiple LLM providers?
+-- YES -> LiteLLM Proxy adds value (unified API, routing, fallbacks)
+-- NO -> Do you need budgets, rate limits, or virtual keys?
    +-- YES -> LiteLLM Proxy (governance layer)
    +-- NO -> Do you need fallbacks or load balancing?
        +-- YES -> LiteLLM Proxy (reliability layer)
        +-- NO -> Use the provider SDK directly (simpler)
```

### Which Routing Strategy?

```
What is your priority?
+-- Even distribution      -> simple-shuffle (default)
+-- Minimize latency       -> latency-based-routing
+-- Respect rate limits     -> usage-based-routing
+-- Minimize cost           -> cost-based-routing
+-- Handle concurrent load  -> least-busy
```

### Virtual Keys vs Master Key Only

```
Do you have multiple teams or users?
+-- YES -> Virtual keys (per-team budgets, model restrictions)
|   Requires: PostgreSQL database
+-- NO -> Do you need spend tracking?
    +-- YES -> Virtual keys (even for single user, enables spend logs)
    |   Requires: PostgreSQL database
    +-- NO -> Master key only (simplest setup, no database needed)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Missing provider prefix in `litellm_params.model` (e.g., `claude-sonnet-4-20250514` instead of `anthropic/claude-sonnet-4-20250514`) -- proxy cannot route without the prefix
- Hardcoding provider API keys in config.yaml instead of using `os.environ/VAR_NAME` -- security breach risk
- Using provider model IDs as `model_name` -- couples all clients to provider naming, breaks when you switch providers
- Master key not starting with `sk-` -- LiteLLM silently rejects it
- Using virtual keys without a PostgreSQL `database_url` -- key generation fails

**Medium Priority Issues:**

- Not setting `num_retries` in `litellm_settings` -- defaults to 0, no retries on transient failures
- Confusing `model_name` (client-facing alias) with `litellm_params.model` (provider route) -- most common config mistake
- Not setting `rpm`/`tpm` on deployments when using `usage-based-routing` -- routing strategy has no data to work with
- Missing `LITELLM_SALT_KEY` in production -- virtual key credentials stored without encryption

**Common Mistakes:**

- Passing `anthropic/claude-sonnet-4-20250514` as the `model` parameter in TypeScript client code -- use the `model_name` alias instead
- Expecting `metadata` field to be typed in OpenAI SDK -- it is a LiteLLM extension, requires `as any` or `extra_body`
- Setting fallbacks using provider model IDs instead of `model_name` aliases -- fallbacks reference model names, not provider routes
- Forgetting that `config.yaml` changes require proxy restart (or use the `/config/update` API endpoint)

**Gotchas & Edge Cases:**

- The `os.environ/` syntax in config.yaml (no `$` prefix) is LiteLLM-specific -- not standard YAML environment variable substitution
- `model_name` matching is exact -- `"claude-sonnet"` and `"Claude-Sonnet"` are different models
- When using `default_fallbacks`, they do NOT apply to `ContentPolicyViolationError` or `ContextWindowExceededError` -- use specialized fallback types for those
- The proxy adds a network hop -- expect 5-20ms additional latency compared to direct provider calls
- `rpm`/`tpm` limits in config are per-deployment, not per-model-group -- a model group with 3 deployments at `rpm: 100` each gets 300 RPM total
- Virtual key spend tracking is eventually consistent -- the `spend` field on a key may lag a few seconds behind actual usage
- The `/v1/` prefix on endpoints is optional -- both `http://localhost:4000/chat/completions` and `http://localhost:4000/v1/chat/completions` work
- Streaming through the proxy works transparently -- no special configuration needed on the proxy side
- The LiteLLM admin UI is available at `http://localhost:4000/ui` when the proxy is running

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the `provider/model-name` format in `litellm_params.model` -- e.g., `anthropic/claude-sonnet-4-20250514`, `openai/gpt-4o`, `azure/my-deployment` -- the provider prefix is how LiteLLM routes to the correct API)**

**(You MUST set `model_name` as the user-facing alias that clients request -- this is NOT the provider model ID, it is the name your TypeScript client passes as `model`)**

**(You MUST point the OpenAI SDK `baseURL` at the proxy URL (e.g., `http://localhost:4000`) and pass the proxy key as `apiKey` -- do NOT use provider API keys directly in client code)**

**(You MUST start master keys with `sk-` -- LiteLLM rejects master keys that do not follow this prefix convention)**

**(You MUST configure `database_url` pointing to PostgreSQL before using virtual keys, spend tracking, or team/user management -- these features require persistent storage)**

**Failure to follow these rules will produce misconfigured proxies with broken routing, security issues, or missing spend data.**

</critical_reminders>
