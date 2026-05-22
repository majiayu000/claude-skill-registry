---
name: electron
description: >
  Implement Electron desktop app patterns for PhotoVault bulk uploader.
  Use when working with main/renderer process communication, chunked uploads,
  preload scripts, protocol handlers, or auto-updater. Includes security
  patterns and memory management for large file uploads.
---

# ⚠️ MANDATORY WORKFLOW - DO NOT SKIP

**When this skill activates, you MUST follow the expert workflow before writing any code:**

1. **Spawn Domain Expert** using the Task tool with this prompt:
   ```
   Read the expert prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\electron-expert.md

   Then research the codebase and write an implementation plan to: docs/claude/plans/electron-[task-name]-plan.md

   Task: [describe the user's request]
   ```

2. **Spawn QA Critic** after expert returns, using Task tool:
   ```
   Read the QA critic prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\qa-critic-expert.md

   Review the plan at: docs/claude/plans/electron-[task-name]-plan.md
   Write critique to: docs/claude/plans/electron-[task-name]-critique.md
   ```

3. **Present BOTH plan and critique to user** - wait for approval before implementing

**DO NOT read files and start coding. DO NOT rationalize that "this is simple." Follow the workflow.**

---

# Electron Desktop App Integration

## Core Principles

### Main Process vs Renderer Process

The main process runs Node.js. The renderer process runs web content. Never give the renderer direct Node access.

```typescript
// main.ts - Main process
ipcMain.handle('read-file', async (_, path) => {
  return fs.readFile(path)
})

// preload.ts - Bridge
contextBridge.exposeInMainWorld('api', {
  readFile: (path) => ipcRenderer.invoke('read-file', path)
})

// renderer.js - Web content
const content = await window.api.readFile('/path/to/file')
```

### Never Enable Node Integration

It's a massive security hole. Use contextBridge instead.

```typescript
// ✅ CORRECT
new BrowserWindow({
  webPreferences: {
    nodeIntegration: false,
    contextIsolation: true,
    preload: path.join(__dirname, 'preload.js'),
  },
})
```

### Stream Large Files

Never load entire files into memory. Stream them chunk by chunk.

```typescript
// ❌ BAD: 4GB file = 4GB RAM usage
const buffer = await fs.readFile(largePath)

// ✅ GOOD: Stream in chunks
const stream = fs.createReadStream(largePath, { highWaterMark: 6 * 1024 * 1024 })
for await (const chunk of stream) {
  await uploadChunk(chunk)
}
```

## Anti-Patterns

**Enabling nodeIntegration**
```typescript
// WRONG: Any website loaded can access filesystem
new BrowserWindow({
  webPreferences: {
    nodeIntegration: true,  // NEVER DO THIS
  },
})
```

**Exposing sensitive functions to renderer**
```typescript
// WRONG: Renderer can delete anything
contextBridge.exposeInMainWorld('api', {
  deleteFile: (path) => fs.unlink(path),
})

// RIGHT: Validate and restrict
contextBridge.exposeInMainWorld('api', {
  deleteUploadedFile: (fileId) => {
    const safePath = validateAndResolvePath(fileId)
    return fs.unlink(safePath)
  },
})
```

**Sending large data through IPC**
```typescript
// WRONG: IPC has limits, blocks main process
mainWindow.webContents.send('file-data', fileBuffer)  // 500MB buffer!

// RIGHT: Send reference, stream separately
mainWindow.webContents.send('file-ready', { path: largeFile, size })
```

**Not cleaning up resources**
```typescript
// WRONG: File handles leak
const stream = fs.createReadStream(path)
stream.pipe(uploadStream)

// RIGHT: Proper cleanup
const stream = fs.createReadStream(path)
try {
  await pipeline(stream, uploadStream)
} finally {
  stream.destroy()
}
```

## Preload Script (Secure Bridge)

```typescript
// src/preload.ts
import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('photovault', {
  selectFiles: () => ipcRenderer.invoke('select-files'),
  selectFolder: () => ipcRenderer.invoke('select-folder'),
  startUpload: (galleryId: string, files: string[]) =>
    ipcRenderer.invoke('start-upload', galleryId, files),
  cancelUpload: () => ipcRenderer.invoke('cancel-upload'),
  authenticate: () => ipcRenderer.invoke('authenticate'),
  getAuthState: () => ipcRenderer.invoke('get-auth-state'),
  logout: () => ipcRenderer.invoke('logout'),

  onUploadProgress: (callback: (progress: UploadProgress) => void) => {
    const listener = (_: any, progress: UploadProgress) => callback(progress)
    ipcRenderer.on('upload-progress', listener)
    return () => ipcRenderer.removeListener('upload-progress', listener)
  },
})
```

## Chunked Upload Manager

```typescript
// src/upload-manager.ts
import { createReadStream, statSync } from 'fs'
import { EventEmitter } from 'events'

const CHUNK_SIZE = 6 * 1024 * 1024  // 6MB chunks
const MAX_RETRIES = 3

export class UploadManager extends EventEmitter {
  private cancelled = false

  async uploadFile(filePath: string, galleryId: string, hubUrl: string, token: string) {
    const stats = statSync(filePath)
    const totalChunks = Math.ceil(stats.size / CHUNK_SIZE)

    const stream = createReadStream(filePath, { highWaterMark: CHUNK_SIZE })

    let chunkIndex = 0
    for await (const chunk of stream) {
      if (this.cancelled) {
        stream.destroy()
        throw new Error('Upload cancelled')
      }

      await this.uploadChunkWithRetry(chunk, chunkIndex, totalChunks, galleryId, hubUrl, token)
      chunkIndex++

      this.emit('progress', {
        file: filePath,
        progress: Math.round((chunkIndex / totalChunks) * 100),
      })
    }
  }

  cancel() { this.cancelled = true }
}
```

## Protocol Handler for Deep Links

```typescript
// In main.ts
function handleDeepLink(url: URL) {
  // photovault://auth?token=X&userId=Y
  if (url.pathname === '//auth' || url.pathname === '/auth') {
    const token = url.searchParams.get('token')
    const userId = url.searchParams.get('userId')

    if (token && userId) {
      authState = { token, userId, authenticated: true }
      mainWindow?.webContents.send('auth-complete', authState)
      mainWindow?.show()
    }
  }
}

// Register protocol
app.setAsDefaultProtocolClient('photovault')
```

## PhotoVault Desktop Context

### Hub API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/api/v1/upload/prepare` | Create gallery, get upload path |
| `/api/v1/upload/chunk` | Upload individual chunk |
| `/api/v1/upload/process-chunked` | Trigger processing after upload |
| `/auth/desktop-callback` | OAuth callback |

### Auth Flow

1. User clicks "Login" in desktop app
2. App opens browser to `{hubUrl}/auth/desktop-callback?desktop=true`
3. User authenticates in browser
4. Hub redirects to `photovault://auth?token=X&userId=Y`
5. Protocol handler captures, stores auth, notifies renderer

### Build Commands

```bash
npm run dev      # Development
npm run build    # Build for current platform
npm run build:all  # Build for all platforms
```

## Debugging Checklist

1. Is nodeIntegration disabled?
2. Is contextIsolation enabled?
3. Are large files being streamed, not loaded into memory?
4. Are IPC messages small (references, not data)?
5. Is cleanup happening in finally blocks?
6. Is the protocol handler registered?
