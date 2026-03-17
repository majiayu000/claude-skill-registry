---
name: SND Questionable
description: Use this skill when implementing quest automation in SND macros using the Questionable plugin. Covers command usage and integration with leveling workflows.
---

# Questionable Plugin (Quest Automation)

> **Source:** https://github.com/pot0to/Questionable (Verified - No IPC APIs found)

Questionable is a small quest helper plugin designed to automatically do your quests where possible.
It utilizes navmesh to automatically travel to all quest waypoints and attempts to complete all steps
along the way (excluding dungeons, single-player duties and combat).

**Not all quests are supported.**

## Required Plugins

- vnavmesh
- TextAdvance
- Lifestream

## Commands

```lua
-- Open the Questing window
yield("/qst")

-- Display simplified commands
yield("/qst help")

-- Display all available commands
yield("/qst help-all")

-- Open the configuration window
yield("/qst config")

-- Start doing quests
yield("/qst start")

-- Stop doing quests
yield("/qst stop")
```

## IPC Methods

**IMPORTANT: Questionable does NOT expose any IPC methods for external use.**

After verifying the official source code at https://github.com/pot0to/Questionable, the plugin does not provide an IPC provider. This means there are **no programmatic APIs** available to check quest status, control the plugin, or query quest information from SND macros.

## Integration with SND Macros

Since Questionable has no IPC, you can only interact with it via:

1. **Chat Commands** - Use `yield("/qst ...")` commands
2. **Manual Coordination** - Structure your macro to work alongside Questionable

### Example: Starting Questionable

```lua
-- Start Questionable from your macro
function StartQuestionable()
    if not HasPlugin("Questionable") then
        yield("/echo [Error] Questionable plugin not found!")
        return false
    end

    yield("/qst start")
    yield("/echo Started Questionable - please monitor manually")
    return true
end
```

### Example: Working Alongside Questionable

Since you can't check if Questionable is running programmatically, structure your macro to assume Questionable will handle quests:

```lua
-- Your leveling macro
function LevelingLoop()
    while Player.Level < MAX_LEVEL do
        -- Do your automation tasks
        CheckRetainers()
        CheckGrandCompany()

        -- Tell user to start Questionable manually
        yield("/echo Please start Questionable (/qst start) to continue leveling")
        yield("/echo Press any key when quests are done...")

        -- Wait for user input or time-based check
        yield("/wait 300")  -- Wait 5 minutes, adjust as needed
    end
end
```

## Notes

- **No IPC Available** - Cannot check quest status, running state, or control programmatically
- **Command-Only Control** - Use `/qst` commands only
- **Manual Coordination Required** - Your macros cannot automatically detect when Questionable finishes
- Does NOT handle: dungeons, single-player duties, combat
- Requires: vnavmesh, TextAdvance, Lifestream plugins

## Workaround: Time-Based Assumptions

Since you can't query Questionable's state, you may need to use time-based waits:

```lua
-- Start Questionable and wait a fixed time
yield("/qst start")
yield("/echo Waiting for quests (assuming 15 minutes)...")
yield("/wait 900")  -- Wait 15 minutes
yield("/qst stop")
```

Or use level checks as a proxy:

```lua
-- Keep running Questionable until level target reached
local startLevel = Svc.ClientState.LocalPlayer.Level
yield("/qst start")

while Svc.ClientState.LocalPlayer.Level < TARGET_LEVEL do
    yield("/wait 60")  -- Check every minute
end

yield("/qst stop")
yield("/echo Reached target level!")
```
