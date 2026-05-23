---
name: SND YesAlready Integration
description: Use this skill when implementing automatic dialog confirmation or UI automation in SND macros using the YesAlready plugin. Covers plugin control, feature management, and temporary pausing.
---

# YesAlready Integration for SND

This skill covers integration with the YesAlready plugin for automatic dialog and UI interaction in SND macros.

> **Source:** https://github.com/PunishXIV/YesAlready/blob/master/YesAlready/IPC/YesAlreadyIPC.cs

## Prerequisites

```lua
-- Always check plugin availability first
if not HasPlugin("YesAlready") then
    yield("/echo [Script] YesAlready plugin not available")
    return
end
```

## IPC API Reference

### Plugin Control Functions
```lua
-- Check if the plugin is enabled
IPC.YesAlready.IsPluginEnabled() → boolean

-- Enable or disable the plugin
IPC.YesAlready.SetPluginEnabled(boolean state) → nil

-- Temporarily pause the plugin for specified milliseconds
IPC.YesAlready.PausePlugin(number milliseconds) → nil
```

### Feature (Bother) Control Functions
```lua
-- Check if a specific feature/bother is enabled
-- name: Full type name of the feature (e.g., "YesAlready.Features.AddonMasterPieceSupplyFeature")
IPC.YesAlready.IsBotherEnabled(string name) → boolean

-- Enable or disable a specific feature/bother
IPC.YesAlready.SetBotherEnabled(string name, boolean state) → nil

-- Temporarily pause a specific feature/bother for specified milliseconds
-- Returns true if the feature was paused, false if not found or not enabled
IPC.YesAlready.PauseBother(string name, number milliseconds) → boolean
```

## Usage Patterns

### Check Plugin State
```lua
function IsYesAlreadyActive()
    if not HasPlugin("YesAlready") then
        return false
    end

    local ok, result = pcall(function()
        return IPC.YesAlready.IsPluginEnabled()
    end)

    return ok and result
end
```

### Enable/Disable Plugin
```lua
function SetYesAlreadyState(enabled)
    if not HasPlugin("YesAlready") then
        return false
    end

    pcall(function()
        IPC.YesAlready.SetPluginEnabled(enabled)
    end)
    return true
end

-- Usage
SetYesAlreadyState(true)   -- Enable
SetYesAlreadyState(false)  -- Disable
```

### Temporarily Pause Plugin
```lua
function PauseYesAlreadyFor(milliseconds)
    if not HasPlugin("YesAlready") then
        return false
    end

    pcall(function()
        IPC.YesAlready.PausePlugin(milliseconds)
    end)
    return true
end

-- Pause for 5 seconds
PauseYesAlreadyFor(5000)
```

### Control Specific Features
```lua
function EnableSpecificFeature(featureName, enabled)
    if not HasPlugin("YesAlready") then
        return false
    end

    pcall(function()
        IPC.YesAlready.SetBotherEnabled(featureName, enabled)
    end)
    return true
end

-- Example: Disable a specific feature temporarily
local featureName = "YesAlready.Features.AddonMasterPieceSupplyFeature"
EnableSpecificFeature(featureName, false)
-- Do something
EnableSpecificFeature(featureName, true)
```

### Pause Specific Feature
```lua
function PauseFeatureFor(featureName, milliseconds)
    if not HasPlugin("YesAlready") then
        return false
    end

    local ok, result = pcall(function()
        return IPC.YesAlready.PauseBother(featureName, milliseconds)
    end)

    return ok and result
end

-- Pause a specific feature for 3 seconds
local success = PauseFeatureFor("YesAlready.Features.SomeFeature", 3000)
if success then
    yield("/echo Feature paused successfully")
end
```

## Common Use Cases

### Temporarily Disable During Sensitive Operations
```lua
-- Disable YesAlready during manual interactions
IPC.YesAlready.SetPluginEnabled(false)
-- Perform manual operations
-- ...
IPC.YesAlready.SetPluginEnabled(true)
```

### Pause During Specific Actions
```lua
-- Pause YesAlready while performing a specific action that needs different handling
function PerformSensitiveAction()
    IPC.YesAlready.PausePlugin(10000)  -- Pause for 10 seconds
    -- Perform action that needs different dialog handling
    yield("/echo Performing sensitive action...")
    -- YesAlready will automatically re-enable after 10 seconds
end
```

### Feature-Specific Control
```lua
-- Disable only a specific YesAlready feature for a task
local feature = "YesAlready.Features.AddonSelectYesnoFeature"
IPC.YesAlready.SetBotherEnabled(feature, false)
-- Perform task where this specific confirmation should not be auto-clicked
-- ...
IPC.YesAlready.SetBotherEnabled(feature, true)
```

## Integration with Other Plugins

YesAlready works well alongside:
- **TextAdvance** - for cutscene/dialog skipping
- **Artisan** - for crafting confirmations
- **AutoRetainer** - for retainer dialog confirmations
- **Deliveroo** - for GC turn-in confirmations

## Best Practices

1. **Configure YesAlready rules in the plugin UI** - The IPC only controls enabling/disabling, not rule configuration
2. **Use PausePlugin for temporary disabling** - Automatically re-enables after the specified time
3. **Check IsPluginEnabled before assuming it's active** - Scripts may run when YesAlready is disabled
4. **Use feature-specific control when possible** - Allows finer control over which dialogs are auto-confirmed
5. **Test with YesAlready disabled first** - Ensure your script handles dialogs gracefully when YesAlready is not active

## Important Notes

- **YesAlready does not provide IPC for dialog interaction** - It works automatically based on its configured rules
- **The IPC is for control only** - You cannot use IPC to click specific buttons or enter values
- **Feature names must be fully qualified** - Use complete type names like "YesAlready.Features.FeatureName"
- **PauseBother returns false if the feature is not found or not enabled** - Check the return value for confirmation
