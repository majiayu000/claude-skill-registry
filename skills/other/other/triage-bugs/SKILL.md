---
name: triage-bugs
description: Triage and prioritize bug reports when the user asks to classify bugs, prioritize a bug backlog, triage issues, or sort bugs by severity for sprint planning
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[bug list, issue tracker query, or sprint name]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: bugs, triage, prioritization
---

# Triage Bugs

## Overview

Classify and prioritize a batch of bug reports using a consistent severity matrix and priority framework. The output is a structured, actionable bug triage that enables sprint planning, on-call prioritization, and resource allocation decisions.

## Workflow

1. **Read project context** — Check `.chalk/docs/` for:
   - Architecture docs (to map bugs to components)
   - Previous triage reports for consistency
   - Team structure or component ownership docs
   - Any existing severity definitions the team uses

2. **Gather bug reports** — From `$ARGUMENTS` and conversation context:
   - If a list of bugs is provided in conversation, use those
   - If a file or document is referenced, read it
   - If pointed to an issue tracker, read available bug details
   - For each bug, extract: title, description, reproduction steps, environment, reporter, date reported

3. **Check reproduction status** — For each bug, determine:
   - **Reproduced**: Steps provided and confirmed working
   - **Partially reproduced**: Steps provided but inconsistent results
   - **Not reproduced**: No reproduction steps or unable to reproduce
   - **Not attempted**: Reproduction has not been tried yet
   - Bugs without reproduction status should be flagged — triaging unreproduced bugs is guesswork

4. **Assign severity** — Using the severity matrix below, classify each bug:
   - **Critical (SEV-1)**: Data loss, security vulnerability, complete feature outage for all users
   - **High (SEV-2)**: Major feature broken with no workaround, significant data corruption risk, affects majority of users
   - **Medium (SEV-3)**: Feature broken but workaround exists, affects subset of users, degraded experience
   - **Low (SEV-4)**: Cosmetic issue, minor inconvenience, affects edge case usage, has easy workaround

5. **Calculate priority** — Priority combines severity with business context:
   - **User Impact**: How many users are affected? (all, most, some, few)
   - **Frequency**: How often does it occur? (every time, often, sometimes, rarely)
   - **Workaround**: Is there a workaround? (none, difficult, easy)
   - Priority = Severity adjusted by impact, frequency, and workaround availability
   - A medium-severity bug that hits every user with no workaround may be higher priority than a high-severity bug that affects 1% of users rarely

6. **Map to components** — For each bug:
   - Identify the affected system component or module
   - Suggest the owning team or area of expertise
   - Note if the bug crosses component boundaries (these are often harder to fix)

7. **Estimate effort** — Provide a rough effort estimate:
   - **Small**: Likely a straightforward fix, isolated change, low risk (< 1 day)
   - **Medium**: Requires investigation, touches multiple files, moderate risk (1-3 days)
   - **Large**: Requires significant investigation or architectural change, high risk (3+ days)
   - **Unknown**: Cannot estimate without further investigation

8. **Group the results** — Present the triaged bugs grouped by:
   - Primary grouping: Severity (Critical first)
   - Secondary grouping: Component
   - Also provide a sprint fitness view: which bugs should go in the next sprint based on priority and effort

9. **Determine the next file number** — List files in `.chalk/docs/engineering/` matching `*_bug_triage*`. Find the highest number and increment by 1.

10. **Write the report** — Save to `.chalk/docs/engineering/<n>_bug_triage_<sprint_or_date>.md` if requested, or present in conversation.

11. **Confirm** — Summarize: total bugs triaged, severity distribution, top 3 priority items, and any bugs that need more information before they can be properly triaged.

## Filename Convention

```
<number>_bug_triage_<sprint_or_date>.md
```

Examples:
- `8_bug_triage_sprint_14.md`
- `10_bug_triage_2024_q4.md`

## Bug Triage Format

```markdown
# Bug Triage Report

Last updated: <YYYY-MM-DD>
Sprint/Period: <sprint name or date range>
Triaged by: <agent or person>

## Summary

| Severity | Count | Action |
|----------|-------|--------|
| Critical (SEV-1) | <n> | Fix immediately |
| High (SEV-2) | <n> | Fix this sprint |
| Medium (SEV-3) | <n> | Schedule for next sprint |
| Low (SEV-4) | <n> | Backlog |
| **Total** | **<n>** | |

| Reproduction Status | Count |
|-------------------|-------|
| Reproduced | <n> |
| Partially reproduced | <n> |
| Not reproduced | <n> |
| Not attempted | <n> |

## Critical (SEV-1)

### BUG-<id>: <Title>

| Field | Value |
|-------|-------|
| Severity | Critical |
| Priority | P0 |
| Component | <component> |
| Suggested Owner | <team or area> |
| Reproduction | Reproduced / Not reproduced |
| User Impact | All users / Most users |
| Frequency | Every time / Often |
| Workaround | None |
| Effort | Small / Medium / Large / Unknown |

**Description**: <1-2 sentence summary>
**Impact**: <What happens to users when this bug occurs>
**Recommendation**: <Fix immediately. Suggested approach if known.>

## High (SEV-2)

### BUG-<id>: <Title>

| Field | Value |
|-------|-------|
| ... | ... |

## Medium (SEV-3)

| Bug ID | Title | Component | Priority | Effort | Workaround |
|--------|-------|-----------|----------|--------|------------|
| BUG-<id> | <title> | <component> | P2 | Medium | <workaround summary> |

## Low (SEV-4)

| Bug ID | Title | Component | Priority | Effort |
|--------|-------|-----------|----------|--------|
| BUG-<id> | <title> | <component> | P3 | Small |

## By Component

| Component | Critical | High | Medium | Low | Total |
|-----------|----------|------|--------|-----|-------|
| <component> | <n> | <n> | <n> | <n> | <n> |

## Sprint Fitness

### Recommended for This Sprint
<Bugs that are high priority AND small/medium effort>

| Bug ID | Title | Severity | Effort | Rationale |
|--------|-------|----------|--------|-----------|
| BUG-<id> | <title> | Critical | Small | Data loss risk, quick fix |

### Needs More Information
<Bugs that cannot be properly prioritized without additional data>

| Bug ID | Title | What is Missing |
|--------|-------|-----------------|
| BUG-<id> | <title> | No reproduction steps |
```

## Severity Matrix

| Severity | Data Impact | Feature Impact | User Scope | Examples |
|----------|------------|----------------|------------|----------|
| Critical | Data loss or corruption | Complete outage | All users | Payment processing fails, user data deleted, auth bypass |
| High | Data integrity risk | Major feature broken, no workaround | Most users | Cannot save documents, search returns wrong results |
| Medium | No data impact | Feature degraded, workaround exists | Some users | Slow page load, filter does not work but manual sort does |
| Low | None | Cosmetic or minor | Few users | Misaligned button, typo in error message, tooltip missing |

## Priority Calculation

Priority is not the same as severity. Priority determines when to fix it.

| | No Workaround | Difficult Workaround | Easy Workaround |
|---|---|---|---|
| **All/Most Users, Frequent** | P0 — Drop everything | P1 — Fix this sprint | P1 — Fix this sprint |
| **All/Most Users, Rare** | P1 — Fix this sprint | P2 — Next sprint | P2 — Next sprint |
| **Some/Few Users, Frequent** | P1 — Fix this sprint | P2 — Next sprint | P3 — Backlog |
| **Some/Few Users, Rare** | P2 — Next sprint | P3 — Backlog | P3 — Backlog |

A Critical severity bug is always P0 regardless of this matrix.

## Anti-patterns

- **All bugs marked critical** — If everything is critical, nothing is. A cosmetic alignment issue is not the same severity as data loss. Use the severity matrix honestly. Teams that over-classify lose the ability to distinguish real emergencies.
- **No severity definition** — Triaging without a shared severity matrix produces inconsistent results. Different people will classify the same bug differently. Always apply the defined matrix, not gut feeling.
- **Triaging without reproduction status** — A bug that cannot be reproduced cannot be reliably fixed or estimated. Flag unreproduced bugs and require reproduction before assigning them to a sprint. Guessing at severity for unreproduced bugs leads to wasted effort.
- **Ignoring frequency and user impact** — Severity alone does not determine priority. A high-severity bug that affects 0.01% of users once a month is lower priority than a medium-severity bug that hits every user daily.
- **Not grouping by component** — A triage report that is just a flat list does not help with assignment. Group by component so team leads can see their scope at a glance.
- **Triaging in isolation** — Bugs often cluster around the same root cause. Before marking 5 bugs as separate items, check whether they share a common component or trigger. Fixing the root cause may resolve multiple bugs.
- **No effort estimation** — Priority without effort context makes sprint planning impossible. A P1 bug that takes 2 weeks to fix needs different planning than a P1 bug that takes 2 hours.
- **Stale triage** — A triage report from 3 sprints ago is misleading. Bugs get fixed, new ones arrive, priorities shift. Re-triage regularly or mark the report with an expiration context.
