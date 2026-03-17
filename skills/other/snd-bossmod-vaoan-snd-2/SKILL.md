---
name: SND BossModReborn Integration
description: Use this skill when implementing combat automation in SND macros using the BossModReborn plugin. Covers preset management, rotation configuration, and AI control via chat commands.
---

# BossModReborn Integration for SND

This skill covers integration with the BossModReborn plugin for combat automation in SND macros. BossMod provides boss mechanics automation, rotation management through presets, and AI control.

> **Source:** https://github.com/awgil/ffxiv_bossmod/blob/master/BossMod/Framework/IPCProvider.cs

## Prerequisites

```lua
-- Always check plugin availability first
if not HasPlugin("BossModReborn") then
    yield("/echo [Script] BossModReborn plugin not available")
    return
end
```

## IPC API Reference

All IPC methods are prefixed with `BossMod.` in the actual IPC calls, but accessed through `IPC.BossModReborn.*` in SND.

### Module Detection
```lua
-- Check if a module exists for a given data ID
IPC.BossModReborn.HasModuleByDataId(dataId) → boolean
-- Example: IPC.BossModReborn.HasModuleByDataId(12345)
```

### Configuration Management
```lua
-- Execute a configuration command
IPC.BossModReborn.Configuration(args, save) → varies
-- args: table of strings representing command arguments
-- save: boolean, whether to save the configuration
-- Example: IPC.BossModReborn.Configuration({"some", "command"}, true)

-- Get last modification time of configuration
IPC.BossModReborn.ConfigurationLastModified() → DateTime
```

### Action Queue
```lua
-- Check if rotation has any non-manual actions queued
IPC.BossModReborn.RotationActionQueueHasEntries() → boolean
```

### Preset Management
```lua
-- Get a preset by name (returns JSON string)
IPC.BossModReborn.PresetsGet(name) → string?
-- Example: local json = IPC.BossModReborn.PresetsGet("My Preset")

-- Create or update a preset from JSON
IPC.BossModReborn.PresetsCreate(presetJson, overwrite) → boolean
-- presetJson: JSON string representing the preset
-- overwrite: boolean, whether to overwrite existing preset

-- Delete a preset by name
IPC.BossModReborn.PresetsDelete(name) → boolean

-- Get the currently active preset name (single preset mode)
IPC.BossModReborn.PresetsGetActive() → string?

-- Set a single preset as active
IPC.BossModReborn.PresetsSetActive(name) → boolean

-- Clear the active preset
IPC.BossModReborn.PresetsClearActive() → boolean

-- Check if presets are force-disabled
IPC.BossModReborn.PresetsGetForceDisabled() → boolean

-- Force-disable presets
IPC.BossModReborn.PresetsSetForceDisabled() → boolean

-- Activate a preset (multi-preset mode)
IPC.BossModReborn.PresetsActivate(name) → boolean

-- Deactivate a preset (multi-preset mode)
IPC.BossModReborn.PresetsDeactivate(name) → boolean

-- Get list of all active preset names
IPC.BossModReborn.PresetsGetActiveList() → table

-- Set multiple presets as active at once
IPC.BossModReborn.PresetsSetActiveList(names) → boolean
-- names: table of preset name strings
```

### Transient Strategy Management
```lua
-- Add a transient strategy override to a preset
IPC.BossModReborn.PresetsAddTransientStrategy(presetName, moduleTypeName, trackName, value) → boolean

-- Add a transient strategy targeting a specific enemy OID
IPC.BossModReborn.PresetsAddTransientStrategyTargetEnemyOID(presetName, moduleTypeName, trackName, value, oid) → boolean

-- Clear a specific transient strategy
IPC.BossModReborn.PresetsClearTransientStrategy(presetName, moduleTypeName, trackName) → boolean

-- Clear all transient strategies for a module
IPC.BossModReborn.PresetsClearTransientModuleStrategies(presetName, moduleTypeName) → boolean

-- Clear all transient strategies for a preset
IPC.BossModReborn.PresetsClearTransientPresetStrategies(presetName) → boolean
```

## Chat Commands

```lua
-- Enable BossMod AI
yield("/bmai on")

-- Disable BossMod AI
yield("/bmai off")

-- Toggle BossMod AI
yield("/bmai toggle")
```

## Usage Patterns

### Check if Module Available for Enemy
```lua
function HasBossModule(enemyDataId)
    if not HasPlugin("BossModReborn") then
        return false
    end
    local ok, result = pcall(function()
        return IPC.BossModReborn.HasModuleByDataId(enemyDataId)
    end)
    return ok and result
end
```

### Manage Active Presets
```lua
-- Activate a preset for combat
function ActivatePreset(presetName)
    if not HasPlugin("BossModReborn") then
        return false
    end

    local ok, result = pcall(function()
        return IPC.BossModReborn.PresetsSetActive(presetName)
    end)

    if ok and result then
        yield("/echo [Script] Activated BossMod preset: " .. presetName)
        return true
    else
        yield("/echo [Script] Failed to activate preset: " .. presetName)
        return false
    end
end

-- Get currently active preset
function GetActivePreset()
    if not HasPlugin("BossModReborn") then
        return nil
    end

    local ok, result = pcall(function()
        return IPC.BossModReborn.PresetsGetActive()
    end)

    return ok and result or nil
end

-- Clear active preset
function ClearActivePreset()
    if not HasPlugin("BossModReborn") then
        return false
    end

    local ok, result = pcall(function()
        return IPC.BossModReborn.PresetsClearActive()
    end)

    return ok and result
end
```

### Multi-Preset Mode
```lua
-- Activate multiple presets at once
function SetActivePresets(presetNames)
    if not HasPlugin("BossModReborn") then
        return false
    end

    local ok, result = pcall(function()
        return IPC.BossModReborn.PresetsSetActiveList(presetNames)
    end)

    if ok and result then
        yield("/echo [Script] Activated " .. #presetNames .. " presets")
        return true
    end
    return false
end

-- Example: activate multiple presets
SetActivePresets({"Tank Preset", "Defensive Preset"})
```

### Combat Control with AI Commands
```lua
function EnableCombatAI()
    yield("/bmai on")
    yield("/wait 0.5")
end

function DisableCombatAI()
    yield("/bmai off")
    yield("/wait 0.5")
end

function ToggleCombatAI()
    yield("/bmai toggle")
    yield("/wait 0.5")
end
```

### Check Action Queue
```lua
-- Check if rotation is actively queuing actions
function IsRotationActive()
    if not HasPlugin("BossModReborn") then
        return false
    end

    local ok, result = pcall(function()
        return IPC.BossModReborn.RotationActionQueueHasEntries()
    end)

    return ok and result
end
```

## Integration Examples

### Switch Presets Based on Content
```lua
function LoadPresetForContent()
    local zoneId = Svc.ClientState.TerritoryType

    -- Example: Different presets for different content
    if zoneId == 123 then
        ActivatePreset("Dungeon Tank")
    elseif zoneId == 456 then
        ActivatePreset("Raid DPS")
    else
        ActivatePreset("Default")
    end
end
```

### Cleanup After Combat
```lua
function CleanupAfterCombat()
    -- Disable AI
    DisableCombatAI()

    -- Clear any active presets
    ClearActivePreset()

    -- Clear transient strategies
    local activePresets = IPC.BossModReborn.PresetsGetActiveList()
    for _, presetName in ipairs(activePresets) do
        IPC.BossModReborn.PresetsClearTransientPresetStrategies(presetName)
    end
end
```

## Best Practices

1. **Always check plugin availability** before making IPC calls
2. **Use pcall** to safely handle IPC failures
3. **Clear active presets** when done to avoid conflicts
4. **Check HasModuleByDataId** before expecting boss automation
5. **Clean up transient strategies** after encounters to avoid stale overrides
