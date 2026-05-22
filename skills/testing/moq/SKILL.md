---
name: moq
description: |
  Creates mock objects and configures test dependencies with Moq.
  Use when: writing unit tests that need to isolate dependencies, verify method calls, or simulate service behavior.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Moq Skill

Moq is the mocking framework used throughout VanDaemon for unit testing. All services are registered as singletons and depend on interfaces, making them ideal candidates for mocking. Tests use `Mock<T>` to create test doubles, `Setup()` to configure behavior, and `Verify()` to assert interactions.

## Quick Start

### Basic Service Mock

```csharp
// Mock a service interface
var mockTankService = new Mock<ITankService>();
mockTankService
    .Setup(x => x.GetAllTanksAsync(It.IsAny<CancellationToken>()))
    .ReturnsAsync(new List<Tank> { new Tank { Id = Guid.NewGuid(), Name = "Fresh Water" } });

var controller = new TanksController(mockTankService.Object);
```

### Mock with Argument Matching

```csharp
var mockControlService = new Mock<IControlService>();
mockControlService
    .Setup(x => x.SetControlStateAsync(
        It.Is<Guid>(id => id != Guid.Empty),
        It.IsAny<object>(),
        It.IsAny<CancellationToken>()))
    .ReturnsAsync(true);
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `Mock<T>` | Create mock instance | `new Mock<ITankService>()` |
| `.Object` | Get mocked instance | `mock.Object` |
| `Setup()` | Configure method behavior | `.Setup(x => x.Method())` |
| `Returns()` | Sync return value | `.Returns(value)` |
| `ReturnsAsync()` | Async return value | `.ReturnsAsync(value)` |
| `It.IsAny<T>()` | Match any argument | `It.IsAny<CancellationToken>()` |
| `It.Is<T>()` | Match with predicate | `It.Is<Guid>(g => g != Guid.Empty)` |
| `Verify()` | Assert method called | `.Verify(x => x.Method(), Times.Once)` |

## Common Patterns

### Mocking Logger (Serilog via ILogger<T>)

```csharp
var mockLogger = new Mock<ILogger<TankService>>();
var service = new TankService(mockLogger.Object, mockFileStore.Object);

// Verify logging occurred (Moq can't verify extension methods directly)
// Use LoggerFactory or just trust the implementation
```

### Mocking JsonFileStore

```csharp
var mockFileStore = new Mock<IJsonFileStore>();
mockFileStore
    .Setup(x => x.LoadAsync<List<Tank>>("tanks.json", It.IsAny<CancellationToken>()))
    .ReturnsAsync(testTanks);
```

### Mocking SignalR Hub Context

```csharp
var mockHubContext = new Mock<IHubContext<TelemetryHub>>();
var mockClients = new Mock<IHubClients>();
var mockGroup = new Mock<IClientProxy>();

mockHubContext.Setup(x => x.Clients).Returns(mockClients.Object);
mockClients.Setup(x => x.Group("tanks")).Returns(mockGroup.Object);
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **xunit** skill for test structure and assertions
- See the **fluent-assertions** skill for readable assertions
- See the **csharp** skill for async/await patterns used with mocks