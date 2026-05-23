---
name: vvvv-channels
description: Helps work with vvvv gamma's Channel system from C# — IChannelHub, public channels, [CanBePublished] attributes, hierarchical data propagation, channel subscriptions, bang channels, and spread sub-channels. Use when reading or writing public channels from C# nodes, publishing .NET types as channels, working with IChannelHub, subscribing to channel changes, or managing hierarchical channel state.
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Tebjan Halm
  version: "1.0"
---

# vvvv gamma Channels — C# Integration

## What Are Channels

Channels are **named, typed, observable value containers** — the central reactive data flow mechanism in vvvv gamma. Any code (patches, C# nodes, external bindings) can read and write channels by their string path.

Key properties:

- Each channel has a **path** (string), a **type**, and a **current value**
- Setting a value fires all subscribers (reactive push)
- vvvv provides built-in channel bindings for MIDI, OSC, Redis, and UI
- Channels persist state across sessions

## Public Channels and IChannelHub

**Public channels** are channels registered in the app-wide channel hub — accessible by any code via string path lookup.

### Core API (`VL.Core.Reactive`)

```csharp
using VL.Core.Reactive;

// Get the app-wide channel hub (singleton)
var hub = IChannelHub.HubForApp;

// Safe lookup — returns null if channel doesn't exist yet
IChannel<object>? ch = hub.TryGetChannel("MyApp.Settings.Volume");

// Read the current value
object? value = ch.Object;

// Write a new value (fires all subscribers)
ch.Object = newValue;
```

**CRITICAL: NEVER use `hub.TryAddChannel()`** — it creates channels with `null` values, which causes `NullReferenceException` in vvvv's `SubChannelsBinding.EnsureMutatingPropertiesAreReflectedInChannels`. The SubChannel system tries to walk properties of the null value and crashes. Always use `TryGetChannel` (lookup only).

## [CanBePublished] Attribute

For vvvv to expose .NET type properties as public channels, the type must be decorated with `[CanBePublished(true)]` from `VL.Core.EditorAttributes`.

```csharp
using VL.Core.EditorAttributes;

// All public properties become channels when this type is published
[CanBePublished(true)]
public class MyModel
{
    // Standard .NET types work directly — float, bool, string, Vector3, etc.
    public float Volume { get; set; } = 0.5f;
    public bool Muted { get; set; } = false;
    public string Label { get; set; } = "Default";

    // Hidden from the channel system entirely
    [CanBePublished(false)]
    public string InternalId { get; } = Guid.NewGuid().ToString();
}
```

Rules:

- `[CanBePublished(true)]` on a class/struct → all properties are published as channels
- `[CanBePublished(false)]` on an individual property → hides it from the channel system
- **.NET types are NOT published by default** — the attribute is required
- Available from `VL.Core` version `2025.7.1-0163`+

## Channel Path Conventions

Channels use dot-separated hierarchical paths. Spread elements use bracket notation:

```
Root.Page.Zone.Group.Parameter          — leaf parameter
Root.Page.Zone                          — hierarchy node (model object)
Root.Page.Items[0].PropertyName         — spread element sub-channel
Root.Page.Items[2].DeleteInstance        — indexed bang channel
```

Sub-channels are **created automatically** by vvvv's SubChannel system when a type with `[CanBePublished(true)]` is published. You don't create them manually.

Use `const string` path constants to avoid typos:

```csharp
public static class ChannelPaths
{
    public const string Volume = "Settings.Audio.Volume";
    public const string Brightness = "App.Scene.Display.Brightness";
}
```

## Retry-Bind Pattern

Channels may not exist when your node starts — vvvv publishes them after model initialization. You must retry each frame until the channel appears:

```csharp
[ProcessNode]
public class MyChannelReader : IDisposable
{
    private IChannel<object>? _channel;

    public void Update(out float value)
    {
        // Retry until channel exists
        if (_channel == null)
        {
            var hub = IChannelHub.HubForApp;
            if (hub != null)
                _channel = hub.TryGetChannel("Settings.Audio.Volume");
        }

        // Read value (with safe cast)
        value = _channel?.Object is float f ? f : 0f;
    }

    public void Dispose() { _channel = null; }
}
```

Once bound, the cached reference is valid for the node's lifetime — no need to re-lookup.

## PublicChannelHelper — Reusable Utility

A helper class that encapsulates the retry-bind + optional subscription pattern. Reusable in any project:

```csharp
public class PublicChannelHelper : IDisposable
{
    private IChannel<object>? _channel;
    private IDisposable? _subscription;
    private readonly Action<object?>? _onNext;

    public PublicChannelHelper(Action<object?>? onNext = null)
    {
        _onNext = onNext;
    }

    public IChannel<object>? Channel => _channel;
    public bool IsBound => _channel != null;

    public bool TryBind(IChannelHub hub, string path)
    {
        if (_channel != null) return true;

        var ch = hub.TryGetChannel(path);
        if (ch == null) return false;

        _channel = ch;
        if (_onNext != null)
            _subscription = ch.Subscribe(new CallbackObserver(_onNext));
        return true;
    }

    public void Dispose()
    {
        _subscription?.Dispose();
        _subscription = null;
        _channel = null;
    }

    private sealed class CallbackObserver : IObserver<object?>
    {
        private readonly Action<object?> _onNext;
        public CallbackObserver(Action<object?> onNext) => _onNext = onNext;
        public void OnNext(object? value) => _onNext(value);
        public void OnError(Exception error) { }
        public void OnCompleted() { }
    }
}
```

Usage in a ProcessNode:

```csharp
[ProcessNode]
public class VolumeReader : IDisposable
{
    private readonly PublicChannelHelper _ch = new();

    public void Update(out float value, out IChannel<object>? channel)
    {
        if (!_ch.IsBound)
        {
            var hub = IChannelHub.HubForApp;
            if (hub != null) _ch.TryBind(hub, "Settings.Audio.Volume");
        }
        value = _ch.Channel?.Object is float f ? f : 0f;
        channel = _ch.Channel;
    }

    public void Dispose() => _ch.Dispose();
}
```

## Channel Accessor Node Patterns

Three patterns for ProcessNodes that wrap channel access:

### Hierarchy Node (reads a model object)

```csharp
[ProcessNode]
public class Camera : IDisposable
{
    private readonly PublicChannelHelper _ch = new();

    public void Update(out CameraSettings? value, out IChannel<object>? channel)
    {
        if (!_ch.IsBound)
        {
            var hub = IChannelHub.HubForApp;
            if (hub != null) _ch.TryBind(hub, "App.Scene.Camera");
        }
        value = _ch.Channel?.Object as CameraSettings;
        channel = _ch.Channel;
    }

    public void Dispose() => _ch.Dispose();
}
```

### Leaf Parameter Node (reads a typed value)

Same pattern as hierarchy node, but the output type is a standard leaf value like `float`, `bool`, or `string`.

### Indexed Spread Element Node (takes `int index`)

```csharp
[ProcessNode]
public class SceneItemAccessor : IDisposable
{
    private PublicChannelHelper _ch = new();
    private int _boundIndex = -1;

    public void Update(out SceneItem? value, out IChannel<object>? channel, int index = 0)
    {
        // Rebind when index changes
        if (index != _boundIndex)
        {
            _ch.Dispose();
            _ch = new();
            _boundIndex = index;
        }
        if (!_ch.IsBound)
        {
            var hub = IChannelHub.HubForApp;
            if (hub != null) _ch.TryBind(hub, $"App.Effects[{index}]");
        }
        value = _ch.Channel?.Object as SceneItem;
        channel = _ch.Channel;
    }

    public void Dispose() => _ch.Dispose();
}
```

## Reactive Subscriptions

Subscribe to channel value changes using the standard `IObservable` pattern:

```csharp
IChannel<object>? ch = hub.TryGetChannel("Settings.Audio.Volume");
if (ch != null)
{
    IDisposable subscription = ch.Subscribe(new CallbackObserver(value =>
    {
        // Called whenever the channel value changes
        if (value is float f)
            ApplyVolume(f);
    }));

    // ALWAYS dispose when done (in node's Dispose method)
}
```

## Bang Channels

For trigger/event properties (delete, insert, move operations), use `System.Reactive.Unit` — NOT float:

```csharp
using System.Reactive;

[CanBePublished(true)]
public class MyInstance
{
    public Unit DeleteInstance { get; set; }     // Bang channel
    public Unit InsertAfterInstance { get; set; } // Bang channel
}
```

The **event IS the bang** — the value is irrelevant. Subscribe and act on the callback:

```csharp
var ch = hub.TryGetChannel("Project.Items[0].DeleteInstance");
ch?.Subscribe(new BangObserver(() =>
{
    // Triggered when the bang fires — queue the action
    _pendingDeletions.Add(0);
}));
```

`Unit` channels show as "Unit" type in vvvv's node browser, not "Float".

## Hierarchical Data Propagation

vvvv's channel system automatically propagates changes through the hierarchy:

- **Write a root record** to its channel → all child channels auto-update
- **Write a leaf channel** → parent channels auto-update
- This is built into vvvv's SubChannel system — no manual propagation needed

This enables efficient bulk operations:

```csharp
// Save: read the root channel → serialize the entire hierarchy
var model = rootChannel.Object as AppModel;
string json = JsonSerializer.Serialize(model);

// Load: deserialize → write to root channel → ALL children update
var loaded = JsonSerializer.Deserialize<AppModel>(json);
rootChannel.Object = loaded;  // Every sub-channel updates automatically
```

## Spread Channels and Sub-Channels

When a `Spread<T>` property is published (where `T` has `[CanBePublished(true)]`), vvvv automatically creates sub-channels for each element:

```
Project.Items           → Spread<ItemModel>
Project.Items[0]        → ItemModel (auto-created)
Project.Items[0].Name   → string (auto-created)
Project.Items[1].Name   → string (auto-created)
```

**Setting the spread channel propagates to all sub-channels automatically.** No need to update individual sub-channels.

When modifying a spread (add/remove/reorder elements):

```csharp
// Build new spread
var newSpread = modifiedList.ToArray().AsSpreadUnsafe();

// Set on spread channel — sub-channels update automatically
spreadChannel.Object = newSpread;
```

**Warning**: `Spread.AsSpreadUnsafe(array)` wraps without copying — the array must NOT be mutated after.

**Feedback loop prevention**: When writing to a channel you're also subscribed to, use a suppression flag:

```csharp
_suppressCallback = true;
_channel.Object = newValue;
_suppressCallback = false;

// In the subscription callback:
void OnChanged(object? value)
{
    if (_suppressCallback) return;
    // Process the change...
}
```

## Critical Rules

1. **NEVER `TryAddChannel`** — only use `TryGetChannel` (lookup-only)
2. **Always retry-bind** — channels appear after model initialization, not immediately
3. **`[CanBePublished(true)]` required** on .NET types for channel publication
4. **Always dispose subscriptions** — in the node's `Dispose()` method
5. **`System.Reactive.Unit` for bangs** — not `float` or `bool`
6. **`Spread.AsSpreadUnsafe`** — array must not be mutated after wrapping
7. **Suppression flags** — prevent feedback loops when writing to subscribed channels

For code examples, see [examples.md](examples.md).
