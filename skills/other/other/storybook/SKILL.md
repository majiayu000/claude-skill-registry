---
name: storybook
description: Document and test React components with Storybook. Covers story writing, controls, args, decorators, play functions, and visual testing. Use for component documentation, design systems, isolated development, and interaction testing.
---

# Storybook

Build and document UI components in isolation with interactive stories.

## Instructions

1. **Write stories for all components** - Each component should have a story file
2. **Use args for props** - Define props through args for interactive controls
3. **Add decorators** - Wrap stories with providers and layout wrappers
4. **Document with MDX** - Write component documentation alongside stories
5. **Test interactions** - Use play functions for interaction testing

## Setup

```bash
# Initialize Storybook in existing project
npx storybook@latest init

# Start Storybook
npm run storybook
```

### Configuration

```ts
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y',
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  docs: {
    autodocs: 'tag',
  },
};

export default config;
```

## Writing Stories

### Basic Story Structure

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger', 'ghost'],
      description: 'The visual style of the button',
    },
    size: {
      control: 'radio',
      options: ['sm', 'md', 'lg'],
    },
    disabled: {
      control: 'boolean',
    },
    onClick: { action: 'clicked' },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    children: 'Primary Button',
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    children: 'Secondary Button',
    variant: 'secondary',
  },
};

export const Disabled: Story = {
  args: {
    children: 'Disabled Button',
    disabled: true,
  },
};
```

### Multiple Variants

```tsx
export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-wrap gap-4">
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="danger">Danger</Button>
      <Button variant="ghost">Ghost</Button>
    </div>
  ),
};

export const AllSizes: Story = {
  render: () => (
    <div className="flex items-center gap-4">
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
};
```

### With Args

```tsx
// args allow interactive control in Storybook UI
export const Playground: Story = {
  args: {
    children: 'Click me',
    variant: 'primary',
    size: 'md',
    disabled: false,
    loading: false,
  },
};
```

## Decorators

### Global Decorators

```tsx
// .storybook/preview.tsx
import type { Preview } from '@storybook/react';
import { ThemeProvider } from '../src/providers/ThemeProvider';
import '../src/styles/globals.css';

const preview: Preview = {
  decorators: [
    (Story) => (
      <ThemeProvider>
        <div className="p-4">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};

export default preview;
```

### Story-Level Decorators

```tsx
export const WithDarkBackground: Story = {
  decorators: [
    (Story) => (
      <div className="bg-gray-900 p-8">
        <Story />
      </div>
    ),
  ],
  args: {
    children: 'Dark Mode Button',
    variant: 'primary',
  },
};
```

## Interaction Testing

### Play Functions

```tsx
import { within, userEvent, expect } from '@storybook/test';

export const ClickInteraction: Story = {
  args: {
    children: 'Click me',
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button', { name: /click me/i });

    await userEvent.click(button);

    // Assertions
    await expect(button).toBeVisible();
  },
};

export const FormSubmission: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Fill form fields
    await userEvent.type(
      canvas.getByLabelText(/email/i),
      'user@example.com'
    );
    await userEvent.type(
      canvas.getByLabelText(/password/i),
      'password123'
    );

    // Submit form
    await userEvent.click(canvas.getByRole('button', { name: /submit/i }));

    // Check result
    await expect(canvas.getByText(/success/i)).toBeInTheDocument();
  },
};
```

## Component Documentation

### MDX Documentation

```mdx
{/* Button.mdx */}
import { Meta, Story, Canvas, Controls, Source } from '@storybook/blocks';
import * as ButtonStories from './Button.stories';

<Meta of={ButtonStories} />

# Button

Buttons trigger actions or navigation. Use the appropriate variant
for the action's importance and context.

## Usage Guidelines

- Use **Primary** for the main action on a page
- Use **Secondary** for less important actions
- Use **Danger** only for destructive actions
- Limit to one primary button per section

## Examples

### Default

<Canvas of={ButtonStories.Primary} />

### All Variants

<Canvas of={ButtonStories.AllVariants} />

## Props

<Controls />

## Accessibility

- Buttons have proper focus states
- Loading state disables interaction and shows spinner
- Use `aria-label` for icon-only buttons

## Code

<Source of={ButtonStories.Primary} />
```

### Inline Stories in MDX

```mdx
import { Canvas, Meta } from '@storybook/blocks';
import { Button } from './Button';

<Meta title="Guide/Button Usage" />

# Using Buttons

Here's how to use buttons in different contexts:

<Canvas>
  <Button variant="primary">Save Changes</Button>
  <Button variant="secondary">Cancel</Button>
</Canvas>
```

## Parameters

### Layout

```tsx
export const Centered: Story = {
  parameters: {
    layout: 'centered', // centered | fullscreen | padded
  },
};
```

### Backgrounds

```tsx
export const OnDark: Story = {
  parameters: {
    backgrounds: {
      default: 'dark',
    },
  },
};
```

### Viewport

```tsx
export const Mobile: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};
```

## Addons

### Accessibility Addon

```tsx
// Automatically checks accessibility
export const AccessibleButton: Story = {
  args: {
    children: 'Accessible',
    'aria-label': 'Accessible button description',
  },
  parameters: {
    a11y: {
      config: {
        rules: [
          { id: 'color-contrast', enabled: true },
        ],
      },
    },
  },
};
```

### Actions Addon

```tsx
const meta: Meta<typeof Button> = {
  component: Button,
  argTypes: {
    onClick: { action: 'clicked' },
    onFocus: { action: 'focused' },
    onBlur: { action: 'blurred' },
  },
};
```

## Project Structure

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   ├── Button.stories.tsx
│   │   ├── Button.mdx
│   │   └── index.ts
│   ├── Card/
│   │   ├── Card.tsx
│   │   ├── Card.stories.tsx
│   │   └── index.ts
│   └── index.ts
├── .storybook/
│   ├── main.ts
│   └── preview.tsx
└── package.json
```

## Best Practices

| Practice | Recommendation |
|----------|----------------|
| **File naming** | `Component.stories.tsx` alongside component |
| **Story naming** | Use descriptive names like `WithIcon`, `Disabled` |
| **Args** | Prefer args over inline JSX for flexibility |
| **Decorators** | Use for providers, layout, theming |
| **Play functions** | Test interactions, not just rendering |
| **Documentation** | Write MDX docs for complex components |

## When to Use

- Component library development
- Design system documentation
- Visual regression testing
- Isolated component development
- Team collaboration on UI
- Accessibility testing

## Notes

- Storybook 7+ uses Component Story Format (CSF) 3
- Works with React, Vue, Angular, Svelte, and more
- Integrates with Chromatic for visual testing
- Supports TypeScript out of the box
- Hot module reloading for fast development
