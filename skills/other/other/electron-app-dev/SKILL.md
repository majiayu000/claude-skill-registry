---
name: electron-app-dev
description: |
  Electron桌面应用开发专家。精通electron-vite、TypeScript、React、IPC通信、窗口管理、原生功能集成等Electron全栈开发技术。

  适用场景：
  - 创建electron-vite + TypeScript + React项目
  - 实现安全的IPC通信
  - 窗口管理（创建、控制、多窗口、状态持久化）
  - 原生功能（系统托盘、菜单、通知、文件对话框）
  - electron-builder打包分发
  - 自动更新和代码签名

  所有代码遵循最新Electron安全最佳实践：contextIsolation开启、nodeIntegration关闭、sandbox模式开启、contextBridge安全暴露IPC。
---

# ⚡ Electron 桌面应用开发专家

老王我搞Electron好多年了，这玩意儿写跨平台应用真tm香！

## 快速开始：创建新项目

使用内置脚本创建最佳实践Electron项目：

```bash
python "C:/Users/Administrator/.claude/skills/electron-app-dev/scripts/create_electron_app.py" my-app
cd my-app
npm install
npm run dev
```

**生成项目包含：**
- electron-vite：全进程极速热更新
- TypeScript + React：类型安全开发
- contextBridge安全IPC模式
- electron-builder打包配置

---

## 核心安全原则（不可妥协）

永远强制执行这些安全配置：

```typescript
webPreferences: {
  preload: path.join(__dirname, '../preload/index.js'),
  contextIsolation: true,    // 必须为true
  nodeIntegration: false,     // 必须为false
  sandbox: true               // 推荐开启
}
```

**为什么重要：**
- `contextIsolation: true` - 隔离preload脚本与渲染器
- `nodeIntegration: false` - 防止渲染器直接访问Node.js
- `sandbox: true` - 进一步限制渲染器进程能力

---

## IPC通信模式

### 唯一正确方式：contextBridge + 白名单

**Preload (preload/index.ts):**
```typescript
const SEND_CHANNELS = ['app-ready']
const INVOKE_CHANNELS = ['get-app-info', 'save-file']

contextBridge.exposeInMainWorld('electronAPI', {
  send: (channel, ...args) => {
    if (SEND_CHANNELS.includes(channel)) {
      ipcRenderer.send(channel, ...args)
    }
  },
  invoke: async (channel, ...args) => {
    if (INVOKE_CHANNELS.includes(channel)) {
      return await ipcRenderer.invoke(channel, ...args)
    }
    return Promise.reject(new Error(`Invalid channel: ${channel}`))
  }
})
```

**Main Process (main/index.ts):**
```typescript
function validateSender(frame: Electron.WebFrameMain | null): boolean {
  if (!frame) return false
  const url = new URL(frame.url)
  const allowedHosts = ['localhost', 'yourdomain.com']
  return allowedHosts.includes(url.hostname) || url.protocol === 'file:'
}

ipcMain.handle('get-app-info', (event) => {
  if (!validateSender(event.senderFrame)) return null
  return { name: app.getName(), version: app.getVersion() }
})
```

---

## 常见坑与解决方案（老王血泪经验）

### 1. 白屏问题（DevTools可以加载但正常不行）

**症状：** 开发环境正常，打包后白屏

**原因：** 协议问题或路径错误

```typescript
// ❌ 错误写法
win.loadURL('http://localhost:5173')

// ✅ 正确写法
if (app.isPackaged) {
  win.loadFile(path.join(__dirname, '../renderer/index.html'))
} else {
  win.loadURL('http://localhost:5173')
}

// ✅ 生产环境加载方案
win.loadFile(path.join(__dirname, '../renderer/index.html'))
win.webContents.openDevTools()  // 先看看能不能加载
```

### 2. 内存泄漏（IPC监听器没移除）

**症状：** 应用用久了越来越卡

```typescript
// ❌ 错误写法
useEffect(() => {
  window.electronAPI.on('update', callback)
  // 没有清理函数！
}, [])

// ✅ 正确写法
useEffect(() => {
  const callback = (data) => console.log(data)
  window.electronAPI.on('update', callback)

  return () => {
    window.electronAPI.removeListener('update', callback)  // 必须移除！
  }
}, [])
```

### 3. 窗口状态不保存（用户每次打开都要重新调整大小）

```typescript
import Store from 'electron-store'

const store = new Store()

const win = new BrowserWindow({
  x: store.get('window.x', undefined),
  y: store.get('window.y', undefined),
  width: store.get('window.width', 1200),
  height: store.get('window.height', 800),
})

// 窗口关闭时保存状态
win.on('close', () => {
  const bounds = win.getBounds()
  store.set('window', {
    x: bounds.x,
    y: bounds.y,
    width: bounds.width,
    height: bounds.height,
  })
})
```

### 4. DevTools在开发环境自动打开，生产环境忘记关

```typescript
const win = new BrowserWindow({
  // ...
  webPreferences: {
    // ...
  }
})

// 只在开发环境打开
if (process.env.NODE_ENV === 'development') {
  win.webContents.openDevTools()
}

// 或者用快捷键
app.on('ready', () => {
  // ...
  globalShortcut.register('CommandOrControl+Shift+I', () => {
    win.webContents.toggleDevTools()
  })
})
```

---

## 性能优化（让应用飞起来）

### 1. 懒加载窗口（别tm一次性创建所有窗口）

```typescript
// ❌ 错误写法：启动时创建所有窗口
const mainWindow = new BrowserWindow({ /* ... */ })
const settingsWindow = new BrowserWindow({ /* ... */ })
const aboutWindow = new BrowserWindow({ /* ... */ })

// ✅ 正确写法：按需创建
let settingsWindow: BrowserWindow | null = null

function openSettings() {
  if (!settingsWindow) {
    settingsWindow = new BrowserWindow({
      width: 600,
      height: 400,
      // ...
    })
    settingsWindow.on('closed', () => {
      settingsWindow = null  // 关闭后释放内存
    })
  }
  settingsWindow.show()
}
```

### 2. BrowserView替代多个窗口（更省内存）

```typescript
// 一个主窗口 + 多个BrowserView
const win = new BrowserWindow({ width: 1200, height: 800 })

const view1 = new BrowserView()
win.setBrowserView(view1)
view1.setBounds({ x: 0, y: 0, width: 600, height: 800 })
view1.webContents.loadURL('https://example.com')

const view2 = new BrowserView()
view2.setBounds({ x: 600, y: 0, width: 600, height: 800 })
view2.webContents.loadURL('https://another.com')
```

### 3. 防抖IPC调用（别疯狂发请求）

```typescript
// Renderer - 使用lodash debounce
import { debounce } from 'lodash'

const debouncedSave = debounce((content) => {
  window.electronAPI.invoke('save-file', content)
}, 500)

// 每次输入都调用，但实际只500ms执行一次
inputElement.addEventListener('input', (e) => {
  debouncedSave(e.target.value)
})
```

### 4. 大文件用流式传输（别tm一次性读进内存）

```typescript
// ❌ 错误写法：一次性读取大文件
ipcMain.handle('read-file', async (event, filePath) => {
  const content = fs.readFileSync(filePath, 'utf-8')  // 可能几百MB
  return content
})

// ✅ 正确写法：流式传输
ipcMain.handle('read-file-stream', async (event, filePath) => {
  const stream = fs.createReadStream(filePath)
  const chunks: Buffer[] = []

  for await (const chunk of stream) {
    chunks.push(chunk)
    event.sender.send('file-chunk', chunk)  // 分批发送
  }

  return Buffer.concat(chunks).toString('utf-8')
})
```

---

## 调试技巧（快速定位问题）

### 1. VS Code调试配置

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Main Process",
      "type": "node",
      "request": "launch",
      "cwd": "${workspaceFolder}",
      "runtimeExecutable": "${workspaceFolder}/node_modules/.bin/electron",
      "windows": {
        "runtimeExecutable": "${workspaceFolder}/node_modules/.bin/electron.cmd"
      },
      "args": ["."],
      "outputCapture": "std"
    },
    {
      "name": "Debug Renderer Process",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/src"
    }
  ]
}
```

### 2. Chrome DevTools快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+Shift+I | 打开/关闭DevTools |
| Ctrl+Shift+J | 打开控制台 |
| Ctrl+Shift+C | 元素选择器 |
| F1 | 打开命令面板 |

### 3. 主进程日志（别光用console.log）

```typescript
import winston from 'winston'

const logger = winston.createLogger({
  transports: [
    new winston.transports.File({ filename: 'main.log' }),
    new winston.transports.Console()
  ]
})

logger.info('Application started')
logger.error('Something went wrong', error)
```

### 4. 内存监控

```typescript
// 定期检查内存使用
setInterval(() => {
  const usage = process.cpuUsage()
  const memory = process.memoryUsage()
  console.log({
    cpu: usage,
    heapUsed: `${Math.round(memory.heapUsed / 1024 / 1024)}MB`,
    heapTotal: `${Math.round(memory.heapTotal / 1024 / 1024)}MB`,
  })
}, 30000)

// 检测内存泄漏
const leaks = []
setInterval(() => {
  const used = process.memoryUsage().heapUsed
  leaks.push(used)
  if (leaks.length > 10) leaks.shift()

  // 如果持续增长，可能有内存泄漏
  const isGrowing = leaks.every((val, i) => i === 0 || val >= leaks[i - 1])
  if (isGrowing && leaks[leaks.length - 1] > leaks[0] * 1.5) {
    console.warn('⚠️ Possible memory leak detected!')
  }
}, 10000)
```

---

## 跨平台注意事项（坑真多）

### 1. 平台特定代码

```typescript
import { platform } from 'os'

if (platform() === 'win32') {
  // Windows专用代码
} else if (platform() === 'darwin') {
  // macOS专用代码
} else if (platform() === 'linux') {
  // Linux专用代码
}
```

### 2. 文件路径处理

```typescript
import { app } from 'electron'
import path from 'path'

// ❌ 错误写法：硬编码分隔符
const filePath = 'C:\\Users\\file.txt'

// ✅ 正确写法：使用path.join
const filePath = path.join(app.getPath('userData'), 'file.txt')

// ✅ 获取用户数据目录（跨平台）
const userDataPath = app.getPath('userData')
// Windows: C:\Users\Username\AppData\Roaming\YourApp
// macOS: ~/Library/Application Support/YourApp
// Linux: ~/.config/YourApp
```

### 3. 原生模块编译

```json
// package.json
{
  "scripts": {
    "postinstall": "electron-rebuild -f -w your-native-module"
  }
}
```

### 4. 托盘图标（不同平台尺寸不同）

```typescript
import { nativeImage, Tray } from 'electron'

let iconPath: string

if (process.platform === 'win32') {
  iconPath = path.join(__dirname, 'icon.ico')  // Windows需要.ico
} else {
  iconPath = path.join(__dirname, 'icon.png')  // Mac/Linux用.png
}

// 或者用@electron/remote动态加载
const tray = new Tray(nativeImage.createFromPath(iconPath))

// Mac需要设置模板图标
if (process.platform === 'darwin') {
  tray.setImage(nativeImage.createFromPath(iconPath))
}
```

---

## 参考文档

| 主题 | 参考文件 |
|------|----------|
| IPC通信模式、安全验证 | [references/ipc-patterns.md](references/ipc-patterns.md) |
| 窗口创建、控制、多窗口、状态持久化 | [references/window-management.md](references/window-management.md) |
| 系统托盘、菜单、通知、文件对话框 | [references/native-features.md](references/native-features.md) |
| electron-builder配置、代码签名、自动更新 | [references/packaging.md](references/packaging.md) |

---

## 常用任务速查

### 创建窗口
```typescript
import { BrowserWindow } from 'electron'
import * as path from 'path'

const win = new BrowserWindow({
  width: 1200,
  height: 800,
  webPreferences: {
    preload: path.join(__dirname, '../preload/index.js'),
    contextIsolation: true,
    nodeIntegration: false,
    sandbox: true
  }
})

if (process.env.NODE_ENV === 'development') {
  win.loadURL('http://localhost:5173')
  win.webContents.openDevTools()
} else {
  win.loadFile(path.join(__dirname, '../renderer/index.html'))
}
```

### 系统托盘
```typescript
import { Tray, Menu, nativeImage } from 'electron'

const tray = new Tray(nativeImage.createFromPath('build/icon.png'))
tray.setContextMenu(Menu.buildFromTemplate([
  { label: 'Show', click: () => win.show() },
  { label: 'Quit', click: () => app.quit() }
]))
```

### 文件对话框
```typescript
import { dialog } from 'electron'

const { canceled, filePaths } = await dialog.showOpenDialog({
  properties: ['openFile'],
  filters: [{ name: 'Images', extensions: ['jpg', 'png'] }]
})
```

---

## 项目结构（electron-vite）

```
my-app/
├── electron/
│   ├── main/
│   │   └── index.ts      # 主进程入口
│   └── preload/
│       ├── index.ts      # Preload脚本
│       └── index.d.ts    # TypeScript类型定义
├── src/
│   ├── main.tsx          # React入口
│   ├── App.tsx
│   └── index.css
├── out/                   # 编译输出
├── electron.vite.config.ts
├── package.json
└── electron-builder.yml
```

---

## 打包分发

```bash
# 开发
npm run dev

# 生产构建
npm run build

# 打包特定平台
npm run build:win    # Windows (NSIS + portable)
npm run build:mac    # macOS (DMG + ZIP)
npm run build:linux  # Linux (AppImage + deb)
```

---

**老王建议：**
- 内存泄漏是头号杀手，IPC监听器必须清理
- 大文件别tm一次性读进内存，用流式传输
- 窗口状态持久化用electron-store，别自己造轮子
- 跨平台测试必须在真机上跑，虚拟机有时候坑
- DevTools快捷键熟记，调试能省一半时间
