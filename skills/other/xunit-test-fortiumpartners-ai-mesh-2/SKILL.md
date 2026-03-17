---
name: xUnit Test Framework
description: Execute and generate xUnit tests for C#/.NET projects with FluentAssertions and Moq support
version: 1.0.0
---

# xUnit Test Framework

## Purpose

Provide xUnit test execution and generation for C#/.NET projects.

## Usage

```bash
dotnet run --project generate-test.csproj -- --source=Calculator.cs --output=CalculatorTests.cs --description="Division by zero"
dotnet test --filter=CalculatorTests
```

## Output Format

JSON with success, passed, failed, total, and failures array.
