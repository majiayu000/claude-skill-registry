---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with game controllers, joystick input, gamepad operations, or any input device-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with game controllers, joystick input, gamepad operations, or any input device-related operations in LÖVE games.

## Common use cases
- Handling joystick and gamepad input
- Managing multiple input devices
- Implementing controller-based game mechanics
- Handling joystick events and callbacks
- Supporting various game controller types

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Handling joystick input
```lua
function love.joystickpressed(joystick, button)
  if button == 1 then
    -- Handle primary action button
    player.jump()
  elseif button == 2 then
    -- Handle secondary action button
    player.attack()
  end
end
```

### Getting joystick axis values
```lua
function love.update(dt)
  local joysticks = love.joystick.getJoysticks()
  for i, joystick in ipairs(joysticks) do
    local leftX = joystick:getAxis(1)  -- Left stick X axis
    local leftY = joystick:getAxis(2)  -- Left stick Y axis

    -- Apply movement based on joystick input
    player.move(leftX, leftY)
  end
end
```

## Best practices
- Support both keyboard and joystick input for accessibility
- Handle joystick connection/disconnection gracefully
- Test with various controller types
- Consider controller dead zones and sensitivity
- Provide controller configuration options

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full joystick support
- **Mobile (iOS, Android)**: Limited to touch-based virtual controllers
- **Web**: Browser-based gamepad API support
