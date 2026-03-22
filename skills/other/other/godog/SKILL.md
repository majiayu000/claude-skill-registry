---
name: godog
description: Gherkin runner for Go
category: Testing-BDD
---

# Godog (Gherkin for Go)

**Category**: Testing  
**Version**: 1.0

## What I Do

Godog is a Cucumber-like BDD framework for Go. I help write executable specifications in Gherkin (Given-When-Then) syntax that drive development through behavior-first test specifications.

## When to Use

- Writing user-facing acceptance tests
- Documenting feature behavior in plain English
- Driving TUI application development with E2E scenarios
- Ensuring domain logic behaves as specified before implementation

## Core Principles

### 1. Steps Call Domain Functions, Never UI Helpers

Godog steps are thin adapters that:
- Extract data from test context
- Call domain functions (pure, testable)
- Send messages to update state
- Assert outcomes on view/state

Never:
- Call `Program.Run()` (creates event loop)
- Call `SubmitHuhForm()` (blocks waiting for TUI)
- Embed business logic in steps (violates separation)

### 2. Given-When-Then Pattern

- **Given**: Set up initial state (via domain function if needed)
- **When**: Invoke business logic (call domain function)
- **Then**: Assert outcomes (check view or state)

### 3. Context Passing for State Sharing

```go
func iHaveAnEvent(ctx context.Context) (context.Context, error) {
    event := createTestEvent()
    // Store in context for later steps
    ctx = context.WithValue(ctx, "event", event)
    return ctx, nil
}
```

### 4. Tag Filtering

- `&&` for AND: `@smoke && @slow` runs only scenarios with both tags
- `~` for NOT: `@wip` runs all except work-in-progress

### 5. Step Definitions Are Thin Adapters

```go
// ✅ CORRECT: Thin adapter calling domain function
func iAcceptTheBurst(ctx context.Context) (context.Context, error) {
    env := support.GetAppEnv(ctx)
    burst, err := capture.CreateBurstFromSuggestion(env.testData.input)
    if err != nil { return ctx, err }
    env.SendMessage(BurstCreatedMsg{Burst: burst})
    return ctx, nil
}

// ❌ INCORRECT: Business logic in step
func iAcceptTheBurst(ctx context.Context) (context.Context, error) {
    env := support.GetAppEnv(ctx)
    if len(env.Events) == 0 { return ctx, errors.New("no events") }  // ❌ Logic
    return ctx, nil
}
```

## Common Patterns

### Reading Test Data from Context
```go
event := ctx.Value("event").(*career.Event)
```

### Sending Messages to Update State
```go
env.SendMessage(EventCreatedMsg{Event: event})
```

### Asserting on View Content
```go
view := env.GetView()
if !strings.Contains(view, expectedText) {
    return ctx, fmt.Errorf("expected text not found")
}
```

## Anti-Patterns to Avoid

- ❌ Business logic in "When" steps (extract to domain function)
- ❌ Calling `Program.Run()` or `SubmitHuhForm()` (deadlocks)
- ❌ Testing UI directly without domain layer (couples tests to UI)
- ❌ Skipping "Given" setup (leaves tests brittle)
- ❌ Vague step names (make steps self-documenting)

## Testing Contract

**Enforcement Rule** (4-step process for writing tests):
1. Identify business logic
2. Extract it into a pure function
3. Test the pure function
4. Do NOT test the runtime event loop

See: KaRiya Obsidian note "Bubble Tea + Huh Testing Contract"

## Related Skills

- `cucumber`: Gherkin syntax and feature files
- `bubble-tea-testing`: TUI testing patterns
- `huh-testing`: Form library testing
- `test-fixtures-go`: Test data factories


## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/Godog.md`

