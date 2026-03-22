---
description:
  Create, update, or validate Storybook stories with comprehensive play
  functions
argument-hint: create|update|validate ComponentName [details]
---

# Writing Stories Skill

You are a Nimbus story specialist. This skill helps you create, update, or
validate Storybook stories (`*.stories.tsx`) with comprehensive play functions
for testing component behavior.

## Critical Requirements

**Stories are BOTH documentation AND tests.** Every interactive component MUST
have play functions that test user interactions, state changes, and
accessibility.

## Mode Detection

Parse the request to determine the operation:

- **create** - Generate new story file with complete test coverage
- **update** - Add stories, enhance play functions, or modify existing tests
- **validate** - Check story compliance with guidelines and test coverage

If no mode is specified, default to **create**.

## Required Research (All Modes)

Before implementation, you MUST research in parallel:

1. **Read** story guidelines and type matrix:

   ```bash
   cat docs/file-type-guidelines/stories.md
   ```

2. **Analyze** component characteristics to determine story type

3. **Review** similar story implementations:
   ```bash
   ls packages/nimbus/src/components/*/*.stories.tsx
   ```

## Story Requirements by Component Type

You MUST determine which story types are needed based on component category. See
docs/file-type-guidelines/stories.md for the complete story type matrix and
decision flowchart.

Quick reference:

- **Simple components**: Base, Sizes, Variants, Disabled, SmokeTest
- **Form components**: Add Required, Invalid, Controlled stories
- **Interactive components**: Add KeyboardNavigation, Controlled stories
- **Portal components**: Add Placement, Dismissal stories with special portal
  testing patterns

## File Structure

### Story File Template

```typescript
import type { Meta, StoryObj } from "@storybook/react-vite";
import { userEvent, within, expect, waitFor, fn } from "storybook/test";
import { ComponentName } from "@commercetools/nimbus";

const meta: Meta<typeof ComponentName> = {
  title: "Components/ComponentName", // StartCase, organized by category
  component: ComponentName,
  parameters: {
    layout: "centered", // or "fullscreen", "padded"
  },
  tags: ["autodocs"],
  argTypes: {
    // Define controls for props
    variant: {
      control: { type: "select" },
      options: ["solid", "outline", "ghost"],
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

// Stories follow below...
```

### Story Organization (REQUIRED)

Stories MUST be exported in this order:

1. **Base/Default** - Simplest usage, first story
2. **Sizes** - Size variants (if applicable)
3. **Variants** - Visual variants (if applicable)
4. **States** - Disabled, Invalid, Required, etc.
5. **Controlled** - Controlled state example
6. **Complex** - Advanced scenarios, edge cases
7. **SmokeTest** - Comprehensive matrix (last story)

## Create Mode

### Step 1: Component Analysis

You MUST analyze:

- Component props and variants
- Interactive behavior (click, type, keyboard nav)
- State management (controlled vs uncontrolled)
- Portal content (overlays, dropdowns)
- Accessibility requirements

### Step 2: Story Templates

#### Base Story (REQUIRED)

```typescript
export const Base: Story = {
  args: {
    children: "Button",
    onPress: fn(),
    ["data-testid"]: "test",
    ["aria-label"]: "test-button",
  },
  play: async ({ canvasElement, args, step }) => {
    const canvas = within(canvasElement);
    const element = canvas.getByTestId("test");

    await step("Test description of what's being tested", async () => {
      await expect(element).toBeInTheDocument();
      // Test specific behavior
    });

    await step("Test interaction", async () => {
      await userEvent.click(element);
      await expect(args.onPress).toHaveBeenCalledTimes(1);
    });

    await step("Test keyboard accessibility", async () => {
      await userEvent.tab();
      await expect(element).toHaveFocus();
      await userEvent.keyboard("{Enter}");
      await expect(args.onPress).toHaveBeenCalledTimes(2);
    });
  },
};
```

#### Sizes Story (REQUIRED if component has sizes)

```typescript
const sizes: ComponentProps["size"][] = ["sm", "md", "lg"];

export const Sizes: Story = {
  args: {
    children: "Demo",
  },
  render: (args) => {
    return (
      <Stack direction="row" gap="400" alignItems="center">
        {sizes.map((size) => (
          <ComponentName key={size} {...args} size={size} />
        ))}
      </Stack>
    );
  },
};
```

#### Variants Story (REQUIRED if component has variants)

```typescript
const variants: ComponentProps["variant"][] = ["solid", "outline", "ghost"];

export const Variants: Story = {
  args: {
    children: "Demo",
  },
  render: (args) => {
    return (
      <Stack direction="row" gap="400" alignItems="center">
        {variants.map((variant) => (
          <ComponentName key={variant} {...args} variant={variant} />
        ))}
      </Stack>
    );
  },
};
```

#### Disabled Story (REQUIRED for interactive components)

```typescript
export const Disabled: Story = {
  args: {
    isDisabled: true,
    ["data-testid"]: "test",
  },
  play: async ({ canvasElement, step }) => {
    const canvas = within(canvasElement);
    const element = canvas.getByTestId("test");

    await step("Cannot be clicked", async () => {
      await userEvent.click(element);
      // Verify no action occurred
    });

    await step("Cannot be focused", async () => {
      await userEvent.tab();
      await expect(element).not.toHaveFocus();
    });
  },
};
```

#### Controlled Story (REQUIRED for stateful components)

```typescript
export const Controlled: Story = {
  render: () => {
    const [value, setValue] = useState("");

    return (
      <Stack gap="400">
        <ComponentName value={value} onChange={setValue} />
        <Text data-testid="value-display">Current value: {value}</Text>
      </Stack>
    );
  },
  play: async ({ canvasElement, step }) => {
    const canvas = within(canvasElement);
    const input = canvas.getByRole("textbox");
    const valueDisplay = canvas.getByTestId("value-display");

    await step("Updates controlled value", async () => {
      await userEvent.type(input, "Hello");
      await expect(input).toHaveValue("Hello");
      await expect(valueDisplay).toHaveTextContent("Current value: Hello");
    });
  },
};
```

#### SmokeTest Story (REQUIRED)

```typescript
export const SmokeTest: Story = {
  args: {
    children: "Demo",
    ["data-testid"]: "test",
  },
  render: (args) => {
    return (
      <Stack gap="600">
        {sizes.map((size) => (
          <Stack key={size} direction="row" gap="400">
            {variants.map((variant) => (
              <ComponentName
                key={variant}
                {...args}
                size={size}
                variant={variant}
              />
            ))}
          </Stack>
        ))}
      </Stack>
    );
  },
};
```

### Step 3: Portal Content Handling

For components that render portal content (Dialog, Menu, Popover, Select):

```typescript
export const PortalExample: Story = {
  play: async ({ canvasElement, step }) => {
    // CRITICAL: Use parent element to capture portal content
    const canvas = within(
      (canvasElement.parentNode as HTMLElement) ?? canvasElement
    );

    await step("Open portal content", async () => {
      const trigger = canvas.getByRole("button");
      await userEvent.click(trigger);

      // Wait for portal content to appear
      await waitFor(() => {
        expect(canvas.getByRole("dialog")).toBeInTheDocument();
      });
    });
  },
};
```

## Play Function Patterns (CRITICAL)

### Structure Requirements

You MUST use this structure:

```typescript
play: async ({ canvasElement, args, step }) => {
  const canvas = within(canvasElement); // or parent for portals

  await step("Descriptive test name", async () => {
    // Test implementation
  });

  await step("Next test", async () => {
    // Test implementation
  });
};
```

### Query Strategy

**Prefer accessible queries (in order of preference):**

1. `canvas.getByRole()` - BEST for interactive elements
2. `canvas.getByLabelText()` - BEST for form inputs
3. `canvas.getByTestId()` - Use sparingly for non-interactive elements
4. `document.querySelector()` - ONLY for portal content when necessary

### Interaction Patterns

#### Click Testing

```typescript
await step("Test click interaction", async () => {
  const button = canvas.getByRole("button");
  await userEvent.click(button);
  await expect(args.onClick).toHaveBeenCalledTimes(1);
});
```

#### Typing Testing

```typescript
await step("Test text input", async () => {
  const input = canvas.getByRole("textbox");
  await userEvent.type(input, "Test value");
  await expect(input).toHaveValue("Test value");

  await userEvent.clear(input);
  await expect(input).toHaveValue("");
});
```

#### Keyboard Navigation

```typescript
await step("Test keyboard navigation", async () => {
  const element = canvas.getByRole("button");

  // Tab to focus
  await userEvent.tab();
  await expect(element).toHaveFocus();

  // Enter to activate
  await userEvent.keyboard("{Enter}");
  await expect(args.onPress).toHaveBeenCalled();

  // Space to activate
  await userEvent.keyboard(" ");
  await expect(args.onPress).toHaveBeenCalledTimes(2);
});
```

#### Arrow Key Navigation (Menu, Select, etc.)

```typescript
await step("Test arrow key navigation", async () => {
  // Navigate down
  await userEvent.keyboard("{ArrowDown}");
  await waitFor(() => {
    const secondItem = canvas.getByRole("menuitem", { name: /Item 2/ });
    expect(secondItem).toHaveFocus();
  });

  // Navigate up
  await userEvent.keyboard("{ArrowUp}");
  await waitFor(() => {
    const firstItem = canvas.getByRole("menuitem", { name: /Item 1/ });
    expect(firstItem).toHaveFocus();
  });
});
```

#### Async Operations

```typescript
await step("Test async state changes", async () => {
  await userEvent.click(triggerButton);

  // Wait for async content to appear
  await waitFor(() => {
    expect(canvas.getByText("Loaded content")).toBeInTheDocument();
  });
});
```

### Accessibility Testing

You MUST test these accessibility features:

```typescript
await step("Test ARIA attributes", async () => {
  const element = canvas.getByRole("button");

  // Required attribute
  await expect(element).toHaveAttribute("aria-label", "Close");

  // Disabled state
  await expect(element).toHaveAttribute("aria-disabled", "true");

  // Invalid state
  await expect(element).toHaveAttribute("data-invalid", "true");
});

await step("Test focus management", async () => {
  // Initial focus
  const firstButton = canvas.getByRole("button", { name: "First" });
  await userEvent.tab();
  await expect(firstButton).toHaveFocus();

  // Focus restoration after dialog close
  await userEvent.keyboard("{Escape}");
  await waitFor(
    () => {
      expect(firstButton).toHaveFocus();
    },
    { timeout: 1000 }
  );
});
```

### State Verification

```typescript
await step("Verify state changes", async () => {
  const checkbox = canvas.getByRole("checkbox");

  // Initial state
  await expect(checkbox).not.toBeChecked();

  // After interaction
  await userEvent.click(checkbox);
  await expect(checkbox).toBeChecked();

  // Visual indication (data attributes)
  await expect(checkbox).toHaveAttribute("data-selected");
});
```

## Common Testing Patterns by Component Type

### Form Inputs (TextInput, Select, Checkbox)

**MUST test:**

- Initial render and attributes
- Focus with Tab
- Type/input value
- Clear value
- Required state (aria-required)
- Disabled state (cannot focus, cannot input)
- Invalid state (can still interact, has data-invalid)
- Controlled state synchronization

### Buttons (Button, IconButton, ToggleButton)

**MUST test:**

- Click interaction
- Focus with Tab
- Keyboard activation (Enter, Space)
- Disabled state (cannot focus, cannot activate)
- Visual variants render correctly

### Overlays (Dialog, Menu, Popover)

**MUST test:**

- Open via trigger
- Portal content appears (use parent element)
- Keyboard navigation inside overlay
- Escape key dismissal
- Focus restoration to trigger
- Backdrop click (if dismissable)

### Navigation (Pagination, Tabs)

**MUST test:**

- Navigation between items
- Keyboard navigation (Arrow keys, Home, End)
- Current item indication
- Disabled navigation buttons at boundaries
- Input validation (for direct input components)

### Selection (RadioGroup, CheckboxGroup, Select)

**MUST test:**

- Single selection (radio) - only one selected
- Multiple selection (checkbox) - multiple selected
- Selection change callbacks
- Keyboard selection (Space, Enter)
- Disabled options cannot be selected

## Update Mode

### Process

1. You MUST read the current story file
2. You MUST identify gaps in test coverage
3. You SHOULD preserve existing story structure
4. You MUST add missing required stories
5. You MUST enhance play functions with missing tests

### Common Updates

- **Add missing story** - Base, Disabled, Controlled, etc.
- **Enhance play function** - Add keyboard nav, accessibility tests
- **Add edge cases** - Boundary conditions, error states
- **Fix failing tests** - Update assertions, fix async timing

### Post-Update

You MUST verify the changes:

```bash
pnpm test:dev packages/nimbus/src/components/{component}/{component}.stories.tsx
```

## Validate Mode

### Validation Checklist

You MUST validate against these requirements:

#### File Structure

- [ ] Story file location:
      `packages/nimbus/src/components/{component}/{component}.stories.tsx`
- [ ] Imports from `@storybook/react-vite` and `storybook/test`
- [ ] Meta configuration with title, component, tags
- [ ] Default export of meta
- [ ] Story type from `StoryObj<typeof meta>`

#### Required Stories

- [ ] Base/Default story exists (MUST be first)
- [ ] Sizes story (if component has sizes)
- [ ] Variants story (if component has variants)
- [ ] Disabled story (for interactive components)
- [ ] Controlled story (for stateful components)
- [ ] SmokeTest story (MUST be last)

#### Play Functions (CRITICAL)

- [ ] ALL interactive components have play functions
- [ ] Uses `step()` for test organization
- [ ] Uses `within()` for scoped queries
- [ ] Uses `waitFor()` for async operations
- [ ] Tests keyboard navigation (Tab, Enter, Space, Arrows)
- [ ] Tests accessibility attributes (aria-_, data-_)
- [ ] Tests state changes and synchronization
- [ ] Tests disabled states (cannot focus, cannot interact)
- [ ] Tests edge cases and boundaries

#### Query Strategy

- [ ] Prefers `getByRole()` for interactive elements
- [ ] Uses `getByLabelText()` for form inputs
- [ ] Uses `getByTestId()` sparingly
- [ ] Portal content uses parent element access
- [ ] No hardcoded selectors without good reason

#### Test Coverage

- [ ] Initial render verified
- [ ] Focus management tested
- [ ] Click/press interactions tested
- [ ] Keyboard interactions tested
- [ ] State synchronization tested
- [ ] Async operations use waitFor
- [ ] Accessibility requirements verified

#### Story Organization

- [ ] Stories in prescribed order
- [ ] Clear, descriptive story names
- [ ] Consistent args usage
- [ ] Proper use of render function for variants

### Validation Report Format

```markdown
## Story Validation: {ComponentName}

### Status: [✅ PASS | ❌ FAIL | ⚠️ WARNING]

### Files Reviewed

- Story file: `{component}.stories.tsx`
- Guidelines: `docs/file-type-guidelines/stories.md`

### ✅ Compliant

[List passing checks]

### ❌ Violations (MUST FIX)

- [Violation with guideline reference and line number]

### ⚠️ Warnings (SHOULD FIX)

- [Non-critical improvements]

### Test Coverage

- Required Stories: [X/Y present]
- Play Functions: [X/Y stories have tests]
- Interaction Testing: [Complete | Partial | Missing]
- Accessibility Testing: [Complete | Partial | Missing]

### Recommendations

- [Specific improvements needed]
```

## Error Recovery

If tests fail:

1. You MUST check test syntax (async/await, expect calls)
2. You MUST verify element queries match actual DOM
3. You MUST check timing (use waitFor for async)
4. You MUST verify portal content uses parent element
5. You SHOULD add debugging steps (`console.log`, `screen.debug()`)

Common issues:

- Missing `waitFor()` for async operations
- Wrong query selectors
- Portal content not accessible (need parent element)
- Timing issues (interactions too fast)
- Missing `await` on async operations

## Clean Testing Patterns

You MUST follow the clean testing patterns documented in:

- **Storybook patterns**:
  `docs/file-type-guidelines/stories.md#clean-testing-patterns-storybook`
- **JSDOM patterns**:
  `docs/file-type-guidelines/unit-testing.md#clean-testing-patterns-jsdom`

Key requirements:

- Add `key` props when mapping arrays in render functions
- Use `userEvent.tab()` for focus management (not `element.focus()`)
- Await all `step()` calls including nested ones
- Add timing delays for React Aria keyboard sequences
- Provide `aria-label` for components without visible labels
- Initialize controlled inputs with defined values

## Reference Examples

You SHOULD reference these stories:

- **Simple**: `packages/nimbus/src/components/button/button.stories.tsx`
- **Form**: `packages/nimbus/src/components/text-input/text-input.stories.tsx`
- **Overlay**: `packages/nimbus/src/components/menu/menu.stories.tsx`
- **Complex**: `packages/nimbus/src/components/dialog/dialog.stories.tsx`
- **Selection**: `packages/nimbus/src/components/select/select.stories.tsx`

## RFC 2119 Key Words

- **MUST** / **REQUIRED** / **SHALL** - Absolute requirement
- **MUST NOT** / **SHALL NOT** - Absolute prohibition
- **SHOULD** / **RECOMMENDED** - Should do unless valid reason not to
- **SHOULD NOT** / **NOT RECOMMENDED** - Should not do unless valid reason
- **MAY** / **OPTIONAL** - Truly optional

---

**Execute story operation for: $ARGUMENTS**
