---
name: vfx-effects
description: Implements visual effects including particle systems, camera effects, lighting, mesh effects, and UI animations. Use when creating combat VFX, environmental effects, feedback systems, or any visual polish.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Visual Effects (VFX)

## Quick Reference Links

**Official Documentation:**
- [Particle Emitters](https://create.roblox.com/docs/effects/particle-emitters) - Particle system guide
- [Beams](https://create.roblox.com/docs/effects/beams) - Beam effects
- [Trails](https://create.roblox.com/docs/effects/trails) - Motion trails
- [Lighting](https://create.roblox.com/docs/environment/lighting) - Light effects
- [ParticleEmitter API](https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter)
- [Beam API](https://create.roblox.com/docs/reference/engine/classes/Beam)
- [Trail API](https://create.roblox.com/docs/reference/engine/classes/Trail)
- [PointLight API](https://create.roblox.com/docs/reference/engine/classes/PointLight)
- [TweenService API](https://create.roblox.com/docs/reference/engine/classes/TweenService)
- [Debris API](https://create.roblox.com/docs/reference/engine/classes/Debris)

**Wiki References:**
- [ParticleEmitter (Wiki)](https://roblox.fandom.com/wiki/ParticleEmitter)
- [Beam (Wiki)](https://roblox.fandom.com/wiki/Beam)
- [Trail (Wiki)](https://roblox.fandom.com/wiki/Trail)
- [Visual Effects (Wiki)](https://roblox.fandom.com/wiki/Visual_effects)

---

When implementing VFX, use these patterns for impactful and performant effects.

## Particle Effects

### Anime Hit VFX
```lua
local function createHitEffect(position, direction, intensity)
    intensity = intensity or 1

    -- Impact flash
    local flash = Instance.new("Part")
    flash.Shape = Enum.PartType.Ball
    flash.Size = Vector3.new(0.1, 0.1, 0.1)
    flash.Position = position
    flash.Anchored = true
    flash.CanCollide = false
    flash.Material = Enum.Material.Neon
    flash.Color = Color3.new(1, 1, 1)
    flash.Parent = workspace.Effects

    -- Scale up and fade
    local tweenInfo = TweenInfo.new(0.15, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
    TweenService:Create(flash, tweenInfo, {
        Size = Vector3.new(3, 3, 3) * intensity,
        Transparency = 1
    }):Play()

    -- Radial lines (speedlines)
    local numLines = 8
    for i = 1, numLines do
        local angle = (i / numLines) * math.pi * 2
        local lineDir = Vector3.new(math.cos(angle), 0, math.sin(angle))

        local line = Instance.new("Part")
        line.Size = Vector3.new(0.1, 0.1, 2)
        line.CFrame = CFrame.lookAt(position, position + lineDir) * CFrame.new(0, 0, -1)
        line.Anchored = true
        line.CanCollide = false
        line.Material = Enum.Material.Neon
        line.Color = Color3.new(1, 0.9, 0.8)
        line.Parent = workspace.Effects

        TweenService:Create(line, TweenInfo.new(0.2), {
            Size = Vector3.new(0.05, 0.05, 5) * intensity,
            CFrame = line.CFrame * CFrame.new(0, 0, -3),
            Transparency = 1
        }):Play()

        Debris:AddItem(line, 0.3)
    end

    -- Screen shake
    shakeCamera(0.3, intensity * 5)

    Debris:AddItem(flash, 0.2)
end
```

### Slash Trail
```lua
local function createSlashTrail(weapon, duration)
    local attachment0 = weapon:FindFirstChild("TrailAttachment0")
    local attachment1 = weapon:FindFirstChild("TrailAttachment1")

    if not attachment0 or not attachment1 then
        -- Create attachments at blade ends
        attachment0 = Instance.new("Attachment")
        attachment0.Name = "TrailAttachment0"
        attachment0.Position = Vector3.new(0, 0, 2)  -- Tip
        attachment0.Parent = weapon

        attachment1 = Instance.new("Attachment")
        attachment1.Name = "TrailAttachment1"
        attachment1.Position = Vector3.new(0, 0, 0)  -- Base
        attachment1.Parent = weapon
    end

    local trail = Instance.new("Trail")
    trail.Attachment0 = attachment0
    trail.Attachment1 = attachment1
    trail.Lifetime = 0.3
    trail.MinLength = 0
    trail.FaceCamera = true
    trail.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.new(1, 1, 1)),
        ColorSequenceKeypoint.new(1, Color3.new(0.8, 0.8, 1))
    })
    trail.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0),
        NumberSequenceKeypoint.new(0.5, 0.3),
        NumberSequenceKeypoint.new(1, 1)
    })
    trail.WidthScale = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 1),
        NumberSequenceKeypoint.new(1, 0.2)
    })
    trail.Parent = weapon

    -- Disable after duration
    task.delay(duration, function()
        trail.Enabled = false
        Debris:AddItem(trail, trail.Lifetime)
    end)

    return trail
end
```

### Aura Effect
```lua
local function createAura(character, color, intensity)
    local hrp = character:FindFirstChild("HumanoidRootPart")
    if not hrp then return end

    local attachment = Instance.new("Attachment")
    attachment.Parent = hrp

    local particles = Instance.new("ParticleEmitter")
    particles.Color = ColorSequence.new(color)
    particles.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.5),
        NumberSequenceKeypoint.new(0.5, 1),
        NumberSequenceKeypoint.new(1, 0)
    })
    particles.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.5),
        NumberSequenceKeypoint.new(1, 1)
    })
    particles.Lifetime = NumberRange.new(0.5, 1)
    particles.Rate = 50 * intensity
    particles.Speed = NumberRange.new(2, 4)
    particles.SpreadAngle = Vector2.new(180, 180)
    particles.Acceleration = Vector3.new(0, 5, 0)
    particles.EmissionDirection = Enum.NormalId.Top
    particles.Parent = attachment

    -- Point light for glow
    local light = Instance.new("PointLight")
    light.Color = color
    light.Brightness = intensity
    light.Range = 10
    light.Parent = hrp

    return {
        stop = function()
            particles.Enabled = false
            TweenService:Create(light, TweenInfo.new(0.5), {Brightness = 0}):Play()
            Debris:AddItem(attachment, 1)
            Debris:AddItem(light, 0.5)
        end
    }
end
```

## Camera Effects

### Screen Shake
```lua
local ShakeModule = {}
local currentShake = Vector3.new()

function ShakeModule.shake(duration, magnitude, frequency)
    frequency = frequency or 20

    local startTime = os.clock()
    local conn
    conn = RunService.RenderStepped:Connect(function()
        local elapsed = os.clock() - startTime
        if elapsed > duration then
            currentShake = Vector3.new()
            conn:Disconnect()
            return
        end

        -- Decay over time
        local decay = 1 - (elapsed / duration)
        local shake = magnitude * decay

        -- Random offset
        currentShake = Vector3.new(
            (math.random() - 0.5) * 2 * shake,
            (math.random() - 0.5) * 2 * shake,
            0
        )
    end)
end

function ShakeModule.getOffset()
    return currentShake
end

-- Apply in camera update
RunService.RenderStepped:Connect(function()
    local offset = ShakeModule.getOffset()
    camera.CFrame = camera.CFrame * CFrame.new(offset)
end)
```

### Hit Stop (Frame Freeze)
```lua
local function hitStop(duration)
    duration = duration or 0.05

    -- Store original time scale
    local originalSpeed = 1

    -- Slow down animations
    for _, player in ipairs(Players:GetPlayers()) do
        local character = player.Character
        if character then
            local humanoid = character:FindFirstChildOfClass("Humanoid")
            if humanoid then
                local animator = humanoid:FindFirstChildOfClass("Animator")
                if animator then
                    for _, track in ipairs(animator:GetPlayingAnimationTracks()) do
                        track:AdjustSpeed(0.01)
                    end
                end
            end
        end
    end

    task.wait(duration)

    -- Restore
    for _, player in ipairs(Players:GetPlayers()) do
        local character = player.Character
        if character then
            local humanoid = character:FindFirstChildOfClass("Humanoid")
            if humanoid then
                local animator = humanoid:FindFirstChildOfClass("Animator")
                if animator then
                    for _, track in ipairs(animator:GetPlayingAnimationTracks()) do
                        track:AdjustSpeed(1)
                    end
                end
            end
        end
    end
end
```

### Zoom Punch Effect
```lua
local function zoomPunch(intensity, duration)
    intensity = intensity or 5
    duration = duration or 0.1

    local camera = workspace.CurrentCamera
    local originalFOV = camera.FieldOfView

    -- Quick zoom in
    TweenService:Create(camera, TweenInfo.new(duration * 0.3, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
        FieldOfView = originalFOV - intensity
    }):Play()

    task.wait(duration * 0.3)

    -- Slower return
    TweenService:Create(camera, TweenInfo.new(duration * 0.7, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
        FieldOfView = originalFOV
    }):Play()
end
```

## Lighting Effects

### Dynamic Muzzle Flash
```lua
local function muzzleFlash(attachment)
    -- Light
    local light = Instance.new("PointLight")
    light.Color = Color3.new(1, 0.9, 0.5)
    light.Brightness = 5
    light.Range = 15
    light.Parent = attachment

    -- Flash particle
    local flash = Instance.new("ParticleEmitter")
    flash.Texture = "rbxassetid://123456789"  -- Muzzle flash texture
    flash.Size = NumberSequence.new(1.5)
    flash.Lifetime = NumberRange.new(0.05)
    flash.Rate = 0
    flash.Speed = NumberRange.new(0)
    flash.Parent = attachment

    flash:Emit(1)

    -- Fade light
    TweenService:Create(light, TweenInfo.new(0.1), {Brightness = 0}):Play()

    Debris:AddItem(light, 0.15)
    Debris:AddItem(flash, 0.1)
end
```

### Lightning Flash
```lua
local function lightningFlash()
    local lighting = game:GetService("Lighting")
    local originalAmbient = lighting.Ambient

    -- Flash white
    lighting.Ambient = Color3.new(1, 1, 1)

    task.wait(0.05)
    lighting.Ambient = originalAmbient
    task.wait(0.1)
    lighting.Ambient = Color3.new(0.8, 0.8, 0.8)
    task.wait(0.05)
    lighting.Ambient = originalAmbient
end
```

## Mesh & Material Effects

### Dissolve Effect
```lua
local function dissolve(part, duration)
    -- Create a dissolve texture
    local surfaceGui = Instance.new("SurfaceGui")
    surfaceGui.Face = Enum.NormalId.Front
    surfaceGui.LightInfluence = 0

    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(1, 0, 1, 0)
    frame.BackgroundTransparency = 1
    frame.Parent = surfaceGui

    local gradient = Instance.new("UIGradient")
    gradient.Rotation = 90
    gradient.Parent = frame

    surfaceGui.Parent = part

    -- Animate gradient offset
    local startTime = os.clock()
    local conn
    conn = RunService.RenderStepped:Connect(function()
        local elapsed = os.clock() - startTime
        local t = elapsed / duration

        if t >= 1 then
            part:Destroy()
            conn:Disconnect()
            return
        end

        gradient.Offset = Vector2.new(0, t * 2 - 1)
        part.Transparency = t
    end)
end
```

### Outline Effect
```lua
local function addOutline(character, color, thickness)
    thickness = thickness or 0.05

    for _, part in ipairs(character:GetDescendants()) do
        if part:IsA("BasePart") and part.Name ~= "HumanoidRootPart" then
            local outline = part:Clone()
            outline.Name = "Outline"
            outline.Size = part.Size + Vector3.new(thickness, thickness, thickness)
            outline.Material = Enum.Material.SmoothPlastic
            outline.Color = color
            outline.CanCollide = false
            outline.Massless = true
            outline.Transparency = 0

            local weld = Instance.new("WeldConstraint")
            weld.Part0 = part
            weld.Part1 = outline
            weld.Parent = outline

            outline.Parent = part
        end
    end
end
```

## UI Visual Effects

### Damage Numbers
```lua
local function showDamageNumber(position, damage, isCrit)
    local billboardGui = Instance.new("BillboardGui")
    billboardGui.Size = UDim2.new(0, 100, 0, 50)
    billboardGui.StudsOffset = Vector3.new(0, 2, 0)
    billboardGui.Adornee = nil
    billboardGui.AlwaysOnTop = true

    local label = Instance.new("TextLabel")
    label.Size = UDim2.new(1, 0, 1, 0)
    label.BackgroundTransparency = 1
    label.Text = tostring(math.floor(damage))
    label.TextColor3 = isCrit and Color3.new(1, 0.8, 0) or Color3.new(1, 1, 1)
    label.TextStrokeTransparency = 0
    label.TextStrokeColor3 = Color3.new(0, 0, 0)
    label.TextScaled = true
    label.Font = Enum.Font.GothamBold
    label.Parent = billboardGui

    -- Position in world
    local part = Instance.new("Part")
    part.Anchored = true
    part.CanCollide = false
    part.Transparency = 1
    part.Size = Vector3.new(0.1, 0.1, 0.1)
    part.Position = position
    part.Parent = workspace.Effects

    billboardGui.Adornee = part
    billboardGui.Parent = part

    -- Animate: rise and fade
    local startY = position.Y
    local startTime = os.clock()

    local conn
    conn = RunService.RenderStepped:Connect(function()
        local elapsed = os.clock() - startTime
        local t = elapsed / 1

        if t >= 1 then
            part:Destroy()
            conn:Disconnect()
            return
        end

        -- Rise with easing
        local easeT = 1 - (1 - t) ^ 2
        part.Position = Vector3.new(position.X, startY + easeT * 3, position.Z)

        -- Fade out
        label.TextTransparency = t
        label.TextStrokeTransparency = t

        -- Scale pop for crits
        if isCrit and t < 0.2 then
            local scale = 1 + math.sin(t * 5 * math.pi) * 0.3
            label.TextSize = 24 * scale
        end
    end)
end
```

### Cooldown Sweep
```lua
local function createCooldownUI(button, cooldownDuration)
    local overlay = Instance.new("Frame")
    overlay.Name = "CooldownOverlay"
    overlay.Size = UDim2.new(1, 0, 1, 0)
    overlay.BackgroundColor3 = Color3.new(0, 0, 0)
    overlay.BackgroundTransparency = 0.5
    overlay.Parent = button

    local gradient = Instance.new("UIGradient")
    gradient.Rotation = -90
    gradient.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0),
        NumberSequenceKeypoint.new(0.5, 0),
        NumberSequenceKeypoint.new(0.501, 1),
        NumberSequenceKeypoint.new(1, 1)
    })
    gradient.Parent = overlay

    -- Animate
    local startTime = os.clock()
    local conn
    conn = RunService.RenderStepped:Connect(function()
        local elapsed = os.clock() - startTime
        local t = elapsed / cooldownDuration

        if t >= 1 then
            overlay:Destroy()
            conn:Disconnect()
            return
        end

        -- Rotate gradient to create sweep effect
        gradient.Rotation = -90 + (t * 360)
    end)
end
```

## Fire & Flame Effects

### Realistic Fire (Multi-Emitter Approach)
Use multiple ParticleEmitters for realistic fire: fire core, smoke, and embers.

```lua
local function createFireEffect(parent)
    local attachment = Instance.new("Attachment")
    attachment.Parent = parent

    -- Fire core (bright flames)
    local fire = Instance.new("ParticleEmitter")
    fire.Name = "FireCore"
    fire.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 255, 200)),    -- White hot center
        ColorSequenceKeypoint.new(0.2, Color3.fromRGB(255, 200, 50)),   -- Yellow
        ColorSequenceKeypoint.new(0.5, Color3.fromRGB(255, 100, 0)),    -- Orange
        ColorSequenceKeypoint.new(0.8, Color3.fromRGB(200, 30, 0)),     -- Red
        ColorSequenceKeypoint.new(1, Color3.fromRGB(50, 0, 0)),         -- Dark red (cools)
    })
    fire.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 2),
        NumberSequenceKeypoint.new(0.3, 3),
        NumberSequenceKeypoint.new(1, 0),
    })
    fire.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.3),
        NumberSequenceKeypoint.new(0.5, 0.5),
        NumberSequenceKeypoint.new(1, 1),
    })
    fire.Lifetime = NumberRange.new(0.3, 0.6)
    fire.Rate = 80
    fire.Speed = NumberRange.new(8, 12)
    fire.SpreadAngle = Vector2.new(15, 15)
    fire.Acceleration = Vector3.new(0, 8, 0)  -- Fire rises
    fire.LightEmission = 1
    fire.LightInfluence = 0
    fire.Parent = attachment

    -- Smoke (darker, slower, rises higher)
    local smoke = Instance.new("ParticleEmitter")
    smoke.Name = "Smoke"
    smoke.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(100, 60, 30)),
        ColorSequenceKeypoint.new(0.5, Color3.fromRGB(60, 60, 60)),
        ColorSequenceKeypoint.new(1, Color3.fromRGB(30, 30, 30)),
    })
    smoke.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 1),
        NumberSequenceKeypoint.new(0.5, 3),
        NumberSequenceKeypoint.new(1, 5),
    })
    smoke.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.6),
        NumberSequenceKeypoint.new(0.5, 0.8),
        NumberSequenceKeypoint.new(1, 1),
    })
    smoke.Lifetime = NumberRange.new(1, 2)
    smoke.Rate = 30
    smoke.Speed = NumberRange.new(3, 6)
    smoke.SpreadAngle = Vector2.new(20, 20)
    smoke.Acceleration = Vector3.new(0, 5, 0)
    smoke.RotSpeed = NumberRange.new(-30, 30)
    smoke.Rotation = NumberRange.new(0, 360)
    smoke.LightInfluence = 0.5
    smoke.Parent = attachment

    -- Embers (small bright sparks)
    local embers = Instance.new("ParticleEmitter")
    embers.Name = "Embers"
    embers.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 200, 50)),
        ColorSequenceKeypoint.new(0.5, Color3.fromRGB(255, 100, 0)),
        ColorSequenceKeypoint.new(1, Color3.fromRGB(100, 30, 0)),
    })
    embers.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.3),
        NumberSequenceKeypoint.new(1, 0),
    })
    embers.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0),
        NumberSequenceKeypoint.new(0.8, 0),
        NumberSequenceKeypoint.new(1, 1),
    })
    embers.Lifetime = NumberRange.new(0.5, 1.5)
    embers.Rate = 20
    embers.Speed = NumberRange.new(5, 10)
    embers.SpreadAngle = Vector2.new(30, 30)
    embers.Acceleration = Vector3.new(0, -3, 0)  -- Gravity pulls embers down
    embers.LightEmission = 1
    embers.Parent = attachment

    -- Point light for illumination
    local light = Instance.new("PointLight")
    light.Color = Color3.fromRGB(255, 150, 50)
    light.Brightness = 2
    light.Range = 15
    light.Parent = parent

    return {
        stop = function()
            fire.Enabled = false
            smoke.Enabled = false
            embers.Enabled = false
            TweenService:Create(light, TweenInfo.new(0.5), {Brightness = 0}):Play()
            Debris:AddItem(attachment, 2)
            Debris:AddItem(light, 0.5)
        end
    }
end
```

### Quick Fire Breath (Attach to Dragon Snout)
Simplified fire breath using just a ParticleEmitter. Ideal for decorative dragons.

```lua
local function addFireBreath(snoutPart, scale)
    scale = scale or 1

    -- Attachment at snout tip
    local att = Instance.new("Attachment")
    att.Position = Vector3.new(0, 0, -snoutPart.Size.Z / 2 - 0.5)
    att.Parent = snoutPart

    -- Fire particles
    local fire = Instance.new("ParticleEmitter")
    fire.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 220, 50)),    -- Yellow hot
        ColorSequenceKeypoint.new(0.4, Color3.fromRGB(255, 100, 0)),   -- Orange
        ColorSequenceKeypoint.new(1, Color3.fromRGB(150, 0, 0)),       -- Red fade
    })
    fire.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 1 * scale),
        NumberSequenceKeypoint.new(0.3, 2 * scale),
        NumberSequenceKeypoint.new(1, 0.5 * scale),
    })
    fire.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.3),
        NumberSequenceKeypoint.new(0.7, 0.6),
        NumberSequenceKeypoint.new(1, 1),
    })
    fire.Lifetime = NumberRange.new(0.3, 0.5)
    fire.Rate = 60
    fire.Speed = NumberRange.new(20 * scale, 30 * scale)
    fire.SpreadAngle = Vector2.new(15, 15)
    fire.Acceleration = Vector3.new(0, 5, 0)  -- Slight rise
    fire.LightEmission = 1
    fire.LightInfluence = 0
    fire.Parent = att

    -- Glow light
    local light = Instance.new("PointLight")
    light.Color = Color3.fromRGB(255, 150, 50)
    light.Brightness = 2
    light.Range = 15 * scale
    light.Parent = snoutPart

    return {
        stop = function()
            fire.Enabled = false
            light.Enabled = false
        end,
        start = function()
            fire.Enabled = true
            light.Enabled = true
        end
    }
end

-- Usage with dragon:
-- local dragon, snout = createDragon(position, BrickColor.new("Bright red"), 1, parent)
-- local fireBreath = addFireBreath(snout, 1)
```

### Fire Breath / Flamethrower
Directional fire stream with aligned particles.

```lua
local function createFireBreath(mouthAttachment, direction, duration)
    duration = duration or 2

    -- Create emitter attachment aligned with direction
    local emitter = Instance.new("Attachment")
    emitter.CFrame = CFrame.lookAt(Vector3.new(), direction)
    emitter.Parent = mouthAttachment.Parent

    -- Main flame stream
    local flame = Instance.new("ParticleEmitter")
    flame.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 255, 200)),
        ColorSequenceKeypoint.new(0.3, Color3.fromRGB(255, 180, 50)),
        ColorSequenceKeypoint.new(0.6, Color3.fromRGB(255, 80, 0)),
        ColorSequenceKeypoint.new(1, Color3.fromRGB(100, 20, 0)),
    })
    flame.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 1),
        NumberSequenceKeypoint.new(0.2, 3),
        NumberSequenceKeypoint.new(0.5, 4),
        NumberSequenceKeypoint.new(1, 2),
    })
    flame.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.2),
        NumberSequenceKeypoint.new(0.6, 0.5),
        NumberSequenceKeypoint.new(1, 1),
    })
    flame.Lifetime = NumberRange.new(0.4, 0.8)
    flame.Rate = 100
    flame.Speed = NumberRange.new(40, 60)
    flame.SpreadAngle = Vector2.new(10, 10)
    flame.Acceleration = Vector3.new(0, 10, 0)  -- Slight rise
    flame.LightEmission = 1
    flame.LightInfluence = 0
    flame.EmissionDirection = Enum.NormalId.Front
    flame.Parent = emitter

    -- Light
    local light = Instance.new("PointLight")
    light.Color = Color3.fromRGB(255, 150, 50)
    light.Brightness = 3
    light.Range = 25
    light.Parent = mouthAttachment.Parent

    -- Flickering light
    local flickerConn
    flickerConn = RunService.Heartbeat:Connect(function()
        light.Brightness = 2.5 + math.random() * 1
    end)

    -- Stop after duration
    task.delay(duration, function()
        flame.Enabled = false
        flickerConn:Disconnect()
        TweenService:Create(light, TweenInfo.new(0.3), {Brightness = 0}):Play()
        Debris:AddItem(emitter, 1)
        Debris:AddItem(light, 0.5)
    end)

    return emitter
end
```

### Fireball Projectile
Projectile with fire trail that explodes on impact.

```lua
local function createFireball(startPos, direction, speed, onHit)
    speed = speed or 50

    -- Fireball core
    local fireball = Instance.new("Part")
    fireball.Shape = Enum.PartType.Ball
    fireball.Size = Vector3.new(2, 2, 2)
    fireball.Position = startPos
    fireball.Anchored = false
    fireball.CanCollide = false
    fireball.Material = Enum.Material.Neon
    fireball.Color = Color3.fromRGB(255, 150, 0)
    fireball.Parent = workspace.Effects

    -- Fire particles on fireball
    local attachment = Instance.new("Attachment")
    attachment.Parent = fireball

    local fireParticles = Instance.new("ParticleEmitter")
    fireParticles.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 255, 200)),
        ColorSequenceKeypoint.new(0.3, Color3.fromRGB(255, 150, 0)),
        ColorSequenceKeypoint.new(1, Color3.fromRGB(200, 50, 0)),
    })
    fireParticles.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 1.5),
        NumberSequenceKeypoint.new(0.5, 2),
        NumberSequenceKeypoint.new(1, 0),
    })
    fireParticles.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.3),
        NumberSequenceKeypoint.new(1, 1),
    })
    fireParticles.Lifetime = NumberRange.new(0.2, 0.4)
    fireParticles.Rate = 60
    fireParticles.Speed = NumberRange.new(2, 5)
    fireParticles.SpreadAngle = Vector2.new(180, 180)
    fireParticles.LightEmission = 1
    fireParticles.Parent = attachment

    -- Fire trail
    local trail = Instance.new("Trail")
    local a0 = Instance.new("Attachment")
    local a1 = Instance.new("Attachment")
    a0.Position = Vector3.new(0, 0.5, 0)
    a1.Position = Vector3.new(0, -0.5, 0)
    a0.Parent = fireball
    a1.Parent = fireball
    trail.Attachment0 = a0
    trail.Attachment1 = a1
    trail.Lifetime = 0.3
    trail.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 200, 50)),
        ColorSequenceKeypoint.new(0.5, Color3.fromRGB(255, 100, 0)),
        ColorSequenceKeypoint.new(1, Color3.fromRGB(150, 30, 0)),
    })
    trail.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.3),
        NumberSequenceKeypoint.new(1, 1),
    })
    trail.WidthScale = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 1),
        NumberSequenceKeypoint.new(1, 0.2),
    })
    trail.LightEmission = 1
    trail.Parent = fireball

    -- Light
    local light = Instance.new("PointLight")
    light.Color = Color3.fromRGB(255, 150, 50)
    light.Brightness = 2
    light.Range = 15
    light.Parent = fireball

    -- Velocity
    local velocity = Instance.new("BodyVelocity")
    velocity.Velocity = direction.Unit * speed
    velocity.MaxForce = Vector3.new(math.huge, math.huge, math.huge)
    velocity.Parent = fireball

    -- Collision detection
    local touched = false
    fireball.Touched:Connect(function(hit)
        if touched then return end
        if hit:IsDescendantOf(workspace.Effects) then return end
        touched = true

        local hitPos = fireball.Position
        fireball:Destroy()

        if onHit then
            onHit(hitPos, hit)
        end
    end)

    -- Timeout
    Debris:AddItem(fireball, 5)

    return fireball
end
```

### Explosion Effect (Fire/Impact)
Multi-layered explosion with flash, fire, smoke, debris, and ground fire.

```lua
local function createExplosion(position, radius, options)
    options = options or {}
    radius = radius or 8
    local damage = options.damage or 50
    local showGroundFire = options.groundFire ~= false

    -- Explosion flash (immediate)
    local flash = Instance.new("Part")
    flash.Shape = Enum.PartType.Ball
    flash.Size = Vector3.new(1, 1, 1)
    flash.Position = position
    flash.Anchored = true
    flash.CanCollide = false
    flash.Material = Enum.Material.Neon
    flash.Color = Color3.fromRGB(255, 255, 200)
    flash.Parent = workspace.Effects

    TweenService:Create(flash, TweenInfo.new(0.15, Enum.EasingStyle.Quad), {
        Size = Vector3.new(radius, radius, radius),
        Transparency = 1
    }):Play()
    Debris:AddItem(flash, 0.2)

    -- Explosion particles attachment
    local explosionPart = Instance.new("Part")
    explosionPart.Position = position
    explosionPart.Anchored = true
    explosionPart.CanCollide = false
    explosionPart.Transparency = 1
    explosionPart.Parent = workspace.Effects

    local attachment = Instance.new("Attachment")
    attachment.Parent = explosionPart

    -- Fire burst (outward)
    local fireBurst = Instance.new("ParticleEmitter")
    fireBurst.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 255, 150)),
        ColorSequenceKeypoint.new(0.3, Color3.fromRGB(255, 150, 50)),
        ColorSequenceKeypoint.new(0.7, Color3.fromRGB(200, 50, 0)),
        ColorSequenceKeypoint.new(1, Color3.fromRGB(50, 10, 0)),
    })
    fireBurst.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 3),
        NumberSequenceKeypoint.new(0.3, radius * 0.7),
        NumberSequenceKeypoint.new(1, 0),
    })
    fireBurst.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.2),
        NumberSequenceKeypoint.new(0.5, 0.5),
        NumberSequenceKeypoint.new(1, 1),
    })
    fireBurst.Lifetime = NumberRange.new(0.5, 1)
    fireBurst.Rate = 0
    fireBurst.Speed = NumberRange.new(radius * 2, radius * 4)
    fireBurst.SpreadAngle = Vector2.new(180, 180)
    fireBurst.Acceleration = Vector3.new(0, -20, 0)
    fireBurst.LightEmission = 1
    fireBurst.Parent = attachment
    fireBurst:Emit(40)

    -- Smoke cloud (rises)
    local smokeCloud = Instance.new("ParticleEmitter")
    smokeCloud.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(80, 50, 30)),
        ColorSequenceKeypoint.new(0.5, Color3.fromRGB(50, 50, 50)),
        ColorSequenceKeypoint.new(1, Color3.fromRGB(30, 30, 30)),
    })
    smokeCloud.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 2),
        NumberSequenceKeypoint.new(0.5, radius * 0.8),
        NumberSequenceKeypoint.new(1, radius * 1.2),
    })
    smokeCloud.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.4),
        NumberSequenceKeypoint.new(0.5, 0.7),
        NumberSequenceKeypoint.new(1, 1),
    })
    smokeCloud.Lifetime = NumberRange.new(2, 4)
    smokeCloud.Rate = 0
    smokeCloud.Speed = NumberRange.new(5, 15)
    smokeCloud.SpreadAngle = Vector2.new(60, 60)
    smokeCloud.Acceleration = Vector3.new(0, 10, 0)
    smokeCloud.RotSpeed = NumberRange.new(-20, 20)
    smokeCloud.Rotation = NumberRange.new(0, 360)
    smokeCloud.EmissionDirection = Enum.NormalId.Top
    smokeCloud.Parent = attachment
    smokeCloud:Emit(20)

    -- Debris/sparks (outward and down)
    local debris = Instance.new("ParticleEmitter")
    debris.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 200, 100)),
        ColorSequenceKeypoint.new(0.5, Color3.fromRGB(200, 100, 50)),
        ColorSequenceKeypoint.new(1, Color3.fromRGB(100, 50, 20)),
    })
    debris.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.5),
        NumberSequenceKeypoint.new(1, 0.1),
    })
    debris.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0),
        NumberSequenceKeypoint.new(0.8, 0),
        NumberSequenceKeypoint.new(1, 1),
    })
    debris.Lifetime = NumberRange.new(1, 2)
    debris.Rate = 0
    debris.Speed = NumberRange.new(radius * 3, radius * 6)
    debris.SpreadAngle = Vector2.new(180, 180)
    debris.Acceleration = Vector3.new(0, -50, 0)  -- Gravity
    debris.LightEmission = 0.8
    debris.Parent = attachment
    debris:Emit(30)

    -- Explosion light
    local light = Instance.new("PointLight")
    light.Color = Color3.fromRGB(255, 150, 50)
    light.Brightness = 5
    light.Range = radius * 3
    light.Parent = explosionPart
    TweenService:Create(light, TweenInfo.new(0.5), {Brightness = 0}):Play()

    -- Ground fire (persistent burning)
    if showGroundFire then
        local groundFire = Instance.new("Part")
        groundFire.Position = position - Vector3.new(0, 1, 0)
        groundFire.Size = Vector3.new(radius, 0.5, radius)
        groundFire.Anchored = true
        groundFire.CanCollide = false
        groundFire.Transparency = 1
        groundFire.Parent = workspace.Effects

        local groundAttachment = Instance.new("Attachment")
        groundAttachment.Parent = groundFire

        local groundFlames = Instance.new("ParticleEmitter")
        groundFlames.Color = ColorSequence.new({
            ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 200, 50)),
            ColorSequenceKeypoint.new(0.5, Color3.fromRGB(255, 100, 0)),
            ColorSequenceKeypoint.new(1, Color3.fromRGB(100, 20, 0)),
        })
        groundFlames.Size = NumberSequence.new({
            NumberSequenceKeypoint.new(0, 1),
            NumberSequenceKeypoint.new(0.5, 2),
            NumberSequenceKeypoint.new(1, 0),
        })
        groundFlames.Transparency = NumberSequence.new({
            NumberSequenceKeypoint.new(0, 0.4),
            NumberSequenceKeypoint.new(1, 1),
        })
        groundFlames.Lifetime = NumberRange.new(0.3, 0.6)
        groundFlames.Rate = 40
        groundFlames.Speed = NumberRange.new(3, 6)
        groundFlames.SpreadAngle = Vector2.new(30, 30)
        groundFlames.Acceleration = Vector3.new(0, 8, 0)
        groundFlames.LightEmission = 1
        groundFlames.Parent = groundAttachment

        -- Fade out ground fire
        task.delay(2, function()
            groundFlames.Enabled = false
            Debris:AddItem(groundFire, 1)
        end)
    end

    Debris:AddItem(explosionPart, 5)

    -- Screen shake
    shakeCamera(0.5, radius * 0.5)
end
```

### Fire Color Palettes

```lua
-- Standard fire (orange/yellow)
local FIRE_STANDARD = {
    ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 255, 200)),    -- White hot
    ColorSequenceKeypoint.new(0.2, Color3.fromRGB(255, 200, 50)),   -- Yellow
    ColorSequenceKeypoint.new(0.5, Color3.fromRGB(255, 100, 0)),    -- Orange
    ColorSequenceKeypoint.new(0.8, Color3.fromRGB(200, 30, 0)),     -- Red
    ColorSequenceKeypoint.new(1, Color3.fromRGB(50, 0, 0)),         -- Dark
}

-- Blue fire (hotter)
local FIRE_BLUE = {
    ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 255, 255)),    -- White
    ColorSequenceKeypoint.new(0.2, Color3.fromRGB(200, 220, 255)),  -- Light blue
    ColorSequenceKeypoint.new(0.5, Color3.fromRGB(100, 150, 255)),  -- Blue
    ColorSequenceKeypoint.new(0.8, Color3.fromRGB(50, 80, 200)),    -- Deep blue
    ColorSequenceKeypoint.new(1, Color3.fromRGB(20, 30, 80)),       -- Dark blue
}

-- Green fire (magical/poison)
local FIRE_GREEN = {
    ColorSequenceKeypoint.new(0, Color3.fromRGB(200, 255, 200)),    -- Light green
    ColorSequenceKeypoint.new(0.3, Color3.fromRGB(100, 255, 100)),  -- Bright green
    ColorSequenceKeypoint.new(0.6, Color3.fromRGB(50, 200, 50)),    -- Green
    ColorSequenceKeypoint.new(1, Color3.fromRGB(20, 80, 20)),       -- Dark green
}

-- Purple fire (void/dark magic)
local FIRE_PURPLE = {
    ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 200, 255)),    -- Light purple
    ColorSequenceKeypoint.new(0.3, Color3.fromRGB(200, 100, 255)),  -- Bright purple
    ColorSequenceKeypoint.new(0.6, Color3.fromRGB(150, 50, 200)),   -- Purple
    ColorSequenceKeypoint.new(1, Color3.fromRGB(50, 20, 80)),       -- Dark purple
}
```

## Advanced VFX

### Beam Weapon
```lua
local function createBeam(startAttachment, endPosition, duration)
    local endPart = Instance.new("Part")
    endPart.Anchored = true
    endPart.CanCollide = false
    endPart.Transparency = 1
    endPart.Size = Vector3.new(0.1, 0.1, 0.1)
    endPart.Position = endPosition
    endPart.Parent = workspace.Effects

    local endAttachment = Instance.new("Attachment")
    endAttachment.Parent = endPart

    local beam = Instance.new("Beam")
    beam.Attachment0 = startAttachment
    beam.Attachment1 = endAttachment
    beam.Width0 = 0.5
    beam.Width1 = 0.3
    beam.FaceCamera = true
    beam.Color = ColorSequence.new(Color3.new(1, 0, 0))
    beam.Transparency = NumberSequence.new(0)
    beam.LightEmission = 1
    beam.LightInfluence = 0
    beam.TextureSpeed = 5
    beam.Parent = startAttachment

    -- Fade out
    task.delay(duration * 0.7, function()
        TweenService:Create(beam, TweenInfo.new(duration * 0.3), {
            Transparency = NumberSequence.new(1)
        }):Play()
    end)

    Debris:AddItem(endPart, duration)
    Debris:AddItem(beam, duration)

    return beam
end
```

### Lightning Chain
```lua
local function createLightningChain(startPos, endPos, segments)
    segments = segments or 8

    local parts = {}
    local direction = endPos - startPos
    local segmentLength = direction.Magnitude / segments

    for i = 1, segments do
        local t1 = (i - 1) / segments
        local t2 = i / segments

        local p1 = startPos + direction * t1
        local p2 = startPos + direction * t2

        -- Add random offset (except for endpoints)
        if i > 1 then
            local jitter = segmentLength * 0.5
            p1 = p1 + Vector3.new(
                (math.random() - 0.5) * jitter,
                (math.random() - 0.5) * jitter,
                (math.random() - 0.5) * jitter
            )
        end

        local segment = Instance.new("Part")
        segment.Anchored = true
        segment.CanCollide = false
        segment.Material = Enum.Material.Neon
        segment.Color = Color3.new(0.7, 0.8, 1)

        local dist = (p2 - p1).Magnitude
        segment.Size = Vector3.new(0.1, 0.1, dist)
        segment.CFrame = CFrame.lookAt((p1 + p2) / 2, p2)
        segment.Parent = workspace.Effects

        table.insert(parts, segment)
    end

    -- Quick flash and fade
    task.delay(0.05, function()
        for _, part in ipairs(parts) do
            TweenService:Create(part, TweenInfo.new(0.1), {Transparency = 1}):Play()
        end
    end)

    task.delay(0.15, function()
        for _, part in ipairs(parts) do
            part:Destroy()
        end
    end)
end
```
