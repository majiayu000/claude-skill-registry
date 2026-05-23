---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with font operations, text display, text formatting, or any font-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with font operations, text display, text formatting, or any font-related operations in LÖVE games.

## Common use cases
- Loading and managing font files
- Rendering text with different styles and sizes
- Working with text formatting and layout
- Handling international text and Unicode characters
- Implementing custom text rendering effects

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Loading and using fonts
```lua
-- Load a font file
local font = love.graphics.newFont("arial.ttf", 24)

-- Set as default font
love.graphics.setFont(font)

-- Draw text
love.graphics.print("Hello World!", 100, 100)
```

### Text formatting
```lua
-- Create fonts with different styles
local titleFont = love.graphics.newFont(36)
local bodyFont = love.graphics.newFont(18)
local boldFont = love.graphics.newFont("bold.ttf", 20)

function love.draw()
  love.graphics.setFont(titleFont)
  love.graphics.print("Game Title", 100, 50)

  love.graphics.setFont(bodyFont)
  love.graphics.printf("This is a paragraph of text that will be wrapped to fit within the specified width.", 100, 150, 400, "left")

  love.graphics.setFont(boldFont)
  love.graphics.print("Important Message!", 100, 300)
end
```

## Best practices
- Load fonts during initialization to avoid runtime delays
- Use appropriate font sizes for different screen resolutions
- Consider memory usage when loading multiple fonts
- Handle font loading errors gracefully
- Test text rendering on target platforms

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full font support
- **Mobile (iOS, Android)**: Full support with some font limitations
- **Web**: Good support but some fonts may not be available
