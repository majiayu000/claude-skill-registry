---
name: constraints-physics
description: Implements constraint-based physics systems including all constraint types, ragdoll systems, custom physics, and network ownership. Use when building mechanical systems, ragdolls, rope physics, or any physics-driven gameplay.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Constraints & Physics

## Quick Reference Links

**Official Documentation:**
- [Constraints Overview](https://create.roblox.com/docs/physics/mechanical-constraints)
- [Mover Constraints](https://create.roblox.com/docs/physics/mover-constraints) - VectorForce, BodyGyro, etc.
- [Physics Simulation](https://create.roblox.com/docs/physics)
- [Network Ownership](https://create.roblox.com/docs/physics/network-ownership)
- [WeldConstraint API](https://create.roblox.com/docs/reference/engine/classes/WeldConstraint)
- [RigidConstraint API](https://create.roblox.com/docs/reference/engine/classes/RigidConstraint)
- [RopeConstraint API](https://create.roblox.com/docs/reference/engine/classes/RopeConstraint)
- [BallSocketConstraint API](https://create.roblox.com/docs/reference/engine/classes/BallSocketConstraint)
- [HingeConstraint API](https://create.roblox.com/docs/reference/engine/classes/HingeConstraint)

**Wiki References:**
- [Constraints (Wiki)](https://roblox.fandom.com/wiki/Constraint)
- [Physics (Wiki)](https://roblox.fandom.com/wiki/Physics)

---

When implementing physics systems, use these constraint patterns for realistic and performant mechanics.

## Constraint Reference

### WeldConstraint
```lua
-- Rigid connection between two parts (no relative movement)
local weld = Instance.new("WeldConstraint")
weld.Part0 = part1
weld.Part1 = part2
weld.Parent = part1

-- Use for: Static connections, attaching accessories
-- Note: More efficient than Motor6D for non-animated joints
```

### Motor6D
```lua
-- Animated joint with C0/C1 transforms
local motor = Instance.new("Motor6D")
motor.Part0 = torso
motor.Part1 = arm
motor.C0 = CFrame.new(1.5, 0.5, 0)  -- Offset from Part0
motor.C1 = CFrame.new(0, 0.5, 0)    -- Offset from Part1
motor.Parent = torso

-- Animate by changing Transform property
motor.Transform = CFrame.Angles(0, 0, math.rad(45))

-- Use for: Character rigs, animated machinery
```

### HingeConstraint
```lua
-- Single-axis rotation (doors, wheels)
local hinge = Instance.new("HingeConstraint")
hinge.Attachment0 = attachment0  -- On Part0
hinge.Attachment1 = attachment1  -- On Part1

-- Limits
hinge.LimitsEnabled = true
hinge.LowerAngle = -90
hinge.UpperAngle = 90

-- Motor mode (powered rotation)
hinge.ActuatorType = Enum.ActuatorType.Motor
hinge.MotorMaxTorque = 10000
hinge.AngularVelocity = 10  -- Target velocity (rad/s)

-- Servo mode (target angle)
hinge.ActuatorType = Enum.ActuatorType.Servo
hinge.TargetAngle = 45
hinge.AngularSpeed = 5
hinge.ServoMaxTorque = 10000

hinge.Parent = part1

-- Read current angle
local currentAngle = hinge.CurrentAngle
```

### BallSocketConstraint
```lua
-- Three-axis rotation (ragdoll joints)
local ballSocket = Instance.new("BallSocketConstraint")
ballSocket.Attachment0 = attachment0
ballSocket.Attachment1 = attachment1

-- Twist limits (rotation around axis)
ballSocket.TwistLimitsEnabled = true
ballSocket.TwistLowerAngle = -45
ballSocket.TwistUpperAngle = 45

-- Cone limits (swing angle)
ballSocket.LimitsEnabled = true
ballSocket.UpperAngle = 60  -- Max angle from axis

ballSocket.Parent = part1
```

### RopeConstraint
```lua
-- Flexible connection with max length
local rope = Instance.new("RopeConstraint")
rope.Attachment0 = attachment0
rope.Attachment1 = attachment1
rope.Length = 10
rope.Restitution = 0.5  -- Bounciness when taut
rope.Visible = true
rope.Thickness = 0.1
rope.Color = BrickColor.new("Brown")
rope.Parent = part1

-- Use for: Chains, swings, tethers
```

### RodConstraint
```lua
-- Rigid connection maintaining fixed distance
local rod = Instance.new("RodConstraint")
rod.Attachment0 = attachment0
rod.Attachment1 = attachment1
rod.Length = 5
rod.Visible = true
rod.Thickness = 0.1
rod.Parent = part1

-- Use for: Pistons, connecting rods, suspension links
```

### SpringConstraint
```lua
-- Damped spring connection
local spring = Instance.new("SpringConstraint")
spring.Attachment0 = attachment0
spring.Attachment1 = attachment1
spring.FreeLength = 5    -- Rest length
spring.Stiffness = 1000  -- Spring constant
spring.Damping = 100     -- Damping coefficient
spring.LimitsEnabled = true
spring.MinLength = 2
spring.MaxLength = 8
spring.Visible = true
spring.Coils = 5
spring.Parent = part1

-- Use for: Suspension, bouncy platforms
```

### PrismaticConstraint
```lua
-- Sliding along one axis
local prismatic = Instance.new("PrismaticConstraint")
prismatic.Attachment0 = attachment0
prismatic.Attachment1 = attachment1

-- Limits
prismatic.LimitsEnabled = true
prismatic.LowerLimit = -5
prismatic.UpperLimit = 5

-- Motor mode
prismatic.ActuatorType = Enum.ActuatorType.Motor
prismatic.MotorMaxForce = 10000
prismatic.Velocity = 5

prismatic.Parent = part1

-- Read current position
local currentPosition = prismatic.CurrentPosition
```

### CylindricalConstraint
```lua
-- Combined rotation and sliding (steering columns)
local cylindrical = Instance.new("CylindricalConstraint")
cylindrical.Attachment0 = attachment0
cylindrical.Attachment1 = attachment1

-- Angular limits and motor (like hinge)
cylindrical.AngularLimitsEnabled = true
cylindrical.LowerAngle = -180
cylindrical.UpperAngle = 180
cylindrical.AngularActuatorType = Enum.ActuatorType.Motor
cylindrical.AngularVelocity = 5
cylindrical.MotorMaxAngularAcceleration = 100
cylindrical.MotorMaxTorque = 1000

-- Linear limits and motor (like prismatic)
cylindrical.LimitsEnabled = true
cylindrical.LowerLimit = 0
cylindrical.UpperLimit = 2

cylindrical.Parent = part1
```

## Alignment Constraints

### AlignPosition
```lua
-- Smoothly move part to target position
local align = Instance.new("AlignPosition")
align.Attachment0 = attachment0
align.Mode = Enum.PositionAlignmentMode.OneAttachment

-- Target options
align.Position = Vector3.new(0, 10, 0)
-- OR
align.Attachment1 = targetAttachment

-- Behavior
align.RigidityEnabled = false  -- Smooth movement
align.MaxForce = 10000
align.MaxVelocity = 50
align.Responsiveness = 20  -- Higher = faster response

-- Or rigid positioning
align.RigidityEnabled = true
-- Ignores MaxForce/MaxVelocity, instantly positions

align.Parent = part
```

### AlignOrientation
```lua
-- Smoothly rotate part to target orientation
local align = Instance.new("AlignOrientation")
align.Attachment0 = attachment0
align.Mode = Enum.OrientationAlignmentMode.OneAttachment

-- Target
align.CFrame = CFrame.Angles(0, math.rad(45), 0)
-- OR
align.Attachment1 = targetAttachment

-- Behavior
align.RigidityEnabled = false
align.MaxTorque = 10000
align.MaxAngularVelocity = 10
align.Responsiveness = 20

align.Parent = part
```

### VectorForce
```lua
-- Apply constant force
local force = Instance.new("VectorForce")
force.Attachment0 = attachment
force.Force = Vector3.new(0, 1000, 0)  -- Upward force
force.RelativeTo = Enum.ActuatorRelativeTo.World
-- or Attachment0 for local space
force.Parent = part
```

### LinearVelocity
```lua
-- Maintain target velocity
local linVel = Instance.new("LinearVelocity")
linVel.Attachment0 = attachment
linVel.VectorVelocity = Vector3.new(0, 0, -50)  -- Forward motion
linVel.MaxForce = math.huge
linVel.RelativeTo = Enum.ActuatorRelativeTo.Attachment0  -- Local space
linVel.Parent = part
```

### AngularVelocity
```lua
-- Maintain rotational velocity
local angVel = Instance.new("AngularVelocity")
angVel.Attachment0 = attachment
angVel.AngularVelocity = Vector3.new(0, 10, 0)  -- Spin around Y
angVel.MaxTorque = math.huge
angVel.RelativeTo = Enum.ActuatorRelativeTo.World
angVel.Parent = part
```

## Ragdoll System

### Converting Character to Ragdoll
```lua
local function activateRagdoll(character)
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid then return end

    -- Disable humanoid control
    humanoid.PlatformStand = true
    humanoid:ChangeState(Enum.HumanoidStateType.Physics)

    -- Convert Motor6D to BallSocket
    for _, motor in ipairs(character:GetDescendants()) do
        if motor:IsA("Motor6D") then
            local part0 = motor.Part0
            local part1 = motor.Part1
            local c0 = motor.C0
            local c1 = motor.C1

            -- Create attachments at motor positions
            local att0 = Instance.new("Attachment")
            att0.CFrame = c0
            att0.Parent = part0

            local att1 = Instance.new("Attachment")
            att1.CFrame = c1
            att1.Parent = part1

            -- Create ball socket
            local socket = Instance.new("BallSocketConstraint")
            socket.Attachment0 = att0
            socket.Attachment1 = att1
            socket.LimitsEnabled = true
            socket.UpperAngle = 45  -- Limit joint movement
            socket.TwistLimitsEnabled = true
            socket.TwistLowerAngle = -30
            socket.TwistUpperAngle = 30
            socket.Parent = part0

            -- Disable motor
            motor.Enabled = false
        end
    end

    -- Configure collision
    for _, part in ipairs(character:GetDescendants()) do
        if part:IsA("BasePart") then
            part.CanCollide = true
        end
    end
end

local function deactivateRagdoll(character)
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid then return end

    -- Re-enable motors
    for _, motor in ipairs(character:GetDescendants()) do
        if motor:IsA("Motor6D") then
            motor.Enabled = true
        end
    end

    -- Remove ball sockets
    for _, constraint in ipairs(character:GetDescendants()) do
        if constraint:IsA("BallSocketConstraint") then
            constraint:Destroy()
        end
    end

    -- Restore humanoid
    humanoid.PlatformStand = false
    humanoid:ChangeState(Enum.HumanoidStateType.GettingUp)
end
```

### Partial Ragdoll (Limb Only)
```lua
local function ragdollLimb(character, limbName)
    local limb = character:FindFirstChild(limbName)
    if not limb then return end

    -- Find motor connecting this limb
    local motor
    for _, m in ipairs(character:GetDescendants()) do
        if m:IsA("Motor6D") and m.Part1 == limb then
            motor = m
            break
        end
    end

    if not motor then return end

    -- Ragdoll just this joint
    local att0 = Instance.new("Attachment")
    att0.CFrame = motor.C0
    att0.Parent = motor.Part0

    local att1 = Instance.new("Attachment")
    att1.CFrame = motor.C1
    att1.Parent = motor.Part1

    local socket = Instance.new("BallSocketConstraint")
    socket.Attachment0 = att0
    socket.Attachment1 = att1
    socket.LimitsEnabled = true
    socket.UpperAngle = 90
    socket.Parent = motor.Part0

    motor.Enabled = false
    limb.CanCollide = true
end
```

## Network Ownership

### Setting Ownership
```lua
-- Parts have network owners that simulate physics
local part = workspace.MyPart

-- Check if ownership can be set
if part:CanSetNetworkOwnership() then
    -- Set to player
    part:SetNetworkOwner(player)

    -- Set to server
    part:SetNetworkOwner(nil)
end

-- Get current owner
local owner = part:GetNetworkOwner()
print("Owner:", owner and owner.Name or "Server")
```

### Ownership for Vehicles
```lua
local function setVehicleOwnership(vehicle, player)
    for _, part in ipairs(vehicle:GetDescendants()) do
        if part:IsA("BasePart") and not part.Anchored then
            if part:CanSetNetworkOwnership() then
                part:SetNetworkOwner(player)
            end
        end
    end
end

-- When driver enters
vehicleSeat:GetPropertyChangedSignal("Occupant"):Connect(function()
    local occupant = vehicleSeat.Occupant
    if occupant then
        local player = Players:GetPlayerFromCharacter(occupant.Parent)
        if player then
            setVehicleOwnership(vehicle, player)
        end
    else
        setVehicleOwnership(vehicle, nil)  -- Back to server
    end
end)
```

### Ownership with Constraints
```lua
-- Constrained parts share network owner with root
-- The "root" is typically the most massive connected part

-- For rope/chain: set ownership on anchor point
anchorPart:SetNetworkOwner(nil)  -- Server controls anchor
-- Other parts follow

-- For vehicles: set on chassis
chassis:SetNetworkOwner(driver)
-- Wheels and body follow automatically
```

## Custom Physics Behaviors

### Custom Gravity
```lua
local function setCustomGravity(part, gravityVector)
    -- Counter default gravity and apply custom
    local attachment = part:FindFirstChild("GravityAttachment") or Instance.new("Attachment", part)
    attachment.Name = "GravityAttachment"

    local force = part:FindFirstChild("GravityForce") or Instance.new("VectorForce", part)
    force.Name = "GravityForce"
    force.Attachment0 = attachment
    force.RelativeTo = Enum.ActuatorRelativeTo.World

    -- Counter default gravity and apply custom
    local counterForce = part:GetMass() * workspace.Gravity
    local customForce = part:GetMass() * gravityVector.Magnitude

    force.Force = Vector3.new(0, counterForce, 0) + gravityVector * part:GetMass()
end

-- Zero gravity
setCustomGravity(part, Vector3.new(0, 0, 0))

-- Reversed gravity
setCustomGravity(part, Vector3.new(0, workspace.Gravity, 0))

-- Diagonal gravity
setCustomGravity(part, Vector3.new(-20, -workspace.Gravity * 0.5, 0))
```

### Buoyancy
```lua
local function addBuoyancy(part, waterHeight, buoyancyFactor)
    buoyancyFactor = buoyancyFactor or 1

    RunService.Heartbeat:Connect(function()
        local pos = part.Position
        local size = part.Size
        local bottom = pos.Y - size.Y/2
        local top = pos.Y + size.Y/2

        if top < waterHeight then
            -- Fully submerged
            local buoyancy = part:GetMass() * workspace.Gravity * buoyancyFactor
            applyForce(part, Vector3.new(0, buoyancy, 0))
        elseif bottom < waterHeight then
            -- Partially submerged
            local submergedRatio = (waterHeight - bottom) / size.Y
            local buoyancy = part:GetMass() * workspace.Gravity * buoyancyFactor * submergedRatio
            applyForce(part, Vector3.new(0, buoyancy, 0))
        end
    end)
end
```

### Magnetic Force
```lua
local function magneticForce(magnet, target, strength, falloff)
    falloff = falloff or 2  -- Inverse square

    RunService.Heartbeat:Connect(function()
        local direction = magnet.Position - target.Position
        local distance = direction.Magnitude

        if distance < 0.1 then return end

        local forceMagnitude = strength / (distance ^ falloff)
        local force = direction.Unit * forceMagnitude

        applyForce(target, force)
    end)
end
```
