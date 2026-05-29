---
name: omni-vu
description: Screen capture, AI vision analysis, and GUI automation for macOS. Use when you need to see what's on screen, analyze UI state, detect changes, or automate mouse/keyboard actions.
---

# omni.vu - Visual Understanding & Automation

## Overview

omni.vu gives you eyes and hands on the user's macOS screen. Use it to:
- **See** what the user sees (screen capture)
- **Understand** UI state with AI vision
- **Detect** changes and wait for events
- **Act** with mouse and keyboard automation

## When to Use This Skill

### Proactively Use omni.vu When:
1. **Debugging UI issues** - "The button isn't working" → capture and analyze
2. **Verifying changes** - After modifying UI code, check if it rendered correctly
3. **Waiting for operations** - Build finishing, deployment completing, tests running
4. **Understanding context** - User describes something on screen you can't see
5. **Automating repetitive tasks** - Clicking through UI flows, filling forms
6. **Documentation** - Capturing screenshots of features

### Do NOT Use When:
- Reading/writing files (use Read/Write tools)
- Running terminal commands (use Bash)
- Making API calls (use appropriate tools)
- User hasn't granted screen recording permission

## Tool Reference

### Capture Tools

#### `vu` - Full Screen Capture
```
vu(monitor=0, save_to_history=True)
```
Captures the entire screen. Returns base64 image.

**Use when**: You need to see everything on screen.

#### `vu_window` - Window Capture
```
vu_window(window_id=None, title="VS Code", include_frame=False)
```
Captures a specific window by ID or title (partial match).

**Use when**: You only need one application's content.

**Workflow**:
1. Call `vu_list_windows` to see available windows
2. Find the window_id or use title matching
3. Call `vu_window` with that ID/title

#### `vu_region` - Region Capture
```
vu_region(x=100, y=100, width=500, height=300)
```
Captures a specific rectangle of the screen.

**Use when**: You need a precise area (error message, specific component).

#### `vu_list_windows` - List Windows
```
vu_list_windows(filter_app="Chrome")
```
Lists all visible windows with metadata.

**Returns**: List of `{window_id, title, owner, x, y, width, height}`

#### `vu_list_monitors` - List Displays
```
vu_list_monitors()
```
Lists connected displays with resolution and scale factor.

### Vision Tools

#### `vu_describe` - AI Vision Analysis
```
vu_describe(
    prompt="What errors are visible?",
    provider="claude",  # or openai, gemini, ollama
    max_tokens=1024,
    capture_first=True
)
```
Captures screen and analyzes with AI.

**Best prompts**:
- "Describe what you see on screen"
- "Are there any error messages visible?"
- "What is the state of the build/test output?"
- "Is the login form filled correctly?"
- "What color is the status indicator?"

**Providers**:
| Provider | Speed | Quality | Cost |
|----------|-------|---------|------|
| claude | Medium | Excellent | $$ |
| openai | Fast | Very Good | $$ |
| gemini | Fast | Good | $ |
| ollama | Slow | Varies | Free |

### Utility Tools

#### `vu_diff` - Change Detection
```
vu_diff(threshold=0.02, monitor=0)
```
Detects if screen changed since last capture.

**Returns**: `{changed: bool, diff_percentage: float}`

**Use for polling patterns**:
```python
# Wait for build to finish
while True:
    result = vu_diff(threshold=0.05)
    if result["changed"]:
        # Screen changed, check what happened
        analysis = vu_describe(prompt="Did the build succeed or fail?")
        break
    # Wait before checking again
```

#### `vu_history` - Capture History
```
vu_history(limit=10, capture_type="full_screen")
```
Gets recent capture metadata.

#### `vu_last` - Last Capture
```
vu_last()
```
Returns the most recent capture with image data.

**Use when**: You need to re-analyze without re-capturing.

#### `vu_status` - System Status
```
vu_status()
```
Returns system info: monitors, providers, safety settings.

### Automation Tools

#### `vu_click` - Mouse Click
```
vu_click(x=500, y=300, button="left", count=1)
```
Clicks at screen coordinates.

**Buttons**: `left`, `right`, `middle`
**Count**: 1 (single), 2 (double), 3 (triple)

**Safety**: Coordinates validated against screen bounds.

#### `vu_move` - Move Cursor
```
vu_move(x=500, y=300, duration_ms=0)
```
Moves cursor to position. Use `duration_ms` for animated movement.

#### `vu_drag` - Drag Operation
```
vu_drag(start_x=100, start_y=100, end_x=500, end_y=300, duration_ms=500)
```
Drags from start to end position.

**Safety**: Maximum 2000px drag distance.

#### `vu_scroll` - Scroll
```
vu_scroll(direction="down", amount=3, x=None, y=None)
```
Scrolls at current or specified position.

**Directions**: `up`, `down`, `left`, `right`
**Amount**: Lines to scroll (1-20)

#### `vu_type` - Type Text
```
vu_type(text="Hello World", delay_between_ms=0)
```
Types text character by character.

**Note**: Click on target field first!

#### `vu_hotkey` - Keyboard Shortcut
```
vu_hotkey(keys="cmd+s")
```
Executes keyboard shortcuts.

**Format**: `modifier+key` (e.g., `cmd+c`, `ctrl+shift+s`, `cmd+opt+i`)
**Modifiers**: `cmd`, `ctrl`, `alt`/`opt`, `shift`

**Blocked hotkeys** (for safety):
- `cmd+q` (quit)
- `cmd+shift+q` (logout)
- `cmd+opt+esc` (force quit)

## Common Workflows

### 1. Debug UI Issue
```
User: "The submit button doesn't do anything when I click it"

1. vu_describe(prompt="Describe the form and submit button state")
2. Analyze: Is button disabled? Is there validation error?
3. If needed: vu_window(title="Chrome") for focused capture
4. Check console: vu_describe(prompt="Are there any errors in the developer console?")
```

### 2. Verify Build/Deploy
```
User: "Run the build and let me know when it's done"

1. Run: npm run build (via Bash)
2. Loop: vu_diff(threshold=0.05)
3. When changed: vu_describe(prompt="What is the build status? Did it succeed or fail?")
4. Report result
```

### 3. Fill a Form
```
User: "Fill out the registration form with test data"

1. vu_describe(prompt="What form fields are visible?")
2. vu_click(x=field_x, y=field_y)  # Click first field
3. vu_type(text="testuser@example.com")
4. vu_hotkey(keys="tab")  # Move to next field
5. vu_type(text="Test User")
6. Continue for each field...
7. vu_click(x=submit_x, y=submit_y)  # Submit
8. vu_describe(prompt="Was the form submitted successfully?")
```

### 4. Navigate UI
```
User: "Open the settings panel in VS Code"

1. vu_list_windows(filter_app="Code")
2. vu_window(title="Code")  # Capture VS Code
3. vu_hotkey(keys="cmd+,")  # Open settings
4. vu_diff()  # Wait for settings to open
5. vu_describe(prompt="Are the VS Code settings now visible?")
```

### 5. Monitor for Changes
```
User: "Watch the dashboard and tell me when the status changes"

1. vu()  # Initial capture
2. Loop every 5 seconds:
   - vu_diff(threshold=0.02)
   - If changed: vu_describe(prompt="What changed on the dashboard?")
3. Report changes to user
```

## Best Practices

### 1. Capture Before Acting
Always capture and analyze before clicking/typing:
```
❌ Bad: vu_click(x=500, y=300)  # Hope it's the right spot

✅ Good:
1. vu_describe(prompt="Where is the submit button?")
2. Parse coordinates from description
3. vu_click(x=parsed_x, y=parsed_y)
```

### 2. Use Appropriate Capture Scope
```
Full screen → General context, multi-app workflows
Window → Single app focus, cleaner output
Region → Specific element, faster/smaller
```

### 3. Specific Vision Prompts
```
❌ Vague: "What do you see?"

✅ Specific:
- "Is there an error message visible? If so, what does it say?"
- "What is the status of the test runner? Passing, failing, or running?"
- "List all form fields visible and their current values"
```

### 4. Rate Limit Automation
Don't spam clicks. Wait between actions:
```
vu_click(x=100, y=100)
# Wait for UI response
vu_diff(threshold=0.01)
vu_click(x=200, y=200)
```

### 5. Verify After Actions
Always verify automation succeeded:
```
vu_type(text="hello@example.com")
vu_describe(prompt="What text is now in the email field?")
```

## Troubleshooting

### "Permission denied" or blank captures
→ Grant Screen Recording permission: System Settings > Privacy > Screen Recording

### Automation not working
→ Grant Accessibility permission: System Settings > Privacy > Accessibility

### Vision analysis failing
→ Check API keys in environment variables
→ Try different provider: `vu_describe(provider="openai")`

### Coordinates seem off
→ Retina display? Coordinates are in logical points, not pixels
→ Multi-monitor? Check `vu_list_monitors()` for display arrangement

### Hotkey blocked
→ Some dangerous hotkeys (cmd+q) are blocked for safety
→ Unblock in config if absolutely necessary

## Configuration

Environment variables:
```bash
OMNI_VU_ANTHROPIC_API_KEY=sk-ant-...    # For Claude vision
OMNI_VU_OPENAI_API_KEY=sk-...           # For GPT-4 vision
OMNI_VU_DEFAULT_PROVIDER=claude          # Default AI provider
OMNI_VU_SAFETY_LEVEL=medium              # low/medium/high
```

History stored at: `~/.omni.vu/captures/`
