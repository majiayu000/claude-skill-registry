---
name: provider-verification
description: Provider verification workflow for contract testing
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Provider Verification Skill

## When to Use This Skill

Use this skill when:

- **Provider Verification tasks** - Working on provider verification workflow for contract testing
- **Planning or design** - Need guidance on Provider Verification approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Implement provider-side verification of consumer contracts using Pact.

## MANDATORY: Documentation-First Approach

Before implementing provider verification:

1. **Invoke `docs-management` skill** for verification patterns
2. **Verify Pact provider patterns** via MCP servers (context7, perplexity)
3. **Base guidance on Pact documentation and verification best practices**

## Provider Verification Overview

```text
PROVIDER VERIFICATION PROCESS:

┌────────────────────────────────────────────────────────────────┐
│                    PROVIDER VERIFICATION                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. FETCH CONTRACTS                                             │
│     ┌──────────────────────────────────────────────┐           │
│     │ Get contracts from Pact Broker               │           │
│     │ - For specific consumers                     │           │
│     │ - For specific branches/environments         │           │
│     │ - Using consumer version selectors           │           │
│     └──────────────────────────────────────────────┘           │
│                                                                 │
│  2. SETUP PROVIDER STATES                                       │
│     ┌──────────────────────────────────────────────┐           │
│     │ For each interaction:                        │           │
│     │ - Parse provider state from contract         │           │
│     │ - Execute state handler                      │           │
│     │ - Seed required data                         │           │
│     │ - Configure dependencies                     │           │
│     └──────────────────────────────────────────────┘           │
│                                                                 │
│  3. REPLAY INTERACTIONS                                         │
│     ┌──────────────────────────────────────────────┐           │
│     │ For each interaction:                        │           │
│     │ - Send request to real provider              │           │
│     │ - Capture actual response                    │           │
│     │ - Compare against expected                   │           │
│     │ - Apply matching rules                       │           │
│     └──────────────────────────────────────────────┘           │
│                                                                 │
│  4. PUBLISH RESULTS                                             │
│     ┌──────────────────────────────────────────────┐           │
│     │ Report verification results to Pact Broker   │           │
│     │ - Tag with provider version                  │           │
│     │ - Include branch/environment info            │           │
│     │ - Enable can-i-deploy checks                 │           │
│     └──────────────────────────────────────────────┘           │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Provider Verification Test (C#)

```csharp
// Provider verification test
// File: OrdersApi.Provider.Tests/OrdersApiProviderTests.cs

using PactNet;
using PactNet.Verifier;
using Microsoft.AspNetCore.Mvc.Testing;

public class OrdersApiProviderTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;
    private readonly ITestOutputHelper _output;

    public OrdersApiProviderTests(
        WebApplicationFactory<Program> factory,
        ITestOutputHelper output)
    {
        _factory = factory;
        _output = output;
    }

    [Fact]
    public void VerifyPacts_WithAllConsumers()
    {
        // Arrange
        var config = new PactVerifierConfig
        {
            LogLevel = PactLogLevel.Information,
            Outputters = new[] { new XUnitOutput(_output) }
        };

        // Start the provider API
        using var server = _factory.CreateDefaultClient();
        var providerUri = _factory.Server.BaseAddress;

        // Act & Assert
        using var verifier = new PactVerifier("OrdersApi", config);

        verifier
            .WithHttpEndpoint(providerUri)
            .WithProviderStateUrl(new Uri(providerUri, "/provider-states"))
            .WithPactBrokerSource(new Uri("https://pact-broker.example.com"), options =>
            {
                options.TokenAuthentication("your-token");
                options.ConsumerVersionSelectors(
                    new ConsumerVersionSelector
                    {
                        MainBranch = true
                    },
                    new ConsumerVersionSelector
                    {
                        DeployedOrReleased = true
                    }
                );
                options.PublishVerificationResults(
                    providerVersion: Environment.GetEnvironmentVariable("GIT_SHA") ?? "local",
                    providerBranch: Environment.GetEnvironmentVariable("GIT_BRANCH"));
            })
            .Verify();
    }
}
```

## Provider State Handlers

```csharp
// Provider state endpoint
// File: OrdersApi/Controllers/ProviderStatesController.cs

[ApiController]
[Route("provider-states")]
public class ProviderStatesController : ControllerBase
{
    private readonly OrdersDbContext _context;
    private readonly IServiceProvider _serviceProvider;

    public ProviderStatesController(
        OrdersDbContext context,
        IServiceProvider serviceProvider)
    {
        _context = context;
        _serviceProvider = serviceProvider;
    }

    [HttpPost]
    public async Task<IActionResult> SetupState([FromBody] ProviderStateRequest request)
    {
        // Clear existing test data
        await CleanupTestData();

        // Handle the specific state
        await HandleState(request.State, request.Params);

        return Ok();
    }

    private async Task HandleState(string state, Dictionary<string, object>? parameters)
    {
        switch (state)
        {
            case "an order with id 123 exists":
                await SeedOrder("123", parameters);
                break;

            case "no order with id non-existent exists":
                // No setup needed - just ensure it doesn't exist
                break;

            case "customer customer-789 exists":
                await SeedCustomer("customer-789", parameters);
                break;

            case "an order was created":
                // For message pacts - seed the event data
                await SeedOrderCreatedEvent(parameters);
                break;

            case "the system has orders matching search criteria":
                await SeedMultipleOrders(parameters);
                break;

            default:
                throw new NotSupportedException($"Unknown provider state: {state}");
        }
    }

    private async Task SeedOrder(string orderId, Dictionary<string, object>? parameters)
    {
        var order = new Order
        {
            Id = orderId,
            CustomerId = GetParam(parameters, "customerId", "customer-456"),
            Status = GetParam(parameters, "status", "Pending"),
            Items = new List<OrderItem>
            {
                new OrderItem
                {
                    ProductId = "prod-1",
                    Quantity = 1,
                    Price = 99.99m
                }
            },
            Total = 99.99m,
            CreatedAt = DateTime.UtcNow
        };

        _context.Orders.Add(order);
        await _context.SaveChangesAsync();
    }

    private async Task SeedCustomer(string customerId, Dictionary<string, object>? parameters)
    {
        var customer = new Customer
        {
            Id = customerId,
            Name = GetParam(parameters, "name", "Test Customer"),
            Email = GetParam(parameters, "email", "test@example.com")
        };

        _context.Customers.Add(customer);
        await _context.SaveChangesAsync();
    }

    private async Task CleanupTestData()
    {
        // Remove test data to ensure clean state
        _context.Orders.RemoveRange(_context.Orders);
        _context.Customers.RemoveRange(_context.Customers);
        await _context.SaveChangesAsync();
    }

    private static T GetParam<T>(Dictionary<string, object>? parameters, string key, T defaultValue)
    {
        if (parameters == null || !parameters.TryGetValue(key, out var value))
            return defaultValue;

        return (T)Convert.ChangeType(value, typeof(T));
    }
}

public class ProviderStateRequest
{
    public string State { get; set; } = string.Empty;
    public Dictionary<string, object>? Params { get; set; }
}
```

## Consumer Version Selectors

```text
CONSUMER VERSION SELECTORS:

Purpose: Specify which consumer pacts to verify

┌─────────────────────────────────────────────────────────────────┐
│ Selector               │ Meaning                                │
├─────────────────────────────────────────────────────────────────┤
│ MainBranch = true      │ Latest from main/master branch         │
│ DeployedOrReleased     │ Currently deployed versions            │
│ Branch = "feature-x"   │ Specific branch                        │
│ Consumer = "OrdersUI"  │ Specific consumer only                 │
│ MatchingBranch = true  │ Same branch as provider                │
│ Latest = true          │ Latest version (any branch)            │
│ Tag = "production"     │ Tagged with specific tag               │
└─────────────────────────────────────────────────────────────────┘

COMMON PATTERNS:

CI Pipeline (feature branch):
- MainBranch = true (always verify against main)
- MatchingBranch = true (verify against same feature branch)
- DeployedOrReleased = true (verify against production)

Release Pipeline:
- DeployedOrReleased = true (all deployed versions)
- MainBranch = true (latest main)

Development:
- Latest = true, Consumer = "OrdersUI" (specific consumer)
```

## Provider State Patterns

```text
STATE HANDLER PATTERNS:

1. DATA SEEDING
   - Create required entities in database
   - Set up relationships
   - Initialize with specific values

2. FEATURE FLAGS
   - Enable/disable features
   - Configure behavior modes

3. EXTERNAL SERVICE MOCKS
   - Configure mock responses
   - Simulate external dependencies

4. TIME MANIPULATION
   - Set system time for date-sensitive tests
   - Configure clock providers

5. AUTHENTICATION
   - Set up test users
   - Configure permissions

BEST PRACTICES:

DO:
✓ Isolate test data (don't affect real data)
✓ Clean up between states
✓ Support parameterized states
✓ Keep states deterministic
✓ Document state requirements

DON'T:
✗ Share state between tests
✗ Rely on existing data
✗ Use real external services
✗ Create side effects
✗ Make states order-dependent
```

## Provider State Test Isolation

```csharp
// Using test containers for isolation
// File: OrdersApi.Provider.Tests/IsolatedProviderTests.cs

public class IsolatedProviderTests : IAsyncLifetime
{
    private readonly PostgreSqlContainer _postgres;
    private WebApplicationFactory<Program> _factory = null!;

    public IsolatedProviderTests()
    {
        _postgres = new PostgreSqlBuilder()
            .WithImage("postgres:16-alpine")
            .Build();
    }

    public async Task InitializeAsync()
    {
        await _postgres.StartAsync();

        _factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(builder =>
            {
                builder.ConfigureServices(services =>
                {
                    // Replace database with test container
                    services.RemoveAll<DbContextOptions<OrdersDbContext>>();
                    services.AddDbContext<OrdersDbContext>(options =>
                        options.UseNpgsql(_postgres.GetConnectionString()));
                });
            });

        // Apply migrations
        using var scope = _factory.Services.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<OrdersDbContext>();
        await context.Database.MigrateAsync();
    }

    public async Task DisposeAsync()
    {
        await _factory.DisposeAsync();
        await _postgres.DisposeAsync();
    }

    [Fact]
    public void VerifyPacts()
    {
        // Test implementation using isolated database
    }
}
```

## Verification Results

```text
VERIFICATION OUTPUT:

Verifying a pact between OrdersClient and OrdersApi
  Given an order with id 123 exists
    a request for an existing order
      with GET /orders/123
        returns a response which
          has status code 200 ✓
          has a matching body ✓
          includes headers ✓

  Given no order with id non-existent exists
    a request for a non-existent order
      with GET /orders/non-existent
        returns a response which
          has status code 404 ✓
          has a matching body ✓

  Given customer customer-789 exists
    a request to create a new order
      with POST /orders
        returns a response which
          has status code 201 ✓
          has a matching body ✓
          includes headers ✓

3 interactions, 0 failures

FAILURE EXAMPLE:

  Given an order with id 123 exists
    a request for an existing order
      with GET /orders/123
        returns a response which
          has status code 200 ✓
          has a matching body
            $.status -> Expected "Pending" but got "Processing" ✗

1 interaction, 1 failure
```

## CI/CD Integration

```yaml
# GitHub Actions example
# .github/workflows/provider-verification.yml

name: Provider Verification

on:
  push:
    branches: [main, 'feature/**']
  workflow_dispatch:
    inputs:
      consumer:
        description: 'Specific consumer to verify'
        required: false

jobs:
  verify:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '10.0.x'

      - name: Restore
        run: dotnet restore

      - name: Build
        run: dotnet build --no-restore

      - name: Verify Pacts
        env:
          GIT_SHA: ${{ github.sha }}
          GIT_BRANCH: ${{ github.ref_name }}
          PACT_BROKER_BASE_URL: ${{ secrets.PACT_BROKER_URL }}
          PACT_BROKER_TOKEN: ${{ secrets.PACT_BROKER_TOKEN }}
        run: dotnet test --filter "Category=Pact"

      - name: Can I Deploy?
        run: |
          pact-broker can-i-deploy \
            --pacticipant OrdersApi \
            --version ${{ github.sha }} \
            --to-environment production
```

## Troubleshooting

```text
COMMON VERIFICATION FAILURES:

1. STATE NOT FOUND
   Error: Unknown provider state: "order exists"
   Fix: Implement the state handler or check state name spelling

2. DATA NOT SEEDED
   Error: 404 when expecting 200
   Fix: Verify state handler seeds data correctly

3. RESPONSE MISMATCH
   Error: Expected "Pending" but got "Processing"
   Fix: Check state sets correct values, or use matchers in contract

4. MISSING FIELDS
   Error: $.newField was not found
   Fix: Add field to response or update contract to use optional matcher

5. STATE CLEANUP ISSUES
   Error: Duplicate key violation
   Fix: Ensure cleanup runs before each state setup

DEBUGGING TIPS:
• Enable verbose logging in verifier
• Log state handler execution
• Check database state after setup
• Verify provider URL is correct
• Ensure authentication is configured
```

## Assessment Template

```markdown
# Provider Verification Assessment: [Provider Name]

## Provider Profile
- **Provider:** [Name]
- **Consumers:** [List]
- **Test Environment:** [Local/CI/Isolated]

## State Handlers

| State | Handler | Data Seeded |
|-------|---------|-------------|
| [State] | [Method] | [What data] |

## Verification Configuration

- **Consumer Selectors:** [MainBranch, DeployedOrReleased, etc.]
- **Publish Results:** [Yes/No]
- **Provider Version:** [Source]
- **Branch Tracking:** [Yes/No]

## Test Isolation

- [ ] Database isolated per test run
- [ ] External services mocked
- [ ] State cleanup between interactions
- [ ] No shared mutable state

## CI/CD Integration

- [ ] Verification in pipeline
- [ ] Results published to broker
- [ ] Can-I-Deploy gate configured
- [ ] Branch protection rules set

## Issues and Gaps

| Issue | Severity | Resolution |
|-------|----------|------------|
| [Issue] | [H/M/L] | [Plan] |
```

## Workflow

When implementing provider verification:

1. **Setup Verification Tests**: Create provider test project
2. **Implement State Handlers**: Handle all required states
3. **Configure Version Selectors**: Choose which pacts to verify
4. **Ensure Test Isolation**: Isolated database, mocked services
5. **Integrate with CI/CD**: Automate verification
6. **Publish Results**: Enable can-i-deploy checks

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
