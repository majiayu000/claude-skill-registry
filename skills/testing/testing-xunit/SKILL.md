---
name: testing-xunit
description: Use when writing unit tests, integration tests, or setting up test projects in C#. Covers xUnit patterns, Moq mocking, Bogus test data generation, and Alba integration testing.
---

# xUnit Testing

Apply these patterns when writing tests in .NET projects.

## Required Packages

```xml
<PackageReference Include="xunit" Version="2.*" />
<PackageReference Include="xunit.runner.visualstudio" Version="2.*" />
<PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.*" />
<PackageReference Include="Moq" Version="4.*" />
<PackageReference Include="Bogus" Version="35.*" />
<PackageReference Include="Alba" Version="8.*" />  <!-- Integration tests -->
```

## Project Structure

```
tests/
├── MyApp.UnitTests/
│   ├── GlobalUsings.cs
│   ├── Fakers/UserFaker.cs
│   └── Services/UserServiceTests.cs
└── MyApp.IntegrationTests/
    └── Endpoints/UserEndpointsTests.cs
```

GlobalUsings.cs:
```csharp
global using Xunit;
global using Moq;
global using Bogus;
```

## Test Naming

Pattern: `MethodName_Scenario_ExpectedResult`

```csharp
GetByIdAsync_WithValidId_ReturnsUser()
GetByIdAsync_WithInvalidId_ReturnsNull()
CreateAsync_WithDuplicateEmail_ThrowsValidationException()
```

## Test Structure

```csharp
[Fact]
public async Task GetByIdAsync_WithValidId_ReturnsUser()
{
    // Arrange
    var expectedUser = new UserFaker().Generate();
    _mockRepo.Setup(r => r.GetByIdAsync(expectedUser.Id)).ReturnsAsync(expectedUser);

    // Act
    var result = await _sut.GetByIdAsync(expectedUser.Id);

    // Assert
    Assert.NotNull(result);
    Assert.Equal(expectedUser.Name, result.Name);
}
```

## Test Data with Bogus

```csharp
public sealed class UserFaker : Faker<User>
{
    public UserFaker()
    {
        RuleFor(u => u.Id, f => f.IndexFaker + 1);
        RuleFor(u => u.Email, f => f.Internet.Email());
        RuleFor(u => u.FirstName, f => f.Name.FirstName());
        RuleFor(u => u.IsActive, true);
    }

    public UserFaker AsInactive()
    {
        RuleFor(u => u.IsActive, false);
        return this;
    }
}

var user = new UserFaker().Generate();
var users = new UserFaker().Generate(10);
var inactiveUser = new UserFaker().AsInactive().Generate();
```

## Mocking with Moq

```csharp
public class UserServiceTests
{
    private readonly Mock<IUserRepository> _mockRepo;
    private readonly UserService _sut;

    public UserServiceTests()
    {
        _mockRepo = new Mock<IUserRepository>();
        _sut = new UserService(_mockRepo.Object);
    }
}

// Setup
_mockRepo.Setup(r => r.GetByIdAsync(1)).ReturnsAsync(new User { Id = 1 });
_mockRepo.Setup(r => r.GetByIdAsync(It.IsAny<int>())).ReturnsAsync(new User());
_mockRepo.Setup(r => r.GetByIdAsync(-1)).ThrowsAsync(new ArgumentException());

// Verify
_mockRepo.Verify(r => r.GetByIdAsync(1), Times.Once);
_mockRepo.Verify(r => r.DeleteAsync(It.IsAny<int>()), Times.Never);
```

## Integration Testing with Alba

```csharp
public class UserEndpointsTests : IAsyncLifetime
{
    private IAlbaHost _host = null!;

    public async Task InitializeAsync()
    {
        _host = await AlbaHost.For<Program>(builder =>
        {
            builder.ConfigureServices(services =>
            {
                services.AddSingleton<IUserRepository, FakeUserRepository>();
            });
        });
    }

    public async Task DisposeAsync() => await _host.DisposeAsync();

    [Fact]
    public async Task GetUser_WithValidId_ReturnsOk()
    {
        await _host.Scenario(_ =>
        {
            _.Get.Url("/api/users/1");
            _.StatusCodeShouldBeOk();
        });
    }

    [Fact]
    public async Task CreateUser_WithValidData_ReturnsCreated()
    {
        var newUser = new UserFaker().Generate();
        var result = await _host.Scenario(_ =>
        {
            _.Post.Json(newUser).ToUrl("/api/users");
            _.StatusCodeShouldBe(HttpStatusCode.Created);
        });
        var created = await result.ReadAsJsonAsync<User>();
        Assert.Equal(newUser.Email, created.Email);
    }
}
```

### Shared Host with Collection Fixture

```csharp
public class AppFixture : IAsyncLifetime
{
    public IAlbaHost Host { get; private set; } = null!;
    public async Task InitializeAsync() => Host = await AlbaHost.For<Program>();
    public async Task DisposeAsync() => await Host.DisposeAsync();
}

[CollectionDefinition("App")]
public class AppCollection : ICollectionFixture<AppFixture> { }

[Collection("App")]
public class UserEndpointsTests
{
    private readonly IAlbaHost _host;
    public UserEndpointsTests(AppFixture fixture) => _host = fixture.Host;
}
```

## Test Attributes

```csharp
[Fact]  // Single test case

[Theory]  // Parameterized
[InlineData(2, 3, 5)]
[InlineData(0, 0, 0)]
public void Add_TwoNumbers_ReturnsSum(int a, int b, int expected)
{
    Assert.Equal(expected, Calculator.Add(a, b));
}

[Theory]
[MemberData(nameof(GetTestCases))]
public void Process_WithTestCases_ReturnsExpected(User input, bool expected) { }

[Trait("Category", "Unit")]  // Run with: dotnet test --filter "Category=Unit"
```

## Assertions

```csharp
Assert.Equal(expected, actual);
Assert.NotNull(obj);
Assert.True(condition);
Assert.Empty(collection);
Assert.Contains(item, collection);
Assert.Single(collection);

Assert.Throws<ArgumentException>(() => DoSomething());
await Assert.ThrowsAsync<InvalidOperationException>(() => DoSomethingAsync());

Assert.IsType<User>(result);
```

## Requirements

1. One assertion focus per test
2. Use `MethodName_Scenario_Expected` naming
3. Keep tests independent with no shared mutable state
4. Use Bogus for realistic test data
5. Mock external dependencies only
6. Test edge cases: null, empty, boundaries
7. Use Theory for data variations
8. Use Alba for integration tests

Do not test implementation details. Do not mock the system under test. Do not use `Thread.Sleep`. Do not share mutable test data.
