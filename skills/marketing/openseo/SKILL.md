---
name: openseo
description: >-
  Uses OpenSEO as the measured SEO data plane for keyword volume and difficulty,
  SERPs, ranked keywords, backlinks, local SEO, rank tracking, Search Console,
  GA4, and site audits. Use for measured SEO metrics, indexing evidence,
  organic analytics, local rankings, backlink profiles, or rank trackers.
  Prefer OpenSEO over guessed metrics when connected; otherwise continue with
  qualitative web research and mark numeric metrics unknown.
category: seo
tier: nice-to-have
layer: strategy
reads:
  - brand/keyword-plan.md
writes:
  - brand/keyword-plan.md
  - brand/learnings.md
env_vars:
  - OPENSEO_API_KEY
  - OPENSEO_MCP_URL
triggers:
  - keyword difficulty
  - search volume
  - serp results
  - ranked keywords
  - backlinks
  - rank tracker
  - gsc performance
allowed-tools:
  - Bash(mktg catalog *)
  - Bash(mktg doctor *)
  - Bash(mktg seo *)
  - Bash(mktg run *)
---

# OpenSEO — Measured SEO Data Plane

OpenSEO supplies evidence; mktg skills supply methodology. Communicate only through OpenSEO's MCP-over-HTTP endpoint. There is no general OpenSEO REST research API, and mktg never calls DataForSEO directly.

## On Activation

1. Run `mktg seo status --json --fields readiness,catalog,project,bindingCorrupt,state`.
2. Interpret readiness:
   - `hosted_oauth_ready`: agent MCP client is authenticated interactively.
   - `hosted_api_key_ready`: headless hosted MCP can use `OPENSEO_API_KEY`.
   - `selfhost_ready`: bound/connected non-hosted MCP endpoint; local Docker HTTP is allowed only on loopback.
   - `not_configured`: continue through Exa/crawl/manual evidence and label KD, volume, CPC, authority, and rank `unknown`.
3. Read `.seo/openseo.json`. If absent and project-scoped tools are needed, use `openseo-project-setup`.
4. Read `get_project_context` before rebuying research. Use its research log to identify still-fresh evidence.
5. Select only the tools needed from the [v0.1.6 tool map](references/tools-v0.1.6.md).

## Authentication

- Root `.mcp.json` intentionally declares the hosted URL without a bearer header so MCP clients can perform OpenSEO OAuth.
- Headless clients may add `Authorization: Bearer ${OPENSEO_API_KEY}` or `x-api-key: ${OPENSEO_API_KEY}` in their private client config. Never write a key value into the repository.
- `OPENSEO_MCP_URL` overrides the endpoint for self-hosting. Hosted default is `https://app.openseo.so/mcp`.
- `mktg catalog info openseo` reports **headless API-key readiness**; `mktg seo status` distinguishes OAuth, API key, and self-host modes.

## Route Evidence, Do Not Duplicate Playbooks

| Need | OpenSEO evidence | mktg owner |
|---|---|---|
| Keyword demand/opportunity | keyword research, metrics, ranked terms, GSC | `openseo-keyword-research` |
| Page mapping/cannibalization | query+page GSC, SERPs, ranked URLs | `openseo-keyword-clustering` |
| Market/competitor | SERP competitors, domain/ranked terms, backlink profiles | competitive OpenSEO skills |
| Technical/indexing | site audit, URL inspection, GSC | `seo-audit` |
| Local visibility | business, local SERP, reviews, categories, rank grid | `seo-audit` with local mode/brief |
| Organic outcomes | GA4 landing/page/event/acquisition/opportunity tools | `seo-audit`, `seo-content`, `seo-machine` |
| AEO hypotheses | SERP, index, audit, backlink, GSC, GA4 evidence only | `ai-seo` owns direct answer-engine observations |

## Cost and Mutation Policy

Before a paid batch, state the exact tool(s), item counts, requested limits, and cost shape. OpenSEO's server requests confirmation above its large-credit threshold, but mktg still asks whenever the planned spend is material or recurring.

Separate **spend** from **mutation**:

- `whoami`, project/context reads, saved-keyword reads, GSC, and GA4 are free reads.
- `save_keywords`, `create_project`, tags, and `update_project_context` mutate shared account state but do not themselves consume DataForSEO credits; confirm broad/destructive changes.
- research, SERP, backlinks, local SEO, site audit, and rank runs may consume credits.
- scheduled rank tracking requires `estimate_rank_tracker_cost`, explicit approval, and the approved credit ceiling passed to the write/run call.

## State Contract

| Evidence | Local contract |
|---|---|
| project/domain/MCP URL | `.seo/openseo.json` |
| keyword transfer | `.seo/keywords-sync.json` → `mktg seo sync-keywords --confirm` |
| rank observations | `.seo/rank-snapshots/<date>.json` |
| backlinks | `.seo/backlinks/<date>.json` with target scope, pagination, and provider limits |
| GSC / GA4 exports | `.seo/gsc/`, `.seo/ga4/` when a file snapshot is needed |
| site audits | `.seo/audits/<audit-id>.json` plus summary |

OpenSEO remains the measurement backend; `brand/` and the active playbook tracker remain mktg's decision memory.

## Anti-Patterns

- **Inventing REST endpoints** — upstream automation is MCP-over-HTTP; guessed REST paths fail and misstate the security boundary.
- **Treating `configured: false` as proof OAuth is disconnected** — catalog readiness is headless env readiness; `mktg seo status` owns the richer truth.
- **Calling DataForSEO directly** — this bypasses OpenSEO's project, usage, and cost controls.
- **Calling free account mutations “paid research”** — spend and shared-state risk need different approvals.
- **Saving only backlink totals** — scope (`exact`, `subfolder`, `domain`, `subdomains`), pagination, and provider limitations determine what totals mean.
- **Claiming OpenSEO MCP measures AI answers** — v0.1.6 has no AI Visibility MCP tools. Use `ai-seo` direct observations and OpenSEO supporting evidence.

## Progressive Enhancement

| Level | Behavior |
|---|---|
| L0 | Qualitative web/manual evidence; metrics `unknown`. |
| L1 | Hosted OAuth or API key exposes measured MCP tools. |
| L2 | Bound project/context avoids duplicate spend and enables GSC/GA4. |
| L3 | Synced snapshots feed mktg playbooks and long-arc trackers. |

After writing artifacts, log completion with `mktg run openseo --complete --writes <paths> --result success --json`.

---

OpenSEO integration targets [every-app/open-seo](https://github.com/every-app/open-seo) v0.1.6 over an MIT-safe HTTP/MCP boundary.
