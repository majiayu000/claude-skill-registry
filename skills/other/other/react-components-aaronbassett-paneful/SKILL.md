---
name: react-component
description: |
  Create and review React components following strict TypeScript patterns, container/presenter architecture, and composition-first design. Use when asked to: (1) Create a React component, (2) Review a React component, (3) Build UI features, (4) Implement forms, (5) Add data fetching with TanStack Query. Enforces KISS/YAGNI principles, headless component patterns, Tailwind v4 styling, and Web3 security best practices.
---

# React Component Skill

## Quick Start

### Creating Components

1.  **Automated Scaffolding**:
    Use the `scaffold-component.mjs` script to quickly generate the boilerplate for a new feature component:

    ```bash
    node .claude/skills/react-component/scripts/scaffold-component.mjs <featureName> <ComponentName>
    ```

    - `<featureName>` (camelCase): e.g., `userProfile` (creates `src/features/userProfile/components/`).
    - `<ComponentName>` (PascalCase): e.g., `UserProfileCard` (generates `UserProfileCardContainer.tsx`, `UserProfileCardView.tsx`, `UserProfileCardView.stories.tsx`).
      _Run this command from the root of your React project._

2.  Read [principles.md](references/principles.md) for core philosophy
3.  Read [patterns.md](references/patterns.md) for container/presenter pattern
4.  Read [project-structure.md](references/project-structure.md) for file placement

### Reviewing Components

1. Read [code-review.md](references/code-review.md) for review checklist
2. Cross-reference with [patterns.md](references/patterns.md) and [security.md](references/security.md)

---

## Component Creation Workflow

### Step 1: Determine Component Type

| Type      | Purpose                         | Contains                 |
| --------- | ------------------------------- | ------------------------ |
| Container | Data fetching, state management | Hooks, no complex markup |
| Presenter | Pure UI rendering               | Props, no side effects   |
| Hook      | Reusable logic                  | No JSX                   |

### Step 2: Choose Location

```
# Shared UI primitive
src/components/ui/<ComponentName>.tsx

# Feature-specific
src/features/<feature>/components/<Name>Container.tsx
src/features/<feature>/components/<Name>View.tsx
```

### Step 3: Implement Pattern

**Container + Presenter pair:**

```tsx
// Container: handles data
export function FeatureContainer() {
  const { data, error, isLoading } = useFeatureQuery()

  if (isLoading) return <FeatureView state="loading" />
  if (error) return <FeatureView state="error" message={error.message} />
  if (!data) return <FeatureView state="empty" />

  return <FeatureView state="ready" data={data} />
}

// Presenter: handles UI
export function FeatureView({ state, data, message }: FeatureViewProps) {
  // Pure rendering based on props
}
```

### Step 4: Add Storybook

Create stories for all four states: loading, error, empty, ready.

```tsx
// FeatureView.stories.tsx
export const Loading = { args: { state: 'loading' } }
export const Empty = { args: { state: 'empty' } }
export const Error = { args: { state: 'error', message: 'Something went wrong' } }
export const Ready = { args: { state: 'ready', data: mockData } }
```

For more on creating interactive stories with controls, documenting with MDX, and mocking API requests for container components, see the [Advanced Storybook Guide](references/advanced-storybook.md).

### Step 5: Verify

- Zero TypeScript errors (strict mode)
- Zero linter warnings
- Follows [naming conventions](references/naming.md)
- Uses only [approved packages](references/packages.md)

---

## Key Rules

### TypeScript

- Strict mode required
- Props interface named `<Component>Props`
- Explicit return types on exported functions

### Styling

- Tailwind v4 only (no `tailwind.config.js`)
- Use `cn()` utility for conditional classes
- Responsive: `sm`, `md`, `lg`, `xl` minimum

### State

- Remote data: TanStack Query
- Local UI: useState/useReducer
- Shared: prop drilling → Context → Zustand (last resort)

### Forms

- React Hook Form + Zod
- Schema in `forms/<schema>.ts`
- Hook in `forms/use-<form>-form.ts`

### Testing

- Vitest + React Testing Library + MSW
- Test behavior, not internals
- No testing Tailwind classes

---

## Reference Files

| File                                                        | When to Read                              |
| ----------------------------------------------------------- | ----------------------------------------- |
| [naming.md](references/naming.md)                           | Variable, function, component naming      |
| [principles.md](references/principles.md)                   | Core philosophy (KISS, YAGNI, UX-first)   |
| [patterns.md](references/patterns.md)                       | Container/presenter, composition          |
| [headless-components.md](references/headless-components.md) | Headless pattern, Radix-style composition |
| [project-structure.md](references/project-structure.md)     | File organization                         |
| [state-and-styling.md](references/state-and-styling.md)     | State management, Tailwind, async UX      |
| [forms-and-testing.md](references/forms-and-testing.md)     | RHF + Zod, Vitest + RTL                   |
| [advanced-storybook.md](references/advanced-storybook.md)   | Interactive stories, MDX, API mocking     |
| [error-handling.md](references/error-handling.md)           | Error boundaries, logging, reporting      |
| [security.md](references/security.md)                       | Web3 safety, logging                      |
| [accessibility.md](references/accessibility.md)             | a11y best practices, testing              |
| [packages.md](references/packages.md)                       | Approved dependencies                     |
| [code-review.md](references/code-review.md)                 | Review checklist                          |

---

## External Resources

- [usehooks](https://github.com/uidotdev/usehooks) - Check before writing custom hooks
- [Radix UI Themes](https://www.radix-ui.com/themes/docs/overview/getting-started)
- [Radix Primitives](https://www.radix-ui.com/primitives/docs/overview/introduction) - Unstyled, accessible components
- [shadcn/ui](https://ui.shadcn.com/) - Pre-built Radix + Tailwind components
