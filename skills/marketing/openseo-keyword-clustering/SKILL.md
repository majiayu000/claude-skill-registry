---
name: openseo-keyword-clustering
description: >-
  Cluster keywords by search intent and map each cluster to an existing or
  proposed page, with cannibalization detection from Search Console. Use this
  skill when the user has a keyword list (saved set, brand/keyword-plan.md,
  GSC export, or seed topic) and needs page targets, content briefs, or a
  site map for SEO pages — especially before seo-content or seo-machine page
  generation. Triggers: "cluster keywords", "keyword mapping", "map keywords
  to pages", "keyword cannibalization", "which page should target".
category: seo
tier: nice-to-have
layer: strategy
reads:
  - brand/keyword-plan.md
writes:
  - brand/keyword-plan.md
env_vars:
  - OPENSEO_API_KEY
  - OPENSEO_MCP_URL
triggers:
  - cluster keywords
  - keyword mapping
  - map keywords to pages
  - keyword cannibalization
  - which page should target
allowed-tools:
  - Bash(mktg catalog *)
  - Bash(mktg run *)
---

# OpenSEO Keyword Clustering

Group keywords into page-level clusters and assign each to an existing URL, a new page proposal, or a do-not-target bucket. Output lands in `marketing/seo/clusters/*.md` (per-cluster briefs) and feeds `seo-content` / `seo-machine` with measured page targets.

## On Activation

1. **Readiness + binding**: `mktg seo status --json --fields readiness,catalog.endpointError,project`. No binding → `openseo-project-setup` first. `not_configured` → do lexical clustering with Exa context but label every cluster "SERP-unvalidated." For a ready state, verify live access with the free `whoami` MCP tool before paid calls.
2. **Keyword source**: prefer (a) `brand/keyword-plan.md` populated sections, (b) `list_saved_keywords` with a tag, (c) GSC live data, (d) seed discovery via `research_keywords`. Under 10 usable terms → simple map, no clustering ceremony.

## OpenSEO MCP Tools

- `get_search_console_performance` with `dimensions: ["query","page"]`: the cannibalization truth source — one query splitting impressions across multiple URLs means existing cannibalization, not theoretical risk.
- `get_ranked_keywords`: domain/page-driven clustering from exact ranking rows + URLs.
- `get_serp_results`: SERP-overlap validation for borderline terms (small batches, ≤10).
- `list_saved_keywords` / `research_keywords`: source sets.
- `save_keywords`: apply cluster tags ONLY after confirmation.

## Workflow

1. Assemble the candidate set from the source hierarchy above; dedupe and drop off-strategy terms.
2. Cluster by intent and page type: same SERP intent + similar ranking pages belong together; different intent/buyer stage/SERP format splits. Lexical similarity is NOT evidence of same-page fit.
3. Borderline terms: small `get_serp_results` overlap check.
4. Assign each cluster: existing URL (if supplied and fitting), new-page proposal, or do-not-target/later.
5. Cannibalization check: GSC query+page data first; otherwise flag where two proposed pages share one intent.
6. Write per-cluster briefs to `marketing/seo/clusters/<cluster-slug>.md`: page type, searcher problem, required sections, internal-link targets, priority.
7. Optionally tag clusters with `save_keywords` after confirmation.
8. Hand off: `seo-content` for single pages, `seo-machine` for programmatic batches — both now have measured targets instead of vibes.

## Output Format

Summary first: cluster count, pages to create, pages to update, cannibalization issues. Then:

| Cluster | Primary keyword | Secondary keywords | Intent | Target page | Priority | Notes |
| ------- | --------------- | ------------------ | ------ | ----------- | -------- | ----- |

## Anti-Patterns

- **Clustering by word similarity alone** — because "best crm for dentists" and "crm pricing dentists" share words but not intent, and forcing them onto one page guarantees neither ranks. SERP intent wins; check overlap when unsure.
- **Clustering tiny sets** — because 6 keywords don't need a clustering framework, they need a paragraph. Under 10 terms, write a simple map.
- **Theoretical cannibalization warnings without data** — because crying cannibalization on every overlapping term freezes page production; GSC query+page splits are the only proof. No GSC → label it "potential," not "confirmed."
- **Retagging saved keywords without confirmation** — because tags are shared account state; a bulk retag can destroy someone else's organization. Confirm first.
- **Producing clusters with no page assignment** — because a cluster without a target page is trivia. Every cluster ends in an existing URL, a new proposal, or an explicit do-not-target decision.

## Close the loop

After writing files, log completion so `mktg plan` / `mktg status` count the work (bare `mktg run` only logs `loaded`):

```bash
mktg run openseo-keyword-clustering --complete --writes <paths written> --result success --json
```


---

*Adapted from [every-app/open-seo](https://github.com/every-app/open-seo) `.agents/skills/keyword-clustering` (MIT). Workflow upstream; mktg artifact paths, brand-memory reads, and handoff wiring added here.*
