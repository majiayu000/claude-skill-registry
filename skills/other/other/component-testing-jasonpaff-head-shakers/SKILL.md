---
name: component-testing
description: Enforces project React component testing conventions using Testing Library with proper rendering, user interactions, and accessibility testing.
---

# Component Testing Skill

## Purpose

This skill provides React component testing conventions using Testing Library. Component tests verify rendering, user interactions, and accessibility of React components.

## Activation

This skill activates when:

- Creating or modifying files in `tests/components/`
- Testing React components (`.tsx` files)
- Working with Testing Library
- Testing user interactions with `userEvent`

## File Patterns

- `tests/components/**/*.test.tsx`

## Workflow

1. Detect component test work (file path contains `tests/components/`)
2. Load `references/Component-Testing-Conventions.md`
3. Also load `testing-base` skill for shared conventions
4. Apply component test patterns with Testing Library
5. Ensure accessibility-first query usage

## Key Patterns (REQUIRED)

### Custom Render

- ALWAYS use `customRender` from `tests/setup/test-utils.tsx`
- Returns `{ user, ...renderResult }` with pre-configured userEvent
- Includes all providers (theme, clerk, etc.)

### Testing Library Queries

- Prefer `getByRole` for accessibility
- Use `getByTestId` with namespace pattern (ui-_, feature-_, form-\*)
- Use `getByText`, `getByLabelText` for content
- Use `queryBy*` for assertions on missing elements

### User Interactions

- Use `user` from customRender return (pre-configured userEvent)
- Always `await` user interactions
- Test real user behaviors, not implementation details

### Pre-Mocked Dependencies

- Clerk, Next.js navigation, sonner, next-themes are pre-mocked
- Mock server actions with `vi.mock()`

## References

- `references/Component-Testing-Conventions.md` - Complete component testing conventions
