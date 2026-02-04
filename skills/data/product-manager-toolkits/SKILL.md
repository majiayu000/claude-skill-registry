---
name: product-manager-toolkits
description: Product management frameworks, templates, and tools for roadmapping, prioritization, user research, stakeholder management, and product strategy.
version: 1.0.0
author: Perry
---

# Product Manager Toolkit

You are an experienced product manager who helps with product strategy, feature prioritization, user research, and stakeholder communication.

## Core PM Frameworks

### 1. Problem Discovery

Before building anything, validate the problem:

```markdown
## Problem Statement

**Who** has this problem?
**What** is the problem they face?
**When/Where** does this problem occur?
**Why** does this problem matter?
**How** are they solving it today?

### Evidence
- User interviews: [count]
- Support tickets: [count]
- Analytics data: [metric]
- Competitor analysis: [findings]

### Impact
- Users affected: [number/percentage]
- Business impact: [revenue/retention/growth]
- Strategic alignment: [company goals]
```

### 2. RICE Prioritization

Score features to prioritize objectively:

| Factor | Definition | Scale |
|--------|-----------|-------|
| **R**each | How many users affected per quarter | Actual number |
| **I**mpact | How much will it move the metric | 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal |
| **C**onfidence | How sure are you about estimates | 100%=high, 80%=medium, 50%=low |
| **E**ffort | Person-months to complete | Actual estimate |

**RICE Score = (Reach × Impact × Confidence) / Effort**

```markdown
## Feature Prioritization

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| Dark mode | 5000 | 1 | 80% | 2 | 2000 |
| Export CSV | 2000 | 2 | 100% | 1 | 4000 |
| SSO | 500 | 3 | 80% | 3 | 400 |
```

### 3. Jobs To Be Done (JTBD)

```markdown
## Job Statement

When [situation/context],
I want to [motivation/goal],
so I can [expected outcome].

### Example
When I'm reviewing my team's weekly progress,
I want to see a summary of completed tasks,
so I can report accurate updates to leadership.

### Job Map
1. Define the goal
2. Locate resources needed
3. Prepare to do the job
4. Confirm readiness
5. Execute the job
6. Monitor progress
7. Modify as needed
8. Conclude the job
```

### 4. Kano Model

Categorize features by user satisfaction:

- **Must-haves** (Basic): Expected, absence causes dissatisfaction
- **Performance** (Linear): More is better, directly proportional to satisfaction
- **Delighters** (Excitement): Unexpected features that create joy
- **Indifferent**: Users don't care either way
- **Reverse**: Some users want it, others don't

## Document Templates

### Product Requirements Document (PRD)

```markdown
# PRD: [Feature Name]

## Overview
**Owner**: [PM Name]
**Status**: Draft | In Review | Approved
**Target Release**: Q[X] 2024

## Problem Statement
[2-3 sentences describing the user problem]

## Goals & Success Metrics
| Goal | Metric | Target |
|------|--------|--------|
| [Goal 1] | [Metric] | [Target] |

## User Stories

### Primary Persona: [Name]
As a [type of user],
I want to [action],
so that [benefit].

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

## Solution Overview
[High-level description of the proposed solution]

### In Scope
- Feature A
- Feature B

### Out of Scope
- Feature X (future consideration)
- Feature Y (not aligned with goals)

## Design
[Link to designs/mockups]

## Technical Considerations
[Any technical constraints or dependencies]

## Dependencies
- [ ] Dependency 1
- [ ] Dependency 2

## Rollout Plan
- Phase 1: Internal testing
- Phase 2: Beta (10% of users)
- Phase 3: General availability

## Open Questions
1. [Question 1]
2. [Question 2]
```

### Feature Spec (Lightweight)

```markdown
# Feature: [Name]

## The Ask
[One paragraph summary]

## Why Now?
[Business justification]

## User Flow
1. User does X
2. System responds with Y
3. User completes Z

## Edge Cases
- What if [scenario]? → [handling]
- What if [scenario]? → [handling]

## Success =
[Single metric that defines success]

## Timeline
- Design: [date]
- Dev Start: [date]
- QA: [date]
- Launch: [date]
```

### Roadmap Format

```markdown
# Product Roadmap - [Quarter/Year]

## Theme: [Strategic Focus]

### Now (Current Sprint)
| Initiative | Status | Owner | Notes |
|------------|--------|-------|-------|
| Feature A | In Progress | @dev | On track |

### Next (Next 2-4 weeks)
| Initiative | Priority | Dependencies |
|------------|----------|--------------|
| Feature B | P0 | Design complete |

### Later (This Quarter)
| Initiative | Status | Notes |
|------------|--------|-------|
| Feature C | Planned | Pending research |

### Future (Backlog)
- Idea X
- Idea Y
- Idea Z
```

## User Research

### Interview Script Template

```markdown
## Interview: [Topic]

### Introduction (2 min)
"Thanks for joining. I'm researching [topic] to understand how we can improve [area]. There are no right or wrong answers—I want to learn about your experience."

### Warm-up (3 min)
- Tell me about your role
- How long have you been using [product]?
- What do you primarily use it for?

### Core Questions (20 min)
1. Walk me through the last time you [did task]
2. What was the most challenging part?
3. How do you currently handle [problem]?
4. What would make this easier?
5. [Specific question about feature]

### Wrap-up (5 min)
- Anything else you'd like to share?
- Can I follow up if I have more questions?

### Notes
[Take detailed notes here]

### Key Insights
- Insight 1
- Insight 2
```

### Survey Best Practices

- Keep surveys under 5 minutes
- Use a mix of quantitative (scale) and qualitative (open-ended)
- Avoid leading questions
- Include a "why" follow-up for key questions
- Test with 5 people before sending widely

## Stakeholder Management

### RACI Matrix

```markdown
## RACI: [Project Name]

| Task | PM | Eng | Design | Exec | Legal |
|------|----|----|--------|------|-------|
| Requirements | A | C | C | I | - |
| Design | C | C | R | I | - |
| Development | I | R | C | I | - |
| Launch | A | R | C | A | C |

R = Responsible (does the work)
A = Accountable (final decision)
C = Consulted (input before)
I = Informed (told after)
```

### Stakeholder Update Email

```markdown
Subject: [Project] Weekly Update - [Date]

## TL;DR
[One sentence summary]

## Progress
✅ Completed: [items]
🔄 In progress: [items]
⏳ Upcoming: [items]

## Metrics
[Key metrics if applicable]

## Blockers/Risks
🚨 [Blocker and mitigation plan]

## Decisions Needed
[Any decisions required from stakeholders]

## Next Week
[Plan for coming week]
```

## Metrics & Analytics

### Pirate Metrics (AARRR)

| Stage | Question | Example Metrics |
|-------|----------|-----------------|
| **A**cquisition | How do users find us? | Signups, traffic sources |
| **A**ctivation | Do they have a good first experience? | Onboarding completion, time to value |
| **R**etention | Do they come back? | DAU/MAU, churn rate |
| **R**evenue | Do they pay? | Conversion rate, ARPU, LTV |
| **R**eferral | Do they tell others? | NPS, referral rate |

### North Star Framework

```markdown
## North Star Metric: [Metric Name]

**Definition**: [How it's calculated]
**Why this metric**: [Connection to value]
**Current**: [value]
**Target**: [goal]

### Input Metrics
1. [Input 1] - affects NSM by [how]
2. [Input 2] - affects NSM by [how]
3. [Input 3] - affects NSM by [how]
```

## Go-To-Market

### Launch Checklist

```markdown
## Launch: [Feature Name]

### Pre-Launch
- [ ] PRD approved
- [ ] Design finalized
- [ ] Development complete
- [ ] QA passed
- [ ] Documentation updated
- [ ] Support team trained
- [ ] Marketing assets ready
- [ ] Analytics tracking verified

### Launch Day
- [ ] Feature flag enabled
- [ ] Monitoring dashboards active
- [ ] Announcement published
- [ ] Support on standby

### Post-Launch
- [ ] Monitor metrics for 48 hours
- [ ] Collect early feedback
- [ ] Address critical issues
- [ ] Share results with team
```

## Quick Reference

### PM Daily Checklist
- [ ] Check key metrics dashboard
- [ ] Review customer feedback/tickets
- [ ] Standup with engineering
- [ ] Unblock team members
- [ ] Move roadmap items forward

### Questions to Ask Before Building
1. What problem does this solve?
2. Who has this problem?
3. How do we know they have it?
4. What's the smallest thing we can build to test?
5. How will we measure success?
