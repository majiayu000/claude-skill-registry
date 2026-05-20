---
name: xunit
description: |
  Writes unit tests and integration tests with xUnit framework.
  Use when: writing new tests, adding test coverage, testing services/controllers/plugins, or debugging test failures.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# xUnit Skill

xUnit is the testing framework for VanDaemon. Tests follow the Arrange-Act-Assert pattern with **FluentAssertions** for readable assertions and **Moq** for mocking dependencies. All test projects use the naming convention `{Project}.Tests`.

## Quick Start

### Service Test Pattern

```csharp
public class TankServiceTests
{
    private readonly Mock<ILogger<TankService>> _loggerMock = new();
    private readonly Mock<ISensorPlugin> _sensorMock = new();
    
    [Fact]
    public async Task GetAllTanksAsync_ReturnsOnlyActiveTanks()
    {
        // Arrange
        var service = new TankService(_loggerMock.Object, _sensorMock.Object);
        
        // Act
        var result = await service.GetAllTanksAsync();
        
        // Assert
        result.Should().NotBeNull();
        result.Should().AllSatisfy(t => t.IsActive.Should().BeTrue());
    }
}
```

### Testing with JsonFileStore

```csharp
[Fact]
public async Task SaveAsync_PersistsDataToFile()
{
    // Arrange - use temp directory for isolation
    var tempPath = Path.Combine(Path.GetTempPath(), $"vandaemon-tests-{Guid.NewGuid()}");
    var loggerMock = new Mock<ILogger<JsonFileStore>>();
    var fileStore = new JsonFileStore(loggerMock.Object, tempPath);
    
    try
    {
        // Act
        await fileStore.SaveAsync("tanks", testTanks);
        var loaded = await fileStore.LoadAsync<List<Tank>>("tanks");
        
        // Assert
        loaded.Should().BeEquivalentTo(testTanks);
    }
    finally
    {
        Directory.Delete(tempPath, recursive: true);
    }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `[Fact]` | Single test case | `[Fact] public async Task Method_Condition_Result()` |
| `[Theory]` | Parameterized tests | `[Theory] [InlineData(0)] [InlineData(100)]` |
| `[Collection]` | Shared test context | `[Collection("Database")]` |
| FluentAssertions | Readable assertions | `result.Should().HaveCount(3)` |
| Moq Setup | Define mock behavior | `mock.Setup(x => x.Method()).ReturnsAsync(value)` |

## Common Patterns

### Testing Async Methods with CancellationToken

**When:** Testing any async service method.

```csharp
[Fact]
public async Task GetTankLevelAsync_PassesCancellationToken()
{
    var cts = new CancellationTokenSource();
    _sensorMock.Setup(x => x.ReadValueAsync(It.IsAny<string>(), cts.Token))
        .ReturnsAsync(75.0);
    
    var result = await _service.GetTankLevelAsync(tankId, cts.Token);
    
    _sensorMock.Verify(x => x.ReadValueAsync(It.IsAny<string>(), cts.Token), Times.Once);
}
```

### Testing Collections

```csharp
result.Should().HaveCount(3);
result.Should().ContainSingle(t => t.Type == TankType.FreshWater);
result.Should().AllSatisfy(t => t.IsActive.Should().BeTrue());
result.Should().BeInAscendingOrder(t => t.Name);
```

## Running Tests

```bash
dotnet test VanDaemon.sln                    # All tests
dotnet test --filter "FullyQualifiedName~TankService"  # Specific class
dotnet test --verbosity normal               # See test output
dotnet test --collect:"XPlat Code Coverage"  # With coverage
```

## See Also

- [patterns](references/patterns.md) - Test patterns and anti-patterns
- [workflows](references/workflows.md) - TDD workflow and test organization

## Related Skills

- See the **moq** skill for mocking patterns
- See the **fluent-assertions** skill for assertion syntax
- See the **dotnet** skill for build/run commands