---
name: playwright-dotnet
description: Guide for E2E testing with Playwright for .NET using Microsoft.Playwright.MSTest.v4 integration
type: domain
enforcement: suggest
priority: high
---

# Playwright for .NET Testing

This skill provides guidance for end-to-end (E2E) testing with **Playwright for .NET** using Microsoft.Playwright.MSTest.v4 integration in this .NET 10 project.

## Table of Contents
1. [Overview](#overview)
2. [Project Setup](#project-setup)
3. [Installing Browsers](#installing-browsers)
4. [Writing Tests](#writing-tests)
5. [Selectors and Assertions](#selectors-and-assertions)
6. [Debugging Tests](#debugging-tests)
7. [CI/CD Integration](#cicd-integration)
8. [Troubleshooting](#troubleshooting)
9. [Quick Reference](#quick-reference)

---

## Overview

### What is Playwright?

Playwright is a **modern E2E testing framework** for web applications. It supports:
- **Multiple browsers**: Chromium, Firefox, WebKit
- **Cross-platform**: Windows, Linux, macOS
- **Auto-waiting**: Smart waits for elements
- **Powerful selectors**: CSS, text, accessibility
- **Reliable**: Reduces flakiness
- **Fast**: Parallel execution

### Microsoft.Playwright.MSTest.v4

This project uses the **MSTest integration** which provides:
- `PageTest` base class - one browser context per test
- `ContextTest` base class - browser context with multiple pages
- `BrowserTest` base class - full browser control
- Built-in fixtures (Page, Context, Browser)
- Automatic cleanup

**Version**: 1.55.0-beta-4 (configured in Directory.Packages.props)

---

## Project Setup

### Current Playwright Projects

This repository has 2 Playwright test projects:
- `tests/ClaudeStack.Web.Tests.Playwright/` - Tests for MVC application
- `tests/ClaudeStack.API.Tests.Playwright/` - Tests for API application

### Project Configuration

Both projects use this configuration:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <EnableMSTestRunner>true</EnableMSTestRunner>
    <OutputType>Exe</OutputType>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Playwright.MSTest.v4" />
    <PackageReference Include="MSTest" />
  </ItemGroup>
</Project>
```

**Key points:**
- Uses Microsoft.Testing.Platform (see mstest-testing-platform skill)
- Package versions managed in Directory.Packages.props (see dotnet-centralized-packages skill)
- MSTestSettings.cs configures method-level parallelization

### Creating New Playwright Project

```bash
# Step 1: Create MSTest project
dotnet new mstest -o tests/Example.NewApp.Tests.Playwright

# Step 2: Edit .csproj to add required properties
# <PropertyGroup>
#   <EnableMSTestRunner>true</EnableMSTestRunner>
#   <OutputType>Exe</OutputType>
# </PropertyGroup>

# Step 3: Add Playwright package reference (version in Directory.Packages.props)
# <PackageReference Include="Microsoft.Playwright.MSTest.v4" />
# <PackageReference Include="MSTest" />

# Step 4: Install browsers (see next section)

# Step 5: Add MSTestSettings.cs with parallelization
# [assembly: Parallelize(Scope = ExecutionScope.MethodLevel)]
```

---

## Installing Browsers

### Initial Browser Installation

After creating a Playwright project or after building, install browsers:

```powershell
# Navigate to the build output directory
cd tests/ClaudeStack.Web.Tests.Playwright/bin/Debug/net10.0

# Run the Playwright PowerShell script
./playwright.ps1 install
```

**Important**: Browsers must be installed **after building** the project because the playwright.ps1 script is generated during build.

### Installation on Different Platforms

**Windows (PowerShell):**
```powershell
pwsh -Command "cd tests/ClaudeStack.Web.Tests.Playwright/bin/Debug/net10.0; ./playwright.ps1 install"
```

**Linux/macOS (Bash):**
```bash
pwsh tests/ClaudeStack.Web.Tests.Playwright/bin/Debug/net10.0/playwright.ps1 install
```

### Installing Specific Browsers

```powershell
# Install only Chromium
./playwright.ps1 install chromium

# Install Chromium and Firefox
./playwright.ps1 install chromium firefox

# Install with dependencies (for Linux CI)
./playwright.ps1 install --with-deps
```

### Browser Locations

Browsers are installed in:
- **Windows**: `%USERPROFILE%\AppData\Local\ms-playwright`
- **Linux**: `~/.cache/ms-playwright`
- **macOS**: `~/Library/Caches/ms-playwright`

---

## Writing Tests

### Basic Test Structure

All tests inherit from `PageTest`:

```csharp
using System.Threading.Tasks;
using Microsoft.Playwright.MSTest;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace ClaudeStack.Web.Tests.Playwright;

[TestClass]
public class HomePageTests : PageTest
{
    [TestMethod]
    public async Task HomePageLoadsSuccessfully()
    {
        await Page.GotoAsync("https://localhost:5001");

        await Expect(Page).ToHaveTitleAsync("Home Page");
    }
}
```

**Key points:**
- Inherit from `PageTest`
- Test methods are `async Task`
- `Page` property available automatically
- `Expect` for assertions

### PageTest Fixtures

`PageTest` provides automatic fixtures:

```csharp
public class MyTests : PageTest
{
    // Available properties:
    // - Page: IPage (automatically created per test)
    // - Context: IBrowserContext
    // - Browser: IBrowser
    // - Playwright: IPlaywright
}
```

### Test Initialization

Use `[TestInitialize]` and `[TestCleanup]` as needed. Page is automatically disposed.

---

## Selectors and Assertions

### Selectors

```csharp
Page.Locator("css")                              // CSS selector
Page.Locator("text=Get Started")                 // Text
Page.GetByTestId("id")                           // Test ID
Page.GetByRole(AriaRole.Button)                  // Accessibility
Page.GetByLabel("Email")                         // Form label
Page.Locator("div").Locator("button")            // Chaining
```

### Assertions

```csharp
await Expect(Page).ToHaveTitleAsync("Title");
await Expect(element).ToBeVisibleAsync();
await Expect(element).ToHaveTextAsync("text");
await Expect(element).ToHaveAttributeAsync("href", "/about");
```

### Actions

```csharp
await element.ClickAsync();
await element.FillAsync("value");
await element.CheckAsync();
await element.SelectOptionAsync("option");
```

---

## Debugging Tests

### Headed Mode

```bash
$env:HEADED="1"
dotnet run --project tests/ClaudeStack.Web.Tests.Playwright
```

### Screenshots and Tracing

```csharp
// Screenshot
await Page.ScreenshotAsync(new() { Path = "screenshot.png" });

// Tracing
await Context.Tracing.StartAsync(new() { Screenshots = true, Snapshots = true });
// ... test actions ...
await Context.Tracing.StopAsync(new() { Path = "trace.zip" });
```

View trace: `pwsh .../playwright.ps1 show-trace trace.zip`

### Playwright Inspector

```bash
$env:PWDEBUG="1"
dotnet run --project tests/ClaudeStack.Web.Tests.Playwright
```

---

## CI/CD Integration

```yaml
# Azure DevOps / GitHub Actions
- Build project: dotnet build tests/**/*.Playwright.csproj
- Install browsers: pwsh .../playwright.ps1 install --with-deps
- Run tests: dotnet run --project tests/ClaudeStack.Web.Tests.Playwright
```

**Important**: Use `--with-deps` flag in CI to install system dependencies (Linux).

---

## Troubleshooting

### Issue: Browsers Not Installed

**Error**: "Executable doesn't exist at..."

**Solution**: Install browsers after building:
```powershell
cd tests/ClaudeStack.Web.Tests.Playwright/bin/Debug/net10.0
./playwright.ps1 install
```

### Issue: playwright.ps1 Not Found

**Cause**: Project not built yet.

**Solution**: Build first, then install browsers:
```bash
dotnet build tests/ClaudeStack.Web.Tests.Playwright
# Then install browsers
```

### Issue: Tests Timeout

**Cause**: Default timeout (30s) exceeded.

**Solution**: Increase timeout:
```csharp
[TestMethod]
[Timeout(60000)]  // 60 seconds
public async Task SlowTest()
{
    // Or set per-action timeout:
    await Page.GotoAsync("https://example.com", new() { Timeout = 60000 });
}
```

### Issue: Element Not Found

**Solution**: Playwright auto-waits, but verify selector:
```csharp
// Debug: Get all matching elements
var count = await Page.Locator("button").CountAsync();
Console.WriteLine($"Found {count} buttons");

// Use more specific selector
var button = Page.GetByRole(AriaRole.Button, new() { Name = "Submit" });
```

### Issue: Flaky Tests

**Solutions:**
1. Use `Expect` assertions (built-in retries)
2. Avoid hardcoded waits
3. Use `Page.WaitForLoadStateAsync(LoadState.NetworkIdle)`
4. Make selectors more specific

---

## Quick Reference

### Base Classes

```csharp
PageTest      // Single page per test (most common)
ContextTest   // Browser context, create own pages
BrowserTest   // Full browser control
```

### Common Patterns

```csharp
// Navigation
await Page.GotoAsync("url");

// Waiting
await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);
await Page.WaitForSelectorAsync("button");

// Locators
Page.Locator("css")
Page.GetByTestId("id")
Page.GetByRole(AriaRole.Button)
Page.GetByText("text")

// Assertions
await Expect(Page).ToHaveTitleAsync("title");
await Expect(element).ToBeVisibleAsync();
await Expect(element).ToHaveTextAsync("text");

// Actions
await element.ClickAsync();
await element.FillAsync("value");
await element.CheckAsync();
```

### Running Tests

```bash
# Run all Playwright tests
dotnet run --project tests/ClaudeStack.Web.Tests.Playwright

# Headed mode
$env:HEADED="1"
dotnet run --project tests/ClaudeStack.Web.Tests.Playwright

# Debug mode
$env:PWDEBUG="1"
dotnet run --project tests/ClaudeStack.Web.Tests.Playwright
```

### Browser Installation

```powershell
cd tests/ClaudeStack.Web.Tests.Playwright/bin/Debug/net10.0
./playwright.ps1 install              # All browsers
./playwright.ps1 install chromium     # Chromium only
./playwright.ps1 install --with-deps  # With system dependencies (Linux)
```

---

## Related Skills

- **mstest-testing-platform**: Running Playwright tests with Microsoft.Testing.Platform
- **dotnet-centralized-packages**: Managing Playwright package versions
- **dotnet-cli-essentials**: Building and running test projects

---

## Additional Resources

- [Playwright .NET Documentation](https://playwright.dev/dotnet/docs/intro)
- [Microsoft.Playwright.MSTest.v4 Package](https://www.nuget.org/packages/Microsoft.Playwright.MSTest.v4)
- [Playwright API Reference](https://playwright.dev/dotnet/docs/api/class-playwright)
- [Best Practices](https://playwright.dev/dotnet/docs/best-practices)

---

## Version Information

- **Microsoft.Playwright.MSTest.v4**: 1.55.0-beta-4
- **Playwright Version**: 1.55 (beta)
- **.NET SDK**: 10.0.100-rc.2.25502.107

This skill is accurate as of Playwright 1.55 beta. Some APIs may change in future versions.
