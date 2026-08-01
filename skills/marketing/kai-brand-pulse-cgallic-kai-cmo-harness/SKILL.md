---
name: kai-brand-pulse
description: Multi-platform brand intelligence pulse - collect cited public reputation evidence across web, news, YouTube, X, LinkedIn, Reddit, and review sites, then turn it into objection mining, content angles, competitor positioning, and surround-sound actions. Use when "brand monitor", "brand pulse", "what are people saying about us", "multi-platform reputation", "brand intelligence", "weekly brand monitoring", "objection mining", or "public reputation scan".
---

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

# /kai-brand-pulse — A Cited Read On What The Public Web Says

## Objective

A current, source-backed picture of a brand's public reputation across web, news, YouTube, X, LinkedIn, Reddit, and review sites — converted into the things marketing can act on: an objection bank in buyers' own words, content angles tied to evidence, competitor positioning, and surround-sound moves. Every claim points at a citation id.

Evidence first, analysis per platform, synthesis last. The order matters because one loud platform will otherwise swallow quieter evidence that is more useful.

**Use it** for a current public read on a brand, product, founder, or client; for objection mining feeding copy, sales, ads, social, or lifecycle; for competitor positioning evidence before `/kai-brand`, `/kai-competitors`, or `/kai-surround-sound`; and for weekly delta monitoring.

**Do not use it** for a full marketing audit (`/kai-audit`), for technical SEO or agent-readiness alone (`/kai-seo-audit`, `/kai-surround-sound`), when there is no approval to collect on a sensitive individual, or when the plan is to publish claims without citations.

## Done when

Work type `audit-report` — floor **E3/C4/O1** (`harness/eco-floors.yaml`), `client_facing: true`.

- **E3** — the delivered pulse is the approved version and every claim in it resolves to a citation id in the run's `raw/` archive or a collector source id.
- **C4** — the Kai Data Provenance Rule: raw search responses and the query plan stored before synthesis, `_data-gaps.md` filled for every surface that could not be reached, `banned_word_check` clean, and `python scripts/quality_gates/audit_provenance_lint.py <run-folder> --audit-dir` passing where the run is client-facing.
- **O1** — each recommended action names the metric it targets and its owner. The pulse's own outcome is whether its recommendations were adopted.

## Constraints

- **Cite every client-facing claim** with a citation id or a collector source id. No citation, no claim.
- **Store the raw archive and query plan before synthesis.** Synthesis that cannot be re-derived from the archive is not a pulse, it is an opinion.
- **Never report review counts, rankings, traffic, share of voice, sentiment share, or platform volume unless the source directly provides them.** Search output is a sampled evidence packet and gets labeled as sampled search evidence. "Observed in search results" is not market share and is not sentiment share.
- **Missing access goes to `_data-gaps.md`** — missing APIs, private platform access, unavailable exports. Not to an estimate.
- **Live search needs `SERPAPI_API_KEY`.** Without it the runner archives the query plan and writes data gaps; it does not invent findings.
- **Read `MARKETING.md` if present** for brand name, domain, ICP, category, competitors, positioning, and voice constraints.
- **For client-facing or quantitative recommendations, load `harness/references/audit-data-provenance.md`** and run the shared collector before writing final claims, declaring `sales_external`, `onboarding_connected`, or `internal_demo`. Cite collector sources for domain, schema, sitemap, or metric claims.
- **Analyze one platform at a time**, using only that platform's packet as source material, and keep platform conclusions separate until every packet has been read.
- **KaiCalls Fit Rule applies** to phone-led businesses: recommend it only when phone-capture evidence supports it, disclose Kai ownership, compare alternatives.
- **Any publishable copy generated from the pulse goes through `/kai-gate`** before it ships.
- **Sensitive individuals require approval before collection.**

## Context

| Need | Load / run |
|---|---|
| Provenance rule, modes, source tiers | `harness/references/audit-data-provenance.md` |
| Brand, domain, ICP, category, competitors | `MARKETING.md` (project root) |
| Evidence collection runner | `python scripts/intel/brand_pulse.py "<brand>" --domain "https://example.com" --category "<category buyers ask about>" --competitor "Competitor A" --competitor "Competitor B" --out "workspace/brand-pulse/<brand>-YYYY-MM-DD"` |
| Runner variants | `--skip-fetch` · `--wiki-dir "<brain-wiki-folder>"` · `--json` |
| Shared source collector | `python -m kai.source_data.collect --url "https://example.com" --firm-name "<brand>" --workflow brand-pulse --mode sales_external --out "workspace/brand-pulse-data"` |
| Weekly delta history | `data/intel/brand_pulse.db` (SQLite, first-seen / last-seen) |

**Surfaces collected by default:**

| Surface | Collection pattern | Why it matters |
|---|---|---|
| Web | Brand, reviews, alternatives, pricing, own-domain entity queries | Entity footprint and objections |
| News | Brand and category news queries | Authority, recency, PR angles |
| YouTube | `site:youtube.com` search fallbacks | Reviews, demos, creator narratives |
| X | `site:x.com`, `site:twitter.com` fallbacks | Fast-moving complaints, praise, comparisons |
| LinkedIn | `site:linkedin.com/posts` and company fallbacks | B2B proof, founder and category narratives |
| Reddit | `site:reddit.com` fallbacks | Raw objections and buying language |
| Review sites | G2, Capterra, Trustpilot, Clutch, Yelp fallbacks | Social proof, complaints, competitor context |

**Per-platform analyzer output** — repeated claims (what the market keeps saying), objections (which pain, doubt, pricing, trust, or support language repeats), proof gaps (what proof buyers need that the brand does not visibly supply), competitor context (who appears beside the brand and why), content angles (what Kai can write, publish, pitch, or test), and AEO actions (which citations, pages, or entity signals feed `/kai-surround-sound`).

**Cross-platform synthesis** produces six things: narrative map, objection bank with cited examples, competitor positioning, evidence-tied content angles, surround-sound actions (third-party citation, directory, review, forum, own-domain AEO), and monitoring deltas since the last run.

**Finding → next Kai move:**

| Finding | Next move |
|---|---|
| Repeated pricing objection | `/kai-landing-page`, `/kai-write`, or a sales FAQ refresh |
| Repeated competitor comparison | `/kai-competitors` plus a comparison page brief |
| Reddit objections | `/kai-reddit-listen` profile keywords and reply guardrails |
| Thin review-site footprint | Review request system, directory cleanup, or `/kai-surround-sound` |
| Strong third-party praise | Repurpose into proof assets, ads, case studies, AEO citations |
| Missing own-domain entity clarity | `/kai-brand`, `/kai-seo-audit`, then `/kai-surround-sound` |

**Output** goes to `workspace/brand-pulse/<run>/`: `brand-pulse-data.json`, `_brand-pulse.md`, `_content-angles.md`, `_objection-mining.md`, `_surround-sound-actions.md`, `_monitoring-plan.md`, `_data-gaps.md`, `raw/query-plan.json`, and `platforms/` (`web.md`, `news.md`, `youtube.md`, `x.md`, `linkedin.md`, `reddit.md`, `reviews.md`).

**Weekly monitoring:** run the same brand on a schedule against the same output convention, e.g. `0 8 * * 1 cd /path/to/kai-cmo-harness && python scripts/intel/brand_pulse.py "<brand>" --domain "https://example.com" --category "<category>" --out "workspace/brand-pulse/<brand>-$(date +\%F)"`. Pass `--wiki-dir` to write a pointer page for Brain wiki ingestion; the full raw archive stays in the workspace.

## Escalate when

- The subject is a private individual, or a named person whose coverage is sensitive, and approval has not been given.
- Search access is unavailable and the user wants conclusions anyway.
- Evidence surfaces a legal, safety, or crisis-communications issue rather than a marketing one.
- Findings would require a public response on a live channel — that is a separate approval.
- The brand's own claims contradict cited third-party evidence in a way that implicates advertising compliance.
