---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with file operations, directory management, file reading/writing, or any filesystem-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with file operations, directory management, file reading/writing, or any filesystem-related operations in LÖVE games.

## Common use cases
- Reading and writing files
- Managing directories and file paths
- Handling game save data and configuration files
- Working with compressed files and archives
- Accessing filesystem information and metadata

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Reading a file
```lua
-- Read the contents of a file
local content = love.filesystem.read("data.txt")
print(content)
```

### Writing to a file
```lua
-- Write data to a file
local success = love.filesystem.write("savegame.dat", gameData)
if success then
  print("Game saved successfully!")
end
```

## Best practices
- Use love.filesystem for all file operations to ensure cross-platform compatibility
- Handle file operations in love.load() or during non-critical game moments
- Always check if files exist before attempting to read them
- Use appropriate file formats for different data types
- Be mindful of filesystem permissions, especially on mobile platforms

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full filesystem support
- **Mobile (iOS, Android)**: Limited to sandboxed storage, some restrictions apply
- **Web**: Very limited filesystem access, mostly read-only operations
