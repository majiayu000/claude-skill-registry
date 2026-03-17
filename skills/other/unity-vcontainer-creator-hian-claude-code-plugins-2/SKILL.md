---
name: unity-vcontainer
description: VContainer dependency injection expert specializing in IoC container configuration, lifecycle management, and Unity-optimized DI patterns. Masters dependency resolution, scoped containers, and testable architecture design. Use PROACTIVELY for VContainer setup, service registration, or SOLID principle implementation.
requires:
  - csharp-plugin:csharp-code-style
---

# Unity VContainer - High-Performance DI for Unity

## Overview

VContainer is a high-performance IoC container for Unity, providing dependency injection patterns for testable and maintainable code.

**Core Topics**:
- Constructor and method injection
- Service registration patterns (Singleton, Transient, Scoped)
- LifetimeScope hierarchies
- MonoBehaviour injection
- Factory patterns with DI
- Testing with mocks

**Foundation Required**: `unity-csharp-fundamentals` (TryGetComponent, FindAnyObjectByType, null-safe coding)

**Learning Path**: DI fundamentals → VContainer basics → Advanced patterns → Testing

## Quick Start

```csharp
using VContainer;
using VContainer.Unity;

// Define service interface
public interface IPlayerService
{
    void Initialize();
}

// Implement service
public class PlayerService : IPlayerService
{
    public void Initialize() => Debug.Log("Player initialized");
}

// Setup LifetimeScope
public class GameLifetimeScope : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        builder.Register<IPlayerService, PlayerService>(Lifetime.Singleton);
        builder.RegisterComponentInHierarchy<PlayerController>();
    }
}

// Inject into MonoBehaviour
public class PlayerController : MonoBehaviour
{
    [Inject] private readonly IPlayerService mPlayerService;

    void Start() => mPlayerService.Initialize();
}
```

## Key Concepts

### Lifetime Scopes
- **Singleton**: One instance per container
- **Transient**: New instance every resolve
- **Scoped**: One instance per scope

### Injection Types
- **Constructor Injection**: Preferred for required dependencies
- **Method Injection**: For optional dependencies
- **Property/Field Injection**: Use `[Inject]` attribute

## Reference Documentation

See [VContainer Best Practices](references/vcontainer-patterns.md) for detailed patterns.

## Best Practices

1. **Register interfaces**: Loose coupling and testability
2. **Constructor injection first**: Explicit dependencies
3. **Avoid Service Locator**: Don't resolve in Update loops
4. **Test with mocks**: Use ContainerBuilder in tests
5. **Clear hierarchies**: Root → Scene → Local scopes
