---
name: unity-async
description: Handle Unity's asynchronous programming patterns including coroutines, async/await, and Job System. Masters Unity's main thread restrictions and threading models. Use when guidance needed on Unity async operations, coroutine optimization, or parallel processing in Unity context.
requires:
  - csharp-plugin:csharp-code-style
  - csharp-plugin:csharp-async-patterns
---

# Unity Async Patterns

## Overview

Unity-specific async patterns extending foundational C# async/await concepts.

**Foundation Required**: `unity-csharp-fundamentals` (TryGetComponent, FindAnyObjectByType, null-safe coding)

**Core Topics**:
- Coroutines and yield instructions
- async/await with Unity main thread constraints
- Unity Job System and Burst compiler
- Thread safety and marshaling
- Addressables and UnityWebRequest integration

**Learning Path**: C# async basics → Unity context → UniTask optimization → Reactive patterns

## Quick Start

### Three Unity Async Approaches

```csharp
// 1. Coroutine (Unity-specific, frame-based)
IEnumerator LoadDataCoroutine()
{
    yield return new WaitForSeconds(1f);
    UnityWebRequest request = UnityWebRequest.Get(url);
    yield return request.SendWebRequest();
    ProcessData(request.downloadHandler.text);
}

// 2. Async/Await (C# standard + Unity constraints)
async Task<string> LoadData(CancellationToken ct)
{
    await Task.Delay(1000, ct);
    using UnityWebRequest request = UnityWebRequest.Get(url);
    await request.SendWebRequest();
    return request.downloadHandler.text;
    // Unity auto-marshals to main thread
}

// 3. Job System (parallel data processing)
[BurstCompile]
struct VelocityJob : IJobParallelFor
{
    [ReadOnly] public NativeArray<Vector3> velocities;
    public NativeArray<Vector3> positions;
    public float deltaTime;

    public void Execute(int index)
    {
        positions[index] += velocities[index] * deltaTime;
    }
}
```

## When to Use

### Unity Async (This Skill)
- Frame-based timing and Unity API integration
- Standard async/await with Unity constraints
- Job System parallelization
- Main thread restrictions and solutions

### Specialized Agents
- **unity-unitask-pro**: Zero-allocation async, memory-critical scenarios
- **unity-reactive-pro**: Event streams, MVVM/MVP, reactive state management

## Reference Documentation

### Unity-Specific Extensions

**[Unity Async Best Practices](references/unity-async-best-practices.md)**
- Coroutines vs async/await decision framework
- Main thread restrictions and solutions
- Job System usage patterns
- MonoBehaviour lifecycle integration

**[Coroutine Patterns](references/coroutine-patterns.md)**
- yield return variations
- Coroutine chaining and composition
- Custom yield instructions
- Performance considerations

**[Unity Threading Guide](references/unity-threading.md)**
- Main thread vs background threads
- UnityMainThreadDispatcher patterns
- Job System and Burst compiler
- Thread-safe data structures (NativeArray, NativeContainer)

## Key Principles

1. **Main Thread Only**: Unity APIs require main thread
2. **Coroutines for Frames**: Frame-based operations use coroutines
3. **Job System for Parallelism**: CPU-intensive data processing
4. **UniTask for Performance**: Zero-allocation critical paths
5. **R3 for Reactive**: Complex event streams and data binding

## Common Patterns

### Frame Timing
```csharp
yield return null;                    // Next frame
yield return new WaitForEndOfFrame(); // After rendering
yield return new WaitForFixedUpdate(); // Physics update
```

### Async Resource Loading
```csharp
AsyncOperation asyncLoad = SceneManager.LoadSceneAsync("Scene");
while (!asyncLoad.isDone)
{
    float progress = Mathf.Clamp01(asyncLoad.progress / 0.9f);
    yield return null;
}
```

### Addressables Integration
```csharp
AsyncOperationHandle<GameObject> handle = Addressables.LoadAssetAsync<GameObject>("AssetKey");
await handle.Task;
GameObject prefab = handle.Result;
```

## Platform Considerations

- **WebGL**: No threading, coroutines primary, Job System unavailable
- **Mobile**: Battery optimization critical, limit thread count
- **Desktop**: Full threading support, higher performance budgets

## Agent Delegation

```
Unity Async Needs
├── Frame timing → unity-async (coroutines)
├── Standard async → unity-async (async/await)
├── Parallel data → unity-async (Job System)
├── Zero-allocation → unity-unitask-pro agent
└── Reactive patterns → unity-reactive-pro agent
```
