---
name: unity-unitask
description: UniTask library expert specializing in allocation-free async/await patterns, coroutine migration, and Unity-optimized asynchronous programming. Masters UniTask performance optimizations, cancellation handling, and memory-efficient async operations. Use PROACTIVELY for UniTask implementation, async optimization, or coroutine replacement.
requires:
  - csharp-plugin:csharp-code-style
---

# UniTask - High-Performance Async for Unity

## Overview

UniTask is a zero-allocation async/await library optimized for Unity, providing allocation-free asynchronous programming patterns superior to standard C# Task.

**Foundation Required**: `unity-csharp-fundamentals` (TryGetComponent, FindAnyObjectByType), `csharp-async-patterns` (Task, async/await), `unity-async` (Unity async context)

**Core Topics**:
- Allocation-free async/await patterns
- Coroutine to UniTask migration
- PlayerLoop-based execution model
- Memory pool management and GC pressure reduction
- Advanced cancellation and timeout handling
- Integration with Unity systems (Addressables, DOTween, etc.)

**Learning Path**: C# async basics → Unity async context → UniTask optimization → Production patterns

## Quick Start

### UniTask vs Task Performance

```csharp
// Standard Task (allocates memory)
public async Task<int> GetStandard()
{
    await Task.Delay(1000);
    return 42;
}

// UniTask (zero allocation)
public async UniTask<int> GetOptimized()
{
    await UniTask.Delay(1000);
    return 42;
}
```

### Basic Patterns

```csharp
// Frame-based delays
await UniTask.Yield();                    // Next frame
await UniTask.DelayFrame(10);            // Wait 10 frames
await UniTask.NextFrame();               // Explicit next frame

// Time-based delays
await UniTask.Delay(TimeSpan.FromSeconds(1));
await UniTask.WaitForSeconds(1f);

// Unity operations
await Resources.LoadAsync<Sprite>("icon").ToUniTask();
await SceneManager.LoadSceneAsync("Level1").ToUniTask();

// Cancellation
CancellationTokenSource cts = new CancellationTokenSource();
await SomeOperation(cts.Token);
```

## When to Use

### UniTask (This Skill)
- Zero-allocation critical paths (mobile, performance-critical scenarios)
- Memory-efficient async operations
- PlayerLoop timing control and customization
- Coroutine replacement for better performance
- Integration with Unity async operations

### Alternatives
- **unity-async skill**: General Unity async patterns, coroutines, Job System
- **Standard Task**: Cross-platform .NET code, non-performance-critical scenarios

## Reference Documentation

### [UniTask Fundamentals](references/unitask-fundamentals.md)
Core UniTask concepts and migration:
- UniTask vs Task performance characteristics
- Coroutine migration patterns
- PlayerLoop execution model
- Memory pool management
- Basic async operations

### [Performance Optimization](references/performance-optimization.md)
Advanced performance techniques:
- Allocation-free patterns
- GC pressure reduction
- PlayerLoop timing control
- Memory profiling with UniTask.Tracker
- Burst-compatible async patterns

### [Integration Patterns](references/integration-patterns.md)
Unity system integrations:
- Addressables async loading
- DOTween integration
- UnityWebRequest patterns
- UI event handling
- AsyncReactiveProperty usage

## Key Principles

1. **Zero-Allocation Focus**: UniTask eliminates allocations for async operations
2. **PlayerLoop Integration**: Tight Unity integration for optimal performance
3. **Always Support Cancellation**: Use `this.GetCancellationTokenOnDestroy()` for MonoBehaviour lifecycle
4. **Prefer UniTask over Task**: Better performance and Unity compatibility
5. **Profile Memory Usage**: Use UniTask.Tracker to monitor active tasks and memory

## Common Patterns

### Automatic Cancellation with MonoBehaviour

```csharp
public class Example : MonoBehaviour
{
    async UniTaskVoid Start()
    {
        // Auto-cancels when GameObject is destroyed
        await LoadData(this.GetCancellationTokenOnDestroy());
    }
}
```

### Parallel Operations

```csharp
// Execute multiple operations in parallel
(int result1, string result2, float result3) = await UniTask.WhenAll(
    Operation1(),
    Operation2(),
    Operation3()
);
```

### Timeout Handling

```csharp
CancellationTokenSource cts = new CancellationTokenSource();
cts.CancelAfterSlim(TimeSpan.FromSeconds(5)); // PlayerLoop-based

try
{
    await LongOperation(cts.Token);
}
catch (OperationCanceledException)
{
    Debug.Log("Operation timed out");
}
```

## Platform Considerations

- **WebGL**: Limited threading, UniTask provides frame-based async as primary pattern
- **Mobile**: Critical for battery optimization and memory efficiency
- **Desktop**: Full feature support with optimal performance

## Best Practices

1. **Use CancellationToken**: Always pass cancellation tokens, prefer `this.GetCancellationTokenOnDestroy()`
2. **Avoid async void**: Use `UniTaskVoid` for fire-and-forget operations
3. **PlayerLoop Optimization**: Use minimal PlayerLoop injection for better performance
4. **Profile with Tracker**: Monitor memory with `UniTask.Tracker` in editor
5. **Chain Operations**: Use `WhenAll`/`WhenAny` for parallel execution
6. **Thread Switching**: Use `SwitchToMainThread()`/`SwitchToThreadPool()` appropriately

## Integration with Other Skills

- **unity-async**: Provides foundation for Unity async patterns
- **unity-reactive**: AsyncReactiveProperty bridges UniTask with R3
- **unity-di**: UniTask works seamlessly with VContainer DI patterns
- **unity-performance**: UniTask reduces GC pressure significantly
