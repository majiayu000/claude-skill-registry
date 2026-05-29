---
name: task-master-viewer
description:
  Launch a Streamlit GUI for Task Master tasks.json editing. Use when users want a visual interface
  instead of CLI/MCP commands.
---

# Task Master Viewer

Visual GUI for managing Task Master `tasks.json` files.

## When to Use

**Use when:**

- User asks to "view tasks visually", "open task editor", "launch GUI", or "see tasks in browser"
- User wants to edit multiple tasks without typing commands
- User needs to reorganize task hierarchy
- CLI/MCP tools feel cumbersome

**Don't use when:**

- User is comfortable with CLI (`task-master list`, etc.)
- User wants to script or automate tasks
- Headless/server environment without browser

## Quick Start

### 1. Check Streamlit Installation

```bash
python -c "import streamlit" 2>/dev/null && echo "✓ Installed" || pip install -U streamlit
```

### 2. Launch Application

```bash
cd .claude/skills/task-master-viewer && streamlit run app.py
```

**Output:**

```
Local URL: http://localhost:8501
```

App opens automatically in user's browser.

### 3. Tell User

```
✓ Task Master editor is open at http://localhost:8501

To stop: Close browser tab and press Ctrl+C
```

## Technical Details

**File Location**: `.claude/skills/task-master-viewer/app.py`

**Dependencies**: `streamlit` (only requirement)

**Default Path**: `PROJECT_ROOT/.taskmaster/tasks/tasks.json`

**Port**: `8501` (auto-increments if busy)

**Theme**: Snowflake brand colors in `.streamlit/config.toml`

**Data Format**: Standard Task Master JSON with tagged task lists

## Stopping the App

**Foreground** (default):

```bash
# User presses Ctrl+C
```

**Kill Process**:

```bash
pkill -f "streamlit run"
```

**Background** (if needed):

```bash
cd .claude/skills/task-master-viewer
nohup streamlit run app.py > /dev/null 2>&1 &
echo $! > streamlit.pid

# To stop:
kill $(cat streamlit.pid)
```

## Common Issues

| Issue                          | Solution                                           |
| ------------------------------ | -------------------------------------------------- |
| "Address already in use"       | `pkill -f "streamlit run"` then restart            |
| "Module 'streamlit' not found" | `pip install streamlit`                            |
| Wrong directory error          | Must run from `.claude/skills/task-master-viewer/` |
| File not found                 | User sets path in sidebar settings                 |

## Best Practices

**Do:**

- ✅ Check/install Streamlit before launching
- ✅ Run from skill directory
- ✅ Tell user the URL
- ✅ Explain how to stop
- ✅ Mention all instructions are in the app

**Don't:**

- ❌ Leave running indefinitely
- ❌ Launch multiple instances
- ❌ Edit tasks.json while app is open
- ❌ Explain features (app has help text)

## Integration

Works alongside:

- Task Master CLI commands
- Task Master MCP tools
- Direct JSON editing (use "🔄 Reload" button)

## Example Response

**User**: "Can I see my tasks visually?"

**Agent**:

```
Installing Streamlit... ✓
Launching Task Master editor... ✓

Editor is open at http://localhost:8501

All instructions are in the app interface.
To stop: Close browser tab and press Ctrl+C.
```
