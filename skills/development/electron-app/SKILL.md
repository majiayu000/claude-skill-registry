---
name: electron-app
description: Build Electron desktop applications with IPC, window management, and packaging. Use when working on TitanMirror desktop app or any cross-platform desktop applications.
---

# 🖥️ Electron App Skill

## Project Structure

```
📁 electron-app/
   📁 main/
      📄 main.js         ← Main process
      📄 preload.js      ← Bridge script
   📁 renderer/
      📄 index.html
      📄 renderer.js     ← Renderer process
      📄 styles.css
   📄 package.json
```

---

## Main Process

```javascript
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  mainWindow.loadFile('renderer/index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
```

---

## IPC Communication

### Preload (Bridge)
```javascript
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  // Renderer → Main
  sendCommand: (cmd) => ipcRenderer.send('command', cmd),
  
  // Main → Renderer
  onFrame: (callback) => ipcRenderer.on('frame', (_, data) => callback(data)),
  
  // Two-way
  getDeviceInfo: () => ipcRenderer.invoke('get-device-info')
});
```

### Main Process Handlers
```javascript
// One-way
ipcMain.on('command', (event, cmd) => {
  socket.emit('command', cmd);
});

// Two-way (async)
ipcMain.handle('get-device-info', async () => {
  return await fetchDeviceInfo();
});

// Send to renderer
mainWindow.webContents.send('frame', frameData);
```

### Renderer Usage
```javascript
// Send command
window.electronAPI.sendCommand({ type: 'click', x: 100, y: 200 });

// Receive frame
window.electronAPI.onFrame((data) => {
  renderFrame(data);
});

// Get data
const info = await window.electronAPI.getDeviceInfo();
```

---

## Window Controls

```javascript
// Fullscreen
mainWindow.setFullScreen(true);

// Always on top
mainWindow.setAlwaysOnTop(true);

// Resize
mainWindow.setSize(800, 600);

// Get bounds
const { width, height } = mainWindow.getBounds();
```

---

## Packaging

### package.json
```json
{
  "name": "titan-mirror",
  "main": "main/main.js",
  "scripts": {
    "start": "electron .",
    "build": "electron-builder"
  },
  "build": {
    "appId": "com.example.titanmirror",
    "win": {
      "target": "nsis"
    },
    "mac": {
      "target": "dmg"
    }
  }
}
```

### Build Commands
```bash
# Development
npm start

# Production build
npm run build
```

---

## TitanMirror Integration

```javascript
// Socket.IO in main process
const io = require('socket.io')(server);

io.on('connection', (socket) => {
  socket.on('frame', (data) => {
    // Forward to renderer
    mainWindow.webContents.send('frame', data);
  });
});

// Renderer receives
window.electronAPI.onFrame((frameData) => {
  const img = new Image();
  img.onload = () => ctx.drawImage(img, 0, 0);
  img.src = 'data:image/jpeg;base64,' + frameData;
});
```
