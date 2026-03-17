---
description: Use this skill when the user asks to "set up testing", "configure tests for Storybook", "add interaction tests", "add accessibility tests", "set up a11y testing", "configure Vitest", "configure Playwright", mentions "play functions", "test-storybook", "component testing", or wants to add comprehensive testing to their Storybook setup. This skill provides guidance on modern Storybook 10 testing with Vitest, Playwright, and axe-core.
---

# Testing Suite Skill

## Overview

Set up and configure comprehensive testing for Storybook 10 components, including interaction tests with play functions, accessibility testing with axe-core, and visual regression testing with Playwright.

This skill provides guidance on implementing modern component testing patterns using Storybook 10's integrated testing capabilities.

## What This Skill Provides

### Testing Strategy Guidance
Configure the right testing setup based on:
- **Project requirements**: Unit, integration, or end-to-end testing
- **Framework choice**: React Testing Library, Vue Testing Library, Svelte Testing Library
- **Testing scope**: Interaction tests, accessibility, visual regression
- **CI/CD integration**: GitHub Actions, GitLab CI, CircleCI

### Interaction Testing
Set up and write interaction tests using:
- **Play functions**: Simulate user interactions in stories
- **Testing Library**: Query elements by role, text, label
- **User events**: Click, type, keyboard, hover, focus
- **Assertions**: Verify component behavior and state

### Accessibility Testing
Configure accessibility validation with:
- **axe-core integration**: WCAG 2.1 compliance checking
- **ARIA validation**: Roles, labels, descriptions
- **Keyboard navigation**: Tab order, focus management
- **Screen reader support**: Semantic HTML, announcements
- **Color contrast**: WCAG AA/AAA compliance

### Visual Regression Testing
Set up visual regression tests with:
- **Playwright integration**: Real browser screenshots
- **Snapshot comparisons**: Detect unintended visual changes
- **Cross-browser testing**: Chromium, Firefox, WebKit
- **Responsive testing**: Multiple viewport sizes

## Testing Levels

### Level 1: Basic Stories
Stories with args and controls only (no automated tests).

**Best for:**
- Component showcases
- Design system documentation
- Quick prototyping

**Setup:**
```typescript
export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Button',
  },
};
```

### Level 2: Interaction Tests
Stories with play functions that test user interactions.

**Best for:**
- Form components
- Interactive widgets
- State management verification

**Setup:**
```typescript
import { expect, userEvent, within } from 'storybook/test';

export const WithInteraction: Story = {
  args: { children: 'Click me' },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    await expect(button).toBeInTheDocument();
    await userEvent.click(button);
    await expect(button).toHaveFocus();
  },
};
```

### Level 3: Accessibility Tests
Stories with axe-core validation rules.

**Best for:**
- Public-facing applications
- Compliance requirements (WCAG 2.1)
- Accessible component libraries

**Setup:**
```typescript
export const AccessibilityValidation: Story = {
  args: { children: 'Button' },
  parameters: {
    a11y: {
      config: {
        rules: [
          { id: 'button-name', enabled: true },
          { id: 'color-contrast', enabled: true },
          { id: 'focus-visible', enabled: true },
        ],
      },
    },
  },
};
```

### Level 4: Full Testing Suite
Combination of interaction tests, accessibility tests, and visual regression.

**Best for:**
- Production applications
- Component libraries
- Critical user flows

## Storybook 10 Testing Features

### Vitest Integration
Storybook 10 uses Vitest as the default test runner:

**Benefits:**
- ⚡ Fast: Runs in real browsers (not JSDOM)
- 📦 Zero config: Works out of the box
- 🎯 Isolated: Each story runs in isolation
- 🔄 Watch mode: Instant feedback on changes

**Setup:**
Add to `package.json`:
```json
{
  "scripts": {
    "test-storybook": "test-storybook"
  }
}
```

### Portable Stories

Run stories directly in unit tests (Vitest/Jest) - perfect for reusable component libraries.

**Why use it:**
- Reuse stories as test cases (no duplication)
- Args, decorators, play functions work automatically
- Test outside Storybook in CI pipelines
- Share components across projects with tests included

**Setup:**
```typescript
// Button.test.tsx
import { composeStories } from '@storybook/react';
import { render, screen } from '@testing-library/react';
import * as stories from './Button.stories';

// Convert all stories to testable components
const { Primary, Disabled, WithIcon } = composeStories(stories);

describe('Button', () => {
  it('renders primary variant', () => {
    render(<Primary />);
    expect(screen.getByRole('button')).toHaveClass('btn-primary');
  });

  it('runs interaction test from story', async () => {
    const { container } = render(<WithIcon />);

    // Play function from story runs automatically
    await WithIcon.play?.({ canvasElement: container });

    expect(screen.getByRole('button')).toHaveFocus();
  });

  it('respects disabled state', () => {
    render(<Disabled />);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

**Single story:**
```typescript
import { composeStory } from '@storybook/react';
import meta, { Primary } from './Button.stories';

const PrimaryButton = composeStory(Primary, meta);

test('primary button', () => {
  render(<PrimaryButton />);
  // Test with all decorators and args applied
});
```

**With custom args override:**
```typescript
const { Primary } = composeStories(stories);

test('custom label', () => {
  render(<Primary>Custom Text</Primary>);
  expect(screen.getByText('Custom Text')).toBeInTheDocument();
});
```

### Playwright Integration
Real browser testing with Playwright:

**Benefits:**
- 🌐 Real browsers: Chromium, Firefox, WebKit
- 📸 Screenshots: Visual regression testing
- 🎬 Video recording: Debug test failures
- 🔍 Tracing: Step-by-step execution

**Setup:**
Storybook 10 includes Playwright by default. Configure in `.storybook/test-runner-jest.config.js`:

```javascript
export default {
  browsers: ['chromium', 'firefox', 'webkit'],
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
};
```

### Testing Library Integration
Query components using accessible selectors:

**Recommended queries (in order of preference):**
1. `getByRole()` - Semantic HTML roles
2. `getByLabelText()` - Form labels
3. `getByPlaceholderText()` - Input placeholders
4. `getByText()` - Visible text content
5. `getByTestId()` - Last resort only

**Example:**
```typescript
const button = canvas.getByRole('button', { name: /submit/i });
const input = canvas.getByLabelText('Email address');
const heading = canvas.getByRole('heading', { level: 1 });
```

## Common Test Patterns

### Button Component Tests
```typescript
export const ButtonInteraction: Story = {
  args: {
    onClick: fn(),
    children: 'Click me',
  },
  play: async ({ args, canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    // Test rendering
    await expect(button).toBeInTheDocument();

    // Test click
    await userEvent.click(button);
    await expect(args.onClick).toHaveBeenCalledTimes(1);

    // Test disabled state
    await expect(button).not.toBeDisabled();
  },
};
```

### Input Component Tests
```typescript
export const InputInteraction: Story = {
  args: {
    label: 'Username',
    onChange: fn(),
  },
  play: async ({ args, canvasElement }) => {
    const canvas = within(canvasElement);
    const input = canvas.getByLabelText('Username');

    // Test typing
    await userEvent.type(input, 'john.doe');
    await expect(input).toHaveValue('john.doe');

    // Test change handler
    await expect(args.onChange).toHaveBeenCalled();

    // Test validation
    await userEvent.clear(input);
    await expect(input).toHaveValue('');
  },
};
```

### Modal Component Tests
```typescript
export const ModalInteraction: Story = {
  args: {
    isOpen: true,
    onClose: fn(),
    title: 'Confirm Action',
  },
  play: async ({ args, canvasElement }) => {
    const canvas = within(canvasElement);
    const dialog = canvas.getByRole('dialog');

    // Test ARIA attributes
    await expect(dialog).toHaveAttribute('aria-modal', 'true');

    // Test focus trap
    const firstButton = canvas.getAllByRole('button')[0];
    firstButton.focus();
    await expect(firstButton).toHaveFocus();

    // Test ESC key
    await userEvent.keyboard('{Escape}');
    await expect(args.onClose).toHaveBeenCalled();
  },
};
```

### Form Component Tests
```typescript
export const FormInteraction: Story = {
  args: {
    onSubmit: fn(),
  },
  play: async ({ args, canvasElement }) => {
    const canvas = within(canvasElement);

    // Fill form
    await userEvent.type(canvas.getByLabelText('Email'), 'test@example.com');
    await userEvent.type(canvas.getByLabelText('Password'), 'password123');

    // Submit
    await userEvent.click(canvas.getByRole('button', { name: /submit/i }));

    // Verify submission
    await expect(args.onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  },
};
```

## Accessibility Test Patterns

### WCAG 2.1 AA Compliance
```typescript
export const WCAG_AA_Compliance: Story = {
  parameters: {
    a11y: {
      config: {
        rules: [
          // Perceivable
          { id: 'color-contrast', enabled: true }, // 1.4.3
          { id: 'image-alt', enabled: true }, // 1.1.1

          // Operable
          { id: 'button-name', enabled: true }, // 4.1.2
          { id: 'link-name', enabled: true }, // 4.1.2
          { id: 'focus-visible', enabled: true }, // 2.4.7

          // Understandable
          { id: 'label', enabled: true }, // 3.3.2
          { id: 'valid-lang', enabled: true }, // 3.1.1

          // Robust
          { id: 'aria-valid-attr', enabled: true }, // 4.1.2
          { id: 'aria-hidden-focus', enabled: true }, // 4.1.2
        ],
      },
    },
  },
};
```

### Keyboard Navigation Tests
```typescript
export const KeyboardNavigation: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Tab through interactive elements
    await userEvent.tab();
    const firstButton = canvas.getAllByRole('button')[0];
    await expect(firstButton).toHaveFocus();

    // Activate with Enter
    await userEvent.keyboard('{Enter}');

    // Activate with Space
    await userEvent.keyboard(' ');

    // Navigate with arrows (for radio/tabs)
    await userEvent.keyboard('{ArrowRight}');
  },
};
```

## Running Tests

### Local Development
```bash
# Run all tests
npm run test-storybook

# Run specific story
npm run test-storybook -- --stories "Button/WithInteraction"

# Watch mode
npm run test-storybook -- --watch

# Debug mode
npm run test-storybook -- --debug
```

### CI/CD Integration
Add to GitHub Actions:
```yaml
name: Storybook Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm ci
      - run: npm run build-storybook
      - run: npm run test-storybook
```

## Test Coverage

Storybook 10 includes V8 coverage (faster than Istanbul):

```json
{
  "scripts": {
    "test-storybook": "test-storybook --coverage",
    "test-storybook:ci": "test-storybook --coverage --coverageReporters=lcov"
  }
}
```

View coverage report:
```bash
npm run test-storybook -- --coverage
# Coverage report: coverage/lcov-report/index.html
```

## Best Practices

### Do's ✅
- Use `getByRole()` for semantic queries
- Test user behavior, not implementation
- Keep tests focused and isolated
- Use meaningful test descriptions
- Test keyboard navigation
- Validate ARIA attributes
- Check color contrast
- Test error states

### Don'ts ❌
- Don't use `getByTestId()` unless necessary
- Don't test internal state
- Don't duplicate tests across stories
- Don't skip accessibility tests
- Don't hardcode timeouts
- Don't ignore flaky tests

## Troubleshooting

### Tests Timing Out
Increase timeout in story:
```typescript
export const SlowLoading: Story = {
  parameters: {
    test: {
      timeout: 10000, // 10 seconds
    },
  },
};
```

### Elements Not Found
Use `findBy` queries for async elements:
```typescript
const button = await canvas.findByRole('button'); // Waits up to 1s
```

### Flaky Tests
Add explicit waits:
```typescript
await waitFor(() => {
  expect(canvas.getByText('Loaded')).toBeInTheDocument();
});
```

## Related Skills

- **story-generation**: Generates stories with tests automatically
- **component-scaffold**: Creates components with test-ready stories

## References

- Storybook Testing Handbook: https://storybook.js.org/docs/writing-tests
- Testing Library Docs: https://testing-library.com/docs/queries/about
- axe-core Rules: https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
