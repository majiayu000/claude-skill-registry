---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with system operations, platform detection, system information retrieval, or any system-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with system operations, platform detection, system information retrieval, or any system-related operations in LÖVE games.

## Common use cases
- Retrieving system and platform information
- Detecting operating system and hardware capabilities
- Accessing system-specific features
- Handling platform-specific behavior
- Managing system resources and capabilities

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Platform detection
```lua
-- Detect current platform
local platform = love.system.getOS()
if platform == "Windows" then
  -- Windows-specific code
elseif platform == "OS X" then
  -- macOS-specific code
elseif platform == "Linux" then
  -- Linux-specific code
end
```

### System information
```lua
-- Get system information
local cpuCores = love.system.getProcessorCount()
local ramMB = love.system.getMemoryUsage() / (1024 * 1024)

print("CPU Cores: " .. cpuCores)
print("Memory Usage: " .. string.format("%.2f", ramMB) .. " MB")
```

## Best practices
- Use system information for platform-specific optimizations
- Handle platform differences gracefully
- Consider performance when accessing system information frequently
- Test on target platforms for compatibility
- Be mindful of privacy when accessing system information

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full system support
- **Mobile (iOS, Android)**: Limited system information access
- **Web**: Very limited system access due to browser restrictions
