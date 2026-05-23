---
name: thinking-opportunity-cost
description: Evaluate decisions by what you give up, not just what you gain. Use for resource allocation, prioritization, build vs. buy choices, and technical debt evaluation.
---

# Opportunity Cost Thinking

## Overview

Opportunity cost is the value of the next-best alternative foregone when making a choice. Every decision to do X is simultaneously a decision not to do Y, Z, and everything else. Engineers often focus on the value of their chosen path while underweighting what they're giving up.

**Core Principle:** The true cost of anything is what you give up to get it. A "free" option that consumes time has massive opportunity cost.

## When to Use

- Resource allocation (time, money, people)
- Feature prioritization
- Build vs. buy decisions
- Technical debt evaluation
- Career decisions
- Architecture choices
- Saying "yes" to any commitment

Decision flow:

```
Making a commitment?
  → Have you considered what you're NOT doing? → no → APPLY OPPORTUNITY COST
  → Is the foregone value significant? → yes → Factor into decision
                                       ↘ no → Proceed
```

## The Opportunity Cost Framework

### Step 1: Identify the Choice

State the decision explicitly:

```
Choice: Build custom authentication system
Commitment: 3 engineers for 4 months
```

### Step 2: List the Alternatives

What else could you do with those resources?

```
Alternatives for 3 engineers × 4 months:
A. Build custom auth (the choice)
B. Use Auth0 ($500/mo) + build 3 features
C. Improve performance of existing system
D. Reduce technical debt backlog by 40%
E. Build new product line MVP
```

### Step 3: Value Each Alternative

Estimate the value of each path:

```markdown
| Alternative | Direct Value | Strategic Value | Risk | Total Value |
|-------------|--------------|-----------------|------|-------------|
| Custom auth | Full control, no vendor cost | IP ownership | High (security) | Medium |
| Auth0 + features | Features faster | Time to market | Low | High |
| Performance work | 2x throughput | Customer satisfaction | Low | Medium-High |
| Tech debt | Faster future dev | Developer retention | Low | Medium |
| New product MVP | Revenue diversification | Growth potential | High | High |
```

### Step 4: Calculate Opportunity Cost

Opportunity cost = Value of best foregone alternative

```
If we choose Custom Auth:
  Best alternative foregone: Auth0 + features (rated "High")
  Opportunity cost: The features we won't build + faster time to market
```

### Step 5: Make Decision with Full Accounting

Total cost of choice = Direct cost + Opportunity cost

```
Custom Auth True Cost:
  Direct: 3 engineers × 4 months = 12 engineer-months
  Opportunity: 3 features delayed by 4 months
             + Market share lost to faster competitors
             + Developer time not on revenue features

Question: Is custom auth worth all of that?
```

## Opportunity Cost Patterns

### The "Free" Trap

Nothing is free if it consumes time:

```
Scenario: "We can build this ourselves instead of paying $10K for the tool"

Analysis:
- Tool cost: $10,000
- Build time: 2 engineers × 2 weeks = 4 engineer-weeks
- Engineer cost: ~$4,000/week fully loaded = $16,000
- Maintenance: 1 week/quarter = $16,000/year ongoing

True cost: $16K + ongoing maintenance > $10K + $0 maintenance
Plus: What else could those engineers have built?
```

### The Sunk Cost Interaction

Don't let sunk costs distort opportunity cost analysis:

```
BAD thinking:
"We've already spent 6 months on this, we can't abandon it"
(Sunk cost fallacy ignores opportunity cost of continuing)

GOOD thinking:
"Given where we are now, what's the best use of the NEXT 6 months?"
(Fresh opportunity cost analysis from current state)
```

### The Hidden Alternative

The status quo is always an alternative:

```
Proposal: Migrate to Kubernetes
Alternatives considered: ECS, Nomad, K8s
Missing alternative: Don't migrate, improve current system

Full analysis should include:
- Cost of migration (all options)
- Cost of staying put (often undervalued)
- Opportunity cost of engineers doing migration vs. features
```

### Time as the Scarcest Resource

Time opportunity cost is often highest:

```
"Quick meeting, only 30 minutes"

For 8-person meeting:
- Direct cost: 30 min × 8 = 4 person-hours
- Opportunity cost: 4 hours not spent on focused work
- Context switching cost: 15 min recovery × 8 = 2 more hours
- True cost: ~6 person-hours of productivity

Question: Is this meeting worth 6 hours of productivity?
```

## Application Areas

### Feature Prioritization

```markdown
## Opportunity Cost Analysis: Feature A vs. B

| Factor | Feature A | Feature B |
|--------|-----------|-----------|
| Dev time | 4 weeks | 2 weeks |
| Revenue impact | $50K/month | $30K/month |
| Time to value | 4 weeks | 2 weeks |

If we build A first:
- We get A in 4 weeks
- We get B in 6 weeks
- 2 extra weeks without B = $60K foregone

If we build B first:
- We get B in 2 weeks
- We get A in 6 weeks
- 2 extra weeks without A = $100K foregone

Decision: Build A first despite higher dev cost (higher opportunity cost of delay)
```

### Build vs. Buy

```markdown
## Build vs. Buy: Monitoring System

Build:
- Development: $200K (4 engineers × 6 months)
- Maintenance: $80K/year
- Time to production: 6 months
- Opportunity cost: Features those engineers would have built

Buy (Datadog):
- License: $50K/year
- Integration: $30K (2 engineers × 1 month)
- Time to production: 1 month
- Opportunity cost: None significant

5-year TCO:
- Build: $200K + ($80K × 5) + opportunity cost = $600K + opportunity
- Buy: ($50K × 5) + $30K = $280K

Decision: Buy unless unique requirements justify 2x+ cost
```

### Technical Debt

```markdown
## Technical Debt Opportunity Cost

Current state: 20% of engineering time on maintenance
Proposed: 3-month refactoring project

Analysis:
- 3 months of refactoring = no features for 3 months
- After refactoring: 10% time on maintenance (saves 10%)
- Break-even: When does saved maintenance = investment?

If team = 10 engineers:
- Investment: 10 × 3 = 30 engineer-months
- Monthly savings: 10 × 10% = 1 engineer-month
- Break-even: 30 months

Opportunity cost: Features not built during 3-month refactoring
Real question: Are those features worth more than 30+ months of 10% overhead?
```

### Hiring Decisions

```markdown
## Hiring Opportunity Cost

Choice: Hire senior engineer at $250K
Alternative: Two mid-level at $300K total

Analysis:
- Senior: Higher immediate productivity, mentorship
- Two mid: More throughput long-term, redundancy

Opportunity cost of senior:
- Fewer total engineers
- Less coverage/redundancy
- Longer ramp-up if they leave

Opportunity cost of two mid:
- More management overhead
- Longer to complex projects
- Training investment

Decision depends on: Current team composition, project complexity, growth stage
```

## Opportunity Cost Template

```markdown
# Opportunity Cost Analysis: [Decision]

## The Choice
What we're considering: [Primary option]
Resource commitment: [Time, money, people]

## Alternatives
What else could we do with these resources?

| # | Alternative | Resource Use | Direct Value | Strategic Value |
|---|-------------|--------------|--------------|-----------------|
| 1 | [Primary choice] | [X] | [Value] | [Strategic] |
| 2 | [Alternative 1] | [X] | [Value] | [Strategic] |
| 3 | [Alternative 2] | [X] | [Value] | [Strategic] |
| 4 | Do nothing | [X] | [Value] | [Strategic] |

## Opportunity Cost Calculation

Best foregone alternative: [Which one]
Value of that alternative: [Quantified if possible]

## True Cost of Primary Choice
- Direct cost: [Resources consumed]
- Opportunity cost: [Value of foregone alternative]
- Total: [Sum]

## Decision
Is [primary choice] worth [total cost]?
[Reasoning]

## Reversibility
If we're wrong, can we change course? At what cost?
```

## Mental Shortcuts

### The "What Else?" Question

Always ask: "If we didn't do this, what would we do instead?"

### The 10x Test

If opportunity cost is 10x the direct cost, rethink the decision.

### The Time Value Multiplier

Engineer time often has 3-5x multiplier in opportunity cost vs. dollar cost.

### The Status Quo Alternative

Always include "change nothing" as an explicit alternative.

## Verification Checklist

- [ ] Explicitly stated the choice and resource commitment
- [ ] Listed at least 3 alternatives (including status quo)
- [ ] Valued each alternative (even roughly)
- [ ] Identified the best foregone alternative
- [ ] Calculated opportunity cost explicitly
- [ ] Made decision accounting for full cost
- [ ] Considered reversibility

## Key Questions

- "What are we NOT doing by choosing this?"
- "Is the 'free' option actually free?"
- "What would we do with these resources otherwise?"
- "What's the value of our next-best alternative?"
- "Is this worth more than everything we're giving up?"
- "Have we included the status quo as an option?"

## Economic Wisdom

"There is no such thing as a free lunch." — Milton Friedman

Every choice has a cost, even if it's not written on an invoice. The cost is what you gave up to make that choice. Recognizing opportunity cost transforms how you evaluate decisions.

"The cost of a thing is the amount of what I will call life which is required to be exchanged for it." — Henry David Thoreau

For engineers: substitute "engineering time" for "life" — it's your most valuable and constrained resource.
