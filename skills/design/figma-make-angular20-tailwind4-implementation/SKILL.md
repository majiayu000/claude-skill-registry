---
name: figma-make-angular20-tailwind4-implementation
description: Implement or refactor UI from Figma Make exports into Angular 20 + Tailwind CSS v4 with direct repository edits, deterministic fallback behavior, and strict reuse of existing project structure, design tokens, and shared components. Use when users ask to implement Figma Make screens, convert Figma Make export code into Angular, update a route/component from Figma URL or node targets, or apply screenshot-driven UI changes immediately (not planning-only advice).
---

# Figma Make Angular 20 Tailwind v4 Implementation

## Goal

Implement requested design changes by combining:

- exported/generated Figma Make project code,
- design information from Figma (nodes, spacing, typography, variants, states),
- existing Angular 20 + Tailwind v4 project conventions.

Do not run long discovery chat. Ask only the minimum blocking question needed to proceed.

## Minimal Input Contract

Accept these inputs when provided:

- `project_root`: path to the Angular project.
- `figma_make_base`: exported Figma Make project path or existing base implementation path.
- `figma_make_corpus_root` (optional): folder containing multiple Figma Make export projects used as support examples.
- `design_source`: Figma URL/node context, Figma Make context, screenshot, or written UI brief.
- `target_scope`: exact page, route, or component to implement.
- `base_reference` (optional): existing route/component to mirror for patterns.
- `constraints` (optional): library/version restrictions, accessibility requirements, deadline scope.

Input fallback policy:
- If one non-critical input is missing, infer from repository context and continue.
- Ask one blocking question only when path resolution, version compatibility, or target scope is unclear enough to block safe edits.
- Path resolution order for missing/invalid paths:
  1. user-provided absolute path,
  2. workspace-relative equivalent,
  3. closest matching existing repository path by name.
- If no safe path can be resolved after the ordered fallback, stop and ask one blocking question.

## Workflow

### 0) Build corpus baseline when multiple exports are provided

- If `figma_make_corpus_root` exists and `scripts/extract_figma_make_exports.ps1` exists, run:
  - `scripts/extract_figma_make_exports.ps1 -RootPath "<figma_make_corpus_root>" -OutputPath "<project_root>/figma-make-export-analysis.md"`
- If the script does not exist, create `<project_root>/figma-make-export-analysis.md` manually by scanning export apps and documenting:
  - stable shared patterns,
  - project-specific deltas,
  - conversion risks.
- Read `references/figma-make-export-baseline.md` for baseline extraction heuristics.
- Treat corpus projects as examples, not mandatory architecture. Reuse only the patterns that fit the current target Angular project.
- Keep generated corpus reports as runtime artifacts; regenerate per corpus instead of relying on stale sample analysis.

### 1) Verify stack and base quickly

- Read project config first (`angular.json`, `package.json`, workspace settings, global styles).
- Confirm `@angular/core` major version is `20`.
- Confirm `tailwindcss` major version is `4`.
- Identify standalone/component architecture, routing shape, shared UI primitives, and token sources.
- If `base_reference` is provided, treat it as the primary pattern source.
- Record the selected pattern source in working notes so reuse decisions remain consistent for the full pass.

Blocking policy:
- If Angular 20 or Tailwind v4 is not present, ask one blocking compatibility question before making compatibility changes.
- If required project paths do not exist, state the missing path once and continue with the closest valid repository path.

### 2) Map Figma inputs to Angular targets

- Map Figma page/frame/component intent to Angular route/component boundaries.
- Translate Figma spacing/typography/color/state details to existing token and utility patterns.
- Derive responsive behavior from Figma Auto Layout and constraints.

### 3) Implement with Angular-first patterns

- Reuse existing layout, spacing, typography, and state patterns.
- Prefer extending existing components over creating duplicates.
- Convert base/export patterns into Angular templates and component APIs.
- Use Angular control flow (`@if`, `@for`, `@switch`) when conditional/list rendering is needed.
- Keep logic in `.ts`, structure in `.html`, and presentation mainly in Tailwind utility classes.
- Create new components only when no suitable base exists.
- Keep component companion files complete for any new component (`.ts`, `.html`, style file, and test/story files when the target project uses them).
- Avoid touching unrelated routes/features unless required by shared-component dependency updates.

### 4) Apply Tailwind v4 implementation rules

- Prefer utility classes in templates over ad-hoc CSS.
- Reuse existing CSS variable tokens and theme layers before adding new values.
- Use the Tailwind v4 CSS-first approach (`@import "tailwindcss";`) unless the project is intentionally pinned to a legacy bridge.

### 5) Implement in a single execution pass

- Make direct code changes for the requested scope instead of running a planning-only response.
- Keep naming, file structure, and component contracts consistent with the project.
- If design details are ambiguous, choose a conservative assumption and continue.
- Document assumptions briefly in the final response.

### 6) Verify behavior and integration

- Run the narrowest useful checks first:
  - targeted tests for touched components/features,
  - workspace typecheck/lint if available,
  - production or dev build only when needed for confidence.
- Required minimum verification:
  - run at least one targeted check for touched scope, and
  - run one integration check (`build`, `typecheck`, or `lint`) when available in project scripts.
- Confirm no obvious regressions in shared components touched by the change.
- Report exactly what was validated and what was not run.
- If validation fails, report the exact command, failure surface, and most likely regression area.

## Iterative Support Cycle

Use this cycle whenever corpus exports are available:

1. Extract
- Produce/update a support report from the export corpus.
- Keep findings concrete: route shape, component families, theme tokens, and state/data patterns.

2. Select
- Pick one reference project that is closest to `target_scope`.
- Keep other projects as secondary fallback for missing patterns.

3. Map
- Map selected export patterns to Angular equivalents before coding:
  - component boundaries,
  - route boundaries,
  - token and theme usage,
  - interaction states.

4. Implement
- Build one vertical slice first (route or major component).
- Reuse existing Angular shared components and Tailwind utilities.

5. Validate and promote
- Verify behavior, then promote repeated mapping rules into reusable project patterns.
- Reuse these promoted patterns in the next iteration.

## Conversation Policy

- Avoid full interview mode.
- Ask at most one concise blocking question at a time.
- Prefer making reasonable assumptions over pausing repeatedly.
- Keep user-facing updates short and implementation-focused.
- If required tools/paths are missing, state the gap in one sentence and continue with the closest deterministic fallback.
- Keep status updates execution-focused and short: current step, next action, and blockers only.

## Output Contract

Return:

1. What was implemented and where (file paths).
2. What base patterns/components were reused.
3. Any assumptions made due to missing design details.
4. What verification commands were run and their outcomes.
5. Any unresolved blockers or validation gaps.

## Guardrails

- Do not rewrite project architecture unless explicitly requested.
- Do not introduce a new UI library when the base project already has one.
- Do not replace broad styling systems for a small feature request.
- Do not fabricate design-token values when repository values already exist.
- Preserve accessibility semantics (`label`, keyboard focus, contrast-aware states).
- When Figma details conflict with established project patterns, follow project patterns and note the delta.
- Do not claim a command was run when it was skipped or unavailable.
- Do not mass-reformat or rename unrelated files as part of UI implementation work.
