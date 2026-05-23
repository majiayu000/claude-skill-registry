---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with sound effects, music playback, audio recording, or any audio-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with sound effects, music playback, audio recording, or any audio-related operations in LÖVE games.

## Common use cases
- Playing background music and sound effects
- Implementing dynamic audio for game events
- Recording and processing audio input
- Creating immersive 3D audio experiences
- Managing multiple audio sources simultaneously

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Playing a sound effect
```lua
-- Load and play a sound effect
local sound = love.audio.newSource("explosion.wav", "static")
love.audio.play(sound)
```

### Background music with volume control
```lua
-- Load background music and set volume
local music = love.audio.newSource("background.mp3", "stream")
music:setVolume(0.5)
music:setLooping(true)
love.audio.play(music)
```

## Best practices
- Use "static" sources for short sound effects and "stream" sources for long music tracks
- Preload audio files during loading screens to avoid delays
- Consider using audio effects (reverb, echo) sparingly for performance
- Test audio on target platforms as format support may vary
- Use appropriate audio formats: OGG/Vorbis for music, WAV for sound effects

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full audio support including 3D audio and effects
- **Mobile (iOS, Android)**: Full support but some effects may be limited
- **Web**: Limited to basic audio playback, no recording or advanced effects

## Performance considerations
- Too many simultaneous audio sources can cause performance issues
- Complex audio effects impact CPU usage
- Streaming audio uses less memory than static audio
- Audio position calculations for 3D audio can be CPU-intensive
