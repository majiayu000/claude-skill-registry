---
name: manage-tech-debt
description: Track, categorize, and prioritize technical debt when the user asks to manage tech debt, create a tech debt register, assess code quality, or plan refactoring work
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Write, Grep, Bash
argument-hint: "[optional: specific area to assess or debt item to add]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: tech-debt, maintenance, quality
---

# Manage Tech Debt

## Overview

Track, categorize, and prioritize technical debt using a structured register. This is an ongoing management skill, not a one-time audit. It uses Martin Fowler's tech debt quadrant to classify debt, assigns an "interest rate" (how much the debt slows us down per sprint), estimates payoff effort, and prioritizes by impact-to-effort ratio aligned with upcoming work.

## Workflow

1. **Read existing register** -- Check for an existing tech debt register at `.chalk/docs/engineering/*_tech_debt_register.md`. If one exists, read it and use it as the starting point. The register is a living document -- update it, do not create duplicates.

2. **Read project context** -- Read `.chalk/docs/engineering/` for:
   - Architecture docs to understand system boundaries
   - ADRs and RFCs to understand intentional design choices (not all suboptimal code is debt)
   - Prior audit reports that may have flagged tech debt
   - Upcoming roadmap or sprint plans to identify strategic alignment opportunities

3. **Determine the operation** -- Based on `$ARGUMENTS` and conversation context:
   - **Add**: Add new debt items to the register
   - **Assess**: Scan the codebase for a specific area and identify debt
   - **Prioritize**: Re-rank existing items based on current context
   - **Review**: Show the current register with updated priorities
   - **Retire**: Mark items as resolved and document the resolution

4. **For new debt items -- Classify using the Tech Debt Quadrant**:

   | | Deliberate | Inadvertent |
   |---|---|---|
   | **Reckless** | "We don't have time for tests" | "What are integration tests?" |
   | **Prudent** | "We'll ship now and refactor before scaling" | "Now we know how this should have been built" |

   - **Reckless/Deliberate**: Knowingly cut corners with no plan to address it. Highest urgency.
   - **Reckless/Inadvertent**: Did not know better at the time. Needs education + fix.
   - **Prudent/Deliberate**: Intentional tradeoff with a plan. Track and execute the plan.
   - **Prudent/Inadvertent**: Learned a better approach after building. Normal and healthy.

5. **For each debt item, capture**:
   - **Category**: Architecture, Code Quality, Testing, Infrastructure, Dependencies, Documentation, Security
   - **Quadrant**: Which cell in the tech debt quadrant
   - **Description**: Concrete description of what the debt is
   - **Location**: Files, modules, or systems affected
   - **Impact (Interest Rate)**: How much this slows the team down *per sprint*, quantified:
     - Hours of extra work per sprint caused by this debt
     - Number of bugs per quarter attributable to this debt
     - Developer experience friction (onboarding time, confusion, workarounds)
   - **Payoff Effort**: Estimated effort to resolve (T-shirt size + approximate hours/days)
   - **Business Justification**: Why fixing this matters in business terms, not just engineering terms
   - **Strategic Alignment**: Does fixing this unblock or de-risk upcoming planned work?

6. **Prioritize the register** -- Rank items by:
   - **Impact/Effort ratio**: High impact, low effort items go first
   - **Strategic alignment**: Debt that blocks upcoming planned work gets a priority boost
   - **Coupling to upcoming work**: If you are already changing the affected area, fix the debt now (lowest marginal cost)
   - **Risk**: Debt that could cause incidents or data loss gets a priority boost regardless of effort

7. **Write or update the register** -- Save to `.chalk/docs/engineering/tech_debt_register.md`. If updating an existing register, preserve history (do not delete resolved items; mark them as resolved with the date).

8. **Summarize** -- Tell the user what was added/changed, the current top 5 priorities, and any items that align with upcoming work.

## Filename Convention

```
tech_debt_register.md
```

A project should have exactly one tech debt register at a fixed path (e.g., `.chalk/docs/engineering/tech_debt_register.md`). If one already exists, update it instead of creating a new one.

## Tech Debt Register Format

```markdown
# Tech Debt Register

Last updated: <YYYY-MM-DD>
Total items: <active count> active, <resolved count> resolved

## Summary

### By Category

| Category | Count | Total Interest (hrs/sprint) |
|----------|-------|-----------------------------|
| Architecture | 3 | 8 |
| Code Quality | 5 | 6 |
| Testing | 2 | 4 |
| Dependencies | 1 | 2 |

### Top 5 Priorities

| # | Item | Interest Rate | Effort | Ratio | Aligned With |
|---|------|--------------|--------|-------|-------------|
| 1 | Payment retry logic | 4 hrs/sprint | 2 days | High | Q2 billing overhaul |
| 2 | Shared validation | 3 hrs/sprint | 1 day | High | API v2 migration |
| 3 | Test database setup | 2 hrs/sprint | 3 days | Medium | — |
| 4 | Legacy auth module | 3 hrs/sprint | 5 days | Medium | Auth service RFC |
| 5 | Missing indexes | 2 hrs/sprint | 0.5 day | High | — |

## Active Debt Items

### TD-001: <Title>

- **Category**: Architecture
- **Quadrant**: Prudent / Deliberate
- **Added**: <YYYY-MM-DD>
- **Location**: `src/payments/retry.ts`, `src/payments/processor.ts`
- **Description**: Payment retry logic uses a simple loop with fixed delays instead of exponential backoff with jitter. This was acceptable at low volume but causes thundering herd problems under load.
- **Impact (Interest Rate)**: ~4 hours/sprint investigating timeout-related payment failures. 2-3 support tickets per week from merchants about failed retries.
- **Payoff Effort**: M (2 days) -- replace retry loop with a proper backoff library, add circuit breaker, update tests.
- **Business Justification**: Payment reliability directly affects merchant trust and revenue. Each failed retry costs an average of $47 in lost transaction value.
- **Strategic Alignment**: Directly relevant to Q2 billing overhaul. Fixing now reduces risk for that project.
- **Priority**: 1 (High impact/effort ratio + strategic alignment)

### TD-002: <Title>

...

## Resolved Debt Items

### TD-008: <Title> [RESOLVED <YYYY-MM-DD>]

- **Resolution**: Refactored in PR #234. Replaced manual SQL with query builder.
- **Actual effort**: 1.5 days (estimated: 2 days)
- **Outcome**: Eliminated 2 hrs/sprint of debugging SQL-related issues.
```

## Interest Rate Guidelines

The "interest rate" is the ongoing cost of *not* fixing the debt. Quantify it as concretely as possible:

| Interest Level | Hours/Sprint | Characteristics |
|---------------|-------------|-----------------|
| **Critical** | 8+ hrs | Causes incidents, blocks features, developers actively work around it every sprint |
| **High** | 4-8 hrs | Regular source of bugs, significant developer friction, slows multiple features |
| **Medium** | 2-4 hrs | Occasional bugs, noticeable friction, slows some features |
| **Low** | 0.5-2 hrs | Minor annoyance, rarely causes issues but adds up over time |
| **Negligible** | <0.5 hrs | Aesthetic concern, not worth prioritizing unless zero-cost to fix |

If you cannot estimate the interest rate, the debt is not well-understood enough to prioritize. Investigate further before adding it to the register.

## Effort Estimation

| Size | Duration | Characteristics |
|------|----------|-----------------|
| **XS** | < 2 hours | Single file change, localized, no risk |
| **S** | 0.5-1 day | Few files, well-understood, low risk |
| **M** | 1-3 days | Multiple files, needs testing, moderate risk |
| **L** | 3-5 days | Cross-module changes, needs migration, high risk |
| **XL** | 1-2 weeks | Architectural change, needs RFC or ADR, phased rollout |

## When to Address Debt

### Fix Now (do not add to register)
- Security vulnerabilities
- Data corruption risks
- Issues causing customer-visible incidents

### Fix When Touching the Area
- Debt with medium interest rate in code you are already changing
- Test gaps for code you are modifying
- Stale documentation for features you are updating

### Schedule Explicitly
- High interest rate items blocking planned work
- Items with high impact/effort ratio
- Debt that will get more expensive to fix over time (coupling is increasing)

### Accept and Document
- Low interest rate in stable code that rarely changes
- Prudent/deliberate debt where the planned payoff timeline has not arrived
- Debt where the fix effort exceeds the projected lifetime cost

## Codebase Assessment Checklist

When asked to assess a specific area for tech debt, check:

| Area | What to Look For |
|------|-----------------|
| **Architecture** | Circular dependencies, god classes/modules, missing abstraction layers, tight coupling |
| **Code Quality** | Code duplication (>3 instances), long functions (>50 lines), deep nesting (>3 levels), magic numbers |
| **Testing** | Missing tests for critical paths, brittle tests, slow test suite, no integration tests |
| **Dependencies** | Outdated packages (>2 major versions behind), packages with known CVEs, abandoned packages |
| **Infrastructure** | Manual deployment steps, missing monitoring, no alerting, single points of failure |
| **Documentation** | Outdated architecture docs, missing API docs, no onboarding guide, stale comments |
| **Security** | Hardcoded secrets, missing input validation, outdated auth patterns, no rate limiting |

## Anti-patterns

- **Infinite list with no prioritization** -- A tech debt register with 50 items and no ranking is a graveyard, not a management tool. Every item must have an interest rate and effort estimate. Rank by impact/effort ratio. If the list exceeds 20 active items, the bottom items should be evaluated for removal.
- **No business justification** -- "This code is ugly" is not a business justification. "This code causes 3 hours of debugging per sprint and has led to 2 production incidents in the last quarter" is. Every debt item must justify its existence in terms a product manager would understand.
- **"Refactor everything"** -- Not all old code is debt. Stable code that works, is tested, and rarely needs changes is *not* debt even if it uses old patterns. Debt is code that actively costs you ongoing effort. Do not confuse "not how I would write it today" with "tech debt."
- **Debt without estimated interest rate** -- If you cannot estimate how much a debt item costs per sprint, you do not understand it well enough to manage it. Investigate and quantify before adding it to the register. "It feels slow" is not a measurement.
- **One-time cleanup events** -- "Tech debt sprint" or "cleanup week" treats debt as a batch problem. Debt is continuous -- address the highest-impact items every sprint as part of regular work. Budget 15-20% of sprint capacity for debt reduction.
- **Ignoring strategic alignment** -- A medium-priority debt item that blocks an upcoming Q3 feature should be fixed now, not after Q3 launches. Always cross-reference the debt register with the product roadmap.
- **Never resolving items** -- If the register only grows and never shrinks, it loses credibility. Track resolutions, celebrate them, and measure the actual payoff vs. estimated payoff. This builds trust in the system.
- **Adding debt without a decision** -- Every new debt item should have an initial decision: fix now, fix when touching, schedule, or accept. Items without a decision sit in limbo and clutter the register.
