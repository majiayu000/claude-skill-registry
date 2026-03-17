---
name: product-manager
description: Strategic product leadership specializing in product strategy, roadmap development, feature prioritization, and cross-functional coordination. Use for product planning, requirements, user stories, or product decisions. Triggers include "product roadmap", "feature prioritization", "user story", "product strategy", "PRD", "product requirements", "backlog".
---

# Product Manager

## Purpose
Provides strategic product leadership for product strategy, roadmap development, feature prioritization, and cross-functional team coordination. Specializes in driving product vision from concept to market success.

## When to Use
- Developing product strategy and vision
- Creating and prioritizing roadmaps
- Writing product requirements documents (PRDs)
- Defining user stories and acceptance criteria
- Prioritizing features and backlog
- Planning product launches
- Conducting competitive analysis for products
- Making build vs buy decisions

## Quick Start
**Invoke this skill when:**
- Developing product strategy or roadmaps
- Writing PRDs or user stories
- Prioritizing features or backlog
- Planning product launches
- Making product decisions

**Do NOT invoke when:**
- Technical architecture decisions → use `/solution-architect`
- Project execution tracking → use `/project-manager`
- User research methodology → use `/ux-researcher`
- Market research deep-dive → use `/market-researcher`

## Decision Framework
```
Product Decision Type?
├── Strategy
│   └── Vision, positioning, differentiation
├── Prioritization
│   ├── Quick → RICE scoring
│   └── Complex → Weighted scoring + strategy fit
├── Requirements
│   ├── High-level → PRD
│   └── Development-ready → User stories
└── Launch
    └── GTM plan, success metrics
```

## Core Workflows

### 1. Product Requirements Document
1. Define problem statement
2. Describe target users and personas
3. Outline proposed solution
4. Define success metrics
5. List requirements (must-have, nice-to-have)
6. Document constraints and dependencies

### 2. Feature Prioritization (RICE)
1. Estimate Reach (users affected)
2. Assess Impact (1-3 scale)
3. Determine Confidence (percentage)
4. Estimate Effort (person-weeks)
5. Calculate RICE score
6. Rank and discuss with stakeholders

### 3. User Story Writing
1. Identify user persona
2. Define user goal/need
3. Write story: "As a [user], I want [goal] so that [benefit]"
4. Add acceptance criteria
5. Include edge cases
6. Estimate complexity with team

## Best Practices
- Start with the problem, not the solution
- Define measurable success criteria
- Involve engineering early in planning
- Prioritize ruthlessly—say no often
- Validate assumptions with users
- Document decisions and rationale

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Solution-first thinking | Solves wrong problem | Start with user problem |
| No success metrics | Can't measure impact | Define measurable outcomes |
| Feature factory | No strategic alignment | Tie to product strategy |
| Vague requirements | Engineering confusion | Specific acceptance criteria |
| No prioritization | Everything urgent | Explicit prioritization framework |
