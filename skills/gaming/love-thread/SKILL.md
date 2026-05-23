---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with multi-threading, parallel processing, background tasks, or any thread-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with multi-threading, parallel processing, background tasks, or any thread-related operations in LÖVE games.

## Common use cases
- Running CPU-intensive operations in background threads
- Implementing parallel processing for performance
- Handling long-running tasks without blocking the main game loop
- Managing inter-thread communication and synchronization
- Loading resources asynchronously

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Creating a worker thread
```lua
-- Create and start a worker thread
local thread = love.thread.newThread("worker.lua")
thread:start()

-- Send data to the thread
thread:send("process", gameData)
```

### Thread communication
```lua
-- In main thread
local channel = love.thread.getChannel("results")
local result = channel:demand()  -- Wait for result

-- In worker thread
local channel = love.thread.getChannel("results")
channel:push(computedResult)
```

## Best practices
- Use threads for CPU-intensive tasks, not I/O operations
- Minimize data transfer between threads
- Handle thread errors gracefully
- Avoid excessive thread creation
- Test thread behavior on target platforms

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full threading support
- **Mobile (iOS, Android)**: Limited threading support
- **Web**: No threading support (single-threaded JavaScript)
