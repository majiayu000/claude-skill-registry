---
name: product-management
description: Product management workflows — feature specs, roadmap planning, stakeholder updates, user research synthesis, competitive analysis, metrics review, sprint planning. Use when writing specs, updating roadmaps, briefing stakeholders, synthesizing research, or reviewing product metrics.
routing:
  triggers:
    - "product management"
    - "feature spec"
    - "PRD"
    - "roadmap"
    - "stakeholder update"
    - "user research"
    - "sprint planning"
    - "product metrics"
  category: business
  force_route: false
  pairs_with:
    - csuite
user-invocable: true
---

# Product Management

Umbrella skill for PM workflows: specs, roadmaps, stakeholder comms, research synthesis, competitive analysis, metrics review, sprint planning, and product brainstorming. Each mode loads its own reference files on demand.

---

## Mode Detection

Classify into one mode before proceeding.

| Mode | Signal Phrases | Reference |
|------|---------------|-----------|
| **SPEC** | write spec, PRD, feature requirements, acceptance criteria, user stories | `references/spec-writing.md` |
| **ROADMAP** | roadmap, prioritize, Now/Next/Later, reprioritize, timeline, OKR alignment | `references/roadmap-planning.md` |
| **STAKEHOLDER** | stakeholder update, status report, executive brief, launch announcement | (inline templates) |
| **RESEARCH** | synthesize research, interview analysis, user feedback, personas, thematic analysis | `references/research-synthesis.md` |
| **COMPETITIVE** | competitive brief, competitor analysis, battle card, positioning, win/loss | (inline templates) |
| **METRICS** | metrics review, KPI, funnel analysis, retention, cohort, dashboard, OKR scoring | `references/metrics-review.md` |
| **SPRINT** | sprint planning, backlog grooming, capacity, sprint goal, carryover | (inline templates) |
| **BRAINSTORM** | brainstorm, explore problem, stress-test idea, thinking partner, assumption testing | (Socratic — see below) |

If the request spans modes, pick the primary mode and note the secondary.

---

## Workflow by Mode

### SPEC Mode

**Load**: `references/spec-writing.md`, `references/llm-pm-failure-modes.md`

1. **Understand** — Accept any input: feature name, problem statement, user request, vague idea.
2. **Gather context** — Ask conversationally (not a wall of questions):
   - User problem and who experiences it
   - Target users / segments
   - Success metrics (how will we know it worked?)
   - Constraints: technical, timeline, regulatory, dependencies
   - Prior art: attempted before? Existing solutions?
3. **Generate PRD** with these sections:

| Section | Content |
|---------|---------|
| Problem Statement | 2-3 sentences. Who, how often, cost of not solving. Grounded in evidence. |
| Goals | 3-5 measurable outcomes. Outcomes not outputs. |
| Non-Goals | 3-5 explicit exclusions with rationale. |
| User Stories | "As a [specific type], I want [capability] so that [benefit]." Group by persona. Include edge cases. |
| Requirements | P0 (must-have), P1 (nice-to-have), P2 (future). Each with acceptance criteria. |
| Success Metrics | Leading (days-weeks) and lagging (weeks-months). Specific targets with measurement method. |
| Open Questions | Tagged by owner (eng, design, legal, data). Blocking vs non-blocking. |
| Timeline | Hard deadlines, dependencies, phasing. |

4. **Review** — Offer iteration, expansion, follow-up artifacts (design brief, ticket breakdown).

**Acceptance criteria format**: Given/When/Then or checklist. Cover happy path, error cases, edge cases. No ambiguous words ("fast", "intuitive") without concrete definitions.

**Scope management**: Write explicit non-goals. Any scope addition requires a scope removal or timeline extension. Separate v1 from v2. Time-box investigations.

### ROADMAP Mode

**Load**: `references/roadmap-planning.md`, `references/llm-pm-failure-modes.md`

1. **Current state** — Get existing roadmap (paste, describe, or build from scratch).
2. **Determine operation**:

| Operation | Inputs | Key Actions |
|-----------|--------|-------------|
| Add item | Name, priority, effort, timeframe, owner, dependencies | Suggest placement based on priorities and capacity |
| Update status | Item + new status (not started / in progress / at risk / blocked / completed / cut) | For at-risk/blocked: require blocker + mitigation |
| Reprioritize | What changed (strategy shift, new data, resource change) | Apply framework (RICE, ICE, MoSCoW, Value/Effort). Show before/after. |
| Move timeline | Why (scope change, dependency slip, resource constraint) | Identify downstream impacts. Flag hard-deadline conflicts. |
| Create new | Timeframe, format preference, initiative list | Use Now/Next/Later unless user specifies otherwise |

3. **Generate** — Status overview, items grouped by timeframe/theme, risks/dependencies, change summary.
4. **Follow up** — Offer audience-specific formatting, change communication drafts.

**Capacity rule**: When adding to roadmap, always ask "What comes off?" Roadmaps are zero-sum against capacity.

### STAKEHOLDER Mode

1. **Update type**: Weekly / Monthly / Launch / Ad-hoc
2. **Audience detection**:

| Audience | Frame | Length |
|----------|-------|--------|
| Executives | Outcome-focused, G/Y/R status, strategic alignment | < 300 words |
| Engineering | Technical detail, links to PRs/tickets, decisions needed with options | As needed |
| Cross-functional | Impact on their team, asks with deadlines, input opportunities | Medium |
| Customers | Benefits-focused, no jargon, honest timelines | Short |
| Board | Metrics-driven, risk-focused, strategic | Very concise |

3. **Generate** using audience-appropriate template.
4. **Risk communication** — Use ROAM framework (Resolved, Owned, Accepted, Mitigated). Every risk comes with: clear statement, quantified impact, likelihood with evidence, mitigation plan, specific ask.

**Executive update rule**: Lead with conclusion, not journey. "We shipped X and it moved Y" not "we had 14 standups." Status color reflects reality, not optimism.

**Gate**: Update draft exists. Audience-appropriate framing verified (no engineering jargon in exec updates, no hand-waving in engineering updates). Every risk has a ROAM classification.

### RESEARCH Mode

**Load**: `references/research-synthesis.md`, `references/llm-pm-failure-modes.md`

1. **Gather inputs** — Accept any combination: pasted text, uploaded files, described findings.
2. **Process** — For each source extract: observations, verbatim quotes, behaviors (vs stated preferences), pain points, positive signals, context.
3. **Thematic analysis**:
   - Familiarize -> Initial coding -> Theme development -> Theme review -> Theme refinement -> Report
   - Affinity mapping: one observation per note, let clusters emerge, split large clusters.
   - Triangulation: methodological, source, temporal. Findings supported by multiple sources are stronger.
4. **Priority matrix**:

| | High Impact | Low Impact |
|---|---|---|
| **High Frequency** | Top priority | Quality-of-life |
| **Low Frequency** | Segment-specific | Note and deprioritize |

5. **Generate synthesis**: Research overview, 5-8 key findings (with evidence, frequency, impact, confidence), user segments/personas, opportunity areas, actionable recommendations, open questions.

**Critical rule**: Distinguish behaviors from stated preferences. Behavioral data always outweighs what users say they want. Quote attribution uses participant type ("Enterprise admin, 200-person team"), never names.

### COMPETITIVE Mode

1. **Scope** — Which competitor(s)? Full comparison or specific area? What decision does this inform?
2. **Research** — Product pages, pricing, changelogs, customer reviews (G2, Capterra), job postings (strategic signals), community discussions.
3. **Generate brief**:
   - Competitor overview (company, positioning, momentum)
   - Feature comparison matrix (Strong/Adequate/Weak/Absent ratings)
   - Positioning analysis (For [target] who [need], [Product] is a [category] that [benefit])
   - Honest strengths and weaknesses
   - Opportunities and threats
   - Strategic implications: build/accelerate/deprioritize, differentiate vs parity, positioning adjustments
4. **Competitive set levels**: Direct (same problem, same way), Indirect (same problem, different way), Adjacent (could expand into your space), Substitute (entirely different approach including "do nothing").

**Honesty rule**: Dismissing competitors makes analysis useless. Rate based on real product experience and customer feedback, not marketing claims. Be honest about where competitors lead.

**Gate**: Competitive brief exists with feature matrix, positioning analysis, and strategic implications. At least one honest "they lead here" finding present.

### METRICS Mode

**Load**: `references/metrics-review.md`, `references/llm-pm-failure-modes.md`

1. **Gather data** — Get metrics with comparison data (previous period, targets). Ask about known events (launches, incidents, seasonality).
2. **Organize** — Use metrics hierarchy:

| Level | Purpose | Examples |
|-------|---------|---------|
| North Star | Core value delivered | WAU completing core workflow |
| L1 (Health) | Lifecycle stages | Acquisition, Activation, Engagement, Retention, Monetization, Satisfaction |
| L2 (Diagnostic) | Drill-down | Funnel steps, feature adoption, segment breakdowns, performance |

3. **Analyze** — For each metric: current value, trend, vs target, rate of change, anomalies. Identify correlations, leading indicators, segment-driven aggregate trends.
4. **Generate review**: Summary (2-3 sentences), scorecard table, trend analysis, bright spots, areas of concern, recommended actions, caveats.
5. **Goal-setting support**: OKRs (2-3 objectives, 2-4 KRs each, outcomes not outputs, 70% completion = target for stretch). Target-setting: baseline -> benchmark -> trajectory -> effort -> confidence.

**Context rule**: Absolute numbers without comparison are useless. Always show vs previous period, vs target, vs benchmark. Small fluctuations are noise — focus on meaningful changes.

### SPRINT Mode

1. **Gather**: Team roster + availability, sprint length, prioritized backlog, carryover, dependencies.
2. **Capacity calculation**: Available days minus overhead (meetings, on-call, PTO). Rule of thumb: 60-70% of time on planned work.
3. **Allocation**: 70% planned features, 20% tech health, 10% unplanned buffer.
4. **Generate sprint plan**:
   - Sprint goal (one sentence)
   - Capacity table (person, available days, allocation, notes)
   - Sprint backlog (P0 must-ship, P1 should-ship, P2 stretch)
   - Planned capacity vs sprint load (target 70-80%)
   - Risks with impact and mitigation
   - Definition of done
   - Key dates (start, mid-sprint check, demo, retro)
5. **Carry over honestly** — If something did not ship, understand why before re-committing.

**Gate**: Sprint plan exists with goal, capacity table, prioritized backlog, and load vs capacity check showing 70-80% target.

### BRAINSTORM Mode (Socratic)

This mode is fundamentally different. The PM does not get a deliverable. They get a thinking partner. **Be opinionated. Push back. Bring unexpected angles. Challenge assumptions.**

**Session principles**:
- Apply frameworks to the specific problem at hand
- Generate, evaluate, then discuss before handing over
- Challenge ideas actively — push back with reasons
- Hold divergent exploration open before converging
- Explore multiple directions before committing

**Sub-modes** — Detect which fits and shift as conversation evolves:

| Sub-mode | When | Approach |
|----------|------|----------|
| Problem Exploration | PM has a problem area, not a defined problem | Ask "who has this problem?" and "what are they doing today?" Map the ecosystem. Distinguish symptoms from root causes. |
| Solution Ideation | Problem is well-defined, need options | Generate 5-7 distinct approaches before evaluating. Include one "do the opposite" and one "remove something." Resist early convergence. |
| Assumption Testing | PM has a direction, needs stress-testing | List every assumption (stated + unstated). Find the riskiest one. Suggest the cheapest test. Play devil's advocate. |
| Strategy Exploration | Big bets, positioning, direction | Map possible moves. Think in bets (odds, payoff). Consider second-order effects and competitive responses. |

**Session rhythm**: Frame -> Diverge -> Provoke -> Converge -> Capture.

**Ideation techniques**:
- Constraint removal: "What if no technical/budget/political constraints?"
- Analogies: "How does [another industry] solve this?"
- Inversion: "How would we make this worse?" Then reverse.
- Decomposition: Break into subproblems, solve independently, recombine.
- User hat-switching: Power user? New user? Admin? Someone who hates the product?

**Frameworks as thinking tools** (use when they help, not as templates):

| Framework | Structure | Failure Mode |
|-----------|-----------|-------------|
| **HMW** | "How might we [outcome] for [user] without [constraint]?" | Too broad ("improve onboarding") or too narrow ("add tooltip to step 3") |
| **JTBD** | "When [situation], I want to [motivation] so I can [outcome]." | Functional jobs are easy; emotional and social jobs are often more powerful. Ask "what did they fire?" |
| **Opportunity Solution Tree** | Outcome -> Opportunities (from research) -> Solutions (multiple per opportunity) -> Experiments (cheapest test) | Opportunities must trace to evidence, not imagination. One solution per opportunity = not enough exploration. |
| **First Principles** | State assumption -> Break to fundamentals -> Question each -> Rebuild | Use when team is stuck in incrementalism |
| **OODA** | Observe -> Orient -> Decide -> Act -> loop | Most teams get stuck in Orient. OODA says: orient with what you have, act, let next cycle correct. |
| **Reverse Brainstorming** | "How to make this worse?" -> List -> Reverse each | When team is stuck; people are better at identifying wrong than imagining right. |

**Provocation prompts**:
- "What is the strongest argument against this?"
- "Who would hate this and why?"
- "What are we not seeing?"
- "What if the opposite were true?"
- "What is the 10x more ambitious version?"

**Gate**: Session produced at least one challenge the PM hadn't considered. Captured decisions/next-steps documented. Frameworks used as thinking tools, not dumped as checklists.

---

## LLM Failure Modes in PM Work

See `references/llm-pm-failure-modes.md` for the complete failure mode catalog (vague specs, fabricated research, generic competitive analysis, metrics without context, happy-path-only specs, framework regurgitation, scope creep enablement). Universal failure modes in `skills/shared-patterns/llm-domain-failure-modes-base.md`.

---

## Prioritization Frameworks (Cross-Mode Reference)

Used in SPEC, ROADMAP, and SPRINT modes.

| Framework | Formula / Method | Best For |
|-----------|-----------------|----------|
| **RICE** | (Reach x Impact x Confidence) / Effort | Large backlog, quantitative comparison |
| **ICE** | Impact x Confidence x Ease (1-10 each) | Quick prioritization, early-stage |
| **MoSCoW** | Must / Should / Could / Won't | Scoping a release, forcing prioritization conversations |
| **Value vs Effort** | 2x2 matrix: Quick Wins, Big Bets, Fill-ins, Money Pits | Visual prioritization in team sessions |

**Failure modes**: Using a framework as a rubber stamp for a decision already made. If the RICE score does not match intuition, investigate why — do not just adjust the inputs until it does.

---

## Output Conventions

- Markdown with clear headers. Scannable. Busy stakeholders read headers and bold text.
- Tables for comparisons, scorecards, feature matrices.
- Status labels: **Done**, **On Track**, **At Risk**, **Blocked**, **Not Started**.
- Executive content: < 300 words. Engineering content: as detailed as needed.
- Every recommendation is specific enough to act on. "Improve onboarding" is not actionable. "Add progress indicator to setup flow" is.
