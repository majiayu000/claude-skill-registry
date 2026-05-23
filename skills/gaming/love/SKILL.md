---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with core functionality for LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with core functionality for LÖVE games.

## Common use cases
- Basic game setup and configuration
- Accessing core framework features
- Handling cross-module functionality
- Game loop management and event handling

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Basic game structure
```lua
-- Main game structure with core LÖVE callbacks
function love.load()
  -- Initialize game resources
  player = {x = 100, y = 100, speed = 200}

  -- Load assets
  playerImage = love.graphics.newImage("player.png")
end

function love.update(dt)
  -- Update game state using delta time
  if love.keyboard.isDown("right") then
    player.x = player.x + player.speed * dt
  end
  if love.keyboard.isDown("left") then
    player.x = player.x - player.speed * dt
  end
end

function love.draw()
  -- Draw game elements
  love.graphics.draw(playerImage, player.x, player.y)
  love.graphics.print("Hello World!", 400, 300)
end

function love.keypressed(key)
  -- Handle key presses
  if key == "escape" then
    love.event.quit()
  end
end
```

### Version compatibility check
```lua
-- Check LÖVE version compatibility
function love.load()
  local major, minor, revision = love.getVersion()
  print("Running LÖVE " .. major .. "." .. minor .. "." .. revision)

  -- Check if current version supports required features
  if love.isVersionCompatible(11, 3) then
    print("Version 11.3+ features are available")
  else
    print("Warning: Some features may not be available")
  end
end
```

## Best practices
- Always check if functions are supported on the target platform
- Handle errors gracefully for cross-platform compatibility
- Use callbacks appropriately for event-driven programming
- Consider performance implications for frequently called functions

## Platform compatibility
Most functions are supported across all platforms, but some may have limitations:
- Desktop (Windows, macOS, Linux): Full support
- Mobile (iOS, Android): Some limitations may apply
- Web: Limited support for certain features
