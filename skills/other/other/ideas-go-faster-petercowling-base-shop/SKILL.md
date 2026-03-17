---
name: ideas-go-faster
description: Radical business growth process auditor. Cabinet Secretary orchestrates multi-lens composite idea generation with attribution, confidence gating, and priority ranking.
---

# Ideas Go Faster — Cabinet Secretary

Cabinet Secretary orchestrates composite business idea generation across multiple expert lenses. Not a kanban health checker. Not a WIP counter. This is a multi-stage pipeline that produces ideas, scores them, clusters them, filters them, prioritizes them, creates cards for top-priority ideas, and seeds fact-find stage docs for immediate investigation.

Pete triggers the sweep via `/ideas-go-faster`. Everything after that is autonomous.

---

## Invocation

```
/ideas-go-faster                           # default: --stance=improve-data
/ideas-go-faster --stance=improve-data
/ideas-go-faster --stance=grow-business
/ideas-go-faster --dry-run                # preview-only: generate/report ideas, no API writes
/ideas-go-faster --dry-run --stance=grow-business
/ideas-go-faster --dry-run --allow-api-degraded   # allow filesystem-only fallback when API preflight fails
/ideas-go-faster --force-code-review       # force technical cabinet even without triggers
/ideas-go-faster --assumptions-file <path-to-md>  # optional assumptions input file
/ideas-go-faster --verbosity=compact|standard|extended
/ideas-go-faster --stage7b                 # enable optional Stage 7b single-card backfill slot
scripts/run-ideas-go-faster.sh --dry-run --stance=improve-data   # recommended runner (loads .env.local)
scripts/run-ideas-go-faster.sh --dry-run --allow-api-degraded --stance=improve-data
```

**Invocation control contract:**
- Assumptions input supports both:
  - inline assumptions block in invocation context
  - `--assumptions-file <path>`
- If both inline and file assumptions are present, file input takes precedence.
- Verbosity mode supports `compact`, `standard`, `extended` (default: `standard`).
- `--allow-api-degraded` is valid only with `--dry-run` (never valid for live mode).
- Recommended execution path is `scripts/run-ideas-go-faster.sh` so Agent API env vars are loaded from `.env.local`.
- `scripts/run-ideas-go-faster.sh` is initiator-agent-preserving: it auto-selects the local agent CLI (`codex` first, then `claude`) so the invoking agent can execute the sweep without forced cross-agent handoff.

---

## Constitution (Non-Negotiable Invariants)

These rules override all other instructions. The sweep must not produce output that violates any of them.

### The Elon Musk 5-Step Algorithm (Constitutional Invariant)

The Musk lens applies this algorithm in **strict order** during its generation pass. Every recommendation from the Musk lens must be classified into one of these steps. They are executed **in strict order** — you must exhaust each step before moving to the next. This is not a tiebreaker. This is the law.

1. **Question every requirement.** Each must have a named owner (a person, not a department). All requirements are recommendations until proven otherwise. Only physics is immutable. If you cannot name who requested it and why, delete it.

2. **Delete parts and processes.** If you're not adding back at least 10% of what you deleted, you didn't delete enough. The best part is no part. The best process is no process.

3. **Simplify and optimize.** Only AFTER steps 1-2. The most common mistake is optimizing something that should not exist. Do not make this mistake.

4. **Accelerate cycle time.** Every process can be sped up. But only AFTER steps 1-3. Speed up a bad process and you get bad results faster.

5. **Automate.** Last, never first. Automating a process that should be deleted is worse than not automating it.

### Anti-Theater Invariants

- **Constraint-first.** Do not propose work until you name the current constraint and the evidence that proves it. No unsourced claims. No hand-waving.
- **Do not optimize work that should not exist.** Before improving a process, ask: should this process exist at all?
- **Activity is not progress.** More tasks does not mean more throughput. More ideas does not mean better ideas. Measure outcomes, not output volume.
- **Do not produce feature-factory outputs.** Every recommendation must tie directly to a named constraint. If it doesn't relieve a constraint, it doesn't belong in the sweep.
- **Evidence and traceability.** Every claim must point to observable facts — API data, plan targets, profile capacity, maturity model position. No hallucinated metrics.
- **Named ownership.** Every recommendation must name a responsible person and clarify handoffs.
- **Smallest shippable learning unit.** Prefer minimal changes that produce a measurable signal quickly. Do not propose 6-month roadmaps.
- **Safety and sustainability.** Do not recommend burnout, heroics, or policy violations. Optimize for sustained throughput.

### Sales-First Portfolio Directives (Ideas-Generation Scope)

For `/ideas-go-faster`, operate in **sales-first mode**:

- Treat **revenue businesses** as primary: `BRIK`, `PIPE`, `XA`, `HEAD`, `PET`, `HBAG`.
- Treat **enabling systems** as secondary: `PLAT`, `BOS`.
- **Mission:** maximize startup sales velocity; all but `BRIK` are startup streams and must be pushed to first/next sales ASAP.
- **Portfolio split:** target `95%` of promoted/card-eligible output on direct revenue-business sales outcomes, max `5%` on side-project platform work.
- **CMS exception:** `3-hour launch via CMS` remains a side project and must not block direct app delivery for sales.
- **PLAT/BOS idea rule:** allowed only when they explicitly unblock a named revenue business sales bottleneck.
- **UI/DS rule:** no standalone `@acme/ui` / `@acme/design-system` cleanup ideas. UI/DS ideas are valid only when attached to a concrete startup-sales deliverable.
- **Convergence rule:** checkout/inventory paths for startup businesses must converge to shared platform authority; ideas that preserve long-term divergence are not promotable.
- **Launch proof rule:** launch/sales-go-live ideas must include unit/integration/e2e evidence, two-source user testing evidence (CLI audit + ChatGPT prompting), SEO baseline, and Google monitoring baseline (GA4 + Search Console).

---

## Operating Mode

**READ + ANALYZE + CONDITIONAL WRITE (Live) / PREVIEW (Dry-Run)**

**Allowed:**
- Read all agent API endpoints (businesses, people, cards, ideas, stage-docs)
- Read business plans from filesystem: `docs/business-os/strategy/<BIZ>/plan.user.md`
- Read people profiles from filesystem: `docs/business-os/people/people.user.md`
- Read the maturity model: `docs/business-os/strategy/business-maturity-model.md`
- Read persona files from `_shared/cabinet/` as needed during execution
- Create ideas via `POST /api/agent/ideas` (live mode only)
- Create cards via `POST /api/agent/cards` (live mode only)
- Create fact-find stage docs via `POST /api/agent/stage-docs` (live mode only)
- Write sweep report to `docs/business-os/sweeps/<YYYY-MM-DD>-sweep.user.md`

**Persistence mode (run-level):**
- **Default (`live`):** run full pipeline including Stage 6/7 persistence.
- **`--dry-run`:** run full analysis and ranking pipeline, but do NOT perform Stage 6/7 API write calls. Output preview tables for would-create ideas/cards/stage-docs in the sweep report.
- **`--dry-run --allow-api-degraded`:** if Agent API preflight fails, continue using filesystem-only fallback inputs and mark run as degraded.

**API preflight mode (run-level):**
- **`strict` (default):** API preflight failures are fatal.
- **`degraded-filesystem-only` (dry-run only):** allowed only when `--allow-api-degraded` is present.

**Not allowed:**
- Modify existing cards or ideas (no PATCH on cards/ideas — Drucker/Porter runs before card creation, so no priority updates needed)
- Stage-doc PATCH is allowed only for latest-wins `fact-find` upsert safety (avoid duplicate stage-doc POSTs)
- Move cards between lanes directly (baseline deterministic lane transitions are handled downstream by /plan-feature and /build-feature)
- Run destructive commands
- Auto-schedule or self-invoke

### In-Run Progress Updates (Mandatory)

The sweep must provide progress visibility while execution is underway.

**Progress artifact:**
- Write to `docs/business-os/sweeps/<YYYY-MM-DD>-progress.user.md` (or run-scoped subdirectory equivalent when used).
- Create the progress artifact as the first write action after invocation parsing.

**Progress artifact frontmatter (required):**
```yaml
---
Type: Sweep-Progress
Date: YYYY-MM-DD
Run-Status: running | complete | partial | failed-preflight
Persistence-Mode: live | dry-run
Stance: improve-data | grow-business
Current-Stage: preflight | stage-1 | stage-2 | stage-3 | stage-4 | stage-5 | stage-5.5 | stage-6 | stage-7 | stage-7.5 | complete
Last-Updated-UTC: YYYY-MM-DDTHH:MM:SSZ
Progress-Events: N
Final-Report-Path: <path-or-pending>
---
```

**Update cadence (required):**
- Emit a progress event at each stage transition (start + complete).
- Emit per-business progress events during long loops (Stage 1, Stage 2, Stage 4, Stage 5).
- Emit heartbeat updates every `<=90 seconds` while a long stage is running.
- After each progress artifact update, emit a concise terminal line:
  - `Progress: <stage> <state> (<completed>/<total>)`

**Completion/failure finalization (required):**
- On success or partial completion, set `Run-Status`, `Current-Stage: complete`, and `Final-Report-Path`.
- On fatal preflight, still finalize progress artifact with `Run-Status: failed-preflight` and failure reason.

### Failure Policy (Two-Phase)

**Phase 1 — Fatal (STOP sweep pipeline stages before persistence):**
Stop the sweep if any of these fail:
- Fetch businesses list from Agent API
- Read maturity model file
- Fetch existing cards/ideas/stage-docs for dedup + priority baseline

In fatal cases: stop all pipeline stages and attempt one final write of a minimal sweep report marked `Run-Status: failed-preflight` including the error.

**Dry-run degraded preflight fallback (explicitly opt-in):**
- Trigger condition: `--dry-run --allow-api-degraded` and Agent API preflight fails.
- Continue in `API-Preflight-Mode: degraded-filesystem-only` using:
  - filesystem business plans under `docs/business-os/strategy/<BIZ>/plan.user.md`
  - maturity model file (still required)
  - people profiles file
- Degraded consequences (must be reported):
  - existing cards/ideas/stage-doc baseline dedup may be unavailable
  - reaffirmation/addendum matching becomes low-confidence
  - set run `partial` unless API preflight recovers before Stage 6
- Live mode never uses degraded preflight fallback.

**Phase 2 — Non-fatal (record + continue during persistence):**
During Stages 6–7 (live-mode creates):
- In `--dry-run`, do NOT issue write calls (`POST/PATCH`) to ideas/cards/stage-docs endpoints; record preview output instead.
- Ideas/cards are non-idempotent POST creates. Do NOT blind-retry create calls.
- On idea/card create failure: run one reconciliation read. If entity is confirmed, treat as success; if not, record failure and continue.
- Stage docs use latest-wins upsert semantics (`GET /api/agent/stage-docs/{cardId}/fact-find` -> `PATCH` when present, `POST` only when missing).
- Mark sweep report `Run-Status: partial` and list all failed creates/updates
- Never create a stage doc unless its card exists
- Emit a reconciliation checklist in the sweep report (what succeeded, what failed, exact repair commands, and next action owner)

Rationale: ideas are always documented in the sweep report; persistence is best-effort without pretending transactional guarantees.

---

## MACRO Framework (Business Process Audit Categories)

Every business is audited against 5 process categories. **Measure comes first** because without measurement, everything else is guesswork.

### M — Measure (Can you see what's happening?)

Without measurement, you are flying blind. This is always the first question.

| Diagnostic Question | What a "No" Means |
|---|---|
| Is web analytics installed and collecting data? (GA, Plausible, etc.) | You cannot measure traffic, conversion, or content performance. CRITICAL gap. |
| Is Search Console connected? | You cannot measure SEO performance, indexing, or keyword rankings. |
| Are conversion events tracked? (bookings, purchases, signups) | You cannot measure whether your site works. |
| Is there marketing attribution? (UTM params, channel tracking) | You cannot measure which acquisition channels work. |
| Are revenue metrics visible? (ADR, RevPAR, occupancy, GMV, AOV) | You cannot measure business health. |
| Is customer feedback collected? (NPS, reviews, surveys, support tickets) | You cannot hear your customers. |
| Are operational metrics tracked? (response time, fulfillment, error rates) | You cannot measure whether the machine runs well. |
| Is there a time-series record? (even a spreadsheet) | You cannot detect trends. Every sweep starts from scratch. |

### A — Acquire (Are customers finding you?)

Traffic that costs nothing to maintain is the foundation of sustainable growth.

| Diagnostic Question | What a "No" Means |
|---|---|
| Is there organic search traffic? | All acquisition is paid — spend stops, traffic stops. |
| Are content assets being produced? (guides, articles, landing pages) | No compounding SEO assets. Every visitor costs marginal money. |
| Is content in target languages? | Missing international traffic at near-zero marginal cost. |
| Are social/referral channels active? | Single-channel dependency. |
| Is there a content calendar or production cadence? | Content production is ad-hoc, not systematic. |
| Does the business appear in relevant directories/aggregators? | Missing distribution channels. |

### C — Convert (Are they buying?)

Traffic without conversion is a vanity metric.

| Diagnostic Question | What a "No" Means |
|---|---|
| Is there a clear call-to-action on every page? | Visitors don't know what to do. |
| Is the checkout/booking flow optimized? | Friction kills conversion. |
| Are pricing and availability clear? | Uncertainty prevents purchase. |
| Is trust established? (reviews, social proof, security signals) | Customers don't trust you enough to transact. |
| Are abandoned carts/bookings tracked and recovered? | Leaving money on the table. |
| Is there A/B testing on conversion paths? | You're guessing, not learning. |

### R — Retain (Are they coming back?)

Acquisition without retention is a leaky bucket.

| Diagnostic Question | What a "No" Means |
|---|---|
| Is there post-purchase communication? (email, follow-up) | Customer relationship ends at checkout. |
| Is there a loyalty/repeat purchase mechanism? | No reason to come back. |
| Are customer service channels responsive? | Customers leave when ignored. |
| Is there self-service content for common questions? | Every support query costs human time. |
| Is customer satisfaction measured? | You don't know if customers are happy. |

### O — Operate (Is the machine efficient?)

Even a good product fails if the operations are broken.

| Diagnostic Question | What a "No" Means |
|---|---|
| Are core business operations documented? | Knowledge is in people's heads — bus factor = 1. |
| Is there cross-app data flow? (products ↔ content ↔ bookings) | Manual data re-entry. Inconsistency. |
| Are operational costs tracked? | You can't optimize what you don't measure. |
| Is the development/deployment pipeline reliable? | Shipping is slow or risky. |
| Are there automated quality checks? (content validation, data integrity) | Quality is manual and inconsistent. |
| Is there capacity planning? (people, infrastructure, budget) | Surprises instead of planning. |

---

## Cabinet Pipeline (7 Stages)

### Stage 1: Preflight + Composite Generation

**Source of truth for businesses:** Agent API (NOT businesses.json).

**Preflight (per sweep):**
1. Fetch businesses from `GET /api/agent/businesses` (fatal if fails).
2. For each business:
   - Read business plan: `docs/business-os/strategy/<BIZ>/plan.user.md` (degrade if missing).
   - Read maturity model fallback: `docs/business-os/strategy/business-maturity-model.md` (fatal if missing).
   - Read people profiles: `docs/business-os/people/people.user.md` (degrade if missing).
   - Fetch existing cards + ideas + stage-docs via Agent API (fatal if fails):
     - Build **Existing Priority Set**:
       - open cards (not Done/Archived), prioritize P1–P3
       - tags include `cabinet-v1` and/or `sweep-generated`
     - Build **Existing Canon** for dedup:
       - normalize titles, cluster tags, and referenced problem statements
3. Build a **DGP Resurfacing Queue** from existing ideas (MANDATORY):
   - Include ideas tagged `dgp` + `gap:<type>` with `status=raw`
   - Query contract: Agent API list calls support only `location=inbox|worked`. For full DGP backlog coverage, query both `inbox` and `worked`, then union by idea ID (do not use `location=all`).
   - Partition by `gap:data`, `gap:timing`, `gap:dependency`
   - Compute `Resurfacing-State`:
     - `ready-now`:
       - `gap:data`: default when stance is `improve-data`; rank by `VOI-Score` DESC
       - `gap:timing`: `Re-evaluate-When` is due (date <= today) or trigger explicitly met
       - `gap:dependency`: dependency evidence indicates prerequisite is complete
     - `watch`: valid DGP but trigger/dependency not yet satisfied
   - Output resurfacing table in sweep report (ready-now first)
4. For each business, write a **Constraint Statement** (1–3 sentences) with:
   - Current constraint (MACRO category)
   - Evidence pointers (file paths and/or API entities)
   - Constraint confidence (0–100, subjective)
5. Resolve **Human Assumptions Input** (optional):
   - Accept inline assumptions block from invocation context.
   - Accept `--assumptions-file <path>` when provided.
   - If both are present, file input wins.
   - Record assumptions source in report frontmatter (`none` | `inline` | `file`).
6. Apply **sales-first portfolio classification** for this run:
   - mark each business as `revenue` or `enabler`
   - define startup set (`PIPE`, `XA`, `HEAD`, `PET`, `HBAG`) for sales-velocity emphasis
   - enforce CMS work as side-project lane (non-blocking)

**Composite Generation (per business):**
Run sequential multi-lens passes to generate ideas.

**Generation cadence (quality-first, mandatory):**
1. **Divergence pass:** Each sub-expert contributes at most 1 net-new candidate idea per business.
2. **Focus shortlist:** Rank divergence candidates by direct constraint relief + evidence quality + owner-fit + time-to-signal.
3. **Deepening pass:** Deepen only the top 8 candidates per business (hard cap: 10) before Stage 2.
4. **Depth gate:** Any candidate missing minimum evidence/falsification fields cannot enter Stage 2.

**Sub-experts in order (generic — all businesses except BRIK):**
1. `musk` (Musk lens — feasibility)
2. `bezos` (Bezos lens — customer-backwards)
3. `hopkins` (Marketing lens — scientific advertising)
4. `ogilvy` (Marketing lens — brand)
5. `reeves` (Marketing lens — USP)
6. `lafley` (Marketing lens — consumer insight)
7. `patterson` (Sales lens — systematic selling)
8. `benioff` (Sales lens — challenger positioning)
9. `chambers` (Sales lens — ecosystem and distribution)
10. `finder` (Sourcing lens — product selection and supplier discovery)
11. `bridge` (Sourcing lens — negotiation and supplier relationship depth)
12. `mover` (Sourcing lens — logistics, compliance, and landed cost)

**BRIK-specific sub-experts (replaces sourcing with brikette lens):**
1. `musk` (Musk lens — feasibility)
2. `bezos` (Bezos lens — customer-backwards)
3. `hopkins` (Marketing lens — scientific advertising)
4. `ogilvy` (Marketing lens — brand)
5. `reeves` (Marketing lens — USP)
6. `lafley` (Marketing lens — consumer insight)
7. `patterson` (Sales lens — systematic selling)
8. `benioff` (Sales lens — challenger positioning)
9. `chambers` (Sales lens — ecosystem and distribution)
10. `crawford` (Brikette lens — interior/lived comfort)
11. `starck` (Brikette lens — interior/bold identity)
12. `nakajima` (Brikette lens — maintenance/TPM)
13. `deming` (Brikette lens — maintenance/quality systems)
14. `kroc` (Brikette lens — cleaning/standards)
15. `gawande` (Brikette lens — cleaning/checklists)
16. `schulze` (Brikette lens — cleaning/culture)
17. `hopkins` (Brikette lens — hostel promotion/scientific advertising)
18. `ogilvy` (Brikette lens — hostel promotion/brand)
19. `sutherland` (Brikette lens — hostel promotion/behavioral economics)
20. `meyer` (Brikette lens — F&B/hospitality)
21. `degroff` (Brikette lens — F&B/bar program)
22. `schrager` (Brikette lens — events/atmosphere)
23. `jones` (Brikette lens — events/community)
24. `generator` (Brikette lens — events/hostel-native ops)

**Note:** Hopkins and Ogilvy appear twice for BRIK — once under Marketing lens (generic frameworks) and once under Brikette lens (hostel-specific framing). Distinguished by `Originator-Lens: marketing` vs `Originator-Lens: brikette`. Clustering (Stage 3) handles any duplicate ideas.

**Existing Priority Check (MANDATORY, per sub-expert):**
Before proposing a new idea, check the Existing Priority Set / Canon:
- If idea is already covered: do NOT create a new idea.
  - Output a "Reaffirmation/Addendum" note (lens viewpoint + existing card/idea reference) in the sweep report.
- If genuinely new or materially different: proceed.

**For each sub-expert (new ideas only):**
1. Read the lens file from `.claude/skills/_shared/cabinet/lens-<lens>.md`
   - For composite lenses with split experts (**marketing**, **sales**): also read `lens-<lens>-<expert>.md` for the current sub-expert pass (e.g., `lens-marketing-hopkins.md` for Hopkins, `lens-sales-benioff.md` for Benioff). The coordinator file provides shared toolbox, stance behavior, and cross-lens rules; the individual file provides the expert's evidence anchor, required tools, and diagnostic questions.
2. Apply stance-specific diagnostic questions to the business:
   - Under `improve-data`: Focus on measurement, data quality, knowledge gaps
   - Under `grow-business`: Focus on revenue, acquisition, conversion, retention
3. Generate 0-1 candidate idea per sub-expert per business (divergence pass only)
4. Format each idea with Dossier Header (see `dossier-template.md`):
   - `Originator-Expert`: person-level attribution (e.g., `hopkins`)
   - `Originator-Lens`: lens-level grouping (e.g., `marketing`)
   - `Confidence-Tier`: Set to `candidate` initially
   - `Confidence-Score`: 0-100 (preliminary, before confidence gate)
   - `Pipeline-Stage`: Set to `candidate`
   - **`Impact-Type`:** growth | savings | risk-avoidance | time
   - **`Impact-Mechanism`:** Acquire | Convert | Retain | Measure | Operate
   - **`Impact-Band`:** XS | S | M | L | XL (see Impact rubric)
   - **`Impact-Confidence`:** 0-100 (subjective; must cite evidence pointers or mark unknown)

**Impact rubric (for Impact-Band):**
- **XS:** small/local improvement; unlikely to move a plan target materially
- **S:** noticeable improvement; could move a sub-metric
- **M:** meaningful; could move a primary KPI if executed well
- **L:** large; likely to move a plan target materially
- **XL:** step-change; materially changes the business trajectory

**Deepening pass (mandatory before Stage 2):**
- Keep top 8 candidates per business from divergence ranking (hard cap 10)
- For each deepened candidate, add all of:
  - `Evidence-Pointers`: at least 2 concrete pointers (files, API entities, or metrics)
  - `Falsification-Test`: one explicit condition that could disprove the core claim
  - `First-Signal`: one measurable leading indicator with owner + review date
- Candidates missing deepening fields are rerouted:
  - to DGP (`Gap-Type=data`) if thesis is promising but under-evidenced
  - to hunch log if no credible test/evidence path exists

**Context discipline:** use compress-and-carry-forward plus summary-block mode and coverage thresholds from the Context Discipline Strategy section.

**MACRO emphasis by stance** (see `stances.md`):
- Under `improve-data`: Measure (HIGH), Operate (HIGH), Acquire (MEDIUM), Convert (MEDIUM), Retain (LOW)
- Under `grow-business`: Acquire (HIGH), Convert (HIGH), Retain (MEDIUM), Measure (MEDIUM), Operate (LOW)

**Musk 5-step constitutional invariant:**
During the Musk lens pass, all recommendations must follow strict step ordering (Question → Delete → Simplify → Accelerate → Automate). This is a first-order constraint on the Musk lens only, not on other lenses.

### Stage 2: Confidence Gate

For each candidate idea, evaluate against the 5 presentable criteria (see `dossier-template.md`).

**Prerequisites:**
- Impact fields (Impact-Type, Impact-Mechanism, Impact-Band, Impact-Confidence) must exist in the Dossier Header, even if values are `unknown`.
- Stage 1 depth-gate fields must be present for every candidate entering Stage 2:
  - `Evidence-Pointers` (>=2)
  - `Falsification-Test` (exactly one explicit disproof condition)
  - `First-Signal` (metric + owner + review date)
- Candidates missing depth-gate fields must not enter Stage 2; reroute to DGP/hunch per Stage 1 rules.

**Assumption Challenge (F3, conditional):**
- If `Assumptions-Source` is `inline` or `file`, evaluate each assumption and classify as `accept`, `condition`, or `reject`.
- Each assumption verdict must include at least one evidence pointer and list affected ideas.
- Ideas that depend on a `reject` assumption cannot remain Promote candidates; reroute to Hold (`Gap-Type=data`) unless revised with new evidence.
- Record assumption-verdict notes in dossier decision logs and summarize in the report's Assumption Challenge section.

1. Customer/user identified — Who is this for? Named segment or persona.
2. Problem statement present — What pain or opportunity? Clear and specific.
3. At least one feasibility signal — Technical or commercial evidence this is doable.
4. Evidence or reasoning chain — Not just assertion. Data, research, or logical argument.
5. Business alignment — How does this serve a known business goal or fill a plan gap?

**Scoring:**
- **5/5 criteria met** → Confidence-Tier: `presentable`, Confidence-Score: 60-100 → Proceed to clustering
- **3-4/5 criteria met** → Confidence-Tier: `decision-gap`, Confidence-Score: 30-59 → Create DGP (see below)
- **0-2/5 criteria met** → Confidence-Tier: `hunch`, Confidence-Score: 0-29 → Log in sweep report only, do NOT persist

**Decision Gap Proposals (DGPs):**

DGP = **Decision Gap Proposal** (not only data gaps).

- Create via `POST /api/agent/ideas` with:
  - `Status`: `raw`
  - `Tags`: `["sweep-generated", "cabinet-v1", "dgp", "gap:<type>"]` where `<type>` is `data`, `timing`, or `dependency`
  - `Content`: Full Dossier with Dossier Header

**Required DGP fields in Dossier Header:**
- `Gap-Type`: `data` | `timing` | `dependency`
- `VOI-Score`: required only if Gap-Type=data (0-1 scale)
- `Decision-Blocked`: what decision cannot be made
- `Re-evaluate-When`: date or trigger condition
- `Owner`: named person responsible for closing the gap

**DGP content must include** (see `data-gap-lifecycle.md`):
- Problem statement (provisional)
- Proposed solution (sketch)
- Blocking questions or triggers (numbered list)
- Proposed investigation or re-evaluation plan
- Presentable Criteria Check — which criteria are met, which are missing
- VOI Justification — required for Gap-Type=data; optional for timing/dependency

**Gap-Type definitions:**
- **data**: Missing information blocks the decision. Requires VOI-Score + investigation plan.
- **timing**: Idea is sound but timing is wrong. Requires triggers + re-evaluation date.
- **dependency**: Prerequisite work must complete first. Names the prerequisite work + owners.

**VOI-Score** (Value of Information, 0-1 — required for Gap-Type=data):
- 0.8-1.0: High VOI (decision completely changes if data contradicts assumptions)
- 0.4-0.7: Medium VOI (data helps but doesn't fundamentally change decision)
- 0.1-0.3: Low VOI (could make decent decision without data)

**Hunches (not persisted):**
- Log in sweep report with rationale for suppression
- If hunch gains new evidence in future sweep, re-submit as fresh evaluation

**Stance sensitivity:** INVARIANT (confidence criteria do not change by stance)

### Stage 3: Cluster/Dedup

Group presentable ideas using clustering rules (see `clustering.md`):

**Hard clustering boundaries (NEVER violated):**
1. Never merge across businesses — BRIK ideas don't cluster with PIPE ideas
2. Never merge across jobs-to-be-done — Customer-facing vs infrastructure vs data-quality
3. Max cluster size: 4 lens variants

**Clustering heuristic:**
Two ideas cluster if:
- Same business
- Same MACRO category (same job-to-be-done)
- Same core problem or opportunity (can be phrased differently but same essence)

**Merged dossier structure:**
1. **Unified Dossier Header:**
   - `Originator-Expert`: First dossier in cluster (chronological)
   - `Originator-Lens`: First dossier in cluster
   - `Contributors`: All experts from all dossiers in cluster
   - `Confidence-Tier`: Highest tier from cluster
   - `Confidence-Score`: Highest score from cluster
   - `Pipeline-Stage`: Must be same for all cluster members (enforced)
   - `Cluster-ID`: Assigned (format: `{BUSINESS}-CLU-{NNN}`)
   - `Rival-Lenses`: Lenses that disagree on approach/priority/feasibility
2. **Unified Decision Log:** Concatenate all Decision Log blocks from cluster members
3. **Main Idea Content:** Most complete variant or synthesis
4. **Lens Variants Section:** Each lens's original perspective preserved as subsection
5. **Agreement Section:** Where lenses converge (what they agree on)
6. **Rivalry Section:** Where lenses disagree (what they disagree on, why, how to resolve)

**Singletons:** Ideas with no match pass through unchanged

**Stance sensitivity:** INVARIANT (clustering rules do not change by stance)

### Stage 4: Munger/Buffett/Thiel Filter

Apply `filter-munger-buffett.md` persona (v2.2) to each clustered dossier. The filter now runs a two-phase process:

**Read the filter persona file:** `.claude/skills/_shared/cabinet/filter-munger-buffett.md`

**Phase 1 — Munger–Thiel Contrarian Gate (mandatory pre-check):**
Produces a **Contrarian Status** (PASS / UNRESOLVED / FAIL) by evaluating 7 required artifacts:
1. Opposite-Side Steelman (Munger) — best argument against the idea
2. Inversion Pre-Mortem (Munger) — top 5 ways it dies with leading indicators + exits
3. Contrarian Secret (Thiel) — "most believe X, truth is ¬X" + operational advantage
4. Capture-Value Proof (Thiel) — pricing power under stress, why customers pay us
5. Competition Escape Plan (Thiel) — wedge, path to differentiation, "by cycle N" milestone
6. Market Definition Reality Check (Thiel) — narrow vs. skeptical framing
7. Incentive Truth-Bending Check (Munger × Thiel) — where we're tempted to misdescribe

**Contrarian Status constrains the final verdict:**
- **PASS** → verdict may be Kill, Hold, or Promote
- **UNRESOLVED** (missing cheap facts) → verdict must be Hold (Promote is blocked)
- **FAIL** (fatal) → verdict must be Kill (unless reframed as tiny timeboxed test → Hold)

**Phase 2 — Munger–Buffett Capital-Allocation Verdict:**
- **Munger:** Inversion (how could this fail?), mental model lattice, avoiding stupidity
- **Buffett:** Circle of competence, margin of safety, opportunity cost, competitive moats

**Verdicts (constrained by Contrarian Status):**
- **Kill** → Reject permanently (outside competence, catastrophic downside, negative opportunity cost, no contrarian secret, commodity with no escape)
- **Hold** → Defer (reason varies — see Gap-Type below)
- **Promote** → Approve for next stage (requires Contrarian Status PASS + within competence, bounded downside, high optionality, passes inversion test, value capture credible)

**Output:** Append TWO Decision Log blocks to dossier:
1. **Munger–Thiel Contrarian Gate block:** Contrarian Status + all 7 artifact sections
2. **Munger-Buffett Filter block:** Verdict + Verdict-Constrained-By + Rationale + Risk-Assessment + Opportunity-Cost

**Killed ideas:** Logged in sweep report with Contrarian Status, not persisted
**Held ideas:** Stored as DGPs (Decision Gap Proposals) with:
- `Tags`: `["sweep-generated", "cabinet-v1", "dgp", "gap:<type>", "held"]`
- Gap-Type determined by Hold reason:
  - `data` — promising thesis but insufficient evidence (needs investigation)
  - `data` — Contrarian Status UNRESOLVED (missing cheap facts for gate artifacts — see `data-gap-lifecycle.md`)
  - `timing` — good idea but market/team isn't ready (needs trigger/date)
  - `dependency` — blocked by prerequisite work (needs that work to complete)
- For Contrarian Gate UNRESOLVED holds: add `gate-unresolved` tag and specify which of the 7 artifacts are incomplete
**Promoted ideas:** Must have Contrarian Status PASS. Proceed to Drucker/Porter priority (Stage 5)

**Stance sensitivity:** STANCE-INVARIANT (bad ideas are bad regardless of stance)

### Stage 5: Drucker/Porter Priority

Apply `prioritize-drucker-porter.md` persona to rank all promoted dossiers **before** card creation:

**Input validation:** Only ideas with Verdict=Promote and Contrarian Status=PASS enter this stage. Ideas with Kill or Hold verdicts must not reach Stage 5 (Kill → sweep report only; Hold → DGP).

**Read the prioritizer persona file:** `.claude/skills/_shared/cabinet/prioritize-drucker-porter.md`

**Read business plans:** For each business, read `docs/business-os/strategy/<BIZ>/plan.user.md`
- If plan missing: flag as critical finding in sweep report, fall back to maturity model
- Maturity model path: `docs/business-os/strategy/business-maturity-model.md`

**Evaluation framework:**
- **Drucker:** Effectiveness over efficiency (doing the right things), manage by objectives, knowledge worker productivity
- **Porter:** Five forces, value chain, strategic positioning (cost leadership OR differentiation), activity system fit

**Priority levels:**
- **P1:** Do immediately (high impact, clear path, urgent timing, strong plan alignment)
- **P2:** Do soon (high impact but needs preparation)
- **P3:** Schedule for later (medium impact, good fit, lower urgency)
- **P4:** Keep in backlog (low urgency, potentially valuable later)
- **P5:** Deprioritize (low fit, low impact, wrong timing)

**Stance weighting (STANCE-SENSITIVE):**

Under `improve-data`:
- Higher weight: Measurement infrastructure, data quality, knowledge gaps, feedback loops, plan/profile completeness
- Lower weight: Revenue tactics, feature development, market expansion
- MACRO emphasis: Measure (HIGH), Operate (HIGH), Acquire (MEDIUM), Convert (MEDIUM), Retain (LOW)

Under `grow-business`:
- Higher weight: Customer acquisition, conversion optimization, revenue growth, retention, competitive positioning
- Lower weight: Pure infrastructure without growth link, measurement for measurement's sake
- MACRO emphasis: Acquire (HIGH), Convert (HIGH), Retain (MEDIUM), Measure (MEDIUM), Operate (LOW)

**Sales-first portfolio gates (mandatory in both stances):**
- Revenue businesses (`BRIK`, `PIPE`, `XA`, `HEAD`, `PET`, `HBAG`) are the default promotion path.
- `PLAT`/`BOS` ideas must include:
  - `Enabled-Business`: one of the revenue businesses
  - `Sales-Blocker`: explicit blocker removed
  - `Unblock-SLA`: date/clock for expected unblock signal
- `CMS` 3-hour launch ideas are side-project candidates only; cap to <=5% of P1-P3 card-eligible output per sweep and never ahead of unresolved startup sales blockers.
- Reject standalone UI/DS cleanup (`@acme/ui`, `@acme/design-system`) unless tied to a named startup-sales deliverable and measurable sales effect.
- Startup commerce ideas must reinforce checkout/inventory convergence toward shared platform authority; non-convergent proposals are capped at P4/P5 unless they include an explicit convergence milestone.

**Output:** Append Decision Log block to dossier with:
- Priority: [P1|P2|P3|P4|P5]
- Potential-Impact: [Impact-Band from dossier + mechanism + confidence assessment]
- Strategic-Fit: How this aligns with business plan targets
- Plan-Target: Which specific plan target this addresses
- Stance-Weight: How stance influenced the ranking
- Sales-Link: direct sales outcome path for this idea
- Enabled-Business: revenue business directly enabled (`self` for revenue-business ideas)
- Economics-Gate: [pass|blocked]
- Economics-Missing-Fields: [list of missing fields, empty if pass]
- Sales-Readiness-Gate: [pass|blocked|n/a]
- Sales-Readiness-Missing-Fields: [list of missing launch-proof fields, empty if pass]
- Rationale: 2-3 sentences using effectiveness, positioning, or value chain reasoning

**Economics gate (F5, mandatory before Stage 6):**
- A Promote candidate must include all fields:
  - `Upside`
  - `Downside`
  - `Reversibility`
  - `Cost-of-Delay`
  - `Time-to-Signal`
- If any field is missing:
  - set `Economics-Gate: blocked`
  - block card eligibility for that idea
  - reroute to Hold (`Gap-Type=data`) with missing fields recorded
  - include the idea in the report's Economics Gate section with blocker reason

**Sales-readiness gate (mandatory for startup launch/sales-go-live ideas):**
- If idea claims launch readiness, checkout readiness, or near-term sales-go-live, it must include:
  - `Unit-Test-Evidence`
  - `Integration-Test-Evidence`
  - `E2E-Test-Evidence`
  - `User-Test-CLI-Audit-Evidence`
  - `User-Test-ChatGPT-Evidence`
  - `SEO-Baseline-Evidence`
  - `Google-Monitoring-Evidence` (GA4 + Search Console baseline; equivalent signal allowed only with explicit rationale)
- CLI audit settings contract for `User-Test-CLI-Audit-Evidence`:
  - Must reference a current output from `.claude/skills/user-testing-audit/scripts/run-user-testing-audit.mjs`
  - Must include no-JS predicate evidence: `NO_JS_BAILOUT_MARKER`, `hasNoI18nKeyLeak`, `hasMetadataBodyParity`, `hasSocialProofSnapshotDate`
  - Must include SEO artifacts from the same run: `...-seo-summary.json` and `...-seo-artifacts/`
  - Must include smoke/go-live signal for launch path confidence: `pnpm launch-smoke --wait --json` (or config `smokeChecks`) and applicable launch-go-live gate status
- Two-source user-testing contract (mandatory):
  - Source A: CLI-agent audit evidence (contract above)
  - Source B: ChatGPT prompting evidence (prompt set, date, verdict, critical risks/open questions)
  - Single-source user testing is invalid for launch/sales-go-live promotion
- If any required field is missing:
  - set `Sales-Readiness-Gate: blocked`
  - block card eligibility for that idea
  - reroute to Hold (`Gap-Type=data`) with missing fields recorded
  - include the idea in the report's gate section with blocker reason

**Traction mode (under `grow-business`, market-facing L1-L2 businesses only):**
- Use traction-mode Decision Log format for P1/P2 (includes Traction Objective, Test Plan, Porter Fit, Abandonment)
- Output a **Rigor Pack** for each P1/P2 (5 components: Objective & Contribution Card, Traction Test Card, Trade-off Statement, Evidence & Unknowns, Abandonment Note)
- Rigor Pack content is passed to Stage 7 for fact-find doc pre-population
- P1 cap: max 3 P1s per business per sweep
- Reversibility rule: if Munger/Buffett noted "bounded and reversible downside" → Rigor Pack sufficient; if cautious → require Full Strategy Pack
- Infrastructure businesses (PLAT, BOS) use standard format under `grow-business`, no traction mode

**No PATCH calls needed:** Priority is assigned before card creation (Stage 6), so cards are created with the correct priority from the start.

**Stance sensitivity:** STANCE-SENSITIVE (plan target weighting changes by stance; traction mode activates under `grow-business` for L1-L2 market-facing businesses)

### Stage 5.5: Persistence Prepare (3A Contract)

Build persistence artifacts before any write call:

- Commit manifest: `docs/business-os/sweeps/<YYYY-MM-DD>-commit-manifest.json`
- Write ledger (initially empty for this run): `docs/business-os/sweeps/<YYYY-MM-DD>-write-ledger.jsonl`
- Card ID map (created during commit): `docs/business-os/sweeps/<YYYY-MM-DD>-card-id-map.json`

**3A invariants:**
- Zero API writes in this stage (live and dry-run).
- Manifest is deterministic and ordered.
- Fact-find payload templates use `{{CARD_ID}}` placeholder.

**Manifest schema (required fields):**
- `operation_id` (stable deterministic id)
- `kind` (`idea_create` | `card_create` | `factfind_upsert`)
- `slug`
- `payload_fingerprint` (SHA256 of canonicalized payload/template)
- `depends_on` (array of operation ids)
- `endpoint`
- `method`

**Manifest build rules:**
1. For each promoted idea, add `idea_create`.
2. For each P1-P3 promoted idea, add `card_create` depending on its `idea_create`.
3. Add `factfind_upsert` operations for Top-K (and optional Stage 7b backfill), with dependencies on `card_create` for new cards.
4. Freeze operation order and emit persistence preview tables from manifest.

### Stage 6: Persistence Commit (3B) — Idea/Card Writes

Execute `idea_create` and `card_create` operations from the manifest in dependency order.

**Pre-check (mandatory):** Before creating any card, assert that the idea has Verdict=Promote, Contrarian Status=PASS, and `Economics-Gate=pass`. For launch/sales-go-live ideas, also require `Sales-Readiness-Gate=pass`. If a Hold/Kill verdict or blocked gate leaks to Stage 6, flag as a pipeline violation in the sweep report and skip card creation for that idea.

**Card creation threshold:** Only P1–P3 ideas get cards by default. P4–P5 ideas are persisted as Idea entities only (documented in sweep report, available for future sweeps, but not progressed to cards). This prevents card flooding while ensuring all ideas are documented.

**Dry-run override (mandatory):**
- If `--dry-run`, do NOT call `POST /api/agent/ideas` or `POST /api/agent/cards`.
- Emit preview rows to write ledger with:
  - `status=would_create`
  - `operation_id`
  - `payload_fingerprint`
  - `request_hash`
- In dry-run, report `Ideas-Persisted: 0`, `Cards-Created: 0`, `Create-Failures: 0`.

**3B write-safety contract (live mode only, mandatory):**
- Use idempotency guard key: `operation_id + payload_fingerprint`.
- If ledger already has `created` or `skipped_existing` for that guard key, skip write.
- Before non-idempotent creates, run reconciliation reads (pre-write lookup) for exact match.
- On ambiguous response (timeout/5xx), run post-failure reconciliation read once.
- No blind retries for idea/card creates.

**Write ledger contract (`docs/business-os/sweeps/<YYYY-MM-DD>-write-ledger.jsonl`):**
- `timestamp`
- `operation_id`
- `payload_fingerprint`
- `request_hash`
- `status` (`created` | `skipped_existing` | `failed` | `would_create`)
- `entity_id` (when known)
- `reconciliation_source` (`prewrite_lookup` | `postfail_lookup` | `none`)

**1) Execute `idea_create`:**
```
POST ${BOS_AGENT_API_BASE_URL}/api/agent/ideas
Headers: X-Agent-API-Key: ${BOS_AGENT_API_KEY}, Content-Type: application/json
Body: {
  "business": "<BIZ>",
  "content": "<Full Dossier with Dossier Header + Decision Log + Idea Content>",
  "tags": ["sweep-generated", "cabinet-v1"],
  "priority": "<P1|P2|P3|P4|P5>",  // from Drucker/Porter (Stage 5)
  "location": "inbox"
}
```

**Routing contract:** Every persisted idea must remain discoverable in `/ideas` (canonical idea UI) via D1-backed list queries; ideas must not be rendered in Kanban lanes.

**2) Execute `card_create` (P1–P3 only):**
```
POST ${BOS_AGENT_API_BASE_URL}/api/agent/cards
Headers: X-Agent-API-Key: ${BOS_AGENT_API_KEY}, Content-Type: application/json
Body: {
  "business": "<BIZ>",
  "title": "<Idea Title>",
  "description": "<1-2 sentence summary>",
  "lane": "Inbox",
  "priority": "<P1|P2|P3>",  // from Drucker/Porter (Stage 5)
  "owner": "Pete",
  "tags": ["sweep-generated", "cabinet-v1"]
}
```

**P4–P5 ideas:** Persisted as Idea entities only (no card). Logged in sweep report. Available for promotion in future sweeps if context changes.

**Card ID map contract (`docs/business-os/sweeps/<YYYY-MM-DD>-card-id-map.json`):**
- On every successful or reconciled `card_create`, write `slug -> cardId` mapping.
- Stage 7 must resolve `{{CARD_ID}}` using this map before any fact-find upsert.

**Stance sensitivity:** INVARIANT (card creation mechanics do not change by stance)

### Stage 7: Fact-Find Seeding (Global Top-K)

Use manifest `factfind_upsert` operations to seed fact-find docs for selected cards.

**Top-K pool (deterministic): newly promoted ideas from this sweep only.**
- Pool source: ideas promoted through Stages 1–5 and converted to cards in Stage 6 during this invocation.
- Exclude existing cards from Top-K selection, even if reaffirmed in this sweep.
- Existing cards are handled only via **Reaffirmations/Addenda** in the sweep report.

**Global selection criteria (not per-business):**
1. **Priority** — P1 before P2 before P3
2. **Contrarian Status boost** — ideas with all 7 gate artifacts scored PASS rank above same-priority ideas where any artifact scored borderline (tiebreaker within same priority)
3. **Impact-Band** — XL before L before M (tiebreaker within same priority + contrarian)
4. **Impact-Confidence** — higher first (tiebreaker within same priority + impact)
5. **Confidence-Score** — higher first (tiebreaker)
6. **Card ID** — ASC (final deterministic tiebreaker)

K=3 (default, max 3 fact-find docs per sweep)

**Dry-run override (mandatory):**
- If `--dry-run`, compute Top-K and any Stage 7b candidate exactly as live, but do NOT call stage-doc endpoints.
- Emit `Fact-Find Seeding Preview` in sweep report with would-create entries (card title, priority, template type, reason selected).
- Emit corresponding `factfind_upsert` ledger rows with `status=would_create`.
- In dry-run, report `Fact-Find-Docs-Created: 0`.

**Card ID injection contract (mandatory):**
- For manifest ops depending on `card_create`, resolve `cardId` from `card-id-map.json`.
- Replace `{{CARD_ID}}` placeholder in template before write call.
- If required card ID cannot be resolved, record failed op and mark run partial.

**Stage-doc write mode (live mode only, latest-wins, mandatory):**
- Execute `factfind_upsert` operations after all dependent `card_create` operations settle.
- For each op:
  1) `GET /api/agent/stage-docs/{cardId}/fact-find`
  2) If exists (200): `PATCH /api/agent/stage-docs/{cardId}/fact-find` using `baseEntitySha` and patch `{ "content": "<new stage markdown body>" }`
  3) If missing (404): `POST /api/agent/stage-docs`
  4) If PATCH returns 409: refetch once and retry once; if still conflicting, record failure and continue (run becomes partial)
- Apply rerun skip rule from Stage 6 (`operation_id + payload_fingerprint`).
- This preserves one logical fact-find stage doc per card with latest content while keeping append-only repository internals.

**For each selected card (standard template — used for `improve-data` or non-traction ideas):**
```
POST ${BOS_AGENT_API_BASE_URL}/api/agent/stage-docs
Headers: X-Agent-API-Key: ${BOS_AGENT_API_KEY}, Content-Type: application/json
Body: {
  "cardId": "<card-id>",
  "stage": "fact-find",
  "content": "# Fact-Finding: <Card Title>\n\n**Source:** Sweep <YYYY-MM-DD>\n**Originator:** <Expert> (<Lens>)\n**Confidence:** <Score>/100\n**Priority:** <P1-P5>\n**Impact:** <Impact-Band> (<Impact-Type> via <Impact-Mechanism>)\n\n## Questions to Answer\n\n1. <Key question about feasibility>\n2. <Key question about approach>\n3. <Key question about measurement>\n\n## Evidence From Sweep\n\n- <evidence bullet 1>\n- <evidence bullet 2>\n\n## Contrarian Gate Summary\n\n**Contrarian Status:** PASS\n**Thiel Secret:** <1-sentence contrarian secret from gate>\n**Competition Escape:** <wedge + by-cycle-N milestone from gate>\n**Capture-Value:** <pricing power thesis from gate>\n\n## Decision Log (from Cabinet)\n\n<Include relevant Decision Log entries from Dossier — both Contrarian Gate block and Munger-Buffett Filter block>\n\n## Recommendations\n\n- First step: <concrete action>\n- Measurement: <what to track>\n\n## Transition Decision\n\n**Status:** Ready for fact-finding\n**Next Lane:** Fact-finding (when Pete reviews)"
}
```

**For P1/P2 cards under `grow-business` with traction mode (Rigor Pack pre-populated):**
```
POST ${BOS_AGENT_API_BASE_URL}/api/agent/stage-docs
Headers: X-Agent-API-Key: ${BOS_AGENT_API_KEY}, Content-Type: application/json
Body: {
  "cardId": "<card-id>",
  "stage": "fact-find",
  "content": "# Fact-Finding (Traction Fast-Track): <Card Title>\n\n**Source:** Sweep <YYYY-MM-DD>\n**Originator:** <Expert> (<Lens>)\n**Confidence:** <Score>/100\n**Priority:** <P1|P2>\n**Impact:** <Impact-Band> (<Impact-Type> via <Impact-Mechanism>)\n**Mode:** Traction (Rigor Pack pre-populated)\n\n## 1. Objective & Contribution Card\n- Objective: <baseline → target → date>\n- Customer: <who specifically>\n- Contribution thesis: <why this produces traction>\n- Owner + check-in: <name + date>\n\n## 2. Traction Test Card\n- Hypothesis: <market / offer / channel>\n- Market contact mechanism: <how we reach buyers this cycle>\n- Offer: <what we're selling/testing>\n- Success metrics: <leading + lagging>\n- Timebox: <days>\n- Kill / iterate / scale criteria: <decision thresholds>\n\n## 3. Trade-off Statement\n<One sentence: We will not do X / serve Y / optimize Z, because we are prioritizing position A.>\n\n## 4. Evidence & Unknowns\n- Known: <1-3 facts>\n- Unknown: <1-2 critical unknowns>\n- Fastest test: <test + owner + deadline>\n\n## 5. Abandonment Note\n- Stop/pause: <what creates capacity>\n- Capacity source: <explicit if nothing stops>\n\n## Contrarian Gate Summary\n\n**Contrarian Status:** PASS\n**Thiel Secret:** <1-sentence contrarian secret from gate>\n**Competition Escape:** <wedge + by-cycle-N milestone from gate>\n**Capture-Value:** <pricing power thesis from gate>\n\n## Decision Log (from Cabinet)\n\n<Include traction-mode Decision Log + Contrarian Gate block + Munger-Buffett Filter block>\n\n## Transition Decision\n\n**Status:** Ready for fact-finding (fast-track evidence pack)\n**Next Lane:** Fact-finding\n**Note:** This fact-find doc was pre-populated from the Drucker/Porter Rigor Pack to accelerate `/fact-find`. It does not replace `/fact-find` and does not skip planning prerequisites."
}
```

**Rigor Pack integration:** When a P1/P2 idea has a Rigor Pack from Stage 5, the Rigor Pack content pre-populates the fact-find stage doc. This accelerates `/fact-find`, but does not replace it. Cards still proceed through the normal `fact-find → plan-feature → build-feature` loop.

**Cards NOT in top K:** Get cards but no fact-find docs (Pete can manually trigger `/fact-find` later if desired)

**Stage 7b backfill budget (optional; disabled by default in Phase 0):**
- Activation: `--stage7b` flag only. This maps to run-level `stage7b_backfill_enabled=true`.
- Budget: max 1 existing `P1|P2` card without a fact-find doc per sweep.
- Selector (deterministic): Priority (`P1` before `P2`) -> Created-Date ASC (oldest first) -> Card ID ASC.
- Reporting: Stage 7 Top-K remains newly promoted ideas only; Stage 7b selection is reported in a separate backfill section (never mixed into Top-K).
- In dry-run: Stage 7b output is preview-only (no stage-doc writes).
- Disable path: omit `--stage7b`.
- Contract reference: `docs/plans/business-os-stage-7b-backfill-decision-memo.md`.

**Stance sensitivity:** INVARIANT (seeding happens based on Drucker/Porter ranking, which is stance-sensitive, but seeding mechanism itself is invariant)

### Stage 7.5: Discovery Index Freshness (Fail-Closed Loop Contract)

In `--dry-run`, skip discovery-index rebuild (no persistence occurred) and record `discovery-index unchanged` in the sweep report.

After Stage 6/7 persistence completes, rebuild discovery index:

```bash
docs/business-os/_meta/rebuild-discovery-index.sh > docs/business-os/_meta/discovery-index.json
```

Rules:
- Retry once after short backoff.
- If second attempt fails:
  - Mark sweep report `Run-Status: partial` (if not already partial).
  - Add explicit marker: `discovery-index stale`.
  - Include failing command + retry count + failing stderr summary.
  - Include reconciliation checklist with exact rerun command and owner.
- Do not emit a clean success completion message while index is stale.

---

## Technical Cabinet (Revised)

### Triggers
Technical cabinet runs if:
- `--force-code-review` is set, OR
- Stance is `improve-data`, OR
- Repo diff artifact exists at `docs/business-os/engineering/repo-diff.user.md` (or dated diffs at `docs/business-os/engineering/diffs/<YYYY-MM-DD>-diff.user.md`)

### Inputs
- Required: `.claude/skills/_shared/cabinet/lens-code-review.md`
- Required for diff-based review: repo diff artifact file (no diff = no diff review)

### Behavior
1. If persona file missing: skip with note "Technical cabinet: persona file not found, skipping."
2. If triggered but diff artifact missing:
   - Run only "static" repo hygiene checks that do not require diffs (if lens supports it).
   - Otherwise skip with note: "Technical cabinet triggered but no diff artifact; skipping to avoid hallucination."
3. Technical cabinet ideas enter pipeline at Stage 2 (confidence gate) with:
   - `Originator-Expert`: code-review
   - `Originator-Lens`: code-review
   - `applies_to`: `[<BIZ>...]` when business-specific, or `["cross-cutting"]` when not tied to one business
4. Cross-cutting technical ideas must remain explicitly tagged as `["cross-cutting"]` in report output; do not force-fit into a single business lane.

### If not triggered
- Skip technical cabinet, note "Technical cabinet: not triggered" in sweep report

---

## Context Discipline Strategy

**Goal:** Maximize sub-expert coverage while respecting context limits.

**Coverage target:** finish >=80% of planned sub-experts per run.

**Persona file structure:**
- Every persona file has a Persona Summary Block at top (20-40 lines)
- Summary block contains: expert identity, core method, signature questions per stance, domain boundaries, MACRO emphasis
- Full file contains: detailed principles, heuristics, examples, failure modes

**Compression strategy:**
1. **Full-context mode (default):** Read entire persona file for each sub-expert
2. **After each sub-expert pass:** Compress output:
   - Keep Dossier Headers + Confidence-Scores
   - Drop reasoning text from previous passes
3. **Summary-block mode (degraded):** If context approaches limit:
   - Switch to reading only Persona Summary Block for remaining sub-experts
   - Flag in sweep report: "Context budget: switched to summary-block mode after [N] sub-experts"
4. **Context exhausted:** If context limit reached before all sub-experts complete:
   - Stop generation
   - Proceed to confidence gate with ideas generated so far
   - Flag in sweep report: "DEGRADED: context limit reached after [N] of [M] sub-experts"

**Tracking:**
- Coverage ratio = `Sub-Experts-Run / Sub-Experts-Planned`
- If degradation occurs and coverage ratio is `<0.80`:
  - mark run `partial`
  - set `Quality-Rerun-Required: yes`
  - include `Rerun Focus Packet` in report: unrun sub-experts, highest-constraint business first, exact rerun command
- If degradation occurs and coverage ratio is `>=0.80`:
  - run may complete, but include explicit residual-risk note for skipped sub-experts
- Priority order for context allocation: Musk > Bezos > Marketing > Sales > Sourcing (non-BRIK) / Brikette (BRIK only)

---

## Sweep Report

Write to `docs/business-os/sweeps/<YYYY-MM-DD>-sweep.user.md` with comprehensive summary:

**Verbosity contract (per promoted idea summary):**
- `compact`: <=120 words
- `standard`: <=220 words (default)
- `extended`: <=350 words

**Frontmatter:**
```yaml
---
Type: Sweep
Date: YYYY-MM-DD
Run-Status: complete | partial | failed-preflight
Persistence-Mode: live | dry-run
API-Preflight-Mode: strict | degraded-filesystem-only
Stance: improve-data | grow-business
Progress-Artifact: docs/business-os/sweeps/<YYYY-MM-DD>-progress.user.md
Assumptions-Source: none | inline | file
Verbosity-Mode: compact | standard | extended
Businesses-Audited: N
Sub-Experts-Run: N (of M)
Sub-Expert-Coverage: N%
Generation-Candidates-Raw: N
Generation-Candidates-Deepened: N
Quality-Rerun-Required: yes | no
Dry-Run-Writes-Blocked: yes | no
Ideas-Generated: N
Reaffirmations: N
Existing-Cards-Reaffirmed: N
Presentable: N
Decision-Gap: N
Hunches: N
Clusters-Formed: N
Contrarian-Gate-Pass: N
Contrarian-Gate-Unresolved: N
Contrarian-Gate-Fail: N
Signal-Quality-Presentable-Rate: N%
Signal-Quality-Contrarian-Unresolved-Rate: N%
Signal-Quality-Evidence-Density: N.N
Filtered-Promote: N
Filtered-Hold: N
Filtered-Kill: N
Ideas-Eligible-For-Persist: N
Cards-Eligible-For-Create: N
Fact-Find-Docs-Eligible-For-Create: N
Ideas-Persisted: N
Cards-Created: N
Create-Failures: N
Fact-Find-Docs-Created: N
DGP-Resurfaced-Ready: N
DGP-Resurfaced-Watch: N
Technical-Cabinet: Yes | No | Skipped
Context-Discipline: Full | Summary-Block | Degraded
---
```

**Report sections:**
1. **Executive Summary:** Run status, stance used, top constraint across all businesses, top 3 actions (Musk-ordered)
2. **Businesses Analyzed:** Per business: maturity level, MACRO scorecard, constraint statement, top ideas
3. **Who Said What (F1):** Attribution table for promoted/held ideas: title, originator sub-expert, lens, business, and confidence tier
4. **Reaffirmations/Addenda:** Ideas that matched existing priorities — lens viewpoint + existing card reference (prevents re-creating known ideas)
5. **Generation Phase:** Per-expert divergence contributions (person-level), raw candidate count, deepened candidate count, cap-enforcement notes
6. **Depth Gate:** Evidence/falsification/first-signal pass rate, candidates rerouted to DGP/hunch
7. **Confidence Gate:** X presentable, Y decision-gap (with Gap-Types), Z hunches
8. **Assumption Challenge (F3):** If assumptions are provided, verdict each assumption (accept/condition/reject), evidence pointer, and affected ideas
9. **Clustering:** N clusters formed, M singletons, agreements recorded, rivalries flagged
10. **Tool-Gap Register (F2):** Aggregated missing tools/data by gap type, impacted business, and evidence pointer
11. **Contrarian Gate:** N PASS, M UNRESOLVED (with incomplete artifacts listed), O FAIL (with fatal reasons)
12. **Munger/Buffett Filter:** A promoted, B held (with Gap-Types), C killed
13. **Kill/Hold Rationale (F4):** Held and killed ideas with reason codes, contrarian status, and restart condition for held ideas
14. **Drucker/Porter Priority:** P1-P5 distribution with Impact-Band, plan alignment, global ranking
15. **Economics + Sales Readiness Gate (F5):** Pass/blocked counts with missing-field reasons (upside, downside, reversibility, cost-of-delay, time-to-signal, unit/integration/e2e evidence, two-source user-testing evidence, SEO evidence, GA4/Search Console monitoring evidence)
16. **Cards Created / Preview:** Live mode: table of created P1-P3 cards with priority + impact. Dry-run: would-create card table only. P4-P5 ideas listed separately.
17. **Fact-Find Seeding / Preview:** Live mode: global top K cards seeded with stage docs (newly promoted ideas only). Dry-run: would-seed preview only.
18. **Existing Card Addenda:** Existing cards surfaced only as reaffirmation/addendum notes (no Top-K mixing)
19. **Technical Cabinet:** Status (triggered/not triggered/skipped), ideas with `applies_to` (`[<BIZ>...]` or `["cross-cutting"]`)
20. **DGPs Created:** Table of decision-gap proposals with Gap-Type + VOI-Scores (data gaps only)
21. **DGP Resurfacing:** Ready-now and watch queues from existing DGP backlog
22. **Persistence Accounting:** Live mode: (if Run-Status = partial) create/update attempts/successes/failures per entity type, list of failed calls. Dry-run: attempted writes must equal 0 + preview counts by entity type.
23. **Reconciliation Checklist:** (required when Run-Status = partial or discovery index is stale)
    - What succeeded (entity counts + IDs)
    - What failed (endpoint/status/payload summary)
    - Index status (`fresh` | `stale`)
    - Exact retry commands
    - Owner and handoff note
24. **Context Discipline:** Full/Summary-Block/Degraded status, coverage ratio, rerun-required flag, residual-risk note
25. **Signal Quality:** presentable-rate, contrarian-unresolved-rate, evidence-density with interpretation
26. **Delta/Coverage (F6):** Comparison vs prior sweep: promoted/held/killed deltas, reaffirmation deltas, and sub-expert coverage delta
27. **Duration:** Wall-clock time for sweep
28. **Run Progress Trace:** Path to progress artifact + stage timeline summary + any heartbeat anomalies
29. **API Preflight Mode:** strict vs degraded-filesystem-only, fallback trigger reason, and dedup confidence impact

**Stance propagation note:**
- Record which stance was active in frontmatter
- Note how stance influenced generation (MACRO emphasis) and prioritization (plan target weighting)
- Munger/Buffett filter and clustering are stance-invariant (note this explicitly)

---

## Graceful Degradation

### Missing Business Plans
- Flag as critical finding in sweep report: "CRITICAL: [BIZ] has no business plan. Drucker/Porter prioritizer operating in degraded mode."
- Fall back to maturity model as proxy for strategic targets
- Maturity-based priority inference:
  - L1 (Catalog Commerce): Under `improve-data` → cost discovery, demand validation; Under `grow-business` → first customer, manual fulfillment
  - L2 (Content Commerce): Under `improve-data` → basic analytics, content measurement; Under `grow-business` → acquisition channels, conversion optimization
  - L3+ (Platform/Ecosystem): Under `improve-data` → advanced analytics, BI; Under `grow-business` → new markets, partnerships

### Missing People Profiles
- Use API defaults (`maxActiveWip: 3` per person)
- Flag as finding in sweep report
- Note that capacity assessments are low-confidence

### Missing Persona Files
- Skip that lens
- Note in sweep report: "Persona file missing: lens-[lens].md — skipped this sub-expert"

### Preflight Failures (Fatal)
- Business list API, maturity model, or existing cards/ideas read fails: STOP
- Write minimal sweep report with `Run-Status: failed-preflight` and error details
- Do NOT proceed to composite generation

### Persistence Failures (Non-fatal)
- Idea/card create fails and reconciliation cannot confirm success: record failure, continue
- Stage-doc upsert fails after one conflict retry: record failure, continue
- Mark sweep report `Run-Status: partial`
- Include counts of create/update attempts/successes/failures per entity type
- Include list of failed calls (endpoint + status + payload summary + reconciliation result when relevant)

### Discovery Index Rebuild Failure (Non-fatal but fail-closed)
- Retry rebuild once.
- If still failing:
  - Mark sweep report `Run-Status: partial`
  - Mark `discovery-index stale`
  - Include failing command and stderr summary
  - Include reconciliation checklist with rerun command and owner
- Do not report sweep as cleanly complete while stale persists.

### Context Budget Exceeded
- Switch to summary-block mode for remaining sub-experts
- Flag in sweep report with degradation point and coverage ratio
- If coverage ratio `<0.80`: mark run `partial`, set `Quality-Rerun-Required: yes`, emit Rerun Focus Packet
- If coverage ratio `>=0.80`: proceed to next stages with residual-risk note

---

## Evaluation Checklist (Pass/Fail)

After producing the sweep report, verify each item. If any FAIL, revise before finalizing.

- [ ] **Stance recorded:** Sweep report frontmatter includes stance used
- [ ] **Persistence mode recorded:** Frontmatter includes `Persistence-Mode` and `Dry-Run-Writes-Blocked`
- [ ] **API preflight mode recorded:** Frontmatter includes `API-Preflight-Mode` and matches strict vs degraded behavior in report narrative
- [ ] **Progress artifact linked:** Sweep report frontmatter includes `Progress-Artifact` path
- [ ] **Progress updates emitted:** Progress artifact records stage transitions and heartbeat cadence (`<=90s`) during long stages
- [ ] **Degraded preflight rules honored:** `degraded-filesystem-only` appears only when `--dry-run --allow-api-degraded` is used; never in live mode
- [ ] **Assumptions source recorded:** Frontmatter includes `Assumptions-Source` and reflects precedence (file wins over inline when both exist)
- [ ] **Verbosity mode recorded:** Frontmatter includes `Verbosity-Mode` and output respects mode limits
- [ ] **Sub-experts run:** Report shows how many sub-experts completed (X of Y)
- [ ] **Who Said What section present:** Promoted/held ideas include originator sub-expert + lens attribution
- [ ] **Generation cadence executed:** Divergence (<=1 candidate per sub-expert) and deepening (top 8, max 10 per business) both recorded
- [ ] **Depth gate executed:** Every Stage 2 candidate includes `Evidence-Pointers` (>=2), `Falsification-Test`, and `First-Signal`
- [ ] **Confidence gate executed:** Presentable/decision-gap/hunch counts recorded
- [ ] **Assumption challenge executed (when assumptions provided):** Every assumption has accept/condition/reject verdict + evidence pointer + affected ideas
- [ ] **Clustering executed:** Clusters formed, agreements/rivalries recorded
- [ ] **Tool-Gap Register present:** Missing tools/data logged with gap types and evidence pointers
- [ ] **Contrarian Gate executed:** All presentable ideas received Contrarian Status (PASS/UNRESOLVED/FAIL) with 7 artifacts evaluated
- [ ] **Contrarian Status constrains verdicts:** No Promote with UNRESOLVED, no non-Kill with FAIL (unless timeboxed-test Hold)
- [ ] **Munger/Buffett filter executed:** Promote/hold/kill verdicts recorded
- [ ] **Kill/Hold rationale present:** Held and killed ideas include reason code and restart condition (for held)
- [ ] **Economics gate executed:** Promoted/card-eligible ideas have upside/downside/reversibility/cost-of-delay/time-to-signal; blocked ideas listed with missing fields
- [ ] **Sales-first directives enforced:** PLAT/BOS ideas explicitly map to revenue-business sales blockers; CMS side-project ideas remain capped and non-blocking
- [ ] **UI/DS guardrail enforced:** No standalone `@acme/ui` / `@acme/design-system` cleanup ideas in promoted/card-eligible set
- [ ] **Sales-readiness gate executed (when applicable):** launch/sales-go-live ideas include unit/integration/e2e evidence, two-source user-testing evidence (CLI audit + ChatGPT), SEO baseline evidence, and GA4/Search Console monitoring evidence
- [ ] **3A manifest emitted:** `docs/business-os/sweeps/<YYYY-MM-DD>-commit-manifest.json` exists with operation dependencies and payload fingerprints
- [ ] **Cards created (or previewed):** Live mode persists via API with tags `["sweep-generated", "cabinet-v1"]`; dry-run records would-create outputs with zero write attempts
- [ ] **Drucker/Porter priority assigned:** P1-P5 distribution recorded
- [ ] **3B write ledger emitted:** `docs/business-os/sweeps/<YYYY-MM-DD>-write-ledger.jsonl` includes operation/status/fingerprint records
- [ ] **Card ID resolution honored:** fact-find writes occur only after `{{CARD_ID}}` resolution via card-id-map
- [ ] **Fact-find seeding (or previewed):** Live mode creates stage docs; dry-run records would-seed outputs with zero write attempts
- [ ] **Top-K pool deterministic:** Top-K selection used only newly promoted ideas from this sweep
- [ ] **Existing cards handled separately:** Existing cards were reported as reaffirmation/addendum only (not mixed into Top-K)
- [ ] **Context discipline:** Degradation status noted if applicable
- [ ] **Technical cabinet:** Status recorded (triggered/not triggered/skipped)
- [ ] **Technical cabinet routing recorded:** Every technical idea includes `applies_to` with business list or `["cross-cutting"]`
- [ ] **DGPs created:** Decision-gap proposals persisted with Gap-Type and tags `["sweep-generated", "cabinet-v1", "dgp", "gap:<type>"]`
- [ ] **DGP resurfacing executed:** Ready-now/watch queues reported for existing DGP backlog
- [ ] **Existing priorities checked:** Reaffirmation/addendum notes recorded for ideas matching existing cards
- [ ] **No PATCH calls:** Drucker/Porter ran before card creation; cards created with correct priority
- [ ] **Coverage rerun contract applied:** If coverage <80%, run marked partial with rerun packet; otherwise residual-risk note present
- [ ] **Delta/Coverage section present:** Includes promoted/held/killed and sub-expert coverage deltas vs prior sweep
- [ ] **Signal quality metrics recorded:** presentable-rate, unresolved-rate, and evidence-density included
- [ ] **Dry-run safety honored:** if `Persistence-Mode=dry-run`, no POST/PATCH writes were attempted for ideas/cards/stage-docs
- [ ] **Reconciliation output present for partial/stale runs:** includes retry commands and owner handoff

---

## Red Flags (Hard Guardrails)

If any of these are true, the sweep report is **invalid** and must be revised:

1. **Skipped divergence/deepening cadence.** Stage 1 must run as divergence (breadth) then deepening (depth).
2. **Generated >1 divergence candidate per sub-expert.** This dilutes focus and creates noise.
3. **Sent Stage 2 candidates without depth-gate fields.** Every candidate must include >=2 evidence pointers, falsification-test, and first-signal.
4. **Skipped confidence gate.** All ideas must pass through presentable/decision-gap/hunch classification.
5. **Skipped clustering.** Must attempt to group semantically similar ideas.
6. **Skipped Munger/Buffett filter.** All presentable ideas must receive Kill/Hold/Promote verdict.
7. **Created cards without Drucker/Porter priority.** Drucker/Porter (Stage 5) must run before card creation (Stage 6). All cards must have P1-P5 ranking at creation time.
8. **Created fact-find docs for low-priority cards.** Only global top K (default K=3) get fact-find docs.
9. **Persisted hunches.** Confidence-Score 0-29 ideas must NOT be persisted (log in report only).
10. **Ignored stance.** Generation and prioritization must reflect stance (improve-data vs grow-business).
11. **Invents metrics not present in the data.** All evidence must be observable.
12. **Deepened >10 candidates per business before Stage 2.** This violates focus cap and harms depth.
13. **Musk lens violates 5-step ordering.** Musk recommendations must follow strict step order (Question → Delete → Simplify → Accelerate → Automate).
14. **Mixed Top-K pool.** Existing cards must not be mixed into Top-K; Top-K must be newly promoted ideas from this sweep only.
15. **Skipped Contrarian Gate.** All presentable ideas must receive Contrarian Status (PASS/UNRESOLVED/FAIL) before capital-allocation verdict.
16. **Promoted with UNRESOLVED Contrarian Status.** Ideas with Contrarian Status UNRESOLVED must be Held (not Promoted). FAIL must be Killed (unless reframed as timeboxed test → Hold).
17. **Missing gate artifacts in decision log.** Both Contrarian Gate block and Munger-Buffett Filter block must appear in decision log for every idea that reaches Stage 4.
18. **Coverage <80% without rerun contract.** Runs below coverage threshold must be marked partial with rerun focus packet.
19. **Missing signal quality section/metrics.** Sweep must report presentable-rate, unresolved-rate, and evidence-density.
20. **Dry-run performed persistence writes.** In `--dry-run`, any POST/PATCH write call to ideas/cards/stage-docs is invalid.
21. **Missing Who Said What attribution for promoted/held ideas.** Promoted/held ideas must include originator sub-expert + lens.
22. **Missing Tool-Gap Register section.** Missing tools/data must be aggregated and reported with gap types.
23. **Hold/Kill rationale missing restart conditions.** Held/killed ideas must include reason code; held ideas must include restart condition.
24. **Missing Delta/Coverage section.** Sweep must compare promoted/held/killed outcomes and sub-expert coverage vs prior sweep.
25. **Assumptions precedence not honored.** If both inline assumptions and `--assumptions-file` are provided, file input must win and source must be reported.
26. **Technical cabinet idea missing `applies_to`.** Every technical idea must declare business targets or `["cross-cutting"]`.
27. **Verbosity mode violated.** Promoted idea summaries must respect configured word limits for compact/standard/extended modes.
28. **Assumption challenge missing despite provided assumptions.** When assumptions are provided, each must be verdicted (accept/condition/reject) with evidence and affected ideas.
29. **Economics gate bypassed.** Any idea promoted to card creation without complete economics fields and `Economics-Gate=pass` is invalid.
30. **Missing 3A commit manifest.** Persistence writes must be driven by deterministic manifest operations with dependency edges and payload fingerprints.
31. **Fact-find write attempted before card ID resolution.** `factfind_upsert` operations must resolve `{{CARD_ID}}` from card-id-map before write.
32. **Rerun duplicate write guard missing.** Writes must honor `operation_id + payload_fingerprint` skip rules using write ledger.
33. **PLAT/BOS idea lacks explicit sales unblock path.** Enabler ideas must name enabled revenue business, blocker, and unblock SLA.
34. **Standalone UI/DS cleanup promoted.** `@acme/ui` / `@acme/design-system` work without startup-sales linkage is invalid.
35. **CMS side-project overtakes sales work.** CMS 3-hour launch ideas exceeding side-lane budget or blocking startup sales work are invalid.
36. **Sales-go-live idea promoted without launch proof.** Missing unit/integration/e2e evidence, missing either user-testing source (CLI audit or ChatGPT), or missing SEO/GA4/Search Console monitoring evidence is invalid.
37. **Non-convergent startup checkout/inventory promoted.** Ideas that preserve long-term divergence from shared platform authority are invalid.
38. **CLI audit evidence ignores required audit settings.** Launch proof missing no-JS predicates (`NO_JS_BAILOUT_MARKER`, `hasNoI18nKeyLeak`, `hasMetadataBodyParity`, `hasSocialProofSnapshotDate`) or missing `...-seo-summary.json`/`...-seo-artifacts/` is invalid.
39. **Missing in-run progress updates.** No progress artifact, missing stage transition updates, or heartbeat gaps >90s during long stages is invalid.
40. **API degraded mode used without explicit dry-run opt-in.** `degraded-filesystem-only` without `--dry-run --allow-api-degraded` is invalid.
41. **API degraded mode used in live persistence mode.** Live mode must remain strict preflight; degraded fallback is dry-run only.

---

## Error Handling (Revised)

| Error | Action |
|---|---|
| Business list API fails | In strict mode: STOP (fatal preflight). In `--dry-run --allow-api-degraded`: continue with filesystem business list fallback, set `API-Preflight-Mode=degraded-filesystem-only`, mark run partial. |
| Maturity model missing | STOP (fatal). |
| Business plan missing | Flag as critical; use maturity fallback; continue. |
| People profiles missing | Use API defaults; flag; continue. |
| Persona file missing | Skip that sub-expert; note in report; continue. |
| Existing cards/ideas/stage-docs read fails | In strict mode: STOP (fatal preflight). In `--dry-run --allow-api-degraded`: continue without API dedup baseline, mark reaffirmation confidence low, set run partial. |
| Context budget exceeded | Switch to summary-block mode. Record coverage ratio. If coverage <80%, mark partial + set `Quality-Rerun-Required: yes` + emit rerun focus packet. If coverage >=80%, continue with residual-risk note. |
| Write call attempted during `--dry-run` | Stop persistence branch, mark run partial, record attempted endpoint as contract violation, continue with preview-only reporting. |
| Commit manifest missing/invalid | Stop persistence branch, mark run partial, record manifest validation failure and required remediation. |
| Card ID unresolved for fact-find upsert | Record failed `factfind_upsert` operation, skip write, keep run partial with reconciliation note. |
| Create idea fails | No blind retry. Reconcile once via list/read; if unresolved, record failure; continue; mark run partial. |
| Create card fails | No blind retry. Reconcile once via list/read; if unresolved, record failure; continue; mark run partial. |
| Upsert stage doc fails | Use latest-wins flow (GET -> PATCH/POST). Retry once only on PATCH 409; if still failing, record; continue; mark run partial. |
| Rate limit 429 | Backoff once for read/reconciliation operations; do not repeat non-idempotent idea/card POST blindly. |
| Discovery index rebuild fails | Retry once; if still fails, mark `discovery-index stale`, keep run partial, include reconciliation checklist with rerun command + owner. |
| Progress artifact write/update fails | Continue sweep, emit terminal warning on each stage transition, mark run partial, and include manual reconstruction steps in reconciliation checklist. |
| `BOS_AGENT_API_BASE_URL` or API key missing | STOP (fatal). |
| `--allow-api-degraded` used without `--dry-run` | STOP before Stage 1 with contract error; degraded mode is dry-run only. |

---

## Integration with Other Skills

| Sweep Output | Next Skill | When |
|---|---|---|
| Missing business plan | `/update-business-plan` | Bootstrap or update the plan |
| Missing people profiles | `/update-people` | Bootstrap profiles with current-state data |
| Top-priority card with fact-find doc | `/fact-find <card-id>` | Deep-dive investigation |
| Card without fact-find doc | `/fact-find <card-id>` | Manual fact-find if desired |
| Card ready for planning | `/plan-feature <slug>` | After fact-find completes |
| DGP created (data gap) | Next sweep with `improve-data` stance | DGP pickup for investigation |
| DGP created (timing gap) | Trigger condition met | Re-evaluate when trigger fires |
| DGP created (dependency gap) | Prerequisite work completes | Re-evaluate after dependency resolved |
| DGP resurfaced (ready-now) | `/work-idea <idea-id>` -> `/fact-find <card-id>` | Convert resurfaced idea to card, then execute investigation |
| Technical cabinet not triggered | Next sweep with trigger conditions | Run occurs automatically when stance/flags/diff artifacts trigger |

---

## Completion Messages

**Standard:**
> "Cabinet sweep complete. Report: `docs/business-os/sweeps/<YYYY-MM-DD>-sweep.user.md`. Progress log: `docs/business-os/sweeps/<YYYY-MM-DD>-progress.user.md`. Stance: `{stance}`. {N} sub-experts run. {X} presentable ideas, {Y} decision-gaps, {Z} hunches. {N} cards created (P1: A, P2: B, P3: C). {K} fact-find docs seeded. Technical cabinet: {status}."

**First sweep (no plans):**
> "First Cabinet sweep complete. Report: `docs/business-os/sweeps/<YYYY-MM-DD>-sweep.user.md`. Progress log: `docs/business-os/sweeps/<YYYY-MM-DD>-progress.user.md`. CRITICAL: No business plans exist. Drucker/Porter operating in degraded mode with maturity model fallback. Recommendation: Bootstrap plans via `/update-business-plan`."

**Context degradation:**
> "Cabinet sweep complete with context degradation. Report: `docs/business-os/sweeps/<YYYY-MM-DD>-sweep.user.md`. Progress log: `docs/business-os/sweeps/<YYYY-MM-DD>-progress.user.md`. Context limit reached after {N} of {M} sub-experts. Switched to summary-block mode. {X} presentable ideas generated. {N} cards created."

**Dry run:**
> "Cabinet sweep dry-run complete. Report: `docs/business-os/sweeps/<YYYY-MM-DD>-sweep.user.md`. Progress log: `docs/business-os/sweeps/<YYYY-MM-DD>-progress.user.md`. Persistence mode: dry-run (no ideas/cards/stage-doc writes). {X} presentable ideas, {Y} would-create cards, {K} would-seed fact-find docs."

**Dry run (API degraded fallback):**
> "Cabinet sweep dry-run complete with API degraded fallback. Report: `docs/business-os/sweeps/<YYYY-MM-DD>-sweep.user.md`. Progress log: `docs/business-os/sweeps/<YYYY-MM-DD>-progress.user.md`. API-Preflight-Mode: degraded-filesystem-only. Dedup baseline confidence reduced; review reaffirmations manually."

---

## Phase 0 Constraints

- **Pete-triggered only.** No automated scheduling or self-invocation.
- **Agent identity.** All API calls use the agent API key. Ideas tagged `["sweep-generated", "cabinet-v1"]`. DGPs tagged `["sweep-generated", "cabinet-v1", "dgp", "gap:<type>"]` (plus `held` when applicable). Cards tagged `["sweep-generated", "cabinet-v1"]`.
- **Prompt-only.** All orchestration logic lives in this SKILL.md. No TypeScript modules. Extract to code later if patterns stabilize.
- **Max 3 fact-find docs per sweep.** Prevents flooding the fact-finding queue.
- **File reads for plans/profiles/personas.** Agent API doesn't expose these yet. Read directly from filesystem.
- **Sweep outputs per invocation.** One final sweep report plus one progress artifact in `docs/business-os/sweeps/`.
- **Default stance:** `improve-data` if no `--stance` parameter provided.
- **Default verbosity:** `standard` if no `--verbosity` parameter provided.
- **Dry-run support:** `--dry-run` keeps full analysis/ranking but blocks Stage 6/7 persistence writes (ideas/cards/stage-docs) and records preview outputs only.
- **Optional degraded dry-run preflight:** `--allow-api-degraded` may be used only with `--dry-run`; it enables filesystem-only fallback when Agent API preflight fails.
- **Live-mode strictness:** live runs must never use degraded API preflight fallback.
- **Assumptions precedence:** if both inline assumptions and `--assumptions-file` are provided, file input takes precedence.
- **Technical cabinet active:** Runs only when trigger conditions in the Technical Cabinet section are met.
- **Generation cadence locked:** Divergence (max 1 candidate per sub-expert) then deepening (top 8, hard cap 10 per business) before Stage 2.

---

## Success Metrics

- Sweep report produced in <10 minutes (all 7 stages)
- Every business analyzed by all available sub-experts (or degraded gracefully)
- Confidence gate produces meaningful distribution (not all presentable, not all hunches)
- Clustering reduces duplicate ideas (at least 20% reduction if semantic overlap exists)
- Munger/Buffett filter kills at least 10% of presentable ideas (prevents "everything is good" bias)
- Drucker/Porter produces meaningful P1-P5 distribution (not all P3)
- Top K cards receive fact-find docs for immediate investigation
- DGPs created with VOI-Scores for future sweep pickup
- Existing DGP backlog is resurfaced each sweep with ready-now/watch states
- Context discipline prevents token exhaustion
- Stance is respected in generation and prioritization stages
- Pete finds the report useful for strategic prioritization (subjective)

---

## Version History

- **v3.6** (2026-02-11): Added explicit API preflight mode contract and runner hardening: introduced `--allow-api-degraded` (dry-run only), strict live-mode preflight requirement, `API-Preflight-Mode` frontmatter/reporting, degraded fallback/error-handling rules, and recommended env-loading wrapper `scripts/run-ideas-go-faster.sh` with initiator-agent-preserving execution (codex/claude auto-select).
- **v3.5** (2026-02-11): Added mandatory in-run progress update contract: progress artifact (`<YYYY-MM-DD>-progress.user.md`) with stage-transition events + `<=90s` heartbeat cadence during long stages, terminal progress-line emission rules, progress linkage in sweep frontmatter, checklist/red-flag enforcement, and failure-handling contract for progress write errors.
- **v3.4** (2026-02-10): RS-03 write-safety split update: introduced explicit 3A/3B persistence contracts (Stage 5.5 prepare manifest with operation dependencies + payload fingerprints; Stage 6/7 commit using write-ledger, card-id-map, and rerun skip guard `operation_id + payload_fingerprint`), plus checklist/red-flag/error-handling requirements for manifest/ledger/card-id resolution.
- **v3.3** (2026-02-10): RS-02B behavioral-gate update: added Assumption Challenge (F3) verdict contract (`accept|condition|reject`) with dependency effects on idea eligibility; added Economics Gate (F5) blocker contract requiring upside/downside/reversibility/cost-of-delay/time-to-signal before card eligibility; updated report sections, checklist, and red flags accordingly.
- **v3.2** (2026-02-10): RS-02C input/UX contract update: added assumptions precedence contract (inline vs `--assumptions-file`), `Verbosity-Mode` frontmatter + word-limit policy (`compact|standard|extended`), and technical cabinet `applies_to` semantics (`[<BIZ>...]` or `["cross-cutting"]`) with checklist/red-flag enforcement.
- **v3.1** (2026-02-10): RS-02A transparency contract update: added deterministic report sections for Who Said What (F1), Tool-Gap Register (F2), Kill/Hold Rationale (F4), and Delta/Coverage (F6); updated Evaluation Checklist and Red Flags to require these sections.
- **v3.0** (2026-02-10): Added `--dry-run` preview mode for persistence-safe sweep execution. Dry-run now computes full pipeline outputs (including ranking and Top-K) while blocking Stage 6/7 API writes (ideas/cards/stage-docs), adding explicit preview reporting, persistence-mode frontmatter, dry-run safety checklist items, red-flag enforcement, and completion messaging.
- **v2.9** (2026-02-10): Contrarian Gate integration: Stage 4 now runs two-phase process (Munger-Thiel Contrarian Gate producing PASS/UNRESOLVED/FAIL → Munger-Buffett Capital-Allocation Verdict constrained by gate status); Stages 5-6 enforce input validation (Promote + PASS only); Stage 7 adds Contrarian Status boost to Top-K selection and gate artifact summaries to fact-find templates; Sweep Report adds Contrarian Gate counts and dedicated report section; Evaluation Checklist gains gate verification items; Red Flags expanded with gate violation rules (12-14).
- **v2.8** (2026-02-09): Stage 7b optional contract formalized (explicit activation flag, deterministic single-slot selector, separate reporting section, disable path, decision memo reference); remains disabled by default in Phase 0.
- **v2.7** (2026-02-09): DGP resurfacing made explicit (preflight queue with ready-now/watch states and report section); Stage 7 Top-K pool made deterministic (newly promoted ideas from this sweep only); existing cards explicitly handled as reaffirmation/addendum only.
- **v2.6** (2026-02-09): Consistency/hardening patch: generic sourcing sub-experts now align to `finder/bridge/mover` (replacing stale `cook/fung/ohno` routing); confidence tier standardized to `decision-gap`; DGP tag schema normalized to `["sweep-generated", "cabinet-v1", "dgp", "gap:<type>"]`; traction fast-track wording now explicitly preserves the `fact-find → plan-feature → build-feature` gate (Rigor Pack pre-populates fact-find but does not bypass it).
- **v2.5** (2026-02-09): Traction-mode integration: Stage 5 now activates traction mode under grow-business for market-facing L1-L2 businesses (Rigor Pack output, P1 cap, reversibility rule wiring, traction-mode Decision Log format); Stage 7 uses Rigor Pack content to pre-populate fact-find stage docs for traction P1/P2 (fast-track fact-find prep); infrastructure businesses excluded from traction mode.
- **v2.4** (2026-02-09): v2.1 operational changes: API as business source-of-truth (not businesses.json); preflight reads existing priorities to prevent re-creating ideas (Existing Priority Set + Canon, reaffirmation/addendum mechanism); Impact fields added to dossiers (Impact-Type, Impact-Mechanism, Impact-Band, Impact-Confidence); Drucker/Porter reordered before card creation (no PATCH needed); P1-P3 card creation threshold; global top-K selection (Priority > Impact > Confidence); Decision Gap Proposals replace Data Gap Proposals (Gap-Type: data/timing/dependency); two-phase failure policy (fatal preflight + best-effort persistence); Technical Cabinet revised with explicit diff artifact triggers; sweep report adds Run-Status, reaffirmations, persistence accounting.
- **v2.3** (2026-02-09): Replaced Ellison with Benioff (startup challenger positioning); split sales experts into individual files; updated persona file reading for both marketing and sales split files.
- **v2.2** (2026-02-09): Updated persona file reading for split marketing expert files; Marketing lens now has coordinator + 4 individual expert files.
- **v2.1** (2026-02-09): Added BRIK-specific lens routing — Brikette lens (15 sub-experts across 6 hostel domains) replaces sourcing lens for BRIK. Hopkins/Ogilvy run twice for BRIK (marketing + brikette framing).
- **v2.0** (2026-02-09): Cabinet Secretary orchestrator with 7-stage pipeline, multi-lens composite generation, confidence gating, clustering, Munger/Buffett filter, Drucker/Porter priority, fact-find seeding. Replaces v1 constraint-diagnostic approach.
- **v1.0** (2026-02-06): Original constraint-diagnostic sweep (preserved in `SKILL.md.pre-cabinet`)
