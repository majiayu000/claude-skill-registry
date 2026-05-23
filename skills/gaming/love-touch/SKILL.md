---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with touch operations, multi-touch gestures, touch events, or any touch-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with touch operations, multi-touch gestures, touch events, or any touch-related operations in LÖVE games.

## Common use cases
- Handling touch screen input
- Implementing multi-touch gestures
- Working with touch-based game controls
- Managing touch events and callbacks
- Supporting mobile touch interfaces

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Handling touch input
```lua
function love.touchpressed(id, x, y, dx, dy, pressure)
  -- Store touch position
  touches[id] = {x = x, y = y, pressure = pressure}

  -- Handle touch at position (x, y)
  handleTouchAt(x, y)
end
```

### Multi-touch handling
```lua
function love.touchmoved(id, x, y, dx, dy, pressure)
  if touches[id] then
    -- Update touch position
    touches[id].x = x
    touches[id].y = y

    -- Handle drag gesture
    handleDrag(id, dx, dy)
  end
end

function love.touchreleased(id, x, y, dx, dy, pressure)
  -- Remove touch
  touches[id] = nil
end
```

## Best practices
- Support both touch and mouse input for cross-platform compatibility
- Handle multi-touch gestures appropriately
- Consider touch interface design for mobile devices
- Test touch input on target platforms
- Be mindful of touch accuracy and precision

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Touch support on touchscreen devices
- **Mobile (iOS, Android)**: Full multi-touch support
- **Web**: Browser-based touch support
