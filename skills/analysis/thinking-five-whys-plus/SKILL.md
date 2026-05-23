---
name: thinking-five-whys-plus
description: Enhanced root cause analysis with explicit bias guards and stopping criteria. Use for incident post-mortems, bug investigations, and process failures where standard 5 Whys might mislead.
---

# Five Whys Plus

## Overview

The Five Whys technique from Toyota Production System is powerful but often misapplied. This enhanced version adds explicit guards against common failures: premature stopping, single-cause bias, blame-oriented thinking, and confirmation bias. It transforms a simple technique into a rigorous root cause methodology.

**Core Principle:** Keep asking "why" until you reach actionable root causes, but guard against the technique's known failure modes.

## When to Use

- Incident post-mortems
- Bug investigations
- Process failures
- Customer complaints
- Recurring problems
- Any situation where you need root cause, not just proximate cause

Decision flow:

```
Problem occurred?
  → Is the cause obvious and verified? → yes → Fix directly
  → Need to find root cause? → yes → APPLY FIVE WHYS PLUS
  → Is this a complex multi-factor problem? → yes → Consider Kepner-Tregoe PA
```

## Standard Five Whys Failure Modes

| Failure Mode | Description | Guard |
|--------------|-------------|-------|
| Premature stopping | Accepting first plausible cause | Minimum depth + actionability test |
| Single-cause bias | Assuming one root cause | Branch on "what else?" |
| Blame orientation | Stopping at human error | "Why was error possible?" |
| Confirmation bias | Finding expected cause | Devil's advocate review |
| Circular reasoning | Why loops back on itself | Detect and break cycles |
| Speculation depth | Going beyond evidence | Evidence requirement |

## The Five Whys Plus Process

### Step 1: State the Problem Precisely

Bad: "The system was slow"
Good: "API response times exceeded 2 seconds for 30% of requests between 14:00-14:45 UTC on January 15"

```markdown
Problem Statement:
- What happened: [Specific observable symptom]
- When: [Time range]
- Where: [Affected systems/users]
- Extent: [Scope and severity]
- Impact: [Business/user impact]
```

### Step 2: Apply "Why" with Evidence Requirement

For each "why," require evidence:

```markdown
Why #1: Why did [problem] occur?
Answer: [Hypothesis]
Evidence: [Data, logs, metrics that support this]
Confidence: [High/Medium/Low]
```

**Evidence types:**
- Logs showing the event
- Metrics correlating with timeline
- Code showing the behavior
- Configuration proving the state
- Testimony from multiple sources

### Step 3: Branch on "What Else?"

After each "why," explicitly ask "what else could cause this?"

```markdown
Why #1: Why did API response times spike?
Primary answer: Database queries were slow
Evidence: DB query times increased from 50ms to 1.5s

What else could cause this?
- [ ] Network latency (checked: normal)
- [ ] Application code changes (checked: none deployed)
- [ ] Memory pressure (checked: normal)
- [ ] External API dependencies (checked: normal)

→ Proceeding with database queries as verified cause
```

### Step 4: Apply "Why Was This Possible?" for Human Error

Never stop at "human error" or "someone made a mistake."

```
BAD chain:
Why did the outage occur? → Config was wrong
Why was config wrong? → Engineer made a typo
→ STOP (blames human)

GOOD chain:
Why did the outage occur? → Config was wrong
Why was config wrong? → Engineer made a typo
Why was a typo possible? → No validation on config changes
Why was there no validation? → Config system doesn't support schemas
Why doesn't it support schemas? → Tech debt, never prioritized
→ ROOT CAUSE: Config validation infrastructure gap
```

### Step 5: Check Stopping Criteria

Only stop when ALL are true:

| Criterion | Question | ✓ |
|-----------|----------|---|
| Actionable | Can we take concrete action on this cause? | |
| Controllable | Is this within our control to fix? | |
| Fundamental | Would fixing this prevent recurrence? | |
| Evidenced | Do we have evidence, not just speculation? | |
| Not-blame | Is this a system issue, not just "someone messed up"? | |

### Step 6: Verify with Counter-Analysis

Before finalizing, apply devil's advocate:

```markdown
Proposed root cause: [X]

Counter-analysis:
1. What evidence contradicts this conclusion?
2. What other explanation fits the evidence?
3. Would someone with a different perspective agree?
4. If we fix X, are we confident the problem won't recur?
5. Are we finding what we expected to find? (confirmation bias check)
```

## Enhanced Template

```markdown
# Five Whys Plus Analysis

## Problem Statement
- **What:** [Specific symptom]
- **When:** [Time range]
- **Where:** [Affected scope]
- **Impact:** [Severity and consequences]

## Why Chain

### Why #1: Why did [problem] occur?
**Answer:**
**Evidence:**
**Confidence:** High / Medium / Low
**What else considered:**
**Ruled out because:**

### Why #2: Why did [answer #1] occur?
**Answer:**
**Evidence:**
**Confidence:**
**What else considered:**
**Ruled out because:**

### Why #3: Why did [answer #2] occur?
**Answer:**
**Evidence:**
**Confidence:**
**What else considered:**
**Ruled out because:**

[Continue as needed...]

## Stopping Criteria Check
- [ ] Actionable: We can take concrete action
- [ ] Controllable: Within our control
- [ ] Fundamental: Prevents recurrence
- [ ] Evidenced: Supported by data
- [ ] System-focused: Not blaming individuals

## Counter-Analysis
**Contradicting evidence:**
**Alternative explanations:**
**Confirmation bias check:**
**Confidence in conclusion:**

## Root Causes Identified
1. [Primary root cause]
2. [Contributing factor if applicable]

## Recommended Actions
| Action | Addresses | Owner | Timeline |
|--------|-----------|-------|----------|
| | | | |

## Verification Plan
How will we know the fix worked?
```

## Example: Production Outage

```markdown
# Five Whys Plus: Payment Service Outage

## Problem Statement
- What: Payment service returned 500 errors
- When: 2024-01-15 14:00-14:45 UTC
- Where: Production, US-East region
- Impact: 2,400 failed transactions, ~$180K revenue impact

## Why Chain

### Why #1: Why did payment service return 500 errors?
**Answer:** Database connection pool exhausted
**Evidence:** Connection pool metrics showed 100/100 in use, logs show "connection wait timeout"
**Confidence:** High
**What else considered:**
- Application bugs (no recent deploys)
- Memory issues (heap normal)
- Network problems (latency normal)

### Why #2: Why was connection pool exhausted?
**Answer:** Queries taking 10x longer than normal
**Evidence:** P99 query time went from 50ms to 500ms at 14:00
**Confidence:** High
**What else considered:**
- Connection leak (connection count stable before incident)
- Sudden traffic spike (traffic was normal)

### Why #3: Why were queries taking 10x longer?
**Answer:** Missing index on payment_status table
**Evidence:** EXPLAIN shows sequential scan on 10M row table
**Confidence:** High
**What else considered:**
- Lock contention (no blocking locks)
- DB resource exhaustion (CPU/memory normal)

### Why #4: Why was the index missing?
**Answer:** Migration to add index was rolled back 2 weeks ago
**Evidence:** Deployment logs show rollback on 2024-01-01
**Confidence:** High

### Why #5: Why was the migration rolled back?
**Answer:** Migration timed out during deploy window
**Evidence:** Deploy log shows "migration timeout after 30 minutes"

### Why #6: Why did migration timeout?
**Answer:** Table too large for online migration in current window
**Evidence:** Table has 10M rows, online migration takes ~2 hours
**Confidence:** High

### Why #7 (System-level): Why wasn't this caught before impact?
**Answer:** No alerting on query performance degradation
**Evidence:** No alerts fired until connection pool exhausted

## Stopping Criteria Check
- [x] Actionable: Can add index, fix alerting
- [x] Controllable: Within our control
- [x] Fundamental: Index prevents query issue, alerting prevents impact
- [x] Evidenced: All steps have supporting data
- [x] System-focused: Process and tooling issues, not blame

## Root Causes Identified
1. **Primary:** Index migration process doesn't handle large tables
2. **Contributing:** No alerting on query latency before connection exhaustion

## Recommended Actions
| Action | Addresses | Owner | Timeline |
|--------|-----------|-------|----------|
| Implement online index creation tool | Root cause 1 | Platform | 2 weeks |
| Add query latency alerting | Root cause 2 | SRE | 1 week |
| Create index during maintenance window | Immediate fix | DBA | Tonight |
```

## Common Patterns to Catch

### The Blame Stop

```
BAD: "Why did it fail?" → "Engineer didn't test properly" → STOP

BETTER: → "Why was it possible to deploy without proper testing?"
        → "Why doesn't the pipeline enforce testing?"
        → System/process root cause
```

### The Premature Technical Stop

```
BAD: "Why was it slow?" → "Query was inefficient" → STOP

BETTER: → "Why was an inefficient query in production?"
        → "Why didn't code review catch it?"
        → "Why don't we have query performance testing?"
```

### The Circular Why

```
DETECT: "Why A?" → "Because B" → "Why B?" → "Because A"

BREAK: Introduce external evidence or third factor
```

### The Speculation Dive

```
DETECT: Answers become increasingly speculative without evidence

BREAK: "What evidence do we have for this?"
       If none, mark as hypothesis and seek evidence
```

## Verification Checklist

- [ ] Problem stated with specific details (what, when, where, extent)
- [ ] Each "why" has supporting evidence
- [ ] "What else?" asked at each branch point
- [ ] Didn't stop at human error—asked "why was error possible?"
- [ ] Stopping criteria all satisfied
- [ ] Counter-analysis performed
- [ ] Root cause is actionable and controllable
- [ ] Actions address root cause, not just symptoms

## Key Questions

- "What evidence supports this answer?"
- "What else could explain this?"
- "Why was this mistake/error/failure possible?"
- "If we stop here, will the problem actually be prevented?"
- "Are we finding what we expected, or what the evidence shows?"
- "Would someone outside our team reach the same conclusion?"

## Ohno's Wisdom (Extended)

Taiichi Ohno said: "By asking 'why' five times and answering each time, we can get to the real cause of the problem."

The extension: Five is not magic. The real guidance is:
1. Keep asking until you reach something actionable
2. But don't speculate past your evidence
3. And never stop at human blame

The technique is simple. Applying it well requires discipline.
