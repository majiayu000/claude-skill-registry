---
name: playwright-selectors
description: Best practices for adding testID and aria-label selectors for Playwright E2E testing in Expo web applications. This skill should be used when adding E2E test coverage, creating new components that need test selectors, or reviewing code for testability.
---

# Playwright Selectors Best Practices

## Overview

This skill provides guidance for adding effective selectors (testID, aria-labels) to Expo/React Native components for Playwright E2E testing. Proper selector strategy ensures tests are reliable, maintainable, and accessible.

## Selector Priority

Choose selectors based on their reliability and accessibility impact, in this priority order:

| Priority | Selector Method | When to Use                               |
| -------- | --------------- | ----------------------------------------- |
| 1        | `getByRole`     | Interactive elements with semantic roles  |
| 2        | `getByText`     | Visible text content                      |
| 3        | `getByLabel`    | Form elements with labels                 |
| 4        | `getByTestId`   | Fallback for elements without semantics   |

### getByRole (Preferred)

Use semantic roles when possible - they improve both accessibility and test resilience.

```typescript
// E2E test - preferred selector
const submitButton = page.getByRole("button", { name: "Submit" });
await expect(submitButton).toBeVisible();
```

### getByTestId (Fallback)

Use testID when semantic selectors are not available, particularly for structural containers.

```typescript
// E2E test - fallback selector
const container = page.getByTestId("home:container");
await expect(container).toBeVisible();
```

## testID Naming Convention

Use a namespaced pattern with colons as separators: `screen:element`

### Format

```
{screen}:{element}
```

- **screen**: lowercase screen/feature name (e.g., `home`, `profile`, `settings`)
- **element**: lowercase element identifier (e.g., `container`, `title`, `submit-button`)

### Examples

| testID                     | Description                      |
| -------------------------- | -------------------------------- |
| `home:container`           | Main container on home screen    |
| `home:title`               | Title text on home screen        |
| `profile:avatar`           | User avatar on profile screen    |
| `settings:dark-mode-toggle`| Dark mode toggle in settings     |
| `auth:login-button`        | Login button on auth screen      |

### Rules

1. Use lowercase only
2. Use colons (`:`) to separate screen from element
3. Use hyphens (`-`) for multi-word elements
4. Be descriptive but concise
5. Avoid redundant words (e.g., `home:home-title` should be `home:title`)

## React Native to HTML Mapping

Understanding how testID propagates from React Native to the web is essential.

### How It Works

1. React Native's `testID` prop is for native testing (XCUITest, Espresso)
2. On web (via react-native-web), `testID` renders as `data-testid` in HTML
3. Playwright's `getByTestId()` queries `data-testid` by default

```typescript
// React Native component
<Box testID="home:container">...</Box>

// Rendered HTML on web
<div data-testid="home:container">...</div>

// Playwright locator
page.getByTestId("home:container")
```

### Gluestack UI Components

Gluestack UI web components (Box, Text, etc.) require explicit testID handling because they use native HTML elements instead of react-native-web components. The web versions have been updated to:

1. Accept a `testID` prop in the TypeScript type
2. Map `testID` to `data-testid` on the rendered HTML element

```typescript
// Gluestack Box web implementation
const Box = ({ testID, ...props }) => (
  <div data-testid={testID} {...props} />
);
```

## When to Add testID

### Add testID To

1. **Interactive elements** that E2E tests will click/interact with
2. **Key structural containers** for page load verification
3. **Dynamic content areas** that change based on state
4. **Form elements** that lack semantic labels

### Do Not Add testID To

1. Every element (over-testing creates maintenance burden)
2. Elements with good semantic selectors (use getByRole instead)
3. Decorative elements not needed for testing
4. Elements inside third-party components (may not propagate)

## Accessibility Best Practices

Prefer semantic selectors and aria-labels over testID when possible.

### aria-label for Testing and Accessibility

When adding labels for testing, use `aria-label` or `accessibilityLabel` to benefit screen reader users too.

```typescript
// Correct - benefits both testing and accessibility
<Pressable
  accessibilityLabel="Close dialog"
  onPress={handleClose}
>
  <XIcon />
</Pressable>

// E2E test uses accessible name
await page.getByRole("button", { name: "Close dialog" }).click();
```

### accessibilityRole for Semantic Elements

Use `accessibilityRole` to provide semantic meaning on web.

```typescript
// Correct - semantic role for assistive technology
<Box accessibilityRole="banner" testID="header:container">
  <Text accessibilityRole="heading">Welcome</Text>
</Box>

// E2E test can use role
await expect(page.getByRole("banner")).toBeVisible();
await expect(page.getByRole("heading", { name: "Welcome" })).toBeVisible();
```

## Implementation Checklist

When adding E2E test coverage to a component:

- [ ] Identify elements that need selectors for testing
- [ ] Prefer semantic selectors (role, text, label) when available
- [ ] Use namespaced testID pattern for elements without semantics
- [ ] Verify testID propagates to `data-testid` on web (check Gluestack components)
- [ ] Add accessibility labels where beneficial
- [ ] Document testIDs in component JSDoc preamble

## Example Component

```typescript
/**
 * Profile screen component.
 *
 * Test IDs for E2E testing:
 * - `profile:container` - Main container
 * - `profile:avatar` - User avatar image
 * - `profile:name` - User display name
 *
 * @module features/profile/screens/Main
 */
export const ProfileScreen = () => (
  <Box testID="profile:container" className="flex-1 p-4">
    <Image
      testID="profile:avatar"
      source={{ uri: user.avatarUrl }}
      accessibilityLabel={`${user.name}'s profile photo`}
    />
    <Text testID="profile:name" accessibilityRole="heading">
      {user.name}
    </Text>
    <Pressable
      accessibilityLabel="Edit profile"
      onPress={handleEdit}
    >
      <Text>Edit</Text>
    </Pressable>
  </Box>
);
```

## Corresponding E2E Test

```typescript
test.describe("Profile Screen", () => {
  test("displays user information", async ({ page }) => {
    await page.goto("/profile");

    // Verify structural container
    await expect(page.getByTestId("profile:container")).toBeVisible();

    // Prefer accessible queries when available
    await expect(page.getByRole("heading")).toHaveText("John Doe");
    await expect(page.getByRole("button", { name: "Edit profile" })).toBeVisible();

    // Use testID for elements without semantic roles
    await expect(page.getByTestId("profile:avatar")).toBeVisible();
  });
});
```
