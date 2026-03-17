---
name: harmony
description: |
  Creates Harmony patches for method interception and runtime modification in BepInEx plugins.
  Use when: intercepting EFT game methods, modifying bot behavior, hooking into game lifecycle events, or patching third-party mod methods.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Harmony Skill

Harmony is the runtime patching library used by BepInEx to intercept and modify game methods without touching original assemblies. In BotMind, Harmony patches are used to hook into EFT's game lifecycle (raid start/end), bot spawning events, and player interactions. All patches live in `src/client/Patches/` and are auto-applied via `Harmony.PatchAll()` in `BotMindPlugin.cs`.

## Quick Start

### Prefix Patch (Run Before Original)

```csharp
[HarmonyPatch(typeof(GameWorld), nameof(GameWorld.OnGameStarted))]
internal static class GameStartedPatch
{
    [HarmonyPrefix]
    private static void Prefix()
    {
        try
        {
            MedicBuddyController.Instance?.OnRaidStarted();
            BotMindPlugin.Log?.LogInfo("Raid started - modules initialized");
        }
        catch (Exception ex)
        {
            BotMindPlugin.Log?.LogError($"GameStartedPatch error: {ex.Message}");
        }
    }
}
```

### Postfix Patch (Run After Original)

```csharp
[HarmonyPatch(typeof(GameWorld), "Dispose")]
internal static class GameWorldDisposePatch
{
    [HarmonyPostfix]
    private static void Postfix()
    {
        MedicBuddyController.Instance?.OnRaidEnded();
        LootFinder.ClearCache();
    }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `[HarmonyPatch]` | Declares target method | `[HarmonyPatch(typeof(BotOwner), "Update")]` |
| `[HarmonyPrefix]` | Runs before original, can skip | Return `false` to skip original |
| `[HarmonyPostfix]` | Runs after original | Access `__result` to modify return |
| `[HarmonyTranspiler]` | IL-level modification | Inject/remove instructions |
| `__instance` | Reference to patched object | `BotOwner __instance` |
| `__result` | Return value (postfix only) | `ref bool __result` |

## Common Patterns

### Conditional Execution with Prefix

**When:** Skip original method based on custom logic

```csharp
[HarmonyPrefix]
private static bool Prefix(BotOwner __instance)
{
    // Skip original if MedicBuddy bot
    if (MedicBuddyController.IsMedicBuddyBot(__instance))
        return false; // Don't run original
    
    return true; // Run original
}
```

### Modifying Return Values

**When:** Change what a method returns without rewriting it

```csharp
[HarmonyPostfix]
private static void Postfix(ref bool __result, BotOwner __instance)
{
    // Force bots to always consider looting safe
    if (BotMindConfig.ForceEnableLooting.Value)
        __result = true;
}
```

### Accessing Private Fields

**When:** Read/write private state from patched class

```csharp
[HarmonyPostfix]
private static void Postfix(BotOwner __instance)
{
    var privateField = Traverse.Create(__instance)
        .Field("_internalState")
        .GetValue<BotState>();
}
```

## See Also

- [patterns](references/patterns.md) - Patch types, parameter injection, error handling
- [workflows](references/workflows.md) - Creating patches, debugging, testing

## Related Skills

- See the **bepinex** skill for plugin lifecycle and when patches are applied
- See the **csharp** skill for reflection patterns used with Traverse
- See the **unity** skill for MonoBehaviour lifecycle hooks that complement patches