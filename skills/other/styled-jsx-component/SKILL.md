---
name: styled-jsx-component
description: Create or refactor a React functional component styled with styled-jsx (<style jsx>). Use for scoped component styles, including variants, theming via CSS variables, and accessible UI patterns.
argument-hint: "[ComponentName] [optional: intent/variant notes]"
---

# styled-jsx Component Skill (React Functional Components)

You are creating or refactoring a React FUNCTIONAL component that uses styled-jsx for styling.

## Inputs

- $ARGUMENTS may include a component name and a short intent/variant description.

## Non-negotiables

1. Functional component only (no class components).
2. Prefer semantic HTML and accessibility by default:
   - Correct element choice (button/a/input/etc)
   - Keyboard support
   - aria-* only when needed
3. Use styled-jsx <style jsx>{`...`}</style> for component-scoped CSS.
4. Keep styling maintainable:
   - Prefer CSS variables for theming/tokens
   - Avoid overly-specific selectors
   - Avoid styling through DOM structure that will change easily
5. Variants:
   - Prefer a single "variant" prop (string union) over many booleans.
   - Use data attributes (e.g., data-variant) for styling hooks.
6. Dynamic styling:
   - Prefer className toggling or CSS variables for runtime values.
   - Use template literal interpolation only when it’s necessary and safe.
7. SSR/Next.js considerations:
   - styled-jsx is SSR-compatible; do not use browser-only APIs during render.

## Output expectations

- Create/modify files per template.md.
- Provide:
  1) Component implementation
  2) Minimal test (render + primary interaction + a11y)
  3) Storybook story (basic variants)
  4) Short usage snippet

## Best-practice patterns to apply

- Tokens:
  - Use CSS vars like --color-fg, --color-bg, --radius, --space-2.
  - Provide sensible defaults in :root only when asked; otherwise keep tokens local to the component with fallback values.
- Prefer:
  - :global(...) only for one-off escape hatches
  - data-* attributes for styling states (data-state, data-variant)
- Avoid:
  - Global leakage
  - Deep descendant styling
  - Interpolating untrusted strings into CSS

Use the accompanying template.md as the default structure; deviate only when the component needs a different intrinsic element type or ref pattern.
