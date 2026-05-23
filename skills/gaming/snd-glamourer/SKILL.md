---
name: SND Glamourer Integration
description: Use this skill when implementing glamour/appearance automation in SND macros using the Glamourer plugin. Covers glamour application, design management, and appearance state.
---

# Glamourer Integration for SND

This skill covers integration with the Glamourer plugin for appearance/glamour automation in SND macros.

> **Source:** https://github.com/Ottermandias/Glamourer/blob/main/Glamourer/Api/IpcProviders.cs

## Prerequisites

```lua
-- Always check plugin availability first
if not HasPlugin("Glamourer") then
    yield("/echo [Script] Glamourer plugin not available")
    return
end
```

## IPC API Reference

All methods use the IPC namespace and follow the pattern `IPC.Glamourer.<MethodName>()`.

### API Version
```lua
-- Get API version (major, minor)
IPC.Glamourer.ApiVersion() → (int, int)

-- Get API major version (legacy)
IPC.Glamourer.ApiVersion() → int
```

### Design Management
```lua
-- Get all designs as GUID → name dictionary
IPC.Glamourer.GetDesignList() → table<Guid, string>

-- Get extended design information (name, path, color, quick design bar flag)
IPC.Glamourer.GetDesignListExtended() → table<Guid, (string, string, uint, bool)>

-- Get extended data for a specific design
IPC.Glamourer.GetExtendedDesignData(Guid designId) → (string, string, uint, bool)

-- Get design as Base64 string
IPC.Glamourer.GetDesignBase64(Guid designId) → string?

-- Get design as JSON object
IPC.Glamourer.GetDesignJObject(Guid designId) → JObject?

-- Add a new design from Base64 or JSON string
IPC.Glamourer.AddDesign(string designData, string name) → (GlamourerApiEc, Guid)

-- Delete a design by GUID
IPC.Glamourer.DeleteDesign(Guid designId) → GlamourerApiEc
```

### Design Application
```lua
-- Apply design by GUID to object index
IPC.Glamourer.ApplyDesign(Guid designId, int objectIndex, uint key, ApplyFlag flags) → GlamourerApiEc

-- Apply design by GUID to character by name
IPC.Glamourer.ApplyDesignName(Guid designId, string playerName, uint key, ApplyFlag flags) → GlamourerApiEc
```

### Item Manipulation
```lua
-- Set equipment item by object index
IPC.Glamourer.SetItem(int objectIndex, ApiEquipSlot slot, ulong itemId, IReadOnlyList<byte> stains, uint key, ApplyFlag flags) → GlamourerApiEc

-- Set equipment item by character name
IPC.Glamourer.SetItemName(string playerName, ApiEquipSlot slot, ulong itemId, IReadOnlyList<byte> stains, uint key, ApplyFlag flags) → GlamourerApiEc

-- Set bonus item (glasses) by object index
IPC.Glamourer.SetBonusItem(int objectIndex, ApiBonusSlot slot, ulong bonusItemId, uint key, ApplyFlag flags) → GlamourerApiEc

-- Set bonus item by character name
IPC.Glamourer.SetBonusItemName(string playerName, ApiBonusSlot slot, ulong bonusItemId, uint key, ApplyFlag flags) → GlamourerApiEc

-- Set meta state (visibility flags) by object index
IPC.Glamourer.SetMetaState(int objectIndex, MetaFlag types, bool newValue, uint key, ApplyFlag flags) → GlamourerApiEc

-- Set meta state by character name
IPC.Glamourer.SetMetaStateName(string playerName, MetaFlag types, bool newValue, uint key, ApplyFlag flags) → GlamourerApiEc
```

### State Management
```lua
-- Get current state as JSON by object index
IPC.Glamourer.GetState(int objectIndex, uint key) → (GlamourerApiEc, JObject?)

-- Get current state as JSON by character name
IPC.Glamourer.GetStateName(string playerName, uint key) → (GlamourerApiEc, JObject?)

-- Get current state as Base64 by object index
IPC.Glamourer.GetStateBase64(int objectIndex, uint key) → (GlamourerApiEc, string?)

-- Get current state as Base64 by character name
IPC.Glamourer.GetStateBase64Name(string playerName, uint key) → (GlamourerApiEc, string?)

-- Apply state from Base64 or JSON by object index
IPC.Glamourer.ApplyState(object applyState, int objectIndex, uint key, ApplyFlag flags) → GlamourerApiEc

-- Apply state from Base64 or JSON by character name
IPC.Glamourer.ApplyStateName(object applyState, string playerName, uint key, ApplyFlag flags) → GlamourerApiEc

-- Revert state to game default by object index
IPC.Glamourer.RevertState(int objectIndex, uint key, ApplyFlag flags) → GlamourerApiEc

-- Revert state to game default by character name
IPC.Glamourer.RevertStateName(string playerName, uint key, ApplyFlag flags) → GlamourerApiEc

-- Unlock state by object index (remove IPC lock)
IPC.Glamourer.UnlockState(int objectIndex, uint key) → GlamourerApiEc

-- Unlock state by character name
IPC.Glamourer.UnlockStateName(string playerName, uint key) → GlamourerApiEc

-- Delete saved player state
IPC.Glamourer.DeletePlayerState(string playerName, ushort worldId, uint key) → GlamourerApiEc

-- Unlock all states with given key
IPC.Glamourer.UnlockAll(uint key) → int

-- Revert to automation design by object index
IPC.Glamourer.RevertToAutomation(int objectIndex, uint key, ApplyFlag flags) → GlamourerApiEc

-- Revert to automation design by character name
IPC.Glamourer.RevertToAutomationName(string playerName, uint key, ApplyFlag flags) → GlamourerApiEc
```

### Events (Subscribable)
```lua
-- Fired when state changes (actor address)
IPC.Glamourer.StateChanged → event Action<nint>

-- Fired when state changes with type information
IPC.Glamourer.StateChangedWithType → event Action<IntPtr, StateChangeType>

-- Fired when state is finalized
IPC.Glamourer.StateFinalized → event Action<IntPtr, StateFinalizationType>

-- Fired when GPose state changes
IPC.Glamourer.GPoseChanged → event Action<bool>
```

### Return Codes (GlamourerApiEc)
```
Success = 0           -- Operation succeeded
InvalidState = 1      -- State data is invalid
DesignNotFound = 2    -- Design GUID not found
ActorNotFound = 3     -- Actor/character not found
ActorNotHuman = 4     -- Actor is not human (minion, pet, etc)
InvalidKey = 5        -- Key doesn't match lock
ItemInvalid = 6       -- Item ID is invalid
NothingDone = 7       -- No changes were made
CouldNotParse = 8     -- Failed to parse design data
UnknownError = 9      -- Unknown error occurred
```

### Apply Flags
```
None = 0              -- No special flags
Once = 1              -- Apply once (manual), not persistent
Equipment = 2         -- Apply equipment only
Customization = 4     -- Apply customization only
```

### Equipment Slots (ApiEquipSlot)
```
Head = 0, Body = 1, Hands = 2, Legs = 3, Feet = 4
Ears = 5, Neck = 6, Wrists = 7, RFinger = 8, LFinger = 9
MainHand = 10, OffHand = 11
```

### Bonus Slots (ApiBonusSlot)
```
Glasses = 0
```

## Usage Patterns

### Apply Glamour Design by GUID
```lua
function ApplyDesignByGuid(designGuid)
    if not HasPlugin("Glamourer") then
        return false
    end

    local playerName = Svc.ClientState.LocalPlayer.Name.TextValue
    local key = 0  -- 0 = no lock
    local flags = 0  -- ApplyFlag.None

    local result = IPC.Glamourer.ApplyDesignName(designGuid, playerName, key, flags)
    return result == 0  -- GlamourerApiEc.Success
end
```

### Find Design by Name and Apply
```lua
function ApplyDesignByName(designName)
    if not HasPlugin("Glamourer") then
        yield("/echo [Script] Glamourer not available")
        return false
    end

    -- Get all designs
    local designs = IPC.Glamourer.GetDesignList()

    -- Find design with matching name
    local foundGuid = nil
    for guid, name in pairs(designs) do
        if name == designName then
            foundGuid = guid
            break
        end
    end

    if not foundGuid then
        yield("/echo [Script] Design '" .. designName .. "' not found")
        return false
    end

    -- Apply the design
    local playerName = Svc.ClientState.LocalPlayer.Name.TextValue
    local result = IPC.Glamourer.ApplyDesignName(foundGuid, playerName, 0, 0)

    return result == 0  -- Success
end
```

### Revert to Game Default
```lua
function RevertGlamour()
    if not HasPlugin("Glamourer") then
        return false
    end

    local playerName = Svc.ClientState.LocalPlayer.Name.TextValue
    local key = 0
    local flags = 6  -- ApplyFlag.Equipment | ApplyFlag.Customization

    local result = IPC.Glamourer.RevertStateName(playerName, key, flags)
    return result == 0  -- Success
end
```

### Apply Design with Lock (Prevent Automation Override)
```lua
function ApplyDesignWithLock(designGuid, lockKey)
    if not HasPlugin("Glamourer") then
        return false
    end

    local playerName = Svc.ClientState.LocalPlayer.Name.TextValue
    local flags = 0  -- Persistent application

    local result = IPC.Glamourer.ApplyDesignName(designGuid, playerName, lockKey, flags)
    return result == 0
end

-- Later, unlock when done
function UnlockDesign(lockKey)
    local playerName = Svc.ClientState.LocalPlayer.Name.TextValue
    IPC.Glamourer.UnlockStateName(playerName, lockKey)
end
```

### Set Individual Equipment Item
```lua
function SetWeapon(itemId, stainId)
    if not HasPlugin("Glamourer") then
        return false
    end

    local playerName = Svc.ClientState.LocalPlayer.Name.TextValue
    local slot = 10  -- ApiEquipSlot.MainHand
    local stains = {stainId or 0}
    local key = 0
    local flags = 1  -- ApplyFlag.Once (manual, not persistent)

    local result = IPC.Glamourer.SetItemName(playerName, slot, itemId, stains, key, flags)
    return result == 0
end
```

## Common Use Cases

### Job-Based Glamour Switching
```lua
-- Build a lookup table of job ID to design GUID
local JobDesigns = {}

function InitJobDesigns()
    -- Get all designs from Glamourer
    local designs = IPC.Glamourer.GetDesignList()

    -- Map designs to jobs based on naming convention
    -- Assumes designs are named like "PLD_Combat", "WAR_Combat", etc.
    for guid, name in pairs(designs) do
        if name:match("^PLD_") then
            JobDesigns[19] = guid  -- Paladin
        elseif name:match("^WAR_") then
            JobDesigns[21] = guid  -- Warrior
        elseif name:match("^DRK_") then
            JobDesigns[32] = guid  -- Dark Knight
        elseif name:match("^GNB_") then
            JobDesigns[37] = guid  -- Gunbreaker
        end
        -- Add more jobs as needed
    end
end

function ApplyJobGlamour()
    local jobId = Svc.ClientState.LocalPlayer.ClassJob.Id
    local designGuid = JobDesigns[jobId]

    if designGuid then
        local playerName = Svc.ClientState.LocalPlayer.Name.TextValue
        IPC.Glamourer.ApplyDesignName(designGuid, playerName, 0, 0)
    end
end
```

### Automation Integration
```lua
-- Apply crafting glamour before crafting session
function StartCraftingSession()
    if not HasPlugin("Glamourer") then
        return
    end

    -- Find crafting design
    local designs = IPC.Glamourer.GetDesignList()
    local craftingGuid = nil
    for guid, name in pairs(designs) do
        if name == "Crafting_Outfit" then
            craftingGuid = guid
            break
        end
    end

    if craftingGuid then
        local playerName = Svc.ClientState.LocalPlayer.Name.TextValue
        IPC.Glamourer.ApplyDesignName(craftingGuid, playerName, 0, 0)
        yield("/wait 0.5")
    end

    -- Continue with crafting...
end

-- Revert after automation completes
function EndAutomation()
    if HasPlugin("Glamourer") then
        local playerName = Svc.ClientState.LocalPlayer.Name.TextValue
        IPC.Glamourer.RevertStateName(playerName, 0, 6)  -- Revert equipment and customization
    end
end
```

## Best Practices

1. **Work with GUIDs, not names** - Use `GetDesignList()` to find designs by name, then use the GUID for operations
2. **Check return codes** - All APIs return `GlamourerApiEc` status codes; check for `Success = 0`
3. **Use appropriate flags** - Use `ApplyFlag.Once = 1` for temporary manual changes, `0` for persistent changes
4. **Handle locks properly** - Use unique keys when locking states, and always unlock when done
5. **Use consistent naming** for designs (e.g., "JobName_Combat", "Crafter_Outfit") for easier lookups
6. **Revert or unlock** when automation completes for a clean state
7. **Add short waits** after applying glamours if subsequent actions depend on appearance
8. **Use player name methods** - `ApplyDesignName()`, `SetItemName()`, etc. are easier than object index methods

## Important Notes

### Design GUIDs vs Names
- Designs are identified by GUID internally
- Use `GetDesignList()` to map names to GUIDs
- Store GUIDs in config for better performance (avoid repeated lookups)

### Locking Mechanism
- The `key` parameter prevents other sources from modifying the state
- Use `key = 0` for no lock (allows automation/other plugins to change appearance)
- Use a unique key (e.g., your macro's hash) to lock and prevent changes
- Always unlock (`UnlockState`/`UnlockStateName`) when done

### Apply Flags Explained
- `Once = 1`: Temporary manual change (doesn't persist, won't override automation)
- `Equipment = 2`: Only apply equipment changes
- `Customization = 4`: Only apply customization (face, body, etc)
- Combine with bitwise OR: `Equipment | Customization = 6` for both

### Actor vs Player Name Methods
- **By Index** (`ApplyDesign`, `SetItem`): Requires object index, works on any actor
- **By Name** (`ApplyDesignName`, `SetItemName`): Easier for player character, searches by name
- Use name methods for player macros, index methods for targeting other actors
