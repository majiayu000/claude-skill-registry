---
version: 1.1.0
name: dev-tdd-backend
description: >
  Test-driven development workflow for C#/.NET using xUnit, NSubstitute,
  and event sourcing (EventSourcing). Covers aggregate testing, specification
  testing, projection testing, and proper test isolation.
  Invoked via /dev-tdd (unified entry point) — not directly.
disable-model-invocation: true
user-invocable: false
context: fork
argument-hint: "[feature description]"
---

# TDD Workflow — Backend (.NET)

Write tests first, then implement. For C#/.NET backend code.

> **Stack:** xUnit, NSubstitute, EventSourcing, Specifications

## When to Activate

- Writing new services, repositories, or API endpoints
- Fixing bugs (write a test that reproduces the bug first)
- Refactoring existing backend code
- Adding new domain logic, aggregates, or specifications

## Core Principles

1. **Tests BEFORE code** — always write the failing test first
2. **80%+ coverage** — unit + integration combined
3. **Test behavior, not implementation** — tests should survive refactors
4. **Isolated tests** — each test sets up its own data, no shared state

## Test Naming Convention

Use the pattern: `Operation_WhenCondition_ShouldOutcome`

```
VerifyEmail_WithCorrectCode_ShouldSucceedAndSetEmail
PlaceOrder_WithEmptyItems_ShouldThrowValidationException
Toggle_WhenArchived_ShouldFail
```

## TDD Cycle

```
RED → GREEN → REFACTOR → repeat
 │       │        │
 │       │        └─ Improve code while tests stay green
 │       └─ Write minimal code to pass
 └─ Write a failing test
```

## Unit Test Pattern (xUnit + NSubstitute)

For testing services with injected dependencies:

```csharp
public class OrderServiceTests
{
    private readonly IOrderRepository _repository;
    private readonly OrderService _sut; // system under test

    public OrderServiceTests()
    {
        _repository = Substitute.For<IOrderRepository>();
        _sut = new OrderService(_repository);
    }

    [Fact]
    public async Task PlaceOrder_WithValidItems_ShouldCreateOrder()
    {
        // Arrange
        var items = new[] { new OrderItem("SKU-001", 2, 9.99m) };

        // Act
        var result = await _sut.PlaceOrderAsync(items);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(OrderStatus.Placed, result.Status);
        Assert.Single(result.Items);
        await _repository.Received(1).SaveAsync(Arg.Any<Order>());
    }

    [Fact]
    public async Task PlaceOrder_WithEmptyItems_ShouldThrowValidationException()
    {
        // Arrange
        var items = Array.Empty<OrderItem>();

        // Act
        var act = () => _sut.PlaceOrderAsync(items);

        // Assert
        await Assert.ThrowsAsync<ValidationException>(act);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(-100)]
    public async Task PlaceOrder_WithInvalidQuantity_ShouldThrowValidationException(int quantity)
    {
        // Arrange
        var items = new[] { new OrderItem("SKU-001", quantity, 9.99m) };

        // Act
        var act = () => _sut.PlaceOrderAsync(items);

        // Assert
        await Assert.ThrowsAsync<ValidationException>(act);
    }
}
```

## Nested Test Class Pattern

Organize tests by operation using nested classes. Useful for aggregates with many operations:

```csharp
public class FeatureFlagTests
{
    public class Create : FeatureFlagTests
    {
        [Fact]
        public void Create_WithValidName_ShouldSetNameAndDisabledState()
        {
            // Arrange & Act & Assert
        }
    }

    public class Toggle : FeatureFlagTests
    {
        [Fact]
        public void Toggle_WhenDisabled_ShouldEnable()
        {
            // Arrange & Act & Assert
        }
    }

    public class Archive : FeatureFlagTests
    {
        [Fact]
        public void Archive_WhenEnabled_ShouldDisableAndArchive()
        {
            // Arrange & Act & Assert
        }
    }
}
```

## Event Sourcing Testing (EventSourcing)

Aggregates are partial classes (generated + manual halves). Test them by applying events through an event stream and asserting aggregate state.

### Testing Aggregate State

```csharp
public class ProfileTests : IAsyncLifetime
{
    private TestContext _context = null!;

    public async Task InitializeAsync()
    {
        _context = TestSetup.GetContext();
    }

    public Task DisposeAsync() => Task.CompletedTask;

    [Fact]
    public async Task Create_ViaSocialLogin_ShouldSetProviderAndExternalId()
    {
        // Arrange
        var profileId = ProfileId.New();
        var stream = _context.Stream.Session();
        await stream.AppendAsync(new ProfileCreatedViaSocialLogin(profileId, "github", "user123"));

        // Act
        var sut = await _context.ProfileFactory.GetAsync(profileId); // system under test

        // Assert
        Assert.Equal("github", sut.Provider);
        Assert.Equal("user123", sut.ExternalId);
    }

    [Fact]
    public async Task VerifyEmail_WithCorrectCode_ShouldSucceedAndSetEmail()
    {
        // Arrange
        var profileId = ProfileId.New();
        var stream = _context.Stream.Session();
        await stream.AppendAsync(new ProfileCreatedViaSocialLogin(profileId, "github", "user123"));

        var sut = await _context.ProfileFactory.GetAsync(profileId); // system under test

        // Act
        var result = sut.VerifyEmail("correct-code", TimeProvider.System);

        // Assert
        Assert.True(result.IsSuccess);
        Assert.Equal("user@example.com", sut.Email);
    }

    [Fact]
    public async Task VerifyEmail_WithExpiredCode_ShouldFail()
    {
        // Arrange
        var profileId = ProfileId.New();
        var stream = _context.Stream.Session();
        await stream.AppendAsync(new ProfileCreatedViaSocialLogin(profileId, "github", "user123"));

        var sut = await _context.ProfileFactory.GetAsync(profileId); // system under test

        // Act
        var result = sut.VerifyEmail("expired-code", TimeProvider.System);

        // Assert
        Assert.False(result.IsSuccess);
    }
}
```

### Key Concepts

- **`TestContext`** — provided by `TestSetup.GetContext()`, contains stream and factories
- **`IEventStream`** — use `_context.Stream.Session()` to get a session, then `AppendAsync()` to add events
- **Partial classes** — aggregates have a generated half (from event definitions) and a manual half (business logic). Tests exercise the manual half.
- **State via events** — set up aggregate state by appending the events that would have produced it, then call methods and assert

## Integration Tests (Event Sourcing)

Test full aggregate lifecycles using `EventSourcing.Testing`:

```csharp
public class ProfileLifecycleTests : IAsyncLifetime
{
    private TestContext _context = null!;

    public async Task InitializeAsync()
    {
        _context = TestSetup.GetContext();
    }

    public Task DisposeAsync() => Task.CompletedTask;

    [Fact]
    public async Task VerifyEmail_WithCorrectCode_ShouldSucceedAndSetEmail()
    {
        // Arrange
        var profileId = ProfileId.New();
        var stream = _context.Stream.Session();
        await stream.AppendAsync(new ProfileCreatedViaSocialLogin(profileId, "github", "user123"));

        var sut = await _context.ProfileFactory.GetAsync(profileId);

        // Act
        var result = sut.VerifyEmail("correct-code", TimeProvider.System);

        // Assert
        Assert.True(result.IsSuccess);
        Assert.Equal("user@example.com", sut.Email);
    }
}
```

## Testing Projections

Test that read model projections correctly transform events into query-friendly views:

```csharp
public class OrderSummaryProjectionTests : IAsyncLifetime
{
    private TestContext _context = null!;

    public async Task InitializeAsync()
    {
        _context = TestSetup.GetContext();
    }

    public Task DisposeAsync() => Task.CompletedTask;

    [Fact]
    public async Task Project_AfterOrderCreated_ShouldContainOrderInSummary()
    {
        // Arrange
        var orderId = OrderId.New();
        var stream = _context.Stream.Session();
        await stream.AppendAsync(new OrderCreated(orderId, "customer-1", DateTime.UtcNow));
        await stream.AppendAsync(new OrderItemAdded(orderId, "SKU-001", 2, 9.99m));

        // Act
        var projection = await _context.GetProjection<OrderSummaryProjection>();

        // Assert
        var summary = projection.GetById(orderId);
        Assert.NotNull(summary);
        Assert.Equal("customer-1", summary.CustomerId);
        Assert.Equal(1, summary.ItemCount);
    }

    [Fact]
    public async Task Project_AfterOrderCancelled_ShouldReflectCancelledStatus()
    {
        // Arrange
        var orderId = OrderId.New();
        var stream = _context.Stream.Session();
        await stream.AppendAsync(new OrderCreated(orderId, "customer-1", DateTime.UtcNow));
        await stream.AppendAsync(new OrderCancelled(orderId, "Changed my mind"));

        // Act
        var projection = await _context.GetProjection<OrderSummaryProjection>();

        // Assert
        var summary = projection.GetById(orderId);
        Assert.NotNull(summary);
        Assert.Equal(OrderStatus.Cancelled, summary.Status);
    }
}
```

## Specification Testing (Specifications)

Test domain specifications by asserting `IsSatisfiedBy()` against various inputs:

```csharp
public class ValidOrderSpecificationTests
{
    private readonly ValidOrderSpecification _sut = new(); // system under test

    [Fact]
    public void IsSatisfiedBy_WithValidOrder_ShouldReturnTrue()
    {
        // Arrange
        var order = new Order { Status = OrderStatus.Placed, ItemCount = 3 };

        // Act
        var result = _sut.IsSatisfiedBy(order);

        // Assert
        Assert.True(result);
    }

    [Fact]
    public void IsSatisfiedBy_WithNoItems_ShouldReturnFalse()
    {
        // Arrange
        var order = new Order { Status = OrderStatus.Placed, ItemCount = 0 };

        // Act
        var result = _sut.IsSatisfiedBy(order);

        // Assert
        Assert.False(result);
    }

    [Fact]
    public void IsSatisfiedBy_WithCancelledOrder_ShouldReturnFalse()
    {
        // Arrange
        var order = new Order { Status = OrderStatus.Cancelled, ItemCount = 3 };

        // Act
        var result = _sut.IsSatisfiedBy(order);

        // Assert
        Assert.False(result);
    }
}
```

## Test File Organization

```
src/
├── MyApp.Api/
│   ├── Endpoints/OrderEndpoints.cs
│   └── Services/OrderService.cs
├── MyApp.Domain/
│   ├── Aggregates/Order.cs
│   ├── Events/OrderCreated.cs
│   └── Specifications/ValidOrderSpecification.cs
└── MyApp.Api.Tests/
    ├── Domain/
    │   └── OrderTests.cs (nested classes per operation)
    ├── Integration/
    │   └── OrderEndpointTests.cs
    └── Specifications/
        └── ValidOrderSpecificationTests.cs
```

## Running Tests

```bash
# All tests
dotnet test

# Specific project
dotnet test tests/MyApp.Api.Tests/

# With coverage
dotnet test --collect:"XPlat Code Coverage"

# Filter by trait
dotnet test --filter "Category=Unit"
```

## Aspire Runtime Verification (Optional)

After tests pass (GREEN phase), if the Aspire AppHost is running, verify there are no runtime errors that unit tests miss:

```
mcp__aspire__execute_resource_command  resourceName: "api"  commandName: "resource-restart"
```

Wait for healthy state, then check for errors:

```
mcp__aspire__list_console_logs  resourceName: "api"
```

Look for:
- **DI resolution failures** — a new service or aggregate factory wasn't registered
- **Startup crashes** — configuration binding errors, missing connection strings
- **Event store errors** — stream read failures, serialization issues after adding new event types
- **Projection catch-up errors** — a new event type isn't handled by an existing projection

These are errors that unit tests (which mock dependencies) won't catch, but that will fail immediately at runtime.

Skip if Aspire is not running or the project doesn't use Aspire.

## Coverage Thresholds

Target 80%+. Configure in `.csproj` or `Directory.Build.props`:

```xml
<PropertyGroup>
  <CollectCoverage>true</CollectCoverage>
  <Threshold>80</Threshold>
</PropertyGroup>
```

## Common Mistakes to Avoid

- **Testing implementation details** — test what the caller sees, not internal state
- **Shared test state** — each test creates its own data, use constructor not static fields
- **Skipping error paths** — test failures, validation errors, not just happy paths
- **Not testing aggregate state via events** — always set up state through event replay, not by directly setting properties
- **Missing async assertions** — use `Assert.ThrowsAsync<>()` not `Assert.Throws<>()`
- **Forgetting the manual half** — aggregates are partial classes; test the business logic methods, not the generated code
