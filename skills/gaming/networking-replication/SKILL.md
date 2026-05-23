---
name: networking-replication
description: Implements networking and replication systems including RemoteEvent optimization, custom replication, lag compensation, client prediction, and bandwidth optimization. Use when building multiplayer games that need smooth networked gameplay.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Networking & Replication

## Quick Reference Links

**Official Documentation:**
- [Remote Events & Functions](https://create.roblox.com/docs/scripting/events/remote-events) - Client-server communication
- [Bindable Events](https://create.roblox.com/docs/scripting/events/bindable-events) - Same-context events
- [Network Ownership](https://create.roblox.com/docs/physics/network-ownership) - Physics authority
- [Client-Server Model](https://create.roblox.com/docs/projects/client-server) - Architecture overview
- [RemoteEvent API](https://create.roblox.com/docs/reference/engine/classes/RemoteEvent)
- [RemoteFunction API](https://create.roblox.com/docs/reference/engine/classes/RemoteFunction)
- [UnreliableRemoteEvent API](https://create.roblox.com/docs/reference/engine/classes/UnreliableRemoteEvent)

**Wiki References:**
- [RemoteEvent (Wiki)](https://roblox.fandom.com/wiki/RemoteEvent)
- [RemoteFunction (Wiki)](https://roblox.fandom.com/wiki/RemoteFunction)
- [Filtering Enabled (Wiki)](https://roblox.fandom.com/wiki/FilteringEnabled)

---

When implementing networking systems, follow these Roblox-specific patterns for optimal multiplayer experience.

## RemoteEvent Optimization

### Batch Multiple Events
```lua
-- BAD: Firing many events per frame
for _, enemy in ipairs(enemies) do
    UpdateEnemyRemote:FireClient(player, enemy.id, enemy.position, enemy.health)
end

-- GOOD: Batch into single event
local updates = {}
for _, enemy in ipairs(enemies) do
    table.insert(updates, {
        id = enemy.id,
        pos = enemy.position,
        hp = enemy.health
    })
end
UpdateEnemiesRemote:FireClient(player, updates)
```

### Delta Compression
```lua
-- Only send changed values
local lastSentState = {}

local function sendStateUpdate(player, entityId, newState)
    local lastState = lastSentState[player.UserId] and lastSentState[player.UserId][entityId] or {}
    local delta = {}

    for key, value in pairs(newState) do
        if lastState[key] ~= value then
            delta[key] = value
        end
    end

    if next(delta) then  -- Only send if changes exist
        StateUpdateRemote:FireClient(player, entityId, delta)
        lastSentState[player.UserId] = lastSentState[player.UserId] or {}
        lastSentState[player.UserId][entityId] = newState
    end
end
```

### Rate Limiting
```lua
local RateLimiter = {}
RateLimiter.calls = {}

function RateLimiter.check(player, remoteName, maxCallsPerSecond)
    local key = player.UserId .. "_" .. remoteName
    local now = os.clock()

    RateLimiter.calls[key] = RateLimiter.calls[key] or {}
    local calls = RateLimiter.calls[key]

    -- Remove old calls (older than 1 second)
    for i = #calls, 1, -1 do
        if now - calls[i] > 1 then
            table.remove(calls, i)
        end
    end

    -- Check limit
    if #calls >= maxCallsPerSecond then
        return false  -- Rate limited
    end

    table.insert(calls, now)
    return true
end

-- Usage in RemoteEvent handler
MyRemote.OnServerEvent:Connect(function(player, data)
    if not RateLimiter.check(player, "MyRemote", 10) then
        warn("Rate limited:", player.Name)
        return
    end
    -- Process request
end)
```

### Unreliable RemoteEvents
```lua
-- Use UnreliableRemoteEvent for frequent non-critical updates
local PositionUpdate = Instance.new("UnreliableRemoteEvent")
PositionUpdate.Name = "PositionUpdate"
PositionUpdate.Parent = ReplicatedStorage

-- Good for: position updates, mouse position, non-critical effects
-- Bad for: damage, purchases, important state changes
```

## Custom Replication System

### NPC Replication with Interpolation
```lua
-- Server: Send position snapshots
local NPC_UPDATE_RATE = 1/20  -- 20 updates per second

local function broadcastNPCPositions()
    local updates = {}

    for _, npc in ipairs(activeNPCs) do
        table.insert(updates, {
            id = npc.id,
            pos = npc.PrimaryPart.Position,
            rot = npc.PrimaryPart.Orientation.Y,
            vel = npc.PrimaryPart.AssemblyLinearVelocity,
            state = npc:GetAttribute("State"),
            timestamp = workspace:GetServerTimeNow()
        })
    end

    NPCUpdateRemote:FireAllClients(updates)
end

task.spawn(function()
    while true do
        broadcastNPCPositions()
        task.wait(NPC_UPDATE_RATE)
    end
end)
```

```lua
-- Client: Interpolate between snapshots
local InterpolationBuffer = {}
InterpolationBuffer.buffers = {}
InterpolationBuffer.BUFFER_TIME = 0.1  -- 100ms interpolation delay

function InterpolationBuffer.addSnapshot(entityId, snapshot)
    InterpolationBuffer.buffers[entityId] = InterpolationBuffer.buffers[entityId] or {}
    local buffer = InterpolationBuffer.buffers[entityId]

    table.insert(buffer, snapshot)

    -- Keep only recent snapshots
    while #buffer > 10 do
        table.remove(buffer, 1)
    end
end

function InterpolationBuffer.getInterpolatedState(entityId)
    local buffer = InterpolationBuffer.buffers[entityId]
    if not buffer or #buffer < 2 then return nil end

    local renderTime = workspace:GetServerTimeNow() - InterpolationBuffer.BUFFER_TIME

    -- Find surrounding snapshots
    local prev, next
    for i = #buffer, 1, -1 do
        if buffer[i].timestamp <= renderTime then
            prev = buffer[i]
            next = buffer[i + 1]
            break
        end
    end

    if not prev then
        return buffer[1]  -- Extrapolate if too far behind
    end

    if not next then
        -- Extrapolate forward
        local dt = renderTime - prev.timestamp
        return {
            pos = prev.pos + prev.vel * dt,
            rot = prev.rot,
            state = prev.state
        }
    end

    -- Interpolate between snapshots
    local t = (renderTime - prev.timestamp) / (next.timestamp - prev.timestamp)
    return {
        pos = prev.pos:Lerp(next.pos, t),
        rot = prev.rot + (next.rot - prev.rot) * t,
        state = next.state  -- Use newer state
    }
end
```

### Late Joiner Synchronization
```lua
-- Server: Send full state to joining players
Players.PlayerAdded:Connect(function(player)
    -- Wait for character to load
    player.CharacterAdded:Wait()

    -- Send current game state
    local fullState = {
        enemies = {},
        players = {},
        worldState = {}
    }

    for _, enemy in ipairs(activeEnemies) do
        table.insert(fullState.enemies, {
            id = enemy.id,
            type = enemy.Type,
            pos = enemy.PrimaryPart.Position,
            health = enemy.Health,
            maxHealth = enemy.MaxHealth
        })
    end

    for _, otherPlayer in ipairs(Players:GetPlayers()) do
        if otherPlayer ~= player then
            table.insert(fullState.players, {
                userId = otherPlayer.UserId,
                position = otherPlayer.Character and otherPlayer.Character.PrimaryPart.Position,
                stats = getPlayerStats(otherPlayer)
            })
        end
    end

    fullState.worldState = {
        timeOfDay = Lighting.ClockTime,
        weather = currentWeather,
        eventFlags = activeEvents
    }

    FullStateSyncRemote:FireClient(player, fullState)
end)
```

## Server Authority

### Authoritative Movement Validation
```lua
-- Server: Validate client-claimed positions
local MAX_SPEED = 50  -- studs per second
local TOLERANCE = 1.5  -- Multiplier for latency tolerance

local lastValidPositions = {}

local function validateMovement(player, claimedPosition)
    local character = player.Character
    if not character then return false end

    local lastPos = lastValidPositions[player.UserId]
    if not lastPos then
        lastValidPositions[player.UserId] = {
            position = claimedPosition,
            time = os.clock()
        }
        return true
    end

    local deltaTime = os.clock() - lastPos.time
    local distance = (claimedPosition - lastPos.position).Magnitude
    local maxDistance = MAX_SPEED * deltaTime * TOLERANCE

    if distance > maxDistance then
        -- Potential speed hack - reject and correct
        warn("Movement validation failed for", player.Name)
        character:PivotTo(CFrame.new(lastPos.position))
        return false
    end

    lastValidPositions[player.UserId] = {
        position = claimedPosition,
        time = os.clock()
    }
    return true
end
```

### Server-Side Hit Registration
```lua
-- Server: Validate all combat hits
HitClaimRemote.OnServerEvent:Connect(function(player, hitData)
    local attacker = player.Character
    local target = getCharacterById(hitData.targetId)

    if not attacker or not target then return end

    -- Validate distance
    local distance = (attacker.PrimaryPart.Position - target.PrimaryPart.Position).Magnitude
    local maxRange = getAttackRange(hitData.attackType) * 1.2  -- 20% tolerance

    if distance > maxRange then
        warn("Hit rejected: out of range")
        return
    end

    -- Validate timing (attack cooldown)
    local lastAttack = attacker:GetAttribute("LastAttackTime") or 0
    local cooldown = getAttackCooldown(hitData.attackType)

    if os.clock() - lastAttack < cooldown * 0.9 then
        warn("Hit rejected: attack on cooldown")
        return
    end

    -- Validate line of sight
    local rayParams = RaycastParams.new()
    rayParams.FilterDescendantsInstances = {attacker}
    local ray = workspace:Raycast(
        attacker.PrimaryPart.Position,
        (target.PrimaryPart.Position - attacker.PrimaryPart.Position),
        rayParams
    )

    if ray and ray.Instance:IsDescendantOf(target) then
        -- Valid hit - apply damage
        local damage = calculateDamage(hitData.attackType, attacker, target)
        applyDamage(target, damage, attacker)

        attacker:SetAttribute("LastAttackTime", os.clock())
    end
end)
```

## Client Prediction

### Input Prediction with Reconciliation
```lua
-- Client: Apply inputs immediately, reconcile with server
local InputHistory = {}
local MAX_HISTORY = 60  -- 1 second at 60fps

local function processInput(input)
    local inputId = #InputHistory + 1
    local predictedState = applyInput(localCharacter, input)

    -- Store for reconciliation
    table.insert(InputHistory, {
        id = inputId,
        input = input,
        predictedState = predictedState,
        timestamp = os.clock()
    })

    -- Trim old history
    while #InputHistory > MAX_HISTORY do
        table.remove(InputHistory, 1)
    end

    -- Send to server
    InputRemote:FireServer(inputId, input)
end

-- Client: Reconcile with server state
ServerStateRemote.OnClientEvent:Connect(function(serverState)
    -- Find the input this state corresponds to
    local reconciledIndex
    for i, entry in ipairs(InputHistory) do
        if entry.id == serverState.lastProcessedInput then
            reconciledIndex = i
            break
        end
    end

    if not reconciledIndex then return end

    -- Check if prediction was wrong
    local predicted = InputHistory[reconciledIndex].predictedState
    local error = (serverState.position - predicted.position).Magnitude

    if error > 0.1 then  -- Significant error
        -- Snap to server position
        localCharacter:PivotTo(CFrame.new(serverState.position))

        -- Re-apply unacknowledged inputs
        for i = reconciledIndex + 1, #InputHistory do
            applyInput(localCharacter, InputHistory[i].input)
        end
    end

    -- Remove acknowledged inputs
    for i = reconciledIndex, 1, -1 do
        table.remove(InputHistory, i)
    end
end)
```

## Lag Compensation

### Server-Side Lag Compensation
```lua
-- Store position history for all players
local PositionHistory = {}
local HISTORY_DURATION = 1  -- 1 second of history

local function recordPosition(character)
    local userId = Players:GetPlayerFromCharacter(character).UserId
    PositionHistory[userId] = PositionHistory[userId] or {}

    table.insert(PositionHistory[userId], {
        position = character.PrimaryPart.Position,
        timestamp = workspace:GetServerTimeNow()
    })

    -- Trim old entries
    local cutoff = workspace:GetServerTimeNow() - HISTORY_DURATION
    while #PositionHistory[userId] > 0 and PositionHistory[userId][1].timestamp < cutoff do
        table.remove(PositionHistory[userId], 1)
    end
end

local function getPositionAtTime(userId, timestamp)
    local history = PositionHistory[userId]
    if not history or #history == 0 then return nil end

    -- Find surrounding entries
    for i = #history, 1, -1 do
        if history[i].timestamp <= timestamp then
            local prev = history[i]
            local next = history[i + 1]

            if not next then
                return prev.position
            end

            -- Interpolate
            local t = (timestamp - prev.timestamp) / (next.timestamp - prev.timestamp)
            return prev.position:Lerp(next.position, t)
        end
    end

    return history[1].position
end

-- Use in hit detection
local function lagCompensatedHitCheck(shooter, targetUserId, shooterTimestamp)
    -- Rewind target to shooter's view time
    local ping = shooter:GetNetworkPing()
    local viewTime = shooterTimestamp - ping / 2

    local targetPastPosition = getPositionAtTime(targetUserId, viewTime)
    if not targetPastPosition then return false end

    -- Check if shot would have hit at that position
    -- ... perform hit detection with past position
end
```

## Bandwidth Optimization

### Quantization
```lua
-- Reduce precision for network transmission
local function quantizePosition(position)
    return Vector3.new(
        math.floor(position.X * 10) / 10,  -- 0.1 stud precision
        math.floor(position.Y * 10) / 10,
        math.floor(position.Z * 10) / 10
    )
end

local function quantizeRotation(rotation)
    return math.floor(rotation * 100) / 100  -- ~0.6 degree precision
end

-- Pack multiple small values into single number
local function packHealth(current, max)
    -- Assumes max health <= 65535 and current <= max
    return current * 65536 + max
end

local function unpackHealth(packed)
    local max = packed % 65536
    local current = math.floor(packed / 65536)
    return current, max
end
```

### String Table for Identifiers
```lua
-- Instead of sending full strings, use numeric IDs
local StringTable = {
    ["FireProjectile"] = 1,
    ["TakeDamage"] = 2,
    ["UseAbility"] = 3,
    -- ... etc
}

local ReverseTable = {}
for str, id in pairs(StringTable) do
    ReverseTable[id] = str
end

-- Send: ActionRemote:FireServer(StringTable["FireProjectile"], data)
-- Receive: local action = ReverseTable[actionId]
```

### Entity Relevancy
```lua
-- Only replicate entities relevant to each player
local RELEVANCY_DISTANCE = 200

local function getRelevantEntities(player)
    local character = player.Character
    if not character then return {} end

    local playerPos = character.PrimaryPart.Position
    local relevant = {}

    for _, entity in ipairs(allEntities) do
        local distance = (entity.Position - playerPos).Magnitude

        if distance <= RELEVANCY_DISTANCE then
            -- Close entities get full updates
            table.insert(relevant, {entity = entity, priority = 1})
        elseif distance <= RELEVANCY_DISTANCE * 2 then
            -- Medium distance gets reduced updates
            table.insert(relevant, {entity = entity, priority = 0.5})
        end
        -- Far entities not replicated
    end

    return relevant
end
```
