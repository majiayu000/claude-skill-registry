---
name: niche-signal-discovery
disable-model-invocation: true
description: "Discover niche first-party signals that differentiate Closed Won vs Closed Lost accounts for ICP analysis. Use when the user provides won/lost customer domain lists and wants differential signals (website content, job listings, tech stack, maturity markers) to build account scoring models and prospecting criteria. Triggers: ICP analysis, niche signals, won vs lost analysis, differential signals, signal discovery, ICP signal report, account scoring signals, lead scoring, first-party signals, buyer signals. Before reading this file, first read gtm-meta-skill to understand the Deepline CLI tool and how to use it. Then read this file for guidance on the task."
---

# Niche Signal Discovery

Discover differential signals between Closed Won and Closed Lost accounts by extracting multi-page website content and job listings, then computing Laplace-smoothed lift scores to identify what distinguishes buyers from non-buyers.

## Prerequisites

- **Deepline CLI** — All enrichment runs through `deepline enrich`. No separate API keys for exa/crustdata/apollo etc.
- **Python 3** stdlib only — no pip dependencies for any shipped script.
- **Credits** — ~6 credits/company for enrichment. Step 7 contact discovery is additional. **Always get user approval before paid steps.**

## Deepline-First Principle

Use `deepline enrich` for all enrichment, `deepline tools execute` for one-offs, `deepline playground` for inspection. Reruns are idempotent. Refer to `gtm-meta-skill` for command patterns and provider playbooks.

## Input requirements

- Won and lost customer domain lists (≥20 won + ≥10 lost for statistical significance)
- **Lookalikes can supplement Won** if Closed Won < 15. Add a Dataset Caveat to the report.
- **Target company context** from Step 0 — what they sell, who they sell to, key personas.

## Pipeline

```
0.    Discover target company (what they sell, who they sell to)
0.5.  Discover ecosystem (competitors, tech stack, buyer personas)
1.    Prepare input CSV (deduplicate within won/lost groups)
1.0.5 Build "do not re-contact" index from user's existing list (scripts/dedupe_utils.py)
1.5.  Generate vertical-specific configs (keywords, tools, job roles)
2.    Multi-page website + job extraction (deepline enrich)
3.    Quality gate — verify file completeness + coverage (>80%)
3.5.  Review configs against enriched data
4.    Differential analysis (scripts/analyze_signals.py)
5.    Generate report — every top signal must include cited evidence
6.    Signal interpretation review
7.    Top 10 net-new prospects [REQUIRED] + contacts/emails [optional, costs credits]
```

**Step 7 is required.** A signal report without 10 actionable companies forces the reader to do their own prospecting pass — exactly the expensive thing they wanted to skip. Contacts/emails are optional only because they cost extra credits; always offer them.

## Signal reliability hierarchy

Highest → lowest confidence:

1. **Job listings** — active budget + acknowledged pain. Highest-intent.
2. **Analyst validation** (Gartner/Forrester) — typically 4-7x lift, rare in lost.
3. **Compliance infrastructure** (SOC2/GDPR/ISO) — procurement maturity.
4. **Buyer pain language** on careers/blog — operational awareness.
5. **Tech stack tools** (niche SaaS) — infrastructure readiness.
6. **Website product/marketing content** — variable; can be buyer OR competitor.

**When website signals fail:** For B2B back-office tools (AR, billing, compliance), buyers don't publish their pain on marketing pages. Prioritize jobs + tech stack + firmographics for these verticals.

## What NOT to use for scoring

CRM fields populated by AE activity — catalyst note count, OCR-derived counts (`number_of_champions_c`, `number_of_decision_makers_c`), MEDDPICC picklists, any "did the AE do X on this opp" field — correlate with win-rate as **engagement artifacts, not causal signals**. They get filled in *after* the AE decides an opp is worth working. **Never use them as scoring inputs.** On one real run, catalyst notes showed "109x lift" — almost made the TL;DR before we caught the direction of causality.

Rule of thumb: every scoring input must be observable BEFORE the AE touches the account. Read `references/scoring-pitfalls.md` for the full list and the "safer alternative read" for loss-reason data.

## Step 0: Target company discovery

**Do this FIRST.** The entire pipeline (exa query, keywords, tech stack, job roles) adapts based on this discovery; skipping it produces generic/irrelevant signals.

```bash
deeplineagent: "Research {{company-domain}}. Summarize what the company sells, who they sell to, what makes them different, and any example customers."
```

Document: (1) product category, (2) target buyer persona, (3) key differentiation, (4) example customers.

## Step 0.5: Ecosystem discovery

Three parallel `deeplineagent` queries:

- **Competitors** — `"{product category} software alternatives competitors"` → 3-5 names
- **Tech stack** — `"{buyer persona} software stack"` → 10-15 tools by category
- **Job roles** — `"{buyer persona} job titles"` → 10-15 title variations

These feed Step 1.5 config generation.

## Step 1: Prepare input CSV

```csv
domain,status
customer1.com,won
non-customer1.com,lost
```

**Deduplicate within the input.** If a domain appears in BOTH won and lost (same company, multiple deals), Deepline only fetches job listings once — silently undercounting `won_with_jobs`. Remove ALL rows for cross-group domains:

```python
from collections import Counter
counts = Counter(r['domain'] for r in rows)
duplicate_domains = {d for d, c in counts.items() if c > 1}
# Drop every row in duplicate_domains, not just one copy.
```

## Step 1.0.5: Build "do not re-contact" index

Before any prospects ship in Step 7, dedupe candidates against whatever "already known" list the user provides — customers, CRM export, past outbound, a previous run's output. **Always ask explicitly**; if the user has no list, note it as a caveat in the final report rather than silently skipping.

**Order: apex domain first, fuzzy company name as fallback.** Use the shipped helper — it handles public-suffix multi-label TLDs (`co.uk`, `co.jp`, `com.au`) and corporate-suffix stripping:

```bash
python3 scripts/dedupe_utils.py --selftest   # one-time sanity check
python3 scripts/dedupe_utils.py \
    --existing customers.csv --candidates prospects_raw.csv \
    --out-actionable prospects_actionable.csv --out-matched already_known.csv
```

Don't silently drop CRM matches — **categorize** them: Net-new / Account-only / Re-engage / Active-open / Current-customer.

**Read `references/dedupe.md`** for the failure modes (raw-string match missing `amsynergy.nikon.com → nikon.com` cost 24 of 50 prospects in one run), category definitions, and library usage.

## Step 1.5: Generate vertical-specific configs

Create three JSON files in `output/{{company}}/`:

```
{{company}}-keywords.json    # product category, pain language, competitor names, maturity terms
{{company}}-tools.json       # niche SaaS tools by category
{{company}}-job-roles.json   # buyer persona job titles
```

**Read `references/keyword-catalog.md`** for the JSON schema, generation patterns, and multi-vertical examples (creative ops, AR automation, sales engagement, developer tools).

**Validation:** Do the configs match the target's vertical and buyer persona? If not, refine based on Step 0/0.5 findings.

## Step 2: Deepline enrichment

**Never scrape just the homepage.** Use `exa_search` with `contents.text` to discover AND scrape ~8 pages per domain in one call.

Generate the exa query dynamically based on the target's product category — see `gtm-meta-skill` for query variants by buyer type (back-office, developer, creative, sales).

```bash
deepline enrich \
  --input output/{{company}}-icp-input.csv \
  --output output/{{company}}-enriched.csv \
  --with '{"alias":"website","tool":"exa_search","payload":{"query":"{{exa-query}}","numResults":8,"type":"auto","includeDomains":["{{domain}}"],"contents":{"text":{"maxCharacters":3000,"verbosity":"compact","includeSections":["body"]}}}}' \
  --with '{"alias":"jobs","tool":"crustdata_job_listings","payload":{"companyDomains":"{{domain}}","limit":50}}'
```

**Cost:** ~5 credits/company (exa) + ~1 credit (crustdata) = **~6 credits/company**. Get user approval first.

## Step 3: Quality gate

`deepline enrich` returns to terminal **before** OS buffers fully flush. Running the analysis script immediately can read a partially-written file and produce `won_with_jobs: 0` even when data is fine. Always verify:

```bash
INPUT_ROWS=$(wc -l < output/{{company}}-icp-input.csv)
OUTPUT_ROWS=$(wc -l < output/{{company}}-enriched.csv)
echo "Input: $INPUT_ROWS, Output: $OUTPUT_ROWS"  # should match
```

Then spot-check that won rows have job data, that website coverage is >80%, and that average content depth is 6-8 pages / 12-20K chars per company.

**Read `references/quality-gate.md`** for the full verification script, the buffer-flush retry pattern, and the "auto-extracted domain validation" check that has caught up to **53% false-positive rates** in CRM-exported customer lists.

## Step 3.5: Review configs against enriched data

```bash
deepline playground output/{{company}}-enriched.csv
```

**Red flags:**
- Keyword in <10% of enriched companies → too niche, broaden
- Keyword in >90% → too generic, refine
- Product-category keywords appear frequently in Won → wrong product category, those companies are competitors not buyers
- Job roles missing from actual listings → wrong buyer persona

Fix and regenerate configs if needed.

## Step 4: Differential analysis

```bash
python3 scripts/analyze_signals.py \
  --input output/{{company}}-enriched.csv \
  --keywords output/{{company}}-keywords.json \
  --tools output/{{company}}-tools.json \
  --job-roles output/{{company}}-job-roles.json \
  --output output/{{company}}-analysis.json
```

The script computes substring-match presence, Laplace-smoothed lift, source breakdown (website/jobs/both), tech-stack mentions, job-role prevalence, anti-fit signals, and **per-keyword evidence quotes** (±40 chars with URLs) — the evidence array is what Step 5 renders.

## Step 5: Report generation

**Read `references/report-template.md`** for the full report structure (Quick Reference Dashboard at the top, then detail sections), the signal-strength visual scale, Apollo URL format, and all quality rules. Critical rules in brief:

- Raw counts always (`15% (6)`, not just `15%`); sample sizes in headers (`Won (n=37)`)
- Bold only signals with lift > 2x AND count ≥ 3 companies
- Flag n=1 signals — they're statistically meaningless
- **Source evidence is mandatory for every top signal** (lift ≥ 1.5 AND won ≥ 3) — 3-5 cited quotes per signal with source type, company, page/job title, ±40-char quote, and live URL. The analysis script outputs this; render it, don't decide whether to. Signals without 3+ citations get demoted and flagged `*(insufficient evidence)*`.
- Annotate each evidence quote with ✅ (clear buyer signal) or ⚠️ (vendor-adjacent — the company sells something similar, so the keyword on their product page isn't a buyer signal)
- Tier 1 cheatsheet point values must match the Section 6 scoring model — cross-check both before shipping

## Step 6: Signal interpretation

**Read `references/signal-interpretation.md`** before writing interpretation columns. Key rules:
- Website content mentioning what the target sells = competitor signal (not buyer)
- Job listings = highest-intent buyer signal
- Same keyword means different things on product page vs careers page vs blog
- Tech stack tools need context — do they create or solve the target's problem?

## Step 7: Top 10 net-new prospects (required)

**10 companies are required for every run; contacts + emails are optional** (additional Deepline credits). Always offer contact discovery; only run it if the user approves the spend.

```bash
# Companies only — no extra credits beyond Step 2 enrichment:
python3 scripts/find_contacts.py --input prospects_actionable.csv --output top10.csv --top 10 --no-contacts

# Companies + contacts + emails — asks for credit approval.
# --roles is REQUIRED in --contacts mode and must be the buyer-persona job
# titles surfaced in YOUR Step 0/0.5 (not a stale list from a different vertical):
python3 scripts/find_contacts.py --input prospects_actionable.csv --output top10.csv --top 10 \
    --contacts --roles "<persona job titles from Step 0.5>"
```

When `--contacts` is on, the orchestrator runs a 3-phase chain via Deepline:
1. `company_to_contact_by_role_waterfall` (free, mature companies)
2. **`exa_search_people` fallback for any company Phase 1 missed** — mandatory. On the run that motivated this, Phase 1 returned 0 contacts on all 10 top prospects (small/non-US industrial); Exa found 15 real contacts at 6 of those 10 in the same pass.
3. `person_linkedin_only_to_email_waterfall` with **apex-domain validation** — providers return stale addresses (`@orbitalatk.com` for someone now at X-Bow, personal Gmails, wrong-company false positives). Mismatched apex → publish "(email not found)", keep the raw value in `raw_email` for auditing.

**Read `references/step-7-prospects.md`** for the required vs. optional output fields, the prospect-card skeleton, the Phase 2 Exa guardrails (title parsing + company-match filter), and the "10 is a ceiling, not a floor" guidance.

## Enrichment data structure

After unwrap, each enriched row has:

- `website` cell → JSON with `data.results[]`, each item: `{text, url, title}`
- `jobs` cell → JSON with `data.listings[]`, each item: `{title, description, url, category}` (note: `title` not `job_title`)

`scripts/analyze_signals.py` auto-detects these columns; override with `--website-col N --jobs-col N` if your CSV uses different column names.

## Common pitfalls (top 6 — full list in references/pitfalls.md)

1. **Skipping target discovery (Step 0)** → generic/irrelevant configs.
2. **Homepage-only scraping** → misses pricing, integrations, security, careers.
3. **Generic tech stack** ("AWS", "GitHub", "Slack" appear on most B2B sites) → search for niche SaaS specific to the buyer persona.
4. **Trusting n=1 signals** → require 3+ companies for Tier 1 scoring; flag single-company signals with a verification note.
5. **Raw-string dedupe missing parent domains** — `amsynergy.nikon.com ≠ nikon.com` for naive comparison. Always use `extract_apex()`. **24 of 50 "net-new" prospects in one real run were already in the CRM** as parent-domain entries the raw-string dedupe missed.
6. **Trusting confirmation-biased CRM fields** (catalyst notes, OCR counts, MEDDPICC) as signals — they're downstream of AE engagement, not causal. Read the "What NOT to use for scoring" section above.

**Read `references/pitfalls.md`** for the full 18-item list including substring false positives, vendor-vs-buyer signal context, back-office-tool interpretation, and shipping-without-prospects.

## Proven signal patterns

**Read `references/proven-signals.md`** for typical lift ranges across verticals (analyst validation 4.5-6.5x, hiring signals 3.8-5.5x, compliance infra 2.1-6.5x, etc.), high-confidence anti-fit patterns (consumer signals 0.2x, retention/churn 0.2-0.4x), and a starter 0-100 scoring model with three tiers (Core Fit / Buying Intent / Infrastructure Readiness).

## References

- **`references/keyword-catalog.md`** — JSON schema + multi-vertical examples for Step 1.5 config generation
- **`references/dedupe.md`** — Step 1.0.5 dedupe failure modes, categorization rules, library usage
- **`references/quality-gate.md`** — Step 3 verification scripts, buffer-flush retry pattern, auto-extracted-domain validation
- **`references/report-template.md`** — Step 5 full report structure, signal-strength scale, Apollo URL format, all quality rules
- **`references/signal-interpretation.md`** — Step 6 buyer-vs-seller-vs-competitor rules
- **`references/step-7-prospects.md`** — Step 7 prospect-card skeleton, Exa guardrails, Phase 3 apex validation
- **`references/scoring-pitfalls.md`** — Confirmation-biased CRM fields to exclude from scoring
- **`references/pitfalls.md`** — Full 18-item pitfalls list
- **`references/proven-signals.md`** — Typical lift ranges + scoring model guidance
- **`scripts/analyze_signals.py`** — Step 4 differential analysis. Auto-detects columns.
- **`scripts/dedupe_utils.py`** — Step 1.0.5 + Step 7 email validation. `extract_apex()`, `norm_name()`, `match_against_existing()`. Stdlib only. `--selftest` flag for one-time install verification.
- **`scripts/find_contacts.py`** — Step 7 orchestrator. `--contacts` / `--no-contacts` toggle, 3-phase Deepline chain.

## Changelog

- **2026-04-07** — Added Step 1.0.5 (dedupe with apex helper), Step 7 (top 10 prospects required, contacts optional via `--contacts`/`--no-contacts`), `references/scoring-pitfalls.md` warning about confirmation-biased CRM fields, mandatory citation rule. Shipped `scripts/dedupe_utils.py` + `scripts/find_contacts.py`. Aggressively trimmed inline detail to references — moved Step 3 quality gate, Step 5 quality rules, Common Pitfalls (items 7-15), and Proven Signal Patterns into `references/`. SKILL.md went from 650 to ~250 lines via progressive disclosure.
