---
name: roblox-api-patterns
description: Provides Roblox-specific API patterns, gotchas, best practices, and platform knowledge. Use when you need to understand Roblox-specific behaviors, services, or common pitfalls.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox API Patterns & Gotchas

## Quick Reference Links

**Official Documentation:**
- [Engine API Reference](https://create.roblox.com/docs/reference/engine) - Complete API reference
- [Luau Language](https://create.roblox.com/docs/luau) - Roblox's Lua variant
- [Scripts Overview](https://create.roblox.com/docs/scripting/scripts) - Script types and lifecycle
- [Services](https://create.roblox.com/docs/reference/engine/classes/ServiceProvider) - All game services
- [Instance API](https://create.roblox.com/docs/reference/engine/classes/Instance)
- [Players API](https://create.roblox.com/docs/reference/engine/classes/Players)
- [RunService API](https://create.roblox.com/docs/reference/engine/classes/RunService)

**Wiki References:**
- [Scripting (Wiki)](https://roblox.fandom.com/wiki/Scripting)
- [Services (Wiki)](https://roblox.fandom.com/wiki/Service)
- [Instance (Wiki)](https://roblox.fandom.com/wiki/Instance)

**Learning Resources:**
- [Roblox DevForum](https://devforum.roblox.com/)
- [Roblox Education](https://create.roblox.com/docs/education)

---

When working with Roblox APIs, be aware of these platform-specific behaviors and patterns.

## Common Gotchas

### Instance.new() - Set Parent Last
```lua
-- BAD: Setting parent first causes events to fire during setup
local part = Instance.new("Part")
part.Parent = workspace  -- Events fire here!
part.Size = Vector3.new(5, 5, 5)  -- Property changes after parenting

-- GOOD: Set all properties, then parent
local part = Instance.new("Part")
part.Size = Vector3.new(5, 5, 5)
part.Position = Vector3.new(0, 10, 0)
part.Anchored = true
part.Parent = workspace  -- Only fires events once, fully configured

-- BETTER: Use Instance.new with parent argument (deprecated but still works)
-- Actually, the second argument is being phased out. Stick with setting parent last.
```

### WaitForChild Timeout
```lua
-- BAD: Can hang indefinitely if child doesn't exist
local child = parent:WaitForChild("MaybeExists")

-- GOOD: Use timeout
local child = parent:WaitForChild("MaybeExists", 5)  -- 5 second timeout
if child then
    -- Child found
else
    warn("Child not found after 5 seconds")
end
```

### Touched Events Fire Multiple Times
```lua
-- BAD: Can trigger multiple times per contact
part.Touched:Connect(function(hit)
    dealDamage(hit)  -- May deal damage multiple times!
end)

-- GOOD: Debounce
local debounce = {}
part.Touched:Connect(function(hit)
    local character = hit.Parent
    if debounce[character] then return end

    debounce[character] = true
    dealDamage(hit)

    task.delay(0.5, function()
        debounce[character] = nil
    end)
end)
```

### os.clock() vs tick() vs time()
```lua
-- os.clock(): High-resolution timer, best for measuring elapsed time
local start = os.clock()
-- ... code ...
local elapsed = os.clock() - start

-- tick(): DEPRECATED, don't use in new code

-- time(): Returns time since game started, affected by time scale
local gameTime = time()

-- workspace:GetServerTimeNow(): Synchronized server time
local serverTime = workspace:GetServerTimeNow()

-- os.time(): Unix timestamp (seconds since 1970)
local unixTime = os.time()
```

### Humanoid States
```lua
-- Humanoid states can be unreliable
-- Don't rely solely on StateChanged

local humanoid = character:WaitForChild("Humanoid")

-- Check state directly
local function isGrounded()
    -- FloorMaterial is more reliable than state
    return humanoid.FloorMaterial ~= Enum.Material.Air
end

-- Or use raycasts
local function isGroundedRaycast()
    local hrp = character:FindFirstChild("HumanoidRootPart")
    if not hrp then return false end

    local result = workspace:Raycast(
        hrp.Position,
        Vector3.new(0, -3.1, 0),  -- Slightly more than hip height
        RaycastParams.new()
    )
    return result ~= nil
end
```

### GetChildren vs GetDescendants
```lua
-- GetChildren: Only immediate children
local children = model:GetChildren()

-- GetDescendants: All descendants (recursive)
local allParts = model:GetDescendants()

-- Both return tables that are snapshots
-- Adding/removing during iteration is safe but won't be reflected
for _, child in ipairs(model:GetChildren()) do
    child:Destroy()  -- Safe, iterating over snapshot
end
```

## Service Patterns

### Players Service
```lua
local Players = game:GetService("Players")

-- Get local player (client only)
local localPlayer = Players.LocalPlayer

-- Player events
Players.PlayerAdded:Connect(function(player)
    -- Note: Character may not exist yet
    player.CharacterAdded:Connect(function(character)
        -- Character loaded
    end)

    -- If character already exists (late connection)
    if player.Character then
        -- Handle existing character
    end
end)

-- PlayerRemoving fires BEFORE player is removed
Players.PlayerRemoving:Connect(function(player)
    -- Save data here, player still valid
end)
```

### RunService
```lua
local RunService = game:GetService("RunService")

-- Different update events
RunService.PreRender:Connect(function(dt)
    -- Before rendering (client only, after input)
end)

RunService.PreAnimation:Connect(function(dt)
    -- Before animation update
end)

RunService.PreSimulation:Connect(function(dt)
    -- Before physics
end)

RunService.PostSimulation:Connect(function(dt)
    -- After physics (same as Stepped)
end)

RunService.Heartbeat:Connect(function(dt)
    -- After physics and before rendering
    -- Most common for game logic
end)

RunService.RenderStepped:Connect(function(dt)
    -- Every frame, client only
    -- Use for camera/visual updates
end)

-- Check context
if RunService:IsClient() then
    -- Client-side code
end
if RunService:IsServer() then
    -- Server-side code
end
if RunService:IsStudio() then
    -- Running in Studio
end
```

### TweenService
```lua
local TweenService = game:GetService("TweenService")

-- Create tween
local tweenInfo = TweenInfo.new(
    1,                           -- Duration
    Enum.EasingStyle.Quad,       -- EasingStyle
    Enum.EasingDirection.Out,    -- EasingDirection
    0,                           -- RepeatCount (0 = no repeat)
    false,                       -- Reverses
    0                            -- DelayTime
)

local tween = TweenService:Create(part, tweenInfo, {
    Position = Vector3.new(0, 10, 0),
    Transparency = 0.5
})

tween:Play()

-- Wait for completion
tween.Completed:Wait()
-- or
tween.Completed:Connect(function(playbackState)
    if playbackState == Enum.PlaybackState.Completed then
        -- Finished normally
    elseif playbackState == Enum.PlaybackState.Cancelled then
        -- Was cancelled
    end
end)

-- Cancel tween
tween:Cancel()

-- Tweening CFrame (doesn't lerp, use custom for smooth rotation)
-- Use CFrame:Lerp() manually for better control
```

### DataStoreService Limits
```lua
local DataStoreService = game:GetService("DataStoreService")

-- Rate limits:
-- GetAsync: 60 + numPlayers * 10 per minute
-- SetAsync: 60 + numPlayers * 10 per minute
-- UpdateAsync: 60 + numPlayers * 10 per minute
-- GetSortedAsync: 5 + numPlayers per minute
-- SetSortedAsync: 60 + numPlayers * 10 per minute

-- Data limits:
-- Key length: 50 characters max
-- Value size: 4MB max
-- Key format: Only alphanumeric and underscores

-- Budget system
local budget = DataStoreService:GetRequestBudgetForRequestType(
    Enum.DataStoreRequestType.GetAsync
)
print("GetAsync budget:", budget)
```

### MarketplaceService
```lua
local MarketplaceService = game:GetService("MarketplaceService")

-- Check ownership
local function ownsGamepass(player, gamepassId)
    local success, owns = pcall(function()
        return MarketplaceService:UserOwnsGamePassAsync(player.UserId, gamepassId)
    end)
    return success and owns
end

-- Developer Products (consumable)
MarketplaceService.ProcessReceipt = function(receiptInfo)
    -- MUST return a value
    -- PurchaseGranted: Purchase successful, receipt cleared
    -- NotProcessedYet: Try again later (player rejoins, etc.)

    local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
    if not player then
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end

    -- Grant product...

    return Enum.ProductPurchaseDecision.PurchaseGranted
end

-- Prompt purchase
MarketplaceService:PromptProductPurchase(player, productId)
MarketplaceService:PromptGamePassPurchase(player, gamepassId)
```

## RemoteEvent/Function Patterns

### Type Safety
```lua
-- Client sends data, server receives
-- NEVER trust client data types

RemoteEvent.OnServerEvent:Connect(function(player, data)
    -- Validate types
    if type(data) ~= "table" then return end
    if type(data.action) ~= "string" then return end
    if type(data.value) ~= "number" then return end

    -- Validate ranges
    if data.value < 0 or data.value > 100 then return end
    if data.value ~= data.value then return end  -- NaN check

    -- Now safe to use
end)
```

### RemoteFunction Timeout
```lua
-- RemoteFunctions can hang if server/client doesn't respond
-- Wrap in pcall and use manual timeout

local function safeInvoke(remote, ...)
    local args = {...}
    local result
    local finished = false

    task.spawn(function()
        local success, response = pcall(function()
            return remote:InvokeServer(unpack(args))
        end)
        if success then
            result = response
        end
        finished = true
    end)

    -- Timeout after 10 seconds
    local startTime = os.clock()
    while not finished and os.clock() - startTime < 10 do
        task.wait()
    end

    return result
end
```

## Physics Patterns

### Network Ownership
```lua
-- Parts have network owners that control physics simulation
local part = workspace.MyPart

-- Set owner to specific player
part:SetNetworkOwner(player)

-- Set owner to server (nil)
part:SetNetworkOwner(nil)

-- Get current owner
local owner = part:GetNetworkOwner()

-- Check if can set
if part:CanSetNetworkOwnership() then
    part:SetNetworkOwner(player)
end

-- Anchored parts have no network owner
-- Welded parts inherit owner from root part
```

### AssemblyLinearVelocity vs Velocity
```lua
-- Velocity is DEPRECATED
-- Use AssemblyLinearVelocity and AssemblyAngularVelocity

local part = workspace.MyPart

-- Get velocity
local linearVel = part.AssemblyLinearVelocity
local angularVel = part.AssemblyAngularVelocity

-- Set velocity (only works if you're network owner)
part.AssemblyLinearVelocity = Vector3.new(0, 50, 0)

-- For applying forces, use constraints instead
local attachment = Instance.new("Attachment", part)
local linearVelocity = Instance.new("LinearVelocity")
linearVelocity.Attachment0 = attachment
linearVelocity.VectorVelocity = Vector3.new(0, 50, 0)
linearVelocity.MaxForce = math.huge
linearVelocity.Parent = part
```

## Animation Patterns

### Loading Animations
```lua
local humanoid = character:WaitForChild("Humanoid")
local animator = humanoid:WaitForChild("Animator")

-- Load animation
local animation = Instance.new("Animation")
animation.AnimationId = "rbxassetid://123456789"

local track = animator:LoadAnimation(animation)

-- Play with settings
track:Play(
    0.1,  -- Fade in time
    1,    -- Weight
    1     -- Speed
)

-- Animation priorities
track.Priority = Enum.AnimationPriority.Action  -- Highest
-- Core < Idle < Movement < Action

-- Animation events
track:GetMarkerReachedSignal("FootstepMarker"):Connect(function()
    playFootstepSound()
end)

-- Stop
track:Stop(0.1)  -- Fade out time
```

## Lighting Patterns

### Time of Day
```lua
local Lighting = game:GetService("Lighting")

-- Set time (0-24 hours)
Lighting.ClockTime = 14.5  -- 2:30 PM

-- Animate day/night cycle
local function updateTimeOfDay()
    Lighting.ClockTime = (Lighting.ClockTime + 0.001) % 24
end

-- Geographic time (affects sun angle)
Lighting.GeographicLatitude = 41.9  -- New York latitude
```

### Post-Processing
```lua
-- Add to Lighting or Camera
local blur = Instance.new("BlurEffect")
blur.Size = 10
blur.Parent = Lighting

local colorCorrection = Instance.new("ColorCorrectionEffect")
colorCorrection.Brightness = 0.1
colorCorrection.Contrast = 0.2
colorCorrection.Saturation = -0.1
colorCorrection.Parent = Lighting

local bloom = Instance.new("BloomEffect")
bloom.Intensity = 0.5
bloom.Size = 24
bloom.Threshold = 0.95
bloom.Parent = Lighting
```

## Common Attribute Patterns

### Using Attributes
```lua
-- Set attribute
part:SetAttribute("Health", 100)
part:SetAttribute("Team", "Red")
part:SetAttribute("IsActive", true)

-- Get attribute
local health = part:GetAttribute("Health")

-- Get all attributes
local attributes = part:GetAttributes()
for name, value in pairs(attributes) do
    print(name, value)
end

-- Listen for changes
part:GetAttributeChangedSignal("Health"):Connect(function()
    local newHealth = part:GetAttribute("Health")
end)

-- Attributes replicate automatically (server -> client)
-- Attributes persist with the instance
```

## Debugging Patterns

### Print Debugging
```lua
-- Use warn for visibility
warn("Important message")

-- Structured logging
local function log(level, message, data)
    local timestamp = os.date("%H:%M:%S")
    local output = string.format("[%s] [%s] %s", timestamp, level, message)
    if data then
        output = output .. " " .. HttpService:JSONEncode(data)
    end
    print(output)
end

log("INFO", "Player joined", {userId = player.UserId})
```

### Error Handling
```lua
-- Always wrap risky operations
local success, result = pcall(function()
    return riskyOperation()
end)

if success then
    -- Use result
else
    warn("Operation failed:", result)
end

-- With xpcall for stack traces
local success, result = xpcall(function()
    return riskyOperation()
end, function(err)
    warn("Error:", err)
    warn(debug.traceback())
end)
```
