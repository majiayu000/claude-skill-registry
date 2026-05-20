---
name: create-estimation
description: Create a three-point estimation when the user asks to estimate effort, scope a feature, size work, forecast timeline, or plan capacity for a project or feature
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Write, Grep
argument-hint: "[feature or work item to estimate]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: planning, estimation, effort
---

# Create Estimation

## Overview

Create a structured three-point estimation using PERT-weighted averages. Breaks work into concrete tasks, estimates each with optimistic/likely/pessimistic bounds, identifies risk factors, and produces a total range with a recommended commitment point.

## Workflow

1. **Read project context** -- Read `.chalk/docs/` for PRDs, user stories, acceptance criteria, and architecture docs. Understanding scope and integration points is essential before estimating.

2. **Determine the next estimation number** -- List files in `.chalk/docs/engineering/` matching the pattern `*_estimation_*.md`. Find the highest number and increment by 1. If none exist, start at `1`.

3. **Understand the scope** -- From `$ARGUMENTS`, conversation context, and project docs, identify:
   - What exactly is being estimated (feature, epic, spike, migration)
   - Acceptance criteria or definition of done
   - Known integration points with existing systems
   - Whether this is greenfield or modification of existing code
   - If scope is unclear, ask the user before estimating -- estimation without scope understanding is guessing

4. **Break into tasks** -- Decompose the work into concrete, estimatable tasks. Each task should be:
   - Small enough to estimate with reasonable confidence (ideally 0.5-3 days of effort)
   - Independent enough to estimate separately
   - Inclusive of all work types: implementation, testing, code review, documentation, deployment

5. **Three-point estimate each task** -- For every task, provide:
   - **Optimistic (O)**: Best case if everything goes smoothly, no surprises, familiar territory
   - **Likely (L)**: Most probable duration given normal conditions, some minor friction
   - **Pessimistic (P)**: Worst reasonable case -- unfamiliar code, complex bugs, unclear requirements (not catastrophic, just hard)

6. **Calculate PERT estimate** -- For each task: `Expected = (O + 4L + P) / 6`. Sum all task estimates for the total.

7. **Identify risk factors** -- List specific risks that could push the estimate toward the pessimistic end. Assign each a probability (low/medium/high) and impact in time.

8. **Calculate risk buffer** -- Add a percentage buffer based on cumulative risk:
   - Well-understood work, few unknowns: 10-20% buffer
   - Some unknowns, moderate integration complexity: 20-40% buffer
   - Significant unknowns, new technology, complex integrations: 40-70% buffer

9. **Determine recommended commitment** -- The number the team should commit to externally. This is the PERT total + risk buffer, rounded to a sensible unit (half-days for small work, days for medium, weeks for large).

10. **Write the file** -- Save to `.chalk/docs/engineering/<n>_estimation_<feature_slug>.md`.

11. **Confirm** -- Tell the user the estimation was created with its path, the recommended commitment, and the confidence range.

## Filename Convention

```
<number>_estimation_<snake_case_feature>.md
```

Examples:
- `2_estimation_user_authentication.md`
- `5_estimation_payment_integration.md`
- `9_estimation_migrate_to_v2_api.md`

## Estimation Format

```markdown
# Estimation: <Feature or Work Item Title>

Last updated: <YYYY-MM-DD>

## Scope

<Brief description of what is being estimated. Link to PRD or user story if available.
State any scope boundaries explicitly: "This estimate covers X but not Y.">

## Assumptions

- <Assumption 1, e.g., "API contracts are finalized and won't change">
- <Assumption 2, e.g., "Design mockups are complete before development starts">
- <Assumption 3, e.g., "One engineer working full-time on this">

## Task Breakdown

| # | Task | Optimistic | Likely | Pessimistic | PERT Estimate |
|---|------|-----------|--------|-------------|---------------|
| 1 | <Task description> | <O> | <L> | <P> | <(O+4L+P)/6> |
| 2 | <Task description> | <O> | <L> | <P> | <(O+4L+P)/6> |
| 3 | <Task description> | <O> | <L> | <P> | <(O+4L+P)/6> |
| ... | ... | ... | ... | ... | ... |
| | **Subtotal** | **<sum O>** | **<sum L>** | **<sum P>** | **<sum PERT>** |

All values in **engineer-days** unless otherwise noted (1 engineer-day = 1 person working 1 full day).

## Commonly Forgotten Tasks

The following are included in the breakdown above. If any were intentionally excluded, note why.

- [ ] Unit and integration tests
- [ ] Error handling and edge cases
- [ ] Code review iterations (typically 1-2 rounds)
- [ ] Documentation updates (API docs, README, runbook)
- [ ] Migration scripts or data backfill
- [ ] Deployment and rollout (feature flags, staged rollout)
- [ ] Monitoring and alerting setup
- [ ] Performance testing under realistic load

## Risk Factors

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| <Specific risk> | Low / Medium / High | +<N> days | <How to reduce likelihood or impact> |
| <Specific risk> | Low / Medium / High | +<N> days | <How to reduce likelihood or impact> |

## Summary

| Metric | Value |
|--------|-------|
| **Optimistic total** | <sum of all O values> |
| **PERT total** | <sum of all PERT values> |
| **Pessimistic total** | <sum of all P values> |
| **Risk buffer** | <X%> (<rationale>) |
| **Recommended commitment** | **<PERT + buffer, rounded>** |
| **Confidence range** | <Optimistic> to <Pessimistic + buffer> |

## Recommended Commitment

**<N> engineer-days** (<approximately N/5 weeks> for a single engineer)

This is the number to communicate externally. It includes the PERT-weighted estimate plus
a <X%> risk buffer for <brief rationale>.

## Revisit Triggers

- Scope changes that add or remove acceptance criteria
- Discovery of unknown integration complexity during implementation
- Actual velocity tracking shows >20% deviation from estimates after first 30% of work
```

## Content Guidelines

### Estimation Units

Use **engineer-days** as the base unit. This measures effort, not calendar time.

- 1 engineer-day = 1 person working 1 full day
- To convert to calendar time, divide by the number of engineers and add coordination overhead (typically 10-20% per additional engineer)
- For very small tasks (< 0.5 days), use hours but convert to days in the summary

### Calibrating Optimistic vs. Pessimistic

The spread between O and P reveals confidence level:

| O:P Ratio | What It Means |
|-----------|---------------|
| 1:1.5 | Very well understood, done it before |
| 1:2 | Mostly understood, some unknowns |
| 1:3 | Significant unknowns, unfamiliar territory |
| 1:5+ | Too uncertain to estimate -- recommend a spike first |

If any single task has a ratio worse than 1:5, flag it as needing a timeboxed investigation spike before estimation is meaningful.

### Breaking Down Tasks Well

Good task breakdown follows these rules:
- Each task has a clear deliverable (not "work on X" but "implement X endpoint with validation")
- Tasks include the full cost: code + tests + review, not just the coding part
- Integration tasks are explicit, not hidden inside implementation tasks
- "Glue work" is accounted for: config changes, environment setup, CI pipeline updates

### Setting Risk Buffer

The buffer is not padding -- it is a quantified acknowledgment of uncertainty:

| Scenario | Suggested Buffer |
|----------|-----------------|
| Mature codebase, well-defined requirements, experienced team | 10-20% |
| Some new technology, requirements mostly stable | 20-40% |
| New codebase or major refactor, evolving requirements | 40-70% |
| Greenfield with unproven technology and unclear requirements | 70-100% (or recommend a spike) |

### Effort vs. Duration

Always clarify the distinction:
- **Effort**: Total engineer-days of work (what you estimate)
- **Duration**: Calendar time to complete (depends on team size, parallel work, interruptions)
- Two engineers don't halve the duration -- coordination overhead adds 10-20% per person
- Context switching between projects adds 20-30% to effective duration

## Anti-patterns

- **Single-point estimates**: "This will take 5 days" is a guess, not an estimate. Always provide the three-point range. The spread itself is valuable information about uncertainty.
- **Anchoring bias**: The first number mentioned becomes the anchor. Break into tasks first, estimate each independently, then sum. Never start with a total and work backward.
- **Not accounting for integration/testing time**: Implementation is typically 40-60% of total effort. The rest is testing, integration, review, deployment, and documentation. If your estimate only covers coding, it is 40-60% of the real number.
- **Estimating without understanding scope**: If you don't have acceptance criteria or a clear definition of done, you cannot estimate. Push back and get clarity first, or estimate the spike to get clarity.
- **Confusing effort with duration**: 10 engineer-days is not "2 weeks." It is 2 weeks for 1 engineer, but could be 1 week for 2 engineers (plus coordination overhead), or 3 weeks for 1 engineer with context switching.
- **Planning fallacy**: People consistently underestimate by 30-50%. If the team has historical data, calibrate against it. If not, lean toward the pessimistic end for commitments.
- **Precision theater**: Reporting "7.3 engineer-days" implies false precision. Round to the nearest 0.5 for small estimates, nearest whole day for medium, nearest week for large.
- **Estimating in isolation**: If the work integrates with systems owned by other teams, account for coordination time, API negotiations, and blocked-waiting time. Cross-team dependencies are the most common source of estimation misses.
