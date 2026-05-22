---
name: fluent-assertions
description: |
  Writes fluent, readable test assertions and validations using FluentAssertions library.
  Use when: Writing unit tests, validating service responses, asserting domain entity states, testing collections and async operations.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# FluentAssertions Skill

FluentAssertions provides a fluent API for expressing test assertions in C#. In VanDaemon, it's used alongside **xUnit** and **Moq** for testing services, controllers, plugins, and the JsonFileStore persistence layer. The library produces clear failure messages that explain exactly what went wrong.

## Quick Start

### Basic Value Assertions

```csharp
// From VanDaemon test patterns
result.Should().NotBeNull();
result.Should().Be(expectedValue);
tank.CurrentLevel.Should().BeInRange(0, 100);
tank.IsActive.Should().BeTrue();
```

### Collection Assertions

```csharp
// Testing tank service returns
var tanks = await tankService.GetAllTanksAsync();
tanks.Should().NotBeNull();
tanks.Should().HaveCount(3);
tanks.Should().AllSatisfy(t => t.IsActive.Should().BeTrue());
tanks.Should().Contain(t => t.Type == TankType.FreshWater);
```

### Async Operation Assertions

```csharp
// Testing async service methods
await service.Invoking(s => s.GetTankByIdAsync(Guid.Empty))
    .Should().ThrowAsync<ArgumentException>();

var result = await service.GetAllControlsAsync();
result.Should().BeEquivalentTo(expectedControls);
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `Should()` | Entry point for all assertions | `value.Should().Be(5)` |
| `BeEquivalentTo()` | Deep object comparison | `actual.Should().BeEquivalentTo(expected)` |
| `AllSatisfy()` | Assert condition on all items | `list.Should().AllSatisfy(x => x.IsActive.Should().BeTrue())` |
| `Invoking()` | Test exception throwing | `obj.Invoking(x => x.Method()).Should().Throw<T>()` |
| `Because()` | Custom failure message | `value.Should().Be(5, "configuration requires this")` |

## Common Patterns

### Service Response Validation

**When:** Testing application services like `TankService`, `ControlService`

```csharp
var mockFileStore = new Mock<IJsonFileStore>();
mockFileStore.Setup(x => x.LoadAsync<List<Tank>>("tanks.json", It.IsAny<CancellationToken>()))
    .ReturnsAsync(testTanks);

var service = new TankService(logger, mockFileStore.Object);
var result = await service.GetAllTanksAsync();

result.Should().NotBeNull();
result.Should().HaveCount(2);
result.First().Name.Should().Be("Fresh Water");
```

### Entity State Assertions

**When:** Validating domain entity properties

```csharp
var tank = new Tank { Type = TankType.FreshWater, AlertLevel = 10 };
tank.Type.Should().Be(TankType.FreshWater);
tank.AlertLevel.Should().BeGreaterThanOrEqualTo(0);
tank.AlertWhenOver.Should().BeFalse("fresh water alerts when level drops below threshold");
```

## See Also

- [patterns](references/patterns.md) - Assertion patterns by type
- [workflows](references/workflows.md) - Testing workflows and best practices

## Related Skills

- **xunit** skill for test framework fundamentals
- **moq** skill for mocking dependencies before asserting results
- **csharp** skill for language features used in assertions