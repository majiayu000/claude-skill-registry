---
name: atomic-atom
description: Create or refactor a React ATOM component (smallest reusable UI primitive). Use for buttons, inputs, icons, text, badges, loaders, etc. Keep atoms presentational and composable.
argument-hint: "[ComponentName] [optional: brief intent]"
---

# Atomic Design: ATOM (React Functional Components)

You are creating an **ATOM**: the smallest reusable UI primitive.

## Inputs

- `$ARGUMENTS` may include a component name and a short intent.

## Hard rules

1. **Functional component only** (no class components).
2. **No business logic, no data fetching, no app state**. Atoms are presentational primitives.
3. **Accessibility first**: correct semantics (`button`, `label`, `input`), keyboard support, `aria-*` only when necessary.
4. **Composable API**:
   - Prefer children/slots over many boolean props.
   - Avoid prop explosions; keep the surface area minimal.
5. **Styling**:
   - Support `className` and merge with base classes.
   - Avoid styling decisions that depend on application state.
6. **TypeScript-friendly**:
   - Prefer extending intrinsic element props (e.g., `React.ButtonHTMLAttributes<HTMLButtonElement>`).
   - Use `forwardRef` when wrapping DOM elements.
7. **Performance**:
   - Keep atoms cheap; use `React.memo` only if there’s a proven need (don’t add by default).

## Output expectations (when generating code)

- Provide:
  1. `Component.tsx` (or `.jsx` if project is JS)
  2. `Component.test.tsx` (minimal: render + key interaction)
  3. `Component.stories.tsx` (basic variants)
- Export as a **named export** by default.
- Include a short usage snippet.

## Recommended folder conventions

- `src/components/atoms/<ComponentName>/`
  - `index.ts`
  - `<ComponentName>.tsx`
  - `<ComponentName>.test.tsx`
  - `<ComponentName>.stories.tsx`

## Atom checklist

- [ ] Correct semantic element
- [ ] Keyboard operable
- [ ] Accepts `className`
- [ ] Props extend intrinsic element props
- [ ] No app-specific dependencies
