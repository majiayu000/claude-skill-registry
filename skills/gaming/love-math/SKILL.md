---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with mathematical operations, random number generation, geometric calculations, or any math-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with mathematical operations, random number generation, geometric calculations, or any math-related operations in LÖVE games.

## Common use cases
- Performing mathematical calculations and transformations
- Generating random numbers for game mechanics
- Working with vectors and matrices
- Implementing geometric algorithms
- Handling noise generation and procedural content

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Random number generation
```lua
-- Generate random numbers
local randomValue = love.math.random()  -- 0.0 to 1.0
local randomInt = love.math.random(1, 100)  -- 1 to 100
```

### Vector operations
```lua
-- Create and manipulate vectors
local vec1 = {x = 10, y = 20}
local vec2 = {x = 5, y = 15}

-- Vector addition
local result = {
  x = vec1.x + vec2.x,
  y = vec1.y + vec2.y
}
```

## Best practices
- Use love.math.random() with proper seeding for reproducibility
- Consider performance implications of complex mathematical operations
- Use appropriate data types for mathematical calculations
- Test mathematical algorithms thoroughly
- Be mindful of floating-point precision issues

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full math support
- **Mobile (iOS, Android)**: Full support
- **Web**: Full support
