---
name: kai-seo-audit
description: One-click technical SEO audit of a website. Runs the full technical SEO audit SOP — crawlability, indexation, Core Web Vitals, schema markup, internal linking, mobile UX, and content quality. Outputs a prioritized fix list. Use when "SEO audit", "technical SEO", "site audit", "crawl issues", "indexation problems", "why aren't we ranking", "SEO health check", or any request to diagnose SEO issues on a website.
---

# /kai-seo-audit — Prioritized Technical Fix List

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

## Objective

A client-facing audit of one site in which every finding is traceable to a retrieved artifact, ordered so the reader knows what to fix first and what it costs. The deliverable states its audit mode, carries a health score computed only from observed checks, lists P0 through P3 fixes with pages affected, and names the access or exports that would remove the remaining uncertainty.

An audit whose numbers cannot be traced back to a collector run is worse than no audit — it moves budget on invented evidence.

## Done when

Work type `audit-report` — floor **E3/C4/O1** (`harness/eco-floors.yaml`).

- **E3** — a named human approved the exact delivered file, hash-pinned, and every quantitative claim in it resolves to a collector source in `workspace/seo-audit/`.
- **C4** — the Kai Data Provenance Rule is satisfied: collector run before writing, mode declared, a collector source cited for every number, missing data in `_data-gaps.md`. `banned_word_check` and `audit_provenance_lint` both pass.
- **O1** — every P0 recommendation names the metric it targets, with a baseline, a threshold, and an owner. Adoption and effect are read at 60 days.

```bash
python scripts/quality_gates/audit_provenance_lint.py workspace/seo-audit --audit-dir
```

## Constraints

**Kai Data Provenance Rule (non-negotiable).** Load `harness/references/audit-data-provenance.md` before writing any finding. Declare one mode:

- `sales_external` — public-only or prospect audits.
- `onboarding_connected` — GSC, GA4, GBP, crawl exports, or SEO platform data are connected.
- `internal_demo` — values are placeholders and labeled as such.

Run the collector before writing. It is shared by all Kai workflows, not audit-only; this audit consumes the `audit-data.json` alias. Existing audit automations may keep using `python -m scripts.audit.collect`; non-audit SEO workflows should prefer `python -m kai.source_data.collect` and read `kai-data.json`.

```bash
python -m scripts.audit.collect --url "<url>" --mode sales_external --workflow seo-audit --out workspace/seo-audit --pagespeed --dataforseo --seo-provider auto --keywords "<kw1>,<kw2>" --location "<city, state>"
```

```bash
python -m scripts.audit.collect --url "<url>" --mode onboarding_connected --workflow seo-audit --out workspace/seo-audit --pagespeed --places --dataforseo --seo-provider auto --gsc --ga4 --keywords "<kw1>,<kw2>" --location "<city, state>" --date-from "<YYYY-MM-DD>" --date-to "<YYYY-MM-DD>"
```

Add `--third-party-sources serpapi,brightlocal,similarweb,builtwith,wappalyzer,bing-webmaster` when licensed vendor or non-Google search data is needed. API vendor values are `third_party_estimate`; supplied exports are `user_provided`.

- **Never publish without source, retrieval date, and artifact/API note:** rankings, traffic, clicks, CTR, Core Web Vitals, PageSpeed, indexed-page counts, backlinks, Domain Rating, AI Overview visibility, schema validity, local pack placement. If the metric is absent from `workspace/seo-audit/audit-data.json`, it is a data gap, not an estimate.
- **Every check carries source metadata:**

```yaml
source_tier: connected | public_observed | user_provided | inferred | missing_data
source_name: ""
source_url: ""
retrieved_at: ""
evidence_artifact: ""
confidence: high | medium | low
score_eligible: true | false
```

- **`inferred` and `missing_data` items are excluded from the health score.**
- **Agent-readiness gate.** Site-level SEO/AEO work audits the domain against `knowledge/checklists/agent-readiness-checklist.md` before recommending outbound work; run `python scripts/quality_gates/agent_readiness_lint.py https://<domain>`. Any P0 failure blocks the plan. Treat `llms.txt` as useful for cooperative agents, not a Google AI Overview ranking requirement.
- **Read `MARKETING.md` from the project root before asking the user anything.** If it does not exist, build it from the codebase — README, manifests, landing pages, route files, analytics and email config — and confirm the draft.
- **No live mutation.** The audit recommends; it does not change robots.txt, sitemaps, tags, or redirects.

**Priority scoring** — the impact/effort matrix that orders the fix list:

| Priority | Impact | Effort | Examples |
|---|---|---|---|
| **P0** | High | < 1 hour | Missing title tags, broken canonical, noindex on important pages |
| **P1** | High | 1 day | CWV failures, redirect chains, thin content |
| **P2** | Medium | 1 week | Schema markup, internal linking optimization |
| **P3** | Low / nice-to-have | Ongoing | Alt text gaps, URL cleanup |

## Context

Six things must be known before the audit is scoped: the URL, the scope (full site or sections), any known issues already flagged, whether Search Console and analytics access exists, what matters most (rankings, traffic, indexation, speed), and which data sources are available — public crawl, PageSpeed Insights, DataForSEO, Ahrefs/Semrush/Moz, GSC, GA4, GBP, Screaming Frog/Sitebulb export. `MARKETING.md` answers most of them.

| Need | Load |
|---|---|
| Audit procedure and coverage | `knowledge/checklists/technical-seo-audit-sop.md` |
| Technical check detail | `knowledge/checklists/technical-seo-checklist.md` |
| SEO validation rules | `knowledge/checklists/seo-checklist.md` |
| Provenance modes, source tiers, data-gap handling | `harness/references/audit-data-provenance.md` |
| Agent legibility rubric | `knowledge/checklists/agent-readiness-checklist.md` |
| Indexation troubleshooting | `harness/references/google-indexation-monitoring.md` |
| Product, ICP, current channels | `MARKETING.md` (project root) |

**Audit layers** — the coverage the report must account for, each finding either observed or logged as a gap:

1. **Crawlability & indexation** — robots.txt blocks, XML sitemap presence/submission/freshness, canonical correctness and consistency, unintended noindex/nofollow, HTTP status codes (404s, redirect chains, 5xx), pagination handling.
2. **Technical performance** — Core Web Vitals (LCP, INP, CLS), mobile-friendliness, server response time and render-blocking resources, HTTPS mixed content and certificates, structured data presence and validity.
3. **On-page** — title tags (unique, keyword-included, under 60 chars), meta descriptions (unique, under 155 chars), one relevant H1 per page, descriptive image alt text, internal linking (orphan pages, link depth), URL structure.
4. **Content quality** — thin pages under 300 words, internal and external duplication, keyword cannibalization, freshness/last-updated, E-E-A-T signals (author bios, citations, credentials).
5. **Off-page** — backlink profile where data exists, unlinked brand mentions, local SEO (GBP, NAP consistency) where applicable.

Use the browse/gstack skill to crawl pages when available; otherwise work from what the user provides or can check, and mark the difference.

**Recurring SEO ops monitor.** For retained or repeated work, write `seo-ops-monitor.md` beside the report: weekly cadence for crawl/indexation/CWV/schema regressions, monthly for content decay, query movement, and internal-link opportunities. Inputs are collector output, GSC/GA4 exports when connected, PageSpeed artifacts, crawl exports, sitemap and robots snapshots, and licensed rank or local vendor exports. Alert rules: new noindex, robots block, sitemap drop, 4xx/5xx spike, redirect chain, canonical conflict, CWV regression, schema error, title/H1 removal, orphaned priority page, organic landing-page drop. Queue format: issue, source, retrieved_at, affected URL, severity, owner, proposed fix, approval needed, status, next check date. Movement, traffic, rankings, and visibility never appear without provenance; missing connected data is a monitor gap.

**Output** goes to `workspace/seo-audit/[domain].md`, stating audit mode, health score, P0–P3 tables with pages affected and fixes, checklist pass/fail results, top recommendations by impact-to-effort, a data-source inventory with retrieval dates and artifacts, and the data gaps that limit confidence. Same path as v1 — downstream tooling does not branch on version.

## Escalate when

- The site cannot be crawled and no export or connected data is available — say so rather than auditing from assumption.
- Search Console or analytics access is claimed but the collector cannot reach it.
- A finding depends on a metric that exists in no source available at the declared mode.
- The declared mode does not match the data actually in hand (for example, `onboarding_connected` with no GSC pull).
- An agent-readiness P0 failure exists — the fix list stops there until it is resolved.
- A recommended fix carries migration, legal, or revenue risk (domain moves, mass redirects, noindexing live templates).
