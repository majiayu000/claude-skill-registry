---
name: new-component
description: Scaffold a new React component with accessibility, Tailwind styling, and a co-located test file
user-invokable: true
---

# new-component

Create a new React component under `src/` with a co-located test file. Default location is `src/app/components/` unless the user specifies otherwise.

## Arguments

The user will provide a component name and optionally a subdirectory.

## Component file conventions

- Use **kebab-case** file names (e.g., `user-profile.tsx`) — enforced by `eslint-plugin-check-file`
- **Named export** only (no default exports, unless it's a Next.js page/layout)
- Use **PascalCase** for the component name (e.g., `UserProfile`)
- Use **Tailwind CSS** for styling
- Props type defined inline or as `type Props = { ... }` in the same file (no separate types file for a single component)
- Add `'use client'` directive at the top if the component uses hooks, event handlers, or browser APIs

## Accessibility requirements (WCAG 2.1 AA)

- Use **semantic HTML** (`nav`, `main`, `section`, `button`, `header`, `footer`, `article`, `aside`, etc.) — not generic `div`/`span`
- All `<img>` elements must have meaningful `alt` text
- Interactive elements must be **keyboard-accessible**
- Form inputs must have associated `<label>` elements
- Use ARIA attributes **only** when semantic HTML is not sufficient

## Test file conventions

- Co-located: `my-component.tsx` -> `my-component.test.tsx`
- The **very first line** must be `// @vitest-environment jsdom`
- Use `@testing-library/react` (`render`, `screen`)
- Query by **accessible roles** (`getByRole`, `getByLabelText`) rather than test IDs
- Use backtick strings for `describe`/`it` labels
- Include at minimum a smoke-test that renders the component and asserts it is in the document

## Example output

For `/new-component UserCard src/app/components`:

`src/app/components/user-card.tsx`:

```tsx
type Props = {
  name: string
}

export const UserCard = ({ name }: Props) => {
  return (
    <article className="rounded-lg border border-neutral-300 p-4">
      <h2>{name}</h2>
    </article>
  )
}
```

`src/app/components/user-card.test.tsx`:

```tsx
// @vitest-environment jsdom
import { render, screen } from '@testing-library/react'
import { UserCard } from './user-card'

describe(`UserCard`, () => {
  it(`should render the user name`, () => {
    render(<UserCard name="Alice" />)
    expect(screen.getByRole(`heading`)).toHaveTextContent(`Alice`)
  })
})
```
