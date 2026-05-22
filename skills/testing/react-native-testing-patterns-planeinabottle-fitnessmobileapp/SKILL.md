---
name: react-native-testing-patterns
description: Implements testing strategies for React Native components, MST stores, and services using Jest, React Testing Library, and Maestro. Use when writing unit, integration, or E2E tests in Fitness Tracker App.
---

# React Native Testing Patterns

This skill provides the established testing patterns for the Fitness Tracker App, ensuring high code quality and reliable automated verification.

## When to Use This Skill

Use this skill when you need to:
- Write unit tests for MST models and stores
- Create component tests using React Testing Library (RTL)
- Mock Expo modules or native dependencies
- Implement E2E flows using Maestro
- Test services, utility functions, or API logic

## Unit Testing (MST)

### Model Testing
```typescript
import { MyModel } from "@/models/MyModel"

describe("MyModel", () => {
  it("can be created", () => {
    const instance = MyModel.create({ id: "1", name: "Test" })
    expect(instance.name).toBe("Test")
  })

  it("handles actions correctly", () => {
    const instance = MyModel.create({ id: "1", name: "Test" })
    instance.setName("Updated")
    expect(instance.name).toBe("Updated")
  })
})
```

## Component Testing (RTL)

### Basic Component Render
```tsx
import { render } from "@testing-library/react-native"
import { ThemeProvider } from "@/theme/context"
import { MyComponent } from "./MyComponent"

describe("MyComponent", () => {
  it("renders correctly", () => {
    const { getByText } = render(
      <ThemeProvider>
        <MyComponent text="Hello" />
      </ThemeProvider>
    )
    expect(getByText("Hello")).toBeDefined()
  })
})
```

## Mocking Patterns

### Mocking Expo Modules
Mocks are usually centralized in `test/setup.ts`.

```typescript
jest.mock("expo-localization", () => ({
  getLocales: () => [{ languageTag: "en-US", textDirection: "ltr" }],
}))
```

## E2E Testing (Maestro)

### Basic Flow Pattern
```yaml
appId: ${MAESTRO_APP_ID}
onFlowStart:
  - runFlow: ../shared/_OnFlowStart.yaml
---
- tapOn: "Home"
- assertVisible: "My Collection"
```

## References

See [MST_TESTING.md](references/MST_TESTING.md) for detailed store testing patterns.

See [COMPONENT_TESTING.md](references/COMPONENT_TESTING.md) for RTL and theme provider patterns.

See [MAESTRO_FLOWS.md](references/MAESTRO_FLOWS.md) for E2E testing best practices.
