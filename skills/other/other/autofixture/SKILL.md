---
name: autofixture
description: >
  Guidance for AutoFixture test data generation library.
  USE FOR: auto-generating test data for unit tests, reducing boilerplate in the Arrange phase,
  creating anonymous objects and collections, customizing test data generation rules,
  integrating with Moq (AutoMoq) and xUnit for fully automated test setup.
  DO NOT USE FOR: integration test data seeding, production data generation, load testing data,
  or replacing dedicated faker libraries when realistic domain data is required.
license: MIT
metadata:
  displayName: "AutoFixture"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "AutoFixture Official Documentation"
    url: "https://autofixture.github.io/"
  - title: "AutoFixture GitHub Repository"
    url: "https://github.com/AutoFixture/AutoFixture"
  - title: "AutoFixture NuGet Package"
    url: "https://www.nuget.org/packages/AutoFixture"
---

# AutoFixture

## Overview

AutoFixture is a .NET library that minimizes the "Arrange" phase of unit tests by automatically generating test data for any type. It creates anonymous instances of classes, structs, primitives, collections, and complex object graphs with valid but unpredictable values. AutoFixture integrates with xUnit, NUnit, MSTest, and Moq (via AutoMoqCustomization) to provide fully auto-wired test fixtures. The core philosophy is that tests should only specify the data that is relevant to the behavior being tested, letting AutoFixture fill in everything else.

## Basic Object Creation

Use `Fixture` to create anonymous instances of any type.

```csharp
using AutoFixture;
using Xunit;

public class BasicCreationTests
{
    private readonly Fixture _fixture = new();

    [Fact]
    public void Create_Primitives()
    {
        int number = _fixture.Create<int>();
        string text = _fixture.Create<string>();
        DateTime date = _fixture.Create<DateTime>();
        Guid id = _fixture.Create<Guid>();

        Assert.NotEqual(0, number);
        Assert.NotEmpty(text);
    }

    [Fact]
    public void Create_Complex_Objects()
    {
        var user = _fixture.Create<User>();

        Assert.NotNull(user.Email);
        Assert.NotNull(user.DisplayName);
        Assert.NotEqual(0, user.Id);
    }

    [Fact]
    public void Create_Collections()
    {
        IEnumerable<User> users = _fixture.CreateMany<User>();      // 3 by default
        List<Order> orders = _fixture.CreateMany<Order>(10).ToList(); // explicit count

        Assert.Equal(3, users.Count());
        Assert.Equal(10, orders.Count);
    }
}
```

## Customizing Object Generation

Override specific properties while letting AutoFixture handle the rest.

```csharp
using AutoFixture;
using Xunit;

public class CustomizationTests
{
    private readonly Fixture _fixture = new();

    [Fact]
    public void Customize_Specific_Properties()
    {
        _fixture.Customize<User>(composer => composer
            .With(u => u.Age, 25)
            .With(u => u.Email, "test@example.com")
            .Without(u => u.Id));  // leave Id as default(int)

        var user = _fixture.Create<User>();

        Assert.Equal(25, user.Age);
        Assert.Equal("test@example.com", user.Email);
        Assert.Equal(0, user.Id);
    }

    [Fact]
    public void Register_Factory_For_Type()
    {
        _fixture.Register<DateTimeOffset>(
            () => new DateTimeOffset(2025, 6, 15, 0, 0, 0, TimeSpan.Zero));

        var order = _fixture.Create<Order>();

        Assert.Equal(2025, order.CreatedAt.Year);
    }

    [Fact]
    public void Build_Single_Object_With_Overrides()
    {
        var user = _fixture.Build<User>()
            .With(u => u.DisplayName, "Alice")
            .With(u => u.IsActive, true)
            .Without(u => u.PasswordHash)
            .Create();

        Assert.Equal("Alice", user.DisplayName);
        Assert.True(user.IsActive);
        Assert.Null(user.PasswordHash);
    }
}
```

## AutoMoq Integration

Automatically create mocks for constructor dependencies using AutoMoqCustomization.

```csharp
using AutoFixture;
using AutoFixture.AutoMoq;
using Moq;
using Xunit;

public class AutoMoqTests
{
    private readonly IFixture _fixture;

    public AutoMoqTests()
    {
        _fixture = new Fixture().Customize(new AutoMoqCustomization
        {
            ConfigureMembers = true,
            GenerateDelegates = true
        });
    }

    [Fact]
    public async Task Service_Returns_User_From_Repository()
    {
        // Arrange: AutoFixture creates the mock and the expected user
        var expectedUser = _fixture.Create<User>();
        var mockRepo = _fixture.Freeze<Mock<IUserRepository>>();

        mockRepo
            .Setup(r => r.GetByIdAsync(expectedUser.Id))
            .ReturnsAsync(expectedUser);

        // AutoFixture creates UserService with the frozen mock injected
        var service = _fixture.Create<UserService>();

        // Act
        var result = await service.GetUserAsync(expectedUser.Id);

        // Assert
        Assert.Equal(expectedUser.DisplayName, result?.DisplayName);
        mockRepo.Verify(r => r.GetByIdAsync(expectedUser.Id), Times.Once);
    }

    [Fact]
    public void Freeze_Returns_Same_Instance()
    {
        // Freeze locks a type to a single instance
        var frozenUser = _fixture.Freeze<User>();
        var service = _fixture.Create<UserService>();

        // Every User created by the fixture is the same frozen instance
        var anotherUser = _fixture.Create<User>();
        Assert.Same(frozenUser, anotherUser);
    }
}
```

## xUnit Integration with AutoData

Use `[AutoData]` and `[InlineAutoData]` to inject generated parameters into test methods.

```csharp
using AutoFixture;
using AutoFixture.Xunit2;
using Xunit;

public class AutoDataTests
{
    [Theory, AutoData]
    public void User_FullName_Combines_First_And_Last(
        string firstName, string lastName)
    {
        var user = new User
        {
            FirstName = firstName,
            LastName = lastName
        };

        string fullName = user.GetFullName();

        Assert.Contains(firstName, fullName);
        Assert.Contains(lastName, fullName);
    }

    [Theory]
    [InlineAutoData("Admin")]
    [InlineAutoData("Editor")]
    public void User_Has_Correct_Role(
        string role, string displayName, string email)
    {
        // role comes from InlineData, the rest from AutoFixture
        var user = new User
        {
            Role = role,
            DisplayName = displayName,
            Email = email
        };

        Assert.Equal(role, user.Role);
        Assert.NotEmpty(displayName);
    }
}

// Custom AutoData with AutoMoq
public class AutoMoqDataAttribute : AutoDataAttribute
{
    public AutoMoqDataAttribute()
        : base(() => new Fixture().Customize(new AutoMoqCustomization()))
    { }
}

[Theory, AutoMoqData]
public async Task GetUser_Returns_NotNull(
    [Frozen] Mock<IUserRepository> mockRepo,
    UserService sut,
    User expectedUser)
{
    mockRepo.Setup(r => r.GetByIdAsync(expectedUser.Id))
        .ReturnsAsync(expectedUser);

    var result = await sut.GetUserAsync(expectedUser.Id);

    Assert.NotNull(result);
}
```

## Custom Specimen Builders

Create reusable generation rules for domain-specific types.

```csharp
using AutoFixture;
using AutoFixture.Kernel;

public class EmailSpecimenBuilder : ISpecimenBuilder
{
    public object Create(object request, ISpecimenContext context)
    {
        if (request is System.Reflection.PropertyInfo pi
            && pi.Name.Contains("Email", StringComparison.OrdinalIgnoreCase)
            && pi.PropertyType == typeof(string))
        {
            var name = context.Resolve(typeof(string)) as string ?? "user";
            return $"{name.ToLower().Replace(" ", "")}@example.com";
        }

        return new NoSpecimen();
    }
}

public class DomainCustomization : ICustomization
{
    public void Customize(IFixture fixture)
    {
        fixture.Customizations.Add(new EmailSpecimenBuilder());
        fixture.Customize<Money>(c => c
            .With(m => m.Currency, "USD")
            .With(m => m.Amount,
                fixture.Create<decimal>() % 10000));
    }
}

// Usage
var fixture = new Fixture().Customize(new DomainCustomization());
var user = fixture.Create<User>();
// user.Email looks like "abc123@example.com"
```

## AutoFixture Feature Comparison

| Feature | AutoFixture | Bogus | Manual Setup |
|---------|-----------|-------|-------------|
| Anonymous data | Automatic | Rule-based | Manual |
| Mock integration | AutoMoq/AutoNSub | None | Manual |
| xUnit integration | [AutoData] | None | None |
| Domain realism | Low | High | Full control |
| Setup effort | Minimal | Medium | High |
| Best for | Unit tests | Realistic fakes | Specific scenarios |

## Best Practices

1. **Use `Freeze<T>()` to share a single instance across the test**: freeze the type that your system-under-test depends on so the same instance is injected both into the SUT and available for assertions.
2. **Specify only test-relevant data with `Build<T>().With()`**: let AutoFixture generate all other properties; tests that over-specify data become brittle and hard to read.
3. **Combine AutoFixture with AutoMoq for zero-setup unit tests**: `AutoMoqCustomization` auto-creates mocks for all interface dependencies, eliminating manual mock construction.
4. **Create custom `ISpecimenBuilder` implementations for domain rules**: email formats, phone numbers, and currency constraints should be defined once in a builder and reused across all test projects.
5. **Use `[AutoData]` and `[InlineAutoData]` for xUnit theories**: this eliminates the need for `new Fixture()` in every test method and makes test parameters self-documenting.
6. **Avoid calling `Create<T>()` for the system-under-test in AutoMoq tests**: let `_fixture.Create<MyService>()` build the SUT so all constructor dependencies are automatically resolved from frozen mocks.
7. **Compose customizations into a single `CompositeCustomization`**: bundle related customizations (AutoMoq + domain rules + date overrides) into one reusable class for consistent fixtures across the test project.
8. **Limit collection sizes with `RepeatCount`**: set `fixture.RepeatCount = 5` or use `CreateMany<T>(count)` to control generated collection sizes and keep tests fast.
9. **Use `fixture.Register<T>()` for types with no public constructor**: register a factory delegate for abstract types, sealed types with private constructors, or types that need specific initialization.
10. **Never use AutoFixture-generated data for integration or contract tests**: auto-generated values are anonymous and unpredictable; integration tests should use explicit, deterministic test data.
