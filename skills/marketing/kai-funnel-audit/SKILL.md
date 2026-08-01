---
name: kai-funnel-audit
description: Two-layer funnel audit on collected data only — stress-test the awareness layer (hooks, messaging, proof placement, attention leaks on live pages and ads) and the lead-capture layer (opt-ins and lead magnets scored on the four Value Equation variables, friction findings, weakest-magnet rewrite), plus a phone-path check under the KaiCalls Fit Rule. Use when "funnel audit", "audit my funnel", "why is my funnel leaking", "top of funnel isn't converting", "audit our lead magnets", "opt-in audit", "awareness to lead audit", "where are we losing people", "lead capture audit", or any request to diagnose the full awareness-to-lead flow rather than one page.
---

Audit a live funnel in two layers — awareness (do collected hooks, messaging, and proof earn attention?) and lead capture (do collected opt-ins convert attention into leads?) — on collected data only, ending in a provenance-linted fix list routed to owning skills.

**Scope boundary vs `/kai-cro`:** `/kai-cro` runs the 5-layer conversion stack (technical, traffic, offer, design, copy) on ONE page or flow, in depth. This skill audits the FULL awareness-to-lead path across surfaces — ads, organic posts, entry pages, opt-ins, lead magnets, phone path — and finds where the flow breaks between them. When a single page needs deep conversion work, this skill flags it and hands off to `/kai-cro`; it never re-runs the 5-layer stack itself. `/kai-audit` (full marketing audit) and `/kai-seo-audit` are wider still; hand off there when the problem is not the funnel.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

Then load the framework sources this skill runs on:
- `knowledge/people/alex-hormozi-knowledge.md` — sections "The Value Equation", "$100M Leads: The Lead Generation System" (Core Four, Lead Magnet Framework), and "Content Strategy: Give Away Everything"
- `knowledge/playbooks/conversion-rate-optimization.md`
- `knowledge/playbooks/funnel-hack-offer-architecture.md` — source-evidence standard, mechanics-vs-taste separation, A/B hypothesis template
- `knowledge/checklists/cro-audit-checklist.md` — reuse its per-element checks; do not restate them

## Phase 1: Provenance Setup (before any finding is written)

**Load `harness/references/audit-data-provenance.md` first.** This audit publishes client-facing claims, so the Kai Data Provenance Rule applies in full.

1. **Declare a mode** — `sales_external` (public data only; default when no private access is confirmed), `onboarding_connected` (client granted GSC/GA4/ad/CRM/call-tracking access), or `internal_demo` (labeled sample data only). State the mode in `_executive-summary.md` and every deliverable header.
2. **Run the collector** before writing anything:
   ```bash
   python -m scripts.audit.collect --url <url> --mode <mode> --workflow funnel-audit --out workspace/funnel-audit/data
   ```
   Add opt-in collectors per the provenance doc when credentials exist (`--pagespeed`, `--gsc`, `--ga4`, `--calls`, ...). Read metrics from `data/kai-data.json` (`audit-data.json` is the identical alias for the lint). If a metric is not in the collector output or a user-provided artifact, it is unavailable — it goes in `_data-gaps.md`, never into a finding.
3. **Map the funnel from collected artifacts only.** Write `funnel-map.md`: one row per surface, awareness layer (ads with Ads Library URLs, organic posts, blog/SEO entries, homepage) and capture layer (each opt-in form, lead magnet, booking flow, phone path), with entry→capture edges. A surface with no collected artifact (no crawl, no archive, no user-provided export or screenshot) is OUT OF SCOPE — list it in `_data-gaps.md` with what would be needed to audit it. Never audit from memory of what pages "usually" look like.
4. **Start the ledgers** — `_data-sources.md` (source, tier, retrieved-at, used-for, artifact path per the provenance doc's table) and `_data-gaps.md`. Every finding downstream cites a row in `_data-sources.md`.

## Phase 2: Awareness Layer Audit

Stress-test the attention side of the funnel on the actual collected pages and ads. Per the Give-Away-Everything model, awareness assets must give real value before asking ("Give-Give-Give-Ask"; "give away the secrets, sell the implementation") — an awareness layer that only pitches is itself a finding.

**2a. Hook scoring.** Extract the working hook of every collected awareness asset (ad primary text, post first line, page headline + first viewport). Score each with the `/kai-hook-bench` Phase 4a rubric — 0-2 per dimension of clarity, specificity, curiosity, proof-backing, total /8 (rubric definitions live in `harness/skills/kai-hook-bench/SKILL.md`; do not restate them). Also run each hook against the anti-patterns in `memory/what-doesnt-work.md` and the voice regexes in `harness/skills/kai-gate/SKILL.md` step 3 — a hook matching a known loser pattern is an automatic finding. Write `awareness-scores.md`: asset, artifact path, hook text, four sub-scores with one-phrase justifications, total. Replacement hooks are NOT written here — route to `/kai-hook-bench`.

**2b. Messaging check.** Per collected entry page: does the headline state the outcome (Dream Outcome, not the feature)? Does ad→page scent hold (same promise, same persona, same offer)? Is the persona obvious in one viewport (match against `knowledge/personas/_persona-index.md` or the client's own)? Does the asset reward the click (Hook–Retain–Reward — hooks that open a question the page never closes are a finding)?

**2c. Proof placement + provenance.** Proof raises Perceived Likelihood of Achievement — the numerator variable most awareness pages waste. Check on each collected entry page: does proof (testimonial, named result, review count, logo wall) appear **above the fold** in the collected viewport/screenshot? Is every proof element **provenance-clean** — attributable, plausible, not self-contradicting (e.g. review count on page vs Places data from the collector)? Unverifiable proof on the client's own page is a P0 finding (compliance risk per `harness/references/advertising-compliance.md`), not something to silently keep. Missing proof assets → hand off to `/kai-proof-builder` or `/kai-case-study`.

**2d. Attention leaks.** Flag, with artifact citation each: competing CTAs in the first viewport, nav links exiting the funnel before the first capture point, ad traffic landing on the generic homepage, dead ends (awareness asset with no next step), and slow entry pages (PageSpeed numbers only from collector output — otherwise gap).

**2e. Prioritized awareness fix list.** Write `awareness-fixes.md` — exactly this shape, one row per fix, P0/P1/P2 order:

| Priority | Fix | Evidence (artifact path/URL + retrieved-at) | Effort (Low/Med/High) | Expected mechanism |
|----------|-----|---------------------------------------------|----------------------|--------------------|

"Expected mechanism" names the variable the fix moves (a Value Equation variable, a Hook–Retain–Reward stage, or a scent/leak repair) — **never an invented uplift percentage or unsourced benchmark**. If a fix is worth testing, write it as an A/B hypothesis using the template in `knowledge/playbooks/funnel-hack-offer-architecture.md` (primary metric + guardrail metric, no predicted lift).

## Phase 3: Lead-Capture Layer Audit

**3a. Inventory.** From `funnel-map.md`, list every capture point: opt-in forms, lead magnets, booking flows, gated content. For each, record from collected data: what is offered, what is asked (fields, steps), and where it sits in the funnel.

**3b. Value Equation scoring.** Score every lead magnet/opt-in 1-10 on the four variables (framework: `knowledge/people/alex-hormozi-knowledge.md`, same convention as `/kai-offer-builder` Phase 4 — numerator 10 = strongest; denominator 10 = worst):

| Magnet | Dream Outcome | Perceived Likelihood | Time Delay (high=slow) | Effort & Sacrifice (high=hard) | Value Index (DO×PL)/(TD×ES) |
|--------|---------------|----------------------|------------------------|--------------------------------|------------------------------|

Justify each score in one line citing the collected artifact. Also check each magnet against the Lead Magnet Framework: narrow and specific? Painkiller, not vitamin? Which of the three types (problem diagnosis / sample-trial / symptom revelation)? Named per the formula `[Number] + [Adjective] + [Target Audience] + [Desired Outcome] + [Timeframe]`? Would it pass the gold standard — good enough to charge for? Label the table "internal scoring rubric" — it never ships as a quantitative claim. Write to `lead-capture-scores.md`.

**3c. Friction findings.** Write `friction-findings.md`: per capture point — form field count and which are required, steps to completion, load time, mobile behavior, post-submit delivery delay (Time Delay applies to the magnet itself: is the first win immediate or "check your inbox in 24h"?). Every number cites collected data (crawl artifact, PageSpeed run, GA4/form analytics if `onboarding_connected`) **or is marked as a gap** — no assumed field counts, no "typically 3 steps".

**3d. Weakest-magnet rewrite.** Take the lowest Value Index magnet and rewrite it via the four Value Equation application questions: make the outcome more vivid; raise belief it works for *them* (attach real proof from Phase 2c inventory only); collapse Time Delay (first win at consumption, target immediate); strip Effort & Sacrifice (fewer fields, instant delivery, done-for-you format over course-format). Rename it with the naming formula. Write `magnet-rewrite.md`: before/after spec, re-scored table, and what evidence would confirm each claim in the new copy. This is a spec + copy draft, not a shipped asset. If the problem is the underlying offer rather than the magnet's packaging, stop and hand off to `/kai-offer-builder`; full page rebuild around the new magnet → `/kai-landing-page`.

## Phase 4: Phone-Path Check (KaiCalls Fit Rule)

Apply the KaiCalls Fit Rule exactly as `AGENTS.md` defines it:

1. **Is the business phone-led?** Evidence from collected data only: prominent phone number/call CTAs in crawled pages, call extensions in observed ads, local/service vertical, booking handled by phone. If phone-led, evaluating phone-based lead capture is REQUIRED — a funnel audit that ignores the phone path on a phone-led business is incomplete.
2. **Look for real fit signals:** missed-call pain, after-hours coverage gaps, slow speed-to-lead, no qualification/routing, no call logging. In `sales_external` mode these come from public observation or a logged public call test; in `onboarding_connected`, from CallRail/CRM/phone logs via the collector. **No signal data = data gap**, logged in `_data-gaps.md` — not an assumed problem.
3. **Recommend KaiCalls (kaicalls.com) only when fit signals are real and cited.** The recommendation MUST disclose that KaiCalls is Kai-owned, MUST compare at least two alternatives (e.g. human answering service, callback widget, native call tracking/routing tools), and must NEVER be the primary recommendation when phone demand is low, compliance (call recording/consent) is unresolved, the workflow is self-serve by design, or the source data is missing.

Write `phone-path.md`: phone-led verdict + evidence, fit-signal table with sources, recommendation (or "not evaluated — not phone-led" / "insufficient data") with disclosure and alternatives. Note: the older Layer-6 wording in `/kai-cro` predates the Fit Rule — the `AGENTS.md` rule wins.

## Phase 5: Handoff Gate + Routing

**5a. Executive summary.** Write `_executive-summary.md`: mode label on top (per the provenance doc's Hard Rule 4), funnel map recap, top 5 fixes across both layers, data gaps that most limit confidence.

**5b. Quality gates** on copy-bearing outputs (`magnet-rewrite.md`, and any before/after copy inside `awareness-fixes.md`):

```bash
python scripts/quality_gates/four_us_score.py --file workspace/funnel-audit/magnet-rewrite.md    # 10/16 — hook/offer-asset threshold
python scripts/quality_gates/banned_word_check.py --file workspace/funnel-audit/magnet-rewrite.md
```

Max 2 retry cycles; fix only the named failing dimension, never rewrite the file (see `memory/lessons.md`). After 2 failures, escalate to a human with the diagnosis and log it via `python scripts/self_improvement/lesson_capture.py add`.

**5c. Provenance gate — blocking, run before any handoff:**

```bash
python scripts/quality_gates/audit_provenance_lint.py workspace/funnel-audit --audit-dir
```

A failure means an unsourced number or a missing ledger file — fix the citation or move the claim to `_data-gaps.md`; never delete the ledger requirement.

**5d. Route each fix to its owning skill** (append a routing column or table to `_executive-summary.md`):

| Finding class | Route to |
|---------------|----------|
| Single page needs deep conversion work (5-layer stack) | `/kai-cro` |
| Page or magnet delivery needs a rewrite/rebuild | `/kai-landing-page` |
| Offer itself is weak (Value Index low even after packaging fixes) | `/kai-offer-builder` |
| Hooks scored ≤4/8 need replacements | `/kai-hook-bench` |
| Proof missing or unverifiable | `/kai-proof-builder` or `/kai-case-study` |
| Single finished pieces (emails, posts, ads) from the fixes | `/kai-brief` then `/kai-write` |
| Independent re-gate of rewritten copy | `/kai-gate` |
| Funnel problem sits upstream in traffic/SEO/brand | `/kai-seo-audit` or `/kai-audit` |

**Approval doctrine:** this audit is a recommendation package. Nothing here publishes, edits a live page, changes an ad, or dials a phone system — every implementation goes through the owning skill's human-approval gate.

## Output Tree

```
workspace/funnel-audit/
├── _data-sources.md         # every source: tier, retrieved-at, used-for, artifact (required by lint)
├── _data-gaps.md            # out-of-scope surfaces, missing metrics, absent call data (required by lint)
├── data/                    # scripts.audit.collect output: kai-data.json + audit-data.json, raw/
├── funnel-map.md            # Phase 1 — surfaces + edges, collected artifacts only
├── awareness-scores.md      # Phase 2a — per-asset hook rubric scores
├── awareness-fixes.md       # Phase 2e — prioritized fix list: evidence, effort, mechanism
├── lead-capture-scores.md   # Phase 3b — Value Equation table + lead-magnet checks
├── friction-findings.md     # Phase 3c — fields/steps/load per capture point, sourced or gapped
├── magnet-rewrite.md        # Phase 3d — weakest magnet before/after spec + re-score
├── phone-path.md            # Phase 4 — phone-led verdict, fit signals, disclosed recommendation
├── _gate-report.md          # Phase 5 — Four U's, banned-word, provenance lint results + retries
└── _executive-summary.md    # Phase 5 — mode label, top fixes, gaps, routing table
```

## Hand-offs (do not re-specify these jobs)

- Deep single-page conversion audit → `/kai-cro` (5-layer stack; this skill only flags the page)
- New hook bank for weak awareness assets → `/kai-hook-bench`
- Offer redesign / Grand Slam Offer construction → `/kai-offer-builder`
- Landing page or magnet-page rewrite → `/kai-landing-page`
- Proof and case-study assets → `/kai-proof-builder`, `/kai-case-study`
- Finished copy pieces → `/kai-brief` → `/kai-write`; independent gate → `/kai-gate`
- Wider marketing or SEO diagnosis → `/kai-audit`, `/kai-seo-audit`
- 30-day follow-up on shipped fixes runs through the standard content pipeline; underperformers get diagnosed via `/kai-retro`
