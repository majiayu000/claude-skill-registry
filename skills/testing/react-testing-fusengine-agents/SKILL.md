---
name: react-testing
description: Testing Library for React 19 - render, screen, userEvent, waitFor, Suspense. Use when writing tests for React components with Vitest.
versions:
  "@testing-library/react": 16.1.0
  "@testing-library/user-event": 14.5.2
  vitest: 2.1.8
  msw: 2.7.0
  react: 19
user-invocable: true
references: references/installation.md, references/queries.md, references/user-events.md, references/async-testing.md, references/msw-setup.md, references/react-19-hooks.md, references/accessibility-testing.md, references/hooks-testing.md, references/vitest-config.md, references/mocking-patterns.md, references/templates/basic-setup.md, references/templates/component-basic.md, references/templates/component-async.md, references/templates/form-testing.md, references/templates/hook-basic.md, references/templates/api-integration.md, references/templates/suspense-testing.md, references/templates/error-boundary.md, references/templates/accessibility-audit.md
related-skills: react-19, solid-react, react-state, react-forms
---

# React Testing Library

Test React components the way users interact with them.

## Agent Workflow (MANDATORY)

Before ANY implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing test patterns
2. **fuse-ai-pilot:research-expert** - Verify latest Testing Library docs via Context7/Exa
3. **mcp__context7__query-docs** - Check userEvent, waitFor patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Testing React component behavior
- Validating user interactions
- Ensuring accessibility compliance
- Mocking API calls with MSW
- Testing custom hooks
- Testing React 19 features (useActionState, use())

### Why React Testing Library

| Feature | Benefit |
|---------|---------|
| User-centric | Tests what users see |
| Accessible queries | Encourages a11y markup |
| No implementation details | Resilient to refactoring |
| Vitest integration | 10-20x faster than Jest |

---

## Critical Rules

1. **Query by role first** - `getByRole` is most accessible
2. **Use userEvent, not fireEvent** - Realistic interactions
3. **waitFor for async** - Never `setTimeout`
4. **MSW for API mocking** - Don't mock fetch
5. **Test behavior, not implementation** - No internal state testing

---

## Reference Guide

### Concepts

| Topic | Reference |
|-------|-----------|
| Setup & installation | `references/installation.md` |
| Query priority | `references/queries.md` |
| User interactions | `references/user-events.md` |
| Async patterns | `references/async-testing.md` |
| API mocking | `references/msw-setup.md` |
| React 19 hooks | `references/react-19-hooks.md` |
| Accessibility | `references/accessibility-testing.md` |
| Custom hooks | `references/hooks-testing.md` |
| Vitest config | `references/vitest-config.md` |
| Mocking patterns | `references/mocking-patterns.md` |

### Templates

| Template | Use Case |
|----------|----------|
| `templates/basic-setup.md` | Vitest + RTL + MSW config |
| `templates/component-basic.md` | Simple component tests |
| `templates/component-async.md` | Loading/error/success |
| `templates/form-testing.md` | Forms + useActionState |
| `templates/hook-basic.md` | Custom hook tests |
| `templates/api-integration.md` | MSW integration tests |
| `templates/suspense-testing.md` | Suspense + use() |
| `templates/error-boundary.md` | Error boundary tests |
| `templates/accessibility-audit.md` | axe-core a11y audit |

---

## Forbidden Patterns

| Pattern | Reason | Alternative |
|---------|--------|-------------|
| `fireEvent` | Not realistic | `userEvent` |
| `setTimeout` | Flaky | `waitFor`, `findBy` |
| `getByTestId` first | Not accessible | `getByRole` |
| Direct fetch mocking | Hard to maintain | MSW |
| Empty `waitFor` | No assertion | Add `expect()` |

---

## Quick Start

### Install

```bash
npm install -D vitest @testing-library/react \
  @testing-library/user-event @testing-library/jest-dom \
  jsdom msw
```

→ See `templates/basic-setup.md` for complete configuration

### Basic Test

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

test('button click works', async () => {
  const user = userEvent.setup()
  render(<Button onClick={fn}>Click</Button>)

  await user.click(screen.getByRole('button'))

  expect(fn).toHaveBeenCalled()
})
```

→ See `templates/component-basic.md` for more examples

---

## Best Practices

### Query Priority

1. `getByRole` - Buttons, headings, inputs
2. `getByLabelText` - Form inputs
3. `getByText` - Static text
4. `getByTestId` - Last resort

### Async Pattern

```typescript
// Preferred: findBy
await screen.findByText('Loaded')

// Alternative: waitFor
await waitFor(() => expect(...).toBeInTheDocument())
```

→ See `templates/component-async.md`

### userEvent Setup

```typescript
const user = userEvent.setup()
await user.click(button)
await user.type(input, 'text')
```

→ See `references/user-events.md`
