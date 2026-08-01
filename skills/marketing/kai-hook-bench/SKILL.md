---
name: kai-hook-bench
description: Generate, rank, and gate a reusable hook bank — sourced pains × named hook formula families, scored on clarity/specificity/curiosity/proof-backing, gated at the 10/16 ad threshold, delivered in 3 lengths with per-hook provenance and downstream routing. Use when "hook bank", "generate hooks", "hook generator", "write hooks for", "ad hooks", "scroll stoppers", "opening lines", "hook ideas", "first 3 seconds", "hook matrix", "I need 50 hooks", or any request to batch-produce attention-openers for ads, social, or video.
---

Build a ranked, provenance-tagged hook bank: sourced pains × formula families → score → gate → route. Hooks matching a known loser pattern are rejected at birth.

**Scope boundaries:** this skill produces the hook bank only. `/kai-social` batches full social posts, `/kai-ad-campaign` builds full ad campaigns, `/kai-write` writes single finished pieces, `/kai-repurpose` fans a pillar into derivatives — they *consume* this bank. Concept-level portfolio strategy (Persona × Desire × Angle bench, budgets, kill rules) belongs to `knowledge/playbooks/combinatorial-creative-bench.md` via `/kai-ad-campaign`; this skill fills the `hook` field of those bench rows.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Load Inputs (pains, personas, winners, losers, proof)

Load all five before generating anything:

1. **Personas** — `knowledge/personas/_persona-index.md`. Pick 1-3 personas via its industry/pain tables (or the client's own from `MARKETING.md`). Note each persona's evidence status; `hypothesis` personas are fine for hook ideation but flag them in provenance.
2. **Sourced pains** — if `workspace/offer-builder/pain-table.md` exists (output of `/kai-offer-builder` Phase 1), use it: every row already has a source column. If it does NOT exist, mine pains with sources — load `harness/references/audit-data-provenance.md`, then:
   ```bash
   python -m scripts.audit.collect --url <business-url> --mode sales_external --workflow hook-bench --out workspace/hook-bench/data
   ```
   plus, where available: Reddit digests (hand off to `/kai-reddit-listen` if no profile exists in `scripts/reddit_monitor/profiles/`), user-provided call notes/reviews (cite file path), explicit WebSearch (URL + retrieval date), or `python scripts/intel/brand_pulse.py <brand> --domain <domain>`. Write `workspace/hook-bench/pain-inputs.md` with the same columns as the offer-builder pain table. **No source, no row.** Never invent "top pains from Reddit", review counts, or frequency percentages. Unsourceable pains go in `workspace/hook-bench/_data-gaps.md`.
3. **Winners** — `knowledge/playbooks/what-works.md`. If it has entries, note which hook styles won; new hooks should extend proven angles first. If empty (fresh install), record "no winners yet — all hooks are experiments" in provenance.
4. **Anti-patterns (rejection list)** — `memory/what-doesnt-work.md` + `memory/lessons.md`. Build `workspace/hook-bench/rejection-rules.md`: one row per banned pattern with the memory line that banned it. Seed rules currently in memory: the binary-contrast construction ("It's not X, it's Y" — reads as LinkedIn slop), and study percentages reframed as promises. Also load the voice-pattern regexes in `harness/skills/kai-gate/SKILL.md` step 3. **Any candidate hook matching a rejection rule is discarded at generation time**, logged to `workspace/hook-bench/rejects.md` with the rule that killed it — it never reaches ranking.
5. **Proof inventory** — proof-led hooks may only cite proof that exists on record. Use, in order: `workspace/proof-library/` if present (owned by `/kai-proof-builder` — hand off there to create or refresh it, don't rebuild it here); case studies already in `workspace/` (produce new ones via `/kai-case-study`); `data/content_log.json` 30-day winners; collector output from step 2. Write `workspace/hook-bench/_proof-inventory.md`: claim, source path/URL, permission status. An empty inventory is a finding (log it in `_data-gaps.md`), not a license to fabricate testimonials or numbers.

Log every source in `workspace/hook-bench/_sources.md` (URL/path, method, retrieval date).

## Phase 2: Hook Formula Library

Load the three mechanics sources and extract the mechanics they state — no vague gestures:

- `knowledge/people/alex-hormozi-knowledge.md` — the hook mechanics live in "$100M Leads": the **Hook–Retain–Reward** content formula (hook = bold claim, counterintuitive statement, or direct problem identification; retain = unresolved questions, storytelling, cliffhangers), the paid-ads rule (**hook in first 3 seconds, appeal to identity or location**, then Problem-Agitation-Solution body), and the **lead magnet naming formula** (`[Number] + [Adjective] + [Target Audience] + [Desired Outcome] + [Timeframe]`). From the same doc's other sections: the **Value Equation** (Dream Outcome × Perceived Likelihood of Achievement ÷ Time Delay × Effort & Sacrifice), the five content pillar categories (business frameworks/own IP, common mistakes, counterintuitive takes, behind-the-scenes, Q&A and consulting replays), the CLOSER "S" step ("Sell the Vacation, Not the Plane Flight"), and "People don't buy products. They buy certainty of outcomes."
- `knowledge/playbooks/ad-creative-best-practices.md` — the 3-Second Rule, the `hook_type` taxonomy (problem, proof, mechanism, contrast, offer, story, pattern interrupt), and the PAS/AIDA/BAB copy formulas.
- `knowledge/playbooks/combinatorial-creative-bench.md` — angle types (loss-aversion, social proof, mechanism, contrast, time math) and the rule that a hook is an *execution* variable inside a P.D.A. concept.

Organize into these **seven formula families** (each is supported by the sources above — cite the exact section per family in the library file):

| Family | Mechanism | Grounding |
|--------|-----------|-----------|
| `pain-callout` | Name the specific sourced pain in the reader's language | Hormozi "direct problem identification"; PAS Pain step; persona-index hook lines |
| `identity-callout` | Name who this is for so the persona is obvious in 3 seconds | Hormozi paid-ads hook rule ("appeal to identity or location"); bench persona-clarity score |
| `dream-outcome` | Lead with the vivid destination, status-aware, not the feature | Value Equation numerator; CLOSER "sell the vacation"; BAB After step |
| `proof-led` | Open with a real result, demo, or named example | "Certainty of outcomes"; `hook_type: proof`; TikTok proof-first hook (`knowledge/channels/tiktok-algorithm.md`) |
| `curiosity-gap` | Bold or counterintuitive claim that opens an unresolved question | Hormozi content pillar "counterintuitive takes" + Retain mechanics; AIDA Attention |
| `common-mistake` | Contrast what the ICP does wrong with what works | Hormozi content pillar "common mistakes"; `hook_type: contrast`; bench contrast angle |
| `speed-effort` | Collapse the Value Equation denominator: outcome + timeframe + low effort | Lead magnet naming formula; MAGIC Interval; Time Delay / Effort & Sacrifice variables |

Write `workspace/hook-bench/formula-library.md`: per family — mechanism, 2-3 fill-in patterns, source citation, and known failure mode (e.g. `common-mistake` degenerates into the banned binary-contrast cliché; `curiosity-gap` degenerates into clickbait that the body can't reward; `speed-effort` degenerates into unsubstantiated timeframe claims, which fail the compliance pass).

## Phase 3: Generation Matrix

Generate `N` hooks per **pain × family** cell (default N=2; take the top 5 pains by frequency signal → up to 70 candidates). For each candidate record: `hook_id` (`HB-{pain#}-{family}-{nn}`), pain row ref, persona, family, draft text, proof ref (or `none`), target platforms.

Rules at generation time:

- **Reject at birth**: run every candidate against `rejection-rules.md` and the kai-gate voice regexes before it enters the matrix. Log kills to `rejects.md`.
- **Quantitative claims** ("booked 40 calls", "took 6 weeks") only from `_proof-inventory.md` or Phase 1 sourced data — otherwise rewrite qualitative or drop.
- **Platform ceilings** (verified against the cited files — respect the tightest ceiling of the hook's target platforms):

| Surface | Constraint | Source |
|---------|-----------|--------|
| X standard post | 280 chars total | `knowledge/channels/twitter-x.md` |
| LinkedIn post | hook lands in first ~210 chars (mobile "...see more" fold) | `knowledge/channels/linkedin-organic.md` |
| Meta ads | primary text 125 chars recommended; headline 40 chars | `knowledge/playbooks/ad-creative-best-practices.md` |
| TikTok | visual hook in first 0.7-2s, must work on mute; ad text 100 chars | `knowledge/channels/tiktok-algorithm.md`; `knowledge/playbooks/ad-creative-best-practices.md` |
| Google Search ads | headline 30 chars | `knowledge/playbooks/ad-creative-best-practices.md` |

Write the full matrix to `workspace/hook-bench/generation-matrix.md`.

## Phase 4: Ranking + Gate

**4a. Rubric.** Score every surviving candidate 0-2 per dimension (0 = fails, 1 = weak, 2 = strong):

| Dimension | 2 means |
|-----------|---------|
| Clarity | Understood in one read, works out of context, no setup needed |
| Specificity | Named persona/situation/number — could not be about any product |
| Curiosity | Opens a question the reader needs the next line to close |
| Proof-backing | Claim is backed by an `_proof-inventory.md` row or sourced pain quote |

Hard rule: a `proof-led` hook with proof-backing 0 is cut or rewritten into another family — it may not ship as proof-led. Justify each score in a phrase, citing the pain row or proof ref. Rank by total (/8); ties break by winner-adjacency (Phase 1 step 3).

**4b. Gate the top set.** Take the top ~25-30 hooks into `hook-bank.md` (Phase 5 format), then run:

```bash
python scripts/quality_gates/four_us_score.py --file workspace/hook-bench/hook-bank.md    # 10/16 — ad/hook threshold
python scripts/quality_gates/banned_word_check.py --file workspace/hook-bench/hook-bank.md
```

Max 2 retry cycles; fix only the named failing dimension or word, never rewrite the bank (see `memory/lessons.md`). After 2 failures, escalate to a human with the diagnosis and log it via `python scripts/self_improvement/lesson_capture.py add`. Record scores, retries, and rubric table in `workspace/hook-bench/_gate-report.md`.

## Phase 5: Hook Bank Output

Write `workspace/hook-bench/hook-bank.md`, ranked. Each entry:

```
### #3 · HB-2-proof-led-01 (score 7/8)
- short  (overlay / one-liner, ≤ 60 chars — fits every ceiling above): "..."
- mid    (caption / primary text, ≤ 125 chars — Meta primary-text ceiling): "..."
- long   (opener, 1-3 sentences, ≤ 210 chars before the fold — LinkedIn/long-caption first lines): "..."
- provenance: pain #2 (source URL/path, date) · family: proof-led · proof: _proof-inventory.md row 4 · persona: Admin Martyr (directional)
- routing: /kai-ad-campaign (Meta TOF) · /kai-social (TikTok overlay)
```

The three lengths carry the same promise — same pain, same claim, no escalation of the claim as length grows.

**Routing notes** (append a routing table to the bank):

| Consumer | Use | They own |
|----------|-----|----------|
| `/kai-social` | short + mid as post/overlay openers | full post body, hashtags, schedule; contract `harness/skill-contracts/social-post.yaml` |
| `/kai-ad-campaign` | short as ad headline seed, mid as primary text seed, `hook_id` fills the bench row's hook field | platform policy check (per-platform table in `.claude/rules/architecture-and-memory.md` + `harness/references/ad-write-guardrails.md`), funnel mapping, upload |
| `/kai-write` | long as first-line/opener for single pieces (script, email, article) | framework, contract, full draft |

**Approval doctrine:** the bank is an internal asset — nothing here posts, uploads, or mutates a live channel. Downstream skills carry their own gates and human approval before anything ships.

**Feedback loop:** when downstream 30-day checks grade a hook-led piece, winners feed `knowledge/playbooks/what-works.md` automatically; graded underperformers get their hook family/pattern diagnosed into `memory/what-doesnt-work.md` via `/kai-retro`, which tightens `rejection-rules.md` on the next run.

## Output Tree

```
workspace/hook-bench/
├── _sources.md              # every source: URL/path, method, retrieval date
├── _data-gaps.md            # unsourceable pains, empty proof inventory, unknown metrics
├── _proof-inventory.md      # sourced proof rows (or pointer to workspace/proof-library/)
├── data/                    # scripts.audit.collect output (kai-data.json), if mined here
├── pain-inputs.md           # Phase 1 pains (only if workspace/offer-builder/pain-table.md absent)
├── rejection-rules.md       # anti-patterns from memory/ + kai-gate regexes
├── rejects.md               # hooks killed at birth, with the rule that killed each
├── formula-library.md       # Phase 2 — 7 families, patterns, citations, failure modes
├── generation-matrix.md     # Phase 3 — full pain × family candidate set
├── _gate-report.md          # Phase 4 — rubric scores, Four U's / banned-word results, retries
└── hook-bank.md             # Phase 5 — ranked bank, 3 lengths, provenance, routing
```

## Hand-offs (do not re-specify these jobs)

- Pains not yet mined → `/kai-offer-builder` Phase 1 (its pain table is this skill's preferred input)
- Proof library missing or stale → `/kai-proof-builder` · customer-story proof → `/kai-case-study`
- Ongoing pain listening → `/kai-reddit-listen`
- Hooks into posts → `/kai-social` · into ads → `/kai-ad-campaign` · into single pieces → `/kai-write` (brief first via `/kai-brief`)
- Independent re-gate of the bank → `/kai-gate`
- Diagnosing underperforming hooks after 30-day grades → `/kai-retro`
