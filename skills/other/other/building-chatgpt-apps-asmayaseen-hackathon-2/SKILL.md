---
name: building-chatgpt-apps
description: |
  Guides creation of ChatGPT Apps with interactive widgets using OpenAI Apps SDK and MCP servers.
  Use when building ChatGPT custom apps with visual UI components, embedded widgets, or rich
  interactive experiences. Covers widget architecture, MCP server setup with FastMCP, response
  metadata, and Developer Mode configuration. NOT when building standard MCP servers without
  widgets (use building-mcp-servers skill instead).
---

# ChatGPT Apps SDK Development Guide

## Overview

Create ChatGPT Apps with interactive widgets that render rich UI inside ChatGPT conversations. Apps combine MCP servers (providing tools) with embedded HTML widgets that communicate via the `window.openai` API.

---

## window.openai API Reference

Widgets communicate with ChatGPT through these APIs:

### sendFollowUpMessage (Recommended for Actions)

Send a follow-up prompt to ChatGPT on behalf of the user:

```javascript
// Trigger a follow-up conversation
if (window.openai?.sendFollowUpMessage) {
  await window.openai.sendFollowUpMessage({
    prompt: 'Summarize this chapter for me'
  });
}
```

**Use for**: Action buttons that suggest next steps (summarize, explain, etc.)

### toolOutput

Send structured data back from widget interactions:

```javascript
// Send data back to ChatGPT
if (window.openai?.toolOutput) {
  window.openai.toolOutput({
    action: 'chapter_selected',
    chapter: 1,
    title: 'Introduction'
  });
}
```

**Use for**: Selections, form submissions, user choices that feed into tool responses.

### callTool

Call another MCP tool from within a widget:

```javascript
// Call a tool directly
if (window.openai?.callTool) {
  await window.openai.callTool({
    name: 'read-chapter',
    arguments: { chapter: 2 }
  });
}
```

**Use for**: Navigation between content, chaining tool calls.

---

## Critical: Button Interactivity Limitations

**Important Discovery**: Widget buttons may render as **static UI elements** rather than interactive JavaScript buttons. ChatGPT renders widgets in a sandboxed iframe where some click handlers don't fire reliably.

### What Works
- `sendFollowUpMessage` - Reliably triggers follow-up prompts
- Simple onclick handlers for `toolOutput` calls
- CSS hover effects and visual feedback

### What May Not Work
- Complex interactive JavaScript (selection APIs, etc.)
- Multiple chained tool calls from buttons
- `window.getSelection()` for text selection features

### Recommended Pattern: Suggestion Buttons

Instead of complex interactions, use simple buttons that suggest prompts:

```html
<div class="action-buttons">
  <button class="btn btn-primary" id="summarizeBtn">
    📝 Summarize Chapter
  </button>
  <button class="btn btn-primary" id="explainBtn">
    💡 Explain Key Concepts
  </button>
</div>

<script>
document.getElementById('summarizeBtn')?.addEventListener('click', async () => {
  if (window.openai?.sendFollowUpMessage) {
    await window.openai.sendFollowUpMessage({
      prompt: 'Summarize this chapter for me'
    });
  }
});

document.getElementById('explainBtn')?.addEventListener('click', async () => {
  if (window.openai?.sendFollowUpMessage) {
    await window.openai.sendFollowUpMessage({
      prompt: 'Explain the key concepts from this chapter'
    });
  }
});
</script>
```

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                        ChatGPT UI                                │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Widget (iframe)                          ││
│  │   HTML + CSS + JS                                          ││
│  │   Calls: window.openai.toolOutput({action: "...", ...})    ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│                     ChatGPT Backend                              │
│                              │                                   │
│                              ▼                                   │
│              MCP Server (FastMCP + HTTP)                         │
│              - Tools: open-book, read-chapter, etc.              │
│              - Resources: widget HTML (text/html+skybridge)      │
│              - Response includes: _meta["openai.com/widget"]     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

1. **Create MCP server** with FastMCP and widget resources
2. **Define widget HTML** that uses `window.openai.toolOutput`
3. **Add response metadata** with `_meta["openai.com/widget"]`
4. **Expose via ngrok** for ChatGPT access
5. **Register in ChatGPT** Developer Mode settings

---

## Widget HTML Requirements

### Basic Widget Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Widget</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 24px;
      color: white;
    }
    .container { max-width: 600px; margin: 0 auto; }
    .card {
      background: rgba(255,255,255,0.95);
      color: #333;
      padding: 24px;
      border-radius: 16px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    .btn {
      background: #667eea;
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 16px;
    }
    .btn:hover { background: #5a6fd6; }
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>Widget Title</h1>
      <p>Widget content here</p>
      <button class="btn" onclick="handleAction()">Click Me</button>
    </div>
  </div>
  <script>
    function handleAction() {
      // Communicate back to ChatGPT
      if (window.openai && window.openai.toolOutput) {
        window.openai.toolOutput({
          action: "button_clicked",
          data: { timestamp: Date.now() }
        });
      }
    }
  </script>
</body>
</html>
```

### Key Widget Rules

1. **Always check `window.openai.toolOutput`** before calling
2. **Use inline styles** - external CSS may not load reliably
3. **Keep widgets self-contained** - all HTML/CSS/JS in one file
4. **Test with actual ChatGPT** - browser preview won't have `window.openai`

---

## MCP Server Setup (FastMCP Python)

### Project Structure

```
my_chatgpt_app/
├── main.py              # FastMCP server with widgets
├── requirements.txt     # Dependencies
└── .env                 # Environment variables
```

### requirements.txt

```
mcp[cli]>=1.9.2
uvicorn>=0.32.0
httpx>=0.28.0
python-dotenv>=1.0.0
```

### main.py Template

```python
import mcp.types as types
from mcp.server.fastmcp import FastMCP

# Widget MIME type for ChatGPT
MIME_TYPE = "text/html+skybridge"

# Define your widget HTML
MY_WIDGET = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: sans-serif; padding: 20px; }
    .container { max-width: 500px; margin: 0 auto; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Hello from Widget!</h1>
    <p>This content renders inside ChatGPT.</p>
  </div>
</body>
</html>'''

# Widget registry
WIDGETS = {
    "main-widget": {
        "uri": "ui://widget/main.html",
        "html": MY_WIDGET,
        "title": "My Widget",
    },
}

# Create FastMCP server
mcp = FastMCP("My ChatGPT App")


@mcp.resource(
    uri="ui://widget/{widget_name}.html",
    name="Widget Resource",
    mime_type=MIME_TYPE
)
def widget_resource(widget_name: str) -> str:
    """Serve widget HTML."""
    widget_key = f"{widget_name}"
    if widget_key in WIDGETS:
        return WIDGETS[widget_key]["html"]
    return WIDGETS["main-widget"]["html"]


def _embedded_widget_resource(widget_id: str) -> types.EmbeddedResource:
    """Create embedded widget resource for tool response."""
    widget = WIDGETS[widget_id]
    return types.EmbeddedResource(
        type="resource",
        resource=types.TextResourceContents(
            uri=widget["uri"],
            mimeType=MIME_TYPE,
            text=widget["html"],
            title=widget["title"],
        ),
    )


def listing_meta() -> dict:
    """Tool metadata for ChatGPT tool listing."""
    return {
        "openai.com/widget": {
            "uri": WIDGETS["main-widget"]["uri"],
            "title": WIDGETS["main-widget"]["title"]
        }
    }


def response_meta() -> dict:
    """Response metadata with embedded widget."""
    return {
        "openai.com/widget": _embedded_widget_resource("main-widget")
    }


@mcp.tool(
    annotations={
        "title": "My Tool",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
    _meta=listing_meta(),
)
def my_tool() -> types.CallToolResult:
    """Description of what this tool does."""
    return types.CallToolResult(
        content=[
            types.TextContent(
                type="text",
                text="Tool executed successfully!"
            )
        ],
        structuredContent={
            "status": "success",
            "message": "Data for the widget"
        },
        _meta=response_meta(),
    )


if __name__ == "__main__":
    import uvicorn
    print("Starting MCP Server on http://localhost:8001")
    print("Connect via: https://your-tunnel.ngrok-free.app/mcp")
    uvicorn.run(
        "main:mcp.app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
```

---

## Response Metadata Format

### Critical: `_meta["openai.com/widget"]`

Tool responses MUST include widget metadata:

```python
types.CallToolResult(
    content=[types.TextContent(type="text", text="...")],
    structuredContent={"key": "value"},  # Data for widget
    _meta={
        "openai.com/widget": types.EmbeddedResource(
            type="resource",
            resource=types.TextResourceContents(
                uri="ui://widget/my-widget.html",
                mimeType="text/html+skybridge",
                text=WIDGET_HTML,
                title="My Widget",
            ),
        )
    },
)
```

### structuredContent

Data passed to the widget. The widget can access this via `window.openai` APIs.

---

## Development Setup

### 1. Start Local Server

```bash
cd my_chatgpt_app
python main.py
# Server runs on http://localhost:8001
```

### 2. Start ngrok Tunnel

```bash
ngrok http 8001
# Get URL like: https://abc123.ngrok-free.app
```

### 3. Register in ChatGPT

1. Go to https://chatgpt.com/apps
2. Click Settings (gear icon)
3. Enable **Developer mode**
4. Click **Create app**
5. Fill in:
   - **Name**: Your App Name
   - **MCP Server URL**: `https://abc123.ngrok-free.app/mcp`
   - **Authentication**: No Auth (for development)
6. Check "I understand and want to continue"
7. Click **Create**

### 4. Test the App

1. Start a new chat in ChatGPT
2. Type `@` to see available apps
3. Select your app
4. Ask it to use your tool

---

## Common Issues and Solutions

### Widget Shows "Loading..." Forever

**Cause**: Widget HTML not being delivered correctly.

**Solution**:
1. Check server logs for `CallToolRequest` processing
2. Verify `_meta["openai.com/widget"]` in response
3. Ensure MIME type is `text/html+skybridge`

### Cached Widget Not Updating

**Cause**: ChatGPT caches widgets aggressively.

**Solution**:
1. Delete the app in Settings > Apps
2. Kill server and ngrok
3. Start fresh ngrok tunnel (new URL)
4. Create new app with new URL
5. Test in new conversation

### Widget JavaScript Errors

**Cause**: `window.openai` not available.

**Solution**: Always check before calling:
```javascript
if (window.openai && window.openai.toolOutput) {
  window.openai.toolOutput({...});
}
```

### Tool Not Showing in @mentions

**Cause**: MCP server not connected or tools not registered.

**Solution**:
1. Check server is running and accessible via ngrok URL
2. Verify ngrok tunnel is active: `curl https://your-url.ngrok-free.app/mcp`
3. Check server logs for `ListToolsRequest`

---

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ building-chatgpt-apps skill ready`

## If Verification Fails

1. Run diagnostic: Check references/ folder exists
2. Check: All reference files present
3. **Stop and report** if still failing

---

## References

- [Complete Template](references/complete_template.md) - Ready-to-use server + widget template
- [Widget Patterns](references/widget_patterns.md) - HTML/CSS/JS widget examples
- [Response Structure](references/response_structure.md) - Metadata format details
- [Debugging Guide](references/debugging.md) - Troubleshooting common issues