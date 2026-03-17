---
name: electron-desktop
description: Desktop application development with Electron for Windows, macOS, and Linux. Use when building cross-platform desktop apps, implementing native OS features, or packaging web apps for desktop.
---

# Electron Desktop Development

Build cross-platform desktop applications using web technologies.

## Platforms Supported

| Platform | Architecture               | Notes              |
| -------- | -------------------------- | ------------------ |
| Windows  | x64, arm64, ia32           | Windows 10+        |
| macOS    | x64, arm64 (Apple Silicon) | macOS 10.15+       |
| Linux    | x64, arm64, armv7l         | Most distributions |

---

## Project Structure

```
my-app/
├── src/
│   ├── main/
│   │   ├── main.ts          # Main process
│   │   ├── preload.ts       # Preload scripts
│   │   └── ipc.ts           # IPC handlers
│   ├── renderer/
│   │   ├── index.html
│   │   ├── App.tsx
│   │   └── components/
│   └── shared/
│       └── types.ts
├── resources/
│   ├── icon.icns            # macOS
│   ├── icon.ico             # Windows
│   └── icon.png             # Linux
├── electron-builder.yml
├── package.json
└── forge.config.ts
```

---

## Main Process

### Entry Point

```typescript
// src/main/main.ts
import { app, BrowserWindow, ipcMain } from "electron";
import path from "path";

let mainWindow: BrowserWindow | null = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
    titleBarStyle: "hiddenInset", // macOS
    frame: process.platform === "darwin", // Windows/Linux custom frame
    show: false, // Show when ready
  });

  // Load the app
  if (process.env.NODE_ENV === "development") {
    mainWindow.loadURL("http://localhost:5173");
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, "../renderer/index.html"));
  }

  // Show when ready to prevent flash
  mainWindow.once("ready-to-show", () => {
    mainWindow?.show();
  });

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
```

### Preload Script (Security Bridge)

```typescript
// src/main/preload.ts
import { contextBridge, ipcRenderer } from "electron";

// Expose safe APIs to renderer
contextBridge.exposeInMainWorld("electronAPI", {
  // File operations
  openFile: () => ipcRenderer.invoke("dialog:openFile"),
  saveFile: (content: string) => ipcRenderer.invoke("dialog:saveFile", content),

  // App info
  getVersion: () => ipcRenderer.invoke("app:getVersion"),

  // Window controls
  minimize: () => ipcRenderer.send("window:minimize"),
  maximize: () => ipcRenderer.send("window:maximize"),
  close: () => ipcRenderer.send("window:close"),

  // Two-way communication
  onUpdateAvailable: (callback: () => void) => {
    ipcRenderer.on("update:available", callback);
    return () => ipcRenderer.removeListener("update:available", callback);
  },
});

// Type definitions for renderer
declare global {
  interface Window {
    electronAPI: {
      openFile: () => Promise<string | null>;
      saveFile: (content: string) => Promise<boolean>;
      getVersion: () => Promise<string>;
      minimize: () => void;
      maximize: () => void;
      close: () => void;
      onUpdateAvailable: (callback: () => void) => () => void;
    };
  }
}
```

### IPC Handlers

```typescript
// src/main/ipc.ts
import { ipcMain, dialog, BrowserWindow } from "electron";
import fs from "fs/promises";

export function setupIPC() {
  // File dialogs
  ipcMain.handle("dialog:openFile", async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      properties: ["openFile"],
      filters: [
        { name: "Text Files", extensions: ["txt", "md"] },
        { name: "All Files", extensions: ["*"] },
      ],
    });

    if (canceled || filePaths.length === 0) return null;
    return fs.readFile(filePaths[0], "utf-8");
  });

  ipcMain.handle("dialog:saveFile", async (_, content: string) => {
    const { canceled, filePath } = await dialog.showSaveDialog({
      filters: [{ name: "Text Files", extensions: ["txt"] }],
    });

    if (canceled || !filePath) return false;
    await fs.writeFile(filePath, content);
    return true;
  });

  // Window controls
  ipcMain.on("window:minimize", (event) => {
    BrowserWindow.fromWebContents(event.sender)?.minimize();
  });

  ipcMain.on("window:maximize", (event) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    if (win?.isMaximized()) {
      win.unmaximize();
    } else {
      win?.maximize();
    }
  });

  ipcMain.on("window:close", (event) => {
    BrowserWindow.fromWebContents(event.sender)?.close();
  });
}
```

---

## Renderer Process (React)

### Using Exposed APIs

```tsx
// src/renderer/App.tsx
import { useState, useEffect } from "react";

function App() {
  const [version, setVersion] = useState("");
  const [content, setContent] = useState("");

  useEffect(() => {
    window.electronAPI.getVersion().then(setVersion);

    const unsubscribe = window.electronAPI.onUpdateAvailable(() => {
      alert("Update available!");
    });

    return unsubscribe;
  }, []);

  const handleOpen = async () => {
    const fileContent = await window.electronAPI.openFile();
    if (fileContent) {
      setContent(fileContent);
    }
  };

  const handleSave = async () => {
    await window.electronAPI.saveFile(content);
  };

  return (
    <div className="app">
      <header className="titlebar">
        <span>My App v{version}</span>
        <div className="window-controls">
          <button onClick={window.electronAPI.minimize}>−</button>
          <button onClick={window.electronAPI.maximize}>□</button>
          <button onClick={window.electronAPI.close}>×</button>
        </div>
      </header>

      <main>
        <button onClick={handleOpen}>Open File</button>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <button onClick={handleSave}>Save File</button>
      </main>
    </div>
  );
}
```

### Custom Title Bar CSS

```css
.titlebar {
  -webkit-app-region: drag; /* Make draggable */
  height: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  background: #1e1e1e;
  color: white;
}

.window-controls {
  -webkit-app-region: no-drag; /* Buttons clickable */
  display: flex;
  gap: 8px;
}

.window-controls button {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: white;
  cursor: pointer;
}

.window-controls button:hover {
  background: rgba(255, 255, 255, 0.1);
}
```

---

## Native Features

### System Tray

```typescript
import { Tray, Menu, nativeImage } from "electron";

let tray: Tray | null = null;

function createTray() {
  const icon = nativeImage.createFromPath("resources/tray-icon.png");
  tray = new Tray(icon.resize({ width: 16, height: 16 }));

  const contextMenu = Menu.buildFromTemplate([
    { label: "Show App", click: () => mainWindow?.show() },
    { type: "separator" },
    { label: "Quit", click: () => app.quit() },
  ]);

  tray.setToolTip("My App");
  tray.setContextMenu(contextMenu);

  tray.on("click", () => {
    mainWindow?.show();
  });
}
```

### Native Menus

```typescript
import { Menu } from "electron";

const template: Electron.MenuItemConstructorOptions[] = [
  {
    label: "File",
    submenu: [
      {
        label: "Open",
        accelerator: "CmdOrCtrl+O",
        click: () => {
          /* handle */
        },
      },
      {
        label: "Save",
        accelerator: "CmdOrCtrl+S",
        click: () => {
          /* handle */
        },
      },
      { type: "separator" },
      { role: "quit" },
    ],
  },
  {
    label: "Edit",
    submenu: [
      { role: "undo" },
      { role: "redo" },
      { type: "separator" },
      { role: "cut" },
      { role: "copy" },
      { role: "paste" },
    ],
  },
];

Menu.setApplicationMenu(Menu.buildFromTemplate(template));
```

### Notifications

```typescript
import { Notification } from "electron";

new Notification({
  title: "Update Available",
  body: "A new version is ready to install.",
  icon: "resources/icon.png",
}).show();
```

### Auto Updates

```typescript
import { autoUpdater } from "electron-updater";

autoUpdater.checkForUpdatesAndNotify();

autoUpdater.on("update-available", () => {
  mainWindow?.webContents.send("update:available");
});

autoUpdater.on("update-downloaded", () => {
  autoUpdater.quitAndInstall();
});
```

---

## Building & Distribution

### electron-builder Configuration

```yaml
# electron-builder.yml
appId: com.mycompany.myapp
productName: My App
copyright: Copyright © 2025

directories:
  output: dist
  buildResources: resources

files:
  - dist/**/*
  - package.json

mac:
  category: public.app-category.developer-tools
  target:
    - target: dmg
      arch: [x64, arm64]
    - target: zip
      arch: [x64, arm64]
  hardenedRuntime: true
  gatekeeperAssess: false
  entitlements: build/entitlements.mac.plist
  notarize: true

win:
  target:
    - target: nsis
      arch: [x64]
  sign: true

linux:
  target:
    - target: AppImage
    - target: deb
    - target: rpm
  category: Development

publish:
  provider: github
  releaseType: release
```

### Build Commands

```bash
# Development
npm run dev

# Build for current platform
npm run build

# Build for all platforms
npm run build:all

# Build for specific platform
npm run build:mac
npm run build:win
npm run build:linux
```

---

## Security Best Practices

### DO:

- Always use `contextIsolation: true`
- Use preload scripts for IPC
- Validate all IPC inputs
- Enable `sandbox: true`
- Sign and notarize for distribution

### DON'T:

- Enable `nodeIntegration`
- Use `remote` module
- Load untrusted content
- Expose full Node.js APIs
- Skip code signing

---

## Alternatives to Consider

| Framework      | Best For                       |
| -------------- | ------------------------------ |
| **Tauri**      | Smaller bundle, Rust backend   |
| **Neutralino** | Lightweight, system webview    |
| **Electron**   | Full Node.js, mature ecosystem |
