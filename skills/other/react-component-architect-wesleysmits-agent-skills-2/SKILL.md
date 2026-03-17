---
name: scaffolding-react-components
description: Scaffolds React/Next.js components with TypeScript, CSS modules, tests, and Storybook stories. Use when the user asks to create a React component, generate component boilerplate, or mentions component architecture.
---

# React Component Architect

## When to use this skill

- User asks to create a new React component
- User wants component scaffolding with tests and stories
- User mentions Next.js component creation
- User asks for TypeScript interfaces for props
- User wants CSS modules or styled components setup

## Workflow

- [ ] Determine component name and location
- [ ] Detect project conventions (file structure, styling approach)
- [ ] Generate component file with TypeScript props
- [ ] Create CSS module with design tokens
- [ ] Generate test file
- [ ] Create Storybook story
- [ ] Export from index if barrel pattern used

## Instructions

### Step 1: Determine Component Details

Gather from user:

- Component name (PascalCase)
- Location: `src/components/`, `app/components/`, or feature folder
- Type: presentational, container, layout, or page component

Derive file paths:

```
src/components/Button/
├── Button.tsx
├── Button.module.css
├── Button.test.tsx
├── Button.stories.tsx
└── index.ts
```

### Step 2: Detect Project Conventions

**Styling approach:**

```bash
ls src/**/*.module.css src/**/*.module.scss 2>/dev/null | head -1 && echo "CSS Modules"
ls src/**/*.styled.ts src/**/*.styles.ts 2>/dev/null | head -1 && echo "Styled Components"
npm ls tailwindcss 2>/dev/null && echo "Tailwind CSS"
```

**Test framework:**

```bash
npm ls jest vitest @testing-library/react 2>/dev/null
```

**Storybook:**

```bash
ls .storybook/main.* 2>/dev/null && echo "Storybook configured"
```

**Barrel exports:**

```bash
ls src/components/index.ts 2>/dev/null && echo "Uses barrel exports"
```

### Step 3: Generate Component File

Use the standard FC structure with TypeScript:

- Export interface for props with JSDoc comments
- Use `FC<Props>` or `forwardRef` for DOM access
- Destructure props with defaults
- Apply CSS module classes

[See component-templates.md](examples/component-templates.md) for full templates including:

- Standard FC component
- forwardRef pattern
- Hooks pattern
- Next.js Server/Client components

### Step 4: Create CSS Module

Use design tokens for consistency:

```css
.root {
  padding: var(--spacing-md, 1rem);
  border-radius: var(--radius-md, 0.5rem);
  background-color: var(--color-primary, #3b82f6);
}

[data-disabled="true"] {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### Step 5: Generate Test File

Use Testing Library with Vitest/Jest:

```tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ComponentName } from "./ComponentName";

describe("ComponentName", () => {
  it("renders children", () => {
    render(<ComponentName>Hello</ComponentName>);
    expect(screen.getByText("Hello")).toBeInTheDocument();
  });

  it("handles click when not disabled", () => {
    const onClick = vi.fn();
    render(<ComponentName onClick={onClick}>Click me</ComponentName>);
    fireEvent.click(screen.getByText("Click me"));
    expect(onClick).toHaveBeenCalledOnce();
  });
});
```

[See testing.md](examples/testing.md) for user events, async testing, context, and hooks testing.

### Step 6: Create Storybook Story

Use CSF3 format for Storybook 7+:

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { ComponentName } from "./ComponentName";

const meta: Meta<typeof ComponentName> = {
  title: "Components/ComponentName",
  component: ComponentName,
  tags: ["autodocs"],
  argTypes: {
    variant: { control: "select", options: ["primary", "secondary"] },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: { children: "Primary Button", variant: "primary" },
};
```

[See storybook.md](examples/storybook.md) for decorators, play functions, and MDX docs.

### Step 7: Create Barrel Export

**index.ts:**

```typescript
export { ComponentName } from "./ComponentName";
export type { ComponentNameProps } from "./ComponentName";
```

**Update parent barrel (if exists):**

```typescript
// src/components/index.ts
export * from "./ComponentName";
```

## Common Patterns

**Compound components:**

```tsx
export const Card = Object.assign(CardRoot, {
  Header: CardHeader,
  Body: CardBody,
});
```

**Polymorphic component:**

```tsx
interface BoxProps<T extends React.ElementType = "div"> {
  as?: T;
}
```

**Context provider:**

```tsx
const Context = createContext<Value | null>(null);
export const useContext = () => {
  const ctx = useContext(Context);
  if (!ctx) throw new Error("Must be used within Provider");
  return ctx;
};
```

[See advanced-patterns.md](examples/advanced-patterns.md) for compound components, HOCs, render props, and error boundaries.

## Validation

Before completing:

- [ ] Component renders without errors
- [ ] TypeScript has no errors
- [ ] Props interface is exported
- [ ] CSS module imports correctly
- [ ] Tests pass
- [ ] Story renders in Storybook
- [ ] Barrel export updated

## Error Handling

- **Module not found**: Check import paths use correct relative paths.
- **CSS module types**: Add `declare module '*.module.css'` to global types if needed.
- **Test setup missing**: Ensure `@testing-library/react` and `@testing-library/jest-dom` are installed.
- **Storybook not rendering**: Check `.storybook/main.js` includes correct story glob pattern.
- **Unsure about conventions**: Check existing components in project for patterns.

## Resources

- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [Testing Library Documentation](https://testing-library.com/docs/react-testing-library/intro/)
- [Storybook Documentation](https://storybook.js.org/docs/react/get-started/introduction)

## Examples

- [Component Templates](examples/component-templates.md) — FC, forwardRef, hooks, Next.js patterns
- [Testing](examples/testing.md) — User events, async, context, hooks testing
- [Storybook](examples/storybook.md) — Decorators, play functions, MDX docs
- [Advanced Patterns](examples/advanced-patterns.md) — Compound components, HOCs, error boundaries
