---
name: SND Combat Plugin Integration
description: Use this skill when implementing combat automation in SND macros using rotation plugins like BossMod, RSR (RotationSolver Reborn), or Wrath. Covers plugin control, state management, and combat patterns.
---

# Combat Plugin Integration for SND

This skill covers integration with combat/rotation plugins for SND macros.

## Supported Plugins

| Plugin | Internal Name | Description |
|--------|---------------|-------------|
| BossMod | BossMod | Boss mechanics and auto-rotation |
| RotationSolver Reborn | RotationSolver | Advanced rotation automation |
| Wrath | WrathCombo | Combo-based rotation helper |

## Plugin Availability

### Check Plugin Availability

```lua
--- Check if a combat plugin is loaded
-- @param pluginName string - Plugin internal name
-- @return boolean - True if available
function HasCombatPlugin(pluginName)
    for plugin in luanet.each(Svc.PluginInterface.InstalledPlugins) do
        if plugin.InternalName == pluginName and plugin.IsLoaded then
            return true
        end
    end
    return false
end

--- Check if any combat plugin is available
-- @return boolean, string - True and plugin name if found
function HasAnyCombatPlugin()
    local plugins = {"BossMod", "RotationSolver", "WrathCombo"}
    for _, name in ipairs(plugins) do
        if HasCombatPlugin(name) then
            return true, name
        end
    end
    return false, nil
end

--- Get available combat plugin
-- @return string|nil - Plugin name or nil
function GetCombatPlugin()
    local has, name = HasAnyCombatPlugin()
    return has and name or nil
end
```

## BossMod Integration

### BossMod AI Control

```lua
--- Enable BossMod AI
-- @return boolean - True if enabled
function EnableBossModAI()
    if not HasCombatPlugin("BossMod") then
        yield("/echo [Script] BossMod not available")
        return false
    end

    yield("/bmai on")
    yield("/wait 0.3")
    return true
end

--- Disable BossMod AI
-- @return boolean - True if disabled
function DisableBossModAI()
    if not HasCombatPlugin("BossMod") then
        return false
    end

    yield("/bmai off")
    yield("/wait 0.3")
    return true
end

--- Toggle BossMod AI
function ToggleBossModAI()
    if not HasCombatPlugin("BossMod") then
        return false
    end

    yield("/bmai")
    yield("/wait 0.3")
    return true
end

--- Set BossMod follow target
-- @param targetName string - Target to follow (or "off")
function SetBossModFollow(targetName)
    if not HasCombatPlugin("BossMod") then
        return false
    end

    if targetName == "off" or targetName == nil then
        yield("/bmfollow off")
    else
        yield("/bmfollow " .. targetName)
    end

    yield("/wait 0.3")
    return true
end
```

### BossMod Positional Commands

```lua
--- Move BossMod AI to position
-- @param direction string - "front", "back", "left", "right", "flank"
function BossModMoveToPositional(direction)
    if not HasCombatPlugin("BossMod") then
        return false
    end

    yield("/bmpos " .. direction)
    return true
end
```

## RotationSolver Reborn (RSR) Integration

### RSR State Control

```lua
--- Check if RSR is available via IPC
-- @return boolean - True if available
function IsRSRAvailable()
    return IPC.RSR ~= nil
end

--- Enable RSR auto rotation
-- @return boolean - True if enabled
function EnableRSR()
    if not HasCombatPlugin("RotationSolver") then
        yield("/echo [Script] RSR not available")
        return false
    end

    yield("/rotation auto")
    yield("/wait 0.3")
    return true
end

--- Disable RSR auto rotation
-- @return boolean - True if disabled
function DisableRSR()
    if not HasCombatPlugin("RotationSolver") then
        return false
    end

    yield("/rotation cancel")
    yield("/wait 0.3")
    return true
end

--- Set RSR to manual mode
function SetRSRManual()
    if not HasCombatPlugin("RotationSolver") then
        return false
    end

    yield("/rotation manual")
    yield("/wait 0.3")
    return true
end

--- Get RSR state (if IPC available)
-- @return string|nil - Current state
function GetRSRState()
    if IPC.RSR and IPC.RSR.GetState then
        return IPC.RSR.GetState()
    end
    return nil
end
```

### RSR Configuration Commands

```lua
--- Set RSR targeting mode
-- @param mode string - "hostile", "friendly", "all"
function SetRSRTargetMode(mode)
    if not HasCombatPlugin("RotationSolver") then
        return false
    end

    yield("/rotation targetmode " .. mode)
    yield("/wait 0.2")
    return true
end

--- Enable/disable RSR AoE
-- @param enabled boolean - True to enable
function SetRSRAoE(enabled)
    if not HasCombatPlugin("RotationSolver") then
        return false
    end

    local cmd = enabled and "/rotation aoe on" or "/rotation aoe off"
    yield(cmd)
    yield("/wait 0.2")
    return true
end
```

## Wrath Integration

### Wrath Control

```lua
--- Check if Wrath is available
-- @return boolean - True if available
function IsWrathAvailable()
    return HasCombatPlugin("WrathCombo")
end

--- Enable Wrath auto rotation
-- @return boolean - True if enabled
function EnableWrath()
    if not HasCombatPlugin("WrathCombo") then
        yield("/echo [Script] Wrath not available")
        return false
    end

    yield("/wrath on")
    yield("/wait 0.3")
    return true
end

--- Disable Wrath auto rotation
-- @return boolean - True if disabled
function DisableWrath()
    if not HasCombatPlugin("WrathCombo") then
        return false
    end

    yield("/wrath off")
    yield("/wait 0.3")
    return true
end

--- Toggle Wrath
function ToggleWrath()
    if not HasCombatPlugin("WrathCombo") then
        return false
    end

    yield("/wrath")
    yield("/wait 0.3")
    return true
end
```

## Universal Combat Control

### Unified Combat Plugin Interface

```lua
--- Combat plugin interface
CombatPlugin = {
    plugin = nil,  -- Active plugin name
}

--- Initialize combat plugin interface
-- @return boolean - True if a plugin is available
function CombatPlugin.Init()
    local has, name = HasAnyCombatPlugin()
    CombatPlugin.plugin = name
    return has
end

--- Enable auto combat
-- @return boolean - True if enabled
function CombatPlugin.Enable()
    if not CombatPlugin.plugin then
        CombatPlugin.Init()
    end

    if CombatPlugin.plugin == "BossMod" then
        return EnableBossModAI()
    elseif CombatPlugin.plugin == "RotationSolver" then
        return EnableRSR()
    elseif CombatPlugin.plugin == "WrathCombo" then
        return EnableWrath()
    end

    yield("/echo [Script] No combat plugin available")
    return false
end

--- Disable auto combat
-- @return boolean - True if disabled
function CombatPlugin.Disable()
    if not CombatPlugin.plugin then
        return false
    end

    if CombatPlugin.plugin == "BossMod" then
        return DisableBossModAI()
    elseif CombatPlugin.plugin == "RotationSolver" then
        return DisableRSR()
    elseif CombatPlugin.plugin == "WrathCombo" then
        return DisableWrath()
    end

    return false
end

--- Get current combat plugin name
-- @return string|nil - Plugin name
function CombatPlugin.GetName()
    return CombatPlugin.plugin
end
```

## Combat State Checking

### Player Combat State

```lua
--- Character conditions for combat
local CharacterCondition = {
    inCombat = 26,
    casting = 27,
    inCombat2 = 34,  -- Alternative combat flag
    unconscious = 35,
    boundByDuty = 37,
}

--- Check if player is in combat
-- @return boolean - True if in combat
function IsInCombat()
    return Svc.Condition[CharacterCondition.inCombat] or
           Svc.Condition[CharacterCondition.inCombat2]
end

--- Check if player is casting
-- @return boolean - True if casting
function IsCasting()
    return Svc.Condition[CharacterCondition.casting]
end

--- Check if player is dead
-- @return boolean - True if dead
function IsDead()
    return Svc.Condition[CharacterCondition.unconscious]
end

--- Check if in duty
-- @return boolean - True if in duty
function IsInDuty()
    return Svc.Condition[CharacterCondition.boundByDuty]
end

--- Wait until out of combat
-- @param timeout number - Maximum wait time (default: 30)
-- @return boolean - True if out of combat
function WaitUntilOutOfCombat(timeout)
    timeout = timeout or 30
    local startTime = os.clock()

    while IsInCombat() and (os.clock() - startTime) < timeout do
        yield("/wait 0.5")
    end

    return not IsInCombat()
end

--- Wait until in combat
-- @param timeout number - Maximum wait time (default: 10)
-- @return boolean - True if in combat
function WaitUntilInCombat(timeout)
    timeout = timeout or 10
    local startTime = os.clock()

    while not IsInCombat() and (os.clock() - startTime) < timeout do
        yield("/wait 0.5")
    end

    return IsInCombat()
end
```

### Target Management

```lua
--- Check if player has a target
-- @return boolean - True if has target
function HasTarget()
    return Svc.Targets.Target ~= nil
end

--- Get current target
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

--- Clear current target
function ClearTarget()
    Svc.Targets.Target = nil
end

--- Check if target is attackable
-- @return boolean - True if attackable
function IsTargetAttackable()
    local target = GetTarget()
    if not target then
        return false
    end

    return target.IsTargetable and
           not target.IsDead and
           target.ObjectKind == ObjectKind.BattleNpc
end

--- Get distance to target
-- @return number - Distance in yalms
function GetTargetDistance()
    local target = GetTarget()
    if not target or not Player.Available then
        return 99999
    end

    local playerPos = Player.Position
    local targetPos = target.Position

    local dx = playerPos.X - targetPos.X
    local dy = playerPos.Y - targetPos.Y
    local dz = playerPos.Z - targetPos.Z

    return math.sqrt(dx*dx + dy*dy + dz*dz)
end

--- Check if target is in range
-- @param maxRange number - Maximum range (default: 25)
-- @return boolean - True if in range
function IsTargetInRange(maxRange)
    maxRange = maxRange or 25
    return GetTargetDistance() <= maxRange
end
```

### Enemy Detection

```lua
--- Find nearest enemy
-- @param maxRange number - Search range (default: 30)
-- @return GameObject|nil - Nearest enemy
function FindNearestEnemy(maxRange)
    maxRange = maxRange or 30
    local nearest = nil
    local nearestDist = maxRange

    local objectTable = Svc.ObjectTable
    if not objectTable then
        return nil
    end

    for i = 0, objectTable.Length - 1 do
        local obj = objectTable[i]
        if obj and
           obj.ObjectKind == ObjectKind.BattleNpc and
           obj.IsTargetable and
           not obj.IsDead and
           IsHostile(obj) then
            local dist = GetDistanceToObject(obj)
            if dist < nearestDist then
                nearest = obj
                nearestDist = dist
            end
        end
    end

    return nearest
end

--- Check if object is hostile
-- @param obj GameObject - The object
-- @return boolean - True if hostile
function IsHostile(obj)
    if not obj then
        return false
    end
    -- Check if enemy (red icon)
    -- This may vary based on game state
    return obj.StatusFlags and (obj.StatusFlags & 1) ~= 0
end

--- Target nearest enemy
-- @param maxRange number - Search range (default: 30)
-- @return boolean - True if target acquired
function TargetNearestEnemy(maxRange)
    local enemy = FindNearestEnemy(maxRange)
    if enemy then
        SetTarget(enemy)
        return true
    end
    return false
end

--- Count enemies in range
-- @param range number - Range to check (default: 30)
-- @return number - Enemy count
function CountEnemiesInRange(range)
    range = range or 30
    local count = 0

    local objectTable = Svc.ObjectTable
    if not objectTable then
        return 0
    end

    for i = 0, objectTable.Length - 1 do
        local obj = objectTable[i]
        if obj and
           obj.ObjectKind == ObjectKind.BattleNpc and
           obj.IsTargetable and
           not obj.IsDead and
           IsHostile(obj) then
            local dist = GetDistanceToObject(obj)
            if dist <= range then
                count = count + 1
            end
        end
    end

    return count
end
```

## Combat Patterns

### Basic Combat Loop

```lua
--- Basic combat loop with rotation plugin
-- @param targetFunc function - Function to acquire targets
-- @param timeout number - Combat timeout (default: 300)
-- @return boolean - True if combat completed successfully
function BasicCombatLoop(targetFunc, timeout)
    timeout = timeout or 300
    local startTime = os.clock()

    -- Initialize combat plugin
    if not CombatPlugin.Init() then
        yield("/echo [Script] No combat plugin available")
        return false
    end

    -- Enable rotation
    CombatPlugin.Enable()

    while (os.clock() - startTime) < timeout do
        -- Check stop conditions
        if StopFlag then
            CombatPlugin.Disable()
            return false
        end

        -- Acquire target if needed
        if not HasTarget() or not IsTargetAttackable() then
            if targetFunc then
                targetFunc()
            else
                TargetNearestEnemy(30)
            end
        end

        -- Check if combat should continue
        if not HasTarget() and not IsInCombat() then
            -- No targets and not in combat, exit
            break
        end

        -- Move to target if needed
        if HasTarget() and not IsTargetInRange(25) then
            local target = GetTarget()
            if target and IPC.vnavmesh then
                IPC.vnavmesh.PathfindAndMoveTo(target.Position, false)
            end
        elseif IPC.vnavmesh and IPC.vnavmesh.IsRunning() then
            -- Stop moving when in range
            IPC.vnavmesh.Stop()
        end

        yield("/wait 0.5")
    end

    -- Cleanup
    CombatPlugin.Disable()
    WaitUntilOutOfCombat(30)

    return true
end
```

### Pull and Fight Pattern

```lua
--- Pull an enemy and fight until dead
-- @param target GameObject - Enemy to pull
-- @param maxRange number - Attack range (default: 25)
-- @return boolean - True if enemy killed
function PullAndFight(target, maxRange)
    maxRange = maxRange or 25

    if not target then
        return false
    end

    -- Target the enemy
    SetTarget(target)
    yield("/wait 0.2")

    -- Move into range
    while GetTargetDistance() > maxRange do
        if IPC.vnavmesh then
            IPC.vnavmesh.PathfindAndMoveTo(target.Position, false)
        end
        yield("/wait 0.3")
    end

    if IPC.vnavmesh then
        IPC.vnavmesh.Stop()
    end

    -- Enable combat
    CombatPlugin.Enable()

    -- Wait for enemy to die
    local timeout = 120
    local startTime = os.clock()

    while (os.clock() - startTime) < timeout do
        local currentTarget = GetTarget()

        -- Check if target is dead
        if not currentTarget or currentTarget.IsDead then
            CombatPlugin.Disable()
            return true
        end

        -- Stay in range
        if GetTargetDistance() > maxRange + 5 then
            if IPC.vnavmesh then
                IPC.vnavmesh.PathfindAndMoveTo(currentTarget.Position, false)
            end
        end

        yield("/wait 0.5")
    end

    CombatPlugin.Disable()
    return false
end
```

### AoE Combat Pattern

```lua
--- AoE combat pattern for multiple enemies
-- @param centerPos Vector3 - Center position for AoE
-- @param pullRadius number - Radius to pull enemies (default: 15)
-- @param timeout number - Combat timeout (default: 180)
-- @return boolean - True if all enemies killed
function AoECombat(centerPos, pullRadius, timeout)
    pullRadius = pullRadius or 15
    timeout = timeout or 180
    local startTime = os.clock()

    -- Enable combat plugin
    CombatPlugin.Enable()

    -- Move to center
    if IPC.vnavmesh then
        IPC.vnavmesh.PathfindAndMoveTo(centerPos, false)
        while IPC.vnavmesh.IsRunning() do
            yield("/wait 0.3")
        end
    end

    -- Combat loop
    while (os.clock() - startTime) < timeout do
        local enemyCount = CountEnemiesInRange(pullRadius + 10)

        if enemyCount == 0 and not IsInCombat() then
            -- All enemies dead
            break
        end

        -- Target nearest if needed
        if not HasTarget() or not IsTargetAttackable() then
            TargetNearestEnemy(pullRadius + 10)
        end

        -- Stay in center area
        local playerPos = Player.Position
        local dx = playerPos.X - centerPos.X
        local dz = playerPos.Z - centerPos.Z
        local distFromCenter = math.sqrt(dx*dx + dz*dz)

        if distFromCenter > pullRadius then
            if IPC.vnavmesh then
                IPC.vnavmesh.PathfindAndMoveTo(centerPos, false)
            end
        end

        yield("/wait 0.5")
    end

    CombatPlugin.Disable()
    WaitUntilOutOfCombat(30)

    return CountEnemiesInRange(pullRadius + 10) == 0
end
```

## Dungeon/Duty Support

### Duty Combat Management

```lua
--- Combat management for duties/dungeons
DutyCombat = {
    enabled = false,
    plugin = nil,
}

--- Initialize duty combat
function DutyCombat.Init()
    DutyCombat.enabled = CombatPlugin.Init()
    DutyCombat.plugin = CombatPlugin.plugin
    return DutyCombat.enabled
end

--- Start duty combat mode
function DutyCombat.Start()
    if not DutyCombat.enabled then
        DutyCombat.Init()
    end

    CombatPlugin.Enable()
    yield("/echo [Script] Combat enabled for duty")
end

--- Stop duty combat mode
function DutyCombat.Stop()
    CombatPlugin.Disable()
    yield("/echo [Script] Combat disabled")
end

--- Handle trash pack
-- @param packCenter Vector3 - Center of trash pack
-- @param timeout number - Pack timeout (default: 120)
function DutyCombat.HandleTrashPack(packCenter, timeout)
    timeout = timeout or 120

    AoECombat(packCenter, 15, timeout)
end

--- Handle boss fight
-- @param bossTarget GameObject - Boss to fight
-- @param timeout number - Boss timeout (default: 600)
function DutyCombat.HandleBoss(bossTarget, timeout)
    timeout = timeout or 600

    if not bossTarget then
        return false
    end

    -- Target boss
    SetTarget(bossTarget)
    CombatPlugin.Enable()

    local startTime = os.clock()

    while (os.clock() - startTime) < timeout do
        local boss = GetTarget()

        -- Check if boss is dead
        if not boss or boss.IsDead then
            yield("/echo [Script] Boss defeated!")
            CombatPlugin.Disable()
            return true
        end

        -- Handle death
        if IsDead() then
            yield("/echo [Script] Player died during boss!")
            -- Wait for raise or release
            yield("/wait 10")
        end

        yield("/wait 0.5")
    end

    CombatPlugin.Disable()
    return false
end
```

## State Machine Integration

```lua
CharacterState = {
    idle = Idle,
    combat = Combat,
    postCombat = PostCombat,
    -- ... other states
}

function Combat()
    -- Enable rotation plugin
    CombatPlugin.Enable()

    -- Combat logic
    if not HasTarget() then
        TargetNearestEnemy(30)
    end

    -- Check exit conditions
    if not IsInCombat() and not HasTarget() then
        State = CharacterState.postCombat
        return
    end

    -- Stay in combat state
end

function PostCombat()
    -- Disable rotation plugin
    CombatPlugin.Disable()

    -- Wait for combat to fully end
    WaitUntilOutOfCombat(10)

    -- Transition to next state
    State = CharacterState.idle
end
```

## Configuration Variables

```lua
configs:
  CombatPlugin:
    default: "auto"
    description: Combat plugin to use (auto, BossMod, RSR, Wrath)
    is_choice: true
    choices: ["auto", "BossMod", "RSR", "Wrath"]
  EnableAutoCombat:
    default: true
    description: Enable automatic combat during automation
  CombatRange:
    default: 25
    description: Maximum combat engagement range
  CombatTimeout:
    default: 300
    description: Combat timeout in seconds
  EnableAoE:
    default: true
    description: Enable AoE skills during combat
  PullRadius:
    default: 15
    description: Radius for pulling enemies
```

## Helper Functions

```lua
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

## Best Practices

1. **Initialize combat plugin early** - Call `CombatPlugin.Init()` at script start
2. **Always disable after combat** - Prevent unintended actions
3. **Use unified interface** - `CombatPlugin.Enable()/Disable()` works with any plugin
4. **Check plugin availability** - Don't assume any specific plugin
5. **Handle combat timeout** - Don't get stuck in combat loops
6. **Wait for out-of-combat** before transitions
7. **Use appropriate ranges** - 25y for ranged, 3y for melee
8. **Handle player death** - Check `IsDead()` in combat loops
9. **Let plugins handle rotations** - Don't implement manual skill usage
10. **Integrate with navigation** - Move to targets when out of range
