---
name: SND Addon Interactions
description: Use this skill when implementing game UI addon interactions in SND macros. Covers crafting addons, shop addons, node access, and general game addon patterns.
---

# Game Addon Interactions for SND

This skill covers integration with FFXIV game UI addons in SND macros.

## Core Addon Functions

### Safe Addon Access

**IMPORTANT:** Always use pcall when accessing addons to avoid errors when addons don't exist.

```lua
--- Safely get an addon with error handling
-- @param name string - Addon name
-- @return Addon|nil - The addon or nil if not found/error
local function _get_addon(name)
    local ok, addon = pcall(Addons.GetAddon, name)
    if ok and addon ~= nil then
        return addon
    end
    return nil
end
```

### Check Addon Readiness
```lua
function IsAddonReady(addonName)
    local addon = _get_addon(addonName)
    return addon and addon.Ready or false
end

--- Check if addon exists/is visible
-- Note: Uses addon.Exists property (not addon.Visible)
function IsAddonVisible(addonName)
    local addon = _get_addon(addonName)
    return addon and addon.Exists or false
end

function WaitForAddonReady(addonName, timeout)
    timeout = timeout or 10
    local startTime = os.clock()

    while not IsAddonReady(addonName) and (os.clock() - startTime) < timeout do
        yield("/wait 0.1")
    end

    return IsAddonReady(addonName)
end

function WaitForAddonVisible(addonName, timeout)
    timeout = timeout or 10
    local startTime = os.clock()

    while not IsAddonVisible(addonName) and (os.clock() - startTime) < timeout do
        yield("/wait 0.1")
    end

    return IsAddonVisible(addonName)
end

function WaitForAddonClosed(addonName, timeout)
    timeout = timeout or 10
    local startTime = os.clock()

    while IsAddonVisible(addonName) and (os.clock() - startTime) < timeout do
        yield("/wait 0.1")
    end

    return not IsAddonVisible(addonName)
end
```

### Safe Addon Callback (Enhanced)

**CRITICAL: Argument Quoting**

String arguments containing spaces or special characters MUST be quoted. The `SafeCallback` function handles this automatically.

```lua
--- Quote a single callback argument if it contains spaces
-- @param arg any - The argument to potentially quote
-- @return string - The argument, quoted if necessary
function QuoteArg(arg)
    local s = tostring(arg)
    if s:find("%s") then
        return '"' .. s .. '"'
    end
    return s
end

--- Build a properly quoted argument string for callbacks
-- @param ... any - Arguments to format
-- @return string - Space-separated, properly quoted arguments
function BuildCallbackArgs(...)
    local args = {...}
    local parts = {}
    for i, arg in ipairs(args) do
        parts[i] = QuoteArg(arg)
    end
    return table.concat(parts, " ")
end

--- Safe callback with automatic argument quoting and error handling
-- @param addonName string - Name of the addon
-- @param useBase boolean - If true, uses CallbackAddon; if false, uses yield /callback
-- @param ... any - Arguments for the callback
-- @return boolean - Success status
function SafeCallback(addonName, useBase, ...)
    if not IsAddonReady(addonName) then
        return false
    end

    local success, err = pcall(function()
        if useBase then
            CallbackAddon(addonName, ...)
        else
            local argStr = BuildCallbackArgs(...)
            yield("/callback " .. addonName .. " " .. argStr)
        end
    end)

    if not success then
        yield("/echo [Script] Callback failed: " .. tostring(err))
        return false
    end

    return true
end

--- Legacy SafeAddonCallback (for backwards compatibility)
function SafeAddonCallback(addonName, ...)
    if not IsAddonReady(addonName) then
        yield("/echo [Script] Addon not ready: " .. addonName)
        return false
    end

    local success, result = pcall(function()
        return CallbackAddon(addonName, ...)
    end)

    if not success then
        yield("/echo [Script] Addon callback failed: " .. tostring(result))
        return false
    end

    return result
end
```

### Check Multiple Addons
```lua
function GetAddonStatus(addonNames)
    local status = {}
    for _, addonName in ipairs(addonNames) do
        status[addonName] = IsAddonReady(addonName)
    end
    return status
end

function AnyAddonReady(addonNames)
    for _, addonName in ipairs(addonNames) do
        if IsAddonReady(addonName) then
            return true, addonName
        end
    end
    return false, nil
end

function AllAddonsReady(addonNames)
    for _, addonName in ipairs(addonNames) do
        if not IsAddonReady(addonName) then
            return false, addonName
        end
    end
    return true, nil
end
```

## Addon Node Access

### Getting Node References

There are two methods to access addon nodes:
1. **`addon:GetNode(path...)`** - Preferred method, uses variadic path
2. **Manual traversal** - Navigate through ChildNodes

```lua
local _unpack = table.unpack or unpack

--- Get a node using addon:GetNode() method (preferred)
-- @param addonName string - Name of the addon
-- @param path table - Array of node indices {i, j, k, ...}
-- @return AtkResNode|nil - The node or nil
local function _get_node(addonName, path)
    if type(path) ~= "table" then return nil end
    local addon = _get_addon(addonName)
    if not (addon and addon.Ready) then return nil end
    local ok, node = pcall(function() return addon:GetNode(_unpack(path)) end)
    if ok then return node end
    return nil
end

--- Get the root node of an addon
-- @param addonName string - Name of the addon
-- @return AtkResNode|nil - The root node or nil
function GetAddonRootNode(addonName)
    local addon = _get_addon(addonName)
    if not (addon and addon.Ready) then
        return nil
    end
    return addon.RootNode
end

--- Navigate to a specific node by index path (using addon:GetNode)
-- @param addonName string - Name of the addon
-- @param ... number - Node indices to traverse
-- @return AtkResNode|nil - The target node or nil
function GetNodeByPath(addonName, ...)
    local path = {...}
    return _get_node(addonName, path)
end

--- Get a node's child by index (0-based)
-- @param parentNode AtkResNode - The parent node
-- @param index number - Child index (0-based)
-- @return AtkResNode|nil - The child node or nil
function GetChildNode(parentNode, index)
    if parentNode and parentNode.ChildNodes and parentNode.ChildNodes[index] then
        return parentNode.ChildNodes[index]
    end
    return nil
end

--- Get a node from addon's Nodes collection by index
-- @param addonName string - Name of the addon
-- @param index number - Node index
-- @return AtkResNode|nil - The node or nil
function GetMyNode(addonName, index)
    local addon = _get_addon(addonName)
    if not (addon and addon.Ready) then return nil end
    local nodes = addon.Nodes
    return nodes and nodes[index] or nil
end
```

### Node Property Access

```lua
--- Check if a node is visible
-- @param node AtkResNode - The node to check
-- @return boolean - True if visible
function IsNodeVisible(node)
    if not node then
        return false
    end
    return node.IsVisible == true
end

--- Get text from a text node
-- @param node AtkTextNode - The text node
-- @return string|nil - The text content or nil
function GetNodeText(node)
    if not node then
        return nil
    end
    -- Different node types have different text properties
    if node.NodeText then
        return tostring(node.NodeText)
    elseif node.Text then
        return tostring(node.Text)
    end
    return nil
end

--- Get the type of a node
-- @param node AtkResNode - The node
-- @return number|nil - The node type ID or nil
function GetNodeType(node)
    if not node then
        return nil
    end
    return node.Type
end

--- Node type constants
NodeType = {
    Res = 0,
    Image = 1,
    Text = 2,
    NineGrid = 3,
    Counter = 4,
    Collision = 5,
    Button = 6,
    Component = 7,
}
```

### Wait for Node Visibility

```lua
--- Wait until a specific addon node becomes visible
-- @param addonName string - Name of the addon
-- @param nodeIndices table - Array of node indices to traverse
-- @param timeout number - Maximum wait time in seconds (default: 10)
-- @return boolean - True if node became visible
function AwaitAddonNodeVisible(addonName, nodeIndices, timeout)
    timeout = timeout or 10
    local startTime = os.clock()

    while (os.clock() - startTime) < timeout do
        if IsAddonReady(addonName) then
            local node = GetAddonRootNode(addonName)
            local valid = true

            for _, idx in ipairs(nodeIndices) do
                if node and node.ChildNodes and node.ChildNodes[idx] then
                    node = node.ChildNodes[idx]
                else
                    valid = false
                    break
                end
            end

            if valid and node and IsNodeVisible(node) then
                return true
            end
        end

        yield("/wait 0.1")
    end

    return false
end

--- Wait until a specific node contains expected text
-- @param addonName string - Name of the addon
-- @param nodeIndices table - Array of node indices to traverse
-- @param expectedText string - Text to match (partial match)
-- @param timeout number - Maximum wait time in seconds (default: 10)
-- @return boolean - True if text was found
function AwaitNodeText(addonName, nodeIndices, expectedText, timeout)
    timeout = timeout or 10
    local startTime = os.clock()

    while (os.clock() - startTime) < timeout do
        if IsAddonReady(addonName) then
            local node = GetAddonRootNode(addonName)

            for _, idx in ipairs(nodeIndices) do
                if node and node.ChildNodes and node.ChildNodes[idx] then
                    node = node.ChildNodes[idx]
                else
                    node = nil
                    break
                end
            end

            if node then
                local text = GetNodeText(node)
                if text and text:find(expectedText) then
                    return true
                end
            end
        end

        yield("/wait 0.1")
    end

    return false
end
```

## Crafting Addons

### RecipeNote Addon
```lua
function IsRecipeNoteReady()
    return Addons.GetAddon("RecipeNote").Ready
end

function OpenRecipeNote()
    if IsRecipeNoteReady() then
        CallbackAddon("RecipeNote", "OpenRecipeNote")
        return true
    end
    return false
end

function CloseRecipeNote()
    if IsRecipeNoteReady() then
        CallbackAddon("RecipeNote", "CloseRecipeNote")
        return true
    end
    return false
end
```

### Synthesis Addon
```lua
function IsSynthesisReady()
    return Addons.GetAddon("Synthesis").Ready
end

function StartSynthesis()
    if IsSynthesisReady() then
        CallbackAddon("Synthesis", "StartSynthesis")
        return true
    end
    return false
end

function IsSynthesisActive()
    if IsSynthesisReady() then
        return CallbackAddon("Synthesis", "IsActive")
    end
    return false
end
```

### Crafting Workflow
```lua
function CompleteCraftingAddonWorkflow(timeout)
    timeout = timeout or 300

    -- Check prerequisites
    if not IsRecipeNoteReady() then
        yield("/echo [Script] ERROR: RecipeNote addon not ready")
        return false
    end

    -- Open RecipeNote
    if not OpenRecipeNote() then
        yield("/echo [Script] ERROR: Failed to open RecipeNote")
        return false
    end

    yield("/wait 1")

    -- Start synthesis
    if not StartSynthesis() then
        yield("/echo [Script] ERROR: Failed to start synthesis")
        return false
    end

    -- Wait for synthesis to complete
    local startTime = os.clock()
    while IsSynthesisActive() and (os.clock() - startTime) < timeout do
        yield("/wait 1")
    end

    if IsSynthesisActive() then
        yield("/echo [Script] WARNING: Synthesis timeout")
        return false
    end

    CloseRecipeNote()
    yield("/echo [Script] Crafting completed successfully")
    return true
end
```

## Shop Addons

### CollectablesShop Addon
```lua
function IsCollectablesShopReady()
    return Addons.GetAddon("CollectablesShop").Ready
end

function OpenCollectablesShop()
    if IsCollectablesShopReady() then
        CallbackAddon("CollectablesShop", "OpenCollectablesShop")
        return true
    end
    return false
end

function CloseCollectablesShop()
    if IsCollectablesShopReady() then
        CallbackAddon("CollectablesShop", "CloseCollectablesShop")
        return true
    end
    return false
end
```

### InclusionShop Addon
```lua
function IsInclusionShopReady()
    return Addons.GetAddon("InclusionShop").Ready
end

function OpenInclusionShop()
    if IsInclusionShopReady() then
        CallbackAddon("InclusionShop", "OpenInclusionShop")
        return true
    end
    return false
end

function CloseInclusionShop()
    if IsInclusionShopReady() then
        CallbackAddon("InclusionShop", "CloseInclusionShop")
        return true
    end
    return false
end
```

### Shop Workflow
```lua
function CompleteShopWorkflow(shopType, timeout)
    timeout = timeout or 60

    -- Check prerequisites based on shop type
    if shopType == "collectables" then
        if not IsCollectablesShopReady() then
            yield("/echo [Script] ERROR: CollectablesShop addon not ready")
            return false
        end
        if not OpenCollectablesShop() then
            yield("/echo [Script] ERROR: Failed to open CollectablesShop")
            return false
        end
    elseif shopType == "inclusion" then
        if not IsInclusionShopReady() then
            yield("/echo [Script] ERROR: InclusionShop addon not ready")
            return false
        end
        if not OpenInclusionShop() then
            yield("/echo [Script] ERROR: Failed to open InclusionShop")
            return false
        end
    end

    yield("/wait 1")

    -- Perform shop operations here
    yield("/echo [Script] Shop operations completed")

    -- Close shop
    if shopType == "collectables" then
        CloseCollectablesShop()
    elseif shopType == "inclusion" then
        CloseInclusionShop()
    end

    yield("/echo [Script] Shop workflow completed successfully")
    return true
end
```

## Game Addons

### TripleTriad Addon
```lua
function IsTripleTriadReady()
    return Addons.GetAddon("TripleTriad").Ready
end

function OpenTripleTriad()
    if IsTripleTriadReady() then
        CallbackAddon("TripleTriad", "OpenTripleTriad")
        return true
    end
    return false
end

function CloseTripleTriad()
    if IsTripleTriadReady() then
        CallbackAddon("TripleTriad", "CloseTripleTriad")
        return true
    end
    return false
end
```

### Generic Addon Functions
```lua
function OpenAddon(addonName)
    if IsAddonReady(addonName) then
        CallbackAddon(addonName, "Open" .. addonName)
        return true
    end
    return false
end

function CloseAddon(addonName)
    if IsAddonReady(addonName) then
        CallbackAddon(addonName, "Close" .. addonName)
        return true
    end
    return false
end
```

### Generic Addon Workflow
```lua
function CompleteAddonWorkflow(addonName, operation, timeout)
    timeout = timeout or 60

    -- Check prerequisites
    if not IsAddonReady(addonName) then
        yield("/echo [Script] ERROR: " .. addonName .. " addon not ready")
        return false
    end

    -- Open addon
    if not OpenAddon(addonName) then
        yield("/echo [Script] ERROR: Failed to open " .. addonName)
        return false
    end

    yield("/wait 1")

    -- Perform operation
    if operation then
        operation()
    end

    -- Close addon
    CloseAddon(addonName)

    yield("/echo [Script] Addon workflow completed successfully")
    return true
end
```

## Error Handling

### Safe Addon Operations
```lua
function SafeAddonOperation(addonName, functionName, ...)
    if not IsAddonReady(addonName) then
        return nil, "Addon not ready: " .. addonName
    end

    local success, result = pcall(function()
        return CallbackAddon(addonName, functionName, ...)
    end)

    if success then
        return result, nil
    else
        return nil, "Addon operation failed: " .. tostring(result)
    end
end
```

### Addon Timeout Handling
```lua
function WaitForAddonOperation(addonName, condition, timeout)
    timeout = timeout or 10
    local startTime = os.clock()

    while not condition() and (os.clock() - startTime) < timeout do
        yield("/wait 0.1")
    end

    if not condition() then
        yield("/echo [Script] Addon operation timeout: " .. addonName)
        return false
    end

    return true
end
```

## State Machine Integration

```lua
CharacterState = {
    ready = Ready,
    openingAddon = OpeningAddon,
    usingAddon = UsingAddon,
    -- ... other states
}

function OpeningAddon()
    if OpenAddon(targetAddon) then
        yield("/echo [Script] Addon opened")
        State = CharacterState.usingAddon
    else
        yield("/echo [Script] Failed to open addon")
        State = CharacterState.ready
    end
end

function UsingAddon()
    if CompleteAddonWorkflow(targetAddon, function()
        yield("/echo [Script] Performing addon operations")
    end, 60) then
        yield("/echo [Script] Addon operations completed")
        State = CharacterState.ready
    else
        yield("/echo [Script] Addon operations failed")
        State = CharacterState.ready
    end
end
```

## Configuration Variables

```lua
configs:
  EnableAddonInteractions:
    default: true
    description: Enable game addon interactions
  AddonTimeout:
    default: 60
    description: Addon timeout in seconds
  AddonWaitTimeout:
    default: 10
    description: Addon wait timeout in seconds
```

## Common Addon Patterns

### SelectYesno Dialog

```lua
--- Handle a Yes/No confirmation dialog
-- @param selectYes boolean - True to select Yes, false for No
-- @param timeout number - Maximum wait time (default: 5)
-- @return boolean - True if dialog was handled
function HandleSelectYesno(selectYes, timeout)
    timeout = timeout or 5

    if not WaitForAddonVisible("SelectYesno", timeout) then
        return false
    end

    yield("/wait 0.2")  -- Brief delay for stability

    local choice = selectYes and 0 or 1
    SafeCallback("SelectYesno", true, true, choice)

    return WaitForAddonClosed("SelectYesno", 3)
end
```

### SelectString Dialog (List Selection)

```lua
--- Select an option from a SelectString dialog by index
-- @param index number - 0-based index of the option to select
-- @param timeout number - Maximum wait time (default: 5)
-- @return boolean - True if selection was made
function SelectStringByIndex(index, timeout)
    timeout = timeout or 5

    if not WaitForAddonVisible("SelectString", timeout) then
        return false
    end

    yield("/wait 0.2")
    SafeCallback("SelectString", true, true, index)

    return WaitForAddonClosed("SelectString", 3)
end

--- Select an option from a SelectString dialog by text content
-- @param searchText string - Text to search for (partial match)
-- @param timeout number - Maximum wait time (default: 5)
-- @return boolean - True if selection was made
function SelectStringByText(searchText, timeout)
    timeout = timeout or 5

    if not WaitForAddonVisible("SelectString", timeout) then
        return false
    end

    -- Search through list items for matching text
    local rootNode = GetAddonRootNode("SelectString")
    if not rootNode then
        return false
    end

    -- Navigate to list component (structure may vary)
    -- This is an example; actual node path depends on addon structure
    local listNode = GetNodeByPath("SelectString", 2, 0)  -- Example path
    if listNode then
        for i = 0, 10 do  -- Check first 10 entries
            local itemNode = GetChildNode(listNode, i)
            if itemNode then
                local text = GetNodeText(itemNode)
                if text and text:find(searchText) then
                    SafeCallback("SelectString", true, true, i)
                    return WaitForAddonClosed("SelectString", 3)
                end
            end
        end
    end

    return false
end
```

### Talk Dialog (NPC Conversation)

```lua
--- Advance a Talk dialog
-- @param timeout number - Maximum wait time (default: 5)
-- @return boolean - True if dialog was advanced
function AdvanceTalk(timeout)
    timeout = timeout or 5

    if not WaitForAddonVisible("Talk", timeout) then
        return false
    end

    yield("/wait 0.1")
    yield("/click Talk")

    return true
end

--- Wait for and advance through all Talk dialogs
-- @param maxDialogs number - Maximum dialogs to advance (default: 20)
-- @param timeout number - Timeout per dialog (default: 2)
function AdvanceAllTalk(maxDialogs, timeout)
    maxDialogs = maxDialogs or 20
    timeout = timeout or 2

    for i = 1, maxDialogs do
        if IsAddonVisible("Talk") then
            AdvanceTalk(timeout)
            yield("/wait 0.3")
        else
            break
        end
    end
end
```

### Request Dialog (Item Hand-in)

```lua
--- Check if Request addon is ready for hand-in
-- @return boolean - True if ready
function IsRequestReady()
    return IsAddonVisible("Request")
end

--- Hand in items via Request dialog
-- @param timeout number - Maximum wait time (default: 10)
-- @return boolean - True if hand-in completed
function CompleteRequest(timeout)
    timeout = timeout or 10

    if not WaitForAddonVisible("Request", timeout) then
        return false
    end

    yield("/wait 0.5")
    SafeCallback("Request", true, true, 0)  -- Click hand-in button

    return WaitForAddonClosed("Request", 5)
end
```

### ContextMenu Handling

```lua
--- Select an option from a context menu by index
-- @param index number - 0-based index of the option
-- @param timeout number - Maximum wait time (default: 3)
-- @return boolean - True if selection was made
function SelectContextMenu(index, timeout)
    timeout = timeout or 3

    if not WaitForAddonVisible("ContextMenu", timeout) then
        return false
    end

    yield("/wait 0.1")
    SafeCallback("ContextMenu", true, true, 0, index, 0)

    return WaitForAddonClosed("ContextMenu", 2)
end
```

### JournalResult (Quest Completion)

```lua
--- Complete a quest via JournalResult dialog
-- @param timeout number - Maximum wait time (default: 10)
-- @return boolean - True if quest was completed
function CompleteQuest(timeout)
    timeout = timeout or 10

    if not WaitForAddonVisible("JournalResult", timeout) then
        return false
    end

    yield("/wait 0.5")
    SafeCallback("JournalResult", true, true, 1)  -- Click complete

    return WaitForAddonClosed("JournalResult", 5)
end
```

### GrandCompanySupplyReward

```lua
--- Handle Grand Company expert delivery reward selection
-- @param timeout number - Maximum wait time (default: 5)
-- @return boolean - True if completed
function AcceptGCReward(timeout)
    timeout = timeout or 5

    if not WaitForAddonVisible("GrandCompanySupplyReward", timeout) then
        return false
    end

    yield("/wait 0.3")
    SafeCallback("GrandCompanySupplyReward", true, true, 0)

    return WaitForAddonClosed("GrandCompanySupplyReward", 3)
end
```

## Common Addon Names Reference

```lua
-- Dialog addons
AddonNames = {
    -- Confirmation dialogs
    SelectYesno = "SelectYesno",
    SelectString = "SelectString",
    SelectIconString = "SelectIconString",
    ContextMenu = "ContextMenu",

    -- NPC interaction
    Talk = "Talk",
    CutSceneSelectString = "CutSceneSelectString",

    -- Quest
    JournalDetail = "JournalDetail",
    JournalResult = "JournalResult",
    Request = "Request",

    -- Crafting
    RecipeNote = "RecipeNote",
    Synthesis = "Synthesis",
    SynthesisSimple = "SynthesisSimple",

    -- Gathering
    Gathering = "Gathering",
    GatheringMasterpiece = "GatheringMasterpiece",

    -- Shops
    Shop = "Shop",
    ShopExchangeCurrency = "ShopExchangeCurrency",
    ShopExchangeItem = "ShopExchangeItem",
    CollectablesShop = "CollectablesShop",
    InclusionShop = "InclusionShop",
    MateriaAttach = "MateriaAttach",

    -- Grand Company
    GrandCompanySupplyList = "GrandCompanySupplyList",
    GrandCompanySupplyReward = "GrandCompanySupplyReward",
    GrandCompanyExchange = "GrandCompanyExchange",

    -- Retainers
    RetainerList = "RetainerList",
    RetainerTaskAsk = "RetainerTaskAsk",
    RetainerTaskResult = "RetainerTaskResult",
    SelectString = "SelectString",  -- Used for retainer menu

    -- Market Board
    ItemSearch = "ItemSearch",
    ItemSearchResult = "ItemSearchResult",
    RetainerSell = "RetainerSell",

    -- Inventory
    Inventory = "Inventory",
    InventoryExpansion = "InventoryExpansion",
    InventoryLarge = "InventoryLarge",

    -- Character
    Character = "Character",
    CharacterClass = "CharacterClass",
    ArmouryBoard = "ArmouryBoard",

    -- Travel
    Teleport = "Teleport",
    TelepotTown = "TelepotTown",  -- Note: game uses "Telepot" not "Teleport"

    -- Housing
    HousingSelectBlock = "HousingSelectBlock",

    -- FATE
    FateProgress = "FateProgress",
}
```

## Best Practices

1. **Always check addon readiness** before performing operations
2. **Use timeouts** for addon operations (default: 10s for waiting, 60s for workflows)
3. **Use safe callbacks** with pcall for error handling
4. **Quote arguments** containing spaces using `QuoteArg()` or `SafeCallback()`
5. **Wait appropriately** after opening addons (yield 0.2-1s depending on addon)
6. **Close addons** after completing operations
7. **Monitor addon states** when needed
8. **Use appropriate wait times**: 0.1s for addon readiness checks
9. **Check visibility** not just readiness for interactive addons
10. **Handle dialog chains** - some operations trigger multiple dialogs
11. **Use node access** for reading addon data, callbacks for interaction
