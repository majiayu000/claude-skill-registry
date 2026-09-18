---
name: kai-local-audit
description: Evidence-first marketing audit of a third-party local business (café, roaster, shop, restaurant, hotel, clinic, home service) from a Google Maps, share.google or website link — located DataForSEO rankings, map packs, search volume and seasonality, listings, reviews, backlinks, AI-assistant answers and a site crawl, plus direct checks (real-browser access, page weight, store shipping quotes, email DNS, mobile screenshots) — delivered as an owner-facing report with priced offers, an exact change list and a 12-week plan, optionally localized and bilingual. Use when "audit this business", "full marketing audit of <business>", "prospect audit", "local business audit", "use DataForSEO for the hard SEO data", "go deeper", "rerun it for local <market>", "also in Spanish", "give me the offers, changes and 3 month plan", or a business link arrives with "audit". For auditing your own product across channels use /kai-audit.
---

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

# /kai-local-audit — What a Local Business's Customers Actually See, and What to Do About It

## Objective

An owner-facing report on one local business that shows how it looks from its customers' towns, phones and languages, backed by located data anyone can re-pull, and that converts each finding into a priced offer, an exact change and a dated week of a 12-week plan. When asked, a localized rerun for a named market and a translated sibling page with identical structure.

The report's value is that it is right about things the owner cannot see from their own laptop: which phones cannot open the site, who owns the map pack in the next town, what AI assistants recommend instead, what shipping really costs a customer.

## Done when

Work type `audit-report` — floor **E3/C4/O1** (`harness/eco-floors.yaml`), `client_facing: true`.

- **E3** — the delivered report (and translated sibling, if requested) is the approved version, and every quantitative claim resolves to `workspace/local-audit/<slug>/audit-data.json` or a dated artifact in `raw/`.
- **C4** — the Kai Data Provenance Rule in full: collector and local-audit pulls ran before writing, the mode is declared, `_data-sources.md` and `_data-gaps.md` exist, `python scripts/quality_gates/audit_provenance_lint.py workspace/local-audit/<slug> --audit-dir` passes, `banned_word_check` passes, and the rendered page has no horizontal overflow at 390 px or 1280 px outside table wrappers, no missing images, no duplicate ids.
- **O1** — the targets table names today's value, the target, the pull that measures it and the re-run date. The outcome read is that re-run.

## Constraints

### Provenance — non-negotiable

- Load `harness/references/audit-data-provenance.md`. Mode is `sales_external` unless the client granted access.
- Run `python -m scripts.audit.collect --url "<url>" --firm-name "<name>" --mode sales_external --workflow local-audit --out workspace/local-audit/<slug>` before writing; `scripts.local_audit.pulls` and `scripts.local_audit.checks` append to the same dataset.
- **No ranking, score or visibility claim from a personal browser session.** Rankings, map packs and AI answers come from located API pulls (coordinates, mobile, market language). Speed scores come from the DataForSEO Lighthouse pull. The reference run's two eyeballed numbers were both wrong.
- Rankings move day to day: date every ranking claim and prefer counts across many located observations over a single position.
- Analytics totals are never reported raw. Split them into real visits and noise (storefront pixels, automation, developer machines, other hosts), report the cleaned figure, and mark that section `onboarding_connected`. Analytics cannot see visitors the site turns away, so it never overrides the access test.
- Share of estimated clicks is modeled (volume × positional CTR) and is labeled as modeled wherever it appears.
- A business recommended by an AI assistant, and any competitor positioning claim, is verified on that business's own site before it is repeated.
- Without `scripts/local_audit/` in the install: direct public checks only, every located metric in `_data-gaps.md`, and the report header says located metrics need the full harness (github.com/cgallic/kai-cmo-harness).

### Conduct

- Read-only on the web: no logins, follows, likes, messages, form submissions or orders. Shipping quotes come from a throwaway cart that is emptied afterwards.
- `brand_pattern` matches only the audited business; a loose pattern produces false "listing found" results.

### Report

- First screen: 3–5 actions for this week, each with the exact URL, number, setting or line of code.
- Offers follow `/kai-offer-builder` doctrine and are priced on measured costs (shipping tiers, fees); every price is a proposal to check against costs; no margins that were not provided.
- Changes are grouped by who does them — code, copy in every market language, commerce admin, Google Business Profile, DNS, social and partner asks — and are exact enough to hand off.
- The 12-week plan starts the next Monday, splits owner and developer work, gives each week a "done when", and places seasonal work where the volume pull shows the peaks.
- KaiCalls Fit Rule: evaluate phone and follow-up capture; disclose Kai ownership; compare alternatives; say plainly when it is not the first fix.
- House voice: no announced lists, dramatic fragments, "not X but Y", or tricolons. Hosted pages carry `noindex,nofollow,noarchive`.
- A translated sibling keeps every tag, attribute and element in place; only visible text, `alt`, `title`, `aria-label` and meta description change; code, URLs, brand names and search queries shown as data stay as they are.

## Context

| Need | Load / run |
|---|---|
| Endpoints, gotchas, deliverable structure, localized rerun, translation method | `harness/references/local-audit-playbook.md` |
| Provenance rule, modes, source tiers | `harness/references/audit-data-provenance.md` |
| Config template | `examples/local-audit-config.example.json` |
| Located pulls | `python -m scripts.local_audit.pulls {balance,volumes,discover,serp,maps,listings,reviews,backlinks,ai,lighthouse,crawl} [--collect]` |
| Direct checks | `python -m scripts.local_audit.checks {access,assets,dns,shopify,all}` |
| Connected analytics (owner token) | `python -m scripts.local_audit.matomo` (Matomo) or `scripts.audit.collect --ga4` |
| Industry checklists | `knowledge/checklists/local-service-business-checklist.md`, `restaurant-food-bev-checklist.md`, `multi-location-checklist.md`, `cro-audit-checklist.md` (Phone-Based Lead Capture) |
| Offers | `/kai-offer-builder` |
| Page rendering | `/kai-html-presentation` or the house strategy-page format |
| Gates | `scripts/quality_gates/audit_provenance_lint.py`, `banned_word_check.py` |

**Output:** `workspace/local-audit/<slug>/` — `config.json`, `audit-data.json`, `kai-data.json`, `_data-sources.md`, `_data-gaps.md`, `raw/` (API responses, direct-check artifacts, screenshots, shipping quotes), `local-audit/` (per-pull summaries), `report.html`, and `<lang>/report.html` when translated.

**Typical cost:** about $8 of DataForSEO credit for two markets with crawl, reviews and AI answers; re-runs of cached pulls are free.

## Escalate when

- DataForSEO credentials are missing or the balance cannot cover the planned pulls — say which metrics become data gaps.
- The business model or target market is ambiguous enough that the keyword set or vantage towns would change materially.
- A finding would require logging in, submitting a form or placing an order to confirm.
- The report will be sent to the business itself and includes pricing proposals the requester has not reviewed.
