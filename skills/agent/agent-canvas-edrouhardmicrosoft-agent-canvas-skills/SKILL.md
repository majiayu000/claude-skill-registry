---
name: agent-canvas
description: Interactive element picker for web pages. Opens a browser with click-to-select UI overlay. Use when you need to let users visually select DOM elements, identify element selectors, or get detailed element information interactively. Triggers on "select an element", "pick element", "let me choose", "which element", or any interactive element selection task. Integrates with agent-eyes for visual context.
---

# Agent Canvas

Interactive element picker that opens a browser window with a DevTools-like selection overlay. Users hover to highlight elements and click to select. Returns detailed element info including selector, bounding box, and computed styles.

## First-Time Setup

**Before first use**, verify dependencies are installed:

```bash
uv run .claude/skills/agent-canvas-setup/scripts/check_setup.py check
```

If checks fail, ask user which installation scope they prefer and run:

```bash
# Recommended: minimal footprint, uv manages deps on-demand
uv run .claude/skills/agent-canvas-setup/scripts/check_setup.py install --scope temporary

# Alternative: create .venv in project
uv run .claude/skills/agent-canvas-setup/scripts/check_setup.py install --scope local
```

See `agent-canvas-setup` skill for full details on installation options.

## Quick Start for AI Agents

When using agent-canvas, **always follow this pattern**:

1. **Launch the picker** (browser opens for user interaction)
2. **Wait for browser to close** (user finishes selecting/editing)
3. **Read session from disk** (NOT from stdout - it may be lost)

```bash
# 1. Launch (user interacts with browser)
uv run .claude/skills/agent-canvas/scripts/agent_canvas.py pick http://localhost:3000 --with-edit --with-eyes

# 2. After browser closes, read the latest session
SESSION_ID=$(ls -t .canvas/sessions/ | head -1)
cat .canvas/sessions/$SESSION_ID/session.json | jq '.summary'
```

## Commands

```bash
SKILL_DIR=".claude/skills/agent-canvas/scripts"
```

### Pick Element

Open browser with element picker overlay. Streams selection events as JSON lines until window is closed:

```bash
# Basic pick - opens browser, streams selections as JSON lines
uv run $SKILL_DIR/agent_canvas.py pick http://localhost:3000

# Pick with agent-eyes integration (adds screenshot + detailed styles per selection)
uv run $SKILL_DIR/agent_canvas.py pick http://localhost:3000 --with-eyes

# Pick with edit panel (floating DevTools for live style editing)
uv run $SKILL_DIR/agent_canvas.py pick http://localhost:3000 --with-edit

# Full workflow: picker + edit panel + agent-eyes (recommended)
uv run $SKILL_DIR/agent_canvas.py pick http://localhost:3000 --with-edit --with-eyes

# Save all selections and edits to file when done
uv run $SKILL_DIR/agent_canvas.py pick http://localhost:3000 --with-edit --output ./session.json
```

**User interaction:**
1. Browser opens with blue highlight overlay
2. Hover over elements to see selector labels
3. Click to select (overlay flashes green, counter increments)
4. Keep clicking to select more elements
5. Close browser window when done

**Streamed output (JSON lines):**
```json
{"event": "session_started", "url": "http://localhost:3000", "timestamp": "...", "features": {"picker": true, "eyes": true, "edit": true}}
{"event": "selection", "index": 1, "timestamp": "...", "element": {"tag": "button", "selector": "#submit", ...}}
{"event": "style_change", "timestamp": "...", "selector": "#submit", "property": "backgroundColor", "newValue": "#ff0000"}
{"event": "session_ended", "timestamp": "...", "total_selections": 1, "total_edits": 1}
```

With `--with-eyes`, each selection event also includes `eyes` (detailed styles) and `screenshot` fields.
With `--with-edit`, style changes made in the floating panel are emitted as `style_change` events.

### Watch for Changes

Monitor page for DOM changes, capture screenshots on each change:

```bash
# Watch with default 2s interval
uv run $SKILL_DIR/agent_canvas.py watch http://localhost:3000

# Custom interval
uv run $SKILL_DIR/agent_canvas.py watch http://localhost:3000 --interval 5

# Custom output directory
uv run $SKILL_DIR/agent_canvas.py watch http://localhost:3000 --output-dir ./snapshots
```

Outputs JSON events to stdout:
```json
{"event": "watch_started", "url": "http://localhost:3000", "interval": 2.0}
{"event": "change_detected", "iteration": 1, "timestamp": "...", "screenshot": ".canvas/screenshots/..."}
```

## Typical Workflow

1. **Let user select element:**
   ```bash
   uv run $SKILL_DIR/agent_canvas.py pick http://localhost:3000 --with-eyes
   ```

2. **Use returned selector for further analysis:**
   ```bash
   # Get accessibility info for selected element
   uv run .claude/skills/agent-eyes/scripts/agent_eyes.py a11y http://localhost:3000 --selector "#selected-element"
   ```

3. **Make changes to the element's styles/content**

4. **Verify changes with agent-eyes:**
   ```bash
   uv run .claude/skills/agent-eyes/scripts/agent_eyes.py screenshot http://localhost:3000
   ```

## Integration with Agent Eyes

When `--with-eyes` flag is used, agent-canvas calls agent-eyes to:
1. Get detailed element description (computed styles, attributes, visibility)
2. Take a screenshot of the selected element

This provides comprehensive visual context for the AI agent to understand and modify the selected element.

## Integration with Canvas Edit

When `--with-edit` flag is used, agent-canvas loads the canvas-edit floating panel:
1. Users can visually adjust styles (colors, typography, spacing) 
2. Changes apply live to the page for preview
3. Style change events stream alongside selection events
4. The panel uses Shadow DOM, so it's invisible to agent-eyes screenshots

**Recommended workflow:**
```bash
uv run $SKILL_DIR/agent_canvas.py pick http://localhost:3000 --with-edit --with-eyes
```
This gives users full control to select elements, preview style changes, while the agent receives both the visual context and the specific CSS changes to implement.

## Session Artifacts (IMPORTANT)

Sessions are **automatically saved** to `.canvas/sessions/<sessionId>/` regardless of how the command is run. This is the **primary way to retrieve session data** - do NOT rely on capturing stdout.

### After Browser Closes - Read the Session

```bash
# List all sessions (most recent first)
ls -lt .canvas/sessions/ | head -5

# Read the latest session
cat .canvas/sessions/$(ls -t .canvas/sessions/ | head -1)/session.json

# Or use jq for formatted output
cat .canvas/sessions/$(ls -t .canvas/sessions/ | head -1)/session.json | jq '.summary'
```

### Session Structure

```
.canvas/sessions/<sessionId>/
├── session.json    # Full event log, selections, edits, screenshots (base64)
└── changes.json    # Extracted save_request (if user clicked "Save All to Code")
```

### Key Fields in session.json

```json
{
  "sessionId": "ses-abc123",
  "url": "http://localhost:3000",
  "summary": {
    "totalSelections": 5,
    "totalEdits": 3,
    "hasSaveRequest": true  // <-- Check this! false = user didn't save changes
  },
  "events": {
    "selections": [...],  // Element selection events with screenshots
    "edits": [...]        // Style/text changes from edit panel
  }
}
```

### Checking What Changed

```bash
# Quick summary
cat .canvas/sessions/<sessionId>/session.json | jq '.summary'

# See all selections (element info)
cat .canvas/sessions/<sessionId>/session.json | jq '.events.selections[] | {selector: .payload.element.selector, text: .payload.element.text}'

# See all edits
cat .canvas/sessions/<sessionId>/session.json | jq '.events.edits'

# Check if save was requested (required for canvas-apply)
cat .canvas/sessions/<sessionId>/session.json | jq '.summary.hasSaveRequest'
```

## Notes

- Browser launches in **visible mode** for `pick` command (user interaction required)
- Browser runs **headless** for `watch` command
- Selection events stream as JSON lines to stdout in real-time
- **Session artifacts are always saved to disk** - use these instead of stdout capture
- Close the browser window to end the session
- Overlay elements are excluded from selection
