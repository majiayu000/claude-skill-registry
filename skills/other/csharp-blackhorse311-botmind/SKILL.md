---
name: csharp
description: |
  Manages C# syntax, patterns, and language features for .NET projects
  Use when: Writing C# code, implementing BigBrain layers, creating BepInEx plugins, handling Unity interop, or working with EFT APIs
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# C# Skill

C# patterns for SPT mod development targeting .NET Standard 2.1 (client) and .NET 9 (server). This codebase uses C# 12 features with Unity interop, BigBrain AI framework integration, and BepInEx plugin architecture. Focus areas: state machines, reflection-based interop, thread safety, and defensive coding for game mod stability.

## Quick Start

### BigBrain Layer Pattern

```csharp
public class LootingLayer : CustomLayer
{
    public override string GetName() => "LootingLayer";
    
    public override bool IsActive()
    {
        try
        {
            if (BotOwner?.IsDead == true) return false;
            return SAINInterop.CanBotQuest(BotOwner, BotOwner.Position, 50f);
        }
        catch (Exception ex)
        {
            BotMindPlugin.Log?.LogError($"[{BotOwner?.name ?? "Unknown"}] IsActive error: {ex.Message}");
            return false; // Fail safe
        }
    }
}
```

### Null-Conditional Navigation

```csharp
// GOOD - Defensive null handling for game objects
var health = player?.ActiveHealthController?.GetBodyPartHealth(EBodyPart.Head)?.Current ?? 0f;

// BAD - Crashes if any part is null
var health = player.ActiveHealthController.GetBodyPartHealth(EBodyPart.Head).Current;
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `volatile` | Singleton instances | `private static volatile MedicBuddyController _instance;` |
| `lock` | Shared mutable state | `lock (_teamLock) { _team.Add(bot); }` |
| `Interlocked` | Atomic counters | `Interlocked.Increment(ref _spawnCount);` |
| Pattern matching | Type checks | `if (target is LootableContainer container)` |
| Null-conditional | Safe navigation | `BotOwner?.Mover?.GoToPoint(pos)` |

## Common Patterns

### Try-Catch Wrapper for Unity Callbacks

**When:** Any method called by Unity or BigBrain framework

```csharp
public override void Update(ActionData data)
{
    try
    {
        // Implementation that may throw
        ProcessLootTarget();
    }
    catch (Exception ex)
    {
        BotMindPlugin.Log?.LogError($"Update error: {ex.Message}\n{ex.StackTrace}");
        // Return to safe state, don't propagate
    }
}
```

### Reflection-Based Soft Dependency

**When:** Optional mod integration (SAIN)

```csharp
private static readonly Type? _sainType;
private static readonly MethodInfo? _canBotQuestMethod;

static SAINInterop()
{
    _sainType = Type.GetType("SAIN.SAINPlugin, SAIN");
    _canBotQuestMethod = _sainType?.GetMethod("CanBotQuest", BindingFlags.Public | BindingFlags.Static);
}
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **dotnet** skill for build configuration and project setup
- See the **bepinex** skill for plugin lifecycle and configuration
- See the **harmony** skill for runtime patching
- See the **xunit** skill for unit testing patterns
- See the **unity** skill for game object and component patterns