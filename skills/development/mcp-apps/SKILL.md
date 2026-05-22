---
name: mcp-apps
description: Build MCP Apps - interactive UI components that render inside AI hosts like Claude, ChatGPT, and VSCode. This skill should be used when creating tools with rich UI, building dashboards or forms for AI interactions, or adding visual interfaces to MCP servers.
---

# MCP Apps Skill

Build interactive UI applications that render directly inside MCP hosts like Claude Desktop, ChatGPT, and VSCode. MCP Apps extend the Model Context Protocol to return rich interfaces instead of plain text.

## When to Use This Skill

- Creating MCP tools with interactive UI (forms, dashboards, visualizations)
- Building visual interfaces for AI-assisted workflows
- Adding rich media viewers (PDFs, maps, 3D models) to conversations
- Creating configuration wizards or multi-step workflows
- Building real-time monitoring dashboards

## Core Concepts

### What Are MCP Apps?

MCP Apps let tools return rich, interactive interfaces instead of plain text. When a tool declares a UI resource, the host renders it in a sandboxed iframe, and users interact with it directly in the conversation.

**Key benefits over regular web apps**:
- **Context preservation** - UI lives inside the conversation
- **Bidirectional data flow** - App can call server tools, host pushes results
- **Integration with host capabilities** - Delegate actions to the host
- **Security guarantees** - Sandboxed iframe with controlled permissions

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Host (Claude, VSCode)                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  Sandboxed Iframe                    │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │              Your MCP App UI                 │    │    │
│  │  │     (React, Vue, Svelte, or vanilla)        │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │                         │                            │    │
│  │                   postMessage                        │    │
│  │                         │                            │    │
│  └─────────────────────────┼────────────────────────────┘    │
│                            │                                  │
│                     JSON-RPC                                  │
│                            │                                  │
│  ┌─────────────────────────┼────────────────────────────┐    │
│  │                   MCP Server                          │    │
│  │  • Tools with _meta.ui.resourceUri                   │    │
│  │  • UI Resources (bundled HTML)                       │    │
│  └───────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────┘
```

### How It Works

1. **Tool declares UI metadata** - Tool description includes `_meta.ui.resourceUri` pointing to a `ui://` resource
2. **Host preloads UI** - Host fetches the bundled HTML before tool execution
3. **Sandboxed rendering** - UI renders in sandboxed iframe with restricted permissions
4. **Bidirectional communication** - App and host communicate via JSON-RPC over postMessage

## Quick Start

### Using the Init Script

```bash
# Scaffold a new MCP App project
python scripts/init_mcp_app.py my-mcp-app --path ./projects
```

This creates a complete project structure with server, UI, and configuration.

### Manual Setup

1. Install dependencies:

```bash
npm install @modelcontextprotocol/ext-apps @modelcontextprotocol/sdk
npm install -D typescript vite vite-plugin-singlefile express cors @types/express @types/cors tsx
```

2. Create project structure:

```
my-mcp-app/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── server.ts           # MCP server
├── mcp-app.html        # UI entry point
└── src/
    └── mcp-app.ts      # UI logic
```

See `references/boilerplate.md` for complete file contents.

## Server Implementation

### Registering a Tool with UI

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { registerAppTool, registerAppResource, RESOURCE_MIME_TYPE } from "@modelcontextprotocol/ext-apps/server";

const server = new McpServer({
  name: "My MCP App Server",
  version: "1.0.0",
});

// The ui:// scheme tells hosts this is an MCP App resource
const resourceUri = "ui://my-tool/app.html";

// Register the tool with UI metadata
registerAppTool(
  server,
  "my-tool",
  {
    title: "My Tool",
    description: "A tool with interactive UI",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string" }
      }
    },
    _meta: {
      ui: { resourceUri }
    }
  },
  async (args) => {
    // Tool logic here
    return {
      content: [{ type: "text", text: JSON.stringify(args) }]
    };
  }
);

// Register the UI resource
registerAppResource(
  server,
  resourceUri,
  resourceUri,
  { mimeType: RESOURCE_MIME_TYPE },
  async () => {
    const html = await fs.readFile("dist/mcp-app.html", "utf-8");
    return {
      contents: [{ uri: resourceUri, mimeType: RESOURCE_MIME_TYPE, text: html }]
    };
  }
);
```

### Exposing via HTTP

```typescript
import express from "express";
import cors from "cors";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";

const app = express();
app.use(cors());
app.use(express.json());

app.post("/mcp", async (req, res) => {
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
    enableJsonResponse: true,
  });
  res.on("close", () => transport.close());
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

app.listen(3001, () => {
  console.log("Server listening on http://localhost:3001/mcp");
});
```

## UI Implementation

### Basic App Class Usage

```typescript
import { App } from "@modelcontextprotocol/ext-apps";

const app = new App({ name: "My App", version: "1.0.0" });

// Connect to host
await app.connect();

// Receive initial tool result
app.ontoolresult = (result) => {
  const data = result.content?.find((c) => c.type === "text")?.text;
  console.log("Received:", data);
  renderUI(data);
};

// Call server tools from UI
async function fetchData() {
  const result = await app.callServerTool({
    name: "fetch-data",
    arguments: { query: "example" },
  });
  return result.content?.find((c) => c.type === "text")?.text;
}

// Update model context
async function notifyModel(info: string) {
  await app.updateModelContext({
    content: [{ type: "text", text: info }],
  });
}

// Log for debugging
app.log("info", "App initialized");

// Open links in user's browser
app.openLink("https://example.com");
```

### HTML Entry Point

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>My MCP App</title>
  <style>
    body { font-family: system-ui, sans-serif; padding: 1rem; }
    /* Add your styles */
  </style>
</head>
<body>
  <div id="app">Loading...</div>
  <script type="module" src="/src/mcp-app.ts"></script>
</body>
</html>
```

## Configuration Files

### vite.config.ts

```typescript
import { defineConfig } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({
  plugins: [viteSingleFile()],
  build: {
    outDir: "dist",
    rollupOptions: {
      input: process.env.INPUT,
    },
  },
});
```

### package.json Scripts

```json
{
  "type": "module",
  "scripts": {
    "build": "INPUT=mcp-app.html vite build",
    "serve": "npx tsx server.ts",
    "dev": "npm run build && npm run serve"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist"
  },
  "include": ["*.ts", "src/**/*.ts"]
}
```

## Testing

### With Claude Desktop

1. Build and start your server:
   ```bash
   npm run build && npm run serve
   ```

2. Expose locally with cloudflared:
   ```bash
   npx cloudflared tunnel --url http://localhost:3001
   ```

3. Add as custom connector in Claude:
   - Profile → Settings → Connectors → Add custom connector
   - Enter the cloudflared URL

4. Chat with Claude and trigger your tool.

### With basic-host

The ext-apps repo includes a test host:

```bash
git clone https://github.com/modelcontextprotocol/ext-apps
cd ext-apps/examples/basic-host
npm install
SERVERS='["http://localhost:3001/mcp"]' npm start
```

Navigate to `http://localhost:8080` to test.

## Security Model

MCP Apps run in sandboxed iframes with:
- No access to parent window DOM
- No cookie or storage access from host
- Cannot navigate parent page
- All communication via auditable JSON-RPC

### Requesting Permissions

```typescript
registerAppTool(server, "camera-tool", {
  // ...
  _meta: {
    ui: {
      resourceUri: "ui://camera/app.html",
      permissions: ["camera", "microphone"], // Request additional permissions
      csp: ["https://cdn.example.com"] // Allow external resources
    }
  }
});
```

## Framework Support

MCP Apps work with any web framework. The ext-apps repo has starters for:
- React
- Vue
- Svelte
- Preact
- Solid
- Vanilla JavaScript

See `references/patterns.md` for framework-specific patterns.

## Common Patterns

### Form with Validation

```typescript
app.ontoolresult = (result) => {
  renderForm(result.content);
};

async function handleSubmit(formData: FormData) {
  const result = await app.callServerTool({
    name: "submit-form",
    arguments: Object.fromEntries(formData),
  });
  
  if (result.isError) {
    showError(result.content);
  } else {
    showSuccess(result.content);
    await app.updateModelContext({
      content: [{ type: "text", text: "User submitted form successfully" }],
    });
  }
}
```

### Real-time Dashboard

```typescript
let intervalId: number;

app.ontoolresult = async () => {
  // Start polling for updates
  intervalId = setInterval(async () => {
    const result = await app.callServerTool({
      name: "get-metrics",
      arguments: {},
    });
    updateDashboard(result.content);
  }, 5000);
};

// Clean up on disconnect
window.addEventListener("beforeunload", () => {
  clearInterval(intervalId);
});
```

### Multi-step Workflow

```typescript
let currentStep = 0;
const steps = ["configure", "review", "confirm"];

async function nextStep(data: unknown) {
  const result = await app.callServerTool({
    name: `workflow-${steps[currentStep]}`,
    arguments: data,
  });
  
  currentStep++;
  
  if (currentStep < steps.length) {
    renderStep(currentStep, result.content);
  } else {
    await app.updateModelContext({
      content: [{ type: "text", text: "Workflow completed" }],
    });
    renderComplete(result.content);
  }
}
```

## Troubleshooting

### UI Not Rendering

- Ensure tool has `_meta.ui.resourceUri` in description
- Check that UI resource is registered with correct URI
- Verify bundled HTML is being served correctly
- Check browser console for errors

### Communication Errors

- Ensure `app.connect()` is called before other operations
- Check that server is running and accessible
- Verify CORS is enabled on server

### Host Not Recognizing App

- Confirm host supports MCP Apps (Claude, VSCode Insiders, ChatGPT)
- Check that server exposes correct MCP endpoint
- Verify cloudflared tunnel is active for remote testing

## References

- `references/boilerplate.md` - Complete project setup code
- `references/patterns.md` - Common UI patterns and examples
- [ext-apps Repository](https://github.com/modelcontextprotocol/ext-apps) - Official SDK and examples
- [MCP Apps Documentation](https://modelcontextprotocol.io/docs/extensions/apps) - Official docs
- [API Reference](https://modelcontextprotocol.github.io/ext-apps/api/) - Full SDK API
