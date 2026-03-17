---
name: styled-jsx-global
description: Add or refactor global styles using styled-jsx (<style jsx global>). Use for resets, typography defaults, global tokens, and safe one-off global selectors.
argument-hint: "[scope: app/layout/component] [intent: reset/tokens/one-off]"
---

# styled-jsx Global Styles Skill

Use styled-jsx global styling responsibly.

## Rules

1. Prefer component-scoped styles. Use global styles only when truly global.
2. Prefer CSS variables for tokens (color, spacing, typography) over global tag styling.
3. Avoid heavy global resets unless the project already uses them.
4. If adding a one-off global selector, keep it narrow and well-commented.

## Output expectations

- Create/modify:
  - src/pages/_app.tsx or src/pages/_document.tsx (Next.js) OR
  - a top-level Layout component OR
  - the requested file
- Include a short explanation of what is global and why.

## Patterns

- Global tokens:
  ```css
  :root { --color-bg: ...; --space-2: ...; }
  ```
- Global typography:
  ```css
  body { font-family: ...; }
  ```
- One-off escape hatch:
  ```css
  <style jsx global>{`
    .third-party-class { ... }
  `}</style>
  ```
