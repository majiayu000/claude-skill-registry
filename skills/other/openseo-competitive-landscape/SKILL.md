---
name: openseo-competitive-landscape
description: >-
  Map who is winning an SEO market with measured data — recurring SERP
  domains, organic footprints, winning content themes, backlink authority,
  and the gaps worth attacking. Use this skill for market-level questions
  ("who ranks for X", "how competitive is this space", "where are the SEO
  openings") before committing to keyword targets or content themes. For one
  named competitor, use openseo-competitor-analysis instead. Triggers:
  "competitive landscape seo", "who ranks for", "seo market map", "how
  competitive is", "serp competitors".
category: seo
tier: nice-to-have
layer: strategy
reads:
  - brand/landscape.md
  - brand/competitors.md
writes:
  - brand/landscape.md
env_vars:
  - OPENSEO_API_KEY
  - OPENSEO_MCP_URL
triggers:
  - competitive landscape seo
  - who ranks for
  - seo market map
  - how competitive is
  - serp competitors
allowed-tools:
  - Bash(mktg catalog *)
  - Bash(mktg run *)
---

# OpenSEO Competitive Landscape

Answer with measured data: who is winning this SEO market, what content works for them, and where the openings are. Findings update `brand/landscape.md` (mktg's market memory) with an evidence tier mktg's `landscape-scan` cannot reach alone.

## On Activation

1. **Readiness + binding**: `mktg seo status --json --fields readiness,catalog.endpointError,project`. `not_configured` → fall back to `landscape-scan` (Exa qualitative) and label authority/metrics `unknown`. For a ready state, verify live access with the free `whoami` MCP tool before paid calls.
2. **Brand grounding**: read `brand/landscape.md` + `brand/competitors.md` (tolerate templates) — known competitors seed the query set; positioning filters "SEO competitor" from "business competitor."

## OpenSEO MCP Tools

- `research_keywords` + `get_keyword_metrics`: build + validate a 5–10 query market set (mixed intent: informational, commercial, comparison, tool terms).
- `find_serp_competitors`: recurring domains across the keyword set at scale — use before manual SERP counting.
- `get_serp_results`: inspect live SERP composition/features (≤10 queries per call).
- `get_domain_overview`: organic footprint for top 3–5 recurring domains.
- `get_ranked_keywords`: exact ranking keywords/URLs/intents for leaders.
- `get_backlinks_overview`: authority comparison where rankings look authority-driven (may be unavailable on some accounts — continue without it).
- `get_backlinks_profile`: sampled link-level evidence for leaders when overview totals are too coarse; record scope, filters, and pagination.
- `get_search_console_performance`: when the user's own domain is compared and GSC is connected, anchor THEIR side with first-party data instead of third-party estimates.

## Workflow

1. Define the market query set (positioning-filtered, mixed intent).
2. `find_serp_competitors` for recurring domains; `get_keyword_metrics` to validate demand/difficulty.
3. Group recurring domains by type: direct product competitors, publishers/media, marketplaces/directories, communities/forums, docs/resources.
4. `get_domain_overview` top 3–5; `get_ranked_keywords` for direct competitors + relevant publishers; `get_backlinks_overview` where authority explains wins.
5. Synthesize: winning content types, SERP formats, authority advantages, underserved angles.
6. Update `brand/landscape.md`: leaders, winnable area, biggest barrier, query set used, content formats that work, keyword/theme gaps — dated, with the measured-vs-estimate caveat.
7. Recommend next: `openseo-competitor-analysis` (one domain), `openseo-keyword-clustering` (page mapping), or `seo-content`.

## Output Format

| Domain | Type | Why they matter | Organic footprint | Winning themes | Weakness/gap |
| ------ | ---- | --------------- | ----------------- | -------------- | ------------ |

## Anti-Patterns

- **Treating business competitors as SEO competitors** — because the company that competes for customers often isn't who competes for SERPs (publishers and directories win informational queries). Label domain types; never merge the lists.
- **Quoting estimate numbers as exact traffic** — because third-party organic estimates can be off by multiples, and a plan built on fake precision breaks on contact with reality. Say "estimate" or "directional."
- **Small query sets presented as market truth** — because 4 queries is a peek, not a map. Call small-set results directional and say what would confirm them.
- **Stopping at "X is winning" without the why** — because a leader list with no content-theme or authority explanation gives the user nothing to act on. Every leader gets a "why they win" and a "where they're weak."
- **Abandoning the analysis when backlinks are unavailable** — because SERP + domain evidence still answers "who and what." Degrade gracefully and name the missing tier.

## Close the loop

After writing files, log completion so `mktg plan` / `mktg status` count the work (bare `mktg run` only logs `loaded`):

```bash
mktg run openseo-competitive-landscape --complete --writes <paths written> --result success --json
```


---

*Adapted from [every-app/open-seo](https://github.com/every-app/open-seo) `.agents/skills/competitive-landscape` (MIT). Workflow upstream; mktg brand-memory writes and fallback wiring added here.*
