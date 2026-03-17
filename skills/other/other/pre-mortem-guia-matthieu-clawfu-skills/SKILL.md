---
name: pre-mortem
description: "Imagine your project has failed spectacularly—then work backward to identify why. Apply Gary Klein's \"prospective hindsight\" technique to catch failures before they happen. Use when: **Before launching** a product, campaign, or major initiative; **Before making** an important decision (hiring, investment, partnership); **Starting a project** to identify risks the team hasn't considered; **When overconfident** and everyone agrees the plan is great; **Before committing resources** to a signific..."
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Pre-Mortem

> Imagine your project has failed spectacularly—then work backward to identify why. Apply Gary Klein's "prospective hindsight" technique to catch failures before they happen.

## When to Use This Skill

- **Before launching** a product, campaign, or major initiative
- **Before making** an important decision (hiring, investment, partnership)
- **Starting a project** to identify risks the team hasn't considered
- **When overconfident** and everyone agrees the plan is great
- **Before committing resources** to a significant undertaking
- **In team planning** to surface concerns people might hesitate to share

## Methodology Foundation

| Aspect | Details |
|--------|---------|
| **Source** | Gary Klein (1989), cognitive psychologist, naturalistic decision making pioneer |
| **Expert** | Klein's research shows pre-mortems increase accuracy of identifying reasons for outcomes by 30% |
| **Core Principle** | "Prospective hindsight" - imagining an event has already occurred dramatically improves our ability to explain it. The future feels distant; the past feels real. |


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Surfaces hidden risks** - Finds dangers invisible to forward-looking planning
2. **Gives permission to criticize** - Team members can voice concerns safely
3. **Reduces overconfidence** - Counters planning fallacy and optimism bias
4. **Improves plans before execution** - Fix problems when they're cheap to fix
5. **Creates psychological safety** - "We're imagining failure" feels safer than "I think this will fail"

## How to Use

### Run a Pre-Mortem
```
Run a Pre-Mortem on this project:
[describe the project, product, or decision]

It's one year from now and this has failed completely. What happened?
```

### Stress-Test a Decision
```
Pre-Mortem this decision:
[describe the decision you're considering]

Assume we made this choice and it went badly. What went wrong?
```

### Team Pre-Mortem Facilitation
```
Help me facilitate a Pre-Mortem session for my team.
Project: [description]
Team size: [number]
Time available: [duration]

Provide the agenda, questions to ask, and how to synthesize findings.
```

## Instructions

When facilitating a Pre-Mortem, follow this systematic process:

### Step 1: Set the Stage

```
## Pre-Mortem Setup

**Project/Decision:** ________________________________

**Timeline:** [Imagine we're looking back from X months/years]

**The Scenario:**
"It is [future date]. This project has failed—not just underperformed,
but failed spectacularly. The results are in and they're bad.

We're now conducting a post-mortem to understand what went wrong.
Looking back, it's obvious why this failed..."

**Rules:**
1. Failure has ALREADY happened (this is a fact in this exercise)
2. Everyone must contribute at least one reason
3. No defending the plan (we're explaining failure, not preventing it)
4. Be specific, not vague
5. "I had a bad feeling" is valid (hindsight makes it concrete)
```

---

### Step 2: Individual Failure Generation (Silent)

```
## Individual Brainstorm (5-10 minutes)

Each person silently writes answers to:

"Looking back, this project failed because..."

1. ________________________________________________
2. ________________________________________________
3. ________________________________________________
4. ________________________________________________
5. ________________________________________________

**Prompt Questions:**
- What did we overlook?
- What assumption proved wrong?
- What external event derailed us?
- Who let us down (vendor, team member, partner)?
- What resource ran out?
- What competitor move hurt us?
- What customer behavior surprised us?
- What technical problem emerged?
- What communication failure occurred?
- What timeline assumption was wrong?
```

**Why Silent First:**
- Prevents groupthink
- Allows introverts equal voice
- Captures diverse concerns before discussion narrows focus

---

### Step 3: Share and Cluster

```
## Round Robin Sharing

**Process:**
1. Each person shares ONE reason (no discussion yet)
2. Continue rounds until all reasons shared
3. Capture on whiteboard/doc as shared

**Clustering:**
Group similar failure reasons into categories:

### EXECUTION FAILURES
- ________________________________
- ________________________________

### EXTERNAL FACTORS
- ________________________________
- ________________________________

### RESOURCE CONSTRAINTS
- ________________________________
- ________________________________

### ASSUMPTION FAILURES
- ________________________________
- ________________________________

### PEOPLE/TEAM ISSUES
- ________________________________
- ________________________________

### TIMING/MARKET
- ________________________________
- ________________________________
```

---

### Step 4: Analyze and Prioritize

```
## Risk Assessment Matrix

For each failure reason, assess:

| Failure Reason | Likelihood | Impact | Detectability | Risk Score |
|----------------|------------|--------|---------------|------------|
| [Reason 1] | H/M/L | H/M/L | Early/Late/Never | ___ |
| [Reason 2] | H/M/L | H/M/L | Early/Late/Never | ___ |
| [Reason 3] | H/M/L | H/M/L | Early/Late/Never | ___ |

**Scoring:**
- High Likelihood + High Impact + Late/Never Detection = CRITICAL
- Medium/Medium/Early = MANAGEABLE
- Low/Any/Early = MONITOR

## Priority Failures

**CRITICAL (Must Address):**
1. ________________________________
2. ________________________________
3. ________________________________

**MONITOR (Watch Closely):**
1. ________________________________
2. ________________________________
```

---

### Step 5: Create Prevention/Mitigation Plans

```
## Prevention Strategies

For each critical risk:

### Risk: [Failure Reason 1]

**Early Warning Signs:**
- ________________________________
- ________________________________

**Prevention Actions:**
- ________________________________
- ________________________________

**If It Happens Anyway (Mitigation):**
- ________________________________
- ________________________________

**Owner:** ____________
**Review Date:** ____________

---

### Risk: [Failure Reason 2]

[Repeat structure]

---

## Tripwires (Automatic Triggers)

"If we see [sign], we immediately [action]"

1. If ______________, then ______________
2. If ______________, then ______________
3. If ______________, then ______________
```

---

### Step 6: Integrate into Plan

```
## Updated Project Plan

### Original Assumptions (Now Questioned)
| Assumption | Pre-Mortem Concern | Validation Plan |
|------------|-------------------|-----------------|
| [Assumption] | [Risk raised] | [How to test] |
| [Assumption] | [Risk raised] | [How to test] |

### New Safeguards Added
- [ ] ________________________________
- [ ] ________________________________
- [ ] ________________________________

### Monitoring Dashboard
Track these metrics as early warning system:
1. ________________________________
2. ________________________________
3. ________________________________

### Scheduled Check-ins
- Week 2: Review assumption #1
- Week 4: Check metric #2
- Month 2: Full pre-mortem review
```

---

## Examples

### Example 1: Product Launch Pre-Mortem

**Context:** SaaS company launching new enterprise product in 3 months.

**Input:**
> "We're launching our enterprise product in Q2. Everyone's excited. Run a Pre-Mortem—what killed us?"

**Output:**

**The Scenario:**
"It's September. Our Q2 enterprise launch failed. We've burned through our runway, the product hasn't gained traction, and we're considering a pivot. What went wrong?"

**Failure Reasons Generated:**

**EXECUTION FAILURES:**
1. We underestimated enterprise sales cycle (6-12 months, not 2)
2. Security review requirements we didn't anticipate (SOC2, etc.)
3. The product wasn't actually enterprise-ready (missing audit logs, SSO)
4. Support couldn't handle enterprise customer expectations

**MARKET/TIMING:**
5. Enterprise budgets were frozen due to economic conditions
6. Two competitors launched similar products in Q1
7. Target companies in "wait and see" mode

**INTERNAL/TEAM:**
8. Sales team had no enterprise experience
9. Engineering bandwidth split between launch and bug fixes
10. Marketing message didn't resonate with enterprise buyers

**RESOURCE:**
11. Ran out of runway before enough deals closed
12. Couldn't hire enterprise sales rep fast enough

**Risk Assessment:**

| Failure Reason | Likelihood | Impact | Priority |
|----------------|------------|--------|----------|
| Enterprise sales cycle underestimated | HIGH | HIGH | CRITICAL |
| Product not enterprise-ready | HIGH | HIGH | CRITICAL |
| Budget freeze | MEDIUM | HIGH | WATCH |
| Competitive launch | MEDIUM | MEDIUM | MONITOR |
| Sales team inexperience | HIGH | HIGH | CRITICAL |

**Prevention Plan:**

**Risk 1: Sales Cycle Underestimated**
- Prevention: Start enterprise conversations NOW (3 months early)
- Validation: Have 5 LOIs before launch, not 5 "interested" calls
- Tripwire: If no LOIs by Week 4, pause launch

**Risk 2: Product Not Enterprise-Ready**
- Prevention: Hire enterprise advisor to audit requirements
- Action: Prioritize SSO, audit logs, SLA before launch
- Tripwire: If security questionnaire failure, delay launch

**Risk 3: Sales Team Inexperience**
- Prevention: Hire one senior enterprise rep or consultant
- Alternative: Partner with enterprise-focused reseller
- Validation: Close one pilot before full launch

**Updated Plan:**
- Push launch to Q3 (realistic timeline)
- Add SOC2 certification to roadmap
- Hire enterprise sales lead in Q1
- Secure 3 design partners before public launch

---

### Example 2: Hiring Decision Pre-Mortem

**Context:** Startup about to make critical senior hire.

**Input:**
> "We're about to hire a VP of Engineering. $300K salary, equity, big commitment. Pre-Mortem this decision—how did this hire fail?"

**Output:**

**The Scenario:**
"It's 12 months later. The VP of Engineering hire was a disaster. We've parted ways (expensively), the team is demoralized, and we've lost 6 months of progress. What happened?"

**Failure Reasons:**

**WRONG FIT:**
1. Great at BigCo process, couldn't handle startup ambiguity
2. Culture mismatch—too hierarchical for our flat structure
3. Technical skills outdated (legacy stack experience)
4. Wanted to build empire, not ship product

**POOR PROCESS:**
5. We were desperate and moved too fast
6. References were from friends, not actual reports
7. Didn't test actual work (no trial project)
8. Founder charisma masked red flags in interviews

**WRONG EXPECTATIONS:**
9. We said "VP" but needed "player-coach"
10. Compensation expectations kept growing
11. They expected more team/budget than we had

**EXTERNAL:**
12. Counter-offers pulled them back mentally
13. Their spouse hated the relocation
14. They took the job as a "stepping stone"

**Risk Assessment:**

| Failure Reason | Likelihood | Impact | Priority |
|----------------|------------|--------|----------|
| Wrong for startup stage | HIGH | CRITICAL | CRITICAL |
| Poor reference checking | MEDIUM | HIGH | CRITICAL |
| Expectations mismatch | HIGH | HIGH | CRITICAL |
| No trial period | MEDIUM | HIGH | ACTION |

**Prevention Plan:**

**Risk 1: Wrong for Startup Stage**
- Prevention: Explicitly discuss startup chaos in interview
- Test: "Tell me about a time you shipped with incomplete specs"
- Red flag: All examples from large companies

**Risk 2: Poor Reference Checking**
- Prevention: Talk to people THEY didn't list
- Minimum: 2 former direct reports (not friends)
- Ask: "Would you enthusiastically rehire them?"

**Risk 3: Expectations Mismatch**
- Prevention: Written expectations doc, signed
- Include: Budget, team size, first-year goals
- Discuss: "What if budget is cut in half?"

**Risk 4: No Trial Period**
- Prevention: Paid 2-week trial project before offer
- Alternative: Advisory period first
- At minimum: Pair on real problem for half-day

**Updated Hiring Process:**
1. Add "startup chaos" scenarios to interview
2. Reference check includes LinkedIn outreach to unlisted people
3. Written expectations document
4. 2-week paid trial before final offer
5. 90-day milestone check-in

---

## Checklists & Templates

### Pre-Mortem Canvas

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRE-MORTEM CANVAS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROJECT: _________________________________________________    │
│                                                                 │
│  DATE OF "FAILURE": _________________                          │
│                                                                 │
│  "It is [date]. This project has failed completely."           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WHY IT FAILED:                                                 │
│                                                                 │
│  1. _______________________________________________________    │
│  2. _______________________________________________________    │
│  3. _______________________________________________________    │
│  4. _______________________________________________________    │
│  5. _______________________________________________________    │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TOP 3 RISKS TO ADDRESS:                                        │
│                                                                 │
│  1. _________________ Prevention: _______________________      │
│  2. _________________ Prevention: _______________________      │
│  3. _________________ Prevention: _______________________      │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TRIPWIRES:                                                     │
│                                                                 │
│  If ___________________ → Then ___________________             │
│  If ___________________ → Then ___________________             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Team Pre-Mortem Facilitation Guide

```
## Pre-Mortem Meeting Agenda

**Duration:** 45-60 minutes
**Attendees:** Full project team
**Materials:** Sticky notes, timer, whiteboard

### 1. SETUP (5 min)
"It's [future date]. This project has failed—not just missed
targets, but failed spectacularly. We're doing a post-mortem.
With the benefit of hindsight, why did this fail?"

### 2. SILENT BRAINSTORM (7 min)
- Everyone writes failure reasons on sticky notes
- One reason per note
- Minimum 5 per person
- No talking

### 3. ROUND ROBIN (15 min)
- Each person shares one note at a time
- Post to wall, no discussion yet
- Continue until all shared
- Cluster similar items

### 4. DISCUSS & PRIORITIZE (15 min)
- Which risks are most likely?
- Which would be most damaging?
- Dot vote: everyone gets 3 dots

### 5. ACTION PLANNING (15 min)
- Top 3 risks get prevention plans
- Assign owners
- Set tripwires

### 6. CLOSE (3 min)
- Capture in doc
- Schedule follow-up
- Thank team for honesty
```

---

### Pre-Mortem Question Bank

```
## Pre-Mortem Prompts

Use these to stimulate thinking about different failure modes:

### EXECUTION
- What part of the plan was unrealistic?
- Where did quality suffer?
- What dependency let us down?

### PEOPLE
- Who underperformed or left?
- What conflict derailed us?
- What communication failed?

### RESOURCES
- What resource ran out?
- What was more expensive than planned?
- What took longer than expected?

### MARKET/EXTERNAL
- What changed in the market?
- What competitor move hurt us?
- What customer behavior surprised us?

### ASSUMPTIONS
- What "fact" proved wrong?
- What did we overlook?
- What seemed obvious in hindsight?

### TIMING
- What should we have done sooner?
- What external event affected us?
- What deadline was unrealistic?
```

---

### Pre-Mortem vs Post-Mortem

```
## When to Use Each

### PRE-MORTEM (Before)
✓ Project hasn't started yet
✓ Major decision pending
✓ Team is overconfident
✓ High-stakes initiative
✓ Want to find problems early

### POST-MORTEM (After)
✓ Project has completed (success or failure)
✓ Want to capture lessons learned
✓ Building institutional knowledge
✓ Improving future processes

### KEY DIFFERENCE

Post-Mortem: "What happened?" (Limited by actual events)
Pre-Mortem: "What COULD happen?" (Unlimited imagination)

Research shows Pre-Mortem generates 30% more failure reasons.
Why? "Prospective hindsight" makes imagined failure feel real.
```

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

- Klein, Gary. "Performing a Project Premortem" Harvard Business Review (2007)
- Klein, Gary. "Sources of Power: How People Make Decisions" (1998)
- Kahneman, Daniel. "Thinking, Fast and Slow" (2011) - Includes Klein's research
- Heath, Chip & Dan. "Decisive" (2013) - Pre-mortem applications

## Related Skills

- [inversion](../inversion/) - Broader framework that includes pre-mortem thinking
- [first-principles](../first-principles/) - Challenge assumptions surfaced in pre-mortem
- [eisenhower-matrix](../eisenhower-matrix/) - Prioritize risks by urgency/importance
- [six-thinking-hats](../six-thinking-hats/) - Black Hat provides similar risk focus

---

## Skill Metadata (Internal Use)

```yaml
name: pre-mortem
category: strategy
subcategory: risk-analysis
version: 1.0
author: MKTG Skills
source_expert: Gary Klein
source_work: "Performing a Project Premortem" (HBR 2007)
difficulty: beginner
estimated_value: $1,000 risk assessment consultation
tags: [risk-management, planning, decision-making, Klein, prospective-hindsight]
created: 2026-01-25
updated: 2026-01-25
```
