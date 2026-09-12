---
name: openseo-competitor-analysis
description: >-
  Deep-dive ONE competitor's organic footprint — exact ranking keywords and
  URLs, content themes, backlink profile, and exploitable gaps — with
  findings written into brand/competitors.md. Use this skill when the user
  names a competitor and wants to know what to learn from them, counter, or
  outrank, including head-to-head comparisons against the user's own domain.
  For market-level mapping first, use openseo-competitive-landscape.
  Triggers: "analyze competitor", "competitor keywords", "competitor
  backlinks", "beat <competitor>", "competitor seo teardown".
category: seo
tier: nice-to-have
layer: strategy
reads:
  - brand/competitors.md
  - brand/positioning.md
writes:
  - brand/competitors.md
env_vars:
  - OPENSEO_API_KEY
  - OPENSEO_MCP_URL
triggers:
  - analyze competitor
  - competitor keywords
  - competitor backlinks
  - beat competitor
  - competitor seo teardown
allowed-tools:
  - Bash(mktg catalog *)
  - Bash(mktg run *)
---

# OpenSEO Competitor Analysis

Analyze one competitor deeply enough to decide what to learn from, avoid, counter-position against, or outrank. Findings merge into `brand/competitors.md` — mktg's competitor memory that `competitive-intel` maintains qualitatively and this skill now grounds in measured rows.

## On Activation

1. **Readiness + binding**: `mktg seo status --json --fields readiness,catalog.endpointError,project`. `not_configured` → hand off to `competitive-intel` (Exa qualitative), labeling metrics `unknown`. For a ready state, verify live access with the free `whoami` MCP tool before paid calls.
2. **Brand grounding**: read `brand/competitors.md` + `brand/positioning.md` (tolerate templates). If the competitor isn't named, ask — never guess the domain.

## OpenSEO MCP Tools

- `get_domain_overview`: baseline organic traffic + keyword count (both domains when comparing).
- `get_ranked_keywords`: exact keyword/URL/rank/intent/traffic rows. Use `maxRank`, `minSearchVolume`, `excludeBrandTerms`, `resultTypes` filters to keep rows relevant.
- `get_backlinks_overview`: backlink/referring-domain profile (may be unavailable — continue without it).
- `get_backlinks_profile`: link-level sources, anchors, authority/spam signals, and lost/broken state when the decision needs more than a summary. Preserve target scope and pagination.
- `find_serp_competitors`: validate the named competitor actually overlaps in search.
- `get_serp_results`: head-to-head SERP checks for the important shared terms.
- `get_search_console_performance`: when comparing to the user's domain and GSC is connected, the USER's baseline is first-party — never estimate your own side from third-party data.
- `research_keywords`: expand gap terms.

## Workflow

1. `get_domain_overview` for the competitor (and the user's domain when comparing).
2. `get_ranked_keywords` for the competitor with sensible filters; same for the user, or `get_serp_results` for shared terms when a lighter check suffices.
3. `find_serp_competitors` when the supplied competitor's search overlap is unclear.
4. Group keywords into themes: product/category, alternatives/comparisons, templates/tools, educational guides, branded demand.
5. `get_backlinks_overview` when authority appears to explain rankings.
6. `get_serp_results` for the important head-to-head terms.
7. Synthesize the plan: what they do well, where they're vulnerable, which pages/keywords to pursue, what NOT to copy.
8. Merge into `brand/competitors.md` (preserve existing sections; date the entry; confirm before overwriting populated competitor entries).
9. Hand off: `competitor-alternatives` for "X vs Y" pages, `seo-content` for gap-driven briefs, `openseo-keyword-clustering` for page mapping.

## Output Format

Start with: snapshot, biggest lesson, best opportunity to beat them. Then:

| Area | Competitor pattern | Evidence | OpenSEO opportunity |
| ---- | ------------------ | -------- | ------------------- |

## Anti-Patterns

- **Treating every competitor keyword as desirable** — because ranking for a term and PROFITING from a term are different things; filter through positioning before anything lands in a plan.
- **Inferring page-level content strategy from keyword rows alone** — because a keyword list can't tell you WHY a page works (structure, depth, format). Use SERP/web evidence for page-level claims.
- **Estimating the user's own performance from third-party data when GSC exists** — because first-party clicks/impressions/position are free and exact; third-party estimates of your own site are the worst data in the room.
- **Recommending "copy what they do"** — because imitation pages lose to the original on authority and freshness. Recommend a stronger angle on the same intent, never a replica.
- **Separating evidence from inference nowhere** — because "they rank for X" (evidence) and "their content strategy is Y" (inference) carry different confidence and must read differently in `brand/competitors.md`.

## Close the loop

After writing files, log completion so `mktg plan` / `mktg status` count the work (bare `mktg run` only logs `loaded`):

```bash
mktg run openseo-competitor-analysis --complete --writes <paths written> --result success --json
```


---

*Adapted from [every-app/open-seo](https://github.com/every-app/open-seo) `.agents/skills/competitor-analysis` (MIT). Workflow upstream; mktg brand-memory writes and handoff wiring added here.*
