---
name: design
description: Design a feature or change into a reviewed ADR. Outputs an accepted decision record ready for /scope.
---

# Design

Produce an Architecture Decision Record (ADR) for a feature or change. Read AGENTS.md if not in context.

## Inputs

Design question or topic. Timebox if relevant.

## Review-aware

Before starting: check if `<artifact>.findings.md` exists for this topic. If it does, read it and incorporate findings before proceeding.

## Workflow

1. **GitHub state check** — Run `gh issue list` and `gh pr list` to avoid proposing already-built or conflicting work.

2. **Shape options** — Produce 1 recommended option (+ 1 alternative max). Include: pros/cons, risks, dependencies, success validation.

3. **Draft ADR** — Write to `.aide/docs/decisions/YYYY-MM-DD-<slug>.md` (AIDE framework decisions) or `docs/decisions/YYYY-MM-DD-<slug>.md` (game/project decisions). Status: `Draft`.

4. **Cross-review** — Use `/findings` to exchange findings before accepting. Do not accept unreviewed ADRs.

5. **Accept** — Set status to `Accepted`. Hand off to `/scope` to decompose into GitHub issues.

## ADR format

```
# Title
Status: Draft | Accepted | Superseded
## Context
## Decision
## Rationale
## Consequences
```

## Reference

- Design pillars: `design/` directory
- Quick reference: `docs/DESIGN_QUICK_REFERENCE.md`
