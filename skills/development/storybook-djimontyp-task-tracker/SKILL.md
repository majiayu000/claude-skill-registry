---
name: storybook
description: Storybook stories, CSF3 format, autodocs. Use for component documentation.
---

# Storybook Skill

## Atomic Rule

**Компонент в `shared/` → story обов'язково в тому ж коміті.**

```
F1 creates component → F1 creates story → Same commit
```

## Before Creating UI

1. **Перевір Storybook** на існуючі компоненти
2. **Використовуй існуючі** замість створення нових
3. **Дотримуйся patterns** з Design System

```bash
just storybook  # http://localhost:6006
```

## Story Requirements

### CSF3 Format

```typescript
import type { Meta, StoryObj } from '@storybook/react-vite';
import { ComponentName } from './ComponentName';

const meta: Meta<typeof ComponentName> = {
  title: 'Category/ComponentName',  // See naming below
  component: ComponentName,
  tags: ['autodocs'],               // REQUIRED!
  parameters: {
    docs: {
      description: {
        component: 'Brief description of the component purpose.',
      },
    },
  },
};

export default meta;
type Story = StoryObj<typeof ComponentName>;

export const Default: Story = {
  args: {
    // Default props
  },
};
```

### Naming Convention

| Location | Title Prefix | Example |
|----------|--------------|---------|
| `shared/ui/` | `UI/` | `UI/Button`, `UI/Card` |
| `shared/patterns/` | `Design System/Patterns/` | `Design System/Patterns/CardWithStatus` |
| `shared/components/` | `Components/` | `Components/DataTable` |
| `features/*/components/` | `Features/{Domain}/` | `Features/Analysis/RunCard` |

### Minimum Stories by Tier

| Tier | Location | Minimum Stories |
|------|----------|-----------------|
| **1** | `shared/ui/` | 4-6 (Default, Variants, States, Sizes) |
| **2** | `shared/patterns/` | 5-8 (All statuses, compositions, use cases) |
| **3** | `features/` | 2-4 (Default, Empty, Loading, Error) |

## Required Story Types

### For Shared UI (Tier 1)

```typescript
// REQUIRED
export const Default: Story = { args: { ... } };

// If component has variants
export const Primary: Story = { args: { variant: 'primary' } };
export const Secondary: Story = { args: { variant: 'secondary' } };
export const Destructive: Story = { args: { variant: 'destructive' } };

// If component has sizes
export const Small: Story = { args: { size: 'sm' } };
export const Large: Story = { args: { size: 'lg' } };

// If component has states
export const Disabled: Story = { args: { disabled: true } };
export const Loading: Story = { args: { loading: true } };
```

### For Patterns (Tier 2)

```typescript
// REQUIRED - All status states
export const Connected: Story = { args: { status: 'connected' } };
export const Validating: Story = { args: { status: 'validating' } };
export const Pending: Story = { args: { status: 'pending' } };
export const Error: Story = { args: { status: 'error' } };

// REQUIRED - Compositions
export const WithFooter: Story = { args: { footer: <Button>Action</Button> } };
export const WithContent: Story = { args: { children: <div>...</div> } };

// REQUIRED - Layout examples
export const CardGrid: Story = {
  render: () => (
    <div className="grid grid-cols-3 gap-4">
      <Component ... />
      <Component ... />
      <Component ... />
    </div>
  ),
};
```

### For Feature Components (Tier 3)

```typescript
// REQUIRED
export const Default: Story = { args: { ... } };
export const Empty: Story = { args: { items: [] } };
export const Loading: Story = { args: { isLoading: true } };
export const Error: Story = { args: { error: new Error('Failed to load') } };
```

## Providers for Stories

| Hook Used | Required Provider |
|-----------|-------------------|
| `useTheme` | `ThemeProvider` |
| `useLocation`, `Link` | `MemoryRouter` |
| `useQuery` | `QueryClientProvider` |
| `useSidebar` | `SidebarProvider` |

### Decorator Template

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { ThemeProvider } from '@/shared/components/ThemeProvider';

const queryClient = new QueryClient();

const meta: Meta<typeof Component> = {
  component: Component,
  decorators: [
    (Story) => (
      <QueryClientProvider client={queryClient}>
        <ThemeProvider>
          <MemoryRouter>
            <Story />
          </MemoryRouter>
        </ThemeProvider>
      </QueryClientProvider>
    ),
  ],
};
```

## When Story Is Mandatory

| Location | Mandatory? | Notes |
|----------|------------|-------|
| `shared/ui/` | ✅ Yes | All UI primitives |
| `shared/patterns/` | ✅ Yes | All patterns |
| `shared/components/` | ✅ Yes | If exported publicly |
| `features/*/components/` | ⚠️ Conditional | If >50 LOC or reused |
| `pages/` | ❌ No | Use E2E tests |

## Output Format

When creating component + story:

```
✅ Component implemented

Component: [Name]
Files:
- [component path]
- [story path]
Story: [Tier] / [# of stories]
Verify: npm run build && npx tsc --noEmit
```

## Interaction Testing

Use `play` functions to test user interactions directly in stories.

### Basic Interaction Test

```typescript
import { expect, within, userEvent } from '@storybook/test';

export const ClickTest: Story = {
  args: {
    onClick: fn(),  // Mock function from @storybook/test
  },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);

    // Find and click button
    const button = canvas.getByRole('button');
    await userEvent.click(button);

    // Assert callback was called
    await expect(args.onClick).toHaveBeenCalled();
  },
};
```

### Form Interaction Test

```typescript
export const FormSubmit: Story = {
  args: {
    onSubmit: fn(),
  },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);

    // Fill form
    await userEvent.type(canvas.getByLabelText('Email'), 'test@example.com');
    await userEvent.type(canvas.getByLabelText('Password'), 'password123');

    // Submit
    await userEvent.click(canvas.getByRole('button', { name: /submit/i }));

    // Assert
    await expect(args.onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  },
};
```

### Dialog/Modal Test

```typescript
export const DialogOpen: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Open dialog
    await userEvent.click(canvas.getByRole('button', { name: /open/i }));

    // Wait for dialog
    await expect(canvas.findByRole('dialog')).resolves.toBeInTheDocument();

    // Close with ESC
    await userEvent.keyboard('{Escape}');
    await expect(canvas.queryByRole('dialog')).not.toBeInTheDocument();
  },
};
```

### Keyboard Navigation Test

```typescript
export const KeyboardNav: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Tab through elements
    await userEvent.tab();
    await expect(canvas.getByRole('button', { name: /first/i })).toHaveFocus();

    await userEvent.tab();
    await expect(canvas.getByRole('button', { name: /second/i })).toHaveFocus();

    // Activate with Enter
    await userEvent.keyboard('{Enter}');
  },
};
```

### When to Add Interaction Tests

| Component Type | Interaction Test Required? |
|----------------|---------------------------|
| Buttons with onClick | ✅ Yes |
| Forms | ✅ Yes |
| Dialogs/Modals | ✅ Yes |
| Dropdowns | ✅ Yes |
| Static display | ❌ No |
| Layout components | ❌ No |

### Running Interaction Tests

```bash
# In Storybook UI - click "Interactions" tab
just storybook

# CLI (requires Storybook running)
just storybook-test

# CI mode
just storybook-test-ci
```

## Templates

Use templates from `@templates/` directory:
- `shared-ui.template.tsx` — for `shared/ui/` components
- `pattern.template.tsx` — for `shared/patterns/` components
- `feature.template.tsx` — for `features/*/` components

## References

- Gold standard: `frontend/src/shared/patterns/CardWithStatus.stories.tsx`
- Empty states: `frontend/src/shared/patterns/EmptyState.stories.tsx`
- [CSF3 Format](https://storybook.js.org/blog/storybook-csf3-is-here/)
- [Autodocs](https://storybook.js.org/docs/writing-docs/autodocs)
- [Interaction Testing](https://storybook.js.org/docs/writing-tests/interaction-testing)
- [Play Functions](https://storybook.js.org/docs/writing-stories/play-function)
