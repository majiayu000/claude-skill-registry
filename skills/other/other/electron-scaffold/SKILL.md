---
name: electron-scaffold
description: Scaffold a native-looking, effective Electron app with best practices baked in. Creates a production-ready Electron application with security hardening, modern tooling, proper IPC patterns, auto-updates, native UI elements, and optimal build configuration. Use this skill when users want to start a new Electron project or modernize an existing one.
---

# Electron Application Scaffolding

Create production-ready Electron applications with security, performance, and native platform integration best practices built in from the start.

## When to Use This Skill

Use this skill when:
- User wants to create a new Electron desktop application from scratch
- User needs to scaffold an Electron project with modern best practices
- User wants a native-looking cross-platform desktop app
- User mentions "Electron app", "desktop app", "cross-platform app", or similar
- User wants to modernize an existing Electron project structure

**DO NOT use this skill for:**
- Modifying the existing TRAE_Extractor-app project (use specific maintenance skills instead)
- Adding features to an already-scaffolded Electron application
- Debugging or fixing issues in an existing Electron app

## Prerequisites Check

Before scaffolding, verify:

1. **Node.js**: Check Node.js version (18.x or higher recommended)
   ```bash
   node --version
   ```

2. **npm or yarn**: Verify package manager is available
   ```bash
   npm --version
   ```

3. **Git**: Ensure git is available for version control
   ```bash
   git --version
   ```

## Architecture Decision Points

### 1. Build Tooling Choice

Ask the user which build system they prefer (or recommend based on use case):

**Electron Forge** (Recommended for most projects)
- All-in-one tooling solution
- Built-in TypeScript support
- Easy plugin system
- Great for: Most new projects, teams wanting batteries-included setup

**Electron Builder**
- Highly configurable
- Excellent multi-platform packaging
- Auto-update support
- Great for: Complex build requirements, specific packaging needs

**Vite + Electron**
- Fastest development experience
- Modern ESM-first approach
- Hot module replacement
- Great for: Modern web frameworks (React, Vue, Svelte), speed-focused development

### 2. Frontend Framework

Determine the UI framework:
- **Vanilla JS/TypeScript**: Lightest, full control
- **React**: Most popular, large ecosystem
- **Vue**: Progressive, easy to learn
- **Svelte**: Smallest bundle, compile-time framework
- **Angular**: Enterprise-ready, opinionated

### 3. TypeScript vs JavaScript

**Strongly recommend TypeScript** for:
- Better IDE support and autocomplete
- Catch errors at compile time
- Better maintainability
- Electron API typing support

## Workflow

### Step 1: Project Initialization

Based on tooling choice, initialize the project:

**For Electron Forge (Recommended):**
```bash
npm init electron-app@latest <app-name> -- --template=webpack-typescript
```

**For Vite + Electron:**
```bash
npm create @quick-start/electron <app-name>
```

**For custom setup:**
Create package.json with proper dependencies (see templates).

### Step 2: Project Structure Setup

Create a well-organized project structure:

```
<app-name>/
├── src/
│   ├── main/              # Main process
│   │   ├── main.ts        # Entry point
│   │   ├── ipc/           # IPC handlers
│   │   ├── menu.ts        # Native menu
│   │   └── tray.ts        # System tray (if needed)
│   ├── preload/           # Preload scripts
│   │   └── preload.ts     # Context bridge
│   ├── renderer/          # Renderer process
│   │   ├── index.html
│   │   ├── index.ts
│   │   └── styles/
│   └── shared/            # Shared types/utilities
│       └── types.ts
├── assets/                # Icons, images
├── resources/             # Build resources
├── dist/                  # Build output
├── package.json
├── tsconfig.json
└── electron-builder.yml   # or forge.config.js
```

### Step 3: Security Configuration

**CRITICAL**: Implement security best practices from the start.

**1. BrowserWindow Security Options:**
```typescript
const mainWindow = new BrowserWindow({
  width: 1200,
  height: 800,
  webPreferences: {
    // Security: Use preload scripts instead of nodeIntegration
    nodeIntegration: false,
    // Security: Isolate context between web content and preload
    contextIsolation: true,
    // Security: Disable remote module
    enableRemoteModule: false,
    // Security: Use sandboxed renderer
    sandbox: true,
    // Preload script for safe IPC
    preload: path.join(__dirname, 'preload.js'),
    // Security: Disable web security only in development if needed
    webSecurity: true,
    // Security: Disable navigation
    allowRunningInsecureContent: false,
  },
});
```

**2. Content Security Policy (CSP):**
```typescript
// In main process or HTML meta tag
session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
  callback({
    responseHeaders: {
      ...details.responseHeaders,
      'Content-Security-Policy': [
        "default-src 'self'",
        "script-src 'self'",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data: https:",
        "connect-src 'self'",
      ].join('; '),
    },
  });
});
```

**3. Context Bridge (preload.ts):**
```typescript
import { contextBridge, ipcRenderer } from 'electron';

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Invoke pattern (request-response)
  getAppVersion: () => ipcRenderer.invoke('app:get-version'),

  // Send pattern (one-way)
  logMessage: (message: string) => ipcRenderer.send('log:message', message),

  // Listener pattern (for receiving events)
  onUpdateAvailable: (callback: (info: any) => void) => {
    ipcRenderer.on('update:available', (_event, info) => callback(info));
  },

  // Remove listener
  removeUpdateListener: () => {
    ipcRenderer.removeAllListeners('update:available');
  },
});
```

**4. IPC Security Pattern:**
```typescript
// main/ipc/handlers.ts
import { ipcMain } from 'electron';

// Use invoke/handle pattern for request-response
ipcMain.handle('app:get-version', async () => {
  return app.getVersion();
});

// Validate and sanitize all inputs
ipcMain.handle('file:read', async (_event, filePath: string) => {
  // Validate path is within allowed directories
  const allowedDir = app.getPath('userData');
  const resolvedPath = path.resolve(filePath);

  if (!resolvedPath.startsWith(allowedDir)) {
    throw new Error('Access denied');
  }

  return fs.readFile(resolvedPath, 'utf-8');
});
```

### Step 4: Native UI Elements

Create native-looking UI components:

**1. Application Menu:**
```typescript
// main/menu.ts
import { Menu, shell } from 'electron';

export function createApplicationMenu(mainWindow: BrowserWindow) {
  const template: MenuItemConstructorOptions[] = [
    {
      label: 'File',
      submenu: [
        {
          label: 'New',
          accelerator: 'CmdOrCtrl+N',
          click: () => mainWindow.webContents.send('file:new'),
        },
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
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' },
      ],
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'Learn More',
          click: async () => {
            await shell.openExternal('https://electronjs.org');
          },
        },
      ],
    },
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}
```

**2. System Tray (Optional):**
```typescript
// main/tray.ts
import { Tray, Menu, nativeImage } from 'electron';

export function createTray(mainWindow: BrowserWindow) {
  const icon = nativeImage.createFromPath(
    path.join(__dirname, '../assets/tray-icon.png')
  );

  const tray = new Tray(icon);

  const contextMenu = Menu.buildFromTemplate([
    {
      label: 'Show App',
      click: () => {
        mainWindow.show();
      },
    },
    {
      label: 'Quit',
      click: () => {
        app.quit();
      },
    },
  ]);

  tray.setContextMenu(contextMenu);
  tray.setToolTip('My Electron App');

  return tray;
}
```

### Step 5: Development Environment Setup

**1. Hot Reload Configuration:**
```typescript
// main.ts
const isDevelopment = process.env.NODE_ENV === 'development';

if (isDevelopment) {
  mainWindow.loadURL('http://localhost:5173'); // Vite dev server
  mainWindow.webContents.openDevTools();
} else {
  mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
}
```

**2. Package.json Scripts:**
```json
{
  "scripts": {
    "dev": "concurrently \"npm:dev:*\"",
    "dev:vite": "vite",
    "dev:electron": "electron .",
    "build": "npm run build:renderer && npm run build:main",
    "build:renderer": "vite build",
    "build:main": "tsc -p tsconfig.main.json",
    "package": "electron-builder",
    "package:all": "electron-builder -mwl",
    "lint": "eslint src --ext .ts,.tsx",
    "typecheck": "tsc --noEmit"
  }
}
```

### Step 6: Auto-Update Configuration

Implement automatic updates using electron-updater:

**1. Install Dependencies:**
```bash
npm install electron-updater
```

**2. Update Configuration:**
```typescript
// main/updater.ts
import { autoUpdater } from 'electron-updater';

export function setupAutoUpdater(mainWindow: BrowserWindow) {
  // Configure update server
  autoUpdater.setFeedURL({
    provider: 'github',
    owner: 'your-username',
    repo: 'your-repo',
  });

  // Check for updates on startup
  autoUpdater.checkForUpdatesAndNotify();

  // Update events
  autoUpdater.on('update-available', (info) => {
    mainWindow.webContents.send('update:available', info);
  });

  autoUpdater.on('update-downloaded', (info) => {
    mainWindow.webContents.send('update:downloaded', info);
  });

  autoUpdater.on('error', (err) => {
    mainWindow.webContents.send('update:error', err);
  });
}
```

**3. electron-builder Configuration:**
```yaml
# electron-builder.yml
appId: com.yourcompany.yourapp
productName: YourApp
directories:
  output: dist
  buildResources: resources
files:
  - src/**/*
  - package.json
mac:
  category: public.app-category.productivity
  target:
    - dmg
    - zip
  hardenedRuntime: true
  gatekeeperAssess: false
  entitlements: resources/entitlements.mac.plist
win:
  target:
    - nsis
    - portable
  publisherName: Your Company
linux:
  target:
    - AppImage
    - deb
  category: Utility
publish:
  provider: github
  owner: your-username
  repo: your-repo
```

### Step 7: TypeScript Configuration

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020", "DOM"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "types": ["node", "electron"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Step 8: Build and Package

**Development:**
```bash
npm run dev
```

**Production Build:**
```bash
npm run build
npm run package
```

**Multi-platform Build:**
```bash
npm run package:all
```

## Best Practices Checklist

When scaffolding, ensure these are implemented:

### Security
- [ ] Context isolation enabled
- [ ] Node integration disabled in renderer
- [ ] Preload script with context bridge
- [ ] Content Security Policy configured
- [ ] Input validation on all IPC handlers
- [ ] Sandbox mode enabled
- [ ] Web security enabled
- [ ] Navigation and redirect guards

### Performance
- [ ] Lazy loading for renderer modules
- [ ] Background throttling configured
- [ ] Memory management for large datasets
- [ ] Efficient IPC patterns (batch updates)
- [ ] Webpack/Vite optimization

### User Experience
- [ ] Native application menu
- [ ] Keyboard shortcuts (accelerators)
- [ ] Window state persistence
- [ ] Proper icon set (all sizes)
- [ ] Splash screen (optional)
- [ ] Error boundaries
- [ ] Loading states

### Developer Experience
- [ ] TypeScript configured
- [ ] Hot reload working
- [ ] DevTools available in development
- [ ] ESLint and Prettier setup
- [ ] Git hooks with Husky (optional)
- [ ] Source maps enabled

### Distribution
- [ ] Auto-update configured
- [ ] Code signing setup (platform-specific)
- [ ] Build scripts for all platforms
- [ ] Proper app metadata
- [ ] License file included

## Error Handling Patterns

### Main Process Errors
```typescript
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  // Log to file or error tracking service
  app.quit();
});

process.on('unhandledRejection', (reason) => {
  console.error('Unhandled Rejection:', reason);
});
```

### Renderer Process Errors
```typescript
window.addEventListener('error', (event) => {
  window.electronAPI.logError({
    message: event.error.message,
    stack: event.error.stack,
  });
});

window.addEventListener('unhandledrejection', (event) => {
  window.electronAPI.logError({
    message: 'Unhandled Promise Rejection',
    reason: event.reason,
  });
});
```

## Platform-Specific Considerations

### macOS
- Use `.icns` icon format
- Implement dock menu
- Handle `activate` event (reopen window)
- Consider macOS-specific menu items (About, Preferences)
- Code signing required for distribution

### Windows
- Use `.ico` icon format
- Handle Squirrel startup events
- Consider Windows toast notifications
- NSIS installer customization
- Code signing with certificate

### Linux
- Use `.png` icon format
- Provide `.desktop` file
- Handle different package formats (deb, AppImage, snap)
- Test on multiple distributions

## Example Scaffolds

### Minimal TypeScript Setup
```bash
# Initialize with Forge
npm init electron-app@latest my-app -- --template=webpack-typescript

# Add security defaults
# Add IPC patterns
# Configure build
```

### React + TypeScript + Vite
```bash
# Create with Vite template
npm create @quick-start/electron my-app -- --template react-ts

# Add security hardening
# Configure auto-update
# Add native menus
```

### Production-Ready Full Setup
- Complete security configuration
- Auto-update with GitHub releases
- Native UI elements (menu, tray)
- Error tracking
- Analytics (optional)
- Crash reporting
- Multi-platform build pipeline

## Tips for Success

1. **Start Secure**: Don't add security later—build it in from day one
2. **Type Everything**: Use TypeScript for both main and renderer processes
3. **Test IPC Early**: IPC issues are easier to debug early
4. **Platform Test**: Test on all target platforms regularly
5. **Monitor Bundle Size**: Keep renderer bundle optimized
6. **Document IPC Contract**: Maintain API documentation between processes
7. **Version Control**: Git ignore `dist/`, `node_modules/`, `.env`
8. **Use Process Manager**: Handle main process crashes gracefully
9. **Implement Logging**: Structured logging helps debug production issues
10. **Plan Updates**: Design update strategy before first release

## Common Pitfalls to Avoid

- ❌ Enabling `nodeIntegration` without good reason
- ❌ Skipping context isolation
- ❌ Loading remote content without validation
- ❌ Exposing entire IPC renderer to web content
- ❌ Ignoring security warnings in console
- ❌ Not testing on all target platforms
- ❌ Hardcoding file paths (use `app.getPath()`)
- ❌ Forgetting to handle window state persistence
- ❌ Not implementing proper error boundaries
- ❌ Skipping code signing for distribution

## Quick Start Command

For most users, recommend this command:

```bash
# Create app with TypeScript and Webpack
npm init electron-app@latest <app-name> -- --template=webpack-typescript

# Then apply security hardening, native UI, and build configuration
```

## Reference Files

For detailed Electron API examples and configuration templates, see:
- `references/electron-security.md` - Security best practices
- `references/ipc-patterns.md` - IPC communication patterns
- `references/build-config.md` - Build and packaging configuration
- `scripts/scaffold.sh` - Automated scaffolding script

## Post-Scaffold Checklist

After scaffolding, guide the user to:

1. ✅ Review and customize `package.json` metadata
2. ✅ Add application icons (all platforms)
3. ✅ Configure code signing certificates
4. ✅ Set up GitHub repository for auto-updates
5. ✅ Test hot reload and development workflow
6. ✅ Build for all target platforms
7. ✅ Test update mechanism
8. ✅ Review security settings
9. ✅ Add error tracking (Sentry, etc.)
10. ✅ Create user documentation

## Version Compatibility

This skill targets:
- **Electron**: v28+ (latest stable)
- **Node.js**: v18+ LTS
- **TypeScript**: v5+
- **Electron Forge**: v7+
- **Electron Builder**: v24+

Always check the latest Electron documentation for breaking changes.
