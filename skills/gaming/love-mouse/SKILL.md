---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with mouse operations, cursor management, mouse events, or any mouse-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with mouse operations, cursor management, mouse events, or any mouse-related operations in LÖVE games.

## Common use cases
- Handling mouse clicks and movements
- Managing mouse cursor visibility and appearance
- Implementing drag-and-drop functionality
- Working with mouse wheel events
- Handling touch input that emulates mouse events

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Handling mouse click
```lua
function love.mousepressed(x, y, button, istouch)
  if button == 1 then  -- Left mouse button
    print("Clicked at: " .. x .. ", " .. y)
    -- Handle left click logic
  end
end
```

### Custom cursor
```lua
function love.load()
  -- Hide default cursor
  love.mouse.setVisible(false)

  -- Load custom cursor image
  cursorImage = love.graphics.newImage("cursor.png")
end

function love.draw()
  -- Draw custom cursor at mouse position
  local x, y = love.mouse.getPosition()
  love.graphics.draw(cursorImage, x, y)
end
```

## Best practices
- Handle both mouse and touch input for cross-platform compatibility
- Use appropriate cursor visibility for different game states
- Consider mouse acceleration and sensitivity on different platforms
- Handle mouse events efficiently to avoid performance issues
- Test mouse input on target platforms as behavior may vary

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full mouse support
- **Mobile (iOS, Android)**: Mouse events emulated from touch input
- **Web**: Full mouse support in browser environment
