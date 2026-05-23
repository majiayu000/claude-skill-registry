---
name: vehicle-physics
description: Implements vehicle physics systems in Roblox including cars, helicopters, boats, planes, motorcycles, and trains. Use when building any driveable/flyable vehicle with realistic physics using constraints.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Vehicle Physics Implementation

When implementing vehicle physics, follow these Roblox-specific patterns and constraints.

## Car Physics

### Basic Setup
```lua
-- Use VehicleSeat for driver control
-- Connect wheels with HingeConstraint (ActuatorType = Motor)
-- Use SpringConstraint for suspension
-- CylindricalConstraint for steering column

local function setupWheel(chassis, wheelPart, isSteer, isDrive)
    local attachment0 = Instance.new("Attachment", chassis)
    local attachment1 = Instance.new("Attachment", wheelPart)

    -- Suspension spring
    local spring = Instance.new("SpringConstraint")
    spring.Attachment0 = attachment0
    spring.Attachment1 = attachment1
    spring.Stiffness = 5000  -- Adjust for vehicle weight
    spring.Damping = 500
    spring.FreeLength = 1
    spring.Parent = chassis

    -- Wheel rotation
    local hinge = Instance.new("HingeConstraint")
    hinge.ActuatorType = Enum.ActuatorType.Motor
    hinge.MotorMaxTorque = isDrive and 10000 or 0
    hinge.Parent = wheelPart
end
```

### Critical Implementation Details
1. **Network Ownership**: Always `SetNetworkOwner(driver)` when player enters vehicle
2. **Friction**: Set `wheelPart.CustomPhysicalProperties` with specific friction values
3. **Anti-Roll**: Use `RodConstraint` between left/right suspension attachments
4. **Steering Ackermann**: Inner wheel turns sharper than outer: `innerAngle = atan(L / (R - W/2))`

### Gear System
```lua
local gearRatios = {3.5, 2.5, 1.8, 1.4, 1.0, 0.8}  -- 6 gears
local finalDrive = 3.7
local maxRPM = 7000

local function calculateWheelTorque(throttle, currentGear, engineRPM)
    local torqueCurve = 1 - ((engineRPM - 4500) / maxRPM)^2  -- Peak at 4500 RPM
    return throttle * baseTorque * torqueCurve * gearRatios[currentGear] * finalDrive
end
```

## Helicopter Physics

### Lift and Control
```lua
-- Main rotor provides lift proportional to collective (throttle)
-- Cyclic control tilts the rotor disc for directional movement
-- Tail rotor counters main rotor torque

local function updateHelicopter(heli, collective, cyclicPitch, cyclicRoll, pedal)
    local rotorRPM = heli:GetAttribute("RotorRPM")
    local airDensity = 1.225  -- kg/m³ at sea level

    -- Lift = 0.5 * rho * A * Cl * V²
    local liftForce = collective * rotorRPM / 500 * heli.Mass * workspace.Gravity

    -- Apply forces
    local bodyForce = heli:FindFirstChild("LiftForce") or Instance.new("VectorForce", heli)
    bodyForce.Force = Vector3.new(
        cyclicRoll * liftForce * 0.3,
        liftForce,
        cyclicPitch * liftForce * 0.3
    )

    -- Anti-torque from tail rotor
    local tailTorque = pedal * rotorRPM * 10
    local bodyTorque = heli:FindFirstChild("YawTorque") or Instance.new("Torque", heli)
    bodyTorque.Torque = Vector3.new(0, tailTorque, 0)
end
```

### Ground Effect
```lua
-- Increase lift when near ground (within 1 rotor diameter)
local function groundEffect(altitude, rotorDiameter)
    if altitude < rotorDiameter then
        return 1 + (1 - altitude/rotorDiameter) * 0.25  -- Up to 25% lift bonus
    end
    return 1
end
```

## Boat Physics

### Buoyancy Implementation
```lua
-- Sample multiple points below waterline
local buoyancyPoints = {
    Vector3.new(2, 0, 3),   -- Front-right
    Vector3.new(-2, 0, 3),  -- Front-left
    Vector3.new(2, 0, -3),  -- Back-right
    Vector3.new(-2, 0, -3), -- Back-left
    Vector3.new(0, 0, 0),   -- Center
}

local function calculateBuoyancy(hull, waterHeight)
    local totalForce = Vector3.new(0, 0, 0)

    for _, localPos in ipairs(buoyancyPoints) do
        local worldPos = hull.CFrame:PointToWorldSpace(localPos)
        local depth = waterHeight - worldPos.Y

        if depth > 0 then
            -- Buoyancy force proportional to submerged depth
            local force = Vector3.new(0, depth * 1000 * hull.Mass / #buoyancyPoints, 0)
            totalForce = totalForce + force
        end
    end

    return totalForce
end
```

### Wave Response
```lua
-- Tilt hull based on wave surface normal
local function getWaveHeight(x, z, time)
    local wave1 = math.sin(x * 0.1 + time) * 2
    local wave2 = math.sin(z * 0.15 + time * 1.3) * 1.5
    return wave1 + wave2
end
```

## Airplane Physics

### Lift and Drag
```lua
local wingArea = 20  -- m²
local dragCoefficient = 0.02
local liftCoefficient = 0.5

local function calculateAeroForces(velocity, angleOfAttack)
    local speed = velocity.Magnitude
    local dynamicPressure = 0.5 * 1.225 * speed^2

    -- Lift perpendicular to velocity
    local Cl = liftCoefficient * math.sin(2 * angleOfAttack)
    local lift = dynamicPressure * wingArea * Cl

    -- Stall: lift drops sharply past critical angle
    if math.abs(angleOfAttack) > math.rad(15) then
        lift = lift * (1 - (math.abs(angleOfAttack) - math.rad(15)) / math.rad(10))
    end

    -- Drag opposes velocity
    local Cd = dragCoefficient + Cl^2 / (math.pi * 8)  -- Induced drag
    local drag = dynamicPressure * wingArea * Cd

    return lift, drag
end
```

## Motorcycle/Bike Balance

```lua
-- Self-stabilization using BodyGyro with low torque
local function setupBikeBalance(bike)
    local gyro = Instance.new("BodyGyro")
    gyro.MaxTorque = Vector3.new(5000, 0, 5000)  -- Only roll and pitch
    gyro.P = 1000
    gyro.D = 100
    gyro.Parent = bike.PrimaryPart

    -- Counter-steering: turn bars opposite to initiate lean
    local function handleSteering(turnInput, speed)
        if speed > 10 then
            -- At speed, steering input causes lean
            local targetLean = turnInput * math.min(speed / 50, 1) * math.rad(45)
            gyro.CFrame = CFrame.Angles(0, 0, targetLean)
        end
    end
end
```

## Train/Rail Following

```lua
-- Constrain train to spline path
local function followRail(train, spline, distance)
    local position = spline:GetPositionAtDistance(distance)
    local tangent = spline:GetTangentAtDistance(distance)

    local alignPos = train:FindFirstChild("RailAlign") or Instance.new("AlignPosition", train.PrimaryPart)
    alignPos.Position = position
    alignPos.RigidityEnabled = true

    local alignOri = train:FindFirstChild("RailOrient") or Instance.new("AlignOrientation", train.PrimaryPart)
    alignOri.CFrame = CFrame.lookAt(position, position + tangent)
end
```

## Common Patterns

### Network Ownership Transfer
```lua
vehicleSeat:GetPropertyChangedSignal("Occupant"):Connect(function()
    local humanoid = vehicleSeat.Occupant
    if humanoid then
        local player = game.Players:GetPlayerFromCharacter(humanoid.Parent)
        if player then
            for _, part in ipairs(vehicle:GetDescendants()) do
                if part:IsA("BasePart") and not part.Anchored then
                    part:SetNetworkOwner(player)
                end
            end
        end
    else
        -- Return to server ownership
        for _, part in ipairs(vehicle:GetDescendants()) do
            if part:IsA("BasePart") then
                part:SetNetworkOwner(nil)
            end
        end
    end
end)
```

### Speedometer/Tachometer
```lua
local function getVehicleSpeed(chassis)
    return chassis.AssemblyLinearVelocity.Magnitude * 3.6  -- Convert to km/h
end

local function getRPMFromWheel(hingeConstraint)
    -- Track angle change over time
    local currentAngle = hingeConstraint.CurrentAngle
    local deltaAngle = currentAngle - lastAngle
    local rpm = (deltaAngle / (2 * math.pi)) * 60 / deltaTime
    return math.abs(rpm)
end
```
