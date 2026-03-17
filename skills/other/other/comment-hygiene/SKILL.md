---
name: comment-hygiene
description: "Use when comment quality, placement, or density affects code readability and maintainability. Goal: comments improve readability by staying necessary, precise, and correctly attached to nearby code."
---

# Comment Hygiene

## Response Contract

- Deliverable: apply the requested changes to the target artifact.
- Chat output: no additional output beyond the deliverable.

## Skill Model

This model classifies what can be commented. It does not imply quality.

### Comment Attachment Sites

- **Surface**
  Public entry points and externally visible surfaces.

- **Data**
  Data shapes and schemas.

- **Rule**
  Rule-bearing logic and decision points.

- **External**
  External coupling and external constraints.

## Standards

Each standard is defined once here and referenced elsewhere by its ID.

- **site.assign — Assign a site**
  Every comment must be assignable to exactly one attachment site: Surface, Data, Rule, or External.

- **site.focus.surface — Surface focus**
  Surface comments cover externally visible meaning and caller-facing constraints.

- **site.focus.data — Data focus**
  Data comments cover representation meaning and structural constraints.

- **site.focus.rule — Rule focus**
  Rule comments cover rule intent and rule boundaries.

- **site.focus.external — External focus**
  External comments cover external assumptions and external constraints.

- **site.closest — Place at the closest site**
  Place the comment at the closest location where a reader needs it for the assigned site and focus.

- **comment.no_narration — No narration**
  Remove comments that restate adjacent code or narrate straightforward steps.

- **comment.nonoverlap — No overlap**
  Avoid multiple comments that cover the same point. If one note spans multiple sites, split it so each comment has one site and one focus.

- **comment.precise — Precise and scoped**
  Use specific terms and explicit conditions. Keep scope bounded to what the assigned site and focus need.

- **comment.stable — Prefer stable content**
  Prefer describing intent, constraints, and externally relevant meaning over volatile implementation detail.

## Workflow

1. Enumerate existing comments and planned comments.
2. Assign each comment to exactly one attachment site and confirm it matches the site focus. Apply `site.assign` and `site.focus.*`.
3. Delete narration and restatement. Apply `comment.no_narration`.
4. De-duplicate overlapping points. Apply `comment.nonoverlap`.
5. Relocate comments to the closest location where readers need them. Apply `site.closest`.
6. Rewrite remaining comments to be specific and bounded. Apply `comment.precise`.
7. Prefer stable content over volatile detail. Apply `comment.stable`.
8. Run acceptance checks.

## Acceptance Criteria

A revision is complete only if all checks pass.

- **Response**: Output satisfies the Response Contract.
- **Standards satisfied**: `site.assign`, `site.focus.*`, `site.closest`, `comment.no_narration`, `comment.nonoverlap`, `comment.precise`, `comment.stable`.
