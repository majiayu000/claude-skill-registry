---
name: normcore
description: Normcore multiplayer networking — Realtime API, Room/Datastore, RealtimeModel, ownership, WebGL, and operational patterns
---

# Normcore Multiplayer Networking

Comprehensive reference for Normcore 3 real-time multiplayer networking in Unity. Covers the full API surface, patterns, and WebGL platform specifics.

**Docs**: https://docs.normcore.io/

## When to Use This Skill

- Implementing multiplayer synchronisation with Normcore
- Creating RealtimeModels for custom data sync
- Setting up player controllers, ownership, physics networking
- Configuring rooms, regions, quickmatch
- Building for **WebGL** (this project's primary target)
- Debugging connection, ownership, or sync issues

## Core Concepts

| Concept                    | Purpose                                                                                                     |
| -------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Realtime**               | Connection manager. Lives in scene. Connects to rooms, manages RealtimeViews.                               |
| **RealtimeView**           | Identity for synced GameObjects. Creates models for each RealtimeComponent.                                 |
| **RealtimeComponent\<T\>** | Syncs scene state ↔ RealtimeModel in datastore. Override `OnRealtimeModelReplaced()`.                       |
| **RealtimeTransform**      | Built-in component for position/rotation/scale sync. Handles rigidbody ownership.                           |
| **RealtimeModel**          | Data container synced across all clients. `[RealtimeModel]` partial class with `[RealtimeProperty]` fields. |
| **Room**                   | Lower-level connection + datastore manager. Realtime wraps this.                                            |
| **Ownership**              | Server-enforced. `ownerID` on models. Cascades parent → children.                                           |
| **EasySync**               | Zero-code sync for scene objects. Converts to RealtimeComponent when needed.                                |

## Architecture Layers

```
Realtime API  →  Bridges Unity scene ↔ datastore (most devs work here)
Room + Datastore API  →  Raw state sync, platform-independent
Transport  →  UDP with fallback, congestion control
```

MVC pattern: **Model** = RealtimeModel in datastore, **View** = GameObjects, **Controller** = RealtimeComponent scripts.

## Supported Primitives (RealtimeModel Fields)

**C#**: `bool`, `byte`, `sbyte`, `short`, `ushort`, `int`, `uint`, `long`, `ulong`, `float`, `double`, `string`, `byte[]`

**Unity**: `Color`, `Vector2`, `Vector3`, `Vector4`, `Quaternion`

**Collections**: `RealtimeArray`, `RealtimeSet`, `RealtimeDictionary`, `StringKeyDictionary`

**Nested models** supported — one RealtimeModel can contain another.

## Quick Patterns

### Player Spawner

```csharp
using Normal.Realtime;

public class PlayerSpawner : MonoBehaviour
{
    private Realtime _realtime;

    void Awake()
    {
        _realtime = GetComponent<Realtime>();
        _realtime.didConnectToRoom += DidConnectToRoom;
    }

    void DidConnectToRoom(Realtime realtime)
    {
        Realtime.Instantiate("Player", Vector3.zero, Quaternion.identity,
            new Realtime.InstantiateOptions {
                ownedByClient            = true,
                preventOwnershipTakeover = true,
                useInstance              = realtime
            });
    }
}
```

### Ownership Guard

```csharp
void Update()
{
    if (!_realtimeView.isOwnedLocallyInHierarchy) return;
    // Local player input here
}
```

### Custom Data Sync (Minimal)

```csharp
[RealtimeModel]
public partial class ScoreModel {
    [RealtimeProperty(1, true, true)] private int _score;
}

public class ScoreSync : RealtimeComponent<ScoreModel> {
    protected override void OnRealtimeModelReplaced(ScoreModel prev, ScoreModel cur) {
        if (prev != null) prev.scoreDidChange -= OnScoreChanged;
        if (cur  != null) cur.scoreDidChange  += OnScoreChanged;
    }
    void OnScoreChanged(ScoreModel m, int score) { /* update UI */ }
    public void AddScore(int amount) { model.score += amount; }
}
```

## Decision Tree

| Need                              | Use                                            |
| --------------------------------- | ---------------------------------------------- |
| Sync a few public fields, no code | **EasySync**                                   |
| Sync custom data with events      | **RealtimeComponent\<T\>** + **RealtimeModel** |
| Sync position/rotation            | **RealtimeTransform**                          |
| Sync animator params              | **RealtimeAnimator**                           |
| Dynamic runtime collections       | **RealtimeSet** / **RealtimeDictionary**       |
| Full control over connection      | **Room + Datastore API** directly              |

## WebGL Callouts

- **No code changes** needed for WebGL builds — Normcore works out of the box
- **Voice chat spatialisation does NOT work** on web (FMOD not supported). Audio routes through browser directly.
- **Region pinging unavailable** in WebGL — use GeoIP distance fallback from `GetRegionsListAsync()`
- **HTTPS required** for production deployment with valid cert, WASM + gzip content headers
- **Cross-platform**: WebGL clients can connect to native clients in the same room
- See [references/webgl-platform.md](references/webgl-platform.md) for full details

## Prefab Requirements

Runtime-spawned objects **must** be in `Assets/Resources/` (or use Addressables / custom `RealtimePrefabLoadDelegate`):

```
Assets/Resources/
├── Player.prefab        ← RealtimeView on root
├── Projectile.prefab
└── NetworkedPickup.prefab
```

## References

- [Realtime API](references/realtime-api.md) — Realtime, RealtimeView, RealtimeComponent, RealtimeTransform
- [Room + Datastore API](references/room-datastore-api.md) — Room, Datastore, RealtimeModel, collections, ownership
- [Synchronising Custom Data](references/synchronising-custom-data.md) — Full model/component guide
- [Networking Patterns](references/networking-patterns.md) — Player controllers, physics, RPC events, prefab pooling
- [WebGL Platform](references/webgl-platform.md) — WebGL config, limitations, React integration
- [Configuration & Ops](references/configuration-and-ops.md) — Regions, quickmatch, disconnect events, auto-reconnect
