---
name: openseo-keyword-research
description: >-
  Discover keyword opportunities with MEASURED volume, keyword difficulty,
  CPC, and intent from OpenSEO, then write them into brand/keyword-plan.md.
  Use this skill whenever someone asks for keyword difficulty, KD, search
  volume, keyword ideas with metrics, striking-distance opportunities from
  Search Console, or SERP-validated keyword priorities. For qualitative
  research without an OpenSEO connection, use mktg's keyword-research
  instead (metrics will be unknown). Triggers: "keyword difficulty",
  "search volume", "keyword opportunities", "striking distance keywords",
  "measured keyword research".
category: seo
tier: nice-to-have
layer: strategy
reads:
  - brand/keyword-plan.md
  - brand/positioning.md
writes:
  - brand/keyword-plan.md
env_vars:
  - OPENSEO_API_KEY
  - OPENSEO_MCP_URL
triggers:
  - keyword difficulty
  - search volume
  - keyword opportunities
  - striking distance keywords
  - measured keyword research
allowed-tools:
  - Bash(mktg catalog *)
  - Bash(mktg run *)
---

# OpenSEO Keyword Research

Turn seed topics into a prioritized, MEASURED keyword opportunity set and land it in `brand/keyword-plan.md`. mktg's `keyword-research` is the playbook (methodology); this skill is the measured-data engine behind it when OpenSEO is configured.

## On Activation

1. **Readiness check**: `mktg seo status --json --fields readiness,catalog.endpointError,project` — if readiness is `not_configured`, stop spending: state the gap and hand off to Exa-backed `keyword-research` with metrics marked `unknown`. For a ready state, verify live access with the free `whoami` MCP tool before paid calls.
2. **Project binding**: read `.seo/openseo.json` for `projectId`. Missing → run `openseo-project-setup` first (or ask the user for the project id).
3. **Brand grounding**: read `brand/positioning.md` + existing `brand/keyword-plan.md` (tolerate templates). Business-fit beats volume-fit — the positioning file is the filter.

## OpenSEO MCP Tools

- `get_search_console_performance`: when GSC is connected, START here. High `rowLimit`, filter average position ~5–20 client-side (the API sorts by clicks, not position). These striking-distance terms are the fastest wins — and zero extra credit cost.
- `get_keyword_metrics`: hydrate up to 700 keywords per call with volume, KD, intent, CPC, trends. Use on striking-distance terms and every candidate set.
- `research_keywords`: discovery from 1–5 seeds per call; prefer ~150 results unless exhaustive research was requested.
- `get_ranked_keywords`: when the brief includes a domain/page — exact ranking rows (near-misses, competitor-owned terms).
- `get_serp_results`: inspect SERPs for top candidates when intent is ambiguous. Keep batches small (≤10 queries).
- `list_saved_keywords`: avoid re-researching what's already saved.
- `save_keywords`: a free shared-state mutation. Use only after confirmation, with concise tags (`topic:<t>`, `intent:<i>`, `page:<slug>`).

## Workflow

1. Normalize seeds into 2–5 distinct research angles filtered by positioning.
2. GSC connected? Pull striking-distance terms first and hydrate with `get_keyword_metrics`. Work that list before broad discovery.
3. `research_keywords` per angle; `get_keyword_metrics` to hydrate; `get_ranked_keywords` if a domain is in the brief.
4. Remove irrelevant, duplicate, branded-only, and off-intent terms.
5. Prioritize by practical opportunity: business fit → clear intent → reasonable KD → volume/CPC signal → winnable SERP.
6. `get_serp_results` for high-potential or ambiguous terms when SERP intent would change the call.
7. Write the shortlist into `brand/keyword-plan.md` (preserve its required sections per `brand/SCHEMA.md`; confirm before overwriting populated sections).
8. Present: best opportunity theme, top keywords now, keywords to save, SERP caveats. Then next actions: `openseo-keyword-clustering`, `seo-content`, or save.

## Cost Discipline

- State estimated call counts before bulk pulls (>200 keywords) and get confirmation.
- Small exploratory batches are fine without asking.
- GSC-first ordering exists precisely to avoid spending credits on data the user already owns.

## Anti-Patterns

- **Inventing metrics when OpenSEO returns nothing** — because a hallucinated KD of "about 35" silently becomes the foundation of a content plan. If OpenSEO doesn't return a value, write `unknown`.
- **Volume-first prioritization** — because a 10k-volume term that doesn't match the product converts nobody and burns months. Positioning filters the list before metrics rank it.
- **`save_keywords` without explicit confirmation** — saves do not burn provider credit, but they mutate shared OpenSEO account state and broad tags can disrupt other workflows. Ask, state the count and tag change, then save.
- **Skipping the GSC-first pass when GSC is connected** — because striking-distance terms (positions 5–20) are provably the cheapest wins in SEO and they're free to read. Discovery research before first-party data is wasted spend.
- **Overwriting a populated `keyword-plan.md` without confirmation** — because that file is brand memory other skills build on (`seo-content`, `seo-machine`). Merge; confirm destructive rewrites.

## Close the loop

After writing files, log completion so `mktg plan` / `mktg status` count the work (bare `mktg run` only logs `loaded`):

```bash
mktg run openseo-keyword-research --complete --writes <paths written> --result success --json
```

## Progressive Enhancement

| Level | Behavior |
|---|---|
| L0 (no OpenSEO) | Hand off to Exa-backed `keyword-research`; metrics `unknown` |
| L1 (`OPENSEO_API_KEY`) | Metrics via available calls; MCP steps deferred |
| L2 (MCP connected) | Full workflow incl. SERP validation |
| L3 (GSC connected) | Striking-distance-first ordering; highest-signal path |

---

*Adapted from [every-app/open-seo](https://github.com/every-app/open-seo) `.agents/skills/keyword-research` (MIT). Workflow and tool guidance upstream; mktg brand-memory writes, positioning filter, and cost discipline added here.*
