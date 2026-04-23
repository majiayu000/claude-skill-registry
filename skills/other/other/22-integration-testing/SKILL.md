---
name: integration-testing
description: "Configures integration tests with WebApplicationFactory and Testcontainers. Provides test database setup, authentication helpers, and utilities for testing API endpoints with real dependencies."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: Testcontainers.PostgreSql, Microsoft.AspNetCore.Mvc.Testing, Respawn
pattern: Integration Testing, Test Fixtures
---

# Integration Test Setup

## Overview

Integration tests verify the full request pipeline:

- **WebApplicationFactory** - In-memory test server
- **Testcontainers** - Real PostgreSQL in Docker
- **Respawn** - Fast database cleanup between tests
- **Authentication helpers** - Test with different users/roles

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `IntegrationTestWebAppFactory` | Custom test server factory |
| `BaseIntegrationTest` | Base class for all tests |
| `Respawner` | Database cleanup utility |
| `TestAuthHandler` | Fake authentication handler |

---

## Test Project Structure

```
tests/
└── {name}.Api.IntegrationTests/
    ├── Infrastructure/
    │   ├── IntegrationTestWebAppFactory.cs
    │   ├── BaseIntegrationTest.cs
    │   ├── TestAuthHandler.cs
    │   └── FakeUserContext.cs
    ├── {Feature}/
    │   ├── Create{Entity}Tests.cs
    │   └── Get{Entity}Tests.cs
    └── {name}.Api.IntegrationTests.csproj
```

---

## Template: Test Project File

```xml
<!-- tests/{name}.Api.IntegrationTests/{name}.Api.IntegrationTests.csproj -->
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="FluentAssertions" Version="6.12.0" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="8.0.0" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="Respawn" Version="6.1.0" />
    <PackageReference Include="Testcontainers.PostgreSql" Version="3.6.0" />
    <PackageReference Include="xunit" Version="2.6.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.4">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
    </PackageReference>
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\src\{name}.api\{name}.api.csproj" />
    <ProjectReference Include="..\..\src\{name}.infrastructure\{name}.infrastructure.csproj" />
  </ItemGroup>

</Project>
```

---

## Template: WebApplicationFactory

```csharp
// tests/{name}.Api.IntegrationTests/Infrastructure/IntegrationTestWebAppFactory.cs
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Testcontainers.PostgreSql;
using {name}.infrastructure;

namespace {name}.Api.IntegrationTests.Infrastructure;

public class IntegrationTestWebAppFactory 
    : WebApplicationFactory<Program>, IAsyncLifetime
{
    private readonly PostgreSqlContainer _dbContainer = new PostgreSqlBuilder()
        .WithImage("postgres:15-alpine")
        .WithDatabase("testdb")
        .WithUsername("postgres")
        .WithPassword("postgres")
        .Build();

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureTestServices(services =>
        {
            // ═══════════════════════════════════════════════════════════════
            // REPLACE DATABASE WITH TEST CONTAINER
            // ═══════════════════════════════════════════════════════════════
            
            services.RemoveAll(typeof(DbContextOptions<ApplicationDbContext>));

            services.AddDbContext<ApplicationDbContext>(options =>
            {
                options.UseNpgsql(_dbContainer.GetConnectionString());
            });

            // ═══════════════════════════════════════════════════════════════
            // REPLACE AUTHENTICATION WITH TEST HANDLER
            // ═══════════════════════════════════════════════════════════════
            
            services.AddAuthentication(options =>
            {
                options.DefaultAuthenticateScheme = TestAuthHandler.SchemeName;
                options.DefaultChallengeScheme = TestAuthHandler.SchemeName;
            })
            .AddScheme<TestAuthSchemeOptions, TestAuthHandler>(
                TestAuthHandler.SchemeName,
                options => { });

            // ═══════════════════════════════════════════════════════════════
            // REPLACE EXTERNAL SERVICES WITH FAKES
            // ═══════════════════════════════════════════════════════════════
            
            // services.RemoveAll<IEmailService>();
            // services.AddSingleton<IEmailService, FakeEmailService>();
        });

        builder.UseEnvironment("Testing");
    }

    public async Task InitializeAsync()
    {
        await _dbContainer.StartAsync();
        
        // Apply migrations
        using var scope = Services.CreateScope();
        var dbContext = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
        await dbContext.Database.MigrateAsync();
    }

    public new async Task DisposeAsync()
    {
        await _dbContainer.StopAsync();
    }
}
```

---

## Template: Test Authentication Handler

```csharp
// tests/{name}.Api.IntegrationTests/Infrastructure/TestAuthHandler.cs
using System.Security.Claims;
using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace {name}.Api.IntegrationTests.Infrastructure;

public class TestAuthSchemeOptions : AuthenticationSchemeOptions
{
    public Guid? UserId { get; set; }
    public string? Email { get; set; }
    public string[]? Roles { get; set; }
    public string[]? Permissions { get; set; }
}

public class TestAuthHandler : AuthenticationHandler<TestAuthSchemeOptions>
{
    public const string SchemeName = "TestScheme";
    public const string TestUserIdHeader = "X-Test-User-Id";
    public const string TestUserEmailHeader = "X-Test-User-Email";
    public const string TestUserRolesHeader = "X-Test-User-Roles";
    public const string TestUserPermissionsHeader = "X-Test-User-Permissions";

    public TestAuthHandler(
        IOptionsMonitor<TestAuthSchemeOptions> options,
        ILoggerFactory logger,
        UrlEncoder encoder)
        : base(options, logger, encoder)
    {
    }

    protected override Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        // Check for test headers
        if (!Request.Headers.TryGetValue(TestUserIdHeader, out var userIdHeader))
        {
            return Task.FromResult(AuthenticateResult.NoResult());
        }

        if (!Guid.TryParse(userIdHeader, out var userId))
        {
            return Task.FromResult(AuthenticateResult.Fail("Invalid user ID"));
        }

        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, userId.ToString()),
            new("sub", userId.ToString())
        };

        // Add email
        if (Request.Headers.TryGetValue(TestUserEmailHeader, out var emailHeader))
        {
            claims.Add(new Claim(ClaimTypes.Email, emailHeader.ToString()));
            claims.Add(new Claim("email", emailHeader.ToString()));
        }

        // Add roles
        if (Request.Headers.TryGetValue(TestUserRolesHeader, out var rolesHeader))
        {
            foreach (var role in rolesHeader.ToString().Split(','))
            {
                claims.Add(new Claim(ClaimTypes.Role, role.Trim()));
            }
        }

        // Add permissions
        if (Request.Headers.TryGetValue(TestUserPermissionsHeader, out var permissionsHeader))
        {
            foreach (var permission in permissionsHeader.ToString().Split(','))
            {
                claims.Add(new Claim("permission", permission.Trim()));
            }
        }

        var identity = new ClaimsIdentity(claims, SchemeName);
        var principal = new ClaimsPrincipal(identity);
        var ticket = new AuthenticationTicket(principal, SchemeName);

        return Task.FromResult(AuthenticateResult.Success(ticket));
    }
}
```

---

## Template: Base Integration Test

```csharp
// tests/{name}.Api.IntegrationTests/Infrastructure/BaseIntegrationTest.cs
using System.Net.Http.Headers;
using System.Net.Http.Json;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Npgsql;
using Respawn;
using {name}.infrastructure;

namespace {name}.Api.IntegrationTests.Infrastructure;

[Collection("Integration")]
public abstract class BaseIntegrationTest : IAsyncLifetime
{
    protected readonly IntegrationTestWebAppFactory Factory;
    protected readonly HttpClient Client;
    protected readonly IServiceScope Scope;
    protected readonly ApplicationDbContext DbContext;

    private static Respawner? _respawner;
    private static string? _connectionString;

    protected BaseIntegrationTest(IntegrationTestWebAppFactory factory)
    {
        Factory = factory;
        Client = factory.CreateClient();
        Scope = factory.Services.CreateScope();
        DbContext = Scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    }

    // ═══════════════════════════════════════════════════════════════
    // AUTHENTICATION HELPERS
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Configure client to authenticate as a specific user
    /// </summary>
    protected void AuthenticateAs(
        Guid userId,
        string email = "test@example.com",
        string[]? roles = null,
        string[]? permissions = null)
    {
        Client.DefaultRequestHeaders.Add(TestAuthHandler.TestUserIdHeader, userId.ToString());
        Client.DefaultRequestHeaders.Add(TestAuthHandler.TestUserEmailHeader, email);

        if (roles?.Length > 0)
        {
            Client.DefaultRequestHeaders.Add(
                TestAuthHandler.TestUserRolesHeader,
                string.Join(",", roles));
        }

        if (permissions?.Length > 0)
        {
            Client.DefaultRequestHeaders.Add(
                TestAuthHandler.TestUserPermissionsHeader,
                string.Join(",", permissions));
        }
    }

    /// <summary>
    /// Configure client to authenticate as admin
    /// </summary>
    protected void AuthenticateAsAdmin()
    {
        AuthenticateAs(
            userId: Guid.NewGuid(),
            email: "admin@example.com",
            roles: new[] { "Admin" },
            permissions: new[] { "users:read", "users:write", "users:delete" });
    }

    /// <summary>
    /// Remove authentication headers
    /// </summary>
    protected void RemoveAuthentication()
    {
        Client.DefaultRequestHeaders.Remove(TestAuthHandler.TestUserIdHeader);
        Client.DefaultRequestHeaders.Remove(TestAuthHandler.TestUserEmailHeader);
        Client.DefaultRequestHeaders.Remove(TestAuthHandler.TestUserRolesHeader);
        Client.DefaultRequestHeaders.Remove(TestAuthHandler.TestUserPermissionsHeader);
    }

    // ═══════════════════════════════════════════════════════════════
    // HTTP HELPERS
    // ═══════════════════════════════════════════════════════════════

    protected async Task<HttpResponseMessage> GetAsync(string url)
    {
        return await Client.GetAsync(url);
    }

    protected async Task<T?> GetAsync<T>(string url)
    {
        var response = await Client.GetAsync(url);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<T>();
    }

    protected async Task<HttpResponseMessage> PostAsync<T>(string url, T content)
    {
        return await Client.PostAsJsonAsync(url, content);
    }

    protected async Task<TResponse?> PostAsync<TRequest, TResponse>(string url, TRequest content)
    {
        var response = await Client.PostAsJsonAsync(url, content);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<TResponse>();
    }

    protected async Task<HttpResponseMessage> PutAsync<T>(string url, T content)
    {
        return await Client.PutAsJsonAsync(url, content);
    }

    protected async Task<HttpResponseMessage> DeleteAsync(string url)
    {
        return await Client.DeleteAsync(url);
    }

    // ═══════════════════════════════════════════════════════════════
    // DATABASE HELPERS
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Add entity directly to database for test setup
    /// </summary>
    protected async Task AddAsync<TEntity>(TEntity entity) where TEntity : class
    {
        DbContext.Set<TEntity>().Add(entity);
        await DbContext.SaveChangesAsync();
    }

    /// <summary>
    /// Get entity from database
    /// </summary>
    protected async Task<TEntity?> FindAsync<TEntity>(Guid id) where TEntity : class
    {
        return await DbContext.Set<TEntity>().FindAsync(id);
    }

    /// <summary>
    /// Execute raw SQL for test setup
    /// </summary>
    protected async Task ExecuteSqlAsync(string sql, object? parameters = null)
    {
        await DbContext.Database.ExecuteSqlRawAsync(sql);
    }

    // ═══════════════════════════════════════════════════════════════
    // LIFECYCLE
    // ═══════════════════════════════════════════════════════════════

    public async Task InitializeAsync()
    {
        // Initialize Respawner once
        if (_respawner is null)
        {
            _connectionString = DbContext.Database.GetConnectionString();
            
            await using var connection = new NpgsqlConnection(_connectionString);
            await connection.OpenAsync();

            _respawner = await Respawner.CreateAsync(connection, new RespawnerOptions
            {
                DbAdapter = DbAdapter.Postgres,
                SchemasToInclude = new[] { "public" },
                TablesToIgnore = new Respawn.Graph.Table[] 
                { 
                    "__EFMigrationsHistory"  // Don't reset migrations table
                }
            });
        }

        // Reset database before each test
        await using var conn = new NpgsqlConnection(_connectionString);
        await conn.OpenAsync();
        await _respawner.ResetAsync(conn);
    }

    public Task DisposeAsync()
    {
        Scope.Dispose();
        return Task.CompletedTask;
    }
}

/// <summary>
/// Collection definition for integration tests
/// Ensures tests share the same WebApplicationFactory
/// </summary>
[CollectionDefinition("Integration")]
public class IntegrationTestCollection : ICollectionFixture<IntegrationTestWebAppFactory>
{
}
```

---

## Template: Integration Tests

```csharp
// tests/{name}.Api.IntegrationTests/{Feature}/Create{Entity}Tests.cs
using System.Net;
using System.Net.Http.Json;
using FluentAssertions;
using {name}.Api.IntegrationTests.Infrastructure;
using {name}.application.{feature}.Create{Entity};

namespace {name}.Api.IntegrationTests.{Feature};

public class Create{Entity}Tests : BaseIntegrationTest
{
    public Create{Entity}Tests(IntegrationTestWebAppFactory factory) 
        : base(factory)
    {
    }

    // ═══════════════════════════════════════════════════════════════
    // SUCCESS TESTS
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task Create_Should_ReturnCreated_When_ValidRequest()
    {
        // Arrange
        AuthenticateAsAdmin();

        var request = new Create{Entity}Request
        {
            Name = "Test Entity",
            Description = "Test Description",
            OrganizationId = Guid.NewGuid()
        };

        // Act
        var response = await PostAsync("/api/v1/{entities}", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);

        var entityId = await response.Content.ReadFromJsonAsync<Guid>();
        entityId.Should().NotBeEmpty();

        // Verify in database
        var entity = await FindAsync<Domain.{Aggregate}.{Entity}>(entityId);
        entity.Should().NotBeNull();
        entity!.Name.Should().Be(request.Name);
    }

    [Fact]
    public async Task Create_Should_ReturnLocationHeader_When_Created()
    {
        // Arrange
        AuthenticateAsAdmin();

        var request = new Create{Entity}Request
        {
            Name = "Test Entity",
            Description = "Test Description",
            OrganizationId = Guid.NewGuid()
        };

        // Act
        var response = await PostAsync("/api/v1/{entities}", request);

        // Assert
        response.Headers.Location.Should().NotBeNull();
        response.Headers.Location!.ToString().Should().Contain("/api/v1/{entities}/");
    }

    // ═══════════════════════════════════════════════════════════════
    // VALIDATION TESTS
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task Create_Should_ReturnBadRequest_When_NameIsEmpty()
    {
        // Arrange
        AuthenticateAsAdmin();

        var request = new Create{Entity}Request
        {
            Name = string.Empty,
            Description = "Test Description",
            OrganizationId = Guid.NewGuid()
        };

        // Act
        var response = await PostAsync("/api/v1/{entities}", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }

    [Fact]
    public async Task Create_Should_ReturnBadRequest_When_NameTooLong()
    {
        // Arrange
        AuthenticateAsAdmin();

        var request = new Create{Entity}Request
        {
            Name = new string('a', 101),  // Exceeds 100 char limit
            Description = "Test Description",
            OrganizationId = Guid.NewGuid()
        };

        // Act
        var response = await PostAsync("/api/v1/{entities}", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }

    // ═══════════════════════════════════════════════════════════════
    // AUTHENTICATION TESTS
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task Create_Should_ReturnUnauthorized_When_NotAuthenticated()
    {
        // Arrange
        RemoveAuthentication();

        var request = new Create{Entity}Request
        {
            Name = "Test Entity",
            Description = "Test Description",
            OrganizationId = Guid.NewGuid()
        };

        // Act
        var response = await PostAsync("/api/v1/{entities}", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }

    // ═══════════════════════════════════════════════════════════════
    // AUTHORIZATION TESTS
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task Create_Should_ReturnForbidden_When_NoWritePermission()
    {
        // Arrange
        AuthenticateAs(
            userId: Guid.NewGuid(),
            permissions: new[] { "entities:read" });  // Only read permission

        var request = new Create{Entity}Request
        {
            Name = "Test Entity",
            Description = "Test Description",
            OrganizationId = Guid.NewGuid()
        };

        // Act
        var response = await PostAsync("/api/v1/{entities}", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Forbidden);
    }

    // ═══════════════════════════════════════════════════════════════
    // CONFLICT TESTS
    // ═══════════════════════════════════════════════════════════════

    [Fact]
    public async Task Create_Should_ReturnConflict_When_NameAlreadyExists()
    {
        // Arrange
        AuthenticateAsAdmin();

        // Create first entity
        var firstRequest = new Create{Entity}Request
        {
            Name = "Duplicate Name",
            Description = "First entity",
            OrganizationId = Guid.NewGuid()
        };
        await PostAsync("/api/v1/{entities}", firstRequest);

        // Try to create second entity with same name
        var secondRequest = new Create{Entity}Request
        {
            Name = "Duplicate Name",  // Same name
            Description = "Second entity",
            OrganizationId = Guid.NewGuid()
        };

        // Act
        var response = await PostAsync("/api/v1/{entities}", secondRequest);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Conflict);
    }
}
```

---

## Template: Get Entity Tests

```csharp
// tests/{name}.Api.IntegrationTests/{Feature}/Get{Entity}Tests.cs
using System.Net;
using System.Net.Http.Json;
using FluentAssertions;
using {name}.Api.IntegrationTests.Infrastructure;
using {name}.application.{feature}.Get{Entity}ById;

namespace {name}.Api.IntegrationTests.{Feature};

public class Get{Entity}Tests : BaseIntegrationTest
{
    public Get{Entity}Tests(IntegrationTestWebAppFactory factory) 
        : base(factory)
    {
    }

    [Fact]
    public async Task GetById_Should_ReturnEntity_When_Exists()
    {
        // Arrange
        AuthenticateAsAdmin();

        var entityId = await CreateTestEntity();

        // Act
        var response = await GetAsync($"/api/v1/{entities}/{entityId}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<{Entity}Response>();
        result.Should().NotBeNull();
        result!.Id.Should().Be(entityId);
    }

    [Fact]
    public async Task GetById_Should_ReturnNotFound_When_NotExists()
    {
        // Arrange
        AuthenticateAsAdmin();
        var nonExistentId = Guid.NewGuid();

        // Act
        var response = await GetAsync($"/api/v1/{entities}/{nonExistentId}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task GetAll_Should_ReturnPaginatedList()
    {
        // Arrange
        AuthenticateAsAdmin();

        // Create multiple entities
        await CreateTestEntity("Entity 1");
        await CreateTestEntity("Entity 2");
        await CreateTestEntity("Entity 3");

        // Act
        var response = await GetAsync("/api/v1/{entities}?pageNumber=1&pageSize=10");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<PagedListResponse>();
        result.Should().NotBeNull();
        result!.Items.Should().HaveCount(3);
        result.TotalCount.Should().Be(3);
    }

    // ═══════════════════════════════════════════════════════════════
    // HELPER METHODS
    // ═══════════════════════════════════════════════════════════════

    private async Task<Guid> CreateTestEntity(string name = "Test Entity")
    {
        var request = new
        {
            Name = name,
            Description = "Test Description",
            OrganizationId = Guid.NewGuid()
        };

        var response = await PostAsync("/api/v1/{entities}", request);
        response.EnsureSuccessStatusCode();

        return await response.Content.ReadFromJsonAsync<Guid>();
    }
}

public class PagedListResponse
{
    public List<{Entity}Response> Items { get; set; } = new();
    public int PageNumber { get; set; }
    public int PageSize { get; set; }
    public int TotalCount { get; set; }
}
```

---

## Template: Test Utilities

```csharp
// tests/{name}.Api.IntegrationTests/Infrastructure/TestDataSeeder.cs
using {name}.infrastructure;

namespace {name}.Api.IntegrationTests.Infrastructure;

public static class TestDataSeeder
{
    public static async Task SeedOrganizationAsync(
        ApplicationDbContext context,
        Guid organizationId,
        string name = "Test Organization")
    {
        var organization = new
        {
            Id = organizationId,
            Name = name,
            CreatedAtUtc = DateTime.UtcNow
        };

        await context.Database.ExecuteSqlRawAsync(
            @"INSERT INTO organizations (id, name, created_at_utc) 
              VALUES ({0}, {1}, {2})",
            organizationId,
            name,
            DateTime.UtcNow);
    }

    public static async Task SeedUserAsync(
        ApplicationDbContext context,
        Guid userId,
        string email,
        Guid organizationId)
    {
        await context.Database.ExecuteSqlRawAsync(
            @"INSERT INTO users (id, email, name, organization_id, is_active, created_at_utc) 
              VALUES ({0}, {1}, {2}, {3}, true, {4})",
            userId,
            email,
            "Test User",
            organizationId,
            DateTime.UtcNow);
    }
}
```

---

## Running Tests

```bash
# Run all integration tests
dotnet test tests/{name}.Api.IntegrationTests

# Run with verbose output
dotnet test tests/{name}.Api.IntegrationTests -v n

# Run specific test class
dotnet test tests/{name}.Api.IntegrationTests --filter "FullyQualifiedName~Create{Entity}Tests"

# Run with code coverage
dotnet test tests/{name}.Api.IntegrationTests --collect:"XPlat Code Coverage"
```

---

## Critical Rules

1. **Fresh database per test** - Use Respawn to reset
2. **Isolated tests** - No shared state between tests
3. **Real database** - Use Testcontainers, not in-memory
4. **Test through HTTP** - Use HttpClient, not direct calls
5. **Authentication helpers** - Easy user impersonation
6. **Meaningful assertions** - Verify both response and database
7. **Test all status codes** - 200, 400, 401, 403, 404, 409
8. **Parallel execution** - Design for concurrent tests
9. **Clean up after tests** - Respawn handles this
10. **CI/CD compatible** - Docker required for Testcontainers

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Sharing state between tests
private static Guid _sharedEntityId;  // Tests will interfere!

// ✅ CORRECT: Create data per test
[Fact]
public async Task Test1()
{
    var entityId = await CreateTestEntity();
}

// ❌ WRONG: Not resetting database
// Tests depend on order and previous test data

// ✅ CORRECT: Reset before each test (handled by BaseIntegrationTest)
public async Task InitializeAsync()
{
    await _respawner.ResetAsync(connection);
}

// ❌ WRONG: Using in-memory database
services.AddDbContext<AppDbContext>(o => o.UseInMemoryDatabase("test"));
// In-memory doesn't support all EF Core features

// ✅ CORRECT: Use real PostgreSQL with Testcontainers
private readonly PostgreSqlContainer _dbContainer = new PostgreSqlBuilder()
    .WithImage("postgres:15-alpine")
    .Build();
```

---

## Related Skills

- `unit-testing` - Unit tests for handlers
- `jwt-authentication` - Authentication to test
- `permission-authorization` - Authorization to test
- `api-controller-generator` - Endpoints to test
