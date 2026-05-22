---
name: security-anticheat
description: Implements security and anti-exploit systems including sanity checks, exploit prevention, secure networking, and data protection. Use when you need to protect a game from exploiters and ensure fair gameplay.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Security & Anti-Exploit

When implementing security, follow the principle: **Never trust the client**. All important logic must be validated server-side.

## Core Principles

1. **Client can see everything** - Assume all client code is readable
2. **Client can send anything** - Validate all RemoteEvent data
3. **Client can modify anything local** - Don't rely on client-side checks
4. **Server is authority** - Server decides what actually happens

## Sanity Checks

### Type Validation
```lua
local function validateTypes(data, schema)
    for key, expectedType in pairs(schema) do
        local value = data[key]

        if expectedType == "number" then
            if type(value) ~= "number" or value ~= value then  -- NaN check
                return false, "Invalid number for " .. key
            end
        elseif expectedType == "string" then
            if type(value) ~= "string" then
                return false, "Invalid string for " .. key
            end
        elseif expectedType == "Vector3" then
            if typeof(value) ~= "Vector3" then
                return false, "Invalid Vector3 for " .. key
            end
        elseif expectedType == "integer" then
            if type(value) ~= "number" or value % 1 ~= 0 then
                return false, "Invalid integer for " .. key
            end
        elseif expectedType == "boolean" then
            if type(value) ~= "boolean" then
                return false, "Invalid boolean for " .. key
            end
        end
    end
    return true
end

-- Usage
AttackRemote.OnServerEvent:Connect(function(player, data)
    local valid, err = validateTypes(data, {
        targetId = "integer",
        damage = "number",
        position = "Vector3"
    })

    if not valid then
        warn("Invalid data from", player.Name, err)
        return
    end

    -- Continue with validated data
end)
```

### Range Validation
```lua
local function clampValue(value, min, max)
    return math.clamp(value, min, max)
end

local function validateRange(value, min, max)
    return type(value) == "number" and value >= min and value <= max
end

-- Example: Validate purchase quantity
PurchaseRemote.OnServerEvent:Connect(function(player, itemId, quantity)
    -- Validate quantity is reasonable
    if not validateRange(quantity, 1, 99) then
        warn("Invalid quantity from", player.Name)
        return
    end

    -- Validate itemId exists
    if not ItemDatabase[itemId] then
        warn("Invalid item from", player.Name)
        return
    end

    -- Process purchase...
end)
```

### Distance Validation
```lua
local function validateDistance(player, targetPosition, maxDistance)
    local character = player.Character
    if not character or not character.PrimaryPart then
        return false
    end

    local playerPos = character.PrimaryPart.Position
    local distance = (targetPosition - playerPos).Magnitude

    return distance <= maxDistance
end

-- Example: Validate interaction distance
InteractRemote.OnServerEvent:Connect(function(player, objectId)
    local object = workspace:FindFirstChild(objectId)
    if not object then return end

    -- Player must be within 10 studs to interact
    if not validateDistance(player, object.Position, 10) then
        warn("Too far to interact:", player.Name)
        return
    end

    -- Process interaction...
end)
```

## Common Exploit Prevention

### Speed Hack Detection
```lua
local PlayerMovement = {}
local MAX_SPEED = 50  -- Maximum allowed speed (studs/second)
local CHECK_INTERVAL = 0.5

local function monitorMovement(player)
    local lastCheck = {
        position = nil,
        time = os.clock()
    }

    local violations = 0
    local MAX_VIOLATIONS = 3

    task.spawn(function()
        while player.Parent do
            task.wait(CHECK_INTERVAL)

            local character = player.Character
            if not character or not character.PrimaryPart then continue end

            local currentPos = character.PrimaryPart.Position
            local currentTime = os.clock()

            if lastCheck.position then
                local distance = (currentPos - lastCheck.position).Magnitude
                local deltaTime = currentTime - lastCheck.time
                local speed = distance / deltaTime

                if speed > MAX_SPEED * 1.5 then  -- 50% tolerance
                    violations = violations + 1
                    warn("Speed violation:", player.Name, speed, "studs/s")

                    if violations >= MAX_VIOLATIONS then
                        -- Teleport back and/or kick
                        character:PivotTo(CFrame.new(lastCheck.position))
                        player:Kick("Movement anomaly detected")
                        return
                    end
                else
                    violations = math.max(0, violations - 1)  -- Decay violations
                end
            end

            lastCheck.position = currentPos
            lastCheck.time = currentTime
        end
    end)
end

Players.PlayerAdded:Connect(function(player)
    player.CharacterAdded:Connect(function()
        task.wait(1)  -- Wait for spawn
        monitorMovement(player)
    end)
end)
```

### Fly Hack Detection
```lua
local function checkGrounded(character)
    local hrp = character:FindFirstChild("HumanoidRootPart")
    local humanoid = character:FindFirstChildOfClass("Humanoid")

    if not hrp or not humanoid then return true end

    -- Check if on ground via Humanoid
    if humanoid.FloorMaterial ~= Enum.Material.Air then
        return true
    end

    -- Raycast down to check for ground
    local rayParams = RaycastParams.new()
    rayParams.FilterDescendantsInstances = {character}

    local result = workspace:Raycast(hrp.Position, Vector3.new(0, -10, 0), rayParams)

    return result ~= nil
end

local function monitorFlight(player)
    local airTime = 0
    local MAX_AIR_TIME = 5  -- Seconds allowed in air

    task.spawn(function()
        while player.Parent do
            task.wait(0.5)

            local character = player.Character
            if not character then continue end

            local humanoid = character:FindFirstChildOfClass("Humanoid")
            if not humanoid then continue end

            -- Allow jumping and falling
            local state = humanoid:GetState()
            if state == Enum.HumanoidStateType.Jumping or
               state == Enum.HumanoidStateType.Freefall then
                airTime = airTime + 0.5
            else
                airTime = 0
            end

            -- Check for extended flight
            if airTime > MAX_AIR_TIME and not checkGrounded(character) then
                warn("Flight detected:", player.Name)
                -- Teleport to ground or kick
            end
        end
    end)
end
```

### Noclip Detection
```lua
local function checkNoclip(character, previousPos, currentPos)
    local rayParams = RaycastParams.new()
    rayParams.FilterDescendantsInstances = {character}

    local direction = currentPos - previousPos
    local distance = direction.Magnitude

    if distance > 1 then  -- Only check significant movement
        local result = workspace:Raycast(previousPos, direction, rayParams)

        if result and result.Distance < distance - 0.5 then
            -- Player passed through something
            return true, result.Position
        end
    end

    return false
end
```

### Damage Validation
```lua
-- NEVER trust client-claimed damage
DamageRemote.OnServerEvent:Connect(function(player, targetId, claimedDamage)
    -- Client should NOT send damage amount
    -- Server calculates damage based on:
    -- 1. What attack was used
    -- 2. Attacker's stats
    -- 3. Target's defenses

    local attacker = player.Character
    local target = getCharacterById(targetId)

    if not attacker or not target then return end

    -- Validate attack is possible
    if not canAttack(attacker) then return end
    if not isInRange(attacker, target) then return end
    if not hasLineOfSight(attacker, target) then return end

    -- Server calculates damage
    local damage = calculateDamage(attacker, target)
    applyDamage(target, damage, attacker)
end)
```

### Currency/Item Duplication Prevention
```lua
-- Use atomic transactions
local function transferItem(fromPlayer, toPlayer, itemId)
    local fromInventory = getInventory(fromPlayer)
    local toInventory = getInventory(toPlayer)

    -- Atomic check and transfer
    local success, err = pcall(function()
        -- Check item exists
        if not fromInventory:HasItem(itemId) then
            error("Item not found")
        end

        -- Remove from sender FIRST
        local removed = fromInventory:RemoveItem(itemId)
        if not removed then
            error("Failed to remove item")
        end

        -- Then add to receiver
        local added = toInventory:AddItem(itemId)
        if not added then
            -- Rollback - return item to sender
            fromInventory:AddItem(itemId)
            error("Failed to add item to receiver")
        end
    end)

    return success, err
end
```

## Rate Limiting

### Per-Remote Rate Limits
```lua
local RateLimits = {
    Attack = {max = 10, window = 1},      -- 10 per second
    Purchase = {max = 5, window = 10},     -- 5 per 10 seconds
    Chat = {max = 5, window = 5},          -- 5 per 5 seconds
}

local PlayerCallCounts = {}

local function checkRateLimit(player, remoteName)
    local limit = RateLimits[remoteName]
    if not limit then return true end

    local key = player.UserId
    PlayerCallCounts[key] = PlayerCallCounts[key] or {}
    PlayerCallCounts[key][remoteName] = PlayerCallCounts[key][remoteName] or {
        count = 0,
        resetTime = os.clock() + limit.window
    }

    local data = PlayerCallCounts[key][remoteName]

    -- Reset if window expired
    if os.clock() > data.resetTime then
        data.count = 0
        data.resetTime = os.clock() + limit.window
    end

    data.count = data.count + 1

    if data.count > limit.max then
        return false  -- Rate limited
    end

    return true
end
```

## Secure Coding Practices

### Server-Side Cooldowns
```lua
-- BAD: Trusting client cooldown
ClientCooldownRemote.OnServerEvent:Connect(function(player, isOnCooldown)
    if isOnCooldown then return end  -- Client can just send false
    -- Do action
end)

-- GOOD: Server tracks cooldowns
local Cooldowns = {}

AbilityRemote.OnServerEvent:Connect(function(player, abilityId)
    local key = player.UserId .. "_" .. abilityId
    local cooldownEnd = Cooldowns[key] or 0

    if os.clock() < cooldownEnd then
        return  -- Still on cooldown
    end

    -- Do action
    Cooldowns[key] = os.clock() + getAbilityCooldown(abilityId)
end)
```

### Validate Ownership
```lua
UseItemRemote.OnServerEvent:Connect(function(player, itemId)
    local inventory = getInventory(player)

    -- Verify player owns this item
    if not inventory:HasItem(itemId) then
        warn("Item ownership failed:", player.Name, itemId)
        return
    end

    -- Verify item is usable in current state
    if player.Character:GetAttribute("Stunned") then
        return
    end

    -- Use item
    inventory:UseItem(itemId)
end)
```

### Action Sequence Validation
```lua
-- Ensure actions happen in valid order
local PlayerStates = {}

local function validateActionSequence(player, action)
    local state = PlayerStates[player.UserId] or "Idle"

    local validTransitions = {
        Idle = {"Attack", "Block", "Dash"},
        Attack = {"Idle", "ComboAttack"},
        Block = {"Idle", "Parry"},
        Dash = {"Idle", "Attack"},
        ComboAttack = {"Idle", "ComboAttack2"},
    }

    local allowed = validTransitions[state]
    if not allowed or not table.find(allowed, action) then
        warn("Invalid action sequence:", player.Name, state, "->", action)
        return false
    end

    return true
end
```

## Detection & Response

### Flagging System
```lua
local SuspicionPoints = {}
local KICK_THRESHOLD = 100
local BAN_THRESHOLD = 300

local function addSuspicion(player, points, reason)
    local userId = player.UserId
    SuspicionPoints[userId] = (SuspicionPoints[userId] or 0) + points

    -- Log for review
    logSuspiciousActivity(player, reason, points, SuspicionPoints[userId])

    if SuspicionPoints[userId] >= BAN_THRESHOLD then
        banPlayer(player, "Automated detection: " .. reason)
    elseif SuspicionPoints[userId] >= KICK_THRESHOLD then
        player:Kick("Suspicious activity detected")
    end
end

-- Decay suspicion over time
task.spawn(function()
    while true do
        task.wait(60)
        for userId, points in pairs(SuspicionPoints) do
            SuspicionPoints[userId] = math.max(0, points - 5)
        end
    end
end)
```

### Evidence Logging
```lua
local function logSuspiciousActivity(player, reason, points, totalPoints)
    local logData = {
        timestamp = os.time(),
        userId = player.UserId,
        username = player.Name,
        reason = reason,
        points = points,
        totalPoints = totalPoints,
        position = player.Character and player.Character.PrimaryPart and
                   player.Character.PrimaryPart.Position or nil,
        serverJobId = game.JobId
    }

    -- Send to external logging service or DataStore
    LoggingService:Log(logData)
end
```

## Data Protection

### DataStore Security
```lua
-- NEVER let client specify DataStore keys
-- BAD:
DataRemote.OnServerEvent:Connect(function(player, key, value)
    DataStore:SetAsync(key, value)  -- Client controls key!
end)

-- GOOD:
DataRemote.OnServerEvent:Connect(function(player, value)
    -- Key is always based on player's UserId
    local key = "Player_" .. player.UserId
    -- Validate value before saving
    if validatePlayerData(value) then
        DataStore:SetAsync(key, value)
    end
end)
```

### Input Sanitization
```lua
local function sanitizeString(str)
    if type(str) ~= "string" then return "" end

    -- Remove control characters
    str = str:gsub("[%c]", "")

    -- Limit length
    str = str:sub(1, 200)

    -- Filter profanity (use TextService for chat)
    return str
end

local function sanitizeNumber(num, min, max, default)
    if type(num) ~= "number" or num ~= num then
        return default
    end
    return math.clamp(num, min, max)
end
```
