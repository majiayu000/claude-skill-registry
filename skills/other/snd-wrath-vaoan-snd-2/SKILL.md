---
name: SND WrathCombo Integration
description: Use this skill when implementing combat rotation automation in SND macros using the WrathCombo plugin. Covers auto-rotation control, combo state management, job configuration, and IPC leasing system.
---

# WrathCombo Integration for SND

This skill covers integration with the WrathCombo plugin for combat rotation automation in SND macros.

**Source:** Verified from official repository
- https://github.com/PunishXIV/WrathCombo/blob/main/WrathCombo/Services/IPC/Provider.cs
- https://github.com/PunishXIV/WrathCombo/blob/main/WrathCombo/Services/IPC/Leasing.cs
- https://github.com/PunishXIV/WrathCombo/blob/main/WrathCombo/Services/IPC/Enums.cs

## Prerequisites

```lua
-- Always check plugin availability first
if not HasPlugin("WrathCombo") then
    yield("/echo [Script] WrathCombo plugin not available")
    return
end
```

## Important: IPC Leasing System

WrathCombo uses a **leasing system** for IPC control. You must register for a lease before making any `Set` calls. This allows users to maintain control and revoke external plugin access.

## IPC API Reference

### Initialization and Status

```lua
-- Check if IPC is ready (caches built, fully initialized)
IPC.WrathCombo.IPCReady() → boolean

-- Test IPC connection
IPC.WrathCombo.Test() → nil  -- Logs "IPC connection successful"
```

### Lease Registration

```lua
-- Register for control of WrathCombo (required before Set calls)
-- Returns: Guid (lease ID) or nil if registration failed
IPC.WrathCombo.RegisterForLease(
    string internalPluginName,  -- Your plugin's internal name
    string pluginName           -- Display name shown to users
) → Guid?

-- Register with callback for lease cancellation
IPC.WrathCombo.RegisterForLeaseWithCallback(
    string internalPluginName,
    string pluginName,
    string? ipcPrefixForCallback  -- nil = same as internalPluginName
) → Guid?

-- Release your lease (call when done)
IPC.WrathCombo.ReleaseControl(Guid lease) → nil
```

### Auto-Rotation Control

```lua
-- Get current auto-rotation state
IPC.WrathCombo.GetAutoRotationState() → boolean

-- Set auto-rotation state (requires lease)
IPC.WrathCombo.SetAutoRotationState(
    Guid lease,
    boolean enabled  -- default: true
) → SetResult

-- Check if current job is ready for auto-rotation
-- (has Single-Target and Multi-Target combos configured in Auto-Mode)
IPC.WrathCombo.IsCurrentJobAutoRotationReady() → boolean

-- Configure current job for auto-rotation (requires lease)
-- Enables ST/MT combos and Auto-Mode using user's existing settings
IPC.WrathCombo.SetCurrentJobAutoRotationReady(Guid lease) → SetResult
```

### Job State Checks

```lua
-- Check if current job has ST/MT combos configured
IPC.WrathCombo.IsCurrentJobConfiguredOn() → Dictionary<ComboTargetTypeKeys, ComboSimplicityLevelKeys?>

-- Check if current job has ST/MT combos in Auto-Mode
IPC.WrathCombo.IsCurrentJobAutoModeOn() → Dictionary<ComboTargetTypeKeys, ComboSimplicityLevelKeys?>
```

### Fine-Grained Combo Control

```lua
-- Get all combo names for a job
IPC.WrathCombo.GetComboNamesForJob(number jobID) → List<string>?

-- Get all combo option names for a job
IPC.WrathCombo.GetComboOptionNamesForJob(number jobID) → Dictionary<string, List<string>>?

-- Get combo state (enabled + auto-mode)
IPC.WrathCombo.GetComboState(string comboInternalName) → Dictionary<ComboStateKeys, bool>?

-- Set combo state (requires lease)
IPC.WrathCombo.SetComboState(
    Guid lease,
    string comboInternalName,
    boolean comboState,  -- default: true
    boolean autoState    -- default: true
) → SetResult

-- Get combo option state
IPC.WrathCombo.GetComboOptionState(string optionName) → boolean

-- Set combo option state (requires lease)
IPC.WrathCombo.SetComboOptionState(
    Guid lease,
    string optionName,
    boolean state  -- default: true
) → SetResult
```

## Enums

### SetResult (Return codes for Set operations)
```lua
local SetResult = {
    IGNORED = -1,           -- Default, shouldn't be seen
    Okay = 0,               -- Success
    OkayWorking = 1,        -- Success, working asynchronously
    IPCDisabled = 10,       -- IPC services disabled
    InvalidLease = 11,      -- Invalid lease ID
    BlacklistedLease = 12,  -- Lease is blacklisted
    Duplicate = 13,         -- Already set to this value
    PlayerNotAvailable = 14,-- Player object not available
    InvalidConfiguration = 15, -- Config not available
    InvalidValue = 16,      -- Invalid value provided
}
```

### ComboStateKeys
```lua
local ComboStateKeys = {
    Enabled = 0,   -- Whether combo is enabled
    AutoMode = 1,  -- Whether combo is in Auto-Mode
}
```

### ComboTargetTypeKeys
```lua
local ComboTargetTypeKeys = {
    SingleTarget = 0,
    MultiTarget = 1,
    HealST = 2,      -- Healer single-target
    HealMT = 3,      -- Healer multi-target
    Other = 4,
}
```

### ComboSimplicityLevelKeys
```lua
local ComboSimplicityLevelKeys = {
    Simple = 0,
    Advanced = 1,
    Other = 2,
}
```

### CancellationReason (Why lease was cancelled)
```lua
local CancellationReason = {
    WrathUserManuallyCancelled = 0,  -- User revoked lease
    LeaseePluginDisabled = 1,        -- Your plugin was disabled
    WrathPluginDisabled = 2,         -- Wrath is being disabled
    LeaseeReleased = 3,              -- You released the lease
    AllServicesSuspended = 4,        -- IPC disabled remotely
    JobChanged = 5,                  -- Player changed jobs
}
```

## Chat Commands

```lua
-- Open WrathCombo window
yield("/wrath")

-- Enable/disable auto-rotation
yield("/wrath auto")      -- Toggle
yield("/wrath auto on")   -- Enable
yield("/wrath auto off")  -- Disable
```

## Usage Patterns

### Basic Auto-Rotation Control
```lua
function EnableWrathAutoRotation()
    if not HasPlugin("WrathCombo") then
        yield("/echo [Script] WrathCombo not available")
        return false
    end

    -- Check if ready
    if not IPC.WrathCombo.IPCReady() then
        yield("/echo [Script] WrathCombo IPC not ready")
        return false
    end

    -- Use chat command for simple toggle (no lease needed)
    yield("/wrath auto on")
    return true
end
```

### Full IPC Control with Lease
```lua
local wrathLease = nil

function RegisterWrathControl()
    if not HasPlugin("WrathCombo") then
        return false
    end

    if not IPC.WrathCombo.IPCReady() then
        return false
    end

    -- Register for lease
    wrathLease = IPC.WrathCombo.RegisterForLease(
        "YourPluginName",
        "Your Plugin Display Name"
    )

    if not wrathLease then
        yield("/echo [Script] Failed to get Wrath lease")
        return false
    end

    return true
end

function SetupAutoRotation()
    if not wrathLease then
        if not RegisterWrathControl() then
            return false
        end
    end

    -- Check if job is ready
    if not IPC.WrathCombo.IsCurrentJobAutoRotationReady() then
        -- Configure job for auto-rotation
        local result = IPC.WrathCombo.SetCurrentJobAutoRotationReady(wrathLease)
        if result ~= 0 and result ~= 1 then  -- Not Okay or OkayWorking
            yield("/echo [Script] Failed to setup job: " .. result)
            return false
        end
    end

    -- Enable auto-rotation
    local result = IPC.WrathCombo.SetAutoRotationState(wrathLease, true)
    return result == 0 or result == 1
end

function ReleaseWrathControl()
    if wrathLease then
        IPC.WrathCombo.ReleaseControl(wrathLease)
        wrathLease = nil
    end
end
```

### Check Job Readiness
```lua
function IsJobReadyForCombat()
    if not HasPlugin("WrathCombo") then
        return false
    end

    return IPC.WrathCombo.IsCurrentJobAutoRotationReady()
end
```

## Auto-Rotation Config Options

These options can be configured via IPC (from `AutoRotationConfigOption` enum):

| Option | Type | Description |
|--------|------|-------------|
| InCombatOnly | bool | Only run in combat |
| DPSRotationMode | enum | DPS rotation behavior |
| HealerRotationMode | enum | Healer rotation behavior |
| FATEPriority | bool | Prioritize FATE targets |
| QuestPriority | bool | Prioritize quest targets |
| SingleTargetHPP | int | Single target HP% threshold |
| AoETargetHPP | int | AoE target HP% threshold |
| SingleTargetRegenHPP | int | Regen HP% threshold |
| ManageKardia | bool | Auto-manage Kardia (SGE) |
| AutoRez | bool | Auto-resurrect |
| AutoRezDPSJobs | bool | Rez as DPS jobs |
| AutoCleanse | bool | Auto-cleanse debuffs |
| IncludeNPCs | bool | Include NPCs in healing |
| OnlyAttackInCombat | bool | Only attack in combat |
| OrbwalkerIntegration | bool | Orbwalker integration |
| AutoRezOutOfParty | bool | Auto-rez out of party members |
| DPSAoETargets | int | AoE target count threshold |
| SingleTargetExcogHPP | int | Excogitation HP% threshold |
| AutoRezDPSJobsHealersOnly | bool | Rez DPS jobs only when healer |

## Best Practices

1. **Always check `IPCReady()`** before using IPC methods
2. **Register for a lease** before making any `Set` calls
3. **Release your lease** when done to be a good citizen
4. **Handle lease cancellation** - users can revoke at any time
5. **Check `IsCurrentJobAutoRotationReady()`** before expecting auto-rotation to work
6. **Use chat commands** for simple on/off toggles without needing a lease
7. **Don't mix IPC with PvP** - IPC doesn't work correctly in PvP

## Notes

- IPC uses a leasing system to give users control over external access
- Leases can be revoked by users at any time
- Job changes will cancel leases (reason: JobChanged)
- `SetCurrentJobAutoRotationReady` works asynchronously and may take several seconds
