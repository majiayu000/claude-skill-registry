---
name: electron-base
description: |
  Build secure desktop applications with Electron 33, Vite, React, and TypeScript. Covers type-safe IPC via contextBridge, OAuth with custom protocol handlers, native module compatibility (better-sqlite3, electron-store), and electron-builder packaging.

  Use when building cross-platform desktop apps, implementing OAuth flows in Electron, handling main/renderer process communication, or packaging with code signing. Prevents: NODE_MODULE_VERSION mismatch, hardcoded encryption keys, context isolation bypasses, sandbox conflicts with native modules.
---

# Electron Base Skill

Build secure, modern desktop applications with Electron 33, Vite, React, and TypeScript.

## Quick Start

### 1. Initialize Project

```bash
# Create Vite project
npm create vite@latest my-app -- --template react-ts
cd my-app

# Install Electron dependencies
npm install electron electron-store
npm install -D vite-plugin-electron vite-plugin-electron-renderer electron-builder
```

### 2. Project Structure

```
my-app/
├── electron/
│   ├── main.ts           # Main process entry
│   ├── preload.ts        # Preload script (contextBridge)
│   └── ipc-handlers/     # Modular IPC handlers
│       ├── auth.ts
│       └── store.ts
├── src/                  # React app (renderer)
├── vite.config.ts        # Dual-entry Vite config
├── electron-builder.json # Build config
└── package.json
```

### 3. Package.json Updates

```json
{
  "main": "dist-electron/main.mjs",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "electron .",
    "package": "electron-builder"
  }
}
```

---

## Architecture Patterns

### Main vs Renderer Process Separation

```
┌─────────────────────────────────────────────────────────────┐
│                     MAIN PROCESS                            │
│  (Node.js + Electron APIs)                                  │
│  - File system access                                       │
│  - Native modules (better-sqlite3)                          │
│  - System dialogs                                           │
│  - Protocol handlers                                        │
└─────────────────────┬───────────────────────────────────────┘
                      │ IPC (invoke/handle)
                      │ Events (send/on)
┌─────────────────────▼───────────────────────────────────────┐
│                   PRELOAD SCRIPT                            │
│  (contextBridge.exposeInMainWorld)                          │
│  - Type-safe API exposed to renderer                        │
│  - No direct ipcRenderer exposure                           │
└─────────────────────┬───────────────────────────────────────┘
                      │ window.electron.*
┌─────────────────────▼───────────────────────────────────────┐
│                  RENDERER PROCESS                           │
│  (Browser context - React app)                              │
│  - No Node.js APIs                                          │
│  - Uses window.electron.* for IPC                           │
└─────────────────────────────────────────────────────────────┘
```

### Type-Safe IPC Pattern

The preload script exposes a typed API to the renderer:

```typescript
// electron/preload.ts
export interface ElectronAPI {
  auth: {
    startOAuth: (provider: 'google' | 'github') => Promise<void>;
    getSession: () => Promise<Session | null>;
    logout: () => Promise<void>;
    onSuccess: (callback: (session: Session) => void) => () => void;
    onError: (callback: (error: string) => void) => () => void;
  };
  app: {
    getVersion: () => Promise<string>;
    openExternal: (url: string) => Promise<void>;
  };
}

// Expose to renderer
contextBridge.exposeInMainWorld('electron', electronAPI);

// Global type declaration
declare global {
  interface Window {
    electron: ElectronAPI;
  }
}
```

---

## Security Best Practices

### REQUIRED: Context Isolation

Always enable context isolation and disable node integration:

```typescript
// electron/main.ts
const mainWindow = new BrowserWindow({
  webPreferences: {
    preload: join(__dirname, 'preload.cjs'),
    contextIsolation: true,    // REQUIRED - isolates preload from renderer
    nodeIntegration: false,    // REQUIRED - no Node.js in renderer
    sandbox: false,            // May need to disable for native modules
  },
});
```

### NEVER: Hardcode Encryption Keys

```typescript
// WRONG - hardcoded key is a security vulnerability
const store = new Store({
  encryptionKey: 'my-secret-key',  // DO NOT DO THIS
});

// CORRECT - derive from machine ID
import { machineIdSync } from 'node-machine-id';

const store = new Store({
  encryptionKey: machineIdSync().slice(0, 32),  // Machine-unique key
});
```

### Sandbox Trade-offs

Native modules like `better-sqlite3` require `sandbox: false`. Document this trade-off:

```typescript
webPreferences: {
  sandbox: false, // Required for better-sqlite3 - document security trade-off
}
```

**Modules requiring sandbox: false:**
- better-sqlite3
- node-pty
- native-keymap

**Modules working with sandbox: true:**
- electron-store (pure JS)
- keytar (uses Electron's safeStorage)

---

## OAuth with Custom Protocol Handlers

### 1. Register Protocol (main.ts)

```typescript
// In development, need to pass executable path
if (process.defaultApp) {
  if (process.argv.length >= 2) {
    app.setAsDefaultProtocolClient('myapp', process.execPath, [process.argv[1]]);
  }
} else {
  app.setAsDefaultProtocolClient('myapp');
}
```

### 2. Handle Protocol URL

```typescript
// Single instance lock (required for reliable protocol handling)
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', (_event, commandLine) => {
    const url = commandLine.find((arg) => arg.startsWith('myapp://'));
    if (url) handleProtocolUrl(url);
    if (mainWindow?.isMinimized()) mainWindow.restore();
    mainWindow?.focus();
  });
}

// macOS handles protocol differently
app.on('open-url', (_event, url) => {
  handleProtocolUrl(url);
});

function handleProtocolUrl(url: string) {
  const parsedUrl = new URL(url);

  if (parsedUrl.pathname.includes('/auth/callback')) {
    const token = parsedUrl.searchParams.get('token');
    const state = parsedUrl.searchParams.get('state');
    const error = parsedUrl.searchParams.get('error');

    if (error) {
      mainWindow?.webContents.send('auth:error', error);
    } else if (token && state) {
      handleAuthCallback(token, state)
        .then((session) => mainWindow?.webContents.send('auth:success', session))
        .catch((err) => mainWindow?.webContents.send('auth:error', err.message));
    }
  }
}
```

### 3. State Validation for CSRF Protection

```typescript
// Start OAuth - generate and store state
ipcMain.handle('auth:start-oauth', async (_event, provider) => {
  const state = crypto.randomUUID();
  store.set('pendingState', state);

  const authUrl = `${BACKEND_URL}/api/auth/signin/${provider}?state=${state}`;
  await shell.openExternal(authUrl);
});

// Verify state on callback
export async function handleAuthCallback(token: string, state: string): Promise<Session> {
  const pendingState = store.get('pendingState');

  if (state !== pendingState) {
    throw new Error('State mismatch - possible CSRF attack');
  }

  store.set('pendingState', null);
  // ... rest of auth flow
}
```

---

## Native Module Compatibility

### better-sqlite3

Requires rebuilding for Electron's Node ABI:

```bash
# Install
npm install better-sqlite3

# Rebuild for Electron
npm install -D electron-rebuild
npx electron-rebuild -f -w better-sqlite3
```

**Vite config - externalize native modules:**

```typescript
// vite.config.ts
electron({
  main: {
    entry: 'electron/main.ts',
    vite: {
      build: {
        rollupOptions: {
          external: ['electron', 'better-sqlite3', 'electron-store'],
        },
      },
    },
  },
});
```

### electron-store

Works with sandbox enabled, but encryption key should be machine-derived:

```typescript
import Store from 'electron-store';
import { machineIdSync } from 'node-machine-id';

interface StoreSchema {
  session: Session | null;
  settings: Settings;
}

const store = new Store<StoreSchema>({
  name: 'myapp-data',
  encryptionKey: machineIdSync().slice(0, 32),
  defaults: {
    session: null,
    settings: { theme: 'system' },
  },
});
```

---

## Build and Packaging

### electron-builder.json

```json
{
  "$schema": "https://raw.githubusercontent.com/electron-userland/electron-builder/master/packages/app-builder-lib/scheme.json",
  "appId": "com.yourcompany.myapp",
  "productName": "MyApp",
  "directories": {
    "output": "release"
  },
  "files": [
    "dist/**/*",
    "dist-electron/**/*"
  ],
  "mac": {
    "category": "public.app-category.productivity",
    "icon": "build/icon.icns",
    "hardenedRuntime": true,
    "gatekeeperAssess": false,
    "entitlements": "build/entitlements.mac.plist",
    "entitlementsInherit": "build/entitlements.mac.plist",
    "target": [
      { "target": "dmg", "arch": ["x64", "arm64"] }
    ],
    "protocols": [
      { "name": "MyApp", "schemes": ["myapp"] }
    ]
  },
  "win": {
    "icon": "build/icon.ico",
    "target": [
      { "target": "nsis", "arch": ["x64"] }
    ]
  },
  "linux": {
    "icon": "build/icons",
    "target": ["AppImage"],
    "category": "Office"
  }
}
```

### macOS Entitlements (build/entitlements.mac.plist)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
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

### Build Commands

```bash
# Development
npm run dev

# Production build
npm run build

# Package for current platform
npm run package

# Package for specific platform
npx electron-builder --mac
npx electron-builder --win
npx electron-builder --linux
```

---

## Known Issues and Prevention

### 1. "Cannot read properties of undefined" in Preload

**Cause:** Accessing window.electron before preload completes.

**Fix:** Use optional chaining or check for existence:

```typescript
// In React component
useEffect(() => {
  if (!window.electron?.auth) return;

  const unsubscribe = window.electron.auth.onSuccess((session) => {
    setSession(session);
  });

  return unsubscribe;
}, []);
```

### 2. NODE_MODULE_VERSION Mismatch

**Cause:** Native module compiled for different Node.js version than Electron uses.

**Fix:**

```bash
# Rebuild native modules for Electron
npx electron-rebuild -f -w better-sqlite3

# Or add to package.json postinstall
"scripts": {
  "postinstall": "electron-rebuild"
}
```

### 3. OAuth State Mismatch

**Cause:** State not persisted or lost between OAuth start and callback.

**Fix:** Use persistent storage (electron-store) not memory:

```typescript
// WRONG - state lost if app restarts
let pendingState: string | null = null;

// CORRECT - persisted storage
const store = new Store({ ... });
store.set('pendingState', state);
```

### 4. Sandbox Conflicts with Native Modules

**Cause:** Sandbox prevents loading native .node files.

**Fix:** Disable sandbox (with documented trade-off) or use pure-JS alternatives:

```typescript
webPreferences: {
  sandbox: false, // Required for better-sqlite3
  // Alternative: Use sql.js (WASM) if sandbox required
}
```

### 5. Dual Auth System Maintenance Burden

**Cause:** Configuring better-auth but using manual OAuth creates confusion.

**Fix:** Choose one approach:
- Use better-auth fully OR
- Use manual OAuth only (remove better-auth)

### 6. Token Expiration Without Refresh

**Cause:** Hardcoded expiration with no refresh mechanism.

**Fix:** Implement token refresh or sliding sessions:

```typescript
// Check expiration with buffer
const session = store.get('session');
const expiresAt = new Date(session.expiresAt);
const bufferMs = 5 * 60 * 1000; // 5 minutes

if (Date.now() > expiresAt.getTime() - bufferMs) {
  await refreshToken(session.token);
}
```

### 7. Empty Catch Blocks Masking Failures

**Cause:** Swallowing errors silently.

**Fix:** Log errors, distinguish error types:

```typescript
// WRONG
try {
  await fetch(url);
} catch {
  // Silent failure - user has no idea what happened
}

// CORRECT
try {
  await fetch(url);
} catch (err) {
  if (err instanceof TypeError) {
    console.error('[Network] Offline or DNS failure:', err.message);
  } else {
    console.error('[Auth] Unexpected error:', err);
  }
  throw err; // Re-throw for caller to handle
}
```

### 8. Hardcoded Encryption Key

**Cause:** Using string literal for encryption.

**Fix:** Derive from machine identifier:

```typescript
import { machineIdSync } from 'node-machine-id';

const store = new Store({
  encryptionKey: machineIdSync().slice(0, 32),
});
```

---

## Vite Configuration

### Full vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import electron from 'vite-plugin-electron/simple';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    electron({
      main: {
        entry: 'electron/main.ts',
        vite: {
          build: {
            outDir: 'dist-electron',
            rollupOptions: {
              external: ['electron', 'better-sqlite3', 'electron-store'],
              output: {
                format: 'es',
                entryFileNames: '[name].mjs',
              },
            },
          },
        },
      },
      preload: {
        input: 'electron/preload.ts',
        vite: {
          build: {
            outDir: 'dist-electron',
            rollupOptions: {
              output: {
                format: 'cjs',
                entryFileNames: '[name].cjs',
              },
            },
          },
        },
      },
      renderer: {},
    }),
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  build: {
    outDir: 'dist',
  },
  optimizeDeps: {
    include: ['react', 'react-dom'],
  },
});
```

---

## Dependencies Reference

### Production Dependencies

```json
{
  "dependencies": {
    "electron-store": "^10.0.0",
    "electron-updater": "^6.3.0"
  },
  "optionalDependencies": {
    "better-sqlite3": "^11.0.0",
    "node-machine-id": "^1.1.12"
  }
}
```

### Development Dependencies

```json
{
  "devDependencies": {
    "electron": "^33.0.0",
    "electron-builder": "^25.0.0",
    "electron-rebuild": "^3.2.9",
    "vite-plugin-electron": "^0.28.0",
    "vite-plugin-electron-renderer": "^0.14.0"
  }
}
```

---

## Security Checklist

Before release, verify:

- [ ] `contextIsolation: true` in webPreferences
- [ ] `nodeIntegration: false` in webPreferences
- [ ] No hardcoded encryption keys
- [ ] OAuth state validation implemented
- [ ] No sensitive data in IPC channel names
- [ ] External links open in system browser (`shell.openExternal`)
- [ ] CSP headers configured for production
- [ ] macOS hardened runtime enabled
- [ ] Code signing configured (if distributing)
- [ ] No empty catch blocks masking errors

---

## Related Skills

- **better-auth** - For backend authentication that pairs with Electron OAuth
- **cloudflare-worker-base** - For building backend APIs
- **tailwind-v4-shadcn** - For styling the renderer UI
