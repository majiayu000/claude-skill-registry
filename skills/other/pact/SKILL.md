---
name: pact
description: >
  Guidance for Pact contract testing framework in .NET.
  USE FOR: consumer-driven contract testing, verifying API compatibility between microservices,
  preventing breaking API changes, generating and verifying Pact files, provider state management,
  CI/CD integration with Pact Broker.
  DO NOT USE FOR: end-to-end testing (use Playwright), unit testing (use xUnit with Moq),
  load testing, or testing internal implementation details.
license: MIT
metadata:
  displayName: "Pact"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Pact Documentation"
    url: "https://docs.pact.io/"
  - title: "PactNet GitHub Repository"
    url: "https://github.com/pact-foundation/pact-net"
  - title: "PactNet NuGet Package"
    url: "https://www.nuget.org/packages/PactNet"
---

# Pact

## Overview

Pact is a consumer-driven contract testing framework that ensures API compatibility between services without requiring both services to run simultaneously. In a Pact workflow, the consumer (API client) defines expectations about the provider's API in a Pact file, and the provider independently verifies that it satisfies those expectations. This catches breaking changes early, before they reach integration or staging environments. The .NET implementation uses `PactNet` to write consumer tests that generate Pact files and provider tests that verify them. Pact Broker provides a central repository for sharing Pact files between teams.

## Consumer Test Setup

Define consumer expectations for a provider's API using PactNet.

```csharp
using PactNet;
using System.Net.Http.Json;
using Xunit;
using Xunit.Abstractions;

public class UserApiConsumerTests
{
    private readonly IPactBuilderV4 _pactBuilder;

    public UserApiConsumerTests(ITestOutputHelper output)
    {
        var pact = Pact.V4(
            consumer: "UserWebApp",
            provider: "UserService",
            new PactConfig
            {
                PactDir = Path.Combine("..", "..", "..", "pacts"),
                LogLevel = PactLogLevel.Information
            });

        _pactBuilder = pact.WithHttpInteractions();
    }

    [Fact]
    public async Task GetUser_Returns_User_When_Exists()
    {
        // Arrange: define the expected interaction
        _pactBuilder
            .UponReceiving("a request to get user 1")
            .Given("user 1 exists")
            .WithRequest(HttpMethod.Get, "/api/users/1")
            .WithHeader("Accept", "application/json")
            .WillRespond()
            .WithStatus(System.Net.HttpStatusCode.OK)
            .WithHeader("Content-Type", "application/json; charset=utf-8")
            .WithJsonBody(new
            {
                id = 1,
                name = "Alice Smith",
                email = "alice@example.com",
                role = "admin"
            });

        await _pactBuilder.VerifyAsync(async ctx =>
        {
            // Act: use the real HTTP client against the Pact mock server
            var client = new HttpClient
            {
                BaseAddress = ctx.MockServerUri
            };

            var user = await client.GetFromJsonAsync<UserDto>(
                "/api/users/1");

            // Assert
            Assert.NotNull(user);
            Assert.Equal("Alice Smith", user.Name);
            Assert.Equal("alice@example.com", user.Email);
        });
    }

    [Fact]
    public async Task GetUser_Returns_404_When_Not_Found()
    {
        _pactBuilder
            .UponReceiving("a request to get a non-existent user")
            .Given("user 999 does not exist")
            .WithRequest(HttpMethod.Get, "/api/users/999")
            .WillRespond()
            .WithStatus(System.Net.HttpStatusCode.NotFound);

        await _pactBuilder.VerifyAsync(async ctx =>
        {
            var client = new HttpClient
            {
                BaseAddress = ctx.MockServerUri
            };

            var response = await client.GetAsync("/api/users/999");

            Assert.Equal(System.Net.HttpStatusCode.NotFound,
                response.StatusCode);
        });
    }

    [Fact]
    public async Task CreateUser_Returns_Created()
    {
        _pactBuilder
            .UponReceiving("a request to create a new user")
            .Given("the users endpoint is available")
            .WithRequest(HttpMethod.Post, "/api/users")
            .WithHeader("Content-Type", "application/json; charset=utf-8")
            .WithJsonBody(new
            {
                name = "Bob Jones",
                email = "bob@example.com"
            })
            .WillRespond()
            .WithStatus(System.Net.HttpStatusCode.Created)
            .WithHeader("Content-Type", "application/json; charset=utf-8")
            .WithJsonBody(new
            {
                id = 2,
                name = "Bob Jones",
                email = "bob@example.com"
            });

        await _pactBuilder.VerifyAsync(async ctx =>
        {
            var client = new HttpClient
            {
                BaseAddress = ctx.MockServerUri
            };

            var response = await client.PostAsJsonAsync("/api/users", new
            {
                name = "Bob Jones",
                email = "bob@example.com"
            });

            Assert.Equal(System.Net.HttpStatusCode.Created,
                response.StatusCode);
        });
    }
}
```

## Provider Verification

Verify that the provider API satisfies all consumer contracts.

```csharp
using PactNet;
using PactNet.Infrastructure.Middleware;
using PactNet.Verifier;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;
using Xunit.Abstractions;

public class UserApiProviderTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;
    private readonly ITestOutputHelper _output;

    public UserApiProviderTests(
        WebApplicationFactory<Program> factory,
        ITestOutputHelper output)
    {
        _factory = factory;
        _output = output;
    }

    [Fact]
    public void Provider_Honors_Consumer_Contracts()
    {
        // Start the real provider API
        var client = _factory.CreateClient();
        var uri = _factory.Server.BaseAddress;

        var verifier = new PactVerifier(
            "UserService",
            new PactVerifierConfig
            {
                LogLevel = PactLogLevel.Information
            });

        verifier
            .WithHttpEndpoint(uri)
            .WithPactBrokerSource(new Uri("https://pact-broker.example.com"),
                options =>
                {
                    options.ConsumerVersionSelectors(
                        new ConsumerVersionSelector
                        {
                            MainBranch = true
                        });
                    options.PublishResults(
                        providerVersion: "1.0.0",
                        providerBranch: "main");
                })
            .WithProviderStateUrl(
                new Uri(uri, "/provider-states"))
            .Verify();
    }
}
```

## Provider States

Set up provider state so the provider matches consumer expectations.

```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("provider-states")]
public class ProviderStatesController : ControllerBase
{
    private readonly IUserRepository _repo;

    public ProviderStatesController(IUserRepository repo)
    {
        _repo = repo;
    }

    [HttpPost]
    public async Task<IActionResult> SetState(
        [FromBody] ProviderStateRequest request)
    {
        switch (request.State)
        {
            case "user 1 exists":
                await _repo.CreateAsync(new User
                {
                    Id = 1,
                    Name = "Alice Smith",
                    Email = "alice@example.com",
                    Role = "admin"
                });
                break;

            case "user 999 does not exist":
                await _repo.DeleteAsync(999);
                break;

            case "the users endpoint is available":
                // No specific setup needed
                break;

            default:
                return BadRequest(
                    $"Unknown provider state: {request.State}");
        }

        return Ok();
    }
}

public record ProviderStateRequest(
    string State,
    Dictionary<string, string>? Params);
```

## Pact with Message-Based Contracts

Test event-driven communication contracts (e.g., message queues).

```csharp
using PactNet;
using System.Text.Json;
using Xunit;

public class OrderEventConsumerTests
{
    [Fact]
    public void Handles_OrderCreated_Message()
    {
        var pact = Pact.V4(
            consumer: "ShippingService",
            provider: "OrderService",
            new PactConfig
            {
                PactDir = Path.Combine("..", "..", "..", "pacts")
            });

        var messagePact = pact.WithMessageInteractions();

        messagePact
            .ExpectsToReceive("an OrderCreated event")
            .Given("order 123 has been placed")
            .WithJsonContent(new
            {
                eventType = "OrderCreated",
                orderId = "order-123",
                customerId = "cust-456",
                totalAmount = 99.99,
                items = new[]
                {
                    new { productId = "prod-1", quantity = 2 }
                }
            })
            .Verify<OrderCreatedEvent>(message =>
            {
                Assert.Equal("order-123", message.OrderId);
                Assert.Equal("cust-456", message.CustomerId);
                Assert.Equal(99.99m, message.TotalAmount);
            });
    }
}
```

## Contract Testing Workflow

| Stage | Action | Owner | Tool |
|-------|--------|-------|------|
| 1. Consumer test | Define expectations, generate Pact file | Consumer team | PactNet consumer |
| 2. Publish Pact | Upload Pact file to Pact Broker | Consumer CI | Pact Broker CLI |
| 3. Provider verify | Run provider tests against Pact | Provider team | PactNet verifier |
| 4. Publish results | Report verification status to Broker | Provider CI | PactNet verifier |
| 5. Can-I-Deploy | Check compatibility before deployment | Both teams | Pact CLI |

## Best Practices

1. **Write consumer tests first, then verify on the provider**: consumer-driven means the consumer defines the contract; the provider adapts to satisfy it, not the other way around.
2. **Use provider states to set up test prerequisites**: define `Given("user 1 exists")` states so the provider can seed data before each interaction is verified.
3. **Test only the contract, not business logic**: Pact tests should verify request/response shapes, status codes, and field types, not complex business calculations.
4. **Use Pact Broker for sharing contracts between teams**: do not pass Pact JSON files through email or shared drives; use the Broker to track versions, branches, and verification results.
5. **Run `can-i-deploy` before every deployment**: integrate the Pact CLI `can-i-deploy` check into your CI/CD pipeline to block deployments when contracts are incompatible.
6. **Version Pact files with the consumer's Git SHA**: tag each Pact publication with the exact commit hash so provider verification results map back to specific consumer versions.
7. **Keep interactions minimal and focused**: each Pact interaction should test one API call; do not chain multiple requests in a single interaction.
8. **Use consumer version selectors for branch-based testing**: configure `ConsumerVersionSelector` with `MainBranch = true` to verify against the latest consumer on the main branch.
9. **Handle provider state cleanup between interactions**: reset the provider's test database or state after each interaction verification to prevent test pollution.
10. **Do not use Pact for performance or load testing**: Pact validates contract compatibility, not API performance; use dedicated load testing tools for throughput and latency measurements.
