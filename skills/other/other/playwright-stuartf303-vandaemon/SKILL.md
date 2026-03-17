---
name: playwright
description: |
  Automates browser testing and E2E test scenarios with Playwright.
  Use when: writing end-to-end tests, testing Blazor WASM UI, validating SignalR real-time updates, testing responsive layouts, or automating browser interactions.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Playwright Skill

Playwright provides browser automation for E2E testing of the VanDaemon Blazor WebAssembly application. Tests run against both API (port 5000) and Web (port 5001) servers, validating real-time SignalR updates, MudBlazor component interactions, and responsive dashboard layouts.

## Quick Start

### Run E2E Tests

```powershell
# Full test suite (starts servers automatically)
./run-e2e-tests.ps1

# Visible browser with slow motion for debugging
./run-e2e-tests.ps1 -Headless $false -SlowMo 500

# Run specific test file
dotnet test tests/VanDaemon.E2E.Tests --filter "FullyQualifiedName~DashboardTests"
```

### Basic Page Test

```csharp
[Fact]
public async Task Dashboard_LoadsSuccessfully()
{
    await Page.GotoAsync("http://localhost:5001");
    await Expect(Page).ToHaveTitleAsync("VanDaemon");
    await Expect(Page.Locator(".mud-main-content")).ToBeVisibleAsync();
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Page Object | Encapsulates page interactions | `var dashboard = new DashboardPage(Page)` |
| Locator | Element selection with auto-wait | `Page.Locator("[data-testid='tank-level']")` |
| Expect | Assertion with retry | `await Expect(locator).ToBeVisibleAsync()` |
| WaitForSelector | Explicit wait for elements | `await Page.WaitForSelectorAsync(".loading", new() { State = WaitForSelectorState.Hidden })` |

## Common Patterns

### Testing MudBlazor Components

**When:** Interacting with Material Design components

```csharp
// Toggle a MudSwitch
var switchControl = Page.Locator("label:has-text('Water Pump')").Locator("..").Locator("input[type='checkbox']");
await switchControl.ClickAsync();
await Expect(switchControl).ToBeCheckedAsync();

// Slider interaction
var dimmer = Page.Locator(".mud-slider input[type='range']");
await dimmer.FillAsync("75");
```

### Waiting for SignalR Updates

**When:** Testing real-time data from TelemetryHub

```csharp
// Wait for SignalR to push tank level update
await Page.WaitForFunctionAsync(@"() => {
    const level = document.querySelector('[data-testid=""fresh-water-level""]');
    return level && parseFloat(level.textContent) > 0;
}", new() { Timeout = 10000 });
```

### Screenshot on Failure

**When:** Debugging flaky tests

```csharp
public async Task TakeScreenshotOnFailure(string testName)
{
    await Page.ScreenshotAsync(new() { 
        Path = $"test-results/{testName}-{DateTime.Now:yyyyMMdd-HHmmss}.png",
        FullPage = true 
    });
}
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **blazor** skill for Blazor WebAssembly patterns being tested
- See the **mudblazor** skill for component selectors and interactions
- See the **signalr** skill for real-time update testing strategies
- See the **xunit** skill for test framework integration
- See the **docker** skill for containerized test execution