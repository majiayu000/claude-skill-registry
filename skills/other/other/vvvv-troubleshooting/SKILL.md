---
name: vvvv-troubleshooting
description: Diagnoses and fixes common vvvv gamma errors in C# nodes, SDSL shaders, and runtime behavior. Use when encountering errors, exceptions, crashes, red nodes, shader compilation failures, missing nodes in the browser, performance issues, or unexpected behavior.
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Tebjan Halm
  version: "1.0"
---

# vvvv gamma Troubleshooting

## C# / ProcessNode Issues

### "Node" Suffix in Class Name

**Symptom**: Node works but has ugly name in vvvv.
**Fix**: Remove "Node" suffix — vvvv convention forbids it.

```csharp
// WRONG
[ProcessNode]
public class SteeringBehaviorNode { }

// CORRECT
[ProcessNode]
public class SteeringBehavior { }
```

### Out Parameters After Inputs

**Symptom**: Pins appear in wrong order or node doesn't compile correctly.
**Fix**: `out` parameters must come FIRST in Update signature.

```csharp
// WRONG
public void Update(float input = 0f, out float result) { ... }

// CORRECT
public void Update(out float result, float input = 0f) { ... }
```

### Node Not Appearing in Node Browser

**Symptom**: Your C# class exists but doesn't show up in vvvv.
**Fix**: Check these in order:
1. `[assembly: ImportAsIs]` attribute exists in your project
2. `[ProcessNode]` attribute on the class
3. Project targets `net8.0`
4. DLL is in the correct `lib/net8.0/` path relative to `.vl` document
5. Project builds without errors

### Allocations Causing Frame Drops

**Symptom**: GC spikes, stuttering, frame drops.
**Diagnosis**: Allocations in the Update loop.

Common culprits:
- `new` keyword in Update method
- LINQ operators (`.Where()`, `.Select()`, `.ToList()`)
- String concatenation (`+` operator on strings)
- Boxing value types (passing `int` where `object` expected)

**Fix**: Cache everything, pre-allocate buffers, eliminate LINQ from hot paths.

### Missing Change Detection

**Symptom**: CPU usage high even when nothing changes.
**Fix**: Compare inputs to cached values, only recompute on change.

```csharp
if (param != _lastParam)
{
    _cached = Compute(param);
    _lastParam = param;
}
result = _cached; // Always output cached
```

### Downstream Nodes See null/default

**Symptom**: Connected nodes get no data, even though the node "works".
**Fix**: Always output cached result, even when no computation happens.

```csharp
// WRONG — output is only set inside the if block
public void Update(out float result, float input = 0f)
{
    if (input != _last)
    {
        result = Compute(input);
        _last = input;
    }
    // result is unassigned when input hasn't changed!
}

// CORRECT — always assign output
public void Update(out float result, float input = 0f)
{
    if (input != _last)
    {
        _cached = Compute(input);
        _last = input;
    }
    result = _cached;
}
```

## SDSL Shader Issues

For SDSL syntax rules, common mistakes, and correct/wrong examples, see [vvvv-shaders/syntax-rules.md](../vvvv-shaders/syntax-rules.md). Key issues: `static const` scope, missing semicolons, missing `override`, enum binding format.

## Runtime Issues

### Memory Leaks

**Symptom**: Memory usage grows over time.
**Causes**:
- Missing `IDisposable` on nodes with native resources
- COM objects (`ComPtr<T>`) not disposed
- Event handler subscriptions not unsubscribed

### Thread Safety

**Symptom**: Intermittent crashes, data corruption.
**Fix**: `Update()` runs on the main thread. Capture `SynchronizationContext` in the constructor, then marshal background results back:

```csharp
private SynchronizationContext _vlSyncContext;

public MyNode()
{
    _vlSyncContext = SynchronizationContext.Current!;
}

// From background thread:
_vlSyncContext.Post(_ => { /* runs on VL thread */ }, null);
```

### Circular Dependencies

**Symptom**: vvvv warns about circular dependency, patch won't compile.
**Fix**: Insert a `FrameDelay` node to break the cycle.

## Build Issues

### Target Framework Mismatch

**Symptom**: DLL loads but types aren't found.
**Fix**: Ensure `.csproj` targets `net8.0` (matching vvvv gamma's runtime).

### Assembly Version Conflicts

**Symptom**: `FileLoadException` or `TypeLoadException` at runtime.
**Fix**: Align package versions with vvvv's bundled versions. Check vvvv's `lib/` folder for reference.

For detailed error-to-solution mapping, see [error-catalog.md](error-catalog.md).
