---
name: pmtl-ui-behavior
description: PMTL_VN interaction and accessibility discipline. Use when building or reviewing forms, navigation, dialogs, loading states, empty states, error handling, and interactive components.
---

# PMTL UI Behavior

## Purpose

Keep PMTL interactive surfaces accessible, predictable, and complete across forms, dialogs, navigation, and state feedback.

## Use When

- Building or reviewing forms, navigation, dialogs, and interactive components.
- Checking loading, empty, success, and error behavior.
- Auditing focus, keyboard flow, or validation quality.

## Required Inputs

- target route, component, or interaction flow
- affected state transitions such as loading, submit, success, empty, or error
- any relevant page or component owner doc

## Expected Output

- Interfaces that communicate state clearly and remain keyboard-usable.
- No critical interaction gaps hidden behind styling alone.

## Execution Approach

1. Map the full interaction cycle before editing UI.
2. Ensure semantic structure, focus handling, and mobile-safe controls.
3. Add explicit state feedback for submit, loading, success, empty, and error paths.
4. Verify the flow with keyboard-first behavior in mind.

## Interaction rules

- Use `:focus-visible`, not generic `:focus`.
- Keep touch targets at least `44x44px`.
- Keep mobile input font size at least `16px`.
- Prefer inline validation and direct field feedback over toast-only failures.
- Focus the first invalid field after failed submit.
- Always provide loading, empty, success, and error states for non-trivial interactive surfaces.
- Use semantic HTML for landmarks and icon-only button labels.
- Prefer keyboard-complete flows: submit on Enter, dismiss on Escape when appropriate, restore focus after dialog close.

## Form discipline

- Labels above inputs.
- Helper text optional, but structure must support it.
- Errors belong near the related control.
- Do not hide critical state changes behind motion alone.

## Verification

- Check keyboard completion: tab order, Enter submit, Escape dismiss where appropriate.
- Check focus landing after validation failure and dialog close.
- Check every non-trivial surface for loading, empty, success, and error states.

## Quality Criteria

- Interaction state is visible without guessing.
- Accessibility is built into the default flow, not bolted on later.
- Motion never becomes the only signal for a state change.

## Edge Cases

- Async forms with partial success need explicit follow-up messaging.
- Toast-only validation is not enough when the form itself can explain the issue.
- Elderly-oriented surfaces need larger targets, calmer state changes, and clearer inline instructions than default app forms.
- Deep-linked flows opened from guides or reminders still need full validation, focus, and retry behavior.

## References

- `design/ui/USER_FLOWS.md`
- `design/ui/COMPONENT_SPECS.md`
- `design/ui/ELDERLY_UX.md`
- `pmtl-fe-implementation`
- `pmtl-review-web-ui`

## Pair with

- `pmtl-fe-implementation` for code structure.
- `pmtl-ui-style-system` for visual hierarchy.
- `pmtl-review-web-ui` when reviewing an existing surface.
- Route-level page work should also read the relevant page owner docs before editing behavior.
