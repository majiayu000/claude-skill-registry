---
name: SND FATE Farming
description: Use this skill when implementing FATE farming automation in SND macros. Covers FATE detection, targeting, level sync, participation, and farming patterns.
---

# FATE Farming for SND

This skill covers FATE (Full Active Time Event) automation patterns for SND macros.

## Prerequisites

```lua
-- FATEs require navigation and combat plugins
if not HasPlugin("vnavmesh") then
    yield("/echo [Script] vnavmesh plugin required for FATE farming")
    StopFlag = true
    return
end
```

## FATE API Reference (SND Built-in)

### Core FATE Functions via Fates Object

```lua
-- Get all active FATEs in the zone (SND built-in)
local fates = Fates.GetActiveFates()

-- Iterate through FATEs
for i = 0, fates.Count - 1 do
    local fate = fates[i]
    -- Process fate
end

-- Get nearest FATE (SND built-in)
local nearestFate = Fates.GetNearestFate()
```

### FATE Object Properties (Built-in)
```lua
-- FATE identification
fate.Id              -- Unique FATE ID
fate.Name            -- FATE name string

-- FATE state
fate.State           -- FateState enum
fate.Progress        -- Completion percentage (0-100)
fate.IsBonus         -- Boolean, true if bonus FATE

-- FATE timing
fate.Duration        -- Total duration in seconds
fate.StartTimeEpoch  -- Unix timestamp when FATE started

-- FATE location
fate.Location        -- Vector3 position (center of FATE)
fate.IconId          -- Icon ID (60722 = boss FATE)

-- Player status
fate.InFate          -- Boolean, true if player is inside FATE area

-- Collection FATEs
fate.EventItem       -- Item ID for collection FATEs
```

### FATE State Enum
```lua
FateState = {
    Preparation = 1,  -- FATE spawning
    Running = 2,      -- FATE active
    Ending = 3,       -- FATE completing
    Ended = 4,        -- FATE finished
    Failed = 5        -- FATE failed
}

-- Check if FATE is active
function IsFateActive(fate)
    if fate.State == nil then
        return false
    end
    return fate.State ~= FateState.Ending and
           fate.State ~= FateState.Ended and
           fate.State ~= FateState.Failed
end

-- Check if player is inside any active FATE
function InActiveFate()
    local activeFates = Fates.GetActiveFates()
    for i = 0, activeFates.Count - 1 do
        if activeFates[i].InFate == true and IsFateActive(activeFates[i]) then
            return true
        end
    end
    return false
end
```

### Entity FATE ID Access
```lua
-- Import EntityWrapper for FATE entity access
local function load_type(type_path)
    local assembly = type_path:match("^[^%.]+")
    luanet.load_assembly(assembly)
    return luanet.import_type(type_path)
end

EntityWrapper = load_type('SomethingNeedDoing.LuaMacro.Wrappers.EntityWrapper')

-- Get FATE ID from an entity (mob)
local fateId = EntityWrapper(entity).FateId

-- Target closest FATE enemy
function AttemptToTargetClosestFateEnemy()
    local closestTarget = nil
    local closestTargetDistance = math.maxinteger

    for i = 0, Svc.Objects.Length - 1 do
        local obj = Svc.Objects[i]
        if obj ~= nil and obj.IsTargetable and obj:IsHostile() and
           not obj.IsDead and EntityWrapper(obj).FateId > 0
        then
            local dist = GetDistanceToPoint(obj.Position)
            if dist < closestTargetDistance then
                closestTargetDistance = dist
                closestTarget = obj
            end
        end
    end

    if closestTarget ~= nil then
        Svc.Targets.Target = closestTarget
    end
end
```

## Alternative FATE Data Access (FateTable)

### Legacy Core FATE Functions

```lua
--- Get a list of all active FATEs in the current zone
-- @return table - Array of FATE objects
function GetActiveFates()
    local fates = {}
    local fateTable = Svc.FateTable

    if not fateTable then
        return fates
    end

    for i = 0, fateTable.Length - 1 do
        local fate = fateTable[i]
        if fate then
            table.insert(fates, fate)
        end
    end

    return fates
end

--- Get FATE by index from the FATE table
-- @param index number - Index in the FATE table
-- @return Fate|nil - The FATE object or nil
function GetFateByIndex(index)
    local fateTable = Svc.FateTable
    if fateTable and index >= 0 and index < fateTable.Length then
        return fateTable[index]
    end
    return nil
end

--- Get the number of active FATEs
-- @return number - Count of active FATEs
function GetFateCount()
    local fateTable = Svc.FateTable
    return fateTable and fateTable.Length or 0
end
```

### FATE Properties

```lua
--- FATE object properties:
-- fate.FateId       - Unique FATE ID
-- fate.Name         - FATE name (localized)
-- fate.Level        - FATE level
-- fate.MaxLevel     - Maximum synced level
-- fate.Progress     - Completion percentage (0-100)
-- fate.TimeRemaining - Seconds remaining
-- fate.State        - FATE state (Running, Preparation, etc.)
-- fate.Position     - Vector3 position (X, Y, Z)
-- fate.Radius       - FATE area radius

--- Check if a FATE is running (not in preparation)
-- @param fate Fate - The FATE object
-- @return boolean - True if running
function IsFateRunning(fate)
    if not fate then
        return false
    end
    return fate.State == 2  -- State 2 = Running
end

--- Check if a FATE is in preparation
-- @param fate Fate - The FATE object
-- @return boolean - True if in preparation
function IsFatePreparing(fate)
    if not fate then
        return false
    end
    return fate.State == 1  -- State 1 = Preparation
end

--- Get distance to FATE center
-- @param fate Fate - The FATE object
-- @return number - Distance in yalms
function GetDistanceToFate(fate)
    if not fate or not Player.Available then
        return 99999
    end

    local playerPos = Player.Position
    local fatePos = fate.Position

    local dx = playerPos.X - fatePos.X
    local dy = playerPos.Y - fatePos.Y
    local dz = playerPos.Z - fatePos.Z

    return math.sqrt(dx*dx + dy*dy + dz*dz)
end

--- Check if player is within FATE area
-- @param fate Fate - The FATE object
-- @return boolean - True if inside
function IsInsideFate(fate)
    if not fate then
        return false
    end
    return GetDistanceToFate(fate) <= fate.Radius
end
```

### FATE Filtering and Selection

```lua
--- Filter FATEs by criteria
-- @param options table - Filter options
-- @return table - Filtered FATE array
function FilterFates(options)
    options = options or {}
    local minLevel = options.minLevel or 1
    local maxLevel = options.maxLevel or 100
    local minProgress = options.minProgress or 0
    local maxProgress = options.maxProgress or 100
    local maxDistance = options.maxDistance or 99999
    local runningOnly = options.runningOnly or false
    local excludeIds = options.excludeIds or {}

    local fates = GetActiveFates()
    local filtered = {}

    -- Build exclusion set for fast lookup
    local excludeSet = {}
    for _, id in ipairs(excludeIds) do
        excludeSet[id] = true
    end

    for _, fate in ipairs(fates) do
        local valid = true

        -- Check exclusion list
        if excludeSet[fate.FateId] then
            valid = false
        end

        -- Check level range
        if valid and (fate.Level < minLevel or fate.Level > maxLevel) then
            valid = false
        end

        -- Check progress range
        if valid and (fate.Progress < minProgress or fate.Progress > maxProgress) then
            valid = false
        end

        -- Check distance
        if valid and GetDistanceToFate(fate) > maxDistance then
            valid = false
        end

        -- Check running state
        if valid and runningOnly and not IsFateRunning(fate) then
            valid = false
        end

        if valid then
            table.insert(filtered, fate)
        end
    end

    return filtered
end

--- Get the nearest FATE
-- @param options table - Optional filter options
-- @return Fate|nil - The nearest FATE or nil
function GetNearestFate(options)
    local fates = FilterFates(options)
    local nearest = nil
    local nearestDist = 99999

    for _, fate in ipairs(fates) do
        local dist = GetDistanceToFate(fate)
        if dist < nearestDist then
            nearest = fate
            nearestDist = dist
        end
    end

    return nearest
end

--- Get the highest progress FATE (for quick completion)
-- @param options table - Optional filter options
-- @return Fate|nil - The highest progress FATE or nil
function GetHighestProgressFate(options)
    options = options or {}
    options.minProgress = options.minProgress or 50  -- At least 50% by default
    options.runningOnly = true

    local fates = FilterFates(options)
    local best = nil
    local bestProgress = 0

    for _, fate in ipairs(fates) do
        if fate.Progress > bestProgress then
            best = fate
            bestProgress = fate.Progress
        end
    end

    return best
end

--- Get FATEs by type/name pattern
-- @param namePattern string - Lua pattern to match FATE name
-- @param options table - Optional filter options
-- @return table - Matching FATEs
function GetFatesByName(namePattern, options)
    local fates = FilterFates(options)
    local matches = {}

    for _, fate in ipairs(fates) do
        if fate.Name and fate.Name:find(namePattern) then
            table.insert(matches, fate)
        end
    end

    return matches
end
```

## Level Sync

### Check and Apply Level Sync

```lua
--- Character condition for level sync
local CharacterCondition = {
    levelSynced = 53  -- Level-synced condition
}

--- Check if player is level synced
-- @return boolean - True if synced
function IsLevelSynced()
    return Svc.Condition[CharacterCondition.levelSynced]
end

--- Check if player needs to sync for a FATE
-- @param fate Fate - The FATE object
-- @return boolean - True if sync needed
function NeedsLevelSync(fate)
    if not fate or not Player.Available then
        return false
    end

    -- If already synced, no need
    if IsLevelSynced() then
        return false
    end

    -- Check if player level exceeds FATE max level
    return Player.Level > fate.MaxLevel
end

--- Apply level sync for FATE
-- @return boolean - True if sync applied or already synced
function ApplyLevelSync()
    if IsLevelSynced() then
        return true
    end

    yield("/levelsync on")
    yield("/wait 0.5")

    return IsLevelSynced()
end

--- Remove level sync
-- @return boolean - True if sync removed
function RemoveLevelSync()
    if not IsLevelSynced() then
        return true
    end

    yield("/levelsync off")
    yield("/wait 0.5")

    return not IsLevelSynced()
end
```

## FATE Participation

### Navigation to FATE

```lua
--- Navigate to a FATE's center
-- @param fate Fate - The FATE object
-- @param fly boolean - Whether to fly (default: true)
-- @param timeout number - Navigation timeout (default: 120)
-- @return boolean - True if reached
function NavigateToFate(fate, fly, timeout)
    if not fate then
        return false
    end

    fly = fly ~= false  -- Default true
    timeout = timeout or 120

    local targetPos = fate.Position

    -- Check if vnavmesh is ready
    if not IPC.vnavmesh.IsReady() then
        yield("/echo [Script] vnavmesh not ready")
        return false
    end

    -- Start navigation
    IPC.vnavmesh.PathfindAndMoveTo(targetPos, fly)

    -- Wait for arrival or timeout
    local startTime = os.clock()
    while (os.clock() - startTime) < timeout do
        -- Check if we've arrived
        if IsInsideFate(fate) then
            IPC.vnavmesh.Stop()
            return true
        end

        -- Check if navigation stopped unexpectedly
        if not IPC.vnavmesh.IsRunning() then
            -- Restart if not at destination
            if not IsInsideFate(fate) then
                IPC.vnavmesh.PathfindAndMoveTo(targetPos, fly)
            end
        end

        yield("/wait 0.5")
    end

    IPC.vnavmesh.Stop()
    yield("/echo [Script] FATE navigation timeout")
    return false
end

--- Navigate to nearest enemy in FATE
-- @param fate Fate - The FATE object
-- @return boolean - True if navigating
function NavigateToFateEnemy(fate)
    if not fate then
        return false
    end

    -- Find nearest FATE enemy
    local nearestEnemy = nil
    local nearestDist = 99999

    for _, obj in pairs(GetNearbyGameObjects(100)) do
        if obj.ObjectKind == ObjectKind.BattleNpc and
           obj.FateId == fate.FateId and
           obj.IsTargetable and
           not obj.IsDead then
            local dist = GetDistanceToObject(obj)
            if dist < nearestDist then
                nearestEnemy = obj
                nearestDist = dist
            end
        end
    end

    if nearestEnemy then
        IPC.vnavmesh.PathfindAndMoveTo(nearestEnemy.Position, false)
        return true
    end

    return false
end
```

### FATE Combat Loop

```lua
--- Basic FATE combat participation
-- @param fate Fate - The FATE object
-- @param combatFunc function - Optional combat handler function
-- @param timeout number - Maximum time in FATE (default: 600)
-- @return boolean, string - Success and reason
function ParticipateFate(fate, combatFunc, timeout)
    if not fate then
        return false, "No FATE specified"
    end

    timeout = timeout or 600  -- 10 minutes default
    local startTime = os.clock()

    yield("/echo [Script] Participating in FATE: " .. (fate.Name or "Unknown"))

    -- Apply level sync if needed
    if NeedsLevelSync(fate) then
        if not ApplyLevelSync() then
            return false, "Failed to apply level sync"
        end
    end

    -- Main participation loop
    while (os.clock() - startTime) < timeout do
        -- Check if FATE is still active
        local currentFate = GetFateByFateId(fate.FateId)
        if not currentFate or not IsFateRunning(currentFate) then
            yield("/echo [Script] FATE completed or ended")
            return true, "FATE completed"
        end

        -- Update progress info
        if currentFate.Progress >= 100 then
            yield("/echo [Script] FATE 100% complete")
            return true, "FATE completed"
        end

        -- Check if still inside FATE area
        if not IsInsideFate(currentFate) then
            yield("/echo [Script] Left FATE area, returning...")
            NavigateToFate(currentFate, false, 30)
        end

        -- Execute combat logic
        if combatFunc then
            combatFunc(currentFate)
        else
            DefaultFateCombat(currentFate)
        end

        yield("/wait 0.5")
    end

    return false, "FATE participation timeout"
end

--- Default combat behavior for FATEs
-- @param fate Fate - The FATE object
function DefaultFateCombat(fate)
    -- Target nearest FATE enemy if no target
    if not HasTarget() or not IsTargetFateEnemy(fate) then
        TargetNearestFateEnemy(fate)
    end

    -- Move to target if too far
    if HasTarget() and GetTargetDistance() > 20 then
        local target = GetTarget()
        if target then
            IPC.vnavmesh.PathfindAndMoveTo(target.Position, false)
        end
    end

    -- Attack (relies on rotation plugin)
    if HasTarget() and GetTargetDistance() <= 25 then
        -- Combat plugins like BossMod/RSR handle rotations
        yield("/wait 0.1")
    end
end

--- Get a FATE by its FateId
-- @param fateId number - The FATE ID
-- @return Fate|nil - The FATE or nil
function GetFateByFateId(fateId)
    local fates = GetActiveFates()
    for _, fate in ipairs(fates) do
        if fate.FateId == fateId then
            return fate
        end
    end
    return nil
end
```

### Targeting FATE Enemies

```lua
--- Target the nearest enemy belonging to a FATE
-- @param fate Fate - The FATE object
-- @return boolean - True if target acquired
function TargetNearestFateEnemy(fate)
    if not fate then
        return false
    end

    local nearestEnemy = nil
    local nearestDist = 99999

    -- Iterate game objects to find FATE enemies
    for _, obj in pairs(GetNearbyGameObjects(50)) do
        if obj.ObjectKind == ObjectKind.BattleNpc and
           obj.FateId == fate.FateId and
           obj.IsTargetable and
           not obj.IsDead then
            local dist = GetDistanceToObject(obj)
            if dist < nearestDist then
                nearestEnemy = obj
                nearestDist = dist
            end
        end
    end

    if nearestEnemy then
        SetTarget(nearestEnemy)
        return true
    end

    return false
end

--- Check if current target is a FATE enemy
-- @param fate Fate - The FATE object
-- @return boolean - True if target is FATE enemy
function IsTargetFateEnemy(fate)
    if not fate or not HasTarget() then
        return false
    end

    local target = GetTarget()
    return target and target.FateId == fate.FateId
end

--- Get target object
-- @return GameObject|nil - Current target
function GetTarget()
    return Svc.Targets.Target
end

--- Set target
-- @param obj GameObject - Object to target
function SetTarget(obj)
    if obj then
        Svc.Targets.Target = obj
    end
end

--- Check if player has a target
-- @return boolean - True if has target
function HasTarget()
    return Svc.Targets.Target ~= nil
end

--- Get distance to current target
-- @return number - Distance in yalms
function GetTargetDistance()
    local target = GetTarget()
    if not target or not Player.Available then
        return 99999
    end

    return GetDistanceToObject(target)
end
```

## FATE Farming Patterns

### Simple FATE Farm Loop

```lua
--- Simple FATE farming loop
-- @param options table - Farming options
function FateFarmLoop(options)
    options = options or {}
    local minLevel = options.minLevel or (Player.Level - 5)
    local maxLevel = options.maxLevel or (Player.Level + 2)
    local maxDistance = options.maxDistance or 500
    local waitBetween = options.waitBetween or 5

    yield("/echo [Script] Starting FATE farming...")

    while not StopFlag do
        -- Find best FATE
        local fate = GetNearestFate({
            minLevel = minLevel,
            maxLevel = maxLevel,
            maxDistance = maxDistance,
            runningOnly = true
        })

        if fate then
            yield("/echo [Script] Found FATE: " .. fate.Name .. " (Lv." .. fate.Level .. ")")

            -- Navigate to FATE
            if NavigateToFate(fate, true, 120) then
                -- Participate
                local success, reason = ParticipateFate(fate, nil, 600)
                yield("/echo [Script] FATE result: " .. (reason or "Unknown"))
            end
        else
            yield("/echo [Script] No FATEs available, waiting...")
        end

        yield("/wait " .. waitBetween)
    end
end
```

### Priority-Based FATE Selection

```lua
--- FATE priority scoring
-- @param fate Fate - The FATE object
-- @param options table - Priority weights
-- @return number - Priority score (higher = better)
function CalculateFatePriority(fate, options)
    options = options or {}

    local distWeight = options.distanceWeight or 1.0
    local progWeight = options.progressWeight or 0.5
    local levelWeight = options.levelWeight or 0.3

    local score = 100  -- Base score

    -- Distance penalty (further = lower score)
    local dist = GetDistanceToFate(fate)
    score = score - (dist * distWeight * 0.1)

    -- Progress bonus (higher progress = higher score)
    score = score + (fate.Progress * progWeight)

    -- Level match bonus
    local levelDiff = math.abs(Player.Level - fate.Level)
    score = score - (levelDiff * levelWeight * 2)

    return score
end

--- Get best FATE by priority
-- @param options table - Filter and priority options
-- @return Fate|nil - Best FATE
function GetBestFate(options)
    local fates = FilterFates(options)
    local best = nil
    local bestScore = -99999

    for _, fate in ipairs(fates) do
        local score = CalculateFatePriority(fate, options)
        if score > bestScore then
            best = fate
            bestScore = score
        end
    end

    return best
end
```

### Blacklist Management

```lua
-- Blacklist for problematic FATEs
local FateBlacklist = {}
local BlacklistTimeout = 300  -- 5 minutes

--- Add FATE to blacklist
-- @param fateId number - FATE ID to blacklist
function BlacklistFate(fateId)
    FateBlacklist[fateId] = os.clock()
    yield("/echo [Script] Blacklisted FATE: " .. fateId)
end

--- Check if FATE is blacklisted
-- @param fateId number - FATE ID to check
-- @return boolean - True if blacklisted
function IsFateBlacklisted(fateId)
    local blacklistTime = FateBlacklist[fateId]
    if not blacklistTime then
        return false
    end

    -- Check if blacklist expired
    if (os.clock() - blacklistTime) > BlacklistTimeout then
        FateBlacklist[fateId] = nil
        return false
    end

    return true
end

--- Get non-blacklisted FATEs
-- @param options table - Filter options
-- @return table - Filtered FATEs
function GetNonBlacklistedFates(options)
    options = options or {}
    local fates = FilterFates(options)
    local filtered = {}

    for _, fate in ipairs(fates) do
        if not IsFateBlacklisted(fate.FateId) then
            table.insert(filtered, fate)
        end
    end

    return filtered
end

--- Clear FATE blacklist
function ClearFateBlacklist()
    FateBlacklist = {}
    yield("/echo [Script] FATE blacklist cleared")
end
```

## Special FATE Types

### Boss FATEs

```lua
--- Check if FATE is a boss FATE (has boss enemies)
-- @param fate Fate - The FATE object
-- @return boolean - True if boss FATE
function IsBossFate(fate)
    if not fate then
        return false
    end

    -- Check for "Slaying" or boss indicators in name
    local bossPatterns = {
        "^It's Not Easy Being",
        "^The ",  -- Many boss FATEs start with "The"
        "Boss",
    }

    for _, pattern in ipairs(bossPatterns) do
        if fate.Name:find(pattern) then
            return true
        end
    end

    return false
end
```

### Collection FATEs

```lua
--- Check if FATE is a collection FATE
-- @param fate Fate - The FATE object
-- @return boolean - True if collection FATE
function IsCollectionFate(fate)
    if not fate then
        return false
    end

    local collectPatterns = {
        "Collect",
        "Gather",
        "Retrieve",
    }

    for _, pattern in ipairs(collectPatterns) do
        if fate.Name:find(pattern) then
            return true
        end
    end

    return false
end

--- Handle collection FATE (interact with items)
-- @param fate Fate - The FATE object
function HandleCollectionFate(fate)
    -- Find collectible objects
    for _, obj in pairs(GetNearbyGameObjects(30)) do
        if obj.FateId == fate.FateId and
           obj.ObjectKind == ObjectKind.EventObj and
           obj.IsTargetable then
            -- Target and interact
            SetTarget(obj)
            yield("/wait 0.3")
            yield("/interact")
            yield("/wait 1")
        end
    end
end
```

### Defense FATEs

```lua
--- Check if FATE is a defense FATE
-- @param fate Fate - The FATE object
-- @return boolean - True if defense FATE
function IsDefenseFate(fate)
    if not fate then
        return false
    end

    local defensePatterns = {
        "Defend",
        "Protect",
        "Guard",
        "Hold",
    }

    for _, pattern in ipairs(defensePatterns) do
        if fate.Name:find(pattern) then
            return true
        end
    end

    return false
end
```

## State Machine Integration

```lua
CharacterState = {
    idle = Idle,
    searchingFate = SearchingFate,
    travelingToFate = TravelingToFate,
    participatingFate = ParticipatingFate,
    -- ... other states
}

local CurrentFate = nil

function Idle()
    yield("/echo [Script] FATE farm idle, searching...")
    State = CharacterState.searchingFate
end

function SearchingFate()
    CurrentFate = GetBestFate({
        minLevel = Player.Level - 5,
        maxLevel = Player.Level + 2,
        runningOnly = true
    })

    if CurrentFate then
        yield("/echo [Script] Found FATE: " .. CurrentFate.Name)
        State = CharacterState.travelingToFate
    else
        yield("/wait 5")
        -- Stay in searching state
    end
end

function TravelingToFate()
    if not CurrentFate then
        State = CharacterState.searchingFate
        return
    end

    if IsInsideFate(CurrentFate) then
        State = CharacterState.participatingFate
        return
    end

    -- Start navigation if not already moving
    if not IPC.vnavmesh.IsRunning() then
        IPC.vnavmesh.PathfindAndMoveTo(CurrentFate.Position, true)
    end
end

function ParticipatingFate()
    if not CurrentFate then
        State = CharacterState.searchingFate
        return
    end

    -- Check if FATE still active
    local activeFate = GetFateByFateId(CurrentFate.FateId)
    if not activeFate or not IsFateRunning(activeFate) then
        yield("/echo [Script] FATE ended")
        RemoveLevelSync()
        CurrentFate = nil
        State = CharacterState.searchingFate
        return
    end

    -- Apply sync if needed
    if NeedsLevelSync(activeFate) then
        ApplyLevelSync()
    end

    -- Combat logic
    DefaultFateCombat(activeFate)
end
```

## Configuration Variables

```lua
configs:
  EnableFateFarming:
    default: true
    description: Enable FATE farming automation
  MinFateLevel:
    default: 1
    description: Minimum FATE level to participate
  MaxFateLevel:
    default: 100
    description: Maximum FATE level to participate
  MaxFateDistance:
    default: 500
    description: Maximum distance to travel for FATEs
  AutoLevelSync:
    default: true
    description: Automatically apply level sync
  FateTimeout:
    default: 600
    description: Maximum time per FATE in seconds
  WaitBetweenFates:
    default: 5
    description: Wait time between FATEs in seconds
  PreferHighProgress:
    default: true
    description: Prefer FATEs with higher completion progress
```

## Helper Functions

```lua
--- Get nearby game objects
-- @param radius number - Search radius
-- @return table - Array of game objects
function GetNearbyGameObjects(radius)
    local objects = {}
    local objectTable = Svc.ObjectTable

    if not objectTable then
        return objects
    end

    for i = 0, objectTable.Length - 1 do
        local obj = objectTable[i]
        if obj then
            local dist = GetDistanceToObject(obj)
            if dist <= radius then
                table.insert(objects, obj)
            end
        end
    end

    return objects
end

--- Get distance to a game object
-- @param obj GameObject - The object
-- @return number - Distance in yalms
function GetDistanceToObject(obj)
    if not obj or not Player.Available then
        return 99999
    end

    local playerPos = Player.Position
    local objPos = obj.Position

    local dx = playerPos.X - objPos.X
    local dy = playerPos.Y - objPos.Y
    local dz = playerPos.Z - objPos.Z

    return math.sqrt(dx*dx + dy*dy + dz*dz)
end

--- Object kind constants
ObjectKind = {
    None = 0,
    Pc = 1,
    BattleNpc = 2,
    EventNpc = 3,
    Treasure = 4,
    Aetheryte = 5,
    GatheringPoint = 6,
    EventObj = 7,
    MountType = 8,
    Companion = 9,
    Retainer = 10,
    AreaObject = 11,
    Housing = 12,
    Cutscene = 13,
    CardStand = 14,
}
```

## Combat Plugin Integration

### Rotation Solver Reborn (RSR)
```lua
-- Turn on auto rotation
yield("/rotation off")
yield("/rotation auto on")

-- Manual mode
yield("/rotation manual")

-- Turn off
yield("/rotation off")

-- AoE settings: 0=Off, 1=Cleave, 2=Full
yield("/rotation settings aoetype 2")
```

### BossMod Reborn (BMR) / Veyn's BossMod (VBM)
```lua
-- Set active preset via IPC
IPC.BossMod.SetActive("PresetName")

-- Clear active preset
IPC.BossMod.ClearActive()

-- AI dodging (BMR)
yield("/bmrai on")
yield("/bmrai off")
yield("/bmrai followtarget on")
yield("/bmrai followcombat on")
yield("/bmrai maxdistancetarget 20")

-- VBM variant
yield("/vbm ai on")
yield("/vbm ai off")
```

### Wrath Combo
```lua
yield("/wrath auto on")
yield("/wrath auto off")
```

### Combat Mod Wrapper Functions
```lua
function TurnOnCombatMods()
    if CombatModsOn then return end
    CombatModsOn = true

    if RotationPlugin == "RSR" then
        yield("/rotation off")
        yield("/rotation auto on")
    elseif RotationPlugin == "BMR" or RotationPlugin == "VBM" then
        IPC.BossMod.SetActive(RotationPreset)
    elseif RotationPlugin == "Wrath" then
        yield("/wrath auto on")
    end
end

function TurnOffCombatMods()
    if not CombatModsOn then return end
    CombatModsOn = false

    if RotationPlugin == "RSR" then
        yield("/rotation off")
    elseif RotationPlugin == "BMR" or RotationPlugin == "VBM" then
        IPC.BossMod.ClearActive()
    elseif RotationPlugin == "Wrath" then
        yield("/wrath auto off")
    end
end
```

## Zone and Aetheryte Management

### Get Aetherytes in Zone
```lua
function GetAetherytesInZone(zoneId)
    local aetherytesInZone = {}
    for _, aetheryte in ipairs(Svc.AetheryteList) do
        if aetheryte.TerritoryId == zoneId then
            table.insert(aetherytesInZone, aetheryte)
        end
    end
    return aetherytesInZone
end

function GetAetheryteName(aetheryte)
    local name = aetheryte.AetheryteData.Value.PlaceName.Value.Name:GetText()
    return name or ""
end

-- Get aetheryte position
local aetherytePos = Instances.Telepo:GetAetherytePosition(aetheryte.AetheryteId)
```

### Get Aetheryte from Territory
```lua
function GetAetheryteNameFromZone(zoneId)
    local territoryData = Excel.GetRow("TerritoryType", zoneId)
    if territoryData and territoryData.Aetheryte and territoryData.Aetheryte.PlaceName then
        return tostring(territoryData.Aetheryte.PlaceName.Name)
    end
    return nil
end
```

### Instance Management
```lua
-- Get current instance
function GetZoneInstance()
    return InstancedContent.PublicInstance.InstanceId
end

-- Change instance
yield("/li 1")  -- Instance 1
yield("/li 2")  -- Instance 2

-- Cycle to next instance
local nextInstance = (GetZoneInstance() % 2) + 1
yield("/li " .. nextInstance)
```

## Chocobo Companion Management

```lua
function GetBuddyTimeRemaining()
    return Instances.Buddy.CompanionInfo.TimeLeft
end

function SummonChocobo(stance)
    -- Check if Gysahl Greens available (Item ID 4868)
    if Inventory.GetItemCount(4868) > 0 then
        yield("/item Gysahl Greens")
        yield("/wait 3")
        yield('/cac "' .. stance .. ' stance"')
    end
end

-- Stances: "Healer", "Attacker", "Defender", "Free", "Follow"
if GetBuddyTimeRemaining() <= 300 then  -- 5 minutes left
    SummonChocobo("Healer")
end
```

## Multi-Zone Farming Pattern

```lua
local ZonesToFarm = {
    { zoneName = "Zone 1", zoneId = 1001 },
    { zoneName = "Zone 2", zoneId = 1002 },
}

local currentZoneIndex = 1

while true do
    local currentZone = ZonesToFarm[currentZoneIndex]

    if Svc.ClientState.TerritoryType ~= currentZone.zoneId then
        local aetheryteName = GetAetheryteNameFromZone(currentZone.zoneId)
        if aetheryteName then
            TeleportTo(aetheryteName)
        end
    end

    -- Farm fates, then move to next zone
    currentZoneIndex = (currentZoneIndex % #ZonesToFarm) + 1
    yield("/wait 1")
end
```

## Chat Message Triggers

```lua
-- Register chat message handler
function OnChatMessage()
    local message = TriggerData.message
    local patternToMatch = "%[FATE%] Complete"

    if message and message:find(patternToMatch) then
        FateComplete = true
    end
end
```

## Best Practices

1. **Always check FATE state** - FATEs can end at any time
2. **Use level sync** when player level exceeds FATE max level
3. **Handle navigation failures** - Restart navigation if stuck
4. **Blacklist problematic FATEs** - Some FATEs may be bugged or stuck
5. **Monitor progress** - Leave FATEs that aren't progressing
6. **Check player state** - Don't start new FATEs while busy
7. **Use appropriate timeouts** - 600s for participation, 120s for navigation
8. **Handle special FATE types** differently (boss, collection, defense)
9. **Integrate with combat plugins** - Don't implement manual rotations
10. **Remove level sync** after FATE completion
11. **Use EntityWrapper** for accessing FATE-specific entity data
12. **Consider instance hopping** when no eligible FATEs available
13. **Use teleport penalties** when calculating closest aetheryte (200 distance typical)
