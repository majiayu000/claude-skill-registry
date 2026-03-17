---
name: SND Artisan Integration
description: Use this skill when implementing crafting automation in SND macros using the Artisan plugin. Covers crafting lists, endurance mode, and crafting state management.
---

# Artisan Integration for SND

This skill covers integration with the Artisan plugin for crafting automation in SND macros.

## Prerequisites

```lua
-- Always check plugin availability first
if not HasPlugin("Artisan") then
    yield("/echo [Script] Artisan plugin not available")
    StopFlag = true
    return
end
```

## Official IPC API Reference

> **Source:** https://github.com/PunishXIV/Artisan/blob/main/Artisan/IPC/IPC.cs

All APIs below are verified against the official Artisan IPC source code.

**Note:** In the C# source, `CraftItem` uses `ushort` for recipeId and `int` for amount. In Lua, both are treated as `number` types.

### Endurance Mode
```lua
-- Get endurance status (is endurance mode enabled)
IPC.Artisan.GetEnduranceStatus() → boolean

-- Set endurance status (enable/disable endurance mode)
IPC.Artisan.SetEnduranceStatus(boolean enabled) → nil
```

### Crafting List Control
```lua
-- Check if a crafting list is currently processing
IPC.Artisan.IsListRunning() → boolean

-- Check if the crafting list is paused
IPC.Artisan.IsListPaused() → boolean

-- Set list pause state (only works if list is already paused)
IPC.Artisan.SetListPause(boolean paused) → nil
```

### Stop/Resume Requests
```lua
-- Get the stop request status
IPC.Artisan.GetStopRequest() → boolean

-- Set stop request (true = stop crafting, false = resume)
-- When true: stops crafting
-- When false: resumes crafting (unless in duty finder/bound by duty)
IPC.Artisan.SetStopRequest(boolean stop) → nil
```

### Craft Specific Item
```lua
-- Craft a specific item by recipe ID
-- Throws exception if recipe ID not found
IPC.Artisan.CraftItem(number recipeId, number amount) → nil
```

### Busy Check
```lua
-- Check if Artisan is busy (endurance running, list processing, or tasks queued)
IPC.Artisan.IsBusy() → boolean
```

### ArtisanMode Enum
```lua
local ArtisanMode = {
    None = 0,
    Endurance = 1,
    Lists = 2,
}
```

## Helper Functions

### Artisan Status Checking
```lua
function IsArtisanRunning()
    return IPC.Artisan.IsListRunning() and not IPC.Artisan.IsListPaused()
end

function IsArtisanPaused()
    return IPC.Artisan.IsListRunning() and IPC.Artisan.IsListPaused()
end

function GetArtisanStatus()
    if not HasPlugin("Artisan") then
        return "not_available"
    end

    if IPC.Artisan.IsListRunning() then
        if IPC.Artisan.IsListPaused() then
            return "paused"
        else
            return "running"
        end
    else
        return "idle"
    end
end
```

### Wait for Completion
```lua
function WaitForArtisanComplete(timeout)
    timeout = timeout or 300 -- 5 minutes default for crafting
    local startTime = os.clock()

    while IsArtisanRunning() and (os.clock() - startTime) < timeout do
        yield("/wait 1")
    end

    if IsArtisanRunning() then
        yield("/echo [Script] Artisan timeout, stopping")
        IPC.Artisan.SetStopRequest(true)
        return false
    end

    return true
end
```

## Crafting Patterns

### Basic Crafting
```lua
-- Check if Artisan is running
if IPC.Artisan.IsListRunning() and not IPC.Artisan.IsListPaused() then
    yield("/echo [Script] Artisan is already running")
    -- Handle already running state
end

-- Start crafting
IPC.Artisan.CraftItem(recipeId, quantity)

-- Wait for crafting to complete
while IPC.Artisan.IsListRunning() and not IPC.Artisan.IsListPaused() do
    yield("/wait 1")
end
```

### Complete Crafting Workflow
```lua
function CompleteCraftingWorkflow(recipeId, quantity, timeout)
    timeout = timeout or 300

    -- Check prerequisites
    if not HasPlugin("Artisan") then
        yield("/echo [Script] ERROR: Artisan plugin not available")
        return false
    end

    if not Player.Available then
        yield("/echo [Script] ERROR: Player not available")
        return false
    end

    -- Check if already running
    if IsArtisanRunning() then
        yield("/echo [Script] Artisan is already running")
        return true
    end

    -- Start crafting
    yield("/echo [Script] Starting crafting: Recipe " .. recipeId .. " x" .. quantity)
    IPC.Artisan.CraftItem(recipeId, quantity)

    -- Wait for completion
    if WaitForArtisanComplete(timeout) then
        yield("/echo [Script] Crafting completed successfully")
        return true
    else
        yield("/echo [Script] Crafting failed or timed out")
        return false
    end
end
```

### Crafting with Retry
```lua
function CraftWithRetry(recipeId, quantity, maxRetries, timeout)
    maxRetries = maxRetries or 3
    timeout = timeout or 300

    for attempt = 1, maxRetries do
        if CompleteCraftingWorkflow(recipeId, quantity, timeout) then
            return true
        end

        if attempt < maxRetries then
            yield("/echo [Script] Crafting attempt " .. attempt .. " failed, retrying")
            yield("/wait 5")
        end
    end

    yield("/echo [Script] Crafting failed after " .. maxRetries .. " attempts")
    return false
end
```

### Pause and Resume
```lua
function PauseArtisan()
    if not HasPlugin("Artisan") then
        return false
    end

    -- Use SetStopRequest(true) to stop crafting
    IPC.Artisan.SetStopRequest(true)
    yield("/echo [Script] Artisan stop requested")
    return true
end

function ResumeArtisan()
    if not HasPlugin("Artisan") then
        return false
    end

    -- Use SetStopRequest(false) to resume crafting
    -- Note: Won't resume if in duty finder or bound by duty
    IPC.Artisan.SetStopRequest(false)
    yield("/echo [Script] Artisan resume requested")
    return true
end

function StopArtisan()
    if not HasPlugin("Artisan") then
        return false
    end

    IPC.Artisan.SetStopRequest(true)
    yield("/echo [Script] Artisan stopped")
    return true
end

-- Check if Artisan is busy with anything
function IsArtisanBusy()
    if not HasPlugin("Artisan") then
        return false
    end
    return IPC.Artisan.IsBusy()
end
```

## Endurance Mode

### Monitor Endurance Status
```lua
function CraftingWithEnduranceCheck(recipeId, quantity)
    -- Start crafting
    IPC.Artisan.CraftItem(recipeId, quantity)

    -- Monitor crafting progress
    while IsArtisanRunning() do
        -- Check endurance status
        if IPC.Artisan.GetEnduranceStatus() then
            yield("/echo [Script] Endurance is active")
        end

        yield("/wait 1")
    end

    yield("/echo [Script] Crafting completed")
end
```

## Error Handling

### Safe Artisan Calls
```lua
function SafeArtisanCall(functionName, ...)
    if not HasPlugin("Artisan") then
        return nil, "Artisan plugin not available"
    end

    local success, result = pcall(function()
        return IPC.Artisan[functionName](...)
    end)

    if success then
        return result, nil
    else
        return nil, "Artisan call failed: " .. tostring(result)
    end
end
```

### Timeout Handling
```lua
local startTime = os.clock()
while IsArtisanRunning() and (os.clock() - startTime) < 300 do
    yield("/wait 1")
end

if IsArtisanRunning() then
    yield("/echo [Script] WARNING: Crafting taking too long, stopping...")
    IPC.Artisan.SetStopRequest(true)
end
```

## State Machine Integration

```lua
CharacterState = {
    ready = Ready,
    crafting = Crafting,
    -- ... other states
}

function Crafting()
    if CompleteCraftingWorkflow(recipeId, quantity, 300) then
        yield("/echo [Script] Crafting completed")
        State = CharacterState.ready
    else
        yield("/echo [Script] Crafting failed")
        State = CharacterState.ready
    end
end
```

## Character Condition Integration

```lua
-- Character conditions for crafting
local CharacterCondition = {
    craftingMode = 5,
    executingCraftingSkill = 40,
    craftingModeIdle = 41
}

-- Check if character is in crafting mode
if Svc.Condition[CharacterCondition.craftingMode] then
    yield("/echo [Script] Character is in crafting mode")
end

-- Check if character is executing crafting skill
if Svc.Condition[CharacterCondition.executingCraftingSkill] then
    yield("/echo [Script] Character is executing crafting skill")
end

-- Check if character is busy (including Artisan)
function IsCharacterBusy()
    return Svc.Condition[CharacterCondition.casting] or
           Svc.Condition[CharacterCondition.betweenAreas] or
           Svc.Condition[CharacterCondition.beingMoved] or
           Svc.Condition[CharacterCondition.craftingMode] or
           Svc.Condition[CharacterCondition.executingCraftingSkill] or
           IsArtisanRunning() or
           Player.IsBusy
end
```

## Configuration Variables

```lua
configs:
  EnableArtisan:
    default: true
    description: Enable Artisan crafting
  CraftingTimeout:
    default: 300
    description: Crafting timeout in seconds
  MaxCraftingRetries:
    default: 3
    description: Maximum crafting retry attempts
  CrafterClass:
    default: "Carpenter"
    description: Select the crafting class to use
    is_choice: true
    choices: ["Carpenter", "Blacksmith", "Armorer", "Goldsmith", "Leatherworker", "Weaver", "Alchemist", "Culinarian"]
  ScripColor:
    default: "Orange"
    description: Type of scrip to use
    is_choice: true
    choices: ["Orange", "Purple"]
```

## Best Practices

1. **Always check plugin availability** before using Artisan
2. **Use longer timeouts** for crafting operations (default: 300s / 5 minutes)
3. **Check crafting state** before starting new crafting
4. **Monitor endurance status** for long crafting sessions
5. **Use appropriate wait times**: 1s for crafting monitoring
6. **Stop crafting** on timeout to prevent stuck states
7. **Check character conditions** for crafting mode status
