---
name: judge
description: Use when the user wants an independent expert review of work done in this conversation before accepting or extending it.
argument-hint: "[description of what to review, or omit for recent work]"
---

subject = $ARGUMENTS

If no subject provided, review the most recent substantive work in this conversation. Identify it from context and confirm with the user before spawning.

If the subject references a file path or folder, read enough to understand full scope before dispatching.

## Purpose

You are the courtroom coordinator, not the judge. The judges are independent teammates with clean context windows who haven't watched you build the thing — that independence is the entire value. Your implementation context is bias; their fresh eyes are the asset.

## Scope

This is not `/qual` (code correctness). This is not `/razor` (should it exist). This is: **given that we're building this thing, did we build it the way an expert would?**

Dimensions: approach selection, architecture fitness, idiom correctness, trade-off awareness, missed alternatives, domain-standard solutions, proportionality of solution to problem.

## Teammates

Spawn from `${CLAUDE_SKILL_DIR}/agents/`. All teammates are **read-only** — analysis only, no edits.

| Teammate | Agent file | Lens |
|----------|-----------|------|
| Domain Expert | `domain-expert.md` | Would a senior specialist in this exact domain do it this way? |
| Pragmatist | `pragmatist.md` | Is this the most direct path to the goal? |
| Alt-Path | `alt-path.md` | What fundamentally different approaches exist that we didn't consider? |

Spawn all three in parallel. Each gets:
- The subject description
- All relevant file paths / code / context
- The project's stack and conventions (detect from codebase)

## Synthesis

### Credibility Filter

LLM reviewers reliably produce "sounds expert" observations that don't survive scrutiny. Every finding must pass all four criteria — without this filter, the report will be 40%+ noise:

1. **Substantiated** — references specific code, decisions, or patterns. "Generally speaking" observations get discarded.
2. **Actionable** — proposes a concrete alternative, not just criticism.
3. **Trade-off honest** — the alternative has costs too. State them.
4. **Calibrated** — distinguish "this is wrong" from "this is one valid approach but here's another" from "this is fine, minor style preference." Overclaiming kills trust and is the single most common failure mode of this skill.

Discard style preferences disguised as expertise. Discard findings where the teammate clearly misunderstood the constraints.

### Convergence Signal

When 2+ teammates independently flag the same concern, elevate it — independent convergence is strong signal. When teammates contradict each other, present both positions with reasoning; don't pick a winner.

### Verdict Scale

| Verdict | Meaning |
|---------|---------|
| **EXPERT-GRADE** | A domain expert would recognize this as their own work. Teammates found style nits at most. |
| **SOLID** | Sound approach. Real improvements found but no fundamental issues. |
| **RETHINK** | Functional but an expert would take a meaningfully different approach. |
| **RED FLAG** | Fundamental approach issue. Specific alternative(s) strongly recommended. |

### Report

1. **Verdict** — one word + one sentence justification
2. **What's strong** — what teammates validated. Pure criticism is dishonest when things were done well, and the user will distrust a report that only finds fault.
3. **Findings** — grouped by importance. Each: concern, evidence, proposed alternative, trade-off of alternative, source teammate(s)
4. **If we could start over** — the single highest-leverage change, if any

**Stop after the report. Do not implement changes unless asked.**
