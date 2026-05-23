---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with keyboard operations, key events, text input, or any keyboard-related operations in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with keyboard operations, key events, text input, or any keyboard-related operations in LÖVE games.

## Common use cases
- Handling keyboard input and key presses
- Managing text input and keyboard events
- Implementing keyboard-based game controls
- Working with keyboard modifiers and special keys
- Supporting international keyboard layouts

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Handling key presses
```lua
function love.keypressed(key, scancode, isrepeat)
  if key == "escape" then
    love.event.quit()
  elseif key == "space" then
    player.jump()
  elseif key == "w" or key == "up" then
    player.moveForward()
  end
end
```

### Text input
```lua
function love.textinput(text)
  -- Handle text input for chat or UI
  if chatting then
    chatMessage = chatMessage .. text
  end
end

function love.keypressed(key)
  if key == "backspace" and chatting then
    -- Remove last character
    chatMessage = chatMessage:sub(1, -2)
  elseif key == "return" and chatting then
    -- Send chat message
    sendChatMessage(chatMessage)
    chatMessage = ""
  end
end
```

## Best practices
- Handle both key names and scancodes appropriately
- Support keyboard remapping for accessibility
- Consider international keyboard layouts
- Test keyboard input on different platforms
- Be mindful of keyboard repeat behavior

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full keyboard support
- **Mobile (iOS, Android)**: Limited to on-screen keyboards
- **Web**: Full keyboard support in browser environment
