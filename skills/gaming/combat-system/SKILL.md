---
name: combat-system
description: Implements combat systems including hitboxes, damage calculation, stun mechanics, melee combat, ranged weapons, and ability systems. Use when building fighting games, shooters, RPG combat, or any game with player-vs-player or player-vs-NPC combat.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Combat System Implementation

When implementing combat systems, follow these Roblox-specific patterns.

## Hitbox Systems

### Battlegrounds-Style Hitbox (GetPartBoundsInBox)
```lua
-- Most common method for melee games like The Strongest Battlegrounds
local function createHitbox(cframe, size, ignoreList, callback)
    local params = OverlapParams.new()
    params.FilterDescendantsInstances = ignoreList
    params.FilterType = Enum.RaycastFilterType.Exclude

    local parts = workspace:GetPartBoundsInBox(cframe, size, params)

    local hitCharacters = {}
    for _, part in ipairs(parts) do
        local character = part.Parent
        local humanoid = character:FindFirstChildOfClass("Humanoid")

        if humanoid and not hitCharacters[character] then
            hitCharacters[character] = true
            callback(humanoid, part)
        end
    end

    return hitCharacters
end

-- Usage with lingering hitbox (active for multiple frames)
local function meleeAttack(attacker, damage, knockback)
    local hitTargets = {}
    local duration = 0.2  -- Hitbox active for 200ms
    local startTime = os.clock()

    while os.clock() - startTime < duration do
        local hitboxCFrame = attacker.HumanoidRootPart.CFrame * CFrame.new(0, 0, -3)
        local hitboxSize = Vector3.new(4, 6, 4)

        createHitbox(hitboxCFrame, hitboxSize, {attacker}, function(humanoid, hitPart)
            if not hitTargets[humanoid.Parent] then
                hitTargets[humanoid.Parent] = true
                applyDamage(humanoid, damage, knockback, attacker)
            end
        end)

        task.wait()
    end
end
```

### Client-Predicted Hitbox (Validate on Server)
```lua
-- Client: Perform hit detection locally for responsiveness
local function clientHitDetection(attackData)
    local hitbox = createHitbox(attackData.cframe, attackData.size, {localPlayer.Character})

    for character, _ in pairs(hitbox) do
        -- Send hit claim to server
        CombatRemote:FireServer("HitClaim", {
            targetId = character:GetAttribute("EntityId"),
            attackId = attackData.id,
            timestamp = workspace:GetServerTimeNow()
        })

        -- Play hit effect immediately (client prediction)
        playHitEffect(character)
    end
end

-- Server: Validate hit claims
local function validateHit(player, data)
    local attacker = player.Character
    local target = getEntityById(data.targetId)

    if not attacker or not target then return false end

    -- Check distance (with tolerance for latency)
    local distance = (attacker.HumanoidRootPart.Position - target.HumanoidRootPart.Position).Magnitude
    if distance > MAX_ATTACK_RANGE * 1.5 then return false end

    -- Check attack is valid (cooldown, state)
    if not canAttack(attacker, data.attackId) then return false end

    -- Check target is damageable
    if not canBeDamaged(target) then return false end

    return true
end
```

### Capsule Hitbox (For Character Shapes)
```lua
-- Multiple overlapping spheres for better character detection
local function capsuleOverlap(startPos, endPos, radius, ignoreList)
    local params = OverlapParams.new()
    params.FilterDescendantsInstances = ignoreList
    params.FilterType = Enum.RaycastFilterType.Exclude

    local hits = {}
    local segments = 5
    local direction = (endPos - startPos)

    for i = 0, segments do
        local t = i / segments
        local pos = startPos + direction * t
        local parts = workspace:GetPartBoundsInRadius(pos, radius, params)

        for _, part in ipairs(parts) do
            hits[part] = true
        end
    end

    return hits
end
```

## Damage Systems

### Damage Calculation
```lua
local DamageSystem = {}

function DamageSystem.calculateDamage(baseDamage, attacker, target)
    local damage = baseDamage

    -- Attacker bonuses
    local attackBonus = attacker:GetAttribute("AttackBonus") or 0
    damage = damage * (1 + attackBonus / 100)

    -- Critical hit
    local critChance = attacker:GetAttribute("CritChance") or 5
    local critMultiplier = attacker:GetAttribute("CritMultiplier") or 1.5
    local isCrit = math.random(100) <= critChance
    if isCrit then
        damage = damage * critMultiplier
    end

    -- Target defense
    local defense = target:GetAttribute("Defense") or 0
    damage = damage * (100 / (100 + defense))  -- Diminishing returns formula

    -- Elemental resistances
    local element = attacker:GetAttribute("DamageElement")
    if element then
        local resistance = target:GetAttribute(element .. "Resistance") or 0
        damage = damage * (1 - resistance / 100)
    end

    return math.floor(damage), isCrit
end

function DamageSystem.applyDamage(humanoid, damage, isCrit, source)
    -- Check invincibility frames
    if humanoid:GetAttribute("Invincible") then return end

    humanoid:TakeDamage(damage)

    -- Fire damage event for UI/effects
    local character = humanoid.Parent
    DamageEvent:Fire(character, damage, isCrit, source)

    -- Track damage source for kill attribution
    character:SetAttribute("LastDamageSource", source and source.Name or "Environment")
    character:SetAttribute("LastDamageTime", os.clock())
end
```

### Damage Over Time (DoT)
```lua
local DoTManager = {}
DoTManager.activeDoTs = {}

function DoTManager.applyDoT(target, dotData)
    local id = HttpService:GenerateGUID()
    local dot = {
        id = id,
        target = target,
        damage = dotData.damage,
        tickRate = dotData.tickRate or 1,
        duration = dotData.duration,
        element = dotData.element,
        source = dotData.source,
        startTime = os.clock(),
        lastTick = 0
    }

    DoTManager.activeDoTs[id] = dot
    return id
end

function DoTManager.update()
    local currentTime = os.clock()

    for id, dot in pairs(DoTManager.activeDoTs) do
        -- Check expiration
        if currentTime - dot.startTime >= dot.duration then
            DoTManager.activeDoTs[id] = nil
            continue
        end

        -- Apply tick damage
        if currentTime - dot.lastTick >= dot.tickRate then
            dot.lastTick = currentTime
            local humanoid = dot.target:FindFirstChildOfClass("Humanoid")
            if humanoid and humanoid.Health > 0 then
                DamageSystem.applyDamage(humanoid, dot.damage, false, dot.source)
            else
                DoTManager.activeDoTs[id] = nil
            end
        end
    end
end
```

## Stun & Status Effects

### Stun Handler Module
```lua
local StunHandler = {}
StunHandler.stunnedEntities = {}

-- Stun priorities (higher overrides lower)
local StunPriority = {
    Stagger = 1,      -- Brief interruption
    Stun = 2,         -- Standard stun
    Knockdown = 3,    -- Longer, on ground
    Ragdoll = 4,      -- Full physics ragdoll
    Frozen = 5        -- Highest priority
}

function StunHandler.applyStun(character, stunType, duration)
    local current = StunHandler.stunnedEntities[character]
    local newPriority = StunPriority[stunType]

    -- Only apply if higher or equal priority
    if current and StunPriority[current.type] > newPriority then
        return false
    end

    -- Apply stun
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid then return false end

    -- Disable movement
    humanoid.WalkSpeed = 0
    humanoid.JumpPower = 0
    humanoid.AutoRotate = false

    StunHandler.stunnedEntities[character] = {
        type = stunType,
        endTime = os.clock() + duration,
        originalWalkSpeed = humanoid:GetAttribute("BaseWalkSpeed") or 16,
        originalJumpPower = humanoid:GetAttribute("BaseJumpPower") or 50
    }

    -- Schedule recovery
    task.delay(duration, function()
        StunHandler.removeStun(character, stunType)
    end)

    return true
end

function StunHandler.removeStun(character, expectedType)
    local stun = StunHandler.stunnedEntities[character]
    if not stun or (expectedType and stun.type ~= expectedType) then return end

    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if humanoid then
        humanoid.WalkSpeed = stun.originalWalkSpeed
        humanoid.JumpPower = stun.originalJumpPower
        humanoid.AutoRotate = true
    end

    StunHandler.stunnedEntities[character] = nil
end

function StunHandler.isStunned(character)
    return StunHandler.stunnedEntities[character] ~= nil
end
```

### Knockback System
```lua
function applyKnockback(character, direction, force, duration)
    local hrp = character:FindFirstChild("HumanoidRootPart")
    if not hrp then return end

    -- Normalize direction and apply force
    local knockbackVelocity = direction.Unit * force

    -- Use LinearVelocity for consistent knockback
    local linearVel = Instance.new("LinearVelocity")
    linearVel.Attachment0 = hrp:FindFirstChild("RootAttachment") or Instance.new("Attachment", hrp)
    linearVel.VectorVelocity = knockbackVelocity
    linearVel.MaxForce = math.huge
    linearVel.RelativeTo = Enum.ActuatorRelativeTo.World
    linearVel.Parent = hrp

    task.delay(duration or 0.2, function()
        linearVel:Destroy()
    end)
end
```

## Melee Combat

### Combo System State Machine
```lua
local ComboSystem = {}

local ComboData = {
    M1 = {
        {name = "Jab", damage = 10, duration = 0.3, canCancel = {0.2, 0.3}},
        {name = "Cross", damage = 12, duration = 0.35, canCancel = {0.25, 0.35}},
        {name = "Hook", damage = 15, duration = 0.4, canCancel = {0.3, 0.4}},
        {name = "Uppercut", damage = 20, duration = 0.5, canCancel = nil, finisher = true}
    }
}

function ComboSystem.new(character)
    return {
        character = character,
        currentCombo = nil,
        comboIndex = 0,
        lastAttackTime = 0,
        inputBuffer = nil,
        comboResetTime = 1.5
    }
end

function ComboSystem.attack(self, attackType)
    local currentTime = os.clock()

    -- Reset combo if too much time passed
    if currentTime - self.lastAttackTime > self.comboResetTime then
        self.comboIndex = 0
        self.currentCombo = nil
    end

    -- Get combo data
    local combo = ComboData[attackType]
    if not combo then return end

    -- Advance combo
    self.comboIndex = self.comboIndex + 1
    if self.comboIndex > #combo then
        self.comboIndex = 1
    end

    local attackData = combo[self.comboIndex]
    self.currentCombo = attackType
    self.lastAttackTime = currentTime

    -- Execute attack
    return self:executeAttack(attackData)
end

function ComboSystem.executeAttack(self, attackData)
    -- Play animation
    local animator = self.character:FindFirstChildOfClass("Humanoid"):FindFirstChildOfClass("Animator")
    local track = animator:LoadAnimation(attackData.animation)
    track:Play()

    -- Create hitbox at appropriate frame
    task.delay(attackData.hitboxDelay or 0.1, function()
        meleeAttack(self.character, attackData.damage, attackData.knockback)
    end)

    return attackData
end
```

## Ranged Combat

### Hitscan Weapon
```lua
function fireHitscan(origin, direction, weaponData)
    local params = RaycastParams.new()
    params.FilterDescendantsInstances = {localPlayer.Character}
    params.FilterType = Enum.RaycastFilterType.Exclude

    -- Apply spread
    local spread = weaponData.spread * (isADS and 0.3 or 1)
    local spreadX = (math.random() - 0.5) * spread
    local spreadY = (math.random() - 0.5) * spread
    local spreadDir = (CFrame.lookAt(origin, origin + direction) * CFrame.Angles(spreadX, spreadY, 0)).LookVector

    local result = workspace:Raycast(origin, spreadDir * weaponData.range, params)

    if result then
        -- Check if hit character
        local character = result.Instance.Parent
        local humanoid = character:FindFirstChildOfClass("Humanoid")

        if humanoid then
            -- Calculate damage falloff
            local distance = result.Distance
            local falloff = 1 - math.clamp((distance - weaponData.falloffStart) / (weaponData.range - weaponData.falloffStart), 0, 0.5)
            local damage = weaponData.baseDamage * falloff

            -- Headshot multiplier
            if result.Instance.Name == "Head" then
                damage = damage * weaponData.headshotMultiplier
            end

            CombatRemote:FireServer("HitscanHit", {
                targetId = character:GetAttribute("EntityId"),
                damage = damage,
                hitPart = result.Instance.Name
            })
        end

        -- Create impact effect
        createImpactEffect(result.Position, result.Normal, result.Material)
    end

    return result
end
```

### Projectile System
```lua
local ProjectileSystem = {}
ProjectileSystem.activeProjectiles = {}

function ProjectileSystem.spawn(data)
    local projectile = {
        id = HttpService:GenerateGUID(),
        position = data.origin,
        velocity = data.direction.Unit * data.speed,
        gravity = data.gravity or Vector3.new(0, -workspace.Gravity, 0),
        damage = data.damage,
        owner = data.owner,
        lifetime = data.lifetime or 10,
        spawnTime = os.clock(),
        radius = data.radius or 0.5
    }

    -- Create visual
    projectile.visual = data.visualTemplate:Clone()
    projectile.visual.CFrame = CFrame.lookAt(data.origin, data.origin + data.direction)
    projectile.visual.Parent = workspace

    ProjectileSystem.activeProjectiles[projectile.id] = projectile
    return projectile
end

function ProjectileSystem.update(dt)
    for id, proj in pairs(ProjectileSystem.activeProjectiles) do
        -- Check lifetime
        if os.clock() - proj.spawnTime > proj.lifetime then
            ProjectileSystem.destroy(id)
            continue
        end

        -- Physics update
        proj.velocity = proj.velocity + proj.gravity * dt
        local newPos = proj.position + proj.velocity * dt

        -- Raycast for collision
        local result = workspace:Raycast(proj.position, newPos - proj.position)
        if result then
            ProjectileSystem.onHit(proj, result)
            ProjectileSystem.destroy(id)
            continue
        end

        proj.position = newPos
        proj.visual.CFrame = CFrame.lookAt(proj.position, proj.position + proj.velocity)
    end
end

function ProjectileSystem.onHit(proj, rayResult)
    local character = rayResult.Instance.Parent
    local humanoid = character:FindFirstChildOfClass("Humanoid")

    if humanoid then
        DamageSystem.applyDamage(humanoid, proj.damage, false, proj.owner)
    end

    -- Spawn explosion/impact
    createExplosion(rayResult.Position, proj.explosionRadius)
end
```

## Ability System

### Cooldown Management
```lua
local CooldownManager = {}
CooldownManager.cooldowns = {}

function CooldownManager.startCooldown(entity, abilityId, duration)
    local key = entity:GetAttribute("EntityId") .. "_" .. abilityId
    CooldownManager.cooldowns[key] = os.clock() + duration
end

function CooldownManager.isOnCooldown(entity, abilityId)
    local key = entity:GetAttribute("EntityId") .. "_" .. abilityId
    local endTime = CooldownManager.cooldowns[key]
    return endTime and os.clock() < endTime
end

function CooldownManager.getRemainingCooldown(entity, abilityId)
    local key = entity:GetAttribute("EntityId") .. "_" .. abilityId
    local endTime = CooldownManager.cooldowns[key]
    if not endTime then return 0 end
    return math.max(0, endTime - os.clock())
end
```

### Ability Base Class
```lua
local Ability = {}
Ability.__index = Ability

function Ability.new(data)
    return setmetatable({
        id = data.id,
        name = data.name,
        cooldown = data.cooldown,
        manaCost = data.manaCost or 0,
        castTime = data.castTime or 0,
        onCast = data.onCast,
        onChannel = data.onChannel,
        onRelease = data.onRelease
    }, Ability)
end

function Ability:canCast(caster)
    -- Check cooldown
    if CooldownManager.isOnCooldown(caster, self.id) then
        return false, "On cooldown"
    end

    -- Check mana
    local mana = caster:GetAttribute("Mana") or 0
    if mana < self.manaCost then
        return false, "Not enough mana"
    end

    -- Check stun
    if StunHandler.isStunned(caster) then
        return false, "Stunned"
    end

    return true
end

function Ability:cast(caster, target)
    local canCast, reason = self:canCast(caster)
    if not canCast then return false, reason end

    -- Consume mana
    local currentMana = caster:GetAttribute("Mana")
    caster:SetAttribute("Mana", currentMana - self.manaCost)

    -- Start cooldown
    CooldownManager.startCooldown(caster, self.id, self.cooldown)

    -- Execute ability
    if self.castTime > 0 then
        -- Channeled ability
        self:startChannel(caster, target)
    else
        -- Instant ability
        self.onCast(caster, target)
    end

    return true
end
```
