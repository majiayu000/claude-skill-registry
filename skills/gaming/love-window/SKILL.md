---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with window operations, display settings, fullscreen modes, or any window-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with window operations, display settings, fullscreen modes, or any window-related operations in LÖVE games.

## Common use cases
- Creating and managing game windows
- Handling window resizing and display modes
- Working with multiple monitors and display settings
- Managing window properties (title, icon, etc.)
- Handling fullscreen and windowed modes

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Creating a window
```lua
-- Set window properties in love.conf
function love.conf(t)
  t.window.title = "My Awesome Game"
  t.window.width = 800
  t.window.height = 600
  t.window.fullscreen = false
end
```

### Handling window resize
```lua
function love.resize(w, h)
  -- Update game view to match new window size
  gameWidth, gameHeight = w, h
  -- Recalculate any UI elements or camera settings
end
```

## Best practices
- Set window properties in love.conf() for best results
- Handle window resize events gracefully
- Test different display modes on target platforms
- Consider aspect ratio when designing for multiple resolutions
- Be mindful of fullscreen performance implications

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full window management support
- **Mobile (iOS, Android)**: Limited window control, mostly fullscreen
- **Web**: Browser window management with some limitations
