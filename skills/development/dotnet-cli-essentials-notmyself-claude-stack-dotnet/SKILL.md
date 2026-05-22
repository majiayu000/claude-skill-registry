---
name: dotnet-cli-essentials
description: Essential .NET CLI commands and patterns for .NET 10 projects with Directory.Build.props and .slnx solutions
type: domain
enforcement: suggest
priority: medium
---

# .NET CLI Essentials

This skill provides guidance for using the **.NET CLI** in this .NET 10 project. Covers common commands for building, running, testing, and managing projects.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Building Projects](#building-projects)
3. [Running Projects](#running-projects)
4. [Testing](#testing)
5. [Solution Management](#solution-management)
6. [Package Management](#package-management)
7. [Quick Reference](#quick-reference)

---

## Project Structure

### This Project's Layout

```
/
├── global.json                    # SDK version pin
├── Directory.Build.props          # Shared MSBuild properties
├── Directory.Packages.props       # Centralized package versions
├── sln.slnx                       # XML-based solution file
├── src/
│   ├── ClaudeStack.Web/              # ASP.NET Core MVC
│   └── ClaudeStack.API/              # Minimal API
└── tests/
    ├── ClaudeStack.Web.Tests/
    ├── ClaudeStack.Web.Tests.Playwright/
    ├── ClaudeStack.API.Tests/
    └── ClaudeStack.API.Tests.Playwright/
```

### Key Configuration Files

**global.json**: Pins .NET SDK to 10.0.100-rc.2.25502.107
**Directory.Build.props**: Sets TargetFramework, ImplicitUsings (disabled), Nullable (disabled)
**Directory.Packages.props**: Centralizes all NuGet package versions (see dotnet-centralized-packages skill)

---

## Building Projects

### Build Entire Solution

```bash
# From solution root
dotnet build

# With configuration
dotnet build --configuration Release

# Verbose output
dotnet build --verbosity detailed
```

### Build Specific Project

```bash
dotnet build src/ClaudeStack.Web/ClaudeStack.Web.csproj
dotnet build src/ClaudeStack.API/ClaudeStack.API.csproj
```

### Clean and Rebuild

```bash
# Clean build artifacts
dotnet clean

# Clean then build
dotnet clean && dotnet build

# Clean specific configuration
dotnet clean --configuration Release
```

### Restore Dependencies

```bash
# Restore NuGet packages
dotnet restore

# Force re-download
dotnet restore --force

# Clear cache and restore
dotnet nuget locals all --clear
dotnet restore
```

---

## Running Projects

### Run Web Application

```bash
# From solution root
dotnet run --project src/ClaudeStack.Web/ClaudeStack.Web.csproj

# Or navigate to project directory
cd src/ClaudeStack.Web
dotnet run
```

**Runs at**: https://localhost:7001 (configured in launchSettings.json)

### Run API Application

```bash
dotnet run --project src/ClaudeStack.API/ClaudeStack.API.csproj
```

**Runs at**: https://localhost:5001

### Watch Mode (Hot Reload)

```bash
# Auto-restart on file changes
dotnet watch --project src/ClaudeStack.Web

# With specific launch profile
dotnet watch --project src/ClaudeStack.Web --launch-profile https
```

**Key feature**: Razor runtime compilation enabled in ClaudeStack.Web - changes to .cshtml files reload automatically.

---

## Testing

### Run All Tests

```bash
# From solution root
dotnet test
```

Runs all 4 test projects:
- ClaudeStack.Web.Tests
- ClaudeStack.API.Tests
- ClaudeStack.Web.Tests.Playwright
- ClaudeStack.API.Tests.Playwright

### Run Specific Test Project

```bash
# Using dotnet run (Microsoft.Testing.Platform)
dotnet run --project tests/ClaudeStack.Web.Tests

# Using dotnet test (also works)
dotnet test tests/ClaudeStack.Web.Tests/ClaudeStack.Web.Tests.csproj
```

See **mstest-testing-platform** skill for detailed testing guidance.

### Run Tests with Filter

```bash
# Run specific test method
dotnet test --filter FullyQualifiedName~TestMethod1

# Run tests in a class
dotnet test --filter FullyQualifiedName~ClaudeStack.Web.Tests.Test1
```

### Test Output

```bash
# Detailed output
dotnet test --verbosity detailed

# Generate TRX results
dotnet test --logger "trx;LogFileName=results.trx"
```

---

## Solution Management

### Solution File (.slnx)

This project uses the **XML-based solution format** (sln.slnx) introduced in .NET:

```bash
# List projects in solution
dotnet sln sln.slnx list

# Add project to solution
dotnet sln sln.slnx add src/Example.NewProject/Example.NewProject.csproj

# Remove project
dotnet sln sln.slnx remove src/Example.OldProject/Example.OldProject.csproj
```

### Create New Project

```bash
# Create new web project
dotnet new mvc -o src/Example.NewWeb

# Create new API project
dotnet new webapi -o src/Example.NewAPI

# Create new test project (DON'T use --test-runner flag!)
dotnet new mstest -o tests/Example.NewWeb.Tests
```

**IMPORTANT**: Never use `--test-runner` flag - it overwrites global.json. The test runner is already configured globally.

### Add Project Reference

```bash
# Add reference from test project to web project
dotnet add tests/ClaudeStack.Web.Tests reference src/ClaudeStack.Web
```

---

## Package Management

### List Packages

```bash
# List packages in solution
dotnet list package

# Show outdated packages
dotnet list package --outdated

# Include transitive dependencies
dotnet list package --include-transitive
```

### Add Package

**With CPM** (this project):
1. Add version to Directory.Packages.props
2. Add reference to .csproj (without version)

```bash
# Step 1: Edit Directory.Packages.props
# <PackageVersion Include="Newtonsoft.Json" Version="13.0.3" />

# Step 2: Add reference to project
dotnet add src/ClaudeStack.Web package Newtonsoft.Json
```

See **dotnet-centralized-packages** skill for details.

---

## Quick Reference

### Common Commands

```bash
# Build
dotnet build                           # Build solution
dotnet build --configuration Release   # Release build
dotnet clean                           # Clean artifacts

# Run
dotnet run --project src/ClaudeStack.Web   # Run web app
dotnet watch --project src/ClaudeStack.Web # Run with hot reload

# Test
dotnet test                            # Run all tests
dotnet run --project tests/ClaudeStack.Web.Tests  # Run specific test project

# Solution
dotnet sln list                        # List projects
dotnet sln add path/to/project.csproj  # Add project

# Packages
dotnet list package                    # List packages
dotnet list package --outdated         # Check for updates
dotnet restore                         # Restore dependencies
```

### Project Commands

```bash
# Create new project
dotnet new mvc -o src/MyProject
dotnet new webapi -o src/MyAPI
dotnet new mstest -o tests/MyTests

# Add references
dotnet add tests/MyTests reference src/MyProject
dotnet add src/MyProject package PackageName
```

### Configuration Flags

```bash
--configuration Release                # Build configuration
--verbosity detailed                   # Output level
--no-restore                          # Skip restore
--no-build                            # Skip build (for tests)
--framework net10.0                   # Target framework
```

### Useful Paths

```bash
# ClaudeStack.Web (MVC)
src/ClaudeStack.Web/ClaudeStack.Web.csproj
https://localhost:7001

# ClaudeStack.API (Minimal APIs)
src/ClaudeStack.API/ClaudeStack.API.csproj
https://localhost:5001

# Test projects
tests/ClaudeStack.Web.Tests
tests/ClaudeStack.API.Tests
tests/ClaudeStack.Web.Tests.Playwright
tests/ClaudeStack.API.Tests.Playwright
```

---

## Related Skills

- **mstest-testing-platform**: Running tests with Microsoft.Testing.Platform
- **dotnet-centralized-packages**: Managing packages with Directory.Packages.props
- **dotnet-minimal-apis**: Building minimal API projects
- **aspnet-configuration**: Configuring appsettings and environments

---

## Additional Resources

- [.NET CLI Overview](https://learn.microsoft.com/en-us/dotnet/core/tools/)
- [dotnet build Reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build)
- [dotnet run Reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-run)
- [dotnet test Reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test)

---

## Version Information

- **.NET SDK**: 10.0.100-rc.2.25502.107 (pinned in global.json)
- **Solution Format**: .slnx (XML-based)
- **Target Framework**: net10.0

This project uses .NET 10 RC 2. Some commands may behave differently in the RTM release.
