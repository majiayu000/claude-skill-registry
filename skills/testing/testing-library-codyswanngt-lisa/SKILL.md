---
name: testing-library
description: Enforces best practices for unit testing with Jest, @testing-library/react-native, and jest-expo in Expo projects. This skill should be used when writing, reviewing, or debugging unit tests to ensure tests are accessible, maintainable, and follow Testing Library guiding principles. Use this skill for test file creation, query selection, async handling, mocking patterns, and Expo Router testing.
---

# Testing Library Best Practices

## Overview

This skill enforces best practices for unit testing in Expo applications using Jest, `@testing-library/react-native`, and `jest-expo`. Tests should be **user-centric**, **accessible**, and **behavior-focused** rather than implementation-focused.

## Core Principles

### 1. Test User Behavior, Not Implementation

Focus on what the component does from a user's perspective, not how it achieves it internally.

```typescript
// Correct - tests visible behavior
expect(screen.getByRole("button", { name: "Submit" })).toBeEnabled();

// Incorrect - tests implementation details
expect(component.state.isSubmitting).toBe(false);
```

### 2. Use Accessible Queries

Queries should reflect how users and assistive technologies interact with the UI.

```typescript
// Correct - uses accessible role and name
screen.getByRole("button", { name: /save changes/i });

// Incorrect - relies on implementation detail
screen.getByTestId("save-btn");
```

### 3. One Assertion Per Behavior

Each test should verify one behavior. Multiple assertions are acceptable when verifying different aspects of the same behavior.

```typescript
// Correct - focused test
test("displays error message when submission fails", async () => {
  render(<Form />);
  await userEvent.press(screen.getByRole("button", { name: "Submit" }));
  expect(await screen.findByRole("alert")).toHaveTextContent("Failed");
});

// Incorrect - testing multiple behaviors
test("form works correctly", async () => {
  // Tests validation, submission, success, and error handling...
});
```

### 4. Prefer userEvent Over fireEvent

`userEvent` simulates realistic user interactions including the full event sequence.

```typescript
// Correct - realistic interaction
const user = userEvent.setup();
await user.press(screen.getByRole("button", { name: "Submit" }));

// Less ideal - simplified event
fireEvent.press(screen.getByRole("button", { name: "Submit" }));
```

## Query Priority

Choose queries based on accessibility, following this priority order:

| Priority | Query            | When to Use                             |
| -------- | ---------------- | --------------------------------------- |
| 1        | `getByRole`      | Interactive elements, headings, buttons |
| 2        | `getByLabelText` | Form fields with labels                 |
| 3        | `getByText`      | Non-interactive content, static text    |
| 4        | `getByTestId`    | Last resort when semantic queries fail  |

For detailed query patterns, see [references/query-priority.md](references/query-priority.md).

## Async Testing Patterns

### Use findBy for Async Assertions

```typescript
// Correct - waits for element to appear
expect(await screen.findByRole("alert")).toBeOnTheScreen();

// Incorrect - may fail if element appears async
expect(screen.getByRole("alert")).toBeOnTheScreen();
```

### Use waitFor for Side Effects

```typescript
// Correct - assertion inside waitFor
await waitFor(() => {
  expect(mockCallback).toHaveBeenCalledWith("success");
});

// Incorrect - side effect inside waitFor
await waitFor(() => {
  fireEvent.press(button); // Never do this
});
```

For comprehensive async patterns, see [references/async-patterns.md](references/async-patterns.md).

## Mocking Patterns

### Required Global Mocks

These must be configured in `jest/setup-jest.ts`:

```typescript
// AsyncStorage
jest.mock("@react-native-async-storage/async-storage", () =>
  require("@react-native-async-storage/async-storage/jest/async-storage-mock")
);

// Expo Fonts (to avoid async icon assertions)
jest.mock("expo-font", () => ({
  ...jest.requireActual("expo-font"),
  isLoaded: jest.fn(() => true),
}));
```

For complete mocking patterns, see [references/mocking-patterns.md](references/mocking-patterns.md).

## Expo Router Testing

Use `renderRouter` from `expo-router/testing-library` instead of `render` when testing components that use Expo Router.

```typescript
import { renderRouter, screen } from "expo-router/testing-library";

test("navigates to player detail", async () => {
  renderRouter({
    index: () => <PlayerList />,
    "players/[id]": () => <PlayerDetail />,
  });

  await userEvent.press(screen.getByRole("button", { name: "View Player" }));
  expect(screen).toHavePathname("/players/123");
});
```

For Expo Router testing details, see [references/expo-router-testing.md](references/expo-router-testing.md).

## Test Structure

### File Organization

- Place test files in `__tests__/` directories, not alongside source files
- Never place tests inside the `app/` directory (Expo Router constraint)
- Use `.test.ts` or `.test.tsx` extensions

### AAA Pattern

Structure every test with Arrange-Act-Assert:

```typescript
test("increments counter when button pressed", async () => {
  // Arrange
  const user = userEvent.setup();
  render(<Counter initialCount={0} />);

  // Act
  await user.press(screen.getByRole("button", { name: "Increment" }));

  // Assert
  expect(screen.getByRole("text", { name: "Count: 1" })).toBeOnTheScreen();
});
```

### Descriptive Test Names

Use descriptive names that explain the expected behavior:

```typescript
// Correct - describes behavior
test("displays validation error when email format is invalid", () => {});
test("disables submit button while form is submitting", () => {});

// Incorrect - vague or implementation-focused
test("email validation works", () => {});
test("sets isSubmitting to true", () => {});
```

## Jest Configuration

### Manual React Native Resolution (No Preset)

Lisa configures Jest manually instead of using the `jest-expo` preset to avoid
jsdom incompatibility with `react-native/jest/setup.js`. The configuration in
`jest.expo.ts` provides haste, resolver, transform, and setupFiles that match
the preset's behavior without redefining `window`.

### Use Fake Timers with userEvent

```typescript
jest.useFakeTimers();

test("handles debounced input", async () => {
  const user = userEvent.setup();
  render(<SearchInput />);

  await user.type(screen.getByRole("textbox"), "query");
  jest.runAllTimers();

  expect(await screen.findByText("Results")).toBeOnTheScreen();
});
```

## Anti-Patterns

### Never Test Implementation Details

```typescript
// Wrong - testing internal state
expect(wrapper.state().isLoading).toBe(true);

// Wrong - testing component methods
expect(wrapper.instance().handleSubmit).toHaveBeenCalled();

// Correct - testing visible behavior
expect(screen.getByRole("progressbar")).toBeOnTheScreen();
```

### Never Use getByTestId as Default

```typescript
// Wrong - using testID when semantic query exists
screen.getByTestId("submit-button");

// Correct - using accessible query
screen.getByRole("button", { name: "Submit" });
```

### Never Wrap render or fireEvent in act()

```typescript
// Wrong - unnecessary act wrapper
await act(async () => {
  render(<Component />);
});

// Correct - render already wraps in act
render(<Component />);
```

### Never Put Side Effects in waitFor

```typescript
// Wrong - side effect in waitFor
await waitFor(() => {
  fireEvent.press(button);
  expect(result).toBeOnTheScreen();
});

// Correct - side effect before waitFor
fireEvent.press(button);
await waitFor(() => {
  expect(result).toBeOnTheScreen();
});
```

### Never Use Multiple Assertions in waitFor

```typescript
// Wrong - multiple assertions
await waitFor(() => {
  expect(title).toBeOnTheScreen();
  expect(subtitle).toBeOnTheScreen();
  expect(button).toBeEnabled();
});

// Correct - single assertion, chain with findBy
expect(await screen.findByRole("heading")).toBeOnTheScreen();
expect(screen.getByText("Subtitle")).toBeOnTheScreen();
expect(screen.getByRole("button")).toBeEnabled();
```

## Quick Reference

### Common Matchers

| Matcher               | Purpose                         |
| --------------------- | ------------------------------- |
| `toBeOnTheScreen()`   | Element is currently rendered   |
| `toBeEnabled()`       | Interactive element is enabled  |
| `toBeDisabled()`      | Interactive element is disabled |
| `toHaveTextContent()` | Element contains text           |
| `toBeVisible()`       | Element is visible to user      |
| `toBeChecked()`       | Checkbox/radio is checked       |

### Query Variants

| Prefix     | Returns              | Throws on 0 | Throws on >1 | Async |
| ---------- | -------------------- | ----------- | ------------ | ----- |
| getBy      | Element              | Yes         | Yes          | No    |
| queryBy    | Element \| null      | No          | Yes          | No    |
| findBy     | Promise\<Element\>   | Yes         | Yes          | Yes   |
| getAllBy   | Element[]            | Yes         | No           | No    |
| queryAllBy | Element[]            | No          | No           | No    |
| findAllBy  | Promise\<Element[]\> | Yes         | No           | Yes   |

## References

- [Query Priority](references/query-priority.md) - Detailed query selection guidance
- [Async Patterns](references/async-patterns.md) - Comprehensive async testing patterns
- [Mocking Patterns](references/mocking-patterns.md) - Common mocking configurations
- [Expo Router Testing](references/expo-router-testing.md) - Testing with Expo Router
