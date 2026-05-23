---
name: expo-devtools-cli
description: Building Expo DevTools Plugins with CLI Interfaces for interacting with running Expo apps using agents.
---

# Building Expo DevTools Plugins with CLI Interfaces

Build CLI tools that communicate with running Expo apps via the DevTools plugin system.

## Architecture Overview

```
┌─────────────────┐     WebSocket      ┌─────────────────┐
│   CLI Client    │◄──────────────────►│  Expo Dev Server │
│  (Bun + Stricli)│                    │   (Metro)        │
└─────────────────┘                    └────────┬────────┘
                                                │
                                       ┌────────▼────────┐
                                       │   React Native  │
                                       │   App + Hook    │
                                       └─────────────────┘
```

## Preferred Tech Stack

| Component     | Technology              | Why                                                 |
| ------------- | ----------------------- | --------------------------------------------------- |
| Runtime       | **Bun**                 | Fast startup, native TypeScript, built-in WebSocket |
| CLI Framework | **@stricli/core**       | Type-safe, lazy loading, tree-shakeable             |
| App Hook      | **expo/devtools**       | `useDevToolsPluginClient` for app-side connection   |
| Protocol      | **JSON over WebSocket** | Simple, debuggable with standard tools              |

## Project Structure

```
cli/
├── index.ts              # Entry point with shebang
├── app.ts                # Stricli app definition with routes
├── client.ts             # WebSocket client for devtools
├── types.ts              # Shared TypeScript types
├── formatters.ts         # Output formatting (table, JSON)
└── commands/
    ├── query.ts          # Read commands
    ├── write.ts          # Write commands
    └── status.ts         # Status/health commands

src/devtools/
└── useMyPluginDevTools.ts  # App-side message handler hook
```

## Step 1: Configure the Module

Add devtools config to `expo-module.config.json`:

```json
{
  "name": "MyModule",
  "platforms": ["ios", "android"],
  "devtools": {
    "name": "My Plugin",
    "id": "my-plugin"
  }
}
```

## Step 2: Create the App-Side Hook

```typescript
// src/devtools/useMyPluginDevTools.ts
import { useEffect } from "react";
import { useDevToolsPluginClient } from "expo/devtools";

interface PluginMessage {
  id: string;
  type: string;
  payload: Record<string, unknown>;
}

export function useMyPluginDevTools() {
  const client = useDevToolsPluginClient("my-plugin"); // Must match devtools.id

  useEffect(() => {
    if (!client) return;

    const handleMessage = (data: PluginMessage) => {
      const { id, type, payload } = data;

      const sendResult = (result: unknown) => {
        client.sendMessage("result", { id, type: "result", data: result });
      };

      const sendError = (error: Error) => {
        client.sendMessage("error", {
          id,
          type: "error",
          error: error.message,
        });
      };

      (async () => {
        try {
          switch (type) {
            case "getData":
              const data = await fetchData(payload.query as string);
              sendResult(data);
              break;
            default:
              sendError(new Error(`Unknown message type: ${type}`));
          }
        } catch (error) {
          sendError(error as Error);
        }
      })();
    };

    const subscription = client.addMessageListener(
      "message",
      (msg: unknown) => {
        handleMessage(msg as PluginMessage);
      }
    );

    return () => {
      subscription?.remove?.();
    };
  }, [client]);
}
```

## Step 3: Create the CLI Client

```typescript
// cli/client.ts
const DEFAULT_PORT = 8081;
const REQUEST_TIMEOUT = 30000;
const PROTOCOL_VERSION = 1;

export class PluginClient {
  private ws: WebSocket | null = null;
  private pending = new Map<string, { resolve: Function; reject: Function }>();
  private connected = false;
  private browserClientId = Date.now().toString();
  private pluginName = "my-plugin"; // Must match devtools.id

  async connect(port = DEFAULT_PORT): Promise<void> {
    if (this.connected) return;

    return new Promise((resolve, reject) => {
      // IMPORTANT: Use the broadcast endpoint
      const url = `ws://localhost:${port}/expo-dev-plugins/broadcast`;
      this.ws = new WebSocket(url);

      const timeout = setTimeout(() => {
        reject(new Error(`Connection timeout to ${url}`));
      }, 10000);

      this.ws.addEventListener("open", () => {
        clearTimeout(timeout);
        this.connected = true;
        this.sendHandshake();
        resolve();
      });

      this.ws.addEventListener("error", () => {
        clearTimeout(timeout);
        reject(new Error(`Failed to connect to Expo devtools at ${url}`));
      });

      this.ws.addEventListener("close", () => {
        this.connected = false;
      });

      this.ws.addEventListener("message", (event) => {
        this.handleMessage(event.data);
      });
    });
  }

  private sendHandshake(): void {
    // CRITICAL: Must include all these fields
    const handshake = {
      protocolVersion: PROTOCOL_VERSION, // Must be 1
      pluginName: this.pluginName,
      method: "handshake",
      browserClientId: this.browserClientId,
      __isHandshakeMessages: true, // Required flag
    };
    this.ws?.send(JSON.stringify(handshake));
  }

  private handleMessage(data: string | ArrayBuffer): void {
    if (typeof data === "string") {
      try {
        const parsed = JSON.parse(data);
        if (parsed.__isHandshakeMessages) return; // Ignore handshake acks
        if (parsed.messageKey) {
          this.handlePackedMessage(parsed);
        }
      } catch {
        // Not JSON, ignore
      }
    }
  }

  private handlePackedMessage(msg: { messageKey: any; payload: any }): void {
    const { messageKey, payload } = msg;
    if (messageKey.pluginName !== this.pluginName) return;

    if (messageKey.method === "result" || messageKey.method === "error") {
      const response = payload as {
        id: string;
        data?: unknown;
        error?: string;
      };
      const pending = this.pending.get(response.id);
      if (!pending) return;

      this.pending.delete(response.id);
      if (messageKey.method === "error" || response.error) {
        pending.reject(new Error(response.error ?? "Unknown error"));
      } else {
        pending.resolve(response.data);
      }
    }
  }

  async send<T>(type: string, payload: unknown): Promise<T> {
    if (!this.ws || !this.connected) {
      throw new Error("Not connected to Expo devtools");
    }

    const id = crypto.randomUUID();
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });

      // CRITICAL: Send as JSON string, NOT binary ArrayBuffer
      const msg = {
        messageKey: { pluginName: this.pluginName, method: "message" },
        payload: { id, type, payload },
      };
      this.ws!.send(JSON.stringify(msg));

      setTimeout(() => {
        if (this.pending.has(id)) {
          this.pending.delete(id);
          reject(new Error("Request timeout"));
        }
      }, REQUEST_TIMEOUT);
    });
  }

  async disconnect(): Promise<void> {
    this.ws?.close();
    this.ws = null;
    this.connected = false;
  }
}
```

## Step 4: Create the CLI Entry Point

```typescript
// cli/index.ts
#!/usr/bin/env bun
import { run } from "@stricli/core";
import { app } from "./app";

await run(app, process.argv.slice(2), { process });
```

```typescript
// cli/app.ts
import { buildApplication, buildRouteMap } from "@stricli/core";

const routes = buildRouteMap({
  routes: {
    status: () => import("./commands/status").then((m) => m.default),
    query: () => import("./commands/query").then((m) => m.default),
  },
});

export const app = buildApplication(routes, {
  name: "my-cli",
  versionInfo: { currentVersion: "1.0.0" },
});
```

## Step 5: Configure package.json

```json
{
  "bin": {
    "my-cli": "cli/index.ts"
  },
  "scripts": {
    "cli": "bun cli/index.ts"
  },
  "dependencies": {
    "@stricli/core": "^1.1.0"
  }
}
```

## Footguns and Solutions

### 1. Binary vs JSON Messages

**Problem**: Messages sent as `ArrayBuffer` are silently ignored.

```typescript
// WRONG - Will not work
const encoder = new TextEncoder();
this.ws.send(encoder.encode(JSON.stringify(msg)).buffer);

// CORRECT - Send as JSON string
this.ws.send(JSON.stringify(msg));
```

**Debugging**: Use `websocat` to test the WebSocket:

```bash
websocat -v ws://localhost:8081/expo-dev-plugins/broadcast
```

### 2. Wrong WebSocket Endpoint

**Problem**: Using `/message` or other endpoints won't work.

```typescript
// WRONG
const url = `ws://localhost:${port}/message`;

// CORRECT - Must use broadcast endpoint
const url = `ws://localhost:${port}/expo-dev-plugins/broadcast`;
```

**Debugging**: Use curl to verify WebSocket upgrade:

```bash
curl -v -H "Connection: Upgrade" -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Key: test" -H "Sec-WebSocket-Version: 13" \
  http://localhost:8081/expo-dev-plugins/broadcast
```

### 3. Missing Handshake Fields

**Problem**: Connection appears to work but messages aren't routed.

```typescript
// WRONG - Missing required fields
const handshake = { pluginName: "my-plugin" };

// CORRECT - All fields required
const handshake = {
  protocolVersion: 1, // Must be 1
  pluginName: "my-plugin",
  method: "handshake",
  browserClientId: "unique-id",
  __isHandshakeMessages: true, // Critical flag
};
```

### 4. Protocol Version Mismatch

**Problem**: `terminateBrowserClient` messages with warning about incompatible clients.

```typescript
// WRONG
protocolVersion: 2;

// CORRECT - Use version 1
protocolVersion: 1;
```

### 5. Plugin Name Mismatch

**Problem**: Messages sent but never received by app.

The `pluginName` must match exactly across:

- `expo-module.config.json` → `devtools.id`
- App hook → `useDevToolsPluginClient("my-plugin")`
- CLI client → `this.pluginName = "my-plugin"`

### 6. Hook Not Setting Up Listener

**Problem**: Hook logs "connected" but messages timeout.

Check that `useDevToolsPluginClient` is imported from the correct package:

```typescript
// CORRECT
import { useDevToolsPluginClient } from "expo/devtools";

// WRONG - different package
import { useDevToolsPluginClient } from "@expo/devtools-plugin-client";
```

### 7. Message Listener Method Name

**Problem**: App receives connection but not messages.

The `addMessageListener` method name must match the `messageKey.method` from CLI:

```typescript
// CLI sends with method: "message"
const msg = {
  messageKey: { pluginName: "my-plugin", method: "message" },
  payload: { id, type, payload },
};

// App listens for "message"
client.addMessageListener("message", handler);
```

## Debugging Techniques

### 1. Monitor WebSocket Traffic

```bash
# Listen to all broadcasts
websocat --no-close -v ws://localhost:8081/expo-dev-plugins/broadcast

# Send test handshake
echo '{"protocolVersion":1,"pluginName":"my-plugin","method":"handshake","browserClientId":"test","__isHandshakeMessages":true}' | \
  websocat ws://localhost:8081/expo-dev-plugins/broadcast
```

### 2. Check App Console Logs

```bash
bunx xcobra expo console --json | grep -i "my-plugin\|devtools"
```

### 3. Verify Hook is Running

Add temporary logging to the hook:

```typescript
useEffect(() => {
  console.log("[DevTools] client:", client ? "connected" : "null");
  if (!client) return;
  console.log("[DevTools] Setting up listener");
  // ...
}, [client]);
```

### 4. Test Connection Independently

```typescript
// Minimal test script
const ws = new WebSocket("ws://localhost:8081/expo-dev-plugins/broadcast");
ws.onopen = () => {
  console.log("Connected");
  ws.send(
    JSON.stringify({
      protocolVersion: 1,
      pluginName: "my-plugin",
      method: "handshake",
      browserClientId: "test",
      __isHandshakeMessages: true,
    })
  );
};
ws.onmessage = (e) => console.log("Received:", e.data);
```

## Testing Workflow

1. **Start the app**: `yarn expo run:ios` or have simulator running with Expo Go
2. **Verify Metro is running**: Check `http://localhost:8081` responds
3. **Test CLI connection**: `bun cli/index.ts status`
4. **Check for errors**: Monitor both CLI output and app console

## Reference Implementation

See the HealthKit CLI in this repo:

- `cli/` - Full CLI implementation
- `src/dev-tools/useHealthKitDevTools.ts` - App-side hook
- `example/App.tsx` - Hook usage in app
