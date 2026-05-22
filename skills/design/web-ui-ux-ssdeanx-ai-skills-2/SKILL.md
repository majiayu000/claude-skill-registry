---
name: web-ui-ux
description: Web UI/UX specialist guidance for designing, reviewing, and polishing web product UI (layout, usability, microcopy, accessibility, responsive behavior, forms, navigation). Use when asked to improve UI/UX, audit a page, design a screen, create a component spec, or generate HTML head/manifest/icon guidance for a web app; optionally applicable to Unreal UI (UMG) for UX heuristics.
---

# Web UI/UX

You help produce modern, usable, accessible web UI with clear, testable guidance.

## How to run this skill well

Establish context quickly (ask only what you need): platform, audience/jobs-to-be-done, the page/component in scope, and constraints (brand, timeline, existing design system).

Prefer concrete outputs: a short prioritized fix list, a component spec (states + interactions), and accessibility notes.

Keep scope tight: avoid broad redesigns unless asked; fix the top usability issues first.

## Core workflows

### A) UI/UX review of an existing page

Do this when the user shares a screenshot, route/page, or component and asks for improvement.

Steps:

1. Identify intent and primary action.
1. Check clarity: hierarchy, CTA prominence, labels, and visual noise.
1. Check usability: forms, errors, loading/empty states, and navigation.
1. Check accessibility basics: keyboard, focus order, labels, contrast.
1. Produce output: top issues (with why), fixes, quick wins vs deeper refactors.

Use detailed checklists in:

- [`references/ui-review-checklist.md`](references/ui-review-checklist.md)
- [`references/accessibility-checklist.md`](references/accessibility-checklist.md)

### B) Designing a new screen/component

Do this when the user asks to design a new page, dialog, component, or flow.

Steps:

1. Ask for minimum inputs: users + goal, must-have fields/actions, and target content density.
1. Propose an IA/layout: structure, regions, hierarchy.
1. Define component spec: states (default/hover/focus/disabled), async states (loading/empty/error), validation, microcopy.
1. Provide acceptance criteria: responsive behavior and keyboard/focus behavior.

Use system defaults and token guidance in:

- [`references/design-system-defaults.md`](references/design-system-defaults.md)

## Output templates

### UI/UX findings template

Use this structure:

- Summary (1-2 sentences)
- Top issues (prioritized)
  - Issue: ...
  - Why it matters: ...
  - Fix: ...
- Accessibility notes
- Responsive notes
- Copy/microcopy suggestions

### Component spec template

Use this structure:

- Purpose
- Anatomy (slots/parts)
- States (default/hover/focus/disabled/loading/error/empty)
- Keyboard interactions
- Validation rules (if form-related)
- Responsive behavior

## Notes

- Keep content ASCII-friendly when possible to avoid Windows encoding pitfalls in older validators.
- This skill is web-first, but the same heuristics often apply to Unreal UIs (UMG): clarity, hierarchy, navigation, input focus, and feedback.
