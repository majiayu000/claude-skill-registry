---
name: skill-editor
description: "Use when a skill specification needs drafting, revision, or review to improve routing precision and execution coherence. Goal: skill specifications are routable from frontmatter and internally coherent without redundant guidance."
---

# Skill Editor

Draft, revise, or review an agent skill specification to improve routing precision and execution usability.

## Response Contract

- Deliverable: apply the requested changes to the target artifact.
- Chat output: no additional output beyond the deliverable.

## Skill Model

Definitions used to reason about skill specifications and edits.

### Semantic Layers

A skill specification has two semantic layers.

- **Frontmatter**
  Routing description. It expresses when the skill should be selected.

- **Body**
  Execution description. It expresses how to perform the task once selected.

## Editing Standards

Apply these standards throughout the edit. Each standard is single-sourced here and referenced elsewhere by its ID.

- **layers.no_overlap — Separate routing and execution**
  Keep routing description in frontmatter and execution description in the body. Do not duplicate the same guidance across layers.

- **routing.alone — Frontmatter routes alone**
  Frontmatter must be sufficient for correct selection without reading the body. Use user-intent phrasing and common request language for the intended task family.

- **routing.boundary — Constrain routing**
  Frontmatter must not claim general capabilities beyond the intended task family. Remove wording that would cause overreach or overlap with nearby skills.

- **body.responsibilities — Organize the body by responsibility**
  Structure the body into responsibility-based sections so each rule has a stable home and boundaries are clear.

- **rules.single_source — Single-source rules and definitions**
  Each rule and definition appears once. Merge overlaps, remove restatement, and avoid parallel formulations.

- **examples.minimal — Examples only for disambiguation**
  Use examples only to resolve ambiguity. Keep them minimal and neutral, and do not introduce conventions through examples.

## Workflow

1. Rewrite frontmatter so it routes correctly on its own. Apply `routing.alone`, `routing.boundary`.
2. Restructure the body into responsibility-based sections and relocate content into its responsible home. Apply `body.responsibilities`.
3. Remove layer overlap by moving routing language out of the body and moving execution guidance out of frontmatter. Apply `layers.no_overlap`.
4. De-duplicate and consolidate rules and definitions until each appears once. Apply `rules.single_source`.
5. Add or trim examples strictly to resolve ambiguity. Apply `examples.minimal`.
6. Run acceptance checks.

## Acceptance Criteria

A revision is complete only if all checks pass.

- **Response**: Output satisfies the Response Contract.
- **Standards satisfied**: `layers.no_overlap`, `routing.alone`, `routing.boundary`, `body.responsibilities`, `rules.single_source`, `examples.minimal`.
