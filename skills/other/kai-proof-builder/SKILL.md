---
name: kai-proof-builder
description: Build and maintain a provenance-clean proof library — inventory every real proof asset (analytics, reviews, permitted testimonials, case studies, press, certifications), categorize it, rewrite each cleared item in 3 lengths, fuse top assets with narrative, and gate everything through FTC testimonial rules before it can ship. Use when "proof library", "gather our proof", "authority builder", "collect testimonials", "social proof assets", "proof points for the sales page", "what results can we claim", or any request to assemble evidence for marketing claims. NEVER invents proof — missing proof is reported as a gap.
---

Build a proof library where every asset has a source, a permission status, and a readiness verdict. The rule that makes this skill different from the viral "authority builder" prompt: **proof is collected, never composed. If it can't be traced to a real source, it doesn't exist.**

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

Also load before starting:
- `harness/references/audit-data-provenance.md` (data modes, source tiers, hard rules)
- `knowledge/people/alex-hormozi-knowledge.md` (Value Equation and proof mechanics — Phase 2 depends on it)
- `memory/lessons.md` (unsourced-claim history)

---

## Phase 1: Proof Inventory Sweep

Enumerate **real** proof sources only. Ask the user which of these exist and where; check connected tools and the repo before asking.

| Source class | Where to look | Tier (per audit-data-provenance.md) |
|--------------|---------------|-------------------------------------|
| Analytics exports | GA4/GSC exports, dashboards, `data/` files the client provides | 1 (connected) or 3 (user-provided) |
| Review platforms | Google reviews, G2, Trustpilot, app stores — captured via collector or screenshot | 1-2 |
| Testimonials | Emails, DMs, survey responses, call transcripts — **written permission required to use with a name** | 3 |
| Case studies | `/kai-case-study` output in `workspace/` — hand off there if none exist yet | 3 |
| Press mentions | Live URLs, archived captures | 2 |
| Certifications / credentials | Certificates, license numbers, partner-program listings | 2-3 |
| Usage stats | The client's own systems: billing, CRM, product database queries they run | 1 or 3 |

**Run the collector** for anything public or quantitative (review counts, rankings, traffic, visible press):

```bash
python -m scripts.audit.collect --url https://<domain> --mode <sales_external|onboarding_connected> --workflow proof-builder --out workspace/proof-library/_data
```

Declare the mode before writing anything (`sales_external` by default; `onboarding_connected` only with confirmed access; `internal_demo` must be labeled sample data everywhere it appears). Read `kai-data.json` from the output folder.

**Every item gets a provenance row** in `workspace/proof-library/_provenance.md`:

| ID | Asset (one line) | Source class | Source location (file/URL/system + date) | Source tier | Permission status | Verification method | Readiness |
|----|------------------|--------------|------------------------------------------|-------------|-------------------|--------------------|-----------|
| P-001 | "Organic clicks up 42% in 90 days" | Analytics export | `_data/kai-data.json` §gsc, 2026-07-10 | 1 | n/a (own data) | Collector output | pending |
| P-002 | Testimonial — Jane D. | Testimonial | email 2026-05-02, forwarded by client | 3 | needs-permission | Written email on file? → verify | pending |

Hard rules for this phase:
- A quote without a locatable source (file, URL, transcript timestamp, email date) is not inventory — it is a gap.
- A number the user "remembers" is Tier 4 until they produce the export. Record it as a gap with a note of who can supply it.
- NEVER fill thin categories with plausible-sounding entries. Log every hole in `workspace/proof-library/_data-gaps.md` with: what's missing, why it matters, who/what can supply it.
- Missing proof is itself a finding. "No usable transformation proof exists — recommend running `/kai-case-study` with the two clients named in the CRM export" is a valid, useful output of this skill.

## Phase 2: Categorize (Value Equation mapping)

Ground categories in what `knowledge/people/alex-hormozi-knowledge.md` actually says. Proof's job in the Value Equation is raising **Perceived Likelihood of Achievement** — the prospect's belief that *they specifically* will get the result ("not just 'this works' but 'this will work FOR ME'"). Third-party validation (reviews, case studies) is more credible than first-person claims. Sort every provenance row into one:

| Category | What it is | Value Equation lever |
|----------|-----------|----------------------|
| **Quantitative** | Measured numbers: metrics, review counts, usage stats | Perceived Likelihood — specific numbers beat adjectives |
| **Qualitative** | Testimonials and reviews in the customer's own words | Perceived Likelihood via similarity — prospect sees someone like them |
| **Transformation** | Before → after arcs (case studies, documented journeys) | Dream Outcome made concrete + Perceived Likelihood; Hormozi frames dream outcome as status elevation — how *others will perceive* the achievement |
| **Authority** | Credentials, certifications, press, expert standing | Perceived Likelihood via source credibility. FTC note: anyone presented as an expert must actually hold the relevant qualifications |

Two more Hormozi mechanics to apply while sorting:
- **"Proof over claims."** In the Give-Away-Everything model, demonstrated work is itself proof of competence — published frameworks, teardowns, and free tools belong in the Authority column when they exist. Don't claim expertise the library can demonstrate.
- **The testimonial flywheel:** premium clients → better results → testimonials that justify the premium (the virtuous cycle from the pricing philosophy section). Transformation assets are the highest-value category; if it's empty, say so in `_data-gaps.md` and recommend the `/kai-case-study` pipeline.

Guarantees and risk reversal also raise Perceived Likelihood, but they are offer mechanics, not proof assets — hand off to `/kai-offer-builder`.

## Phase 3: Rewrite in 3 Lengths (numbers and quotes frozen)

For each row marked Tier 1-3 with permission resolved, produce three renderings:

1. **Stat line** (≤ 20 words) — for ads, headers, social proof bars
2. **Short blurb** (40-80 words) — for landing page sections, email, sales decks
3. **Full story** (200-400 words) — for case-study callouts, long-form pages

Non-negotiable rewrite rules:
- **No number changes.** Not rounded up, not "nearly," not annualized, not extrapolated. The number in the rendering must equal the number in the source.
- **Direct quotes stay verbatim and attributed.** Ellipses may shorten a quote only if the meaning is unchanged; never splice two quotes into one. Attribution matches the permission status (named / first-name / anonymized).
- No superlatives ("best," "#1," "fastest") unless a Tier 1-2 source substantiates that exact comparative claim.
- Each rendering carries its provenance ID in an HTML comment: `<!-- proof: P-001 -->`.

Write to `workspace/proof-library/<category>/<id>-<slug>.md` (all three lengths in one file). Single-piece polish beyond this is `/kai-write`'s job; distribution across channels is `/kai-repurpose`'s.

## Phase 4: Proof-Story Fusion (top assets only)

Pick the 3-5 strongest cleared assets (prefer Transformation and Quantitative with named permission). Pair each with narrative — logic + emotion, the case-study arc from `/kai-case-study`: before state in the customer's words → turning point → measured after state.

Fusion integrity rule — mark every sentence in the story as one of:
- `[S]` sourced — traceable to the provenance row, transcript, or export
- `[C]` connective tissue — transitions and framing the writer added

`[C]` sentences may set scene and connect facts. They may NOT add events, feelings the customer never expressed, dialogue, or implied metrics. If the story only works because of an invented detail, the story is not ready — log what's missing (usually: a follow-up question for the customer) in `_data-gaps.md`.

Write to `workspace/proof-library/fusion/<id>-story.md` with the `[S]`/`[C]` markup in a review copy and a clean copy below it.

## Phase 5: Compliance Gate (FTC testimonial/endorsement rules)

Load `harness/references/advertising-compliance.md` (§1 Endorsement & Disclosure Rules, §2 Truth in Advertising & Substantiation, §10 Fake Reviews Rule) and `harness/references/creator-disclosure.md`. Check every asset:

1. **Genuine and current** — testimonials must reflect the endorser's genuine, current experience. Stale results (product changed, customer churned) get flagged for re-verification.
2. **Typical results** — if a featured result is atypical, the rendering must disclose what typical consumers achieve. "Results not typical" alone is NOT sufficient — state the typical outcome, sourced from Tier 1-3 data. If no typical-results data exists, the atypical claim is blocked, not disclaimed around.
3. **Material connection disclosure** — payment, free product, affiliate, employment, or family relationship with any endorser must be disclosed clearly and BEFORE or alongside the endorsement, never buried (16 CFR Part 255). Per-channel disclosure formats: `harness/references/creator-disclosure.md`.
4. **No unsubstantiated superlatives** — comparative and superiority claims need real substantiation; anecdotal/testimonial evidence is never sufficient substantiation for an objective product claim.
5. **Fake Reviews Rule** — no purchased, incentivized-without-disclosure, insider, or AI-fabricated reviews anywhere in the library. If provenance can't rule this out for a review source, the asset is blocked.
6. **Expert framing** — any asset presenting someone as an expert requires verified qualifications in the provenance row.

Then run the standard gates on every rendered file:

```bash
python scripts/quality_gates/four_us_score.py --file <file>    # 12/16 full stories & fusion pieces; 10/16 stat lines & blurbs
python scripts/quality_gates/banned_word_check.py --file <file> # zero violations
```

Max 2 retry cycles, fixing only the named failure. After 2 failures, escalate to a human with specifics and log the diagnosis per `memory/lessons.md` doctrine.

## Phase 6: Publish-Readiness Ledger

Set the Readiness column in `_provenance.md` for every row:

| Verdict | Meaning |
|---------|---------|
| `cleared` | Source verified, permission on file, compliance gate passed — usable by other skills |
| `needs-permission` | Real asset, but written permission (or typical-results data, or disclosure language) is outstanding — list exactly what's needed and from whom |
| `blocked` | Unverifiable source, failed compliance, permission refused, or fabrication risk — do not use; state why |

Rules:
- **Anything not `cleared` NEVER ships.** Downstream skills (`/kai-landing-page`, `/kai-social`, `/kai-write`, `/kai-brief`) may only pull assets marked `cleared`, referenced by provenance ID.
- End with a summary block: counts per verdict, top gaps from `_data-gaps.md`, and the single highest-value next action (e.g., "get written permission from the P-002 customer — strongest transformation asset in the library").
- **Approval doctrine:** this skill builds a library; it does not publish. Any use of a cleared asset on a live channel goes through `/kai-gate` and human approval first. Permission requests to customers are drafted for the human to send — never sent autonomously.

## Output

```
workspace/proof-library/
├── _provenance.md          # Ledger: every asset, source, tier, permission, verification, readiness
├── _data-gaps.md           # Missing proof, unverifiable claims, outstanding permissions — never guessed
├── _data/                  # Collector output (kai-data.json) from scripts.audit.collect
├── quantitative/           # <id>-<slug>.md — 3 lengths each
├── qualitative/
├── transformation/
├── authority/
├── fusion/                 # Top-asset proof stories with [S]/[C] markup
└── _quality-report.md      # Gate scores, compliance checklist results, retry log
```

Maintenance: re-run Phase 1 quarterly or after any product/pricing change; recheck `cleared` testimonials for currency (Phase 5 rule 1). New wins land here first, then feed `/kai-case-study` and `knowledge/playbooks/what-works.md`.
