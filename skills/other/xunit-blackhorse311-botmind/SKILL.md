---
name: xunit
description: |
  Writes and manages xUnit tests with FluentAssertions and Moq for BotMind mod testing.
  Use when: writing unit tests, creating test fixtures, mocking EFT/Unity dependencies, or validating bot behavior logic.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# xUnit Skill

Unit testing for BotMind uses xUnit 2.9.x with FluentAssertions for readable assertions and Moq for mocking EFT game classes that can't be instantiated directly. Tests live in `src/tests/` and follow the `MethodName_Scenario_ExpectedResult` naming convention.

## Quick Start

### Basic Test Structure

```csharp
using FluentAssertions;
using Moq;
using Xunit;

namespace Blackhorse311.BotMind.Tests;

public class LootFinderTests
{
    [Fact]
    public void FindLootableTargets_NoTargetsInRange_ReturnsEmptyList()
    {
        // Arrange
        var finder = new LootFinder(searchRadius: 50f);
        
        // Act
        var targets = finder.FindLootableTargets(Vector3.zero);
        
        // Assert
        targets.Should().BeEmpty();
    }
}
```

### Mocking EFT Classes

```csharp
[Fact]
public void IsActive_BotInCombat_ReturnsFalse()
{
    // Arrange
    var mockBotOwner = new Mock<BotOwner>();
    mockBotOwner.Setup(b => b.Memory.IsUnderFire).Returns(true);
    
    var layer = new LootingLayer(mockBotOwner.Object);
    
    // Act & Assert
    layer.IsActive().Should().BeFalse();
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `[Fact]` | Single test case | `[Fact] public void Method_Does_Thing()` |
| `[Theory]` | Parameterized tests | `[Theory] [InlineData(1)] [InlineData(2)]` |
| `Should()` | FluentAssertions entry | `result.Should().Be(expected)` |
| `Mock<T>` | Create mock object | `new Mock<BotOwner>()` |
| `Setup()` | Define mock behavior | `.Setup(x => x.Prop).Returns(val)` |

## Common Patterns

### Testing State Machines

**When:** Testing logic classes with multiple states (LootCorpseLogic, HealPatientLogic)

```csharp
[Fact]
public void Update_ReachesTarget_TransitionsToLootingState()
{
    // Arrange
    var logic = CreateLootCorpseLogic(distanceToTarget: 1.0f);
    
    // Act
    logic.Update(new ActionData());
    
    // Assert
    logic.CurrentState.Should().Be(ELootState.Looting);
}
```

### Testing Configuration Bounds

**When:** Validating BepInEx config constraints

```csharp
[Theory]
[InlineData(5, 10)]      // Below minimum, should clamp to 10
[InlineData(250, 200)]   // Above maximum, should clamp to 200
[InlineData(50, 50)]     // Valid value, unchanged
public void SearchRadius_ClampsToValidRange(float input, float expected)
{
    var config = new BotMindConfig { SearchRadius = input };
    config.SearchRadius.Should().Be(expected);
}
```

## Running Tests

```bash
# Run all tests
dotnet test src/tests/Blackhorse311.BotMind.Tests.csproj

# Run with verbose output
dotnet test --logger "console;verbosity=detailed"

# Run specific test class
dotnet test --filter "FullyQualifiedName~LootFinderTests"

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"
```

## See Also

- [patterns](references/patterns.md) - Test patterns and FluentAssertions usage
- [workflows](references/workflows.md) - TDD workflows and CI integration

## Related Skills

- See the **csharp** skill for language patterns used in tests
- See the **dotnet** skill for build and project configuration