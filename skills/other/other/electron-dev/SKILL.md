---
name: electron-dev
description: Electron desktop application development with React, TypeScript, and Vite. Use when building desktop apps, implementing IPC communication, managing windows/tray, handling PTY terminals, integrating WebRTC/audio, or packaging with electron-builder. Covers patterns from AudioBash, Yap, and Pisscord projects.
---

# Electron desktop development

Patterns and practices for building production-quality Electron applications with React and TypeScript.

## Architecture patterns

### Project structure
```
app/
├── electron/
│   ├── main.cjs              # Main process (CommonJS required)
│   ├── preload.cjs           # Context bridge for secure IPC
│   └── server.cjs            # Optional: WebSocket/HTTP server
├── src/
│   ├── components/           # React components
│   ├── services/             # Business logic (API clients, Firebase)
│   ├── utils/                # Utilities (audio, formatting)
│   ├── types.ts              # TypeScript interfaces
│   ├── App.tsx               # Root component
│   └── index.tsx             # React entry
├── assets/                   # Icons, sounds, images
├── package.json
├── vite.config.ts
└── electron-builder.yml      # Build configuration
```

### IPC communication pattern

**Main process (main.cjs):**
```javascript
const { ipcMain } = require('electron');

// Handle async requests from renderer
ipcMain.handle('action-name', async (event, args) => {
  try {
    const result = await someAsyncOperation(args);
    return { success: true, data: result };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Send data to renderer
mainWindow.webContents.send('event-name', data);
```

**Preload script (preload.cjs):**
```javascript
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  actionName: (args) => ipcRenderer.invoke('action-name', args),
  onEventName: (callback) => {
    const handler = (event, data) => callback(data);
    ipcRenderer.on('event-name', handler);
    return () => ipcRenderer.removeListener('event-name', handler);
  }
});
```

**Renderer (React):**
```typescript
const result = await window.electron.actionName(args);

useEffect(() => {
  return window.electron.onEventName((data) => {
    setState(data);
  });
}, []);
```

## System tray integration

```javascript
const { Tray, Menu, nativeImage } = require('electron');

let tray = null;

function createTray() {
  const icon = nativeImage.createFromPath(path.join(__dirname, '../assets/tray-icon.png'));
  tray = new Tray(icon.resize({ width: 16, height: 16 }));

  tray.setToolTip('App Name');
  tray.setContextMenu(Menu.buildFromTemplate([
    { label: 'Show', click: () => mainWindow.show() },
    { label: 'Quit', click: () => app.quit() }
  ]));

  tray.on('click', () => {
    mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
  });
}

// Hide to tray instead of closing
mainWindow.on('close', (event) => {
  if (!app.isQuitting) {
    event.preventDefault();
    mainWindow.hide();
  }
});
```

## Global shortcuts

```javascript
const { globalShortcut } = require('electron');

app.whenReady().then(() => {
  // Register with conflict detection
  const registered = globalShortcut.register('Alt+S', () => {
    mainWindow.webContents.send('shortcut-triggered', 'toggle-recording');
  });

  if (!registered) {
    console.error('Shortcut registration failed - conflict detected');
  }
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});
```

## PTY terminal integration (node-pty)

```javascript
const pty = require('node-pty');

const shell = process.platform === 'win32' ? 'powershell.exe' : process.env.SHELL || '/bin/bash';

const ptyProcess = pty.spawn(shell, [], {
  name: 'xterm-256color',
  cols: 80,
  rows: 24,
  cwd: process.env.HOME,
  env: process.env
});

ptyProcess.onData((data) => {
  mainWindow.webContents.send('terminal-data', { tabId, data });
});

ipcMain.on('terminal-write', (event, { tabId, data }) => {
  ptyProcess.write(data);
});

ipcMain.on('terminal-resize', (event, { tabId, cols, rows }) => {
  ptyProcess.resize(cols, rows);
});
```

## Audio recording workflow

```typescript
// Request microphone access
const stream = await navigator.mediaDevices.getUserMedia({
  audio: {
    echoCancellation: true,
    noiseSuppression: true,
    autoGainControl: true
  }
});

// Record audio
const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
const chunks: Blob[] = [];

mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
mediaRecorder.onstop = async () => {
  const blob = new Blob(chunks, { type: 'audio/webm' });
  const base64 = await blobToBase64(blob);
  // Send to transcription API
};

mediaRecorder.start();
// Later: mediaRecorder.stop();
```

## WebRTC patterns (PeerJS)

```typescript
import Peer from 'peerjs';

const peer = new Peer(userId, {
  host: 'peerjs-server.com',
  port: 443,
  secure: true
});

// Answer incoming calls
peer.on('call', (call) => {
  call.answer(localStream);
  call.on('stream', (remoteStream) => {
    audioElement.srcObject = remoteStream;
  });
});

// Make outgoing calls
const call = peer.call(remoteUserId, localStream);
call.on('stream', (remoteStream) => {
  audioElement.srcObject = remoteStream;
});

// Screen sharing via replaceTrack (no renegotiation)
const screenStream = await navigator.mediaDevices.getDisplayMedia({ video: true });
const videoTrack = screenStream.getVideoTracks()[0];
const sender = peerConnection.getSenders().find(s => s.track?.kind === 'video');
await sender.replaceTrack(videoTrack);
```

## Build configuration (electron-builder.yml)

```yaml
appId: com.yourname.appname
productName: AppName
directories:
  output: release

win:
  target:
    - target: nsis
      arch: [x64]
  icon: assets/icon.ico

nsis:
  oneClick: false
  allowToChangeInstallationDirectory: true
  installerIcon: assets/icon.ico
  uninstallerIcon: assets/icon.ico

mac:
  target:
    - target: dmg
      arch: [x64, arm64]
  icon: assets/icon.icns

linux:
  target:
    - target: AppImage
      arch: [x64]
  icon: assets/icon.png

publish:
  provider: github
  owner: username
  repo: repo-name

extraResources:
  - from: "node_modules/node-pty/build/Release/"
    to: "node-pty/"
    filter: ["*.node"]
```

## Common pitfalls

**Stale closures in callbacks:**
```typescript
// Problem: State is stale in async callbacks
const [state, setState] = useState(initialValue);
peer.on('call', () => {
  console.log(state); // Always shows initialValue
});

// Solution: Use refs for async callback access
const stateRef = useRef(state);
useEffect(() => { stateRef.current = state; }, [state]);
peer.on('call', () => {
  console.log(stateRef.current); // Current value
});
```

**Context isolation security:**
- Never expose `ipcRenderer` directly to renderer
- Always use `contextBridge.exposeInMainWorld()`
- Validate all IPC arguments in main process
- Use TypeScript interfaces for IPC contracts

**Cross-platform shell detection:**
```javascript
const shell = process.platform === 'win32'
  ? 'powershell.exe'
  : process.env.SHELL || '/bin/bash';

const shellArgs = process.platform === 'win32'
  ? ['-NoLogo']
  : [];
```

## Development workflow

```bash
# Development (hot reload)
npm run electron:dev

# Production build
npm run electron:build

# Run built app locally
npx electron dist/

# Package for distribution
npm run package
```
