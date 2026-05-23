---
name: building-chatgpt-apps
description: Guides creation of ChatGPT Apps with interactive widgets using the Apps SDK and MCP servers. Use when building ChatGPT custom apps with visual UI components, embedded widgets, or rich interactive experiences. Covers widget architecture, MCP server setup with FastMCP, response metadata, and Developer Mode configuration. NOT when building standard MCP servers without widgets (use building-mcp-servers skill instead).
---

# Apps SDK Development Guide

## Overview

Create ChatGPT Apps with interactive widgets that render rich UI inside ChatGPT conversations. The Apps SDK combines MCP servers (providing tools) with embedded HTML widgets that communicate via the `window.openai` API.

**Official Documentation**: https://developers.openai.com/apps-sdk/
**Examples Repository**: https://github.com/openai/openai-apps-sdk-examples

## Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        ChatGPT UI                                │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Widget (iframe)                          ││
│  │   React/Vanilla JS + CSS                                    ││
│  │   window.openai.* APIs for host communication               ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│                     ChatGPT Backend                              │
│                              │                                   │
│                              ▼                                   │
│              MCP Server (HTTP/SSE)                               │
│              - Tools: exposed actions                            │
│              - Resources: widget HTML (text/html+skybridge)      │
│              - Response: structuredContent + _meta               │
└─────────────────────────────────────────────────────────────────┘
```

**Flow**: User prompt → Model invokes tool → Server returns structured data → Widget renders → Model narrates result

---

## window.openai API Reference

Complete API surface for widget-host communication:

### State & Data Access

| Property | Purpose | Example |
|----------|---------|---------|
| `toolInput` | Arguments passed when tool was invoked | `window.openai.toolInput` |
| `toolOutput` | Structured content from server response | `window.openai.toolOutput` |
| `toolResponseMetadata` | Server `_meta` hidden from model | `window.openai.toolResponseMetadata` |
| `widgetState` | Persisted UI state snapshot | `window.openai.widgetState` |

### Runtime Actions

| Method | Purpose | Example |
|--------|---------|---------|
| `callTool(name, args)` | Invoke another MCP tool | `await window.openai.callTool("refresh_data", {city})` |
| `sendFollowUpMessage({prompt})` | Insert conversational message | `await window.openai.sendFollowUpMessage({prompt: "Summarize"})` |
| `setWidgetState(state)` | Persist state synchronously | `window.openai.setWidgetState({favorites: []})` |
| `uploadFile(file)` | Upload user file (PNG/JPEG/WebP) | `const {fileId} = await window.openai.uploadFile(file)` |
| `getFileDownloadUrl({fileId})` | Get temporary download URL | `const {downloadUrl} = await window.openai.getFileDownloadUrl({fileId})` |

### Layout Control

| Method | Purpose |
|--------|---------|
| `requestDisplayMode({mode})` | Request layout: `"inline"`, `"pip"`, `"fullscreen"` |
| `requestModal(...)` | Spawn ChatGPT-owned modal |
| `notifyIntrinsicHeight(...)` | Report dynamic height to avoid clipping |
| `openExternal({href})` | Open vetted external link |
| `requestClose()` | Close widget from UI |

### Context Properties (Read-Only)

```javascript
window.openai.theme        // "light" | "dark"
window.openai.displayMode  // "inline" | "pip" | "fullscreen"
window.openai.maxHeight    // container height in px
window.openai.safeArea     // viewport constraints
window.openai.userAgent    // browser identifier
window.openai.locale       // "en-US", "es-ES", etc.
```

### Code Examples

**sendFollowUpMessage (Best for Action Buttons)**:
```javascript
async function suggestAction(prompt) {
  if (window.openai?.sendFollowUpMessage) {
    await window.openai.sendFollowUpMessage({ prompt });
  }
}
// Usage: suggestAction('Summarize this chapter');
```

**callTool (For Tool Chaining)**:
```javascript
async function refreshData(city) {
  if (window.openai?.callTool) {
    const result = await window.openai.callTool("refresh_list", { city });
    // result contains fresh structuredContent
  }
}
```

**Note**: `callTool` requires tool metadata `"openai/widgetAccessible": true`.

---

## Tool Definition with Metadata

Tools require proper metadata to enable widget rendering:

### TypeScript/Node.js Pattern

```typescript
server.registerTool(
  "kanban-board",
  {
    title: "Show Kanban Board",
    inputSchema: { workspace: z.string() },
    annotations: {
      readOnlyHint: true,      // Skip confirmation for read operations
      destructiveHint: false,  // Set true for delete/modify actions
      openWorldHint: false     // Set true if publishing externally
    },
    _meta: {
      "openai/outputTemplate": "ui://widget/kanban.html",  // Required
      "openai/widgetAccessible": true,  // Enable callTool from widget
      "openai/visibility": "public",    // "private" hides from model
      "openai/toolInvocation/invoking": "Loading board…",
      "openai/toolInvocation/invoked": "Board ready."
    }
  },
  async ({ workspace }) => {
    const tasks = await db.fetchTasks(workspace);
    return {
      // Data for model narration (keep concise)
      structuredContent: {
        columns: ["todo", "in-progress", "done"].map(status => ({
          id: status,
          tasks: tasks.filter(t => t.status === status)
        }))
      },
      // Optional markdown for model
      content: [{ type: "text", text: "Here's your board." }],
      // Large/sensitive data for widget only (model never sees)
      _meta: {
        tasksById: Object.fromEntries(tasks.map(t => [t.id, t])),
        lastSyncedAt: new Date().toISOString()
      }
    };
  }
);
```

### Python/FastMCP Pattern

```python
from mcp.server.fastmcp import FastMCP
import mcp.types as types

mcp = FastMCP("My App")

@mcp.tool(
    annotations={
        "title": "Show Dashboard",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
    _meta={
        "openai/outputTemplate": "ui://widget/dashboard.html",
        "openai/widgetAccessible": True,
    },
)
def show_dashboard(user_id: str) -> types.CallToolResult:
    data = fetch_user_data(user_id)
    return types.CallToolResult(
        content=[types.TextContent(type="text", text="Dashboard loaded.")],
        structuredContent={"summary": data.summary},
        _meta={"fullData": data.dict(), "timestamp": datetime.now().isoformat()}
    )
```

### Tool Metadata Reference

| Key | Type | Purpose |
|-----|------|---------|
| `openai/outputTemplate` | string (URI) | **Required**. Resource URI for widget HTML |
| `openai/widgetAccessible` | boolean | Enable `window.openai.callTool` from widget |
| `openai/visibility` | `"public"` or `"private"` | Hide tool from model but keep widget-callable |
| `openai/toolInvocation/invoking` | string (≤64 chars) | Status text while executing |
| `openai/toolInvocation/invoked` | string (≤64 chars) | Status text when complete |
| `openai/fileParams` | string[] | Input fields accepting file objects |

### Response Payload Structure

| Field | Visibility | Purpose |
|-------|------------|---------|
| `structuredContent` | Model + Widget | Concise JSON for model narration |
| `content` | Model + Widget | Optional markdown/plaintext |
| `_meta` | Widget Only | Sensitive/large data hidden from model |

## Widget Resource Registration

Resources define widget HTML with proper MIME type:

### TypeScript Pattern

```typescript
server.registerResource(
  "kanban-widget",
  "ui://widget/kanban.html",
  {},
  async () => ({
    contents: [{
      uri: "ui://widget/kanban.html",
      mimeType: "text/html+skybridge",  // Required for widget rendering
      text: WIDGET_HTML,
      _meta: {
        "openai/widgetPrefersBorder": true,
        "openai/widgetDomain": "https://chatgpt.com",
        "openai/widgetCSP": {
          connect_domains: ["https://api.example.com"],
          resource_domains: ["https://*.oaistatic.com"],
          frame_domains: []
        }
      }
    }]
  })
);
```

### Python Pattern

```python
@mcp.resource(
    uri="ui://widget/{widget_name}.html",
    name="Widget Resource",
    mime_type="text/html+skybridge"
)
def widget_resource(widget_name: str) -> str:
    return WIDGETS[widget_name]["html"]
```

### Widget Resource Metadata

| Key | Purpose |
|-----|---------|
| `openai/widgetPrefersBorder` | Visual border preference |
| `openai/widgetDomain` | Dedicated origin for API allowlisting |
| `openai/widgetCSP` | Security boundaries (connect, resource, frame domains) |
| `openai/widgetDescription` | Summary shown when widget loads |

---

## React Hooks for Widgets

Official patterns for React-based widgets:

### useOpenAiGlobal (Reactive State Subscription)

```typescript
import { useSyncExternalStore } from "react";

export function useOpenAiGlobal<K extends keyof OpenAiGlobals>(
  key: K
): OpenAiGlobals[K] {
  return useSyncExternalStore(
    (onChange) => {
      const handle = (e: CustomEvent) => {
        if (e.detail.globals[key] !== undefined) onChange();
      };
      window.addEventListener("SET_GLOBALS", handle, { passive: true });
      return () => window.removeEventListener("SET_GLOBALS", handle);
    },
    () => window.openai?.[key]
  );
}
```

### useWidgetState (Persistent Component State)

```typescript
export function useWidgetState<T>(defaultState?: T | (() => T)) {
  const widgetStateFromWindow = useOpenAiGlobal("widgetState") as T;

  const [state, _setState] = useState<T | null>(() =>
    widgetStateFromWindow ?? (typeof defaultState === "function"
      ? defaultState()
      : defaultState ?? null)
  );

  useEffect(() => {
    _setState(widgetStateFromWindow);
  }, [widgetStateFromWindow]);

  const setState = useCallback((newState: T | ((prev: T) => T)) => {
    _setState((prev) => {
      const next = typeof newState === "function" ? newState(prev) : newState;
      window.openai?.setWidgetState(next);
      return next;
    });
  }, []);

  return [state, setState] as const;
}
```

### Helper Hooks

```typescript
export function useToolInput() {
  return useOpenAiGlobal("toolInput");
}

export function useToolOutput() {
  return useOpenAiGlobal("toolOutput");
}

export function useToolResponseMetadata() {
  return useOpenAiGlobal("toolResponseMetadata");
}
```

---

## Quick Start

1. **Create MCP server** with tools and widget resources
2. **Define widget HTML** with `window.openai` communication
3. **Set tool metadata** with `openai/outputTemplate` pointing to widget
4. **Return structured responses** with `structuredContent` + `_meta`
5. **Expose via ngrok** for ChatGPT access
6. **Register in ChatGPT** Developer Mode settings

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

## OAuth 2.1 Authentication

For apps requiring user authentication:

### Protected Resource Metadata

Host at `/.well-known/oauth-protected-resource`:

```json
{
  "resource": "https://your-mcp.example.com",
  "authorization_servers": ["https://auth.yourcompany.com"],
  "scopes_supported": ["files:read", "files:write"]
}
```

### Tool Security Schemes

```typescript
securitySchemes: [
  { type: "noauth" },  // Public access
  { type: "oauth2", scopes: ["docs.read"] }  // Authenticated access
]
```

### Token Validation

Servers must:
- Validate signature/issuer via authorization server's JWKS
- Reject expired tokens (`exp`/`nbf` claims)
- Confirm audience matches (`aud` claim)
- Return `401` with `WWW-Authenticate` header on failure

### Error Response (Triggers Auth UI)

```json
{
  "_meta": {
    "mcp/www_authenticate": [
      "Bearer resource_metadata=\"https://.../.well-known/oauth-protected-resource\", error=\"insufficient_scope\""
    ]
  },
  "isError": true
}
```

---

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Widget shows "Loading..." | HTML not delivered correctly | Check `_meta` with `openai/outputTemplate`, verify MIME type |
| Widget not updating | Aggressive caching | Delete app, restart ngrok with new URL, create new app |
| JavaScript errors | `window.openai` unavailable | Always use optional chaining: `window.openai?.methodName` |
| Tool not in @mentions | MCP server disconnected | Verify ngrok URL, check server logs for `ListToolsRequest` |
| `callTool` not working | Widget access disabled | Add `"openai/widgetAccessible": true` to tool metadata |

---

## Decision Logic

| Situation | Pattern |
|-----------|---------|
| Simple display widget | Vanilla HTML + CSS + JS |
| Complex interactive UI | React + hooks (useWidgetState) |
| Multi-tool workflow | `callTool` from widget with `widgetAccessible: true` |
| User suggestions | `sendFollowUpMessage` (most reliable) |
| Persistent UI state | `setWidgetState` + `widgetState` |
| Large data payloads | Send via `_meta` (hidden from model) |
| User authentication | OAuth 2.1 with security schemes |
| Display mode changes | `requestDisplayMode` (inline/pip/fullscreen) |

---

## Safety

### NEVER
- Embed API keys, tokens, or secrets in `structuredContent`, `content`, or `_meta`
- Rely on `userAgent` or `locale` hints for authorization decisions
- Expose destructive operations without user intent verification

### ALWAYS
- Validate tokens server-side (ChatGPT assumes tokens are untrusted)
- Use environment variables for secrets
- Design handlers as idempotent (model may retry)
- Check `window.openai` existence before calling methods

---

## References

- [Official Docs](https://developers.openai.com/apps-sdk/)
- [Examples Repo](https://github.com/openai/openai-apps-sdk-examples)
- [Complete Template](references/complete_template.md) - Ready-to-use server + widget
- [Widget Patterns](references/widget_patterns.md) - HTML/CSS/JS examples
- [Response Structure](references/response_structure.md) - Metadata format details
- [Debugging Guide](references/debugging.md) - Troubleshooting common issues
