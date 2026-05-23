---
name: SND Deliveroo Integration
description: Use this skill when implementing Grand Company delivery automation in SND macros using the Deliveroo plugin. Covers GC turn-ins, expert delivery, and supply provisioning.
---

# Deliveroo Integration for SND

This skill covers integration with the Deliveroo plugin for Grand Company delivery automation in SND macros.

> **Source:** https://github.com/VeraNala/Deliveroo/blob/master/Deliveroo/External/DeliverooIpc.cs
>
> **Note:** The original repository at https://git.carvel.li/liza/Deliveroo is archived and inaccessible. This documentation is verified from a GitHub mirror at VeraNala/Deliveroo.
>
> **Author:** Liza Carvelli
> **Purpose:** "Better Grand Company Deliveries"

## Prerequisites

```lua
-- Always check plugin availability first
if not HasPlugin("Deliveroo") then
    yield("/echo [Script] Deliveroo plugin not available")
    return
end
```

## IPC API Reference

**IMPORTANT:** Deliveroo has a very minimal IPC API - only 3 endpoints exist. Most control is done via slash commands.

### Verified IPC Methods (from source)

```lua
-- Check if turn-in is currently running
-- IPC Name: "Deliveroo.IsTurnInRunning"
IPC.Deliveroo.IsTurnInRunning() → boolean
```

### IPC Events (Subscribe only - cannot call directly)

These are notification events that Deliveroo sends when state changes:

```lua
-- Event sent when turn-in starts
-- IPC Name: "Deliveroo.TurnInStarted"
-- (Cannot call - listen only)

-- Event sent when turn-in stops
-- IPC Name: "Deliveroo.TurnInStopped"
-- (Cannot call - listen only)
```

## Chat Commands

Since Deliveroo's IPC is minimal, most control is done via slash commands:

```lua
-- Open Deliveroo window
yield("/deliveroo")

-- Start expert delivery (main use case)
yield("/deliveroo expert")

-- Stop current delivery operation
yield("/deliveroo stop")
```

## Usage Patterns

### Check if Turn-In is Running

```lua
function IsDeliverooRunning()
    if not HasPlugin("Deliveroo") then
        return false
    end

    local ok, result = pcall(function()
        return IPC.Deliveroo.IsTurnInRunning()
    end)

    return ok and result
end
```

### Start Expert Delivery via Command

```lua
function StartExpertDelivery()
    if not HasPlugin("Deliveroo") then
        yield("/echo [Script] Deliveroo not available")
        return false
    end

    -- Use slash command - IPC doesn't have start method
    yield("/deliveroo expert")
    yield("/wait 1")

    return true
end
```

### Wait for Delivery Complete

```lua
function WaitForDeliveryComplete(timeout)
    timeout = timeout or 300
    local startTime = os.clock()

    -- Initial wait for Deliveroo to start
    yield("/wait 2")

    while IsDeliverooRunning() and (os.clock() - startTime) < timeout do
        yield("/wait 1")
    end

    return not IsDeliverooRunning()
end
```

### Complete Delivery Workflow

```lua
function DoExpertDelivery(timeout)
    timeout = timeout or 300

    if not HasPlugin("Deliveroo") then
        yield("/echo [Script] ERROR: Deliveroo not available")
        return false
    end

    -- Check if already running
    if IsDeliverooRunning() then
        yield("/echo [Script] Deliveroo already running")
        return WaitForDeliveryComplete(timeout)
    end

    -- Start via command
    yield("/deliveroo expert")
    yield("/wait 2")

    -- Wait for completion
    if WaitForDeliveryComplete(timeout) then
        yield("/echo [Script] Expert delivery completed")
        return true
    else
        yield("/echo [Script] Expert delivery timed out")
        yield("/deliveroo stop")
        return false
    end
end
```

### Stop Delivery

```lua
function StopDelivery()
    -- Use slash command - IPC doesn't have stop method
    yield("/deliveroo stop")
    yield("/wait 0.5")
end
```

## Integration with Other Plugins

Deliveroo is often used with AutoRetainer for automated GC turn-ins:

```lua
-- Example: Expert delivery after retainer runs
function DoGCTurnInsAfterRetainers()
    -- Wait for retainer operations to complete first
    while IPC.AutoRetainer.IsBusy() do
        yield("/wait 5")
    end

    -- Do expert delivery
    DoExpertDelivery(300)
end
```

## GC Seal Information (Via Game Data)

Since Deliveroo doesn't expose seal information via IPC, use game data directly:

```lua
-- Get current GC seals from game
-- Note: This requires accessing game memory/addons, not Deliveroo IPC
-- Example using SND's built-in functions if available:
local seals = Player.GCSeals  -- If this API exists in SND
```

## Best Practices

1. **Use slash commands for control** - Deliveroo's IPC is minimal (status check only)
2. **Only IsTurnInRunning is callable** - Other methods in old docs were fabricated
3. **Add waits after commands** - Slash commands need processing time
4. **Use timeouts** when waiting for delivery completion
5. **Check plugin availability** before any Deliveroo operations

## What Deliveroo Does NOT Expose via IPC

The following methods were previously documented but **DO NOT EXIST** in the IPC:

- ~~`IPC.Deliveroo.IsBusy()`~~ - Use `IsTurnInRunning()` instead
- ~~`IPC.Deliveroo.GetTurnInStatus()`~~ - Not available
- ~~`IPC.Deliveroo.StartExpertDelivery()`~~ - Use `/deliveroo expert` command
- ~~`IPC.Deliveroo.Stop()`~~ - Use `/deliveroo stop` command
- ~~`IPC.Deliveroo.Pause()`~~ - Not available
- ~~`IPC.Deliveroo.Resume()`~~ - Not available
- ~~`IPC.Deliveroo.GetItemFilter()`~~ - Not available
- ~~`IPC.Deliveroo.SetItemFilter()`~~ - Not available
- ~~`IPC.Deliveroo.GetGCRankRequirement()`~~ - Not available
- ~~`IPC.Deliveroo.CanTurnInItem()`~~ - Not available
- ~~`IPC.Deliveroo.GetCurrentSeals()`~~ - Not available via IPC
- ~~`IPC.Deliveroo.GetMaxSeals()`~~ - Not available via IPC
- ~~`IPC.Deliveroo.GetSealCapForRank()`~~ - Not available via IPC

## Verification History

- **2025-12-11:** Verified against source code at VeraNala/Deliveroo (GitHub mirror)
- **Source file:** `Deliveroo/External/DeliverooIpc.cs`
- **Finding:** Only 3 IPC endpoints exist (1 callable method + 2 events)
