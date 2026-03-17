---
name: universal-figma-skill
description: Unified Figma-to-Angular 20 delivery workflow for implementation and refactor requests. Use when users ask to implement UI from Figma URLs or node IDs, convert Figma Make exports to Angular 20 + Tailwind v4, enforce Atomic Design decomposition, normalize feature-first folder structure, apply component companion-file rules, and bridge eligible icons to existing lucide-angular usage without adding new UI/icon libraries.
---

# Universal Figma Skill

## Goal

Run one deterministic, end-to-end workflow for Figma-driven Angular delivery without manually switching between multiple skills.

## Skill Composition

Load and apply these source skills in this order:

1. `../figma-make-guidelines/SKILL.md`
2. `../figma-make-angular20-tailwind4-implementation/SKILL.md`
3. `../figma-atomic-design-implementation/SKILL.md`
4. `../figma-lucide-angular-bridge/SKILL.md`
5. `../angular-folder-structure/SKILL.md`
6. `../angular-component-rule/SKILL.md`

If one source file is unavailable, continue with remaining sources and report the missing file.

## Required Inputs

Collect and confirm these inputs before editing:

1. Target project/workspace path.
2. Design source (Figma URL/file key/node ID, Figma Make export path, or screenshot scope).
3. Implementation scope (route, page, component, or refactor boundary).

If one required input is missing and cannot be inferred safely, ask one blocking question and stop before edits.

## Execution Order (Deterministic)

### Phase 1: Intake and baseline

1. Collect the minimum required design and project inputs.
2. Verify Angular and Tailwind versions and existing architecture quickly.
3. Infer missing non-blocking details and avoid long discovery chat.
4. Identify existing reusable components/tokens before creating new UI primitives.

### Phase 2: Guidelines and mapping

1. Generate or update `guidelines/Guidelines.md` only when the request includes Figma Make guideline creation or standardization.
2. Map Figma frames/components to Angular boundaries (route, page, template, organism, molecule, atom).
3. Plan reusable primitives before page-level implementation.

### Phase 3: Implementation

1. Implement in Atomic Design sequence: atoms, molecules, organisms, templates, pages.
2. Follow Angular 20 + Tailwind v4 project conventions and reuse existing components first.
3. Apply Lucide bridge rules: replace Lucide icon assets with `lucide-angular` only when confidently mapped and already installed.
4. Keep edits limited to scoped files and direct shared dependencies.

### Phase 4: Structure and completeness enforcement

1. Enforce feature-first folder boundaries and pages/templates/components/data-access placement.
2. Enforce Angular component companion files and structural rules for all touched components.
3. Auto-create missing companions non-destructively, including stories only when Storybook is detected.

### Phase 5: Validation and report

1. Run targeted verification (tests/typecheck/build as appropriate).
2. Report implementation paths, reuse decisions, assumptions, and verification results.
3. Report component completeness metrics and any unfixable structural violations.
4. If verification cannot run, state exactly what was unavailable and why.

## Branching Rules

1. If the user asks only for guidelines output, run only the guideline branch and stop.
2. If the user asks only for code implementation, skip guideline generation unless explicitly requested.
3. If the user asks for architecture or folder refactor, prioritize folder-structure enforcement before deep UI edits.
4. If `lucide-angular` is not installed, do not install from this skill; keep normal asset flow.
5. If design scope is ambiguous across multiple plausible targets, ask one blocking scope question before edits.

## Guardrails

1. Preserve existing project architecture unless user requests wider refactor.
2. Do not introduce new UI/icon libraries.
3. Do not overwrite existing files when enforcing component completeness.
4. Ask at most one blocking question at a time; otherwise proceed with conservative assumptions.
5. Use repository tokens/patterns over raw Figma values when they conflict; report deltas.

## Required Output Contract

Return:

1. Workflow branches executed.
2. Files created or updated with paths.
3. Atomic component tree for implemented UI (when code was changed).
4. Reuse vs new-component decisions.
5. Style and Storybook detection outcomes.
6. Verification commands run and outcomes.
7. Remaining manual follow-ups, if any.

## Success Criteria

The run is complete only when:

1. Executed branches match user scope and are listed explicitly.
2. All touched files comply with folder and companion-file rules.
3. Validation status is truthful (pass/fail/unavailable with reason).
4. Report includes assumptions, design-to-code deltas, and follow-ups.
