---
name: SND Core
description: Use this skill when creating or editing SND Lua macros for FFXIV. Provides metadata structure, state machine patterns, character conditions, configuration system, Player API, Entity system, Excel data access, and core utility functions.
---

# SND Core Development

This skill covers the foundational patterns for SND (Something Need Doing) Lua macros.

## Metadata Structure Requirements

Every SND macro MUST start with this metadata header:

```lua
--[=====[
[[SND Metadata]]
author: 'Your Name'
version: 1.0.0
description: Brief description of what the macro does
plugin_dependencies:
- PluginName1
- PluginName2
configs:
  NumberSetting:
    description: A numeric setting with min/max
    default: 50
    min: 1
    max: 100
  StringSetting:
    description: A text setting
    default: SomeValue
  BooleanSetting:
    description: A true/false setting
    default: true
[[End Metadata]]
--]=====]
```

### Required Fields
- **author**: String - Creator of the macro
- **version**: String - Semantic versioning (MAJOR.MINOR.PATCH)
- **description**: String - Brief description of macro functionality

### Optional Fields
- **plugin_dependencies**: Array of required Dalamud plugins
- **configs**: User-configurable settings object

### Configuration Field Properties
Each config setting can have:
- **description**: What this setting does (REQUIRED - put before default)
- **default**: Default value (string, number, or boolean)
- **min**: Minimum value (for numbers)
- **max**: Maximum value (for numbers)

### Configuration Examples
```lua
configs:
  -- Numeric with range
  GameCount:
    description: Number of games to play. Set to 0 to skip.
    default: 125
    min: 0
    max: 1000

  -- Boolean
  EnableFeature:
    description: Enable this feature (true/false)
    default: true

  -- String
  TargetName:
    description: Name of the target NPC
    default: SomeNPC
```

**IMPORTANT:** The `description` field should come BEFORE `default` in the YAML structure for proper display in SND.

## Configuration Access

**IMPORTANT:** Config values are stored in SND's JSON as strings, regardless of the declared type. Always convert appropriately.

```lua
-- Always use Config.Get() to access configuration values
local settingValue = Config.Get("SettingName")
local numericValue = tonumber(Config.Get("NumericSetting"))
local booleanValue = Config.Get("BooleanSetting") == "true" or Config.Get("BooleanSetting") == true

-- Type-safe access functions
function GetConfigAsString(key, defaultValue)
    return Config.Get(key) or defaultValue or ""
end

function GetConfigAsNumber(key, defaultValue)
    local value = Config.Get(key)
    return value and tonumber(value) or defaultValue or 0
end

function GetConfigAsBoolean(key, defaultValue)
    local value = Config.Get(key)
    -- Handle both string "true" and actual boolean true
    if value == "true" or value == true then return true end
    if value == "false" or value == false then return false end
    return defaultValue or false
end
```

### How Configs Work in SND

1. **Metadata YAML → SND JSON**: When syncing, the YAML metadata in your Lua file is parsed and converted to SND's internal JSON format.

2. **SND JSON Format**: Each config becomes a JSON object with these properties:
   - `Value`: Current value (string)
   - `DefaultValue`: Default value from metadata (string)
   - `Description`: Description text
   - `Type`: "bool", "int", or "string" (auto-detected)
   - `MinValue`/`MaxValue`: For numeric types (string or null)

3. **Type Detection**:
   - `true`/`false` → `bool`
   - Numeric values → `int`
   - Everything else → `string`

4. **Example JSON output** (what SND stores):
```json
{
  "Debug": {
    "Value": "true",
    "DefaultValue": "true",
    "Description": "Show debug info",
    "Type": "bool",
    "MinValue": null,
    "MaxValue": null
  },
  "Breakpoint1": {
    "Value": "50",
    "DefaultValue": "50",
    "Description": "First breakpoint level",
    "Type": "int",
    "MinValue": "1",
    "MaxValue": "100"
  }
}
```

## Logging System

Standardized logging with prefix and optional echo to chat.

```lua
-- Configuration
echoLog = true           -- Set to false to disable chat echo
PREFIX  = "[Script]"     -- Prefix for all messages

-- Internal helpers
local function _echo(s)
    yield("/echo " .. tostring(s))
end

local function _log(s)
    local msg = tostring(s)
    Dalamud.Log(msg)
    if echoLog then _echo(msg) end
end

local function _fmt(msg, ...)
    return string.format("%s %s", PREFIX, string.format(msg, ...))
end

-- Public logging functions
function Logf(msg, ...)   _log(_fmt(msg, ...))  end
function Echof(msg, ...)  _echo(_fmt(msg, ...)) end

-- Aliases for convenience
Log,  log  = Logf,  Logf
Echo, echo = Echof, Echof
```

### Usage Examples

```lua
-- Simple logging
Log("Starting script")
Echo("Player name: %s", Player.Name)

-- With format arguments
Logf("Processing item %d of %d", currentItem, totalItems)
Echof("Distance to target: %.2f", distance)

-- Conditional logging
if debugMode then
    Log("Debug: current state = %s", tostring(State))
end
```

## Player API

### IMPORTANT: Player vs Svc.ClientState.LocalPlayer

There are TWO ways to access player data, and they return DIFFERENT things:

1. **`Player.*`** - SND wrapper object (some properties return nil or wrapper objects)
2. **`Svc.ClientState.LocalPlayer`** - Direct Dalamud access (more reliable for level/job)

```lua
-- WRONG: These may return nil or wrapper objects
local level = Player.Level           -- Returns nil!
local job = Player.Job               -- Returns wrapper object, not ID!

-- CORRECT: Use Svc.ClientState.LocalPlayer for level and job info
local lp = Svc.ClientState.LocalPlayer
if lp then
    local currentLevel = lp.Level              -- Returns actual level number
    local currentJobId = lp.ClassJob.RowId     -- Returns job ID number
end
```

### Player Availability and Basic Info
```lua
-- Check if player is available (Player wrapper)
if Player.Available then
    -- Player is available for operations
end

-- Check if player is busy (Player wrapper)
if Player.IsBusy then
    -- Player is busy with something
end

-- Get player name (Player wrapper)
local playerName = Player.Name

-- Get player level - USE LocalPlayer!
local lp = Svc.ClientState.LocalPlayer
local level = lp and lp.Level or 0
```

### Player Position
```lua
-- Get player position
local pos = Player.Position
local x = pos.X
local y = pos.Y
local z = pos.Z

-- Example: Log current position
yield("/echo [Script] Position: " .. pos.X .. ", " .. pos.Y .. ", " .. pos.Z)
```

### Player Job/Class
```lua
-- CORRECT: Get current job information via LocalPlayer
local lp = Svc.ClientState.LocalPlayer
if lp then
    local jobId = lp.ClassJob.RowId
    local jobAbbr = lp.ClassJob.Value.Abbreviation:ToString()
    local jobName = lp.ClassJob.Value.Name:ToString()

    yield("/echo [Script] Current job: " .. jobAbbr .. " (ID: " .. jobId .. ") Lv." .. lp.Level)
end

-- Example: Check if on specific job
local lp = Svc.ClientState.LocalPlayer
if lp and lp.ClassJob.RowId == 14 then -- Carpenter
    yield("/echo [Script] Currently on Carpenter")
end
```

### Gearsets (for listing saved gearsets)
```lua
-- Get gearset info
local gs = Player.GetGearset(1)  -- API index 1-100
if gs and gs.ClassJob and gs.ClassJob > 0 then
    local jobId = gs.ClassJob
    local gearsetName = gs.Name
    local itemLevel = gs.ItemLevel  -- ITEM LEVEL of the gear, NOT character job level!
end

-- Iterate all gearsets to find which jobs have gearsets
for idx = 1, 100 do
    local gs = Player.GetGearset(idx)
    if gs and gs.ClassJob and gs.ClassJob > 0 and gs.Name and gs.Name ~= "" then
        yield("/echo Job ID: " .. gs.ClassJob .. " Gearset: " .. gs.Name .. " iLvl: " .. gs.ItemLevel)
    end
end
```

**CRITICAL WARNING - Gearset Index Offset:**
`Player.GetGearset(idx)` returns gearsets where the API index is **OFF BY ONE** from the UI slot number!

- API index 1 = UI slot 2
- API index 5 = UI slot 6
- etc.

When using `/gearset change`, you must use the **UI slot number**, not the API index:
```lua
-- CORRECT: Switch to a gearset by job ID
for idx = 1, 100 do
    local gs = Player.GetGearset(idx)
    if gs and gs.ClassJob == targetJobId then
        local uiSlot = idx + 1  -- Convert API index to UI slot!
        yield("/gearset change " .. uiSlot)
        break
    end
end

-- WRONG: This uses the API index directly (will switch to wrong gearset!)
-- yield("/gearset change " .. idx)  -- DON'T DO THIS!
```

**WARNING:** `gs.ItemLevel` is the average item level of the GEAR in that gearset, NOT the character's level in that job!

### Getting Job Levels

Use `Player.GetJob(jobId).Level` to get the level for ANY job:

```lua
-- Get level for a specific job by ID
local level = Player.GetJob(15).Level  -- e.g., 88 for Machinist (ID 15)

-- Get all job levels
local classJobSheet = Excel.GetSheet("ClassJob")
for jobId = 1, 42 do
    local job = Player.GetJob(jobId)
    if job and job.Level and job.Level > 0 then
        local jobRow = classJobSheet:GetRow(jobId)
        local abbr = jobRow and tostring(jobRow.Abbreviation) or "?"
        yield("/echo " .. abbr .. ": Lv." .. tostring(job.Level))
    end
end
```

**Working approaches:**
- `Player.GetJob(jobId).Level` → Returns level for any job ✓
- `Svc.ClientState.LocalPlayer.Level` → Current job level only ✓

**Non-working approaches:**
- `Player.Level` → nil
- `Player.GetLevel(x)` → nil (method doesn't exist)
- `Player.ClassJob` → nil

### Combat and Casting State
```lua
-- Check if player is in combat
Player.InCombat → boolean

-- Check if player is casting
Player.IsCasting → boolean

-- Get current cast info (when casting)
Player.CastInfo → table  -- Contains spell info when casting

-- Check if player is alive
Player.IsAlive → boolean

-- Get current HP/MP
Player.CurrentHp → number
Player.MaxHp → number
Player.CurrentMp → number
Player.MaxMp → number
```

### Player Status Effects
```lua
-- Get player status list
local statusList = Player.Status

-- Check for specific status
function HasStatusId(targetId)
    local statusList = Player.Status

    if not statusList then
        return false
    end

    for i = 0, statusList.Count - 1 do
        local status = statusList:get_Item(i)
        if status and status.StatusId == targetId then
            return true
        end
    end

    return false
end

-- Example: Check for Superior Spiritbond Potion (ID 49)
if HasStatusId(49) then
    yield("/echo [Script] Has potion effect active")
end

-- Iterate all statuses
if Player.Status then
    for i = 0, Player.Status.Count - 1 do
        local status = Player.Status:get_Item(i)
        local statusId = status.StatusId
        local statusName = status.Name
        yield("/echo [Script] Status: " .. statusName .. " (ID: " .. statusId .. ")")
    end
end
```

## Entity System

### Getting Entities
```lua
-- Get player entity
local player = Entity.Player

-- Get current target entity
local target = Entity.Target

-- Get entity by name
local npc = Entity.GetEntityByName("NPC Name")

-- Get entity by ID
local entity = Entity.GetEntityById(entityId)

-- Get entity by DataId (for NPCs with specific DataIds)
local entity = Entity.GetEntityByDataId(dataId)

-- Get nearest entity by name
local nearest = Entity.GetNearestEntityByName("NPC Name")

-- Get all entities matching criteria
local entities = Entity.GetEntitiesByName("NPC Name")  -- Returns table
```

### Entity Filtering
```lua
-- Get entities within range
local nearbyEntities = Entity.GetEntitiesInRange(maxDistance)

-- Get targetable entities
local targetable = Entity.GetTargetableEntities()

-- Get enemy entities in combat
local enemies = Entity.GetEnemiesInCombat()
```

### Svc.Targets System

Access various target slots through `Svc.Targets`:

```lua
-- Available target slots
local targetSlots = {
    "Target",                   -- Current target
    "CurrentTarget",            -- Same as Target
    "PreviousTarget",           -- Last target
    "SoftTarget",               -- Soft target (hover)
    "MouseOverTarget",          -- Mouse hover target
    "MouseOverNameplateTarget", -- Nameplate hover target
    "FocusTarget",              -- Focus target
    "GPoseTarget",              -- GPose target
}

--- Safely get a target slot (avoids getters that can throw)
-- @param slotName string - The target slot name
-- @return IGameObject|nil - The target object or nil
local function GetTargetSlot(slotName)
    local ok, val = pcall(function() return Svc.Targets[slotName] end)
    if not ok then return nil end
    return val
end

--- Describe an IGameObject briefly
-- @param go IGameObject - The game object to describe
-- @return table - Object info {name, kind, gameObjectId, dataId, hp, maxHp, position}
function DescribeGameObject(go)
    if not go then return nil end

    local function try(fn) local ok, v = pcall(fn); return ok and v or nil end

    return {
        name = try(function() return go.Name:ToString() end) or tostring(go),
        kind = try(function() return go.ObjectKind end),
        gameObjectId = try(function() return go.GameObjectId end) or try(function() return go.EntityId end),
        dataId = try(function() return go.DataId end),
        hp = try(function() return go.CurrentHp end),
        maxHp = try(function() return go.MaxHp end),
        position = try(function() return go.Position end),
    }
end

-- Example: Get and describe focus target
local focusTarget = GetTargetSlot("FocusTarget")
if focusTarget then
    local info = DescribeGameObject(focusTarget)
    print(("Focus: %s (HP: %d/%d)"):format(info.name, info.hp or 0, info.maxHp or 0))
end
```

### Entity Properties
```lua
if entity then
    -- Get entity name
    local name = entity.Name

    -- Get entity position
    local position = entity.Position
    local x = position.X
    local y = position.Y
    local z = position.Z

    -- Set entity as target
    entity:SetAsTarget()

    -- Interact with entity
    entity:Interact()
end
```

### Distance to Target
```lua
function GetDistanceToTarget()
    if not Entity.Player or not Entity.Target then
        return nil
    end

    local playerPos = Entity.Player.Position
    local targetPos = Entity.Target.Position

    local dx = playerPos.X - targetPos.X
    local dy = playerPos.Y - targetPos.Y
    local dz = playerPos.Z - targetPos.Z

    return math.sqrt(dx * dx + dy * dy + dz * dz)
end

-- Example usage
local distance = GetDistanceToTarget()
if distance and distance < 3.0 then
    yield("/echo [Script] Close enough to interact")
end
```

### Target NPC by Name
```lua
function TargetNpcByName(npcName)
    local npc = Entity.GetEntityByName(npcName)
    if npc then
        npc:SetAsTarget()
        return true
    end
    return false
end

function InteractWithNpc(npcName)
    local npc = Entity.GetEntityByName(npcName)
    if npc then
        npc:SetAsTarget()
        yield("/wait 0.5")
        npc:Interact()
        return true
    end
    return false
end
```

### Advanced Distance Helpers

```lua
import("System.Numerics")  -- Required for Vector3

--- Calculate distance between two positions
-- @param pos1 Vector3 - First position
-- @param pos2 Vector3 - Second position
-- @return number - Distance in yalms
function DistanceBetweenPositions(pos1, pos2)
    if not (pos1 and pos2) then return math.huge end
    return Vector3.Distance(pos1, pos2)
end

--- Check if two positions are within a maximum distance
-- Uses squared distance for efficiency (avoids sqrt)
-- @param pos1 Vector3 - First position
-- @param pos2 Vector3 - Second position
-- @param maxDist number - Maximum distance
-- @return boolean - True if within distance
function IsWithinDistance(pos1, pos2, maxDist)
    if not (pos1 and pos2 and maxDist) then return false end
    local distSq
    if Vector3.DistanceSquared then
        distSq = Vector3.DistanceSquared(pos1, pos2)
    else
        local dx = pos1.X - pos2.X
        local dy = pos1.Y - pos2.Y
        local dz = pos1.Z - pos2.Z
        distSq = dx*dx + dy*dy + dz*dz
    end
    return distSq <= (maxDist * maxDist)
end

--- Check if current target is within specified distance
-- @param maxDist number - Maximum distance
-- @return boolean - True if target is within distance
function IsTargetWithin(maxDist)
    if not (Entity and Entity.Player and Entity.Target and maxDist) then
        return false
    end
    return IsWithinDistance(Entity.Player.Position, Entity.Target.Position, maxDist)
end

--- Get target name safely
-- @return string - Target name or empty string
function GetTargetName()
    return (Entity and Entity.Target and Entity.Target.Name) or ""
end
```

### Robust Entity Interaction

```lua
--- Interact with entity by name with timeout and verification
-- @param name string - Entity name to interact with
-- @param timeout number - Maximum seconds to wait (default: 5)
-- @return boolean - True if interaction succeeded
function InteractByName(name, timeout)
    if type(name) ~= "string" or name == "" then
        Log("InteractByName: invalid name '%s'", tostring(name))
        return false
    end
    timeout = toNumberSafe(timeout, 5, 0.1)

    local e = Entity.GetEntityByName(name)
    if not e then
        Log("InteractByName: entity not found '%s'", name)
        return false
    end

    local start = os.clock()
    while (os.clock() - start) < timeout do
        e:SetAsTarget()
        yield("/wait 0.1")

        local tgt = Entity.Target
        if tgt and tgt.Name == name then
            e:Interact()
            return true
        end
        yield("/wait 0.1")
    end

    Log("InteractByName: timeout '%s'", name)
    return false
end
```

### Character Info Helpers

```lua
--- Get character name from LocalPlayer
-- IMPORTANT: Use :ToString() method, NOT tostring() or .TextValue
-- tostring() gives weird output with extra IDs like "Name: 12345@World: -67890"
-- @return string|nil - Character name or nil
function GetCharacterName()
    local lp = Svc and Svc.ClientState and Svc.ClientState.LocalPlayer
    if not lp then return nil end
    return lp.Name:ToString()
end

--- Get character home world name
-- IMPORTANT: Use :ToString() method for clean output
-- @return string|nil - World name or nil
function GetCharacterWorld()
    local lp = Svc and Svc.ClientState and Svc.ClientState.LocalPlayer
    if not lp then return nil end
    return lp.HomeWorld.Value.Name:ToString()
end

--- Get character unique key (Name@World)
-- Useful for persisting per-character data
-- @return string|nil - "CharacterName@WorldName" or nil
function GetCharacterKey()
    local lp = Svc and Svc.ClientState and Svc.ClientState.LocalPlayer
    if not lp then return nil end
    local name = lp.Name:ToString()
    local world = lp.HomeWorld.Value.Name:ToString()
    return name .. "@" .. world
end

--- Get character position from ClientState
-- @return Vector3|nil - Position or nil
function GetCharacterPosition()
    local player = Svc and Svc.ClientState and Svc.ClientState.LocalPlayer
    return player and player.Position or nil
end

--- Get current job ID
-- @return number|nil - Job ID or nil
function GetCharacterJob()
    local lp = Svc and Svc.ClientState and Svc.ClientState.LocalPlayer
    return lp and lp.ClassJob and lp.ClassJob.RowId or nil
end

--- Get current job level
-- @return number - Current job level or 0
function GetCharacterLevel()
    local lp = Svc and Svc.ClientState and Svc.ClientState.LocalPlayer
    return lp and lp.Level or 0
end
```

### IMPORTANT: String Conversion Gotcha

When accessing string properties from game objects (like `Name`, `World`, etc.):

```lua
-- WRONG: tostring() gives weird output with extra metadata
local name = tostring(lp.Name)  -- Returns "Name: 12345@World: -67890"

-- WRONG: .TextValue may not exist or return nil
local name = lp.Name.TextValue  -- May error or return nil

-- CORRECT: Use :ToString() method
local name = lp.Name:ToString()  -- Returns "Character Name"
```

This applies to most game string objects like:
- `lp.Name:ToString()`
- `lp.HomeWorld.Value.Name:ToString()`
- `lp.ClassJob.Value.Name:ToString()`
- `lp.ClassJob.Value.Abbreviation:ToString()`

## Excel Data Access

Access game data sheets for information lookup. Excel lookups return structured data from the game's internal sheets.

### Basic Excel Usage
```lua
-- Get territory/zone information
local territory = Excel.GetRow("TerritoryType", territoryId)
local placeName = territory.PlaceName.Name
local aetheryteName = territory.Aetheryte.PlaceName.Name

-- Get item information
local item = Excel.GetRow("Item", itemId)
local itemName = item.Name

-- Get job information
local job = Excel.GetRow("ClassJob", jobId)
local jobName = job.Name
local jobAbbreviation = job.Abbreviation
```

### Get Zone Information
```lua
function GetZoneId()
    return Svc.ClientState.TerritoryType
end

-- Check if in specific zone
if Svc.ClientState.TerritoryType == 129 then -- Limsa Lominsa Lower Decks
    yield("/echo [Script] Currently in Limsa")
end
```

### Safe PlaceName by Territory (Handles Multiple Data Formats)
```lua
--[[
Get localized place name from territory ID.
Handles the various ways PlaceName can be stored (string, userdata, number).
Returns: ok (boolean), data/error (table with name or error string)
]]
function PlaceNameByTerritory(id)
    local tid = toNumberSafe(id, nil, 1)
    if not tid then return false, "invalid territory id: "..tostring(id) end

    local terr = Excel.GetSheet("TerritoryType")
    if not terr then return false, "TerritoryType sheet not found" end

    local row = terr:GetRow(tid)
    if not row then return false, "TerritoryType row not found for id "..tid end

    local pn = row.PlaceName
    if not pn then return false, "PlaceName field missing for territory id "..tid end

    -- Handle string type
    if type(pn) == "string" and #pn > 0 then
        return true, { name = pn, territoryId = tid, source = "TerritoryType.PlaceName:string" }
    end

    -- Handle userdata type (most common)
    if type(pn) == "userdata" then
        local okv, val = pcall(function() return pn.Value end)
        if okv and val then
            local okn, nm = pcall(function() return val.Singular or val.Name or val:ToString() end)
            if okn and nm and nm ~= "" then
                return true, { name = tostring(nm), territoryId = tid, source = "TerritoryType.PlaceName:userdata.Value" }
            end
        end
        local okid, rid = pcall(function() return pn.RowId end)
        if okid and type(rid) == "number" then
            local place = Excel.GetSheet("PlaceName")
            if not place then return false, "PlaceName sheet not found (RowId="..tostring(rid)..")" end
            local prow = place:GetRow(rid)
            if not prow then return false, "PlaceName row not found (RowId="..tostring(rid)..")" end
            local okn2, nm2 = pcall(function() return prow.Singular or prow.Name or prow:ToString() end)
            if okn2 and nm2 and nm2 ~= "" then
                return true, { name = tostring(nm2), territoryId = tid, source = "PlaceName(RowId)" }
            end
            return false, "PlaceName values empty (RowId="..tostring(rid)..")"
        end
        return false, "unsupported PlaceName userdata shape for territory id "..tid
    end

    -- Handle numeric type (direct PlaceName RowId)
    if type(pn) == "number" then
        local place = Excel.GetSheet("PlaceName")
        if not place then return false, "PlaceName sheet not found" end
        local prow = place:GetRow(pn)
        if not prow then return false, "PlaceName row not found (id="..tostring(pn)..")" end
        local okn, nm = pcall(function() return prow.Singular or prow.Name or prow:ToString() end)
        if okn and nm and nm ~= "" then
            return true, { name = tostring(nm), territoryId = tid, source = "PlaceName(numeric)" }
        end
        return false, "PlaceName values empty (id="..tostring(pn)..")"
    end

    return false, "unsupported PlaceName type: "..type(pn)
end

-- Simple wrapper that returns just the name
function GetZoneName(territoryType)
    territoryType = territoryType or Svc.ClientState.TerritoryType
    local ok, dataOrErr = PlaceNameByTerritory(territoryType)
    if ok then
        return dataOrErr.name
    else
        return nil
    end
end
```

### ENpcResident Name Lookup
```lua
-- Resolve an ENpcResident name directly by DataId
function GetENpcResidentName(dataId)
    local id = toNumberSafe(dataId, nil)
    if not id then return nil, "ENpcResident: invalid id '"..tostring(dataId).."'" end

    local sheet = Excel.GetSheet("ENpcResident")
    if not sheet then return nil, "ENpcResident sheet not available" end

    local row = sheet:GetRow(id)
    if not row then return nil, "ENpcResident: no row for id "..tostring(id) end

    local name = row.Singular or row.Name
    if not name or name == "" then return nil, "ENpcResident: name missing for id "..tostring(id) end

    return tostring(name), nil
end

-- Example usage:
-- local npcName = GetENpcResidentName(1052612) -- Returns NPC name
```

### NPC Name Resolution (Multi-Sheet Chain Lookup)

Comprehensive NPC name resolution that handles multiple Excel sheet chains:
- ENpcResident (direct lookup)
- EventNpc → ENpcResident
- BNpcBase → BNpcName

```lua
local DEBUG_NPC = false  -- Set to true for debug output

--- Resolve NPC name from multiple Excel sheet sources
-- @param kind string|number - Object kind ("EventNpc", "3", etc.)
-- @param dataId number - The NPC's DataId
-- @return string|nil, string - Name and source sheet, or nil and "unresolved"
local function ResolveNpcName(kind, dataId)
    local k = tostring(kind):lower()

    -- ENpcResident fast-path (most common)
    do
        local en = Excel.GetSheet("ENpcResident")
        if en then
            local row = en:GetRow(dataId)
            if row and (row.Singular or row.Name) then
                if DEBUG_NPC then print(("ENpcResident(%d) → %s"):format(dataId, row.Singular or row.Name)) end
                return row.Singular or row.Name, "ENpcResident"
            end
        end
    end

    -- EventNpc → ENpcResident chain
    if k == "eventnpc" or k == "3" then
        local ev = Excel.GetSheet("EventNpc")
        if ev then
            local evRow = ev:GetRow(dataId)
            if evRow then
                local link = evRow.ENpcResident or evRow.NameId or evRow.ENpcResidentId
                local linkId = (type(link) == "table" and link.RowId) or link
                local en = Excel.GetSheet("ENpcResident")
                local enRow = en and linkId and en:GetRow(linkId)
                if enRow and (enRow.Singular or enRow.Name) then
                    if DEBUG_NPC then print(("EventNpc(%d) → ENpcResident(%d) → %s"):format(dataId, linkId, enRow.Singular or enRow.Name)) end
                    return enRow.Singular or enRow.Name, "EventNpc → ENpcResident"
                end
            end
        end
    end

    -- BNpcBase → BNpcName chain (for battle NPCs/enemies)
    do
        local base = Excel.GetSheet("BNpcBase")
        local b = base and base:GetRow(dataId)
        if b then
            local link = b.BNpcName or b.NameId
            local nameId = (type(link) == "table" and link.RowId) or link
            local names = Excel.GetSheet("BNpcName")
            local nm = names and names:GetRow(nameId)
            if nm and (nm.Singular or nm.Name) then
                if DEBUG_NPC then print(("BNpcBase(%d) → BNpcName(%d) → %s"):format(dataId, nameId, nm.Singular or nm.Name)) end
                return nm.Singular or nm.Name, "BNpcBase → BNpcName"
            end
        end
    end

    if DEBUG_NPC then print(("Unresolved: kind=%s dataId=%s"):format(k, tostring(dataId))) end
    return nil, "unresolved"
end

-- Cache for resolved NPC names
local npcNameCache = {}

--- Get NPC name with caching
-- @param kind string|number - Object kind
-- @param dataId number - The NPC's DataId
-- @return string|nil, string - Name and source
function GetNpcName(kind, dataId)
    local key = tostring(kind) .. ":" .. tostring(dataId)
    local cached = npcNameCache[key]
    if cached ~= nil then return cached.name, cached.source end

    local name, source = ResolveNpcName(kind, dataId)
    npcNameCache[key] = { name = name, source = source }
    return name, source
end

--- Clear NPC name cache
function ClearNpcNameCache()
    npcNameCache = {}
end

-- Example usage:
-- local name, source = GetNpcName("EventNpc", 1052642)
-- print("Resolved NPC name:", name or "<not found>", "from sheet:", source)
```

### ClassJob Table Builder
```lua
-- Build a table of job information from the ClassJob sheet
function BuildJobTable(firstId, lastId)
    firstId = toNumberSafe(firstId, 1, 1)
    lastId  = toNumberSafe(lastId,  42, firstId)

    local sheet = Excel.GetSheet("ClassJob")
    if not sheet then return nil, "ClassJob sheet not found" end

    local jobs, missing = {}, {}
    for id = firstId, lastId do
        local row = sheet:GetRow(id)
        if row then
            local name = row.Name or row["Name"]
            local abbr = row.Abbreviation or row["Abbreviation"]
            if name and abbr then
                jobs[id] = { name = tostring(name), abbr = tostring(abbr) }
            else
                table.insert(missing, ("id=%d missing Name/Abbreviation"):format(id))
            end
        else
            table.insert(missing, ("id=%d row not found"):format(id))
        end
    end

    if next(jobs) == nil then
        return nil, "ClassJob table empty; " .. table.concat(missing, "; ")
    end
    return jobs, (#missing > 0) and missing or nil
end

-- Get specific job info
function GetJobName(jobId)
    local sheet = Excel.GetSheet("ClassJob")
    if not sheet then return "Unknown" end
    local row = sheet:GetRow(jobId)
    if row and row.Name then
        return tostring(row.Name)
    end
    return "Unknown"
end

function GetJobAbbreviation(jobId)
    local sheet = Excel.GetSheet("ClassJob")
    if not sheet then return "UNK" end
    local row = sheet:GetRow(jobId)
    if row and row.Abbreviation then
        return tostring(row.Abbreviation)
    end
    return "UNK"
end
```

### Gearset Cache System
```lua
local _gearsetCache = nil
local _gearsetStamp = nil

-- Build a table mapping ClassJob ID to gearset info
-- IMPORTANT: Stores uiSlot (idx + 1) for use with /gearset change command!
function BuildGearsetTable(force)
    if _gearsetCache and not force then
        return _gearsetCache
    end

    local gearset = {}
    for idx = 1, 100 do
        local gs = Player.GetGearset(idx)
        if gs and gs.ClassJob and gs.ClassJob > 0 and gs.Name and gs.Name ~= "" then
            -- Store UI slot (idx + 1), not API index!
            gearset[gs.ClassJob] = { uiSlot = idx + 1, name = gs.Name }
        end
    end

    _gearsetCache = gearset
    _gearsetStamp = os.clock()
    return gearset
end

function InvalidateGearsetCache()
    _gearsetCache = nil
    _gearsetStamp = nil
    Dalamud.Log("[Script] Gearset cache invalidated")
end

-- Get gearset for a specific job
-- Returns { uiSlot = N, name = "..." } or nil
function GetGearsetForJob(jobId)
    local gearsets = BuildGearsetTable()
    return gearsets[jobId]
end
```

### Eorzea Time Utilities
```lua
-- Get current Eorzea hour (0-23)
function GetEorzeaHour()
    local et = os.time() * 1440 / 70
    return math.floor((et % 86400) / 3600)
end

-- Convert Eorzea time to Unix timestamp
function EorzeaTimeToUnixTime(eorzeaTime)
    return Instances.Framework.EorzeaTime
end
```

## State Machine Architecture

Complex macros MUST use this state machine pattern:

```lua
-- Define states
CharacterState = {
    ready = Ready,
    working = Working,
    error = Error,
    recovery = Recovery
}

-- State functions
function Ready()
    if someCondition then
        State = CharacterState.working
    elseif errorCondition then
        State = CharacterState.error
    end
end

function Working()
    if workComplete then
        State = CharacterState.ready
    elseif errorOccurred then
        State = CharacterState.error
    end
end

function Error()
    yield("/echo [Script] ERROR: " .. errorMessage)
    State = CharacterState.recovery
end

function Recovery()
    if recoverySuccessful then
        State = CharacterState.ready
    else
        yield("/echo [Script] Recovery failed, stopping")
        StopFlag = true
    end
end

-- Main execution loop
State = CharacterState.ready
while not StopFlag do
    if not IsCharacterBusy() then
        State()
    end
    yield("/wait 0.1")
end
```

### State Machine Best Practices
1. Use descriptive state names (not s1, s2, s3)
2. Keep states focused on single responsibility
3. Handle all state transitions explicitly
4. Include error and recovery states
5. Log important state transitions

## Character Condition Constants

Complete list of all character conditions (102 entries):

```lua
CharacterCondition = {
    normalConditions                   = 1,   -- moving or standing still
    dead                               = 2,
    emoting                            = 3,
    mounted                            = 4,
    crafting                           = 5,
    gathering                          = 6,
    meldingMateria                     = 7,
    operatingSiegeMachine              = 8,
    carryingObject                     = 9,
    mounted2                           = 10,
    inThatPosition                     = 11,
    chocoboRacing                      = 12,
    playingMiniGame                    = 13,
    playingLordOfVerminion             = 14,
    participatingInCustomMatch         = 15,
    performing                         = 16,
    -- 17-24 unused/unknown
    occupied                           = 25,
    inCombat                           = 26,
    casting                            = 27,
    sufferingStatusAffliction          = 28,
    sufferingStatusAffliction2         = 29,
    occupied30                         = 30,
    occupiedInEvent                    = 31,
    occupiedInQuestEvent               = 32,
    occupied33                         = 33,
    boundByDuty34                      = 34,
    occupiedInCutSceneEvent            = 35,
    inDuelingArea                      = 36,
    tradeOpen                          = 37,
    occupied38                         = 38,
    occupiedMateriaExtractionAndRepair = 39,
    executingCraftingAction            = 40,
    preparingToCraft                   = 41,
    executingGatheringAction           = 42,
    fishing                            = 43,
    -- 44 unused
    betweenAreas                       = 45,
    stealthed                          = 46,
    -- 47 unused
    jumping48                          = 48,
    autorunActive                      = 49,
    occupiedSummoningBell              = 50,
    betweenAreasForDuty                = 51,
    systemError                        = 52,
    loggingOut                         = 53,
    conditionLocation                  = 54,
    waitingForDuty                     = 55,
    boundByDuty56                      = 56,
    mounting57                         = 57,
    watchingCutscene                   = 58,
    waitingForDutyFinder               = 59,
    creatingCharacter                  = 60,
    jumping61                          = 61,
    pvpDisplayActive                   = 62,
    sufferingStatusAffliction63        = 63,
    mounting64                         = 64,
    carryingItem                       = 65,
    usingPartyFinder                   = 66,
    usingHousingFunctions              = 67,
    transformed                        = 68,
    onFreeTrial                        = 69,
    beingMoved                         = 70,
    mounting71                         = 71,
    sufferingStatusAffliction72        = 72,
    sufferingStatusAffliction73        = 73,
    registeringForRaceOrMatch          = 74,
    waitingForRaceOrMatch              = 75,
    waitingForTripleTriadMatch         = 76,
    flying                             = 77,
    watchingCutscene78                 = 78,
    inDeepDungeon                      = 79,
    swimming                           = 80,
    diving                             = 81,
    registeringForTripleTriadMatch     = 82,
    waitingForTripleTriadMatch83       = 83,
    participatingInCrossWorldPartyOrAlliance = 84,
    unknown85                          = 85,  -- Part of gathering
    dutyRecorderPlayback               = 86,
    casting87                          = 87,
    inThisState88                      = 88,
    inThisState89                      = 89,
    rolePlaying                        = 90,
    inDutyQueue                        = 91,
    readyingVisitOtherWorld            = 92,
    waitingToVisitOtherWorld           = 93,
    usingFashionAccessory              = 94,
    boundByDuty95                      = 95,
    unknown96                          = 96,
    disguised                          = 97,
    recruitingWorldOnly                = 98,
    unknown99                          = 99,
    editingPortrait                    = 100,
    unknown101                         = 101,
    pilotingMech                       = 102,
}

-- Check condition
if Svc.Condition[CharacterCondition.casting] then
    -- Handle casting
end

if Svc.Condition[CharacterCondition.betweenAreas] then
    -- Player is teleporting
end

if Svc.Condition[CharacterCondition.inCombat] then
    -- Player is in combat
end

-- Comprehensive busy check
function IsCharacterBusy()
    return Svc.Condition[CharacterCondition.casting] or
           Svc.Condition[CharacterCondition.betweenAreas] or
           Svc.Condition[CharacterCondition.beingMoved] or
           Svc.Condition[CharacterCondition.occupiedInQuestEvent] or
           Svc.Condition[CharacterCondition.occupiedInCutSceneEvent] or
           Svc.Condition[CharacterCondition.watchingCutscene] or
           Player.IsBusy
end

-- Wait for not busy
function WaitForNotBusy(timeout)
    timeout = timeout or 30
    local startTime = os.clock()

    while IsCharacterBusy() and (os.clock() - startTime) < timeout do
        yield("/wait 0.1")
    end

    return not IsCharacterBusy()
end

-- Common condition checks
function IsInCombat()
    return Svc.Condition[CharacterCondition.inCombat]
end

function IsMounted()
    return Svc.Condition[CharacterCondition.mounted]
end

function IsFlying()
    return Svc.Condition[CharacterCondition.flying]
end

function IsCrafting()
    return Svc.Condition[CharacterCondition.crafting]
end

function IsGathering()
    return Svc.Condition[CharacterCondition.gathering]
end

function IsFishing()
    return Svc.Condition[CharacterCondition.fishing]
end

function IsBetweenAreas()
    return Svc.Condition[CharacterCondition.betweenAreas] or
           Svc.Condition[CharacterCondition.betweenAreasForDuty]
end
```

## Core Utility Functions

### Plugin Availability Check
```lua
function HasPlugin(pluginName)
    for plugin in luanet.each(Svc.PluginInterface.InstalledPlugins) do
        if plugin.InternalName == pluginName and plugin.IsLoaded then
            return true
        end
    end
    return false
end

-- Usage
if not HasPlugin("RequiredPlugin") then
    yield("/echo [Script] Missing required plugin: RequiredPlugin")
    StopFlag = true
end

--- List all installed plugins with their status
function GetPlugins()
    local plugins = {}
    for plugin in luanet.each(Svc.PluginInterface.InstalledPlugins) do
        table.insert(plugins, { name = plugin.InternalName, loaded = plugin.IsLoaded })
    end
    table.sort(plugins, function(a,b) return a.name:lower() < b.name:lower() end)

    Log("Installed plugins:")
    for _, p in ipairs(plugins) do
        Log("  %s | Enabled: %s", p.name, tostring(p.loaded))
    end
    return plugins
end
```

### Advanced IPC Subscriber Access

For accessing IPC functions not exposed through the standard `IPC.*` interface, use reflection-based subscribers.

```lua
import "System"

-- IPC subscriber cache
local ipc_subscribers = {}

--- Get a generic method from a type using reflection
-- @param targetType Type - The target .NET type
-- @param method_name string - Method name to find
-- @param genericTypes table - Array of Type objects for generics
-- @return MethodInfo - The constructed generic method
local function get_generic_method(targetType, method_name, genericTypes)
    local genericArgsArr = luanet.make_array(Type, genericTypes)
    local methods = targetType:GetMethods()
    for i = 0, methods.Length - 1 do
        local m = methods[i]
        if m.Name == method_name and m.IsGenericMethodDefinition
           and m:GetGenericArguments().Length == genericArgsArr.Length then
            local ok, constructed = pcall(function()
                return m:MakeGenericMethod(genericArgsArr)
            end)
            if ok then return constructed end
        end
    end
    return nil
end

--- Register an IPC subscriber for a signature
-- @param ipc_signature string - The IPC signature (e.g., "PluginName.MethodName")
-- @param result_type string|nil - .NET type for return value (nil for actions)
-- @param arg_types table - Array of .NET type strings for arguments
-- @return boolean - True if registered successfully
function RequireIPC(ipc_signature, result_type, arg_types)
    if ipc_subscribers[ipc_signature] then
        return true  -- Already loaded
    end

    local pi = Svc.PluginInterface
    if not pi then
        Log("RequireIPC: PluginInterface not available")
        return false
    end

    arg_types = arg_types or {}
    -- Append result type (System.Object for actions)
    arg_types[#arg_types + 1] = result_type or 'System.Object'

    -- Convert string types to Type objects
    for i, v in pairs(arg_types) do
        arg_types[i] = Type.GetType(v)
    end

    local method = get_generic_method(pi:GetType(), 'GetIpcSubscriber', arg_types)
    if not method then
        Log("RequireIPC: GetIpcSubscriber not found for %s", ipc_signature)
        return false
    end

    local sig = luanet.make_array(Object, { ipc_signature })
    local subscriber = method:Invoke(pi, sig)
    if not subscriber then
        Log("RequireIPC: IPC not found: %s", ipc_signature)
        return false
    end

    local kind = (result_type == nil) and "action" or "function"
    ipc_subscribers[ipc_signature] = { kind = kind, sub = subscriber }
    Log("RequireIPC: Loaded %s IPC: %s", kind, ipc_signature)
    return true
end

--- Invoke a registered IPC subscriber
-- @param ipc_signature string - The IPC signature
-- @param ... any - Arguments to pass
-- @return any - Result from function IPC, nil from action IPC
function InvokeIPC(ipc_signature, ...)
    local entry = ipc_subscribers[ipc_signature]
    if not entry then
        Log("InvokeIPC: IPC not loaded: %s", ipc_signature)
        return nil
    end

    if entry.kind == "function" then
        return entry.sub:InvokeFunc(...)
    else
        entry.sub:InvokeAction(...)
        return nil
    end
end

--- Clear IPC subscriber cache
function ResetIPCCache()
    ipc_subscribers = {}
    Log("IPC subscriber cache cleared")
end
```

#### IPC Usage Example

```lua
-- Register an IPC function that returns a boolean
RequireIPC("SomePlugin.IsReady", "System.Boolean", {})

-- Register an IPC action (no return value) with string argument
RequireIPC("SomePlugin.DoSomething", nil, {"System.String"})

-- Invoke them
local ready = InvokeIPC("SomePlugin.IsReady")
if ready then
    InvokeIPC("SomePlugin.DoSomething", "parameter")
end
```

### Distance Calculations
```lua
function GetDistanceToPoint(targetX, targetY, targetZ)
    if not Player.Available or not Player.Position then
        return math.huge
    end

    local px = Player.Position.X
    local py = Player.Position.Y
    local pz = Player.Position.Z

    local dx = targetX - px
    local dy = targetY - py
    local dz = targetZ - pz

    return math.sqrt(dx * dx + dy * dy + dz * dz)
end

function IsAtPosition(targetX, targetY, targetZ, tolerance)
    tolerance = tolerance or 2.0
    return GetDistanceToPoint(targetX, targetY, targetZ) <= tolerance
end

function DistanceBetween(x1, y1, z1, x2, y2, z2)
    local dx = x2 - x1
    local dy = y2 - y1
    local dz = z2 - z1
    return math.sqrt(dx * dx + dy * dy + dz * dz)
end

function GetDistanceToEntity(entity)
    if not entity or not entity.Position then
        return math.huge
    end
    local playerPos = Player.Position
    local entityPos = entity.Position
    local dx = entityPos.X - playerPos.X
    local dy = entityPos.Y - playerPos.Y
    local dz = entityPos.Z - playerPos.Z
    return math.sqrt(dx * dx + dy * dy + dz * dz)
end
```

### Inventory Management
```lua
-- Get free inventory slots
local freeSlots = Inventory.GetFreeInventorySlots()

-- Get item count
local itemCount = Inventory.GetItemCount(itemId)

-- Get HQ item count
local hqCount = Inventory.GetHqItemCount(itemId)

-- Get collectable item count
local collectableCount = Inventory.GetCollectableItemCount(itemId, collectability)

-- Use item
local item = Inventory.GetInventoryItem(itemId)
if item then
    item:Use()
end

-- Helper functions
function GetFreeInventorySlots()
    return Inventory.GetFreeInventorySlots()
end

function HasInventorySpace(requiredSlots)
    requiredSlots = requiredSlots or 1
    return Inventory.GetFreeInventorySlots() >= requiredSlots
end

function GetItemCount(itemId)
    return Inventory.GetItemCount(itemId)
end

function HasItem(itemId, requiredCount)
    requiredCount = requiredCount or 1
    return Inventory.GetItemCount(itemId) >= requiredCount
end

function ValidateInventorySpace(requiredSlots, operation)
    requiredSlots = requiredSlots or 1
    operation = operation or "operation"

    if not HasInventorySpace(requiredSlots) then
        yield("/echo [Script] ERROR: Not enough inventory space for " .. operation)
        return false
    end
    return true
end
```

### Timing Constants and Sleep
```lua
-- Standard timing constants
TIME = {
    POLL    = 0.10,  -- canonical polling step
    TIMEOUT = 10.0,  -- default time budget
    STABLE  = 0.0    -- default stability window
}

-- Sleep helper (yields with /wait)
function Sleep(seconds)
    local s = seconds or 0
    s = tonumber(s) or 0
    if s < 0 then s = 0 end
    s = math.floor(s * 10 + 0.5) / 10
    yield("/wait " .. s)
end
```

### Number Helper (Safe Parsing with Clamping)
```lua
-- Safe number parsing with optional min/max clamping
function toNumberSafe(s, default, min, max)
    if s == nil then return default end
    local str = tostring(s):gsub("[^%d%-%.]", "")
    local n = tonumber(str)
    if n == nil then return default end
    if min ~= nil and n < min then n = min end
    if max ~= nil and n > max then n = max end
    return n
end

-- Examples:
-- toNumberSafe("123", 0)           -> 123
-- toNumberSafe("abc", 0)           -> 0
-- toNumberSafe("50", 0, 0, 100)    -> 50
-- toNumberSafe("150", 0, 0, 100)   -> 100 (clamped)
-- toNumberSafe("-10", 0, 0, 100)   -> 0 (clamped)
```

### Wait and Timeout Patterns
```lua
function WaitWithTimeout(condition, timeout, interval)
    timeout = timeout or 30
    interval = interval or 0.1
    local startTime = os.clock()

    while not condition() and (os.clock() - startTime) < timeout do
        yield("/wait " .. interval)
    end

    return condition()
end

-- Wait until condition with timeout (basic version)
function WaitUntil(condition, timeout)
    local startTime = os.clock()
    while not condition() and (os.clock() - startTime) < timeout do
        yield("/wait 0.1")
    end
    return condition()
end
```

### Advanced WaitUntil with Stability Window
```lua
--[[
WaitUntil with stability window - condition must remain true for stableSec
continuously before success is returned.

Usage:
  WaitUntil(predicateFn, timeoutSec, pollSec, stableSec)

  predicateFn : function() -> true/false  (checked each poll)
  timeoutSec  : max seconds before giving up (default 10)
  pollSec     : seconds between checks (default 0.10)
  stableSec   : must remain true for this many seconds continuously (default 0)

Returns: true if condition satisfied, false on timeout

Examples:
  -- Wait until addon "Talk" is ready (10s max):
  WaitUntilStable(function()
      return Addons.GetAddon("Talk").Ready
  end, 10.0)

  -- Wait until crafting condition holds for 2s (15s max):
  WaitUntilStable(function()
      return Svc.Condition[CharacterCondition.crafting]
  end, 15.0, 0.10, 2.0)
]]
function WaitUntilStable(predicateFn, timeoutSec, pollSec, stableSec)
    timeoutSec = toNumberSafe(timeoutSec, TIME.TIMEOUT, 0.1)
    pollSec    = toNumberSafe(pollSec,    TIME.POLL,   0.01)
    stableSec  = toNumberSafe(stableSec,  TIME.STABLE, 0.0)

    local start     = os.clock()
    local holdStart = nil

    while (os.clock() - start) < timeoutSec do
        local ok, res = pcall(predicateFn)
        if ok and res then
            if not holdStart then holdStart = os.clock() end
            if (os.clock() - holdStart) >= stableSec then return true end
        else
            holdStart = nil
        end
        Sleep(pollSec)
    end
    return false
end

-- Wait for condition to be stable for a specified duration
function WaitConditionStable(conditionIdx, want, stableSec, timeoutSec, pollSec)
    want       = (want ~= false)
    stableSec  = toNumberSafe(stableSec,  2.0,   0.0)
    timeoutSec = toNumberSafe(timeoutSec, 15.0,  0.1)
    pollSec    = toNumberSafe(pollSec,    TIME.POLL, 0.01)

    if not (Svc and Svc.Condition) then
        Dalamud.Log("[Script] WaitConditionStable: Svc.Condition unavailable")
        return false
    end

    local ok = WaitUntilStable(function()
        return Svc.Condition[conditionIdx] == want
    end, timeoutSec, pollSec, stableSec)

    if not ok then
        Dalamud.Log("[Script] WaitConditionStable: timeout")
    end
    return ok
end
```

### Safe Function Execution
```lua
function SafeExecute(func, errorMessage)
    local success, result = pcall(func)
    if success then
        return result, nil
    else
        return nil, errorMessage or tostring(result)
    end
end
```

### Retry Pattern
```lua
function RetryWithBackoff(func, maxRetries, baseDelay)
    maxRetries = maxRetries or 3
    baseDelay = baseDelay or 1

    for attempt = 1, maxRetries do
        local success, result = pcall(func)
        if success then
            return result, nil
        end

        if attempt < maxRetries then
            local delay = baseDelay * (2 ^ (attempt - 1))
            yield("/echo [Script] Attempt " .. attempt .. " failed, retrying in " .. delay .. "s")
            yield("/wait " .. delay)
        end
    end

    return nil, "Function failed after " .. maxRetries .. " attempts"
end
```

## Addon Interactions

### Addon State Checking
```lua
-- Check if addon is ready
if Addons.GetAddon("AddonName").Ready then
    -- Addon is ready
end

-- Wait for addon to be ready
while not Addons.GetAddon("AddonName").Ready do
    yield("/wait 0.1")
end

-- Check if addon is visible
if Addons.GetAddon("AddonName").Visible then
    -- Addon is visible
end
```

### Addon Callbacks
```lua
-- Basic callback
yield("/callback AddonName true 0")

-- Callback with parameters
yield("/callback AddonName true 1 2 3")

-- Close addon
yield("/callback AddonName false -1")
```

### Addon Node Access
```lua
-- Get addon node
local node = Addons.GetAddon("AddonName"):GetNode(1, 2, 3)

-- Get node text
local text = node.Text

-- Check if node is visible
if node.Visible then
    -- Node is visible
end
```

### Safe Addon Functions
```lua
function IsAddonReady(addonName)
    return Addons.GetAddon(addonName).Ready
end

function WaitForAddonReady(addonName, timeout)
    timeout = timeout or 10
    local startTime = os.clock()

    while not Addons.GetAddon(addonName).Ready and (os.clock() - startTime) < timeout do
        yield("/wait 0.1")
    end

    return Addons.GetAddon(addonName).Ready
end

function SafeAddonCallback(addonName, ...)
    if not IsAddonReady(addonName) then
        yield("/echo [Script] Addon not ready: " .. addonName)
        return false
    end

    local args = {...}
    local callbackStr = "/callback " .. addonName .. " true"
    for _, arg in ipairs(args) do
        callbackStr = callbackStr .. " " .. tostring(arg)
    end
    yield(callbackStr)
    return true
end
```

## Logging and Echo

```lua
-- Standard logging (to Dalamud log)
Dalamud.Log("[ScriptName] Message")

-- User echo (visible in game)
yield("/echo [ScriptName] User message")

-- Formatted logging
yield("/echo [Script] Value: " .. tostring(value))

-- Error logging
yield("/echo [Script] ERROR: Description")
```

## Teleportation Pattern

```lua
function TeleportTo(aetheryteName)
    yield("/li tp " .. aetheryteName)
    yield("/wait 1")

    -- Wait for casting to begin
    while Svc.Condition[CharacterCondition.casting] do
        yield("/wait 1")
    end

    -- Wait for teleport to complete
    while Svc.Condition[CharacterCondition.betweenAreas] do
        yield("/wait 1")
    end

    yield("/wait 1")
end
```

## Svc.ClientState Access

Access client state information through `Svc.ClientState`:

```lua
-- Basic client state properties
local territoryType = Svc.ClientState.TerritoryType  -- Current zone ID
local mapId = Svc.ClientState.MapId                  -- Current map ID
local isLoggedIn = Svc.ClientState.IsLoggedIn        -- Login status
local localContentId = Svc.ClientState.LocalContentId -- Character content ID

-- Local player access
local lp = Svc.ClientState.LocalPlayer
if lp then
    -- World information
    local function try(fn) local ok, v = pcall(fn); return ok and v or nil end
    local currentWorld = try(function() return lp.CurrentWorld.Value.Name:ToString() end)
    local homeWorld = try(function() return lp.HomeWorld.Value.Name:ToString() end)

    -- ClassJob information
    local jobId = try(function() return lp.ClassJob.RowId end)
              or try(function() return lp.ClassJob.Value.RowId end)
    local jobAbbr = try(function() return lp.ClassJob.Value.Abbreviation:ToString() end)
    local jobName = try(function() return lp.ClassJob.Value.Name:ToString() end)

    print(("World: %s (Home: %s)"):format(currentWorld or "?", homeWorld or "?"))
    print(("Job: %s (%s) ID=%d"):format(jobName or "?", jobAbbr or "?", jobId or 0))
end
```

## Debug and Reflection Utilities

Utilities for inspecting objects at runtime (useful for debugging and discovery).

```lua
--- Print a formatted heading
local function head(label) print(("\n== %s =="):format(label)) end

--- Reflect & dump an instance's properties (name, CLR type, current value)
-- @param label string - Label for the dump
-- @param obj any - Object to inspect
function DumpInstance(label, obj)
    if obj == nil then print(label .. ": <nil>"); return end
    local okT, t = pcall(function() return obj:GetType() end)
    if not okT or not t then print(label .. ": no GetType()"); return end

    head(label)
    print("Type:", t.FullName)
    local props = t:GetProperties()
    for i = 0, props.Length - 1 do
        local p = props[i]
        local okV, val = pcall(function() return p:GetValue(obj, nil) end)
        local v = okV and val or "<error>"
        local vstr = (v == nil and "<nil>")
                  or ((type(v) == "boolean" or type(v) == "number") and tostring(v))
                  or tostring(v)
        print(string.format("%-22s : %-12s = %s", p.Name, p.PropertyType.Name, vstr))
    end
end

--- List property names & CLR types on an object without invoking getters
-- @param label string - Label for the dump
-- @param obj any - Object to inspect
function DumpPropertyTypes(label, obj)
    if not obj then print(label .. ": <nil>"); return end
    local okT, t = pcall(function() return obj:GetType() end)
    if not okT or not t then print(label .. ": no GetType()"); return end

    head(label .. " (property types)")
    print("Type:", t.FullName)
    local props = t:GetProperties()
    for i = 0, props.Length - 1 do
        local p = props[i]
        print(string.format("%-22s : %s", p.Name, p.PropertyType.Name))
    end
end

--- Dump only the *type* (shape) of a property on a parent object
-- @param label string - Label for the dump
-- @param parentObj any - Parent object
-- @param propName string - Property name to inspect
function DumpPropertyType(label, parentObj, propName)
    if not parentObj then print(label .. ": parent <nil>"); return end
    local ok, pt = pcall(function()
        local t = parentObj:GetType()
        local p = t:GetProperty(propName)
        return p and p.PropertyType or nil
    end)
    if not ok or not pt then print(label .. ": no type available"); return end

    head(label .. " (property type)")
    print("Type:", pt.FullName)
    local props = pt:GetProperties()
    for i = 0, props.Length - 1 do
        local p = props[i]
        print(string.format("%-22s : %s", p.Name, p.PropertyType.Name))
    end
end

-- Example usage:
-- DumpInstance("Player.Entity", Player.Entity)
-- DumpPropertyTypes("Svc.Targets", Svc.Targets)
-- DumpPropertyType("Player.Entity.Target", Player.Entity, "Target")
```

## SND Built-in Global Functions

These are global functions available in SND Lua macros without needing any plugin.

### Action Execution
```lua
-- Execute a game action safely by ID
ExecuteActionSafeNumber(number actionId, number actionType) → nil

-- Execute action by name
ExecuteAction(string actionName) → nil

-- Execute action on target
ExecuteActionOnTarget(string actionName, number targetId) → nil
```

### String/Variable Storage
```lua
-- Get stored string value
GetString(string key) → string

-- Set string value
SetString(string key, string value) → nil

-- Get stored number value
GetNumber(string key) → number

-- Set number value
SetNumber(string key, number value) → nil
```

### Casting Information
```lua
-- Get casting-related number value
GetCastingNumber(string key) → number

-- Set casting number value
SetCastingNumber(string key, number value) → nil

-- Check if player is casting
IsCasting() → boolean

-- Get current cast time remaining
GetCastTimeRemaining() → number
```

### Targeting Functions
```lua
-- Get focus target
FocusTarget() → Entity

-- Set target by entity
SetTarget(Entity entity) → nil

-- Get target info
GetTargetInfo() → table
```

### Movement Checks
```lua
-- Check if something is nearing (distance check)
GetNearing(number x, number y, number z, number distance) → boolean

-- Check if player is moving
IsMoving() → boolean

-- Get distance to coordinates
GetDistanceTo(number x, number y, number z) → number
```

### Addon/UI Access
```lua
-- Get addon by name (returns addon wrapper)
GetAddon(string addonName) → Addon

-- Check if addon is visible
IsAddonVisible(string addonName) → boolean

-- Check if addon is ready
IsAddonReady(string addonName) → boolean
```

## SND Commands Reference

### Macro Control Commands
```lua
-- Run a specific macro by name
yield("/pcraft run MacroName")

-- Run all macros marked as loop
yield("/pcraft runall")

-- Run a macro in step mode (pause between steps)
yield("/pcraft step MacroName")

-- Pause all running macros
yield("/pcraft pause")

-- Resume paused macros
yield("/pcraft resume")
yield("/pcraft resume all")

-- Stop current macro
yield("/pcraft stop")

-- Stop all running macros
yield("/pcraft stopall")

-- Stop loop macros only
yield("/pcraft stoploop")

-- Toggle macro execution
yield("/pcraft toggle")

-- Show help
yield("/pcraft help")
```

### Yield Commands (In-Macro Commands)
```lua
-- Execute a game action
yield("/action ActionName")
yield("/ac ActionName")        -- Short form

-- Click a pre-defined UI button
yield("/click ButtonName")

-- Hold a key with auto-effects (stops at end of macro)
yield("/hold KeyName")

-- Use an item from inventory
yield("/item ItemName")

-- Loop - copy current macro pattern
yield("/loop")
yield("/loop 5")               -- Loop 5 times

-- Remove held keyboard keys
yield("/notify")

-- Require specific stats/items before continuing
yield("/requirestats")
yield("/require ItemName")

-- Send key to game
yield("/send KeyName")
yield("/sendkey KeyName")

-- Target commands
yield("/target TargetName")
yield("/targetenemy")

-- Wait commands
yield("/wait 1.5")             -- Wait 1.5 seconds
yield("/waitaddon AddonName")  -- Wait for addon to be ready
```

### Available Click Targets
Common `/click` targets for UI automation:
```lua
-- Selection dialogs
yield("/click AddonReaderSelect")
yield("/click BannerSelect")
yield("/click SelectString")
yield("/click SelectYesno")

-- Banking/Trading
yield("/click Bank")
yield("/click Bankroll")

-- Duty Finder
yield("/click DutyFinder")
yield("/click ContentsFinderConfirm")

-- Grand Company
yield("/click GrandCompanySupplyList")

-- Housing
yield("/click HousingAethernet")

-- Shops
yield("/click InclusionShop")
yield("/click Shop")

-- Talk/Dialog
yield("/click Talk Click")

-- Cancel/Close
yield("/click Cancel")
```

## Best Practices

1. **Always check prerequisites** before starting operations
2. **Use timeouts** for all waiting operations
3. **Check plugin availability** before using plugin APIs
4. **Use appropriate wait times**: 0.1s for condition checks, 1s for movement/teleportation
5. **Handle all state transitions** explicitly in state machines
6. **Provide clear error messages** with `[Script]` prefix
7. **Validate configuration values** before use
8. **Use semantic versioning** (MAJOR.MINOR.PATCH)
9. **Update version fingerprint** for any changes
10. **Use pcall** for risky operations
11. **Check Player.Available** before player operations
12. **Use Entity system** for NPC interactions
13. **Use Excel.GetRow** for game data lookups
