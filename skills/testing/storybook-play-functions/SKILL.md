---
name: storybook-play-functions
description: Use when adding interaction testing to Storybook stories. Enables automated testing of component behavior, user interactions, and state changes directly in stories.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Storybook - Play Functions

Write automated interaction tests within stories using play functions to verify component behavior, simulate user actions, and test edge cases.

## Key Concepts

### Play Functions

Play functions run after a story renders, allowing you to simulate user interactions:

```typescript
import { within, userEvent, expect } from '@storybook/test';
import type { Meta, StoryObj } from '@storybook/react';
import { LoginForm } from './LoginForm';

const meta = {
  component: LoginForm,
} satisfies Meta<typeof LoginForm>;

export default meta;
type Story = StoryObj<typeof meta>;

export const FilledForm: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    await userEvent.type(canvas.getByLabelText('Email'), 'user@example.com');
    await userEvent.type(canvas.getByLabelText('Password'), 'password123');
    await userEvent.click(canvas.getByRole('button', { name: /submit/i }));

    await expect(canvas.getByText('Welcome!')).toBeInTheDocument();
  },
};
```

### Testing Library Integration

Storybook integrates with Testing Library for queries and interactions:

- `within(canvasElement)` - Scopes queries to the story
- `userEvent` - Simulates realistic user interactions
- `expect` - Jest-compatible assertions
- `waitFor` - Waits for async changes

### Test Execution

Play functions execute:

- When viewing a story in Storybook
- During visual regression testing
- In test runners for automated testing
- On story hot-reload during development

## Best Practices

### 1. Use Testing Library Queries

Use semantic queries to find elements:

```typescript
export const SearchFlow: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Good - Semantic queries
    const searchInput = canvas.getByRole('searchbox');
    const submitButton = canvas.getByRole('button', { name: /search/i });
    const results = canvas.getByRole('list', { name: /results/i });

    await userEvent.type(searchInput, 'storybook');
    await userEvent.click(submitButton);

    await expect(results).toBeInTheDocument();
  },
};
```

### 2. Simulate Realistic User Behavior

Use `userEvent` for realistic interactions:

```typescript
import { userEvent } from '@storybook/test';

export const FormInteraction: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Type naturally with delay
    await userEvent.type(canvas.getByLabelText('Name'), 'John Doe', {
      delay: 100,
    });

    // Tab between fields
    await userEvent.tab();

    // Select from dropdown
    await userEvent.selectOptions(
      canvas.getByLabelText('Country'),
      'United States'
    );

    // Click submit
    await userEvent.click(canvas.getByRole('button', { name: /submit/i }));
  },
};
```

### 3. Test Async Behavior

Use `waitFor` for async state changes:

```typescript
import { waitFor } from '@storybook/test';

export const AsyncData: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    await userEvent.click(canvas.getByRole('button', { name: /load data/i }));

    // Wait for loading state
    await waitFor(() => {
      expect(canvas.getByText('Loading...')).toBeInTheDocument();
    });

    // Wait for data to appear
    await waitFor(
      () => {
        expect(canvas.getByRole('list')).toBeInTheDocument();
        expect(canvas.getAllByRole('listitem')).toHaveLength(5);
      },
      { timeout: 3000 }
    );
  },
};
```

### 4. Test Error States

Validate error handling and validation:

```typescript
export const ValidationErrors: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Submit empty form
    await userEvent.click(canvas.getByRole('button', { name: /submit/i }));

    // Verify error messages
    await expect(canvas.getByText('Email is required')).toBeInTheDocument();
    await expect(canvas.getByText('Password is required')).toBeInTheDocument();

    // Fill only email
    await userEvent.type(canvas.getByLabelText('Email'), 'invalid-email');
    await userEvent.click(canvas.getByRole('button', { name: /submit/i }));

    // Verify email validation
    await expect(canvas.getByText('Email is invalid')).toBeInTheDocument();
  },
};
```

### 5. Compose Complex Scenarios

Break complex interactions into steps:

```typescript
export const CheckoutFlow: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Step 1: Add items to cart
    await userEvent.click(canvas.getByRole('button', { name: /add to cart/i }));
    await expect(canvas.getByText('1 item in cart')).toBeInTheDocument();

    // Step 2: Proceed to checkout
    await userEvent.click(canvas.getByRole('button', { name: /checkout/i }));
    await expect(canvas.getByRole('heading', { name: /checkout/i })).toBeInTheDocument();

    // Step 3: Fill shipping info
    await userEvent.type(canvas.getByLabelText('Address'), '123 Main St');
    await userEvent.type(canvas.getByLabelText('City'), 'New York');
    await userEvent.selectOptions(canvas.getByLabelText('State'), 'NY');

    // Step 4: Submit order
    await userEvent.click(canvas.getByRole('button', { name: /place order/i }));
    await waitFor(() => {
      expect(canvas.getByText('Order confirmed!')).toBeInTheDocument();
    });
  },
};
```

## Common Patterns

### Modal Interactions

```typescript
export const OpenModal: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Modal not visible initially
    expect(canvas.queryByRole('dialog')).not.toBeInTheDocument();

    // Click trigger
    await userEvent.click(canvas.getByRole('button', { name: /open/i }));

    // Modal appears
    const modal = canvas.getByRole('dialog');
    await expect(modal).toBeInTheDocument();

    // Close modal
    await userEvent.click(within(modal).getByRole('button', { name: /close/i }));

    // Modal disappears
    await waitFor(() => {
      expect(canvas.queryByRole('dialog')).not.toBeInTheDocument();
    });
  },
};
```

### Keyboard Navigation

```typescript
export const KeyboardNav: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    const firstItem = canvas.getAllByRole('menuitem')[0];
    firstItem.focus();

    // Navigate with arrow keys
    await userEvent.keyboard('{ArrowDown}');
    await expect(canvas.getAllByRole('menuitem')[1]).toHaveFocus();

    await userEvent.keyboard('{ArrowDown}');
    await expect(canvas.getAllByRole('menuitem')[2]).toHaveFocus();

    // Select with Enter
    await userEvent.keyboard('{Enter}');
    await expect(canvas.getByText('Item 3 selected')).toBeInTheDocument();

    // Close with Escape
    await userEvent.keyboard('{Escape}');
    await waitFor(() => {
      expect(canvas.queryByRole('menu')).not.toBeInTheDocument();
    });
  },
};
```

### Multi-Step Forms

```typescript
export const Wizard: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Step 1
    await userEvent.type(canvas.getByLabelText('First Name'), 'John');
    await userEvent.type(canvas.getByLabelText('Last Name'), 'Doe');
    await userEvent.click(canvas.getByRole('button', { name: /next/i }));

    // Step 2
    await expect(canvas.getByText('Step 2 of 3')).toBeInTheDocument();
    await userEvent.type(canvas.getByLabelText('Email'), 'john@example.com');
    await userEvent.click(canvas.getByRole('button', { name: /next/i }));

    // Step 3
    await expect(canvas.getByText('Step 3 of 3')).toBeInTheDocument();
    await userEvent.click(canvas.getByRole('checkbox', { name: /agree/i }));
    await userEvent.click(canvas.getByRole('button', { name: /submit/i }));

    // Success
    await waitFor(() => {
      expect(canvas.getByText('Registration complete!')).toBeInTheDocument();
    });
  },
};
```

### Drag and Drop

```typescript
export const DragDrop: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    const draggable = canvas.getByRole('button', { name: /drag me/i });
    const dropzone = canvas.getByRole('region', { name: /drop zone/i });

    // Perform drag and drop
    await userEvent.pointer([
      { keys: '[MouseLeft>]', target: draggable },
      { coords: { x: 100, y: 100 } },
      { target: dropzone },
      { keys: '[/MouseLeft]' },
    ]);

    await expect(canvas.getByText('Item dropped!')).toBeInTheDocument();
  },
};
```

### File Upload

```typescript
export const FileUpload: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    const file = new File(['content'], 'test.txt', { type: 'text/plain' });
    const input = canvas.getByLabelText('Upload file');

    await userEvent.upload(input, file);

    await expect(canvas.getByText('test.txt')).toBeInTheDocument();
    await expect(canvas.getByText('1 file selected')).toBeInTheDocument();
  },
};
```

## Advanced Patterns

### Reusable Play Functions

```typescript
// helpers.ts
export async function login(canvas: ReturnType<typeof within>) {
  await userEvent.type(canvas.getByLabelText('Email'), 'user@example.com');
  await userEvent.type(canvas.getByLabelText('Password'), 'password123');
  await userEvent.click(canvas.getByRole('button', { name: /login/i }));
}

// Story.stories.tsx
export const AfterLogin: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await login(canvas);

    // Test authenticated state
    await expect(canvas.getByText('Welcome, User!')).toBeInTheDocument();
  },
};
```

### Step-Through Testing

```typescript
import { step } from '@storybook/test';

export const MultiStep: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    await step('Fill in personal info', async () => {
      await userEvent.type(canvas.getByLabelText('Name'), 'John Doe');
      await userEvent.type(canvas.getByLabelText('Email'), 'john@example.com');
    });

    await step('Select preferences', async () => {
      await userEvent.click(canvas.getByLabelText('Subscribe to newsletter'));
      await userEvent.selectOptions(canvas.getByLabelText('Theme'), 'dark');
    });

    await step('Submit form', async () => {
      await userEvent.click(canvas.getByRole('button', { name: /submit/i }));
      await expect(canvas.getByText('Success!')).toBeInTheDocument();
    });
  },
};
```

## Anti-Patterns

### ❌ Don't Use Direct DOM Manipulation

```typescript
// Bad
export const Bad: Story = {
  play: async ({ canvasElement }) => {
    const input = canvasElement.querySelector('input');
    input.value = 'text';
    input.dispatchEvent(new Event('input'));
  },
};
```

```typescript
// Good
export const Good: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.type(canvas.getByRole('textbox'), 'text');
  },
};
```

### ❌ Don't Forget Async/Await

```typescript
// Bad - Missing await
export const Bad: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    userEvent.click(canvas.getByRole('button'));  // Won't work!
    expect(canvas.getByText('Clicked')).toBeInTheDocument();
  },
};
```

```typescript
// Good
export const Good: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.click(canvas.getByRole('button'));
    await expect(canvas.getByText('Clicked')).toBeInTheDocument();
  },
};
```

### ❌ Don't Use Brittle Selectors

```typescript
// Bad - Fragile selectors
export const Bad: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.click(canvas.getByText('Submit'));  // Breaks if text changes
  },
};
```

```typescript
// Good - Semantic selectors
export const Good: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.click(canvas.getByRole('button', { name: /submit/i }));
  },
};
```

## Related Skills

- **storybook-story-writing**: Creating stories to test with play functions
- **storybook-args-controls**: Using args to test different component states
- **storybook-configuration**: Setting up test runner for automated testing
