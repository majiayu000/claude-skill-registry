---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with sound operations, audio decoding, sound data manipulation, or any sound-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with sound operations, audio decoding, sound data manipulation, or any sound-related operations in LÖVE games.

## Common use cases
- Decoding sound files and formats
- Managing sound data and audio buffers
- Performing sound transformations and effects
- Working with compressed audio formats
- Handling sound metadata and properties

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Decoding sound data
```lua
-- Decode a sound file
local soundData = love.sound.newSoundData("effect.wav")

-- Play the sound
local source = love.audio.newSource(soundData)
love.audio.play(source)
```

### Sound data manipulation
```lua
-- Create and modify sound data
local sampleRate = 44100
local bitDepth = 16
local channels = 1
local duration = 1.0  -- 1 second

local soundData = love.sound.newSoundData(
  sampleRate * duration,
  sampleRate,
  bitDepth,
  channels
)

-- Generate a simple sine wave
for i = 0, soundData:getSampleCount() - 1 do
  local time = i / sampleRate
  local value = math.sin(time * 440 * 2 * math.pi)  -- 440Hz sine wave
  soundData:setSample(i, value)
end

-- Create and play the sound
local source = love.audio.newSource(soundData)
love.audio.play(source)
```

## Best practices
- Use appropriate sound formats for different use cases
- Consider memory usage when working with large sound files
- Handle sound decoding errors gracefully
- Test sound formats on target platforms
- Be mindful of performance with real-time sound processing

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full sound support
- **Mobile (iOS, Android)**: Full support with some format limitations
- **Web**: Good support but some formats may not be available
