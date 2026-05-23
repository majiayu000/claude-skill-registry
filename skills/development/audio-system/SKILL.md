---
name: audio-system
description: Implements audio systems including sound management, music systems, positional audio, and audio effects. Use when adding sound effects, music, ambient audio, or any audio features to a game.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Audio Systems

## Quick Reference Links

**Official Documentation:**
- [Audio Overview](https://create.roblox.com/docs/sound) - Complete audio guide
- [Sound Objects](https://create.roblox.com/docs/sound/objects) - Sound, SoundGroup, SoundService
- [Audio Effects](https://create.roblox.com/docs/sound/dynamic-effects) - Reverb, EQ, Distortion
- [Sound API](https://create.roblox.com/docs/reference/engine/classes/Sound)
- [SoundService API](https://create.roblox.com/docs/reference/engine/classes/SoundService)
- [SoundGroup API](https://create.roblox.com/docs/reference/engine/classes/SoundGroup)
- [AudioEmitter API](https://create.roblox.com/docs/reference/engine/classes/AudioEmitter)
- [AudioListener API](https://create.roblox.com/docs/reference/engine/classes/AudioListener)

**Wiki References:**
- [Sound (Wiki)](https://roblox.fandom.com/wiki/Sound)
- [SoundService (Wiki)](https://roblox.fandom.com/wiki/SoundService)

---

When implementing audio, follow these patterns for immersive and performant sound design.

## Sound Management

### Sound Pooling
```lua
local SoundPool = {}
SoundPool.pools = {}

function SoundPool.create(soundId, poolSize)
    poolSize = poolSize or 5

    local pool = {
        sounds = {},
        currentIndex = 1
    }

    for i = 1, poolSize do
        local sound = Instance.new("Sound")
        sound.SoundId = soundId
        sound.Parent = SoundService
        table.insert(pool.sounds, sound)
    end

    SoundPool.pools[soundId] = pool
    return pool
end

function SoundPool.play(soundId, properties)
    local pool = SoundPool.pools[soundId]
    if not pool then
        pool = SoundPool.create(soundId)
    end

    local sound = pool.sounds[pool.currentIndex]
    pool.currentIndex = pool.currentIndex % #pool.sounds + 1

    -- Apply properties
    if properties then
        for key, value in pairs(properties) do
            sound[key] = value
        end
    end

    sound:Play()
    return sound
end

-- Usage
SoundPool.create("rbxassetid://123456789", 10)  -- Pre-create pool
SoundPool.play("rbxassetid://123456789", {Volume = 0.5, PlaybackSpeed = 1.2})
```

### Sound Priority System
```lua
local SoundManager = {}
SoundManager.activeSounds = {}
SoundManager.maxSounds = 32  -- Roblox limit is higher, but good for performance

local SoundPriority = {
    UI = 100,
    PlayerAction = 80,
    Combat = 70,
    Environment = 50,
    Ambient = 30
}

function SoundManager.play(soundId, priority, properties)
    priority = priority or SoundPriority.Environment

    -- Check if we need to stop lower priority sounds
    if #SoundManager.activeSounds >= SoundManager.maxSounds then
        -- Find lowest priority sound
        local lowestPriority = priority
        local lowestIndex = nil

        for i, soundData in ipairs(SoundManager.activeSounds) do
            if soundData.priority < lowestPriority then
                lowestPriority = soundData.priority
                lowestIndex = i
            end
        end

        if lowestIndex then
            local removed = table.remove(SoundManager.activeSounds, lowestIndex)
            removed.sound:Stop()
        else
            return nil  -- Can't play, all sounds are higher priority
        end
    end

    local sound = Instance.new("Sound")
    sound.SoundId = soundId

    if properties then
        for key, value in pairs(properties) do
            sound[key] = value
        end
    end

    sound.Parent = SoundService
    sound:Play()

    local soundData = {
        sound = sound,
        priority = priority
    }

    table.insert(SoundManager.activeSounds, soundData)

    sound.Ended:Connect(function()
        local index = table.find(SoundManager.activeSounds, soundData)
        if index then
            table.remove(SoundManager.activeSounds, index)
        end
        sound:Destroy()
    end)

    return sound
end
```

### Volume Categories
```lua
local VolumeManager = {}
VolumeManager.categories = {
    Master = 1,
    Music = 0.7,
    SFX = 0.8,
    Voice = 1,
    Ambient = 0.5
}

VolumeManager.soundGroups = {}

function VolumeManager.setup()
    -- Create SoundGroups for each category
    for category, defaultVolume in pairs(VolumeManager.categories) do
        local group = Instance.new("SoundGroup")
        group.Name = category
        group.Volume = defaultVolume
        group.Parent = SoundService
        VolumeManager.soundGroups[category] = group
    end

    -- Set Master as parent of others
    for category, group in pairs(VolumeManager.soundGroups) do
        if category ~= "Master" then
            group.Parent = VolumeManager.soundGroups.Master
        end
    end
end

function VolumeManager.setVolume(category, volume)
    VolumeManager.categories[category] = volume
    if VolumeManager.soundGroups[category] then
        VolumeManager.soundGroups[category].Volume = volume
    end
end

function VolumeManager.playInCategory(soundId, category, properties)
    local sound = Instance.new("Sound")
    sound.SoundId = soundId
    sound.SoundGroup = VolumeManager.soundGroups[category]

    if properties then
        for key, value in pairs(properties) do
            sound[key] = value
        end
    end

    sound.Parent = SoundService
    sound:Play()

    return sound
end
```

## Music Systems

### Music Playlist
```lua
local MusicPlayer = {}
MusicPlayer.playlist = {}
MusicPlayer.currentIndex = 0
MusicPlayer.currentSound = nil
MusicPlayer.isPlaying = false
MusicPlayer.shuffle = false

function MusicPlayer.addTrack(soundId, name)
    table.insert(MusicPlayer.playlist, {
        id = soundId,
        name = name
    })
end

function MusicPlayer.play()
    if #MusicPlayer.playlist == 0 then return end

    MusicPlayer.isPlaying = true

    if MusicPlayer.currentIndex == 0 then
        MusicPlayer.next()
    elseif MusicPlayer.currentSound then
        MusicPlayer.currentSound:Resume()
    end
end

function MusicPlayer.pause()
    if MusicPlayer.currentSound then
        MusicPlayer.currentSound:Pause()
    end
end

function MusicPlayer.next()
    if MusicPlayer.currentSound then
        MusicPlayer.currentSound:Stop()
        MusicPlayer.currentSound:Destroy()
    end

    if MusicPlayer.shuffle then
        MusicPlayer.currentIndex = math.random(1, #MusicPlayer.playlist)
    else
        MusicPlayer.currentIndex = MusicPlayer.currentIndex % #MusicPlayer.playlist + 1
    end

    local track = MusicPlayer.playlist[MusicPlayer.currentIndex]

    MusicPlayer.currentSound = Instance.new("Sound")
    MusicPlayer.currentSound.SoundId = track.id
    MusicPlayer.currentSound.Volume = 0.5
    MusicPlayer.currentSound.Looped = false
    MusicPlayer.currentSound.SoundGroup = VolumeManager.soundGroups.Music
    MusicPlayer.currentSound.Parent = SoundService

    MusicPlayer.currentSound.Ended:Connect(function()
        if MusicPlayer.isPlaying then
            MusicPlayer.next()
        end
    end)

    if MusicPlayer.isPlaying then
        MusicPlayer.currentSound:Play()
    end
end

function MusicPlayer.previous()
    MusicPlayer.currentIndex = MusicPlayer.currentIndex - 2
    if MusicPlayer.currentIndex < 0 then
        MusicPlayer.currentIndex = #MusicPlayer.playlist - 1
    end
    MusicPlayer.next()
end
```

### Crossfade Transition
```lua
local function crossfade(fromSound, toSound, duration)
    duration = duration or 2

    toSound.Volume = 0
    toSound:Play()

    local startTime = os.clock()
    local fromVolume = fromSound.Volume

    local conn
    conn = RunService.Heartbeat:Connect(function()
        local elapsed = os.clock() - startTime
        local t = math.min(elapsed / duration, 1)

        fromSound.Volume = fromVolume * (1 - t)
        toSound.Volume = fromVolume * t

        if t >= 1 then
            fromSound:Stop()
            conn:Disconnect()
        end
    end)
end
```

### Contextual Music
```lua
local MusicContext = {}
MusicContext.contexts = {
    peaceful = "rbxassetid://peaceful_music",
    combat = "rbxassetid://combat_music",
    boss = "rbxassetid://boss_music",
    victory = "rbxassetid://victory_music"
}
MusicContext.currentContext = nil
MusicContext.currentSound = nil

function MusicContext.setContext(contextName)
    if contextName == MusicContext.currentContext then return end

    local newSoundId = MusicContext.contexts[contextName]
    if not newSoundId then return end

    local newSound = Instance.new("Sound")
    newSound.SoundId = newSoundId
    newSound.Looped = true
    newSound.Parent = SoundService

    if MusicContext.currentSound then
        crossfade(MusicContext.currentSound, newSound, 2)
        task.delay(2, function()
            MusicContext.currentSound:Destroy()
            MusicContext.currentSound = newSound
        end)
    else
        newSound.Volume = 0.5
        newSound:Play()
        MusicContext.currentSound = newSound
    end

    MusicContext.currentContext = contextName
end

-- Usage
MusicContext.setContext("peaceful")
-- Later, when combat starts:
MusicContext.setContext("combat")
```

## Positional Audio

### 3D Sound Setup
```lua
local function play3DSound(soundId, position, properties)
    local part = Instance.new("Part")
    part.Anchored = true
    part.CanCollide = false
    part.Transparency = 1
    part.Size = Vector3.new(0.1, 0.1, 0.1)
    part.Position = position
    part.Parent = workspace

    local sound = Instance.new("Sound")
    sound.SoundId = soundId
    sound.RollOffMode = Enum.RollOffMode.Linear
    sound.RollOffMinDistance = properties.minDistance or 10
    sound.RollOffMaxDistance = properties.maxDistance or 100
    sound.Volume = properties.volume or 1
    sound.Parent = part

    sound:Play()

    sound.Ended:Connect(function()
        part:Destroy()
    end)

    return sound, part
end
```

### Sound Falloff Modes
```lua
-- Linear falloff (most predictable)
sound.RollOffMode = Enum.RollOffMode.Linear
sound.RollOffMinDistance = 10  -- Full volume within this distance
sound.RollOffMaxDistance = 100 -- Silent beyond this distance

-- Inverse (more realistic)
sound.RollOffMode = Enum.RollOffMode.Inverse
-- Volume = 1 / (1 + (distance - minDistance) / (maxDistance - minDistance))

-- InverseTapered (smoother falloff)
sound.RollOffMode = Enum.RollOffMode.InverseTapered
-- Combines linear and inverse

-- Custom falloff with emitter size
sound.EmitterSize = 5  -- Sound appears to come from area, not point
```

### Footstep Sounds
```lua
local FootstepSounds = {
    [Enum.Material.Grass] = "rbxassetid://grass_step",
    [Enum.Material.Concrete] = "rbxassetid://concrete_step",
    [Enum.Material.Wood] = "rbxassetid://wood_step",
    [Enum.Material.Metal] = "rbxassetid://metal_step",
    [Enum.Material.Sand] = "rbxassetid://sand_step",
    [Enum.Material.Water] = "rbxassetid://water_splash"
}

local function setupFootsteps(character)
    local humanoid = character:WaitForChild("Humanoid")
    local rootPart = character:WaitForChild("HumanoidRootPart")

    local lastStep = 0
    local stepInterval = 0.4  -- Seconds between steps

    humanoid.Running:Connect(function(speed)
        if speed > 1 then
            local now = os.clock()
            if now - lastStep >= stepInterval / (speed / 16) then
                lastStep = now

                -- Get ground material
                local ray = workspace:Raycast(
                    rootPart.Position,
                    Vector3.new(0, -3, 0)
                )

                local material = ray and ray.Material or Enum.Material.Concrete
                local soundId = FootstepSounds[material] or FootstepSounds[Enum.Material.Concrete]

                local sound = Instance.new("Sound")
                sound.SoundId = soundId
                sound.Volume = 0.5
                sound.PlaybackSpeed = 0.9 + math.random() * 0.2  -- Slight variation
                sound.Parent = rootPart
                sound:Play()

                Debris:AddItem(sound, 1)
            end
        end
    end)
end
```

## Audio Effects

### Sound Groups & Effects
```lua
-- Create reverb effect
local reverbGroup = Instance.new("SoundGroup")
reverbGroup.Name = "Reverb"
reverbGroup.Parent = SoundService

local reverb = Instance.new("ReverbSoundEffect")
reverb.DecayTime = 2
reverb.Density = 0.8
reverb.Diffusion = 0.9
reverb.DryLevel = 0
reverb.WetLevel = -6
reverb.Parent = reverbGroup

-- Create low-pass filter (muffled)
local muffledGroup = Instance.new("SoundGroup")
muffledGroup.Name = "Muffled"
muffledGroup.Parent = SoundService

local lowPass = Instance.new("EqualizerSoundEffect")
lowPass.HighGain = -20  -- Reduce high frequencies
lowPass.MidGain = -5
lowPass.LowGain = 0
lowPass.Parent = muffledGroup

-- Assign sounds to groups
caveSound.SoundGroup = reverbGroup
underwaterSound.SoundGroup = muffledGroup
```

### Dynamic Audio Processing
```lua
local function applyUnderwaterEffect(enable)
    local muffleEffect = camera:FindFirstChild("UnderwaterMuffle")

    if enable then
        if not muffleEffect then
            muffleEffect = Instance.new("EqualizerSoundEffect")
            muffleEffect.Name = "UnderwaterMuffle"
            muffleEffect.HighGain = -30
            muffleEffect.MidGain = -10
            muffleEffect.LowGain = 5
            muffleEffect.Parent = SoundService
        end
    else
        if muffleEffect then
            muffleEffect:Destroy()
        end
    end
end
```

### Doppler Effect (Moving Sources)
```lua
-- Roblox doesn't have built-in Doppler, but we can simulate it
local function simulateDoppler(sound, sourceVelocity, listenerVelocity)
    local speedOfSound = 343  -- m/s

    local relativeVelocity = sourceVelocity - listenerVelocity
    local directionToListener = (camera.CFrame.Position - sound.Parent.Position).Unit
    local approachSpeed = relativeVelocity:Dot(directionToListener)

    -- Doppler shift formula
    local dopplerShift = speedOfSound / (speedOfSound + approachSpeed)
    sound.PlaybackSpeed = dopplerShift

    -- Also adjust volume slightly
    if approachSpeed > 0 then
        sound.Volume = sound.Volume * 1.1  -- Approaching, slightly louder
    else
        sound.Volume = sound.Volume * 0.9  -- Receding, slightly quieter
    end
end
```

## Ambient Audio

### Ambient Soundscape
```lua
local AmbientManager = {}
AmbientManager.activeSounds = {}

function AmbientManager.setup(sounds)
    for _, soundData in ipairs(sounds) do
        local sound = Instance.new("Sound")
        sound.SoundId = soundData.id
        sound.Volume = soundData.volume or 0.3
        sound.Looped = true
        sound.Parent = SoundService

        AmbientManager.activeSounds[soundData.name] = {
            sound = sound,
            baseVolume = soundData.volume or 0.3
        }
    end
end

function AmbientManager.setIntensity(name, intensity)
    local data = AmbientManager.activeSounds[name]
    if data then
        data.sound.Volume = data.baseVolume * intensity
    end
end

function AmbientManager.start()
    for _, data in pairs(AmbientManager.activeSounds) do
        data.sound:Play()
    end
end

-- Usage
AmbientManager.setup({
    {name = "wind", id = "rbxassetid://wind", volume = 0.2},
    {name = "birds", id = "rbxassetid://birds", volume = 0.3},
    {name = "water", id = "rbxassetid://river", volume = 0.4}
})
AmbientManager.start()

-- Based on location
if isNearWater then
    AmbientManager.setIntensity("water", 1)
else
    AmbientManager.setIntensity("water", 0.2)
end
```

### Region-Based Audio
```lua
local AudioRegions = {}

local function checkAudioRegions()
    local character = Players.LocalPlayer.Character
    if not character then return end

    local position = character.PrimaryPart.Position

    for _, region in ipairs(AudioRegions) do
        local inRegion = position.X >= region.min.X and position.X <= region.max.X
                     and position.Y >= region.min.Y and position.Y <= region.max.Y
                     and position.Z >= region.min.Z and position.Z <= region.max.Z

        if inRegion and not region.active then
            region.active = true
            region.sound:Play()
            if region.onEnter then region.onEnter() end
        elseif not inRegion and region.active then
            region.active = false
            region.sound:Stop()
            if region.onExit then region.onExit() end
        end
    end
end

RunService.Heartbeat:Connect(checkAudioRegions)
```
