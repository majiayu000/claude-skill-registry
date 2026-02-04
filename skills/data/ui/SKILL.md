---
name: ui
description: UI/UE (user interface & user experience) skill for designing and reviewing interfaces. Use for tasks like creating UI specs, interaction states, component guidelines, visual hierarchy, responsive layouts, accessibility, design tokens, and handoff-ready requirements for engineers.
---

# ui

Use this skill for UI/UE 设计与评审：把“体验”落到可交付的界面规范与交互细节。

## Outputs (choose what the task needs)

- Screen list + navigation map
- Wireframe-level UI spec (layout, components, spacing)
- Interaction spec (states, transitions, micro-interactions)
- Component guidelines (variants, props, usage rules)
- Design tokens (colors, typography, spacing, radii, shadows)
- Accessibility checklist (WCAG basics)
- Engineer handoff notes (assets, copy, edge cases)

## Workflow

1) Clarify context
- Platform: Web / mobile / mini program.
- Users and primary tasks; define success for the screen.

2) Define information hierarchy
- What is primary CTA? What must be seen first?
- Use progressive disclosure for secondary actions.

3) Specify layouts and components
- Grid system / spacing rules.
- Component inventory and reuse plan.
- Responsive behavior (breakpoints) where relevant.

4) Define states (must-have)
- Empty / loading / error / success
- Disabled / hover / focus / pressed
- Validation states for forms

5) Interaction details
- Feedback timing, confirmations, undo patterns.
- Prevent errors; provide clear recovery paths.

6) Visual design consistency
- Tokenize: colors, typography scale, spacing, radii.
- Ensure contrast and readable typography.

7) Accessibility
- Keyboard navigation, focus order, ARIA labels (web).
- Dynamic type and screen reader labels (mobile).

## UI acceptance criteria template

- Given [state], when [action], then [UI updates] within [time].
- Copy: [exact text], error message: [exact text].
- Responsive: at [breakpoint], [layout change].
- Accessibility: [tab order], [label], [contrast].

