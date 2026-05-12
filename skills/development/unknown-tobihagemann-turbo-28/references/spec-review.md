# Spec Review Reference

## Review Instructions

Read project context (CLAUDE.md and any existing codebase) to understand constraints. For any concrete codebase claim the spec makes (named functions, file locations, API shapes, data-flow assertions), open the cited file and verify it. Wrong factual claims about current code pass text-only review and surface later as unimplementable plans.

## What to Review

- **Structural completeness** — Spec has the mandatory sections `## Overview`, `## Requirements`, and `## Design`. Requirements uses contiguous `R<N>` IDs starting at `R1` with no gaps or duplicates, including across subheadings when requirements are grouped. Every Design element traces to at least one requirement.
- **Completeness** — Missing requirements, undefined behavior, TODOs, placeholder text, or "TBD" markers that would block planning
- **Consistency** — Internal contradictions between sections (e.g., data model conflicts with API design, feature list conflicts with MVP scope)
- **Clarity** — Ambiguous requirements that could lead to misinterpretation during implementation
- **Codebase accuracy** — Concrete claims the spec makes about current code (named functions, file paths, type shapes, module boundaries, existing API surfaces) must match what is in the repo. Spot-check by opening the cited files. Flag wrong citations, misdescribed seams, and nonexistent-but-assumed APIs — these mislead planning the most.
- **Scope** — Spec focuses on a coherent system. No unconnected components or features that serve no specified consumer
- **YAGNI** — Unrequested features, over-engineering, or premature abstractions that add complexity without clear value
- **Design Direction** — Whether the proposed system design is the simplest safe option. Challenge assumptions about users, environment, or dependencies and flag when a different approach would be safer or simpler
- **Failure Modes** — Scenarios the spec does not account for: partial failure, race conditions, stale state, rollback, data loss, and degraded dependencies

## Determination Criteria

Flag an issue only when ALL of these hold:

1. It would cause problems during implementation planning or lead to building the wrong thing
2. The issue is discrete and actionable (not a vague concern or general suggestion)
3. The author would likely fix the issue if made aware of it
4. The issue is clearly not an intentional design choice, OR it challenges a design choice with evidence of concrete failure modes or a simpler alternative

## Priority Levels

- **P0** — Spec is fundamentally flawed. Missing core requirement or internal contradiction that blocks planning
- **P1** — Significant gap that will likely cause planning or implementation problems
- **P2** — Moderate issue that should be addressed before planning
- **P3** — Minor improvement

## What to Ignore

- Wording, stylistic, or cosmetic preferences that don't affect clarity
- Alternative architectural approaches without evidence of concrete advantages over the chosen one
- Suggestions that add complexity without clear planning value
