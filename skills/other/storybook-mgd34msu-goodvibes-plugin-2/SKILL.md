---
name: storybook
description: Develops and documents UI components in isolation with Storybook's interactive workshop environment. Use when building component libraries, documenting design systems, or when user mentions Storybook, component documentation, or UI development.
---

# Storybook

Industry-standard workshop for building, documenting, and testing UI components in isolation.

## Quick Start

```bash
# Install in existing project
npx storybook@latest init

# Start Storybook
npm run storybook
```

## Project Structure

```
.storybook/
  main.ts           # Configuration
  preview.ts        # Global decorators and parameters
  preview-head.html # Custom head content
src/
  components/
    Button/
      Button.tsx
      Button.stories.tsx
      Button.module.css
```

## Configuration

### main.ts

```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [
    '@storybook/addon-onboarding',
    '@storybook/addon-essentials',
    '@chromatic-com/storybook',
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
  staticDirs: ['../public'],
  typescript: {
    reactDocgen: 'react-docgen-typescript',
  },
};

export default config;
```

### preview.ts

```typescript
// .storybook/preview.ts
import type { Preview } from '@storybook/react';
import '../src/styles/globals.css';

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1a1a1a' },
        { name: 'gray', value: '#f5f5f5' },
      ],
    },
    layout: 'centered',
  },
  decorators: [
    (Story) => (
      <div style={{ margin: '1rem' }}>
        <Story />
      </div>
    ),
  ],
  globalTypes: {
    theme: {
      name: 'Theme',
      description: 'Global theme',
      defaultValue: 'light',
      toolbar: {
        icon: 'circlehollow',
        items: ['light', 'dark'],
        showName: true,
      },
    },
  },
};

export default preview;
```

## Writing Stories

### Basic Story

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger'],
    },
    size: {
      control: 'radio',
      options: ['sm', 'md', 'lg'],
    },
    onClick: { action: 'clicked' },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

// Stories
export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Button',
  },
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Button',
  },
};

export const Large: Story = {
  args: {
    size: 'lg',
    children: 'Large Button',
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled',
  },
};
```

### With Decorators

```tsx
export const InDarkMode: Story = {
  decorators: [
    (Story) => (
      <div className="dark bg-gray-900 p-4">
        <Story />
      </div>
    ),
  ],
  args: {
    children: 'Dark Mode Button',
  },
};

// Decorator with args access
export const WithContext: Story = {
  decorators: [
    (Story, context) => (
      <ThemeProvider theme={context.globals.theme}>
        <Story />
      </ThemeProvider>
    ),
  ],
};
```

### With Play Functions (Interaction Testing)

```tsx
import { within, userEvent, expect } from '@storybook/test';

export const Filled: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Type in input
    const input = canvas.getByPlaceholderText('Enter email');
    await userEvent.type(input, 'test@example.com', { delay: 100 });

    // Click button
    const button = canvas.getByRole('button', { name: /submit/i });
    await userEvent.click(button);

    // Assert
    await expect(canvas.getByText('Success!')).toBeInTheDocument();
  },
};

export const WithValidation: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Submit empty form
    await userEvent.click(canvas.getByRole('button'));

    // Check for error
    await expect(canvas.getByText('Email is required')).toBeVisible();
  },
};
```

### Async Stories

```tsx
export const WithData: Story = {
  loaders: [
    async () => ({
      users: await fetch('/api/users').then((r) => r.json()),
    }),
  ],
  render: (args, { loaded: { users } }) => (
    <UserList users={users} {...args} />
  ),
};

// Or with render function
export const Loading: Story = {
  render: () => {
    const [data, setData] = useState(null);

    useEffect(() => {
      fetchData().then(setData);
    }, []);

    if (!data) return <Skeleton />;
    return <Component data={data} />;
  },
};
```

## Controls

### ArgTypes

```tsx
const meta: Meta<typeof Button> = {
  argTypes: {
    // Control types
    variant: {
      control: 'select',
      options: ['primary', 'secondary'],
      description: 'Visual style variant',
      table: {
        type: { summary: 'string' },
        defaultValue: { summary: 'primary' },
      },
    },

    size: {
      control: 'inline-radio',
      options: ['sm', 'md', 'lg'],
    },

    disabled: {
      control: 'boolean',
    },

    count: {
      control: { type: 'number', min: 0, max: 100, step: 1 },
    },

    color: {
      control: 'color',
    },

    date: {
      control: 'date',
    },

    items: {
      control: 'object',
    },

    label: {
      control: 'text',
    },

    // Disable control
    onClick: {
      control: false,
    },

    // Categorize in table
    theme: {
      table: {
        category: 'Styling',
      },
    },
  },
};
```

## Documentation

### MDX Documentation

```mdx
{/* Button.mdx */}
import { Canvas, Meta, Story, Controls, ArgTypes } from '@storybook/blocks';
import * as ButtonStories from './Button.stories';

<Meta of={ButtonStories} />

# Button

Buttons trigger actions when clicked.

## Usage

```tsx
import { Button } from '@/components/Button';

<Button variant="primary" onClick={handleClick}>
  Click me
</Button>
```

## Examples

### Primary Button

<Canvas of={ButtonStories.Primary} />

### All Variants

<Canvas>
  <Story of={ButtonStories.Primary} />
  <Story of={ButtonStories.Secondary} />
  <Story of={ButtonStories.Danger} />
</Canvas>

## Props

<Controls />

<ArgTypes of={ButtonStories} />
```

### Component Documentation

```tsx
// Button.tsx - JSDoc for autodocs
interface ButtonProps {
  /** The visual style variant */
  variant?: 'primary' | 'secondary' | 'danger';
  /** Button size */
  size?: 'sm' | 'md' | 'lg';
  /** Whether the button is disabled */
  disabled?: boolean;
  /** Click handler */
  onClick?: () => void;
  /** Button content */
  children: React.ReactNode;
}

/**
 * Primary UI component for user interaction.
 *
 * @example
 * ```tsx
 * <Button variant="primary" onClick={handleClick}>
 *   Click me
 * </Button>
 * ```
 */
export function Button({ variant = 'primary', size = 'md', ...props }: ButtonProps) {
  // ...
}
```

## Addons

### Essential Addons (Included)

```typescript
// Already included with @storybook/addon-essentials:
// - Controls: Interactive props
// - Actions: Event logging
// - Docs: Auto-documentation
// - Viewport: Responsive testing
// - Backgrounds: Background colors
// - Toolbars: Global controls
// - Measure: Layout measurement
// - Outline: DOM outlines
```

### Accessibility Testing

```bash
npm install -D @storybook/addon-a11y
```

```typescript
// .storybook/main.ts
addons: ['@storybook/addon-a11y'],

// In story
export const Accessible: Story = {
  parameters: {
    a11y: {
      config: {
        rules: [{ id: 'color-contrast', enabled: true }],
      },
    },
  },
};
```

### Interactions

```bash
npm install -D @storybook/addon-interactions @storybook/test
```

```tsx
import { within, userEvent, expect, fn } from '@storybook/test';

const meta: Meta<typeof Form> = {
  args: {
    onSubmit: fn(),
  },
};

export const Submitted: Story = {
  play: async ({ args, canvasElement }) => {
    const canvas = within(canvasElement);

    await userEvent.type(canvas.getByLabelText('Email'), 'test@test.com');
    await userEvent.click(canvas.getByRole('button'));

    await expect(args.onSubmit).toHaveBeenCalled();
  },
};
```

## Testing Stories

### With Test Runner

```bash
npm install -D @storybook/test-runner

# Run tests
npx test-storybook

# Watch mode
npx test-storybook --watch
```

### With Vitest

```typescript
// Button.test.tsx
import { composeStories } from '@storybook/react';
import { render, screen } from '@testing-library/react';
import * as stories from './Button.stories';

const { Primary, Secondary } = composeStories(stories);

test('Primary button renders correctly', () => {
  render(<Primary />);
  expect(screen.getByRole('button')).toHaveClass('btn-primary');
});

test('runs play function', async () => {
  const { container } = render(<Secondary />);
  await Secondary.play?.({ canvasElement: container });
});
```

## Visual Testing with Chromatic

```bash
# Install
npm install -D chromatic

# Run
npx chromatic --project-token=<token>
```

```yaml
# .github/workflows/chromatic.yml
name: Chromatic
on: push
jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
      - run: npm ci
      - uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
```

## Build and Deploy

```bash
# Build static Storybook
npm run build-storybook

# Output in storybook-static/
```

```yaml
# Deploy to GitHub Pages
# .github/workflows/deploy.yml
name: Deploy Storybook
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build-storybook
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./storybook-static
```

## Reference Files

- [patterns.md](references/patterns.md) - Common Storybook patterns
- [testing.md](references/testing.md) - Testing strategies with Storybook
