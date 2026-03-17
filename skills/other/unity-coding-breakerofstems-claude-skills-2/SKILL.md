---
name: unity-coding
description: Implement gameplay and system code following Unity conventions
---

# Unity Coding Skill

Write Unity C# code safely following best practices and conventions.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Implement gameplay and system code changes that work in both Editor and headless/server contexts.

## Code Style Rules

### Namespaces

Always use namespaces matching folder structure:
```csharp
// File: Assets/Scripts/Player/Movement/PlayerController.cs
namespace MyGame.Player.Movement
{
    public class PlayerController : MonoBehaviour
    {
    }
}
```

### Assembly Definitions (asmdef)

- Each major feature should have its own `.asmdef`
- Reference other assemblies explicitly
- Keeps compile times fast and dependencies clear

```
Assets/
  Scripts/
    Core/
      Core.asmdef           # Core utilities
    Player/
      Player.asmdef         # References: Core
    Networking/
      Networking.asmdef     # References: Core
```

### Folder Layout

```
Assets/
  Scripts/
    Core/           # Utilities, extensions, base classes
    Player/         # Player-specific code
    Enemies/        # Enemy AI and behavior
    UI/             # UI controllers (not MonoBehaviours when possible)
    Networking/     # Netcode, server logic
    Data/           # ScriptableObjects, data containers
  Prefabs/
  Scenes/
  Resources/        # Use sparingly
  StreamingAssets/
```

## Editor vs Runtime Code

### No Editor-Time Side Effects

Code in `Assets/Scripts/` should never:
- Use `#if UNITY_EDITOR` for runtime logic
- Access `UnityEditor` namespace in runtime code
- Modify assets at runtime expecting Editor serialization

Editor-only code goes in:
```
Assets/
  Editor/
    MyEditorTools.cs    # UnityEditor namespace OK here
```

### Headless-Friendly Code

For server/headless builds, avoid:
```csharp
// BAD - crashes in headless
Camera.main.transform.position

// GOOD - null-safe
if (Camera.main != null)
    Camera.main.transform.position
```

Check for headless mode:
```csharp
if (SystemInfo.graphicsDeviceType == GraphicsDeviceType.Null)
{
    // Running headless
}
```

## ScriptableObjects vs MonoBehaviours

### Use ScriptableObjects For:

- Configuration data
- Shared state between scenes
- Event channels
- Asset references

```csharp
[CreateAssetMenu(fileName = "GameConfig", menuName = "Config/GameConfig")]
public class GameConfig : ScriptableObject
{
    public float playerSpeed = 5f;
    public int maxHealth = 100;
}
```

### Use MonoBehaviours For:

- Scene-specific behavior
- Components that need Update/FixedUpdate
- Physics interactions
- Visual/audio feedback

## Deterministic Server Code

For multiplayer/server authority:

```csharp
// Use FixedUpdate for deterministic physics
void FixedUpdate()
{
    // Physics logic here
}

// Avoid Time.deltaTime in gameplay logic
// Use Time.fixedDeltaTime or fixed tick rates

// Avoid Random.Range for gameplay - use seeded random
private System.Random _seededRandom;
```

## Allowed Tools

- `dotnet` CLI (if using .NET tools)
- `git`, `gh`
- Text editors
- No GUI assumptions

## Patterns

### Dependency Injection (Simple)

```csharp
public class PlayerController : MonoBehaviour
{
    [SerializeField] private GameConfig _config;
    [SerializeField] private InputReader _inputReader;

    // Dependencies injected via Inspector
}
```

### Event-Driven Architecture

```csharp
// Event channel (ScriptableObject)
[CreateAssetMenu(menuName = "Events/Void Event")]
public class VoidEventChannel : ScriptableObject
{
    public event System.Action OnEventRaised;
    public void RaiseEvent() => OnEventRaised?.Invoke();
}
```

## Policies

- Follow existing project conventions first
- Prefer composition over inheritance
- Keep MonoBehaviours thin - delegate to plain C# classes
- No magic strings - use constants or enums
- Null-check external references (Camera.main, etc.)
