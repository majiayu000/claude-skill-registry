---
name: arch-test
description: Generate architecture tests to enforce structural rules
argument-hint: "[--rules=layers|naming|dependencies]"
tags: [testing, architecture, netarchtest, quality]
user-invocable: true
---

# Architecture Tests

Generate tests that enforce architectural rules and prevent drift.

## For .NET (NetArchTest)
```bash
dotnet add package NetArchTest.Rules
```
```csharp
[Fact]
public void Controllers_ShouldNotReference_Repositories()
{
    Types.InAssembly(typeof(Program).Assembly)
        .That().ResideInNamespace("Controllers")
        .ShouldNot().HaveDependencyOn("Repositories")
        .GetResult().IsSuccessful.Should().BeTrue();
}

[Fact]
public void Services_ShouldHave_InterfacePrefix()
{
    Types.InAssembly(typeof(Program).Assembly)
        .That().ResideInNamespace("Services.Interfaces")
        .Should().HaveNameStartingWith("I")
        .GetResult().IsSuccessful.Should().BeTrue();
}
```

## Arguments
- `--rules=<layers|naming|dependencies>`: Which rules to generate