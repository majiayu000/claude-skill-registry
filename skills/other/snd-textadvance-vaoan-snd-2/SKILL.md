---
name: SND TextAdvance Integration
description: Use this skill when implementing automatic dialog/cutscene advancement in SND macros using the TextAdvance plugin. Covers dialog control, cutscene skipping, and quest interaction automation.
---

# TextAdvance Integration for SND

This skill covers integration with the TextAdvance plugin for automatic dialog and cutscene advancement in SND macros.

> **Source:** https://github.com/NightmareXIV/TextAdvance/blob/master/TextAdvance/Services/IPCProvider.cs

## Prerequisites

```lua
-- Always check plugin availability first
if not HasPlugin("TextAdvance") then
    yield("/echo [Script] TextAdvance plugin not available")
    StopFlag = true
    return
end
```

## Plugin Availability

```lua
--- Check if TextAdvance is available
-- @return boolean - True if available
function HasTextAdvance()
    for plugin in luanet.each(Svc.PluginInterface.InstalledPlugins) do
        if plugin.InternalName == "TextAdvance" and plugin.IsLoaded then
            return true
        end
    end
    return false
end

--- Check if TextAdvance IPC is available
-- @return boolean - True if IPC available
function IsTextAdvanceIPCAvailable()
    return IPC.TextAdvance ~= nil
end
```

## Official IPC API Reference

### State Query Methods

```lua
--- Check if TextAdvance is enabled
-- @return boolean - True if enabled
IPC.TextAdvance.IsEnabled()

--- Check if TextAdvance is paused (blocklisted)
-- @return boolean - True if paused
IPC.TextAdvance.IsPaused()

--- Check if in external control mode
-- @return boolean - True if under external control
IPC.TextAdvance.IsInExternalControl()

--- Check if TextAdvance task manager is busy
-- @return boolean - True if busy with movement/interaction
IPC.TextAdvance.IsBusy()
```

### Configuration Query Methods

```lua
--- Check if quest accept is enabled
-- @return boolean - True if enabled
IPC.TextAdvance.GetEnableQuestAccept()

--- Check if quest complete is enabled
-- @return boolean - True if enabled
IPC.TextAdvance.GetEnableQuestComplete()

--- Check if reward pick is enabled
-- @return boolean - True if enabled
IPC.TextAdvance.GetEnableRewardPick()

--- Check if cutscene ESC is enabled
-- @return boolean - True if enabled
IPC.TextAdvance.GetEnableCutsceneEsc()

--- Check if cutscene skip confirm is enabled
-- @return boolean - True if enabled
IPC.TextAdvance.GetEnableCutsceneSkipConfirm()

--- Check if request hand-in is enabled
-- @return boolean - True if enabled
IPC.TextAdvance.GetEnableRequestHandin()

--- Check if request fill is enabled
-- @return boolean - True if enabled
IPC.TextAdvance.GetEnableRequestFill()

--- Check if talk skip is enabled
-- @return boolean - True if enabled
IPC.TextAdvance.GetEnableTalkSkip()

--- Check if auto-interact is enabled
-- @return boolean - True if enabled
IPC.TextAdvance.GetEnableAutoInteract()
```

### External Control Methods

```lua
--- Enable external control of TextAdvance
-- @param requester string - Unique identifier for the requester
-- @param config table - ExternalTerritoryConfig object
-- @return boolean - True if control was acquired
IPC.TextAdvance.EnableExternalControl(requester, config)

--- Disable external control of TextAdvance
-- @param requester string - Unique identifier (must match EnableExternalControl)
-- @return boolean - True if control was released
IPC.TextAdvance.DisableExternalControl(requester)
```

### Movement and Interaction Methods

```lua
--- Enqueue move and interact with target
-- @param moveData table - MoveData object with position, dataID, noInteract
-- MoveData structure:
--   {
--     Position = Vector3(x, y, z),  -- Destination position
--     DataID = uint,                 -- Object DataID (0 for any targetable)
--     NoInteract = boolean,          -- If true, don't interact after moving
--     Mount = boolean or nil,        -- Force mount state (nil = auto)
--     Fly = boolean or nil           -- Force fly state (nil = auto)
--   }
IPC.TextAdvance.EnqueueMoveAndInteract(moveData)

--- Enqueue move to 2D point (ignores Y coordinate)
-- @param moveData table - MoveData object
-- @param distance number - Distance threshold to consider "arrived"
IPC.TextAdvance.EnqueueMoveTo2DPoint(moveData, distance)

--- Enqueue move to 3D point (includes Y coordinate)
-- @param moveData table - MoveData object
-- @param distance number - Distance threshold to consider "arrived"
IPC.TextAdvance.EnqueueMoveTo3DPoint(moveData, distance)

--- Stop all movement and interaction tasks
IPC.TextAdvance.Stop()
```

### Example: Using IPC Methods

```lua
--- Check if TextAdvance will handle quest dialogs
function WillAutoAcceptQuest()
    if not HasPlugin("TextAdvance") then
        return false
    end

    return IPC.TextAdvance.IsEnabled() and
           IPC.TextAdvance.GetEnableQuestAccept() and
           not IPC.TextAdvance.IsPaused()
end

--- Move to NPC and interact using TextAdvance IPC
-- @param x number - X coordinate
-- @param y number - Y coordinate
-- @param z number - Z coordinate
-- @param dataId number - NPC DataID (0 for any targetable at position)
-- @return boolean - True if task was enqueued
function MoveAndInteractWithNPC(x, y, z, dataId)
    if not HasPlugin("TextAdvance") then
        return false
    end

    local moveData = {
        Position = Vector3(x, y, z),
        DataID = dataId or 0,
        NoInteract = false,
        Mount = nil,  -- Let TextAdvance decide
        Fly = nil     -- Let TextAdvance decide
    }

    IPC.TextAdvance.EnqueueMoveAndInteract(moveData)

    -- Wait for task to start
    yield("/wait 0.5")

    -- Wait for completion
    while IPC.TextAdvance.IsBusy() do
        yield("/wait 0.5")
    end

    return true
end

--- External control example (advanced)
function TakeControlOfTextAdvance()
    local requester = "MyScript"
    local config = {
        -- ExternalTerritoryConfig structure
        -- (See TextAdvance source for details)
    }

    local success = IPC.TextAdvance.EnableExternalControl(requester, config)
    if success then
        yield("/echo [Script] TextAdvance external control acquired")
    end

    return success
end

function ReleaseControlOfTextAdvance()
    local requester = "MyScript"
    IPC.TextAdvance.DisableExternalControl(requester)
    yield("/echo [Script] TextAdvance external control released")
end
```

## TextAdvance Control Commands

**Note:** Most users should use the command-based control methods below. The IPC methods above are primarily for advanced scenarios like external control, state queries, and integrated movement/interaction systems.

### Enable/Disable TextAdvance

```lua
--- Enable TextAdvance auto-advance
-- @return boolean - True if command sent
function EnableTextAdvance()
    if not HasTextAdvance() then
        yield("/echo [Script] TextAdvance not available")
        return false
    end

    yield("/at e")  -- Alternative: "/textadvance enable"
    yield("/wait 0.2")
    return true
end

--- Disable TextAdvance auto-advance
-- @return boolean - True if command sent
function DisableTextAdvance()
    if not HasTextAdvance() then
        return false
    end

    yield("/at d")  -- Alternative: "/textadvance disable"
    yield("/wait 0.2")
    return true
end

--- Toggle TextAdvance
-- @return boolean - True if command sent
function ToggleTextAdvance()
    if not HasTextAdvance() then
        return false
    end

    yield("/at")  -- Toggle command
    yield("/wait 0.2")
    return true
end
```

### Advanced Commands

```lua
--- Enable quick dialog (faster advancement)
-- @return boolean - True if command sent
function EnableQuickDialog()
    if not HasTextAdvance() then
        return false
    end

    yield("/at qd on")
    yield("/wait 0.2")
    return true
end

--- Disable quick dialog
-- @return boolean - True if command sent
function DisableQuickDialog()
    if not HasTextAdvance() then
        return false
    end

    yield("/at qd off")
    yield("/wait 0.2")
    return true
end

--- Enable cutscene skip
-- @return boolean - True if command sent
function EnableCutsceneSkip()
    if not HasTextAdvance() then
        return false
    end

    yield("/at cs on")
    yield("/wait 0.2")
    return true
end

--- Disable cutscene skip
-- @return boolean - True if command sent
function DisableCutsceneSkip()
    if not HasTextAdvance() then
        return false
    end

    yield("/at cs off")
    yield("/wait 0.2")
    return true
end

--- Enable auto-accept quests
-- @return boolean - True if command sent
function EnableAutoAcceptQuest()
    if not HasTextAdvance() then
        return false
    end

    yield("/at qa on")
    yield("/wait 0.2")
    return true
end

--- Disable auto-accept quests
-- @return boolean - True if command sent
function DisableAutoAcceptQuest()
    if not HasTextAdvance() then
        return false
    end

    yield("/at qa off")
    yield("/wait 0.2")
    return true
end
```

## Dialog State Detection

### Check Dialog Addons

```lua
--- Check if any dialog addon is visible
-- @return boolean, string - True and addon name if dialog is open
function IsDialogOpen()
    local dialogAddons = {
        "Talk",
        "SelectString",
        "SelectYesno",
        "SelectIconString",
        "CutSceneSelectString",
        "JournalDetail",
        "JournalResult",
        "Request",
    }

    for _, addonName in ipairs(dialogAddons) do
        if IsAddonVisible(addonName) then
            return true, addonName
        end
    end

    return false, nil
end

--- Check if Talk addon is visible
-- @return boolean - True if visible
function IsTalkOpen()
    return IsAddonVisible("Talk")
end

--- Check if cutscene is playing
-- @return boolean - True if in cutscene
function IsInCutscene()
    local CharacterCondition = {
        watchingCutscene = 10,
        watchingCutscene2 = 11,
        dutyRecorderPlayback = 98,
    }

    return Svc.Condition[CharacterCondition.watchingCutscene] or
           Svc.Condition[CharacterCondition.watchingCutscene2] or
           Svc.Condition[CharacterCondition.dutyRecorderPlayback]
end

--- Check if in quest interaction
-- @return boolean - True if in quest event
function IsInQuestEvent()
    local CharacterCondition = {
        occupiedInQuestEvent = 32,
        occupiedInEvent = 31,
    }

    return Svc.Condition[CharacterCondition.occupiedInQuestEvent] or
           Svc.Condition[CharacterCondition.occupiedInEvent]
end

--- Helper function to check addon visibility
-- @param addonName string - Name of the addon
-- @return boolean - True if visible
function IsAddonVisible(addonName)
    local addon = Addons.GetAddon(addonName)
    return addon and addon.Ready and addon.Visible
end
```

## Quest Interaction Patterns

### NPC Interaction with TextAdvance

```lua
--- Interact with NPC and wait for dialog with TextAdvance handling
-- @param npcName string - Name of the NPC (optional, uses target)
-- @param timeout number - Maximum wait time (default: 30)
-- @return boolean - True if interaction completed
function InteractWithNPC(npcName, timeout)
    timeout = timeout or 30

    -- Enable TextAdvance for this interaction
    EnableTextAdvance()

    -- Interact
    if npcName then
        yield("/target " .. npcName)
        yield("/wait 0.3")
    end

    yield("/interact")

    -- Wait for dialog to appear
    local startTime = os.clock()
    while (os.clock() - startTime) < timeout do
        local dialogOpen, addonName = IsDialogOpen()

        if dialogOpen then
            yield("/echo [Script] Dialog opened: " .. (addonName or "Unknown"))
            return true
        end

        -- Check if in quest event
        if IsInQuestEvent() then
            return true
        end

        yield("/wait 0.5")
    end

    yield("/echo [Script] NPC interaction timeout")
    return false
end

--- Wait for dialog to close (interaction complete)
-- @param timeout number - Maximum wait time (default: 60)
-- @return boolean - True if dialog closed
function WaitForDialogClose(timeout)
    timeout = timeout or 60
    local startTime = os.clock()

    while (os.clock() - startTime) < timeout do
        local dialogOpen = IsDialogOpen()

        if not dialogOpen and not IsInQuestEvent() and not IsInCutscene() then
            return true
        end

        yield("/wait 0.5")
    end

    return false
end

--- Complete NPC interaction (interact and wait for completion)
-- @param npcName string - Name of the NPC (optional)
-- @param timeout number - Maximum wait time (default: 60)
-- @return boolean - True if interaction fully completed
function CompleteNPCInteraction(npcName, timeout)
    timeout = timeout or 60

    -- Interact with NPC
    if not InteractWithNPC(npcName, 10) then
        return false
    end

    -- Wait for dialog/interaction to complete
    return WaitForDialogClose(timeout)
end
```

### Quest Workflow

```lua
--- Accept a quest from NPC
-- @param npcName string - Quest giver NPC name (optional)
-- @param timeout number - Timeout (default: 60)
-- @return boolean - True if quest accepted
function AcceptQuest(npcName, timeout)
    timeout = timeout or 60

    -- Enable auto-accept
    EnableAutoAcceptQuest()
    EnableTextAdvance()

    -- Interact with quest giver
    if not InteractWithNPC(npcName, 10) then
        return false
    end

    -- Wait for quest acceptance to complete
    local startTime = os.clock()
    while (os.clock() - startTime) < timeout do
        -- Check if JournalDetail opened (quest offered)
        if IsAddonVisible("JournalDetail") then
            -- TextAdvance should auto-accept, but we can force it
            yield("/wait 0.5")
            if IsAddonVisible("JournalDetail") then
                yield("/click JournalDetail Accept")
            end
        end

        -- Check if dialog closed (quest accepted)
        if not IsDialogOpen() and not IsInQuestEvent() then
            yield("/echo [Script] Quest accepted")
            return true
        end

        yield("/wait 0.5")
    end

    return false
end

--- Complete/turn in a quest
-- @param npcName string - NPC name (optional)
-- @param timeout number - Timeout (default: 60)
-- @return boolean - True if quest completed
function CompleteQuest(npcName, timeout)
    timeout = timeout or 60

    EnableTextAdvance()

    -- Interact with NPC
    if not InteractWithNPC(npcName, 10) then
        return false
    end

    -- Wait for completion dialog
    local startTime = os.clock()
    while (os.clock() - startTime) < timeout do
        -- Check if JournalResult opened (quest completion)
        if IsAddonVisible("JournalResult") then
            yield("/wait 0.5")
            if IsAddonVisible("JournalResult") then
                yield("/click JournalResult Complete")
            end
        end

        -- Check if Request addon appeared (item turn-in)
        if IsAddonVisible("Request") then
            yield("/wait 0.5")
            yield("/click Request HandIn")
        end

        -- Check if dialog closed (quest completed)
        if not IsDialogOpen() and not IsInQuestEvent() then
            yield("/echo [Script] Quest completed")
            return true
        end

        yield("/wait 0.5")
    end

    return false
end
```

## Cutscene Handling

### Cutscene Skip

```lua
--- Skip current cutscene
-- @param timeout number - Timeout (default: 30)
-- @return boolean - True if cutscene ended
function SkipCutscene(timeout)
    timeout = timeout or 30

    if not IsInCutscene() then
        return true  -- Not in cutscene
    end

    EnableCutsceneSkip()

    local startTime = os.clock()
    while IsInCutscene() and (os.clock() - startTime) < timeout do
        -- Try to skip
        yield("/click SelectYesno Yes")  -- Confirm skip if prompted
        yield("/wait 0.5")
    end

    return not IsInCutscene()
end

--- Wait for cutscene to end (with auto-skip enabled)
-- @param timeout number - Timeout (default: 120)
-- @return boolean - True if cutscene ended
function WaitForCutsceneEnd(timeout)
    timeout = timeout or 120
    local startTime = os.clock()

    while IsInCutscene() and (os.clock() - startTime) < timeout do
        yield("/wait 1")
    end

    return not IsInCutscene()
end
```

## TextAdvance Configuration Presets

### Automation Presets

```lua
--- Configure TextAdvance for full automation
function ConfigureForFullAutomation()
    if not HasTextAdvance() then
        return false
    end

    EnableTextAdvance()
    EnableQuickDialog()
    EnableCutsceneSkip()
    EnableAutoAcceptQuest()

    yield("/echo [Script] TextAdvance configured for full automation")
    return true
end

--- Configure TextAdvance for manual play
function ConfigureForManualPlay()
    if not HasTextAdvance() then
        return false
    end

    DisableTextAdvance()
    DisableQuickDialog()
    DisableCutsceneSkip()
    DisableAutoAcceptQuest()

    yield("/echo [Script] TextAdvance disabled for manual play")
    return true
end

--- Configure TextAdvance for quest grinding
function ConfigureForQuestGrinding()
    if not HasTextAdvance() then
        return false
    end

    EnableTextAdvance()
    EnableQuickDialog()
    EnableCutsceneSkip()
    EnableAutoAcceptQuest()

    yield("/echo [Script] TextAdvance configured for quest grinding")
    return true
end

--- Configure TextAdvance for story content
function ConfigureForStoryContent()
    if not HasTextAdvance() then
        return false
    end

    DisableTextAdvance()  -- Let player read dialog
    DisableCutsceneSkip()  -- Watch cutscenes
    DisableAutoAcceptQuest()  -- Manual quest acceptance

    yield("/echo [Script] TextAdvance configured for story content")
    return true
end
```

## Integration with Other Plugins

### TextAdvance + Lifestream

```lua
--- Teleport and talk to NPC
-- @param aetheryteId number - Aetheryte to teleport to
-- @param npcName string - NPC to talk to
-- @return boolean - True if successful
function TeleportAndTalkToNPC(aetheryteId, npcName)
    -- Enable TextAdvance
    EnableTextAdvance()

    -- Teleport
    if IPC.Lifestream then
        yield("/tp " .. aetheryteId)

        -- Wait for teleport
        yield("/wait 3")
        while Svc.Condition[45] do  -- BetweenAreas
            yield("/wait 1")
        end
        yield("/wait 2")
    end

    -- Navigate and talk
    return CompleteNPCInteraction(npcName, 60)
end
```

### TextAdvance + vnavmesh

```lua
--- Navigate to NPC and interact
-- @param position Vector3 - NPC position
-- @param npcName string - NPC name
-- @return boolean - True if successful
function NavigateAndInteract(position, npcName)
    -- Enable TextAdvance
    EnableTextAdvance()

    -- Navigate to position
    if IPC.vnavmesh then
        IPC.vnavmesh.PathfindAndMoveTo(position, false)

        -- Wait for arrival
        local timeout = 60
        local startTime = os.clock()
        while IPC.vnavmesh.IsRunning() and (os.clock() - startTime) < timeout do
            yield("/wait 0.5")
        end
    end

    -- Interact with NPC
    return CompleteNPCInteraction(npcName, 60)
end
```

## State Machine Integration

```lua
CharacterState = {
    idle = Idle,
    interacting = Interacting,
    inCutscene = InCutscene,
    -- ... other states
}

function Interacting()
    -- TextAdvance handles dialogs automatically
    -- Just wait for interaction to complete

    if not IsDialogOpen() and not IsInQuestEvent() then
        yield("/echo [Script] Interaction complete")
        DisableTextAdvance()
        State = CharacterState.idle
        return
    end

    -- Check for cutscene transition
    if IsInCutscene() then
        State = CharacterState.inCutscene
        return
    end

    -- Still interacting, stay in this state
end

function InCutscene()
    -- TextAdvance with cutscene skip enabled handles this
    -- Just wait for cutscene to end

    if not IsInCutscene() then
        yield("/echo [Script] Cutscene ended")
        State = CharacterState.idle
        return
    end

    -- Still in cutscene
end
```

## Error Handling

```lua
--- Safe TextAdvance command
-- @param command string - TextAdvance command
-- @return boolean - True if command sent
function SafeTextAdvanceCommand(command)
    if not HasTextAdvance() then
        yield("/echo [Script] TextAdvance not available")
        return false
    end

    local success = pcall(function()
        yield(command)
    end)

    return success
end

--- Interaction with timeout and retry
-- @param interactFunc function - Function to perform interaction
-- @param maxRetries number - Maximum retries (default: 3)
-- @param timeout number - Timeout per attempt (default: 30)
-- @return boolean - True if successful
function InteractWithRetry(interactFunc, maxRetries, timeout)
    maxRetries = maxRetries or 3
    timeout = timeout or 30

    for attempt = 1, maxRetries do
        local success = interactFunc(timeout)
        if success then
            return true
        end

        yield("/echo [Script] Interaction attempt " .. attempt .. " failed, retrying...")
        yield("/wait 2")
    end

    yield("/echo [Script] Interaction failed after " .. maxRetries .. " attempts")
    return false
end
```

## Configuration Variables

```lua
configs:
  EnableTextAdvance:
    default: true
    description: Enable TextAdvance during automation
  QuickDialog:
    default: true
    description: Enable quick dialog advancement
  AutoCutsceneSkip:
    default: true
    description: Automatically skip cutscenes
  AutoAcceptQuests:
    default: false
    description: Automatically accept quests
  DialogTimeout:
    default: 60
    description: Dialog interaction timeout in seconds
  CutsceneTimeout:
    default: 120
    description: Cutscene skip timeout in seconds
```

## Character Conditions Reference

```lua
-- Conditions related to dialog/interaction
local CharacterCondition = {
    occupiedInEvent = 31,          -- In event/interaction
    occupiedInQuestEvent = 32,     -- In quest event
    watchingCutscene = 10,         -- Watching cutscene
    watchingCutscene2 = 11,        -- Alternative cutscene flag
    dutyRecorderPlayback = 98,     -- Watching duty recording
    betweenAreas = 45,             -- Loading screen
    casting = 27,                  -- Casting (can't interact)
}

--- Check if player can interact
-- @return boolean - True if can interact
function CanInteract()
    return not Svc.Condition[CharacterCondition.casting] and
           not Svc.Condition[CharacterCondition.betweenAreas] and
           not IsInCutscene() and
           Player.Available
end
```

## Best Practices

1. **Enable TextAdvance before interactions** - Call `EnableTextAdvance()` before NPC interactions
2. **Disable when not needed** - Don't leave TextAdvance enabled permanently
3. **Use appropriate timeouts** - 30-60s for dialogs, 120s for cutscenes
4. **Check dialog state** before and after interactions
5. **Handle cutscenes separately** - They may interrupt normal flow
6. **Use configuration presets** for consistent behavior
7. **Wait for dialog close** before continuing automation
8. **Handle item turn-in** (Request addon) during quest completion
9. **Retry failed interactions** - Network issues can cause failures
10. **Integrate with navigation** for complete quest automation
