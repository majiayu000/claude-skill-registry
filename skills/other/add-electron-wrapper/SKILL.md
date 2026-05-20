---
description: Add Electron wrapper for NovaTune Player desktop app with secure token storage (project)
---
# Add Electron Wrapper Skill

Package the NovaTune Player as a desktop application using Electron with security hardening and OS keychain integration.

## Overview

This skill adds an Electron wrapper to `apps/player` for:
- Windows, macOS, and Linux desktop builds
- Secure refresh token storage in OS keychain
- Media key integration
- Auto-updates
- Cross-platform packaging

## Project Structure

```
apps/player-electron/
├── package.json
├── electron-builder.yml
├── tsconfig.json
├── src/
│   ├── main/
│   │   ├── index.ts
│   │   ├── preload.ts
│   │   ├── ipc-handlers.ts
│   │   └── secure-storage.ts
│   └── renderer/
│       └── (symlink or copy of apps/player/dist)
└── resources/
    ├── icon.icns      (macOS)
    ├── icon.ico       (Windows)
    └── icon.png       (Linux)
```

## Main Process

### src/main/index.ts

```typescript
import { app, BrowserWindow, ipcMain } from 'electron';
import { join } from 'path';
import { setupIpcHandlers } from './ipc-handlers';

const isDev = process.env.NODE_ENV === 'development';

const createWindow = () => {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webSecurity: true,
    },
    titleBarStyle: 'hiddenInset', // macOS
    frame: true,
    backgroundColor: '#1a1a1a',
  });

  // Content Security Policy
  win.webContents.session.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Content-Security-Policy': [
          "default-src 'self'",
          "script-src 'self'",
          "style-src 'self' 'unsafe-inline'",
          "img-src 'self' data: blob: https:",
          "media-src 'self' blob: https:",
          "connect-src 'self' http://localhost:* https://*.novatune.dev",
        ].join('; '),
      },
    });
  });

  if (isDev) {
    win.loadURL('http://localhost:5173');
    win.webContents.openDevTools();
  } else {
    win.loadFile(join(__dirname, '../renderer/index.html'));
  }

  return win;
};

app.whenReady().then(() => {
  setupIpcHandlers();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
```

## Preload Script

### src/main/preload.ts

```typescript
import { contextBridge, ipcRenderer } from 'electron';

// Expose secure API to renderer
contextBridge.exposeInMainWorld('electronAPI', {
  // Secure storage
  getSecureToken: (): Promise<string | null> =>
    ipcRenderer.invoke('secure-storage:get'),
  setSecureToken: (token: string): Promise<void> =>
    ipcRenderer.invoke('secure-storage:set', token),
  deleteSecureToken: (): Promise<void> =>
    ipcRenderer.invoke('secure-storage:delete'),

  // App info
  getAppVersion: (): Promise<string> =>
    ipcRenderer.invoke('app:version'),

  // Platform
  getPlatform: (): NodeJS.Platform => process.platform,
});

// Type declaration for renderer
declare global {
  interface Window {
    electronAPI: {
      getSecureToken: () => Promise<string | null>;
      setSecureToken: (token: string) => Promise<void>;
      deleteSecureToken: () => Promise<void>;
      getAppVersion: () => Promise<string>;
      getPlatform: () => NodeJS.Platform;
    };
  }
}
```

## Secure Storage

### src/main/secure-storage.ts

```typescript
import keytar from 'keytar';

const SERVICE_NAME = 'NovaTune';
const ACCOUNT_NAME = 'refresh_token';

export const secureStorage = {
  async get(): Promise<string | null> {
    try {
      return await keytar.getPassword(SERVICE_NAME, ACCOUNT_NAME);
    } catch (error) {
      console.error('Failed to get secure token:', error);
      return null;
    }
  },

  async set(token: string): Promise<void> {
    try {
      await keytar.setPassword(SERVICE_NAME, ACCOUNT_NAME, token);
    } catch (error) {
      console.error('Failed to set secure token:', error);
      throw error;
    }
  },

  async delete(): Promise<void> {
    try {
      await keytar.deletePassword(SERVICE_NAME, ACCOUNT_NAME);
    } catch (error) {
      console.error('Failed to delete secure token:', error);
    }
  },
};
```

### src/main/ipc-handlers.ts

```typescript
import { ipcMain, app } from 'electron';
import { secureStorage } from './secure-storage';

export function setupIpcHandlers(): void {
  // Secure storage handlers
  ipcMain.handle('secure-storage:get', async () => {
    return secureStorage.get();
  });

  ipcMain.handle('secure-storage:set', async (_, token: string) => {
    return secureStorage.set(token);
  });

  ipcMain.handle('secure-storage:delete', async () => {
    return secureStorage.delete();
  });

  // App info
  ipcMain.handle('app:version', () => {
    return app.getVersion();
  });
}
```

## Renderer Integration

### packages/core/src/auth/storage.ts

```typescript
// Platform-aware token storage
export interface TokenStorage {
  getRefreshToken(): Promise<string | null>;
  setRefreshToken(token: string): Promise<void>;
  clearRefreshToken(): Promise<void>;
}

// Detect platform and return appropriate storage
export function createTokenStorage(): TokenStorage {
  // Electron
  if (typeof window !== 'undefined' && window.electronAPI) {
    return {
      getRefreshToken: () => window.electronAPI.getSecureToken(),
      setRefreshToken: (token) => window.electronAPI.setSecureToken(token),
      clearRefreshToken: () => window.electronAPI.deleteSecureToken(),
    };
  }

  // Web fallback
  return {
    getRefreshToken: () => Promise.resolve(localStorage.getItem('refresh_token')),
    setRefreshToken: (token) => {
      localStorage.setItem('refresh_token', token);
      return Promise.resolve();
    },
    clearRefreshToken: () => {
      localStorage.removeItem('refresh_token');
      return Promise.resolve();
    },
  };
}
```

## Package Configuration

### package.json

```json
{
  "name": "novatune-player-desktop",
  "version": "1.0.0",
  "description": "NovaTune Music Player for Desktop",
  "main": "dist/main/index.js",
  "scripts": {
    "dev": "concurrently \"pnpm dev:main\" \"pnpm dev:renderer\"",
    "dev:main": "tsc -p tsconfig.main.json -w",
    "dev:renderer": "pnpm --filter player dev",
    "build": "pnpm build:renderer && pnpm build:main && electron-builder",
    "build:main": "tsc -p tsconfig.main.json",
    "build:renderer": "pnpm --filter player build && cp -r ../player/dist dist/renderer",
    "pack": "electron-builder --dir",
    "dist": "electron-builder"
  },
  "dependencies": {
    "keytar": "^7.9.0"
  },
  "devDependencies": {
    "electron": "^31.0.0",
    "electron-builder": "^24.13.0",
    "concurrently": "^8.2.0",
    "typescript": "^5.6.0",
    "@types/node": "^20.14.0"
  },
  "build": {
    "extends": "./electron-builder.yml"
  }
}
```

### electron-builder.yml

```yaml
appId: dev.novatune.player
productName: NovaTune
copyright: Copyright © 2024 NovaTune

directories:
  output: release/${version}
  buildResources: resources

files:
  - dist/**/*
  - package.json

mac:
  category: public.app-category.music
  icon: resources/icon.icns
  hardenedRuntime: true
  gatekeeperAssess: false
  entitlements: resources/entitlements.mac.plist
  entitlementsInherit: resources/entitlements.mac.plist

win:
  icon: resources/icon.ico
  target:
    - nsis
    - portable

linux:
  icon: resources/icon.png
  target:
    - AppImage
    - deb
  category: Audio

nsis:
  oneClick: false
  allowToChangeInstallationDirectory: true
  createDesktopShortcut: true

publish:
  provider: github
  owner: novatune
  repo: player

autoUpdate:
  enabled: true
```

## Security Hardening

### resources/entitlements.mac.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
  <false/>
  <key>com.apple.security.cs.disable-library-validation</key>
  <false/>
  <key>com.apple.security.network.client</key>
  <true/>
  <key>com.apple.security.files.user-selected.read-write</key>
  <true/>
</dict>
</plist>
```

## Development Workflow

```bash
# Development
cd apps/player-electron

# Install dependencies
pnpm install

# Run in development mode
pnpm dev

# Build for current platform
pnpm build

# Build for all platforms
pnpm dist
```

## Implementation Steps

1. **Create project structure**
   ```bash
   mkdir -p apps/player-electron/{src/main,resources}
   ```

2. **Initialize package**
   ```bash
   cd apps/player-electron
   pnpm init
   pnpm add keytar
   pnpm add -D electron electron-builder typescript @types/node concurrently
   ```

3. **Create main process files**
   - `src/main/index.ts`
   - `src/main/preload.ts`
   - `src/main/secure-storage.ts`
   - `src/main/ipc-handlers.ts`

4. **Update packages/core auth storage**
   - Add platform detection
   - Use Electron API when available

5. **Add build configuration**
   - `electron-builder.yml`
   - Platform-specific entitlements

6. **Test security**
   - Verify context isolation
   - Verify sandbox mode
   - Verify CSP headers

## Related Documentation

- **Frontend Plan**: `doc/implementation/frontend/main.md`
- **Section 12**: Desktop (Electron) Packaging

## Related Skills

- **implement-player-app** - Base player app
- **add-capacitor-android** - Mobile packaging

## Claude Agents

- **vue-app-implementer** - Base app implementation
- **electron-wrapper-implementer** - Electron-specific tasks
