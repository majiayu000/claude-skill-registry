---
name: Roadmap Builder
slug: roadmap-builder
description: Create strategic product roadmaps with theme-based planning, OKRs, and stakeholder alignment
category: project
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "build roadmap"
  - "create roadmap"
  - "product roadmap"
  - "roadmap planning"
  - "quarterly planning"
tags:
  - roadmap
  - strategy
  - product
  - okrs
  - themes
  - planning
---

# Roadmap Builder

The Roadmap Builder skill helps product teams create strategic roadmaps that align tactical execution with business objectives. It emphasizes theme-based planning over feature lists, outcome-focused goals using OKRs, and flexible planning that adapts to market feedback and changing priorities.

This skill excels at translating business strategy into quarterly themes, breaking themes into initiatives and epics, aligning stakeholders around shared goals, and maintaining roadmap clarity while preserving execution flexibility.

Roadmap Builder follows modern product management principles: outcomes over outputs, themes over features, and quarterly planning with monthly reviews.

## Core Workflows

### Workflow 1: Create Product Roadmap

**Steps:**
1. **Define Strategic Context**
   - Review company vision and business goals
   - Analyze market position and competitive landscape
   - Gather customer insights and pain points
   - Identify key metrics to move (North Star, etc.)
   - Understand resource constraints (team, budget, time)

2. **Set Quarterly Themes**
   - Define 2-4 themes for next quarter
   - Each theme represents a strategic bet or focus area
   - Themes should be outcome-oriented, not feature lists
   - Examples: "Reduce churn", "Enterprise-ready", "10x performance"
   - Align themes with OKRs or company goals

3. **Create OKRs for Each Theme**
   - **Objective**: Qualitative, inspiring goal
   - **Key Results**: 3-5 measurable outcomes
   - Ensure Key Results are ambitious but achievable
   - Define baseline and target metrics
   - Assign ownership to product/engineering leads

4. **Identify Initiatives**
   - For each theme, brainstorm potential initiatives
   - Initiative = significant effort to move a Key Result
   - Prioritize initiatives by impact vs. effort
   - Select top 2-4 initiatives per theme
   - Estimate rough timeline (weeks or months)

5. **Break Down into Epics**
   - Decompose initiatives into epics
   - Epic = large user story spanning multiple sprints
   - Write epic descriptions with user value and success criteria
   - Sequence epics based on dependencies and learning goals
   - Assign to teams or squads

6. **Create Timeline View**
   - Plot themes, initiatives, and epics on timeline
   - Use swim lanes for different teams or product areas
   - Show dependencies and sequencing
   - Highlight milestones and release dates
   - Add confidence levels (high/medium/low)

7. **Stakeholder Alignment**
   - Present roadmap to leadership and stakeholders
   - Gather feedback and adjust priorities
   - Communicate trade-offs and decisions
   - Set expectations on what's NOT on roadmap
   - Establish review cadence (monthly or quarterly)

**Output:** Strategic roadmap with themes, OKRs, initiatives, epics, and timeline.

### Workflow 2: Quarterly Roadmap Review

**Steps:**
1. Review previous quarter's OKRs and achievement
2. Analyze what worked, what didn't, and why
3. Gather updated customer and market insights
4. Assess team capacity and velocity trends
5. Set next quarter's themes and OKRs
6. Adjust long-term roadmap based on learnings
7. Communicate changes to all stakeholders

### Workflow 3: Monthly Roadmap Health Check

**Steps:**
1. Review progress on current initiatives
2. Check if Key Results are trending toward targets
3. Identify risks, blockers, or scope issues
4. Adjust timeline or scope if needed
5. Communicate status to stakeholders
6. Reprioritize if market or business conditions change

### Workflow 4: Feature Request Evaluation

**When new feature requests arrive:**
1. Understand the underlying customer problem
2. Evaluate against current themes and OKRs
3. Assess impact (how many users, revenue potential)
4. Estimate effort and opportunity cost
5. Decide: Add to roadmap, defer to backlog, or decline
6. Communicate decision with clear rationale

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Create roadmap | "build product roadmap" |
| Set quarterly themes | "define Q[n] themes" |
| Create OKRs | "create OKRs for [theme]" |
| Add initiative | "add initiative: [description]" |
| Review roadmap | "roadmap health check" |
| Quarterly planning | "plan Q[n] roadmap" |
| Evaluate feature | "evaluate feature: [idea]" |
| Show timeline | "show roadmap timeline" |
| Stakeholder view | "create stakeholder roadmap view" |
| Prioritize initiatives | "prioritize roadmap items" |

## Best Practices

- **Themes over features**: Organize by strategic themes, not lists of features; themes provide context and flexibility
- **Outcomes over outputs**: Focus on business outcomes (reduce churn, increase revenue) not outputs (ship feature X)
- **Use OKRs properly**: Objectives inspire, Key Results measure; aim for 70% achievement (not 100%)
- **Plan quarterly, review monthly**: Quarter is sweet spot for strategic planning; review monthly to adapt
- **Communicate the "why"**: Every roadmap item should clearly connect to business strategy
- **Show confidence levels**: Be transparent about uncertainty; high/medium/low confidence
- **Timelines are estimates**: Use "Q2" or "H2" not specific dates; preserve flexibility
- **Visualize simply**: Avoid cluttered roadmaps; focus on themes and key milestones
- **Say no strategically**: Roadmap power comes from what you DON'T do; protect focus
- **Align, don't dictate**: Roadmap should align teams, not micromanage execution
- **Balance innovation and maintenance**: Reserve capacity for tech debt, bugs, and platform improvements
- **Update regularly**: Stale roadmaps kill trust; keep it current and communicate changes

## Roadmap Formats

### Theme-Based Roadmap
```
Q1 2026: Enterprise-Ready
  Initiative: SSO & Advanced Security
  Initiative: Audit Logs & Compliance

Q2 2026: 10x Performance
  Initiative: Database Optimization
  Initiative: Caching Layer

Q3 2026: Mobile-First Experience
  Initiative: Native Mobile Apps
  Initiative: Offline Support
```

### Now-Next-Later Roadmap
```
NOW (this quarter)
  - Theme 1: [Active work]
  - Theme 2: [Active work]

NEXT (next quarter)
  - Theme 3: [Planned]
  - Theme 4: [Planned]

LATER (future)
  - Theme 5: [Exploring]
  - Theme 6: [Researching]
```

### Outcome-Based Roadmap
```
Goal: Reduce Customer Churn by 30%
  → Improve onboarding (Q1)
  → Better customer support (Q2)
  → Product stability (Q2-Q3)

Goal: 2x Enterprise Revenue
  → SSO & Advanced Auth (Q1)
  → Compliance Features (Q2)
  → Enterprise Admin Tools (Q3)
```

## OKR Template

```
Theme: [Strategic Focus Area]

Objective: [Inspiring, qualitative goal]

Key Results:
  KR1: [Metric] from [baseline] to [target]
  KR2: [Metric] from [baseline] to [target]
  KR3: [Metric] from [baseline] to [target]

Initiatives:
  1. [Initiative name] - [Timeline]
  2. [Initiative name] - [Timeline]
  3. [Initiative name] - [Timeline]
```

**Example:**
```
Theme: Enterprise-Ready

Objective: Make our product the default choice for enterprise customers

Key Results:
  KR1: Increase enterprise deals from 5/quarter to 15/quarter
  KR2: Achieve SOC 2 Type II certification
  KR3: Reduce enterprise sales cycle from 6 months to 3 months

Initiatives:
  1. SSO & Advanced Auth - Q1
  2. Audit Logs & Compliance - Q1-Q2
  3. Enterprise Admin Console - Q2
```

## Prioritization Framework

### RICE Scoring
For each initiative:
- **Reach**: How many customers will benefit?
- **Impact**: How much will it help them? (0.25, 0.5, 1, 2, 3)
- **Confidence**: How sure are we? (%, as decimal)
- **Effort**: Person-months required

Score = (Reach × Impact × Confidence) / Effort

### Value vs. Complexity Matrix
```
       HIGH VALUE
           |
   DO NEXT | DO FIRST
           |
  -------- + --------  COMPLEXITY
           |
   SKIP    | DO LATER
           |
      LOW VALUE
```

### Strategic Alignment Score
Rate each initiative (1-5):
- Aligns with company vision
- Moves key business metrics
- Requested by strategic customers
- Competitive necessity
- Technical foundation for future work

Total score guides prioritization.

## Timeline Planning

**Rough Sizing:**
- **Small Initiative**: 1-2 months
- **Medium Initiative**: 3-4 months
- **Large Initiative**: 5-6 months

**If longer than 6 months**: Break into smaller initiatives.

**Buffer Rules:**
- Add 20% time buffer for unknowns
- Reserve 20% capacity for bugs and support
- Plan for 70% of team's theoretical capacity

## Stakeholder Communication

**Executive Roadmap**: High-level themes and business outcomes
**Team Roadmap**: Detailed initiatives, epics, and dependencies
**Customer Roadmap**: Public-facing features and timelines (broad)
**Board Roadmap**: Strategic bets and expected business impact

**Update Cadence:**
- Executives: Quarterly with monthly check-ins
- Teams: Bi-weekly or sprint planning
- Customers: Major releases or quarterly updates
- Board: Quarterly or as needed

## Integration Points

- **Project Planner**: Converts roadmap initiatives into project plans
- **Sprint Planner**: Breaks epics into sprint work
- **OKR Tracker**: Monitors Key Results progress
- **Analytics**: Tracks metrics and validates outcomes
- **User Research**: Informs roadmap priorities with customer insights
- **GitHub Projects**: Links initiatives to code and releases
