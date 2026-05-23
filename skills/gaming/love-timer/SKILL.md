---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with time measurement, frame rate control, performance monitoring, or any time-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with time measurement, frame rate control, performance monitoring, or any time-related operations in LÖVE games.

## Common use cases
- Measuring elapsed time and performance
- Controlling game frame rate and timing
- Implementing smooth animations and transitions
- Profiling and optimizing game performance
- Handling time-based game mechanics

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Measuring delta time
```lua
-- Use delta time for frame-rate independent movement
function love.update(dt)
  local moveSpeed = 200  -- pixels per second
  local distance = moveSpeed * dt
  player.x = player.x + distance
end
```

### Performance measurement
```lua
-- Measure function execution time
local startTime = love.timer.getTime()

-- Perform some operations
complexOperation()

local endTime = love.timer.getTime()
local elapsed = endTime - startTime
print("Operation took: " .. elapsed .. " seconds")
```

## Best practices
- Use delta time (dt) for all time-based calculations
- Consider using love.timer for high-precision timing
- Be mindful of performance when using frequent timing calls
- Test timing behavior on target platforms
- Use appropriate time units for different measurements

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full timer support
- **Mobile (iOS, Android)**: Full support
- **Web**: Full support
