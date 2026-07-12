---
name: routerbase-model-routing
description: Choose RouterBase model IDs and routing strategies for chat, image, video, audio, and embeddings workloads. Use when comparing providers, selecting GPT, Claude, Gemini, image, video, or audio models on RouterBase, designing fallback paths, checking pricing or availability, planning cost/latency/quality tradeoffs, querying the RouterBase Models API, or documenting how an app should route model requests through RouterBase.
---

# RouterBase Model Routing

## Overview

Use [routerbase](https://routerbase.com) to pick and document model choices behind one API key and one OpenAI-compatible integration surface. This skill helps agents turn workload requirements into a practical model shortlist, fallback plan, and validation checklist.

Read `references/routerbase-models.md` when exact catalog API calls, model examples, or selection heuristics are needed.

## Routing Workflow

1. Classify the task modality: chat, image, video, audio, embeddings, or mixed.
2. Identify hard constraints: quality target, latency budget, price ceiling, context length, tool calling, vision, JSON mode, region/compliance needs, and fallback tolerance.
3. Query the live RouterBase catalog when possible:

```bash
curl "https://routerbase.com/api/v1/models?task=chat" \
  -H "Authorization: Bearer $ROUTERBASE_API_KEY"
```

4. Shortlist one primary model and one or two fallback models. Prefer fallbacks with the same modality and similar capability shape.
5. Check current pricing before final recommendations:

```bash
curl "https://routerbase.com/api/v1/pricing" \
  -H "Authorization: Bearer $ROUTERBASE_API_KEY"
```

6. Document the decision as a table: use case, primary model, fallback model, reason, validation test, and known caveats.

## Selection Heuristics

- For general chat, prefer a balanced fast model first, then escalate only when reasoning quality or context length requires it.
- For high-stakes reasoning, choose a flagship model and require human review of outputs.
- For latency-sensitive UX, prefer smaller or flash-tier models and keep prompts compact.
- For tool-heavy agents, choose chat models documented to support tool calling and test the exact tool schema.
- For JSON outputs, use `response_format` where the selected model supports JSON mode, and add schema validation in application code.
- For prompt caching benefits, place stable system prompts, policies, and tool definitions before variable user content.
- For media workflows, keep routing separate by modality; image, video, and audio endpoints have different sync/async behavior.

## Fallback Design

Use explicit application-level fallback logic unless the user has configured RouterBase's smart routing in their account or upstream settings.

```js
const modelPlan = [
  "anthropic/claude-sonnet-4-6",
  "google/gemini-2.5-flash",
];

for (const model of modelPlan) {
  try {
    return await client.chat.completions.create({ model, messages });
  } catch (error) {
    if (!isRetryableRouterBaseError(error)) throw error;
  }
}
```

Classify retryable errors conservatively: transient network failures, timeouts, `429`, and `5xx` are reasonable candidates; auth errors, invalid model IDs, validation errors, and policy errors should not be retried blindly.

## Recommendation Format

When recommending a routing plan, include:

- Primary model and why it fits.
- Fallback model and what tradeoff it makes.
- Current catalog/pricing check status.
- Any feature assumptions that must be tested, such as tool calling, vision, JSON mode, context size, prompt caching, or streaming.
- A minimal eval prompt or request fixture the user can run before production.

Avoid pretending prices or supported model IDs are permanent. RouterBase's docs explicitly describe the model and pricing catalog as changing with upstream providers.
