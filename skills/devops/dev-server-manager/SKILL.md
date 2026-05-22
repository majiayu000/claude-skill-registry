---
name: Dev Server Manager
description: Start, stop, and manage the Vite development server for the Babylon.js game. Use when the user wants to run the dev server, test the game, check if server is running, or troubleshoot server issues.
---

# Dev Server Manager

Manage the Vite development server for testing and development.

## Quick Start

### Start the development server
```bash
cd /home/gianfiorenzo/Documents/vscode/babylon_fp
npm run dev
```

The server will start on `http://localhost:5173` (or next available port).

### Check if server is running
```bash
lsof -i :5173 || echo "Server not running on port 5173"
```

### Stop the server (if running in background)
```bash
pkill -f "vite"
```

## Server Commands

### Start with specific port
```bash
cd /home/gianfiorenzo/Documents/vscode/babylon_fp
npm run dev -- --port 3000
```

### Start with host exposure (accessible on network)
```bash
cd /home/gianfiorenzo/Documents/vscode/babylon_fp
npm run dev -- --host
```

### Preview production build
```bash
cd /home/gianfiorenzo/Documents/vscode/babylon_fp
npm run build
npm run preview
```

## Troubleshooting

### Port already in use
```bash
# Find process using port 5173
lsof -i :5173

# Kill the process
kill -9 <PID>
```

### Clear Vite cache
```bash
cd /home/gianfiorenzo/Documents/vscode/babylon_fp
rm -rf node_modules/.vite
npm run dev
```

### Check for dependency issues
```bash
cd /home/gianfiorenzo/Documents/vscode/babylon_fp
npm install
npm run dev
```

## Testing Workflow

1. **Start server**: `npm run dev`
2. **Open browser**: Navigate to `http://localhost:5173`
3. **Test features**: Check map editor, NPC system, day/night cycle
4. **Watch console**: Browser console shows runtime errors
5. **Hot reload**: Changes auto-reload (no restart needed)

## Server Output Interpretation

- **Local**: http://localhost:5173/ - Server URL
- **Network**: Shows if accessible on local network
- **ready in Xms**: Server startup time
- **HMR update**: Hot module replacement working
- **error**: Check the error message for details