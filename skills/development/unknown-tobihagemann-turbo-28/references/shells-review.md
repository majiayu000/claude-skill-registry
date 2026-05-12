# Shells Review Reference

## Review Instructions

Shells review focuses on structural wiring, not broad codebase patterns. Skip sweeping project-context reads — but spot-check any concrete codebase element a shell names (function, file, type, API surface) to verify it exists and can carry the contract the shell assigns to it. A shell whose Produces or Consumes cites a nonexistent or misdescribed seam is a structural wiring bug.

## What to Review

- **Spec coverage** — The union of every shell's `Covers Spec Requirements` field must equal the full set of `R<N>` IDs in the spec's `## Requirements` section. Flag any R-id not covered by any shell. Partial coverage must be marked `R<N> (partial: <what's deferred>)` with the deferred work named in that shell's Open Questions.
- **Wiring** — Every entry in a shell's `Consumes` field must trace to a prior shell's `Produces` entry (check dependency ordering via `depends_on` frontmatter) or an explicit "from existing codebase" annotation. Flag missing prerequisites (Consumes with no source), dead ends (Produces not consumed by any later shell and not part of the final system's entry points), and implicit dependencies (Consumes tracing to a shell not in `depends_on`).
- **Cited-element accuracy** — For each external resource a shell names (file path, function, type, API surface, codebase reference, documentation link), open the cited target and verify it exists and supports the contract the shell assigns to it. Wrong citations pass spec-text review and surface later as unimplementable shells.
- **Completeness** — Walk through shells in dependency order, accumulating Produces. After the final shell, verify every spec requirement is satisfied by a reachable component. No component should be orphaned.
- **No duplication** — A bare `R<N>` claiming full coverage must appear in exactly one shell. A partial marker `R<N> (partial: <what's deferred>)` may co-occur with other partial markers for the same R-id only when the deferred slices are non-overlapping. Flag: a bare `R<N>` appearing in more than one shell; overlapping partial slices for the same R-id; a bare `R<N>` co-occurring with any partial marker for the same R-id.

## Determination Criteria

Flag an issue only when it would cause implementation problems, incorrect wiring, or spec coverage gaps. The issue must be discrete and actionable.

## Priority Levels

- **P0** — Spec requirement missing from all shells, or shell chain produces a broken system
- **P1** — Dead end, missing prerequisite, or implicit dependency that will cause implementation problems
- **P2** — Moderate issue: duplicated requirement, unclear shell boundary, or ordering improvement
- **P3** — Minor improvement

## What to Ignore

- Stylistic preferences that don't affect wiring or coverage
- Implementation details that belong in the expanded plan, not the shell
