---
name: SND AutoRetainer Integration
description: Use this skill when implementing retainer management in SND macros using the AutoRetainer plugin. Covers character data access, retainer inventory, task management, multi-mode, auto-login, and venture tracking.
---

# AutoRetainer Integration for SND

This skill covers integration with the AutoRetainer plugin for retainer management in SND macros.

> **Source Status:** Partially Verified - Core API methods verified from https://github.com/PunishXIV/AutoRetainerAPI/blob/main/AutoRetainerAPI/AutoRetainerApi.cs. Additional IPC methods documented from community testing and usage.

## Prerequisites

```lua
-- Always check plugin availability first
if not HasPlugin("AutoRetainer") then
    yield("/echo [Script] AutoRetainer plugin not available")
    StopFlag = true
    return
end
```

## CRITICAL: Character ID Access

**ALWAYS use `Svc.ClientState.LocalContentId` for character data access. Using `Player.CID` causes SEHException crashes.**

```lua
-- CORRECT - Use this
local currentCharId = Svc.ClientState.LocalContentId
local characterData = IPC.AutoRetainer.GetOfflineCharacterData(currentCharId)

-- WRONG - Causes SEHException crash
-- local characterData = IPC.AutoRetainer.GetOfflineCharacterData(Player.CID)
```

## Complete API Reference

### Verified Core API Methods (from AutoRetainerApi.cs)

These methods are confirmed from the official AutoRetainerAPI source code:

```lua
-- Get offline character data (VERIFIED - requires Svc.ClientState.LocalContentId)
IPC.AutoRetainer.GetOfflineCharacterData(number contentId) -> OfflineCharacterData
-- Properties: .RetainersAwaitingProcessing (boolean)

-- Write offline character data (VERIFIED)
IPC.AutoRetainer.WriteOfflineCharacterData(OfflineCharacterData data) -> nil
-- WARNING: Must read, modify, and write back within single framework update

-- Get additional retainer data (VERIFIED)
IPC.AutoRetainer.GetAdditionalRetainerData(number contentId, string retainerName) -> AdditionalRetainerData

-- Write additional retainer data (VERIFIED)
IPC.AutoRetainer.WriteAdditionalRetainerData(number contentId, string retainerName, AdditionalRetainerData data) -> nil
-- WARNING: Must read, modify, and write back within single framework update

-- Get registered characters (VERIFIED)
IPC.AutoRetainer.GetRegisteredCharacters() -> table
-- Returns list of all known character content IDs (excluding blacklisted/uninitialized)

-- Set venture override (VERIFIED - use during OnSendRetainerToVenture event)
IPC.AutoRetainer.SetVenture(number ventureId) -> nil

-- Get/Set suppressed state (VERIFIED)
IPC.AutoRetainer.GetSuppressed() -> boolean
IPC.AutoRetainer.SetSuppressed(boolean suppressed) -> nil

-- Check if API is ready (VERIFIED)
IPC.AutoRetainer.Ready -> boolean (property)
```

### Additional IPC Methods (Community Documented)

These methods are documented from community usage and testing. They work in practice but may need verification against latest source:

### Basic Status and Control Functions

```lua
-- Check if AutoRetainer is busy
IPC.AutoRetainer.IsBusy() -> boolean

-- Get multi-mode status
IPC.AutoRetainer.GetMultiModeEnabled() -> boolean

-- Set multi-mode enabled/disabled
IPC.AutoRetainer.SetMultiModeEnabled(boolean enabled) -> nil

-- Alternative method to enable multi-mode
IPC.AutoRetainer.EnableMultiMode() -> nil
```

### Inventory and Retainer Management

```lua
-- Get number of free inventory slots
IPC.AutoRetainer.GetInventoryFreeSlotCount() -> number

-- Get information about enabled retainers
IPC.AutoRetainer.GetEnabledRetainers() -> table

-- Check if any retainers are available for current character
IPC.AutoRetainer.AreAnyRetainersAvailableForCurrentChara() -> boolean

-- Get retainer inventory
IPC.AutoRetainer.GetRetainerInventory(number retainerId) -> Inventory
```

### Character and Data Management

```lua
-- Get list of registered characters
IPC.AutoRetainer.GetRegisteredCharacters() -> table

-- Get offline character data (ALWAYS use Svc.ClientState.LocalContentId!)
IPC.AutoRetainer.GetOfflineCharacterData(number contentId) -> OfflineCharacterDataWrapper

-- OfflineCharacterDataWrapper properties:
-- .RetainersAwaitingProcessing (boolean) - Whether retainers need processing
```

### Task Management and Control

```lua
-- Abort all current AutoRetainer tasks
IPC.AutoRetainer.AbortAllTasks() -> nil

-- Disable all AutoRetainer functions
IPC.AutoRetainer.DisableAllFunctions() -> nil

-- Enqueue HET (Hunt, Exploration, Trade) task
-- onFailure: true to retry on failure, false to stop on failure
IPC.AutoRetainer.EnqueueHET(boolean onFailure) -> nil

-- Enqueue initiation task
IPC.AutoRetainer.EnqueueInitiation() -> nil

-- Start retainer task
IPC.AutoRetainer.StartRetainerTask(number retainerId, number taskType, number taskId) -> boolean

-- Get retainer task status
IPC.AutoRetainer.GetRetainerTaskStatus(number retainerId) -> TaskStatus
```

### Auto-Login and Relog Functions

```lua
-- Check if auto-login is possible
IPC.AutoRetainer.CanAutoLogin() -> boolean

-- Relog to specific character
-- Format: "CharacterName WorldName"
IPC.AutoRetainer.Relog(string charaNameWithWorld) -> nil
```

### Options and Settings

```lua
-- Get retainer sense option status
IPC.AutoRetainer.GetOptionRetainerSense() -> boolean

-- Set retainer sense option
IPC.AutoRetainer.SetOptionRetainerSense(boolean enabled) -> nil

-- Suppress or unsuppress AutoRetainer (VERIFIED - see Verified Core API Methods section)
-- This is an alias for SetSuppressed in the verified API
IPC.AutoRetainer.SetSuppressed(boolean suppressed) -> nil
```

### Grand Company and Venture Information

```lua
-- Get Grand Company information
IPC.AutoRetainer.GetGCInfo() -> table

-- Get closest retainer venture seconds remaining
IPC.AutoRetainer.GetClosestRetainerVentureSecondsRemaining(number contentId) -> number
```

### Submersible Management

```lua
-- Get enabled submarines
IPC.AutoRetainer.GetEnabledSubmarines() -> table

-- Check if any submarines are available
IPC.AutoRetainer.AreAnySubmarinesAvailableForCurrentChara() -> boolean
```

### Additional Character Functions

```lua
-- Get all registered characters (for multi-character automation)
IPC.AutoRetainer.GetRegisteredCharacters() -> table
-- Returns list of registered character content IDs
```

## Helper Functions

### AutoRetainer Status Checking

```lua
function IsAutoRetainerBusy()
    if not HasPlugin("AutoRetainer") then
        return false
    end
    return IPC.AutoRetainer.IsBusy()
end

function WaitForAutoRetainerComplete(timeout)
    timeout = timeout or 300
    local startTime = os.clock()

    while IsAutoRetainerBusy() and (os.clock() - startTime) < timeout do
        yield("/wait 1")
    end

    if IsAutoRetainerBusy() then
        yield("/echo [Script] AutoRetainer timeout")
        return false
    end

    return true
end
```

### Safe Character Data Retrieval

```lua
-- VERIFIED: Uses official GetOfflineCharacterData API
function GetAutoRetainerCharacterData()
    if not HasPlugin("AutoRetainer") then
        return nil, "AutoRetainer plugin not available"
    end

    -- CRITICAL: Always use Svc.ClientState.LocalContentId (VERIFIED)
    local currentCharId = Svc.ClientState.LocalContentId
    local success, result = pcall(function()
        return IPC.AutoRetainer.GetOfflineCharacterData(currentCharId)
    end)

    if success then
        return result, nil
    else
        return nil, "Failed to get character data: " .. tostring(result)
    end
end
```

### Multi-Mode Control

```lua
function EnableAutoRetainerMultiMode()
    if not HasPlugin("AutoRetainer") then
        yield("/echo [Script] AutoRetainer not available")
        return false
    end

    IPC.AutoRetainer.SetMultiModeEnabled(true)
    yield("/echo [Script] AutoRetainer multi-mode enabled")
    return true
end

function DisableAutoRetainerMultiMode()
    if not HasPlugin("AutoRetainer") then
        return false
    end

    IPC.AutoRetainer.SetMultiModeEnabled(false)
    yield("/echo [Script] AutoRetainer multi-mode disabled")
    return true
end
```

### Retainer Availability

```lua
function AreRetainersAvailable()
    if not HasPlugin("AutoRetainer") then
        return false
    end

    return IPC.AutoRetainer.AreAnyRetainersAvailableForCurrentChara()
end

function CheckRetainersAwaitingProcessing()
    local charData = GetAutoRetainerCharacterData()
    if charData and charData.RetainersAwaitingProcessing then
        return true
    end
    return false
end
```

### Venture Time Checking

```lua
function GetNextVentureTime()
    if not HasPlugin("AutoRetainer") then
        return nil
    end

    local currentCharId = Svc.ClientState.LocalContentId
    local seconds = IPC.AutoRetainer.GetClosestRetainerVentureSecondsRemaining(currentCharId)
    return seconds
end

function FormatVentureTime(seconds)
    if not seconds then
        return "Unknown"
    end

    local minutes = math.floor(seconds / 60)
    local hours = math.floor(minutes / 60)
    minutes = minutes % 60

    if hours > 0 then
        return string.format("%dh %dm", hours, minutes)
    else
        return string.format("%dm", minutes)
    end
end
```

## Usage Patterns

### Check AutoRetainer Availability

```lua
if IPC.AutoRetainer and not IPC.AutoRetainer.IsBusy() then
    yield("/echo [Script] AutoRetainer is available and ready")
else
    yield("/echo [Script] AutoRetainer is busy or unavailable")
end
```

### Check Retainers Awaiting Processing

```lua
local charData = IPC.AutoRetainer.GetOfflineCharacterData(Svc.ClientState.LocalContentId)
if charData and charData.RetainersAwaitingProcessing then
    yield("/echo [Script] Retainers are waiting to be processed")
    IPC.AutoRetainer.EnableMultiMode()
else
    yield("/echo [Script] No retainers waiting for processing")
end
```

### Inventory Space Check

```lua
local freeSlots = IPC.AutoRetainer.GetInventoryFreeSlotCount()
if freeSlots < 5 then
    yield("/echo [Script] Warning: Low inventory space (" .. freeSlots .. " slots)")
else
    yield("/echo [Script] Inventory space OK (" .. freeSlots .. " slots)")
end
```

### Complete AutoRetainer Workflow

```lua
function HandleAutoRetainerWorkflow()
    -- Check if AutoRetainer is available
    if not IPC.AutoRetainer or IPC.AutoRetainer.IsBusy() then
        yield("/echo [Script] AutoRetainer not available")
        return false
    end

    -- Check inventory space
    local freeSlots = IPC.AutoRetainer.GetInventoryFreeSlotCount()
    if freeSlots < 3 then
        yield("/echo [Script] Not enough inventory space")
        return false
    end

    -- Check if retainers need processing
    local charData = IPC.AutoRetainer.GetOfflineCharacterData(Svc.ClientState.LocalContentId)
    if charData and charData.RetainersAwaitingProcessing then
        yield("/echo [Script] Enabling AutoRetainer for retainer processing")
        IPC.AutoRetainer.EnableMultiMode()
        return true
    else
        yield("/echo [Script] No retainers need processing")
        return false
    end
end
```

### Relog to Another Character

```lua
function RelogToCharacter(characterName, worldName)
    if not HasPlugin("AutoRetainer") then
        yield("/echo [Script] AutoRetainer not available")
        return false
    end

    if not IPC.AutoRetainer.CanAutoLogin() then
        yield("/echo [Script] Auto-login not available")
        return false
    end

    local charaWithWorld = characterName .. " " .. worldName
    yield("/echo [Script] Relogging to: " .. charaWithWorld)
    IPC.AutoRetainer.Relog(charaWithWorld)
    return true
end
```

## Error Handling

### Safe AutoRetainer Calls

```lua
function SafeAutoRetainerCall(functionName, ...)
    if not HasPlugin("AutoRetainer") then
        return nil, "AutoRetainer plugin not available"
    end

    local success, result = pcall(function()
        return IPC.AutoRetainer[functionName](...)
    end)

    if success then
        return result, nil
    else
        return nil, "AutoRetainer call failed: " .. tostring(result)
    end
end
```

## State Machine Integration

```lua
CharacterState = {
    ready = Ready,
    checkingRetainers = CheckingRetainers,
    processingRetainers = ProcessingRetainers,
    -- ... other states
}

function CheckingRetainers()
    if AreRetainersAvailable() then
        yield("/echo [Script] Retainers available, processing...")
        IPC.AutoRetainer.EnqueueInitiation()
        State = CharacterState.processingRetainers
    else
        yield("/echo [Script] No retainers to process")
        State = CharacterState.ready
    end
end

function ProcessingRetainers()
    if not IPC.AutoRetainer.IsBusy() then
        yield("/echo [Script] Retainer processing complete")
        State = CharacterState.ready
    end
    -- Still processing, stay in this state
end
```

## Character Condition Integration

```lua
-- Character condition for summoning bell
local CharacterCondition = {
    occupiedSummoningBell = 50
}

-- Check if at summoning bell
if Svc.Condition[CharacterCondition.occupiedSummoningBell] then
    yield("/echo [Script] At summoning bell")
end

-- Check if character is busy (including AutoRetainer)
function IsCharacterBusy()
    return Svc.Condition[CharacterCondition.casting] or
           Svc.Condition[CharacterCondition.betweenAreas] or
           Svc.Condition[CharacterCondition.beingMoved] or
           Svc.Condition[CharacterCondition.occupiedSummoningBell] or
           IPC.AutoRetainer.IsBusy() or
           Player.IsBusy
end
```

## Configuration Variables

```lua
configs:
  EnableAutoRetainer:
    default: true
    description: Enable AutoRetainer integration
  Retainers:
    default: true
    description: Automatically interact with retainers for ventures
  RetainerTaskTimeout:
    default: 300
    description: Retainer task timeout in seconds
  MaxRetainerRetries:
    default: 3
    description: Maximum retainer operation retry attempts
```

## Common Issues and Solutions

### Issue 1: `System.Runtime.InteropServices.SEHException`
**Problem:** Using incorrect character ID parameters.

**Solution:** Always use `Svc.ClientState.LocalContentId`:
```lua
-- WRONG - causes SEHException
local characterData = IPC.AutoRetainer.GetOfflineCharacterData(Player.CID)

-- CORRECT
local characterData = IPC.AutoRetainer.GetOfflineCharacterData(Svc.ClientState.LocalContentId)
```

### Issue 2: `attempt to call a nil value`
**Problem:** Trying to call a property as a function.

**Solution:** Access the property correctly:
```lua
-- WRONG
if ARRetainersWaitingToBeProcessed() then

-- CORRECT
local characterData = IPC.AutoRetainer.GetOfflineCharacterData(Svc.ClientState.LocalContentId)
if characterData and characterData.RetainersAwaitingProcessing then
```

### Issue 3: API Functions Not Available
**Problem:** AutoRetainer functions return `nil` or cause errors.

**Solution:** Always check if the API is available:
```lua
if IPC.AutoRetainer then
    local isBusy = IPC.AutoRetainer.IsBusy()
else
    yield("/echo [Script] AutoRetainer plugin not available")
end
```

## API Verification Notes

### Verified Methods (AutoRetainerApi.cs)
The following methods are confirmed from the official AutoRetainerAPI source code at https://github.com/PunishXIV/AutoRetainerAPI:

- `GetOfflineCharacterData(ulong contentId)` - Returns OfflineCharacterData with .RetainersAwaitingProcessing property
- `WriteOfflineCharacterData(OfflineCharacterData)` - Must be used within same frame as read
- `GetAdditionalRetainerData(ulong contentId, string name)` - Returns AdditionalRetainerData
- `WriteAdditionalRetainerData(ulong contentId, string name, AdditionalRetainerData)` - Must be used within same frame as read
- `GetRegisteredCharacters()` - Returns List<ulong> of character content IDs
- `SetVenture(uint ventureId)` - Override venture assignment (event-specific)
- `GetSuppressed()` / `SetSuppressed(bool)` - Control suppressed state
- `Ready` property - Check if API is initialized

### Community Documented Methods
The following methods are documented from community usage and testing. They work in practice but the exact IPC provider source has not been verified:

- `IsBusy()` - Check if AutoRetainer is processing
- `GetMultiModeEnabled()` / `SetMultiModeEnabled(bool)` - Multi-mode control
- `EnableMultiMode()` - Alternative multi-mode enable
- `GetInventoryFreeSlotCount()` - Inventory space check
- `GetEnabledRetainers()` - Enabled retainer list
- `AreAnyRetainersAvailableForCurrentChara()` - Retainer availability
- `GetRetainerInventory(retainerId)` - Retainer inventory access
- `AbortAllTasks()` - Cancel all tasks
- `DisableAllFunctions()` - Disable AutoRetainer
- `EnqueueHET(onFailure)` - Hunt/Exploration/Trade tasks
- `EnqueueInitiation()` - Start retainer processing
- `StartRetainerTask(retainerId, taskType, taskId)` - Start specific task
- `GetRetainerTaskStatus(retainerId)` - Task status check
- `CanAutoLogin()` - Auto-login availability
- `Relog(charaNameWithWorld)` - Character switch
- `GetOptionRetainerSense()` / `SetOptionRetainerSense(bool)` - RetainerSense option
- `GetGCInfo()` - Grand Company information
- `GetClosestRetainerVentureSecondsRemaining(contentId)` - Venture timer
- `GetEnabledSubmarines()` - Submarine list
- `AreAnySubmarinesAvailableForCurrentChara()` - Submarine availability

### Known API Changes Needed
The AutoRetainer plugin uses IPC providers that are defined in the main AutoRetainer plugin (not the API library). To fully verify all methods, we would need access to:
- `PunishXIV/AutoRetainer` repository IPC provider implementations
- Current testing to confirm method signatures match actual behavior

## Best Practices

1. **ALWAYS use `Svc.ClientState.LocalContentId`** - Never use `Player.CID` (causes crashes) [VERIFIED]
2. **Use pcall** for all AutoRetainer API calls
3. **Check plugin availability** before using AutoRetainer
4. **Check IsBusy()** before starting new operations
5. **Handle errors gracefully** with meaningful messages
6. **Check inventory space** before processing retainers
7. **Verify retainer availability** before processing
8. **Use multi-mode appropriately** based on your needs
9. **Check summoning bell condition** when managing retainers
10. **Never store OfflineCharacterData or AdditionalRetainerData** - Must read, modify, and write within single frame [VERIFIED]
