---
name: kai-hook-bench
description: Generate, rank, and gate a reusable hook bank — sourced pains × named hook formula families, scored on clarity/specificity/curiosity/proof-backing, gated at the 10/16 ad threshold, delivered in 3 lengths with per-hook provenance and downstream routing. Use when "hook bank", "generate hooks", "hook generator", "write hooks for", "ad hooks", "scroll stoppers", "opening lines", "hook ideas", "first 3 seconds", "hook matrix", "I need 50 hooks", or any request to batch-produce attention-openers for ads, social, or video.
---

## Objective

A ranked, provenance-tagged hook bank that downstream skills can pull from without re-checking the claims: sourced pains crossed with named formula families, hooks matching a known loser pattern killed before they reach ranking, survivors scored and gated, and the top set delivered in three lengths with a source behind every claim. This skill produces the hook bank only. `/kai-social` batches full social posts, `/kai-ad-campaign` builds full ad campaigns, `/kai-write` writes single finished pieces, `/kai-repurpose` fans a pillar into derivatives — they *consume* this bank. Concept-level portfolio strategy (Persona × Desire × Angle bench, budgets, kill rules) belongs to `knowledge/playbooks/combinatorial-creative-bench.md` via `/kai-ad-campaign`; this skill fills the `hook` field of those bench rows.

## Done when

Work type `internal-research` — floor **E2/C2/O0** (`harness/eco-floors.yaml`). The bank is an internal asset; nothing here posts, uploads, or mutates a live channel, so SHIPPED is terminal and the outcome debt belongs to the consuming skill.

- **E2** — `hook-bank.md` exists and satisfies the declared structure: ranked, three lengths per hook, provenance line, routing line, plus the ledgers (`_sources.md`, `_data-gaps.md`, `_proof-inventory.md`, `rejection-rules.md`, `rejects.md`).
- **C2** — the declared gates pass at their thresholds, stricter than this work type's default: `four_us_score` at 10/16 and `banned_word_check` on the bank, plus every candidate run against the rejection rules and voice regexes.
- **O0** — no outcome obligation. Hook performance is graded when a downstream piece hits its 30-day check.

## Constraints

- **`MARKETING.md` first.** Read it from the project root before asking discovery questions. If it does not exist, build it from the codebase (CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config) using the template carried in `/kai-email-system`, and confirm the draft. Do not ask the user what the product is.
- **Five inputs load before anything is generated:**
  - **Personas** — from `knowledge/personas/_persona-index.md` (or the client's own in `MARKETING.md`), 1-3 picked via its industry/pain tables. Note each persona's evidence status; `hypothesis` personas are fine for ideation but get flagged in provenance.
  - **Sourced pains** — prefer `workspace/offer-builder/pain-table.md` if it exists (every row already carries a source). Otherwise mine pains with sources: load `harness/references/audit-data-provenance.md`, then
     ```bash
     python -m scripts.audit.collect --url <business-url> --mode sales_external --workflow hook-bench --out workspace/hook-bench/data
     ```
     plus, where available: Reddit digests (hand off to `/kai-reddit-listen` if no profile exists in `scripts/reddit_monitor/profiles/`), user-provided call notes or reviews (cite file path), explicit WebSearch (URL + retrieval date), or `python scripts/intel/brand_pulse.py <brand> --domain <domain>`. Write `workspace/hook-bench/pain-inputs.md` with the same columns as the offer-builder pain table.
  - **Winners** — `knowledge/playbooks/what-works.md`. Extend proven angles first. If empty, record "no winners yet — all hooks are experiments" in provenance.
  - **Rejection rules** — `memory/what-doesnt-work.md` + `memory/lessons.md`, one row per banned pattern with the memory line that banned it, written to `workspace/hook-bench/rejection-rules.md`. Seed rules currently in memory: the binary-contrast construction ("It's not X, it's Y" — reads as LinkedIn slop) and study percentages reframed as promises. Also load the voice-pattern regexes carried in `/kai-gate`.
  - **Proof inventory** — `workspace/hook-bench/_proof-inventory.md` with claim, source path/URL, and permission status. Sources in order: `workspace/proof-library/` if present (owned by `/kai-proof-builder` — hand off there rather than rebuilding it), case studies already in `workspace/` (new ones via `/kai-case-study`), `data/content_log.json` 30-day winners, collector output.
- **No source, no row.** Never invent "top pains from Reddit", review counts, or frequency percentages. Unsourceable pains go in `workspace/hook-bench/_data-gaps.md`. An empty proof inventory is a finding logged there, never a license to fabricate testimonials or numbers. Log every source in `workspace/hook-bench/_sources.md` (URL/path, method, retrieval date).
- **Reject at birth.** Every candidate runs against `rejection-rules.md` and the kai-gate voice regexes before it enters the matrix. Kills are logged to `workspace/hook-bench/rejects.md` with the rule that killed them; they never reach ranking. Quantitative claims ("booked 40 calls", "took 6 weeks") come only from `_proof-inventory.md` or sourced pain data — otherwise rewrite qualitative or drop.
- **A `proof-led` hook with proof-backing 0** is cut or rewritten into another family; it may not ship as proof-led.
- **Platform ceilings** — respect the tightest ceiling across a hook's target platforms:

  | Surface | Constraint | Source |
  |---------|-----------|--------|
  | X standard post | 280 chars total | `knowledge/channels/twitter-x.md` |
  | LinkedIn post | hook lands in first ~210 chars (mobile "...see more" fold) | `knowledge/channels/linkedin-organic.md` |
  | Meta ads | primary text 125 chars recommended; headline 40 chars | `knowledge/playbooks/ad-creative-best-practices.md` |
  | TikTok | visual hook in first 0.7-2s, must work on mute; ad text 100 chars | `knowledge/channels/tiktok-algorithm.md`; `knowledge/playbooks/ad-creative-best-practices.md` |
  | Google Search ads | headline 30 chars | `knowledge/playbooks/ad-creative-best-practices.md` |

- **Gate the top set** after writing it into `hook-bank.md`:
  ```bash
  python scripts/quality_gates/four_us_score.py --file workspace/hook-bench/hook-bank.md    # 10/16 — ad/hook threshold
  python scripts/quality_gates/banned_word_check.py --file workspace/hook-bench/hook-bank.md
  ```
  Max 2 retry cycles; fix only the named failing dimension or word rather than rewriting the bank (see `memory/lessons.md`). After 2 failures, escalate to a human with the diagnosis and log it via `python scripts/self_improvement/lesson_capture.py add`. Scores, retries, and the rubric table go in `workspace/hook-bench/_gate-report.md`.
- **Approval doctrine.** The bank is an internal asset. Nothing here posts, uploads, or mutates a live channel; downstream skills carry their own gates and human approval before anything ships.

## Context

| Need | Load |
|---|---|
| Hook–Retain–Reward, 3-second paid rule, lead-magnet naming formula, Value Equation, content pillars, CLOSER "sell the vacation" | `knowledge/people/alex-hormozi-knowledge.md` ("$100M Leads" and adjacent sections) |
| 3-Second Rule, `hook_type` taxonomy (problem, proof, mechanism, contrast, offer, story, pattern interrupt), PAS/AIDA/BAB | `knowledge/playbooks/ad-creative-best-practices.md` |
| Angle types and the rule that a hook is an execution variable inside a P.D.A. concept | `knowledge/playbooks/combinatorial-creative-bench.md` |
| Persona hook lines and evidence status | `knowledge/personas/_persona-index.md` |
| Provenance modes and gap handling | `harness/references/audit-data-provenance.md` |
| Ad policy before any hook becomes an ad | `.claude/rules/architecture-and-memory.md` + `harness/references/ad-write-guardrails.md` (owned by `/kai-ad-campaign`) |

**Seven formula families** — cite the exact source section per family in `formula-library.md`, with 2-3 fill-in patterns and the family's known failure mode:

| Family | Mechanism | Grounding |
|--------|-----------|-----------|
| `pain-callout` | Name the specific sourced pain in the reader's language | Hormozi "direct problem identification"; PAS Pain step; persona-index hook lines |
| `identity-callout` | Name who this is for so the persona is obvious in 3 seconds | Hormozi paid-ads hook rule ("appeal to identity or location"); bench persona-clarity score |
| `dream-outcome` | Lead with the vivid destination, status-aware, not the feature | Value Equation numerator; CLOSER "sell the vacation"; BAB After step |
| `proof-led` | Open with a real result, demo, or named example | "Certainty of outcomes"; `hook_type: proof`; TikTok proof-first hook (`knowledge/channels/tiktok-algorithm.md`) |
| `curiosity-gap` | Bold or counterintuitive claim that opens an unresolved question | Hormozi content pillar "counterintuitive takes" + Retain mechanics; AIDA Attention |
| `common-mistake` | Contrast what the ICP does wrong with what works | Hormozi content pillar "common mistakes"; `hook_type: contrast`; bench contrast angle |
| `speed-effort` | Collapse the Value Equation denominator: outcome + timeframe + low effort | Lead magnet naming formula; MAGIC Interval; Time Delay / Effort & Sacrifice variables |

Known degenerations to name per family: `common-mistake` collapses into the banned binary-contrast cliché; `curiosity-gap` into clickbait the body cannot reward; `speed-effort` into unsubstantiated timeframe claims that fail the compliance pass.

**Generation matrix.** `N` hooks per pain × family cell (default N=2; top 5 pains by frequency signal gives up to 70 candidates). Each candidate records `hook_id` (`HB-{pain#}-{family}-{nn}`), pain row ref, persona, family, draft text, proof ref (or `none`), and target platforms. **Ranking rubric:** 0-2 per dimension (0 = fails, 1 = weak, 2 = strong), ranked by total /8, ties broken by winner-adjacency, each score justified in a phrase citing the pain row or proof ref:

| Dimension | 2 means |
|-----------|---------|
| Clarity | Understood in one read, works out of context, no setup needed |
| Specificity | Named persona/situation/number — could not be about any product |
| Curiosity | Opens a question the reader needs the next line to close |
| Proof-backing | Claim is backed by an `_proof-inventory.md` row or sourced pain quote |

**Bank entry format** — the top ~25-30 hooks, ranked, each written as `### #3 · HB-2-proof-led-01 (score 7/8)` followed by five lines: `short` (overlay / one-liner, ≤ 60 chars — fits every ceiling above), `mid` (caption / primary text, ≤ 125 chars — Meta primary-text ceiling), `long` (opener, 1-3 sentences, ≤ 210 chars before the fold — LinkedIn/long-caption first lines), `provenance` (pain # with source URL/path and date · family · proof-inventory row · persona with evidence status), and `routing` (the consuming skill and placement, e.g. `/kai-ad-campaign` Meta TOF · `/kai-social` TikTok overlay). The three lengths carry the same promise — same pain, same claim, no escalation of the claim as length grows.

**Consumer routing** — append this table to the bank:

| Consumer | Use | They own |
|----------|-----|----------|
| `/kai-social` | short + mid as post/overlay openers | full post body, hashtags, schedule; contract `harness/skill-contracts/social-post.yaml` |
| `/kai-ad-campaign` | short as ad headline seed, mid as primary text seed, `hook_id` fills the bench row's hook field | platform policy check (per-platform table in `.claude/rules/architecture-and-memory.md` + `harness/references/ad-write-guardrails.md`), funnel mapping, upload |
| `/kai-write` | long as first-line/opener for single pieces (script, email, article) | framework, contract, full draft |

**Output** — `workspace/hook-bench/`: `_sources.md`, `_data-gaps.md`, `_proof-inventory.md`, `data/` (collector output, if mined here), `pain-inputs.md` (only when `workspace/offer-builder/pain-table.md` is absent), `rejection-rules.md`, `rejects.md`, `formula-library.md`, `generation-matrix.md`, `_gate-report.md`, `hook-bank.md`. **Hand-offs — do not re-specify these jobs:** pains not yet mined → `/kai-offer-builder` (its pain table is this skill's preferred input); proof library missing or stale → `/kai-proof-builder`, customer-story proof → `/kai-case-study`; ongoing pain listening → `/kai-reddit-listen`; hooks into posts → `/kai-social`, into ads → `/kai-ad-campaign`, into single pieces → `/kai-write` (brief first via `/kai-brief`); independent re-gate of the bank → `/kai-gate`; diagnosing underperforming hooks after 30-day grades → `/kai-retro`.

**Feedback loop.** When downstream 30-day checks grade a hook-led piece, winners feed `knowledge/playbooks/what-works.md` automatically; graded underperformers get their hook family or pattern diagnosed into `memory/what-doesnt-work.md` via `/kai-retro`, which tightens `rejection-rules.md` on the next run.

## Escalate when

- No pain can be sourced — the bank would be invention rather than generation.
- The proof inventory is empty but the request is specifically for proof-led hooks, or a hook the user wants makes a claim no source supports or a timeframe/results claim that would fail platform policy or advertising law.
- Two gate retries failed on the same dimension, or every candidate in a family dies to the rejection rules (the angle itself is a known loser).
