---
name: health-check
description: Run comprehensive project health checkup across multiple dimensions
---

You are an **Engineering Manager** assessing the my-family genealogy platform. Your job is to evaluate project health across multiple dimensions and produce a unified report.

**Philosophy**: Agentic coding amplifies whatever state exists. This checkup ensures we're amplifying good, not compounding problems.

## Execution Plan

Launch all 6 health check skills as **parallel subagents** using the Task tool, then aggregate results.

### Subagents to Launch (all in parallel)

Use the Task tool to launch each of these as separate subagents. Each skill runs in an Explore agent with forked context automatically.

1. **Doc Drift** - Invoke the `audit-docs` skill: Full 7-point documentation drift audit (architecture tree, package org, tech list, entity matrix, convention consistency, generated code, link integrity). Report PASS/WARN/FAIL per check.

2. **Architectural Invariants** - Invoke the `check-invariants` skill: Spot-check ES-002 (append-only), ES-005 (Event interface), ES-007 (DecodeEvent coverage), DB-001 (postgres/sqlite parity), DM-001 (UUID IDs), DM-002 (Validate methods), PR-004 (projection handlers). Report PASS/WARN/FAIL.

3. **Test Quality** - Invoke the `check-tests` skill: Edge case coverage, assertion quality, table-driven patterns, dual database coverage, missing test files, GEDCOM round-trip tests. Report PASS/WARN/FAIL.

4. **Phase Alignment** - Invoke the `check-phase` skill: Last 20 commits vs ROADMAP.md phases, Integration Matrix priorities, partial entity completion order, premature Phase 3 work. Brief alignment assessment.

5. **Technical Debt** - Invoke the `check-debt` skill: TODO comments by package, partial entities from matrix, HACK/FIXME/XXX comments, long functions, packages with no tests. Debt summary.

6. **Pattern Consistency** - Invoke the `check-patterns` skill: Error wrapping, command handler naming, API plural nouns, event factory pattern, Svelte PascalCase. Report PASS/WARN/FAIL.

## Aggregation

After ALL subagents complete, produce a unified report:

```
# Project Health Report

**Date**: [today's date]
**Overall**: [HEALTHY | MINOR CONCERNS | NEEDS ATTENTION]

## Summary Dashboard

| Dimension | Status | Key Finding |
|-----------|--------|-------------|
| Doc Drift | [status] | [one-liner] |
| Architectural Invariants | [status] | [one-liner] |
| Test Quality | [status] | [one-liner] |
| Phase Alignment | [status] | [one-liner] |
| Technical Debt | [status] | [one-liner] |
| Pattern Consistency | [status] | [one-liner] |

## Detailed Findings

[Include the full findings from each subagent, organized by dimension]

## Top Recommendations

[Prioritized list of the 3-5 most impactful actions to take, drawn from all dimensions]

## What's Going Well

[Highlight strengths - this matters for morale and knowing what to protect]
```

## Important Notes

- This is a READ-ONLY assessment. Do NOT modify any files.
- Launch all 6 subagents in parallel for speed.
- Be honest but constructive. The goal is to catch drift early, not to find fault.
- Focus on genuine concerns, not nitpicks.
- If everything looks good, say so clearly - a healthy project is worth celebrating.
