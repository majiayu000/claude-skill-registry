---
name: thinking-pre-mortem
description: Imagine a project has failed and work backward to identify why. Use at project kickoffs, before major decisions, or when optimism may be obscuring risks.
---

# Pre-Mortem Analysis

## Overview
The pre-mortem, developed by psychologist Gary Klein, uses "prospective hindsight" to improve risk identification. Instead of asking "What could go wrong?" (which triggers defensiveness), assume the project HAS failed and ask "Why did it fail?" This simple reframe improves risk identification by approximately 30%.

**Core Principle:** It's easier to explain failure after the fact than predict it beforehand. Use this bias productively.

## When to Use
- Project kickoff (before work begins)
- Before committing to a major technical decision
- Sprint planning for high-risk work
- Before launch or major release
- When team seems overconfident
- After a plan is formed but before execution

Decision flow:
```
Starting significant work? → yes → Team confident? → yes → PRE-MORTEM ESSENTIAL
                                                   ↘ no → Pre-mortem still valuable
                         ↘ no → Standard risk assessment may suffice
```

## The Process

### Step 1: Set the Stage (2 min)
Gather the team. Explain:
> "Imagine we're 6 months in the future. The project has failed—not just missed a deadline, but failed spectacularly. We're in the postmortem. Your job: explain what went wrong."

Key: Use past tense. The failure has already happened.

### Step 2: Silent Brainstorming (5-7 min)
Each person independently writes reasons for failure:
- No discussion during this phase
- Aim for 5-10 reasons each
- Include technical, process, people, and external factors
- Think about what YOU specifically might have contributed to failure

Prompt: "It's [future date]. The project failed. Write down all the reasons why."

### Step 3: Round-Robin Sharing (10-15 min)
Go around the room, each person shares ONE reason per round:
- No critiquing or dismissing
- Facilitator captures all items
- Continue until all unique reasons surfaced
- Duplicates show consensus on key risks

### Step 4: Categorize and Prioritize (5-10 min)
Group by theme and assess:

| Category | Risk | Likelihood | Impact | Priority |
|----------|------|------------|--------|----------|
| Technical | API integration fails | High | Critical | P0 |
| Process | Requirements unclear | Medium | High | P1 |
| People | Key person leaves | Low | Critical | P1 |
| External | Vendor delays | Medium | Medium | P2 |

### Step 5: Develop Mitigations (10-15 min)
For top risks, define:
```
Risk: API integration fails
Mitigation: 
- Spike on integration in week 1
- Identify fallback vendor
- Build abstraction layer for swap-ability
Owner: [Name]
Checkpoint: Week 2 review
```

### Step 6: Update the Plan
Incorporate mitigations into project plan:
- Add spike/investigation tasks
- Build in contingency time
- Assign risk owners
- Schedule risk review checkpoints

## Pre-Mortem Template

```markdown
# Pre-Mortem: [Project Name]
Date: [Date]
Participants: [Names]

## The Scenario
It is [Future Date]. [Project] has failed spectacularly. 

## Failure Reasons Identified

### Technical
- [Reason 1]
- [Reason 2]

### Process  
- [Reason 1]
- [Reason 2]

### People/Team
- [Reason 1]
- [Reason 2]

### External/Dependencies
- [Reason 1]
- [Reason 2]

## Priority Risks and Mitigations

### P0: [Risk Name]
- **Description**: [What went wrong]
- **Mitigation**: [How to prevent]
- **Owner**: [Who]
- **Checkpoint**: [When to verify]

### P1: [Risk Name]
...

## Plan Updates
- [ ] [Action item from pre-mortem]
- [ ] [Action item from pre-mortem]

## Review Schedule
- [Date]: First risk checkpoint
- [Date]: Mid-project risk review
```

## Why Pre-Mortems Work

1. **Legitimizes Pessimism**: Team members can voice concerns without seeming negative
2. **Bypasses Groupthink**: Individual brainstorming before sharing prevents anchoring
3. **Uses Hindsight Bias**: Easier to explain past than predict future
4. **Creates Psychological Safety**: "The project failed" removes blame
5. **Surfaces Hidden Knowledge**: People share concerns they wouldn't otherwise raise

## Common Failure Categories to Prompt

| Category | Example Failures |
|----------|-----------------|
| Requirements | Scope creep, unclear success criteria, missing stakeholder |
| Technical | Wrong architecture, integration failures, scale issues |
| Timeline | Underestimation, dependencies delayed, parallel work blocked |
| Team | Key person unavailable, skill gaps, communication breakdown |
| External | Vendor issues, regulatory changes, market shift |
| Process | Insufficient testing, deployment problems, no rollback |

## Facilitation Tips
- **Enforce silence** during brainstorming—no discussion
- **Use past tense** consistently ("failed" not "might fail")
- **Capture everything**—don't filter during collection
- **Include yourself**—what might YOU have done wrong?
- **Follow up**—pre-mortem is worthless without action

## Verification Checklist
- [ ] Conducted at appropriate time (before significant work)
- [ ] All team members participated
- [ ] Silent brainstorming enforced
- [ ] 20+ failure reasons collected
- [ ] Risks prioritized by likelihood × impact
- [ ] Top 3-5 risks have explicit mitigations
- [ ] Mitigations assigned owners and checkpoints
- [ ] Plan updated to incorporate findings
- [ ] Follow-up risk review scheduled

## Key Questions
- "The project failed. Why?"
- "What did we miss that was obvious in retrospect?"
- "What warning signs did we ignore?"
- "What did I personally contribute to the failure?"
- "What did we assume that turned out to be wrong?"
- "Who did we forget to involve?"
