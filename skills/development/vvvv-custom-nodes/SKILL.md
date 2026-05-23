---
name: vvvv-custom-nodes
description: "Helps write C# node classes for vvvv gamma — the [ProcessNode] pattern, Update() method, out parameters, pin configuration, change detection, stateless operation nodes, and service consumption via NodeContext (IFrameClock, Game access, logging). Use when writing a node class, adding pins, implementing change detection, accessing services in node constructors, or creating stateless utility methods. Requires [assembly: ImportAsIs]."
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Tebjan Halm
  version: "1.0"
---

# Writing Custom Nodes for vvvv gamma

## ProcessNode Pattern — The Core Pattern

Every stateful C# node in vvvv gamma uses `[ProcessNode]`:

```csharp
[ProcessNode]
public class MyTransform : IDisposable
{
    private float _lastInput;
    private float _cachedResult;

    /// <summary>
    /// Transforms input values with caching.
    /// </summary>
    public void Update(
        out float result,       // OUT parameters FIRST
        out string error,       // More out params
        float input = 0f,       // Value inputs with defaults AFTER
        bool reset = false)
    {
        error = null;

        if (input != _lastInput || reset)
        {
            _cachedResult = ExpensiveComputation(input);
            _lastInput = input;
        }

        result = _cachedResult; // ALWAYS output cached data
    }

    public void Dispose() { /* cleanup */ }
}
```

**Prerequisite**: `[ProcessNode]` only works if `[assembly: ImportAsIs]` is set on the assembly. Projects created by vvvv include this automatically. For library-level `ImportAsIs` with Namespace/Category parameters, see vvvv-node-libraries.

### Non-Negotiable Rules

1. **`[ProcessNode]` attribute** on every stateful node class
2. **No "Node" in the vvvv-visible name** — everything in vvvv is already a node, so "Node" suffix is redundant
3. **`out` parameters FIRST**, value inputs with defaults AFTER
4. **XML comments** on class and Update method (shown as tooltip in vvvv)
5. **ZERO allocations in Update** — no `new`, no LINQ, cache everything
6. **Change detection** — only recompute when inputs actually change
7. **Always output latest data** — even when no work is done, output cached result
8. **No unnecessary public members** — data flows through Update in/out params only
9. **`IDisposable`** for any node holding native/unmanaged resources

### Live Reload Behavior

When the .vl document references a .csproj source project, vvvv compiles C# via Roslyn at runtime. On .cs file save, vvvv recompiles and restarts affected nodes:

1. `Dispose()` is called on the current instance (if `IDisposable`)
2. The new constructor runs with a fresh `NodeContext`
3. `Update()` resumes on the next frame

Implications for node authors:

- **Instance fields reset** — any state accumulated during runtime (caches, counters, connections) is lost on code change. This is expected.
- **Static fields also reset** — the entire in-memory assembly is replaced. Do not rely on static state to survive edits.
- **Dispose must be thorough** — native handles, network connections, and GPU resources must be released. Leaks accumulate across reloads during development.
- **Constructor must be fast** — it runs each time you save. Defer heavy initialization to the first `Update()` call using a `_needsInit` flag.
- The rules about caching and change detection above exist partly because of this: your code runs in a program that never stops. Allocations in `Update()` cause GC pressure in a 60 FPS loop that may run for hours.

### Class Naming vs Node Name

The rule is: **users must never see "Node" in vvvv's node browser**. How you achieve this:

```csharp
// Simple: class name IS the node name — no suffix needed
[ProcessNode]
public class Wander { }              // vvvv shows: "Wander"

// Class has "Node" suffix + Name property strips it — also fine
[ProcessNode(Name = "Scan")]
public class ScanNode { }            // vvvv shows: "Scan"

// Completely different internal name — fine when class manages another type
[ProcessNode(Name = "MeshRenderer", Category = "Stride.Rendering.Custom")]
public class CustomMeshRenderer { }  // vvvv shows: "MeshRenderer"
```

### HasStateOutput — Exposing Node Instance

```csharp
[ProcessNode(HasStateOutput = true)]
public class ParticleSystem
{
    // The node itself becomes an output pin,
    // allowing downstream nodes to call methods on it
    public void Update(out int particleCount, ...) { ... }
}
```

Alternative: return `this` from a method to expose the instance.

### Pin Visibility

```csharp
public void Update(
    out Spread<float> result,
    [Pin(Visibility = PinVisibility.OnlyInspector)] out string error,
    float input = 0f,
    [Pin(Visibility = PinVisibility.Optional)] bool advanced = false)
{
    // PinVisibility values:
    // Visible       — always shown (default)
    // Optional      — user can show/hide
    // Hidden        — not visible, only via inspector
    // OnlyInspector — only in inspector panel (use for debug/error outputs)
}
```

### Pin Groups (Collection Inputs)

For Spread inputs with add/remove buttons in vvvv:

```csharp
public void Update(
    out float result,
    [Pin(Name = "Input", PinGroupKind = PinGroupKind.Collection, PinGroupDefaultCount = 2)]
    Spread<IRenderer?> input)
{ }
```

### DefaultValue for Complex Types

For defaults that cannot be C# literal expressions:

```csharp
public void Update(
    [DefaultValue(typeof(Color4), "0.1, 0.1, 0.15, 1.0")] Color4 clearColor,
    [DefaultValue(typeof(Int2), "1920, 1080")] Int2 size,
    bool clear = true)
{ }
```

## Constructor Patterns

**Simple node** (no special context):
```csharp
public MyNode() { }
```

**Node needing NodeContext** (for AppHost, services, Fuse shader graphs):
```csharp
public MyNode(NodeContext nodeContext)
{
    _nodeContext = nodeContext;
    // Access: nodeContext.AppHost.IsExported, nodeContext.AppHost.Services, etc.
}
```

For IFrameClock injection, Stride Game access, logging, and service consumption patterns, see [services.md](services.md).

## Change Detection Patterns

### Simple — Direct Field Comparison

```csharp
private float _lastParam;
private Result _cached;

public void Update(out Result result, float param = 0f)
{
    if (param != _lastParam)
    {
        _cached = Compute(param);
        _lastParam = param;
    }
    result = _cached;
}
```

### Multi-Input — Hash Check

```csharp
private int _lastHash;
private Config _cached;

public void Update(out Config config, float a = 0f, int b = 0, string c = "")
{
    int hash = HashCode.Combine(a, b, c);
    if (hash != _lastHash)
    {
        _cached = new Config(a, b, c);
        _lastHash = hash;
    }
    config = _cached;
}
```

### Reference Types — Identity Check

```csharp
if (!ReferenceEquals(newBuffer, _lastBuffer))
{
    ProcessBuffer(newBuffer);
    _lastBuffer = newBuffer;
}
```

### Rebuild Flag — For Pipeline/Effect State

When multiple setters can invalidate state:

```csharp
private bool _needsRebuild = true;

public void SetShader(ShaderStage vs) { _shader = vs; _needsRebuild = true; }

public void Update(out Effect effect)
{
    if (_needsRebuild)
    {
        RebuildPipeline();
        _needsRebuild = false;
    }
    effect = _cachedEffect;
}
```

### Quick Reference

| Input Type | Comparison | Notes |
|---|---|---|
| Value types (int, float, bool) | `!=` | Direct comparison |
| Reference types (objects) | `ReferenceEquals()` | Identity, not equality |
| Multiple inputs | `HashCode.Combine()` | Single hash for dirty check |
| Collections | Length + sample elements | Full comparison too expensive |
| Multiple setters | `_needsRebuild` flag | Set flag in setters, check in Update |

## Return-Based Output (Single Output)

When a node has a single primary output, you can return it directly instead of using `out`:

```csharp
[ProcessNode]
public class NoiseSteering
{
    private SteeringConfig? _cached;

    public ISteering Update(
        float strength = 2.0f,
        float noiseFrequency = 0.05f,
        int priority = 0)
    {
        if (_cached is null || _cached.Strength != strength ||
            _cached.NoiseFrequency != noiseFrequency || _cached.Priority != priority)
        {
            _cached = new SteeringConfig(strength, noiseFrequency, priority);
        }
        return _cached;
    }
}
```

Mix return + `out` when you have one primary output plus additional outputs:
```csharp
public ReadOnlySpan<ParticleState> Update(
    SimulationConfig config,
    float deltaTime,
    out TimingStats stats)  // Secondary output via out
{
    // Returns primary output, secondary via out
}
```

## Rising Edge Detection (Bang/Trigger)

For boolean inputs that should trigger once (not every frame they're true):

```csharp
private bool _lastTrigger;

public void Update(out bool triggered, bool trigger = false)
{
    triggered = trigger && !_lastTrigger; // Rising edge only
    _lastTrigger = trigger;
}
```

## Operation Nodes

vvvv auto-generates nodes from **all public C# methods** — no attribute needed. Don't create `[ProcessNode]` wrappers for simple methods that just forward calls. Struct `Split()` methods also become nodes automatically.

Static methods auto-generate nodes — no `[ProcessNode]` needed:

```csharp
public static class MathOps
{
    public static float Remap(float value, float inMin = 0f, float inMax = 1f,
                              float outMin = 0f, float outMax = 1f)
    {
        float t = (value - inMin) / (inMax - inMin);
        return outMin + t * (outMax - outMin);
    }
}
```

### When to Use Which

| Pattern | Use When |
|---|---|
| `[ProcessNode]` class | Manages state between frames, caching, dirty-checking |
| Static method | Pure function, no state, transforms input to output |
| Struct + `Split()` | Data containers that unpack into separate pins |

## Memory & Performance in Update Loop

- **No `new` keyword** in hot paths
- **No LINQ** (`.Where`, `.Select`, `.ToList`) — hidden allocations via enumerators
- **Cache collections** — pre-allocate, reuse arrays/lists
- **No string concatenation** — use `StringBuilder` if needed, but avoid in hot path
- **Vector types**: `System.Numerics` internally for SIMD, `Stride.Core.Mathematics` at API boundaries
- **Zero-cost conversion**: `Unsafe.As<StrideVector3, NumericsVector3>(ref val)`

For custom regions (delegate-based, ICustomRegion, IRegion\<TInlay\>), see [regions.md](regions.md).
For advanced patterns (FragmentSelection, Smell, Dynamic Enums, Settings/Split, Pin Name Derivation), see [advanced.md](advanced.md).
For service consumption (IFrameClock, Game, Logging), see [services.md](services.md).
For working with public channels from C# nodes, see vvvv-channels.
For code examples, see [examples.md](examples.md).
For starter templates, see [templates/](templates/).
