---
name: bepinex
description: |
  Develops BepInEx plugins with hooks, patches, and mod initialization for Unity games.
  Use when: Creating BepInEx plugins, setting up plugin entry points, configuring mod settings, or integrating with Harmony patches.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# BepInEx Skill

BepInEx is the plugin framework for Unity game modding. This project uses BepInEx 5.x with .NET Standard 2.1 for SPT (Single Player Tarkov) modding. Plugins are loaded via `[BepInPlugin]` attributes and use `ConfigFile` for settings. All patches use **Harmony** (see the **harmony** skill).

## Quick Start

### Plugin Entry Point

```csharp
[BepInPlugin("com.blackhorse311.botmind", "BotMind", "1.0.0")]
[BepInDependency("xyz.drakia.bigbrain", BepInDependency.DependencyFlags.HardDependency)]
[BepInDependency("me.sol.sain", BepInDependency.DependencyFlags.SoftDependency)]
public class BotMindPlugin : BaseUnityPlugin
{
    public static ManualLogSource Log { get; private set; }
    
    private void Awake()
    {
        Log = Logger;
        Log.LogInfo("BotMind is loading...");
        
        // Initialize configuration
        BotMindConfig.Initialize(Config);
        
        // Apply Harmony patches
        new Harmony("com.blackhorse311.botmind").PatchAll();
        
        Log.LogInfo("BotMind loaded successfully!");
    }
}
```

### Configuration Binding

```csharp
public static class BotMindConfig
{
    public static ConfigEntry<bool> EnableLooting { get; private set; }
    public static ConfigEntry<float> SearchRadius { get; private set; }
    
    public static void Initialize(ConfigFile config)
    {
        EnableLooting = config.Bind(
            "General",           // Section
            "Enable Looting",    // Key
            true,                // Default
            "Enable bot looting behavior"  // Description
        );
        
        SearchRadius = config.Bind(
            "Looting",
            "Search Radius",
            50f,
            new ConfigDescription(
                "Loot search distance in meters",
                new AcceptableValueRange<float>(10f, 200f)
            )
        );
    }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Plugin GUID | Unique identifier | `"com.author.modname"` |
| Hard dependency | Required mod | `DependencyFlags.HardDependency` |
| Soft dependency | Optional mod | `DependencyFlags.SoftDependency` |
| ConfigEntry | Runtime setting | `config.Bind("Section", "Key", default)` |
| ManualLogSource | Logging | `Logger.LogInfo("message")` |

## Common Patterns

### Soft Dependency Check

**When:** Integrating with optional mods like SAIN

```csharp
private static bool _sainChecked;
private static bool _sainAvailable;

public static bool IsSAINAvailable()
{
    if (!_sainChecked)
    {
        _sainAvailable = Chainloader.PluginInfos.ContainsKey("me.sol.sain");
        _sainChecked = true;
    }
    return _sainAvailable;
}
```

### Lifecycle Hooks

**When:** Responding to game events

```csharp
private void Awake()    // Plugin load - register patches, config
private void Start()    // After all plugins loaded
private void OnEnable() // Plugin enabled
private void OnDisable() // Plugin disabled
private void OnDestroy() // Cleanup resources
```

## See Also

- [patterns](references/patterns.md) - Plugin structure, config, logging
- [workflows](references/workflows.md) - Build, deploy, debug

## Related Skills

- **harmony** - Patching game methods
- **csharp** - Language patterns
- **unity** - MonoBehaviour lifecycle
- **dotnet** - Build and project configuration