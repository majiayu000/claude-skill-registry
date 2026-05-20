---
name: claude-computer-use-advanced
description: Advanced computer use patterns for UI automation, application control, and multi-step workflows using Claude's computer use tool. Use when automating desktop tasks, testing applications, analyzing screen content, controlling software programmatically, or building computer vision workflows. Supports zoom tool for enhanced vision on Opus 4.5, multi-step automation, and sophisticated application control.
---

# Claude Computer Use Advanced

## Overview

Claude's computer use tool enables AI agents to interact with desktop environments programmatically. This skill provides advanced patterns for building sophisticated UI automation workflows, testing applications, extracting data from screens, and controlling applications across operating systems.

Computer use represents a major advancement in AI capability - rather than relying on APIs, Claude can interact with any software the same way a human would: by viewing the screen, clicking elements, typing text, and using keyboard shortcuts. This makes it possible to automate virtually any desktop task that has a graphical interface.

**Core Capabilities**:
- Take screenshots and analyze visual content
- Click on screen elements using precise coordinates
- Type text and submit forms
- Press keyboard shortcuts and special keys
- Scroll, drag, and perform complex mouse operations
- Use zoom tool to inspect specific screen regions (Opus 4.5 only)
- Execute multi-step automation workflows
- Control applications and software programmatically

**Key Models**:
- **Claude Opus 4.5** (`computer_20251124`): Newest version with zoom tool for enhanced vision accuracy
- **Claude 4 / Sonnet 3.7** (`computer_20250124`): Stable version with full action support

## When to Use

Use computer use for these common scenarios:

**Desktop Automation**
- Batch processing repetitive tasks
- Form filling and data entry workflows
- File and folder management
- Configuration and setup automation
- Multi-application workflows

**Application Testing**
- Automated UI testing frameworks
- Cross-platform testing workflows
- Visual regression testing
- User interaction simulation
- Quality assurance automation

**Screen Analysis & Data Extraction**
- Extracting text and data from applications
- Analyzing visual layouts and designs
- Reading content from non-API systems
- Screenshot analysis and understanding
- OCR-like text extraction from screens

**Application Control & Integration**
- Controlling legacy applications without APIs
- Creating automation agents for closed systems
- Building RPA (Robotic Process Automation) workflows
- Orchestrating multi-application processes
- Software testing and validation

## Computer Use Tasks

### Task 1: Taking Screenshots

Screenshots form the foundation of computer use - Claude needs to see the screen to know what to do next.

**When to Use**:
- As the first action in any workflow
- Before clicking on elements (to get coordinates)
- To analyze the current application state
- To understand what's visible on screen
- After actions to verify results

**How It Works**:
The screenshot action captures the entire display and returns it as a base64-encoded image. Claude can then analyze the screenshot to understand the interface, identify elements, and determine the next action.

**Basic Example**:
```python
action = {
    "type": "screenshot"
}
```

**Coordinate System**:
- Origin (0, 0) is at the top-left of the screen
- X increases to the right
- Y increases downward
- Coordinates refer to pixel positions on the display

**Best Practices**:
1. Always start with a screenshot to establish the initial state
2. Take screenshots after significant actions to verify success
3. Use zoom tool (Opus 4.5) for precise element location
4. Consider display resolution when planning coordinates
5. Standard resolution: 1280x800 (recommended: 1024x768)

---

### Task 2: Clicking Elements

Clicking is the primary way to interact with UI elements - buttons, links, checkboxes, menu items, and any clickable interface element.

**When to Use**:
- Activating buttons and submitting forms
- Opening menus and selecting options
- Clicking links to navigate
- Toggling checkboxes and radio buttons
- Selecting items in lists or dropdowns

**How It Works**:
The click action takes x,y coordinates and sends a mouse click at that position. Claude uses the screenshot to identify element locations and then clicks on them.

**Basic Example**:
```python
action = {
    "type": "left_click",
    "coordinate": [640, 400]  # x, y from screenshot
}
```

**Coordinate Precision**:
- Aim for the center of clickable elements
- Use zoom tool (Opus 4.5) when precise coordinates are needed
- If click misses, take another screenshot and adjust
- Small elements may require zoomed region for accuracy

**Advanced Click Types**:
- `left_click`: Standard single click
- `right_click`: Opens context menus
- `double_click`: Selects text or activates double-click actions
- `middle_click`: Some applications use middle-click
- `click_holding`: Click and hold for drag operations

**Best Practices**:
1. Take a screenshot before clicking to find correct coordinates
2. Identify button/link boundaries visually
3. Use center coordinates for best accuracy
4. Verify clicks succeeded with follow-up screenshots
5. Handle missed clicks by retrying with adjusted coordinates

---

### Task 3: Typing Text & Form Input

Typing enables text input - entering data into forms, search boxes, command prompts, and text fields.

**When to Use**:
- Filling out form fields with text
- Entering search queries
- Typing commands or code
- Inputting credentials (in secure environments only)
- Text area and field population

**How It Works**:
The type action sends keyboard input character by character. The text is typed at the current cursor position, typically after clicking a text field.

**Basic Example**:
```python
# Click text field first
action = {"type": "left_click", "coordinate": [500, 300]}

# Then type text
action = {
    "type": "type",
    "text": "Hello, World!"
}
```

**Text Input Workflow**:
1. Take screenshot to see the form
2. Click on the target text field
3. Type the text
4. Optionally press Enter or Tab to submit/move to next field
5. Screenshot to verify input

**Special Characters**:
```python
# Use key action for special characters
action = {"type": "key", "key": "Return"}       # Enter key
action = {"type": "key", "key": "Tab"}          # Tab key
action = {"type": "key", "key": "BackSpace"}    # Delete character
action = {"type": "key", "key": "ctrl+a"}       # Select all
action = {"type": "key", "key": "ctrl+c"}       # Copy
action = {"type": "key", "key": "ctrl+v"}       # Paste
```

**Best Practices**:
1. Always click the text field first to focus it
2. Clear existing text with Ctrl+A and Delete if needed
3. Use Tab to move between form fields
4. Press Enter to submit forms
5. Take screenshots between actions to verify input

---

### Task 4: Keyboard Control & Special Keys

Keyboard actions provide precise control over keys, shortcuts, and special inputs beyond text typing.

**When to Use**:
- Pressing keyboard shortcuts (Ctrl+C, Ctrl+V, etc.)
- Using special keys (Enter, Tab, Escape, arrows)
- Navigating menus and dialogs with keyboard
- Using application-specific hotkeys
- Controlling focus and navigation

**How It Works**:
The key action presses keyboard keys or combinations. It can send single keys or key combinations (like Ctrl+A).

**Common Keys**:
```python
# Navigation
{"type": "key", "key": "Return"}      # Enter key
{"type": "key", "key": "Tab"}         # Tab to next field
{"type": "key", "key": "BackSpace"}   # Delete character
{"type": "key", "key": "Delete"}      # Delete forward
{"type": "key", "key": "Escape"}      # Escape/Cancel

# Arrows
{"type": "key", "key": "Up"}
{"type": "key", "key": "Down"}
{"type": "key", "key": "Left"}
{"type": "key", "key": "Right"}

# Shortcuts
{"type": "key", "key": "ctrl+a"}      # Select all
{"type": "key", "key": "ctrl+c"}      # Copy
{"type": "key", "key": "ctrl+v"}      # Paste
{"type": "key", "key": "ctrl+z"}      # Undo
{"type": "key", "key": "ctrl+s"}      # Save
{"type": "key", "key": "alt+Tab"}     # Switch windows
```

**Key Holding** (for drag operations):
```python
{"type": "key", "key": "shift", "held": True}  # Hold shift while clicking
```

**Best Practices**:
1. Use keyboard shortcuts when available
2. Tab through form fields instead of clicking each one
3. Use Escape to close dialogs or cancel operations
4. Combine arrow keys for navigation
5. Use Ctrl+A before typing to replace selected text

---

### Task 5: Using the Zoom Tool (Opus 4.5 Exclusive)

The zoom tool is a powerful feature exclusive to Claude Opus 4.5 that lets you inspect specific regions of the screen at full resolution, enabling precise element location and visual analysis.

**What It Does**:
The zoom tool captures a rectangular region of the screen and returns it at full resolution without downscaling. This allows Claude to see fine details, read small text, identify exact element boundaries, and determine precise click coordinates.

**When to Use**:
- Locating small UI elements accurately
- Reading fine-print text
- Analyzing icon details
- Identifying exact button positions
- Handling crowded interfaces
- Improving coordinate precision for clicks

**How It Works**:
You provide a rectangular region defined by coordinates [x1, y1, x2, y2] where:
- (x1, y1) = top-left corner of region
- (x2, y2) = bottom-right corner of region

**Basic Example**:
```python
# Zoom into a specific region to see details
action = {
    "type": "zoom",
    "coordinate": [400, 200, 800, 400]  # [x1, y1, x2, y2]
}
```

**Zoom Workflow Example**:
```python
# 1. Take full screenshot to understand layout
{"type": "screenshot"}

# 2. Identify region with uncertain element location
# Need to find exact position of "Submit" button

# 3. Zoom into that region for precise view
{"type": "zoom", "coordinate": [300, 350, 700, 450]}

# 4. With precise view, identify exact coordinates
# See "Submit" button at pixel position [550, 385]

# 5. Click with confidence
{"type": "left_click", "coordinate": [550, 385]}
```

**Region Selection**:
- Small regions (50x50) for individual elements
- Medium regions (200x200) for control groups
- Larger regions up to full screen
- Leave sufficient margins around target element

**Vision Accuracy Benefits**:
- Opus 4.5's improved vision can read text more accurately
- Zoom provides full resolution for detail inspection
- Better at identifying element boundaries
- Helps with crowded or complex UIs
- Reduces click coordinate errors

**Best Practices**:
1. Use zoom when initial screenshot doesn't clearly show element
2. Zoom into area 20-30 pixels beyond element on all sides
3. Use full region coordinates from screenshot
4. Zoom only when precision is critical
5. Combine with screenshots for optimal efficiency

---

### Task 6: Multi-Step Automation Workflows

Complex automation requires coordinating multiple actions across steps - this task covers orchestrating sophisticated workflows.

**When to Use**:
- Multi-application workflows
- Complex data entry processes
- Testing procedures with multiple steps
- Sequential automation tasks
- Conditional workflows (if this, then that)

**How It Works**:
Agent loops execute sequences of actions, using screenshots to understand results and determine next steps. The loop continues until the workflow is complete.

**Basic Agent Loop Pattern**:
```python
# Pseudo-code for agent loop
actions = []

# Step 1: Take screenshot to see initial state
actions.append({"type": "screenshot"})

# Step 2: Analyze screenshot and click button
actions.append({"type": "left_click", "coordinate": [100, 50]})

# Step 3: Take screenshot to see result
actions.append({"type": "screenshot"})

# Step 4: Fill form based on new state
actions.append({"type": "left_click", "coordinate": [200, 200]})
actions.append({"type": "type", "text": "Form data"})

# Step 5: Submit
actions.append({"type": "left_click", "coordinate": [200, 300]})

# Step 6: Verify with screenshot
actions.append({"type": "screenshot"})
```

**Error Recovery**:
```python
# If a click misses or action fails:
# 1. Take screenshot
# 2. Re-evaluate coordinates
# 3. Retry with adjusted position
# 4. Use zoom for precision if needed
# 5. Continue workflow
```

**Workflow State Tracking**:
- Track which steps are complete
- Remember important data extracted
- Maintain context about current application state
- Use screenshots as state checkpoints
- Save intermediate results for verification

**Best Practices**:
1. Take screenshots at workflow boundaries
2. Verify each major step with feedback
3. Handle unexpected states gracefully
4. Use Try/catch-like patterns for errors
5. Log important transitions for debugging

---

### Task 7: Application Control & System Interaction

Beyond UI clicks, computer use enables controlling applications, navigating system interfaces, and performing system-level tasks.

**When to Use**:
- Window/application navigation
- File system interaction (opening files, folders)
- System settings configuration
- Application launching and management
- Multi-window workflows

**How It Works**:
Standard mouse/keyboard operations work with any application:
- Clicking desktop, taskbar, menu items
- Opening file dialogs and navigating folders
- Using File/Edit/View menus
- Performing system-level operations
- Managing multiple windows

**Application Navigation Example**:
```python
# Open application menu
{"type": "left_click", "coordinate": [500, 10]}  # Menu bar

# Take screenshot to see menu
{"type": "screenshot"}

# Click menu item
{"type": "left_click", "coordinate": [520, 100]}

# Wait for dialog to open
{"type": "screenshot"}

# Interact with dialog
{"type": "left_click", "coordinate": [300, 300]}
```

**File System Navigation**:
```python
# Open File > Open dialog with keyboard shortcut
{"type": "key", "key": "ctrl+o"}

# Take screenshot to see file dialog
{"type": "screenshot"}

# Navigate to folder (multiple methods)
# Method 1: Type path directly
{"type": "type", "text": "/path/to/folder"}

# Method 2: Double-click folders in explorer
{"type": "double_click", "coordinate": [400, 200]}

# Select and open file
{"type": "left_click", "coordinate": [400, 250]}
{"type": "key", "key": "Return"}
```

**Multi-Window Workflows**:
```python
# Switch between windows
{"type": "key", "key": "alt+Tab"}

# Take screenshot to verify window
{"type": "screenshot"}

# Interact with new window
{"type": "left_click", "coordinate": [500, 400]}
```

**Best Practices**:
1. Use keyboard shortcuts when available
2. Navigate menus through visual screenshots
3. Handle different menu layouts gracefully
4. Use file dialog navigation carefully
5. Take screenshots between window switches

---

## Quick Start Example

Here's a complete example of a simple automation workflow - filling out a web form:

```python
import anthropic
import base64

client = anthropic.Anthropic(api_key="your-api-key")

# Define the computer use tool
tools = [
    {
        "name": "computer",
        "type": "computer_20251124",  # Opus 4.5 with zoom
        "display_width_px": 1024,
        "display_height_px": 768,
        "display_number": ":1"
    }
]

# Start with a screenshot
messages = [
    {
        "role": "user",
        "content": "Fill out the contact form with name 'John Doe' and email 'john@example.com', then submit it."
    }
]

# Add the screenshot action
messages.append({
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "First, take a screenshot to see the current state of the screen."
        }
    ]
})

# Create the request with beta header
response = client.messages.create(
    model="claude-opus-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=messages,
    headers={"anthropic-beta": "computer-use-2025-11-24"}
)

# Process the response - it will contain tool use actions
for content_block in response.content:
    if content_block.type == "tool_use":
        action = content_block.input

        # Execute the action and get result
        if action["type"] == "screenshot":
            # Return screenshot (base64 encoded)
            result = capture_screenshot()  # Your implementation
        elif action["type"] == "left_click":
            # Execute click
            result = click_at_coordinates(action["coordinate"])
        elif action["type"] == "type":
            # Type text
            result = type_text(action["text"])

        # Continue with the agent loop
        # ... (add result back to messages and continue)
```

## API Reference

For detailed API specifications, parameters, response formats, and advanced usage patterns, see:
- **`references/computer-use-api.md`** - Complete API documentation with all tool versions and action types

## Advanced Patterns

For sophisticated automation patterns, multi-step workflows, zoom tool techniques, and best practices:
- **`references/advanced-patterns.md`** - Advanced automation, error handling, and optimization

## Security & Deployment

For security considerations, safe deployment practices, and operational guidelines:
- **`references/security-deployment.md`** - Security, containerization, monitoring, and responsible use

## Security & Limitations

**Security Considerations**:
1. **Isolation**: Deploy in isolated virtual machines or containers with minimal privileges
2. **Network Control**: Restrict internet access via domain allowlists
3. **Credentials**: Avoid providing sensitive credentials unless absolutely necessary
4. **Confirmation**: Request human approval for significant decisions
5. **Input Validation**: Validate all user inputs to prevent prompt injection

**Known Limitations**:
1. **Latency**: Not suitable for time-sensitive interactive tasks
2. **Vision Accuracy**: Computer vision may misidentify elements or coordinates
3. **Application Support**: Spreadsheets and specialized applications can be unreliable
4. **Account Management**: Cannot reliably create accounts or share content on social platforms
5. **Prompt Injection**: Vulnerable to prompt injection in web-based environments
6. **Resolution**: Recommended maximum 1280x800 resolution
7. **Token Cost**: Screenshots consume tokens due to vision processing

## Related Skills

- **anthropic-expert** - Overview of Claude computer use and tool use capabilities
- **claude-opus-4-5-guide** - Opus 4.5 features including zoom tool enhancements
- **multi-ai-research** - Research patterns for investigating third-party applications

---

**Learn More**: Start with the Quick Start example above, then explore the reference guides for advanced patterns and complete API documentation.
