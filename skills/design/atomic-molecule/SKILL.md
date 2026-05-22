---
name: atomic-molecule
description: Create or refactor a React MOLECULE (a small composition of atoms). Use for input groups, labeled fields, search bars, card headers, etc. Keep molecules reusable and lightly stateful only for UI concerns.
argument-hint: "[ComponentName] [optional: brief intent]"
---

# Atomic Design: MOLECULE (React Functional Components)

You are creating a **MOLECULE**: a composition of atoms that forms a small UI pattern.

## Hard rules

1. **Functional components only**.
2. **Composition over configuration**:
   - Prefer composing atoms with children/slots.
   - Keep props focused on the pattern’s essential degrees of freedom.
3. **State scope**:
   - Local UI state is allowed only when it’s intrinsic to the widget (e.g., input focus, password visibility).
   - No remote fetching; no app-level orchestration.
4. **Accessibility**:
   - Ensure correct labeling relationships (`label` + `htmlFor`, `aria-describedby`, error messaging).
5. **Controlled/uncontrolled**:
   - Prefer controlled where it matters; if supporting both, do it intentionally and document behavior.

## Output expectations

- Provide:
  1. `Component.tsx`
  2. `Component.test.tsx` (render + key interactions + a11y-critical attributes)
  3. `Component.stories.tsx` (happy path + edge states like error/disabled)

## Recommended folder conventions

- `src/components/molecules/<ComponentName>/...`

## Molecule checklist

- [ ] Built from atoms
- [ ] Minimal and well-documented props
- [ ] Handles validation/error UI predictably
- [ ] No domain-specific coupling
