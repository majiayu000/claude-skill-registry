---
name: hr
description: People operations workflows — recruiting pipeline, performance reviews, compensation analysis, offer drafting, interview prep, onboarding, org planning. Use when managing hiring pipelines, writing performance reviews, analyzing compensation, drafting offers, or planning organizational changes.
routing:
  triggers:
    - "HR"
    - "human resources"
    - "recruiting"
    - "performance review"
    - "compensation"
    - "hiring"
    - "onboarding"
    - "org planning"
  not_for: "code performance review (use reviewer-code). This skill covers people performance reviews and HR operations."
  category: business
  force_route: false
  pairs_with:
    - csuite
    - data-analysis
user-invocable: true
---

# HR — People Operations

Umbrella skill for all people operations: recruiting, performance management, compensation, offer drafting, interview design, onboarding, org planning, people analytics, and policy lookup. Each mode loads its own references on demand.

**Scope**: Decisions and artifacts involving people's careers, compensation, and organizational structure. Use csuite for strategic business decisions, data-analysis for general analytics, professional-communication for non-HR business writing.

---

## Mode Detection

Classify the request into exactly one mode. If the request spans modes, choose the primary and note the secondary.

| Mode | Signal Phrases | References |
|------|---------------|------------|
| **RECRUITING** | Pipeline, candidates, sourcing, screening, hiring status, time to fill | `references/recruiting.md` |
| **PERFORMANCE** | Review, self-assessment, calibration, feedback, rating, promotion case | `references/performance-management.md` |
| **COMPENSATION** | Pay, salary, equity, comp bands, benchmarking, offer competitive, retention risk | `references/compensation.md` |
| **OFFER** | Draft offer, offer letter, comp package, signing bonus, start date | `references/compensation.md` |
| **INTERVIEW** | Interview plan, questions, scorecard, evaluation rubric, debrief | `references/recruiting.md` |
| **ONBOARDING** | New hire, first week, 30/60/90, onboarding checklist, buddy | `references/recruiting.md` |
| **ORG-PLANNING** | Headcount, reorg, team structure, span of control, org design | `references/org-planning.md` |
| **PEOPLE-ANALYTICS** | Attrition, headcount report, diversity metrics, org health, flight risk | `references/org-planning.md` |
| **POLICY** | PTO, benefits, leave, expenses, handbook, remote work policy | (no reference — use user-provided policy docs) |

**Always load**: `references/llm-hr-failure-modes.md` — applies to every mode.

---

## Sensitivity Guardrails

HR content touches people's careers, livelihoods, and legal rights. These guardrails are non-negotiable.

| Rule | Rationale |
|------|-----------|
| Source compensation data from user-provided or public databases | Invented market rates cause real pay decisions. State "I don't have current market data" when you don't. |
| Focus recommendations on skills, behaviors, outcomes | "Hire more [group]" or "this candidate fits the culture" introduces bias. Focus on skills, behaviors, outcomes. |
| Include legal review disclaimer on all binding language | Offer letters, policy interpretations, and termination language need legal review. Always state this. |
| Ask for jurisdiction before advising on compliance | Employment law varies by country, state, city. Ask for jurisdiction before advising on compliance, leave, or termination. |
| Minimize PII retention; use role/level identifiers | Names, salaries, SSNs, demographics — minimize retention. Use role/level when names aren't needed. |
| Flag when output needs legal review | Offer letters, PIPs, termination docs, policy changes, accommodation decisions — always flag. |

---

## Workflow

### Mode: RECRUITING

**Framework**: DEFINE → PIPELINE → EVALUATE

**Phase 1: DEFINE** — Clarify role requirements and pipeline structure.

- Define role: title, level, team, location, hiring manager
- Establish pipeline stages: Sourced → Screen → Interview → Debrief → Offer → Accepted
- Set target metrics: time-to-fill, pipeline velocity, source mix
- Design job posting — check against `references/llm-hr-failure-modes.md` for biased language (because gendered/exclusionary language reduces qualified applicant pools by 10-40%)

**Gate**: Role defined. Pipeline stages agreed. Posting reviewed for bias.

**Phase 2: PIPELINE** — Track and manage candidates through stages.

- Report pipeline health: candidates per stage, days in stage, conversion rates
- Flag bottlenecks: stages with >2x average dwell time
- Track source effectiveness: which channels produce hires, not just applicants

**Gate**: Pipeline metrics current. Bottlenecks identified.

**Phase 3: EVALUATE** — Structure interviews and decisions.

- Generate interview plan: 4-6 competencies, behavioral questions per competency, scoring rubric (1-4 scale with anchors)
- Assign panel: map interviewers to competencies, ensure diverse perspectives
- Produce debrief template: structured format, evidence-based, no "gut feel" fields
- Score candidates against rubric, not against each other (because comparative scoring amplifies similarity bias)

**Gate**: Interview kit complete. Debrief structured. Decision evidence-based.

**Onboarding sub-mode** (after offer acceptance):

- Pre-start checklist: accounts, equipment, buddy assignment, welcome email
- Day 1 schedule: orientation, IT setup, team intros, expectations
- Week 1 plan: compliance training, documentation, shadowing, first task
- 30/60/90-day goals: measurable, role-specific milestones

---

### Mode: PERFORMANCE

**Framework**: STRUCTURE → WRITE → CALIBRATE

**Phase 1: STRUCTURE** — Select review type and load template.

| Type | Use When |
|------|----------|
| Self-assessment | Employee writing their own review |
| Manager review | Manager writing review for direct report |
| Calibration prep | Preparing rating distributions for calibration meeting |

**Gate**: Review type selected. Template loaded.

**Phase 2: WRITE** — Generate review content with behavioral specificity.

Self-assessment:
- Key accomplishments: situation, contribution, impact (measurable)
- Goals review: status + evidence per goal
- Growth areas and challenges
- Next-period goals (specific, measurable)

Manager review:
- Overall rating with 2-3 sentence summary
- Strengths with specific behavioral examples (not personality traits)
- Development areas with actionable guidance (not vague directives)
- Goal achievement ratings with observations
- Development plan: skill → current level → target → actions
- Compensation recommendation with justification

**Constraint**: Describe observable behavior with specific examples ("documentation was incomplete on 3 of 5 deliverables") — because personality feedback triggers defensiveness and has no actionable path. See `references/llm-hr-failure-modes.md`.

**Gate**: Review content complete. All feedback behavior-based. Development areas actionable.

**Phase 3: CALIBRATE** — Prepare rating distribution and promotion cases.

- Team overview: employee, role, level, tenure, proposed rating
- Distribution check against targets: Exceeds (~15-20%), Meets (~60-70%), Below (~10-15%)
- Discussion points: borderline cases, role changes, first-at-level reviews
- Promotion candidates: current level, proposed level, evidence of next-level performance
- Compensation actions: promotions, equity refreshes, market adjustments, retention grants

**Constraint**: Present rating targets as guidelines, with flexibility for team context (because forced ranking creates perverse incentives and has been abandoned by most organizations).

**Gate**: Distribution documented. Promotion cases evidence-based. Compensation actions justified.

---

### Mode: COMPENSATION

**Framework**: BENCHMARK → ANALYZE → RECOMMEND

**Phase 1: BENCHMARK** — Establish market data context.

- Identify components: base salary, equity, bonus (target + signing), benefits
- Key variables: role, level, location, company stage, industry
- Data sources: user-provided data, public salary databases, uploaded CSVs
- **Never invent percentile numbers** — if you don't have data, say so explicitly and offer to analyze user-provided data

**Gate**: Components identified. Variables specified. Data sources declared.

**Phase 2: ANALYZE** — Score against market and internal equity.

- Percentile bands: 25th, 50th, 75th, 90th for each component
- Band placement: where each employee falls within their band (below/at/above)
- Internal equity: same-role comparisons, compression detection, tenure-pay correlation
- Outlier detection: employees significantly above/below band midpoints
- Retention risk: below-band + high performer = flight risk

**Constraint**: Always state data vintage and source limitations. "Based on 2024 Levels.fyi data" not "the market rate is $X" — because stale data presented as current causes underpayment or overpayment.

**Gate**: Analysis complete. Sources cited. Limitations stated.

**Phase 3: RECOMMEND** — Deliver actionable compensation recommendations.

- Adjustment recommendations with priority ranking
- Budget impact modeling: total cost of recommended changes
- Equity refresh guidance: vesting cliffs, refresh cadence, retention timing
- Offer structuring: base/equity/bonus mix by company stage and candidate preference

**Gate**: Recommendations prioritized. Budget impact calculated. Sources documented.

**Offer drafting sub-mode:**

- Assemble package: base, equity (shares + vesting schedule + valuation method), bonus (target + signing), benefits summary
- Draft offer letter text — include disclaimer: "This draft requires legal review before sending"
- Negotiation guidance for hiring manager: flexibility ranges, non-monetary levers, walk-away points
- Flag compliance requirements by jurisdiction (at-will language, non-compete enforceability, benefits mandates)

---

### Mode: ORG-PLANNING

**Framework**: ASSESS → MODEL → PLAN

**Phase 1: ASSESS** — Map current organizational state.

| Metric | Healthy Range | Warning Sign |
|--------|---------------|--------------|
| Span of control | 5-8 direct reports | <3 (too narrow) or >12 (too wide) |
| Management layers | 4-6 per 500 people | Excess layers = slow decisions |
| IC-to-manager ratio | 6:1 to 10:1 | <4:1 = top-heavy |
| Team size | 5-9 people | <4 = fragile, >12 = unmanageable |
| Single points of failure | 0 | Any = structural risk |

**Gate**: Current state mapped. Structural issues identified.

**Phase 2: MODEL** — Design target state and transition.

- Headcount modeling: role, level, location, cost, timeline, hiring sequence
- Org design options: functional, product, matrix, pod — with trade-offs per option
- Capacity planning: current capacity vs. planned work, gap analysis
- Sequencing: which hires unlock the most capacity or reduce the most risk

**Constraint**: Never recommend org changes based on individuals ("move Alice because she's difficult") — structure around roles and capabilities (because person-dependent org design creates fragility and masks management problems).

**Gate**: Target state modeled. Sequencing justified. Budget estimated.

**Phase 3: PLAN** — Convert to executable hiring roadmap.

- Phased hiring plan: Q1/Q2/Q3/Q4 with roles, cost, dependencies
- Reporting line changes with communication plan
- Risk mitigation: what happens if key hires take longer than planned
- Success metrics: time to productivity, team health scores, delivery velocity

**Gate**: Roadmap executable. Risks mitigated. Success metrics defined.

**People analytics sub-mode:**

- Headcount reports: by team, location, level, tenure — snapshot and trend
- Attrition analysis: voluntary/involuntary, regrettable/non-regrettable, by team, trend lines
- Diversity metrics: representation by level/team/function, pipeline diversity, promotion rate parity, pay equity
- Engagement indicators: survey scores, eNPS, participation rates, theme analysis
- Flight risk modeling: below-band compensation + low engagement + tenure inflection points

---

### Mode: POLICY

**Framework**: FIND → EXPLAIN → CAVEAT

1. Search user-provided policy documents or handbook
2. Answer in plain language — no legalese
3. Quote specific policy language with source citation
4. Note exceptions and special cases
5. For legal/compliance questions: "Consult HR or legal directly for your specific situation"

**Constraint**: Answer only from user-provided policy documents. State when no source is available — do not guess (because fabricated policy guidance creates liability).

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No compensation data | User asks "what should we pay" without data | State limitation explicitly. Offer to analyze user-provided data or recommend public sources (Levels.fyi, Glassdoor, Radford). |
| Biased language in output | LLM generates gendered, ageist, or exclusionary phrasing | Run output against `references/llm-hr-failure-modes.md` bias checklist. Rewrite flagged phrases. |
| Jurisdiction unknown | Legal advice requested without location | Ask for jurisdiction before proceeding. Never default to US employment law. |
| Confidentiality scope unclear | User shares individual comp/performance data | Confirm intended audience. Remind that HR data is need-to-know. Minimize PII in outputs. |
| Template vs. real data confusion | User treats template placeholders as recommendations | Label all templates explicitly: "[PLACEHOLDER — replace with actual data]". |
| Policy not found | User asks about policy with no handbook provided | State clearly: no policy source available. Do not fabricate. Suggest uploading handbook. |

---

## References

| Reference | When to Load | Content |
|-----------|-------------|---------|
| `references/recruiting.md` | RECRUITING, INTERVIEW, ONBOARDING modes | Pipeline stages, velocity metrics, interview frameworks, evaluation rubrics, onboarding checklists |
| `references/performance-management.md` | PERFORMANCE mode | Review structure, calibration methodology, feedback patterns, development planning |
| `references/compensation.md` | COMPENSATION, OFFER modes | Market benchmarking, internal equity analysis, offer structuring, equity modeling |
| `references/org-planning.md` | ORG-PLANNING, PEOPLE-ANALYTICS modes | Headcount modeling, org design principles, capacity planning, people analytics |
| `references/llm-hr-failure-modes.md` | **Every mode** | Bias detection, fabrication risks, compliance gaps, inappropriate language patterns |
