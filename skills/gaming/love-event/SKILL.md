---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with event management, event callbacks, event pumping, or any event-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with event management, event callbacks, event pumping, or any event-related operations in LÖVE games.

## Common use cases
- Managing game events and callbacks
- Implementing custom event handling systems
- Working with event queues and pumping
- Handling system and user-generated events
- Managing event flow and propagation

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Custom event handling
```lua
-- Pump and handle events manually
function love.update(dt)
  love.event.pump()

  for name, a, b, c, d, e, f in love.event.poll() do
    if name == "quit" then
      if not love.quit or not love.quit() then
        return a or 0
      end
    end
    -- Handle other events
  end
end
```

### Event callback
```lua
-- Custom quit handler
function love.quit()
  -- Save game state before quitting
  saveGameState()
  return false  -- Allow normal quit process
end
```

## Best practices
- Use love.event.pump() regularly to process events
- Handle quit events gracefully
- Consider performance when polling events frequently
- Test event handling on different platforms
- Be mindful of event queue limits

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full event support
- **Mobile (iOS, Android)**: Full support
- **Web**: Full support
