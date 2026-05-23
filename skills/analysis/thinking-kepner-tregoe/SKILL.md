---
name: thinking-kepner-tregoe
description: Systematic rational process for complex problem analysis, decision making, and risk assessment. Use for high-stakes engineering decisions, root cause analysis beyond 5 Whys, and multi-factor evaluations requiring structured criteria.
---

# Kepner-Tregoe Rational Process

## Overview

The Kepner-Tregoe (KT) methodology, developed by Charles Kepner and Benjamin Tregoe in the 1950s, provides four integrated analytical processes for rational thinking. Unlike heuristic approaches, KT offers rigorous frameworks for separating fact from speculation and making defensible decisions.

**Core Principle:** Separate what you know from what you assume. Use structured comparison to reveal truth.

## When to Use

- Complex engineering problems with multiple potential causes
- High-stakes decisions requiring documented rationale
- Root cause analysis when 5 Whys yields ambiguous results
- Evaluating alternatives with competing criteria
- Post-implementation risk assessment
- Incident response requiring systematic triage
- Architecture decisions with long-term implications

Decision flow:

```text
Complex problem? → yes → Multiple concerns/unclear priority? → yes → Start with SA
                                                            ↘ no → Known single problem? → yes → PA
                                                                                         ↘ no → Decision needed? → yes → DA
                                                                                                                 ↘ no → Implementation risk? → yes → PPA
               ↘ no → Simpler frameworks may suffice
```

## The Four Processes

| Process | Purpose | Key Question |
|---------|---------|--------------|
| **SA** - Situation Analysis | Clarify and prioritize | "What's going on?" |
| **PA** - Problem Analysis | Find root cause | "Why did this happen?" |
| **DA** - Decision Analysis | Evaluate alternatives | "What should we do?" |
| **PPA** - Potential Problem Analysis | Anticipate risks | "What could go wrong?" |

---

## Process 1: Situation Analysis (SA)

Use when facing multiple concerns, unclear priorities, or overwhelm.

### Purpose

Break complex situations into manageable components, set priorities, and plan approach.

### Steps

#### Step 1: List All Concerns

Brainstorm everything that needs attention:

```markdown
Concerns:
- Production API latency increased 3x
- New feature deployment blocked
- Team velocity dropped 40%
- Customer complaints about checkout errors
- Database connection pool exhaustion
- Unclear requirements for Q2 roadmap
```

#### Step 2: Separate and Clarify

For each concern, ask: "Is this one issue or multiple?"

```markdown
"Production performance issues" →
  - API latency (response time)
  - Database connections (resource exhaustion)
  - Memory usage (potential leak)
```

#### Step 3: Set Priority

Use Timing, Impact, Trend (TIT):

| Concern | Timing | Impact | Trend | Priority |
|---------|--------|--------|-------|----------|
| API latency | Urgent | High | Worsening | P0 |
| DB connections | Urgent | Critical | Stable | P0 |
| Checkout errors | Soon | High | Worsening | P1 |
| Velocity drop | Soon | Medium | Stable | P2 |

**Timing:** When must action be taken?
**Impact:** What's the consequence of inaction?
**Trend:** Is it getting better, worse, or stable?

#### Step 4: Plan Approach

For each prioritized concern, determine:

- Which KT process applies (PA, DA, PPA)?
- Who should be involved?
- What information is needed?

### SA Template

```markdown
# Situation Analysis: [Context]
Date: [Date]

## Concerns Inventory
| # | Concern | Clarification Needed? |
|---|---------|----------------------|
| 1 | [Concern] | [Yes/No - details] |

## Priority Matrix
| Concern | Timing | Impact | Trend | Priority | Next Process |
|---------|--------|--------|-------|----------|--------------|
| | | | | | SA/PA/DA/PPA |

## Action Plan
| Priority | Concern | Process | Owner | Deadline |
|----------|---------|---------|-------|----------|
| P0 | | | | |
```

---

## Process 2: Problem Analysis (PA)

Use when you need to find root cause of a deviation from expected performance.

### Purpose

Systematically identify the true cause by comparing what IS happening vs. what IS NOT.

### Key Concept: The IS/IS-NOT Matrix

The power of PA lies in specification through contrast. A problem exists in a specific context—understanding boundaries reveals cause.

### Steps

#### Step 1: State the Problem

Be precise about the deviation:

```text
BAD: "The system is slow"
GOOD: "API response time increased from 200ms to 800ms for /checkout endpoint starting Monday 9 AM"
```

#### Step 2: Specify the Problem (IS/IS-NOT)

| Dimension | IS | IS NOT | Distinction |
|-----------|-----|---------|-------------|
| **WHAT** | | | |
| What object has the problem? | /checkout endpoint | /cart, /product, /user endpoints | Only payment-related |
| What is the defect? | 4x latency increase | Errors, timeouts, data corruption | Performance only |
| **WHERE** | | | |
| Where is the object when observed? | Production US-East | Production EU, US-West, staging | Single region |
| Where on the object? | Database query phase | Auth, validation, response serialization | DB layer |
| **WHEN** | | | |
| When was it first observed? | Monday 9:00 AM | Before Monday, after 6 PM | Business hours |
| When in lifecycle/pattern? | During checkout submit | During browsing, cart add | Write operations |
| **EXTENT** | | | |
| How many objects affected? | ~30% of checkout requests | 100% of requests | Intermittent |
| How much of object affected? | 600ms additional latency | Complete failure | Degradation |
| Is it growing/spreading? | Stable since Tuesday | Getting worse | Plateaued |

#### Step 3: Identify Distinctions

For each IS/IS-NOT pair, ask: "What's unique or distinctive about the IS side?"

```markdown
Distinctions identified:
- Only /checkout endpoint (payment processing)
- Only US-East region (specific DB replica)
- Only during business hours (load-related?)
- Only ~30% of requests (specific query pattern?)
- Started Monday 9 AM (deployment? config change?)
```

#### Step 4: Identify Changes

What changed in, on, around, or about the distinctions?

```markdown
Changes near Monday 9 AM:
- Payment provider SDK updated (Sunday night deploy)
- Database index rebuild scheduled (Sunday maintenance)
- New fraud detection rules enabled (Monday 8:45 AM)
```

#### Step 5: Generate Possible Causes

Combine distinctions and changes:

```markdown
Possible causes:
1. Fraud detection rules causing additional DB queries
2. Payment SDK making synchronous external calls
3. Index rebuild affected checkout-related queries
```

#### Step 6: Test Against Specification

For each possible cause, verify it explains ALL IS and IS-NOT:

| Possible Cause | Explains IS? | Explains IS-NOT? | Verdict |
|----------------|--------------|------------------|---------|
| Fraud rules | ✓ Only checkout | ✓ Only write ops | ✓ Possible |
| Payment SDK | ✓ Only checkout | ✗ Would affect all regions | ✗ Ruled out |
| Index rebuild | ✓ DB layer | ✗ Would affect all queries | ✗ Ruled out |

#### Step 7: Verify True Cause

Design verification to confirm or rule out:

```markdown
Verification plan for "Fraud detection rules":
1. Check timing: Rules enabled 8:45 AM (matches)
2. Check scope: Rules only on checkout (matches)
3. Test: Disable rules in canary, measure latency
4. Examine: Query logs for fraud check queries
```

### IS/IS-NOT Template

```markdown
# Problem Analysis: [Problem Statement]
Date: [Date]

## Problem Specification

### What
| Question | IS | IS NOT | Distinction |
|----------|-----|---------|-------------|
| What object has the problem? | | | |
| What specifically is wrong? | | | |

### Where
| Question | IS | IS NOT | Distinction |
|----------|-----|---------|-------------|
| Where is the problem observed? | | | |
| Where on the object is it? | | | |

### When
| Question | IS | IS NOT | Distinction |
|----------|-----|---------|-------------|
| When first observed? | | | |
| Any pattern to occurrence? | | | |

### Extent
| Question | IS | IS NOT | Distinction |
|----------|-----|---------|-------------|
| How many/much affected? | | | |
| Is it changing? | | | |

## Distinctions Summary
1. [Unique characteristic]
2. [Unique characteristic]

## Changes Near Distinctions
| Change | When | What Changed |
|--------|------|--------------|
| | | |

## Possible Causes
| # | Cause | Based on |
|---|-------|----------|
| 1 | | Distinction + Change |

## Cause Testing
| Cause | Explains IS | Explains IS-NOT | Verdict |
|-------|-------------|-----------------|---------|
| | | | |

## Verification Plan
- [ ] [Test to confirm/rule out most likely cause]

## Confirmed Root Cause
[Cause with evidence]
```

---

## Process 3: Decision Analysis (DA)

Use when choosing among alternatives with multiple criteria.

### Purpose

Make systematic, defensible decisions by separating MUSTS from WANTS and scoring alternatives objectively.

### Steps

#### Step 1: Clarify the Decision

State the decision clearly:

```text
"Select a message queue system for order processing"
"Choose deployment strategy for the new auth service"
```

#### Step 2: Develop Objectives

List what the decision must accomplish:

```markdown
Objectives:
- Handle 10K messages/second throughput
- Provide at-least-once delivery guarantees
- Support multiple consumer groups
- Minimize operational overhead
- Stay within $5K/month budget
- Integrate with existing monitoring
```

#### Step 3: Classify as MUST vs WANT

**MUST:** Non-negotiable requirements (pass/fail)
**WANT:** Desirable attributes (weighted scoring)

| Objective | MUST/WANT | Weight (1-10) |
|-----------|-----------|---------------|
| 10K msg/sec throughput | MUST | - |
| At-least-once delivery | MUST | - |
| Under $5K/month | MUST | - |
| Multiple consumer groups | WANT | 9 |
| Low operational overhead | WANT | 8 |
| Existing monitoring integration | WANT | 6 |
| Strong community/docs | WANT | 5 |
| Team familiarity | WANT | 4 |

#### Step 4: Generate Alternatives

List viable options:

```markdown
Alternatives:
A. Apache Kafka (self-managed)
B. AWS SQS + SNS
C. RabbitMQ (self-managed)
D. Amazon MSK (managed Kafka)
```

#### Step 5: Screen Against MUSTs

| Alternative | 10K msg/sec | At-least-once | Under $5K | MUST Score |
|-------------|-------------|---------------|-----------|------------|
| Kafka | ✓ Yes | ✓ Yes | ✓ Yes | PASS |
| SQS+SNS | ✓ Yes | ✓ Yes | ✓ Yes | PASS |
| RabbitMQ | ✗ ~5K limit | ✓ Yes | ✓ Yes | FAIL |
| MSK | ✓ Yes | ✓ Yes | ✗ ~$8K | FAIL |

RabbitMQ and MSK eliminated—don't meet MUSTs.

#### Step 6: Score Against WANTs

Rate each alternative 1-10 on each WANT:

| WANT (Weight) | Kafka | SQS+SNS |
|---------------|-------|---------|
| Consumer groups (9) | 10 | 7 |
| Low ops overhead (8) | 4 | 9 |
| Monitoring integration (6) | 7 | 10 |
| Community/docs (5) | 10 | 8 |
| Team familiarity (4) | 3 | 8 |

#### Step 7: Calculate Weighted Scores

| WANT | Weight | Kafka Score | Kafka Weighted | SQS Score | SQS Weighted |
|------|--------|-------------|----------------|-----------|--------------|
| Consumer groups | 9 | 10 | 90 | 7 | 63 |
| Low ops overhead | 8 | 4 | 32 | 9 | 72 |
| Monitoring | 6 | 7 | 42 | 10 | 60 |
| Community | 5 | 10 | 50 | 8 | 40 |
| Team familiarity | 4 | 3 | 12 | 8 | 32 |
| **TOTAL** | | | **226** | | **267** |

SQS+SNS scores higher on weighted WANTs.

#### Step 8: Assess Risks (→ feeds into PPA)

Before final decision, consider adverse consequences:

| Alternative | Risk | Likelihood | Severity |
|-------------|------|------------|----------|
| SQS+SNS | Message ordering challenges | Medium | High |
| SQS+SNS | Vendor lock-in | High | Medium |
| Kafka | Operational complexity | High | High |

#### Step 9: Make Decision

Consider scores AND risks to make final choice. Document rationale.

### DA Template

```markdown
# Decision Analysis: [Decision Statement]
Date: [Date]
Decision Maker: [Name]

## Objectives
| Objective | MUST/WANT | Weight |
|-----------|-----------|--------|
| | | |

## Alternatives
1. [Option A]
2. [Option B]
3. [Option C]

## MUST Screening
| Alternative | MUST 1 | MUST 2 | MUST 3 | Pass/Fail |
|-------------|--------|--------|--------|-----------|
| | | | | |

## WANT Scoring
| WANT (Weight) | Alt A | Alt B | Alt C |
|---------------|-------|-------|-------|
| (w) | score | score | score |
| **Weighted Total** | | | |

## Risk Assessment
| Alternative | Risk | L | S | Mitigation |
|-------------|------|---|---|------------|
| | | | | |

## Decision
**Selected:** [Alternative]
**Rationale:** [Why this choice given scores and risks]
```

---

## Process 4: Potential Problem Analysis (PPA)

Use after making a decision or before implementation to anticipate and prevent problems.

### Purpose

Identify what could go wrong with a planned action and develop preventive/contingent actions.

### Steps

#### Step 1: State the Plan

Describe what will be implemented:

```markdown
Plan: Migrate order service from monolith to microservice
Timeline: 4 weeks
Key changes: New service, message queue, database split
```

#### Step 2: Identify Potential Problems

Walk through the plan and ask "What could go wrong?":

```markdown
Potential problems:
1. Message queue loses orders during migration
2. New service has undiscovered bugs in production
3. Database sync fails, causing data inconsistency
4. Rollback needed but unclear how to reverse
5. Performance degradation under load
6. Team lacks Kafka operational knowledge
```

#### Step 3: Assess Each Potential Problem

Rate probability (P) and seriousness (S):

| Potential Problem | Probability | Seriousness | P×S |
|-------------------|-------------|-------------|-----|
| Lost orders | Medium | Critical | HIGH |
| Undiscovered bugs | High | High | HIGH |
| Data sync failure | Medium | Critical | HIGH |
| Rollback unclear | Medium | High | MEDIUM |
| Performance issues | Medium | Medium | MEDIUM |
| Kafka knowledge gap | High | Medium | MEDIUM |

#### Step 4: Identify Likely Causes

For high P×S problems, determine probable causes:

```markdown
Problem: Message queue loses orders
Likely causes:
- Consumer crashes before acknowledgment
- Queue overflow during peak
- Network partition between services
- Misconfigured dead letter queue
```

#### Step 5: Develop Preventive Actions

Actions to reduce probability of cause occurring:

| Cause | Preventive Action | Owner |
|-------|-------------------|-------|
| Consumer crash | Implement idempotent processing with transactional outbox | Dev team |
| Queue overflow | Configure auto-scaling, set appropriate limits | Platform |
| Network partition | Deploy in same availability zone initially | Infra |
| DLQ misconfigured | Pre-production DLQ testing with failure injection | QA |

#### Step 6: Develop Contingent Actions

Actions to reduce impact IF problem occurs:

| Problem | Contingent Action | Trigger |
|---------|-------------------|---------|
| Lost orders | Replay from audit log, manual reconciliation | Order count mismatch > 0.1% |
| Data sync failure | Activate sync monitor, pause writes, manual fix | Sync lag > 5 minutes |
| Performance issues | Activate circuit breaker, failover to monolith | p99 > 2s for 5 min |

#### Step 7: Build Monitoring/Triggers

Define how you'll detect problems and when to activate contingent actions.

### PPA Template

```markdown
# Potential Problem Analysis: [Plan Name]
Date: [Date]

## Plan Summary
[Brief description of what will be implemented]

## Potential Problems
| # | Problem | P (H/M/L) | S (H/M/L) | Priority |
|---|---------|-----------|-----------|----------|
| 1 | | | | |

## High-Priority Problem Analysis

### Problem: [Name]
**Likely Causes:**
1. [Cause]

**Preventive Actions:**
| Cause | Action | Owner | Due |
|-------|--------|-------|-----|
| | | | |

**Contingent Actions:**
| Trigger | Action | Owner |
|---------|--------|-------|
| | | |

## Monitoring Plan
| What to Monitor | Threshold | Alert | Response |
|-----------------|-----------|-------|----------|
| | | | |

## Review Schedule
- Pre-implementation review: [Date]
- Post-implementation check: [Date]
```

---

## Integrating the Four Processes

Typical flow for complex situations:

```text
1. SA: "We have multiple issues after the release"
   → Separate concerns, prioritize
   → P0: Production errors (needs PA)
   → P1: Architecture decision (needs DA)
   → P2: Future release risks (needs PPA)

2. PA: Investigate production errors
   → IS/IS-NOT analysis
   → Identify root cause
   → Feeds solution options into DA

3. DA: Choose solution approach
   → Define objectives
   → Score alternatives
   → Select best option
   → Risk assessment feeds PPA

4. PPA: Plan implementation
   → Identify what could go wrong
   → Preventive and contingent actions
   → Monitoring plan
```

## Integration with Other Thinking Skills

| Skill | Integration Point |
|-------|-------------------|
| **thinking-pre-mortem** | Use as input to PPA—pre-mortem identifies problems, PPA develops mitigations |
| **thinking-inversion** | Use in PA—invert "what would cause this?" to identify possible causes |
| **thinking-first-principles** | Use in DA—challenge MUST criteria, are they truly fundamental? |
| **thinking-debiasing** | Apply checklist when scoring DA alternatives, evaluating PA causes |
| **thinking-systems** | Use in SA—understand how concerns interconnect, avoid siloed analysis |
| **tools-debugging-root-cause** | PA complements debugging—PA for systematic cause identification, debugging for code-level investigation |

## Verification Checklist

- [ ] Used appropriate KT process for the situation type
- [ ] SA: All concerns listed, separated, and prioritized with TIT criteria
- [ ] PA: IS/IS-NOT fully specified across all four dimensions
- [ ] PA: Each possible cause tested against specification
- [ ] DA: MUST/WANT clearly separated, MUSTs are truly non-negotiable
- [ ] DA: Weighted scores calculated, not just intuition
- [ ] PPA: High P×S problems have both preventive and contingent actions
- [ ] PPA: Triggers defined for contingent action activation
- [ ] Analysis documented for future reference and team alignment

## Key Questions by Process

### Situation Analysis

- "What are ALL the concerns we're facing?"
- "Is this one problem or several?"
- "What's the timing, impact, and trend?"
- "Which process should we use for each concern?"

### Problem Analysis

- "What specifically IS happening vs IS NOT?"
- "What's unique about where/when this occurs?"
- "What changed in, on, or around the distinctions?"
- "Does this cause explain BOTH the IS and IS-NOT?"

### Decision Analysis

- "What are the MUST-have requirements?"
- "How important is each WANT relative to others?"
- "How well does each alternative satisfy each objective?"
- "What risks come with each alternative?"

### Potential Problem Analysis

- "What could go wrong with this plan?"
- "What would cause each problem?"
- "How can we prevent the cause?"
- "If it happens anyway, how do we minimize damage?"
