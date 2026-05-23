---
name: SND Ice
description: Use this skill when implementing Cosmic Exploration automation in SND macros using the Ice plugin. Covers starting/stopping Ice, IPC API, and integration with leveling workflows.
---

# Ice Plugin (Cosmic Exploration)

> **Source:** https://github.com/LeontopodiumNivale14/Ices-Cosmic-Exploration/blob/Main-Branch/ICE/IPC/IceCosmicExplorationIPC.cs

Ice is a plugin for automating Cosmic Exploration content in FFXIV. It handles mission selection, gathering, and grinding for Cosmic/Lunar credits.

## IPC API Reference

The Ice plugin provides a comprehensive IPC API for programmatic control:

```lua
-- Check if Ice is running
local running = IPC.Ice.IsRunning()  -- Returns bool

-- Enable/disable Ice automation
IPC.Ice.Enable()   -- Start Ice
IPC.Ice.Disable()  -- Stop Ice

-- Get current state (returns string: "Idle", "Running", etc.)
local state = IPC.Ice.CurrentState()

-- Get current mission ID being run
local missionId = IPC.Ice.CurrentMission()  -- Returns uint

-- Mission Management
-- Add missions to the enabled list (takes HashSet<uint>)
IPC.Ice.AddMissions({1, 2, 3})

-- Remove missions from the enabled list
IPC.Ice.RemoveMissions({4, 5, 6})

-- Toggle mission states
IPC.Ice.ToggleMissions({1, 2})

-- Enable ONLY these missions (disables all others)
IPC.Ice.OnlyMissions({7, 8, 9})

-- Clear all enabled missions
IPC.Ice.ClearAllMissions()

-- Flag a mission area on the map (opens map and shows gathering radius)
IPC.Ice.FlagMissionArea(missionId)

-- Settings Management
-- Change boolean settings (valid configs below)
IPC.Ice.ChangeSetting("OnlyGrabMission", true)
IPC.Ice.ChangeSetting("StopAfterCurrent", false)
IPC.Ice.ChangeSetting("StopOnceHitCosmoCredits", true)
IPC.Ice.ChangeSetting("StopOnceHitLunarCredits", true)
IPC.Ice.ChangeSetting("XPRelicGrind", false)

-- Change numeric settings
IPC.Ice.ChangeSettingAmount("CosmoCreditsCap", 5000)
IPC.Ice.ChangeSettingAmount("LunarCreditsCap", 3000)
```

### Available Boolean Settings

| Setting | Description |
|---------|-------------|
| `OnlyGrabMission` | Only grab missions without completing them |
| `StopAfterCurrent` | Stop after completing the current mission |
| `StopOnceHitCosmoCredits` | Stop when Cosmo credits cap is reached |
| `StopOnceHitLunarCredits` | Stop when Lunar credits cap is reached |
| `XPRelicGrind` | Enable XP relic grinding mode |

### Available Numeric Settings

| Setting | Description |
|---------|-------------|
| `CosmoCreditsCap` | Maximum Cosmo credits before stopping (if enabled) |
| `LunarCreditsCap` | Maximum Lunar credits before stopping (if enabled) |

## Basic Commands

```lua
-- Start Ice automation (slash command)
yield("/ice start")

-- Stop Ice automation (slash command)
yield("/ice stop")
```

**Note:** The IPC API (`IPC.Ice.Enable()`/`IPC.Ice.Disable()`) is preferred over slash commands for programmatic control, as it provides immediate feedback and doesn't require waiting for command processing.

## Practical Usage Examples

### Example 1: Check if Ice is Running Before Starting

```lua
if not IPC.Ice.IsRunning() then
    IPC.Ice.Enable()
    LogInfo("[Ice] Started Ice automation")
end
```

### Example 2: Stop After Current Mission

```lua
-- Set Ice to stop after completing the current mission
IPC.Ice.ChangeSetting("StopAfterCurrent", true)
LogInfo("[Ice] Ice will stop after current mission completes")
```

### Example 3: Configure Specific Missions

```lua
-- Clear all missions and enable only specific ones
IPC.Ice.ClearAllMissions()
IPC.Ice.OnlyMissions({12, 15, 18})  -- Enable only missions 12, 15, 18
IPC.Ice.Enable()
LogInfo("[Ice] Running only missions 12, 15, 18")
```

### Example 4: Set Credit Caps

```lua
-- Configure Ice to stop at credit thresholds
IPC.Ice.ChangeSetting("StopOnceHitCosmoCredits", true)
IPC.Ice.ChangeSettingAmount("CosmoCreditsCap", 10000)
IPC.Ice.ChangeSetting("StopOnceHitLunarCredits", true)
IPC.Ice.ChangeSettingAmount("LunarCreditsCap", 5000)
LogInfo("[Ice] Configured credit caps")
```

### Example 5: Wait for Ice to Complete

```lua
-- Start Ice and wait for it to finish
IPC.Ice.Enable()

-- Wait until Ice is no longer running
while IPC.Ice.IsRunning() do
    yield("/wait 5")
end

LogInfo("[Ice] Ice has completed all missions")
```

## Integration Pattern

Ice is typically used in combination with job switching and gear equipping. You can use either IPC or slash commands:

### Using IPC (Recommended)

```lua
-- Stop Ice before switching jobs
if IPC.Ice.IsRunning() then
    IPC.Ice.Disable()
    LogInfo("[Ice] Stopped Ice for job switch")
end
yield("/wait 1")

-- Switch job (uiSlot = API index + 1!)
yield("/gearset change " .. uiSlot)
yield("/wait 1")

-- Equip recommended gear (AutoDuty)
yield("/ad equiprec")
yield("/wait 2")

-- Resume Ice automation
IPC.Ice.Enable()
LogInfo("[Ice] Restarted Ice after job switch")
```

### Using Slash Commands (Legacy)

```lua
-- Stop Ice before switching jobs (use multiple stops to ensure it registers)
yield("/ice stop")
yield("/wait 0.5")
yield("/ice stop")
yield("/wait 0.5")
yield("/ice stop")
yield("/wait 1")

-- Switch job (uiSlot = API index + 1!)
yield("/gearset change " .. uiSlot)
yield("/wait 1")

-- Equip recommended gear (AutoDuty)
yield("/ad equiprec")
yield("/wait 2")

-- Resume Ice automation
yield("/ice start")
```

**Note:** The IPC method is more reliable as it provides immediate state feedback, while slash commands may require multiple attempts to register.

## Typical Workflow

1. Stop Ice
2. Check job levels against breakpoints
3. Switch to job that needs leveling (if any)
4. Equip recommended gear
5. Start Ice again

## Plugin Dependencies

When using Ice, you typically also need:
- **AutoDuty** - For `/ad equiprec` (equip recommended gear)
- **ICE** - The internal plugin name is `ICE` (all caps) for plugin_dependencies

## Example: Job Switch with Ice (Modern IPC)

```lua
local function SwitchJobAndRestartIce(jobId)
    -- Stop current automation if running
    if IPC.Ice.IsRunning() then
        IPC.Ice.Disable()
        LogInfo("[Ice] Stopped Ice for job switch")
    end
    yield("/wait 1")

    -- Find and switch gearset
    for idx = 1, 100 do
        local gs = Player.GetGearset(idx)
        if gs and gs.ClassJob == jobId then
            -- IMPORTANT: UI slot = API index + 1!
            local uiSlot = idx + 1
            yield("/gearset change " .. uiSlot)
            yield("/wait 1")

            -- Equip recommended gear
            yield("/ad equiprec")
            yield("/wait 2")

            -- Resume automation
            IPC.Ice.Enable()
            LogInfo("[Ice] Restarted Ice on job " .. jobId)
            return true
        end
    end

    LogInfo("[Ice] Could not find gearset for job " .. jobId)
    return false
end
```

## Example: Job Switch with Ice (Legacy Slash Commands)

```lua
local function SwitchJobAndRestartIce_Legacy(jobId)
    -- Stop current automation (multiple times to ensure it registers)
    yield("/ice stop")
    yield("/wait 0.5")
    yield("/ice stop")
    yield("/wait 0.5")
    yield("/ice stop")
    yield("/wait 1")

    -- Find and switch gearset
    for idx = 1, 100 do
        local gs = Player.GetGearset(idx)
        if gs and gs.ClassJob == jobId then
            -- IMPORTANT: UI slot = API index + 1!
            local uiSlot = idx + 1
            yield("/gearset change " .. uiSlot)
            yield("/wait 1")

            -- Equip recommended gear
            yield("/ad equiprec")
            yield("/wait 2")

            -- Resume automation
            yield("/ice start")
            return true
        end
    end
    return false
end
```

## Notes

### Best Practices
- **Prefer IPC API over slash commands** for better reliability and immediate state feedback
- Use `IPC.Ice.IsRunning()` to check state before starting/stopping
- Always stop Ice before switching jobs to avoid issues
- **CRITICAL:** `Player.GetGearset(idx)` returns API index, but `/gearset change` uses UI slot numbers. Always use `idx + 1` for the gearset change command!
- Give adequate wait time between commands (1-2 seconds)
- Can't switch jobs during crafting, Mech Ops, or other duties - wait for them to complete first

### IPC Advantages
- **Immediate feedback:** No need to wait for command processing
- **State checking:** Can query if Ice is running before acting
- **Mission control:** Programmatically configure which missions to run
- **Settings management:** Change caps and behaviors on the fly
- **No multiple retries:** Unlike slash commands which may need multiple attempts

### Legacy Slash Commands
- If using slash commands, **use multiple `/ice stop` commands** (3x with waits) to ensure Ice actually stops
- Slash commands are still valid but less reliable for automation
- Consider migrating existing scripts to IPC for better control

### Integration
- Ice handles the actual Cosmic Exploration content automatically
- Use in combination with breakpoint-based leveling scripts
- Can configure missions, credit caps, and stopping conditions via IPC
- Perfect for automated job leveling rotations
