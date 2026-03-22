---
name: gen-test
description: Generate a Vitest test file for a given source file, following project testing conventions
user-invokable: true
---

# gen-test

Generate a Vitest test file for the specified source file. The test file must be co-located with the source file (e.g., `foo.ts` -> `foo.test.ts`).

## Arguments

The user will provide a file path or describe the module to test.

## Component tests (anything that renders JSX)

- The **very first line** must be `// @vitest-environment jsdom` — no blank lines above it
- Use `@testing-library/react` for rendering and querying (`render`, `screen`)
- Use `@testing-library/jest-dom` matchers (e.g., `toHaveTextContent`, `toBeInTheDocument`)
- Query by accessible roles (`getByRole`, `getByLabelText`) rather than test IDs
- Next.js pages/layouts use `export default` — import accordingly

Example shape:

```tsx
// @vitest-environment jsdom
import { render, screen } from '@testing-library/react'
import MyPage from './page'

describe(`MyPage`, () => {
  it(`should render the heading`, () => {
    render(<MyPage />)
    expect(screen.getByRole(`heading`)).toHaveTextContent(`Expected text`)
  })
})
```

## API route tests (anything under `src/app/api/`)

- Do NOT add the jsdom pragma
- Call route handler functions (`GET`, `POST`, etc.) directly — they return a standard `Response`
- Use the Drizzle `db` instance directly for database assertions
- Clean up database state in `beforeEach`
- Use `@/db` and `@/const/...` path aliases for imports

Example shape:

```ts
import { db } from '@/db'
import { myTable } from '@/db/schema'
import { GET } from './route'

beforeEach(async () => {
  await db.delete(myTable)
})

describe(`/api/my-endpoint`, () => {
  it(`should return success`, async () => {
    const response = await GET()

    expect(response.status).toBe(200)
    expect(await response.json()).toEqual({ success: true })
  })
})
```

## General conventions

- Use backtick strings for `describe` and `it` labels (not single/double quotes)
- Follow AAA pattern: Arrange, Act, Assert (with blank lines separating each phase when all three are present)
- Use descriptive test names: `it('returns 404 when resource not found')`
- Named exports only — no default exports (except Next.js page/layout components)
- One `describe` block per logical unit; nest when testing sub-behaviors
