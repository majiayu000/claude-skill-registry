---
name: npc-ai
description: Implements NPC and AI systems including pathfinding, behavior trees, state machines, combat AI, perception systems, and NPC management. Use when building enemy AI, friendly NPCs, boss fights, or any autonomous characters.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox NPC & AI Systems

When implementing AI systems, use these Roblox-specific patterns for performant and intelligent NPCs.

## NPC Creation (CRITICAL: Use Modern Patterns)

**NEVER build NPCs by manually creating Parts.** Use `HumanoidDescription` + `CreateHumanoidModelFromDescriptionAsync`.

### Creating NPCs with HumanoidDescription

```lua
local Players = game:GetService("Players")

-- Create a basic NPC
local function createNPC(config)
    local description = Instance.new("HumanoidDescription")

    -- Customize appearance
    description.HeadColor = config.headColor or Color3.new(1, 0.8, 0.6)
    description.TorsoColor = config.torsoColor or Color3.new(0.2, 0.2, 0.8)
    description.LeftArmColor = config.headColor or Color3.new(1, 0.8, 0.6)
    description.RightArmColor = config.headColor or Color3.new(1, 0.8, 0.6)
    description.LeftLegColor = config.legColor or Color3.new(0.1, 0.1, 0.4)
    description.RightLegColor = config.legColor or Color3.new(0.1, 0.1, 0.4)

    -- Body proportions
    description.BodyTypeScale = config.bodyType or 0.5
    description.HeightScale = config.height or 1
    description.WidthScale = config.width or 1
    description.HeadScale = config.headScale or 1

    -- Accessories (comma-separated asset IDs)
    if config.hat then
        description.HatAccessory = config.hat
    end
    if config.shirt then
        description.Shirt = config.shirt
    end
    if config.pants then
        description.Pants = config.pants
    end

    -- Animations (optional custom animations)
    if config.idleAnimation then
        description.IdleAnimation = config.idleAnimation
    end
    if config.walkAnimation then
        description.WalkAnimation = config.walkAnimation
    end

    -- Create with proper rig (R15 recommended for modern features)
    local npc = Players:CreateHumanoidModelFromDescriptionAsync(
        description,
        config.rigType or Enum.HumanoidRigType.R15
    )
    npc.Name = config.name or "NPC"

    return npc
end

-- Usage
local guard = createNPC({
    name = "Guard",
    headColor = Color3.new(0.8, 0.6, 0.4),
    torsoColor = Color3.new(0.3, 0.3, 0.7),
    hat = "2551510151",  -- Asset ID
    height = 1.1,
    bodyType = 0.3
})
guard:PivotTo(CFrame.new(0, 5, 0))
guard.Parent = workspace.NPCs
```

### Clone Player Appearance for NPC

```lua
local function createNPCFromPlayer(player)
    local description = Players:GetHumanoidDescriptionFromUserIdAsync(player.UserId)
    local npc = Players:CreateHumanoidModelFromDescriptionAsync(
        description,
        Enum.HumanoidRigType.R15
    )
    npc.Name = player.Name .. "_NPC"
    return npc
end

-- Create NPC from any user ID
local function createNPCFromUserId(userId, npcName)
    local description = Players:GetHumanoidDescriptionFromUserIdAsync(userId)
    local npc = Players:CreateHumanoidModelFromDescriptionAsync(
        description,
        Enum.HumanoidRigType.R15
    )
    npc.Name = npcName or "NPC"
    return npc
end
```

### Modify Existing NPC Appearance

```lua
local function modifyNPCAppearance(npc, modifications)
    local humanoid = npc:FindFirstChildOfClass("Humanoid")
    if not humanoid then return end

    -- IMPORTANT: Get current description, don't create new
    local description = humanoid:GetAppliedDescription()

    -- Apply modifications
    if modifications.hat then
        -- Append to existing accessories
        local existing = description.HatAccessory
        description.HatAccessory = existing ~= "" and (existing .. "," .. modifications.hat) or modifications.hat
    end
    if modifications.torsoColor then
        description.TorsoColor = modifications.torsoColor
    end

    -- Apply updated description
    humanoid:ApplyDescriptionAsync(description)
end
```

## Pathfinding

### Basic PathfindingService Usage
```lua
local PathfindingService = game:GetService("PathfindingService")

local function createPath(agentParams)
    return PathfindingService:CreatePath({
        AgentRadius = agentParams.radius or 2,
        AgentHeight = agentParams.height or 5,
        AgentCanJump = agentParams.canJump ~= false,
        AgentCanClimb = agentParams.canClimb or false,
        WaypointSpacing = agentParams.waypointSpacing or 4,
        Costs = agentParams.costs or {
            Water = 20,      -- Avoid water
            Mud = 5,         -- Prefer avoiding mud
            DangerZone = 100 -- Really avoid danger
        }
    })
end

local function moveTo(npc, targetPosition)
    local humanoid = npc:FindFirstChildOfClass("Humanoid")
    local rootPart = npc:FindFirstChild("HumanoidRootPart")

    if not humanoid or not rootPart then return false end

    local path = createPath({radius = 2, height = 5})

    local success, err = pcall(function()
        path:ComputeAsync(rootPart.Position, targetPosition)
    end)

    if not success or path.Status ~= Enum.PathStatus.Success then
        -- Direct movement as fallback
        humanoid:MoveTo(targetPosition)
        return false
    end

    local waypoints = path:GetWaypoints()

    for i, waypoint in ipairs(waypoints) do
        if waypoint.Action == Enum.PathWaypointAction.Jump then
            humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
        end

        humanoid:MoveTo(waypoint.Position)

        local reached = humanoid.MoveToFinished:Wait()
        if not reached then
            -- Path blocked, recompute
            return moveTo(npc, targetPosition)
        end
    end

    return true
end
```

### Dynamic Path Recomputation
```lua
local function followTargetDynamic(npc, target, updateInterval)
    updateInterval = updateInterval or 0.5

    local path = createPath({radius = 2, height = 5})
    local currentWaypointIndex = 1
    local waypoints = {}

    local humanoid = npc:FindFirstChildOfClass("Humanoid")
    local rootPart = npc:FindFirstChild("HumanoidRootPart")

    -- Listen for path blocked
    path.Blocked:Connect(function(blockedIndex)
        if blockedIndex >= currentWaypointIndex then
            -- Recompute path
            computePath()
        end
    end)

    local function computePath()
        local targetPos = target.PrimaryPart and target.PrimaryPart.Position
        if not targetPos then return end

        path:ComputeAsync(rootPart.Position, targetPos)

        if path.Status == Enum.PathStatus.Success then
            waypoints = path:GetWaypoints()
            currentWaypointIndex = 2  -- Skip first (current position)
            moveToNextWaypoint()
        end
    end

    local function moveToNextWaypoint()
        if currentWaypointIndex > #waypoints then
            computePath()  -- Reached end, recompute
            return
        end

        local waypoint = waypoints[currentWaypointIndex]

        if waypoint.Action == Enum.PathWaypointAction.Jump then
            humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
        end

        humanoid:MoveTo(waypoint.Position)
    end

    humanoid.MoveToFinished:Connect(function(reached)
        if reached then
            currentWaypointIndex = currentWaypointIndex + 1
            moveToNextWaypoint()
        else
            computePath()  -- Stuck, recompute
        end
    end)

    -- Periodic recomputation for moving targets
    task.spawn(function()
        while npc.Parent and target.Parent do
            task.wait(updateInterval)
            computePath()
        end
    end)

    computePath()  -- Initial computation
end
```

## Behavior Trees

### Behavior Tree Structure
```lua
local BehaviorTree = {}
BehaviorTree.__index = BehaviorTree

-- Node statuses
local Status = {
    Success = "Success",
    Failure = "Failure",
    Running = "Running"
}

-- Base Node
local Node = {}
Node.__index = Node

function Node.new(name)
    return setmetatable({name = name}, Node)
end

function Node:tick(blackboard)
    return Status.Failure
end

-- Selector: Returns success on first successful child
local Selector = setmetatable({}, {__index = Node})
Selector.__index = Selector

function Selector.new(name, children)
    local self = setmetatable(Node.new(name), Selector)
    self.children = children
    return self
end

function Selector:tick(blackboard)
    for _, child in ipairs(self.children) do
        local status = child:tick(blackboard)
        if status ~= Status.Failure then
            return status
        end
    end
    return Status.Failure
end

-- Sequence: Returns failure on first failed child
local Sequence = setmetatable({}, {__index = Node})
Sequence.__index = Sequence

function Sequence.new(name, children)
    local self = setmetatable(Node.new(name), Sequence)
    self.children = children
    return self
end

function Sequence:tick(blackboard)
    for _, child in ipairs(self.children) do
        local status = child:tick(blackboard)
        if status ~= Status.Success then
            return status
        end
    end
    return Status.Success
end

-- Condition Node
local Condition = setmetatable({}, {__index = Node})
Condition.__index = Condition

function Condition.new(name, checkFunc)
    local self = setmetatable(Node.new(name), Condition)
    self.check = checkFunc
    return self
end

function Condition:tick(blackboard)
    return self.check(blackboard) and Status.Success or Status.Failure
end

-- Action Node
local Action = setmetatable({}, {__index = Node})
Action.__index = Action

function Action.new(name, actionFunc)
    local self = setmetatable(Node.new(name), Action)
    self.action = actionFunc
    return self
end

function Action:tick(blackboard)
    return self.action(blackboard)
end
```

### Example Combat AI Behavior Tree
```lua
local function createCombatAI(npc)
    local blackboard = {
        npc = npc,
        target = nil,
        lastAttackTime = 0,
        health = 100
    }

    local tree = Selector.new("Root", {
        -- Priority 1: Flee if low health
        Sequence.new("FleeIfLowHealth", {
            Condition.new("IsLowHealth", function(bb)
                return bb.health < 20
            end),
            Action.new("Flee", function(bb)
                fleeBehavior(bb.npc, bb.target)
                return Status.Running
            end)
        }),

        -- Priority 2: Attack if target in range
        Sequence.new("AttackSequence", {
            Condition.new("HasTarget", function(bb)
                return bb.target ~= nil
            end),
            Condition.new("InAttackRange", function(bb)
                local distance = getDistance(bb.npc, bb.target)
                return distance < 5
            end),
            Condition.new("CanAttack", function(bb)
                return os.clock() - bb.lastAttackTime > 1
            end),
            Action.new("Attack", function(bb)
                attackTarget(bb.npc, bb.target)
                bb.lastAttackTime = os.clock()
                return Status.Success
            end)
        }),

        -- Priority 3: Chase target
        Sequence.new("ChaseSequence", {
            Condition.new("HasTarget", function(bb)
                return bb.target ~= nil
            end),
            Action.new("ChaseTarget", function(bb)
                moveTo(bb.npc, bb.target.PrimaryPart.Position)
                return Status.Running
            end)
        }),

        -- Priority 4: Patrol
        Action.new("Patrol", function(bb)
            patrolBehavior(bb.npc)
            return Status.Running
        end)
    })

    -- Tick the tree regularly
    task.spawn(function()
        while npc.Parent do
            tree:tick(blackboard)
            task.wait(0.1)
        end
    end)

    return blackboard
end
```

## State Machines

### Finite State Machine
```lua
local StateMachine = {}
StateMachine.__index = StateMachine

function StateMachine.new(initialState)
    return setmetatable({
        currentState = initialState,
        states = {},
        transitions = {}
    }, StateMachine)
end

function StateMachine:addState(name, callbacks)
    self.states[name] = {
        enter = callbacks.enter or function() end,
        update = callbacks.update or function() end,
        exit = callbacks.exit or function() end
    }
end

function StateMachine:addTransition(from, to, condition)
    self.transitions[from] = self.transitions[from] or {}
    table.insert(self.transitions[from], {
        target = to,
        condition = condition
    })
end

function StateMachine:changeState(newState)
    if not self.states[newState] then return end

    if self.currentState then
        self.states[self.currentState].exit(self)
    end

    self.currentState = newState
    self.states[newState].enter(self)
end

function StateMachine:update(dt)
    -- Check transitions
    local transitions = self.transitions[self.currentState]
    if transitions then
        for _, transition in ipairs(transitions) do
            if transition.condition(self) then
                self:changeState(transition.target)
                return
            end
        end
    end

    -- Update current state
    if self.states[self.currentState] then
        self.states[self.currentState].update(self, dt)
    end
end

-- Example usage for NPC
local function createNPCStateMachine(npc)
    local sm = StateMachine.new("Idle")

    sm.npc = npc
    sm.target = nil
    sm.patrolIndex = 1
    sm.patrolPoints = getPatrolPoints(npc)

    sm:addState("Idle", {
        enter = function(self)
            self.npc:FindFirstChildOfClass("Humanoid").WalkSpeed = 0
        end,
        update = function(self, dt)
            -- Look around occasionally
            if math.random() < 0.01 then
                lookAround(self.npc)
            end
        end
    })

    sm:addState("Patrol", {
        enter = function(self)
            self.npc:FindFirstChildOfClass("Humanoid").WalkSpeed = 8
        end,
        update = function(self, dt)
            local target = self.patrolPoints[self.patrolIndex]
            if reachedPoint(self.npc, target) then
                self.patrolIndex = self.patrolIndex % #self.patrolPoints + 1
            end
            moveTo(self.npc, target)
        end
    })

    sm:addState("Chase", {
        enter = function(self)
            self.npc:FindFirstChildOfClass("Humanoid").WalkSpeed = 16
        end,
        update = function(self, dt)
            if self.target then
                moveTo(self.npc, self.target.PrimaryPart.Position)
            end
        end
    })

    sm:addState("Attack", {
        enter = function(self)
            self.npc:FindFirstChildOfClass("Humanoid").WalkSpeed = 0
        end,
        update = function(self, dt)
            if self.target then
                faceTarget(self.npc, self.target)
                attack(self.npc, self.target)
            end
        end
    })

    -- Transitions
    sm:addTransition("Idle", "Patrol", function(self)
        return os.clock() % 10 > 5  -- Alternate idle/patrol
    end)

    sm:addTransition("Patrol", "Chase", function(self)
        return self.target ~= nil
    end)

    sm:addTransition("Chase", "Attack", function(self)
        return self.target and getDistance(self.npc, self.target) < 5
    end)

    sm:addTransition("Attack", "Chase", function(self)
        return self.target and getDistance(self.npc, self.target) > 7
    end)

    sm:addTransition("Chase", "Patrol", function(self)
        return self.target == nil
    end)

    return sm
end
```

## Perception Systems

### Vision Cone
```lua
local function canSeeTarget(npc, target, fovAngle, maxDistance)
    fovAngle = fovAngle or 90  -- degrees
    maxDistance = maxDistance or 50

    local npcRoot = npc:FindFirstChild("HumanoidRootPart")
    local targetRoot = target:FindFirstChild("HumanoidRootPart")

    if not npcRoot or not targetRoot then return false end

    local toTarget = targetRoot.Position - npcRoot.Position
    local distance = toTarget.Magnitude

    -- Distance check
    if distance > maxDistance then return false end

    -- Angle check (dot product)
    local npcForward = npcRoot.CFrame.LookVector
    local directionToTarget = toTarget.Unit
    local dot = npcForward:Dot(directionToTarget)
    local angle = math.deg(math.acos(dot))

    if angle > fovAngle / 2 then return false end

    -- Line of sight check (raycast)
    local rayParams = RaycastParams.new()
    rayParams.FilterDescendantsInstances = {npc}

    local result = workspace:Raycast(npcRoot.Position, toTarget, rayParams)

    if result then
        return result.Instance:IsDescendantOf(target)
    end

    return false
end
```

### Hearing System
```lua
local SoundEvents = {}

local function emitSound(position, radius, soundType)
    for _, npc in ipairs(activeNPCs) do
        local npcPos = npc.PrimaryPart.Position
        local distance = (position - npcPos).Magnitude

        if distance <= radius then
            -- Sound intensity falls off with distance
            local intensity = 1 - (distance / radius)

            -- Notify NPC's AI
            local ai = npc:GetAttribute("AIController")
            if ai then
                ai:onHearSound(position, soundType, intensity)
            end
        end
    end
end

-- Usage
emitSound(player.Character.PrimaryPart.Position, 30, "Gunshot")
emitSound(player.Character.PrimaryPart.Position, 10, "Footstep")
```

### Memory System
```lua
local NPCMemory = {}

function NPCMemory.new(forgetTime)
    return {
        memories = {},
        forgetTime = forgetTime or 30
    }
end

function NPCMemory:remember(entityId, data)
    self.memories[entityId] = {
        data = data,
        lastSeen = os.clock()
    }
end

function NPCMemory:getLastKnown(entityId)
    local memory = self.memories[entityId]
    if not memory then return nil end

    if os.clock() - memory.lastSeen > self.forgetTime then
        self.memories[entityId] = nil
        return nil
    end

    return memory.data
end

function NPCMemory:forgetOld()
    local now = os.clock()
    for entityId, memory in pairs(self.memories) do
        if now - memory.lastSeen > self.forgetTime then
            self.memories[entityId] = nil
        end
    end
end

-- Usage in AI
local function updatePerception(npc, memory)
    for _, player in ipairs(Players:GetPlayers()) do
        if player.Character and canSeeTarget(npc, player.Character, 90, 50) then
            memory:remember(player.UserId, {
                position = player.Character.PrimaryPart.Position,
                lastSeenTime = os.clock()
            })
        end
    end
end
```

## NPC Management

### NPC Pooling
```lua
local NPCPool = {}
NPCPool.available = {}
NPCPool.active = {}
NPCPool.template = nil

function NPCPool.init(template, initialSize)
    NPCPool.template = template

    for i = 1, initialSize do
        local npc = template:Clone()
        npc.Parent = nil  -- Not in workspace
        table.insert(NPCPool.available, npc)
    end
end

function NPCPool.spawn(position, data)
    local npc

    if #NPCPool.available > 0 then
        npc = table.remove(NPCPool.available)
    else
        npc = NPCPool.template:Clone()
    end

    -- Reset NPC state
    npc:PivotTo(CFrame.new(position))
    local humanoid = npc:FindFirstChildOfClass("Humanoid")
    humanoid.Health = humanoid.MaxHealth

    -- Apply data
    for key, value in pairs(data or {}) do
        npc:SetAttribute(key, value)
    end

    npc.Parent = workspace.NPCs
    table.insert(NPCPool.active, npc)

    return npc
end

function NPCPool.despawn(npc)
    -- Remove from active
    local index = table.find(NPCPool.active, npc)
    if index then
        table.remove(NPCPool.active, index)
    end

    -- Reset and return to pool
    npc.Parent = nil
    table.insert(NPCPool.available, npc)
end
```

### Performance Budgeting
```lua
local AI_BUDGET_MS = 5  -- Max 5ms per frame for AI

local function updateAllAI()
    local startTime = os.clock()
    local processed = 0

    for _, npc in ipairs(activeNPCs) do
        -- Process this NPC's AI
        updateNPCAI(npc)
        processed = processed + 1

        -- Check budget
        local elapsed = (os.clock() - startTime) * 1000
        if elapsed > AI_BUDGET_MS then
            break
        end
    end

    -- Continue next frame with remaining NPCs
    -- Use round-robin or priority-based ordering
end

RunService.Heartbeat:Connect(updateAllAI)
```
