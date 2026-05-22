---
name: mstest-testing-platform
description: Guide for using MSTest with Microsoft.Testing.Platform (the new test runner, not legacy VSTest) in .NET 10 projects
type: domain
enforcement: suggest
priority: high
---

# MSTest with Microsoft.Testing.Platform

This skill provides guidance for using **Microsoft.Testing.Platform** (the new test runner) with MSTest in this .NET 10 project. This is NOT the legacy VSTest runner.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Platform Overview](#platform-overview)
3. [Project Setup](#project-setup)
4. [Running Tests](#running-tests)
5. [Test Configuration](#test-configuration)
6. [Test Parallelization](#test-parallelization)
7. [Debugging Tests](#debugging-tests)
8. [CI/CD Integration](#cicd-integration)
9. [Troubleshooting](#troubleshooting)
10. [Quick Reference](#quick-reference)

---

## Prerequisites

This project uses:
- **.NET 10 SDK**: 10.0.100-rc.2.25502.107 (configured in global.json)
- **MSTest Package**: 4.0.0-preview.25465.3 (configured in Directory.Packages.props)
- **Microsoft.Testing.Platform**: Included in MSTest 4.0.0+

The test runner is configured globally in `global.json`:
```json
{
  "test": {
    "runner": "Microsoft.Testing.Platform"
  }
}
```

---

## Platform Overview

Microsoft.Testing.Platform is the **new test runner** replacing legacy VSTest. Key differences:

- **Command**: Use `dotnet run --project` (preferred) or `dotnet test`
- **Performance**: Faster, more efficient than VSTest
- **Project Type**: Requires `OutputType=Exe` (not Library)
- **Configuration**: Requires `EnableMSTestRunner=true` in .csproj
- **MSTest Version**: Requires 4.0.0+ (this project uses 4.0.0-preview.25465.3)

---

## Project Setup

### Required Project Configuration

All test projects in this repository require these properties:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <EnableMSTestRunner>true</EnableMSTestRunner>
    <OutputType>Exe</OutputType>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="MSTest" />
  </ItemGroup>
</Project>
```

**Key Properties:**
- `EnableMSTestRunner`: Enables Microsoft.Testing.Platform
- `OutputType=Exe`: Makes the test project executable (required for the new runner)
- Package version is managed in `Directory.Packages.props` (see dotnet-centralized-packages skill)

### Current Test Projects

This repository has 4 test projects configured correctly:
- `tests/ClaudeStack.Web.Tests/ClaudeStack.Web.Tests.csproj`
- `tests/ClaudeStack.API.Tests/ClaudeStack.API.Tests.csproj`
- `tests/ClaudeStack.Web.Tests.Playwright/ClaudeStack.Web.Tests.Playwright.csproj`
- `tests/ClaudeStack.API.Tests.Playwright/ClaudeStack.API.Tests.Playwright.csproj`

All follow the same configuration pattern.

---

## Running Tests

### Primary Method: dotnet run

The **preferred way** to run tests with Microsoft.Testing.Platform:

```bash
# Run all tests in a specific project
dotnet run --project tests/ClaudeStack.Web.Tests/ClaudeStack.Web.Tests.csproj

# Run all tests in a specific project (shorter path)
dotnet run --project tests/ClaudeStack.Web.Tests

# Run all tests in all projects (from solution root)
dotnet test
```

### Test Filtering

Use the `--filter` option to run specific tests:

```bash
# Run a specific test method
dotnet test --filter FullyQualifiedName~TestMethod1

# Run all tests in a class
dotnet test --filter FullyQualifiedName~ClaudeStack.Web.Tests.Test1

# Run tests matching a pattern
dotnet test --filter Name~Login

# Run tests by trait/category
dotnet test --filter TestCategory=Integration
```

### Running from Test Project Directory

```bash
# Navigate to test project
cd tests/ClaudeStack.Web.Tests

# Run tests
dotnet run

# Or use dotnet test
dotnet test
```

### Running All Tests

```bash
# From solution root, run all tests
dotnet test
```

This runs all 4 test projects sequentially.

---

## Test Configuration

### MSTestSettings.cs

Each test project has a `MSTestSettings.cs` file for test execution configuration:

```csharp
using Microsoft.VisualStudio.TestTools.UnitTesting;

[assembly: Parallelize(Scope = ExecutionScope.MethodLevel)]
```

This file controls test parallelization behavior (see next section).

### Test Class Structure

Standard MSTest attributes: `[TestClass]`, `[TestMethod]`, `[TestInitialize]`, `[TestCleanup]`

**Important**: ImplicitUsings is disabled. Always include: `using Microsoft.VisualStudio.TestTools.UnitTesting;`

---

## Test Parallelization

### Current Configuration

All test projects use **method-level parallelization**:

```csharp
[assembly: Parallelize(Scope = ExecutionScope.MethodLevel)]
```

This means test methods run in parallel within each test class.

### Parallelization Scopes

Available options:

```csharp
// Method-level: Test methods run in parallel (current setting)
[assembly: Parallelize(Scope = ExecutionScope.MethodLevel)]

// Class-level: Test classes run in parallel, methods sequential within class
[assembly: Parallelize(Scope = ExecutionScope.ClassLevel)]
```

### Controlling Parallelization

Disable parallelization for specific tests:

```csharp
[TestClass]
[DoNotParallelize]
public class SequentialTests
{
    [TestMethod]
    public void MustRunSequentially()
    {
        // This test class won't run in parallel with others
    }
}
```

### Performance Considerations

- **Method-level** (current): Fastest, but tests must be thread-safe
- **Class-level**: Safer if tests share state within a class
- **No parallelization**: Slowest, but safest for tests with external dependencies

---

## Debugging Tests

### Visual Studio

1. Set breakpoints in test code
2. Right-click test → "Debug Test"
3. Or use Test Explorer: Debug → Debug All Tests

### Visual Studio Code

Use the `.NET Core Test Explorer` extension:
1. Install extension
2. Set breakpoints
3. Click "Debug Test" in Test Explorer

### Command Line Debugging

Not directly supported. Use IDE debugging instead.

### Debug Output

Use `TestContext` to write debug output:

```csharp
[TestClass]
public class MyTests
{
    public TestContext TestContext { get; set; }

    [TestMethod]
    public void MyTest()
    {
        TestContext.WriteLine("Debug message");
    }
}
```

Output appears in test results.

---

## CI/CD Integration

### Azure DevOps

Use the `DotNetCoreCLI@2` task:

```yaml
- task: DotNetCoreCLI@2
  displayName: 'Run Tests'
  inputs:
    command: 'test'
    projects: '**/*.Tests.csproj'
    arguments: '--configuration Release'
```

### GitHub Actions

```yaml
- name: Run Tests
  run: dotnet test --configuration Release
```

### Test Results Publishing

```bash
# Generate TRX results
dotnet test --logger "trx;LogFileName=test-results.trx"
```

In CI/CD, use `--logger trx` and publish with `PublishTestResults@2` task (Azure DevOps) or upload artifacts (GitHub Actions).

---

## Troubleshooting

### Issue: Tests Don't Run

**Symptoms**: Test project builds but tests don't execute

**Solution**: Verify project configuration:
```xml
<EnableMSTestRunner>true</EnableMSTestRunner>
<OutputType>Exe</OutputType>
```

### Issue: "dotnet test" Fails with Errors

**Symptoms**: `dotnet test` works but shows warnings or errors

**Solution**: Use `dotnet run --project` instead:
```bash
dotnet run --project tests/ClaudeStack.Web.Tests
```

### Issue: Global.json Overwritten

**Symptoms**: After creating new test project, global.json is replaced

**Cause**: Using `--test-runner` flag with `dotnet new mstest`

**Solution**:
1. **NEVER** use `--test-runner` flag when creating test projects in this repository
2. The test runner is already configured in global.json
3. Correct command:
   ```bash
   # CORRECT
   dotnet new mstest -o tests/NewProject

   # WRONG - will overwrite global.json
   dotnet new mstest -o tests/NewProject --test-runner Microsoft.Testing.Platform
   ```
4. After creating project, manually add to .csproj:
   ```xml
   <PropertyGroup>
     <EnableMSTestRunner>true</EnableMSTestRunner>
     <OutputType>Exe</OutputType>
   </PropertyGroup>
   ```

### Issue: Tests Run Sequentially (Slow)

**Symptoms**: Tests take longer than expected

**Solution**: Verify MSTestSettings.cs has parallelization:
```csharp
[assembly: Parallelize(Scope = ExecutionScope.MethodLevel)]
```

### Issue: Package Version Conflicts

**Symptoms**: Build errors about MSTest versions

**Solution**: Check Directory.Packages.props. Never add Version attribute to PackageReference in .csproj (see dotnet-centralized-packages skill).

### Issue: Implicit Usings Errors

**Symptoms**: Missing namespace errors (e.g., "TestClass not found")

**Solution**: Add explicit using statements:
```csharp
using Microsoft.VisualStudio.TestTools.UnitTesting;
```

ImplicitUsings is disabled in this project (Directory.Build.props).

---

## Quick Reference

### Commands

```bash
# Run tests in a project
dotnet run --project tests/ClaudeStack.Web.Tests

# Run all tests
dotnet test

# Run specific test
dotnet test --filter FullyQualifiedName~TestMethod1

# Run with detailed output
dotnet test --verbosity detailed

# Generate test results
dotnet test --logger "trx;LogFileName=results.trx"
```

### Required Project Properties

```xml
<PropertyGroup>
  <EnableMSTestRunner>true</EnableMSTestRunner>
  <OutputType>Exe</OutputType>
</PropertyGroup>
```

### Required Package

```xml
<ItemGroup>
  <PackageReference Include="MSTest" />
</ItemGroup>
```

Version managed in Directory.Packages.props.

### MSTestSettings.cs Template

```csharp
using Microsoft.VisualStudio.TestTools.UnitTesting;

[assembly: Parallelize(Scope = ExecutionScope.MethodLevel)]
```

### Test Class Template

```csharp
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace YourNamespace.Tests
{
    [TestClass]
    public class YourTests
    {
        [TestMethod]
        public void YourTest()
        {
            // Arrange
            var expected = true;

            // Act
            var actual = true;

            // Assert
            Assert.AreEqual(expected, actual);
        }
    }
}
```

### Creating New Test Project

```bash
# Step 1: Create project (DO NOT use --test-runner flag)
dotnet new mstest -o tests/NewProject

# Step 2: Manually add to .csproj
# <PropertyGroup>
#   <EnableMSTestRunner>true</EnableMSTestRunner>
#   <OutputType>Exe</OutputType>
# </PropertyGroup>

# Step 3: Add MSTestSettings.cs
# [assembly: Parallelize(Scope = ExecutionScope.MethodLevel)]

# Step 4: Add to solution
dotnet sln add tests/NewProject/NewProject.csproj
```

---

## Related Skills

- **dotnet-centralized-packages**: Managing package versions in Directory.Packages.props
- **playwright-dotnet**: E2E testing with Playwright and MSTest integration
- **dotnet-cli-essentials**: General .NET CLI commands and patterns

---

## Version Information

- **MSTest**: 4.0.0-preview.25465.3
- **Microsoft.Testing.Platform**: Included in MSTest 4.0.0+
- **.NET SDK**: 10.0.100-rc.2.25502.107

This skill is accurate as of .NET 10 RC 2. Some details may change in the RTM release.

---

## Additional Resources

- [Microsoft.Testing.Platform Documentation](https://learn.microsoft.com/en-us/dotnet/core/testing/testing-platform)
- [MSTest Documentation](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-mstest)
- [Test Parallelization](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-mstest-writing-tests#parallelization)
