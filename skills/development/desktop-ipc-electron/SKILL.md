---
name: desktop-ipc-electron
description: Type-safe Electron IPC patterns with typed channels, electron-trpc, MessagePort, and utility process communication
---

# Electron Type-Safe IPC Patterns

> **Quick Guide:** All Electron IPC flows through a preload script using `contextBridge.exposeInMainWorld()`. Make it type-safe by defining a shared channel map that constrains channel names, payloads, and return types across main, preload, and renderer. For end-to-end type safety with minimal boilerplate, use `electron-trpc` (tRPC over IPC). For high-throughput streaming or renderer-to-renderer communication, use `MessageChannelMain`/`MessagePort`. For CPU-intensive background work, use `utilityProcess` with `parentPort`. Always validate IPC input in the main process -- treat renderer messages as untrusted.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST validate and sanitize ALL data received via IPC in the main process -- treat renderer messages as untrusted input)**

**(You MUST use `contextBridge.exposeInMainWorld()` in preload scripts -- never expose `ipcRenderer` directly)**

**(You MUST define IPC channel names and payload types in a single shared file -- never use untyped string literals for channel names)**

**(You MUST use `ipcMain.handle()` / `ipcRenderer.invoke()` for request-response IPC -- `sendSync` blocks the renderer)**

**(You MUST clean up IPC listeners when components unmount or windows close -- listener leaks cause memory issues and duplicate handlers)**

</critical_requirements>

---

**Auto-detection:** Electron IPC, ipcMain, ipcRenderer, contextBridge, preload, type-safe IPC, electron-trpc, ipcLink, createIPCHandler, exposeElectronTRPC, MessageChannelMain, MessagePortMain, MessagePort, utilityProcess, parentPort, typed channels, IPC channel map, postMessage, webContents.send, ipcMain.handle, ipcRenderer.invoke

**When to use:**

- Adding type safety to Electron IPC communication
- Setting up electron-trpc for end-to-end typed IPC
- Defining shared channel/payload types between main and renderer
- Building typed preload APIs with contextBridge
- Using MessagePort for high-throughput or renderer-to-renderer communication
- Implementing utility process IPC for background tasks
- Validating and sanitizing IPC input in main process handlers

**When NOT to use:**

- Choosing a UI framework for the renderer (use the appropriate framework skill)
- General Electron app setup, packaging, or native APIs (use the Electron framework skill)
- Simple IPC that does not need type safety beyond basic JavaScript

**Key patterns covered:**

- Shared IPC channel map with typed payloads and return types
- Typed preload API via contextBridge with declaration augmentation
- electron-trpc for end-to-end type safety (queries, mutations, subscriptions)
- Request-response (`handle`/`invoke`) with typed wrappers
- Fire-and-forget (`on`/`send`) with typed channels
- Main-to-renderer push (`webContents.send`) with typed events
- MessagePort for high-throughput and renderer-to-renderer communication
- Utility process IPC with `parentPort` and MessagePort transfer
- IPC input validation and channel allowlisting

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Shared channel map, typed preload, typed wrappers, declaration augmentation
- [examples/electron-trpc.md](examples/electron-trpc.md) - electron-trpc setup, queries, mutations, subscriptions
- [examples/message-ports.md](examples/message-ports.md) - MessagePort patterns, renderer-to-renderer, utility process IPC
- [reference.md](reference.md) - IPC method quick reference, decision framework, security checklist

---

<philosophy>

## Philosophy

Electron IPC is stringly typed by default -- channel names are plain strings, payloads are `any`, and there is no compile-time guarantee that the main process handler matches what the renderer sends. Type-safe IPC solves this by defining a single source of truth for channel names, argument types, and return types, then threading those types through typed wrapper functions.

**Three levels of type safety, pick one:**

1. **Shared channel map + typed wrappers** (DIY) -- define an `IpcChannelMap` interface, create thin typed wrappers around `ipcMain`/`ipcRenderer`. Zero dependencies, full control.
2. **electron-trpc** (library) -- tRPC over Electron IPC. Define a router in main with Zod-validated procedures, get a fully typed client in the renderer. Best DX for complex apps.
3. **MessagePort with typed messages** -- for high-throughput streaming or renderer-to-renderer communication where standard IPC overhead matters.

**When to use each:**

- **Shared channel map:** Most apps. Simple, no dependencies, covers `handle`/`invoke`, `send`/`on`, and `webContents.send`.
- **electron-trpc:** Apps with many IPC endpoints, complex input validation, or subscription needs. Worth the dependency when you have 10+ IPC channels.
- **MessagePort:** Real-time data feeds, large binary transfers, or direct renderer-to-renderer communication. Not a replacement for standard IPC -- an addition for specific high-throughput needs.

**When NOT to use type-safe IPC:**

- Prototyping where speed matters more than safety
- Apps with 1-2 trivial IPC calls where the overhead of typed infrastructure is not justified

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Shared IPC Channel Map

Define all channel names, argument types, and return types in a single shared file. Both main and renderer import from this file.

```typescript
// shared/ipc-channels.ts
export interface IpcHandleChannels {
  "file:read": (filePath: string) => { content: string };
  "file:write": (filePath: string, content: string) => { success: boolean };
  "dialog:open": (options: OpenDialogOptions) => string | null;
  "app:version": () => string;
}

export interface IpcSendChannels {
  "analytics:track": [eventName: string, metadata: Record<string, unknown>];
  "log:error": [message: string, stack?: string];
}

export interface IpcMainToRendererChannels {
  "update:progress": { percent: number; message: string };
  "update:available": { version: string };
  "theme:changed": "light" | "dark";
}
```

**Why good:** Single source of truth for all IPC contracts, TypeScript catches mismatches at compile time, channel names are autocompleted

See [examples/core.md](examples/core.md) for typed wrappers that consume this map.

---

### Pattern 2: Typed Preload with contextBridge

Build a typed preload API from the channel map, then augment `window` so the renderer gets full autocompletion.

```typescript
// preload.ts
import { contextBridge, ipcRenderer } from "electron";
import type {
  IpcHandleChannels,
  IpcSendChannels,
} from "../shared/ipc-channels";

type ElectronAPI = {
  invoke: <C extends keyof IpcHandleChannels>(
    channel: C,
    ...args: Parameters<IpcHandleChannels[C]>
  ) => Promise<ReturnType<IpcHandleChannels[C]>>;
  send: <C extends keyof IpcSendChannels>(
    channel: C,
    ...args: IpcSendChannels[C]
  ) => void;
  on: (channel: string, callback: (...args: unknown[]) => void) => () => void;
};

contextBridge.exposeInMainWorld("electronAPI", {
  invoke: (channel, ...args) => ipcRenderer.invoke(channel, ...args),
  send: (channel, ...args) => ipcRenderer.send(channel, ...args),
  on: (channel, callback) => {
    const listener = (_event: unknown, ...args: unknown[]) => callback(...args);
    ipcRenderer.on(channel, listener);
    return () => ipcRenderer.removeListener(channel, listener);
  },
} satisfies ElectronAPI);
```

```typescript
// shared/electron-api.d.ts -- augment window for renderer autocompletion
import type { ElectronAPI } from "../preload";

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}
```

**Why good:** renderer gets autocomplete on channel names and typed payloads, `on` returns an unsubscribe function for easy cleanup

See [examples/core.md](examples/core.md) for the full pattern with main process typed handlers.

---

### Pattern 3: electron-trpc for End-to-End Type Safety

For apps with many IPC endpoints, electron-trpc provides the best developer experience by leveraging tRPC's router pattern.

```typescript
// main/router.ts
import { initTRPC } from "@trpc/server";
import { z } from "zod";

const t = initTRPC.create({ isServer: true });

export const router = t.router({
  readFile: t.procedure
    .input(z.object({ path: z.string() }))
    .query(async ({ input }) => {
      const content = await fs.readFile(input.path, "utf-8");
      return { content };
    }),
  saveSettings: t.procedure
    .input(z.object({ theme: z.enum(["light", "dark"]) }))
    .mutation(async ({ input }) => {
      await saveToStore(input);
      return { success: true };
    }),
});

export type AppRouter = typeof router;
```

```typescript
// renderer/client.ts
import { createTRPCProxyClient } from "@trpc/client";
import { ipcLink } from "electron-trpc/renderer";
import type { AppRouter } from "../main/router";

export const trpc = createTRPCProxyClient<AppRouter>({
  links: [ipcLink()],
});

// Fully typed -- autocomplete on procedures, typed input/output
const result = await trpc.readFile.query({ path: "/some/file.txt" });
```

**Why good:** Zod validates input at runtime in main, TypeScript validates at compile time in renderer, adding a new procedure auto-surfaces in the client

See [examples/electron-trpc.md](examples/electron-trpc.md) for full setup including preload, subscriptions, and context patterns.

---

### Pattern 4: IPC Input Validation

Always validate arguments in main process handlers. The renderer can be compromised via XSS -- main process handlers have full Node.js access.

```typescript
// main/handlers.ts
const ALLOWED_EXTENSIONS = new Set([".txt", ".md", ".json"]);
const MAX_CONTENT_LENGTH = 10 * 1024 * 1024; // 10MB

ipcMain.handle("file:read", async (_event, filePath: unknown) => {
  // Type check
  if (typeof filePath !== "string") {
    throw new Error("filePath must be a string");
  }
  // Path traversal prevention
  const resolved = path.resolve(app.getPath("userData"), filePath);
  if (!resolved.startsWith(app.getPath("userData"))) {
    throw new Error("Access denied: path outside allowed directory");
  }
  // Extension allowlist
  const ext = path.extname(resolved);
  if (!ALLOWED_EXTENSIONS.has(ext)) {
    throw new Error(`File type not allowed: ${ext}`);
  }
  return { content: await fs.readFile(resolved, "utf-8") };
});
```

**Why good:** validates type, prevents path traversal, restricts file extensions, uses named constants

See [examples/core.md](examples/core.md) for a channel validation middleware pattern.

---

### Pattern 5: MessagePort for High-Throughput Communication

Use `MessageChannelMain` for streaming data, large transfers, or direct renderer-to-renderer communication.

```typescript
// main.ts -- create a port pair and send one end to renderer
import { MessageChannelMain } from "electron";

function createDataChannel(win: BrowserWindow): MessagePortMain {
  const { port1, port2 } = new MessageChannelMain();
  win.webContents.postMessage("port-transfer", null, [port2]);
  port1.start();
  return port1;
}
```

```typescript
// preload.ts -- receive port and expose to renderer
ipcRenderer.on("port-transfer", (event) => {
  const [port] = event.ports;
  contextBridge.exposeInMainWorld("dataPort", port);
});
```

**Key points:** ports are transferred via `postMessage` (not `send`/`invoke`), `port.start()` must be called on the main side, renderer side auto-starts when adding a `message` listener.

See [examples/message-ports.md](examples/message-ports.md) for renderer-to-renderer and utility process patterns.

---

### Pattern 6: Utility Process IPC

Use `utilityProcess.fork()` for CPU-intensive work. Communication flows through `parentPort`.

```typescript
// main.ts
import { utilityProcess } from "electron";

const worker = utilityProcess.fork(path.join(__dirname, "worker.js"));
worker.postMessage({ type: "process-data", payload: largeDataset });
worker.on("message", (result) => {
  mainWindow.webContents.send("processing-complete", result);
});
```

```typescript
// worker.ts (runs in utility process)
process.parentPort.on("message", (event) => {
  const { type, payload } = event.data;
  if (type === "process-data") {
    const result = heavyComputation(payload);
    process.parentPort.postMessage({ type: "result", data: result });
  }
});
```

**Key points:** utility processes have full Node.js access, communicate via `parentPort.postMessage()`, and should be used instead of `child_process.fork()` in Electron apps.

See [examples/message-ports.md](examples/message-ports.md) for typed utility process communication.

</patterns>

---

<decision_framework>

## Decision Framework

### Which Type Safety Approach?

```
How many IPC channels does the app have?
+-- 1-5 channels?
|   +-- Shared channel map + typed wrappers (no dependencies)
+-- 5-20 channels?
|   +-- Shared channel map works, but electron-trpc adds value
+-- 20+ channels or complex validation?
|   +-- electron-trpc (Zod validation + typed client)
+-- Need subscriptions / real-time updates?
    +-- electron-trpc subscriptions OR MessagePort
```

### Which IPC Pattern?

```
Renderer needs a response from main?
+-- YES --> ipcMain.handle() + ipcRenderer.invoke()
Renderer sends data, no response needed?
+-- YES --> ipcMain.on() + ipcRenderer.send()
Main needs to push data to renderer?
+-- YES --> webContents.send() + ipcRenderer.on() (in preload)
Two renderers need to communicate?
+-- YES --> MessagePort (set up via main process)
High-frequency streaming data?
+-- YES --> MessagePort (avoids per-message IPC overhead)
CPU-intensive background work?
+-- YES --> utilityProcess.fork() + parentPort
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**Critical Security Issues:**

- Exposing `ipcRenderer` directly via `contextBridge` instead of wrapping specific channels -- gives renderer full IPC access
- Not validating IPC arguments in main process handlers -- path traversal, injection, privilege escalation
- Using `ipcRenderer.sendSync()` -- blocks the entire renderer process, causes UI freezes
- Accepting arbitrary file paths from renderer without resolving and checking boundaries

**Type Safety Issues:**

- Using string literals for channel names without a shared type map -- typos become runtime bugs
- Defining IPC types separately in main and renderer -- they will drift apart
- Not augmenting `window` type with the preload API -- renderer code has no autocompletion
- Using `any` for IPC payloads -- defeats the purpose of typed IPC

**Architecture Issues:**

- Not cleaning up `ipcRenderer.on` listeners when components unmount -- causes memory leaks and duplicate handlers
- Direct renderer-to-renderer communication without going through main or MessagePort -- not possible in Electron
- Putting business logic in the renderer that should live in main
- Using `child_process.fork()` instead of `utilityProcess.fork()` in Electron apps

**electron-trpc Gotchas:**

- Forgetting `exposeElectronTRPC()` in the preload script -- client silently fails
- Not using a transformer (e.g., SuperJSON) when procedures return `Date`, `Map`, or `Set` -- serialization loses type information
- Subscriptions auto-cancel on window navigation -- resubscribe if the page is a SPA that does not reload
- Custom error classes lose properties during IPC serialization -- use plain error objects or error codes

**MessagePort Gotchas:**

- Ports must be transferred via `postMessage`, not `send` or `invoke` -- the transfer list is a third argument
- Main side must call `port.start()` explicitly -- forgetting this means no messages flow
- `port.close` event fires when the remote end is garbage collected -- handle gracefully
- `SharedArrayBuffer` is NOT reliably supported in Electron across process boundaries due to cross-origin isolation limitations

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST validate and sanitize ALL data received via IPC in the main process -- treat renderer messages as untrusted input)**

**(You MUST use `contextBridge.exposeInMainWorld()` in preload scripts -- never expose `ipcRenderer` directly)**

**(You MUST define IPC channel names and payload types in a single shared file -- never use untyped string literals for channel names)**

**(You MUST use `ipcMain.handle()` / `ipcRenderer.invoke()` for request-response IPC -- `sendSync` blocks the renderer)**

**(You MUST clean up IPC listeners when components unmount or windows close -- listener leaks cause memory issues and duplicate handlers)**

**Failure to follow these rules will create security vulnerabilities, type mismatches across process boundaries, and memory leaks.**

</critical_reminders>
