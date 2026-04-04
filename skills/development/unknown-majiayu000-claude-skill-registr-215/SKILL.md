---
name: team-topologies
description: Four fundamental team types and interaction modes from Team Topologies
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Team Topologies Skill

## When to Use This Skill

Use this skill when:

- **Team Topologies tasks** - Working on four fundamental team types and interaction modes from team topologies
- **Planning or design** - Need guidance on Team Topologies approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Design team structures using the four fundamental team types from Team Topologies.

## MANDATORY: Documentation-First Approach

Before applying Team Topologies:

1. **Invoke `docs-management` skill** for team design patterns
2. **Verify Team Topologies concepts** via MCP servers (perplexity)
3. **Base guidance on Skelton & Pais methodology**

## Four Fundamental Team Types

```text
Team Topologies Model:

┌─────────────────────────────────────────────────────────────────┐
│                      STREAM-ALIGNED TEAMS                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Feature    │  │  Feature    │  │  Feature    │              │
│  │  Team A     │  │  Team B     │  │  Team C     │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│         └────────────────┼────────────────┘                      │
│                          │                                       │
│         ┌────────────────┴────────────────┐                      │
│         ▼                                 ▼                      │
│  ┌─────────────────┐              ┌─────────────────┐            │
│  │    PLATFORM     │              │    ENABLING     │            │
│  │     TEAM        │              │     TEAM        │            │
│  └─────────────────┘              └─────────────────┘            │
│                                                                  │
│                   ┌─────────────────┐                            │
│                   │  COMPLICATED    │                            │
│                   │  SUBSYSTEM TEAM │                            │
│                   └─────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

## Stream-Aligned Teams

```text
STREAM-ALIGNED TEAM

Purpose: Primary value delivery, end-to-end ownership

Characteristics:
• Aligned to a single business stream
• Cross-functional (dev, test, ops, UX)
• End-to-end responsibility
• Close to the customer
• Majority of teams should be this type

Responsibilities:
• Own a portion of the value stream
• Deliver features to production
• Respond to customer feedback
• Own operational aspects
• Continuously improve their flow

Examples:
• Checkout Team (e-commerce)
• Mobile App Team
• Customer Onboarding Team
• Payments Team

Anti-patterns:
✗ Depends on many other teams
✗ Blocked frequently
✗ No production ownership
✗ Unclear customer/user
```

## Platform Teams

```text
PLATFORM TEAM

Purpose: Reduce cognitive load for stream-aligned teams

Characteristics:
• Treat platform as product
• Internal customers are other teams
• Self-service is the goal
• APIs and documentation focused
• Enable fast flow of stream-aligned teams

Responsibilities:
• Build internal developer platform
• Provide self-service capabilities
• Maintain stability and reliability
• Document and support platform
• Gather feedback from consuming teams

Examples:
• Infrastructure Platform Team
• Developer Experience Team
• Data Platform Team
• Security Platform Team

Platform Thinkables:
┌─────────────────────────────────────────┐
│           PLATFORM LAYERS               │
├─────────────────────────────────────────┤
│ Developer Experience                    │
│ (CLI, portal, templates, docs)          │
├─────────────────────────────────────────┤
│ Runtime Platform                        │
│ (containers, serverless, databases)     │
├─────────────────────────────────────────┤
│ Infrastructure                          │
│ (cloud, networking, security)           │
└─────────────────────────────────────────┘
```

## Enabling Teams

```text
ENABLING TEAM

Purpose: Help stream-aligned teams overcome obstacles

Characteristics:
• Specialists in a particular area
• Temporary engagement model
• Knowledge transfer focus
• Research and evaluate options
• Not doing the work FOR teams

Responsibilities:
• Identify capability gaps
• Research solutions
• Coach and mentor teams
• Help teams adopt new practices
• Measure improvement

Examples:
• DevOps Enablement Team
• Architecture Advisory Team
• Quality Engineering Team
• Agile Coaching Team

Engagement Model:
┌─────────────┐     ┌─────────────┐
│  Enabling   │────►│  Stream     │
│    Team     │     │  Team       │
└─────────────┘     └─────────────┘
       │
       ▼
[Time-boxed engagement]
       │
       ▼
[Transfer knowledge & leave]

Anti-patterns:
✗ Permanent dependency created
✗ Doing work instead of enabling
✗ No knowledge transfer
✗ No clear exit criteria
```

## Complicated Subsystem Teams

```text
COMPLICATED SUBSYSTEM TEAM

Purpose: Handle complex technical domains

Characteristics:
• Specialists in a complex area
• Reduce cognitive load on others
• Domain requires rare expertise
• Well-defined interfaces
• Relatively rare team type

When to Create:
• Math-heavy algorithms
• Legacy system specialists
• Specialized hardware integration
• Complex regulatory domains
• AI/ML model specialists

Examples:
• Video Codec Team
• Machine Learning Platform Team
• Financial Calculations Team
• Cryptography Team

Warning Signs You Don't Need One:
✗ Creating to "own" technology
✗ Architecture astronaut syndrome
✗ Avoiding sharing knowledge
✗ Politics rather than complexity
```

## Team Type Selection Guide

```text
Decision Matrix:

┌─────────────────────────────────────────────────────────────┐
│ Question                           │ Points To              │
├─────────────────────────────────────────────────────────────┤
│ Aligned to business capability?    │ Stream-aligned         │
│ Enables other teams?               │ Platform or Enabling   │
│ Creates self-service products?     │ Platform               │
│ Transfers knowledge then leaves?   │ Enabling               │
│ Requires rare specialist skills?   │ Complicated Subsystem  │
│ Has internal "customers"?          │ Platform               │
│ Has external customers?            │ Stream-aligned         │
└─────────────────────────────────────────────────────────────┘

Target Distribution:
• 80%+ Stream-aligned
• 10-15% Platform
• 5-10% Enabling
• <5% Complicated Subsystem
```

## Team Sizing

```text
Team Size Guidelines:

DUNBAR'S NUMBER AND TEAMS:
• 5-9 people per team (ideal)
• 15 max for loose-knit team
• Trust erodes beyond these limits

TWO-PIZZA RULE:
• If can't feed with two pizzas, too big
• Optimizes for communication

COGNITIVE LOAD PRINCIPLE:
• Team must be able to understand their domain
• Too big = too much to know
• Too small = too much per person

ANTI-PATTERNS:
✗ Teams of 1-2 (bus factor, isolation)
✗ Teams of 20+ (communication overhead)
✗ Frequent team changes
```

## Team Evolution

```text
How Teams Evolve:

TEAM CREATION:
1. Start with mission/purpose
2. Identify required skills
3. Define boundaries
4. Establish interaction modes

TEAM GROWTH:
1. Add capabilities gradually
2. Watch cognitive load
3. Consider splitting when >9 people

TEAM SPLITTING:
1. Identify natural seams
2. Ensure each has clear purpose
3. Define new interaction modes
4. Plan transition period

TEAM MERGING (Rare):
1. Only when strong synergies
2. Watch for culture clashes
3. Clear combined purpose needed
```

## Assessment Template

```markdown
# Team Topology Assessment: [Organization/Product]

## Current State

### Team Inventory

| Team | Current Type | Size | Dependencies | Issues |
|------|--------------|------|--------------|--------|
| [Name] | [Type] | [N] | [List] | [Problems] |

### Dependency Map

```text
[ASCII dependency diagram]
```

## Analysis

### Stream-Aligned Teams

- Count: [N]
- Percentage: [%]
- Issues: [List]

### Platform Teams

- Count: [N]
- Percentage: [%]
- Issues: [List]

### Enabling Teams

- Count: [N]
- Percentage: [%]
- Issues: [List]

### Complicated Subsystem Teams

- Count: [N]
- Percentage: [%]
- Issues: [List]

## Recommendations

### Team Type Changes

| Team | Current | Recommended | Rationale |
|------|---------|-------------|-----------|
| [Name] | [Type] | [Type] | [Why] |

### New Teams Needed

| Team | Type | Purpose |
|------|------|---------|
| [Name] | [Type] | [Why] |

### Teams to Merge/Split

| Action | Teams | Rationale |
|--------|-------|-----------|
| [Split/Merge] | [Names] | [Why] |

## Implementation Roadmap

1. [Phase 1 actions]
2. [Phase 2 actions]

## Workflow

When applying Team Topologies:

1. **Map Current State**: Inventory existing teams
2. **Classify Types**: Identify current team types
3. **Assess Gaps**: Compare to target distribution
4. **Identify Issues**: Dependencies, cognitive load, blockers
5. **Design Target**: Optimal team structure
6. **Plan Evolution**: How to get from current to target
7. **Execute Gradually**: Evolutionary change, not big bang

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
