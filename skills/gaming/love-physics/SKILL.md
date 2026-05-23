---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with physics operations, collision detection, rigid body dynamics, or any physics-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with physics operations, collision detection, rigid body dynamics, or any physics-related operations in LÖVE games.

## Common use cases
- Creating physics-based game mechanics
- Implementing realistic object interactions
- Handling collision detection and response
- Working with rigid bodies and constraints
- Simulating real-world physics behavior

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Creating a physics world
```lua
-- Create a physics world
local world = love.physics.newWorld(0, 9.81 * 64, true)  -- gravity: 0, 9.81*64

-- Create a ground body
local ground = love.physics.newBody(world, 400, 550)
local groundShape = love.physics.newRectangleShape(800, 50)
local groundFixture = love.physics.newFixture(ground, groundShape)
```

### Physics object
```lua
-- Create a dynamic physics object
local ballBody = love.physics.newBody(world, 400, 100, "dynamic")
local ballShape = love.physics.newCircleShape(20)
local ballFixture = love.physics.newFixture(ballBody, ballShape, 1)

-- Apply force to the object
ballBody:applyLinearImpulse(100, -500)
```

## Best practices
- Use appropriate physics scale for your game
- Consider performance implications of complex physics simulations
- Handle physics collisions and contacts efficiently
- Test physics behavior on target platforms
- Be mindful of physics accuracy vs performance trade-offs

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full physics support
- **Mobile (iOS, Android)**: Full support but performance may vary
- **Web**: Good support with some limitations
