---
name: ideas-go-faster
description: Radical business growth process auditor. Identifies missing or broken growth processes, diagnoses the #1 constraint per business, generates scored interventions using the Elon Musk 5-step algorithm, and autonomously creates cards from top-scoring ideas. No human in the loop.
---

# Ideas Go Faster

Radical business growth process auditor. Not a kanban health checker. Not a WIP counter. Not housekeeping.

This skill audits the business machine itself: identifying missing processes, broken feedback loops, unmeasured outcomes, and stalled growth levers. It reads business plans and people profiles as living inputs, compares reality to targets, diagnoses the single biggest constraint per business, generates interventions using the Elon Musk 5-step algorithm, and autonomously creates cards from top-scoring ideas.

Pete triggers the sweep via `/ideas-go-faster`. Everything after that is autonomous.

---

## Constitution (Non-Negotiable Invariants)

These rules override all other instructions. The sweep must not produce output that violates any of them.

### The Elon Musk 5-Step Algorithm (Strict Ordering)

Every recommendation must be classified into one of these steps. They are executed **in strict order** — you must exhaust each step before moving to the next. This is not a tiebreaker. This is the law.

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

### Deletion-First Forcing Questions

Before recommending ANY new work, force yourself through these questions:

- "What would happen if we removed this step entirely?"
- "Which tasks exist only because a previous decision wasn't revisited?"
- "Is this requirement a proxy for fear/risk that could be handled differently?"
- "Who requested this, and are they still the right person to own it?"
- "If we deleted this and nobody noticed for a week, was it ever needed?"

---

## Operating Mode

**READ + ANALYZE + WRITE (Ideas + Cards)**

**Allowed:**
- Read all agent API endpoints (businesses, people, cards, ideas, stage-docs)
- Read business plans from filesystem: `docs/business-os/strategy/<BIZ>/plan.user.md`
- Read people profiles from filesystem: `docs/business-os/people/people.user.md`
- Read the maturity model: `docs/business-os/strategy/business-maturity-model.md`
- Read previous sweep reports from `docs/business-os/sweeps/`
- Create raw ideas via `POST /api/agent/ideas`
- Create cards via `POST /api/agent/cards` (auto-work-up of top ideas)
- Create fact-find stage docs via `POST /api/agent/stage-docs`
- Write sweep report to `docs/business-os/sweeps/<YYYY-MM-DD>-sweep.user.md`

**Not allowed:**
- Modify existing cards, ideas, or stage docs (no PATCH calls)
- Move cards between lanes (use `/propose-lane-move`)
- Run destructive commands
- Auto-schedule or self-invoke
- Count WIP, compute aging metrics, or analyze lane distribution as primary outputs

**Fail-closed:** If any API call fails, stop and surface the error. Do not write the sweep report with partial data.

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

## Data Sources

### Agent API (Primary — cards, ideas, people capacity)

```
Base URL: ${BOS_AGENT_API_BASE_URL}
Auth Header: X-Agent-API-Key: ${BOS_AGENT_API_KEY}
```

| Endpoint | Returns |
|---|---|
| `GET /api/agent/businesses` | `{ businesses: Business[] }` |
| `GET /api/agent/people` | `{ people: Person[] }` (includes `capacity.maxActiveWip`) |
| `GET /api/agent/cards` | `{ cards: Card[] }` (all cards, all businesses, all lanes) |
| `GET /api/agent/ideas?location=inbox` | `{ ideas: Idea[] }` |
| `GET /api/agent/ideas?location=worked` | `{ ideas: Idea[] }` |
| `GET /api/agent/stage-docs?cardId={ID}` | `{ stageDocs: StageDoc[] }` |

### Filesystem (Plans, Profiles, Maturity Model)

| Source | Path | What it Contains |
|---|---|---|
| Business plans | `docs/business-os/strategy/<BIZ>/plan.user.md` | Strategy, risks, opportunities, learnings, metrics/KPIs |
| People profiles | `docs/business-os/people/people.user.md` | Roles, responsibilities, capabilities, gaps, availability |
| Maturity model | `docs/business-os/strategy/business-maturity-model.md` | L1/L2/L3 progression framework |
| Previous sweeps | `docs/business-os/sweeps/<date>-sweep.user.md` | Historical sweep reports |

**If a file does not exist:** Do not crash. Flag it as a finding. Missing business plans or people profiles are themselves critical gaps that the sweep must diagnose and act on.

---

## Sweep Workflow

### Step 1: Ingest Data

Fetch current state from all sources:

**API calls (parallel where possible):**
1. `GET /api/agent/businesses`
2. `GET /api/agent/people`
3. `GET /api/agent/cards`
4. `GET /api/agent/ideas?location=inbox`
5. `GET /api/agent/ideas?location=worked`
6. For each card in an active lane (Fact-finding, In progress, Blocked): `GET /api/agent/stage-docs?cardId={ID}`

**File reads:**
7. For each business: read `docs/business-os/strategy/<BIZ>/plan.user.md` (if exists)
8. Read `docs/business-os/people/people.user.md` (if exists)
9. Read `docs/business-os/strategy/business-maturity-model.md`
10. Read previous sweep report (most recent by date in `docs/business-os/sweeps/`)

**If any API call fails:** STOP. Surface the error. Do not proceed with partial data.
**If a file read fails:** Note the absence. Continue with available data. The absence is itself a finding.

### Step 2: Assess Each Business Against MACRO

For each business, walk through all 5 MACRO categories. For each diagnostic question, assess:

- **GREEN:** Process exists and is measurably effective
- **YELLOW:** Process exists but is incomplete, unmeasured, or underperforming
- **RED:** Process does not exist or is completely broken

Cross-reference against:
- The business plan (if exists): Are plan targets being pursued? What's drifting?
- The maturity model: What level is this business at? What does the next level require?
- Current cards/ideas: Is anyone working on the gaps?

### Step 3: Diagnose ONE Constraint Per Business

From the MACRO assessment, identify the **single most important constraint** for each business. Not two. Not three. One.

**Output format per business:**

> **Business:** {NAME} ({CODE})
> **Maturity:** L{N} → L{N+1}
>
> **Constraint statement:** "{BUSINESS} is rate-limited by ____."
>
> **MACRO category:** {Measure | Acquire | Convert | Retain | Operate}
>
> **Evidence:**
> - (3-7 bullets, each citing specific observable facts)
>
> **Confidence:** X/10
> - (if < 7: list specific evidence gaps)
>
> **Plan alignment:** {On track | Drifting | No plan exists}
>
> **What to question first (Musk Step 1):**
> - Who requested this constraint? Is it actually a requirement, or an assumption?
>
> **What to delete (Musk Step 2):**
> - What processes/tasks/approvals could be removed to relieve this?
>
> **Disproof signals:** What would we observe in the next sweep that proves this diagnosis wrong?

**Common mistakes:**
- Naming a symptom ("things are slow") instead of a mechanism ("no analytics means we can't measure whether 168 guides are generating traffic")
- Picking multiple constraints without ranking one as primary
- Making claims without observable evidence
- Diagnosing kanban lane health instead of business process health

### Step 4: Generate Interventions (Musk-Ordered)

For each business constraint, generate 3-5 interventions. **Strictly ordered by Musk algorithm** — list all Question/Delete interventions before any Simplify, list all Simplify before any Accelerate, list all Accelerate before any Automate.

Per intervention:

- **Title** — concise action statement
- **Musk step:** Question | Delete | Simplify | Accelerate | Automate
- **Targets constraint:** (link to the business constraint statement)
- **Mechanism:** Why this relieves the constraint
- **Evidence:** (2+ bullets from the data)
- **Score:** Impact (0-10), Confidence (0-10), Time-to-signal (0-10), Effort (0-10), Risk (0-10)
- **Priority:** `(Impact x Confidence x Time-to-signal) / (Effort x (1 + Risk))`
- **First step (<48h):** one concrete action
- **Measurement plan:** leading + lagging indicators
- **Suggested skill:** e.g., `/fact-find <topic>`, `/work-idea <title>`, `/update-business-plan`

**Scoring rules:**
- If Risk >= 8: require staged rollout + explicit reviewer
- If Confidence <= 4: treat as discovery — propose the minimal experiment, not a build
- When Priority scores are within 10%: prefer earlier Musk steps (Question/Delete over Automate)

**Confidence thresholds:**
- 0-3: Discovery needed — insufficient data to act
- 4-6: Weak evidence — design experiment first
- 7-8: Solid — evidence supports the intervention
- 9-10: Strong — clear signal from data

When confidence < 7, list the specific evidence gaps and what data would raise it.

### Step 5: Compare to Plan Targets & Forecast Trajectory

For each business with a plan:

1. **Extract plan targets** — KPIs, milestones, strategic priorities with target dates
2. **Compare to observable reality** — What progress is visible in cards, ideas, and stage docs?
3. **Assess trajectory:**

> **{BUSINESS} trajectory:**
> At current pace, {BUSINESS} will {reach/miss} {target} by {date}.
> Evidence: {2-3 bullets citing observable velocity/blockers}.
> To hit the target: {what would need to change}.

For businesses without plans:

> **{BUSINESS} trajectory:**
> No business plan exists. Cannot assess trajectory against targets.
> The #1 action is to bootstrap a plan via `/update-business-plan`.
> Based on maturity model position (L{N}), the next milestone is: {L{N+1} description}.

### Step 6: Write Sweep Report

Write to `docs/business-os/sweeps/<YYYY-MM-DD>-sweep.user.md` using the report template below.

### Step 7: Create Raw Ideas (Stage 1 — Autonomous)

For ALL interventions generated in Step 4 (across all businesses), create raw ideas in the inbox via the API:

```json
{
  "method": "POST",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/ideas",
  "headers": {
    "X-Agent-API-Key": "${BOS_AGENT_API_KEY}",
    "Content-Type": "application/json"
  },
  "body": {
    "business": "<business code>",
    "content": "# <Idea Title>\n\n**Source:** Sweep <YYYY-MM-DD>\n**Constraint:** <constraint statement>\n**Musk Step:** <Question|Delete|Simplify|Accelerate|Automate>\n**MACRO Category:** <Measure|Acquire|Convert|Retain|Operate>\n\n## Priority Score\n- Impact: X/10\n- Confidence: X/10\n- Time-to-signal: X/10\n- Effort: X/10\n- Risk: X/10\n- **Priority: X.X**\n\n## Mechanism\n<why this relieves the constraint>\n\n## Evidence\n- <bullet 1>\n- <bullet 2>\n\n## First Step (<48h)\n<concrete action>\n\n## Measurement\n- Leading: <indicator>\n- Lagging: <indicator>",
    "tags": ["raw", "sweep-generated", "sweep-<YYYY-MM-DD>"]
  }
}
```

### Step 8: Auto-Work-Up Top Ideas (Stage 2 — Autonomous)

For the top-scoring ideas (highest Priority), automatically create cards in the kanban system. These enter as Inbox cards, ready for `/fact-find`.

**Threshold:** Ideas with Priority score in the top 3 across all businesses, AND Priority > 5.0.

**Max 3 auto-created cards per sweep.** If more than 3 qualify, take the top 3 by Priority. The rest remain as raw ideas in the inbox.

For each auto-worked-up idea:

**1) Assign kanban priority (P0-P3):**

| Condition | Kanban Priority |
|---|---|
| Constraint is in Measure category AND business has zero analytics | P0 (Critical) |
| Constraint blocks maturity level progression | P1 (High) |
| Constraint is evidenced but doesn't block progression | P2 (Medium) |
| Constraint is low-confidence or discovery-needed | P3 (Low) |

**2) Create card via API:**

```json
{
  "method": "POST",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/cards",
  "headers": {
    "X-Agent-API-Key": "${BOS_AGENT_API_KEY}",
    "Content-Type": "application/json"
  },
  "body": {
    "business": "<business code>",
    "title": "<Idea Title>",
    "description": "<1-2 sentence summary of the constraint + mechanism>",
    "lane": "Inbox",
    "priority": "<P0|P1|P2|P3>",
    "owner": "Pete",
    "tags": ["sweep-auto", "sweep-<YYYY-MM-DD>"]
  }
}
```

**3) Create initial fact-find stage doc:**

```json
{
  "method": "POST",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/stage-docs",
  "headers": {
    "X-Agent-API-Key": "${BOS_AGENT_API_KEY}",
    "Content-Type": "application/json"
  },
  "body": {
    "cardId": "<card-id-from-create>",
    "stage": "fact-find",
    "content": "# Fact-Finding: <Idea Title>\n\n**Source:** Sweep <YYYY-MM-DD>\n**Constraint:** <constraint statement>\n**MACRO Category:** <category>\n**Musk Step:** <step>\n\n## Questions to Answer\n\n1. <Key question about feasibility>\n2. <Key question about approach>\n3. <Key question about measurement>\n\n## Evidence From Sweep\n\n- <evidence bullet 1>\n- <evidence bullet 2>\n\n## Recommendations\n\n- First step: <concrete action>\n- Measurement: <what to track>\n\n## Transition Decision\n\n**Status:** Needs fact-finding\n**Next Lane:** Fact-finding (when Pete reviews)"
  }
}
```

**All auto-created cards are tagged `sweep-auto`** so Pete can identify AI-generated work and review it. The sweep acts; Pete reviews the output, not the input.

---

## Plan & Profile Integration

### Reading Business Plans

For each business, attempt to read `docs/business-os/strategy/<BIZ>/plan.user.md`.

**If the plan exists:**
- Extract current strategic priorities and their statuses
- Extract KPI targets and current values
- Extract active risks and opportunities
- Compare plan priorities to active cards — are the right things being worked on?
- Check plan staleness — when was it last updated? Is it more than 30 days old?

**If the plan does not exist:**
- This is a **critical finding**. A business without a plan is flying blind.
- Generate an intervention: "Bootstrap business plan for {BIZ} via `/update-business-plan`"
- Score this intervention HIGH — Impact 9, Confidence 10, Time-to-signal 8, Effort 3, Risk 1

### Reading People Profiles

Attempt to read `docs/business-os/people/people.user.md`.

**If profiles exist:**
- Extract current workload and capacity per person
- Extract skills and knowledge gaps
- Use capability-to-requirement matching when scoring intervention Effort
- Flag capacity bottlenecks (person at >80% with high-priority work queued)

**If profiles do not exist:**
- Use API-provided defaults (`maxActiveWip: 3` per person)
- Generate an intervention: "Bootstrap people profiles via `/update-people`"
- Note that allocation recommendations are low-confidence without profiles

### Plan Staleness Signals

| Condition | Signal |
|---|---|
| Plan last updated >30 days ago | YELLOW — plan may be drifting from reality |
| Plan last updated >90 days ago | RED — plan is likely obsolete |
| Plan has metrics with no current values | YELLOW — measurement gap |
| Plan priorities don't match active cards | RED — plan-execution misalignment |

---

## Trajectory Forecasting

Keep it simple. Prose, not models. Evidence-based, not speculative.

### Per-Business Trajectory Statement

For each business, produce a trajectory statement in this format:

> **{BUSINESS} ({MATURITY}):** At current pace, {outcome prediction with timeframe}.
> Evidence: {2-3 observable facts}.
> To change this trajectory: {1-2 specific actions}.

**Examples:**

> **Brikette (L2→L3):** At current pace, Brikette will not reach L3 in 2026 because cross-app integrations require analytics infrastructure that does not exist. The 168 guides are invisible without measurement.
> Evidence: Zero GA/Search Console integration. No conversion tracking. 4 L3 cards in progress but none address analytics.
> To change this trajectory: Install Google Analytics and Search Console this week. Measure before building more.

> **Product Pipeline (Pre-L1):** At current pace, PIPE will not launch a product in 2026. No Amazon seller account. No fulfillment validated. No first product selected.
> Evidence: Zero revenue. No active cards addressing launch prerequisites.
> To change this trajectory: Set up Amazon seller account (2-hour task) and validate fulfillment for one test product.

### What Forecasting Needs (But Doesn't Have Yet)

The sweep should note what additional data would improve forecasts:
- Card completion velocity (requires transition timestamps — not currently tracked)
- Revenue time series (requires analytics — not currently installed)
- Content production rate (guides per week/month)
- Customer acquisition cost trends

These are inputs the sweep **requests** from the measurement infrastructure. It does not build the infrastructure.

---

## Sweep Report Template

```markdown
---
Type: Sweep
Date: YYYY-MM-DD
Previous-Sweep: docs/business-os/sweeps/YYYY-MM-DD-sweep.user.md  # or "None"
Businesses-Audited: N
Ideas-Created: N
Cards-Created: N
---

# Business Growth Audit — YYYY-MM-DD

## One-Pager

**Across all businesses, the single biggest constraint is: <one sentence>.**

- **Action 1:** <delete/question recommendation>
- **Action 2:** <simplify recommendation>
- **Action 3:** <accelerate recommendation>

**If we do nothing:** <one sentence consequence with timeframe>.

## Business Summaries

### {BUSINESS} — {Name} ({Maturity Level})

**Constraint:** "{BUSINESS} is rate-limited by ____."
**MACRO category:** {category}
**Confidence:** X/10
**Plan alignment:** {On track | Drifting | No plan exists}

**MACRO Scorecard:**

| Category | Status | Key Finding |
|----------|--------|-------------|
| Measure | RED/YELLOW/GREEN | <one-line finding> |
| Acquire | RED/YELLOW/GREEN | <one-line finding> |
| Convert | RED/YELLOW/GREEN | <one-line finding> |
| Retain | RED/YELLOW/GREEN | <one-line finding> |
| Operate | RED/YELLOW/GREEN | <one-line finding> |

**Trajectory:** <prose trajectory statement>

**Top Interventions (Musk-ordered):**

| Rank | Intervention | Musk Step | Priority | First Step |
|------|-------------|-----------|----------|------------|
| 1 | ... | Question/Delete | X.X | ... |
| 2 | ... | Simplify | X.X | ... |
| 3 | ... | Accelerate | X.X | ... |

(Repeat for each business)

## Detailed Interventions

### {BUSINESS}: Intervention 1 — {Title}

**Musk step:** {Question | Delete | Simplify | Accelerate | Automate}
**Targets constraint:** {constraint statement}
**MACRO category:** {category}

**Mechanism:** {why this relieves the constraint}

**Evidence:**
- {bullet 1}
- {bullet 2}

**Scores:** Impact X, Confidence X, Time-to-signal X, Effort X, Risk X → **Priority: X.X**

**First step (<48h):** {concrete action}

**Measurement:**
- Leading: {indicator}
- Lagging: {indicator}

**Suggested skill:** `/{skill} {args}`

(Repeat for each intervention, grouped by business)

## Ideas Created (Stage 1 — Raw)

| Business | Idea Title | Musk Step | Priority | Tags |
|----------|-----------|-----------|----------|------|
| ... | ... | ... | X.X | raw, sweep-generated |

## Cards Created (Stage 2 — Auto-Worked-Up)

| Card ID | Business | Title | Kanban Priority | Tags |
|---------|----------|-------|-----------------|------|
| ... | ... | ... | P0/P1/P2/P3 | sweep-auto |

## Plan & Profile Status

| Business | Plan Exists? | Plan Last Updated | Profiles Exist? |
|----------|-------------|-------------------|-----------------|
| ... | Yes/No | date or N/A | Yes/No |

## Reflection (vs Previous Sweep)

<If previous sweep exists:>

- **Constraint shifts:** {which businesses changed their #1 constraint}
- **Ideas acted on:** {which previous sweep ideas became cards or were completed}
- **Trajectory changes:** {improving/stable/degrading per business, with evidence}
- **What was wrong:** {predictions from last sweep that proved incorrect}

<If no previous sweep:>

First sweep — no prior data for comparison.

## Data Gaps & Forecast Inputs Needed

- {What data would improve the next sweep}
- {What measurement infrastructure is missing}
- {What would raise confidence on specific diagnoses}
```

---

## Evaluation Checklist (Pass/Fail)

After producing the sweep report, verify each item. If any FAIL, revise before finalizing.

- [ ] **Constraint named:** Every business has exactly ONE named constraint with evidence
- [ ] **Musk ordering enforced:** Interventions listed Question/Delete before Simplify before Accelerate before Automate
- [ ] **No kanban housekeeping:** Report does NOT contain WIP counts, aging tables, or lane distribution as primary analysis
- [ ] **Evidence-backed:** Every claim cites observable data (API snapshot, plan contents, or file state)
- [ ] **Ideas created:** Raw ideas posted to API with scores and tags
- [ ] **Cards created:** Top ideas auto-worked-up to cards (max 3) with `sweep-auto` tag
- [ ] **Trajectory included:** Every business has a prose trajectory forecast

---

## Red Flags (Hard Guardrails)

If any of these are true, the sweep report is **invalid** and must be revised:

1. **Recommends Automate before exhausting Delete.** The Musk algorithm is strict ordering, not a menu.
2. **Recommends new work without naming the constraint it relieves.** Every recommendation must tie to a specific constraint.
3. **Uses WIP counts, aging metrics, or lane distribution as primary analysis.** This is not a kanban health checker. Use business process gaps, not board state.
4. **Invents metrics not present in the data.** If you can't observe it, you can't claim it.
5. **Suggests "work harder/longer" as the main lever.** System problems require system solutions, not heroics.
6. **Produces >10 ideas with no prioritization.** Noise, not signal.
7. **Proposes risky changes with no rollout/rollback plan.** Risk >= 8 requires staged rollout.
8. **Reassigns work ignoring stated capacity.** Use people profile data. Respect limits.
9. **Conflates activity with progress.** More tasks does not mean more throughput.
10. **Optimizes something that should be deleted.** Step 3 before Step 2 is a red flag.

---

## Edge Cases

### No business plans exist

This is the expected state for the first sweep. Handle it:
- Flag as the **highest-priority finding** across all businesses
- Generate a P0 intervention: "Bootstrap business plan via `/update-business-plan`" for each business
- Use the maturity model as a proxy for strategic targets
- Note that plan-vs-reality comparison is impossible without plans
- All trajectory forecasts should note "No plan exists — forecasting against maturity model only"

### No people profiles exist

- Use API defaults (`maxActiveWip: 3` per person)
- Flag as a high-priority finding
- Generate an intervention: "Bootstrap people profiles via `/update-people`"
- Note that all allocation and capacity assessments are low-confidence

### API not available

- STOP immediately. Do not produce a sweep with stale or partial data.
- Surface the error with the URL and status code.
- Recommend: check `BOS_AGENT_API_BASE_URL` and `BOS_AGENT_API_KEY` environment variables.

### Business with no cards or ideas

- This is a signal, not an absence of data.
- A business with zero activity is either pre-launch (expected) or stalled (needs diagnosis).
- Check the maturity model position and plan targets to determine which.

### Previous sweep recommendations not acted on

- Note this explicitly in the Reflection section.
- If the same constraint appears in consecutive sweeps with no action taken, escalate its severity.
- Ask: "Why was this not acted on? Is the recommendation wrong, or is there a meta-constraint (capacity, priority, external dependency) blocking action?"

---

## Integration with Other Skills

| Sweep Output | Next Skill | When |
|---|---|---|
| Missing business plan | `/update-business-plan` | Bootstrap or update the plan |
| Missing people profiles | `/update-people` | Bootstrap profiles with current-state data |
| Auto-created card in Inbox | `/fact-find <card-id>` | Deep-dive before planning |
| Area needing investigation | `/fact-find <topic>` | When sweep evidence is insufficient |
| Card ready for planning | `/plan-feature <slug>` | After fact-find completes |
| Card ready to move lanes | `/propose-lane-move <card-id>` | When evidence supports transition |
| Stale card to reconsider | `/propose-lane-move <card-id>` | Suggest Done/Reflected for abandoned work |
| Repo changes to detect | `/scan-repo` | Complement sweep with change-detection |
| Idea needing work-up | `/work-idea <idea-id>` | Manual work-up for ideas below auto-threshold |

---

## Phase 0 Constraints

- **Pete-triggered only.** No automated scheduling or self-invocation.
- **Agent identity.** All API calls use the agent API key. Created ideas tagged `sweep-generated`. Created cards tagged `sweep-auto`.
- **Prompt-only.** All analysis logic lives in this SKILL.md. No TypeScript modules. Extract to code later if patterns stabilize.
- **Max 3 auto-created cards per sweep.** Prevents flooding the kanban with AI-generated work.
- **File reads for plans/profiles.** Agent API doesn't expose these yet. Read directly from filesystem.
- **No throughput metrics.** Cards have `Created` and `Updated` dates but no per-lane transition history. Cannot compute cycle time or throughput. Note this as a measurement gap.
- **Default capacity.** `maxActiveWip = 3` per person unless people profiles provide richer data.
- **Single sweep report per invocation.** One file in `docs/business-os/sweeps/`.

---

## Success Metrics

- Sweep report produced in <5 minutes
- Every business has exactly one named constraint with evidence
- At least one intervention per business is type Question or Delete
- All interventions follow strict Musk ordering
- No WIP tables, aging charts, or lane distribution in the report
- Raw ideas created with priority scores
- Top ideas auto-worked-up to cards with `sweep-auto` tag
- Missing plans/profiles flagged as findings (not crashes)
- Pete finds the report useful for strategic prioritization (subjective)

---

## Error Handling

| Error | Action |
|---|---|
| API returns non-200 | STOP. Surface error with URL and status code. Do not write partial report. |
| API returns empty cards list | Proceed. A business with zero cards is a finding, not an error. |
| Business plan file not found | Note absence. Generate "bootstrap plan" intervention. Continue sweep. |
| People profile file not found | Use API defaults. Generate "bootstrap profiles" intervention. Continue sweep. |
| Previous sweep file cannot be parsed | Skip reflection section. Note parsing error. |
| Rate limit hit (429) | STOP. Surface error. Wait 60 seconds and retry. |
| `BOS_AGENT_API_BASE_URL` not set | STOP. Inform user to set environment variable. |
| Idea creation fails | Log the failure. Continue with remaining ideas. Note in report. |
| Card creation fails | Log the failure. Continue with remaining cards. Note in report. |

---

## Completion Messages

**Standard:**
> "Sweep complete. Report: `docs/business-os/sweeps/<YYYY-MM-DD>-sweep.user.md`. {N} raw ideas created. {N} cards auto-created (tagged `sweep-auto`). Top constraint: <one-liner per business>. Suggested next step: `/<skill> <args>`."

**First sweep (no plans/profiles):**
> "First sweep complete. Report: `docs/business-os/sweeps/<YYYY-MM-DD>-sweep.user.md`. {N} raw ideas created. {N} cards auto-created. CRITICAL: No business plans or people profiles exist — bootstrapping these is the #1 recommendation. Run `/update-business-plan` for each business."

**Insufficient data:**
> "Sweep complete with limited confidence. Report: `docs/business-os/sweeps/<YYYY-MM-DD>-sweep.user.md`. Data gaps noted. Recommend: <specific data-gathering action>."
