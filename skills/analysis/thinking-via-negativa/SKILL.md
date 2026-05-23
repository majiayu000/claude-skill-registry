---
name: thinking-via-negativa
description: Improve by removal rather than addition. Focus on what to stop doing, eliminate the negative, and subtract complexity. Use for system simplification, process improvement, and feature prioritization.
---

# Via Negativa

## Overview

Via Negativa, articulated by Nassim Taleb in "Antifragile," is the principle that improvement often comes from subtraction rather than addition. We're biased toward adding (features, processes, complexity) when removing (bugs, friction, unnecessary work) often provides more value with less risk.

**Core Principle:** Focus on what to remove, not what to add. Subtraction is more robust than addition.

## When to Use

- System simplification
- Process improvement
- Feature prioritization (what NOT to build)
- Performance optimization
- Reducing technical debt
- Personal productivity
- Decision-making (what to avoid)
- Code review (what to delete)

Decision flow:

```
Trying to improve something?
  → First instinct is to add? → yes → PAUSE, CONSIDER SUBTRACTION
  → Can you achieve the goal by removing instead? → yes → REMOVE FIRST
  → Is current complexity necessary? → no → SIMPLIFY VIA NEGATIVA
```

## The Via Negativa Process

### Step 1: Identify What to Eliminate

Instead of "What should we add?", ask:

```
- What's not working that we should remove?
- What's causing harm we should stop?
- What's unnecessary complexity we should eliminate?
- What's outdated that we should delete?
```

### Step 2: Catalog Candidates for Removal

List elements that might be subtracted:

```markdown
## Candidates for Removal

Code:
- Dead code (unreachable)
- Deprecated features (still running)
- Unused dependencies
- Redundant abstractions

Process:
- Meetings that don't produce decisions
- Approval steps that don't add value
- Reports no one reads
- Alerts no one acts on

Features:
- Low-usage functionality
- Legacy features maintained "just in case"
- Edge cases that complicate the core
```

### Step 3: Evaluate Impact of Removal

For each candidate:

```markdown
| Element | Usage | Maintenance Cost | Risk of Removal | Value of Removal |
|---------|-------|------------------|-----------------|------------------|
| Feature X | 0.1% of users | 20 hrs/month | Low | High |
| Meeting Y | 8 people | 4 hrs/week | None | High |
| Process Z | 5 approvers | 2 days/request | Medium | Medium |
```

### Step 4: Remove with Monitoring

Subtract and verify no harm:

```markdown
Week 1: Remove Feature X for 10% of users
Week 2: Monitor complaints, metrics
Week 3: If no issues, remove for 50%
Week 4: Full removal and code deletion
```

## Via Negativa Patterns

### Subtractive Design

Add by removing:

```
Goal: Make the product easier to use
Additive approach: Add tutorial, tooltips, help section
Via Negativa: Remove confusing features, simplify flow, delete options

Often more effective:
- Fewer choices = easier decisions
- Less surface area = less to learn
- Simpler UI = faster adoption
```

### The Pruning Principle

Healthy growth requires pruning:

```
Codebase:
- Every feature has maintenance cost
- Old features create complexity tax
- Pruning unused code enables healthier growth

Team:
- Every process has coordination cost
- Old processes accumulate like barnacles
- Pruning enables focus on what matters
```

### Harm Reduction Over Benefit Addition

Removing bad is often more impactful than adding good:

```
Performance:
- Removing one slow query helps more than adding one cache
- Eliminating N+1 beats adding read replicas
- Deleting unused indexes beats adding new ones

Health (Taleb's domain):
- Removing sugar helps more than adding supplements
- Stopping smoking beats starting exercise
- Eliminating stress beats adding meditation
```

### The 80/20 Removal

Remove the 80% that provides 20% of value:

```markdown
## Feature Usage Analysis

| Feature | Users | Revenue | Maintenance |
|---------|-------|---------|-------------|
| Core A | 90% | 70% | 20% |
| Core B | 85% | 25% | 15% |
| Edge C | 5% | 3% | 25% |
| Edge D | 2% | 2% | 40% |

Via Negativa: Remove Edge C and D
Result: 65% less maintenance for 5% of value
        Enables focus on Core A and B
```

## Application Areas

### Code

```markdown
## Via Negativa Code Review

Before adding new code, ask:
1. Can we solve this by removing existing code?
2. Is there dead code to delete?
3. Are there unused imports/dependencies?
4. Is there duplication to consolidate?
5. Are there unnecessary abstractions?

Rule: Every PR should delete at least as much as it adds
      (aspirational, not mandatory)
```

### Process

```markdown
## Via Negativa Process Audit

List all recurring processes:
- Daily standup (15 min/day × 8 people = 10 hrs/week)
- Sprint planning (2 hrs × 8 people = 16 hrs/sprint)
- Weekly status report (2 hrs to write)
- Monthly review (4 hrs × 5 people = 20 hrs/month)

For each, ask:
- What happens if we stop?
- Can we reduce frequency?
- Can we reduce attendees?
- Can we reduce duration?

Often: Half the meetings, half the reports = more productive
```

### Features

```markdown
## Via Negativa Product Strategy

Instead of roadmap of additions, create:

## Sunset List
| Feature | Usage | Decision | Timeline |
|---------|-------|----------|----------|
| Export to CSV | 0.5% | Remove | Q2 |
| Legacy API v1 | 2% | Deprecate | Q3 |
| Advanced filters | 3% | Simplify | Q2 |

## Maintenance Liberation
Removing 3 features frees 2 engineers for core work

## Simplicity Gains
- Fewer code paths to test
- Smaller attack surface
- Easier onboarding
- Faster development
```

### Personal Productivity

```markdown
## Via Negativa for Focus

Don't add:
- More productivity apps
- More systems
- More commitments

Instead remove:
- Notifications
- Unnecessary meetings
- Low-value tasks
- Context switching
- Decision fatigue (reduce choices)

"Stop doing" list > "To do" list
```

### Architecture

```markdown
## Via Negativa Architecture Review

Before adding complexity, audit existing:

Services to consolidate:
- Microservice A and B do similar things → Merge
- Service C has one caller → Inline

Dependencies to remove:
- Library X is used for one function → Write function
- Framework Y is overkill → Use lighter alternative

Layers to eliminate:
- Abstraction that has one implementation → Remove
- API that wraps another API identically → Direct call
```

## Via Negativa Template

```markdown
# Via Negativa Analysis: [System/Process/Product]

## Current State
[Description of what exists]

## Candidates for Removal

### Category 1: Unused/Dead
| Element | Evidence of Non-Use | Removal Risk |
|---------|---------------------|--------------|
| | | |

### Category 2: Low-Value High-Cost
| Element | Value Provided | Maintenance Cost | Ratio |
|---------|---------------|------------------|-------|
| | | | |

### Category 3: Redundant
| Element | Duplicated By | Removal Path |
|---------|---------------|--------------|
| | | |

## Removal Priority
1. [Element] - [Why first]
2. [Element] - [Why second]

## Removal Plan
| Element | Week | Monitor | Rollback |
|---------|------|---------|----------|
| | | | |

## Expected Benefits
- Reduced complexity: [Measure]
- Freed resources: [Measure]
- Improved focus: [Measure]
```

## The Lindy Connection

Via Negativa aligns with Lindy:
- Old things that have survived removal attempts are robust
- New additions are fragile, unproven
- Subtracting recent additions is lower risk than adding new things

## Verification Checklist

- [ ] Asked "what can we remove?" before "what should we add?"
- [ ] Identified candidates for removal in multiple categories
- [ ] Evaluated usage/value of removal candidates
- [ ] Planned gradual removal with monitoring
- [ ] Considered second-order effects of removal
- [ ] Resisted the urge to add when subtraction would work

## Key Questions

- "What can we remove instead of add?"
- "What would happen if we stopped doing this?"
- "What's the maintenance cost of this existing thing?"
- "Is this complexity earning its keep?"
- "What should we stop doing?"
- "What would we not build if starting from scratch?"

## Taleb's Wisdom

"The first principle of iatrogenics: we do not need evidence of harm to claim that a treatment is harmful; we need evidence of benefit to claim it is not harmful."

Applied to software: We don't need evidence that a feature is actively harmful to remove it; we need evidence it provides benefit to keep it.

"Via Negativa is more powerful than Via Positiva: omission does less harm than commission."

Removing is safer than adding. Every addition has unknown side effects. Removal of recent additions reverts to a known-good state. When in doubt, subtract.

"The best way to live is to maximize the number of decisions not made."

Reduce decisions through simplification. Fewer features = fewer decisions to make. Fewer processes = fewer coordination points. Simpler is more robust.
