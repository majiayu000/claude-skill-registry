---
name: swing-mortem
description: Prospective failure analysis using Gary Klein's pre-mortem technique. Assumes complete failure, works backward to identify risks, leading indicators, and circuit breakers. Counters optimism bias by forcing systematic exploration of failure modes before they materialize. Use for project plans, architecture decisions, technology adoption, business strategy, or feature launches. Triggers on "리스크", "위험", "실패하면", "swing-mortem", "뭐가 잘못될 수 있어", "risk", "what could go wrong", "걱정되는 점", "failure modes", "리스크 분석", "위험 분석".
argument-hint: "[plan, decision, or initiative to stress-test for future failure]"
allowed-tools: Read, Grep, Glob, Bash, Agent
---

# Pre-Mortem

Prospective failure analysis that defeats optimism bias by assuming failure first, then working backward to surface risks, early warnings, and escape hatches.

**Based on Gary Klein's pre-mortem technique:** Instead of asking "will this work?" (which triggers optimism bias), this skill forces the question: "It's 6 months from now and this has completely failed. What went wrong?"

**Key distinction from swing-review:**
- `swing-review` examines the **CURRENT** state — "what's wrong NOW?"
- `swing-mortem` examines the **FUTURE** — "what will go wrong LATER?"
- Adversarial review finds existing flaws. Pre-mortem anticipates flaws that don't exist yet.


## Rules (Absolute)

1. **Never produce generic risks.** Every failure scenario must name specific technologies, quantities, timelines, or conditions. "The database might not scale" is banned. "PostgreSQL connection pool exhaustion at >2,000 concurrent users due to long-running analytical queries holding connections for 30s+" is acceptable.
2. **Exactly 5 scenarios across 5 categories.** One Technical, one Organizational, one External, one Temporal, one Assumption. No category may be skipped, no category may have more than one scenario.
3. **Leading indicators must be observable and measurable.** "Watch out for problems" is banned. Every indicator must specify what to measure, what threshold signals danger, and where to observe it.
4. **Circuit breakers must include a specific trigger condition.** "If things go wrong" is banned. Every trigger must be a measurable condition with a concrete threshold.
5. **The swing-mortem summary is MANDATORY.** It is the BLUF of the analysis. It must appear at the end and synthesize the highest risk, its leading indicator, and its escape hatch in one paragraph.
6. **Assume complete failure.** Not partial, not "underperformance." The premise is total failure. This extreme framing is what forces creative risk identification — do not soften it.
7. **Specificity over coverage.** One deeply analyzed, plausible failure scenario per category is worth more than five shallow ones. Depth beats breadth.


## Process

Execute these 6 phases sequentially. Do NOT skip phases.

### Phase 1: Set the Failure Frame

Establish the temporal and contextual frame before any analysis.

```
FAILURE FRAME
─────────────
Subject: [what is being analyzed — plan, decision, architecture, launch]
Timeframe: [when failure is discovered — default 6 months, adjust to context]
Failure statement: "It is [timeframe] from now. [Subject] has failed completely.
Not partially underperformed — completely failed. The team is conducting a
post-mortem. What went wrong?"
```

If the subject is ambiguous or too broad, **ask one clarifying question** before proceeding. "Analyze our project" is too vague. "Analyze our migration from MongoDB to PostgreSQL for the user service" is actionable.

Before generating scenarios, gather context:
- If code/architecture exists, **read relevant files** to ground scenarios in reality
- If a project plan exists, **examine timelines and dependencies**
- If prior decisions are documented, **review the rationale and constraints**

Do not generate scenarios from imagination alone when concrete artifacts are available.

### Phase 2: Failure Scenario Generation

Generate exactly 5 failure scenarios, one per category. Each scenario must be a specific, plausible narrative — not a generic risk label.

#### Category 1: Technical
The technology didn't work as expected. Name the specific technology, the specific failure mode, and the specific conditions under which it failed.

#### Category 2: Organizational
Team, process, or communication broke down. Name the specific team dynamics, handoff points, or process gaps that caused failure.

#### Category 3: External
Market shifted, competitor moved, regulation changed, or a dependency broke. Name the specific external force and its specific impact.

#### Category 4: Temporal
Timeline was wrong. Name what took longer (or what window was missed) and by how much, with the specific cascading consequence.

#### Category 5: Assumption
A core assumption turned out to be false. Name the specific assumption, why it seemed reasonable at the time, and what reality turned out to be.

Format each scenario as:

```
SCENARIO [N]: [Category] — [Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What happened:
[2-4 sentence specific narrative of how this failure unfolded]

Why it was plausible:
[1-2 sentences on why this wasn't obvious beforehand]

Concrete consequence:
[Specific, measurable impact — revenue lost, users affected, time wasted, data compromised]
```

### Phase 3: Likelihood x Impact Matrix

Rate each scenario and determine priority:

```
RISK MATRIX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
| # | Category       | Scenario             | Likelihood | Impact       | Priority |
|---|----------------|----------------------|------------|--------------|----------|
| 1 | Technical      | [title]              | H / M / L  | Cat/Sev/Mod  | [rank]   |
| 2 | Organizational | [title]              | H / M / L  | Cat/Sev/Mod  | [rank]   |
| 3 | External       | [title]              | H / M / L  | Cat/Sev/Mod  | [rank]   |
| 4 | Temporal       | [title]              | H / M / L  | Cat/Sev/Mod  | [rank]   |
| 5 | Assumption     | [title]              | H / M / L  | Cat/Sev/Mod  | [rank]   |
```

**Likelihood:** High (>50%), Medium (15-50%), Low (<15%)
**Impact:** Catastrophic (project killed, irreversible damage), Severe (major rework, significant loss), Moderate (setback, recoverable with effort)

**Priority scoring:**
- High + Catastrophic = P1
- High + Severe OR Medium + Catastrophic = P2
- Medium + Severe OR High + Moderate = P3
- Everything else = P4

Select the **top 3 by priority** for detailed analysis in Phases 4-5. In case of tie, prefer higher Likelihood.

### Phase 4: Leading Indicators

For each of the top 3 risks, identify 2-3 early warning signals. These are observable, measurable conditions that would indicate the failure mode is beginning to materialize — before it's too late.

```
LEADING INDICATORS — Scenario [N]: [Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Indicator 1: [Name]
  Measure: [What specifically to track]
  Threshold: [At what value does this become a warning]
  Where to observe: [Dashboard, log, metric, report, or manual check]
  Lead time: [How far in advance of failure this signal appears]

Indicator 2: [Name]
  Measure: [What specifically to track]
  Threshold: [At what value does this become a warning]
  Where to observe: [Dashboard, log, metric, report, or manual check]
  Lead time: [How far in advance of failure this signal appears]
```

Every indicator must pass the **"intern test"**: could a new team member, given this description alone, determine whether the threshold has been crossed? If not, make it more specific.

### Phase 5: Circuit Breakers

For each of the top 3 risks, define the decision framework for when and how to change course.

```
CIRCUIT BREAKER — Scenario [N]: [Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Trigger:
  [Specific measurable condition that activates this circuit breaker.
   Must be a concrete threshold, not "if things go wrong."]

Fallback:
  [The alternative path. What do you switch to? Be specific about
   the replacement approach, not just "find another way."]

Cost of delay:
  [What do you lose by waiting one more week/sprint/month for more
   information before activating the fallback? Quantify if possible.]

Decision owner:
  [Who has authority to pull this trigger? Role, not name.]
```

### Phase 6: Pre-Mortem Summary (BLUF)

Synthesize the entire analysis into one paragraph. This is the most important output — the reader should be able to read ONLY this paragraph and walk away with the critical insight.

Format:

```
PRE-MORTEM SUMMARY
━━━━━━━━━━━━━━━━━━

The highest risk to [subject] is [specific scenario from top priority].
You'll know it's happening when [most actionable leading indicator with
threshold]. Your escape hatch is [primary fallback from circuit breaker].
The cost of ignoring this: [concrete consequence]. The cost of acting
too early: [trade-off of the fallback]. Monitor [specific metric] starting
[when] to stay ahead of this risk.
```


## Output Format

```markdown
## Pre-Mortem: [Subject]

### Failure Frame
> It is [timeframe] from now. [Subject] has failed completely. What went wrong?

### Failure Scenarios

#### Scenario 1: Technical — [Title]
**What happened:** [Narrative]
**Why plausible:** [Reasoning]
**Consequence:** [Specific impact]

#### Scenario 2: Organizational — [Title]
**What happened:** [Narrative]
**Why plausible:** [Reasoning]
**Consequence:** [Specific impact]

#### Scenario 3: External — [Title]
**What happened:** [Narrative]
**Why plausible:** [Reasoning]
**Consequence:** [Specific impact]

#### Scenario 4: Temporal — [Title]
**What happened:** [Narrative]
**Why plausible:** [Reasoning]
**Consequence:** [Specific impact]

#### Scenario 5: Assumption — [Title]
**What happened:** [Narrative]
**Why plausible:** [Reasoning]
**Consequence:** [Specific impact]

### Risk Matrix
| # | Category | Scenario | Likelihood | Impact | Priority |
|---|----------|----------|------------|--------|----------|
| 1 | Technical | ... | ... | ... | ... |
| 2 | Organizational | ... | ... | ... | ... |
| 3 | External | ... | ... | ... | ... |
| 4 | Temporal | ... | ... | ... | ... |
| 5 | Assumption | ... | ... | ... | ... |

### Deep Analysis (Top 3 Risks)

#### Risk [N]: [Title]

**Leading Indicators:**
1. **[Indicator name]** — Measure: [what], Threshold: [value], Where: [location], Lead time: [duration]
2. **[Indicator name]** — Measure: [what], Threshold: [value], Where: [location], Lead time: [duration]

**Circuit Breaker:**
- **Trigger:** [specific measurable condition]
- **Fallback:** [concrete alternative]
- **Cost of delay:** [what you lose by waiting]
- **Decision owner:** [role]

[Repeat for each top risk]

### Pre-Mortem Summary
The highest risk to [subject] is [X]. You'll know it's happening when [Y]. Your escape hatch is [Z]. The cost of ignoring this: [consequence]. The cost of acting too early: [trade-off]. Monitor [metric] starting [when].
```


## Quality Calibration

### BAD Pre-Mortem (Don't Do This)

```
## Pre-Mortem: New Microservices Migration

### Failure Scenarios

#### Scenario 1: Technical — It didn't scale
**What happened:** The system couldn't handle the load.
**Why plausible:** Scaling is hard.
**Consequence:** Users were unhappy.

#### Scenario 2: Organizational — Communication issues
**What happened:** Teams didn't communicate well.
**Why plausible:** Communication is always a challenge.
**Consequence:** Things were delayed.

#### Scenario 3: External — Market changed
**What happened:** The market shifted.
**Why plausible:** Markets are unpredictable.
**Consequence:** Revenue was impacted.

### Leading Indicators
- Watch out for scaling issues
- Monitor team communication
- Keep an eye on the market

### Circuit Breakers
- If things go wrong, switch to plan B
- If communication breaks down, have more meetings
```

**Why this is bad:**
- Every scenario is generic — could apply to literally any project
- No specific technologies, numbers, or conditions named
- "It didn't scale" is not a scenario — it's a category label
- Leading indicators are unmeasurable platitudes ("watch out for", "keep an eye on")
- Circuit breakers have no trigger thresholds and no concrete fallbacks
- "Have more meetings" is not a circuit breaker — it's a coping mechanism
- No risk matrix, no priority ranking, no swing-mortem summary

### GOOD Pre-Mortem (Do This)

```
## Pre-Mortem: Migrating Order Service from Monolith to Event-Driven Microservices

### Failure Frame
> It is 6 months from now. The microservices migration has failed completely.
> The team reverted to the monolith. What went wrong?

### Failure Scenarios

#### Scenario 1: Technical — Kafka consumer lag cascades into order loss
**What happened:** Under Black Friday load (12x normal), Kafka consumer groups
for the order-processing service fell behind by 4+ hours. The dead letter queue
filled its 10GB allocation. 2,340 orders were silently dropped because the
retry policy exhausted its 3 attempts while downstream inventory service was
backpressured. No alert fired because monitoring tracked consumer group status
(STABLE) rather than consumer lag (which had no threshold configured).
**Why plausible:** Load testing only covered 3x normal traffic. The failure
mode — consumer lag + DLQ overflow + silent drop — requires all three conditions
simultaneously, which wasn't in the test matrix.
**Consequence:** $180K in lost orders, 2,340 customer support tickets, and a
forced rollback to the monolith under production load — itself causing a 45-minute
outage during the revert.

#### Scenario 2: Organizational — Domain boundary mismatch between teams
**What happened:** The "order" bounded context was split between Team Alpha
(order creation) and Team Bravo (fulfillment). Both teams independently implemented
inventory reservation — Alpha with optimistic locking, Bravo with pessimistic
locking. The conflict wasn't discovered until integration testing in week 14 of
a 16-week timeline, requiring a 6-week redesign of the inventory domain model.
**Why plausible:** Domain-Driven Design workshops defined bounded contexts on
paper, but the actual code ownership didn't align. No cross-team code review
process existed for shared domain objects.
**Consequence:** 6-week schedule slip, team morale damage from rework, and the
inventory service shipped with a compatibility shim that became permanent
technical debt.

### Risk Matrix
| # | Category | Scenario | Likelihood | Impact | Priority |
|---|----------|----------|------------|--------|----------|
| 1 | Technical | Kafka consumer lag cascade | Medium | Catastrophic | P2 |
| 2 | Organizational | Domain boundary mismatch | High | Severe | P2 |

### Deep Analysis — Risk 1: Kafka Consumer Lag Cascade

**Leading Indicators:**
1. **Consumer lag growth rate** — Measure: max consumer lag across all
   partitions for order-processing group. Threshold: >10,000 messages or
   lag growing >500 msg/sec for 5 consecutive minutes. Where: Kafka
   monitoring dashboard (Burrow or equivalent). Lead time: 2-4 hours
   before DLQ overflow at projected rates.
2. **DLQ fill rate** — Measure: dead letter queue size as percentage of
   allocated storage. Threshold: >30% capacity outside of known incident
   windows. Where: Kafka topic metrics + PagerDuty alert. Lead time:
   1-2 hours before overflow.

**Circuit Breaker:**
- **Trigger:** Consumer lag exceeds 1 hour AND DLQ reaches 50% capacity
  during any traffic event exceeding 5x baseline.
- **Fallback:** Activate synchronous HTTP fallback path for order processing
  (already exists in monolith, needs a feature flag to route traffic).
  Accept the latency penalty (800ms vs 200ms) to guarantee zero order loss.
- **Cost of delay:** Each hour of delay at Black Friday volumes risks ~$30K
  in dropped orders. The fallback path adds 600ms latency but loses zero orders.
- **Decision owner:** On-call SRE lead with VP Engineering escalation.

### Pre-Mortem Summary
The highest risk to the order service migration is Kafka consumer lag cascading
into silent order loss under peak load. You'll know it's happening when consumer
lag exceeds 10,000 messages with a growth rate above 500 msg/sec for 5 minutes.
Your escape hatch is the synchronous HTTP fallback path behind a feature flag.
The cost of ignoring this: thousands of lost orders and a forced rollback under
production pressure. The cost of acting too early: 4x higher latency on order
processing during the traffic spike. Monitor Kafka consumer lag starting 2 weeks
before any projected traffic event exceeding 3x baseline.
```

**Why this is good:**
- Scenarios name specific technologies (Kafka, DLQ, optimistic/pessimistic locking)
- Quantities are concrete (12x load, 2,340 orders, $180K, 10GB, 45 minutes)
- Leading indicators have precise thresholds (>10,000 messages, >500 msg/sec, >30% capacity)
- Circuit breaker has a measurable trigger, a concrete fallback, and quantified trade-offs
- Pre-mortem summary is a self-contained briefing that an executive could act on
- Failure narratives are causal chains, not labels — each explains HOW the failure unfolded


## When to Use

- Before committing to a project plan or timeline
- Before making an irreversible architecture decision
- Before adopting a new technology in production
- Before a major feature launch or product pivot
- Before entering a new market or customer segment
- When the team is highly confident and nobody is raising concerns
- When stakes are high and the cost of failure exceeds the cost of analysis
- When someone says "what's the worst that could happen?"

## When NOT to Use

- For existing flaws in current code (use `swing-review` — it examines what's wrong NOW)
- For comparing technology options (use `swing-research` — it gathers facts, not failure scenarios)
- For generating creative alternatives (use `swing-options` — different cognitive mode)
- For routine code review
- When the decision is trivially reversible (low stakes don't justify the analysis)
- When the team needs encouragement, not caution (read the room)

## Integration Notes

- **With swing-clarify:** Run swing-clarify first on ambiguous requests before invoking this skill. Clarified scope produces better results.
- **With swing-review:** Complementary, not overlapping. Run `swing-mortem` first to anticipate future risks, then `swing-review` on the current implementation to find existing flaws. Together they cover temporal risk: future (swing-mortem) + present (adversarial).
- **With swing-research:** When a swing-mortem scenario depends on uncertain facts (e.g., "will Kafka handle this load?"), invoke `swing-research` to verify the factual basis before rating likelihood.
- **With swing-options:** After swing-mortem reveals high-priority risks, use `swing-options` to generate alternative approaches that avoid the top failure modes entirely.
- **With orchestrator strategy team:** Pre-mortem output feeds directly into the strategy team's Devil's Advocate agent for additional stress-testing of the risk assessment itself.
