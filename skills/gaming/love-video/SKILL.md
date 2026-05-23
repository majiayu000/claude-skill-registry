---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with video operations, video decoding, video streaming, or any video-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with video operations, video decoding, video streaming, or any video-related operations in LÖVE games.

## Common use cases
- Playing video files and streams
- Managing video playback and control
- Handling video decoding and processing
- Implementing video-based game elements
- Working with video metadata and properties

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Playing a video
```lua
-- Load and play a video file
local video = love.graphics.newVideo("intro.mp4")
video:play()

function love.draw()
  if video:isPlaying() then
    love.graphics.draw(video, 0, 0)
  end
end
```

### Video control
```lua
-- Control video playback
function love.keypressed(key)
  if key == "space" then
    if video:isPlaying() then
      video:pause()
    else
      video:play()
    end
  elseif key == "escape" then
    video:stop()
  end
end
```

## Best practices
- Preload videos during loading screens
- Consider performance implications of video playback
- Use appropriate video formats and codecs
- Handle video loading and playback errors gracefully
- Test video playback on target platforms

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full video support
- **Mobile (iOS, Android)**: Limited video format support
- **Web**: Browser-based video support with format limitations
