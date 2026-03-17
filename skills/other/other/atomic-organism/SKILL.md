---
name: atomic-organism
description: Create or refactor a React ORGANISM (a meaningful UI section composed of molecules/atoms). Use for nav bars, product grids, comment lists, forms, dialogs, etc. Organisms may accept data and callbacks but should remain reusable across pages.
argument-hint: "[ComponentName] [optional: brief intent]"
---

# Atomic Design: ORGANISM (React Functional Components)

You are creating an **ORGANISM**: a larger section of UI composed of molecules and atoms.

## Hard rules

1. **Functional components only**.
2. **Data boundary**:
   - Organisms can accept data via props and emit events via callbacks.
   - Avoid direct fetching inside the organism unless the project explicitly uses component-level fetching patterns (if so, isolate it and justify).
3. **Dependency discipline**:
   - Organisms may import molecules/atoms and shared utilities.
   - Avoid importing page-level modules or routing concerns.
4. **State**:
   - Local state for UI coordination is fine (open/close, selected tab).
   - Prefer lifting state up when it becomes cross-organism/page relevant.
5. **Testability**:
   - Prefer pure props-driven behavior; inject dependencies via props.
   - Use stable selectors (`role`, `labelText`) rather than brittle test IDs unless necessary.

## Output expectations

- Provide:
  1. `Component.tsx`
  2. `Component.test.tsx` (behavior-driven)
  3. `Component.stories.tsx` (mock data variants)

## Recommended folder conventions

- `src/components/organisms/<ComponentName>/...`

## Organism checklist

- [ ] Clear props contract (data in, events out)
- [ ] No routing/global singleton coupling unless standard for the repo
- [ ] Uses semantic landmarks where appropriate (`nav`, `main`, `section`, headings)
