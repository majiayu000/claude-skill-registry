---
name: fake-json-server
description: >
  Guidance for FakeServer and fake JSON API servers for .NET testing.
  USE FOR: mocking REST APIs during development, creating stub HTTP endpoints for integration tests,
  simulating third-party API responses, building prototype backends for frontend development,
  testing HTTP client code without external dependencies.
  DO NOT USE FOR: production API hosting, load testing (use proper test infrastructure),
  contract testing (use Pact), or testing real database interactions (use Testcontainers).
license: MIT
metadata:
  displayName: "Fake JSON Server"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Fake JSON Server GitHub Repository"
    url: "https://github.com/ttu/dotnet-fake-json-server"
  - title: "FakeServer NuGet Package"
    url: "https://www.nuget.org/packages/FakeServer"
---

# Fake JSON Server

## Overview

Fake JSON Server provides lightweight, in-process HTTP servers for testing .NET applications that depend on external REST APIs. Instead of calling real third-party services during tests, you create fake endpoints that return predetermined responses. In .NET, this is typically accomplished using `WebApplicationFactory`, `WireMock.Net`, or custom `DelegatingHandler` implementations. These approaches let you test HTTP client code, retry logic, error handling, and response parsing without network dependencies, rate limits, or flaky external services.

## WebApplicationFactory for In-Process API Faking

Use ASP.NET Core's `WebApplicationFactory` to create a full fake API in-process.

```csharp
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System.Net.Http.Json;
using Xunit;

public class FakeApiFactory : WebApplicationFactory<FakeApiFactory>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.Configure(app =>
        {
            app.UseRouting();
            app.UseEndpoints(endpoints =>
            {
                endpoints.MapGet("/api/users", () => new[]
                {
                    new { Id = 1, Name = "Alice", Email = "alice@example.com" },
                    new { Id = 2, Name = "Bob", Email = "bob@example.com" }
                });

                endpoints.MapGet("/api/users/{id:int}", (int id) =>
                    id == 1
                        ? Results.Ok(new { Id = 1, Name = "Alice", Email = "alice@example.com" })
                        : Results.NotFound());

                endpoints.MapPost("/api/users", (CreateUserRequest req) =>
                    Results.Created($"/api/users/3",
                        new { Id = 3, Name = req.Name, Email = req.Email }));
            });
        });
    }
}

public record CreateUserRequest(string Name, string Email);

public class FakeApiTests : IClassFixture<FakeApiFactory>
{
    private readonly HttpClient _client;

    public FakeApiTests(FakeApiFactory factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetUsers_Returns_List()
    {
        var users = await _client.GetFromJsonAsync<List<UserDto>>(
            "/api/users");

        Assert.NotNull(users);
        Assert.Equal(2, users.Count);
    }

    [Fact]
    public async Task GetUser_NotFound_Returns_404()
    {
        var response = await _client.GetAsync("/api/users/999");

        Assert.Equal(System.Net.HttpStatusCode.NotFound, response.StatusCode);
    }
}
```

## WireMock.Net for HTTP Mocking

Use WireMock.Net for flexible request matching and response stubbing.

```csharp
using WireMock.Server;
using WireMock.RequestBuilders;
using WireMock.ResponseBuilders;
using System.Net.Http.Json;
using Xunit;

public class WireMockTests : IAsyncLifetime
{
    private WireMockServer _server = null!;
    private HttpClient _client = null!;

    public Task InitializeAsync()
    {
        _server = WireMockServer.Start();
        _client = new HttpClient
        {
            BaseAddress = new Uri(_server.Url!)
        };

        // Stub: GET /api/products returns a list
        _server
            .Given(Request.Create()
                .WithPath("/api/products")
                .UsingGet())
            .RespondWith(Response.Create()
                .WithStatusCode(200)
                .WithHeader("Content-Type", "application/json")
                .WithBodyAsJson(new[]
                {
                    new { Id = 1, Name = "Widget", Price = 19.99 },
                    new { Id = 2, Name = "Gadget", Price = 49.99 }
                }));

        // Stub: GET /api/products/1 returns a single product
        _server
            .Given(Request.Create()
                .WithPath("/api/products/1")
                .UsingGet())
            .RespondWith(Response.Create()
                .WithStatusCode(200)
                .WithBodyAsJson(new { Id = 1, Name = "Widget", Price = 19.99 }));

        // Stub: simulate a server error
        _server
            .Given(Request.Create()
                .WithPath("/api/products/error")
                .UsingGet())
            .RespondWith(Response.Create()
                .WithStatusCode(500)
                .WithBody("Internal Server Error"));

        return Task.CompletedTask;
    }

    [Fact]
    public async Task GetProducts_Returns_Products()
    {
        var products = await _client
            .GetFromJsonAsync<List<ProductDto>>("/api/products");

        Assert.NotNull(products);
        Assert.Equal(2, products.Count);
    }

    [Fact]
    public async Task ServerError_Is_Handled()
    {
        var response = await _client.GetAsync("/api/products/error");

        Assert.Equal(System.Net.HttpStatusCode.InternalServerError,
            response.StatusCode);
    }

    public Task DisposeAsync()
    {
        _client.Dispose();
        _server.Stop();
        return Task.CompletedTask;
    }
}
```

## Custom DelegatingHandler for HttpClient Mocking

Create a fake HTTP handler for testing HttpClient-based services without a server.

```csharp
using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using Xunit;

public class FakeHttpHandler : DelegatingHandler
{
    private readonly Dictionary<string, Func<HttpRequestMessage, HttpResponseMessage>>
        _responses = new();

    public FakeHttpHandler Respond(
        string pathAndMethod,
        Func<HttpRequestMessage, HttpResponseMessage> handler)
    {
        _responses[pathAndMethod] = handler;
        return this;
    }

    protected override Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request,
        CancellationToken cancellationToken)
    {
        string key = $"{request.Method} {request.RequestUri?.AbsolutePath}";

        if (_responses.TryGetValue(key, out var handler))
            return Task.FromResult(handler(request));

        return Task.FromResult(new HttpResponseMessage(HttpStatusCode.NotFound));
    }
}

public class HttpClientServiceTests
{
    [Fact]
    public async Task Service_Parses_Api_Response()
    {
        // Arrange
        var fakeHandler = new FakeHttpHandler()
            .Respond("GET /api/weather", _ => new HttpResponseMessage
            {
                StatusCode = HttpStatusCode.OK,
                Content = JsonContent.Create(new
                {
                    City = "Seattle",
                    Temperature = 72,
                    Condition = "Sunny"
                })
            })
            .Respond("GET /api/weather/error", _ => new HttpResponseMessage
            {
                StatusCode = HttpStatusCode.ServiceUnavailable,
                Content = new StringContent("Service down")
            });

        var httpClient = new HttpClient(fakeHandler)
        {
            BaseAddress = new Uri("https://api.weather.example.com")
        };

        var service = new WeatherService(httpClient);

        // Act
        var weather = await service.GetWeatherAsync("Seattle");

        // Assert
        Assert.Equal("Seattle", weather.City);
        Assert.Equal(72, weather.Temperature);
    }
}
```

## JSON File-Based Data Store

Serve responses from JSON files for more complex test scenarios.

```csharp
using System.Text.Json;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;

public class JsonFileApiFactory : WebApplicationFactory<JsonFileApiFactory>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.Configure(app =>
        {
            app.UseRouting();
            app.UseEndpoints(endpoints =>
            {
                endpoints.MapGet("/api/{resource}", async (string resource) =>
                {
                    string filePath = Path.Combine(
                        "TestData", $"{resource}.json");

                    if (!File.Exists(filePath))
                        return Results.NotFound();

                    string json = await File.ReadAllTextAsync(filePath);
                    var data = JsonSerializer.Deserialize<JsonElement>(json);
                    return Results.Ok(data);
                });

                endpoints.MapGet("/api/{resource}/{id:int}",
                    async (string resource, int id) =>
                {
                    string filePath = Path.Combine(
                        "TestData", $"{resource}.json");

                    if (!File.Exists(filePath))
                        return Results.NotFound();

                    string json = await File.ReadAllTextAsync(filePath);
                    var items = JsonSerializer
                        .Deserialize<JsonElement[]>(json);

                    var item = items?.FirstOrDefault(i =>
                        i.GetProperty("id").GetInt32() == id);

                    return item.HasValue
                        ? Results.Ok(item.Value)
                        : Results.NotFound();
                });
            });
        });
    }
}
```

## Simulating Delays and Failures

Test retry logic and timeout handling with configurable response delays.

```csharp
using WireMock.Server;
using WireMock.RequestBuilders;
using WireMock.ResponseBuilders;
using Xunit;

public class ResilienceTests : IAsyncLifetime
{
    private WireMockServer _server = null!;

    public Task InitializeAsync()
    {
        _server = WireMockServer.Start();

        // Simulate a slow response (3 second delay)
        _server
            .Given(Request.Create()
                .WithPath("/api/slow")
                .UsingGet())
            .RespondWith(Response.Create()
                .WithStatusCode(200)
                .WithBody("{\"status\":\"ok\"}")
                .WithDelay(TimeSpan.FromSeconds(3)));

        // Simulate intermittent failures (fault injection)
        _server
            .Given(Request.Create()
                .WithPath("/api/flaky")
                .UsingGet())
            .InScenario("Flaky")
            .WillSetStateTo("FirstCall")
            .RespondWith(Response.Create()
                .WithStatusCode(503));

        _server
            .Given(Request.Create()
                .WithPath("/api/flaky")
                .UsingGet())
            .InScenario("Flaky")
            .WhenStateIs("FirstCall")
            .WillSetStateTo("SecondCall")
            .RespondWith(Response.Create()
                .WithStatusCode(200)
                .WithBody("{\"status\":\"ok\"}"));

        return Task.CompletedTask;
    }

    [Fact]
    public async Task Client_Times_Out_On_Slow_Response()
    {
        var client = new HttpClient
        {
            BaseAddress = new Uri(_server.Url!),
            Timeout = TimeSpan.FromSeconds(1)
        };

        await Assert.ThrowsAsync<TaskCanceledException>(
            () => client.GetAsync("/api/slow"));
    }

    public Task DisposeAsync()
    {
        _server.Stop();
        return Task.CompletedTask;
    }
}
```

## Approach Comparison

| Feature | WebApplicationFactory | WireMock.Net | DelegatingHandler |
|---------|---------------------|-------------|-------------------|
| Server required | In-process | Localhost port | None |
| Request matching | ASP.NET routing | Flexible matchers | Manual |
| Delay simulation | Manual middleware | Built-in | Manual |
| Scenario support | Manual state | Built-in state machine | Manual |
| Setup complexity | Medium | Low | Low |
| Best for | Full API fakes | Third-party API mocks | Unit testing HttpClient |

## Best Practices

1. **Choose the right approach for your test level**: use `DelegatingHandler` for unit tests, WireMock.Net for integration tests against third-party APIs, and `WebApplicationFactory` for full API simulation.
2. **Define fake responses in separate JSON files for complex payloads**: keep test data in `TestData/*.json` files rather than inline string literals to improve readability and allow reuse.
3. **Test error responses and edge cases, not just happy paths**: configure fakes to return 400, 404, 500, and timeout responses to verify your error handling and retry logic.
4. **Use WireMock.Net scenarios for stateful API simulation**: model multi-step workflows (create, then retrieve) with WireMock's scenario state machine instead of static stubs.
5. **Dispose fake servers and HTTP clients in test teardown**: implement `IAsyncLifetime` or `IDisposable` to stop WireMock servers and dispose HttpClient instances after each test class.
6. **Verify request content in addition to response handling**: use WireMock's `_server.LogEntries` or handler assertions to confirm your code sends correct request bodies, headers, and query parameters.
7. **Isolate each test class with its own fake server port**: avoid port conflicts by letting WireMock auto-assign ports with `WireMockServer.Start()` instead of specifying fixed ports.
8. **Simulate realistic latency in integration tests**: add small delays (50-200ms) to fake responses to catch race conditions and timeout bugs that only appear with real network latency.
9. **Use `HttpClientFactory` patterns in production code for testability**: register named or typed HTTP clients so tests can replace the handler without changing business logic.
10. **Do not use fake servers as a substitute for contract tests**: fake servers validate your code's behavior against assumed responses; use Pact to validate that the real API actually matches those assumptions.
