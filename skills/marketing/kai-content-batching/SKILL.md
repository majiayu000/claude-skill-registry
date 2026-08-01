---
name: kai-content-batching
description: Turn a brand's positioning into a 30-day, multi-platform content batch — 3-7 pillars, subtopic matrix mapped to funnel stage and persona, pillar pieces plus derivative fan-out, proof elements in at least half the slots, all registered in the editorial calendar store and quality-gated. Use when "content batch", "batch my content", "30 days of content", "month of content", "content batching machine", "content pillars", "fill the content calendar", "plan a month of posts", or any request to produce a full month of multi-platform content in one run.
---

Turn positioning into a 30-day, gated, proof-loaded content batch. Pillars → subtopics → pillar pieces → derivatives → calendar.

**Scope boundaries:** `/kai-content-calendar` plans blog/SEO calendars; `/kai-social` batches social-only; `/kai-write` writes one piece; `/kai-repurpose` fans one pillar into 15-25 derivatives. This skill orchestrates all of them into one 30-day multi-platform batch. Hand off instead of duplicating.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Extract Content Pillars (3-7)

Load before extracting:
- `MARKETING.md` — positioning, ICP, value prop, channels
- `knowledge/playbooks/what-works.md` — measured winners; pillars should extend proven angles
- `memory/what-doesnt-work.md` — **banned angles.** Any pillar or hook style logged there is excluded (e.g., binary-contrast "It's not X, it's Y" hooks; study percentages reframed as promises)
- `knowledge/people/alex-hormozi-knowledge.md` — "Content Strategy: Give Away Everything" section

Apply the **Give-Away-Everything model**: give away the secrets, sell the implementation. Only ~1% of consumers implement free content themselves; the other 99% are the buyers. The content IS the proof of competence — trust, not information, is the bottleneck. So pillars must teach the actual method, not tease it.

Derive 3-7 pillars using Hormozi's five working categories as the starting grid, then keep only the ones the brand can own:
1. **Own frameworks** — the brand's IP, step-by-step
2. **Common mistakes** — what the ICP gets wrong (contrast positioning)
3. **Counterintuitive takes** — challenge consensus (attention)
4. **Behind-the-scenes** — real work, real results (trust; requires proof inventory, Phase 4)
5. **Q&A / implementation replays** — giving away implementation in real time

Test each candidate pillar against the **Value Equation** (Value = (Dream Outcome × Perceived Likelihood of Achievement) ÷ (Time Delay × Effort & Sacrifice)): a pillar earns its slot only if its content raises the ICP's perceived likelihood of the dream outcome or cuts their time/effort. Pillars that only describe the product fail this test — cut them.

Write `workspace/content-batch/_pillars.md`: pillar name, category, ICP pain it maps to, Value Equation variable it moves, winner evidence (cite the `what-works.md` entry or mark "unproven — new bet"), and any excluded angles with the `what-doesnt-work.md` line that banned them.

## Phase 2: Subtopic Matrix (8-10 per pillar)

Load `knowledge/personas/_persona-index.md` and pick 1-2 primary personas per pillar (use its industry/pain selection tables). Then expand each pillar into 8-10 subtopics, each tagged:

| Field | Values |
|-------|--------|
| Funnel stage | TOFU (problem-aware) / MOFU (solution-aware) / BOFU (product-aware) |
| Persona | one of the 8 (or null for pure SEO informational) |
| Primary format | blog, linkedin-article, email, video script, social post, etc. |
| Channel(s) | verify the guide exists in `knowledge/channels/` before assigning — e.g. `knowledge/channels/linkedin-organic.md`, `knowledge/channels/twitter-x.md`, `knowledge/channels/instagram.md`, `knowledge/channels/tiktok-algorithm.md`, `knowledge/channels/email-lifecycle.md`, `knowledge/channels/youtube.md`, `knowledge/channels/seo-content.md`, `knowledge/channels/newsletter-strategy.md` |
| Proof slot? | yes/no (Phase 4 fills these) |

Stage mix follows Give-Away-Everything economics: **TOFU/MOFU give the full method** (framework breakdowns, mistakes, takes); **BOFU sells implementation** (case studies, offer-adjacent pieces). Default to roughly 60/25/15 TOFU/MOFU/BOFU — a planning default, not a measured benchmark; shift it if `what-works.md` evidence points elsewhere. For BOFU pieces that touch the offer itself, load `knowledge/playbooks/funnel-hack-offer-architecture.md` — offer mechanics come from sourced funnel evidence, not invented claims, and any Grand Slam Offer framing ("so good the prospect feels stupid saying no") must describe the brand's real, documented offer.

If subtopics need live keyword/SERP grounding, hand keyword research to `/kai-topical-map` or `/kai-content-calendar` rather than guessing volumes.

Write `workspace/content-batch/_subtopic-matrix.md` (one table per pillar).

## Phase 3: Pillar Production and Derivative Fan-Out

Per `knowledge/playbooks/content-repurposing.md`, one strong pillar yields 15-25 assets — Hormozi runs the same math as 1 recording → 4+ long-form episodes → 40-80 clips. Per `knowledge/playbooks/content-publication-velocity.md`, complete a segment before expecting results — finish one pillar's cluster before scattering across all of them.

1. **Select 4-5 pillar pieces** for the 30 days (about one per week), one per pillar, choosing the subtopic with the strongest winner evidence first.
2. **Brief each** via `/kai-brief` (schema: `harness/brief-schema.md`) — persona, angle, keyword, format from the matrix row.
3. **Produce each pillar piece** — hand off to `/kai-write`. It loads the right framework and skill contract itself; do not respecify them here. Write pillars repurposing-ready: self-contained H2 sections, standalone data points, quotable frameworks.
4. **Fan out each gated pillar** — hand off to `/kai-repurpose`. Do NOT respecify derivative formats, counts, or platform adaptations here; that skill owns the extraction map and the 15-25 asset set. Pass it the platform list from the Phase 2 matrix and the proof-slot flags from Phase 4.

4-5 pillars × 15-25 derivatives comfortably covers 30+ daily slots across platforms.

## Phase 4: Proof-Loop Injection

Target: **at least half of all calendar slots carry a proof element** (result, named example, screenshot, review, case study, before/after). Hormozi's rule — proof over claims; behind-the-scenes transparency is a pillar category, not decoration.

Every proof element must come from a **real proof inventory**:

1. If `workspace/proof-library/` exists (output of a prior `/kai-proof-builder` run), load it and use only entries with sources.
2. If it does not exist, build `workspace/content-batch/_proof-inventory.md` from real sources only:
   - `data/content_log.json` 30-day winners (runtime log — absent on a fresh clone) and `knowledge/playbooks/what-works.md` entries
   - existing case studies in `workspace/` (or produce new ones via `/kai-case-study` — interviews/data required, that skill owns the format)
   - live public data (reviews, rankings, mentions): load `harness/references/audit-data-provenance.md`, then run `python -m scripts.audit.collect --url <url> --mode <mode> --workflow content-batching --out workspace/content-batch/data/` and cite the collector output for every number.
3. Each inventory row: proof claim, source (file path, collector artifact, or approved customer quote with permission status), and which calendar slots use it.
4. **Missing proof goes in `workspace/content-batch/_data-gaps.md`, never invented.** No fabricated testimonials, review counts, revenue numbers, or "top pains from Reddit" without a real listening run (`/kai-reddit-listen`). If the inventory cannot cover half the slots, fill the shortfall with framework/mistake content and log the gap — a thin proof month is a finding, not a failure to hide.

## Phase 5: Assemble the 30-Day Calendar and Register It

Build `workspace/content-batch/_calendar-30day.md`: date × slot table with title, pillar, format, channel, persona, funnel stage, proof element (or "—"), and asset path. Sequence per the repurposing playbook's weekly workflow: lead each week with the pillar piece on its highest-reach channel, then roll that pillar's derivatives out across the rest of the week (playbook cadence: pillar Monday, clips/email/visuals/community posts Tuesday-Friday).

Register every slot in the editorial calendar store (verified against `scripts/campaigns/calendar.py`):

```bash
python scripts/campaigns/calendar.py --add --site <brand> \
  --title "<slot title>" --publish-at 2026-08-04T14:00Z \
  --format <blog|linkedin-article|email|social|...> \
  --keyword "<target keyword or empty>" --persona <persona-or-omit> \
  --notes "pillar=<pillar-slug>; proof=<inventory-row-or-none>"
# verify:
python scripts/campaigns/calendar.py --list --status planned --site <brand>
```

`--add` requires `--site`, `--title`, and `--publish-at` (ISO 8601, UTC assumed if naive). Items land as `planned`; the agent loop's hourly `editorial_calendar_tick` turns due items into drafts that flow through the normal gate + approval pipeline. Add `--campaign-id` if the batch belongs to a tracked campaign (`scripts/campaigns/campaign_tracker.py`).

**Approval doctrine:** registering `planned` items schedules draft generation only. Nothing publishes or posts to a live channel without explicit human approval; the store itself never sets `published` without a human-in-the-loop publish.

## Phase 6: Gate Every Asset

No asset enters the calendar ungated. Run on every finished piece (or hand the batch to `/kai-gate`):

```bash
python scripts/quality_gates/four_us_score.py --file <file>          # 12/16 publishing; 10/16 ads, email, hooks
python scripts/quality_gates/banned_word_check.py --file <file>      # Tier 1 = instant reject
python scripts/quality_gates/seo_lint.py --file <file> --keyword "<target keyword>"  # SEO/blog pieces only
```

Max 2 retry cycles per asset; fix only the named failing dimension, never rewrite the whole draft (see `memory/lessons.md`). After 2 failures, mark the slot `skipped` in the calendar store with the diagnosis in `--notes`, escalate to a human, and log repeated diagnoses to `memory/lessons.md`.

Write `workspace/content-batch/_gate-report.md`: per-asset scores, retries, escalations, and the proof-coverage ratio (proof slots ÷ total slots — must be ≥ 0.5 or explained in `_data-gaps.md`).

## Output

```
workspace/content-batch/
├── _pillars.md               # 3-7 pillars, Value Equation test, banned-angle exclusions
├── _subtopic-matrix.md       # 8-10 subtopics per pillar × stage × persona × channel
├── _proof-inventory.md       # sourced proof elements (or pointer to workspace/proof-library/)
├── _data-gaps.md             # missing proof/data — logged, never guessed
├── _calendar-30day.md        # the 30-day slot table + calendar store item ids
├── _gate-report.md           # gate scores, retries, proof-coverage ratio
├── data/                     # scripts.audit.collect artifacts (if live data pulled)
├── pillars/                  # /kai-write output, one file per pillar piece
└── derivatives/              # /kai-repurpose output trees, one folder per pillar
```

Done means: pillars grounded in winners, zero banned angles, every asset gated, ≥50% proof coverage (or gap-logged), all slots `planned` in the calendar store, and nothing live-published without human approval.
