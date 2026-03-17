---
name: estimation-patterns
model: standard
description: Practical estimation techniques for software tasks — methods comparison, decomposition, complexity multipliers, buffer calculation, bias awareness, and communication strategies. Use when estimating features, sprint planning, or presenting timelines to stakeholders.
---

# Estimation Patterns (Meta-Skill)

Systematic approaches for producing accurate, defensible software estimates.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install estimation-patterns
```


---

## When to Use

- Estimating a feature, bug fix, or project timeline
- Breaking down work for sprint planning or roadmap forecasting
- Presenting estimates to stakeholders or product managers
- Reviewing historical accuracy to calibrate future estimates
- Noticing a pattern of missed deadlines or blown budgets

---

## Estimation Methods

Choose the method that matches your context and audience.

| Method | Best For | Granularity | Pros | Cons |
|----------------------|-------------------------------|-----------------|-----------------------------------------------|-----------------------------------------------|
| T-Shirt Sizing | Roadmap planning, backlog grooming | XS, S, M, L, XL | Fast, low-friction, good for relative ranking | Not actionable for scheduling |
| Story Points | Sprint planning, team velocity | Fibonacci (1-21) | Abstracts away individual speed, tracks velocity | Meaningless outside the team, gaming risk |
| Time-Based | Client quotes, contractor work | Hours / days | Universally understood, maps to budgets | Anchoring bias, implies false precision |
| Three-Point | High-uncertainty tasks | Min / likely / max | Captures uncertainty range, enables PERT | Requires discipline to set honest bounds |
| Reference Comparison | Recurring task types | Relative to past | Grounded in real data, hard to argue with | Requires historical records, breaks on novelty |

**Three-point formula (PERT):**

```
Expected = (Optimistic + 4 x Likely + Pessimistic) / 6
Standard Deviation = (Pessimistic - Optimistic) / 6
```

Use the standard deviation to express confidence ranges (e.g., "3-5 days at 68% confidence, 2-6 days at 95%").

---

## Task Decomposition

Break work down until every sub-task is **< 4 hours** of effort. Anything larger hides unknowns.

| Level | Example | Target Size |
|----------------|-------------------------------------------|---------------|
| Epic | User authentication system | 2-6 weeks |
| Feature | OAuth2 login with Google | 3-10 days |
| Task | Implement callback handler | 1-3 days |
| Sub-task | Parse and validate OAuth token | 1-4 hours |
| Atomic step | Write token expiry check function | 30-90 minutes |

**Decomposition checklist:**

1. Can I describe what "done" looks like in one sentence?
2. Is there exactly one unknown, or zero?
3. Could a teammate pick this up without a walkthrough?
4. Is it under 4 hours? If no — split again.

**If you cannot decompose a task**, it signals a spike is needed. Timebox the spike (2-4 hours), then re-estimate.

---

## Complexity Multipliers

Apply these multipliers to your base estimate when complexity factors are present. Multipliers stack multiplicatively.

| Factor | Multiplier | Rationale |
|--------------------------|------------|----------------------------------------------------|
| New technology / stack | 1.5x | Learning curve, unexpected gotchas, doc-hunting |
| Unclear requirements | 2.0x | Discovery work, rework cycles, stakeholder alignment |
| Legacy code | 1.5x | Undocumented behavior, fragile tests, hidden coupling |
| Cross-team dependency | 1.5x | Coordination overhead, blocking, API negotiation |
| First-time task | 2.0x | No reference point, unknown unknowns dominate |
| Regulatory / compliance | 1.5x | Audit trails, review gates, documentation overhead |

**Example:** A 2-day base estimate on legacy code (1.5x) with unclear requirements (2.0x) becomes `2 x 1.5 x 2.0 = 6 days`.

**Rule:** Never apply more than 3 multipliers — if that many factors converge, the task needs a spike or a scope reduction, not a bigger number.

---

## Buffer Calculation

Raw estimates are point predictions. Reality is a distribution.

| Buffer Type | Rule of Thumb | When to Apply |
|------------------------|-------------------------|-------------------------------------------------|
| Known unknowns | +20% of total estimate | Integration points, third-party APIs, minor gaps |
| Unknown unknowns | +50% of total estimate | New domain, first release, greenfield system |
| Team velocity factor | / focus ratio (e.g., 0.7) | Account for meetings, reviews, context switching |
| Sequential dependency | +10% per handoff | Each team/person boundary adds coordination drag |

**Effective estimate formula:**

```
Effective = (Base Estimate x Multipliers) / Focus Ratio + Buffer
```

**Focus ratio guidelines:**

| Scenario | Typical Focus Ratio |
|-----------------------------------|---------------------|
| Dedicated to one project | 0.75-0.85 |
| Split across 2 projects | 0.50-0.60 |
| On-call rotation active | 0.60-0.70 |
| Heavy meeting load (> 3h/day) | 0.45-0.55 |

---

## Historical Calibration

Track actual vs estimated to improve over time. This is the single most effective way to get better at estimation.

**Tracking table:**

| Task | Estimated | Actual | Ratio (A/E) | Notes |
|---------------------|-----------|--------|-------------|--------------------------|
| Auth flow | 3 days | 5 days | 1.67 | OAuth docs were outdated |
| Dashboard charts | 5 days | 4 days | 0.80 | Reused existing component |
| DB migration | 2 days | 6 days | 3.00 | Discovered data quality issues |

**Accuracy ratio:** Calculate your rolling average of `Actual / Estimated` over the last 10-20 tasks.

- Ratio **< 0.8** — you're overestimating (sandbagging or excessive buffers)
- Ratio **0.8-1.2** — well calibrated
- Ratio **> 1.2** — you're underestimating (apply the ratio as a correction factor)

**Calibration action:** Multiply future estimates by your rolling accuracy ratio until it converges toward 1.0.

---

## Common Estimation Biases

Recognize these cognitive traps — awareness alone reduces their effect.

| Bias | Description | Mitigation |
|---------------------|----------------------------------------------------------|---------------------------------------------------|
| Planning Fallacy | Assuming best-case scenario despite past evidence | Use historical data, not intuition |
| Anchoring | First number heard dominates all subsequent estimates | Estimate independently before discussing |
| Optimism Bias | "It'll be simpler than last time" | Apply the three-point method, honor the pessimistic |
| Scope Creep | Estimate stays fixed while scope grows | Re-estimate when scope changes, always |
| Hofstadter's Law | "It always takes longer, even when you account for it" | Add buffer, then add more buffer for novel work |
| Dunning-Kruger | Novices underestimate; experts sometimes overestimate | Cross-check with a second estimator |
| Sunk Cost Pressure | Refusing to re-estimate because the original was "approved" | Treat estimates as living artifacts, update often |

---

## Estimation by Task Type

Use these ranges as starting heuristics, then adjust with multipliers and historical data.

| Task Type | Typical Range | Key Variables |
|---------------------|------------------|------------------------------------------------|
| Bug fix (isolated) | 2-8 hours | Reproducibility, code familiarity, test coverage |
| Bug fix (systemic) | 1-3 days | Root cause depth, blast radius, regression risk |
| Small feature | 1-3 days | Spec clarity, UI complexity, number of endpoints |
| Medium feature | 3-10 days | Cross-cutting concerns, data model changes |
| Large feature | 2-4 weeks | Architecture decisions, team coordination |
| Refactor (local) | 1-3 days | Test coverage, coupling, blast radius |
| Refactor (systemic) | 1-4 weeks | Number of callers, migration strategy needed |
| Spike / research | 2-8 hours (timeboxed) | Always timebox — output is knowledge, not code |
| DevOps / infra | 1-5 days | Provider docs quality, IAM complexity, testing |

---

## Communication

How you present an estimate matters as much as the number itself.

**Always present as a range, never a single number:**

- Bad: "It'll take 5 days."
- Good: "3-7 days, most likely 5. The range depends on the payment API response format — I'll know more after the spike."

**Confidence levels:**

| Confidence | What It Means | When to Use |
|------------|--------------------------------------------|------------------------------------|
| High (+-15%) | Well-understood scope, done similar before | Familiar task, clear spec |
| Medium (+-30%) | Some unknowns, reasonable decomposition | Most sprint-level estimates |
| Low (+-50%+) | Significant unknowns, rough order of magnitude | Roadmap forecasts, presale quotes |

**Stakeholder communication rules:**

1. State the range and the confidence level together
2. Name the top 1-3 risks that could push toward the upper bound
3. Offer to de-risk with a timeboxed spike before committing
4. Explicitly state what is **not** included (e.g., "does not include QA, deployment, or docs")
5. Update estimates proactively when new information surfaces — don't wait until the deadline

---

## Anti-Patterns

| Anti-Pattern | Why It's Harmful | Better Approach |
|------------------------|-----------------------------------------------------|----------------------------------------------|
| Padding silently | Erodes trust when discovered; hides real uncertainty | Use explicit buffers with stated rationale |
| Sandbagging | Destroys velocity data; breeds complacency | Track accuracy ratio, aim for calibration |
| Not decomposing | Large estimates hide unknowns and compound errors | Break to < 4-hour sub-tasks, estimate bottom-up |
| Single-point estimates | Implies false certainty, no room for variance | Always give a range with confidence level |
| Estimating under pressure | Anchoring to what the stakeholder wants to hear | Ask for time to decompose; never estimate on the spot |
| Copy-paste estimates | Every task has different context and risk profile | Estimate fresh, use references as starting points only |
| Ignoring rework cycles | First pass is rarely final — reviews, feedback, QA | Factor in at least one review-and-revise loop |

---

## NEVER Do

1. **NEVER give a single-number estimate without a range** — it communicates false precision and sets you up for failure
2. **NEVER estimate a task you haven't decomposed** — large estimates are guesses wearing a suit
3. **NEVER let an old estimate stand after scope changes** — estimates are invalidated the moment requirements shift
4. **NEVER estimate in someone else's units** — your days are not their days; clarify assumptions about focus time and interrupts
5. **NEVER skip recording actuals** — estimation without feedback is astrology, not engineering
6. **NEVER commit to an estimate made under pressure** — say "let me break this down and get back to you in an hour"
7. **NEVER treat an estimate as a promise or a deadline** — estimates are probabilistic forecasts, not contracts
