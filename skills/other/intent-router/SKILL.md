---
name: intent-router
description: >
  Classify the information-need of a query and dispatch it to the
  appropriate retrieval or reasoning strategy. Use before read-side
  memory access, before multi-strategy retrieval, or any time you'd
  otherwise default to "one retriever for everything". Returns a
  strategy label, a token budget, and a retrieval depth so downstream
  handlers can be specialised. Backed by Pre-Route (arxiv 2605.10235v2)
  and MemFlow (arxiv 2605.03312v1), which together show LLMs possess
  latent routing ability elicitable via a structured prompt — and that
  externalising the routing decision improves small-model performance
  by ~2x. Triggers: "route this", "what strategy", "before retrieving",
  "intent classification", or any query whose ideal handling depends on
  what KIND of question it is.
user-invocable: true
version: 1.0.2
format: 2025-10-02
triggers:
  - "route this query"
  - "what retrieval strategy"
  - "what reasoning strategy"
  - "intent classification before retrieval"
  - "front-run the memory access"
updated: 2026-05-16
status: ACTIVE
source: arxiv 2605.10235v2 (Pre-Route), 2605.03312v1 (MemFlow)
---

# Intent Router

## Why

The 2026 frontier converges on one architectural shift: **route → strategy → act**, replacing the historical *one-retriever-for-everything* pattern. Different query intents demand categorically different handlers:

- **lookup** — direct factual recall, single retrieval, small budget
- **multi-hop** — chain through intermediate facts, deeper retrieval, larger budget
- **global** — summarise/aggregate across a broad slice, retrieve broadly + compress
- **verification** — check a claim against evidence, retrieve narrowly + compare
- **deep-reason** — escalate to a higher-tier model, retrieve generously, allow chain-of-thought
- **lexical** — exact-match / keyword (BM25 territory), no embedding, narrow budget

The empirical claim: a single fixed strategy is dominated on every axis by the conditional strategy.

## How

Before any memory access or multi-strategy retrieval, run a structured-prompt classification pass that returns:

```json
{
  "strategy": "lookup|multi-hop|global|verification|deep-reason|lexical",
  "token_budget": 2000,
  "retrieval_depth": 5,
  "refinement_policy": "none|verbal-rerank|consensus-check",
  "confidence": 0.0
}
```

If confidence < 0.6, fall back to the broadest strategy (`global`) so the system degrades gracefully rather than mis-routing.

### Output format vs confidence

The full JSON envelope is the canonical form when downstream consumers read it programmatically (typed pipelines, gating code). For inline human-facing routing decisions, taper the ceremony to match the confidence:

- **confidence ≥ 0.9** — emit just the strategy label on one line (e.g., `route: lexical`). The other fields default; don't print the envelope.
- **0.6 ≤ confidence < 0.9** — emit the strategy + 1-line rationale. Skip the JSON.
- **confidence < 0.6** — emit the full JSON envelope with the `global` fallback explicit. This is the only case where the structured output earns its tokens.

Rationale: a CTA audit (`.planning/patterns/skill-audits/intent-router-2026-05-16.md`) found that high-confidence lexical-class probes produced full JSON envelopes that downstream consumers did not read. The output was surface-anchoring without information gain.

## When to skip

- You're already in a typed pipeline whose strategy is fixed (e.g., a search command that's explicitly lexical).
- The query is short enough that the routing call costs more than it saves (rule of thumb: < 20 tokens of question text).
- **Scoped exact-match lookup in a known directory** — the surface form is so cleanly lexical that classification cannot change the outcome. Triggers: "find files in `src/X/` that contain literal string `Y`", "grep for `Z` under `path/`", "list all files referencing `IDENT`". The routing decision is structurally pinned to `lexical`; just `grep`. Added 2026-05-16 from CTA audit (`.planning/patterns/skill-audits/intent-router-2026-05-16.md`) — the bounded probe showed the routing ceremony added overhead without changing the action.
- You're in a streaming/interactive context where added latency dominates the routing payoff.

## Integration

- `wrap:execute` and `wrap:verify` — invoke intent-router as the FIRST step in handler dispatch.
- `gsd-graphify` — already does query routing internally; intent-router exposes the same primitive uniformly to other skills.
- Future `src/memory/strategies/` directory will be the typed substrate; this skill is the policy on top.

## Cross-references

- Rosetta concept #7 (Intent Routing) — canonical definition
- College: `agent-systems / agent-memory / agent-intent-routing`
- Related skills: `graphify` (when query is graph-shaped), `gsd-explore` (when intent is exploratory)
