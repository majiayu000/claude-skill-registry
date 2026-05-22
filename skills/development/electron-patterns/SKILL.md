---
name: electron-patterns
description: Electron desktop patterns including IPC, security, auto-update, and native integrations.
agents: [spark]
triggers: [electron, desktop, ipc, native menu, system tray]
---

# Electron Desktop Patterns

Cross-platform desktop development with Electron, covering security, IPC, and native integrations.

## Core Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Framework | Electron 28+ | Desktop apps |
| Build | electron-builder, electron-forge | Packaging |
| Language | TypeScript 5+ (strict) | Type safety |
| UI | React/shadcn/ui | Renderer process |
| Testing | Playwright, Vitest | E2E and unit tests |
| Updates | electron-updater | Auto-update |

## Context7 Library IDs

Query these libraries for current best practices:

- **Electron**: `/electron/electron`
- **electron-builder**: `/electron-userland/electron-builder`
- **Better Auth**: `/better-auth/better-auth`

## Architecture

```
┌─────────────────────────────────────────────────┐
│                 Main Process                     │
│  (Node.js - full system access)                 │
│  - Window management                            │
│  - Native menus, tray, notifications            │
│  - File system, auto-update                     │
│  - IPC handler                                  │
└───────────────────┬─────────────────────────────┘
                    │ IPC (contextBridge)
┌───────────────────▼─────────────────────────────┐
│              Preload Script                      │
│  (Limited Node.js - contextBridge only)         │
│  - Expose safe APIs to renderer                 │
│  - Type-safe IPC channels                       │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│              Renderer Process                    │
│  (Chromium - web context only)                  │
│  - React UI, shadcn/ui components               │
│  - Uses window.api from preload                 │
└─────────────────────────────────────────────────┘
```

## Security Rules

1. **Context isolation always.** Never expose Node.js to renderer
2. **IPC for everything.** Main ↔ Renderer via IPC only
3. **Preload scripts.** Use for secure API exposure
4. **Code sign releases.** Required for macOS/Windows
5. **Auto-update.** Use electron-updater

## Main Process

```typescript
// main.ts
import { app, BrowserWindow, ipcMain, shell } from 'electron';
import path from 'path';

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,  // REQUIRED
      nodeIntegration: false,   // REQUIRED
      sandbox: true,            // RECOMMENDED
    },
  });
  
  // Open external links in browser
  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
  
  win.loadFile('index.html');
}

// IPC handlers
ipcMain.handle('read-file', async (_, filePath: string) => {
  return fs.promises.readFile(filePath, 'utf-8');
});
```

## Preload Script

```typescript
// preload.ts
import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('api', {
  readFile: (path: string) => ipcRenderer.invoke('read-file', path),
  onUpdateAvailable: (callback: () => void) => 
    ipcRenderer.on('update-available', callback),
});
```

## Renderer Usage

```typescript
// Type declaration
declare global {
  interface Window {
    api: {
      readFile: (path: string) => Promise<string>;
      onUpdateAvailable: (callback: () => void) => void;
    };
  }
}

// React component
function App() {
  const loadFile = async () => {
    const content = await window.api.readFile('/path/to/file');
  };
}
```

## Native Menus

```typescript
import { Menu, shell } from 'electron';

const template: Electron.MenuItemConstructorOptions[] = [
  {
    label: 'File',
    submenu: [
      { label: 'New', accelerator: 'CmdOrCtrl+N', click: () => {} },
      { type: 'separator' },
      { role: 'quit' },
    ],
  },
  {
    label: 'Edit',
    submenu: [
      { role: 'undo' },
      { role: 'redo' },
      { type: 'separator' },
      { role: 'cut' },
      { role: 'copy' },
      { role: 'paste' },
    ],
  },
];

Menu.setApplicationMenu(Menu.buildFromTemplate(template));
```

## System Tray

```typescript
import { Tray, Menu, nativeImage } from 'electron';

const tray = new Tray(nativeImage.createFromPath('icon.png'));
tray.setContextMenu(Menu.buildFromTemplate([
  { label: 'Show App', click: () => mainWindow.show() },
  { label: 'Quit', click: () => app.quit() },
]));
```

## Auto-Update

```typescript
import { autoUpdater } from 'electron-updater';

autoUpdater.checkForUpdatesAndNotify();

autoUpdater.on('update-available', () => {
  mainWindow.webContents.send('update-available');
});

autoUpdater.on('update-downloaded', () => {
  autoUpdater.quitAndInstall();
});
```

## electron-builder.yml

```yaml
appId: com.company.myapp
productName: MyApp
directories:
  output: dist
files:
  - "build/**/*"
  - "node_modules/**/*"
mac:
  category: public.app-category.productivity
  hardenedRuntime: true
  gatekeeperAssess: false
  entitlements: "build/entitlements.mac.plist"
  entitlementsInherit: "build/entitlements.mac.plist"
win:
  target: nsis
linux:
  target:
    - AppImage
    - deb
publish:
  provider: github
```

## Hardened Runtime Entitlements

```xml
<!-- entitlements.mac.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
</dict>
</plist>
```

## Validation Commands

```bash
# Type check
npx tsc --noEmit

# Lint
npx eslint .

# Tests
npm test

# Build (without signing)
npm run build

# Package for current platform
npm run package
```

## Guidelines

- Always use context isolation
- Never expose Node.js to renderer
- Use preload scripts for safe API exposure
- Sign releases for distribution
- Implement auto-update for seamless updates
- Handle external links in default browser
- Use native menus for platform conventions
