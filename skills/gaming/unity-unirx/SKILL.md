---
name: unity-unirx
description: UniRx (Reactive Extensions) library expert for legacy Unity projects. Specializes in UniRx-specific patterns, Observable streams, and ReactiveProperty. Use for maintaining existing UniRx codebases. For new projects, use unity-r3 skill instead.
requires:
  - csharp-plugin:csharp-code-style
---

# Unity UniRx - Reactive Extensions for Unity (Legacy)

## Overview

UniRx is a legacy Reactive Extensions library for Unity, widely used in pre-2022 Unity projects. For new projects, prefer R3 (`unity-r3` skill).

**Library**: [UniRx by neuecc](https://github.com/neuecc/UniRx)

**UniRx vs R3**: UniRx is the predecessor to R3. R3 offers better performance and modern C# features, but UniRx is still maintained and used in many existing projects.

**Status**: ⚠️ Legacy library - Maintained but not actively developed. New projects should use R3.

**Foundation Required**: `unity-csharp-fundamentals` (TryGetComponent, FindAnyObjectByType), `csharp-async-patterns` (async fundamentals), `unity-async` (Unity context)

**Core Topics**:
- Observable sequences and observers
- Reactive operators and transformations
- ReactiveProperty and ReactiveCommand
- UniRx-specific Unity integration
- MessageBroker pattern
- MainThreadDispatcher

**Learning Path**: C# events → UniRx basics → Observable composition → MVVM with UniRx

## Quick Start

### Basic Observable Patterns

```csharp
using UniRx;
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        // Button clicks
        button.OnClickAsObservable()
            .Subscribe(_ => Debug.Log("Clicked"))
            .AddTo(this);

        // Update loop as observable
        Observable.EveryUpdate()
            .Where(_ => Input.GetKeyDown(KeyCode.Space))
            .Subscribe(_ => Jump())
            .AddTo(this);

        // Time-based
        Observable.Timer(TimeSpan.FromSeconds(1))
            .Subscribe(_ => Debug.Log("1 second passed"))
            .AddTo(this);
    }
}
```

### ReactiveProperty (UniRx)

```csharp
using UniRx;

public class Player : MonoBehaviour
{
    // IntReactiveProperty is UniRx-specific
    public IntReactiveProperty Health = new IntReactiveProperty(100);
    public ReadOnlyReactiveProperty<bool> IsDead;

    void Awake()
    {
        IsDead = Health
            .Select(h => h <= 0)
            .ToReadOnlyReactiveProperty();

        IsDead.Where(dead => dead)
            .Subscribe(_ => OnDeath())
            .AddTo(this);
    }

    public void TakeDamage(int amount)
    {
        Health.Value -= amount;
    }
}
```

## When to Use

### Unity UniRx (This Skill)
- ✅ Maintaining existing UniRx projects
- ✅ Unity 2019 - 2021 LTS projects
- ✅ Projects with large UniRx codebase
- ✅ Teams experienced with UniRx

### When to Choose R3 Instead
- ✅ New projects (Unity 2022+)
- ✅ Better performance requirements
- ✅ Async enumerable integration needed
- ✅ Modern C# feature support

## UniRx-Specific Features

### MessageBroker Pattern

```csharp
using UniRx;

// Global event system
public class GameEvents
{
    public struct PlayerDiedEvent { }
    public struct ScoreChangedEvent { public int NewScore; }
}

// Publish
MessageBroker.Default.Publish(new GameEvents.PlayerDiedEvent());

// Subscribe
MessageBroker.Default.Receive<GameEvents.PlayerDiedEvent>()
    .Subscribe(_ => ShowGameOver())
    .AddTo(this);
```

### ReactiveCommand

```csharp
using UniRx;

public class ViewModel
{
    // Command can be enabled/disabled reactively
    public ReactiveCommand AttackCommand { get; }

    private IntReactiveProperty mStamina = new IntReactiveProperty(100);

    public ViewModel()
    {
        // Command only enabled when stamina > 10
        AttackCommand = mStamina
            .Select(s => s > 10)
            .ToReactiveCommand();

        AttackCommand.Subscribe(_ => ExecuteAttack());
    }
}
```

### MainThreadDispatcher

```csharp
using UniRx;
using System.Threading.Tasks;

async Task DoBackgroundWork()
{
    // Do background work
    await Task.Run(() => HeavyComputation());

    // Return to Unity main thread
    await UniRx.MainThreadDispatcher.SendStartCoroutine(UpdateUI());
}
```

## Common UniRx Patterns

### UI Event Handling

```csharp
// Input field with validation
inputField.OnValueChangedAsObservable()
    .Where(text => text.Length >= 3)
    .Throttle(TimeSpan.FromMilliseconds(500))
    .Subscribe(text => ValidateInput(text))
    .AddTo(this);

// Toggle button
toggle.OnValueChangedAsObservable()
    .Subscribe(isOn => OnToggleChanged(isOn))
    .AddTo(this);
```

### Coroutine Integration

```csharp
// Convert coroutine to observable
Observable.FromCoroutine<string>(observer => GetDataCoroutine(observer))
    .Subscribe(data => ProcessData(data))
    .AddTo(this);

IEnumerator GetDataCoroutine(IObserver<string> observer)
{
    UnityWebRequest www = UnityWebRequest.Get(url);
    yield return www.SendWebRequest();
    observer.OnNext(www.downloadHandler.text);
    observer.OnCompleted();
}
```

### MVVM Pattern (UniRx)

```csharp
// ViewModel
public class PlayerViewModel : IDisposable
{
    private CompositeDisposable mDisposables = new CompositeDisposable();

    public IReadOnlyReactiveProperty<int> Health { get; }
    public IReadOnlyReactiveProperty<string> Status { get; }
    public ReactiveCommand HealCommand { get; }

    private IntReactiveProperty mHealth = new IntReactiveProperty(100);

    public PlayerViewModel()
    {
        Health = mHealth.ToReadOnlyReactiveProperty().AddTo(mDisposables);

        Status = mHealth
            .Select(h => h <= 30 ? "Critical" : h <= 70 ? "Wounded" : "Healthy")
            .ToReadOnlyReactiveProperty()
            .AddTo(mDisposables);

        HealCommand = mHealth
            .Select(h => h < 100)
            .ToReactiveCommand()
            .AddTo(mDisposables);

        HealCommand.Subscribe(_ => mHealth.Value += 20).AddTo(mDisposables);
    }

    public void Dispose()
    {
        mDisposables.Dispose();
    }
}
```

## Migration to R3

If migrating from UniRx to R3:

### API Differences

```csharp
// UniRx
IntReactiveProperty health = new IntReactiveProperty(100);
ReadOnlyReactiveProperty<bool> isDead = health
    .Select(h => h <= 0)
    .ToReadOnlyReactiveProperty();

// R3 (nearly identical)
ReactiveProperty<int> health = new ReactiveProperty<int>(100);
ReadOnlyReactiveProperty<bool> isDead = health
    .Select(h => h <= 0)
    .ToReadOnlyReactiveProperty();
```

### Key Migration Points
1. **Namespace**: `using UniRx;` → `using R3;`
2. **Types**: `IntReactiveProperty` → `ReactiveProperty<int>`
3. **MessageBroker**: No direct equivalent in R3 (implement custom or use event aggregator)
4. **MainThreadDispatcher**: R3 uses `Observable.ReturnOnMainThread()` and Unity's `SynchronizationContext`

## Integration with Other Skills

- **unity-r3**: Modern alternative for new projects
- **unity-unitask**: UniRx can work with UniTask via conversion methods
- **unity-vcontainer**: Inject ReactiveProperty as dependencies
- **unity-ui**: Bind UniRx observables to UI elements
- **unity-async**: Bridge async operations with `Observable.FromAsync()`

## Platform Considerations

- **WebGL**: Full support with frame-based timing
- **Mobile**: Efficient for UI and event handling
- **All Platforms**: Mature and battle-tested

## Best Practices

1. **Always use AddTo()**: Prevent memory leaks with automatic disposal
2. **Use CompositeDisposable**: Group related subscriptions for cleanup
3. **Throttle/Debounce input**: Prevent excessive processing
4. **ReactiveProperty for state**: Better than manual event raising
5. **MessageBroker for global events**: Decoupled communication
6. **MainThreadDispatcher awareness**: Always return to main thread for Unity APIs
7. **Consider migration to R3**: For long-term projects on Unity 2022+

## Performance Notes

UniRx performance is good but R3 offers:
- 30-50% better allocation performance
- Struct-based observers (zero allocation)
- Better GC pressure management
- Async enumerable integration

For performance-critical applications on Unity 2022+, migrate to R3.

## Reference

For detailed UniRx patterns, refer to:
- [UniRx GitHub](https://github.com/neuecc/UniRx)
- [UniRx Official Wiki](https://github.com/neuecc/UniRx/wiki)

**Migration Guide**: See `unity-r3` skill for R3 patterns and migration considerations.
