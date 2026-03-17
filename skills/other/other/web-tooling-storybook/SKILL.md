---
name: web-tooling-storybook
description: Storybook 8 patterns - CSF 3.0, args, controls, autodocs, play functions, interaction testing, visual testing, addons configuration
---

# Storybook Patterns

> **Quick Guide:** Storybook is a component workshop for building and documenting UI in isolation. Use CSF 3.0 format with typed `meta` and story objects. Define component variants via `args`. Use play functions for interaction testing. Enable `autodocs` for automatic documentation. Configure addons in `.storybook/main.ts`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use CSF 3.0 format with `satisfies Meta<typeof Component>` for type-safe story metadata)**

**(You MUST define a default `meta` export with `component` property - stories without `component` won't render)**

**(You MUST use `args` for defining props - NOT rendering components with hardcoded props)**

**(You MUST use play functions with `@storybook/test` utilities for interaction testing - NOT custom event firing)**

**(You MUST use named exports for stories - default export is reserved for meta object)**

</critical_requirements>

---

**Auto-detection:** Storybook, .stories.tsx, .stories.ts, CSF, Component Story Format, meta, Meta, StoryObj, args, argTypes, play function, autodocs, @storybook/test, @storybook/addon-essentials

**When to use:**

- Developing UI components in isolation without full application context
- Creating interactive documentation for component libraries
- Testing component interactions and visual states
- Building design systems with comprehensive examples
- Generating automatic API documentation from TypeScript props
- Visual regression testing with Chromatic or similar tools

**When NOT to use:**

- E2E user flow testing spanning multiple pages (use Playwright/Cypress)
- Unit testing pure functions without UI (use Vitest directly)
- Integration testing with real backend services
- Performance testing and load testing

**Key patterns covered:**

- CSF 3.0 story format with TypeScript
- Args and ArgTypes for props control
- Play functions for interaction testing
- Autodocs for automatic documentation
- MDX for custom documentation pages
- Decorators and parameters
- Addon configuration and customization
- Visual testing integration

**Detailed Resources:**

- For code examples, see `examples/` folder:
  - [examples/core.md](examples/core.md) - CSF 3.0 format, args, controls
  - [examples/docs.md](examples/docs.md) - Autodocs, MDX documentation
  - [examples/testing.md](examples/testing.md) - Play functions, interaction testing
  - [examples/addons.md](examples/addons.md) - Addon configuration
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Storybook enables **component-driven development** - building UI from the bottom up, starting with basic components and progressively combining them into complex interfaces.

**Core Principles:**

1. **Isolation** - Develop components without needing the full application, database, or authentication
2. **Documentation** - Stories serve as living documentation that stays in sync with code
3. **Testing** - Use stories as test fixtures for interaction, visual, and accessibility testing
4. **Collaboration** - Designers, developers, and stakeholders can review components independently

**The Story Paradigm:**

A "story" captures a specific state of a component. Each story represents one meaningful variation - a button's primary state, disabled state, loading state, etc. Stories are not test cases; they are documented examples.

**When to use Storybook:**

- Building component libraries or design systems
- Developing UI in parallel with backend work
- Creating documentation for component APIs
- Visual testing and regression detection
- Reviewing UI changes in pull requests

**When NOT to use:**

- For user journey testing (use E2E tools)
- For testing business logic without UI
- For components that require full application context

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: CSF 3.0 Story Format

Component Story Format 3.0 is the standard for writing stories. It uses typed objects for maximum type safety.

#### Basic Story Structure

```typescript
// button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./button";

// Meta object describes the component
const meta = {
  title: "Components/Button",
  component: Button,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
  argTypes: {
    onClick: { action: "clicked" },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

// Each named export is a story
export const Primary: Story = {
  args: {
    variant: "primary",
    children: "Primary Button",
  },
};

export const Secondary: Story = {
  args: {
    variant: "secondary",
    children: "Secondary Button",
  },
};

export const Disabled: Story = {
  args: {
    variant: "primary",
    children: "Disabled Button",
    disabled: true,
  },
};
```

**Why good:** `satisfies Meta<typeof Button>` provides full type checking while allowing inference, stories are simple objects, `tags: ["autodocs"]` generates documentation automatically

---

### Pattern 2: Args and ArgTypes Configuration

Args define prop values for stories. ArgTypes configure controls in the Storybook UI.

#### ArgTypes Configuration

```typescript
const meta = {
  title: "Components/Card",
  component: Card,
  argTypes: {
    // Control type for enums
    variant: {
      control: { type: "select" },
      options: ["default", "outline", "filled"],
      description: "Visual variant of the card",
    },
    // Control type for booleans
    isLoading: {
      control: { type: "boolean" },
      description: "Shows loading skeleton",
    },
    // Control type for strings
    title: {
      control: { type: "text" },
      description: "Card title text",
    },
    // Range control for numbers
    padding: {
      control: { type: "range", min: 0, max: 64, step: 4 },
      description: "Padding in pixels",
    },
    // Color picker
    backgroundColor: {
      control: { type: "color" },
    },
    // Hide from controls
    internalId: {
      table: { disable: true },
    },
    // Action handler
    onClose: {
      action: "closed",
    },
  },
} satisfies Meta<typeof Card>;
```

#### Default Args

```typescript
const meta = {
  title: "Components/Input",
  component: Input,
  // Default args applied to all stories
  args: {
    placeholder: "Enter text...",
    disabled: false,
  },
} satisfies Meta<typeof Input>;

export default meta;
type Story = StoryObj<typeof meta>;

// Story inherits default args, only overrides what changes
export const Default: Story = {};

export const WithLabel: Story = {
  args: {
    label: "Email address",
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
  },
};
```

**Why good:** centralized defaults reduce duplication, argTypes provide interactive documentation, control types match prop types for intuitive editing

---

### Pattern 3: Decorators for Context

Decorators wrap stories with providers, layouts, or styling context.

#### Component-Level Decorators

```typescript
const meta = {
  title: "Components/Modal",
  component: Modal,
  decorators: [
    // Add padding around the story
    (Story) => (
      <div style={{ padding: "3rem" }}>
        <Story />
      </div>
    ),
    // Wrap with theme provider
    (Story) => (
      <ThemeProvider theme="light">
        <Story />
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof Modal>;
```

#### Global Decorators

```typescript
// .storybook/preview.tsx
import type { Preview } from "@storybook/react";
import { ThemeProvider } from "../src/theme-provider";

const preview: Preview = {
  decorators: [
    (Story) => (
      <ThemeProvider>
        <Story />
      </ThemeProvider>
    ),
  ],
};

export default preview;
```

#### Story-Level Decorators

```typescript
export const InDarkMode: Story = {
  decorators: [
    (Story) => (
      <div className="dark" style={{ background: "#1a1a1a", padding: "2rem" }}>
        <Story />
      </div>
    ),
  ],
  args: {
    children: "Dark Mode Button",
  },
};
```

**Why good:** decorators keep component code clean, global decorators ensure consistent context, story decorators allow specific variations

---

### Pattern 4: Parameters for Story Configuration

Parameters configure Storybook features and addons per story, component, or globally.

#### Common Parameters

```typescript
const meta = {
  title: "Components/Dialog",
  component: Dialog,
  parameters: {
    // Layout options: centered, fullscreen, padded
    layout: "centered",

    // Background options
    backgrounds: {
      default: "light",
      values: [
        { name: "light", value: "#ffffff" },
        { name: "dark", value: "#1a1a1a" },
        { name: "brand", value: "#0066ff" },
      ],
    },

    // Viewport configuration
    viewport: {
      defaultViewport: "mobile1",
    },

    // Disable specific controls panel
    controls: {
      expanded: true,
      sort: "requiredFirst",
    },

    // Documentation page order
    docs: {
      description: {
        component: "A modal dialog for user confirmations.",
      },
    },
  },
} satisfies Meta<typeof Dialog>;
```

#### Story-Specific Parameters

```typescript
export const MobileView: Story = {
  parameters: {
    viewport: {
      defaultViewport: "mobile1",
    },
    chromatic: {
      viewports: [320, 768],
    },
  },
};

export const FullPage: Story = {
  parameters: {
    layout: "fullscreen",
  },
};
```

**Why good:** parameters configure addon behavior declaratively, can be set at any level (global, component, story), consistent API across all addons

---

### Pattern 5: Play Functions for Interaction Testing

Play functions enable interaction testing within stories using the `@storybook/test` utilities.

#### Basic Interaction Testing

```typescript
import type { Meta, StoryObj } from "@storybook/react";
import { expect, fn, userEvent, within } from "@storybook/test";
import { LoginForm } from "./login-form";

const meta = {
  title: "Forms/LoginForm",
  component: LoginForm,
  args: {
    onSubmit: fn(),
  },
} satisfies Meta<typeof LoginForm>;

export default meta;
type Story = StoryObj<typeof meta>;

export const FilledForm: Story = {
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);

    // Find elements
    const emailInput = canvas.getByLabelText(/email/i);
    const passwordInput = canvas.getByLabelText(/password/i);
    const submitButton = canvas.getByRole("button", { name: /sign in/i });

    // Interact with form
    await userEvent.type(emailInput, "test@example.com");
    await userEvent.type(passwordInput, "password123");
    await userEvent.click(submitButton);

    // Assert callback was called
    await expect(args.onSubmit).toHaveBeenCalledWith({
      email: "test@example.com",
      password: "password123",
    });
  },
};
```

#### Composing Play Functions

```typescript
export const Default: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await expect(canvas.getByRole("button")).toBeInTheDocument();
  },
};

export const Clicked: Story = {
  play: async (context) => {
    // Run the Default story's play function first
    await Default.play?.(context);

    const canvas = within(context.canvasElement);
    const button = canvas.getByRole("button");

    await userEvent.click(button);
    await expect(button).toHaveAttribute("data-state", "pressed");
  },
};
```

See [examples/testing.md](examples/testing.md) for more play function patterns.

**Why good:** tests run in actual browser environment, reuses Testing Library queries for consistency, play functions double as documentation

---

### Pattern 6: Render Functions for Complex Stories

Use the `render` property when you need more control than `args` provides.

#### Custom Render Function

```typescript
export const WithMultipleItems: Story = {
  render: (args) => (
    <List>
      <ListItem {...args} title="First Item" />
      <ListItem {...args} title="Second Item" />
      <ListItem {...args} title="Third Item" />
    </List>
  ),
  args: {
    isSelected: false,
  },
};
```

#### Render with Hooks

```typescript
export const Controlled: Story = {
  render: function Render(args) {
    const [isOpen, setIsOpen] = useState(false);

    return (
      <div>
        <Button onClick={() => setIsOpen(true)}>Open Dialog</Button>
        <Dialog {...args} open={isOpen} onClose={() => setIsOpen(false)} />
      </div>
    );
  },
  args: {
    title: "Controlled Dialog",
  },
};
```

**Why good:** render functions allow complex compositions, named functions enable hooks, args still control individual props

---

### Pattern 7: Story Organization

Organize stories with a clear hierarchy that reflects your component structure.

#### Title Hierarchy

```typescript
// Organized by category
const meta = {
  title: "Components/Forms/Input", // Creates nested navigation
  component: Input,
} satisfies Meta<typeof Input>;

// Alternative structures:
// "Design System/Atoms/Button"
// "Pages/Dashboard/Header"
// "Features/Authentication/LoginForm"
```

#### Naming Conventions

```typescript
// Good: Descriptive story names
export const Default: Story = {};
export const WithIcon: Story = {};
export const Disabled: Story = {};
export const Loading: Story = {};
export const WithValidationError: Story = {};

// Bad: Unclear names
export const Story1: Story = {};
export const Test: Story = {};
```

#### Story Order

```typescript
const meta = {
  title: "Components/Button",
  component: Button,
  parameters: {
    docs: {
      // Control story order in docs
      page: () => (
        <>
          <Title />
          <Subtitle />
          <Description />
          <Primary />
          <Controls />
          <Stories />
        </>
      ),
    },
  },
} satisfies Meta<typeof Button>;
```

**Why good:** hierarchical titles create intuitive navigation, descriptive names serve as documentation, consistent patterns across the codebase

</patterns>

---

<integration>

## Integration Guide

**Works with your component framework:**

- Stories import and render your actual components
- TypeScript types flow from component props to story args
- Same styling solution (CSS modules, Tailwind) works in Storybook

**Works with your testing tools:**

- Play functions use Testing Library queries (same as RTL)
- Stories can be imported as test fixtures in Vitest/Jest
- Visual testing tools (Chromatic) use stories as test cases

**Works with your CI/CD:**

- `build-storybook` creates static site for deployment
- Storybook Test runner integrates with CI for interaction tests
- Visual regression tools integrate via CI

**Styling boundary:**

- Storybook handles: component isolation, documentation, controls
- Your styling skill handles: actual CSS implementation

**Testing boundary:**

- Storybook handles: component interaction testing, visual states
- Your E2E skill handles: full user journeys, navigation flows

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Using default export for stories** - Default export is reserved for meta; stories must be named exports
- **Hardcoding props in JSX instead of using args** - Defeats the purpose of controls; makes stories non-interactive
- **Missing `component` property in meta** - Stories won't render correctly; autodocs won't work
- **Using `fireEvent` instead of `userEvent` in play functions** - Doesn't simulate real user behavior
- **Importing from `@storybook/testing-library`** - Deprecated; use `@storybook/test` instead
- **Using `argTypesRegex` for play function handlers** - Implicit actions cannot be used in play functions; use explicit `fn()`

**Medium Priority Issues:**

- **Not using `satisfies Meta<typeof Component>`** - Loses type safety on story args
- **Putting business logic in play functions** - Play functions are for interaction, not logic testing
- **Missing `tags: ["autodocs"]`** - Won't generate automatic documentation
- **Overly complex render functions** - If render is complex, component API may need refactoring

**Common Mistakes:**

- Forgetting to `await` userEvent actions in play functions
- Using `any` type instead of `StoryObj<typeof meta>`
- Not setting up global decorators for providers (ThemeProvider, etc.)
- Putting test assertions in stories without play functions

**Gotchas & Edge Cases:**

- `args` are serializable - functions must use `action` or `fn()` from `@storybook/test`
- Play functions run after render - use `waitFor` for async content
- Decorators run outermost to innermost - order matters for context
- `canvas.getByRole` uses Testing Library - same accessibility rules apply
- Hot reload preserves args state - may need manual refresh for some changes
- Storybook 8 uses `react-docgen` by default (not `react-docgen-typescript`) - imported types may not be extracted
- In Storybook 8.2+, use `initialGlobals` instead of deprecated `globals` in preview.ts
- Built-in tags: `dev` (sidebar visibility), `test` (test inclusion), `autodocs` (docs generation) - use `!tag` to remove inherited tags
- Vitest addon (8.4+) is recommended over test-runner for Vite projects - provides Storybook UI integration

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use CSF 3.0 format with `satisfies Meta<typeof Component>` for type-safe story metadata)**

**(You MUST define a default `meta` export with `component` property - stories without `component` won't render)**

**(You MUST use `args` for defining props - NOT rendering components with hardcoded props)**

**(You MUST use play functions with `@storybook/test` utilities for interaction testing - NOT custom event firing)**

**(You MUST use named exports for stories - default export is reserved for meta object)**

**Failure to follow these rules will produce untestable stories, missing documentation, and broken controls.**

</critical_reminders>
