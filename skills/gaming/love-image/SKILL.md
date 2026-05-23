---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with image operations, texture management, image data manipulation, or any image-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with image operations, texture management, image data manipulation, or any image-related operations in LÖVE games.

## Common use cases
- Loading and processing image files
- Managing image data and textures
- Performing image transformations and manipulations
- Working with compressed image formats
- Handling image metadata and properties

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Loading an image
```lua
-- Load an image file
local imageData = love.image.newImageData("texture.png")
local image = love.graphics.newImage(imageData)
```

### Creating image data
```lua
-- Create new image data
local width, height = 256, 256
local imageData = love.image.newImageData(width, height)

-- Modify pixel data
for y = 0, height-1 do
  for x = 0, width-1 do
    local r = x / width
    local g = y / height
    local b = 0.5
    imageData:setPixel(x, y, r, g, b, 1)
  end
end

-- Create image from data
local image = love.graphics.newImage(imageData)
```

## Best practices
- Load images during initialization to avoid runtime delays
- Use appropriate image formats for different use cases
- Consider memory usage when working with large images
- Handle image loading errors gracefully
- Test image formats on target platforms

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full image support
- **Mobile (iOS, Android)**: Full support with some format limitations
- **Web**: Good support but some formats may not be available
