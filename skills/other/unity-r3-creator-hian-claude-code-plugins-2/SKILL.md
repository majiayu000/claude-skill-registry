---
name: unity-r3
description: R3 (Reactive Extensions) library expert specializing in modern reactive programming patterns, event-driven architectures, and Observable streams. Masters R3-specific features, async enumerable integration, and Unity-optimized reactive patterns. Use PROACTIVELY for R3 implementation, reactive programming, or MVVM/MVP architecture.
requires:
  - csharp-plugin:csharp-code-style
---

# Unity R3 - Modern Reactive Extensions for Unity

## Overview

R3 is a modern, high-performance Reactive Extensions library for Unity developed by Cysharp (same author as UniTask), providing observable streams and reactive patterns optimized for Unity.

**Library**: [R3 by Cysharp](https://github.com/Cysharp/R3)

**R3 vs UniRx**: R3 is the modern successor to UniRx with better performance, async enumerable support, and Unity 2022+ optimization. For legacy UniRx projects, see `unity-unirx` skill.

**Foundation Required**: `unity-csharp-fundamentals` (TryGetComponent, FindAnyObjectByType), `csharp-async-patterns` (async fundamentals), `unity-async` (Unity context)

**Core Topics**:
- Observable sequences and observers
- Reactive operators and transformations
- Hot vs Cold observables
- ReactiveProperty for state management
- Event-driven architecture patterns
- MVVM/MVP implementation
- UI event handling and data binding

**Learning Path**: C# events → Reactive patterns → Observable composition → MVVM architecture

## Quick Start

### Basic Observable Patterns

```csharp
using R3;

// Create observable from events
button.OnClickAsObservable()
    .Subscribe(_ => Debug.Log("Button clicked!"))
    .AddTo(this);

// Property observation
this.ObserveEveryValueChanged(x => x.transform.position)
    .Subscribe(pos => Debug.Log($"Position: {pos}"))
    .AddTo(this);

// Time-based observables
Observable.Interval(TimeSpan.FromSeconds(1))
    .Subscribe(x => Debug.Log($"Tick: {x}"))
    .AddTo(this);
```

### ReactiveProperty

```csharp
// Reactive state management
public class Player : MonoBehaviour
{
    public ReactiveProperty<int> Health { get; } = new(100);
    public ReadOnlyReactiveProperty<bool> IsDead { get; }

    public Player()
    {
        IsDead = Health.Select(h => h <= 0).ToReadOnlyReactiveProperty();
    }
}
```

## When to Use

### Unity Reactive (This Skill)
- Event-driven architecture and complex event handling
- MVVM/MVP pattern implementation
- UI data binding and reactive state
- Asynchronous event streams
- Complex state management
- Real-time data flow coordination

### Alternatives
- **unity-unirx**: Legacy UniRx library (pre-2022 projects)
- **unity-async/unity-unitask**: Single async operations, not event streams
- **C# events**: Simple event handling without composition

### R3-Specific Features
- Async enumerable (`IAsyncEnumerable<T>`) integration
- Better performance than UniRx
- Unity 2022+ optimization
- Struct-based observers for zero allocation
- Built-in time providers for testing

## Reference Documentation

### [Reactive Fundamentals](references/reactive-fundamentals.md)
Core R3 concepts:
- Observable creation patterns
- Hot vs Cold observables
- Subscription lifecycle
- Marble diagrams
- Basic operators (Select, Where, DistinctUntilChanged)

### [Reactive Operators](references/reactive-operators.md)
Transformation and composition:
- Filtering operators (Where, Throttle, Debounce)
- Transformation operators (Select, SelectMany)
- Combination operators (CombineLatest, Merge, Zip)
- Time operators (Delay, Timeout, Sample)
- Error handling operators (Catch, Retry)

### [Architecture Patterns](references/architecture-patterns.md)
Application patterns:
- MVVM with ReactiveProperty
- Event Aggregator pattern
- State management systems
- UI data binding
- Message broker implementation

## Key Principles

1. **Declarative Event Handling**: Define what should happen, not how to subscribe/unsubscribe
2. **Automatic Disposal**: Use `AddTo(this)` for MonoBehaviour lifecycle management
3. **Composition over Callbacks**: Chain operators instead of nested callbacks
4. **Hot/Cold Awareness**: Understand when observables start emitting
5. **Marble Diagram Thinking**: Visualize data flow over time

## Common Patterns

### UI Event Handling

```csharp
// Button with throttle to prevent spam
button.OnClickAsObservable()
    .Throttle(TimeSpan.FromSeconds(1))
    .Subscribe(_ => OnButtonClick())
    .AddTo(this);

// Input validation
inputField.OnValueChangedAsObservable()
    .Where(text => text.Length > 3)
    .Throttle(TimeSpan.FromSeconds(0.5))
    .Subscribe(ValidateInput)
    .AddTo(this);
```

### State Management

```csharp
public class GameState : MonoBehaviour
{
    public ReactiveProperty<int> Score { get; } = new(0);
    public ReactiveProperty<int> Lives { get; } = new(3);
    public ReadOnlyReactiveProperty<bool> GameOver { get; }

    public GameState()
    {
        GameOver = Lives.Select(l => l <= 0).ToReadOnlyReactiveProperty();

        GameOver.Where(over => over)
            .Subscribe(_ => OnGameOver())
            .AddTo(this);
    }
}
```

### Multiple Stream Combination

```csharp
// Combine position and health for decision making
Observable.CombineLatest(
    playerTransform.ObserveEveryValueChanged(t => t.position),
    playerHealth.Health,
    (pos, health) => new { Position = pos, Health = health }
)
.Where(state => state.Health < 30)
.Subscribe(state => FindNearestHealthPack(state.Position))
.AddTo(this);
```

## Integration with Other Skills

- **unity-unitask**: Convert observables to UniTask with `ToUniTask()`
- **unity-vcontainer**: Inject ReactiveProperty as dependencies via VContainer
- **unity-ui**: Bind observables to UI elements for automatic updates
- **unity-async**: Bridge async operations with `Observable.FromAsync()`
- **unity-unirx**: For legacy projects (not recommended for new projects)

## Platform Considerations

- **WebGL**: Full support with frame-based timing
- **Mobile**: Efficient for UI and event handling
- **All Platforms**: Zero allocation after initial setup

## Best Practices

1. **Always use AddTo()**: Prevent memory leaks with automatic disposal
2. **Throttle/Debounce user input**: Prevent excessive processing
3. **Use ReactiveProperty for state**: Better than manual event raising
4. **Understand hot vs cold**: Know when subscriptions trigger work
5. **Avoid nested subscriptions**: Use `SelectMany` for flattening
6. **Test with TestScheduler**: Write deterministic reactive tests
7. **Consider backpressure**: Handle fast producers with `Sample` or `Buffer`
