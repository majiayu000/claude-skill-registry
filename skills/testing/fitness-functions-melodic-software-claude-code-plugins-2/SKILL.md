---
name: fitness-functions
description: Architecture test guidance for .NET using NetArchTest and ArchUnitNET. Use when enforcing architectural boundaries, testing module dependencies, validating layer constraints, or creating performance fitness functions. Includes code generation templates.
allowed-tools: Read, Write, Glob, Grep, Bash, Skill
---

# Fitness Functions

## When to Use This Skill

Use this skill when you need to:

- Enforce architectural boundaries between modules
- Test that dependencies follow prescribed rules
- Validate layer constraints (e.g., no UI → Domain)
- Create performance fitness functions
- Generate architecture test code
- Audit existing architecture for violations

**Keywords:** fitness functions, architecture tests, NetArchTest, ArchUnitNET, dependency rules, layer constraints, architectural boundaries, module isolation, architecture validation, performance tests

## What Are Fitness Functions?

Fitness functions are automated tests that validate architectural characteristics. They provide objective, repeatable verification that the system maintains desired properties as it evolves.

### Types of Fitness Functions

| Type | Validates | Example |
| --- | --- | --- |
| **Dependency** | Component relationships | "Domain cannot depend on Infrastructure" |
| **Layer** | Vertical slice rules | "Controllers only call Application layer" |
| **Naming** | Convention compliance | "Handlers must end with 'Handler'" |
| **Performance** | Runtime characteristics | "API response < 200ms at p95" |
| **Cyclomatic** | Code complexity | "No method > 10 cyclomatic complexity" |

## Quick Start

### 1. Install Required Package

```bash
# For NetArchTest (simpler, recommended for most cases)
dotnet add package NetArchTest.Rules

# For ArchUnitNET (more powerful, Java-like syntax)
dotnet add package ArchUnitNET
dotnet add package ArchUnitNET.xUnit  # or .NUnit
```

### 2. Create Test Project

```bash
dotnet new xunit -n YourSolution.ArchitectureTests
dotnet add YourSolution.ArchitectureTests reference src/YourSolution.Domain
dotnet add YourSolution.ArchitectureTests reference src/YourSolution.Application
dotnet add YourSolution.ArchitectureTests reference src/YourSolution.Infrastructure
```

### 3. Write First Test

```csharp
public class DependencyTests
{
    [Fact]
    public void Domain_ShouldNotDependOn_Infrastructure()
    {
        var result = Types.InAssembly(typeof(Order).Assembly)
            .ShouldNot()
            .HaveDependencyOn("YourSolution.Infrastructure")
            .GetResult();

        Assert.True(result.IsSuccessful, result.FailingTypeNames?.FirstOrDefault());
    }
}
```

## NetArchTest Patterns

NetArchTest provides a fluent API for testing architectural constraints.

**Detailed patterns:** See `references/netarchtest-patterns.md`

### Common Rules

```csharp
// Dependency constraints
Types.InAssembly(domainAssembly)
    .ShouldNot()
    .HaveDependencyOn("Microsoft.EntityFrameworkCore");

// Naming conventions
Types.InAssembly(applicationAssembly)
    .That()
    .ImplementInterface(typeof(IRequestHandler<,>))
    .Should()
    .HaveNameEndingWith("Handler");

// Layer isolation
Types.InNamespace("Domain")
    .ShouldNot()
    .HaveDependencyOnAny("Application", "Infrastructure", "Api");
```

## ArchUnitNET Patterns

ArchUnitNET offers more expressive rules with a syntax similar to ArchUnit for Java.

**Detailed patterns:** See `references/archunitnet-patterns.md`

### Common Rules

```csharp
// Define architecture layers
private static readonly Architecture Architecture =
    new ArchLoader().LoadAssemblies(
        typeof(Order).Assembly,
        typeof(OrderHandler).Assembly,
        typeof(OrderRepository).Assembly
    ).Build();

private static readonly IObjectProvider<IType> DomainLayer =
    Types().That().ResideInNamespace("Domain").As("Domain Layer");

private static readonly IObjectProvider<IType> InfrastructureLayer =
    Types().That().ResideInNamespace("Infrastructure").As("Infrastructure Layer");

[Fact]
public void DomainLayer_ShouldNotDependOn_InfrastructureLayer()
{
    IArchRule rule = Types().That().Are(DomainLayer)
        .Should().NotDependOnAny(InfrastructureLayer);

    rule.Check(Architecture);
}
```

## Dependency Rules Catalog

Common dependency rules for modular monoliths:

**Full catalog:** See `references/dependency-rules.md`

### Module Isolation

```csharp
[Fact]
public void Modules_ShouldNotCrossReference_CoreProjects()
{
    var orderingCore = Types.InAssembly(typeof(Order).Assembly);
    var inventoryCore = Types.InAssembly(typeof(Product).Assembly);

    // Ordering.Core cannot reference Inventory.Core
    var result = orderingCore
        .ShouldNot()
        .HaveDependencyOn("Inventory.Core")
        .GetResult();

    Assert.True(result.IsSuccessful);
}
```

### Shared Kernel Constraints

```csharp
[Fact]
public void SharedKernel_ShouldNotDependOn_AnyModule()
{
    var sharedKernel = Types.InAssembly(typeof(Entity).Assembly);

    var result = sharedKernel
        .ShouldNot()
        .HaveDependencyOnAny(
            "Ordering", "Inventory", "Shipping", "Customers")
        .GetResult();

    Assert.True(result.IsSuccessful);
}
```

## Performance Fitness Functions

Test runtime characteristics to ensure performance standards.

**Detailed guide:** See `references/performance-fitness.md`

### Response Time Test

```csharp
[Fact]
public async Task Api_ShouldRespondWithin_200ms()
{
    var client = _factory.CreateClient();
    var stopwatch = Stopwatch.StartNew();

    var response = await client.GetAsync("/api/orders/123");

    stopwatch.Stop();
    Assert.True(stopwatch.ElapsedMilliseconds < 200,
        $"Response took {stopwatch.ElapsedMilliseconds}ms");
}
```

### Memory Allocation Test

```csharp
[Fact]
public void Handler_ShouldNotAllocateExcessiveMemory()
{
    var before = GC.GetTotalMemory(true);

    for (int i = 0; i < 1000; i++)
    {
        _handler.Handle(new GetOrderQuery(Guid.NewGuid()));
    }

    var after = GC.GetTotalMemory(true);
    var allocated = (after - before) / 1000;  // Per operation

    Assert.True(allocated < 10_000, $"Allocated {allocated} bytes per operation");
}
```

## Code Generation Templates

Use these templates to quickly create architecture tests:

- `references/templates/architecture-test-template.cs` - Full test class scaffold
- `references/templates/performance-test-template.cs` - Performance test patterns

### Quick Template Usage

```bash
# Copy template and customize
cp templates/architecture-test-template.cs tests/ArchitectureTests.cs
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
- name: Run Architecture Tests
  run: dotnet test --filter Category=Architecture
  continue-on-error: false  # Fail pipeline on violations
```

### Test Categories

```csharp
[Trait("Category", "Architecture")]
public class DependencyTests
{
    // Architecture tests run separately from unit tests
}
```

## Integration with Event Storming

Fitness functions enforce the boundaries discovered through event storming:

```text
Event Storming → Bounded Contexts
    ↓
Modular Architecture → Module Structure
    ↓
Fitness Functions → Enforce Boundaries
```

After event storming identifies bounded contexts:

1. Define modules based on contexts
2. Create dependency rules between modules
3. Add fitness functions to enforce isolation

## Best Practices

1. **Run in CI/CD** - Catch violations before merge
2. **Start with critical rules** - Don't try to test everything at once
3. **Clear failure messages** - Make violations easy to understand
4. **Categorize tests** - Separate from unit/integration tests
5. **Document intent** - Explain why each rule exists
6. **Review regularly** - Update rules as architecture evolves

## Troubleshooting

### Common Issues

**Test finds no types:**

- Check assembly references in test project
- Verify namespace patterns match actual namespaces

**False positives:**

- Add exclusions for legitimate dependencies
- Check for indirect dependencies via shared packages

**Performance tests flaky:**

- Use warm-up runs before measuring
- Run in isolated environment
- Use statistical significance (multiple runs)

## References

- `references/netarchtest-patterns.md` - NetArchTest usage patterns
- `references/archunitnet-patterns.md` - ArchUnitNET usage patterns
- `references/performance-fitness.md` - Performance testing patterns
- `references/dependency-rules.md` - Common dependency rules catalog
- `references/templates/architecture-test-template.cs` - Test class template
- `references/templates/performance-test-template.cs` - Performance test template

## Version History

- **v1.0.0** (2025-12-22): Initial release
  - NetArchTest and ArchUnitNET patterns
  - Dependency rules catalog
  - Performance fitness functions
  - Code generation templates
  - CI/CD integration guidance

---

## Last Updated

**Date:** 2025-12-22
**Model:** claude-opus-4-5-20251101
