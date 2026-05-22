---
name: figma-atomic-design-implementation
description: Implement or refactor Figma screens in Angular using strict Atomic Design order (atoms -> molecules -> organisms -> templates -> pages), reusable component APIs, and complete companion files (.ts, .html, style, .stories.ts, .spec.ts). Use for Figma-to-code delivery, design-system normalization, component decomposition, and atomic architecture cleanup.
---

# Figma Atomic Design Implementation

## Goal

Implement Figma UI in strict Atomic Design order and produce reusable Angular components with full file completeness.

## Preconditions

- Confirm target Figma node/page scope and destination Angular feature path before editing.
- Audit existing components first to reuse safely instead of creating duplicates.
- Follow repository Angular conventions for style extension (`.css` or `.scss`) and naming.
- If required context is missing (for example node scope or target path), ask one focused question and continue.

## Required build order

Follow this exact sequence and do not skip levels:

1. Atoms
2. Molecules
3. Organisms
4. Templates
5. Pages

If a requested page is complex, still start from missing atoms first.

## Workflow

### 1) Analyze Figma scope

- Identify visual primitives and interactions from Figma node(s).
- Extract repeated UI primitives before building page-specific structures.
- Note states needed at each level (default, hover, focus, disabled, selected, loading, error where relevant).
- List candidate components by level before creating files.

### 2) Build atoms

- Create smallest independent UI units first (button, input, label, icon wrapper, badge, avatar, divider, etc.).
- Keep atom API narrow and generic.
- Do not encode page/business-specific assumptions in atoms.
- Reuse an existing atom if extension is lower risk than creating a new variant.

### 3) Build molecules

- Compose atoms into small functional groups (search field, form row, card header, menu item, etc.).
- Keep molecule inputs explicit and minimal.
- Prefer content projection or simple typed inputs over rigid one-off markup.
- Prevent molecules from directly depending on page-level services.

### 4) Build organisms

- Compose molecules into section-level structures (navbar, sidebar block, product grid section, auth form panel, etc.).
- Keep organisms layout-aware but still reusable across templates.
- Keep data and business orchestration outside visual organisms when possible.

### 5) Build templates

- Arrange organisms into page skeletons with responsive layout rules.
- Use realistic placeholder data contracts, not hardcoded business data.
- Keep templates focused on structure and slots/regions.

### 6) Build pages

- Connect templates to page-level routing/data/state.
- Keep page components thin: orchestrate data and pass view models down.
- Avoid duplicating markup that already exists in atoms/molecules/organisms.

### 7) Validate and report

- Run the quality gates below before completion.
- If a gate fails, fix it before final output.
- Report tree, files, reuse decisions, and remaining gaps using the output contract.

## Angular file completeness contract

For every component created or modified in this workflow, enforce companion files:

- `<name>.component.ts`
- `<name>.component.html`
- `<name>.component.css` (or `.scss` only when repository convention requires it)
- `<name>.component.spec.ts`
- `<name>.component.stories.ts`

If any companion file is missing, create it before considering the implementation complete.

## Reusability rules

- Use consistent, semantic, design-system-oriented naming.
- Prefer configurable inputs/outputs over duplicated variants.
- Keep styles scoped and token-aware; avoid one-off values when project tokens exist.
- Do not create page-specific atoms or molecules.
- Before creating a new component, check whether an existing reusable component can be extended safely.

## Deterministic decision rules

- New primitive visual element reused in 2+ places: create or extend an atom.
- New composition of existing atoms with local behavior only: create or extend a molecule.
- New section-level block coordinating multiple molecules: create or extend an organism.
- Page layout region changes without business orchestration changes: update template first.
- Data-loading, route wiring, or page state orchestration: update page level, not lower levels.

## Quality gates before completion

Run this checklist:

1. Atomic order preserved (atoms -> molecules -> organisms -> templates -> pages).
2. No skipped level for newly introduced UI patterns.
3. All touched components include full companion files.
4. Stories show representative states and variants.
5. Specs cover render and key behavior.
6. Markup and styles stay clean and readable.
7. Reuse audit documented for each new component.
8. No page-specific assumptions leak into atoms or molecules.

## Output contract

When reporting results, include:

1. Component tree grouped by atomic level.
2. Files created/updated for each component (`.ts`, `.html`, style, `.stories.ts`, `.spec.ts`).
3. Reuse decisions (what was reused vs newly created and why).
4. Any remaining gaps to finish full atomic coverage.
5. Which quality gates passed and which required rework.
