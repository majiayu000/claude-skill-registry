---
name: ue
description: UE (user experience engineering) skill for defining end-to-end user experience behavior and interaction logic. Use for tasks like flow design, interaction models, state machines, error recovery, input validation, usability heuristics, accessibility, and turning UX intent into testable acceptance criteria for implementation.
---

# ue

Use this skill for UE（User Experience Engineering / 体验工程）工作：把体验目标落地为“可实现 + 可测试”的交互与状态规范。

## Outputs (choose what the task needs)

- End-to-end flows (happy path + edge cases)
- Interaction/state spec (state machine)
- Error handling & recovery spec
- Form validation rules (client/server responsibilities)
- Accessibility and inclusive UX requirements
- Testable acceptance criteria (Given/When/Then)

## Workflow

1) Define the experience goal
- What user problem are we solving in this flow?
- What does success look like (time to complete, error rate, satisfaction)?

2) Model the flow as states
- Enumerate states: idle → input → validating → loading → success/error.
- Include empty/loading/offline/permission denied/timeouts.
- Define transitions, triggers, and side effects.

3) Specify interactions
- Primary/secondary actions per state.
- Feedback timing: spinners, skeletons, toasts, confirmations.
- Undo/cancel patterns where applicable.

4) Validation & constraints
- Field rules (length, format, enum) and error messages (exact copy).
- Decide what is validated client-side vs server-side.
- Idempotency and retry rules for network actions.

5) Error taxonomy & recovery
- User mistakes vs system errors vs dependency failures.
- Recovery path: retry, fallback, save draft, contact support.
- Avoid dead ends; preserve user input when possible.

6) Accessibility
- Keyboard navigation/focus order (web).
- Screen reader labels and dynamic text (mobile).
- Do not rely on color alone for status.

## UE acceptance criteria template

- Given [state], when [event], then [transition] and [UI result].
- When network timeout occurs, system [behavior] and user can [recovery].
- Validation: for [invalid input], show [message] and prevent [action].

