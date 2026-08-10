---
name: ai-deep-research
description: "Builds repeatable deep-research workflows for verified synthesis. Use when producing evidence-backed briefs, comparisons, dossiers, or research pipelines."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Deep Research

Use this skill to design and run repeatable research workflows that gather evidence across many sources, preserve provenance, and synthesize results into decision-ready outputs.

This skill covers both **native deep-research agents** (ChatGPT Deep Research, Gemini Deep Research, Perplexity Deep Research, Claude with web search) and **custom agentic research pipelines** (planner / searcher / verifier / synthesizer split).

## ASCII Flow

```text
research question
  |
  v
research plan
  scope + source targets + queries + stop criteria + freshness window
  |
  v
evidence gathering
  primary sources first + source ledger + hostile-source checks
  |
  v
verification
  isolated verifier checks claims against ledger, not researcher context
  |
  v
synthesis
  evidence-tiered answer + citations + contradictions + unknowns
```

## Quick Reference

| Question | Default |
|----------|---------|
| When to use a native agent vs custom pipeline? | Native for ad-hoc, open-ended questions. Custom for repeatable, auditable, or multi-source workflows. |
| What is the first artifact of any research task? | The source ledger — never the synthesis. |
| When is a source trustworthy? | When it is a primary document with a stable URL, author attribution, and a verifiable date. |
| What stops an unbounded research loop? | An explicit stop criterion defined before the loop starts (saturation condition or max iterations). |
| How to handle contradictory sources? | Separate them into evidence tiers; do not resolve by averaging. |

## Use This Skill When

- You need to produce a sourced comparison, brief, memo, or research dossier.
- You need to choose between a native deep-research agent and a custom pipeline.
- You want to build a repeatable, auditable research workflow with provenance.
- You need to detect hostile sources, citation laundering, or model-output-as-source.
- You need to run a verifier subagent that has not seen the researcher's context.

## Do Not Use This Skill For

- Single-lookup current facts — use ordinary browsing or direct tools.
- Long-lived retrieval serving — use [ai-rag](../ai-rag/SKILL.md).
- Local note-vault packaging — use [docs-notes-retrieval](../docs-notes-retrieval/SKILL.md).

## Current Stance

The durable pattern is not "send a single query and summarize the top results."

The default architecture (as of last_validated date above):

1. **Plan before searching**: emit a structured research plan with queries, source targets, and success criteria before any tool call.
2. **Ledger as contract**: the source ledger is the primary artifact — synthesis is derived from it, not the other way around.
3. **Verifier isolation**: the verifier subagent must not share context with the researcher — it reads only the ledger and checks claims independently.
4. **Evidence tier separation**: primary sources (original docs, filings, specs) are never mixed with secondary commentary or model-generated summaries in the same evidence bucket.
5. **Saturation-first synthesis**: synthesize only after the research loop has reached saturation (new queries return no novel facts), not on a time budget.
6. **Freshness windows are explicit**: every claim in the final output carries a date anchor and a freshness class (stable / volatile / unknown).
7. **Hostile source detection is mandatory for public-web research**: adversarial SEO, AI-generated content farms, and citation-laundering chains are real threats.

## Patterns

Full catalog → [references/patterns-catalog.md](references/patterns-catalog.md)

| ID | Name | When to reach for it |
|----|------|----------------------|
| P1 | Source-ledger-as-contract | Always — every research task |
| P2 | Plan-then-execute loop | Multi-query or multi-source tasks |
| P3 | Multi-agent research swarm | Large corpora with parallel query paths |
| P4 | Verifier subagent | Any claim that will reach a user or decision |
| P5 | Freshness-window sourcing | Time-sensitive domains (AI, market, regulatory) |
| P6 | Evidence-tier separation | When primary and secondary sources both exist |
| P7 | Citation back-pointer | Every synthesis sentence that makes a factual claim |
| P8 | Stop-criterion-as-eval | To prevent unbounded research loops |
| P9 | Hostile-source detection | Public-web research, vendor comparisons |
| P10 | Synthesis-after-saturation | All multi-pass research tasks |

## Anti-Patterns

Full catalog → [references/anti-patterns-catalog.md](references/anti-patterns-catalog.md)

| ID | Name | Why it matters |
|----|------|----------------|
| A1 | Pre-synthesizing the answer | Frames all subsequent evidence gathering; produces confirmation bias |
| A2 | Single-pass search | Misses contradictions, minority sources, and laterally relevant evidence |
| A3 | Mixing evidence tiers | Primary docs and blog summaries in the same bucket degrade citation quality |
| A4 | Model-output-as-source | LLM summaries carry hallucination risk; they are working notes, not source truth |
| A5 | Unbounded research loop | Without a stop criterion, cost and time grow unboundedly with no quality signal |
| A6 | Citation laundering | Citing a secondary article that in turn cites the primary — provenance chain breaks |
| A7 | Verifier-with-same-context | Verifier that read the same sources as researcher adds no independence |
| A8 | Vague consensus language | "Multiple sources say" without naming them is unfalsifiable |
| A9 | Date-free volatile claims | Time-sensitive facts without date anchors decay silently |
| A10 | Retrofitting citations | Writing first, citing later consistently inflates confidence in unsupported claims |
| A11 | Overweighting recency | Newest is not most authoritative — prefer canonical primary sources |
| A12 | Storing evidence with synthesis | Mixed buckets cause RAG follow-on to cite derived text as original evidence |

## Decision Matrix: Native Agent vs Custom Pipeline

See full decision guide → [references/native-deep-research-agents.md](references/native-deep-research-agents.md)

| Criterion | Native agent | Custom pipeline |
|-----------|-------------|-----------------|
| Setup time | Minutes | Hours to days |
| Auditability | Limited (opaque search path) | Full (ledger + traces) |
| Repeatability | Low (non-deterministic) | High (seeded, logged) |
| Source control | None | Full |
| Freshness control | Model-dependent | Explicit per query |
| Multi-step planning | Implicit | Explicit (P2) |
| Verifier isolation | Not available | P4 |
| Cost predictability | Low | High |
| Best for | Ad-hoc exploration, open questions, competitive overview | Repeatable workflows, regulated outputs, source-auditable deliverables |

**Decision rule:** choose a native agent when speed matters and provenance does not. Choose a custom pipeline when the output will be cited, published, used in a product, or needs to be reproduced.

### Native agents comparison

Full table with API surfaces and citation fidelity → [references/native-deep-research-agents.md](references/native-deep-research-agents.md)

| Agent | API model ID / tool | Strengths | Limitations |
|-------|---------------------|-----------|-------------|
| ChatGPT Deep Research (OpenAI) | `o3-deep-research` (depth) / `o4-mini-deep-research` (speed/cost) — Responses API | Strongest source diversity, long synthesis, strong multi-step reasoning (RL-post-trained) | **Sunset scheduled 2026-07-23** (recommended replacement: `gpt-5.5-pro`) — verify at `developers.openai.com/api/docs/deprecations` before starting new work, the feature guide page does not surface this. Slow (5–30 min), opaque search log, citations can go stale |
| Gemini Deep Research (Google) | `deep-research-preview-04-2026` / `deep-research-max-preview-04-2026` (Interactions API) | Explicit plan review before execution, Google index, async + streaming, MCP support | Preview model IDs include date suffix — will change; thinner synthesis depth than ChatGPT DR |
| Perplexity Deep Research | `sonar-deep-research` (Chat Completions API) | Fastest (2–5 min), paragraph-level inline citations, real-time index | Citation laundering risk on SEO topics; shorter synthesis; model averages contradictions rather than flagging; multi-component pricing makes budgeting error-prone |
| Claude with web search | `web_search_20260318` (current: adds response-inclusion control) / `web_search_20260209` (dynamic filtering, GA) / `web_search_20250305` (basic) | Full tool-call audit trail, structured output, P2/P4 composable, memory-tool-backed persistence | No dedicated DR mode; needs P2 loop for DR-equivalent depth |
| Grok DeepSearch (xAI) | `web_search` / `x_search` server-side tools (documented at `docs.x.ai`) | Only agent with X/Twitter as a primary indexed source; now has a documented, API-invocable tool surface | No dedicated report-generating deep-research model or endpoint comparable to the other four; citation auditability less mature |

## Architecture, Workflow, and Contracts

Full depth — planner / searcher / verifier / synthesizer subagent split, canonical contract shapes (`ResearchPlan`, `SourceLedger`, `EvidenceTier`, `VerifierReport`, `SynthesisArtifact`), stop-criterion design, freshness window classes — in [references/agentic-research-loop-architecture.md](references/agentic-research-loop-architecture.md).

### Default Workflow

1. Frame the research question narrowly enough to be falsifiable.
2. Emit a structured research plan — see [assets/templates/research-plan.template.md](assets/templates/research-plan.template.md).
3. Execute the planner/searcher loop; record every source in the ledger before any synthesis.
4. Run the verifier subagent (must not share context with the searcher).
5. Separate evidence tiers: primary, secondary, and model-working-notes.
6. Check freshness windows; date-stamp all volatile claims.
7. Synthesize into the requested artifact; every factual claim carries a citation back-pointer.
8. Archive the ledger separately — see [assets/templates/source-ledger.template.md](assets/templates/source-ledger.template.md).

## Known Traps

| Trap | Resolution |
|------|-----------|
| Starting with synthesis and backfilling sources | Freeze the ledger first; emit no synthesis until the ledger passes a minimum source count and verifier check |
| Using model outputs as sources in the next research pass | Stamp working notes with `tier: model-output`; the verifier rejects them as primary evidence |
| Verifier reads the same context as researcher | Give the verifier only the ledger JSONL, not the search session |
| Research loop never terminates | Define the stop criterion in the plan: saturation (no novel facts in N iterations) or hard cap (M total queries) |
| Citation laundering through secondary articles | Trace every citation to its primary document; reject chains longer than two hops |
| Mixing old and new evidence for fast-moving topics | Apply P5 freshness-window sourcing; reject sources older than the window for volatile claims |
| Hostile SEO sources polluting vendor comparisons | Apply P9 hostile-source detection before adding any URL to the ledger |
| S2S session-state loss on agentic research re-runs | Persist the ledger and plan to disk before each iteration; resume from ledger state, not from conversation context |
| Trusting a vendor's feature guide as the source of truth for model availability | A provider's "how to use X" guide and its deprecations/sunset page are maintained on different cadences and can disagree — the guide may still recommend a model days before its documented shutdown. Check the deprecations page separately before wiring a pipeline to any specific model ID |

## Navigation

### References

- [references/patterns-catalog.md](references/patterns-catalog.md) — P1–P10 named patterns
- [references/anti-patterns-catalog.md](references/anti-patterns-catalog.md) — A1–A12 with detection signals
- [references/native-deep-research-agents.md](references/native-deep-research-agents.md) — Comparison table, ChatGPT DR, Gemini DR, Perplexity DR, xAI Grok DeepSearch, Claude with web search, Anthropic memory tool, URL-health recipe
- [references/agentic-research-loop-architecture.md](references/agentic-research-loop-architecture.md) — Planner / searcher / verifier / synthesizer subagent split
- [references/research-workflow.md](references/research-workflow.md) — Staged research loop and source-plan design
- [references/evidence-packaging.md](references/evidence-packaging.md) — Provenance, citation, and synthesis-packaging rules

### Assets / Templates

- [assets/templates/research-plan.template.md](assets/templates/research-plan.template.md) — Research plan scaffold
- [assets/templates/source-ledger.template.md](assets/templates/source-ledger.template.md) — Source ledger scaffold

### Scripts

- `python3 scripts/citation_verifier.py --input claims.jsonl` — Checks JSONL of {claim, source_url, supporting_quote} and reports unsupported claims

### Data

- [data/sources.json](data/sources.json) — Curated source repos and tool references

## Related Skills

- [../ai-rag/SKILL.md](../ai-rag/SKILL.md) — Retrieval architecture and serving indexes
- [../docs-notes-retrieval/SKILL.md](../docs-notes-retrieval/SKILL.md) — Local note-vault packaging
- [../agents-mcp/SKILL.md](../agents-mcp/SKILL.md) — MCP search, docs, and memory tool surfaces
- [../qa-agent-testing/SKILL.md](../qa-agent-testing/SKILL.md) — Eval harnesses for productized research workflows
- [../ai-agents/SKILL.md](../ai-agents/SKILL.md) — Agent architecture (planner/searcher/verifier split)

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Start from `data/sources.json` for workflow and tool references.
- Verify native deep-research agent capabilities and output formats before recommending them for specific use cases — features change frequently.
- Check the provider's **deprecations/sunset page**, not just its feature guide, before committing a pipeline to a specific model ID — the two pages update on different cadences and the guide can lag behind an already-announced shutdown by days or weeks.
- If live verification is unavailable, mark native-agent capability claims as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
