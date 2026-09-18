---
name: kai-local-audit
description: Evidence-first marketing audit of a third-party local business (café, roaster, shop, restaurant, hotel, clinic, home service) from a Google Maps, share.google or website link — located DataForSEO rankings, map packs, search volume and seasonality, listings, reviews, backlinks, AI-assistant answers and a site crawl, plus direct checks (real-browser access, page weight, store shipping quotes, email DNS, mobile screenshots) — delivered as an owner-facing report with priced offers, an exact change list and a 12-week plan, optionally localized and bilingual. Use when "audit this business", "full marketing audit of <business>", "prospect audit", "local business audit", "use DataForSEO for the hard SEO data", "go deeper", "rerun it for local <market>", "also in Spanish", "give me the offers, changes and 3 month plan", or a business link arrives with "audit". For auditing your own product across channels use /kai-audit.
---

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

Audit someone else's local business the way its customers meet it: from their town, on their phones, in their language. Then turn every finding into a priced offer, an exact change and a dated week.

Load before starting: `harness/references/local-audit-playbook.md` (endpoints, gotchas, deliverable structure) and `harness/references/audit-data-provenance.md`.

## Non-Negotiable: Kai Data Provenance

- Declare the mode. Prospects and anyone who has not granted access are `sales_external`.
- Run `python -m scripts.audit.collect --url "<url>" --firm-name "<name>" --mode sales_external --workflow local-audit --out workspace/local-audit/<slug>` before writing. The local-audit pulls below append to the same `audit-data.json`.
- Every ranking, volume, review count, rating, referring-domain count, map-pack placement, AI-answer count, Lighthouse score and page weight in the report cites its source and retrieval date. Anything not in `audit-data.json` or a dated direct check goes in `_data-gaps.md`.
- Never report a ranking or score observed in a personal browser. The reference run's two eyeballed numbers were both wrong.
- Modeled numbers (share of estimated clicks) are labeled as modeled with the formula.

**If `scripts/local_audit/` is not in this install:** run the public direct checks by hand (Phase 3), cite URLs and dates, put every located-ranking, volume, listing, review, backlink and AI-answer metric in `_data-gaps.md`, and say in the report header that located metrics need the full harness (github.com/cgallic/kai-cmo-harness).

## Phase 0: Identify the business

1. Resolve the link and read the business's own site.
2. Write one sentence stating the actual business model and every sales channel (storefront, order form, online store, wholesale, marketplaces, DMs) and contact point. Correct the request if it assumed the wrong model.
3. Pick the industry checklists that apply: `knowledge/checklists/local-service-business-checklist.md`, `restaurant-food-bev-checklist.md`, `multi-location-checklist.md`, plus `cro-audit-checklist.md` (Phone-Based Lead Capture) always.

## Phase 1: Configure

1. Copy `examples/local-audit-config.example.json` to `workspace/local-audit/<slug>/config.json`.
2. Fill: business, domain, store domain, a `brand_pattern` that matches only this business, 3–6 vantage towns with coordinates, home market and buyer market location codes, keywords by intent (brand, buy, category/wholesale, origins or specialties, tourism, local town terms, gifts/subscriptions, near-me) in every language the market uses, Maps queries, listing name casings, category groups, partner and competitor review targets (`cid` from Maps or listings), competitor domains, local media pattern, AI prompts per language, Lighthouse URLs, crawl targets.
3. Check the balance: `python -m scripts.local_audit.pulls balance`.

## Phase 2: Pull located data

Run in this order (each is re-runnable; responses cache in `raw/`):

```bash
python -m scripts.local_audit.pulls volumes    --config <cfg> --out workspace/local-audit/<slug>
python -m scripts.local_audit.pulls discover   --config <cfg> --out workspace/local-audit/<slug>
python -m scripts.local_audit.pulls serp       --config <cfg> --out workspace/local-audit/<slug>
python -m scripts.local_audit.pulls maps       --config <cfg> --out workspace/local-audit/<slug>
python -m scripts.local_audit.pulls listings   --config <cfg> --out workspace/local-audit/<slug>
python -m scripts.local_audit.pulls reviews    --config <cfg> --out workspace/local-audit/<slug>
python -m scripts.local_audit.pulls crawl      --config <cfg> --out workspace/local-audit/<slug>
python -m scripts.local_audit.pulls backlinks  --config <cfg> --out workspace/local-audit/<slug>
python -m scripts.local_audit.pulls ai         --config <cfg> --out workspace/local-audit/<slug>
python -m scripts.local_audit.pulls lighthouse --config <cfg> --out workspace/local-audit/<slug>
python -m scripts.local_audit.pulls reviews --collect --config <cfg> --out workspace/local-audit/<slug>
python -m scripts.local_audit.pulls crawl   --collect --config <cfg> --out workspace/local-audit/<slug>
```

Then read `local-audit/*.json` summaries. Verify every business an AI assistant recommends and every competitor positioning claim against that business's own site before repeating it.

## Phase 3: Direct checks

1. `python -m scripts.local_audit.checks all --config <cfg> --out workspace/local-audit/<slug>` — real-browser access (HTTP 406 to older phones and in-app browsers), asset weight and animated WebP, email SPF/DKIM/DMARC, store catalog and policy pages.
2. In a browser: mobile screenshots at 390×844 with an overflow probe; store shipping quotes from a throwaway cart (1, 2, 3–6 units, add-ons, local and far ZIPs), then empty the cart; order and contact forms (fields, labels, what happens next — do not submit); Instagram and partner-account follower counts and post dates; Facebook About contact details; Meta Ad Library; Yelp and TripAdvisor presence; brand-name knowledge panel.
3. Save screenshots and quotes under `workspace/local-audit/<slug>/raw/` and list them in `_data-sources.md`.

Do not log in, follow, like, message, submit forms, or place orders.

## Phase 3b: Connected analytics (when a token exists)

`python -m scripts.local_audit.matomo --config <cfg> --out workspace/local-audit/<slug>` (Matomo; GA4 comes from `scripts.audit.collect --ga4`). Report the cleaned real-visit count, name every noise bucket, and list any host reporting in that is not the live site. Declare `onboarding_connected` for this section. Analytics cannot see visitors the site blocks, so it never overrides the access test.

## Phase 4: Write the report

Structure and section list: playbook §4. Required:

1. **Start here · this week** — 3–5 actions with the exact URL, number, setting or line of code.
2. **Headline findings** ordered by revenue impact; scorecard 0–5 per area.
3. Evidence sections with source footers.
4. **Offers** — `/kai-offer-builder` doctrine; seven slots; prices built on the measured shipping and fees; every price marked as a proposal to check against costs.
5. **Changes** — by owner: code, copy (all languages), commerce admin, Google Business Profile, DNS, social and partner asks.
6. **12-week plan** — starts next Monday; owner and developer columns; "done when"; seasonal peaks from the volume pull; targets table with the re-run date.
7. **Phone and follow-up** — KaiCalls Fit Rule: disclose that KaiCalls is Kai-owned, compare alternatives, and say plainly when it is not the first fix.

Write in the house voice: no announced lists, no dramatic fragments, no "not X but Y". Render as a single self-contained HTML page (`/kai-html-presentation` or the house strategy-page format) with `noindex,nofollow,noarchive` if it will be hosted.

## Phase 5: Localize and translate (when asked)

- **Localized rerun:** playbook §5. Add a market section after the headlines and patch the plan and targets.
- **Bilingual:** playbook §6. Parallel chunk translation with one brief and glossary, tag-signature comparison, language subpath and toggle.

## Phase 6: Gate and hand off

```bash
python scripts/quality_gates/audit_provenance_lint.py workspace/local-audit/<slug> --audit-dir
python scripts/quality_gates/banned_word_check.py workspace/local-audit/<slug>/report.html
```

Check the rendered page at 390 px and 1280 px (no overflow outside table wrappers, all images loaded, no duplicate ids or dead anchors). ECO work type `audit-report` (E3/C4/O1): the targets table is the O1 baseline, measured by re-running the same pulls on the stated date.

## Output

```text
workspace/local-audit/<slug>/
├── config.json
├── audit-data.json, kai-data.json, _data-sources.md, _data-gaps.md
├── raw/                 # API responses, direct-check artifacts, screenshots, shipping quotes
├── local-audit/         # per-pull summaries
├── report.html          # owner-facing audit + offers + changes + 12-week plan
└── <lang>/report.html   # translated sibling, when requested
```
